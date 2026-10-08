from pathlib import Path

import pytest

from app.analytics import compute_metrics
from app.db import Database
from app.seed import seed_demo
from app.service import Service


@pytest.mark.parametrize(
    "start,end,department",
    [(None, None, None), ("2026-10-04", "2026-10-06", "housekeeping"), ("2020-01-01", "2020-01-02", None)],
)
def test_sql_and_python_metric_definitions_agree(tmp_path, start, end, department):
    db = Database(tmp_path / "demo.sqlite")
    db.initialize()
    seed_demo(db)
    now = "2026-10-08T18:00:00Z"
    expected = compute_metrics(
        Service(db).list_requests(
            {"role": "manager", "department_id": None}, department=department, start=start, end=end
        ),
        now=now,
    )
    with db.connect() as c:
        result = dict(
            c.execute(
                Path("analytics/metrics.sql").read_text(),
                {"start": start, "end": end, "department": department, "now": now},
            ).fetchone()
        )
    for key, value in result.items():
        if key == "resolved_requests" and value is None:
            value = 0
        assert value == expected[key], key
