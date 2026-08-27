from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unittest

from app import ROOT_DIR


class DashboardParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids: set[str] = set()
        self.i18n_keys: set[str] = set()
        self.aria_live: dict[str, str] = {}
        self.weekdays: list[str] = []
        self._weekday_depth = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.add(element_id)
            if values.get("aria-live"):
                self.aria_live[element_id] = values["aria-live"]
        key = values.get("data-i18n")
        if key:
            self.i18n_keys.add(key)
        classes = set((values.get("class") or "").split())
        if "weekday-row" in classes:
            self._weekday_depth += 1

    def handle_endtag(self, tag):
        if tag == "div" and self._weekday_depth:
            self._weekday_depth -= 1

    def handle_data(self, data):
        if self._weekday_depth:
            text = data.strip()
            if text:
                self.weekdays.append(text)


class DashboardContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT_DIR / "web" / "index.html").read_text(encoding="utf-8")
        cls.js = (ROOT_DIR / "web" / "app.js").read_text(encoding="utf-8")
        cls.css = (ROOT_DIR / "web" / "styles.css").read_text(encoding="utf-8")
        cls.texts = json.loads((ROOT_DIR / "web" / "dashboard-texts.de.v1.json").read_text(encoding="utf-8"))
        cls.parser = DashboardParser()
        cls.parser.feed(cls.html)

    def test_required_dashboard_regions_exist(self):
        required = {
            "monthGrid", "todoList", "eventList", "reminderRegion", "systemSummary",
            "developerPanel", "settingsPanel", "upcomingList", "readyPill", "nextTitle",
        }
        self.assertTrue(required.issubset(self.parser.ids), required - self.parser.ids)

    def test_dashboard_text_catalog_is_versioned_german_and_complete(self):
        self.assertEqual(self.texts.get("schema_version"), 1)
        self.assertEqual(self.texts.get("catalog_version"), "1.0.0")
        self.assertEqual(self.texts.get("language"), "de")
        messages = self.texts.get("messages")
        self.assertIsInstance(messages, dict)
        missing = sorted(self.parser.i18n_keys - set(messages))
        self.assertEqual(missing, [])
        self.assertTrue(all(isinstance(messages[key], str) and messages[key].strip() for key in self.parser.i18n_keys))

    def test_month_calendar_is_monday_to_sunday(self):
        for weekday in ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"):
            self.assertIn(f">{weekday}<", self.html)
        self.assertIn("(start.getDay()+6)%7", self.js)

    def test_dashboard_uses_tested_core_api_contracts(self):
        required = (
            "/api/status",
            "/api/todos",
            "/api/events?limit=5",
            "/api/calendar?view=month",
            "/api/calendar?view=year",
            "/api/calendar/reminders/due",
            "/reminders/${reminder.minutes_before}/ack",
        )
        for marker in required:
            self.assertIn(marker, self.js)

    def test_reminders_are_not_acknowledged_while_page_is_hidden(self):
        self.assertIn("if(document.visibilityState!=='visible') return;", self.js)
        self.assertIn("button.addEventListener('click',()=>ackReminder", self.js)
        self.assertNotRegex(self.js, r"renderReminders\([^)]*\)[\s\S]{0,500}await\s+api\([^\n]*?/ack")
        self.assertIn("const REMINDER_POLL_MS=60000", self.js)
        self.assertEqual(self.parser.aria_live.get("reminderRegion"), "assertive")

    def test_user_titles_are_inserted_as_text_not_html(self):
        self.assertIn("title.textContent=event.title", self.js)
        self.assertIn("title.textContent=item.title", self.js)
        self.assertNotIn("innerHTML=event.title", self.js)
        self.assertNotIn("innerHTML=item.title", self.js)

    def test_diagnostics_do_not_dump_full_config(self):
        diagnostic_match = re.search(r"const diagnostic=\{([\s\S]*?)\n  \};", self.js)
        self.assertIsNotNone(diagnostic_match)
        block = diagnostic_match.group(1)
        self.assertNotIn("config:", block)
        self.assertNotIn("active_project", block)
        self.assertNotIn("favorites", block)

    def test_responsive_and_accessibility_guards_are_present(self):
        self.assertIn("prefers-reduced-motion:reduce", self.css)
        self.assertIn("button:focus-visible", self.css)
        self.assertIn("@media(max-width:720px)", self.css)
        self.assertIn("@media(max-width:430px)", self.css)
        self.assertIn('class="skip-link"', self.html)


if __name__ == "__main__":
    unittest.main()
