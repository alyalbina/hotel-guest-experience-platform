import pytest

from app.analytics import compute_metrics


def request(
    status="resolved", response="2026-10-08T10:10:00Z", resolved="2026-10-08T10:40:00Z", reopened=0, csat=5
):
    return {
        "created_at": "2026-10-08T10:00:00Z",
        "responded_at": response,
        "resolved_at": resolved,
        "first_resolved_at": resolved,
        "status": status,
        "reopen_count": reopened,
        "csat": csat,
        "sla_minutes": 40,
        "department_name": "Housekeeping",
    }


def test_empty_cohort_is_not_zero_percent():
    m = compute_metrics([])
    assert m["number_of_requests"] == 0
    for key in [
        "average_response_minutes",
        "average_resolution_minutes",
        "completion_rate",
        "sla_compliance",
        "reopened_requests_rate",
        "csat_mean",
    ]:
        assert m[key] is None


def test_denominators_sla_boundary_and_reopened_active():
    active = request(status="reopened", response="2026-10-08T10:20:00Z", resolved=None, reopened=1, csat=None)
    active["first_resolved_at"] = "2026-10-08T10:30:00Z"
    rows = [
        request(),
        request(resolved="2026-10-08T11:00:00Z", csat=3),
        active,
        request(status="cancelled", response=None, resolved=None, csat=None),
    ]
    m = compute_metrics(rows, now="2026-10-08T12:00:00Z")
    assert m["average_response_minutes"] == pytest.approx(13.3)
    assert m["average_resolution_minutes"] == 50
    assert m["completion_rate"] == 50 and m["sla_compliance"] == 50
    assert m["reopened_requests_rate"] == pytest.approx(33.3)
    assert m["csat_mean"] == 4 and m["csat_positive_rate"] == 50
    assert m["overdue_active_requests"] == 1
