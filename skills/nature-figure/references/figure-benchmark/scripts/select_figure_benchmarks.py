#!/usr/bin/env python3
"""Deterministically select candidate figures from a manifest.

The selector is intentionally conservative:
- it never edits the manifest or corpus;
- it returns candidates, not approved benchmarks;
- source, rights, visual quality, and transferability still require inspection.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


SCHEMA_VERSION = "figure-corpus-selection.v1.1"
STATUS = "CANDIDATES_ONLY_NOT_APPROVED"
REQUIRED_COLUMNS = {"reference_id", "local_path"}
SEARCH_FIELDS = (
    "paper_title",
    "caption_text",
    "figure_role",
    "archetype",
    "data_analysis_type",
    "data_type",
    "figure_type",
    "venue",
    "notes",
)
CSV_OUTPUT_FIELDS = (
    "rank",
    "selector_score",
    "match_strength",
    "matched_terms",
    "warnings",
    "reference_id",
    "local_path",
    "source_pdf_path",
    "source_url",
    "paper_title",
    "doi",
    "venue",
    "year",
    "figure_id",
    "caption_text",
    "figure_role",
    "archetype",
    "data_type",
    "data_analysis_type",
    "figure_type",
    "extraction_quality",
    "license_status",
    "metadata_status",
    "classification_status",
    "ncs_template_status",
)


@dataclass(frozen=True)
class Query:
    figure_types: tuple[str, ...] = ()
    data_types: tuple[str, ...] = ()
    data_analysis_types: tuple[str, ...] = ()
    figure_roles: tuple[str, ...] = ()
    archetypes: tuple[str, ...] = ()
    venue_family: str = ""
    venues: tuple[str, ...] = ()
    terms: tuple[str, ...] = ()
    limit: int = 12
    include_missing: bool = False
    require_reviewed: bool = False


def normalize(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).casefold()


def split_values(values: Iterable[str] | None) -> tuple[str, ...]:
    items: list[str] = []
    for value in values or ():
        for item in str(value).split(","):
            cleaned = normalize(item)
            if cleaned and cleaned not in items:
                items.append(cleaned)
    return tuple(items)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve_local_path(value: str, manifest_path: Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = manifest_path.parent / path
    return path


def venue_family_matches(venue: str, family: str) -> bool:
    venue_norm = normalize(venue)
    family_norm = normalize(family)
    if not family_norm:
        return True

    nature = venue_norm.startswith("nature")
    science = venue_norm in {
        "science",
        "science advances",
        "science immunology",
        "science robotics",
        "science signaling",
        "science translational medicine",
    }
    cell = (
        venue_norm == "cell"
        or venue_norm.startswith("cell reports")
        or venue_norm
        in {
            "cell metabolism",
            "cell systems",
            "current biology",
            "developmental cell",
            "immunity",
            "joule",
            "matter",
            "one earth",
            "patterns",
        }
    )
    pnas = venue_norm == "pnas" or venue_norm.startswith(
        "proceedings of the national academy of sciences"
    )

    if family_norm == "nature":
        return nature
    if family_norm == "science":
        return science
    if family_norm == "cell":
        return cell
    if family_norm == "pnas":
        return pnas
    if family_norm == "ncs":
        return nature or science or cell or pnas
    raise ValueError(
        f"Unsupported venue family {family!r}; use nature, science, cell, pnas, or ncs."
    )


def is_metadata_verified(value: str) -> bool:
    norm = normalize(value)
    return (
        "verified" in norm
        and "unverified" not in norm
        and "provisional" not in norm
    )


def is_classification_reviewed(value: str) -> bool:
    norm = normalize(value)
    return bool(norm) and not any(
        marker in norm for marker in ("needs_review", "unreviewed", "unresolved", "provisional")
    )


def is_extraction_reviewed(value: str) -> bool:
    norm = normalize(value)
    return bool(norm) and not any(
        marker in norm for marker in ("unreviewed", "low_quality", "failed", "unresolved")
    )


def contains_any(value: str, requested: Sequence[str]) -> bool:
    norm = normalize(value)
    return not requested or any(item in norm for item in requested)


def build_warnings(row: dict[str, str], local_path_exists: bool) -> list[str]:
    warnings: list[str] = []
    if not local_path_exists:
        warnings.append("LOCAL_PATH_MISSING")
    if not is_metadata_verified(row.get("metadata_status", "")):
        warnings.append("METADATA_NOT_VERIFIED")
    if not is_classification_reviewed(row.get("classification_status", "")):
        warnings.append("CLASSIFICATION_REVIEW_REQUIRED")
    if not is_extraction_reviewed(row.get("extraction_quality", "")):
        warnings.append("EXTRACTION_REVIEW_REQUIRED")
    license_status = normalize(row.get("license_status", ""))
    if not license_status or any(
        marker in license_status for marker in ("provisional", "local_use", "unknown", "restricted")
    ):
        warnings.append("RIGHTS_REVIEW_REQUIRED")
    if not normalize(row.get("source_url", "")) and not normalize(
        row.get("source_pdf_path", "")
    ):
        warnings.append("SOURCE_LOCATOR_MISSING")
    return warnings


def score_row(
    row: dict[str, str],
    query: Query,
    local_path_exists: bool,
) -> tuple[int, list[str], str]:
    score = 0
    if local_path_exists:
        score += 20
    if query.figure_types:
        score += 30
    if query.data_types:
        score += 20
    if query.data_analysis_types:
        score += 20
    if query.venue_family or query.venues:
        score += 20

    role_match = contains_any(row.get("figure_role", ""), query.figure_roles)
    archetype_match = contains_any(row.get("archetype", ""), query.archetypes)
    if query.figure_roles:
        score += 15 if role_match else -10
    if query.archetypes:
        score += 15 if archetype_match else -10

    search_blob = " ".join(normalize(row.get(field, "")) for field in SEARCH_FIELDS)
    matched_terms = [term for term in query.terms if term in search_blob]
    score += 8 * len(matched_terms)

    if is_metadata_verified(row.get("metadata_status", "")):
        score += 6
    if is_classification_reviewed(row.get("classification_status", "")):
        score += 6
    if is_extraction_reviewed(row.get("extraction_quality", "")):
        score += 4
    if "protected" in normalize(row.get("ncs_template_status", "")):
        score += 3

    requested_signals = (
        len(query.figure_roles) + len(query.archetypes) + len(query.terms)
    )
    matched_signals = (
        (len(query.figure_roles) if query.figure_roles and role_match else 0)
        + (len(query.archetypes) if query.archetypes and archetype_match else 0)
        + len(matched_terms)
    )
    if requested_signals == 0:
        strength = "FILTER_ONLY"
    else:
        ratio = matched_signals / requested_signals
        strength = "STRONG" if ratio >= 0.75 else "MODERATE" if ratio > 0 else "WEAK"
    return score, matched_terms, strength


def select_candidates(manifest_path: Path, query: Query) -> dict[str, Any]:
    manifest_path = manifest_path.resolve()
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    if query.limit < 1:
        raise ValueError("--limit must be at least 1")

    counters = {
        "manifest_rows": 0,
        "eligible_rows": 0,
        "excluded_missing_path": 0,
        "excluded_figure_type": 0,
        "excluded_data_type": 0,
        "excluded_data_analysis_type": 0,
        "excluded_venue": 0,
        "excluded_review_status": 0,
        "classification_review_required": 0,
        "metadata_not_verified": 0,
        "extraction_review_required": 0,
    }
    ranked: list[dict[str, Any]] = []

    with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or ())
        missing_columns = sorted(REQUIRED_COLUMNS - fieldnames)
        if missing_columns:
            raise ValueError(
                "Manifest is missing required columns: " + ", ".join(missing_columns)
            )
        strict_filter_columns = {
            "figure_type": query.figure_types,
            "data_type": query.data_types,
            "data_analysis_type": query.data_analysis_types,
        }
        unavailable_filter_columns = sorted(
            column
            for column, requested in strict_filter_columns.items()
            if requested and column not in fieldnames
        )
        if unavailable_filter_columns:
            raise ValueError(
                "Manifest is missing columns required by strict filters: "
                + ", ".join(unavailable_filter_columns)
            )

        for raw_row in reader:
            row = {key: (value or "") for key, value in raw_row.items()}
            counters["manifest_rows"] += 1
            local_path = resolve_local_path(row.get("local_path", ""), manifest_path)
            local_path_exists = bool(row.get("local_path")) and local_path.is_file()

            if not local_path_exists and not query.include_missing:
                counters["excluded_missing_path"] += 1
                continue
            if query.figure_types and normalize(row.get("figure_type", "")) not in set(
                query.figure_types
            ):
                counters["excluded_figure_type"] += 1
                continue
            if query.data_types and normalize(row.get("data_type", "")) not in set(
                query.data_types
            ):
                counters["excluded_data_type"] += 1
                continue
            if query.data_analysis_types and normalize(
                row.get("data_analysis_type", "")
            ) not in set(query.data_analysis_types):
                counters["excluded_data_analysis_type"] += 1
                continue
            if query.venue_family and not venue_family_matches(
                row.get("venue", ""), query.venue_family
            ):
                counters["excluded_venue"] += 1
                continue
            if query.venues and not contains_any(row.get("venue", ""), query.venues):
                counters["excluded_venue"] += 1
                continue
            if query.require_reviewed and not (
                is_metadata_verified(row.get("metadata_status", ""))
                and is_classification_reviewed(row.get("classification_status", ""))
                and is_extraction_reviewed(row.get("extraction_quality", ""))
            ):
                counters["excluded_review_status"] += 1
                continue

            counters["eligible_rows"] += 1
            if not is_classification_reviewed(row.get("classification_status", "")):
                counters["classification_review_required"] += 1
            if not is_metadata_verified(row.get("metadata_status", "")):
                counters["metadata_not_verified"] += 1
            if not is_extraction_reviewed(row.get("extraction_quality", "")):
                counters["extraction_review_required"] += 1

            score, matched_terms, strength = score_row(row, query, local_path_exists)
            candidate = {key: row.get(key, "") for key in CSV_OUTPUT_FIELDS if key in row}
            candidate.update(
                {
                    "selector_score": score,
                    "match_strength": strength,
                    "matched_terms": matched_terms,
                    "warnings": build_warnings(row, local_path_exists),
                    "local_path": str(local_path),
                }
            )
            ranked.append(candidate)

    ranked.sort(
        key=lambda item: (
            -int(item["selector_score"]),
            normalize(item.get("reference_id", "")),
        )
    )
    selected = ranked[: query.limit]
    for index, candidate in enumerate(selected, start=1):
        candidate["rank"] = index

    return {
        "schema_version": SCHEMA_VERSION,
        "status": STATUS,
        "manifest": str(manifest_path),
        "manifest_sha256": sha256_file(manifest_path),
        "query": {
            "figure_types": list(query.figure_types),
            "data_types": list(query.data_types),
            "data_analysis_types": list(query.data_analysis_types),
            "figure_roles": list(query.figure_roles),
            "archetypes": list(query.archetypes),
            "venue_family": query.venue_family,
            "venues": list(query.venues),
            "terms": list(query.terms),
            "limit": query.limit,
            "include_missing": query.include_missing,
            "require_reviewed": query.require_reviewed,
        },
        "corpus_health": counters,
        "candidate_count": len(selected),
        "candidates": selected,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def write_csv(path: Path, candidates: Sequence[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_OUTPUT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for candidate in candidates:
            row = dict(candidate)
            row["matched_terms"] = "|".join(candidate.get("matched_terms", []))
            row["warnings"] = "|".join(candidate.get("warnings", []))
            writer.writerow(row)


def run_self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="figure-selector-") as temp_dir:
        root = Path(temp_dir)
        images = root / "images"
        images.mkdir()
        for name in ("r1.jpg", "r2.jpg", "r3.jpg", "r5.jpg", "r6.jpg"):
            (images / name).write_bytes(b"fixture")

        manifest = root / "manifest.csv"
        fields = [
            "reference_id",
            "local_path",
            "source_url",
            "paper_title",
            "venue",
            "caption_text",
            "figure_role",
            "archetype",
            "data_type",
            "data_analysis_type",
            "figure_type",
            "extraction_quality",
            "license_status",
            "metadata_status",
            "classification_status",
            "ncs_template_status",
        ]
        rows = [
            {
                "reference_id": "r1",
                "local_path": str(images / "r1.jpg"),
                "source_url": "https://doi.org/10.example/r1",
                "paper_title": "Coupled feedback framework",
                "venue": "Nature Communications",
                "caption_text": "Mechanism feedback and boundary conditions",
                "figure_role": "conceptual_summary",
                "archetype": "mechanism map",
                "data_type": "environmental_science_conceptual_reference",
                "data_analysis_type": "conceptual_summary",
                "figure_type": "conceptual_mechanism_diagram",
                "extraction_quality": "MANUALLY_REVIEWED",
                "license_status": "LOCAL_USE_ONLY",
                "metadata_status": "VERIFIED",
                "classification_status": "VISUALLY_CONFIRMED",
                "ncs_template_status": "",
            },
            {
                "reference_id": "r2",
                "local_path": str(images / "r2.jpg"),
                "source_url": "https://doi.org/10.example/r2",
                "paper_title": "Feedback synthesis",
                "venue": "Nature Reviews Earth & Environment",
                "caption_text": "Feedback framework",
                "figure_role": "conceptual_summary",
                "archetype": "mechanism map",
                "data_type": "environmental_science_conceptual_reference",
                "data_analysis_type": "conceptual_summary",
                "figure_type": "conceptual_mechanism_diagram",
                "extraction_quality": "AUTO_EXTRACTED_UNREVIEWED",
                "license_status": "LOCAL_USE_ONLY_PROVISIONAL",
                "metadata_status": "VERIFIED_METADATA_IF_PROVISIONAL",
                "classification_status": "RULE_INFERRED_NEEDS_REVIEW",
                "ncs_template_status": "",
            },
            {
                "reference_id": "r3",
                "local_path": str(images / "r3.jpg"),
                "source_url": "https://doi.org/10.example/r3",
                "paper_title": "Workflow",
                "venue": "Science",
                "caption_text": "Processing pipeline",
                "figure_role": "workflow",
                "archetype": "method schematic",
                "data_type": "workflow_or_metadata",
                "data_analysis_type": "method_structure",
                "figure_type": "pipeline_schematic",
                "extraction_quality": "MANUALLY_REVIEWED",
                "license_status": "LOCAL_USE_ONLY",
                "metadata_status": "VERIFIED",
                "classification_status": "VISUALLY_CONFIRMED",
                "ncs_template_status": "",
            },
            {
                "reference_id": "r4",
                "local_path": str(images / "missing.jpg"),
                "source_url": "https://doi.org/10.example/r4",
                "paper_title": "Missing figure",
                "venue": "Nature",
                "caption_text": "Feedback",
                "figure_role": "conceptual_summary",
                "archetype": "mechanism map",
                "data_type": "environmental_science_conceptual_reference",
                "data_analysis_type": "conceptual_summary",
                "figure_type": "conceptual_mechanism_diagram",
                "extraction_quality": "MANUALLY_REVIEWED",
                "license_status": "LOCAL_USE_ONLY",
                "metadata_status": "VERIFIED",
                "classification_status": "VISUALLY_CONFIRMED",
                "ncs_template_status": "",
            },
            {
                "reference_id": "r5",
                "local_path": str(images / "r5.jpg"),
                "source_url": "https://doi.org/10.example/r5",
                "paper_title": "Conceptual chemistry framework",
                "venue": "Nature Communications",
                "caption_text": "Mechanism feedback and boundary conditions",
                "figure_role": "conceptual_summary",
                "archetype": "mechanism map",
                "data_type": "environmental_chemistry_material",
                "data_analysis_type": "conceptual_summary",
                "figure_type": "conceptual_mechanism_diagram",
                "extraction_quality": "MANUALLY_REVIEWED",
                "license_status": "LOCAL_USE_ONLY",
                "metadata_status": "VERIFIED",
                "classification_status": "VISUALLY_CONFIRMED",
                "ncs_template_status": "",
            },
            {
                "reference_id": "r6",
                "local_path": str(images / "r6.jpg"),
                "source_url": "https://doi.org/10.example/r6",
                "paper_title": "Conceptual relationship framework",
                "venue": "Nature Communications",
                "caption_text": "Mechanism feedback and boundary conditions",
                "figure_role": "conceptual_summary",
                "archetype": "mechanism map",
                "data_type": "environmental_science_conceptual_reference",
                "data_analysis_type": "relationship_analysis",
                "figure_type": "conceptual_mechanism_diagram",
                "extraction_quality": "MANUALLY_REVIEWED",
                "license_status": "LOCAL_USE_ONLY",
                "metadata_status": "VERIFIED",
                "classification_status": "VISUALLY_CONFIRMED",
                "ncs_template_status": "",
            },
        ]
        with manifest.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

        before_hash = sha256_file(manifest)
        query = Query(
            figure_types=("conceptual_mechanism_diagram",),
            data_types=("environmental_science_conceptual_reference",),
            data_analysis_types=("conceptual_summary",),
            figure_roles=("conceptual",),
            archetypes=("mechanism",),
            venue_family="ncs",
            terms=("feedback", "boundary"),
            limit=3,
        )
        result = select_candidates(manifest, query)
        ids = [candidate["reference_id"] for candidate in result["candidates"]]
        assert ids == ["r1", "r2"], ids
        assert result["candidates"][0]["match_strength"] == "STRONG"
        assert "CLASSIFICATION_REVIEW_REQUIRED" in result["candidates"][1]["warnings"]
        assert result["corpus_health"]["excluded_missing_path"] == 1
        assert result["corpus_health"]["excluded_figure_type"] == 1
        assert result["corpus_health"]["excluded_data_type"] == 1
        assert result["corpus_health"]["excluded_data_analysis_type"] == 1

        output_json = root / "out" / "candidates.json"
        output_csv = root / "out" / "candidates.csv"
        write_json(output_json, result)
        write_csv(output_csv, result["candidates"])
        assert json.loads(output_json.read_text(encoding="utf-8"))["status"] == STATUS
        with output_csv.open("r", encoding="utf-8-sig", newline="") as handle:
            assert len(list(csv.DictReader(handle))) == 2
        assert sha256_file(manifest) == before_hash

    print("SELF_TEST=PASS")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Select auditable candidate figures from a CSV manifest without modifying "
            "the manifest or corpus. Output candidates are not approved benchmarks."
        )
    )
    parser.add_argument("--manifest", type=Path, help="Path to REFERENCE_FIGURE_MANIFEST.csv")
    parser.add_argument(
        "--figure-type",
        action="append",
        default=[],
        help="Exact figure_type value; repeat or comma-separate.",
    )
    parser.add_argument(
        "--figure-role",
        action="append",
        default=[],
        help="Preferred figure_role substring; repeat or comma-separate.",
    )
    parser.add_argument(
        "--data-type",
        action="append",
        default=[],
        help="Strict exact data_type filter; repeat or comma-separate.",
    )
    parser.add_argument(
        "--data-analysis-type",
        action="append",
        default=[],
        help="Strict exact data_analysis_type filter; repeat or comma-separate.",
    )
    parser.add_argument(
        "--archetype",
        action="append",
        default=[],
        help="Preferred archetype substring; repeat or comma-separate.",
    )
    parser.add_argument(
        "--venue-family",
        choices=("nature", "science", "cell", "pnas", "ncs"),
        default="",
        help="Strict venue-family filter.",
    )
    parser.add_argument(
        "--venue",
        action="append",
        default=[],
        help="Strict venue substring filter; repeat or comma-separate.",
    )
    parser.add_argument(
        "--term",
        action="append",
        default=[],
        help=(
            "Soft claim/comparator/uncertainty/caption search term; repeat or "
            "comma-separate."
        ),
    )
    parser.add_argument("--limit", type=int, default=12, help="Maximum candidates (default: 12).")
    parser.add_argument(
        "--include-missing",
        action="store_true",
        help="Include rows whose local_path is missing; off by default.",
    )
    parser.add_argument(
        "--require-reviewed",
        action="store_true",
        help="Require verified metadata and reviewed classification/extraction.",
    )
    parser.add_argument("--output-json", type=Path, help="Optional JSON audit output.")
    parser.add_argument("--output-csv", type=Path, help="Optional ranked CSV output.")
    parser.add_argument("--self-test", action="store_true", help="Run deterministic fixtures.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.self_test:
        run_self_test()
        return 0
    if args.manifest is None:
        parser.error("--manifest is required unless --self-test is used")

    query = Query(
        figure_types=split_values(args.figure_type),
        data_types=split_values(args.data_type),
        data_analysis_types=split_values(args.data_analysis_type),
        figure_roles=split_values(args.figure_role),
        archetypes=split_values(args.archetype),
        venue_family=args.venue_family,
        venues=split_values(args.venue),
        terms=split_values(args.term),
        limit=args.limit,
        include_missing=args.include_missing,
        require_reviewed=args.require_reviewed,
    )
    result = select_candidates(args.manifest, query)
    if args.output_json:
        write_json(args.output_json, result)
    if args.output_csv:
        write_csv(args.output_csv, result["candidates"])

    summary = {
        "schema_version": result["schema_version"],
        "status": result["status"],
        "manifest": result["manifest"],
        "manifest_sha256": result["manifest_sha256"],
        "candidate_count": result["candidate_count"],
        "corpus_health": result["corpus_health"],
        "top_reference_ids": [
            candidate["reference_id"] for candidate in result["candidates"]
        ],
        "output_json": str(args.output_json.resolve()) if args.output_json else "",
        "output_csv": str(args.output_csv.resolve()) if args.output_csv else "",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, ValueError, csv.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
