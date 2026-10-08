"""Created-date cohort metrics. Definitions also appear in docs/metrics.md."""

from collections import Counter
from datetime import datetime, timezone


def minutes(start, end):
    return (datetime.fromisoformat(end) - datetime.fromisoformat(start)).total_seconds() / 60


def average(values):
    return round(sum(values) / len(values), 1) if values else None


def percentage(numerator, denominator):
    return round(100 * numerator / denominator, 1) if denominator else None


def compute_metrics(rows, now=None):
    now = now or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    responses = [minutes(r["created_at"], r["responded_at"]) for r in rows if r["responded_at"]]
    resolved = [r for r in rows if r["status"] == "resolved" and r["resolved_at"]]
    ever_resolved = [r for r in rows if r["first_resolved_at"]]
    ratings = [r["csat"] for r in resolved if r["csat"] is not None]
    active = [r for r in rows if r["status"] not in {"resolved", "cancelled"}]
    return {
        "number_of_requests": len(rows),
        "average_response_minutes": average(responses),
        "responded_requests": len(responses),
        "average_resolution_minutes": average([minutes(r["created_at"], r["resolved_at"]) for r in resolved]),
        "resolved_requests": len(resolved),
        "completion_rate": percentage(len(resolved), len(rows)),
        "sla_compliance": percentage(
            sum(minutes(r["created_at"], r["resolved_at"]) <= r["sla_minutes"] for r in resolved),
            len(resolved),
        ),
        "reopened_requests_rate": percentage(
            sum(r["reopen_count"] > 0 for r in ever_resolved), len(ever_resolved)
        ),
        "ever_resolved_requests": len(ever_resolved),
        "csat_mean": average(ratings),
        "csat_positive_rate": percentage(sum(x >= 4 for x in ratings), len(ratings)),
        "csat_responses": len(ratings),
        "csat_response_rate": percentage(len(ratings), len(resolved)),
        "active_requests": len(active),
        "overdue_active_requests": sum(minutes(r["created_at"], now) > r["sla_minutes"] for r in active),
        "requests_by_department": dict(Counter(r["department_name"] for r in rows)),
        "requests_by_status": dict(Counter(r["status"] for r in rows)),
        "requests_by_day": dict(sorted(Counter(r["created_at"][:10] for r in rows).items())),
        "as_of": now,
    }
