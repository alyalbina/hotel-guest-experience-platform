# Product case study: design, evidence and quality report

Validation date: 8 October 2026 (UTC). This report covers the new static portfolio page and regression checks on the existing product.

**Case study:** https://alyalbina.github.io/hotel-guest-experience-platform/case-study/  
**Interactive product demo:** https://alyalbina.github.io/hotel-guest-experience-platform/demo/  
**CV, LinkedIn Featured / Projects and interview copy:** [portfolio.md](portfolio.md)

## Published review

The live case study was opened and checked on GitHub Pages. Decision, Blueprint and SLA controls updated correctly; screenshot enlargement closed with Escape; the demo button opened the existing preview with 96 fictional requests. No site-origin console warnings or errors were observed.

Changes are in **`feat-product-case-study`**, with [Pull Request #1](https://github.com/alyalbina/hotel-guest-experience-platform/pull/1). GitHub Pages serves that branch's `/docs` folder for review; `main` was not changed. The downloaded feature-branch archive contained **91 files**, byte-identical to the prepared public worktree at commit `0ef78f4` (before this report's publication note).

[CI run #10](https://github.com/alyalbina/hotel-guest-experience-platform/actions/runs/37851920032) passed with the new case-study smoke step. [Pages deployment #4](https://github.com/alyalbina/hotel-guest-experience-platform/actions/runs/37852034091) passed. The PR showed 13 successful checks and no conflicts before this documentation-only publication note; current status remains available on the PR.

## Design and implementation

The page uses an editorial grid, large typography, a restrained green/paper palette and actual application screenshots. It starts with the product, then connects research with decisions, service/system models, implementation and measurement. A short reading path helps a recruiter scan the strongest evidence in two minutes.

Plain HTML, CSS and JavaScript are sufficient for this content. The page has no build step, third-party scripts, web fonts, tracking, paid APIs, account requirement or backend connection. It reuses the existing screenshots and links to the original source documents. Secondary screenshots load lazily. GitHub Pages serves it from `docs/case-study/`; the existing `docs/demo/` remains a separate interactive product preview.

Interactive elements include four finding-to-decision explanations, four service/system artifact views, guest/staff scenarios, six metric definitions, historical research disclosure, screenshot zoom and a responsive navigation menu. Tab groups support arrow keys, Home and End. The image dialog supports Escape, a focus loop and focus restoration. A skip link, visible focus styling and reduced-motion preference are included.

## Evidence boundaries

| Page content | Source and treatment |
| --- | --- |
| 182 completed questionnaires, qualitative work and reported service problems | [Research](research.md); thesis-reported, not revalidated. No respondent distributions or interview counts were invented. |
| Historical NPS, CSAT and CES | Collapsed disclosure; preserved units and missing calculation/scale details. Not compared with synthetic metrics. |
| Finding → hypothesis → decision → expected outcome | [PRD](prd.md), [BRD](brd.md), [processes](processes.md); the causal trace is an editorial reconstruction, not a tested causal effect. |
| CJM, Blueprint, process views, architecture | English reconstructions supported by existing [CJM](customer-journey.md), [Blueprint](service-blueprint.md), [architecture](architecture.md), [ERD](data-model.md) and [UML](uml.md). Not claimed to be surviving original diagram files. |
| Product screenshots | Actual reconstructed web application. The guest flow is explicitly a representation, not a captured live Telegram conversation. |
| 2024 and 2026 contribution | [Provenance](provenance.md); original bot attribution is retained, and the rebuild names AI engineering assistance. |
| Hotel impact | Hypotheses only. No production rollout, financial gain or measured guest improvement is claimed. |

## Synthetic analytics

The public preview contains **96 fictional requests** with a fixed demonstration clock. These records are unrelated to the 182 survey respondents. The page uses the same definitions as [metrics.md](metrics.md) and the existing analytics code.

| Metric | Demo value | Eligibility |
| --- | --- | --- |
| Average response time | 12.1 min | 89 acknowledged requests; from creation to first human acknowledgement |
| Average resolution time | 122.8 min | 68 currently resolved requests; from creation to latest resolution |
| SLA compliance | 39.7% | Currently resolved requests within their snapshotted category threshold; open work excluded |
| Completion rate | 70.8% | 68 currently resolved / 96 created requests |
| Reopen rate | 10.1% | Ever-reopened requests / 69 ever-resolved requests |
| CSAT | 3.9 / 5 | 43 rated currently resolved requests; rating coverage 63.2% |

Active overdue requests are a separate guardrail. SLA values are demo assumptions. Synthetic results illustrate a measurement system, not service performance at Novotel or another hotel.

## Executed checks

| Check | Result |
| --- | --- |
| Existing Python/domain/API/analytics tests | **34 passed**; app coverage **89.67%**, above the configured 85% floor |
| Existing browser workflow | Passed: sign-in, filtering, assignment, state changes, history, analytics and browser-only preview |
| Case-study HTML references | **61** asset, document, anchor and control references verified against the repository |
| Responsive layout | Checked at **320, 390, 768, 1024 and 1440 px**; no document overflow, including alternate artifact views |
| Interactive content | Decision, artifact, scenario and metric tabs, historical disclosure and every screenshot zoom passed |
| Keyboard behavior | Tab navigation, tab-group keys, mobile-menu Escape, dialog focus loop and return passed |
| Reduced motion | Confirmed automatic rather than smooth scroll under the preference |
| Runtime resources | No JavaScript exceptions or HTTP resource failures in the local case-study smoke check |
| Existing demo CTA | Opens the working preview with all 96 synthetic requests |
| Visual review | Desktop/mobile hero and research, decisions, models, product, analytics and contribution sections inspected |

Ruff checks, Python formatting and JavaScript syntax are part of the local release gate. GitHub Actions adds the new case-study browser check to the existing workflow, alongside Python 3.11/3.12/3.13 checks and dependency inspection. The page describes coverage as approximately 90%; coverage is a code metric, not a product-quality or hotel-impact score.

Reproduce locally:

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
pytest -q --cov=app --cov-fail-under=85
ruff check .
ruff format --check .
node --check docs/case-study/case-study.js  # optional syntax check; Node is not needed to run the site
python scripts/check_public_tree.py
python scripts/browser_smoke.py
python scripts/case_study_smoke.py
```

The new smoke script serves `docs/` on a temporary local port and stops it after the check. `CHROMIUM_EXECUTABLE` can specify an existing Chromium installation. `CASE_STUDY_ARTIFACT_DIR` optionally retains visual-review screenshots and the JSON result.

## Limits and next checks

- Automated checks used Chromium. Safari, Firefox, real phone devices, screen-reader testing and a complete automated accessibility audit have not been performed.
- Local source-link checks verify destinations in the repository; they do not replace checking the final deployed page and GitHub links.
- Contrast and keyboard behavior were reviewed, but no formal WCAG certification or external accessibility audit is claimed.
- No measured Lighthouse score, load-test result or performance benchmark is claimed. The site avoids third-party network dependencies and reuses local image assets.
- Live Telegram delivery and Google Sheets authentication still need newly issued credentials and external acceptance checks. The portfolio page does not connect to those services.
- No real hotel pilot or employer/recruiter usability test has been completed. Adoption, handoff delays, guest satisfaction and operational effects require a baseline and a controlled pilot.
- A LinkedIn profile URL was not supplied, so the footer does not invent one. The prepared Featured and Projects copy is available in `portfolio.md`.

The changes are prepared in a separate branch and pull request. Publication can use that branch's `docs/` folder for review; merging into `main` remains a user-controlled decision. After a merge, GitHub Pages can return to `main` without changing the public URLs.
