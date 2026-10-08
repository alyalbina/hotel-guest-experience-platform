# Product metrics framework

**Status:** new operational framework. Thesis research NPS/CSAT/CES are historical reported measures and are not mixed with demo request metrics. All seeded activity is synthetic, generated with random seed 2024 and UTC anchor **2026-10-08 18:00**. Departments/SLA assumptions are invented demo configuration, not confirmed hotel policy.

## Metric contract

Filters select requests **created** between inclusive UTC dates and optionally a department. The API further restricts agents to their department. The inbox status/search filters do not redefine KPI cohorts; department/date filters do. Open/reopened/cancelled requests remain in total volume and completion denominator. Means/rates with an empty eligible denominator return null and display “—”.

| Metric | Formula / eligible rows | Interpretation and caveat |
| --- | --- | --- |
| Number of Requests | Count all requests in creation cohort | Workload/adoption; no duplicate count for the same source reference |
| Average Response Time | Mean `(responded_at - created_at)` in minutes for rows with first response | Staff acknowledgement, not bot confirmation or employee assignment; unresponded requests excluded |
| Average Resolution Time | Mean `(resolved_at - created_at)` for currently resolved rows | End-to-end through latest resolution, including reopen cycles; excludes unfinished work |
| Requests by Department | Count per request department | Configured category routing, not a validated staffing model |
| SLA Compliance | Currently resolved within snapshotted resolution threshold / all currently resolved × 100 | Exactly on deadline passes; current overdue backlog is shown separately |
| Completion Rate | Currently resolved / all requests in cohort × 100 | Cancelled remains in denominator; a reopened row is no longer complete |
| Reopened Requests Rate | Ever-resolved rows with `reopen_count > 0` / ever-resolved rows × 100 | Each request counted once regardless of number of reopens |
| CSAT mean | Mean current 1–5 rating among rated currently resolved requests | Mean score, not satisfaction percentage |
| Positive CSAT | Ratings 4–5 / ratings on currently resolved requests × 100 | Optional additional interpretation of requested CSAT |
| CSAT Response Rate | Rated currently resolved / currently resolved × 100 | Reveals feedback selection bias |
| Overdue Active Requests | Active age exceeds snapshotted SLA | Avoids hiding unresolved breaches in closed-only SLA compliance |

Reopening clears the latest resolution timestamp and current rating; the first resolution and earlier rating events remain. Response timestamp stays at first acknowledgement. UI charts and SQL use the same definitions. Synthetic preview time is fixed for reproducibility; the local application uses current UTC for active overdue workload.

## SQL and reproducibility

[Aggregate query](../analytics/metrics.sql) uses `:start`, `:end`, `:department`, `:now`; null date/department means unrestricted. [Breakdowns](../analytics/breakdowns.sql) use the same cohort. Python/SQL parity tests include full, filtered and empty cohorts, with a floating-point rounding guard at SLA boundaries.

```python
import sqlite3
from pathlib import Path

conn = sqlite3.connect("data/hotel.sqlite")
conn.row_factory = sqlite3.Row
params = {"start": None, "end": None, "department": None, "now": "2026-10-08T18:00:00Z"}
result = dict(conn.execute(Path("analytics/metrics.sql").read_text(), params).fetchone())
conn.close()
print(result)
```

## Data quality

Require ordered UTC timestamps, known category/department, unique request/source IDs and a valid rating. Missing response is unknown/not-yet-responded rather than zero minutes. Keep the response sample size visible. Preserve cancellation and reopen events rather than editing history. Do not infer staff productivity from counts without task mix and shift exposure.

The demo's regular demand pattern deliberately makes the chart understandable; it is not realistic occupancy forecasting or a model fitted to real hotel records. No synthetic average or percentage belongs in an achievement statement.

## Pilot measurement plan

Primary candidate: median and p90 response/resolution time by comparable category and shift. Guardrails: reopen rate, CSAT and its response rate, overdue backlog, abandonment/repeat contacts, and staff workload. The current dashboard implements means plus specified rates; p50/p90 and adoption instrumentation are next steps.

Collect a baseline with the same timing definitions; train staff on acknowledgement/closure; pilot a limited set of departments; compare workload/request mix and calendar effects. Prefer an appropriate randomized or phased rollout if operationally possible. A simple before/after comparison does not establish causality. Define target thresholds and power/sample requirements after observing baseline variance; do not invent a promised uplift or statistically significant result.
