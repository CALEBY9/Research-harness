"""Check Nature upstream and prepare isolated comparisons; never install or merge."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import difflib
import json
import logging
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "https://github.com/Yuan1z0825/nature-skills.git"
DISCOVERY = {".agents", ".codex", ".claude"}


def git(*args, cwd=None):
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    result = subprocess.run(["git", *map(str, args)], cwd=cwd, env=env,
                            capture_output=True, timeout=120)
    if result.returncode:
        raise ValueError(f"Git failed ({result.returncode}): " +
                         result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def commit_id(value):
    if not re.fullmatch(r"[0-9a-fA-F]{40}", value):
        raise ValueError("Use a full 40-character commit SHA, not a moving branch.")
    return value.lower()


def config(root):
    return json.loads((root / "docs/nature_upstream.json").read_text(encoding="utf-8"))


def check(root=ROOT):
    line = git("ls-remote", UPSTREAM, "refs/heads/main").decode("utf-8").strip()
    if not line or len(line.splitlines()) != 1:
        raise ValueError("Expected exactly one upstream main reference.")
    latest = commit_id(line.split()[0])
    return {"upstream_commit": latest,
            "scoped_import_commit": config(root)["scoped_import_commit"],
            "source_changed": False, "live_installation_changed": False,
            "note": "A matching commit does not mean all upstream files were adopted."}


def selected_skills(requested, mappings):
    unknown = sorted(set(requested) - mappings.keys())
    if unknown:
        raise ValueError("Unknown or unadopted skills: " + ", ".join(unknown))
    selected = list(dict.fromkeys(requested))
    if any(name != "nature-shared" for name in selected) and "nature-shared" not in selected:
        selected.append("nature-shared")
    return selected


def fetch_commit(cache, revision):
    git("fetch", "--no-tags", "--depth=1", UPSTREAM, revision, cwd=cache)
    actual = git("rev-parse", "FETCH_HEAD", cwd=cache).decode("ascii").strip()
    if actual != revision:
        raise ValueError("Fetched commit differs from the requested SHA.")


def snapshot(cache, revision, selected, mappings):
    files = {}
    for name in selected:
        prefix = mappings[name]
        source_path = PurePosixPath(prefix)
        if source_path.is_absolute() or ".." in source_path.parts or "\\" in prefix:
            raise ValueError("Invalid upstream skill mapping: " + name)
        listing = git("ls-tree", "-rz", "--full-tree", revision, "--", prefix, cwd=cache)
        for entry in listing.split(b"\0"):
            if not entry:
                continue
            metadata, raw_path = entry.split(b"\t", 1)
            mode, kind, _ = metadata.decode("ascii").split()
            upstream_path = raw_path.decode("utf-8")
            if mode not in {"100644", "100755"} or kind != "blob":
                raise ValueError("Links/submodules are not copied: " + upstream_path)
            relative = PurePosixPath(upstream_path).relative_to(source_path)
            if ".." in relative.parts or "\\" in upstream_path:
                raise ValueError("Unsafe upstream path: " + upstream_path)
            local_path = (PurePosixPath(name) / relative).as_posix()
            files[local_path] = git("show", f"{revision}:{upstream_path}", cwd=cache)
        if f"{name}/SKILL.md" not in files:
            raise ValueError("Mapped skill is missing at this commit: " + name)
    return files


def local_snapshot(root, selected):
    files = {}
    for name in selected:
        directory = root / "skills" / name
        if directory.is_symlink() or directory.is_junction():
            raise ValueError("Local skill directory is a link: " + name)
        for path in directory.rglob("*"):
            if path.is_symlink() or path.is_junction():
                raise ValueError("Local source contains a link: " + name)
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                files[path.relative_to(root / "skills").as_posix()] = path.read_bytes()
        if f"{name}/SKILL.md" not in files:
            raise ValueError("Local skill is missing: " + name)
    return files


def differences(local, upstream, base=None):
    rows, patch = [], []
    for path in sorted(local.keys() | upstream.keys() | (base or {}).keys()):
        left, right = local.get(path), upstream.get(path)
        original = base.get(path) if base is not None else None
        if left == right:
            status = "identical"
        elif base is None:
            status = "manual_comparison"
        elif left == original:
            status = "upstream_only"
        elif right == original:
            status = "local_only"
        else:
            status = "both_changed"
        rows.append({"path": path, "comparison": status,
                     "local_present": left is not None, "upstream_present": right is not None})
        if left == right:
            continue
        try:
            before = (left or b"").decode("utf-8-sig").splitlines(keepends=True)
            after = (right or b"").decode("utf-8-sig").splitlines(keepends=True)
        except UnicodeError:
            patch.append(f"Binary content differs: {path}\n")
        else:
            # Display only: this compares local with upstream, not an applicable merge patch.
            diff = difflib.unified_diff(before, after, fromfile="local/" + path,
                                        tofile="upstream/" + path)
            patch.extend(line if line.endswith("\n") else line + "\n" for line in diff)
    return rows, "".join(patch)


def write_snapshot(directory, files):
    for relative, content in files.items():
        destination = directory / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)


def prepare(target, revision, requested, base_revision=None, root=ROOT):
    revision = commit_id(revision)
    base_revision = commit_id(base_revision) if base_revision else None
    settings = config(root)
    selected = selected_skills(requested, settings["skills"])
    target = Path(target).absolute()
    if target.exists() or target.is_symlink():
        raise ValueError("Review directory exists; select a fresh directory.")
    resolved = target.resolve()
    source_root = root.resolve()
    if (resolved == source_root or source_root.is_relative_to(resolved) or
            resolved.is_relative_to(source_root / "skills") or
            DISCOVERY.intersection(target.parts) or DISCOVERY.intersection(resolved.parts)):
        raise ValueError("Review directory overlaps source or live skill discovery.")
    local = local_snapshot(root, selected)
    resolved.mkdir(parents=True)
    cache = resolved / "upstream_git"
    git("init", "--bare", cache)
    fetch_commit(cache, revision)
    upstream = snapshot(cache, revision, selected, settings["skills"])
    base = None
    if base_revision:
        if base_revision != revision:
            fetch_commit(cache, base_revision)
        base = snapshot(cache, base_revision, selected, settings["skills"])
    rows, patch = differences(local, upstream, base)
    write_snapshot(resolved / "local_skills", local)
    write_snapshot(resolved / "upstream_skills", upstream)
    if base is not None:
        write_snapshot(resolved / "base_skills", base)
    result = {"status": "PREPARED_FOR_REVIEW", "upstream_commit": revision,
              "base_commit": base_revision, "selected_skills": selected,
              "source_changed": False, "live_installation_changed": False,
              "automatic_merge": False, "files": rows,
              "note": "Review and merge explicitly. Missing baseline requires manual comparison; no copy is activated."}
    (resolved / "review.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (resolved / "review.diff").write_text(patch, encoding="utf-8")
    return result


def watch(root=ROOT):
    """Check once and stage a new upstream version; never change installed skills."""
    directory = root / "local_state/nature_upstream_watch"
    directory.mkdir(parents=True, exist_ok=True)
    state_path = directory / "watch_state.json"
    checked_at = datetime.now(timezone.utc).isoformat()
    try:
        settings = config(root)
        state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
        previous = commit_id(state.get("observed_commit", settings["watch_initial_commit"]))
        result = check(root)
        latest = result["upstream_commit"]
        pending = state.get("pending_review")
        if latest != previous:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            target = directory / f"review_{latest[:12]}_{stamp}"
            # A missing historical base must not become an assumed merge ancestor.
            review = prepare(target, latest, list(settings["skills"]), root=root)
            pending = {"upstream_commit": latest,
                       "directory": str(target.relative_to(root)),
                       "compared_files": len(review["files"])}
        result.update({"checked_at": checked_at,
                       "status": "UPDATE_AWAITING_REVIEW" if pending else "WAITING_FOR_UPSTREAM_UPDATE",
                       "pending_review": pending, "automatic_install": False})
        state_path.write_text(json.dumps({"observed_commit": latest, "pending_review": pending},
                                         indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        # Keep the prior observation on failure so a later run retries the update.
        failure = {"checked_at": checked_at, "status": "CHECK_FAILED", "error": str(error),
                   "source_changed": False, "live_installation_changed": False}
        (directory / "check_result.json").write_text(json.dumps(failure, indent=2) + "\n",
                                                     encoding="utf-8")
        raise
    (directory / "check_result.json").write_text(json.dumps(result, indent=2) + "\n",
                                                 encoding="utf-8")
    return result


def next_check(now):
    scheduled = now.replace(hour=9, minute=0, second=0, microsecond=0)
    scheduled += timedelta(days=(-now.weekday()) % 7)
    return scheduled if scheduled > now else scheduled + timedelta(weeks=1)


def check_due(now, checked_at):
    return checked_at is None or datetime.fromisoformat(checked_at) < next_check(now) - timedelta(weeks=1)


def wait_until(scheduled):
    # Recheck wall time so sleep/resume or a clock change cannot postpone a due check.
    while True:
        remaining = (scheduled - datetime.now().astimezone()).total_seconds()
        if remaining <= 0:
            return
        time.sleep(min(60, remaining))


def monitor(root=ROOT):
    """User-login background monitor for hosts that cannot register scheduled tasks."""
    directory = root / "local_state/nature_upstream_watch"
    directory.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=directory / "monitor.log", encoding="utf-8", level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    while True:
        previous_report = directory / "check_result.json"
        checked_at = json.loads(previous_report.read_text(encoding="utf-8"))["checked_at"] \
            if previous_report.exists() else None
        if check_due(datetime.now().astimezone(), checked_at):
            try:
                result = watch(root)
                logging.info("%s %s", result["status"], result["upstream_commit"])
            except (OSError, ValueError, KeyError, subprocess.TimeoutExpired):
                logging.exception("Upstream check failed; see check_result.json. Next attempt is next Monday.")
        now = datetime.now().astimezone()
        scheduled = next_check(now)
        (directory / "monitor_status.json").write_text(json.dumps(
            {"process_id": os.getpid(), "next_check": scheduled.isoformat(),
             "schedule": "Monday 09:00 local time, weekly",
             "automatic_install": False}, indent=2) + "\n", encoding="utf-8")
        wait_until(scheduled)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="Read upstream main; do not write anything")
    commands.add_parser("watch", help="Check once; save local status and stage changed upstream for review")
    commands.add_parser("monitor", help="Check weekly on Monday at 09:00; catch up on login, never install")
    staging = commands.add_parser("prepare", help="Save original versions and a review diff; never install")
    staging.add_argument("--commit", required=True)
    staging.add_argument("--target", required=True, type=Path)
    staging.add_argument("--skill", action="append", required=True)
    staging.add_argument("--base", help="Verified pristine upstream commit; not a harness snapshot")
    args = parser.parse_args()
    try:
        if args.command == "check":
            result = check()
        elif args.command == "watch":
            result = watch()
        elif args.command == "monitor":
            monitor()
            return
        else:
            result = prepare(args.target, args.commit, args.skill, args.base)
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        parser.exit(2, str(error) + "\n")
    summary = {key: value for key, value in result.items() if key != "files"}
    if "files" in result:
        summary["compared_files"] = len(result["files"])
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
