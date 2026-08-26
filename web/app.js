const state={config:null,status:null};
const $=(s)=>document.querySelector(s);

async function api(path,options={}){
  const res=await fetch(path,{...options,headers:{'Content-Type':'application/json',...(options.headers||{})}});
  const data=await res.json();
  if(!res.ok||!data.ok) throw new Error(data.error||`HTTP ${res.status}`);
  return data;
}

function applyConfig(config){
  state.config=config;
  document.documentElement.dataset.theme=config.theme;
  document.documentElement.style.fontSize=`${config.font_scale}%`;
  $('#expertToggle').checked=Boolean(config.expert_visible);
  $('#expertBox').hidden=!config.expert_visible;
  document.querySelectorAll('[data-theme]').forEach(b=>b.classList.toggle('selected',b.dataset.theme===config.theme));
  document.querySelectorAll('[data-font]').forEach(b=>b.classList.toggle('selected',Number(b.dataset.font)===Number(config.font_scale)));
  $('#favoriteCount').textContent=`${(config.favorites||[]).length} gespeichert`;
}

function applyStatus(status){
  state.status=status;
  $('#statusText').textContent=`Version ${status.version} · offline-first · Backend ${status.bind}`;
  $('#readyPill').textContent=status.ready?'🟢 bereit':'🟠 prüfen';
  $('#expertInfo').textContent=`Internet nötig: ${status.internet_required?'ja':'nein'} · externe Python-Pakete: ${status.external_python_packages.length}`;
  applyConfig(status.config);
}

async function refresh(){
  $('#readyPill').textContent='🟠 prüfen';
  try{applyStatus(await api('/api/status'));}
  catch(err){
    $('#readyPill').textContent='🔴 Eingriff';
    $('#statusText').textContent=`Systemprüfung fehlgeschlagen: ${err.message}`;
  }
}

async function updateConfig(changes){
  try{
    const data=await api('/api/config',{method:'POST',body:JSON.stringify(changes)});
    applyConfig(data.config);
  }catch(err){
    $('#statusText').textContent=`Einstellung konnte nicht gespeichert werden: ${err.message}`;
  }
}

$('#refreshBtn').addEventListener('click',refresh);
document.querySelectorAll('[data-theme]').forEach(b=>b.addEventListener('click',()=>updateConfig({theme:b.dataset.theme})));
document.querySelectorAll('[data-font]').forEach(b=>b.addEventListener('click',()=>updateConfig({font_scale:Number(b.dataset.font)})));
$('#expertToggle').addEventListener('change',e=>updateConfig({expert_visible:e.target.checked}));

refresh();
