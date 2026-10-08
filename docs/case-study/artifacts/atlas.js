"use strict";

const filters = [...document.querySelectorAll("[data-filter]")];
const artifacts = [...document.querySelectorAll(".artifact")];
const count = document.getElementById("artifact-count");
for (const button of filters) {
  button.addEventListener("click", () => {
    const group = button.dataset.filter;
    for (const filter of filters) filter.setAttribute("aria-pressed", String(filter === button));
    for (const artifact of artifacts) artifact.hidden = group !== "all" && artifact.dataset.group !== group;
    const visible = artifacts.filter(artifact => !artifact.hidden).length;
    count.textContent = `${visible} artifacts shown`;
  });
}

const dialog = document.getElementById("diagram-dialog");
const canvas = document.getElementById("diagram-canvas");
let trigger;
for (const button of document.querySelectorAll("[data-diagram]")) {
  button.addEventListener("click", () => {
    trigger = button;
    const artifact = button.closest(".artifact");
    const drawing = button.querySelector("svg").cloneNode(true);
    const marker = drawing.querySelector("marker");
    const originalId = marker.id;
    marker.id = `zoom-${originalId}`;
    for (const edge of drawing.querySelectorAll("[marker-end]")) {
      edge.setAttribute("marker-end", `url(#${marker.id})`);
    }
    canvas.replaceChildren(drawing);
    canvas.scrollLeft = 0;
    canvas.scrollTop = 0;
    document.getElementById("diagram-title").textContent = artifact.querySelector("h2").textContent;
    document.getElementById("diagram-context").textContent = [...artifact.querySelectorAll(".artifact-reading > div")]
      .map(part => `${part.querySelector("dt").textContent}: ${part.querySelector("dd").textContent}`)
      .join(" ");
    dialog.showModal();
    document.body.style.overflow = "hidden";
  });
}
dialog.addEventListener("close", () => {
  document.body.style.overflow = "";
  canvas.replaceChildren();
  if (trigger) trigger.focus();
});
dialog.addEventListener("keydown", event => {
  if (event.key !== "Tab") return;
  const controls = [...dialog.querySelectorAll("button, [tabindex='0']")];
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
// A deep link exposes its group, even after using a filter in the same tab.
function exposeLinkedArtifact() {
  const target = artifacts.find(artifact => `#${artifact.id}` === location.hash);
  if (target && target.hidden) filters.find(button => button.dataset.filter === "all").click();
}
window.addEventListener("hashchange", exposeLinkedArtifact);
exposeLinkedArtifact();
