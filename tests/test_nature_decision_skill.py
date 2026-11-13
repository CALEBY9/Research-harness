"""Check the decision skill's bundled evidence and routing contracts."""
import json
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "nature-decision"
EXPECTED_CARDS = {
    "business-investment.md": ("李嘉诚", "巴菲特"),
    "engineering-strategy.md": ("马斯克", "毛泽东"),
    "research-science.md": ("施一公", "颜宁", "谷保静", "奥斯特罗姆"),
    "learning-judgment.md": ("卡尼曼与阿莫斯·特沃斯基", "邓洛斯基与杰弗里·卡皮克"),
}
EXPECTED_ROUTES = {
    "RA-DECISION-01-INVESTMENT": "nature-decision",
    "RA-DECISION-02-LEARNING": "nature-decision",
    "RA-DECISION-03-RESEARCH-RESOURCES": "nature-decision",
    "RA-DECISION-04-EXPLICIT-SCIENTIFIC": "nature-decision",
    "RA-DECISION-05-EXPERT-LENS": "nature-decision",
    "RA-DECISION-06-HOME-PURCHASE": "nature-decision",
    "RA-DECISION-07-UNBUNDLED-EXPERT": "nature-decision",
    "RA-DISTILLER-01-PUBLIC-DECISION-FRAMEWORK": "nature-scholar-distiller",
    "RA-INSIGHT-01-PHENOMENON": "nature-scientific-insight",
    "RA-INSIGHT-02-NOVEL-PUBLISHABLE": "nature-scientific-insight",
}


class DecisionSkillTests(unittest.TestCase):
    def test_entrypoint_links_and_explicit_invocation(self):
        body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: nature-decision", body)
        links = re.findall(r"\]\((references/[^)]+\.md)\)", body)
        self.assertEqual(
            {Path(link).name for link in links},
            set(EXPECTED_CARDS),
        )
        for link in links:
            with self.subTest(link=link):
                self.assertTrue((SKILL / link).is_file())
        metadata = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("$nature-decision", metadata)

    def test_each_expert_card_has_sources_transfer_and_limits(self):
        for filename, names in EXPECTED_CARDS.items():
            text = (SKILL / "references" / filename).read_text(encoding="utf-8")
            sections = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
            cards = dict(zip(sections[1::2], sections[2::2]))
            for name in names:
                with self.subTest(file=filename, expert=name):
                    matching = [body for title, body in cards.items() if name in title]
                    self.assertEqual(len(matching), 1)
                    card = matching[0]
                    self.assertIn("**公开证据**", card)
                    self.assertIn("**可迁移启发（推断）**", card)
                    self.assertIn("**如何使用**", card)
                    self.assertIn("**失效与边界**", card)
                    source_block = card.split("**可迁移启发（推断）**", 1)[0]
                    urls = set(re.findall(r"https://[^)\s]+", source_block))
                    self.assertGreaterEqual(len(urls), 2)
                    for url in urls:
                        self.assertTrue(urlsplit(url).netloc)

    def test_decision_and_scientific_routes_have_distinct_owners(self):
        path = ROOT / "skills" / "research-agent" / "references" / "copilot-regression.json"
        cases = json.loads(path.read_text(encoding="utf-8"))["cases"]
        indexed = {case["case_id"]: case for case in cases}
        self.assertEqual(len(indexed), len(cases), "Duplicate regression case IDs")
        for case_id, owner in EXPECTED_ROUTES.items():
            with self.subTest(case=case_id):
                self.assertEqual(indexed[case_id]["expected_owner"], owner)
                self.assertTrue(indexed[case_id]["required_boundary"])
        self.assertIn(
            "nature-decision",
            indexed["RA-INSIGHT-01-PHENOMENON"]["forbidden_owners"],
        )
        self.assertIn(
            "nature-decision",
            indexed["RA-DISTILLER-01-PUBLIC-DECISION-FRAMEWORK"]["forbidden_owners"],
        )


if __name__ == "__main__":
    unittest.main()
