import re
import unittest
from pathlib import Path


HTML_PATH = Path(__file__).parents[1] / "index.html"

FOCUSREWARD_URL = "https://github.com/Vexun/FocusReward"
GACHABOORU_URL = "https://github.com/Vexun/Gachabooru"
FOCUSREWARD_DESCRIPTION = (
    "Earn points by completing tasks, then spend them to unlock distracting sites "
    "for a limited time — a desktop app, browser extension, and local API."
)
GACHABOORU_DESCRIPTION = (
    "A local, single-user gacha game built on Danbooru images. Draw five cards, "
    "call heads or tails to keep them, and bank your collection."
)
CONSTRUCTION_MESSAGE = "Still under construction, this is just temporary"


class ProjectsViewTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = HTML_PATH.read_text(encoding="utf-8")
        cls.flat = re.sub(r"\s+", " ", cls.html)

    def test_projects_view_and_title(self):
        self.assertRegex(self.html, r'class="view projects"[^>]*id="projects"')
        self.assertIn('<h2 class="projects-title">Projects</h2>', self.html)

    def test_project_cards_link_to_repositories(self):
        for name, url, description in (
            ("FocusReward", FOCUSREWARD_URL, FOCUSREWARD_DESCRIPTION),
            ("Gachabooru", GACHABOORU_URL, GACHABOORU_DESCRIPTION),
        ):
            self.assertIn(f'href="{url}"', self.flat)
            self.assertIn(f"<h3>{name}</h3>", self.flat)
            self.assertIn(description, self.flat)

        self.assertEqual(self.flat.count('target="_blank"'), 2)
        self.assertEqual(self.flat.count('rel="noopener noreferrer"'), 2)

    def test_construction_message_follows_projects(self):
        self.assertIn(CONSTRUCTION_MESSAGE, self.flat)
        self.assertLess(
            self.flat.index("Gachabooru</h3>"),
            self.flat.index(CONSTRUCTION_MESSAGE),
        )

    def test_social_links_are_shared_not_duplicated(self):
        self.assertEqual(self.html.count('class="social-links"'), 1)
        self.assertNotIn("social-links--inline", self.html)
        self.assertNotIn("cloneNode", self.html)

    def test_page_indicator(self):
        self.assertIn('class="page-dots', self.html)
        self.assertEqual(self.html.count('class="dot"'), 2)
        self.assertIn('data-view="0"', self.html)
        self.assertIn('data-view="1"', self.html)
        self.assertIn('aria-label="Home"', self.html)
        self.assertIn('aria-label="Projects"', self.html)

        active = re.findall(r'<button[^>]*aria-current="page"[^>]*>', self.html)
        self.assertEqual(len(active), 1)
        self.assertIn('data-view="0"', active[0])

    def test_indicator_dots_expand_to_lines_on_hover(self):
        self.assertRegex(self.html, r"\.dot::after\s*\{[^}]*width:\s*5px")
        self.assertRegex(self.html, r"\.dot::after\s*\{[^}]*border-radius:\s*50%")
        self.assertRegex(
            self.html, r'\.dot\[aria-current="page"\]::after\s*\{[^}]*width:\s*6px'
        )
        self.assertRegex(self.html, r"\.dot:hover::after\s*\{[^}]*width:\s*20px")
        self.assertRegex(
            self.html,
            r'\.page-dots:hover\s+\.dot\[aria-current="page"\]::after\s*\{[^}]*width:\s*24px',
        )
        self.assertRegex(
            self.html, r"\.page-dots:hover\s*\{[^}]*--dots-gap:\s*0\.3rem"
        )
        self.assertRegex(
            self.html,
            r"\.page-dots:hover\s+\.dot::after\s*\{[^}]*transform:\s*translateY\(0\)",
        )

        dots = re.search(r"\.page-dots\s*\{([^}]*)\}", self.html)
        self.assertIn("--dots-gap: 0rem", dots.group(1))
        self.assertIn("translateY(-14px)", self.html)
        self.assertIn("translateY(14px)", self.html)

    def test_current_page_indicator_is_centered(self):
        self.assertIn('class="page-dots page-dots--home"', self.html)
        self.assertRegex(self.html, r"\.page-dots--projects\s*\{[^}]*translateY")
        self.assertIn('classList.toggle("page-dots--home"', self.html)
        self.assertIn('classList.toggle("page-dots--projects"', self.html)

    def test_slide_and_input_wiring(self):
        track_styles = re.search(r"\.track\s*\{([^}]*)\}", self.html)
        if track_styles is None:
            self.fail("track styles are missing")
        styles = track_styles.group(1)
        self.assertIn("transform:", styles)
        self.assertIn("transition: transform", styles)

        for token in (
            "translateX(",
            "pointerdown",
            "pointerup",
            "#projects",
            "ArrowRight",
            "wheel",
            "deltaY",
        ):
            self.assertIn(token, self.html)


if __name__ == "__main__":
    unittest.main()
