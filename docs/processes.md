# AS-IS and TO-BE process mapping

**Provenance:** AS-IS is reconstructed from T1 pp. 24–26, including the visually inspected swimlane diagram. Original TO-BE comes from pp. 40–42. The current process includes new reliability/access controls and is labeled separately.

## AS-IS: manual service handling

```mermaid
flowchart TD
  Need["Guest needs help"] --> Channel{"Phone or reception?"}
  Channel -->|Phone| Call["Call reception"]
  Channel -->|In person| Visit["Visit reception"]
  Call --> Answer{"Call answered?"}
  Answer -->|No| Important{"Request still important?"}
  Important -->|Yes| Visit
  Important -->|No| Leave["Abandon request"]
  Answer -->|Yes| Intake["Reception accepts request"]
  Visit --> Intake
  Intake --> Owner{"Reception can fulfill?"}
  Owner -->|Yes| Direct["Reception performs service"]
  Owner -->|No| Handoff["Hand off to department"]
  Handoff --> Work["Department performs service"]
  Direct --> Report["Completion reported"]
  Work --> Report
  Report --> Happy{"Guest satisfied?"}
  Happy -->|No| Need
  Happy -->|Yes| End["Service complete"]
```

The model exposes abandonment, repeat contacts and manual responsibility handoffs. It does not establish how often these occurred or the measured time lost.

## Original TO-BE: thesis prototype

Guest registration/intake in Telegram → request record in Google Sheets → AppSheet staff filtering and task detail → staff assignment/status update. The thesis describes guests, rooms, employees, departments and categories. The surviving bot writes requests but does not independently demonstrate staff authentication, automatic guest progress notifications or a working reporting module. AppSheet is unavailable for rerunning.

## Current TO-BE: runnable reconstruction

```mermaid
flowchart TD
  Intake["Guest selects service and details"] --> Validate{"Input valid?"}
  Validate -->|No| Correct["Ask guest to correct input"]
  Correct --> Intake
  Validate -->|Yes| Save["Commit request and event"]
  Save --> Stored{"Committed?"}
  Stored -->|No| Retry["Explain failure; preserve form"]
  Retry --> Intake
  Stored -->|Yes| Confirm["Confirm request ID"]
  Save --> Queue["Department queue"]
  Queue --> Staff["Authenticated staff assign and acknowledge"]
  Staff --> Progress["Record service progress"]
  Progress --> Resolve["Resolve with timestamp"]
  Resolve --> Follow{"Further work needed?"}
  Follow -->|Yes| Reopen["Reopen with reason"]
  Reopen --> Progress
  Follow -->|No| Feedback["Guest checks status and rates"]
```

## Responsibility changes

| Step | AS-IS | Current prototype | Remaining operational work |
| --- | --- | --- | --- |
| Intake | Reception remembers or relays request | Validated structured record | Confirm channel adoption and check-in identity |
| Routing | Staff interpret and find department | Category supplies default department | Hotel approves taxonomy/routing |
| Ownership | Manual handoff | Explicit eligible assignee | Agree shift and escalation procedures |
| Response | Phone/reception interaction | First staff acknowledgement timestamp | Ensure button matches actual human response |
| Completion | Verbal report | Explicit state, event and resolution time | Define fulfillment quality and closure policy |
| Repeat contact | Guest asks again | Staff may reopen with reason | Guests cannot self-reopen in this version |
| Reporting | Incomplete management visibility | Defined cohort metrics | Pilot measurement and data-quality review |

The new platform records state, not physical service execution. A staff click is operational evidence only if staff follow an agreed procedure.
