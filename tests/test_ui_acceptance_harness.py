import re
import unittest

from app import ROOT_DIR
from scripts.ui_acceptance import inline_page


class UiAcceptanceHarnessTests(unittest.TestCase):
    def test_product_stylesheets_are_embedded_from_index_contract(self):
        page = inline_page("window.__fixture_ready = true;")
        self.assertIn('data-inline-source="styles.css"', page)
        self.assertIn('data-inline-source="acceptance.css"', page)
        self.assertNotRegex(page, r'<link\s+rel="stylesheet"\s+href="/')
        self.assertIn("grid-template-columns:repeat(12,minmax(0,1fr))", page)

    def test_fixture_executes_before_product_javascript(self):
        marker = "window.__fixture_ready = true;"
        page = inline_page(marker)
        fixture_position = page.index(marker)
        app_position = page.index("const state=")
        self.assertLess(fixture_position, app_position)
        self.assertNotRegex(page, r'<script\s+src="/app\.js')

    def test_harness_does_not_depend_on_specific_dashboard_query_version(self):
        page = inline_page("window.__fixture_ready = true;")
        self.assertNotIn("?contract=dashboard-v2.3", page)
        self.assertEqual(len(re.findall(r'data-inline-source="(?:styles|acceptance)\.css"', page)), 2)

    def test_ci_entrypoint_is_only_a_thin_wrapper(self):
        ci = (ROOT_DIR / "scripts" / "ui_acceptance_ci.py").read_text(encoding="utf-8")
        self.assertIn("from ui_acceptance import main", ci)
        self.assertNotIn("def run_browser", ci)
        self.assertNotIn("def inline_page_with_fixture", ci)
        self.assertNotIn("dashboard-v2.", ci)
        self.assertLess(len(ci.splitlines()), 25)


if __name__ == "__main__":
    unittest.main()
