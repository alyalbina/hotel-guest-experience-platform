# Analytical decision example: do closed metrics hide waiting work?

**Status: a new 2026 analytical exercise using synthetic data.** This is an example of analysis and a proposed operational decision, not a finding about Novotel Moscow.

## Question and cohort

Which requests should a service manager inspect before treating a completion or SLA percentage as evidence of healthy operations?

Use the original 96-record demo, all creation dates and departments, at **2026-10-08 18:00 UTC**. These are generated fictional requests, not the thesis survey's 182 questionnaires. Browser edits change the preview cohort; restore 96 records to reproduce this snapshot.

## Query and result

Run [metrics.sql](../analytics/metrics.sql) with `start`, `end` and `department` set to `NULL`, and `now` set to `2026-10-08T18:00:00Z`. [Metrics setup](metrics.md#sql-and-reproducibility) provides the executable Python example.

| Observed synthetic output | Result | What it includes |
| --- | --- | --- |
| Volume | 96 | All requests, including cancelled/reopened |
| Completion | 68 / 96 = 70.8% | Currently resolved only in numerator |
| Resolution SLA compliance | 27 / 68 = 39.7% | Currently resolved rows only |
| Overdue active work | 25 requests | New, acknowledged, in-progress or reopened rows past their assumed SLA |
| Mean resolution | 122.8 minutes | Currently resolved rows; unfinished work excluded |

To inspect individual overdue requests, use the same fixed clock:

```sql
SELECT r.id, d.name AS department, r.service, r.status, r.assigned_to,
       r.created_at, r.sla_minutes,
       ROUND((julianday(:now)-julianday(r.created_at))*1440, 1) AS age_minutes
FROM requests r
JOIN departments d ON d.id = r.department_id
WHERE r.status NOT IN ('resolved', 'cancelled')
  AND ROUND((julianday(:now)-julianday(r.created_at))*1440, 6) > r.sla_minutes
ORDER BY r.created_at ASC;
```

The list is for this unrestricted cohort. Add the same department/created-date predicates as `metrics.sql` when comparing a filtered dashboard.

## Interpretation → proposed action

Closed-only SLA excludes 25 overdue active requests. Even if the closed-case average improved, that could reflect a changed case mix or a growing unfinished backlog. The dashboard therefore places overdue workload beside SLA and shows eligible counts.

A proposed manager action is to review the oldest overdue rows, confirm ownership, and inspect workload by department and service. Increasing staffing is premature: the synthetic records cannot distinguish understaffing, logging delay, service complexity or inaccurate SLA rules.

## What would validate the decision?

1. Agree with staff what acknowledgement and completion mean; compare timestamps with observed service events.
2. Replace assumed SLA thresholds with approved service/category policies.
3. Collect comparable baseline and pilot creation cohorts. Include still-open requests and report median/p90, category, department, shift and occupancy context.
4. Check guardrails: reopens, cancellation/repeat contacts, overdue backlog, CSAT response rate and staff logging burden.
5. Prefer a phased or randomized rollout where feasible. A before/after average alone does not establish a product effect.

## Walk the numbers through one request

The [90-second guide](https://alyalbina.github.io/hotel-guest-experience-platform/demo/?tour=request) adds a fictional extra-towels request. Its explicitly scripted timestamps are creation 17:40, assignment 17:41, acknowledgement 17:42, progress 17:44 and resolution 17:52 UTC. The guide calls the preview's existing update and metric functions, then compares the 96-row baseline with the 97-row cohort. It invents no rating. Those aggregate changes demonstrate metric calculations, not an improvement experiment.
