/* An optional guided walkthrough of the same in-memory preview workflow. */
"use strict";
if (preview) document.addEventListener("DOMContentLoaded", () => {
 const id="tour-001", clock="2026-10-08T", baseline=()=>demoMetrics(window.HOTEL_DEMO.requests);
 let step=0, busy=false;
 const stages=[
  ["One request. A complete service workflow.","Follow a fictional extra-towels request from intake to the analytics dashboard. Starting restores the 96-record demo and discards earlier changes in this tab.","Start the walkthrough"],
  ["01 / Capture the context","The request keeps its guest, room, department and details. Saving creates a record; it does not mean a person has responded.","Assign housekeeping"],
  ["02 / Make ownership explicit","An eligible housekeeping employee now owns the request. Assignment alone does not start the human-response metric.","Acknowledge the request"],
  ["03 / Record a human response","Acknowledgement is recorded at 17:42 UTC: two minutes after creation. The bot's save confirmation is not counted as a staff response.","Start fulfillment"],
  ["04 / Keep progress visible","The request is in progress. Staff and managers can inspect its timestamped history; physical delivery remains an operational responsibility.","Record resolution"],
  ["05 / Close the loop","Resolution is recorded at 17:52 UTC: 12 minutes after creation. This closes a fictional request; it does not prove that a real hotel delivered towels.","See the analytical effect"],
  ["06 / Read the denominator","The dashboard recalculates from 97 fictional requests. Compare the original 96-record cohort with one added resolution. A change in these numbers is arithmetic, not evidence of hotel improvement.","Restart with fresh demo data"]
 ];
 const box=document.createElement("section");box.id="guided-demo";box.className="guided-demo";box.hidden=true;box.setAttribute("aria-labelledby","guide-title");
 document.querySelector(".page-header").after(box);
 const launcher=document.createElement("button");launcher.id="guide-launch";launcher.className="ghost guide-launch";launcher.textContent="Try the 90-second guided demo";document.querySelector(".page-header").after(launcher);
 const clear=()=>{closeDrawer();for(const field of ["search","department","start-date","end-date"])$(field).value="";status="";displayLimit=12;document.querySelectorAll("[data-status]").forEach(b=>b.classList.toggle("active",b.dataset.status===""));};
 function renderGuide(focus=false) {
  const [title,description,action]=stages[step],r=demoRows.find(r=>r.id===id),base=baseline(),after=demoMetrics(demoRows);
  const record=r?`<p class="mini-label">LIVE PREVIEW RECORD / ${esc(id)}</p><h3>${esc(r.service)}</h3>${pill(r.status)}<dl><div><dt>Responsible employee</dt><dd>${esc(r.assignee_name||"Unassigned")}</dd></div><div><dt>First human response</dt><dd>${r.responded_at?"2 minutes · 17:42 UTC":"Not recorded"}</dd></div><div><dt>Resolution</dt><dd>${r.resolved_at?"12 minutes · 17:52 UTC":"Not recorded"}</dd></div><div><dt>History</dt><dd>${r.events.length} timestamped events</dd></div></dl><button class="ghost" id="guide-history">Inspect request history</button>`:"<p class=\"mini-label\">WHAT YOU WILL SEE</p><h3>Capture → assign → acknowledge → resolve</h3><p>Then inspect the effect on the same analytics used by the staff workspace.</p>";
  const comparison=step===6?`<div class="guide-comparison"><p class="mini-label">BASELINE → AFTER THIS SCRIPTED REQUEST</p><dl><div><dt>Requests</dt><dd>${base.number_of_requests} → ${after.number_of_requests}</dd></div><div><dt>Resolved</dt><dd>${base.resolved_requests} → ${after.resolved_requests}</dd></div><div><dt>Completion</dt><dd>${base.completion_rate}% → ${after.completion_rate}%</dd></div><div><dt>Avg. response</dt><dd>${base.average_response_minutes} → ${after.average_response_minutes} min</dd></div><div><dt>Avg. resolution</dt><dd>${base.average_resolution_minutes} → ${after.average_resolution_minutes} min</dd></div></dl><p>No CSAT score is invented for this request.</p></div>`:"";
  box.innerHTML=`<div class="guide-story"><p class="eyebrow">GUIDED DEMO · SYNTHETIC DATA · ABOUT 90 SECONDS</p><h2 id="guide-title" tabindex="-1">${title}</h2><p>${description}</p>${comparison}<div class="guide-actions"><button class="primary" id="guide-next">${action}</button><button class="ghost" id="guide-reset">Restore 96 records</button><button class="ghost" id="guide-close">Close guide</button></div><p class="guide-clock">Scripted clock: 8 Oct 2026, 17:40–17:52 UTC. Clicks do not measure elapsed time. Refresh resets changes.</p><p id="guide-error" role="status"></p></div><div class="guide-record">${record}</div>`;
  $("guide-next").onclick=advance;$("guide-reset").onclick=reset;$("guide-close").onclick=()=>{box.hidden=true;launcher.hidden=false;launcher.focus();};
  if($("guide-history"))$("guide-history").onclick=()=>openRequest(id);
  if(focus)$("guide-title").focus({preventScroll:true});
 }
 async function reset() {clear();demoRows=structuredClone(window.HOTEL_DEMO.requests);step=0;selectPage("operations");await refresh();$("notification").hidden=true;renderGuide(true);}
 async function advance() {
  if(busy)return;busy=true;$("guide-next").disabled=true;
  try {
   if(step===0||step===6) {
    await reset();
    createPreviewRequest({guest_id:catalog.guests[0].id,category:"amenities",service:"Extra towels",detail:"Two extra towels, please. Fictional guided-demo request."},clock+"17:40:00Z",id);
    $("search").value=id;step=1;await refresh();
   }else if(step===5){clear();step=6;selectPage("analytics");await refresh();}
   else {
    const r=demoRows.find(r=>r.id===id),expected=[null,"new","new","acknowledged","in_progress"][step];
    if(!r||r.status!==expected||(step===1&&r.assigned_to!==null)||(step===2&&r.responded_at!==null))throw new Error("This request changed outside the guide. Restore the 96 records and restart the scenario.");
    closeDrawer();current=structuredClone(r);
    const agent=catalog.staff.find(s=>s.role==="agent"&&s.department_id===r.department_id);
    if(step===1&&!agent)throw new Error("No eligible housekeeping employee is available.");
    const payload=step===1?{assigned_to:agent.id}: {status:[null,null,"acknowledged","in_progress","resolved"][step],note:"Scripted guided-demo action"};
    const time=[null,"17:41:00Z","17:42:00Z","17:44:00Z","17:52:00Z"][step];
    if(!await updateRequest(payload,clock+time))throw new Error("The update failed. Restore the demo and try again.");
    current=null;step++;
   }
   renderGuide(true);
  }catch(error){$("guide-error").textContent=error.message;$("guide-next").disabled=false;}
  finally{busy=false;}
 }
 launcher.onclick=()=>{launcher.hidden=true;box.hidden=false;renderGuide(true);box.scrollIntoView({block:"start",behavior:"smooth"});};
 if(new URLSearchParams(location.search).get("tour")==="request"){launcher.hidden=true;box.hidden=false;renderGuide();}
});
