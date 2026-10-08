import pytest

from app.db import Database
from app.security import hash_password
from app.service import Service


@pytest.fixture
def domain(tmp_path):
    db = Database(tmp_path / "test.sqlite")
    db.initialize()
    with db.connect() as c:
        c.executemany(
            "INSERT INTO staff(id,username,name,role,department_id,password_hash) VALUES (?,?,?,?,?,?)",
            [
                (1, "manager", "Manager", "manager", None, hash_password("test-password")),
                (2, "hk", "Housekeeping Agent", "agent", "housekeeping", hash_password("test-password")),
                (3, "eng", "Engineering Agent", "agent", "engineering", hash_password("test-password")),
                (4, "analyst", "Analyst", "analyst", None, hash_password("test-password")),
            ],
        )
    svc = Service(db)
    guest = svc.register_guest(123456, "R101", "Fictional Guest")
    return db, svc, guest


@pytest.fixture
def manager():
    return {"id": 1, "role": "manager", "department_id": None}
