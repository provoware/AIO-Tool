from pathlib import Path
import unittest

from app import ROOT_DIR


class HelperUiContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css=(ROOT_DIR/"web"/"helper-ui.css").read_text(encoding="utf-8")
        cls.native_html=(ROOT_DIR/"web"/"native-acceptance.html").read_text(encoding="utf-8")
        cls.native_js=(ROOT_DIR/"web"/"native-acceptance.js").read_text(encoding="utf-8")
        cls.safe_html=(ROOT_DIR/"web"/"safe-file-sim.html").read_text(encoding="utf-8")
        cls.safe_js=(ROOT_DIR/"web"/"safe-file-sim.js").read_text(encoding="utf-8")
        cls.native_server=(ROOT_DIR/"scripts"/"native_acceptance_runner.py").read_text(encoding="utf-8")
        cls.safe_server=(ROOT_DIR/"scripts"/"safe_file_simulator.py").read_text(encoding="utf-8")

    def test_helper_pages_use_external_shared_css_without_inline_style(self):
        for html in (self.native_html,self.safe_html):
            self.assertIn('href="/helper-ui.css"',html)
            self.assertNotIn("<style>",html)
            self.assertNotIn('style="',html)

    def test_helper_csp_no_longer_requires_unsafe_inline_styles(self):
        for server in (self.native_server,self.safe_server):
            self.assertIn("style-src 'self'",server)
            self.assertNotIn("style-src 'unsafe-inline'",server)
            self.assertIn('"/helper-ui.css"',server)

    def test_native_report_link_does_not_nest_button_in_anchor(self):
        self.assertIn('class="button-like" href="/report.txt"',self.native_html)
        self.assertNotIn('<a href="/report.txt" download><button',self.native_html)

    def test_native_and_safe_scripts_do_not_use_inner_html(self):
        self.assertNotIn("innerHTML",self.native_js)
        self.assertNotIn("innerHTML",self.safe_js)

    def test_native_progress_uses_semantic_progress_element(self):
        self.assertIn('<progress id="progressBar"',self.native_html)
        self.assertIn("$('#progressBar').value=report.progress_percent",self.native_js)

    def test_safe_file_policy_exposes_pressed_state(self):
        self.assertIn('aria-pressed="true"',self.safe_html)
        self.assertIn("setAttribute('aria-pressed'",self.safe_js)

    def test_shared_helper_ui_keeps_touch_targets_and_reduced_motion(self):
        self.assertIn("min-height:44px",self.css)
        self.assertIn("prefers-reduced-motion:reduce",self.css)


if __name__=="__main__":
    unittest.main()
