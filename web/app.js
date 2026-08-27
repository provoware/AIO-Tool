const state={
  config:null,
  status:null,
  todos:null,
  events:[],
  calendar:null,
  upcoming:[],
  texts:{},
  errors:{},
  visibleReminderKeys:new Set(),
  monthAnchor:null,
  lastRefresh:null
};

const REMINDER_POLL_MS=60000;
const $=(selector)=>document.querySelector(selector);
const $$=(selector)=>Array.from(document.querySelectorAll(selector));

function localIsoDate(value=new Date()){
  const year=value.getFullYear();
  const month=String(value.getMonth()+1).padStart(2,'0');
  const day=String(value.getDate()).padStart(2,'0');
  return `${year}-${month}-${day}`;
}

function parseLocalDate(iso){
  const [year,month,day]=iso.split('-').map(Number);
  return new Date(year,month-1,day,12,0,0,0);
}

function monthAnchor(value=new Date()){
  return new Date(value.getFullYear(),value.getMonth(),1,12,0,0,0);
}

function t(key,fallback=''){
  return state.texts[key]??fallback??key;
}

async function loadTexts(){
  try{
    const res=await fetch('/dashboard-texts.de.v1.json',{cache:'no-store'});
    const data=await res.json();
    if(!res.ok||data.schema_version!==1||data.language!=='de'||typeof data.messages!=='object') throw new Error('Textkatalog ungültig');
    state.texts=data.messages;
  }catch(err){
    state.errors.texts=String(err.message||err);
  }
  $$('[data-i18n]').forEach(node=>{
    const value=t(node.dataset.i18n,'');
    if(value) node.textContent=value;
  });
}

async function api(path,options={}){
  const headers={...(options.headers||{})};
  if(options.body!==undefined) headers['Content-Type']='application/json';
  const res=await fetch(path,{...options,headers});
  let data;
  try{data=await res.json();}
  catch{throw new Error(`Ungültige Serverantwort (HTTP ${res.status})`);}
  if(!res.ok||!data.ok){
    const error=new Error(data.error||`HTTP ${res.status}`);
    error.help=data.help||null;
    error.detail=data.detail||null;
    error.status=res.status;
    throw error;
  }
  return data;
}

function recordError(area,err){
  state.errors[area]={
    message:err?.message||String(err),
    action:err?.help?.action||'',
    rule_id:err?.help?.rule_id||null
  };
}

function clearError(area){delete state.errors[area];}

async function safeLoad(area,loader){
  try{
    const result=await loader();
    clearError(area);
    return result;
  }catch(err){
    recordError(area,err);
    return null;
  }
}

function applyConfig(config){
  if(!config) return;
  state.config=config;
  document.documentElement.dataset.theme=config.theme;
  document.documentElement.style.fontSize=`${config.font_scale}%`;
  $('#expertToggle').checked=Boolean(config.expert_visible);
  $('#developerToggle').hidden=!config.expert_visible;
  if(!config.expert_visible){
    $('#developerPanel').hidden=true;
    $('#developerToggle').setAttribute('aria-expanded','false');
  }
  $$('[data-theme]').forEach(button=>button.classList.toggle('selected',button.dataset.theme===config.theme));
  $$('[data-font]').forEach(button=>button.classList.toggle('selected',Number(button.dataset.font)===Number(config.font_scale)));
  updateDensity();
}

function applyStatus(status){
  if(!status) return;
  state.status=status;
  applyConfig(status.config);
  $('#versionChip').textContent=status.version;
  $('#systemVersion').textContent=status.version;
  $('#systemBind').textContent=status.bind;
  $('#systemPackages').textContent=String(status.external_python_packages?.length??0);
  const registryOk=Boolean(status.core?.version_registry?.ok);
  $('#systemRegistry').textContent=registryOk?'🟢 konsistent':'🟠 prüfen';
  $('#registryBadge').textContent=registryOk?'🟢 Registry':'🟠 Registry';
  $('#openTodoMetric').textContent=String(status.core?.todos_open??0);
  $('#calendarMetric').textContent=String(status.core?.calendar_events??0);
  $('#historyMetric').textContent=String(status.core?.events??0);
  $('#statusText').textContent=`Version ${status.version} · lokal auf ${status.bind} · Internet nicht erforderlich`;
  renderDiagnostics();
}

