# Technical audit and remediation

Audit date: 2026-10-08. Scope: all surviving source files, both archive manifests, dependency declarations, configuration structure and thesis-described workflows. No uploaded token or service-account key was used to contact an external service.

## Findings

| Priority | Original location | Finding | Rebuild action |
| --- | --- | --- | --- |
| P0 | `.env`, `credits.json` | Telegram token and Google private key are packaged with source | Excluded; rotation remains an account-owner action |
| P0 | `handlers/author/upload_db.py`, `upload_logs.py`, `update_db.py` | Database/log exports and replacement callbacks lack local authorization checks | Removed from the public runtime; all staff API reads/writes authenticate |
| P0 | `handlers/author/commands.py` | Destructive callback branches omit the author check; delete/update capabilities are unsafe for a portfolio bot | Removed; no filesystem/DB replacement through Telegram |
| P1 | `register.py`, `ordering_service.py` | Success is sent before Sheets/SQLite persistence; FSM data is cleared before external write finishes | SQLite commits before success; failed submissions preserve input state |
| P1 | `utils/gsheets_api.py` | Service-account authorization runs on import; Sheets is mandatory for intake | Optional, explicitly invoked export; core startup is credential-free |
| P1 | `gsheets_api.py`, `work_db.py` | Synchronous network and SQLite calls sit inside `async` functions | Bot database work uses `asyncio.to_thread`; web endpoints run in worker threads |
| P1 | `get_num_free_row`, `save_task_in_table` | Read-free-row then write creates races; sheet growth targets default worksheet | Intake uses atomic SQLite insert; snapshot uses one RAW batch update |
| P1 | `database/work_db.py` | Early fetch returns bypass connection closure | Context-managed connections commit/rollback and always close |
| P1 | `database/keys.py` | No guest uniqueness, foreign keys or valid-status checks beyond primary keys | FKs, unique Telegram/source IDs, CHECK constraints and explicit state machine |
| P1 | Catalog callbacks / registration | Arbitrary or stale category selections, missing text and oversized/profile fields are not validated | Listed-value validation, FSM filters, text limits and expired-button handling |
| P1 | `worksheet.update` | USER_ENTERED parsing risks spreadsheet formula interpretation | Export uses RAW, neutralizes formula-leading text and excludes guest/detail fields |
| P2 | Requirements | 2023-era aiogram/aiohttp/frozenlist pins make modern-Python installation fragile | Tested aiogram 3.31.0 stack and exact audited runtime constraints |
| P2 | Task model | Created date in Sheets lacks time; no response/resolution events | UTC-second timestamps, immutable first-response/first-resolution and latest resolution |
| P2 | Original profile form | Birth date, gender, email and phone are collected unconditionally | Optional validated compatibility flow; room/name default |
| P2 | Generic SQL helpers | Values are parameterized, but table/column identifiers are interpolated | Fixed query shapes; dynamic query fields come only from code |
| P2 | Misc/admin/test utilities | Developer file-ID helper, destructive author commands, unused entity/profile helpers and broken generic sheet wrappers | Not carried into production code |

Unauthorized callback checks are an observed absence in source, not proof of a successfully executed attack against the deployed bot. Similarly, old dependency pins are not labeled vulnerable without a vulnerability-database result.

## Starter comparison

All 32 Python files in C2 match C1 exactly. The starter improves packaging, `.gitignore`, examples and security guidance. It does not fix the above behaviors. All original Python files pass AST parsing, but syntax validity does not establish integration correctness. Neither archive contains a SQLite database or a live AppSheet app, so no actual guest rows or original database integrity were available to test.

## Current verification scope

The new application is independently runnable. Tests cover domain behavior, database constraints and transactions, offline aiogram dispatch, HTTP permissions, CSRF, concurrency, Sheets adapter contract/failure isolation and metric definitions. Browser checks operate the actual panel and standalone preview. See [validation](validation.md) for results.

Residual limits: no production identity verification; no real hotel pilot; unfinished FSM sessions are not durable; SQLite is single-node; the event log is application-managed rather than tamper-evident. Successful local tests do not validate a real Telegram token, spreadsheet access or a public deployment.
