import json
import sys

from app.cli import main


def test_public_demo_regenerates_in_isolation(domain, monkeypatch, tmp_path):
    db, svc, guest = domain
    rid = svc.create_request(guest, "amenities", "Extra towels", "PRIVATE_CONTENT_MUST_NOT_EXPORT")
    monkeypatch.setenv("DATABASE_PATH", str(db.path))
    monkeypatch.setenv("DEMO_MODE", "true")
    monkeypatch.chdir(tmp_path)
    (tmp_path / "app/static").mkdir(parents=True)
    monkeypatch.setattr(sys, "argv", ["cli", "export-demo"])
    main()
    exported = (tmp_path / "app/static/demo-data.js").read_text()
    assert "PRIVATE_CONTENT_MUST_NOT_EXPORT" not in exported
    assert "Fictional Guest" not in exported
    payload = json.loads(exported.removeprefix("window.HOTEL_DEMO = ").rstrip(";\n"))
    assert len(payload["requests"]) == 96
    assert all(r["source_ref"].startswith("synthetic:") for r in payload["requests"])
    with db.connect() as c:
        assert (
            c.execute("SELECT detail FROM requests WHERE id=?", (rid,)).fetchone()[0]
            == "PRIVATE_CONTENT_MUST_NOT_EXPORT"
        )