function updateReadyState(){
  const areas=Object.keys(state.errors);
  if(!state.status){
    $('#readyPill').textContent='🔴 Eingriff';
    $('#statusText').textContent=areas.length?`Systemstatus nicht vollständig: ${humanError(areas[0])}`:'Systemstatus nicht verfügbar.';
    return;
  }
  if(areas.length){
    $('#readyPill').textContent='🟠 teilweise';
    $('#statusText').textContent=`Grundsystem bereit · ${areas.length} Bereich(e) konnten nicht vollständig geladen werden.`;
  }else{
    $('#readyPill').textContent='🟢 bereit';
  }
}

function humanError(area){
  const entry=state.errors[area];
  if(!entry) return area;
  return entry.action?`${entry.message} ${entry.action}`:entry.message;
}

function updateDensity(){
  const width=window.innerWidth;
  const height=window.innerHeight;
  const font=Number(state.config?.font_scale||100);
  let density='normal';
  if(width>=1500&&height>=850&&font<=120) density='wide';
  if(width<1120||height<720||font>=130) density='compact';
  document.documentElement.dataset.density=density;
  const labels={compact:'kompakt',normal:'normal',wide:'weit'};
  $('#densityChip').textContent=`Ansicht: ${labels[density]}`;
}

function formatDate(iso,options={day:'2-digit',month:'2-digit'}){
  try{return new Intl.DateTimeFormat('de-DE',options).format(parseLocalDate(iso));}
  catch{return iso;}
}

