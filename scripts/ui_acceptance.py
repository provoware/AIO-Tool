#!/usr/bin/env python3
from __future__ import annotations

import argparse
import calendar
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "ui" / "layout-contract.v1.json"
DEFAULT_OUTPUT = ROOT / "artifacts" / "ui-acceptance"
READY_JS = """() => {
  const badge=document.querySelector('#todoCountBadge');
  const grid=document.querySelector('#monthGrid');
  return Boolean(badge && badge.textContent.trim() !== '—' && grid && grid.children.length >= 28);
}"""


def load_contract() -> dict[str, Any]:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise SystemExit("FEHLER: unbekanntes UI-Vertragsschema")
    return data


def inline_page() -> str:
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")
    js = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
    html = html.replace('<link rel="stylesheet" href="/styles.css?contract=dashboard-v2.2">', f"<style>{css}</style>")
    html = html.replace('<link rel="stylesheet" href="/styles.css">', f"<style>{css}</style>")
    html = html.replace('<script src="/app.js?contract=dashboard-v2.2" defer></script>', f"<script>{js}</script>")
    html = html.replace('<script src="/app.js" defer></script>', f"<script>{js}</script>")
    return html


def fixtures(font_scale: int) -> dict[str, Any]:
    today = date.today()
    tomorrow = today + timedelta(days=1)
    events = [
        {"id":"cal-1","title":"Dashboard prüfen","date":today.isoformat(),"start_time":"10:00","end_time":None,"category":"Test","description":None,"reminders":[0],"todo_id":None},
        {"id":"cal-2","title":"Nächster Entwicklungsschritt","date":tomorrow.isoformat(),"start_time":"15:30","end_time":None,"category":"Projekt","description":None,"reminders":[],"todo_id":None},
    ]
    todos = [
        {"id":"todo-1","title":"Systemprüfung ansehen","due_date":today.isoformat(),"due_time":"09:30","priority":"high","category":"System","note":None,"calendar_event_id":None},
        {"id":"todo-2","title":"Kalender prüfen","due_date":tomorrow.isoformat(),"due_time":None,"priority":"normal","category":"Planung","note":None,"calendar_event_id":None},
        {"id":"todo-3","title":"Dokumentation lesen","due_date":None,"due_time":None,"priority":"low","category":"Dokumentation","note":None,"calendar_event_id":None},
    ]
    history=[]
    for i,(area,message) in enumerate([
        ("System","Oberflächenprüfung wurde erfolgreich vorbereitet."),
        ("Kalender","Termin Dashboard prüfen wurde gespeichert."),
        ("TODO","TODO Systemprüfung ansehen wurde angelegt."),
        ("Versionierung","Version wurde mit der Oberfläche abgeglichen."),
        ("Start","Lokaler Arbeitsbereich wurde gestartet."),
    ]):
        history.append({"id":f"evt-{i}","time":(datetime.now()-timedelta(minutes=i*3)).isoformat(timespec="seconds"),"kind":"validation","area":area,"level":"green","message":message,"details":{}})
    return {"config":{"theme":"steel-night","font_scale":font_scale,"expert_visible":False,"setup_complete":True,"active_project":None,"favorites":[]},"events":events,"todos":todos,"history":history,"reminder_acked":False}


def month_payload(events: list[dict[str,Any]], anchor: str) -> dict[str,Any]:
    d=date.fromisoformat(anchor); start=d.replace(day=1); end=d.replace(day=calendar.monthrange(d.year,d.month)[1])
    selected=[e for e in events if start.isoformat() <= e["date"] <= end.isoformat()]
    by_date:dict[str,list[dict[str,Any]]]={}
    for e in selected: by_date.setdefault(e["date"],[]).append(e)
    return {"view":"month","anchor":anchor,"start":start.isoformat(),"end":end.isoformat(),"events":selected,"by_date":by_date}


def year_payload(events: list[dict[str,Any]], anchor: str) -> dict[str,Any]:
    d=date.fromisoformat(anchor); start=date(d.year,1,1); end=date(d.year,12,31)
    selected=[e for e in events if start.isoformat() <= e["date"] <= end.isoformat()]
    by_date:dict[str,list[dict[str,Any]]]={}
    for e in selected: by_date.setdefault(e["date"],[]).append(e)
    return {"view":"year","anchor":anchor,"start":start.isoformat(),"end":end.isoformat(),"events":selected,"by_date":by_date}


