# Research and product discovery

**Status:** English reconstruction of the 2024 thesis, not a new hotel study. Primary source: T1 pp. 11–21. The underlying survey dataset, recordings, transcripts and original editable boards are unavailable.

## Methods and evidence limits

| Method | What the thesis reports | What can be verified now |
| --- | --- | --- |
| Desk research | Hospitality literature and analysis of online guest reviews | Narrative and cited references in T1; no independently collected review corpus |
| Qualitative research | Interviews across guest segments; grouping with an Affinity Diagram | Method and artifacts in T1; no achieved interview count or transcripts |
| Quantitative research | 182 completed questionnaires | Stated count and summary values; no raw responses to reproduce analysis |
| Service design | CJM, Service Blueprint, Affinity and Fishbone diagrams | Embedded diagrams and prose were inspected; English artifacts are reconstructions |

The thesis discusses a planned 5–8 respondents per key segment. That is not a confirmed total number of completed interviews. Claims of statistical representativeness or causal relationships cannot be independently supported with the preserved materials.

## Historical reported measurements

| Measure | Thesis-reported value | Interpretation boundary |
| --- | --- | --- |
| NPS | -2.34 | Reported as an “average”; promoter/detractor counts and computation are missing |
| CSAT | 3.02 / 5 | Reported mean score; not a positive-response percentage |
| CES | 3.48 / 7 | Question wording and scale direction are unavailable |

These figures describe the thesis's research reporting, not a measured before/after effect. They are not imported into the operational demo. In particular, we do not infer whether a higher CES means easier or harder service without the original question and anchors.

## Themes and decisions

| Evidence theme | Guest or staff need | Decision | Confidence boundary |
| --- | --- | --- | --- |
| Delayed response and room cleaning | Know whether help is being handled | Explicit acknowledgement and service status | Theme reported; new states require usability validation |
| Requests lost in manual handoffs | Keep context and identify responsibility | Stable ID, department routing, assignee and event history | Requirements supported; improvement unmeasured |
| Friction visiting reception or using a phone | Ask for help from the room | Structured Telegram intake | Original prototype decision; Telegram adoption in target market untested |
| Staff lack service information | Make a request understandable to the receiving team | Category, subservice and free-text details together | Original catalog preserved; effectiveness untested |
| Managers lack a complete daily picture | Review workload and delays | Cohort-based operations dashboard | Reporting requirement in T1; dashboard is a new module |

## Affinity reconstruction

The visually inspected source board (T1 p. 17, Figure 2) has four groups: **information and communication**, **room amenities**, **stay conditions**, and **staff skills**. English summaries preserve those original headings without fabricating quotes or translating every sticky note. See the [deep dive](research-deep-dive.md) and [visual atlas](https://alyalbina.github.io/hotel-guest-experience-platform/case-study/artifacts/).

Access to service, execution delays, information flow and operational visibility are the portfolio's **product-level synthesis**, rather than the original affinity headings. These lenses explain which parts of the broad research map are addressed by the MVP.

## Fishbone reconstruction

The thesis organizes delay causes into people, process, technology and infrastructure (pp. 19–20). The [deep dive](research-deep-dive.md) translates all listed cause groups, and the atlas renders the fishbone. The digital product addresses task capture, handoff, status and information flow. Staff training, incentives and the physical hotel layout remain operational interventions outside application scope. A software queue alone cannot solve those causes.

## Inspect the complete research-to-delivery chain

[Research & Analysis Atlas](https://alyalbina.github.io/hotel-guest-experience-platform/case-study/artifacts/) → [research deep dive](research-deep-dive.md) → [evidence/requirement/verification register](research-traceability.md). These distinguish original design intent, preserved implementation and the current rebuild, including the fact that rich states and reopening were already designed in the thesis.

## Discovery questions for a new pilot

Can guests complete intake without staff assistance? Does the selected service reach the right department? Which fields help staff act? Will guests use Telegram in the target market? Does acknowledgement reduce repeat contacts? Do timestamps reflect actual human action rather than merely a button click?

Use observed task completion, short guest/staff interviews and a defined service-time baseline before making market or impact claims. Dubai is a target employment market for this portfolio; it is not a market already researched by the thesis.
