# Validation report

Execution date: **2026-10-08**. Environment: Python **3.12.14**, Linux, aiogram **3.31.0**, FastAPI **0.143.0**, SQLite via Python stdlib, headless Chromium **153**. These are local results, not a published GitHub workflow run.

## Results actually executed

| Check | Result | Scope |
| --- | --- | --- |
| Original Python AST parse | 32 / 32 pass | Syntax only; original integrations were not started |
| Original vs starter Python bytes | 32 / 32 identical | Starter is packaging cleanup, not runtime repair |
| pytest | **34 tests passed** | Domain, API, offline bot dispatch, export and metrics |
| Measured application coverage | **90.12%, displayed as 90%** | 658 measured statements; CLI intentionally excluded from coverage but public-export privacy has a direct test |
| Domain/service coverage | **96%** | Not a claim of exhaustive branch coverage |
| SQL vs Python metrics | Passed full/filtered/empty cohort parity | Includes denominator/rounding and SLA boundary behavior |
| Ruff | Lint and formatting pass | Python source/tests/scripts |
| JavaScript syntax | `node --check` passes | Build-free frontend |
| Dependency audit | **40 runtime packages, 0 known findings** | pip-audit vulnerability DB at audit time; not a guarantee of future safety |
| Actual browser workflow | Passed | Login, filters, assignment, state lifecycle, reopen reason, creation and escaped text |
| Mobile rendering | No document overflow at **390px** | Inbox adapts to request cards; not a full accessibility audit |
| Static preview | Passed | Opens from a local file; new request appears; refresh resets to 96 |
| Browser JavaScript errors | **0** in tested workflow | Does not certify all browser engines |
| Screenshots | **5** captured and inspected | Actual inbox/analytics/case/detail/mobile, all fictional data |
| Publication gate | Passed | No prohibited public files or recognized credential patterns |
| Documentation local links | Checked after authoring | References resolve within the package |

Coverage rounding: 593 covered of 658 statements. The suite emits one non-failing Starlette test-client notice about its future HTTP client interface. HTTP/API checks still pass; no application warning was hidden to obtain a clean-looking result.

## Important test cases

- Concurrent duplicate submissions produce one request and one initial event.
- Concurrent staff updates with the same version allow one save and one conflict.
- Invalid relationships, assignees and transitions leave the request/event state unchanged.
- Missing session/CSRF, read-only analyst and cross-department agent operations are rejected.
- Real aiogram Router/Dispatcher/FSM are fed fake Telegram updates; persistence failure produces retry guidance rather than a false success message.
- Guest status and rating are scoped to the registered guest; reopened requests clear current CSAT.
- Sheets export contract uses RAW values, formula-leading text guards and no guest identity/detail; network failure leaves local requests intact.
- Public demo regeneration ignores an operational database containing private test content.
- Browser creation treats an HTML payload as text and does not insert an image/event handler.

## Not verified externally

**Live Telegram:** no external `getMe`, real delivery, real callback or polling acceptance was performed. Original credentials were never used. Offline dispatch verifies application handling, not account permissions/network access.

**Live Google Sheets:** no authorized real spreadsheet was accessed. The adapter is tested with a mocked client; worksheet creation/access/large-sheet quotas and actual export need replacement credentials and a dedicated test sheet.

**Public GitHub/Pages:** repository creation and hosting are external pending actions. Workflow YAML is supplied, but CI/Pages are not counted as run. The README's planned preview URL is explicitly conditional on publication.

**Hotel operations:** no field trial, staff usability sample, authenticated check-in or demonstrated business/financial improvement.

**Broader systems:** Python 3.11/3.13 CI is configured but not executed locally; Windows instructions were authored but not run on Windows; full accessibility, load, recovery and independent penetration testing remain planned.

## Reproduction

Run the commands in [setup](setup.md). `scripts/browser_smoke.py` uses an isolated temporary database and regenerates the screenshots. Default Playwright Chromium can be installed; an existing executable can be selected with `CHROMIUM_EXECUTABLE`. Public preview assets come from deterministic seeded data in an isolated database, never a working hotel's records.
