"""Exercise staging/data-boundary failures without touching live installations."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "harness", Path(__file__).resolve().parents[1] / "scripts/harness.py")
harness = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(harness)


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.sandbox = tempfile.TemporaryDirectory()
        self.addCleanup(self.sandbox.cleanup)
        self.base = Path(self.sandbox.name)
        self.repo = self.base / "repo"
        skill = self.repo / "skills/research-agent"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: research-agent\ndescription: Research entry.\n---\nBody.\n", encoding="utf-8")
        (skill / "references/copilot-regression.json").write_text(
            json.dumps({"cases": [{"case_id": "sample", "expected_owner": "research-agent"}]}),
            encoding="utf-8")
        (self.repo / "skills/catalog.json").write_text(json.dumps({
            "active": ["research-agent"], "inactive": [], "shared": [],
            "support_files": [], "exclude": []}), encoding="utf-8")

    def test_valid_source_does_not_claim_behavioral_execution(self):
        result = harness.validate(self.repo)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["behavioral_evaluations_executed"], 0)

    def test_missing_owner_is_rejected(self):
        path = self.repo / "skills/research-agent/references/copilot-regression.json"
        path.write_text(json.dumps({"cases": [{"case_id": "bad", "expected_owner": "missing"}]}))
        self.assertIn("Missing route owner", " ".join(harness.validate(self.repo)["errors"]))

    def test_missing_active_source_is_still_rejected(self):
        (self.repo / "skills/research-agent/SKILL.md").unlink()
        with self.assertRaisesRegex(ValueError, "Catalog/source mismatch"):
            harness.load_catalog(self.repo)

    def test_secret_scan_reports_locator_without_secret(self):
        fake = "ghp_" + "X" * 36
        (self.repo / "example.txt").write_text(fake)
        result = harness.validate(self.repo)
        self.assertEqual(result["status"], "FAIL")
        self.assertNotIn(fake, json.dumps(result))
        self.assertIn("example.txt:1", json.dumps(result))

    def test_invalid_python_is_rejected(self):
        (self.repo / "bad.py").write_text("def broken(:\n")
        self.assertEqual(harness.validate(self.repo)["status"], "FAIL")

    def test_malformed_regression_pack_returns_visible_failure(self):
        path = self.repo / "skills/research-agent/references/copilot-regression.json"
        path.write_text("{broken")
        result = harness.validate(self.repo)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("JSON syntax", " ".join(result["errors"]))

    def test_stage_preserves_source_and_copies_exact_content(self):
        source = self.repo / "skills/research-agent/SKILL.md"
        before = source.read_bytes()
        target = self.base / "trial"
        result = harness.stage(target, ["research-agent"], self.repo)
        self.assertFalse(result["live_installation_changed"])
        self.assertEqual(before, source.read_bytes())
        self.assertEqual(before, (target / "research-agent/SKILL.md").read_bytes())

    def test_existing_target_is_never_overwritten(self):
        target = self.base / "existing"
        target.mkdir()
        sentinel = target / "work.txt"
        sentinel.write_text("user work")
        with self.assertRaises(ValueError):
            harness.stage(target, ["research-agent"], self.repo)
        self.assertEqual(sentinel.read_text(), "user work")
        self.assertEqual(list(target.iterdir()), [sentinel])

    def test_unknown_skill_fails_before_target_creation(self):
        target = self.base / "trial"
        with self.assertRaises(ValueError):
            harness.stage(target, ["research-agent", "missing"], self.repo)
        self.assertFalse(target.exists())

    def test_live_discovery_path_is_refused(self):
        target = self.base / ".agents/skills"
        with self.assertRaises(ValueError):
            harness.stage(target, ["research-agent"], self.repo)
        self.assertFalse(target.exists())

    def test_private_fixture_is_marked_unexecuted(self):
        path = self.repo / "skills/research-agent/references/copilot-regression.json"
        path.write_text(json.dumps({"cases": [{"case_id": "private", "fixture": {"path": "private.txt"}}]}))
        self.assertEqual(harness.validate(self.repo)["private_fixture_cases_not_executed"], ["private"])

    def distribution_fixture(self):
        shared = self.repo / "skills/shared-references"
        shared.mkdir()
        (shared / "evidence.md").write_text("Shared evidence instructions.\n", encoding="utf-8")
        inactive = self.repo / "skills/retired-writing"
        inactive.mkdir()
        (inactive / "SKILL.md").write_text(
            "---\nname: retired-writing\ndescription: Historical only.\n---\n", encoding="utf-8")
        (self.repo / "LICENSE").write_text("Fixture license.\n", encoding="utf-8")
        reference = self.repo / "skills/research-agent/reference-only"
        reference.mkdir()
        (reference / "sample.txt").write_text("Not licensed for redistribution.\n", encoding="utf-8")
        (self.repo / "skills/catalog.json").write_text(json.dumps({
            "active": ["research-agent"], "inactive": ["retired-writing"],
            "shared": ["shared-references"], "support_files": ["LICENSE"],
            "exclude": ["skills/research-agent/reference-only"]}), encoding="utf-8")

    def test_default_stage_includes_shared_and_license_but_not_inactive_or_excluded(self):
        self.distribution_fixture()
        target = self.base / "distribution"
        harness.stage(target, None, self.repo)
        self.assertTrue((target / "shared-references/evidence.md").is_file())
        self.assertTrue((target / "LICENSE").is_file())
        self.assertFalse((target / "retired-writing").exists())
        self.assertFalse((target / "research-agent/reference-only").exists())

    def test_install_dry_run_makes_no_directories(self):
        self.distribution_fixture()
        target = self.base / "new-project/.agents/skills"
        result = harness.install(target, None, self.repo, dry_run=True)
        self.assertEqual(result["status"], "INSTALL_PLAN")
        self.assertFalse(target.parent.exists())

    def test_removed_inactive_source_remains_rejected_and_detectable(self):
        self.distribution_fixture()
        retired = self.repo / "skills/retired-writing"
        (retired / "SKILL.md").unlink()
        retired.rmdir()
        self.assertEqual(harness.validate(self.repo)["status"], "PASS")
        target = self.base / "installed"
        with self.assertRaisesRegex(ValueError, "inactive skill"):
            harness.install(target, ["retired-writing"], self.repo)
        harness.install(target, None, self.repo)
        self.assertFalse((target / "retired-writing").exists())
        (target / "retired-writing").mkdir()
        (target / "retired-writing/SKILL.md").write_text("Old entry.\n", encoding="utf-8")
        result = harness.check_installation(target, None, self.repo)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["inactive_present"], ["retired-writing"])

    def test_explicit_install_preserves_unrelated_skills_and_checks_complete_package(self):
        self.distribution_fixture()
        target = self.base / "project/.agents/skills"
        other = target / "unrelated/SKILL.md"
        other.parent.mkdir(parents=True)
        other.write_text("User-owned skill.\n", encoding="utf-8")
        harness.install(target, ["research-agent"], self.repo)
        self.assertEqual(other.read_text(encoding="utf-8"), "User-owned skill.\n")
        self.assertEqual(harness.check_installation(target, None, self.repo)["status"], "PASS")

    def test_install_conflict_is_detected_before_any_file_is_copied(self):
        self.distribution_fixture()
        target = self.base / "installed"
        (target / "shared-references").mkdir(parents=True)
        sentinel = target / "shared-references/user.md"
        sentinel.write_text("Keep.\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Existing installation entries"):
            harness.install(target, None, self.repo)
        self.assertFalse((target / "research-agent").exists())
        self.assertFalse((target / "LICENSE").exists())
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "Keep.\n")

    def test_inactive_skill_cannot_be_explicitly_installed(self):
        self.distribution_fixture()
        target = self.base / "installed"
        with self.assertRaisesRegex(ValueError, "inactive skill"):
            harness.install(target, ["retired-writing"], self.repo)
        self.assertFalse(target.exists())

    def test_missing_shared_file_fails_installation_check(self):
        self.distribution_fixture()
        target = self.base / "installed"
        harness.install(target, None, self.repo)
        (target / "shared-references/evidence.md").unlink()
        result = harness.check_installation(target, None, self.repo)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("shared-references/evidence.md", result["missing"])

    def test_changed_skill_and_residual_inactive_entry_are_reported(self):
        self.distribution_fixture()
        target = self.base / "installed"
        harness.install(target, None, self.repo)
        (target / "research-agent/SKILL.md").write_text("Local edit.\n", encoding="utf-8")
        (target / "retired-writing").mkdir()
        (target / "retired-writing/SKILL.md").write_text("Old entry.\n", encoding="utf-8")
        result = harness.check_installation(target, None, self.repo)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("research-agent/SKILL.md", result["changed"])
        self.assertEqual(result["inactive_present"], ["retired-writing"])

    def test_install_rejects_source_overlap(self):
        with self.assertRaisesRegex(ValueError, "overlaps source"):
            harness.install(self.repo / "skills", None, self.repo)

    def test_catalog_rejects_path_traversal(self):
        path = self.repo / "skills/catalog.json"
        catalog = json.loads(path.read_text(encoding="utf-8"))
        catalog["support_files"] = ["../private.txt"]
        path.write_text(json.dumps(catalog), encoding="utf-8")
        self.assertEqual(harness.validate(self.repo)["status"], "FAIL")

    def test_new_skill_requires_explicit_active_or_inactive_classification(self):
        skill = self.repo / "skills/unclassified"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\nname: unclassified\ndescription: Not yet reviewed.\n---\n", encoding="utf-8")
        self.assertEqual(harness.validate(self.repo)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
