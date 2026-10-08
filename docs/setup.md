# Setup and operation

## No-install preview

Open `OPEN_DEMO.html` in Chrome, Edge, Firefox or Safari. It contains all CSS, JavaScript and synthetic data. It works without Python, an API key or a network request. You can filter, assign/change requests and create fictional requests. Reloading resets all changes. There is no real staff authentication or backend in this mode.

## Full application on Windows

Install Python 3.12 from [python.org](https://www.python.org/downloads/). Extract this repository to a normal folder. In File Explorer, open that folder and open PowerShell/Terminal there.

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m app.cli seed
.venv\Scripts\python.exe -m uvicorn app.web:create_app --factory --host 127.0.0.1 --port 8000
```

Using the interpreter's explicit path avoids changing PowerShell's script policy or relying on activation. Open **http://127.0.0.1:8000**. Sign in with `demo` / `PortfolioDemo2026!`. Keep the terminal running. Ctrl+C stops the panel; saved records remain in `data/hotel.sqlite`.

## macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m app.cli seed
.venv/bin/python -m uvicorn app.web:create_app --factory --host 127.0.0.1 --port 8000
```

Direct dependencies and runtime constraints are pinned. Python 3.12 was tested locally. CI is configured for 3.11/3.12/3.13; no local pass for the other versions is claimed.

## Demo roles and reset

Manager: `demo`. Analyst: `analyst`. Agents: `housekeeping-agent`, `food-agent`, `events-agent`, `engineering-agent`, `security-agent`, `concierge-agent`. All use the **demo-only** password `PortfolioDemo2026!`. An agent only sees their department; an analyst can read but cannot edit.

Seeding preserves a populated request dataset rather than overwriting it. For a fresh demo, stop both processes and choose a new `DATABASE_PATH` in `.env`, then seed/start again. Do not delete a database that might contain personal or important records. Never copy an operational SQLite file into a public repository.

## Telegram integration

1. Revoke the old token through BotFather. Issue a new token for a test bot.
2. Copy `.env.example` to `.env` in the repository root. Enter only your new `TELEGRAM_BOT_TOKEN` privately. Keep the shared `DATABASE_PATH` unchanged between bot and panel.
3. In a second terminal, run `.venv\Scripts\python.exe -m app.bot` (Windows) or `.venv/bin/python -m app.bot` (macOS/Linux).
4. In Telegram: `/start` → room → fictional name → category → service → details. Verify the ID in the staff panel. Acknowledge/resolve it; then use `/requests` and `/rate REQUEST_ID 5`.
5. Test `/cancel`, invalid inputs and a bot restart. Saved requests persist; unfinished conversation state resets. Run only one polling process for the same bot token.

Default registration asks only room/name. Set `COLLECT_EXTENDED_PROFILE=true` to demonstrate the optional legacy date/gender/email/phone flow, with validation and `/skip`. Demo registration is not verified hotel check-in. Use fictional profile fields.

## Private non-demo staff setup

For a private prototype instance, choose a **fresh** database path and set `DEMO_MODE=false`. Initialize and create a staff account:

```bash
python -m app.cli init
python -m app.cli staff --username manager --name "Service Manager" --role manager
python -m app.cli staff --username housekeeping --name "Housekeeping" --role agent --department housekeeping
```

Password entry is hidden and requires at least 12 characters. Username is unique. Configure HTTPS before non-demo browser use because Secure cookies intentionally do not work over plain HTTP. This command creates accounts, not hotel SSO/MFA. Follow [security](../SECURITY.md) before handling guest data.

## Optional Google Sheets export

Create a replacement least-privilege service-account key only if needed. Keep its JSON outside the repository. Enable the Sheets API and share a dedicated test spreadsheet with the service-account email. Set `GOOGLE_CREDENTIALS_FILE` to that private path and `GOOGLE_SHEET_ID` to the spreadsheet's ID, then run:

```bash
python -m app.cli sheets
```

The dedicated **Portfolio Requests** tab is a replaceable snapshot; it is not an AppSheet database or writeback sync. Export includes operational fields only, no guest names, contacts, room identifiers or detail text. This helper uses spreadsheet scope and `open_by_key`, so Drive-wide browsing is unnecessary. Never use a tab with unrelated content; the command overwrites this dedicated snapshot tab.

## Tests and preview regeneration

```bash
python -m pip install -r requirements-dev.txt
pytest -q --cov=app
ruff check .
ruff format --check .
python scripts/check_public_tree.py
python -m playwright install chromium
python scripts/browser_smoke.py
python -m app.cli export-demo
python scripts/build_preview.py
```

`export-demo` creates a fresh isolated synthetic dataset. It never reads operational records, including edited demo notes. `build_preview.py` produces the standalone HTML and GitHub Pages assets. Browser smoke uses a temporary database; it does not mutate your saved queue. The optional `CHROMIUM_EXECUTABLE` environment variable allows an existing local Chromium binary.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| `No module named app` | Run commands from the repository root |
| Bot token error | Check newly issued private token; panel does not need it |
| Telegram polling conflict | Stop duplicate polling processes |
| Google export fails | Check replacement key, file path, Sheets API and sharing; requests stay locally saved |
| Login stops after repeated attempts | Wait 15 minutes; do not weaken the limit |
| Non-demo login loops on local HTTP | Use HTTPS for Secure cookies; use demo mode for fictional local demonstration |
| Seeding refuses an existing staff/guest DB | Choose a fresh demo database path instead of mixing demo credentials into private records |
| New requests absent in panel | Check bot/panel database paths and current department/date/status filters |
| Saved conflict warning | Refresh the request; another operation changed its version |
| Browser binaries cannot download | Use the standalone preview; run browser tests once an executable is available |
