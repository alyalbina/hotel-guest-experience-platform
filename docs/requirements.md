# Functional and non-functional requirements

**Provenance:** T1 pp. 26–31 use FURPS+ and broader integration/availability ambitions. The following narrows those ambitions to a verifiable local portfolio release. IDs/thresholds here are reconstructed or new specifications, not original verbatim requirements.

## Functional traceability

| ID | Requirement | Origin | Story / implemented component |
| --- | --- | --- | --- |
| FR-01 | Register one guest per Telegram identity with validated room/name | Original + new constraints | US-01; bot/service/schema |
| FR-02 | Capture catalog category/service/details with durable request ID | Original + new idempotency | US-02; service transaction |
| FR-03 | Route by category to department | Thesis requirement; new routing configuration | US-02; catalog |
| FR-04 | Filter queue by status, department, search and created dates | AppSheet reconstruction + new dates | US-03; API and UI |
| FR-05 | Assign eligible staff and record ownership | Thesis use case; reconstruction | US-04; service |
| FR-06 | Enforce explicit status transitions and reasons | Expanded from original status | US-05; TRANSITIONS |
| FR-07 | Preserve timed request history and reject stale updates | New | US-06; events/version |
| FR-08 | Authenticate staff and restrict permissions | New concrete implementation | US-07; web/security |
| FR-09 | Let guests retrieve their own status and submit CSAT | New | US-08/09; bot/service |
| FR-10 | Calculate requested operational metrics with cohort filters | Thesis reporting ambition; new module | US-10; analytics/SQL |
| FR-11 | Export an optional safe Sheets snapshot | Revised original integration | US-11; sheets CLI |
| FR-12 | Ship a no-install synthetic preview | New | US-12; preview builder |

## FURPS+ for this release

| Area / ID | Requirement and acceptance boundary | Status |
| --- | --- | --- |
| Functionality / NFR-F1 | Every staff read/mutation checks session and department/role | Implemented and tested |
| Usability / NFR-U1 | Browser workspace usable at 390px and 1440px without page overflow; labels and textual status indicators | Browser-tested at those sizes |
| Usability / NFR-U2 | Full keyboard focus containment, screen-reader audit, WCAG conformance and multilingual UI | Planned; no certification claim |
| Reliability / NFR-R1 | Request + event are committed/rolled back together; duplicate update source does not double-create | Implemented and tested |
| Reliability / NFR-R2 | Sheets outage must not block local intake | Implemented separation; adapter failure tested |
| Reliability / NFR-R3 | Durable unfinished conversation state, automated backups and recovery drill | Planned; saved requests already persist |
| Performance / NFR-P1 | Bot sync database work must not block the async event loop; page must demonstrate 96 synthetic requests | Implemented; no formal throughput/p95 benchmark |
| Performance / NFR-P2 | Defined concurrent-user load and p95 response-time budget for a real pilot | Planned, not established by screenshots |
| Supportability / NFR-S1 | Explicit setup, pinned direct dependencies, audited transitive constraints and CI workflow | Implemented; GitHub CI execution pending publication |
| Supportability / NFR-S2 | Fresh imports need no Google credentials or Telegram token for the panel | Implemented and tested |
| Additional / NFR-A1 | Public tree contains no original credentials/database/PDF; data is synthetic and labeled | Publication gate plus manual inspection |
| Additional / NFR-A2 | UTC timestamps, stable IDs, FK/status checks and stale-version conflicts | Implemented and tested |
| Additional / NFR-A3 | Verified hotel identity, approved retention and private HTTPS hosting | Planned deployment requirements |

Thesis requirements such as CRM/ERP integration, high availability, horizontal scaling and multiple languages are not silently counted as implemented. The new prototype deliberately favors a reviewable, small architecture.
