"use strict";

const repository = "https://github.com/alyalbina/hotel-guest-experience-platform";

// Editorial reconstructions of the documented reasoning, not interview quotes.
const findings = {
  context: {
    title: "Keep the request intact.",
    finding: "Requests can be lost during manual departmental handoffs.",
    pain: "Guests repeat information; staff receive incomplete context.",
    hypothesis: "A shared, durable record may reduce missed or repeated requests.",
    design: "Persist a request ID and timestamped event history; confirm only after saving.",
    outcome: "More traceable service. Validate missed requests and repeat contacts in a pilot.",
    boundary: "Implemented in the 2026 rebuild. The operational improvement remains unvalidated.",
    source: "/blob/main/docs/user-stories.md",
  },
  ownership: {
    title: "Make responsibility explicit.",
    finding: "Manual handoffs obscure which department and employee should act.",
    pain: "Staff need actionable details and an identifiable owner.",
    hypothesis: "Department routing and visible assignment may reduce handoff ambiguity.",
    design: "Route by category; let staff assign an eligible employee; enforce department and role scope.",
    outcome: "Clearer ownership. Test routing accuracy, staff task completion and handoff delays.",
    boundary: "Assignment workflow reconstructed; enforced roles are new in 2026. Shift and escalation procedures remain pilot work.",
    source: "/blob/main/docs/brd.md",
  },
  access: {
    title: "Reduce the effort to ask.",
    finding: "Room-phone, language and reception friction complicate asking for service.",
    pain: "Guests want to submit a clear request from the room and know what happens next.",
    hypothesis: "Structured messaging and retrievable status may reduce repeat contacts and guest effort.",
    design: "Telegram category/service intake, saved confirmation and an own-request status command.",
    outcome: "A simpler request journey. Test unassisted task completion and actual channel preference.",
    boundary: "Telegram intake is the original concept. Status lookup is new. Market adoption and live delivery are not validated.",
    source: "/blob/main/docs/customer-journey.md",
  },
  visibility: {
    title: "Give managers a usable operating view.",
    finding: "Managers lack a consistent picture of service demand, delays and completion.",
    pain: "A ticket count alone cannot show whether the team responds or resolves work well.",
    hypothesis: "Explicit timing and quality metrics may support better service-process decisions.",
    design: "A creation-cohort dashboard, SQL definitions and visible eligibility/denominator rules.",
    outcome: "More informed review. Validate data quality, decision usefulness and service outcomes in a pilot.",
    boundary: "The analytics module is new in 2026. Its demonstrated values are synthetic, not measured hotel performance.",
    source: "/blob/main/docs/metrics.md",
  },
};

// Values checked against app.analytics.compute_metrics on the preserved demo.
// Fixed sample: 96 synthetic requests, anchor 2026-10-08T18:00:00Z.
const metrics = {
  response: {
    question: "How long until staff acknowledge a request?",
    formula: "Mean time from creation to first staff acknowledgement, across 89 acknowledged requests.",
    caveat: "Unacknowledged requests are excluded. Bot confirmation and assignment do not count as staff response.",
  },
  resolution: {
    question: "How long does the complete service cycle take?",
    formula: "Mean time from creation to latest resolution, across 68 currently resolved requests.",
    caveat: "Includes reopen cycles. Unfinished work is excluded, so read overdue active workload alongside this mean.",
  },
  sla: {
    question: "Which completed requests met their service deadline?",
    formula: "Currently resolved within the snapshotted resolution threshold / all 68 currently resolved requests × 100.",
    caveat: "The thresholds are demo assumptions. This closed-only metric excludes unfinished breaches; 25 active demo requests are overdue.",
  },
  completion: {
    question: "What share of the intake is currently resolved?",
    formula: "68 currently resolved requests / all 96 requests in the creation cohort × 100.",
    caveat: "Cancelled requests stay in the denominator. Reopened requests no longer count as currently complete.",
  },
  reopen: {
    question: "How often did a resolved request need more work?",
    formula: "Ever-resolved requests reopened at least once / 69 ever-resolved requests × 100.",
    caveat: "Each request counts once, regardless of repeated reopens. Reopen reasons need review before inferring poor service.",
  },
  csat: {
    question: "How do responding guests rate the resolved service?",
    formula: "Mean current 1–5 score from 43 rated, currently resolved requests; demo feedback coverage is 63.2%.",
    caveat: "A mean is not a satisfied-response percentage. Response selection matters; reopening clears the current score.",
  },
};

