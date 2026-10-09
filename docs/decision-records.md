# Three decisions behind the rebuild

**Status: new 2026 decision records.** These explain implemented choices using preserved source, current code and tests. They are not contemporaneous 2024 records or evidence of hotel impact. [Provenance](provenance.md) separates thesis design, surviving code, reconstruction and new development.

## 1. A small staff workspace rather than another low-code dependency

**Need:** recover request review, departmental ownership and status updates described for the lost AppSheet application, with a demonstrable interface and explicit access rules.

| Option | Benefit | Cost at this scope | Decision |
| --- | --- | --- | --- |
| Recreate AppSheet | Familiar original interaction model | External platform configuration; original app is unavailable | Preserve its documented workflow, not its installation |
| Streamlit | Quick analytical screens in Python | Less direct control over a custom inbox/drawer workflow | Useful alternative for a standalone analytics tool |
| FastAPI + HTML/CSS/JS | One Python backend, explicit HTTP operations, no frontend build | UI state and accessibility require manual care and browser verification | Implemented |
| React + FastAPI | Components and tooling for larger interfaces | Separate toolchain and deployment surface | Reconsider if UI complexity/team size warrants it |

**2024 → 2026:** Telegram/aiogram 2 + SQLite → Sheets → AppSheet becomes Telegram/aiogram 3 and a staff API → shared domain service → SQLite. Sheets is an optional snapshot export. The staff web panel is new development; the underlying service concept and categories come from the thesis.

**Verification:** local authenticated browser smoke covers creation, assignment, transitions, history, analytics and role behavior. The public static preview demonstrates interaction using browser memory. It does not authenticate staff or persist records.

**Revisit:** introduce a component framework when reusable screens, contributors and maintenance needs outweigh its tooling cost. Validate actual staff usability before increasing scope.

## 2. One durable request before a save confirmation

**Need:** retain context across the handoff and avoid a guest seeing a capture confirmation for an unsaved request.

**Alternatives:** retain two synchronous writes to SQLite and Sheets; make Sheets the primary queue; or commit the operational record locally and export separately.

**Choice:** request and creation event commit in one SQLite transaction. Bot and staff actions use the same domain service. Sheets export is explicit and outside intake. State transitions and optimistic record versions prevent arbitrary edits and silent stale updates.

**Cost:** SQLite supports a small single-host demonstration. It is not a shared database for independent deployments. Exported Sheets data is a snapshot, not bidirectional synchronization. History is operational and not tamper-evident. A saved request is not a guarantee of physical service.

**Verification:** [domain tests](../tests/test_domain.py), [audit](audit.md), [architecture](architecture.md) and [user stories](user-stories.md). Transaction, state, access and conflict tests verify software boundaries; they do not measure missed requests in hotel operations.

**Revisit:** measured write contention, multiple instances or operational resilience requirements may justify PostgreSQL, background delivery and stronger retention/backup controls.

## 3. Human response and unfinished work must remain visible

**Need:** produce interpretable metrics rather than a dashboard that rewards automatic confirmations or hides unfinished work.

**Alternatives:** use bot confirmation or assignment as response; average only closed cases without a backlog guardrail; or define staff acknowledgement separately and expose eligible counts and overdue active work.

**Choice:** assignment alone leaves `responded_at` empty. First staff acknowledgement sets response time. Resolution and resolution SLA use currently resolved rows; the UI also shows overdue active requests. Reopened requests leave the completion numerator; CSAT uses rated currently resolved requests with its response rate.

**Cost:** means omit unfinished rows and can hide outliers. Staff logging habits affect timestamps. Demo SLA thresholds are assumptions. Neither counts nor ratings identify causes or productivity without task mix and shift exposure.

**Verification:** SQL/Python parity tests cover full, filtered and empty cohorts. The [guided demo](https://alyalbina.github.io/hotel-guest-experience-platform/demo/?tour=request) verifies that assignment leaves response empty, then records a scripted 2-minute response and 12-minute resolution. Browser checks inspect actual timestamps and recalculated metrics.

**Revisit:** validate staff logging and hotel SLA policy; add median/p90 and shift/category segmentation when real data is available. Use a defined baseline and pilot protocol before claiming improvement. See [the analytical decision example](analytics-case.md).
