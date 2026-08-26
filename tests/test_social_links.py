import re
import unittest
from pathlib import Path


HTML_PATH = Path(__file__).parents[1] / "index.html"


class SocialLinksTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = HTML_PATH.read_text(encoding="utf-8")

    def test_modular_data_and_rendering(self):
        self.assertRegex(self.html, r"const\s+socialLinks\s*=\s*\[")
        self.assertRegex(self.html, r"socialLinks\.forEach\s*\(")
        self.assertIn('document.createElement("a")', self.html)
        self.assertIn("socialLinksContainer.append(link)", self.html)

    def test_required_links_and_labels(self):
        self.assertIn('{ label: "X.com", url: "https://x.com/" }', self.html)
        self.assertIn('{ label: "GitHub", url: "https://github.com/" }', self.html)

    def test_bottom_centered_independent_group(self):
        social_styles = re.search(r"\.social-links\s*\{([^}]*)\}", self.html)
        if social_styles is None:
            self.fail("social-links styles are missing")
        styles = social_styles.group(1)
        self.assertIn("position: fixed", styles)
        self.assertIn("bottom:", styles)
        self.assertIn("left: 50%", styles)
        self.assertIn("transform: translateX(-50%)", styles)
        self.assertIn("display: flex", styles)
        self.assertIn("justify-content: center", styles)

    def test_opacity_states(self):
        self.assertRegex(self.html, r"\.social-links\s+a\s*\{[^}]*opacity:\s*0\.[0-9]+")
        self.assertRegex(self.html, r"\.social-links\s+a:hover\s*\{[^}]*opacity:\s*1")

    def test_external_link_security_attributes(self):
        self.assertIn('link.target = "_blank"', self.html)
        self.assertIn('link.rel = "noopener noreferrer"', self.html)


if __name__ == "__main__":
    unittest.main()
