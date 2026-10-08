"""Developer entry points. Secrets are entered through hidden prompts."""

import argparse
import getpass
import json
import tempfile
from pathlib import Path

from app.analytics import compute_metrics
from app.config import Settings
from app.db import Database
from app.security import hash_password
from app.seed import seed_demo
from app.service import Service


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["init", "seed", "staff", "export-demo", "sheets"])
    parser.add_argument("--username")
    parser.add_argument("--name")
    parser.add_argument("--role", choices=["manager", "agent", "analyst"], default="manager")
    parser.add_argument("--department")
    args = parser.parse_args()
    settings = Settings.from_env()
    db = Database(settings.database)
    db.initialize()
    if args.command == "seed":
        if not settings.demo:
            parser.error("Demo seeding requires DEMO_MODE=true")
        print("Demo seeded" if seed_demo(db) else "Existing dataset preserved")
    elif args.command == "staff":
        if not args.username or not args.name or (args.role == "agent" and not args.department):
            parser.error("Provide --username and --name; agents also require --department")
        password = getpass.getpass("New staff password (12+ characters): ")
        if len(password) < 12:
            parser.error("Password must contain at least 12 characters")
        with db.connect() as c:
            c.execute(
                "INSERT INTO staff(username,name,role,department_id,password_hash) VALUES (?,?,?,?,?)",
                (args.username, args.name, args.role, args.department, hash_password(password)),
            )
        print("Staff account created")
    elif args.command == "export-demo":
        if not settings.demo:
            parser.error("Export-demo only operates in demo mode")
        # Never read operational records for a public demo export.
        with tempfile.TemporaryDirectory() as temporary:
            demo_db = Database(Path(temporary) / "synthetic.sqlite")
            demo_db.initialize()
            seed_demo(demo_db)
            with demo_db.connect() as c:
                staff = [dict(x) for x in c.execute("SELECT id,name,role,department_id FROM staff")]
            svc = Service(demo_db)
            manager = {"id": 1, "role": "manager", "department_id": None}
            rows = svc.list_requests(manager)
            dataset = {
                "label": "SYNTHETIC DEMO DATA",
                "requests": [svc.detail(r["id"], manager) for r in rows],
                "metrics": compute_metrics(rows, now="2026-10-08T18:00:00Z"),
                "staff": staff,
            }
        destination = Path("app/static/demo-data.js")
        destination.write_text("window.HOTEL_DEMO = " + json.dumps(dataset, ensure_ascii=True) + ";\n")
        print(f"Generated {len(rows)} synthetic requests in isolation; no operational records exported")
    elif args.command == "sheets":
        from app.sheets import export_snapshot

        try:
            print(f"Exported {export_snapshot(db, settings)} operational rows")
        except Exception as error:
            raise SystemExit(
                f"Export failed ({type(error).__name__}). Local requests are preserved. Check configuration privately."
            ) from None
    else:
        print("Database initialized")


if __name__ == "__main__":
    main()
