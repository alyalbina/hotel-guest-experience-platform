# Business Requirements Document

**Source basis:** T1 pp. 22–31 and 74–76. This is a reconstructed business specification with current implementation boundaries.

## Business problem and objectives

Manual request handling creates avoidable guest effort and weak task visibility. Establish a central request record, make service ownership visible, support repeatable handoffs and provide operational evidence for service decisions. The thesis includes ambitions and illustrative financial calculations; they are not realized benefits.

## Stakeholders

| Stakeholder | Interest | Decision/input |
| --- | --- | --- |
| Hotel leadership | Service reputation, cost and guest loyalty | Sponsor scope and approve pilot success criteria |
| Service managers | Workload visibility and consistent execution | Approve categories, routing, SLA and staff procedures |
| Reception staff | Clear intake and fewer ambiguous handoffs | Validate queue and assignment workflow |
| Department staff | Actionable tasks and clear responsibility | Validate service details and status semantics |
| Guests, including VIP guests | Accessible help and appropriate service | Test ease of intake and perceived response |
| Analyst | Trusted operational definitions | Define denominators, quality checks and cohort comparisons |

Hotel leadership, managers, staff, guests and VIP guests appear in the thesis stakeholder analysis. The analyst is specified as a system actor. This table is an adapted responsibility model, not an existing hotel org chart.

## Business requirements

| ID | Requirement | Rationale | Delivery boundary |
| --- | --- | --- | --- |
| BR-01 | Give each request a durable central identity | Reduce lost context | Implemented SQLite record |
| BR-02 | Record category, department and responsible employee | Clarify handoff | Routing implemented; individual assignment is manual |
| BR-03 | Preserve status and action history | Support service coordination | New event model implemented |
| BR-04 | Provide a low-effort guest intake channel | Reduce reception/phone friction | Original Telegram concept; adoption unvalidated |
| BR-05 | Provide service-performance reporting | Inform staffing/process review | New synthetic dashboard, not hotel outcomes |
| BR-06 | Limit access to operationally necessary data | Protect guest information | Server roles, minimal profile defaults |
| BR-07 | Fit existing operations without large setup costs | Support practical demonstration | Local Python/SQLite; optional Sheets snapshot |

## Business rules

Categories have a default department. A request snapshots its SLA threshold at creation; later configuration changes do not alter past evaluation. Eligible assignees are managers or agents in the same department. Agents can manage their department's queue; analyst accounts read only. First response means the first staff acknowledgement, not bot auto-confirmation or assignment. Reopening requires a reason and clears the current resolution and rating so follow-up quality can be rated afresh.

Catalog services represent requests, not commitments of availability, payment or booking. Emergency help is outside this system's assured capability. Reception remains a fallback channel. Demo guests, staff and SLA settings are fictional.

## Business impact model

Hypotheses: more complete intake could reduce missed requests; clear responsibility could reduce handoff delays; status visibility could reduce repeat contacts; operational review could identify persistent service gaps. Test through a hotel pilot with observed workflows and a baseline. Any labor-cost scenario should use measured task minutes, actual request volume, loaded hourly cost and adoption/maintenance costs.

The original thesis's revenue and labor-savings calculations use illustrative inputs (pp. 74–76). This portfolio does not use them as CV achievements or a validated ROI model.

## Dependencies and sign-off needed for a hotel pilot

Hotel-approved identities, service taxonomy/routing, staff procedures, SLA definitions, fallback handling, data retention and pilot measures. None is assumed approved because it was described in a thesis. Current delivery is a demonstrable portfolio package.
