#!/usr/bin/env python3
"""Validate a machine-readable equation semantic-integrity ledger.

The validator is dependency-free. It does not extract MathType/OLE equations;
it validates a formula-aware ledger produced by the manuscript workflow and
fails closed when parsing or scientific adjudication remains unresolved.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
MODES = {"revision", "submission", "proof"}
PARSE_STATUSES = {"PARSED", "MANUAL_REQUIRED"}
PROOF_CLASSES = {
    "PUBLISHER_ERROR",
    "OBVIOUS_AUTHOR_ERROR",
    "CLARITY_CORRECTION",
    "SCIENTIFIC_DECISION_REQUIRED",
    "MODEL_OR_RESULTS_CHANGE",
}
PROOF_DISPOSITIONS = {"APPLY", "REQUEST_EDITOR_APPROVAL", "HOLD"}


@dataclass
class Finding:
    code: str
    severity: str
    message: str
    equation_id: str | None = None
    correction_id: str | None = None


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any) -> list[str] | None:
    if not isinstance(value, list) or not all(_nonempty(item) for item in value):
        return None
    return [item.strip() for item in value]


def _fingerprint_present(row: dict[str, Any], prefix: str) -> bool:
    text = row.get(f"{prefix}_text")
    digest = row.get(f"{prefix}_sha256")
    return _nonempty(text) or (isinstance(digest, str) and bool(SHA256_RE.fullmatch(digest)))


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def validate_ledger(data: Any, verify_files: bool = False) -> dict[str, Any]:
    findings: list[Finding] = []
    computed_first_use: dict[str, list[str]] = {}

    def add(code: str, message: str, *, equation_id: str | None = None,
            correction_id: str | None = None, severity: str = "BLOCK") -> None:
        findings.append(Finding(code, severity, message, equation_id, correction_id))

    if not isinstance(data, dict):
        return {"verdict": "BLOCK", "findings": [asdict(Finding("LEDGER_NOT_OBJECT", "BLOCK", "Ledger root must be a JSON object."))]}

    if data.get("schema_version") != "1.0":
        add("SCHEMA_VERSION", "schema_version must be '1.0'.")

    mode = data.get("mode")
    if mode not in MODES:
        add("MODE_INVALID", f"mode must be one of {sorted(MODES)}.")

    strict_local = data.get("strict_local_definitions")
    if not isinstance(strict_local, bool):
        add("STRICT_LOCAL_MISSING", "strict_local_definitions must be true or false.")
        strict_local = True

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        add("ARTIFACTS_MISSING", "At least one frozen artifact with role, path, and SHA-256 is required.")
        artifacts = []
    roles: set[str] = set()
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            add("ARTIFACT_INVALID", f"Artifact row {index + 1} must be an object.")
            continue
        role = artifact.get("role")
        path_text = artifact.get("path")
        digest = artifact.get("sha256")
        if not _nonempty(role) or not _nonempty(path_text) or not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            add("ARTIFACT_CONTRACT", f"Artifact row {index + 1} requires non-empty role/path and a 64-character SHA-256.")
            continue
        role = role.strip()
        if role in roles:
            add("ARTIFACT_ROLE_DUPLICATE", f"Artifact role '{role}' is duplicated.")
        roles.add(role)
        if verify_files:
            path = Path(path_text)
            if not path.is_file():
                add("ARTIFACT_MISSING", f"Artifact does not exist: {path}")
            elif _sha256_file(path) != digest.upper():
                add("ARTIFACT_HASH_STALE", f"Artifact hash is stale for role '{role}': {path}")

    if mode == "proof":
        if "accepted_source" not in roles:
            add("PROOF_ACCEPTED_SOURCE_MISSING", "Proof mode requires an accepted_source artifact.")
        if "production_proof" not in roles:
            add("PRODUCTION_PROOF_MISSING", "Proof mode requires a production_proof artifact.")

    symbols = data.get("symbols")
    if not isinstance(symbols, list) or not symbols:
        add("SYMBOL_REGISTRY_MISSING", "A non-empty canonical symbol registry is required.")
        symbols = []

    canonical: dict[str, dict[str, Any]] = {}
    alias_to_symbol: dict[str, str] = {}
    for index, row in enumerate(symbols):
        if not isinstance(row, dict):
            add("SYMBOL_ROW_INVALID", f"Symbol row {index + 1} must be an object.")
            continue
        symbol = row.get("symbol")
        aliases = row.get("aliases", [])
        if not _nonempty(symbol) or not _nonempty(row.get("meaning")) or not _nonempty(row.get("unit")):
            add("SYMBOL_CONTRACT", f"Symbol row {index + 1} requires symbol, meaning, and unit/dimension.")
            continue
        symbol = symbol.strip()
        if symbol in canonical:
            add("SYMBOL_DUPLICATE", f"Canonical symbol '{symbol}' is duplicated.")
            continue
        if aliases is None:
            aliases = []
        parsed_aliases = _string_list(aliases)
        if parsed_aliases is None:
            add("ALIASES_INVALID", f"Aliases for '{symbol}' must be a list of non-empty strings.")
            parsed_aliases = []
        canonical[symbol] = row
        for alias in parsed_aliases:
            if alias == symbol:
                add("ALIAS_EQUALS_CANONICAL", f"Alias '{alias}' duplicates its canonical symbol.")
            elif alias in alias_to_symbol and alias_to_symbol[alias] != symbol:
                add("ALIAS_COLLISION", f"Alias '{alias}' maps to multiple canonical symbols.")
            else:
                alias_to_symbol[alias] = symbol
    for alias, owner in alias_to_symbol.items():
        if alias in canonical and alias != owner:
            add("ALIAS_CANONICAL_COLLISION", f"Alias '{alias}' is also a canonical symbol.")

    expected_count = data.get("expected_display_count")
    if not isinstance(expected_count, int) or isinstance(expected_count, bool) or expected_count < 1:
        add("EXPECTED_COUNT_INVALID", "expected_display_count must be a positive integer.")
        expected_count = 0

    equations = data.get("equations")
    if not isinstance(equations, list):
        add("EQUATIONS_INVALID", "equations must be a list.")
        equations = []
    if expected_count and len(equations) != expected_count:
        add("DISPLAY_COUNT_MISMATCH", f"Expected {expected_count} displayed equations but ledger contains {len(equations)}.")

    ids: set[str] = set()
    indices: set[int] = set()
    ordered: list[tuple[int, dict[str, Any], str]] = []
    for row_number, row in enumerate(equations, start=1):
        if not isinstance(row, dict):
            add("EQUATION_ROW_INVALID", f"Equation row {row_number} must be an object.")
            continue
        eq_id = str(row.get("id", "")).strip()
        display_index = row.get("display_index")
        if not eq_id:
            add("EQUATION_ID_MISSING", f"Equation row {row_number} has no id.")
            eq_id = f"<row-{row_number}>"
        elif eq_id in ids:
            add("EQUATION_ID_DUPLICATE", f"Equation id '{eq_id}' is duplicated.", equation_id=eq_id)
        ids.add(eq_id)
        if not isinstance(display_index, int) or isinstance(display_index, bool) or display_index < 1:
            add("DISPLAY_INDEX_INVALID", "display_index must be a positive integer.", equation_id=eq_id)
        else:
            if display_index in indices:
                add("DISPLAY_INDEX_DUPLICATE", f"display_index {display_index} is duplicated.", equation_id=eq_id)
            indices.add(display_index)
            ordered.append((display_index, row, eq_id))

    if expected_count and indices != set(range(1, expected_count + 1)):
        add("DISPLAY_INDEX_GAP", "Physical display indices must be contiguous from 1 to expected_display_count.")

    seen_symbols: set[str] = set()
    for _, row, eq_id in sorted(ordered, key=lambda item: item[0]):
        formula_symbols = _string_list(row.get("formula_symbols"))
        local_definitions = _string_list(row.get("local_definitions"))
        if not formula_symbols:
            add("FORMULA_SYMBOLS_INVALID", "formula_symbols must be a non-empty string list.", equation_id=eq_id)
            formula_symbols = []
        if local_definitions is None:
            add("LOCAL_DEFINITIONS_INVALID", "local_definitions must be a string list, which may be empty.", equation_id=eq_id)
            local_definitions = []
        if len(formula_symbols) != len(set(formula_symbols)):
            add("FORMULA_SYMBOL_DUPLICATE", "formula_symbols contains duplicates.", equation_id=eq_id)
        if len(local_definitions) != len(set(local_definitions)):
            add("LOCAL_DEFINITION_DUPLICATE", "local_definitions contains duplicates.", equation_id=eq_id)

        for token in formula_symbols:
            if token in alias_to_symbol:
                add("ALIAS_IN_FORMULA", f"Deprecated alias '{token}' used; canonical symbol is '{alias_to_symbol[token]}'.", equation_id=eq_id)
            elif token not in canonical:
                add("UNKNOWN_FORMULA_SYMBOL", f"Formula symbol '{token}' is absent from the registry.", equation_id=eq_id)
        for token in local_definitions:
            if token in alias_to_symbol:
                add("ALIAS_IN_DEFINITION", f"Deprecated alias '{token}' used; canonical symbol is '{alias_to_symbol[token]}'.", equation_id=eq_id)
            elif token not in canonical:
                add("UNKNOWN_DEFINITION_SYMBOL", f"Defined symbol '{token}' is absent from the registry.", equation_id=eq_id)

        first_use = [token for token in formula_symbols if token not in seen_symbols]
        computed_first_use[eq_id] = first_use
        exemptions = row.get("definition_exemptions", [])
        if not isinstance(exemptions, list):
            add("EXEMPTIONS_INVALID", "definition_exemptions must be a list.", equation_id=eq_id)
            exemptions = []
        exempt_symbols: set[str] = set()
        for exemption in exemptions:
            if not isinstance(exemption, dict) or not _nonempty(exemption.get("symbol")) or not _nonempty(exemption.get("reason")) or not _nonempty(exemption.get("locator")):
                add("EXEMPTION_CONTRACT", "Each definition exemption requires symbol, reason, and locator.", equation_id=eq_id)
                continue
            symbol = exemption["symbol"].strip()
            exempt_symbols.add(symbol)
            if symbol not in first_use:
                add("EXEMPTION_NOT_FIRST_USE", f"Exemption for '{symbol}' is not a first-use symbol.", equation_id=eq_id)
        if strict_local and exemptions:
            add("STRICT_LOCAL_EXEMPTION", "definition_exemptions are forbidden when strict_local_definitions is true.", equation_id=eq_id)

        missing = [token for token in first_use if token not in local_definitions and token not in exempt_symbols]
        extra = [token for token in local_definitions if token not in formula_symbols]
        if missing:
            add("FIRST_USE_DEFINITION_MISSING", f"First-use symbols are not locally defined: {', '.join(missing)}.", equation_id=eq_id)
        if extra:
            add("EQUATION_EXTERNAL_DEFINITION", f"Local explanation defines symbols absent from the equation: {', '.join(extra)}.", equation_id=eq_id)

        if row.get("parse_status") not in PARSE_STATUSES:
            add("PARSE_STATUS_INVALID", f"parse_status must be one of {sorted(PARSE_STATUSES)}.", equation_id=eq_id)
        elif row.get("parse_status") == "MANUAL_REQUIRED":
            add("FORMULA_MANUAL_REVIEW", "Formula extraction/interpretation requires manual review.", equation_id=eq_id, severity="MANUAL_REQUIRED")
        for locator in ("formula_locator", "definition_locator"):
            if not _nonempty(row.get(locator)):
                add("LOCATOR_MISSING", f"{locator} is required.", equation_id=eq_id)
        if not _fingerprint_present(row, "formula"):
            add("FORMULA_FINGERPRINT_MISSING", "Provide formula_text or a valid formula_sha256.", equation_id=eq_id)
        if not _fingerprint_present(row, "definition"):
            add("DEFINITION_FINGERPRINT_MISSING", "Provide definition_text or a valid definition_sha256.", equation_id=eq_id)
        if not isinstance(row.get("model_bound"), bool):
            add("MODEL_BOUND_INVALID", "model_bound must be true or false.", equation_id=eq_id)
        elif row.get("model_bound") and not _nonempty(row.get("model_locator")):
            add("MODEL_LOCATOR_MISSING", "A model-bound equation requires model_locator.", equation_id=eq_id)
        seen_symbols.update(formula_symbols)

    cross_references = data.get("cross_references", [])
    if not isinstance(cross_references, list):
        add("CROSS_REFERENCES_INVALID", "cross_references must be a list.")
        cross_references = []
    for index, reference in enumerate(cross_references, start=1):
        if not isinstance(reference, dict) or not _nonempty(reference.get("target")) or not _nonempty(reference.get("source_locator")):
            add("CROSS_REFERENCE_CONTRACT", f"Cross-reference row {index} requires target and source_locator.")
            continue
        target = reference["target"].strip()
        if target not in ids:
            add("CROSS_REFERENCE_TARGET_MISSING", f"Cross-reference target '{target}' does not exist.")

    proof_corrections = data.get("proof_corrections", [])
    if not isinstance(proof_corrections, list):
        add("PROOF_CORRECTIONS_INVALID", "proof_corrections must be a list.")
        proof_corrections = []
    correction_ids: set[str] = set()
    for index, correction in enumerate(proof_corrections, start=1):
        if not isinstance(correction, dict):
            add("PROOF_CORRECTION_INVALID", f"Proof correction row {index} must be an object.")
            continue
        correction_id = str(correction.get("id", "")).strip()
        classification = correction.get("classification")
        disposition = correction.get("disposition")
        if not correction_id:
            add("PROOF_CORRECTION_ID_MISSING", f"Proof correction row {index} has no id.")
            correction_id = f"<correction-{index}>"
        elif correction_id in correction_ids:
            add("PROOF_CORRECTION_ID_DUPLICATE", f"Proof correction id '{correction_id}' is duplicated.", correction_id=correction_id)
        correction_ids.add(correction_id)
        if classification not in PROOF_CLASSES:
            add("PROOF_CLASS_INVALID", f"classification must be one of {sorted(PROOF_CLASSES)}.", correction_id=correction_id)
        if disposition not in PROOF_DISPOSITIONS:
            add("PROOF_DISPOSITION_INVALID", f"disposition must be one of {sorted(PROOF_DISPOSITIONS)}.", correction_id=correction_id)
        if not _nonempty(correction.get("proof_locator")) or not _nonempty(correction.get("proposed_action")):
            add("PROOF_CORRECTION_CONTRACT", "proof_locator and proposed_action are required.", correction_id=correction_id)
        changes_results = correction.get("changes_model_or_results")
        if not isinstance(changes_results, bool):
            add("PROOF_CHANGE_FLAG_MISSING", "changes_model_or_results must be true or false.", correction_id=correction_id)
        if classification in {"OBVIOUS_AUTHOR_ERROR", "CLARITY_CORRECTION"}:
            if changes_results is not False:
                add("OBVIOUS_CHANGE_NOT_LOCAL", "An obvious/clarity correction cannot change model behavior or reported results.", correction_id=correction_id)
            if not _nonempty(correction.get("authoritative_basis")):
                add("AUTHORITATIVE_BASIS_MISSING", "An obvious/clarity correction requires one authoritative basis.", correction_id=correction_id)
        if classification == "PUBLISHER_ERROR" and not _nonempty(correction.get("accepted_source_locator")):
            add("ACCEPTED_SOURCE_LOCATOR_MISSING", "A publisher error requires an accepted-source locator.", correction_id=correction_id)
        if classification in {"SCIENTIFIC_DECISION_REQUIRED", "MODEL_OR_RESULTS_CHANGE"} and disposition == "APPLY":
            add("SCIENTIFIC_CHANGE_SILENT_APPLY", "Scientific decisions or model/results changes cannot be silently applied in proof mode.", correction_id=correction_id)
        if disposition in {"REQUEST_EDITOR_APPROVAL", "HOLD"}:
            add("PROOF_CORRECTION_UNRESOLVED", f"Correction disposition is {disposition}.", correction_id=correction_id, severity="MANUAL_REQUIRED")

    verdict = "PASS" if not findings else "BLOCK"
    severity_counts: dict[str, int] = {}
    for finding in findings:
        severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1
    return {
        "verdict": verdict,
        "mode": mode,
        "counts": {
            "artifacts": len(artifacts),
            "symbols": len(symbols),
            "equations": len(equations),
            "cross_references": len(cross_references),
            "proof_corrections": len(proof_corrections),
            "findings_by_severity": severity_counts,
        },
        "computed_first_use": computed_first_use,
        "findings": [asdict(item) for item in findings],
    }


def _valid_fixture() -> dict[str, Any]:
    digest = "0" * 64
    return {
        "schema_version": "1.0",
        "mode": "revision",
        "strict_local_definitions": True,
        "expected_display_count": 1,
        "artifacts": [{"role": "manuscript", "path": "manuscript.docx", "sha256": digest}],
        "symbols": [
            {"symbol": "S_ele", "meaning": "electricity supply", "unit": "MWh/month", "aliases": []},
            {"symbol": "Q_T", "meaning": "thermal generation", "unit": "MWh/month", "aliases": ["G_thermal"]},
        ],
        "equations": [{
            "id": "16",
            "display_index": 1,
            "formula_symbols": ["S_ele", "Q_T"],
            "local_definitions": ["S_ele", "Q_T"],
            "definition_exemptions": [],
            "formula_locator": "p. 6 Eq. 16",
            "definition_locator": "p. 6 paragraph after Eq. 16",
            "formula_text": "S_ele = Q_T",
            "definition_text": "where S_ele ... and Q_T ...",
            "model_bound": True,
            "model_locator": "model.mdl:901",
            "parse_status": "PARSED",
        }],
        "cross_references": [{"target": "16", "source_locator": "Section 3.4.2"}],
        "proof_corrections": [],
    }


def self_test() -> int:
    valid = _valid_fixture()
    if validate_ledger(valid)["verdict"] != "PASS":
        print("SELF_TEST=FAIL valid fixture", file=sys.stderr)
        return 1

    mismatch = json.loads(json.dumps(valid))
    mismatch["symbols"].append({"symbol": "D_ele", "meaning": "demand", "unit": "MWh/month", "aliases": []})
    mismatch["equations"][0]["local_definitions"] = ["S_ele", "G_thermal", "D_ele"]
    codes = {item["code"] for item in validate_ledger(mismatch)["findings"]}
    required = {"FIRST_USE_DEFINITION_MISSING", "EQUATION_EXTERNAL_DEFINITION", "ALIAS_IN_DEFINITION"}
    if not required.issubset(codes):
        print(f"SELF_TEST=FAIL mismatch codes={sorted(codes)}", file=sys.stderr)
        return 1

    numbering = json.loads(json.dumps(valid))
    numbering["expected_display_count"] = 2
    codes = {item["code"] for item in validate_ledger(numbering)["findings"]}
    if not {"DISPLAY_COUNT_MISMATCH", "DISPLAY_INDEX_GAP"}.issubset(codes):
        print(f"SELF_TEST=FAIL numbering codes={sorted(codes)}", file=sys.stderr)
        return 1

    proof = json.loads(json.dumps(valid))
    proof["mode"] = "proof"
    proof["artifacts"] = [
        {"role": "accepted_source", "path": "accepted.docx", "sha256": "0" * 64},
        {"role": "production_proof", "path": "proof.pdf", "sha256": "1" * 64},
    ]
    proof["proof_corrections"] = [{
        "id": "P1",
        "classification": "SCIENTIFIC_DECISION_REQUIRED",
        "disposition": "APPLY",
        "proof_locator": "Eq. 51",
        "proposed_action": "Choose a different scientific constraint.",
        "changes_model_or_results": True,
    }]
    codes = {item["code"] for item in validate_ledger(proof)["findings"]}
    if "SCIENTIFIC_CHANGE_SILENT_APPLY" not in codes:
        print(f"SELF_TEST=FAIL proof codes={sorted(codes)}", file=sys.stderr)
        return 1

    publisher = json.loads(json.dumps(proof))
    publisher["proof_corrections"] = [{
        "id": "P2",
        "classification": "PUBLISHER_ERROR",
        "disposition": "APPLY",
        "proof_locator": "Eq. 48",
        "accepted_source_locator": "accepted.docx Eq. 48",
        "proposed_action": "Restore the multiplication sign changed during typesetting.",
        "changes_model_or_results": False,
    }]
    if validate_ledger(publisher)["verdict"] != "PASS":
        print("SELF_TEST=FAIL publisher-error fixture", file=sys.stderr)
        return 1

    print("SELF_TEST=PASS")
    return 0


def write_template(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_valid_fixture(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Equation Semantic Integrity Report",
        "",
        f"- Verdict: `{report.get('verdict')}`",
        f"- Mode: `{report.get('mode')}`",
        f"- Equations: `{report.get('counts', {}).get('equations', 0)}`",
        "",
        "| Severity | Code | Equation | Correction | Message |",
        "|---|---|---|---|---|",
    ]
    for item in report.get("findings", []):
        message = str(item.get("message", "")).replace("|", "\\|")
        lines.append(
            f"| {item.get('severity', '')} | {item.get('code', '')} | "
            f"{item.get('equation_id') or ''} | {item.get('correction_id') or ''} | {message} |"
        )
    if not report.get("findings"):
        lines.append("| PASS | NONE |  |  | No blocking findings. |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an equation semantic-integrity ledger without editing manuscript files.")
    parser.add_argument("ledger", nargs="?", help="Path to ledger JSON")
    parser.add_argument("--verify-files", action="store_true", help="Verify frozen artifact paths and SHA-256 values")
    parser.add_argument("--output", help="Write JSON validation report")
    parser.add_argument("--report-md", help="Write Markdown validation report")
    parser.add_argument("--write-template", help="Write a valid starter ledger and exit")
    parser.add_argument("--self-test", action="store_true", help="Run deterministic built-in regression tests")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if args.write_template:
        write_template(Path(args.write_template))
        print(f"TEMPLATE_WRITTEN={args.write_template}")
        return 0
    if not args.ledger:
        parser.error("ledger is required unless --self-test or --write-template is used")

    try:
        data = json.loads(Path(args.ledger).read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"LEDGER_READ_ERROR={exc}", file=sys.stderr)
        return 2

    report = validate_ledger(data, verify_files=args.verify_files)
    encoded = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(encoded, encoding="utf-8")
    if args.report_md:
        Path(args.report_md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report_md).write_text(markdown_report(report), encoding="utf-8")
    print(encoded, end="")
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
