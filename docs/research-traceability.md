# Evidence → requirements → delivered behavior → verification

**Status:** 2026 editorial traceability reconstruction. Evidence comes from the 2024 thesis and preserved code; the chain is not proof that a feature caused a measured hotel improvement. T1 refers to the thesis PDF page numbers. Requirement/story IDs are defined in [requirements](requirements.md) and [user-stories](user-stories.md).

| ID / thesis evidence | Interpretation / design artifact | Requirement and story | Delivery classification / behavior | Technical verification | Field validation still needed |
| --- | --- | --- | --- | --- | --- |
| E01: requests lost or forgotten, pp. 25-26 | AS-IS handoff; Blueprint backstage coordination | BR-01, FR-02, US-02 | Original intake + new durability: stable ID, atomic request/event save, duplicate protection | `test_domain`, offline `test_bot` | Observe missed requests / repeat contacts before and after adoption |
| E02: inefficient allocation and manual responsibility, pp. 19-20, 25-26 | Fishbone process causes; stakeholder ownership | BR-02, FR-03/05, US-04 | Thesis assignment design reconstructed: department routing and eligible staff assignment | `test_domain`, staff browser workflow | Validate department taxonomy, shifts, escalation and actual handoff time |
| E03: room-phone and reception friction, p. 25 | CJM service-request moment; Affinity communication cluster | BR-04, FR-01/02, US-01/02 | Original Telegram intake; new validated adapter and saved confirmation | `test_bot`, `test_domain` | Unassisted completion, real guest channel preference, language needs |
| E04: delays and weak completion visibility, pp. 17-20, 42-45 | Blueprint; original sequence/state design | BR-03, FR-06/07/09, US-05/06/08 | Original lifecycle intent + new enforcement: acknowledgement, progress, resolution, reopening, history and guest lookup | `test_domain`, `test_web`, `test_bot`, browser workflow | Staff status semantics, guest comprehension and correspondence with physical fulfillment |
| E05: leadership lacks a complete daily picture, p. 25 | Stakeholder matrix; reporting ambition | BR-05, FR-10, US-10 | New analytics module: defined cohorts, timing, SLA, completion, reopen and CSAT | `test_analytics`, `test_sql`, analytics browser check | Data quality, decision usefulness and comparable operational baseline |
| E06: historical satisfaction/effort reporting, pp. 15-17 | Survey aggregates; feedback opportunity | FR-09/10, US-09/10 | Historical aggregates preserved separately; new per-request rating with explicit eligibility | `test_bot`, `test_domain`, `test_analytics` | Recover question/scale details; investigate rating nonresponse; no before/after claim |
| E07: technology/data-access and integration problems, pp. 19-20 | Fishbone technology branch; component model | NFR-R1/R2, FR-11, US-11 | Revised original integration: SQLite authority and optional safe Sheets export | `test_domain`, `test_sheets` failure adapter checks | Newly issued credentials and live external acceptance; no hotel-system integration claimed |
| E08: staff skills, motivation and physical layout, pp. 17-20, 25 | Affinity non-product themes; Fishbone people/environment | Pilot dependencies in BRD and roadmap | Outside software scope: training, incentives, equipment and workspace interventions | No software test can validate these interventions | Management-led change and observational research |

## Read one complete decision

**E01 / lost request context.** The thesis describes lost or forgotten requests. AS-IS and the Blueprint make the manual handoff visible. A durable central record is a reasonable product hypothesis, expressed as BR-01 / FR-02 / US-02. The rebuilt implementation verifies persistence before confirming success and avoids duplicate records for a repeated source reference. Automated checks support those behaviors. They do **not** show that the hotel missed fewer requests; that needs a real workflow baseline and pilot.

## Original design versus current implementation

| Model | Original thesis scope | Surviving code boundary | Current representation / change |
| --- | --- | --- | --- |
| Use Case | Guest, reception/department staff and analyst; authorization and request work, pp. 35-37 | Guest registration and request creation; lost AppSheet cannot be rerun | Explicit manager/agent/analyst roles; limited own-request guest lookup; no verified stay identity |
| Class | Guest, room, task, employee, department and their operations, pp. 37-40 | Denormalized users/guests/tasks schema; no original DB file supplied | Logical entities separated from physical schema; events and versioning added; no reservations engine |
| Activity | Guest/system/reception/department processing, pp. 40-42 | Original bot intake only independently inspectable | Validation, atomic save failure and enforced staff steps added |
| Sequence | Guest authorization, create, notify, assign and fulfill, pp. 42-43 | Proactive notifications are not established by surviving handlers | Save-before-confirmation and versioned updates; original notification ambition remains planned |
| State | Created, accepted, in progress, completed, cancelled and reopened, pp. 43-45 | Bot writes `Incompleted`; conceptual states differ across artifacts | Defined transitions, reasons and timestamps implemented; detailed states are an original design idea |
| Component | UI, authorization, request/task/employee/notification services and DB, pp. 45-48 | Bot, SQLite and Google Sheets integration | Lean adapters/domain/database/metrics/export; no unnecessary microservices |
| Deployment | Client, web and database service nodes, pp. 48-53 | Python service deployment file exists; full historic deployment not tested | Two Python processes on one host; separate GitHub Pages synthetic preview |
| ERD | Seven AppSheet logical entities and relationships, pp. 64-68 | Actual bot schema differs from the conceptual ERD | Normalized operational schema with foreign keys, history and sessions |

## How claims are classified

**Original:** documented in the thesis/source. **Reconstructed:** a new English view based on evidence. **New:** delivered in the portfolio rebuild. **Planned:** absent from the current release. Many chains contain more than one classification; the origin of an idea is separate from the date its implementation was verified.

**Thesis-reported** does not mean independently recomputed; **implemented** does not mean tested with real guests; **technically checked** does not mean production ready; **expected impact** is a hypothesis. The 182 survey responses and 96 synthetic demo requests belong to different datasets and cannot be joined or compared as a treatment/control study.