def init_script(f: dict[str,Any]) -> str:
    texts=json.loads((ROOT/"web"/"dashboard-texts.de.v1.json").read_text(encoding="utf-8"))
    version=(ROOT/"VERSION").read_text(encoding="utf-8").strip()
    payload=json.dumps({"f":f,"texts":texts,"version":version},ensure_ascii=False).replace("</","<\\/")
    month=json.dumps(month_payload(f["events"], date.today().isoformat()), ensure_ascii=False)
    year=json.dumps(year_payload(f["events"], date.today().isoformat()), ensure_ascii=False)
    return f'''(()=>{{
const x={payload}; const ok=(body,status=200)=>Promise.resolve(new Response(JSON.stringify({{ok:true,...body}}),{{status,headers:{{"Content-Type":"application/json"}}}}));
window.fetch=(input,options={{}})=>{{const raw=typeof input==="string"?input:input.url; const u=new URL(raw,"http://aio.local"); const p=u.pathname;
 if(p==="/dashboard-texts.de.v1.json") return Promise.resolve(new Response(JSON.stringify(x.texts),{{status:200,headers:{{"Content-Type":"application/json"}}}}));
 if(p==="/api/status") return ok({{version:x.version,ready:true,bind:"127.0.0.1",internet_required:false,external_python_packages:[],config:x.f.config,core:{{version_registry:{{ok:true}},todos_open:x.f.todos.length,todos_archived:0,calendar_events:x.f.events.length,events:x.f.history.length,error_help:{{rules_version:"fixture",text_catalog:{{catalog_version:"fixture"}}}}}}}});
 if(p==="/api/config"){{if((options.method||"GET").toUpperCase()==="POST") Object.assign(x.f.config,JSON.parse(options.body||"{{}}")); return ok({{config:x.f.config}});}}
 if(p==="/api/todos") return ok({{items:x.f.todos,next:x.f.todos.slice(0,3),archive_count:0}});
 if(p.startsWith("/api/todos/")&&p.endsWith("/complete")){{const id=p.split("/")[3];x.f.todos=x.f.todos.filter(t=>t.id!==id);return ok({{item:{{id}}}});}}
 if(p==="/api/events") return ok({{events:x.f.history.slice(0,5)}});
 if(p==="/api/calendar/reminders/due"){{const e=x.f.events[0];return ok({{reminders:x.f.reminder_acked?[]:[{{event_id:e.id,title:e.title,date:e.date,start_time:e.start_time,minutes_before:0}}]}});}}
 if(p.includes("/reminders/")&&p.endsWith("/ack")){{x.f.reminder_acked=true;return ok({{event:x.f.events[0]}});}}
 if(p==="/api/calendar") return ok({{calendar:u.searchParams.get("view")==="year"?{year}:{month}}});
 return Promise.resolve(new Response(JSON.stringify({{ok:false,error:"fixture endpoint missing: "+p}}),{{status:404,headers:{{"Content-Type":"application/json"}}}}));
}}; }})()'''


def expected_spans(contract:dict[str,Any], mode:str)->dict[str,int]:
    if mode=="desktop": return contract["grid"]["desktop_spans"]
    if mode=="medium": return contract["grid"]["medium_spans"]
    return {"modules":12,"calendar":12,"status":12}


def audit(page, contract:dict[str,Any], scenario:dict[str,Any])->dict[str,Any]:
    expected=expected_spans(contract,scenario["expected_mode"]); rules=contract["rules"]
    return page.evaluate('''({required,expected,rules})=>{
const visible=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return !e.hidden&&s.display!=="none"&&s.visibility!=="hidden"&&r.width>0&&r.height>0};
const rect=e=>{const r=e.getBoundingClientRect();return {left:r.left,top:r.top,right:r.right,bottom:r.bottom,width:r.width,height:r.height}};
const regions=[...document.querySelectorAll("[data-ui-region]")].filter(visible); const missing=required.filter(n=>!regions.some(e=>e.dataset.uiRegion===n));
const overlap=[]; for(let i=0;i<regions.length;i++)for(let j=i+1;j<regions.length;j++){const a=rect(regions[i]),b=rect(regions[j]);const w=Math.min(a.right,b.right)-Math.max(a.left,b.left),h=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);if(w>rules.max_region_overlap_css_px&&h>rules.max_region_overlap_css_px)overlap.push([regions[i].dataset.uiRegion,regions[j].dataset.uiRegion]);}
const small=[...document.querySelectorAll("button,.nav-item,.module-tile")].filter(visible).filter(e=>{const r=e.getBoundingClientRect();return r.height+0.5<rules.min_interactive_height_css_px||r.width+0.5<rules.min_interactive_width_css_px}).map(e=>(e.innerText||e.getAttribute("aria-label")||e.tagName).trim().slice(0,60));
const spans={}; for(const [n,s] of Object.entries({modules:".module-column",calendar:".calendar-column",status:".status-column"})){const st=getComputedStyle(document.querySelector(s));const raw=st.gridColumnStart+" "+st.gridColumnEnd;const m=raw.match(/span\\s+(\\d+)/);spans[n]=m?Number(m[1]):null;}
const spanMismatch=Object.keys(expected).filter(k=>spans[k]!==expected[k]).map(k=>({name:k,expected:expected[k],actual:spans[k]}));
return {overflow:Math.max(0,document.documentElement.scrollWidth-document.documentElement.clientWidth),missing,overlap,small,spans,spanMismatch,weekday:getComputedStyle(document.querySelector(".weekday-row")).gridTemplateColumns.split(" ").filter(Boolean).length,month:getComputedStyle(document.querySelector("#monthGrid")).gridTemplateColumns.split(" ").filter(Boolean).length};
}''',{"required":contract["required_regions"],"expected":expected,"rules":rules})


