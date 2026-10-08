# User stories and acceptance criteria

**Status:** reconstructed core stories plus new portfolio safeguards. IDs connect to [requirements](requirements.md). Tests referenced below verify the implemented logic, not a hotel field trial.

| ID / origin | Story | Acceptance criteria | Verification |
| --- | --- | --- | --- |
| US-01 / Original intake | As a guest, I register so my requests include a room and a name | Given an unregistered Telegram identity, `/start` asks for a listed room and a name; invalid room/name is rejected; repeating registration reuses the guest; optional legacy profile fields validate or skip | `test_domain`, `test_bot` |
| US-02 / Original intake, new reliability | As a guest, I choose a service and provide actionable detail | Category/service must match the catalog; 1–1000 printable characters; request and initial event commit before success; duplicate source reference produces one record | `test_domain`, offline aiogram workflow |
| US-03 / Reconstructed staff workflow | As a service manager, I filter requests by status and department | Queue accepts department/status, inclusive created-date filters and service/room/ID search; empty results are understandable; filters do not bypass role scope | `test_web`, browser smoke |
| US-04 / Reconstructed assignment | As a manager, I assign work to an eligible employee | Only a manager or same-department agent can be selected; analyst/other-department assignment is rejected; event records actor and assignee ID; assignment does not set response time | `test_domain`, browser smoke |
| US-05 / Reconstructed status, new detailed states | As an employee, I record service progress | Only allowed transitions succeed; first acknowledgement sets first-response once; resolution sets resolution; cancelled/reopened requires a reason; event is atomic with change | `test_domain`, browser smoke |
| US-06 / New event history | As a manager, I review a request's history | Detail shows chronological creation, assignment, status, note and rating events; actor/time/reason are visible where present; stale updates return conflict | `test_domain`, `test_web`, browser smoke |
| US-07 / New access control | As hotel leadership, I restrict staff access | Unauthenticated API returns 401; agent cannot access another department; analyst cannot mutate; cookie is HttpOnly; writes require matching CSRF token | `test_web` |
| US-08 / New guest lookup | As a guest, I check the state of my requests | `/requests` shows at most the latest 20 requests for the registered Telegram guest; it never accepts an arbitrary other guest ID | `test_bot`, service query |
| US-09 / New feedback | As a guest, I rate completed service | Integer rating 1–5; guest owns request; current state resolved; one current rating; reopening clears it while rating events remain | `test_domain`, `test_bot` |
| US-10 / New analytics | As an analyst, I compare operational workload and quality | Number, response/resolution, department volume, SLA, completion, reopen and CSAT are computed for the same creation cohort; rates use specified denominators; empty cohort shows no value rather than 0% | `test_analytics`, `test_sql` |
| US-11 / Revised Sheets integration | As a manager, I export an operational snapshot | Explicit CLI invocation; no identity/free-text export; RAW values/formula guard; export failure cannot delete or fail local intake | `test_sheets` |
| US-12 / New portfolio preview | As a recruiter, I inspect the product without installing a backend | Standalone HTML loads local synthetic data; filters, assignments/status and creation can be explored; refresh resets preview changes; copy identifies simulation | Browser smoke |

Planned stories: verified guest stay, PMS synchronization, proactive Telegram updates, original AppSheet bulk actions and employee/room management. These have no “done” claim in this release.
