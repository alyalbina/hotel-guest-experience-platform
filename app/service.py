"""Transactional domain logic shared by bot and staff API; no external network."""

import re
import uuid
from datetime import datetime, timezone

from app.catalog import CATEGORIES, ROOMS

TRANSITIONS = {
    "new": {"acknowledged", "cancelled"},
    "acknowledged": {"in_progress", "resolved", "cancelled"},
    "in_progress": {"resolved", "cancelled"},
    "resolved": {"reopened"},
    "reopened": {"in_progress", "resolved", "cancelled"},
    "cancelled": set(),
}


def utcnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class DomainError(Exception):
    def __init__(self, message, status=400):
        self.message = message
        self.status = status
        super().__init__(message)


def clean(value, minimum=1, maximum=1000):
    if not isinstance(value, str):
        raise DomainError("Text is required")
    value = value.strip()
    if not minimum <= len(value) <= maximum or any(ord(c) < 32 and c not in "\n\t" for c in value):
        raise DomainError(f"Text must contain {minimum}-{maximum} printable characters")
    return value


def validate_profile(field, value):
    value = clean(value, maximum=100)
    if field == "birthday":
        try:
            date = datetime.strptime(value, "%Y-%m-%d").date()
            if date > datetime.now(timezone.utc).date() or date.year < 1900:
                raise ValueError
        except ValueError:
            raise DomainError("Use a valid date in YYYY-MM-DD format") from None
    elif field == "gender" and value not in {"Female", "Male", "Prefer not to say"}:
        raise DomainError("Choose one of the listed options")
    elif field == "email" and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
        raise DomainError("Use a valid email address")
    elif field == "phone" and not re.fullmatch(r"\+?[0-9 ()-]{7,25}", value):
        raise DomainError("Use a valid phone number")
    return value


JOINED = """SELECT r.*, g.name AS guest_name, g.room_id AS room,
 d.name AS department_name, c.name AS category_name, s.name AS assignee_name
 FROM requests r JOIN guests g ON g.id=r.guest_id
 JOIN departments d ON d.id=r.department_id JOIN categories c ON c.id=r.category_id
 LEFT JOIN staff s ON s.id=r.assigned_to"""


