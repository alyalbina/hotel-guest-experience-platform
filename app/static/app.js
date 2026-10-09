/* The static preview uses in-memory fictional data; the app uses authenticated API calls. */
"use strict";
const $ = (id) => document.getElementById(id);
const preview = document.documentElement.dataset.preview === "true";
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const labels = {new:"New", acknowledged:"Acknowledged", in_progress:"In progress", resolved:"Resolved", reopened:"Reopened", cancelled:"Cancelled"};
const transitions = {new:["acknowledged","cancelled"],acknowledged:["in_progress","resolved","cancelled"],in_progress:["resolved","cancelled"],resolved:["reopened"],reopened:["in_progress","resolved","cancelled"],cancelled:[]};
let csrf = "", account = {role:"manager", name:"Demo Manager"}, page = "operations", status = "", displayLimit = 12, rows = [], metrics = {}, catalog = {}, current = null, refreshVersion = 0;
let demoRows = preview ? structuredClone(window.HOTEL_DEMO.requests) : [];
const fullCatalog = [
 {id:"cleaning",name:"Room cleaning & care",department:"housekeeping",services:["Urgent cleaning","Scheduled cleaning"]},
 {id:"amenities",name:"Amenities & supplies",department:"housekeeping",services:["Extra towels","Extra pillows or blankets","Tea / coffee kit"]},
 {id:"room_service",name:"Room service",department:"food",services:["In-room dining"]},
 {id:"restaurant",name:"Restaurant services",department:"food",services:["Restaurant table booking"]},
 {id:"venue",name:"Venue booking",department:"events",services:["Banquet hall booking","Conference room booking"]},
 {id:"event",name:"Event organisation",department:"events",services:["Wedding","Corporate event","Team building","Birthday"]},
 {id:"maintenance",name:"Repair & maintenance",department:"engineering",services:["Air conditioning / heating","Electrical issue","Plumbing"]},
 {id:"safety",name:"Safety & security",department:"security",services:["Lost property","Room access","Emergency assistance"]},
 {id:"personal",name:"Personal requests",department:"concierge",services:["Event tickets","Transport","Restaurant recommendations","Other"]}
];
const format = (n, suffix="") => n === null || n === undefined ? "—" : `${n}${suffix}`;
const when = (s) => s ? new Date(s).toLocaleString("en-GB",{timeZone:"UTC",day:"2-digit",month:"short",hour:"2-digit",minute:"2-digit"}) : "—";
const pill = (s) => `<span class="status-pill ${esc(s)}">${esc(labels[s] || s)}</span>`;
function notify(message, error=false) { $("notification").hidden=false; $("notification").textContent=message; $("notification").classList.toggle("error",error); }
async function api(path, options={}) {
 const response=await fetch(`/api/${path}`,{...options,headers:{"Content-Type":"application/json","X-CSRF-Token":csrf,...options.headers}});
 let data; try {data=await response.json();} catch {throw new Error("The server could not return this request. Please retry.");}
 if(!response.ok) {if(response.status===401 && path!=="login") {$("workspace").hidden=true;$("login-view").hidden=false;} throw new Error(typeof data.detail==="string" ? data.detail : "Please check the form values.");}
 return data;
}
function filteredDemo(includeStatus=true) {
 const dep=$("department").value, start=$("start-date").value, end=$("end-date").value, search=$("search").value.toLowerCase();
 if(start && end && start>end) throw new Error("Start date must not follow end date.");
 return demoRows.filter(r=>(!dep||r.department_id===dep)&&(!start||r.created_at.slice(0,10)>=start)&&(!end||r.created_at.slice(0,10)<=end)&&(!includeStatus||!status||r.status===status)&&(!includeStatus||!search||[r.service,r.room,r.id].some(x=>x.toLowerCase().includes(search)))).sort((a,b)=>b.created_at.localeCompare(a.created_at));
}
function demoMetrics(data) {
 const elapsed=(r,t)=>(Date.parse(t)-Date.parse(r.created_at))/60000;
 const avg=a=>a.length?Math.round(a.reduce((x,y)=>x+y,0)/a.length*10)/10:null;
 const pct=(x,y)=>y?Math.round(x/y*1000)/10:null;
 const responded=data.filter(r=>r.responded_at), resolved=data.filter(r=>r.status==="resolved"&&r.resolved_at), ever=data.filter(r=>r.first_resolved_at), rated=resolved.filter(r=>r.csat!==null),active=data.filter(r=>!["resolved","cancelled"].includes(r.status));
 const counts=(key)=>data.reduce((out,r)=>{out[key(r)]=(out[key(r)]||0)+1;return out;},{});
 return {number_of_requests:data.length,active_requests:active.length,overdue_active_requests:active.filter(r=>elapsed(r,"2026-10-08T18:00:00Z")>r.sla_minutes).length,average_response_minutes:avg(responded.map(r=>elapsed(r,r.responded_at))),responded_requests:responded.length,average_resolution_minutes:avg(resolved.map(r=>elapsed(r,r.resolved_at))),resolved_requests:resolved.length,completion_rate:pct(resolved.length,data.length),sla_compliance:pct(resolved.filter(r=>elapsed(r,r.resolved_at)<=r.sla_minutes).length,resolved.length),reopened_requests_rate:pct(ever.filter(r=>r.reopen_count>0).length,ever.length),ever_resolved_requests:ever.length,csat_mean:avg(rated.map(r=>r.csat)),csat_positive_rate:pct(rated.filter(r=>r.csat>=4).length,rated.length),csat_responses:rated.length,csat_response_rate:pct(rated.length,resolved.length),requests_by_department:counts(r=>r.department_name),requests_by_day:counts(r=>r.created_at.slice(0,10))};
}
function params() {
 const p=new URLSearchParams(); for(const [key,id] of [["department","department"],["start","start-date"],["end","end-date"]]) if($(id).value)p.set(key,$(id).value); return p;
}
async function refresh() {
 const version=++refreshVersion;
 try {
  let nextRows,nextMetrics;
  if(preview) {nextRows=filteredDemo();nextMetrics=demoMetrics(filteredDemo(false));}
  else {const p=params(),q=new URLSearchParams(p);if(status)q.set("status",status);if($("search").value)q.set("search",$("search").value);[nextRows,nextMetrics]=await Promise.all([api(`requests?${q}`),api(`metrics?${p}`)]);}
  if(version!==refreshVersion)return; rows=nextRows;metrics=nextMetrics;render();
 } catch(error) {notify(error.message,true);}
}
function render() {
 const cards=page==="analytics" ? [
  ["Avg. resolution",format(metrics.average_resolution_minutes),"min",`${metrics.resolved_requests} currently resolved requests`,"◷"],
  ["Completion rate",format(metrics.completion_rate),"%",`${metrics.resolved_requests} of ${metrics.number_of_requests} requests`,"✓"],
  ["Reopened requests",format(metrics.reopened_requests_rate),"%",`Denominator: ${metrics.ever_resolved_requests} ever resolved`,"↺"],
  ["Guest CSAT",format(metrics.csat_mean),"/ 5",`${metrics.csat_responses} synthetic ratings`,"☆"]
 ] : [
  ["Total requests",format(metrics.number_of_requests),"","Selected creation cohort","▤"],
  ["Active requests",format(metrics.active_requests),"",`${metrics.overdue_active_requests} past their demo SLA`,"◉"],
  ["Avg. first response",format(metrics.average_response_minutes),"min",`${metrics.responded_requests} acknowledged requests`,"◷"],
  ["SLA compliance",format(metrics.sla_compliance),"%",`${metrics.resolved_requests} resolved requests evaluated`,"✓"]
 ];
 $("metric-cards").innerHTML=cards.map(([title,value,unit,caption,symbol])=>`<article class="metric-card"><div class="metric-top"><span>${title}</span><span class="metric-symbol">${symbol}</span></div><div class="metric-value">${value} <span class="metric-unit">${unit}</span></div><div class="metric-caption">${caption}</div></article>`).join("");
 $("nav-count").textContent=metrics.active_requests;$("queue-count").textContent=rows.length;
 $("request-table").innerHTML=rows.slice(0,displayLimit).map(r=>`<tr><td><span class="service-name">${esc(r.service)}</span><span class="request-id">${esc(r.id)}</span></td><td>${esc(r.guest_name)}<span class="room-label">Room ${esc(r.room)}</span></td><td><span class="department-dot"></span>${esc(r.department_name)}</td><td>${pill(r.status)}</td><td>${esc(r.assignee_name||"Unassigned")}</td><td class="muted">${when(r.created_at)}</td><td><button class="open-request" data-request="${esc(r.id)}" aria-label="Open request ${esc(r.id)}">↗</button></td></tr>`).join("") || '<tr><td colspan="7" class="empty-state">No requests match these filters.</td></tr>';
 $("table-summary").textContent=`Showing ${Math.min(displayLimit,rows.length)} of ${rows.length} requests`;$("show-more").hidden=displayLimit>=rows.length;
 const departments=Object.entries(metrics.requests_by_department||{}).sort((a,b)=>b[1]-a[1]),max=Math.max(1,...departments.map(x=>x[1]));
 $("department-chart").innerHTML=departments.map(([name,n])=>`<div class="bar-row"><div class="bar-label"><span>${esc(name)}</span><strong>${n}</strong></div><div class="bar-track"><div class="bar-fill" style="width:${n/max*100}%"></div></div></div>`).join("") || '<p class="muted">No data in this cohort.</p>';
 $("quality-metrics").innerHTML=[
  ["SLA compliance",format(metrics.sla_compliance,"%"),`${metrics.resolved_requests} currently resolved requests`],
  ["Positive CSAT (4–5)",format(metrics.csat_positive_rate,"%"),`${metrics.csat_responses} ratings · response rate ${format(metrics.csat_response_rate,"%")}`],
  ["Overdue active requests",format(metrics.overdue_active_requests),"Demo resolution SLA has elapsed"],
  ["Total requests",format(metrics.number_of_requests),"Created-date cohort; all statuses included"]
 ].map(([name,n,note])=>`<div class="quality-row"><div>${name}<small>${note}</small></div><strong>${n}</strong></div>`).join("");
 const days=Object.entries(metrics.requests_by_day||{}).sort((a,b)=>a[0].localeCompare(b[0])),dayMax=Math.max(1,...days.map(x=>x[1]));
 $("trend-chart").innerHTML=days.map(([day,n])=>`<div class="trend-item"><span>${n}</span><div class="trend-bar" style="height:${n/dayMax*115}px"></div><span>${day.slice(5)}</span></div>`).join("") || '<p class="muted">No requests in this period.</p>';
}
function selectPage(next) {
 page=next;document.querySelectorAll("[data-page]").forEach(b=>b.classList.toggle("active",b.dataset.page===page));
 for(const name of ["operations","analytics","case"])$(name+"-page").hidden=name!==page;
 $("metric-cards").hidden=page==="case";document.querySelector(".filters").hidden=page==="case";$("new-request").hidden=page!=="operations"||account.role!=="manager";
 $("breadcrumb").textContent={operations:"OPERATIONS",analytics:"ANALYTICS",case:"PRODUCT CASE STUDY"}[page];
 $("page-title").textContent={operations:"Every request. One workspace.",analytics:"Make service performance visible.",case:"From a guest problem to a product."}[page];
 $("page-subtitle").textContent={operations:"Coordinate the team and keep guest requests moving.",analytics:"Operational metrics with transparent definitions and denominators.",case:"The research, decisions and boundaries behind this prototype."}[page];render();
}
async function openRequest(id) {
 try {current=preview?structuredClone(demoRows.find(r=>r.id===id)):await api("requests/"+id);renderDetail();$("detail-drawer").hidden=false;$("drawer-overlay").hidden=false;$("close-drawer").focus();} catch(error){notify(error.message,true);}
}
function renderDetail() {
 const r=current,write=account.role!=="analyst",staff=catalog.staff.filter(s=>s.role==="manager"||(s.role==="agent"&&s.department_id===r.department_id));
 $("detail-content").innerHTML=`<p class="eyebrow">REQUEST / ${esc(r.id)}</p><h2>${esc(r.service)}</h2>${pill(r.status)}<div class="detail-info"><div><small>GUEST / ROOM</small>${esc(r.guest_name)} · ${esc(r.room)}</div><div><small>DEPARTMENT</small>${esc(r.department_name)}</div><div><small>CREATED · UTC</small>${when(r.created_at)}</div><div><small>DEMO SLA</small>${r.sla_minutes} minutes</div></div><h3 class="small">Request details</h3><p class="detail-description">${esc(r.detail)}</p>${write?`<form id="detail-form" class="detail-form"><label>Responsible employee<select id="assign-select"><option value="">Unassigned</option>${staff.map(s=>`<option value="${s.id}"${r.assigned_to===s.id?" selected":""}>${esc(s.name)}</option>`).join("")}</select></label><button type="button" id="assign-button" class="ghost">Save assignment</button><label>Next status<select id="next-status"><option value="">Choose a transition</option>${(transitions[r.status]||[]).map(s=>`<option value="${s}">${labels[s]}</option>`).join("")}</select></label><label>Note / reason<textarea id="change-note" rows="3" maxlength="500" placeholder="Reason required for reopening or cancellation"></textarea></label><div class="actions"><button type="submit" class="primary">Save update</button></div></form>`:'<p class="muted small">Analyst access · read-only</p>'}<h3 class="small">Request history <span class="tag">${r.events.length}</span></h3><div class="timeline">${[...r.events].reverse().map(e=>`<div class="event"><strong>${esc(e.action.replaceAll("_"," "))}${e.to_status?" → "+esc(labels[e.to_status]):""}</strong><small>${when(e.occurred_at)} UTC · ${esc(e.actor_name||"Guest / system")}</small>${e.note?`<p>${esc(e.note)}</p>`:""}</div>`).join("")}</div><p class="small muted">Record version ${r.version} · changes are checked for conflicts.</p>`;
 if(write){$("assign-button").onclick=()=>updateRequest({assigned_to:$("assign-select").value?Number($("assign-select").value):null});$("detail-form").onsubmit=e=>{e.preventDefault();const payload={note:$("change-note").value};if($("next-status").value)payload.status=$("next-status").value;updateRequest(payload);};}
}
async function updateRequest(payload, previewTime="2026-10-08T18:00:00Z") {
 try {
  if(preview) {
   const r=demoRows.find(x=>x.id===current.id),now=previewTime,note=(payload.note||"").trim();
   if(payload.status){if(!transitions[r.status].includes(payload.status))throw new Error("Invalid transition");if(["reopened","cancelled"].includes(payload.status)&&!note)throw new Error("Add a reason for reopening or cancellation.");const old=r.status;r.status=payload.status;r.responded_at=r.responded_at||(payload.status!=="cancelled"?now:null);r.resolved_at=payload.status==="resolved"?now:null;r.first_resolved_at=r.first_resolved_at||r.resolved_at;if(payload.status==="reopened"){r.reopen_count++;r.csat=null;}r.events.push({action:"status_changed",to_status:payload.status,from_status:old,note,occurred_at:now,actor_name:"Demo Manager"});}
   else if("assigned_to" in payload){r.assigned_to=payload.assigned_to;r.assignee_name=catalog.staff.find(s=>s.id===r.assigned_to)?.name||null;r.events.push({action:"assigned",note:`Employee ID: ${r.assigned_to??"unassigned"}`,occurred_at:now,actor_name:"Demo Manager"});}
   else {if(!note)throw new Error("Choose a status or add a note.");r.events.push({action:"note",note,occurred_at:now,actor_name:"Demo Manager"});}
   r.version++;current=structuredClone(r);
  } else current=await api("requests/"+current.id,{method:"PATCH",body:JSON.stringify({version:current.version,...payload})});
  renderDetail();await refresh();notify(preview?"Preview updated. Changes stay in this tab and reset when refreshed.":"Request saved. History updated.");return true;
 }catch(error){notify(error.message,true);if(!preview&&current)await openRequest(current.id);return false;}
}
function createPreviewRequest(payload, created="2026-10-08T18:00:00Z", rid="preview-"+crypto.randomUUID().slice(0,8)) {
 if(!preview)throw new Error("Preview creation is unavailable in the full app.");
 const guest=catalog.guests.find(g=>g.id===payload.guest_id),cat=catalog.categories.find(c=>c.id===payload.category),dep=catalog.departments.find(d=>d.id===cat?.department);
 if(!guest||!cat||!dep||!cat.services.includes(payload.service)||!payload.detail?.trim())throw new Error("Check the guest, service and request details.");
 if(demoRows.some(r=>r.id===rid))throw new Error("Request ID already exists.");
 demoRows.unshift({id:rid,guest_id:guest.id,guest_name:guest.name,room:guest.room_id,category_id:cat.id,category_name:cat.name,department_id:dep.id,department_name:dep.name,service:payload.service,detail:payload.detail.trim(),status:"new",created_at:created,responded_at:null,resolved_at:null,first_resolved_at:null,reopen_count:0,csat:null,assigned_to:null,assignee_name:null,sla_minutes:dep.sla_minutes,version:1,events:[{action:"created",to_status:"new",note:"Fictional preview request",occurred_at:created}]});
 return rid;
}
function closeDrawer() {$("detail-drawer").hidden=true;$("drawer-overlay").hidden=true;current=null;}
function loadCatalog() {
 $("department").innerHTML='<option value="">All departments</option>'+catalog.departments.map(d=>`<option value="${esc(d.id)}">${esc(d.name)}</option>`).join("");
 $("create-guest").innerHTML=catalog.guests.map(g=>`<option value="${g.id}">${esc(g.name)} · ${esc(g.room_id)}</option>`).join("");
 $("create-category").innerHTML=catalog.categories.map(c=>`<option value="${c.id}">${esc(c.name)}</option>`).join("");updateServices();
}
function updateServices(){const c=catalog.categories.find(x=>x.id===$("create-category").value);$("create-service").innerHTML=(c?.services||[]).map(s=>`<option>${esc(s)}</option>`).join("");}
async function enterWorkspace() {
 if(preview) {
  catalog={categories:fullCatalog,staff:window.HOTEL_DEMO.staff,departments:[...new Map(demoRows.map(r=>[r.department_id,{id:r.department_id,name:r.department_name,sla_minutes:r.sla_minutes}])).values()].sort((a,b)=>a.name.localeCompare(b.name)),guests:[...new Map(demoRows.map(r=>[r.guest_id,{id:r.guest_id,name:r.guest_name,room_id:r.room}])).values()]};
  $("demo-label").textContent="Interactive preview · synthetic data · changes reset on refresh";$("logout").hidden=true;
 }else {account=await api("me");csrf=account.csrf;catalog=await api("catalog");const config=await api("config");$("demo-label").textContent=config.demo?"Synthetic demo data · use fictional information only":"Staff workspace · prototype";}
 $("user-label").innerHTML=`${esc(account.name)}<small>${esc(account.role)} workspace</small>`;loadCatalog();$("login-view").hidden=true;$("workspace").hidden=false;await refresh();selectPage(page);
}
$("login-form").onsubmit=async e=>{e.preventDefault();try{const result=await api("login",{method:"POST",body:JSON.stringify({username:$("username").value,password:$("password").value})});csrf=result.csrf;$("login-error").textContent="";await enterWorkspace();}catch(error){$("login-error").textContent=error.message;}};
$("logout").onclick=async()=>{try{await api("logout",{method:"POST"});location.reload();}catch(error){notify(error.message,true);}};
document.querySelectorAll("[data-page]").forEach(b=>b.onclick=()=>selectPage(b.dataset.page));
document.querySelectorAll("[data-status]").forEach(b=>b.onclick=()=>{status=b.dataset.status;displayLimit=12;document.querySelectorAll("[data-status]").forEach(x=>x.classList.toggle("active",x===b));refresh();});
$("request-table").onclick=e=>{const b=e.target.closest("[data-request]");if(b)openRequest(b.dataset.request);};
for(const id of ["department","start-date","end-date"])$(id).onchange=()=>{displayLimit=12;refresh();};
let searchTimer;$("search").oninput=()=>{clearTimeout(searchTimer);searchTimer=setTimeout(()=>{displayLimit=12;refresh();},180);};
$("clear-filters").onclick=()=>{for(const id of ["department","start-date","end-date","search"])$(id).value="";refresh();};
$("show-more").onclick=()=>{displayLimit+=12;render();};$("close-drawer").onclick=closeDrawer;$("drawer-overlay").onclick=closeDrawer;document.addEventListener("keydown",e=>{if(e.key==="Escape")closeDrawer();});
$("new-request").onclick=()=>$("create-dialog").showModal();$("close-create").onclick=()=>$("create-dialog").close();$("create-category").onchange=updateServices;
$("create-form").onsubmit=async e=>{e.preventDefault();try{
 const payload={guest_id:Number($("create-guest").value),category:$("create-category").value,service:$("create-service").value,detail:$("create-detail").value.trim()};if(!payload.detail)throw new Error("Add request details.");let rid;
 if(preview)rid=createPreviewRequest(payload);
 else{const r=await api("requests",{method:"POST",body:JSON.stringify(payload)});rid=r.id;}
 $("create-dialog").close();$("create-detail").value="";await refresh();await openRequest(rid);notify("New request saved.");
 }catch(error){notify(error.message,true);}};
(async()=>{if(preview){await enterWorkspace();return;}try{await enterWorkspace();}catch{const config=await api("config");$("login-view").hidden=false;if(config.demo){$("username").value=config.demo_username;$("password").value=config.demo_password;$("login-note").textContent="Demo credentials are prefilled. Analyst: analyst; department agent: housekeeping-agent. Same demo password. Use fictional information.";}}})().catch(error=>{ $("login-view").hidden=false;$("login-error").textContent=error.message;});
