import sqlite3
from concurrent.futures import ThreadPoolExecutor

import pytest

from app.service import DomainError, validate_profile


def create(domain, detail="Two towels please", source_ref=None):
    _, svc, guest = domain
    return svc.create_request(guest, "amenities", "Extra towels", detail, source_ref)


def test_registration_idempotent_and_minimal(domain):
    db, svc, guest = domain
    assert svc.register_guest(123456, "R101", "Fictional Guest") == guest
    with db.connect() as c:
        row = c.execute("SELECT * FROM guests").fetchone()
        assert row["birthday"] is None and row["email"] is None
    with pytest.raises(DomainError):
        svc.register_guest(44, "R999", "X")


@pytest.mark.parametrize(
    "field,value",
    [
        ("birthday", "2028-10-10"),
        ("birthday", "2000-02-30"),
        ("email", "bad"),
        ("phone", "x"),
        ("gender", "invalid"),
    ],
)
def test_legacy_profile_validation(field, value):
    with pytest.raises(DomainError):
        validate_profile(field, value)


def test_profile_valid_and_oversized_content(domain):
    assert validate_profile("birthday", "2000-01-01") == "2000-01-01"
    assert validate_profile("email", "demo@example.invalid") == "demo@example.invalid"
    with pytest.raises(DomainError):
        create(domain, "x" * 1001)
    with pytest.raises(DomainError):
        create(domain, "\x00")


def test_invalid_service_or_missing_guest_rolls_back(domain):
    db, svc, guest = domain
    with pytest.raises(DomainError):
        svc.create_request(guest, "amenities", "Plumbing", "Invalid")
    with pytest.raises(DomainError):
        svc.create_request(999, "amenities", "Extra towels", "Missing")
    with db.connect() as c:
        assert c.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == 0
        assert c.execute("PRAGMA foreign_key_check").fetchall() == []
        with pytest.raises(sqlite3.IntegrityError):
            c.execute("INSERT INTO guests(name,room_id,created_at) VALUES ('Test','missing','2026-01-01')")


def test_parameterized_content_and_search(domain, manager):
    rid = create(domain, "Robert'); DROP TABLE guests; --")
    _, svc, _ = domain
    assert svc.detail(rid, manager)["detail"].startswith("Robert")
    assert svc.list_requests(manager, search="' OR 1=1 --") == []


def test_concurrent_duplicate_submission_creates_one_event(domain):
    with ThreadPoolExecutor(max_workers=4) as executor:
        ids = list(executor.map(lambda _: create(domain, source_ref="tg:123:5"), range(4)))
    assert len(set(ids)) == 1
    db, svc, _ = domain
    with db.connect() as c:
        assert c.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == 1
        assert c.execute("SELECT COUNT(*) FROM request_events").fetchone()[0] == 1
    other = svc.register_guest(111, "R101", "Other Demo Guest")
    with pytest.raises(DomainError):
        svc.create_request(other, "amenities", "Extra towels", "Other", "tg:123:5")


def test_concurrent_registration_creates_one_guest(domain):
    db, svc, _ = domain
    with ThreadPoolExecutor(max_workers=4) as executor:
        ids = list(executor.map(lambda _: svc.register_guest(888888, "R102", "New Demo Guest"), range(4)))
    assert len(set(ids)) == 1
    with db.connect() as c:
        assert c.execute("SELECT COUNT(*) FROM guests WHERE telegram_id=888888").fetchone()[0] == 1


def test_status_history_timestamps_reopen_and_rating(domain, manager, monkeypatch):
    _, svc, guest = domain
    monkeypatch.setattr("app.service.utcnow", lambda: "2026-10-08T10:00:00Z")
    rid = create(domain)
    monkeypatch.setattr("app.service.utcnow", lambda: "2026-10-08T10:05:00Z")
    r = svc.mutate(rid, manager, 1, status="acknowledged")
    assert r["responded_at"] == "2026-10-08T10:05:00Z"
    r = svc.mutate(rid, manager, 2, status="in_progress")
    monkeypatch.setattr("app.service.utcnow", lambda: "2026-10-08T10:30:00Z")
    r = svc.mutate(rid, manager, 3, status="resolved")
    svc.rate(rid, guest, 5)
    with pytest.raises(DomainError):
        svc.rate(rid, guest, 4)
    r = svc.detail(rid, manager)
    monkeypatch.setattr("app.service.utcnow", lambda: "2026-10-08T10:40:00Z")
    r = svc.mutate(rid, manager, r["version"], status="reopened", note="Towels not delivered")
    assert r["resolved_at"] is None and r["reopen_count"] == 1
    assert r["csat"] is None
    assert r["first_resolved_at"] == "2026-10-08T10:30:00Z"
    assert r["responded_at"] == "2026-10-08T10:05:00Z"
    assert len(r["events"]) == 6


def test_rbac_assignment_and_conflict(domain, manager):
    db, svc, _ = domain
    rid = create(domain)
    hk = {"id": 2, "role": "agent", "department_id": "housekeeping"}
    eng = {"id": 3, "role": "agent", "department_id": "engineering"}
    analyst = {"id": 4, "role": "analyst", "department_id": None}
    assert svc.detail(rid, hk)["id"] == rid
    assert svc.list_requests(eng) == []
    for staff in [eng, analyst]:
        with pytest.raises(DomainError) as error:
            svc.mutate(rid, staff, 1, status="acknowledged")
        assert error.value.status == 403
    for assignee in [3, 4, 999]:
        with pytest.raises(DomainError):
            svc.mutate(rid, manager, 1, assigned_to=assignee, assign=True)
    r = svc.mutate(rid, manager, 1, assigned_to=2, assign=True)
    assert r["assigned_to"] == 2 and r["responded_at"] is None
    with pytest.raises(DomainError) as error:
        svc.mutate(rid, manager, 1, status="acknowledged")
    assert error.value.status == 409
    with pytest.raises(DomainError):
        svc.mutate(rid, manager, 2, status="resolved")
    with pytest.raises(DomainError):
        svc.mutate(rid, manager, 2, status="cancelled")
    with db.connect() as c:
        assert c.execute("SELECT COUNT(*) FROM request_events").fetchone()[0] == 2


def test_csat_ownership_status_and_integer(domain, manager):
    _, svc, guest = domain
    rid = create(domain)
    for score in [0, 6, True, 1.5]:
        with pytest.raises(DomainError):
            svc.rate(rid, guest, score)
    with pytest.raises(DomainError):
        svc.rate(rid, guest + 1, 5)
    with pytest.raises(DomainError):
        svc.rate(rid, guest, 5)


def test_concurrent_staff_updates_allow_only_one(domain, manager):
    _, svc, _ = domain
    rid = create(domain)

    def update(_):
        try:
            svc.mutate(rid, manager, 1, status="acknowledged")
            return "saved"
        except DomainError as error:
            return error.status

    with ThreadPoolExecutor(max_workers=2) as e:
        results = list(e.map(update, range(2)))
    assert sorted(map(str, results)) == ["409", "saved"]
