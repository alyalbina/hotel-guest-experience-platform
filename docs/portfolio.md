# CV, LinkedIn and interview material

Use project/research positioning rather than inventing hotel employment, a production rollout or measured improvement. Distinguish the original 2024 thesis from the 2026 portfolio reconstruction. Replace a planned GitHub/Pages link with a verified live link only after publication. Technical implementation in the rebuild used AI assistance; do not claim sole authorship of the original bot.

## English CV: general project entry

### Short entry for the visual case study

**Hotel Guest Experience & Service Automation Platform**  
HSE University thesis, 2024; AI-assisted portfolio reconstruction, 2026

- Translated guest-service research into product decisions, AS-IS/TO-BE processes, requirements, UX flows and system/data models.
- Reconstructed documented hotel staff workflows as a working web workspace with request ownership, status history and operational analytics.
- Defined service metrics and SQL logic; presented the research-to-delivery case with a clearly labelled synthetic demo and explicit validation limits.

**Case:** https://alyalbina.github.io/hotel-guest-experience-platform/case-study/  
**Code:** https://github.com/alyalbina/hotel-guest-experience-platform

### LinkedIn Featured

**Title:** From guest-service research to a working hospitality product

**Description:** An interactive case covering discovery, service design, requirements, system decisions and operational metrics. Based on my 2024 HSE thesis, with an AI-assisted 2026 reconstruction. Includes a working synthetic demo and a clear distinction between technical validation and hotel impact.

### LinkedIn Projects: concise version

**Hotel Guest Experience & Service Automation Platform**

A hospitality product case originating in my 2024 Business Informatics thesis at HSE University. The research reports 182 completed questionnaires and qualitative guest-experience work. I connected service problems with CJM, Service Blueprint, requirements, UX flows and system models.

The 2026 AI-assisted reconstruction replaces the lost AppSheet workflow with a demonstrable staff workspace and adds SQL-backed operational metrics. The interactive case shows how findings informed product decisions. Demo data is synthetic; no production hotel rollout or measured business improvement is claimed. Original coding attribution is retained in the provenance record.

### Longer entry and role-specific positioning

**Hotel Guest Experience & Service Automation Platform**  
HSE University graduation project, 2024; portfolio reconstruction, 2026

- Designed a hotel guest-service solution using service-design research, stakeholder analysis, AS-IS/TO-BE mapping, FURPS+ requirements, UML and an ERD.
- Translated findings from a thesis reporting 182 completed questionnaires and qualitative research into structured request intake, departmental routing and staff task-management workflows.
- Reconstructed the Telegram/AppSheet prototype as a demonstrable Python platform with a staff web workspace, request history and role-based access.
- Defined response/resolution, SLA, completion, reopen and CSAT metrics; added SQL queries and a clearly labeled synthetic analytics demo.

Optional short line: **Python, SQL, Telegram, FastAPI, SQLite, service design, requirements engineering, product analytics.**

If personally conducted research details differ from the thesis reporting, adjust the first two bullets to the actual contribution. Do not add “reduced response time by X%” or “increased CSAT” without pilot data.

## Business Analyst emphasis

**Designed the requirements and operating model for a hotel request-management prototype: stakeholder roles, AS-IS/TO-BE, FURPS+, UML, ERD, user stories and acceptance criteria. Reconstructed documented staff workflows into a runnable demo and linked requirements to automated verification.**

Discussion focus: separate business needs from implementation, resolve status-model inconsistencies, show role boundaries, trace a lost-request problem to a transaction/event rule, and explain which original integration requirements are still planned.

## Product Analyst emphasis

**Built a reproducible service-operations analytics case with SQL and synthetic data, defining response/resolution time, SLA compliance, completion, reopens and CSAT. Specified creation-cohort filters, denominator rules, missing-data treatment and guardrails for a future hotel pilot.**

Discussion focus: response selection bias, open-case censoring, closed-only SLA, cancellation denominator, reopens versus event counts, CSAT response rate and before/after confounding. Show SQL/Python parity, not a made-up improvement.

## Product Manager emphasis

**Developed a research-led hospitality product case from guest-service problems through discovery, workflow design and a demonstrable MVP. Prioritized structured intake, ownership and status visibility, and prepared an impact-measurement framework and roadmap with explicit validation boundaries.**

Discussion focus: scope decisions, the handoff problem, channel adoption, why a lean stack is sufficient, and the difference between shipping a prototype and proving its operational benefit.

## UX Researcher / AI Product Manager relevance

For UXR, prioritize research limitations, CJM/Blueprint and how evidence changed the workflow. The preserved materials do not prove a specific usability-study sample or improvement.

