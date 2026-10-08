# Product Requirements Document

Version 1.0 · 2026 portfolio rebuild · Owner: Albina Urubkina.

**Provenance:** problem and core guest/staff workflow derive from T1 pp. 24–31, 36–42, 69–74. Authentication, detailed states, events and analytics are new implementation decisions.

## Product outcome

Give hotel teams one traceable record from guest intake to service completion. The portfolio outcome is a working, understandable demonstration of research-to-delivery reasoning. Operational improvement remains a pilot hypothesis.

## Users and jobs

| User | Job to be done | Current access |
| --- | --- | --- |
| Guest | Submit a service request from the room and find its status | Telegram, scoped to their own registration |
| Reception / service manager | Triage requests and allocate responsibility | Manager account; all departments |
| Department employee | Act on service work and record progress | Agent account; own department |
| Analyst / manager | Understand demand, delays and feedback | Read-only analyst or manager dashboard |

## MVP scope

Register room/name, retain the original nine categories and 23 services, capture details, create a durable request ID, route to a department, support authenticated queue filtering, assign staff, change status, retain history, and calculate the requested operational metrics. Optional extended registration preserves legacy field compatibility; optional Sheets export provides an operational snapshot.

Outside this release: verified check-in, payments, reservations, inventory availability, PMS/CRM synchronization, AI answers, automatic dispatch to individual staff, proactive guest notifications, employee/room CRUD and original AppSheet bulk editing. Service selection captures a request; it does not book or fulfill the requested service automatically.

## Core workflow

1. Guest chooses a demo room and name, then a service category and option.
2. Details are validated; SQLite inserts the request and initial event atomically.
3. A success message includes the durable ID only after commit.
4. Manager assigns an eligible employee. Assignment alone is not counted as response.
5. Staff acknowledge and progress the request; resolution records a UTC timestamp.
6. A manager or eligible department employee may reopen with a reason. History and first-resolution time remain; current resolution/CSAT clear.
7. Guest checks `/requests` and rates a currently resolved request once through `/rate`.

## Workflow decisions

`new → acknowledged → in_progress → resolved` is the normal path. Acknowledged requests may resolve directly. Active work may cancel with a reason. Resolved work may reopen with a reason, then progress or resolve again. Cancelled work is terminal in this version. The status machine is enforced by the service, not just dropdown options.

The richer state model extends AppSheet's described complete/incomplete filters. A compatibility view would map resolved to complete and all active states to incomplete; cancelled needs a deliberate third category. No historic rows were migrated because none were provided.

## Release acceptance

Guest submission survives a Sheets outage; duplicate source events create one request; unauthorized staff cannot read or change another department's records; analysts cannot write; concurrent changes reject stale versions; request/event writes are atomic; timestamps support reproducible metrics; preview data is visibly synthetic; the app runs without paid APIs; setup and test commands are documented.

This release is accepted as a local portfolio prototype, not as production hotel software. See [user stories](user-stories.md) and [validation](validation.md).

## Product hypotheses and pilot design

Measure baseline response/resolution distributions, overdue active workload and service-level CSAT. Pilot comparable categories/shifts with clear staff acknowledgement instructions. Track request volume and adoption so changes are not confused with a different request mix. Review both speed and quality; closing requests quickly must not worsen reopens or CSAT. No percentage improvement target is presented as achieved.

## Risks and unresolved decisions

Self-reported room numbers do not verify hotel identity. Guests may prefer WhatsApp/phone/reception. Department routing and SLA durations are portfolio assumptions requiring hotel approval. Reconstructed screens require staff usability testing. One SQLite file is suitable for a small demonstrator, not a multi-property fleet. Define guest-data retention and staff onboarding before any personal-data pilot.
