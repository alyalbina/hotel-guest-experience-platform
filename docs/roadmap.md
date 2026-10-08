# Backlog and roadmap

Priorities reflect a portfolio release first, then external validation and a limited hotel pilot. A completed item means demonstrated locally; it does not imply a production rollout.

| Priority / ID | Item | Status | Evidence / dependency |
| --- | --- | --- | --- |
| P0 / SEC-01 | Remove original secret-bearing files and admin destructive/export callbacks | Done in new public code | Audit and publication gate |
| P0 / SEC-02 | Revoke original Telegram token / Google key | Owner action pending | BotFather and Google Cloud accounts |
| P0 / CORE-01 | Make local request/event persistence atomic and deduplicated | Done | Transaction/concurrency tests |
| P0 / BOT-01 | Migrate core registration/catalog/submission to aiogram 3 | Done offline | Real dispatch with fake transport; live acceptance pending |
| P0 / WEB-01 | Rebuild queue/filter/detail/assignment/status | Done | Browser workflow and API tests |
| P0 / AUTH-01 | Add sessions, CSRF and role/department checks | Done | API tests |
| P1 / ANA-01 | Add eight requested metrics, SQL and cohort visuals | Done with synthetic data | Metric parity and browser tests |
| P1 / DOC-01 | Publish source-grounded English artifacts and contribution boundaries | Done | Documentation and provenance |
| P1 / DEMO-01 | Prepare no-install preview and screenshots | Done | Standalone browser tests |
| P1 / PUB-01 | Create GitHub repository and enable Pages | Prepared, external action pending | Publication package and instructions |
| P1 / INT-01 | Verify live Telegram with a new token | Pending credentials | Register → submit → staff resolve → guest rate |
| P1 / INT-02 | Verify optional Sheets with a new least-privilege key | Pending if needed | RAW snapshot, re-export and access-failure test |
| P2 / ID-01 | Verify guest stay via hotel-issued code/PMS | Planned | Hotel partnership and identity requirements |
| P2 / UX-01 | Staff usability/keyboard focus/screen-reader audit | Planned | Research participants; accessibility fixes |
| P2 / OPS-01 | Backup/recovery, retention and private deployment procedures | Planned | Defined data policy and host |
| P2 / BOT-02 | Durable unfinished FSM, guest notifications and rate limits | Planned | Bot usage/load evidence |
| P2 / ANA-02 | p50/p90, adoption and repeat-contact instrumentation | Planned | Baseline definitions and field data |
| P2 / APP-01 | Employee/room administration and AppSheet-style bulk actions | Planned | Actual staff demand, not portfolio feature count |
| P2 / PILOT-01 | Hotel service pilot and impact evaluation | Planned | Identity/privacy/operations/measurement readiness |
| P3 / SCALE-01 | PostgreSQL, multi-property and worker queues | Deferred | Only if measured deployment needs justify complexity |
| P3 / AI-01 | AI classification or drafting | Deferred | A validated need and quality/safety evaluation; no AI feature claimed |

## Release sequence

**R1: portfolio MVP** — runnable local app, safe source, offline bot verification, staff workspace, documented SQL/synthetic analytics and static preview. This package delivers R1.

**R1.1: externally verified demo** — new credentials, live Telegram/Sheets acceptance, GitHub CI and public Pages preview. Pages remains a synthetic simulation; hosting it does not host the bot/backend.

**R2: controlled hotel pilot** — hotel identity, staff training, operational fallback, privacy/backup procedures and a defined baseline. Only after this stage should measured outcomes be added to the CV.

**R3: scale by evidence** — integrations, additional staff functions and architecture growth based on observed constraints. No fixed dates or invented delivery estimates are imposed on a solo portfolio project.
