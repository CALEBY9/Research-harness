"""Research Harness distribution and maintenance; standard library, no model calls."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORE = {".git", ".agent", "local_state", "__pycache__", ".venv", "node_modules"}
TEXT = {".md", ".py", ".json", ".yaml", ".yml", ".toml", ".txt", ".sh", ".mjs",
        ".tsv", ".tex", ".bib", ".ris", ".nbib"}
SECRET_PATTERNS = [
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    re.compile(r"\bsk-(?:proj-|ant-api\d+-)?[A-Za-z0-9_-]{32,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"https?://[^\s/@:]+:[^\s/@]+@"),
]


def source_files(root=ROOT):
    return [p for p in root.rglob("*") if p.is_file()
            and not any(part in IGNORE for part in p.relative_to(root).parts)]


def load_catalog(root=ROOT):
    """Read the explicit active set; archived directories are never auto-enabled."""
    catalog = json.loads((root / "skills/catalog.json").read_text(encoding="utf-8"))
    for key in ("active", "inactive", "shared", "support_files", "exclude"):
        values = catalog.get(key) if isinstance(catalog, dict) else None
        if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
            raise ValueError(f"Catalog {key} must be a list of paths/names")
        if len(values) != len(set(values)):
            raise ValueError(f"Duplicate catalog entry: {key}")
        for value in values:
            parts = Path(value).parts
            if not parts or Path(value).is_absolute() or ".." in parts or "\\" in value or ":" in value:
                raise ValueError(f"Invalid catalog path: {value}")
            if key in {"active", "inactive", "shared"} and not re.fullmatch(r"[a-z0-9-]+", value):
                raise ValueError(f"Invalid skill/resource name: {value}")
    active, inactive = set(catalog["active"]), set(catalog["inactive"])
    if not active or active & inactive:
        raise ValueError("Catalog needs a nonempty active set, disjoint from inactive skills")
    discovered = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
    # Retired names remain detectable even after their source directories are removed.
    mismatch = (active - discovered) | (discovered - active - inactive)
    if mismatch:
        raise ValueError(f"Catalog/source mismatch: {sorted(mismatch)}")
    for name in catalog["shared"]:
        if not (root / "skills" / name).is_dir() or name in inactive:
            raise ValueError(f"Missing or inactive shared resource: {name}")
    for name in catalog["support_files"]:
        if not (root / name).is_file():
            raise ValueError(f"Missing distribution notice/license: {name}")
    return catalog


def validate(root=ROOT):
    errors = []
    catalog = None
    try:
        catalog = load_catalog(root)
    except (OSError, ValueError) as error:
        errors.append(f"Distribution catalog: {error}")
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    names = set()
    for skill in skills:
        text = skill.read_text(encoding="utf-8-sig")
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            errors.append(f"Invalid frontmatter: {skill.relative_to(root)}")
            continue
        for key in ("name", "description"):
            if not re.search(rf"^{key}:\s*\S", parts[1], re.M):
                errors.append(f"Missing {key}: {skill.relative_to(root)}")
        match = re.search(r"^name:\s*['\"]?([^\s'\"]+)", parts[1], re.M)
        if match:
            name = match.group(1)
            if name in names:
                errors.append(f"Duplicate skill name: {name}")
            names.add(name)
            if name != skill.parent.name and (skill.parent.name, name) != ("humanizer", "humanizer:humanizer"):
                errors.append(f"Undeclared folder/name mismatch: {skill.parent.name} / {name}")
    if not skills:
        errors.append("No installed source snapshot under skills/.")
    py_count = 0
    for path in source_files(root):
        if catalog and excluded(path, root, catalog):
            continue
        rel = path.relative_to(root)
        if path.name in {"auth.json", "credentials.json"} or path.name == ".env" or (
                path.name.startswith(".env.") and path.name != ".env.example") or path.suffix in {".pem", ".key"}:
            errors.append(f"Forbidden sensitive filename: {rel}")
        if path.suffix not in TEXT:
            continue
        try:
            content = path.read_text(encoding="utf-8-sig")
        except UnicodeError:
            errors.append(f"Non-UTF8 text: {rel}")
            continue
        for index, line in enumerate(content.splitlines(), 1):
            if any(pattern.search(line) for pattern in SECRET_PATTERNS):
                errors.append(f"Potential credential, inspect locally without printing value: {rel}:{index}")
        if path.suffix == ".py":
            try:
                ast.parse(content, filename=str(rel))
                py_count += 1
            except SyntaxError as error:
                errors.append(f"Python syntax: {rel}:{error.lineno}")
        if path.suffix == ".json":
            try:
                json.loads(content)
            except json.JSONDecodeError as error:
                errors.append(f"JSON syntax: {rel}:{error.lineno}")
    pack = root / "skills/research-agent/references/copilot-regression.json"
    cases = []
    private_cases = []
    if pack.is_file():
        try:
            payload = json.loads(pack.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            payload = {}
            # The JSON check above already records the exact failure locator.
        cases = payload.get("cases", []) if isinstance(payload, dict) else []
        if not isinstance(cases, list) or any(not isinstance(c, dict) or "case_id" not in c for c in cases):
            errors.append("Invalid regression cases: expected objects with case_id")
            cases = []
        if not cases:
            errors.append("Regression cases missing or empty")
        ids = [case["case_id"] for case in cases]
        if len(ids) != len(set(ids)):
            errors.append("Duplicate regression case IDs")
        for case in cases:
            owner = case.get("expected_owner")
            if owner and owner not in names:
                errors.append(f"Missing route owner: {case['case_id']} -> {owner}")
            elif owner and catalog and owner not in catalog["active"]:
                errors.append(f"Inactive route owner: {case['case_id']} -> {owner}")
            if "fixture" in case:
                private_cases.append(case["case_id"])
    else:
        errors.append("Research Agent regression pack missing")
    return {"status": "FAIL" if errors else "PASS", "skills": len(skills),
            "active_skills": len(catalog["active"]) if catalog else 0,
            "python_parsed": py_count, "regression_definitions": len(cases),
            "private_fixture_cases_not_executed": private_cases,
            "behavioral_evaluations_executed": 0, "errors": errors,
            "limits": "Structural/known-pattern credential scan only; not full secret detection or scientific QA."}


def doctor(root=ROOT, target=None):
    paths = []
    catalog = load_catalog(root)
    for path in source_files(root / "skills"):
        if path.suffix not in TEXT or excluded(path, root, catalog):
            continue
        content = path.read_text(encoding="utf-8-sig")
        for index, line in enumerate(content.splitlines(), 1):
            if re.search(r"[A-Z]:[/\\]|/(?:Users|home)/[^/\s]+/", line):
                paths.append({"file": path.relative_to(root).as_posix(), "line": index})
    kb_value = os.environ.get("RESEARCH_AGENT_KB_ROOT")
    kb = Path(kb_value).expanduser() if kb_value else None
    result = {"status": "LOCAL_DEPENDENCIES_PRESENT" if paths else "NO_ABSOLUTE_PATHS_FOUND",
            "absolute_path_locations": paths,
            "optional_kb": {"configured": kb is not None,
                            "root_exists": kb.is_dir() if kb else False,
                            "library_entrypoint_exists": (kb / "papers/scripts/research_library.py").is_file() if kb else False},
            "note": "Locators only; no source text or secret values. Paths may include examples. Review before migration."}
    if target is not None:
        result["installation"] = check_installation(target, None, root)
    return result


def distribution_plan(selected, root=ROOT):
    result = validate(root)
    if result["errors"]:
        raise ValueError("Source validation failed; run validate to inspect locators.")
    catalog = load_catalog(root)
    requested = list(dict.fromkeys(selected or catalog["active"]))
    missing = sorted(set(requested) - set(catalog["active"]))
    if missing:
        raise ValueError("Unknown or inactive skill: " + ", ".join(missing))
    directories = list(dict.fromkeys(requested + catalog["shared"]))
    entries = {name: root / "skills" / name for name in directories}
    for relative in catalog["support_files"]:
        name = Path(relative).name
        if name in entries:
            raise ValueError(f"Distribution destination collision: {name}")
        entries[name] = root / relative
    return catalog, directories, entries


def check_target(target, root):
    if target == root or root.is_relative_to(target) or target.is_relative_to(root / "skills"):
        raise ValueError("Target overlaps source.")


def excluded(path, root, catalog):
    relative = path.relative_to(root)
    if any(part in IGNORE for part in relative.parts) or path.suffix in {".pyc", ".pyo"}:
        return True
    return any(relative == Path(item) or Path(item) in relative.parents for item in catalog["exclude"])


def copy_distribution(target, entries, root, catalog):
    def ignore(directory, names):
        return [name for name in names if excluded(Path(directory) / name, root, catalog)]

    target.mkdir(parents=True, exist_ok=True)
    for name, source in entries.items():
        if source.is_dir():
            shutil.copytree(source, target / name, ignore=ignore)
        else:
            shutil.copy2(source, target / name)


def stage(target, selected, root=ROOT):
    """Stage active skills, shared dependencies and notices outside discovery."""
    root = root.resolve()
    target = target.expanduser().resolve()
    if target.exists():
        raise ValueError("Staging target exists. Select a fresh directory; existing files are never overwritten.")
    check_target(target, root)
    if any(part in {".codex", ".agents", ".claude"} for part in target.parts):
        raise ValueError("Use a staging directory outside live CLI configuration/skill discovery.")
    catalog, directories, entries = distribution_plan(selected, root)
    copy_distribution(target, entries, root, catalog)
    return {"status": "STAGED", "skills": len(set(directories) & set(catalog["active"])),
            "directories": directories, "live_installation_changed": False,
            "note": "Active skills plus shared resources/notices; external dependencies are not installed."}


def install(target, selected, root=ROOT, dry_run=False):
    """Explicit installation; preflight every destination and never overwrite."""
    root = root.resolve()
    target = target.expanduser().resolve()
    check_target(target, root)
    catalog, directories, entries = distribution_plan(selected, root)
    conflicts = [name for name in entries if (target / name).exists() or (target / name).is_symlink()]
    if target.exists() and not target.is_dir():
        raise ValueError("Installation target is not a directory")
    if conflicts:
        raise ValueError("Existing installation entries; compare before updating: " + ", ".join(conflicts))
    if not dry_run:
        copy_distribution(target, entries, root, catalog)
    return {"status": "INSTALL_PLAN" if dry_run else "INSTALLED", "target": str(target),
            "skills": len(set(directories) & set(catalog["active"])),
            "directories": directories, "notices": [name for name, src in entries.items() if src.is_file()],
            "note": "No runtime settings, models, accounts or third-party services are configured."}


def check_installation(target, selected, root=ROOT):
    """Verify distributed files, without claiming host discovery or model behavior."""
    root = root.resolve()
    target = target.expanduser().resolve()
    catalog, directories, entries = distribution_plan(selected, root)
    missing, changed = [], []
    for name, source in entries.items():
        if source.is_dir():
            files = [p for p in source.rglob("*") if p.is_file() and not excluded(p, root, catalog)]
            pairs = [(p, target / name / p.relative_to(source)) for p in files]
        else:
            pairs = [(source, target / name)]
        for original, installed in pairs:
            if not installed.is_file():
                missing.append(installed.relative_to(target).as_posix())
            elif original.read_bytes() != installed.read_bytes():
                changed.append(installed.relative_to(target).as_posix())
    inactive = [name for name in catalog["inactive"] if (target / name / "SKILL.md").exists()]
    return {"status": "FAIL" if missing or changed or inactive else "PASS", "target": str(target),
            "directories": directories, "missing": missing, "changed": changed, "inactive_present": inactive,
            "limits": "File layout/content only; host discovery, external tools and research quality are not tested."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="Check source structure, Python/JSON and known secret patterns")
    diagnosis = commands.add_parser("doctor", help="Report path dependencies and optional KB binding")
    diagnosis.add_argument("--target", type=Path, help="Also check an installation")
    commands.add_parser("list", help="List active, inactive and shared distribution entries")
    staging = commands.add_parser("stage", help="Copy source to a fresh directory; never activate skills")
    staging.add_argument("--target", required=True, type=Path)
    staging.add_argument("--skill", action="append", dest="selected")
    installation = commands.add_parser("install", help="Install to an explicit target without overwriting entries")
    installation.add_argument("--target", required=True, type=Path)
    installation.add_argument("--skill", action="append", dest="selected")
    installation.add_argument("--dry-run", action="store_true")
    checking = commands.add_parser("check", help="Verify installed files against this checkout")
    checking.add_argument("--target", required=True, type=Path)
    checking.add_argument("--skill", action="append", dest="selected")
    args = parser.parse_args()
    try:
        if args.command == "validate":
            result = validate()
        elif args.command == "doctor":
            result = doctor(target=args.target)
        elif args.command == "list":
            result = load_catalog()
        elif args.command == "stage":
            result = stage(args.target, args.selected)
        elif args.command == "install":
            result = install(args.target, args.selected, dry_run=args.dry_run)
        else:
            result = check_installation(args.target, args.selected)
    except (OSError, ValueError) as error:
        parser.exit(2, f"{error}\n")
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 1 if result.get("status") == "FAIL" or result.get("installation", {}).get("status") == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
