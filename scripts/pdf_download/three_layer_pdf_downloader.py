#!/usr/bin/env python
"""Audited batch PDF downloader with authorized-browser handoff.

The automatic lane only uses direct/official open-access candidates and the
installed paper-fetch CLI.  Items that still need an institutional login or a
publisher verification step are written to a resumable manual portal.  This
module never attempts to solve or bypass CAPTCHA, Turnstile, reCAPTCHA, or
Cloudflare challenges.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote, urlencode

import requests

try:
    import fitz  # PyMuPDF
except Exception:  # pragma: no cover - exercised through the explicit failure result
    fitz = None


PDF_MAGIC = b"%PDF-"
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
DEFAULT_MIN_BYTES = 20 * 1024
DEFAULT_MIN_PAGES = 1
DEFAULT_TITLE_THRESHOLD = 0.35
DEFAULT_MAX_PDF_BYTES = 200 * 1024 * 1024
DEFAULT_WORKERS = 4
DEFAULT_PAPER_FETCH_CONCURRENCY = 4
USER_AGENT = "three-layer-pdf-downloader/2.0 (official-OA-authorized-browser)"
TITLE_STOPWORDS = {
    "with", "from", "using", "based", "between", "model", "models", "deep",
    "learning", "machine", "study", "case", "data", "analysis", "method",
    "methods", "results", "towards", "through", "under", "over", "into",
}


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def run_tag() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def normalize_doi(value: str) -> str:
    text = str(value or "").strip()
    text = re.sub(r"^doi\s*:\s*", "", text, flags=re.I)
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text, flags=re.I)
    match = DOI_RE.search(text)
    if match:
        text = match.group(0)
    return text.strip().rstrip(".,;").lower()


def normalized_field(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(name or "").lower())


def pick(row: dict[str, Any], *names: str) -> str:
    wanted = {normalized_field(name) for name in names}
    for key, value in row.items():
        if normalized_field(key) in wanted and value is not None:
            text = str(value).strip()
            if text:
                return text
    return ""


def row_key(row: dict[str, str]) -> str:
    if row.get("doi"):
        return f"doi:{row['doi']}"
    return "title:" + re.sub(r"\s+", " ", row.get("title", "").strip().lower())


def safe_stem(value: str, fallback: str = "paper") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", str(value or "")).strip("._-")
    return (cleaned[:140] or fallback).rstrip(".")


def expected_filename(row: dict[str, str]) -> str:
    if row.get("doi"):
        return safe_stem(row["doi"].replace("/", "_")) + ".pdf"
    digest = hashlib.sha256(row.get("title", "").encode("utf-8")).hexdigest()[:12]
    return f"title_{digest}_{safe_stem(row.get('title', ''), 'paper')[:70]}.pdf"


def canonicalize_row(raw: dict[str, Any], index: int) -> dict[str, str]:
    doi = normalize_doi(pick(raw, "DOI", "doi_norm", "identifier"))
    title = pick(raw, "Article Title", "title", "paper_title")
    row = {
        "id": pick(raw, "id", "paper_id", "record_id") or str(index),
        "doi": doi,
        "title": title,
        "source": pick(raw, "Source Title", "source", "journal", "venue"),
        "year": pick(raw, "Publication Year", "year"),
        "publisher": pick(raw, "Publisher", "publisher"),
        "pdf_url": pick(raw, "PDF URL", "pdf_url", "url_for_pdf"),
        "landing_url": pick(raw, "URL", "landing_url", "source_url"),
    }
    row["expected_filename"] = expected_filename(row)
    return row


def load_rows(path: Path, limit: int | None = None) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    if not path.exists():
        raise FileNotFoundError(f"Input CSV not found: {path}")
    rows: list[dict[str, str]] = []
    rejected: list[dict[str, Any]] = []
    seen: set[str] = set()
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"Input CSV has no header: {path}")
        for index, raw in enumerate(reader, 1):
            row = canonicalize_row(dict(raw), index)
            if not row["doi"] and not row["title"]:
                rejected.append({**row, "status": "invalid_input", "reason": "missing_doi_and_title"})
                continue
            key = row_key(row)
            if key in seen:
                rejected.append({**row, "status": "duplicate_skipped", "reason": "duplicate_identifier"})
                continue
            seen.add(key)
            rows.append(row)
            if limit and len(rows) >= limit:
                break
    return rows, rejected


def title_tokens(text: str) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9]{4,}", str(text or "").lower()))
    return {token for token in tokens if token not in TITLE_STOPWORDS}


def title_score(title: str, pdf_text: str) -> float:
    wanted = title_tokens(title)
    if not wanted:
        return 0.0
    found = title_tokens(pdf_text[:12000])
    return len(wanted & found) / max(1, len(wanted))


def inspect_pdf(path: Path, max_pages: int = 5) -> dict[str, Any]:
    info: dict[str, Any] = {
        "candidate_pdf": str(path),
        "size_bytes": 0,
        "magic_ok": False,
        "page_count": -1,
        "text": "",
        "inspect_error": "",
    }
    try:
        info["size_bytes"] = path.stat().st_size
        with path.open("rb") as handle:
            info["magic_ok"] = handle.read(5) == PDF_MAGIC
    except Exception as exc:
        info["inspect_error"] = f"read_error:{exc}"
        return info
    if not info["magic_ok"]:
        info["inspect_error"] = "not_pdf_magic"
        return info
    if fitz is None:
        info["inspect_error"] = "pdf_parser_unavailable"
        return info
    try:
        document = fitz.open(str(path))
        try:
            info["page_count"] = document.page_count
            chunks = []
            for page_index in range(min(max_pages, document.page_count)):
                try:
                    chunks.append(document.load_page(page_index).get_text("text") or "")
                except Exception:
                    pass
            info["text"] = "\n".join(chunks)
        finally:
            document.close()
    except Exception as exc:
        info["inspect_error"] = f"pdf_parse_error:{exc}"
    return info


def validate_inspection(
    inspection: dict[str, Any],
    row: dict[str, str],
    min_bytes: int = DEFAULT_MIN_BYTES,
    min_pages: int = DEFAULT_MIN_PAGES,
    threshold: float = DEFAULT_TITLE_THRESHOLD,
) -> dict[str, Any]:
    result = {
        "valid": False,
        "reason": "",
        "candidate_pdf": inspection.get("candidate_pdf", ""),
        "size_bytes": inspection.get("size_bytes", 0),
        "page_count": inspection.get("page_count", -1),
        "doi_match": False,
        "title_score": 0.0,
    }
    if inspection.get("inspect_error"):
        result["reason"] = inspection["inspect_error"]
        return result
    if int(inspection.get("size_bytes") or 0) < min_bytes:
        result["reason"] = "too_small"
        return result
    if int(inspection.get("page_count") or -1) < min_pages:
        result["reason"] = "too_few_pages"
        return result
    text = str(inspection.get("text") or "")
    compact_text = re.sub(r"\s+", "", text.lower())
    doi = normalize_doi(row.get("doi", ""))
    doi_match = bool(doi and re.sub(r"\s+", "", doi) in compact_text)
    score = title_score(row.get("title", ""), text)
    result["doi_match"] = doi_match
    result["title_score"] = round(score, 4)
    if not doi_match and score < threshold:
        result["reason"] = "doi_title_mismatch"
        return result
    result["valid"] = True
    result["reason"] = "accepted"
    return result


def validate_pdf(
    path: Path,
    row: dict[str, str],
    min_bytes: int = DEFAULT_MIN_BYTES,
    min_pages: int = DEFAULT_MIN_PAGES,
    threshold: float = DEFAULT_TITLE_THRESHOLD,
) -> dict[str, Any]:
    return validate_inspection(inspect_pdf(path), row, min_bytes, min_pages, threshold)


def unique_target(output_dir: Path, row: dict[str, str]) -> Path:
    target = output_dir / row["expected_filename"]
    if not target.exists():
        return target
    suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
    return target.with_name(f"{target.stem}.validated_{suffix}{target.suffix}")


def commit_candidate(candidate: Path, output_dir: Path, row: dict[str, str]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    target = unique_target(output_dir, row)
    partial = output_dir / f".{target.name}.{os.getpid()}.partial"
    shutil.copy2(candidate, partial)
    os.replace(partial, target)
    return target


def existing_result(
    output_dir: Path,
    row: dict[str, str],
    min_bytes: int,
    min_pages: int,
    threshold: float,
) -> dict[str, Any] | None:
    target = output_dir / row["expected_filename"]
    if not target.exists():
        return None
    validation = validate_pdf(target, row, min_bytes, min_pages, threshold)
    if validation["valid"]:
        return {
            **row,
            "status": "already_exists",
            "reason": "validated_existing_pdf",
            "accepted_pdf": str(target),
            "validation": validation,
            "layer": "existing",
        }
    return None


def candidate_urls(
    row: dict[str, str],
    session: requests.Session,
    include_metadata_lookups: bool = True,
) -> tuple[list[tuple[str, str]], list[str]]:
    candidates: list[tuple[str, str]] = []
    diagnostics: list[str] = []
    if row.get("pdf_url"):
        candidates.append(("input_pdf_url", row["pdf_url"]))
    doi = row.get("doi", "")
    if not doi:
        return candidates, diagnostics

    arxiv_match = re.match(r"10\.48550/arxiv\.(.+)", doi, flags=re.I)
    if arxiv_match:
        arxiv_id = arxiv_match.group(1)
        candidates.append(("arxiv_official", f"https://arxiv.org/pdf/{quote(arxiv_id, safe='/.')}.pdf"))

    if not include_metadata_lookups:
        return candidates, diagnostics

    openalex_url = "https://api.openalex.org/works/" + quote(f"https://doi.org/{doi}", safe="")
    try:
        response = session.get(openalex_url, timeout=(10, 20))
        if response.status_code == 200:
            payload = response.json()
            locations = [payload.get("best_oa_location"), payload.get("primary_location")]
            locations.extend(payload.get("locations") or [])
            for location in locations:
                if isinstance(location, dict) and location.get("pdf_url"):
                    candidates.append(("openalex_oa", str(location["pdf_url"])))
        else:
            diagnostics.append(f"openalex_http_{response.status_code}")
    except Exception as exc:
        diagnostics.append(f"openalex_error:{type(exc).__name__}")

    email = os.environ.get("UNPAYWALL_EMAIL") or os.environ.get("CROSSREF_MAILTO") or ""
    if "@" in email:
        try:
            response = session.get(
                f"https://api.unpaywall.org/v2/{quote(doi, safe='')}?{urlencode({'email': email})}",
                timeout=(10, 20),
            )
            if response.status_code == 200:
                payload = response.json()
                locations = [payload.get("best_oa_location")]
                locations.extend(payload.get("oa_locations") or [])
                for location in locations:
                    if isinstance(location, dict) and location.get("url_for_pdf"):
                        candidates.append(("unpaywall_oa", str(location["url_for_pdf"])))
            else:
                diagnostics.append(f"unpaywall_http_{response.status_code}")
        except Exception as exc:
            diagnostics.append(f"unpaywall_error:{type(exc).__name__}")

    candidates.append(("doi_content_negotiation", f"https://doi.org/{quote(doi, safe='/')}"))
    seen: set[str] = set()
    unique: list[tuple[str, str]] = []
    for source, url in candidates:
        if not url.startswith(("https://", "http://")) or url in seen:
            continue
        seen.add(url)
        unique.append((source, url))
    return unique, diagnostics


def download_url(
    session: requests.Session,
    source: str,
    url: str,
    stage_path: Path,
    row: dict[str, str],
    min_bytes: int,
    min_pages: int,
    threshold: float,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    attempt: dict[str, Any] = {"source": source, "url": url, "ok": False, "reason": "", "tries": []}
    stage_path.parent.mkdir(parents=True, exist_ok=True)
    retryable_statuses = {408, 425, 429, 500, 502, 503, 504}
    for try_number in (1, 2):
        try:
            with session.get(
                url,
                headers={"Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.2"},
                stream=True,
                allow_redirects=True,
                timeout=(10, timeout_seconds),
            ) as response:
                attempt["http_status"] = response.status_code
                attempt["final_url"] = response.url
                attempt["content_type"] = response.headers.get("content-type", "")
                attempt["tries"].append({"try": try_number, "http_status": response.status_code})
                if response.status_code != 200:
                    attempt["reason"] = f"http_{response.status_code}"
                    if response.status_code in retryable_statuses and try_number == 1:
                        time.sleep(1)
                        continue
                    return attempt
                total = 0
                with stage_path.open("wb") as handle:
                    for chunk in response.iter_content(chunk_size=128 * 1024):
                        if not chunk:
                            continue
                        total += len(chunk)
                        if total > DEFAULT_MAX_PDF_BYTES:
                            raise ValueError("candidate_exceeds_max_pdf_bytes")
                        handle.write(chunk)
            validation = validate_pdf(stage_path, row, min_bytes, min_pages, threshold)
            attempt["validation"] = validation
            attempt["ok"] = bool(validation["valid"])
            attempt["reason"] = validation["reason"]
            return attempt
        except requests.RequestException as exc:
            attempt["tries"].append({"try": try_number, "error": f"{type(exc).__name__}:{exc}"})
            attempt["reason"] = f"download_error:{type(exc).__name__}:{exc}"
            if try_number == 1:
                time.sleep(1)
                continue
            return attempt
        except Exception as exc:
            attempt["tries"].append({"try": try_number, "error": f"{type(exc).__name__}:{exc}"})
            attempt["reason"] = f"download_error:{type(exc).__name__}:{exc}"
            return attempt
    return attempt


def try_official_row(
    row: dict[str, str],
    output_dir: Path,
    run_dir: Path,
    min_bytes: int,
    min_pages: int,
    threshold: float,
) -> dict[str, Any]:
    existing = existing_result(output_dir, row, min_bytes, min_pages, threshold)
    if existing:
        return existing
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    urls, diagnostics = candidate_urls(row, session, include_metadata_lookups=False)
    attempts: list[dict[str, Any]] = []
    attempted_urls: set[str] = set()
    for phase in ("direct", "metadata"):
        if phase == "metadata":
            discovered, extra_diagnostics = candidate_urls(row, session, include_metadata_lookups=True)
            diagnostics.extend(extra_diagnostics)
            urls = discovered
        for source, url in urls:
            if url in attempted_urls:
                continue
            attempted_urls.add(url)
            index = len(attempts) + 1
            stage = run_dir / "official_staging" / safe_stem(row_key(row)) / f"candidate_{index}.pdf"
            attempt = download_url(session, source, url, stage, row, min_bytes, min_pages, threshold)
            attempts.append(attempt)
            if attempt["ok"]:
                target = commit_candidate(stage, output_dir, row)
                try:
                    stage.unlink(missing_ok=True)
                except OSError:
                    pass
                return {
                    **row,
                    "status": "accepted",
                    "reason": "official_or_oa_pdf_validated",
                    "accepted_pdf": str(target),
                    "layer": "official_oa",
                    "source_used": source,
                    "attempts": attempts,
                    "diagnostics": diagnostics,
                }
            try:
                stage.unlink(missing_ok=True)
            except OSError:
                pass
    return {
        **row,
        "status": "automatic_pending",
        "reason": "official_oa_exhausted",
        "layer": "official_oa",
        "attempts": attempts,
        "diagnostics": diagnostics,
    }


def paper_fetch_batch(
    rows: list[dict[str, str]],
    results_by_key: dict[str, dict[str, Any]],
    output_dir: Path,
    run_dir: Path,
    timeout_seconds: int,
    concurrency: int,
    min_bytes: int,
    min_pages: int,
    threshold: float,
) -> dict[str, Any]:
    pending = [row for row in rows if results_by_key[row_key(row)]["status"] == "automatic_pending"]
    diagnostics: dict[str, Any] = {"attempted": len(pending), "command_available": False, "pdf_candidates": 0}
    if not pending:
        return diagnostics
    executable = shutil.which("paper-fetch")
    if not executable:
        diagnostics["reason"] = "paper_fetch_cli_missing"
        return diagnostics
    diagnostics["command_available"] = True
    stage = run_dir / "paper_fetch"
    stage.mkdir(parents=True, exist_ok=True)
    query_file = stage / "queries.txt"
    query_file.write_text("\n".join(row["doi"] or row["title"] for row in pending) + "\n", encoding="utf-8")
    batch_results = stage / "batch-results.jsonl"
    executable_path = Path(executable)
    command_prefix = [executable]
    child_env = os.environ.copy()
    if executable_path.suffix.lower() in {".cmd", ".bat"}:
        install_root = executable_path.parent.parent
        runtime_python = install_root / "runtime" / "python.exe"
        if runtime_python.is_file():
            command_prefix = [str(runtime_python), "-X", "utf8", "-m", "paper_fetch.cli"]
            child_env.setdefault("PAPER_FETCH_ENV_FILE", str(install_root / "offline.env"))
            child_env.setdefault("PYTHONUTF8", "1")
            child_env.setdefault("PYTHONIOENCODING", "utf-8")
    command = [
        *command_prefix,
        "--query-file", str(query_file),
        "--output-dir", str(stage),
        "--batch-results", str(batch_results),
        "--batch-concurrency", str(max(1, min(8, concurrency))),
        "--format", "json",
        "--artifact-mode", "all",
        "--asset-profile", "none",
        "--max-tokens", "1",
    ]
    diagnostics["command"] = command
    try:
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=max(timeout_seconds, timeout_seconds * min(4, len(pending))),
            env=child_env,
        )
        diagnostics["returncode"] = proc.returncode
        diagnostics["stderr_tail"] = proc.stderr[-2000:]
    except subprocess.TimeoutExpired as exc:
        diagnostics["returncode"] = "timeout"
        diagnostics["stderr_tail"] = ((exc.stderr or "") if isinstance(exc.stderr, str) else "")[-2000:]
    except Exception as exc:
        diagnostics["returncode"] = "exception"
        diagnostics["stderr_tail"] = repr(exc)

    candidates = sorted(stage.rglob("*.pdf"))
    diagnostics["pdf_candidates"] = len(candidates)
    unused_rows = {row_key(row): row for row in pending}
    for candidate in candidates:
        inspection = inspect_pdf(candidate)
        best: tuple[float, str, dict[str, Any]] | None = None
        for key, row in unused_rows.items():
            validation = validate_inspection(inspection, row, min_bytes, min_pages, threshold)
            if not validation["valid"]:
                continue
            score = (2.0 if validation["doi_match"] else 0.0) + float(validation["title_score"])
            if best is None or score > best[0]:
                best = (score, key, validation)
        if best is None:
            continue
        _, key, validation = best
        row = unused_rows.pop(key)
        target = commit_candidate(candidate, output_dir, row)
        results_by_key[key] = {
            **row,
            "status": "accepted",
            "reason": "paper_fetch_pdf_artifact_validated",
            "accepted_pdf": str(target),
            "layer": "paper_fetch",
            "validation": validation,
        }
    return diagnostics


def load_institution_config() -> dict[str, Any]:
    config_dir = os.environ.get("LIT_DL_CONFIG_DIR")
    path = Path(config_dir) / "school.json" if config_dir else Path.home() / ".config" / "lit-dl" / "school.json"
    if not path.exists():
        return {"path": str(path), "configured": False, "entry_urls": []}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"path": str(path), "configured": False, "entry_urls": [], "warning": f"invalid_config:{exc}"}
    urls: list[tuple[str, str]] = []
    discovery = payload.get("discovery") if isinstance(payload, dict) else {}
    auth = payload.get("auth") if isinstance(payload, dict) else {}
    proxy = payload.get("proxy") if isinstance(payload, dict) else {}
    for label, value in [
        ("Library resource entry", (discovery or {}).get("resource_entry_url")),
        ("Library resource portal", (discovery or {}).get("resource_portal_url")),
        ("Web of Science entry", (discovery or {}).get("web_of_science_url")),
        ("CARSI entry", (auth or {}).get("carsi_entry")),
        ("EZproxy entry", (proxy or {}).get("ezproxy_url")),
    ]:
        if isinstance(value, str) and value.startswith(("https://", "http://")):
            urls.append((label, value))
    deduped = list(dict.fromkeys(urls))
    school = payload.get("school") if isinstance(payload, dict) else {}
    return {
        "path": str(path),
        "configured": True,
        "school_name": (school or {}).get("name", ""),
        "entry_urls": deduped,
    }


def publisher_links(row: dict[str, str]) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    if row.get("doi"):
        links.append(("DOI / publisher", f"https://doi.org/{quote(row['doi'], safe='/')}"))
    if row.get("landing_url", "").startswith(("https://", "http://")):
        links.append(("Input landing page", row["landing_url"]))
    query = row.get("doi") or row.get("title")
    if query:
        links.append(("Crossref search", f"https://search.crossref.org/?{urlencode({'q': query})}"))
        links.append(("Google Scholar", f"https://scholar.google.com/scholar?{urlencode({'q': query})}"))
    return links


def build_portal(
    rows: list[dict[str, str]],
    reasons: dict[str, str],
    work_dir: Path,
    download_dir: Path,
) -> dict[str, Any]:
    manual_dir = work_dir / "manual_handoff"
    manual_dir.mkdir(parents=True, exist_ok=True)
    download_dir.mkdir(parents=True, exist_ok=True)
    config = load_institution_config()
    queue: list[dict[str, Any]] = []
    for row in rows:
        queue.append({
            **row,
            "status": "waiting_user",
            "handoff_reason": reasons.get(row_key(row), "automatic_layers_exhausted"),
            "next_action": "complete_login_or_verification_in_shared_browser_tab_then_save_pdf",
            "links": [{"label": label, "url": url} for label, url in publisher_links(row)],
        })
    queue_csv = manual_dir / "manual_download_queue.csv"
    fields = [
        "id", "doi", "title", "source", "year", "publisher", "expected_filename",
        "status", "handoff_reason", "next_action",
    ]
    with queue_csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(queue)
    queue_json = manual_dir / "manual_download_queue.json"
    queue_json.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")

    institution_buttons = "".join(
        f'<button class="institution" data-url="{html.escape(url, quote=True)}">{html.escape(label)}</button>'
        for label, url in config.get("entry_urls", [])
    ) or "<span class=\"muted\">No institution profile configured; DOI links will still reuse your normal browser session.</span>"
    embedded = json.dumps(queue, ensure_ascii=False).replace("</", "<\\/")
    portal = manual_dir / "manual_download_portal.html"
    portal.write_text(
        """<!doctype html><html><head><meta charset="utf-8"><title>Authorized PDF handoff</title>