class Service:
    def __init__(self, db):
        self.db = db

    def register_guest(self, telegram_id, room, name, **profile):
        if room not in ROOMS:
            raise DomainError("Select an available demo room")
        name = clean(name, maximum=80)
        extra = {
            f: validate_profile(f, profile[f]) if profile.get(f) else None
            for f in ("birthday", "gender", "email", "phone")
        }
        with self.db.connect() as c:
            c.execute("BEGIN IMMEDIATE")
            old = c.execute("SELECT id FROM guests WHERE telegram_id=?", (telegram_id,)).fetchone()
            if old:
                return old["id"]
            return c.execute(
                "INSERT INTO guests(telegram_id,room_id,name,birthday,gender,email,phone,created_at) VALUES (?,?,?,?,?,?,?,?)",
                (telegram_id, room, name, *extra.values(), utcnow()),
            ).lastrowid

    def guest_for_telegram(self, telegram_id):
        with self.db.connect() as c:
            r = c.execute("SELECT id,name,room_id FROM guests WHERE telegram_id=?", (telegram_id,)).fetchone()
            return dict(r) if r else None

    def create_request(self, guest_id, category, service, detail, source_ref=None):
        detail = clean(detail, maximum=1000)
        cat = next((x for x in CATEGORIES if x[0] == category), None)
        if not cat or service not in cat[3]:
            raise DomainError("Invalid category or service")
        now, request_id = utcnow(), uuid.uuid4().hex[:12]
        with self.db.connect() as c:
            c.execute("BEGIN IMMEDIATE")
            if source_ref:
                old = c.execute(
                    "SELECT id,guest_id FROM requests WHERE source_ref=?", (source_ref,)
                ).fetchone()
                if old:
                    if old["guest_id"] != guest_id:
                        raise DomainError("Conflicting source reference", 409)
                    return old["id"]
            if not c.execute("SELECT id FROM guests WHERE id=?", (guest_id,)).fetchone():
                raise DomainError("Guest not found", 404)
            sla = c.execute("SELECT sla_minutes FROM departments WHERE id=?", (cat[2],)).fetchone()[0]
            c.execute(
                """INSERT INTO requests(id,guest_id,category_id,department_id,service,detail,status,created_at,sla_minutes,source_ref)
                VALUES (?,?,?,?,?,?,'new',?,?,?)""",
                (request_id, guest_id, category, cat[2], service, detail, now, sla, source_ref),
            )
            c.execute(
                "INSERT INTO request_events(request_id,action,to_status,occurred_at) VALUES (?,'created','new',?)",
                (request_id, now),
            )
        return request_id

    @staticmethod
    def authorize(staff, request, write=False):
        if write and staff["role"] == "analyst":
            raise DomainError("Analyst accounts are read-only", 403)
        if staff["role"] == "agent" and staff["department_id"] != request["department_id"]:
            raise DomainError("This request belongs to another department", 403)

    def list_requests(self, staff, status=None, department=None, search="", start=None, end=None):
        clauses, args = [], []
        if staff["role"] == "agent":
            clauses.append("r.department_id=?")
            args.append(staff["department_id"])
        for field, value in (("r.status", status), ("r.department_id", department)):
            if value:
                clauses.append(field + "=?")
                args.append(value)
        if search:
            clauses.append("(r.service LIKE ? OR g.room_id LIKE ? OR r.id LIKE ?)")
            args.extend(["%" + search + "%"] * 3)
        if start:
            clauses.append("r.created_at>=?")
            args.append(start + "T00:00:00Z")
        if end:
            clauses.append("r.created_at<=?")
            args.append(end + "T23:59:59Z")
        query = (
            JOINED
            + (" WHERE " + " AND ".join(clauses) if clauses else "")
            + " ORDER BY r.created_at DESC, r.id"
        )
        with self.db.connect() as c:
            return [dict(x) for x in c.execute(query, args)]

    def detail(self, request_id, staff):
        with self.db.connect() as c:
            row = c.execute(JOINED + " WHERE r.id=?", (request_id,)).fetchone()
            if not row:
                raise DomainError("Request not found", 404)
            self.authorize(staff, row)
            result = dict(row)
            result["events"] = [
                dict(x)
                for x in c.execute(
                    """SELECT e.*,s.name AS actor_name FROM request_events e
                LEFT JOIN staff s ON s.id=e.actor_id WHERE request_id=? ORDER BY occurred_at,e.id""",
                    (request_id,),
                )
            ]
            return result

    def mutate(self, request_id, staff, version, status=None, assigned_to=None, note="", assign=False):
        note = clean(note, minimum=0, maximum=500)
        with self.db.connect() as c:
            c.execute("BEGIN IMMEDIATE")
            row = c.execute("SELECT * FROM requests WHERE id=?", (request_id,)).fetchone()
            if not row:
                raise DomainError("Request not found", 404)
            self.authorize(staff, row, write=True)
            if version != row["version"]:
                raise DomainError("Request changed. Refresh and try again.", 409)
            now = utcnow()
            if status:
                if status not in TRANSITIONS[row["status"]]:
                    raise DomainError("Invalid status transition", 409)
                if status in {"cancelled", "reopened"} and not note:
                    raise DomainError("A reason is required for cancellation or reopening")
                responded = row["responded_at"] or (now if status not in {"cancelled"} else None)
                resolved = now if status == "resolved" else None
                first_resolved = row["first_resolved_at"] or resolved
                c.execute(
                    """UPDATE requests SET status=?,responded_at=?,resolved_at=?,first_resolved_at=?,
                    reopen_count=reopen_count+?,csat=CASE WHEN ?='reopened' THEN NULL ELSE csat END,
                    version=version+1 WHERE id=?""",
                    (
                        status,
                        responded,
                        resolved,
                        first_resolved,
                        int(status == "reopened"),
                        status,
                        request_id,
                    ),
                )
                c.execute(
                    """INSERT INTO request_events(request_id,actor_id,action,from_status,to_status,note,occurred_at)
                    VALUES (?,?,'status_changed',?,?,?,?)""",
                    (request_id, staff["id"], row["status"], status, note, now),
                )
            elif assign:
                if assigned_to is not None:
                    target = c.execute("SELECT * FROM staff WHERE id=?", (assigned_to,)).fetchone()
                    if (
                        not target
                        or target["role"] == "analyst"
                        or (target["role"] == "agent" and target["department_id"] != row["department_id"])
                    ):
                        raise DomainError("Choose a manager or employee in the request department")
                c.execute(
                    "UPDATE requests SET assigned_to=?,version=version+1 WHERE id=?",
                    (assigned_to, request_id),
                )
                c.execute(
                    """INSERT INTO request_events(request_id,actor_id,action,note,occurred_at)
                    VALUES (?,?,'assigned',?,?)""",
                    (
                        request_id,
                        staff["id"],
                        f"Employee ID: {assigned_to if assigned_to is not None else 'unassigned'}",
                        now,
                    ),
                )
            else:
                if not note:
                    raise DomainError("Add a note or select an action")
                c.execute("UPDATE requests SET version=version+1 WHERE id=?", (request_id,))
                c.execute(
                    "INSERT INTO request_events(request_id,actor_id,action,note,occurred_at) VALUES (?,?,'note',?,?)",
                    (request_id, staff["id"], note, now),
                )
        return self.detail(request_id, staff)

    def guest_requests(self, guest_id):
        with self.db.connect() as c:
            return [
                dict(x)
                for x in c.execute(
                    "SELECT id,service,status FROM requests WHERE guest_id=? ORDER BY created_at DESC LIMIT 20",
                    (guest_id,),
                )
            ]

    def rate(self, request_id, guest_id, score):
        if type(score) is not int or score not in range(1, 6):
            raise DomainError("Rating must be an integer from 1 to 5")
        with self.db.connect() as c:
            row = c.execute("SELECT guest_id,status,csat FROM requests WHERE id=?", (request_id,)).fetchone()
            if not row or row["guest_id"] != guest_id:
                raise DomainError("Request not found", 404)
            if row["status"] != "resolved":
                raise DomainError("Rate a resolved request", 409)
            if row["csat"] is not None:
                raise DomainError("This request has already been rated", 409)
            c.execute("UPDATE requests SET csat=?,version=version+1 WHERE id=?", (score, request_id))
            c.execute(
                "INSERT INTO request_events(request_id,action,note,occurred_at) VALUES (?,'rated',?,?)",
                (request_id, f"Score: {score}/5", utcnow()),
            )