def failures(a:dict[str,Any],contract:dict[str,Any])->list[str]:
    r=contract["rules"]; out=[]
    if a["overflow"]>r["max_horizontal_overflow_css_px"]: out.append(f"horizontaler Overflow {a['overflow']}px")
    if a["missing"]: out.append("fehlende Bereiche: "+", ".join(a["missing"]))
    if a["overlap"]: out.append("Überlappungen: "+str(a["overlap"]))
    if a["small"]: out.append("zu kleine Bedienelemente: "+", ".join(a["small"][:5]))
    if a["spanMismatch"]: out.append("Raster-Spannen: "+str(a["spanMismatch"]))
    if a["weekday"]!=7 or a["month"]!=7: out.append("Kalender nicht 7-spaltig")
    return out


def interactions(page)->dict[str,bool]:
    out={}
    page.locator('[data-module-mode="all"]').click(); out["module_all"]=page.locator("#developerToggle").is_visible()
    page.locator("#settingsToggle").click(); out["settings_open"]=page.locator("#settingsPanel").is_visible(); page.locator("#settingsClose").click(); out["settings_close"]=not page.locator("#settingsPanel").is_visible()
    badge=page.locator("#todoCountBadge").inner_text().strip(); before=int(badge) if badge.isdigit() else -1
    todo_action=page.locator("#todoList .icon-action")
    if todo_action.count(): todo_action.first.click(); page.wait_for_timeout(150)
    after_text=page.locator("#todoCountBadge").inner_text().strip(); after=int(after_text) if after_text.isdigit() else -1
    out["todo_complete"]=before>0 and after==before-1
    rem=page.locator("#reminderRegion .reminder-ack"); out["reminder_visible"]=rem.count()>0
    if rem.count(): rem.first.click(); page.wait_for_timeout(100)
    out["reminder_ack"]=page.locator("#reminderRegion .reminder-card").count()==0
    return out


def run_browser(p,browser_name:str,contract:dict[str,Any],output:Path)->dict[str,Any]:
    browser=getattr(p,browser_name).launch(headless=True); report={"browser":browser_name,"scenarios":[]}
    try:
        for scenario in contract["scenarios"]:
            context=browser.new_context(viewport={"width":scenario["viewport"][0],"height":scenario["viewport"][1]},locale="de-DE",reduced_motion="reduce")
            page=context.new_page(); errors=[]; page.on("pageerror",lambda e:errors.append(str(e)))
            page.add_init_script(init_script(fixtures(scenario["font_scale"])))
            page.set_content(inline_page(),wait_until="load")
            ready_error=None
            try: page.wait_for_function(READY_JS,timeout=10000)
            except Exception as exc: ready_error=f"Dashboard wurde nicht rechtzeitig bereit: {type(exc).__name__}"
            page.wait_for_timeout(100)
            a=audit(page,contract,scenario); f=failures(a,contract); inter={"boot_ready":ready_error is None}
            if ready_error: f.append(ready_error)
            else:
                try: inter.update(interactions(page))
                except Exception as exc: f.append(f"Interaktionsprüfung abgebrochen: {type(exc).__name__}: {exc}")
            f += ["Interaktion fehlgeschlagen: "+k for k,v in inter.items() if not v]
            shot=output/f"{browser_name}-{scenario['id']}.png"; page.screenshot(path=str(shot),full_page=True,animations="disabled")
            report["scenarios"].append({"scenario":scenario,"audit":a,"interactions":inter,"errors":errors,"failures":f+["Browserfehler: "+e for e in errors],"screenshot":shot.name}); context.close()
    finally: browser.close()
    return report


def main()->None:
    ap=argparse.ArgumentParser(); ap.add_argument("--browser",action="append",choices=["chromium","firefox"],dest="browsers"); ap.add_argument("--strict",action="store_true"); ap.add_argument("--output",type=Path,default=DEFAULT_OUTPUT); args=ap.parse_args()
    browsers=args.browsers or ["chromium"]; contract=load_contract(); args.output.mkdir(parents=True,exist_ok=True)
    report={"schema_version":1,"contract_version":contract["contract_version"],"source_version":(ROOT/"VERSION").read_text().strip(),"browsers":[],"failures":[],"failure_count":0}
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            for b in browsers:
                print("UI-Akzeptanz:",b)
                try: report["browsers"].append(run_browser(p,b,contract,args.output))
                except Exception as exc: report["failures"].append(f"{b}: Browserlauf abgebrochen: {type(exc).__name__}: {exc}")
    except ImportError:
        report["failures"].append("Playwright fehlt: python3 -m pip install -r requirements-ui.txt")
    all_fail=list(report["failures"])+[f"{b['browser']}/{s['scenario']['id']}: {x}" for b in report["browsers"] for s in b["scenarios"] for x in s["failures"]]
    report["failures"]=all_fail; report["failure_count"]=len(all_fail)
    (args.output/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if all_fail:
        print("UI ACCEPTANCE: FEHLER"); [print("-",x) for x in all_fail]
        if args.strict: raise SystemExit(1)
    else: print(f"UI ACCEPTANCE PASS: {len(browsers)} Browser × {len(contract['scenarios'])} Szenarien")

if __name__=="__main__": main()
