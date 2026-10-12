"""Exercise the adopted upstream retry-zero correction without HTTP requests."""
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

FOLDER = Path(__file__).resolve().parents[1] / "skills/nature-academic-search/scripts"


class CitationRetryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("citation_format", FOLDER / "format-converter.py")
        cls.module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(FOLDER))
        try:
            spec.loader.exec_module(cls.module)
        finally:
            sys.path.remove(str(FOLDER))

    @staticmethod
    def response(content):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = content
        return response

    def test_crossref_zero_attempt_setting_downloads_once(self):
        payload = {"message": {"title": ["Test title"], "author": [],
                               "issued": {"date-parts": [[2020]]}}}
        with tempfile.TemporaryDirectory() as folder, redirect_stdout(io.StringIO()), \
                patch.object(self.module, "urlopen", return_value=self.response(json.dumps(payload).encode())) as request, \
                patch.object(self.module, "DELAY", 0):
            ok, filename = self.module.download_crossref("10.1/test", folder, "ris", retries=0)
            self.assertTrue(ok)
            self.assertTrue((Path(folder) / filename).is_file())
            request.assert_called_once()

    def test_zero_attempt_failures_are_visible_and_write_no_files(self):
        with tempfile.TemporaryDirectory() as folder, redirect_stdout(io.StringIO()), \
                patch.object(self.module, "urlopen", side_effect=OSError("fixture failure")) as request, \
                patch.object(self.module, "DELAY", 0):
            self.assertIsNone(self.module.efetch_medline("1", retries=0))
            for method, identifier in [(self.module.download_crossref, "10.1/test"),
                                       (self.module.download_arxiv, "1")]:
                ok, message = method(identifier, folder, "ris", retries=0)
                self.assertFalse(ok)
                self.assertIn("fixture failure", message)
            self.assertEqual(request.call_count, 3)
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_medline_zero_attempt_setting_reads_once(self):
        with patch.object(self.module, "urlopen", return_value=self.response(b"PMID- 1\n")) as request:
            self.assertEqual(self.module.efetch_medline("1", retries=0), "PMID- 1\n")
            request.assert_called_once()

    def test_arxiv_zero_attempt_setting_downloads_once(self):
        xml = b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Test</title><id>http://arxiv.org/abs/1</id><published>2020-01-01</published><author><name>Test Author</name></author></entry></feed>'
        with tempfile.TemporaryDirectory() as folder, redirect_stdout(io.StringIO()), \
                patch.object(self.module, "urlopen", return_value=self.response(xml)) as request, \
                patch.object(self.module, "DELAY", 0):
            ok, filename = self.module.download_arxiv("1", folder, "ris", retries=0)
            self.assertTrue(ok)
            self.assertTrue((Path(folder) / filename).is_file())
            request.assert_called_once()


if __name__ == "__main__":
    unittest.main()