function formatDateTime(value){
  try{return new Intl.DateTimeFormat('de-DE',{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'}).format(new Date(value));}
  catch{return value||'—';}
}

function monthLabel(anchor){
  return new Intl.DateTimeFormat('de-DE',{month:'long',year:'numeric'}).format(anchor);
}

function renderCalendar(){
  const calendar=state.calendar;
  const grid=$('#monthGrid');
  grid.replaceChildren();
  $('#monthTitle').textContent=monthLabel(state.monthAnchor);
  if(!calendar){
    const error=document.createElement('p');
    error.className='inline-error';
    error.textContent=humanError('calendar')||'Kalender konnte nicht geladen werden.';
    grid.append(error);
    $('#calendarEmpty').hidden=true;
    return;
  }

  const start=parseLocalDate(calendar.start);
  const end=parseLocalDate(calendar.end);
  const leading=(start.getDay()+6)%7;
  for(let i=0;i<leading;i++){
    const blank=document.createElement('div');
    blank.className='day-cell blank';
    blank.setAttribute('aria-hidden','true');
    grid.append(blank);
  }

  const today=localIsoDate();
  let eventCount=0;
  for(let day=1;day<=end.getDate();day++){
    const date=new Date(start.getFullYear(),start.getMonth(),day,12,0,0,0);
    const iso=localIsoDate(date);
    const events=calendar.by_date?.[iso]||[];
    eventCount+=events.length;
    const cell=document.createElement('div');
    cell.className='day-cell';
    cell.setAttribute('role','gridcell');
    cell.tabIndex=0;
    if(iso===today) cell.classList.add('today');
    const weekday=(date.getDay()+6)%7;
    if(weekday>=5) cell.classList.add('weekend');

    const head=document.createElement('div');
    head.className='day-number';
    const number=document.createElement('span');
    number.textContent=String(day);
    head.append(number);
    if(events.length){
      const badge=document.createElement('small');
      badge.textContent=String(events.length);
      badge.setAttribute('aria-label',`${events.length} Termine`);
      head.append(badge);
    }
    cell.append(head);

    const list=document.createElement('div');
    list.className='day-events';
    events.slice(0,3).forEach(event=>{
      const item=document.createElement('span');
      item.className='calendar-event';
      item.textContent=`${event.start_time?event.start_time+' ':''}${event.title}`;
      item.title=[event.start_time,event.end_time?`– ${event.end_time}`:'',event.title].filter(Boolean).join(' ');
      list.append(item);
    });
    if(events.length>3){
      const more=document.createElement('span');
      more.className='calendar-more';
      more.textContent=`+${events.length-3} weitere`;
      list.append(more);
    }
    cell.append(list);
    grid.append(cell);
  }
  $('#calendarEmpty').hidden=eventCount!==0;
}

function renderUpcoming(){
  const container=$('#upcomingList');
  container.replaceChildren();
  const today=localIsoDate();
  const items=(state.upcoming||[])
    .filter(event=>event.date>=today)
    .sort((a,b)=>(a.date.localeCompare(b.date)||(a.start_time||'00:00').localeCompare(b.start_time||'00:00')))
    .slice(0,5);
  $('#upcomingCount').textContent=String(items.length);
  if(!items.length){
    container.append(emptyMessage(t('upcoming.empty','Keine kommenden Termine im geladenen Jahr.')));
    return;
  }
  items.forEach(event=>{
    const row=document.createElement('div');
    row.className='list-row appointment-row';
    const date=document.createElement('div');
    date.className='date-block';
    date.innerHTML=`<strong>${formatDate(event.date,{day:'2-digit'})}</strong><small>${formatDate(event.date,{month:'short'})}</small>`;
    const text=document.createElement('div');
    text.className='list-main';
    const title=document.createElement('strong');
    title.textContent=event.title;
    const meta=document.createElement('small');
    meta.textContent=[event.start_time,event.category].filter(Boolean).join(' · ')||t('calendar.allDay','ohne Uhrzeit');
    text.append(title,meta);
    row.append(date,text);
    container.append(row);
  });
}

function emptyMessage(text){
  const node=document.createElement('p');
  node.className='empty-message';
  node.textContent=text;
  return node;
}

function renderTodos(){
  const container=$('#todoList');
  container.replaceChildren();
  const next=state.todos?.next||[];
  const open=state.todos?.items?.length??state.status?.core?.todos_open??0;
  $('#todoCountBadge').textContent=String(open);
  if(!next.length){
    container.append(emptyMessage(t('todo.empty','Keine offenen TODOs.')));
    return;
  }
  next.forEach(item=>{
    const row=document.createElement('div');
    row.className='list-row todo-row';
    const main=document.createElement('div');
    main.className='list-main';
    const title=document.createElement('strong');
    title.textContent=item.title;
    const meta=document.createElement('small');
    const due=[item.due_date?formatDate(item.due_date,{day:'2-digit',month:'2-digit'}):'',item.due_time||'',item.priority==='high'?'hoch':''].filter(Boolean);
    meta.textContent=due.join(' · ')||t('todo.noDate','ohne Termin');
    main.append(title,meta);
    const done=document.createElement('button');
    done.type='button';
    done.className='icon-action';
    done.textContent='✓';
    done.title=`${item.title} erledigen`;
    done.setAttribute('aria-label',`${item.title} erledigen`);
    done.addEventListener('click',()=>completeTodo(item.id,done));
    row.append(main,done);
    container.append(row);
  });
}

async function completeTodo(id,button){
  button.disabled=true;
  try{
    await api(`/api/todos/${encodeURIComponent(id)}/complete`,{method:'POST',body:'{}'});
    await refreshData({keepMonth:true});
  }catch(err){
    recordError('todo-action',err);
    button.disabled=false;
    $('#statusText').textContent=`TODO konnte nicht erledigt werden: ${humanError('todo-action')}`;
    updateReadyState();
  }
}

function renderEvents(){
  const container=$('#eventList');
  container.replaceChildren();
  const events=state.events||[];
  if(!events.length){
    container.append(emptyMessage(t('events.empty','Noch keine Ereignisse vorhanden.')));
    return;
  }
  events.slice(0,5).forEach(event=>{
    const row=document.createElement('div');
    row.className=`timeline-row level-${event.level||'info'}`;
    const dot=document.createElement('span');
    dot.className='timeline-dot';
    dot.setAttribute('aria-hidden','true');
    const text=document.createElement('div');
    const message=document.createElement('strong');
    message.textContent=event.message;
    const meta=document.createElement('small');
    meta.textContent=`${event.area||'Allgemein'} · ${formatDateTime(event.time)}`;
    text.append(message,meta);
    row.append(dot,text);
    container.append(row);
  });
}

function renderDiagnostics(){
  if(!state.status) return;
  const core=state.status.core||{};
  const diagnostic={
    version:state.status.version,
    ready:state.status.ready,
    bind:state.status.bind,
    registry_ok:Boolean(core.version_registry?.ok),
    todos_open:core.todos_open??null,
    calendar_events:core.calendar_events??null,
    events:core.events??null,
    error_rule_version:core.error_help?.rules_version??null,
    text_catalog_version:core.error_help?.text_catalog?.catalog_version??null,
    dashboard_errors:Object.fromEntries(Object.entries(state.errors).map(([key,value])=>[key,{message:value.message,rule_id:value.rule_id}]))
  };
  $('#developerInfo').textContent=JSON.stringify(diagnostic,null,2);
}

function renderNextStep(){
  const reminderCount=$('#reminderRegion').childElementCount;
  if(reminderCount){
    $('#nextTitle').textContent=t('next.reminder','Erinnerung prüfen');
    $('#nextText').textContent=t('next.reminder.help','Eine fällige Erinnerung wartet oben auf Bestätigung.');
    return;
  }
  const todo=state.todos?.next?.[0];
  if(todo){
    $('#nextTitle').textContent=`TODO: ${todo.title}`;
    $('#nextText').textContent=todo.due_date?`Termin ${formatDate(todo.due_date,{day:'2-digit',month:'2-digit',year:'numeric'})}${todo.due_time?' · '+todo.due_time:''}`:t('next.todo.help','Die nächste offene Aufgabe ist direkt rechts erreichbar.');
    return;
  }
  const appointment=(state.upcoming||[]).filter(item=>item.date>=localIsoDate()).sort((a,b)=>a.date.localeCompare(b.date))[0];
  if(appointment){
    $('#nextTitle').textContent=`Termin: ${appointment.title}`;
    $('#nextText').textContent=`${formatDate(appointment.date,{weekday:'short',day:'2-digit',month:'2-digit'})}${appointment.start_time?' · '+appointment.start_time:''}`;
    return;
  }
  $('#nextTitle').textContent=t('next.clear','Alles ruhig');
  $('#nextText').textContent=t('next.clear.help','Aktuell gibt es keine offenen TODOs oder kommenden Termine im geladenen Zeitraum.');
}

function reminderKey(reminder){return `${reminder.event_id}:${reminder.minutes_before}`;}

function renderReminders(reminders){
  reminders.forEach(reminder=>{
    const key=reminderKey(reminder);
    if(state.visibleReminderKeys.has(key)) return;
    state.visibleReminderKeys.add(key);
    const alert=document.createElement('article');
    alert.className='reminder-card';
    alert.dataset.reminderKey=key;
    alert.setAttribute('role','alert');

    const icon=document.createElement('span');
    icon.className='reminder-icon';
    icon.textContent='⏰';
    const body=document.createElement('div');
    body.className='reminder-body';
    const title=document.createElement('strong');
    title.textContent=reminder.title;
    const meta=document.createElement('span');
    const lead=reminder.minutes_before===0?t('reminder.now','jetzt'):reminder.minutes_before===1440?t('reminder.day','1 Tag vorher'):`${reminder.minutes_before} Min. vorher`;
    meta.textContent=`${formatDate(reminder.date,{weekday:'short',day:'2-digit',month:'2-digit'})} · ${reminder.start_time} · ${lead}`;
    body.append(title,meta);
    const button=document.createElement('button');
    button.type='button';
    button.className='reminder-ack';
    button.textContent=t('reminder.seen','Gesehen');
    button.addEventListener('click',()=>ackReminder(reminder,alert,button));
    alert.append(icon,body,button);
    $('#reminderRegion').append(alert);
  });
  renderNextStep();
}

async function ackReminder(reminder,node,button){
  if(document.visibilityState!=='visible') return;
  button.disabled=true;
  try{
    await api(`/api/calendar/${encodeURIComponent(reminder.event_id)}/reminders/${reminder.minutes_before}/ack`,{method:'POST',body:'{}'});
    node.remove();
    state.visibleReminderKeys.delete(reminderKey(reminder));
    clearError('reminders');
    renderNextStep();
    const events=await safeLoad('events',()=>api('/api/events?limit=5'));
    if(events){state.events=events.events||[];renderEvents();}
  }catch(err){
    recordError('reminders',err);
    button.disabled=false;
    $('#statusText').textContent=`Erinnerung konnte nicht quittiert werden: ${humanError('reminders')}`;
    updateReadyState();
  }
}

async function checkReminders(){
  if(document.visibilityState!=='visible') return;
  const result=await safeLoad('reminders',()=>api('/api/calendar/reminders/due?limit=20'));
  if(result) renderReminders(result.reminders||[]);
  updateReadyState();
  renderDiagnostics();
}

async function loadMonth(){
  const anchor=localIsoDate(state.monthAnchor);
  const result=await safeLoad('calendar',()=>api(`/api/calendar?view=month&date=${encodeURIComponent(anchor)}`));
  if(result) state.calendar=result.calendar;
  renderCalendar();
}

async function loadUpcoming(){
  const anchor=localIsoDate(new Date());
  const result=await safeLoad('upcoming',()=>api(`/api/calendar?view=year&date=${encodeURIComponent(anchor)}`));
  if(result) state.upcoming=result.calendar?.events||[];
  renderUpcoming();
}

async function refreshData({keepMonth=false}={}){
  $('#readyPill').textContent='🟠 prüfen';
  if(!keepMonth) state.monthAnchor=monthAnchor(new Date());

  const [statusResult,todoResult,eventResult]=await Promise.all([
    safeLoad('status',()=>api('/api/status')),
    safeLoad('todos',()=>api('/api/todos')),
    safeLoad('events',()=>api('/api/events?limit=5'))
  ]);
  if(statusResult) applyStatus(statusResult);
  if(todoResult){state.todos=todoResult;renderTodos();}
  if(eventResult){state.events=eventResult.events||[];renderEvents();}
  await Promise.all([loadMonth(),loadUpcoming(),checkReminders()]);

  state.lastRefresh=new Date();
  $('#lastRefresh').textContent=`Aktualisiert ${new Intl.DateTimeFormat('de-DE',{hour:'2-digit',minute:'2-digit'}).format(state.lastRefresh)}`;
  renderNextStep();
  renderDiagnostics();
  updateReadyState();
}

async function updateConfig(changes){
  try{
    const data=await api('/api/config',{method:'POST',body:JSON.stringify(changes)});
    applyConfig(data.config);
    clearError('config');
  }catch(err){
    recordError('config',err);
    $('#statusText').textContent=`Einstellung konnte nicht gespeichert werden: ${humanError('config')}`;
  }
  updateReadyState();
}

function shiftMonth(delta){
  state.monthAnchor=new Date(state.monthAnchor.getFullYear(),state.monthAnchor.getMonth()+delta,1,12,0,0,0);
  loadMonth().then(()=>{renderNextStep();updateReadyState();});
}

function setSettings(open){
  $('#settingsPanel').hidden=!open;
  $('#settingsToggle').setAttribute('aria-expanded',String(open));
  if(open) $('#settingsTitle').focus?.();
}

function setDeveloper(open){
  if(!state.config?.expert_visible) return;
  $('#developerPanel').hidden=!open;
  $('#developerToggle').setAttribute('aria-expanded',String(open));
  if(open) renderDiagnostics();
}

async function copyDiagnostics(){
  const text=$('#developerInfo').textContent;
  const button=$('#copyDiagnosticBtn');
  try{
    await navigator.clipboard.writeText(text);
    button.textContent=t('dev.copied','Kopiert ✓');
  }catch{
    button.textContent=t('dev.copyFailed','Kopieren nicht möglich');
  }
  window.setTimeout(()=>{button.textContent=t('dev.copy','Diagnose kopieren');},1800);
}

function bindEvents(){
  $('#refreshBtn').addEventListener('click',()=>refreshData({keepMonth:true}));
  $('#prevMonthBtn').addEventListener('click',()=>shiftMonth(-1));
  $('#nextMonthBtn').addEventListener('click',()=>shiftMonth(1));
  $('#todayBtn').addEventListener('click',()=>{state.monthAnchor=monthAnchor(new Date());loadMonth();});
  $('#settingsToggle').addEventListener('click',()=>setSettings($('#settingsPanel').hidden));
  $('#settingsClose').addEventListener('click',()=>setSettings(false));
  $('#developerToggle').addEventListener('click',()=>setDeveloper($('#developerPanel').hidden));
  $('#copyDiagnosticBtn').addEventListener('click',copyDiagnostics);
  $$('[data-theme]').forEach(button=>button.addEventListener('click',()=>updateConfig({theme:button.dataset.theme})));
  $$('[data-font]').forEach(button=>button.addEventListener('click',()=>updateConfig({font_scale:Number(button.dataset.font)})));
  $('#expertToggle').addEventListener('change',event=>updateConfig({expert_visible:event.target.checked}));
  $$('[data-module-mode]').forEach(button=>button.addEventListener('click',()=>{
    $$('[data-module-mode]').forEach(item=>item.classList.toggle('selected',item===button));
    $('#moduleGrid').dataset.mode=button.dataset.moduleMode;
  }));
  window.addEventListener('resize',updateDensity,{passive:true});
  document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible') checkReminders();});
}

async function boot(){
  state.monthAnchor=monthAnchor(new Date());
  $('#moduleGrid').dataset.mode='frequent';
  await loadTexts();
  bindEvents();
  await refreshData();
  window.setInterval(checkReminders,REMINDER_POLL_MS);
}

boot();
