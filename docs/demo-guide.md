# Demo script and walkthrough

## One request in about 90 seconds

Open [the guided public demo](https://alyalbina.github.io/hotel-guest-experience-platform/demo/?tour=request). The intro leaves the original 96 records untouched. Click Start to restore the baseline and create `tour-001`, a fictional extra-towels request.

1. Assign housekeeping. Explain that assignment does not count as a human response.
2. Acknowledge, then start fulfillment. Inspect the request history if desired; close it to continue.
3. Record resolution, then open the analytical effect. Compare the original cohort with one extra resolved request.
4. Restore 96 records to clear the walkthrough, or close the guide and freely explore.

The guide uses a **scripted clock** on 8 October 2026: created 17:40, assigned 17:41, acknowledged 17:42, in progress 17:44, resolved 17:52 UTC. Its two-minute response and 12-minute resolution are assigned fictional intervals, not time measured from clicks or hotel outcomes. No CSAT rating is fabricated. The offline `OPEN_DEMO.html` includes the same optional guide.

## Recruiter walkthrough: about three minutes

1. Open the public preview or `OPEN_DEMO.html`. Explain that all operations are synthetic and preview edits reset on refresh.
2. Show the inbox: one operational record, department/status/date filters, assigned employees and clear request identity.
3. Open `demo-1001`, the fictional extra-towels request. Assign a housekeeping employee, acknowledge, progress and resolve. Reopen with a reason to demonstrate history and follow-up rules.
4. Open Service Analytics. Explain response/resolution, SLA, completion, reopens and CSAT; point to denominators and overdue active workload.
5. Open Product Case Study. Connect the research-reported problems and 182 questionnaires to design decisions. State that measured business improvement is not yet available.

## Full technical walkthrough

Run the full local application, sign in and create a request for a fictional guest. Demonstrate persistence after restarting the server. Compare manager/analyst/department-agent accounts. Show a rejected stale-version update, the SQLite constraints and tests, and the SQL/Python parity query. With a new Telegram token, register and submit from Telegram, resolve from the panel, then check/rate through the bot. Live Telegram acceptance is separate from offline bot tests.

## Example guest requests

| Category / service | Fictional detail |
| --- | --- |
| Amenities / Extra towels | Please bring two towels before 19:00. |
| Maintenance / Air conditioning | Cooling is not working in the demo room. Please check after 14:00. |
| Room service / In-room dining | Please share today's menu and vegetarian options. |
| Personal requests / Transport | Could you arrange a taxi for 08:30 tomorrow? |
| Restaurant / Table booking | A table for two at 20:00, if available. |

These are intake examples. The product does not automatically make bookings, process payment or guarantee availability.

## What to say about the screenshots

They come from the rebuilt 2026 app, not the lost AppSheet installation. Request inbox and analytics show the initial synthetic snapshot. The mobile screenshot may include an extra fictional request created during the browser smoke flow. Values are illustrative software outputs, not historical hotel measurements.

## Discussion prompts

Why Telegram? It was the thesis prototype channel; target-market adoption still needs testing. Why no AI? This service workflow does not yet need it. Why SQLite? It makes a small single-host demonstration durable and easy to run. Why a separate preview? A recruiter can inspect the interaction immediately; persistence/security remain demonstrable in the full app.
