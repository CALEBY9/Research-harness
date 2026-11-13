"""Exercise the real CLI from a source-only copy with an empty user profile."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DistributionCLITests(unittest.TestCase):
    def test_fresh_profile_install_and_check_without_private_bindings(self):
        with tempfile.TemporaryDirectory(prefix="research_distribution_") as directory:
            base = Path(directory)
            source = base / "source copy"
            (source / "scripts").mkdir(parents=True)
            shutil.copy2(ROOT / "scripts/harness.py", source / "scripts/harness.py")
            shutil.copytree(ROOT / "skills", source / "skills",
                            ignore=shutil.ignore_patterns("figures4papers", "__pycache__", "*.pyc"))
            for name in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
                shutil.copy2(ROOT / name, source / name)
            profile = base / "empty profile"
            profile.mkdir()
            target = profile / ".agents/skills"
            env = dict(os.environ, HOME=str(profile), USERPROFILE=str(profile),
                       CODEX_HOME=str(profile / ".codex"), PYTHONUTF8="1")
            env.pop("RESEARCH_AGENT_KB_ROOT", None)

            def run(*arguments):
                return subprocess.run(
                    [sys.executable, "-I", "-S", "-X", "utf8", "-B", str(source / "scripts/harness.py"), *arguments],
                    cwd=base, env=env, text=True, encoding="utf-8",
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)

            validated = run("validate")
            self.assertEqual(validated.returncode, 0, validated.stderr)
            self.assertEqual(json.loads(validated.stdout)["status"], "PASS")
            preview = run("install", "--target", "~/.agents/skills", "--dry-run")
            self.assertEqual(preview.returncode, 0, preview.stderr)
            self.assertFalse(target.exists())
            installed = run("install", "--target", "~/.agents/skills")
            self.assertEqual(installed.returncode, 0, installed.stderr)
            self.assertEqual(json.loads(installed.stdout)["status"], "INSTALLED")
            catalog = json.loads((source / "skills/catalog.json").read_text(encoding="utf-8"))
            names = {p.parent.name for p in target.glob("*/SKILL.md")}
            self.assertEqual(names, set(catalog["active"]))
            self.assertTrue((target / "shared-references/scripts/clean_final_scanner.py").is_file())
            self.assertTrue((target / "nature-shared/SKILL.md").is_file())
            self.assertTrue((target / "NATURE_LICENSE").is_file())
            self.assertFalse((target / "ars-academic-writing").exists())
            self.assertFalse((target / "nature-figure/assets/figures4papers").exists())
            checked = run("check", "--target", "~/.agents/skills")
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertEqual(json.loads(checked.stdout)["status"], "PASS")
            original = (target / "research-agent/SKILL.md").read_bytes()
            repeated = run("install", "--target", "~/.agents/skills")
            self.assertNotEqual(repeated.returncode, 0)
            self.assertIn("Existing installation entries", repeated.stderr)
            self.assertEqual(original, (target / "research-agent/SKILL.md").read_bytes())
            self.assertFalse((profile / ".codex").exists())


if __name__ == "__main__":
    unittest.main()
