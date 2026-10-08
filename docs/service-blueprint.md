# Service Blueprint

**Source reconstruction:** T1 pp. 18–19, visually inspected. The original broad blueprint spans online booking, arrival, service use, departure and review, with customer/frontstage/backstage/support layers. This table translates its topology without reproducing the persona portrait or identifiable data.

| Layer | Booking | Arrival | Stay and services | Departure | Review |
| --- | --- | --- | --- | --- | --- |
| Physical / digital evidence | Hotel/booking site | Reception | Room, hotel, restaurant | Reception/bill | Review platform |
| Customer action | Select and book hotel | Register at reception | Use facilities and ask for services | Pay and check out | Publish feedback |
| Frontstage staff | Provide service information | Register guest and provide room | Interact with guest and fulfill services | Explain bill and departure | Respond to feedback |
| Backstage work | Process reservation | Prepare registration and room | Coordinate departments | Process account/payment | Analyze guest feedback |
| Support process | Booking/operations IT | Staff training/preparation | Maintenance and operational support | Finance/marketing operations | Feedback collection/analytics |

The thesis blueprint is descriptive. It does not prove a working digital integration for booking, payment or reputation platforms.

## Current request-handling blueprint

**Status:** narrowed TO-BE reconstruction and new implementation. This is the part the portfolio can demonstrate.

| Layer | Identify need | Capture request | Triage / assign | Fulfill | Follow up |
| --- | --- | --- | --- | --- | --- |
| Guest action | Choose service | Submit details | Wait / check `/requests` | Receive physical service | Rate after resolution |
| Visible interface | Telegram category/service menu | Durable request ID | Current status on lookup | Resolved status | `/rate ID SCORE` |
| Staff frontstage | Reception fallback | Read context in inbox | Assign eligible employee; acknowledge | Record progress and resolve | Reopen if more work needed |
| Backstage system | Validated guest/catalog context | Request + event transaction | Department scope, ownership/version checks | Timestamped state changes | Current CSAT; retained event history |
| Support system | Catalog/room configuration | SQLite durability and keys | Session/CSRF/role controls | Workflow procedures and eventual backups | Metric definitions and analyst review |
| Failure control | Expired buttons route to `/start` | Do not confirm failed persistence | Reject invalid assignee/stale record | Require valid transition | Clear rating on reopen; verify ownership |

The line of interaction separates guest messages from staff actions. The line of visibility separates the staff workflow from database/security controls. The line of internal interaction separates domain behavior from support operations such as backup and pilot training.

Proactive notifications, verified room access, hotel SSO, escalation scheduling and physical fulfillment remain outside this release. The bot's immediate saved confirmation must not be interpreted as a human response or completed service.
