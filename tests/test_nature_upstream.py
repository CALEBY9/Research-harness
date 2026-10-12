"""Verify real Git review preparation without network or live skill writes."""
import importlib.util
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "nature_upstream", Path(__file__).resolve().parents[1] / "scripts/nature_upstream.py")
updater = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(updater)


class NatureUpstreamTests(unittest.TestCase):
    def setUp(self):
        box = tempfile.TemporaryDirectory()
        self.addCleanup(box.cleanup)
        self.base = Path(box.name)
        self.root = self.base / "harness"
        (self.root / "docs").mkdir(parents=True)
        self.mappings = {"nature-writing": "skills/nature-writing",
                         "nature-shared": "skills/nature-shared",
                         "researchwrite": "skills/nature-proposal-writer"}
        (self.root / "docs/nature_upstream.json").write_text(json.dumps(
            {"skills": self.mappings, "scoped_import_commit": "1" * 40,
             "watch_initial_commit": "1" * 40}), encoding="utf-8")
        for name in self.mappings:
            folder = self.root / "skills" / name
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text("local " + name + "\n", encoding="utf-8")
        self.sha = "a" * 40

    def upstream_fixture(self):
        repo = self.base / "upstream"
        updater.git("init", "--initial-branch=main", repo)
        for name, mapping in self.mappings.items():
            folder = repo / mapping
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text("base " + name + "\n", encoding="utf-8")
        updater.git("add", ".", cwd=repo)
        self.commit(repo, "base")
        old = updater.git("rev-parse", "HEAD", cwd=repo).decode().strip()
        (repo / self.mappings["nature-writing"] / "SKILL.md").write_text(
            "upstream changed\n", encoding="utf-8")
        (repo / self.mappings["nature-shared"] / "new-reference.md").write_text(
            "new shared reference\n", encoding="utf-8")
        updater.git("add", ".", cwd=repo)
        self.commit(repo, "change")
        new = updater.git("rev-parse", "HEAD", cwd=repo).decode().strip()
        return repo, old, new

    @staticmethod
    def commit(repo, message):
        updater.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                    "commit", "-m", message, cwd=repo)

    def test_no_baseline_requires_manual_comparison(self):
        rows, diff = updater.differences({"a.md": b"local\n"}, {"a.md": b"upstream\n"})
        self.assertEqual(rows[0]["comparison"], "manual_comparison")
        self.assertIn("-local", diff)
        self.assertIn("+upstream", diff)

    def test_three_way_classification_preserves_both_edits(self):
        original = {"a": b"old", "b": b"old", "c": b"old"}
        local = {"a": b"local", "b": b"old", "c": b"local"}
        new = {"a": b"old", "b": b"upstream", "c": b"upstream"}
        rows, _ = updater.differences(local, new, original)
        self.assertEqual([r["comparison"] for r in rows],
                         ["local_only", "upstream_only", "both_changed"])
        self.assertEqual(local["c"], b"local")

    def test_removed_upstream_file_is_explicit(self):
        rows, _ = updater.differences({"keep.md": b"local"}, {}, {"keep.md": b"old"})
        self.assertFalse(rows[0]["upstream_present"])
        self.assertTrue(rows[0]["local_present"])
        self.assertEqual(rows[0]["comparison"], "both_changed")

    def test_existing_target_never_overwritten(self):
        target = self.base / "review"
        target.mkdir()
        sentinel = target / "author.txt"
        sentinel.write_text("retain")
        with self.assertRaises(ValueError):
            updater.prepare(target, self.sha, ["nature-writing"], root=self.root)
        self.assertEqual(sentinel.read_text(), "retain")
        self.assertEqual(list(target.iterdir()), [sentinel])

    def test_source_and_live_discovery_targets_rejected(self):
        for target in [self.root / "skills/review", self.base / ".agents/skills/review",
                       self.root, self.base]:
            with self.subTest(target=str(target)), self.assertRaises(ValueError):
                updater.prepare(target, self.sha, ["nature-writing"], root=self.root)
        self.assertFalse((self.root / "skills/review").exists())
        self.assertFalse((self.base / ".agents").exists())

    def test_moving_branch_and_unknown_skill_rejected_before_writing(self):
        target = self.base / "review"
        with self.assertRaises(ValueError):
            updater.prepare(target, "main", ["nature-writing"], root=self.root)
        with self.assertRaises(ValueError):
            updater.prepare(target, self.sha, ["unadopted"], root=self.root)
        self.assertFalse(target.exists())

    def test_real_prepare_retains_local_files_and_reports_conflict(self):
        repo, old, new = self.upstream_fixture()
        source = self.root / "skills/nature-writing/SKILL.md"
        before = source.read_bytes()
        target = self.base / "review"
        with patch.object(updater, "UPSTREAM", str(repo)):
            result = updater.prepare(target, new, ["nature-writing"], old, self.root)
        self.assertEqual(source.read_bytes(), before)
        self.assertEqual((target / "local_skills/nature-writing/SKILL.md").read_bytes(), before)
        self.assertEqual((target / "upstream_skills/nature-writing/SKILL.md").read_bytes(),
                         b"upstream changed\n")
        self.assertEqual((target / "base_skills/nature-writing/SKILL.md").read_bytes(),
                         b"base nature-writing\n")
        rows = {row["path"]: row for row in result["files"]}
        self.assertEqual(rows["nature-writing/SKILL.md"]["comparison"], "both_changed")
        self.assertIn("nature-shared/new-reference.md", rows)
        self.assertFalse(result["source_changed"])
        self.assertFalse(result["live_installation_changed"])
        self.assertFalse(result["automatic_merge"])

    def test_directory_mapping_and_missing_baseline_are_honest(self):
        repo, _, new = self.upstream_fixture()
        target = self.base / "review"
        with patch.object(updater, "UPSTREAM", str(repo)):
            result = updater.prepare(target, new, ["researchwrite"], root=self.root)
        self.assertIsNone(result["base_commit"])
        self.assertTrue((target / "upstream_skills/researchwrite/SKILL.md").is_file())
        self.assertFalse((target / "upstream_skills/nature-proposal-writer").exists())
        self.assertEqual(result["selected_skills"], ["researchwrite", "nature-shared"])

    def test_unavailable_base_fails_without_success_record(self):
        repo, _, new = self.upstream_fixture()
        target = self.base / "review"
        source = self.root / "skills/nature-writing/SKILL.md"
        before = source.read_bytes()
        with patch.object(updater, "UPSTREAM", str(repo)), self.assertRaises(ValueError):
            updater.prepare(target, new, ["nature-writing"], "0" * 40, self.root)
        self.assertFalse((target / "review.json").exists())
        self.assertEqual(source.read_bytes(), before)

    def test_upstream_git_symlink_rejected(self):
        repo, _, _ = self.upstream_fixture()
        blob = subprocess.run(["git", "hash-object", "-w", "--stdin"],
                              cwd=repo, input=b"../../outside", capture_output=True, check=True)
        updater.git("update-index", "--add", "--cacheinfo",
                    "120000," + blob.stdout.decode().strip() + ",skills/nature-writing/link", cwd=repo)
        self.commit(repo, "link")
        revision = updater.git("rev-parse", "HEAD", cwd=repo).decode().strip()
        with self.assertRaises(ValueError):
            updater.snapshot(repo, revision, ["nature-writing"], self.mappings)

    def test_check_reads_remote_without_altering_source(self):
        repo, _, new = self.upstream_fixture()
        before = (self.root / "docs/nature_upstream.json").read_bytes()
        with patch.object(updater, "UPSTREAM", str(repo)):
            result = updater.check(self.root)
        self.assertEqual(result["upstream_commit"], new)
        self.assertEqual((self.root / "docs/nature_upstream.json").read_bytes(), before)

    def test_watch_unchanged_commit_does_not_prepare_or_touch_sources(self):
        before = updater.local_snapshot(self.root, list(self.mappings))
        observation = {"upstream_commit": "1" * 40, "source_changed": False,
                       "live_installation_changed": False}
        with patch.object(updater, "check", return_value=observation), \
                patch.object(updater, "prepare") as staging:
            result = updater.watch(self.root)
        staging.assert_not_called()
        self.assertEqual(result["status"], "WAITING_FOR_UPSTREAM_UPDATE")
        self.assertIsNone(result["pending_review"])
        self.assertFalse(result["automatic_install"])
        self.assertEqual(updater.local_snapshot(self.root, list(self.mappings)), before)

    def test_watch_new_commit_stages_once_and_retains_pending_review(self):
        repo, _, new = self.upstream_fixture()
        before = updater.local_snapshot(self.root, list(self.mappings))
        with patch.object(updater, "UPSTREAM", str(repo)):
            first = updater.watch(self.root)
            with patch.object(updater, "prepare") as staging:
                second = updater.watch(self.root)
        staging.assert_not_called()
        self.assertEqual(first["status"], "UPDATE_AWAITING_REVIEW")
        self.assertEqual(second["pending_review"], first["pending_review"])
        folder = self.root / first["pending_review"]["directory"]
        review = json.loads((folder / "review.json").read_text(encoding="utf-8"))
        self.assertEqual(review["selected_skills"], list(self.mappings))
        self.assertEqual(review["upstream_commit"], new)
        self.assertIsNone(review["base_commit"])
        self.assertFalse(review["automatic_merge"])
        self.assertEqual(updater.local_snapshot(self.root, list(self.mappings)), before)

    def test_watch_failed_stage_keeps_observation_and_retries(self):
        directory = self.root / "local_state/nature_upstream_watch"
        directory.mkdir(parents=True)
        state_path = directory / "watch_state.json"
        before = json.dumps({"observed_commit": "1" * 40, "pending_review": None})
        state_path.write_text(before, encoding="utf-8")
        observation = {"upstream_commit": self.sha, "source_changed": False,
                       "live_installation_changed": False}
        with patch.object(updater, "check", return_value=observation), \
                patch.object(updater, "prepare", side_effect=ValueError("fetch failed")), \
                self.assertRaisesRegex(ValueError, "fetch failed"):
            updater.watch(self.root)
        self.assertEqual(state_path.read_text(encoding="utf-8"), before)
        failed = json.loads((directory / "check_result.json").read_text(encoding="utf-8"))
        self.assertEqual(failed["status"], "CHECK_FAILED")
        with patch.object(updater, "check", return_value=observation), \
                patch.object(updater, "prepare", return_value={"files": []}) as staging:
            result = updater.watch(self.root)
        staging.assert_called_once()
        self.assertEqual(result["status"], "UPDATE_AWAITING_REVIEW")

    def test_watch_network_failure_is_visible_without_success_state(self):
        with patch.object(updater, "check", side_effect=ValueError("offline")), \
                self.assertRaisesRegex(ValueError, "offline"):
            updater.watch(self.root)
        directory = self.root / "local_state/nature_upstream_watch"
        self.assertFalse((directory / "watch_state.json").exists())
        report = json.loads((directory / "check_result.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "CHECK_FAILED")
        self.assertEqual(report["error"], "offline")

    def test_monitor_next_check_follows_local_nine_oclock_schedule(self):
        zone = timezone(timedelta(hours=8))
        morning = datetime(2026, 10, 12, 8, 30, tzinfo=zone)
        self.assertEqual(updater.next_check(morning), morning.replace(hour=9, minute=0))
        exact = morning.replace(hour=9, minute=0)
        self.assertEqual(updater.next_check(exact), exact + timedelta(days=1))
        afternoon = morning.replace(hour=14)
        self.assertEqual(updater.next_check(afternoon), exact + timedelta(days=1))


if __name__ == "__main__":
    unittest.main()
