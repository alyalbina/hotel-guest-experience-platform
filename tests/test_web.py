from fastapi.testclient import TestClient

from app.config import Settings
from app.security import token_hash
from app.web import create_app


def login(client, name="demo"):
    r = client.post("/api/login", json={"username": name, "password": "PortfolioDemo2026!"})
    assert r.status_code == 200
    return {"X-CSRF-Token": r.json()["csrf"]}


def test_api_login_csrf_workflow_and_logout(tmp_path):
    app = create_app(Settings(database=tmp_path / "demo.sqlite"))
    with TestClient(app) as c:
        assert c.get("/api/requests").status_code == 401
        headers = login(c)
        token = c.cookies.get("hotel_session")
        with app.state.db.connect() as conn:
            assert conn.execute("SELECT token_hash FROM sessions").fetchone()[0] == token_hash(token)
            assert token not in str(conn.execute("SELECT * FROM sessions").fetchone())
        rows = c.get("/api/requests").json()
        assert len(rows) == 96
        r = next(x for x in rows if x["status"] == "new")
        body = {"version": r["version"], "status": "acknowledged"}
        assert c.patch("/api/requests/" + r["id"], json=body).status_code == 403
        update = c.patch("/api/requests/" + r["id"], json=body, headers=headers)
        assert update.status_code == 200 and update.json()["status"] == "acknowledged"
        assert c.patch("/api/requests/" + r["id"], json=body, headers=headers).status_code == 409
        assert c.get("/api/metrics?start=not-a-date").status_code == 422
        assert c.get("/api/requests?start=2026-10-09&end=2026-10-08").status_code == 422
        assert c.get("/").status_code == 200
        assert c.get("/static/app.js").status_code == 200
        assert "default-src" in c.get("/").headers["content-security-policy"]
        assert c.post("/api/logout", headers=headers).status_code == 200
        assert c.get("/api/me").status_code == 401


def test_department_access_and_read_only_analyst(tmp_path):
    app = create_app(Settings(database=tmp_path / "demo.sqlite"))
    with TestClient(app) as c:
        headers = login(c, "housekeeping-agent")
        rows = c.get("/api/requests").json()
        assert rows and all(r["department_id"] == "housekeeping" for r in rows)
        assert c.get("/api/requests?department=engineering").json() == []
        with app.state.db.connect() as conn:
            rid = conn.execute(
                "SELECT id FROM requests WHERE department_id='engineering' LIMIT 1"
            ).fetchone()[0]
        assert c.get("/api/requests/" + rid).status_code == 403
        c.post("/api/logout", headers=headers)
        headers = login(c, "analyst")
        row = c.get("/api/requests").json()[0]
        assert (
            c.patch(
                "/api/requests/" + row["id"],
                json={"version": row["version"], "note": "Edit"},
                headers=headers,
            ).status_code
            == 403
        )
        assert (
            c.post(
                "/api/requests",
                json={"guest_id": 1, "category": "amenities", "service": "Extra towels", "detail": "Please"},
                headers=headers,
            ).status_code
            == 403
        )


def test_manager_create_and_login_throttling(tmp_path):
    app = create_app(Settings(database=tmp_path / "demo.sqlite"))
    with TestClient(app) as c:
        headers = login(c)
        r = c.post(
            "/api/requests",
            json={"guest_id": 1, "category": "amenities", "service": "Extra towels", "detail": "Fictional"},
            headers=headers,
        )
        assert r.status_code == 201 and r.json()["status"] == "new"
        for _ in range(9):
            assert c.post("/api/login", json={"username": "unknown", "password": "wrong"}).status_code == 401
        assert (
            c.post("/api/login", json={"username": "demo", "password": "PortfolioDemo2026!"}).status_code
            == 429
        )


def test_production_has_no_demo_credentials_or_seed(tmp_path):
    app = create_app(Settings(database=tmp_path / "prod.sqlite", demo=False))
    with TestClient(app) as c:
        config = c.get("/api/config").json()
        assert config["demo_password"] is None and config["demo_username"] is None
        assert (
            c.post("/api/login", json={"username": "demo", "password": "PortfolioDemo2026!"}).status_code
            == 401
        )
        with app.state.db.connect() as conn:
            assert conn.execute("SELECT COUNT(*) FROM guests").fetchone()[0] == 0