function renderFinding(key, button) {
  const data = findings[key];
  document.getElementById("decision-title").textContent = data.title;
  for (const field of ["finding", "pain", "hypothesis", "design", "outcome", "boundary"]) {
    document.getElementById(`decision-${field}`).textContent = data[field];
  }
  document.getElementById("decision-source").href = repository + data.source;
  document.getElementById("decision-panel").setAttribute("aria-labelledby", button.id);
}

function renderMetric(key, button) {
  const data = metrics[key];
  for (const field of ["question", "formula", "caveat"]) {
    document.getElementById(`metric-${field}`).textContent = data[field];
  }
  document.getElementById("metric-panel").setAttribute("aria-labelledby", button.id);
}

function activateTab(button, tabs) {
  for (const tab of tabs) {
    const selected = tab === button;
    tab.setAttribute("aria-selected", String(selected));
    tab.tabIndex = selected ? 0 : -1;
    if (tab.dataset.tab) {
      document.getElementById(tab.getAttribute("aria-controls")).hidden = !selected;
    }
  }
  if (button.dataset.finding) renderFinding(button.dataset.finding, button);
  if (button.dataset.metric) renderMetric(button.dataset.metric, button);
}

// WAI-style automatic activation: arrows, Home/End and a single Tab stop.
for (const list of document.querySelectorAll('[role="tablist"]')) {
  const tabs = [...list.querySelectorAll('[role="tab"]')];
  for (const tab of tabs) {
    tab.addEventListener("click", () => activateTab(tab, tabs));
    tab.addEventListener("keydown", (event) => {
      const current = tabs.indexOf(tab);
      let next;
      if (["ArrowRight", "ArrowDown"].includes(event.key)) next = (current + 1) % tabs.length;
      if (["ArrowLeft", "ArrowUp"].includes(event.key)) next = (current - 1 + tabs.length) % tabs.length;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      activateTab(tabs[next], tabs);
      tabs[next].focus();
    });
  }
}

const menu = document.querySelector(".menu-toggle");
const pageNav = document.getElementById("page-nav");
function closeMenu() {
  document.body.classList.remove("menu-open");
  menu.setAttribute("aria-expanded", "false");
}
menu.addEventListener("click", () => {
  const open = menu.getAttribute("aria-expanded") !== "true";
  document.body.classList.toggle("menu-open", open);
  menu.setAttribute("aria-expanded", String(open));
});
pageNav.addEventListener("click", (event) => {
  if (event.target.closest("a")) closeMenu();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && menu.getAttribute("aria-expanded") === "true") {
    closeMenu();
    menu.focus();
  }
});

const dialog = document.getElementById("image-dialog");
const expandedImage = document.getElementById("expanded-image");
for (const button of document.querySelectorAll("[data-zoom]")) {
  button.addEventListener("click", () => {
    expandedImage.src = button.dataset.zoom;
    expandedImage.alt = button.querySelector("img").alt;
    document.getElementById("image-caption").textContent = button.dataset.caption;
    dialog.showModal();
    document.body.style.overflow = "hidden";
  });
}
dialog.addEventListener("close", () => {
  document.body.style.overflow = "";
  expandedImage.removeAttribute("src");
});
dialog.addEventListener("keydown", (event) => {
  if (event.key !== "Tab") return;
  const controls = [...dialog.querySelectorAll("button, a[href], [tabindex='0']")]
    .filter((element) => !element.disabled && element.getClientRects().length);
  const first = controls[0];
  const last = controls[controls.length - 1];
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
});
dialog.addEventListener("click", (event) => {
  if (event.target !== dialog) return;
  const bounds = dialog.getBoundingClientRect();
  if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) {
    dialog.close();
  }
});

const navLinks = [...pageNav.querySelectorAll('a[href^="#"]')];
const progress = document.querySelector(".read-progress span");
let queued = false;
function updateReadingPosition() {
  const length = document.documentElement.scrollHeight - window.innerHeight;
  progress.style.width = `${length > 0 ? Math.min(100, Math.max(0, window.scrollY / length * 100)) : 0}%`;
  let current;
  for (const link of navLinks) {
    const section = document.querySelector(link.getAttribute("href"));
    if (section.getBoundingClientRect().top < window.innerHeight * 0.35) current = link;
  }
  for (const link of navLinks) {
    if (link === current) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  }
  queued = false;
}
function scheduleReadingPosition() {
  if (!queued) {
    queued = true;
    requestAnimationFrame(updateReadingPosition);
  }
}
window.addEventListener("scroll", scheduleReadingPosition, { passive: true });
window.addEventListener("resize", () => {
  if (window.innerWidth > 760) closeMenu();
  scheduleReadingPosition();
});
updateReadingPosition();
