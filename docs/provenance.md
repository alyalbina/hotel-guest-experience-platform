# Evidence, provenance and authorship

## Sources reviewed

- **T1:** Albina Urubkina, HSE University, Business Informatics, 2024. Graduation thesis, “Development of a customer-centric service for the hotel business using service-design methodology: the case of Novotel Moscow.” Uploaded PDF: 84 pages. Page references below use PDF page numbers, which align with printed numbering.
- **C1:** Uploaded original `guestmanagerbot` archive. All 32 Python files were read and parsed. Configuration and Google credential material were inspected privately; values are not reproduced.
- **C2:** Uploaded GitHub starter archive. All 32 Python files are byte-identical to C1. It removes secret-bearing files and adds publication guidance, but does not repair runtime behavior.

The full thesis, original configuration, deployment service file, credentials and any real records are deliberately excluded from this public package. The reconstructed diagrams replace original screenshots that may contain names, contact details or identifiable portraits.

## Classification vocabulary

**Original** means present in the 2024 thesis or surviving source. **Reconstructed** means a fresh English artifact or implementation derived from that evidence; it is not the lost original file. **New** means developed for the 2026 portfolio. **Planned** means not implemented. “Described in thesis” is weaker than independently running and verifying the original system.

| Item | Classification | Evidence / boundary |
| --- | --- | --- |
| 182 questionnaires | Original, thesis-reported | T1 pp. 15–16; raw rows unavailable |
| Interviews and affinity analysis | Original, described | T1 pp. 14–17; achieved interview count and transcripts unavailable |
| Historical NPS / CSAT / CES | Original, thesis-reported | T1 pp. 15–17; calculations cannot be reproduced |
| CJM, Blueprint, Fishbone | Original artifacts; English reconstructions | T1 pp. 17–20 |
| Stakeholder matrix, AS-IS / TO-BE, FURPS+ | Original artifacts; English reconstructions | T1 pp. 23–31, 40–42 |
| Seven UML diagram types | Original artifacts; refreshed current-model sources | T1 pp. 35–53; current states/auth are new |
| AppSheet data model | Original, described; reconstructed mapping | T1 pp. 64–68 |
| AppSheet staff screens | Original, described; new web replacement | T1 pp. 69–73; AppSheet app cannot be run |
| Telegram registration and nine categories | Original code; new aiogram 3 adapter | C1 handlers, catalog and keyboard modules |
| SQLite and Sheets integration | Original code; restructured persistence/export | C1 database and utils modules |
| Staff session authentication and enforced roles | New | Current API/security/schema |
| Rich states, event history and conflict detection | New implementation | The original bot only creates `Incompleted` tasks |
| Guest status lookup and CSAT collection | New | Not demonstrated by the surviving original bot |
| SQL dashboard and synthetic operational data | New | Seed is generated, not reconstructed guest activity |
| Piloted service improvement / financial returns | Planned validation | T1 p. 74 explicitly leaves impact testing for a later stage |

## Personal contribution claims

Albina is the thesis author and may present its research, service-design work, business/system analysis and prototype project. The surviving files do not resolve the complete division of original coding work.

The new implementation is a clean rebuild with AI engineering assistance, guided by the original thesis and source. It should be presented as a reconstruction/extension, not as code independently written in 2024. Before using a CV statement about personally coding the original bot, confirm the actual contribution history.

## Research and analysis atlas

The [16-view visual atlas](https://alyalbina.github.io/hotel-guest-experience-platform/case-study/artifacts/) was redrawn in English in 2026 after reviewing the embedded thesis figures. The original affinity group headings and Fishbone causes are translated, while long research notes and persona text are summarized. CJM, Blueprint, stakeholder and process views are reconstructions; the FURPS+ view pairs the original framework with current controls. Seven UML views and the ERD describe the current system and link to editable sources or the full data model. Selected relationships are labelled as such.

The thesis already **designed** detailed request states, reopening, authorization and notifications (pp. 35-53). New state/access enforcement must not be presented as proof that these concepts were absent from the 2024 design. The preserved bot only creates `Incompleted` tasks; proactive notifications and verified hotel identity remain planned. [Research traceability](research-traceability.md) separates design intent, surviving implementation and the rebuild.

The atlas contains no original respondent records, private quotations, portrait imagery, credential-bearing screenshots or research distribution reconstructed without data. All 16 diagrams are new renderings, not surviving original editable boards.

Novotel is the thesis case context. No current partnership, brand endorsement, authorized hotel deployment or access to its production systems is claimed.
