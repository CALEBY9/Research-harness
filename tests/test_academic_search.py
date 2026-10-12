"""Exercise the OpenAlex HTTP boundary without credentials or network access."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import urllib.error
import urllib.parse


SPEC = importlib.util.spec_from_file_location(
    "academic_search", Path(__file__).resolve().parents[1]
    / "skills/nature-academic-search/scripts/academic_search.py")
academic_search = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(academic_search)


class OpenAlexBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.work = {
            "title": "A relevant study", "doi": "https://doi.org/10.1234/example",
            "publication_year": 2024, "cited_by_count": 3,
            "authorships": [{"author": {"display_name": "Example Author"}}],
            "primary_location": {"source": {"display_name": "Example Journal"}},
            "abstract_inverted_index": {"evidence": [1], "Observed": [0]},
        }
        self.author = {
            "id": "https://openalex.org/A123", "display_name": "Example Author",
            "orcid": "https://orcid.org/0000-0002-1825-0097", "works_count": 3,
            "last_known_institutions": [{"display_name": "Example University"}],
        }

    def test_anonymous_search_preserves_query_filters_and_results(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(
                academic_search.urllib.request, "urlopen",
                return_value=io.BytesIO(json.dumps({"results": [self.work]}).encode())) as call:
            results = academic_search.search("wind aquaculture", year_from=2020)
        request = call.call_args.args[0]
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(request.full_url).query)
        self.assertIsNone(request.get_header("Authorization"))
        self.assertEqual(query["search"], ["wind aquaculture"])
        self.assertEqual(query["filter"], ["from_publication_date:2020-01-01"])
        self.assertEqual(results[0]["doi"], "10.1234/example")
        self.assertEqual(results[0]["abstract"], "Observed evidence")

    def test_authenticated_work_and_author_lookups_keep_key_out_of_url(self):
        credential = "test-openalex-credential"
        operations = [
            (lambda: academic_search.search("wind"), self.work),
            (lambda: academic_search.fetch_author_candidates("Example Author"), self.author),
            (lambda: academic_search.resolve_by_orcid("0000-0002-1825-0097"), self.author),
        ]
        for operation, record in operations:
            with self.subTest(operation=operation), patch.dict(
                    os.environ, {"OPENALEX_API_KEY": credential}, clear=True), patch.object(
                    academic_search.urllib.request, "urlopen",
                    return_value=io.BytesIO(json.dumps({"results": [record]}).encode())) as call:
                self.assertTrue(operation())
            request = call.call_args.args[0]
            self.assertEqual(request.get_header("Authorization"), "Bearer " + credential)
            self.assertNotIn(credential, request.full_url)
            self.assertNotIn("api_key", request.full_url)

    def test_authentication_and_quota_errors_remain_visible_without_retry(self):
        credential = "test-openalex-credential"
        for code in (401, 429):
            stderr = io.StringIO()
            failure = urllib.error.HTTPError(
                "https://api.openalex.org/works", code, "Rejected", {}, None)
            with self.subTest(code=code), patch.dict(
                    os.environ, {"OPENALEX_API_KEY": credential}, clear=True), patch.object(
                    academic_search.sys, "argv", ["academic_search.py", "wind"]), patch.object(
                    academic_search.urllib.request, "urlopen", side_effect=failure) as call, \
                    contextlib.redirect_stderr(stderr):
                self.assertEqual(academic_search.main(), 1)
            self.assertEqual(call.call_count, 1)
            self.assertIn(f"HTTP {code}", stderr.getvalue())
            self.assertNotIn(credential, stderr.getvalue())

    def test_non_json_response_is_a_visible_cli_failure(self):
        stderr = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), patch.object(
                academic_search.sys, "argv", ["academic_search.py", "wind"]), patch.object(
                academic_search.urllib.request, "urlopen", return_value=io.BytesIO(b"not JSON")), \
                contextlib.redirect_stderr(stderr):
            self.assertEqual(academic_search.main(), 1)
        self.assertIn("non-JSON response", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
