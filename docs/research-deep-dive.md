# Research and service-design deep dive

**Author / context:** Albina Urubkina, Business Informatics, HSE University, 2024. Novotel Moscow is the thesis case context, not a current client or product endorsement.

**Treatment:** English reconstruction of the preserved thesis. T1 means the 84-page PDF privately reviewed for this project; PDF and printed page numbering align. The original editable research boards, respondent-level dataset and interview transcripts were not supplied. This document adds interpretation and traceability in 2026, without representing them as a new field study.

**Visual companion:** [Research & Analysis Atlas](https://alyalbina.github.io/hotel-guest-experience-platform/case-study/artifacts/) contains 16 readable, labelled diagrams. [Evidence-to-requirement register](research-traceability.md) explains how findings became scope, requirements and verification.

## 1. Discovery question and scope

The thesis asks how a customer-centric service could improve the hotel guest experience using service design. Its discovery is broader than the software: room comfort, information, staff professionalism, booking, arrival, fulfillment and feedback all appear. The portfolio's MVP narrows this to **guest service requests and the departmental work behind them**.

This narrowing matters: a digital request queue can retain context and make responsibility visible. It cannot repair Wi-Fi, change workspace layout, train employees or guarantee physical service quality.

## 2. Research design and evidence available

| Method / T1 source | What was done or described | Role in discovery | Preserved evidence / limits |
| --- | --- | --- | --- |
| Desk research, pp. 11-14 | Hospitality literature, service practices and online-review analysis | Identify a broad opportunity space and recurring service problems | Narrative and citations; no independently reusable review corpus or coded sample |
| Guest interviews, pp. 14-15 | Interviews across guest segments, in person or by video; topics included room comfort, service quality, accessibility and staff professionalism | Explain the guest experience behind aggregate satisfaction | Interview method and synthesis artifacts; achieved count, guide, recordings and transcripts unavailable |
| Survey, pp. 15-17 | Questionnaire with closed and open questions; **182 completed questionnaires** reported | Summarize perceived guest experience | Sample count and historical aggregates; raw rows, response dates and sampling frame unavailable |
| Affinity synthesis, p. 17 | Grouped observations into four original clusters | Organize reported problems and separate opportunity areas | Embedded diagram and prose inspected; original sticky-note sources and coding decisions unavailable |
| CJM, p. 18 | Broad six-stage guest journey | Locate friction and choose the request portion for the MVP | Embedded map and narrative; emotions/persona thoughts are interpreted, not measured or verified quotations |
| Service Blueprint, p. 19 | Customer, frontstage, backstage and support layers | Connect guest friction to coordination behind the visible service | Embedded diagram inspected; no timing observations or validated service standard |
| Fishbone, pp. 19-20 | Delay causes grouped into people, process, technology and infrastructure | Identify product levers and non-product dependencies | Hypothesized root-cause model; not causal proof |

The thesis mentions an intended 5-8 interview respondents per key segment. This is a sampling intention, not a confirmed completed total. No demographic distribution, confidence interval, correlation, saturation claim or theme frequency is inferred.

## 3. Historical quantitative reporting

| Metric | Thesis value | What can be said | What cannot be established |
| --- | --- | --- | --- |
| NPS | **-2.34** | This is the value reported as an "average" in T1 pp. 15-17 | Promoter/detractor counts, correct NPS calculation, confidence interval and denominator |
| CSAT | **3.02 / 5** | Reported mean satisfaction rating | Satisfied-response percentage or comparable operational CSAT |
| CES | **3.48 / 7** | Reported mean effort score | Meaning of high/low values without original question wording and scale anchors |

The source contains a metric illustration, but respondent-level counts cannot be recovered reliably. The portfolio therefore retains the reported aggregates and does not redraw invented distributions. These are historical research values, separate from the **96 fictional operational requests** in the product demo.

## 4. Affinity Diagram: preserve the original synthesis

The original board's headings are translated below. They replace the earlier portfolio's four editorial theme labels, which were useful product summaries but did not reproduce the source grouping.

| Original cluster / translated heading | Source-supported summary | Product interpretation | Intervention boundary |
| --- | --- | --- | --- |
| Information and communication | Incomplete or inconsistent information and friction communicating with staff | Structured catalog, actionable details and a retrievable request record | Channel choice and multilingual adoption need fresh validation |
| Room amenities | Room comfort, Wi-Fi and facilities contribute to perceived service | Let guests report the issue and route it to a team | Infrastructure upgrades are not delivered by the app |
| Stay conditions | Booking friction, delays and service quality affect the stay | Concentrate the prototype on the request-handling problem | Reservations, billing and the entire stay are outside scope |
| Staff skills | Knowledge, communication and professionalism matter | Make ownership and task context explicit | Training, incentives and staffing remain operational work |

Summaries are reconstructed from the diagram headings and thesis narrative. They are not verbatim respondent quotes or an exhaustive translation of each sticky note. The artifact supports opportunity framing; it does not prove which problem affects the most guests.

## 5. CJM: why the MVP has a narrow boundary

The original map follows **booking → check-in → stay → requesting personalized service → check-out → review**. It includes guest steps, goals, thoughts, emotions, problems and opportunities. The complete English table is in [customer-journey.md](customer-journey.md); the atlas renders its six stages visually.

The request stage combines communication friction, delays and missed details. This is where a traceable intake and staff queue have a direct product role. Arrival and checkout pain remain visible in the research, but they do not become falsely "implemented" booking/payment features. Persona thoughts are summarized as interpreted experience, not presented as interview quotations.

## 6. Blueprint: what the guest cannot see

The broad source blueprint connects booking, arrival, services, departure and review with physical/digital evidence, guest actions, frontstage staff, backstage operations and support processes. The product reconstruction focuses on **capture → triage/assign → fulfill → follow up**, documented in [service-blueprint.md](service-blueprint.md).

This model supports two distinctions. First, reception accepting an input and a department physically fulfilling it are different responsibilities. Second, a bot's saved confirmation is different from a human response. The current platform therefore records durable capture, staff acknowledgement and resolution separately. A timestamp only reflects service if staff follow agreed procedures.

## 7. Fishbone: causes software can and cannot address

The visually inspected source lists the following causes (T1 p. 20):

| Category | Translated causes | Response in the portfolio |
| --- | --- | --- |
| People | Insufficient staff qualifications; communication barriers; lack of motivation | Clear context and responsibility can support staff; training and motivation need operational interventions |
| Organizational processes | Inefficient task allocation; missing standardization; system-integration problems | Department routing and assignment; explicit lifecycle; integration remains limited |
| Technology | Problems accessing data; lack of automation; outdated software/equipment | Shared operational record and analytics; no claim to modernize hotel equipment |
| Environment and infrastructure | Organizational culture; inconvenient workspace layout | Retained as dependencies outside the software scope |

The wording "root cause" describes the thesis analysis technique. None of these relationships was established through a controlled causal study. See the atlas for the translated fishbone and [roadmap](roadmap.md) for further validation.

## 8. From discovery into business and system analysis

| Artifact | Question answered | Source and adaptation |
| --- | --- | --- |
| Stakeholder matrix | Who sponsors, approves, operates and experiences the change? | T1 pp. 23-24; qualitative influence/interest matrix and [BRD](brd.md) |
| AS-IS | Where are manual handoffs, abandonment and repeat contacts? | T1 pp. 24-26; [process mapping](processes.md) |
| TO-BE | How should a request reach staff with enough context? | T1 pp. 40-43 and 64-73; original Telegram/Sheets/AppSheet concept distinguished from the current rebuild |
| FURPS+ | What does the service need beyond a happy-path feature list? | T1 pp. 27-31; [requirements](requirements.md), with new concrete controls and planned pilot checks |
| Seven UML types | What capabilities, responsibilities, relationships and runtime interactions form the solution? | T1 pp. 35-53; current editable [UML sources](uml.md) and eight system/data atlas views |
| ERD / AppSheet structure | Which records and relationships support the staff workflow? | T1 pp. 64-68; [original/current mapping](data-model.md) |

The original UML already describes rich request states, authorization, notifications and reopening. The preserved Python bot demonstrates less: it creates `Incompleted` tasks. The portfolio distinguishes **original design intent**, **surviving implementation** and **new enforced behavior**; it does not claim these ideas first appeared in 2026.

## 9. Contribution and an interview reading path

Albina's thesis contribution includes research, synthesis, service design, stakeholder/process analysis, requirements, UX/system models and prototype-project coordination. The original bot credits another developer, and the 2026 rebuild uses AI engineering assistance; see [provenance](provenance.md).

For a Business Analyst interview, show AS-IS, stakeholder roles and a requirement with acceptance criteria. For Product / UX interviews, show one affinity theme, the relevant CJM moment and a scope decision. For Product Analytics, explain why historical satisfaction research cannot be compared directly with synthetic operational metrics, then show the metric denominator and pilot design. These are different readings of the same evidence, not different versions of the result.

## 10. Next validation work

Recover raw research material if available; verify questionnaire wording and historical calculation methods; run new guest/staff usability sessions; confirm routing, identity and closure policies; establish a real operational baseline. Assess missed/repeated contacts, human response, resolution, overdue active requests and feedback coverage before claiming improvement. The thesis itself leaves impact testing for later (p. 74).
