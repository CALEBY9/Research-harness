#!/usr/bin/env python3
"""Scan final manuscript artifacts for author-process and toolchain leakage.

The scanner is intentionally dependency-free. It extracts visible text from
plain text files and common Office Open XML containers, then reports high-risk
phrases that should not appear in clean scholarly deliverables.
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


NS_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
NS_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


@dataclass(frozen=True)
class PatternRule:
    risk_type: str
    decision: str
    pattern: str
    suggestion: str
    flags: int = re.IGNORECASE


RULES: list[PatternRule] = [
    # Reviewer/revision leakage.
    PatternRule("revision_response_leakage", "REMOVE", r"\breviewer[- ]response\b", "Move to response letter or audit report."),
    PatternRule("revision_response_leakage", "REMOVE", r"\breviewers?' concern\b", "State the scientific rationale directly."),
    PatternRule("revision_response_leakage", "REMOVE", r"\breviewer questions?\b", "Move to response letter."),
    PatternRule("revision_response_leakage", "REMOVE", r"\bin response to (the )?concern\b", "Move to response letter."),
    PatternRule("revision_response_leakage", "REMOVE", r"\baccording to the reviewer\b", "Move to response letter."),
    PatternRule("revision_response_leakage", "REMOVE", r"\bas requested by the reviewer\b", "Move to response letter."),
    PatternRule("revision_response_leakage", "REMOVE", r"\brevised audit\b", "Use a reader-facing validation term or move to audit report."),
    PatternRule("revision_response_leakage", "REMOVE", r"\bRevision implemented\b", "Move implementation status to change log."),
    PatternRule("revision_response_leakage", "RECAST", r"\bwas revised to\b", "Describe the final method/result directly."),
    PatternRule("revision_response_leakage", "RECAST", r"\brevised manuscript\b", "Use 'the manuscript' only outside response materials."),
    PatternRule("revision_response_leakage", "RECAST", r"\bnew and revised\b", "Use the final scholarly concept."),
    PatternRule("revision_response_leakage", "REMOVE", r"根据审稿人|审稿人指出|审稿意见|回应审稿人", "Move reviewer-facing wording to response letter.", 0),
    PatternRule("revision_response_leakage", "RECAST", r"原稿|原文|改为|修改为|标黄|修订", "Use clean final wording, not before/after wording.", 0),

    # Before/after and original-to-final process framing.
    PatternRule("before_after_process_framing", "RECAST", r"\bbased on the original\b", "State the final basis or data source directly."),
    PatternRule("before_after_process_framing", "RECAST", r"\boriginal (model|formulation|manuscript)\b", "Use final scholarly terminology."),
    PatternRule("before_after_process_framing", "RECAST", r"\blegacy variable\b", "Use 'former notation' only in supplements if needed."),
    PatternRule("before_after_process_framing", "RECAST", r"\boriginal-to-calibrated\b", "Use 'calibrated'."),
    PatternRule("before_after_process_framing", "RECAST", r"\bbaseline-to-calibrated\b", "Use 'calibrated'."),
    PatternRule("before_after_process_framing", "RECAST", r"\b(is|are) replaced by\b", "Describe the final model relation directly."),
    PatternRule("before_after_process_framing", "RECAST", r"\breplaces the original\b", "Describe the final model relation directly."),
    PatternRule("before_after_process_framing", "RECAST", r"\bretired from\b", "Move historical notation to supplement or omit."),
    PatternRule("before_after_process_framing", "RECAST", r"\bnewly introduced\b", "Use 'the model includes' or the final concept."),
    PatternRule("before_after_process_framing", "RECAST", r"\bintroduced only\b", "Use the final scope statement."),

    # Toolchain/runtime/implementation leakage.
    PatternRule("tool_runtime_leakage", "RECAST", r"\bimplemented model\b", "Use 'the model specifies' or 'the calibrated model'."),
    PatternRule("tool_runtime_leakage", "RECAST", r"\bimplementation-level\b", "Use a methodological term or omit."),
    PatternRule("tool_runtime_leakage", "RECAST", r"\bin implementation\b", "Use 'in the model' only when scientifically needed."),
    PatternRule("tool_runtime_leakage", "RECAST", r"\bactive runtime model\b", "Use 'calibrated model'."),
    PatternRule("tool_runtime_leakage", "RECAST", r"\bruntime coverage\b", "Use 'scenario coverage' if reader-facing."),
    PatternRule("tool_runtime_leakage", "RECAST", r"\baccepted runtime outputs?\b", "Use 'reported model outputs'."),
    PatternRule("tool_runtime_leakage", "REMOVE", r"\bparser outputs?\b", "Move parser details to audit/reproducibility notes."),
    PatternRule("tool_runtime_leakage", "REMOVE", r"\bGUI export\b", "Move export details to reproducibility notes."),
    PatternRule("tool_runtime_leakage", "REMOVE", r"\bscript generated\b", "Move generation details to audit/reproducibility notes."),
    PatternRule("tool_runtime_leakage", "REMOVE", r"\bInternal QA\b", "Move QA status to internal checklist."),
    PatternRule("tool_runtime_leakage", "REMOVE", r"\bartifact render\b", "Move renderer details to QA report."),
    PatternRule("tool_runtime_leakage", "REMOVE", r"\bWord-native PDF QA\b", "Move QA status to internal checklist."),
    PatternRule("tool_runtime_leakage", "RECAST", r"\bworkflow\b", "Use a scientific process term only if this is the research object."),
    PatternRule("tool_runtime_leakage", "REMOVE", r"\bworkspace\b", "Remove local working-environment language."),

    # Placeholders, internal codes, and local locators.
    PatternRule("placeholder_internal_code", "REMOVE", r"\bTODO(?:_CITE)?\b", "Resolve placeholder before submission.", 0),
    PatternRule("placeholder_internal_code", "REMOVE", r"\bremove before submission\b", "Remove internal instruction."),
    PatternRule("placeholder_internal_code", "REMOVE", r"\bbefore submission\b", "Remove internal instruction unless in checklist."),
    PatternRule("placeholder_internal_code", "REMOVE", r"\bDraft positioning\b", "Remove draft marker."),
    PatternRule("placeholder_internal_code", "REMOVE", r"\bProvisional\b", "Remove draft marker unless it names a formal policy."),
    PatternRule("placeholder_internal_code", "REMOVE", r"\bmachine-simulated\b", "Use methodological term if needed."),
    PatternRule("placeholder_internal_code", "RECAST", r"\b(?:internal|author-side) (?:field|stage|run|dataset|version) (?:name|label|code)\b", "Map the author-side locator through a Publication Terminology Map."),
    PatternRule("local_path_or_file_artifact", "REMOVE", r"[A-Za-z]:\\(?:[^\\/:*?\"<>|\r\n]+\\)+[^\\/:*?\"<>|\r\n]+", "Remove local Windows path."),
    PatternRule("local_path_or_file_artifact", "REMOVE", r"\b[\w.-]+\.(?:py|ipynb|R|r|do|csv|tsv|xlsx|docx|pptx|png|svg|pdf)\b", "Keep file names only in data/code availability or supplement."),
]


TEXT_SUFFIXES = {
    ".txt",
    ".md",
    ".markdown",
    ".csv",
    ".tsv",
    ".tex",
    ".xml",
    ".svg",
    ".html",
    ".htm",
    ".json",
    ".yml",
    ".yaml",
}


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def text_from_word_element(elem: ET.Element) -> str:
    return normalize_space("".join((node.text or "") for node in elem.iter(f"{NS_W}t")))


def scan_docx_structural(path: Path) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    if path.suffix.lower() != ".docx":
        return hits
    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
        if "word/comments.xml" in names:
            try:
                comments_root = ET.fromstring(zf.read("word/comments.xml"))
            except ET.ParseError:
                comments_root = None
            if comments_root is not None:
                for comment in comments_root.iter(f"{NS_W}comment"):
                    cid = comment.attrib.get(f"{NS_W}id", "")
                    author = comment.attrib.get(f"{NS_W}author", "")
                    ctext = text_from_word_element(comment)
                    hits.append(
                        {
                            "artifact": str(path),
                            "location": f"{path.name}:word/comments.xml:comment:{cid}",
                            "risk_type": "document_structure_leakage",
                            "decision": "REMOVE",
                            "pattern": "<w:comment>",
                            "match": f"Word comment {cid}",
                            "snippet": f"author={author}; text={ctext}",
                            "suggested_recast": "Remove all Word comments from the clean manuscript; move any needed note to the response letter, audit report, or internal checklist.",
                        }
                    )

        structural_checks = [
            ("ins", "<w:ins>", "tracked insertion"),
            ("del", "<w:del>", "tracked deletion"),
            ("moveFrom", "<w:moveFrom>", "tracked move-from"),
            ("moveTo", "<w:moveTo>", "tracked move-to"),
            ("commentReference", "<w:commentReference>", "comment reference"),
            ("commentRangeStart", "<w:commentRangeStart>", "comment range"),
        ]
        for part in sorted(name for name in names if name.startswith("word/") and name.endswith(".xml")):
            try:
                root = ET.fromstring(zf.read(part))
            except ET.ParseError:
                continue
            for local, pattern, label in structural_checks:
                elems = list(root.iter(f"{NS_W}{local}"))
                if not elems:
                    continue
                hits.append(
                    {
                        "artifact": str(path),
                        "location": f"{path.name}:{part}",
                        "risk_type": "document_structure_leakage",
                        "decision": "REMOVE",
                        "pattern": pattern,
                        "match": f"{label}: {len(elems)}",
                        "snippet": f"{len(elems)} {label} element(s) remain in {part}",
                        "suggested_recast": "Clean manuscripts must not contain unresolved comments or tracked-change structures.",
                    }
                )
    return hits


def iter_text_xml(xml_bytes: bytes, source: str) -> Iterable[tuple[str, str]]:
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return

    # Word paragraphs retain useful ordering and locations.
    para_idx = 0
    for para in root.iter(f"{NS_W}p"):
        texts = [node.text or "" for node in para.iter(f"{NS_W}t")]
        value = normalize_space("".join(texts))
        if value:
            para_idx += 1
            yield f"{source}:p{para_idx}", value

    # DrawingML text boxes and PowerPoint runs.
    drawing_idx = 0
    for para in root.iter(f"{NS_A}p"):
        texts = [node.text or "" for node in para.iter(f"{NS_A}t")]
        value = normalize_space("".join(texts))
        if value:
            drawing_idx += 1
            yield f"{source}:drawing{drawing_idx}", value


def iter_docx(path: Path) -> Iterable[tuple[str, str]]:
    with zipfile.ZipFile(path) as zf:
        names = [
            name
            for name in zf.namelist()
            if name.startswith("word/")
            and name.endswith(".xml")
            and (
                name == "word/document.xml"
                or name.startswith("word/header")
                or name.startswith("word/footer")
                or name in {"word/footnotes.xml", "word/endnotes.xml", "word/comments.xml"}
            )
        ]
        for name in sorted(names):
            yield from iter_text_xml(zf.read(name), f"{path.name}:{name}")


def iter_pptx(path: Path) -> Iterable[tuple[str, str]]:
    with zipfile.ZipFile(path) as zf:
        names = [
            name
            for name in zf.namelist()
            if name.endswith(".xml")
            and (
                name.startswith("ppt/slides/")
                or name.startswith("ppt/notesSlides/")
                or name.startswith("ppt/comments/")
            )
        ]
        for name in sorted(names):
            yield from iter_text_xml(zf.read(name), f"{path.name}:{name}")


def iter_xlsx(path: Path) -> Iterable[tuple[str, str]]:
    with zipfile.ZipFile(path) as zf:
        for name in sorted(name for name in zf.namelist() if name in {"xl/sharedStrings.xml"} or name.startswith("xl/worksheets/")):
            yield from iter_text_xml(zf.read(name), f"{path.name}:{name}")


def iter_plain(path: Path) -> Iterable[tuple[str, str]]:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        return

    if path.suffix.lower() in {".html", ".htm", ".xml", ".svg"}:
        text = re.sub(r"<[^>]+>", " ", text)
        text = html.unescape(text)

    for idx, line in enumerate(text.splitlines(), start=1):
        value = normalize_space(line)
        if value:
            yield f"{path.name}:line{idx}", value


def iter_artifact_text(path: Path) -> Iterable[tuple[str, str]]:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        yield from iter_docx(path)
    elif suffix == ".pptx":
        yield from iter_pptx(path)
    elif suffix == ".xlsx":
        yield from iter_xlsx(path)
    elif suffix in TEXT_SUFFIXES:
        yield from iter_plain(path)


def collect_paths(inputs: list[str]) -> list[Path]:
    paths: list[Path] = []
    for item in inputs:
        path = Path(item)
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and (child.suffix.lower() in TEXT_SUFFIXES or child.suffix.lower() in {".docx", ".pptx", ".xlsx"}):
                    paths.append(child)
        elif path.is_file():
            paths.append(path)
    return sorted(set(paths))


def snippet(text: str, start: int, end: int, radius: int = 90) -> str:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    prefix = "..." if left > 0 else ""
    suffix = "..." if right < len(text) else ""
    return prefix + text[left:right] + suffix


def is_url_filename_context(text: str, start: int, end: int) -> bool:
    left = start
    while left > 0 and not text[left - 1].isspace():
        left -= 1
    right = end
    while right < len(text) and not text[right].isspace():
        right += 1
    token = text[left:right].strip("()[]{}<>.,;")
    return token.lower().startswith(("http://", "https://", "doi:", "www."))


def build_extra_term_rules(inline_terms: list[str], term_files: list[str]) -> list[PatternRule]:
    """Build literal project-local rules without embedding project vocabulary here."""
    terms: list[str] = []
    for term in inline_terms:
        value = term.strip()
        if value:
            terms.append(value)
    for item in term_files:
        path = Path(item)
        if not path.is_file():
            raise ValueError(f"extra-term file not found: {path}")
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            value = line.strip()
            if value and not value.startswith("#"):
                terms.append(value)

    rules: list[PatternRule] = []
    seen: set[str] = set()
    for term in terms:
        key = term.casefold()
        if key in seen:
            continue
        seen.add(key)
        rules.append(
            PatternRule(
                "project_local_term",
                "RECAST",
                re.escape(term),
                "Map this project-local locator to reader-facing terminology or move it to project QA records.",
            )
        )
    return rules


def scan_record(path: Path, location: str, text: str, rules: list[PatternRule]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for rule in rules:
        for match in re.finditer(rule.pattern, text, flags=rule.flags):
            if rule.risk_type == "local_path_or_file_artifact" and is_url_filename_context(text, match.start(), match.end()):
                continue
            hits.append(
                {
                    "artifact": str(path),
                    "location": location,
                    "risk_type": rule.risk_type,
                    "decision": rule.decision,
                    "pattern": rule.pattern,
                    "match": match.group(0),
                    "snippet": snippet(text, match.start(), match.end()),
                    "suggested_recast": rule.suggestion,
                }
            )
    return hits


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["artifact", "location", "risk_type", "decision", "pattern", "match", "snippet", "suggested_recast"]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, scanned: list[Path], hits: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    by_decision = Counter(row["decision"] for row in hits)
    by_risk = Counter(row["risk_type"] for row in hits)
    lines = [
        "# Clean-Final Scanner Report",
        "",
        f"- Artifacts scanned: {len(scanned)}",
        f"- High-risk hits: {len(hits)}",
        f"- Verdict: {'FAIL' if hits else 'PASS'}",
        "",
        "## Counts By Decision",
        "",
    ]
    if by_decision:
        lines.extend(f"- {key}: {value}" for key, value in sorted(by_decision.items()))
    else:
        lines.append("- none")
    lines.extend(["", "## Counts By Risk Type", ""])
    if by_risk:
        lines.extend(f"- {key}: {value}" for key, value in sorted(by_risk.items()))
    else:
        lines.append("- none")
    lines.extend(["", "## Hits", ""])
    if hits:
        for idx, row in enumerate(hits, start=1):
            lines.extend(
                [
                    f"### {idx}. {row['decision']} / {row['risk_type']}",
                    f"- Artifact: `{row['artifact']}`",
                    f"- Location: `{row['location']}`",
                    f"- Match: `{row['match']}`",
                    f"- Suggested action: {row['suggested_recast']}",
                    f"- Snippet: {row['snippet']}",
                    "",
                ]
            )
    else:
        lines.append("No unresolved high-risk hits detected.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan clean manuscript artifacts for process/toolchain leakage.")
    parser.add_argument("paths", nargs="+", help="Files or directories to scan.")
    parser.add_argument("--out-csv", default="clean_final_scan.csv", help="CSV output path.")
    parser.add_argument("--out-md", default="clean_final_scan_report.md", help="Markdown report output path.")
    parser.add_argument("--extra-term", action="append", default=[], help="Project-local literal term to flag; repeat as needed.")
    parser.add_argument("--extra-term-file", action="append", default=[], help="UTF-8 file with one project-local literal term per line; repeat as needed.")
    parser.add_argument("--no-fail", action="store_true", help="Return 0 even when hits are found.")
    args = parser.parse_args(argv)

    try:
        extra_rules = build_extra_term_rules(args.extra_term, args.extra_term_file)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    rules = [*RULES, *extra_rules]

    scanned = collect_paths(args.paths)
    hits: list[dict[str, str]] = []
    unsupported: list[Path] = []
    for path in scanned:
        extracted = list(iter_artifact_text(path))
        if not extracted:
            unsupported.append(path)
            continue
        for location, text in extracted:
            hits.extend(scan_record(path, location, text, rules))
        hits.extend(scan_docx_structural(path))

    write_csv(Path(args.out_csv), hits)
    write_report(Path(args.out_md), scanned, hits)

    print(f"artifacts_scanned={len(scanned)}")
    print(f"high_risk_hits={len(hits)}")
    print(f"project_local_rules={len(extra_rules)}")
    print(f"csv={args.out_csv}")
    print(f"report={args.out_md}")
    if unsupported:
        print(f"unsupported_or_empty={len(unsupported)}")
    if hits and not args.no_fail:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