For AI PM, position this as evidence of discovery, workflow/system design and measurement. The product contains no implemented AI feature. Discuss a possible future classifier only as a hypothesis requiring need, data and quality evaluation.

## LinkedIn Projects

**Title:** Hotel Guest Experience & Service Automation Platform

**Description:**

A research-led hotel service case originating in my 2024 Business Informatics graduation thesis at HSE University. The thesis reports 182 completed questionnaires and qualitative guest-experience research, supported by CJM, Service Blueprint, AS-IS/TO-BE, FURPS+, UML and data modeling.

In 2026, I reconstructed the original Telegram + Google Sheets + AppSheet prototype into a demonstrable Python platform with a staff web workspace, request ownership/status history and SQL-backed metric definitions. The public preview uses synthetic data and separates original work, reconstructed artifacts and new functionality. No production rollout or measured business improvement is claimed.

**Skills:** Business Analysis; Product Discovery; Service Design; Requirements Engineering; SQL; Product Analytics; System Design; UX Research.

## GitHub About

**Description:** Research-led hotel service prototype: Telegram intake, staff workflows and operational analytics. HSE thesis case rebuilt with Python, FastAPI and SQLite. Synthetic public demo.

**Topics:** `business-analysis`, `product-management`, `service-design`, `product-analytics`, `hospitality`, `python`, `fastapi`, `aiogram`, `sqlite`, `sql`, `portfolio`.

Website: use the verified live Pages preview after deployment.

## Elevator pitch: about 30 seconds

“My graduation project focused on how hotels handle guest requests. I used service-design research and business analysis to connect guest pain points with a clearer operating workflow. The original prototype combined Telegram, Google Sheets and AppSheet. I have now reconstructed the case as a working portfolio platform with a staff workspace, request history and transparent operational metrics. The public demo is synthetic, and I am explicit about what was implemented and what still needs a hotel pilot.”

## Product interview story

“The problem was not just asking for help; it was what happened after the request. The thesis described delays, manual handoffs and requests that guests had to repeat. I used the journey and service blueprint to narrow the MVP to intake, responsibility and status visibility rather than trying to digitize the whole hotel.

The original prototype used Telegram for guests and AppSheet for staff. When the AppSheet app was lost, I reconstructed its documented workflow and used the rebuild to resolve reliability gaps: persistent identity, atomic recording and explicit progress/history. I kept the architecture small enough to demonstrate without paid services.

For evaluation, I defined response and resolution timing separately from the bot's automatic confirmation. I also added reopen and CSAT guardrails so faster closure would not automatically be treated as better service. The important limitation is that a functioning demo is not impact evidence. The next step is a hotel-approved pilot with a comparable baseline and staff procedures.”

## Technical interview story

“The original bot used aiogram 2.25.1 and synchronous Google Sheets calls in async handlers. It could confirm success before persistence. The rebuild uses aiogram 3 and a shared Python domain service. Telegram and FastAPI both call that service; SQLite is the operational record.

A request and its initial event are written in one transaction. Telegram source references prevent duplicate submission. Staff changes include an expected version checked under a write lock, so competing edits return a conflict. The API authenticates staff, enforces department/role scope and checks CSRF on writes.

The metric framework uses a created-date cohort with explicit eligibility rules. SQL queries are checked against Python results. The bot tests exercise actual aiogram dispatch using a fake transport; browser checks exercise the actual panel and static preview. Live Telegram and Google access need newly issued credentials and separate acceptance checks.”

## Questions to prepare for

| Question | Honest answer boundary |
| --- | --- |
| Did you write all the original bot code yourself? | The preserved original credits another developer. Explain your verified contribution; the 2026 rebuild used AI engineering assistance. |
| What was the measured business improvement? | No hotel pilot result survives/is evidenced. Explain hypotheses and measurement plan. |
| Can you reproduce the original survey metrics? | No raw responses are preserved; values are thesis-reported and not recomputed. |
| Why does the demo have 96 requests? | It is a generated sample for software demonstration, unrelated to 182 questionnaire respondents. |
| What happened to AppSheet? | The app is unavailable; screens, entity model and workflow were reconstructed from the thesis. |
| What does SLA compliance exclude? | Current unresolved and cancelled work; overdue active volume is shown separately. |
| Is it appropriate for Dubai? | Hospitality is relevant, but local channel adoption, languages, hotel identity and operations need discovery; no Dubai customer research is claimed. |

Practice by showing a real screen, a source artifact and one SQL query. Only claim technical skills you can explain and demonstrate in an interview.
