"""Offline fixture adapters test bookkeeping, never Research Agent improvement."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "behavioral_eval", Path(__file__).resolve().parents[1] / "scripts/behavioral_eval.py")
evaluation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evaluation)


class BehavioralEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "active.txt").write_text("old instructions", encoding="utf-8")
        (self.root / "candidate.txt").write_text("new instructions", encoding="utf-8")
        (self.root / "input.txt").write_text("read-only task", encoding="utf-8")
        adapter = self.root / "adapter.py"
        adapter.write_text('''import json, sys
r = json.load(sys.stdin)
assert "rubric" not in r and "held_out" not in r
print(json.dumps(dict(run_id=r["run_id"], runtime=r["runtime"], execution_kind="fixture",
    output="fixture response", trace=[{"event":"fixture"}], subagent_count=0,
    changed_files=[], validation_commands=[], owner_route=["research-agent"],
    runtime_evidence="offline fixture only")))
''', encoding="utf-8")
        self.manifest = dict(evaluation_scope="router_text", runtime=dict(
            model="fixture", reasoning_effort="none", permissions="none", tools=[],
            budget={"calls": 1}, isolation="fresh fixture process"),
            repetitions=1, timeout_seconds=10, adapter=[sys.executable, str(adapter)],
            rubric={m: "0 failed; 1 incomplete; 2 supported" for m in evaluation.METRICS},
            protected_rules=["read-only"], target_improvement="preserve task scope",
            active="active.txt", candidate="candidate.txt", cases=[dict(
                case_id=f"c{i}", split="selection", held_out=i > 2,
                withheld_from_candidate_design="independent fixture declaration",
                provenance="synthetic bookkeeping test, not behavioral evidence", input_path="input.txt")
                for i in range(5)])
        self.path = self.root / "manifest.json"
        self.directory = self.root / "trial"
        self.save_manifest()

    def save_manifest(self):
        self.path.write_text(json.dumps(self.manifest), encoding="utf-8")

    def freeze(self):
        return evaluation.freeze(self.path, self.directory)

    def model_receipts(self):
        """Fabricated in-test records only; never persisted as research evidence."""
        plan = evaluation.load_plan(self.directory)
        for i, case in enumerate(plan["cases"]):
            for arm in ("active", "candidate"):
                rid = f"case-{i+1:03d}-{arm}-1"
                work = self.directory / rid
                work.mkdir()
                evaluation.write_new(work / "receipt.json", dict(run_id=rid, case_id=case["case_id"],
                    arm=arm, repetition=1, plan_id=plan["plan_id"], completed=True,
                    result=dict(run_id=rid, runtime=plan["runtime"], execution_kind="model",
                        output="synthetic test record", trace=[{"event": "test"}], subagent_count=0,
                        changed_files=[], validation_commands=[], owner_route=[], runtime_evidence="test")))

    def review(self):
        result = evaluation.report(self.directory)
        review = dict(plan_id=result["plan_id"], runs={rid: dict(receipt_sha256=sha,
            scores={m: 2 for m in evaluation.METRICS}, evidence_locators=["test fixture"],
            hard_regressions=[]) for rid, sha in result["receipt_digests"].items()})
        path = self.root / "review.json"
        path.write_text(json.dumps(review), encoding="utf-8")
        return path, review

    def test_five_definitions_are_zero_executions(self):
        self.freeze()
        result = evaluation.report(self.directory)
        self.assertEqual(result["case_definitions"], 5)
        self.assertEqual(result["behavioral_evaluations_executed"], 0)

    def test_fixture_subprocess_excluded_and_retry_does_not_overwrite(self):
        self.freeze()
        evaluation.run(self.directory, "c0", "active", 1)
        self.assertEqual(evaluation.report(self.directory)["fixture_runs_excluded"], 1)
        self.assertEqual(evaluation.report(self.directory)["completed_model_arm_runs"], 0)
        with self.assertRaises(FileExistsError):
            evaluation.run(self.directory, "c0", "active", 1)

    def test_frozen_plan_tampering_rejected(self):
        self.freeze()
        path = self.directory / "plan.json"
        plan = evaluation.read(path)
        plan["runtime"]["model"] = "changed"
        path.write_text(json.dumps(plan))
        with self.assertRaises(ValueError):
            evaluation.report(self.directory)

    def test_heldout_requires_explicit_provenance(self):
        self.manifest["cases"][-1].pop("withheld_from_candidate_design")
        self.save_manifest()
        with self.assertRaises(ValueError):
            self.freeze()
        self.assertFalse(self.directory.exists())

    def test_pairs_and_individual_runs_have_different_counts(self):
        self.freeze()
        self.model_receipts()
        result = evaluation.report(self.directory)
        self.assertEqual(result["behavioral_evaluations_executed"], 5)
        self.assertEqual(result["completed_model_arm_runs"], 10)
        self.assertEqual(result["held_out_paired_cases_declared"], 2)
        self.assertFalse(result["ready_for_promotion_review"])

    def test_hard_regression_rejects_even_with_missing_reviews(self):
        self.freeze()
        self.model_receipts()
        path, review = self.review()
        rid = next(iter(review["runs"]))
        review["runs"] = {rid: review["runs"][rid]}
        review["runs"][rid]["hard_regressions"] = ["read-only violation"]
        path.write_text(json.dumps(review))
        self.assertEqual(evaluation.report(self.directory, path)["decision"], "REJECT_REGRESSION")

    def test_human_review_never_auto_promotes(self):
        self.freeze()
        self.model_receipts()
        path, review = self.review()
        review["human_adjudication"] = dict(target_improved=True, no_protected_regression=True,
                                           reviewer="fixture human", evidence_locator="fixture decision")
        path.write_text(json.dumps(review))
        result = evaluation.report(self.directory, path)
        self.assertTrue(result["ready_for_promotion_review"])
        self.assertEqual(result["decision"], "STAGE_FOR_HUMAN_REVIEW")

    def test_failure_is_visible_and_not_counted(self):
        self.manifest["adapter"] = [sys.executable, "-c", "raise SystemExit(3)"]
        self.save_manifest()
        self.freeze()
        with self.assertRaises(ValueError):
            evaluation.run(self.directory, "c0", "candidate", 1)
        result = evaluation.report(self.directory)
        self.assertEqual(len(result["failed_attempts"]), 1)
        self.assertEqual(result["completed_model_arm_runs"], 0)

    def test_runtime_mismatch_is_rejected(self):
        self.freeze()
        self.model_receipts()
        path = self.directory / "case-001-active-1/receipt.json"
        receipt = evaluation.read(path)
        receipt["result"]["runtime"]["model"] = "different"
        path.write_text(json.dumps(receipt))
        with self.assertRaises(ValueError):
            evaluation.report(self.directory)

    def test_score_regression_prevents_readiness(self):
        self.freeze()
        self.model_receipts()
        path, review = self.review()
        review["human_adjudication"] = dict(target_improved=True, no_protected_regression=True,
                                           reviewer="fixture human", evidence_locator="fixture")
        review["runs"]["case-001-candidate-1"]["scores"]["route_correctness"] = 1
        path.write_text(json.dumps(review))
        self.assertFalse(evaluation.report(self.directory, path)["ready_for_promotion_review"])

    def test_review_binding_rejects_changed_receipt(self):
        self.freeze()
        self.model_receipts()
        path, review = self.review()
        receipt_path = self.directory / "case-001-active-1/receipt.json"
        receipt = evaluation.read(receipt_path)
        receipt["result"]["output"] = "changed"
        receipt_path.write_text(json.dumps(receipt))
        with self.assertRaises(ValueError):
            evaluation.report(self.directory, path)


if __name__ == "__main__":
    unittest.main()
