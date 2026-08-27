from html.parser import HTMLParser
import json
import re
import unittest

from app import ROOT_DIR
from app.config import THEMES
from app.instance_identity import UI_CONTRACT_VERSION


class DashboardParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=set();self.i18n_keys=set();self.aria_live={};self.weekdays=[];self.theme_ids=set();self._weekday_depth=0

    def handle_starttag(self,tag,attrs):
        values=dict(attrs);element_id=values.get("id")
        if element_id:
            self.ids.add(element_id)
            if values.get("aria-live"):self.aria_live[element_id]=values["aria-live"]
        if values.get("data-i18n"):self.i18n_keys.add(values["data-i18n"])
        if values.get("data-theme"):self.theme_ids.add(values["data-theme"])
        if "weekday-row" in set((values.get("class") or "").split()):self._weekday_depth+=1

    def handle_endtag(self,tag):
        if tag=="div" and self._weekday_depth:self._weekday_depth-=1

    def handle_data(self,data):
        if self._weekday_depth and data.strip():self.weekdays.append(data.strip())


class DashboardContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=(ROOT_DIR/"web"/"index.html").read_text(encoding="utf-8")
        cls.js=(ROOT_DIR/"web"/"app.js").read_text(encoding="utf-8")
        cls.css=(ROOT_DIR/"web"/"styles.css").read_text(encoding="utf-8")
        cls.texts=json.loads((ROOT_DIR/"web"/"dashboard-texts.de.v1.json").read_text(encoding="utf-8"))
        cls.parser=DashboardParser();cls.parser.feed(cls.html)

    def test_required_dashboard_regions_exist(self):
        required={"monthGrid","todoList","eventList","reminderRegion","systemSummary","developerPanel","settingsPanel","upcomingList","readyPill","nextTitle","bootGuard"}
        self.assertTrue(required.issubset(self.parser.ids),required-self.parser.ids)

    def test_dashboard_text_catalog_is_versioned_german_and_complete(self):
        self.assertEqual(self.texts.get("schema_version"),1)
        self.assertEqual(self.texts.get("catalog_version"),"1.0.0")
        self.assertEqual(self.texts.get("language"),"de")
        messages=self.texts.get("messages")
        self.assertIsInstance(messages,dict)
        self.assertEqual(sorted(self.parser.i18n_keys-set(messages)),[])

    def test_ui_contract_is_single_version(self):
        self.assertEqual(UI_CONTRACT_VERSION,"dashboard-v2.3")
        self.assertIn('content="dashboard-v2.3"',self.html)
        self.assertIn('contract=dashboard-v2.3',self.html)

    def test_theme_picker_matches_config_and_has_pressed_semantics(self):
        self.assertEqual(self.parser.theme_ids,THEMES)
        self.assertIn("aurora-glass",self.parser.theme_ids)
        self.assertIn('aria-pressed="false"',self.html)
        self.assertIn("setAttribute('aria-pressed'",self.js)

    def test_month_calendar_is_monday_to_sunday(self):
        for weekday in ("Mo","Di","Mi","Do","Fr","Sa","So"):
            self.assertIn(f">{weekday}<",self.html)
        self.assertIn("(start.getDay()+6)%7",self.js)

    def test_dashboard_uses_tested_core_api_contracts(self):
        for marker in ("/api/status","/api/todos","/api/events?limit=5","/api/calendar?view=month","/api/calendar?view=year","/api/calendar/reminders/due","/reminders/${reminder.minutes_before}/ack"):
            self.assertIn(marker,self.js)

    def test_reminders_are_not_acknowledged_while_page_is_hidden(self):
        self.assertRegex(self.js,r"if\(document\.visibilityState!==['\"]visible['\"]\)\s*return;")
        self.assertIn("addEventListener('click',()=>ackReminder",self.js)
        self.assertIn("const REMINDER_POLL_MS=60000",self.js)
        self.assertEqual(self.parser.aria_live.get("reminderRegion"),"assertive")

    def test_dynamic_user_content_avoids_inner_html(self):
        self.assertNotIn("innerHTML",self.js)
        self.assertIn("title.textContent=event.title",self.js)
        self.assertIn("title.textContent=item.title",self.js)

    def test_failed_loads_do_not_reuse_stale_or_fake_empty_data(self):
        self.assertIn("state.calendar=result?.calendar||null",self.js)
        self.assertIn("state.upcoming=result?.calendar?.events||null",self.js)
        self.assertIn("state.todos=todoResult||null",self.js)
        self.assertIn("state.events=eventResult?.events||null",self.js)
        self.assertIn("if(state.todos===null)",self.js)
        self.assertIn("if(state.events===null)",self.js)
        self.assertIn("if(state.upcoming===null)",self.js)

    def test_successful_todo_retry_clears_action_error(self):
        self.assertIn("clearError('todo-action')",self.js)

    def test_boot_guard_has_success_and_failure_paths(self):
        self.assertIn("guard.classList.add('ready')",self.js)
        self.assertIn("boot().catch",self.js)
        self.assertIn("guard.classList.add('error')",self.js)

    def test_requests_have_timeout_and_clear_user_guidance(self):
        self.assertIn("const REQUEST_TIMEOUT_MS=8000",self.js)
        self.assertIn("controller.abort()",self.js)
        self.assertIn("Zeitüberschreitung: Das lokale Backend antwortet nicht rechtzeitig",self.js)
        self.assertIn("Lokales Backend nicht erreichbar",self.js)

    def test_refresh_has_single_flight_busy_feedback(self):
        self.assertIn("if(state.refreshing) return false",self.js)
        self.assertIn("setRefreshBusy(true)",self.js)
        self.assertIn("setRefreshBusy(false)",self.js)
        self.assertIn("button.setAttribute('aria-busy',String(busy))",self.js)
        self.assertIn("Prüfe …",self.js)

    def test_config_save_is_serialized_and_rolls_back_preview_on_failure(self):
        self.assertIn("if(state.configSaving) return",self.js)
        self.assertIn("setSettingsBusy(true)",self.js)
        self.assertIn("setSettingsBusy(false)",self.js)
        self.assertIn("if(previous) applyConfig(previous)",self.js)
        self.assertIn("applyConfig({...previous,...changes})",self.js)

    def test_settings_heading_is_programmatically_focusable(self):
        self.assertIn('id="settingsTitle" tabindex="-1"',self.html)

    def test_calendar_does_not_create_dozen_keyboard_stops(self):
        self.assertNotIn("cell.tabIndex=0",self.js)

    def test_diagnostics_do_not_dump_full_config(self):
        match=re.search(r"diagnostic=\{([\s\S]*?)\n  \};",self.js)
        self.assertIsNotNone(match)
        block=match.group(1)
        self.assertNotIn("active_project",block)
        self.assertNotIn("favorites",block)

    def test_responsive_and_accessibility_guards_are_present(self):
        self.assertIn("prefers-reduced-motion:reduce",self.css)
        self.assertIn("focus-visible",self.css)
        self.assertIn("@media(max-width:720px)",self.css)
        self.assertIn("@media(max-width:430px)",self.css)
        self.assertIn('class="skip-link"',self.html)

    def test_modern_theme_tokens_preserve_high_contrast_mode(self):
        for token in ("--panel-solid","--elevated","--accent2","--line-strong","--surface-tint"):
            self.assertIn(token,self.css)
        self.assertIn('html[data-theme="high-contrast"]',self.css)
        self.assertIn("--shadow:none",self.css)


if __name__=="__main__":
    unittest.main()
