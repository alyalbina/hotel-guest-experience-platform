"""Deterministic fictional operations. Never imports thesis respondent data."""

import random
from datetime import datetime, timedelta, timezone

from app.catalog import CATEGORIES, DEPARTMENTS, ROOMS
from app.security import hash_password

DEMO_PASSWORD = "PortfolioDemo2026!"
ANCHOR = datetime(2026, 10, 8, 18, 0, tzinfo=timezone.utc)


def stamp(value):
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def seed_demo(db):
    rng = random.Random(2024)
    with db.connect() as c:
        c.execute("BEGIN IMMEDIATE")
        if c.execute("SELECT COUNT(*) FROM requests").fetchone()[0]:
            return False
        if (
            c.execute("SELECT COUNT(*) FROM staff").fetchone()[0]
            or c.execute("SELECT COUNT(*) FROM guests").fetchone()[0]
        ):
            raise RuntimeError("Refusing to add demo users to an existing non-demo database")
        password = hash_password(DEMO_PASSWORD)
        staff = [
            (1, "demo", "Demo Manager", "manager", None, password),
            (2, "analyst", "Demo Analyst", "analyst", None, password),
        ]
        staff += [
            (i + 3, f"{d[0]}-agent", f"Demo {d[1]} Agent", "agent", d[0], password)
            for i, d in enumerate(DEPARTMENTS)
        ]
        c.executemany("INSERT INTO staff VALUES (?,?,?,?,?,?)", staff)
        for i in range(1, 13):
            c.execute(
                "INSERT INTO guests(id,telegram_id,name,room_id,created_at) VALUES (?,?,?,?,?)",
                (
                    i,
                    -1000 - i,
                    f"Demo Guest {i:02d}",
                    ROOMS[(i - 1) % len(ROOMS)],
                    stamp(ANCHOR - timedelta(days=15)),
                ),
            )
        for i in range(96):
            cat = CATEGORIES[i % len(CATEGORIES)]
            department_index = next(j for j, d in enumerate(DEPARTMENTS) if d[0] == cat[2])
            sla = DEPARTMENTS[department_index][2]
            created = ANCHOR - timedelta(hours=i * 3 + 1, minutes=rng.randrange(40))
            status = (
                "new"
                if i < 4
                else rng.choices(["resolved", "in_progress", "acknowledged", "cancelled"], [65, 20, 10, 5])[0]
            )
            reopened = int(i % 13 == 0 and status in {"resolved", "in_progress"})
            if reopened and status == "in_progress":
                status = "reopened"
            response = (
                created + timedelta(minutes=rng.randrange(3, 22))
                if status not in {"new", "cancelled"}
                else None
            )
            resolution = (
                created + timedelta(minutes=rng.randrange(30, 180) + reopened * 120)
                if status == "resolved"
                else None
            )
            first = created + timedelta(minutes=28) if reopened else resolution
            csat = rng.choice([2, 3, 4, 4, 5, 5]) if status == "resolved" and i % 3 != 0 else None
            assigned = department_index + 3 if status != "new" else None
            rid = f"demo-{1001 + i}"
            detail = (
                f"Synthetic request: {cat[3][i % len(cat[3])].lower()}. Please confirm the service timing."
            )
            if i == 0:
                detail = "Could we have two extra towels before 19:00? This is a fictional demo request."
                cat = CATEGORIES[1]
                department_index = 0
                sla = 60
            c.execute(
                """INSERT INTO requests(id,guest_id,category_id,department_id,service,detail,status,assigned_to,
                      created_at,responded_at,first_resolved_at,resolved_at,sla_minutes,reopen_count,csat,source_ref)
                      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    rid,
                    (i % 12) + 1,
                    cat[0],
                    cat[2],
                    cat[3][i % len(cat[3])],
                    detail,
                    status,
                    assigned,
                    stamp(created),
                    stamp(response) if response else None,
                    stamp(first) if first else None,
                    stamp(resolution) if resolution else None,
                    sla,
                    reopened,
                    csat,
                    f"synthetic:{i}",
                ),
            )
            events = [(None, "created", None, "new", "Synthetic dataset", created)]
            if assigned:
                events.append(
                    (1, "assigned", None, None, f"Employee ID: {assigned}", created + timedelta(minutes=1))
                )
            if response:
                events.append(
                    (assigned, "status_changed", "new", "acknowledged", "Request acknowledged", response)
                )
                if status != "acknowledged":
                    events.append(
                        (
                            assigned,
                            "status_changed",
                            "acknowledged",
                            "in_progress",
                            "Service started",
                            response + timedelta(minutes=2),
                        )
                    )
            if reopened:
                events.extend(
                    [
                        (
                            assigned,
                            "status_changed",
                            "in_progress",
                            "resolved",
                            "Initial service completed",
                            first,
                        ),
                        (
                            1,
                            "status_changed",
                            "resolved",
                            "reopened",
                            "Follow-up needed (synthetic)",
                            first + timedelta(minutes=5),
                        ),
                    ]
                )
                if status == "resolved":
                    events.append(
                        (
                            assigned,
                            "status_changed",
                            "reopened",
                            "in_progress",
                            "Follow-up started",
                            first + timedelta(minutes=8),
                        )
                    )
            if resolution:
                events.append(
                    (assigned, "status_changed", "in_progress", "resolved", "Service completed", resolution)
                )
            if status == "cancelled":
                events.append(
                    (
                        1,
                        "status_changed",
                        "new",
                        "cancelled",
                        "Guest withdrew request (synthetic)",
                        created + timedelta(minutes=10),
                    )
                )
            if csat:
                events.append(
                    (None, "rated", None, None, f"Score: {csat}/5", resolution + timedelta(minutes=5))
                )
            c.executemany(
                """INSERT INTO request_events(request_id,actor_id,action,from_status,to_status,note,occurred_at)
                           VALUES (?,?,?,?,?,?,?)""",
                [(rid, a, act, old, new, note, stamp(t)) for a, act, old, new, note, t in events],
            )
    return True
