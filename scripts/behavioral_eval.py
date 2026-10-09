"""Freeze and replay paired evaluations through an explicitly supplied local adapter.

No default model, provider, hook, judge or live-skill installation is configured.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

METRICS = (
    "route_correctness", "evidence_locator_retention", "authority_state_accuracy",
    "author_boundary_protection", "conflict_exposure", "unnecessary_rerun_avoidance",
    "claim_calibration", "handoff_actionability",
)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_result(result, run_id, runtime):
    require(result["run_id"] == run_id, "Adapter returned another run ID.")
    require(result["runtime"] == runtime, "Observed runtime differs from frozen runtime.")
    require(result["execution_kind"] in {"model", "fixture"}, "Invalid execution kind.")
    require(isinstance(result["output"], str) and result["output"].strip(), "Missing output.")
    require(isinstance(result["trace"], list) and result["trace"], "Missing execution trace.")
    require(type(result["subagent_count"]) is int and result["subagent_count"] >= 0, "Invalid subagent count.")
    for field in ("changed_files", "validation_commands", "owner_route"):
        require(isinstance(result[field], list), "Missing observation: " + field)
    require(result["runtime_evidence"], "Missing runtime evidence locator.")


def freeze(manifest, target):
    """Snapshot inputs and rubric before any outputs; never invent held-out provenance."""
    manifest, target = Path(manifest).resolve(), Path(target).resolve()
    plan = read(manifest)
    require(not target.exists(), "Choose a fresh evaluation directory.")
    require(not any(p in {".codex", ".claude", ".agents", "skills"} for p in target.parts),
            "Keep private evaluation evidence outside skill/config discovery directories.")
    require(plan["evaluation_scope"] in {"router_text", "agent_workflow"}, "Invalid evaluation scope.")
    runtime = plan["runtime"]
    for field in ("model", "reasoning_effort", "permissions", "tools", "budget", "isolation"):
        require(field in runtime, "Missing runtime field: " + field)
    require(isinstance(runtime["tools"], list), "tools must be a list.")
    require(type(plan["repetitions"]) is int and plan["repetitions"] > 0, "Invalid repetitions.")
    require(type(plan["timeout_seconds"]) is int and plan["timeout_seconds"] > 0, "Invalid timeout.")
    require(isinstance(plan["adapter"], list) and plan["adapter"]
            and all(isinstance(x, str) and x for x in plan["adapter"]), "adapter must be an argv list.")
    require(set(plan["rubric"]) == set(METRICS), "Supply all eight rubric definitions.")
    require(all(isinstance(v, str) and v.strip() for v in plan["rubric"].values()), "Empty rubric.")
    require(plan["protected_rules"] and plan["target_improvement"], "Declare hard gates and target improvement.")
    for arm in ("active", "candidate"):
        source = (manifest.parent / plan[arm]).resolve()
        plan[arm] = {"source": str(source), "text": source.read_text(encoding="utf-8-sig")}
        plan[arm]["sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    require(plan["active"]["sha256"] != plan["candidate"]["sha256"], "Arms are identical.")
    cases = plan["cases"]
    require(isinstance(cases, list) and cases, "No cases supplied.")
    ids = [c["case_id"] for c in cases]
    require(all(isinstance(i, str) and i for i in ids) and len(set(ids)) == len(ids), "Invalid/duplicate case IDs.")
    for case in cases:
        require(case["split"] in {"probe", "selection", "test"}, "Invalid case split.")
        require(type(case["held_out"]) is bool and case["provenance"], "Missing case provenance.")
        require(not case["held_out"] or (case["split"] != "probe" and case.get("withheld_from_candidate_design")),
                "Held-out cases need a provenance explanation; this is not independently certified.")
        case["input"] = (manifest.parent / case.pop("input_path")).read_text(encoding="utf-8-sig")
        require(case["input"].strip(), "Empty case input.")
    plan["frozen_at"] = datetime.now(timezone.utc).isoformat()
    plan["plan_id"] = digest(plan)
    target.mkdir(parents=True)
    write_new(target / "plan.json", plan)
    return {"plan_id": plan["plan_id"], "cases": len(cases), "behavioral_evaluations_executed": 0}


def load_plan(directory):
    plan = read(Path(directory) / "plan.json")
    identity = plan.pop("plan_id")
    require(digest(plan) == identity, "Frozen plan changed; create a new evaluation directory.")
    plan["plan_id"] = identity
    return plan


def run(directory, case_id, arm, repetition):
    """One explicit invocation; adapter must enforce the declared isolation/permissions."""
    directory = Path(directory).resolve()
    plan = load_plan(directory)
    require(arm in {"active", "candidate"}, "Invalid arm.")
    require(1 <= repetition <= plan["repetitions"], "Invalid repetition.")
    matches = [(i, c) for i, c in enumerate(plan["cases"]) if c["case_id"] == case_id]
    require(len(matches) == 1, "Unknown case ID.")
    index, case = matches[0]
    run_id = f"case-{index + 1:03d}-{arm}-{repetition}"
    work = directory / run_id
    work.mkdir()  # existing attempts, including failures, are never overwritten
    request = {"run_id": run_id, "plan_id": plan["plan_id"], "runtime": plan["runtime"],
               "evaluation_scope": plan["evaluation_scope"], "instruction": plan[arm]["text"],
               "input": case["input"]}
    # Rubric, expected answers, opposite-arm outputs and split labels stay out of the request.
    started = datetime.now(timezone.utc).isoformat()
    receipt = {"run_id": run_id, "case_id": case_id, "arm": arm, "repetition": repetition,
               "plan_id": plan["plan_id"], "started_at": started, "completed": False}
    try:
        process = subprocess.run(plan["adapter"], input=json.dumps(request), text=True,
                                 encoding="utf-8", capture_output=True, cwd=work,
                                 timeout=plan["timeout_seconds"], shell=False)
        require(process.returncode == 0, f"Adapter exited {process.returncode}; output withheld to avoid credential leakage.")
        result = json.loads(process.stdout)
        validate_result(result, run_id, plan["runtime"])
        receipt.update(completed=True, result=result)
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        receipt["error_type"] = type(error).__name__
        write_new(work / "receipt.json", receipt)
        raise ValueError(f"Evaluation attempt failed ({type(error).__name__}); inspect adapter locally. No behavioral success recorded.") from None
    receipt["finished_at"] = datetime.now(timezone.utc).isoformat()
    write_new(work / "receipt.json", receipt)
    return {"run_id": run_id, "completed": True, "execution_kind": result["execution_kind"]}


def report(directory, review_path=None):
    """Recount real receipts; human judgments are supplied evidence, never self-generated."""
    directory = Path(directory).resolve()
    plan = load_plan(directory)
    expected = {f"case-{i + 1:03d}-{arm}-{r}": (c, arm, r)
                for i, c in enumerate(plan["cases"]) for arm in ("active", "candidate")
                for r in range(1, plan["repetitions"] + 1)}
    completed = {}
    failed = []
    fixtures = 0
    for path in sorted(directory.glob("case-*/receipt.json")):
        receipt = read(path)
        rid = receipt["run_id"]
        require(rid in expected and path.parent.name == rid, "Unexpected receipt identity.")
        case, arm, repetition = expected[rid]
        require(receipt["plan_id"] == plan["plan_id"] and receipt["case_id"] == case["case_id"]
                and receipt["arm"] == arm and receipt["repetition"] == repetition, "Receipt binding mismatch.")
        require(type(receipt["completed"]) is bool, "Invalid completion marker.")
        if not receipt["completed"]:
            failed.append(rid)
            continue
        result = receipt["result"]
        validate_result(result, rid, plan["runtime"])
        if result["execution_kind"] == "model":
            completed[rid] = receipt
        else:
            fixtures += 1
    paired = [c for i, c in enumerate(plan["cases"]) if all(
        f"case-{i + 1:03d}-{a}-{r}" in completed
        for a in ("active", "candidate") for r in range(1, plan["repetitions"] + 1))]
    decision = "STAGE_FOR_HUMAN_REVIEW"
    reviewed = 0
    hard = []
    score_regressions = []
    eligible = False
    if review_path:
        review = read(review_path)
        require(review["plan_id"] == plan["plan_id"], "Review belongs to another plan.")
        for rid, judgment in review["runs"].items():
            require(rid in completed, "Cannot grade a missing/failed/fixture run.")
            require(judgment["receipt_sha256"] == digest(completed[rid]), "Reviewed receipt changed.")
            require(set(judgment["scores"]) == set(METRICS), "Incomplete rubric scores.")
            require(all(type(v) is int and 0 <= v <= 2 for v in judgment["scores"].values()), "Invalid score.")
            require(judgment["evidence_locators"] and isinstance(judgment["hard_regressions"], list), "Missing judgment evidence.")
            hard.extend(judgment["hard_regressions"])
            if completed[rid]["arm"] == "candidate":
                for metric in ("authority_state_accuracy", "author_boundary_protection"):
                    if judgment["scores"][metric] == 0:
                        hard.append(rid + ": " + metric + " scored 0")
            reviewed += 1
        for rid, judgment in review["runs"].items():
            if completed[rid]["arm"] != "candidate":
                continue
            active_id = rid.replace("-candidate-", "-active-")
            if active_id in review["runs"]:
                for metric, value in judgment["scores"].items():
                    if value < review["runs"][active_id]["scores"][metric]:
                        score_regressions.append(rid + ": " + metric)
        if hard:
            decision = "REJECT_REGRESSION"
        elif len(completed) == len(expected) and reviewed == len(expected):
            human = review.get("human_adjudication", {})
            eligible = (not score_regressions and human.get("target_improved") is True and human.get("no_protected_regression") is True
                        and bool(human.get("reviewer")) and bool(human.get("evidence_locator")))
    return {"decision": decision, "ready_for_promotion_review": eligible,
            "plan_id": plan["plan_id"], "evaluation_scope": plan["evaluation_scope"],
            "case_definitions": len(plan["cases"]), "behavioral_evaluations_executed": len(paired),
            "completed_model_arm_runs": len(completed), "fixture_runs_excluded": fixtures,
            "held_out_paired_cases_declared": sum(c["held_out"] for c in paired),
            "failed_attempts": failed, "reviewed_arm_runs": reviewed, "hard_regressions": hard,
            "score_regressions": score_regressions,
            "receipt_digests": {rid: digest(r) for rid, r in completed.items()},
            "limits": "Adapter observations and human provenance require audit. Counts do not prove improvement; no automatic PROMOTE or installation."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    freezing = commands.add_parser("freeze")
    freezing.add_argument("manifest", type=Path)
    freezing.add_argument("target", type=Path)
    running = commands.add_parser("run", help="Explicitly execute one configured adapter invocation")
    running.add_argument("directory", type=Path)
    running.add_argument("--case", required=True)
    running.add_argument("--arm", choices=("active", "candidate"), required=True)
    running.add_argument("--repetition", type=int, default=1)
    reporting = commands.add_parser("report")
    reporting.add_argument("directory", type=Path)
    reporting.add_argument("--review", type=Path)
    reporting.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "freeze":
            result = freeze(args.manifest, args.target)
        elif args.command == "run":
            result = run(args.directory, args.case, args.arm, args.repetition)
        else:
            result = report(args.directory, args.review)
            if args.output:
                require(args.output.suffix.lower() == ".json", "Report output must end in .json.")
                require(not args.output.exists() and not args.output.with_suffix(".md").exists(),
                        "Choose fresh JSON and Markdown report paths.")
                write_new(args.output, result)
                md = args.output.with_suffix(".md")
                with md.open("x", encoding="utf-8") as stream:
                    stream.write("# Behavioral evaluation report\n\n```json\n" + json.dumps(result, ensure_ascii=False, indent=2) + "\n```\n")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"Evaluation failed: {type(error).__name__}. Check local inputs and documented schema.\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result.get("decision") == "REJECT_REGRESSION" else 0


if __name__ == "__main__":
    sys.exit(main())
