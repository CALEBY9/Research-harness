"""One-time, allowlisted import of the installed research skill source.

Does not read global config, credentials, sessions, memory, or research projects.
Existing destinations are refused. Run validate before committing any import.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil

LOCAL = """research-agent nature-scientific-insight humanizer humanizer-zh nature-literature-kb
nature-research-discovery nature-method-design nature-experiment-plan nature-data-analysis nature-evidence-audit nature-literature-synthesis
nature-paper-format nature-scholar-distiller""".split()
EXCLUDE = {".git", ".agent", "__pycache__", ".venv", "node_modules", "candidates"}
EXTENSIONS = {".md", ".py", ".json", ".yaml", ".yml", ".toml", ".txt", ".sh",
              ".mjs", ".tsv", ".tex", ".bib", ".ris", ".nbib", ".png", ".jpg", ".pdf"}
BARE_NAMES = {"LICENSE", "NOTICE", ".gitignore", ".gitattributes"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    repo = args.repo.resolve()
    if (repo / "skills").exists() or (repo / "docs/import_manifest.json").exists():
        parser.error("Import destination already exists; use reviewed file-level diffs for updates.")
    sources = [(args.home / ".codex/skills" / name, "local-support", name) for name in LOCAL]
    selected = []
    excluded = []
    for source, group, name in sources:
        if not (source / "SKILL.md").is_file():
            parser.error(f"Required installed skill missing: {name}")
        for path in sorted(source.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(source)
            if any(part in EXCLUDE for part in relative.parts) or path.suffix in {".pyc", ".log"}:
                continue
            if path.is_symlink() or not path.resolve().is_relative_to(source.resolve()):
                parser.error(f"External file link requires separate review: {name}/{relative}")
            if path.suffix not in EXTENSIONS and path.name not in BARE_NAMES:
                excluded.append(f"{name}/{relative.as_posix()}")
                continue
            selected.append((path, Path("skills") / name / relative))
    if excluded:
        parser.error("Unreviewed file types: " + ", ".join(excluded))
    rows = []
    for source, relative in selected:
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise RuntimeError(f"Copy mismatch: {relative}")
        rows.append({"path": relative.as_posix(), "source_sha256": digest})
    manifest = {
        "schema_version": 1,
        "scope": "installed skill source snapshot, not an upstream pristine release",
        "skills": [{"name": name, "source_group": group} for _, group, name in sources],
        "files": rows,
        "excluded": sorted(EXCLUDE | {"*.pyc", "*.log"}),
        "note": "Hashes verify initial import only; legitimate future source edits need not match them."
    }
    (repo / "docs").mkdir(exist_ok=True)
    (repo / "docs/import_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"skills": len(sources), "files": len(rows), "copy_verified": True}))


if __name__ == "__main__":
    main()
