from __future__ import annotations

import argparse
import contextlib
import csv
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "pdf_download" / "three_layer_pdf_downloader.py"
SPEC = importlib.util.spec_from_file_location("three_layer_pdf_downloader", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ThreeLayerDownloaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_csv(self, rows: list[dict[str, str]]) -> Path:
        path = self.root / "papers.csv"
        fields = list(rows[0])
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def make_pdf(self, name: str, text: str) -> Path:
        if MODULE.fitz is None:
            self.skipTest("PyMuPDF is unavailable")
        path = self.root / name
        document = MODULE.fitz.open()
        for _ in range(2):
            page = document.new_page()
            page.insert_text((72, 72), text, fontsize=11)
        document.save(str(path))
        document.close()
        return path

    def test_normalize_doi(self) -> None:
        self.assertEqual(
            MODULE.normalize_doi("https://doi.org/10.1038/S41586-024-00001-2"),
            "10.1038/s41586-024-00001-2",
        )

    def test_load_rows_accepts_title_and_deduplicates_doi(self) -> None:
        path = self.write_csv([
            {"DOI": "10.1000/ABC", "Article Title": "First paper"},
            {"DOI": "https://doi.org/10.1000/abc", "Article Title": "Duplicate"},
            {"DOI": "", "Article Title": "Title only paper"},
        ])
        rows, rejected = MODULE.load_rows(path)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["doi"], "10.1000/abc")
        self.assertEqual(rows[1]["title"], "Title only paper")
        self.assertEqual(rejected[0]["status"], "duplicate_skipped")

    def test_pdf_validation_requires_identity_evidence(self) -> None:
        pdf = self.make_pdf(
            "valid.pdf",
            "A Verified Climate Attribution Study. DOI 10.1234/example.2026.1",
        )
        row = MODULE.canonicalize_row(
            {"DOI": "10.1234/example.2026.1", "Article Title": "A Verified Climate Attribution Study"},
            1,
        )
        result = MODULE.validate_pdf(pdf, row, min_bytes=100, min_pages=1, threshold=0.35)
        self.assertTrue(result["valid"])
        mismatch = MODULE.canonicalize_row(
            {"DOI": "10.9999/wrong", "Article Title": "Unrelated Ocean Economics"},
            2,
        )
        bad = MODULE.validate_pdf(pdf, mismatch, min_bytes=100, min_pages=1, threshold=0.35)
        self.assertFalse(bad["valid"])
        self.assertEqual(bad["reason"], "doi_title_mismatch")

    def test_portal_reuses_named_tab_and_does_not_auto_solve_challenges(self) -> None:
        row = MODULE.canonicalize_row(
            {"DOI": "10.1234/example", "Article Title": "Example paper"}, 1
        )
        manifest = MODULE.build_portal(
            [row],
            {MODULE.row_key(row): "publisher_verification_waiting_user"},
            self.root / "work",
            self.root / "downloads",
        )
        portal = Path(manifest["portal_html"]).read_text(encoding="utf-8")
        self.assertIn("authorized_paper_session", portal)
        self.assertIn("must be completed manually", portal)
        self.assertNotIn("simulateDrag", portal)
        self.assertFalse(manifest["automatic_challenge_solving"])

    def test_batch_dry_run_writes_bridge_contract(self) -> None:
        input_csv = self.write_csv([
            {"DOI": "10.1234/example", "Article Title": "Example paper"},
        ])
        output = self.root / "pdfs"
        work = self.root / "work"
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = MODULE.main([
                "batch", "--input", str(input_csv), "--out-dir", str(output),
                "--work-dir", str(work), "--dry-run", "--no-build-portal",
            ])
        self.assertEqual(code, 0)
        summary = Path(stdout.getvalue().strip().splitlines()[-1])
        self.assertEqual(summary.name, "DOWNLOAD_SUMMARY.md")
        payload = json.loads((summary.parent / "download_results.json").read_text(encoding="utf-8"))
        self.assertTrue(payload["success"])
        self.assertEqual(payload["results"][0]["status"], "planned")
        self.assertFalse(payload["automatic_challenge_solving"])

    def test_receiver_dry_run_then_commit(self) -> None:
        input_csv = self.write_csv([
            {"DOI": "10.1234/example.2026.1", "Article Title": "A Verified Climate Attribution Study"},
        ])
        downloads = self.root / "downloads"
        downloads.mkdir()
        source = self.make_pdf(
            "browser.pdf",
            "A Verified Climate Attribution Study. DOI 10.1234/example.2026.1",
        )
        source.replace(downloads / source.name)
        common = dict(
            input=str(input_csv),
            download_dir=str(downloads),
            out_dir=str(self.root / "pdfs"),
            work_dir=str(self.root / "work"),
            min_bytes=100,
            min_pages=1,
            title_threshold=0.35,
        )
        dry_summary = MODULE.receive_downloads(argparse.Namespace(**common, commit=False))
        dry_payload = json.loads((dry_summary.parent / "download_results.json").read_text(encoding="utf-8"))
        self.assertEqual(dry_payload["results"][0]["status"], "dry_run_match")
        commit_summary = MODULE.receive_downloads(argparse.Namespace(**common, commit=True))
        commit_payload = json.loads((commit_summary.parent / "download_results.json").read_text(encoding="utf-8"))
        self.assertEqual(commit_payload["results"][0]["status"], "accepted")
        self.assertTrue(Path(commit_payload["results"][0]["accepted_pdf"]).exists())

    def test_paper_fetch_batch_accepts_only_valid_pdf_artifact(self) -> None:
        command_file = Path.home() / "AppData" / "Local" / "PaperFetchSkill" / "bin" / "paper-fetch.cmd"
        if not command_file.exists():
            self.skipTest("paper-fetch launcher is unavailable")
        row = MODULE.canonicalize_row(
            {"DOI": "10.1234/example.2026.1", "Article Title": "A Verified Climate Attribution Study"},
            1,
        )
        results = {
            MODULE.row_key(row): {**row, "status": "automatic_pending", "reason": "official_oa_exhausted"}
        }

        def fake_run(command: list[str], **_: object) -> SimpleNamespace:
            self.assertIn("paper_fetch.cli", command)
            stage = Path(command[command.index("--output-dir") + 1])
            stage.mkdir(parents=True, exist_ok=True)
            pdf = self.make_pdf(
                "paper-fetch-source.pdf",
                "A Verified Climate Attribution Study. DOI 10.1234/example.2026.1",
            )
            MODULE.shutil.copy2(pdf, stage / "provider-source.pdf")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        with mock.patch.object(MODULE.shutil, "which", return_value=str(command_file)), mock.patch.object(
            MODULE.subprocess, "run", side_effect=fake_run
        ):
            diagnostics = MODULE.paper_fetch_batch(
                [row], results, self.root / "pdfs", self.root / "work", 30, 2, 100, 1, 0.35
            )
        self.assertTrue(diagnostics["command_available"])
        self.assertEqual(results[MODULE.row_key(row)]["status"], "accepted")
        self.assertTrue(Path(results[MODULE.row_key(row)]["accepted_pdf"]).exists())

    def test_waiting_user_preserves_automatic_attempt_evidence(self) -> None:
        row = MODULE.canonicalize_row(
            {"DOI": "10.1234/example", "Article Title": "Example paper"}, 1
        )
        failed = {
            **row,
            "status": "automatic_pending",
            "reason": "official_oa_exhausted",
            "attempts": [{"source": "doi_content_negotiation", "reason": "http_403"}],
        }
        with mock.patch.object(MODULE, "try_official_row", return_value=failed):
            summary = MODULE.run_download(
                [row], [], self.root / "pdfs", self.root / "work", False, False, True,
                True, 30, 1, 1, 100, 1, 0.35, "batch",
            )
        payload = json.loads((summary.parent / "download_results.json").read_text(encoding="utf-8"))
        result = payload["results"][0]
        self.assertEqual(result["status"], "waiting_user")
        self.assertEqual(result["attempts"][0]["reason"], "http_403")


if __name__ == "__main__":
    unittest.main()