<style>
body{font-family:Arial,sans-serif;margin:22px;color:#202124}button{margin:4px;padding:7px 10px}code{background:#f5f5f5;padding:2px 4px}.muted{color:#666}.card{border:1px solid #ddd;border-radius:8px;padding:14px;margin:12px 0}.done{opacity:.55}.title{font-weight:650}.links a{margin-right:12px}.status{font-size:12px;color:#555}
</style></head><body>
<h1>Authorized PDF handoff</h1>
<p>Automatic OA/official retrieval has finished. Use the same named browser tab for institution login or publisher verification, save real PDFs to <code>"""
        + html.escape(str(download_dir))
        + """</code>, then run <code>three-layer-receive</code>. CAPTCHA, Cloudflare, Turnstile, reCAPTCHA, QR, OTP, and sliders must be completed manually; this portal does not bypass them.</p>
<div><strong>Institution entry:</strong> """ + institution_buttons + """</div>
<p><button id="open-next">Open next pending paper in shared tab</button><button id="reset">Reset local marks</button> <span id="count" class="status"></span></p>
<div id="queue"></div>
<script>
const papers=""" + embedded + """;
const storageKey='three-layer-pdf-handoff-v1';
let marks=JSON.parse(localStorage.getItem(storageKey)||'{}');
const sharedName='authorized_paper_session';
function esc(value){return String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function safeUrl(value){try{const u=new URL(value);return ['http:','https:'].includes(u.protocol)?u.href:'#';}catch{return '#';}}
function save(){localStorage.setItem(storageKey,JSON.stringify(marks));render();}
function openUrl(url){window.open(url,sharedName);}
function render(){
 const root=document.getElementById('queue'); root.innerHTML='';
 let done=0;
 papers.forEach((p,i)=>{
  const card=document.createElement('div'); card.className='card '+(marks[p.id]?'done':'');
  const links=(p.links||[]).map(x=>`<a href="${esc(safeUrl(x.url))}" target="${sharedName}">${esc(x.label)}</a>`).join('');
  card.innerHTML=`<div class="title">${i+1}. ${esc(p.title||p.doi)}</div><div><code>${esc(p.doi||'title-only')}</code></div><div class="links">${links}</div><div class="status">${esc(p.handoff_reason)} | expected: ${esc(p.expected_filename)}</div>`;
  const b=document.createElement('button'); b.textContent=marks[p.id]?'Mark pending':'Mark handled'; b.onclick=()=>{marks[p.id]=!marks[p.id];save();}; card.appendChild(b);
  root.appendChild(card); if(marks[p.id])done++;
 });
 document.getElementById('count').textContent=`${done}/${papers.length} locally marked handled`;
}
document.querySelectorAll('button.institution').forEach(b=>b.onclick=()=>openUrl(b.dataset.url));
document.getElementById('open-next').onclick=()=>{const p=papers.find(x=>!marks[x.id]); if(p&&p.links&&p.links.length)openUrl(p.links[0].url);};
document.getElementById('reset').onclick=()=>{marks={};save();}; render();
</script></body></html>""",
        encoding="utf-8",
    )
    manifest = {
        "created_at": now_iso(),
        "status": "waiting_user" if queue else "empty",
        "rows": len(queue),
        "portal_html": str(portal),
        "queue_csv": str(queue_csv),
        "queue_json": str(queue_json),
        "download_dir": str(download_dir),
        "institution_config": config,
        "shared_browser_target": "authorized_paper_session",
        "automatic_challenge_solving": False,
    }
    (manual_dir / "manual_handoff_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return manifest


def handoff_reason(paper_fetch_diagnostics: dict[str, Any]) -> str:
    text = str(paper_fetch_diagnostics.get("stderr_tail") or "").lower()
    if any(term in text for term in ("captcha", "turnstile", "recaptcha", "cloudflare", "challenge", "verification")):
        return "publisher_verification_waiting_user"
    if any(term in text for term in ("no_access", "login", "institution", "carsi", "sso", "shibboleth")):
        return "institution_login_waiting_user"
    return "automatic_layers_exhausted"


def write_run_artifacts(run_dir: Path, payload: dict[str, Any]) -> Path:
    run_dir.mkdir(parents=True, exist_ok=True)
    results_json = run_dir / "download_results.json"
    results_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = run_dir / "status_manifest.jsonl"
    with manifest.open("w", encoding="utf-8") as handle:
        for result in payload.get("results", []):
            handle.write(json.dumps(result, ensure_ascii=False) + "\n")
    counts = Counter(str(result.get("status", "unknown")) for result in payload.get("results", []))
    summary = run_dir / "DOWNLOAD_SUMMARY.md"
    lines = [
        "# Three-layer PDF download summary",
        "",
        f"- Created: `{payload.get('created_at')}`",
        f"- Operation: `{payload.get('operation')}`",
        f"- Success: `{payload.get('success')}`",
        f"- Status counts: `{dict(counts)}`",
        f"- Accepted count: `{payload.get('accepted_count', 0)}`",
        f"- Waiting-user count: `{payload.get('waiting_user_count', 0)}`",
        f"- Automatic challenge solving: `false`",
        f"- Results JSON: `{results_json}`",
        f"- Status manifest: `{manifest}`",
    ]
    portal = payload.get("manual_portal") or {}
    if portal.get("portal_html"):
        lines.append(f"- Manual authorized-browser portal: `{portal['portal_html']}`")
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def finish_payload(
    operation: str,
    run_dir: Path,
    results: list[dict[str, Any]],
    success: bool,
    **extra: Any,
) -> Path:
    counts = Counter(str(result.get("status", "unknown")) for result in results)
    payload = {
        "created_at": now_iso(),
        "operation": operation,
        "success": success,
        "run_ok": True,
        "results": results,
        "accepted_count": counts.get("accepted", 0) + counts.get("already_exists", 0),
        "waiting_user_count": counts.get("waiting_user", 0),
        "status_counts": dict(counts),
        "raw_scansci_fallback": "disabled_by_default",
        "automatic_challenge_solving": False,
        **extra,
    }
    return write_run_artifacts(run_dir, payload)


def run_download(
    rows: list[dict[str, str]],
    rejected: list[dict[str, Any]],
    output_dir: Path,
    work_dir: Path,
    dry_run: bool,
    skip_official: bool,
    skip_paper_fetch: bool,
    no_build_portal: bool,
    paper_fetch_timeout_seconds: int,
    workers: int,
    paper_fetch_concurrency: int,
    min_bytes: int,
    min_pages: int,
    threshold: float,
    operation: str,
) -> Path:
    current_run = work_dir / "runs" / run_tag()
    output_dir.mkdir(parents=True, exist_ok=True)
    results_by_key: dict[str, dict[str, Any]] = {}
    for row in rows:
        existing = existing_result(output_dir, row, min_bytes, min_pages, threshold)
        if existing:
            results_by_key[row_key(row)] = existing
        else:
            results_by_key[row_key(row)] = {**row, "status": "planned" if dry_run else "automatic_pending", "reason": "not_started"}

    if dry_run:
        results = list(results_by_key.values()) + rejected
        portal = None
        if not no_build_portal:
            planned = [row for row in rows if results_by_key[row_key(row)]["status"] == "planned"]
            portal = build_portal(planned, {row_key(row): "dry_run_planned" for row in planned}, work_dir, work_dir / "browser_downloads")
        return finish_payload(operation, current_run, results, True, dry_run=True, manual_portal=portal)

    if not skip_official:
        pending = [row for row in rows if results_by_key[row_key(row)]["status"] == "automatic_pending"]
        with ThreadPoolExecutor(max_workers=max(1, min(8, workers))) as executor:
            futures = {
                executor.submit(
                    try_official_row, row, output_dir, current_run, min_bytes, min_pages, threshold
                ): row
                for row in pending
            }
            for future in as_completed(futures):
                row = futures[future]
                try:
                    results_by_key[row_key(row)] = future.result()
                except Exception as exc:  # pragma: no cover - defensive isolation per paper
                    results_by_key[row_key(row)] = {
                        **row,
                        "status": "automatic_pending",
                        "reason": f"official_layer_exception:{type(exc).__name__}:{exc}",
                    }

    paper_fetch_diagnostics: dict[str, Any] = {"attempted": 0, "skipped": bool(skip_paper_fetch)}
    if not skip_paper_fetch:
        paper_fetch_diagnostics = paper_fetch_batch(
            rows,
            results_by_key,
            output_dir,
            current_run,
            paper_fetch_timeout_seconds,
            paper_fetch_concurrency,
            min_bytes,
            min_pages,
            threshold,
        )

    reason = handoff_reason(paper_fetch_diagnostics)
    waiting_rows: list[dict[str, str]] = []
    reasons: dict[str, str] = {}
    for row in rows:
        key = row_key(row)
        if results_by_key[key]["status"] == "automatic_pending":
            previous = results_by_key[key]
            results_by_key[key] = {
                **previous,
                **row,
                "status": "waiting_user",
                "reason": reason,
                "next_action": "use_authorized_browser_portal_then_three_layer_receive",
            }
            waiting_rows.append(row)
            reasons[key] = reason

    portal = None
    if waiting_rows and not no_build_portal:
        portal = build_portal(waiting_rows, reasons, work_dir, work_dir / "browser_downloads")
    results = [results_by_key[row_key(row)] for row in rows] + rejected
    success = any(result.get("status") in {"accepted", "already_exists"} for result in results)
    return finish_payload(
        operation,
        current_run,
        results,
        success,
        dry_run=False,
        manual_portal=portal,
        paper_fetch=paper_fetch_diagnostics,
    )


def receive_downloads(args: argparse.Namespace) -> Path:
    input_path = Path(args.input)
    rows, rejected = load_rows(input_path)
    output_dir = Path(args.out_dir)
    work_dir = Path(args.work_dir)
    download_dir = Path(args.download_dir)
    current_run = work_dir / "runs" / run_tag()
    candidates = sorted(download_dir.rglob("*.pdf")) if download_dir.exists() else []
    available = {row_key(row): row for row in rows}
    results: list[dict[str, Any]] = []
    for candidate in candidates:
        inspection = inspect_pdf(candidate)
        best: tuple[float, str, dict[str, Any]] | None = None
        for key, row in available.items():
            validation = validate_inspection(
                inspection, row, args.min_bytes, args.min_pages, args.title_threshold
            )
            if not validation["valid"]:
                continue
            score = (2.0 if validation["doi_match"] else 0.0) + float(validation["title_score"])
            if best is None or score > best[0]:
                best = (score, key, validation)
        if best is None:
            results.append({
                "source_pdf": str(candidate),
                "status": "no_match",
                "reason": inspection.get("inspect_error") or "no_doi_or_title_match",
            })
            continue
        _, key, validation = best
        row = available.pop(key)
        existing = existing_result(output_dir, row, args.min_bytes, args.min_pages, args.title_threshold)
        if existing:
            results.append({**existing, "source_pdf": str(candidate)})
        elif args.commit:
            target = commit_candidate(candidate, output_dir, row)
            results.append({
                **row,
                "source_pdf": str(candidate),
                "accepted_pdf": str(target),
                "status": "accepted",
                "reason": "manual_authorized_pdf_validated",
                "layer": "manual_receiver",
                "validation": validation,
            })
        else:
            results.append({
                **row,
                "source_pdf": str(candidate),
                "status": "dry_run_match",
                "reason": "manual_pdf_validated_commit_required",
                "layer": "manual_receiver",
                "validation": validation,
            })
    for row in available.values():
        results.append({**row, "status": "waiting_user", "reason": "no_matching_pdf_in_download_dir"})
    results.extend(rejected)
    if args.commit:
        success = any(result.get("status") in {"accepted", "already_exists"} for result in results)
    else:
        success = True
    return finish_payload(
        "receive",
        current_run,
        results,
        success,
        commit=bool(args.commit),
        download_dir=str(download_dir),
    )


def add_validation_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--min-bytes", type=int, default=DEFAULT_MIN_BYTES)
    parser.add_argument("--min-pages", type=int, default=DEFAULT_MIN_PAGES)
    parser.add_argument("--title-threshold", type=float, default=DEFAULT_TITLE_THRESHOLD)


def add_download_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--work-dir", required=True)
    parser.add_argument("--paper-fetch-timeout-seconds", type=int, default=180)
    parser.add_argument("--scansci-timeout-seconds", type=int, default=90, help="Compatibility option; raw scansci fallback is disabled by default.")
    parser.add_argument("--skip-official", action="store_true")
    parser.add_argument("--skip-paper-fetch", action="store_true")
    parser.add_argument("--skip-scansci", action="store_true", help="Compatibility option; raw scansci fallback is already disabled.")
    parser.add_argument("--no-build-portal", action="store_true")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--paper-fetch-concurrency", type=int, default=DEFAULT_PAPER_FETCH_CONCURRENCY)
    add_validation_args(parser)


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download validated academic PDFs through official/OA, paper-fetch, and authorized-browser handoff lanes."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    one = sub.add_parser("download-one", help="Download one DOI/title")
    one.add_argument("--doi", default="")
    one.add_argument("--title", default="")
    one.add_argument("--source", default="")
    one.add_argument("--year", default="")
    one.add_argument("--publisher", default="")
    add_download_args(one)

    batch = sub.add_parser("batch", help="Download a DOI/title CSV")
    batch.add_argument("--input", required=True)
    batch.add_argument("--limit", type=int, default=0)
    batch.add_argument("--dry-run", action="store_true")
    add_download_args(batch)

    portal = sub.add_parser("portal", help="Build a same-tab authorized-browser handoff portal")
    portal.add_argument("--input", required=True)
    portal.add_argument("--work-dir", required=True)
    portal.add_argument("--download-dir", required=True)

    receive = sub.add_parser("receive", help="Validate manually downloaded PDFs")
    receive.add_argument("--input", required=True)
    receive.add_argument("--download-dir", required=True)
    receive.add_argument("--out-dir", required=True)
    receive.add_argument("--work-dir", required=True)
    receive.add_argument("--commit", action="store_true")
    add_validation_args(receive)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = make_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.command == "download-one":
        row = canonicalize_row(
            {
                "DOI": args.doi,
                "Article Title": args.title,
                "Source Title": args.source,
                "Publication Year": args.year,
                "Publisher": args.publisher,
            },
            1,
        )
        rejected: list[dict[str, Any]] = []
        rows = [row]
        if not row["doi"] and not row["title"]:
            rows = []
            rejected = [{**row, "status": "invalid_input", "reason": "missing_doi_and_title"}]
        summary = run_download(
            rows,
            rejected,
            Path(args.out_dir),
            Path(args.work_dir),
            False,
            args.skip_official,
            args.skip_paper_fetch,
            args.no_build_portal,
            args.paper_fetch_timeout_seconds,
            args.workers,
            args.paper_fetch_concurrency,
            args.min_bytes,
            args.min_pages,
            args.title_threshold,
            "download-one",
        )
    elif args.command == "batch":
        rows, rejected = load_rows(Path(args.input), args.limit or None)
        summary = run_download(
            rows,
            rejected,
            Path(args.out_dir),
            Path(args.work_dir),
            args.dry_run,
            args.skip_official,
            args.skip_paper_fetch,
            args.no_build_portal,
            args.paper_fetch_timeout_seconds,
            args.workers,
            args.paper_fetch_concurrency,
            args.min_bytes,
            args.min_pages,
            args.title_threshold,
            "batch",
        )
    elif args.command == "portal":
        rows, rejected = load_rows(Path(args.input))
        work_dir = Path(args.work_dir)
        portal_manifest = build_portal(
            rows,
            {row_key(row): "manual_portal_requested" for row in rows},
            work_dir,
            Path(args.download_dir),
        )
        results = [
            {**row, "status": "waiting_user", "reason": "manual_portal_requested"}
            for row in rows
        ] + rejected
        summary = finish_payload(
            "portal", work_dir / "runs" / run_tag(), results, True, manual_portal=portal_manifest
        )
    else:
        summary = receive_downloads(args)
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
