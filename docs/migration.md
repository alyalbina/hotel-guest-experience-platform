# Migration from aiogram 2.25.1 and the original prototype

## Version choice

aiogram **3.31.0** is the current stable release verified from [PyPI](https://pypi.org/project/aiogram/) on 2026-10-08. The [official migration guide](https://docs.aiogram.dev/en/latest/migration_2_to_3.html) explains the breaking changes. The new adapter was installed and tested with that version rather than just changing the old requirement line.

| Old pattern | Current equivalent |
| --- | --- |
| Global `Dispatcher(bot, storage=...)` | Independent Dispatcher + dedicated Router + supplied Bot |
| `executor.start_polling` | `await dispatcher.start_polling(bot)` |
| `message_handler` / `callback_query_handler` | Router observers and explicit filters |
| Implicit state/content filters | `StatesGroup`, `FSMContext`, state and `F.text` filters |
| Global `dp.current_state` | Injected FSMContext |
| Keyboard `.add` construction | Explicit `InlineKeyboardMarkup` rows |
| Sync I/O inside async functions | SQLite work via `asyncio.to_thread` |
| Global HTML parsing for all text | Plain text; untrusted fields are not interpreted as HTML |

## Feature mapping

| Original behavior | Current behavior | Compatibility decision |
| --- | --- | --- |
| `/start`, room, name | Preserved with validation | Same nine demo rooms |
| Birth date, gender, email, phone | Optional legacy flow | `COLLECT_EXTENDED_PROFILE=true`; supports skip; off by default for minimization |
| Nine categories / 23 options | English catalog | All options retained; departments/SLA configured locally |
| In-room menu image | Optional `MENU_FILE_ID` | Menu image can fail without blocking request entry |
| Request detail submission | Durable ID and atomic local save | Confirms success only after commit |
| Callback cancellation | `/cancel` plus expired-button guidance | No dependency on old keyboard payloads |
| Mandatory Sheets writes and category lookups | Local category routing; optional manual snapshot | Intentionally revised integration; no two-way sync |
| Developer/admin DB and filesystem helpers | Removed | Unsafe maintenance capabilities are not user features |
| AppSheet status/filter/detail | Rebuilt web workflow | Added auth/events/richer status; not a restoration of the app binary |
| Guest status/CSAT | New commands | Clearly added, not attributed to surviving original bot |

The original prototype's core product functions are retained or reconstructed. Privacy defaults, integration topology, status model and maintenance commands changed deliberately; this is not a transparent in-place library upgrade.

## Rollout order

1. Revoke old credentials and preserve a private source backup outside public Git history.
2. Use a fresh schema; seed fictional data for demonstration. Run the offline suite and browser checks.
3. If a private legacy database is found later, inspect schema and back it up. Map guest keys/request keys to new IDs, map status strings explicitly, and migrate in an isolated dry run. Do not fabricate historic response/resolution times or CSAT.
4. Reconcile counts, guest/task relationships and status totals. Flag unmapped categories/staff instead of silently assigning them. Review personal-data minimization before any export.
5. Issue a new Telegram token. Start one polling instance. Test registration, all catalog branches, cancellation, failed/retried persistence, status lookup and rating with fictional data.
6. Configure new Sheets credentials only if export is needed. Verify a dedicated tab and permissions. No AppSheet writeback is supported.
7. Record external acceptance separately from local test results before using “live integration verified” language.

There is no legacy data migration in this package because neither archive includes the original database. FSM state from aiogram 2 is not transferred; unfinished conversations restart, while successfully saved records would be migrated only through an explicit data migration.
