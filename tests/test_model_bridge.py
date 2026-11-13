"""Exercise the bridge over real loopback HTTP without using any model quota."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "model_bridge", Path(__file__).resolve().parents[1] /
    "skills/research-agent/scripts/model_bridge.py")
bridge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bridge)


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.instruction = self.root / "task.md"
        self.instruction.write_text("用中文写结果，不新增结论。", encoding="utf-8")
        self.evidence = self.root / "evidence.md"
        self.evidence.write_text("Synthetic observation: 6.0 vs 4.5 mg/L; n=12.", encoding="utf-8")
        self.secret = "fixture-client-credential"
        self.addCleanup(patch.stopall)
        patch.dict(os.environ, {"TEST_BRIDGE_KEY": self.secret}).start()
        self.calls = []
        self.http_status = 200
        self.reply = {"model": "gemini-fixture", "choices": [
            {"message": {"content": "均值为 4.5 mg/L。"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 17, "completion_tokens": 9, "total_tokens": 26}}
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                owner.calls.append(("GET", self.path, self.headers.get("Authorization"), None))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"data": [{"id": "gemini-fixture"}]}).encode())

            def do_POST(self):
                payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                owner.calls.append(("POST", self.path, self.headers.get("Authorization"), payload))
                self.send_response(owner.http_status)
                if owner.http_status == 302:
                    self.send_header("Location", "/credential-trap")
                self.end_headers()
                body = owner.reply if owner.http_status == 200 else {"error": owner.secret}
                self.wfile.write(json.dumps(body, ensure_ascii=False).encode("utf-8"))

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.close_server)
        self.config = {"providers": {"local": {
            "base_url": f"http://127.0.0.1:{self.server.server_port}/v1",
            "api_key_env": "TEST_BRIDGE_KEY", "timeout_seconds": 2}},
            "roles": {"writer": {"provider": "local", "model": "gemini-fixture",
                                 "max_output_tokens": 512}}}

    def close_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def call(self, **kwargs):
        return bridge.run_call(self.config, "writer", self.instruction,
                               [self.evidence], self.root / "run", **kwargs)

    def test_actual_utf8_evidence_is_sent_and_response_requires_host_review(self):
        result = self.call()
        self.assertEqual(len(self.calls), 1)
        method, path, auth, payload = self.calls[0]
        self.assertEqual((method, path), ("POST", "/v1/chat/completions"))
        self.assertEqual(auth, "Bearer " + self.secret)
        self.assertIn(self.instruction.read_text(encoding="utf-8"), payload["messages"][1]["content"])
        self.assertIn(self.evidence.read_text(encoding="utf-8"), payload["messages"][1]["content"])
        self.assertEqual(payload["max_tokens"], 512)
        self.assertEqual(result["status"], "AWAITING_HOST_REVIEW")
        self.assertTrue(result["host_review_required"])
        self.assertIsNone(result["account_quota_remaining"])
        self.assertEqual((self.root / "run/response.md").read_text(encoding="utf-8"), "均值为 4.5 mg/L。")
        for p in (self.root / "run").iterdir():
            self.assertNotIn(self.secret, p.read_text(encoding="utf-8"))

    def test_models_discovery_makes_no_generation_request(self):
        self.assertEqual(bridge.model_list(self.config, "local")["models"], ["gemini-fixture"])
        self.assertEqual(self.calls[0][0], "GET")

    def test_existing_output_is_preserved_before_spending_quota(self):
        out = self.root / "run"
        out.mkdir()
        (out / "response.md").write_text("Author text.")
        with self.assertRaises(FileExistsError):
            self.call()
        self.assertEqual(self.calls, [])
        self.assertEqual((out / "response.md").read_text(), "Author text.")

    def test_missing_credential_fails_before_output_and_network(self):
        with patch.dict(os.environ, {}, clear=True), self.assertRaises(bridge.BridgeError):
            self.call()
        self.assertFalse((self.root / "run").exists())
        self.assertEqual(self.calls, [])

    def test_rate_limit_is_not_retried_and_body_is_not_exposed(self):
        self.http_status = 429
        with self.assertRaisesRegex(bridge.BridgeError, "HTTP 429") as error:
            self.call()
        self.assertNotIn(self.secret, str(error.exception))
        self.assertEqual(len(self.calls), 1)
        saved = (self.root / "run/result.json").read_text(encoding="utf-8")
        self.assertNotIn(self.secret, saved)
        self.assertEqual(json.loads(saved)["status"], "FAILED")

    def test_redirect_does_not_forward_credentials_or_follow(self):
        self.http_status = 302
        with self.assertRaisesRegex(bridge.BridgeError, "redirected"):
            self.call()
        self.assertEqual(len(self.calls), 1)

    def test_truncated_text_is_retained_as_partial_not_success(self):
        self.reply["choices"][0]["finish_reason"] = "length"
        with self.assertRaisesRegex(bridge.BridgeError, "partial text retained"):
            self.call()
        self.assertTrue((self.root / "run/partial_response.md").exists())
        self.assertFalse((self.root / "run/response.md").exists())
        self.assertEqual(json.loads((self.root / "run/result.json").read_text())["status"], "FAILED")

    def test_empty_text_is_not_success(self):
        self.reply["choices"][0]["message"]["content"] = " "
        with self.assertRaisesRegex(bridge.BridgeError, "no usable text"):
            self.call()
        self.assertFalse((self.root / "run/response.md").exists())

    def test_malformed_response_is_not_success(self):
        self.reply = {"unexpected": True}
        with self.assertRaisesRegex(bridge.BridgeError, "Incomplete"):
            self.call()
        self.assertEqual(json.loads((self.root / "run/result.json").read_text())["status"], "FAILED")

    def test_provider_reported_model_is_not_silently_relabelled(self):
        self.reply["model"] = "another-provider-model"
        result = self.call()
        self.assertEqual(result["requested_model"], "gemini-fixture")
        self.assertEqual(result["reported_model"], "another-provider-model")
        self.assertFalse(result["reported_matches_requested"])
        self.assertFalse(result["model_identity_confirmed"])

    def test_invalid_output_budget_fails_before_request(self):
        for value in (0, -1, True, 32769):
            with self.subTest(value=value), self.assertRaises(bridge.BridgeError):
                self.call(token_limit=value)
        self.assertEqual(self.calls, [])

    def test_no_scarce_role_is_called_implicitly(self):
        self.config["roles"]["story"] = {"provider": "local", "model": "claude-fixture"}
        self.call()
        self.assertEqual([x[3]["model"] for x in self.calls], ["gemini-fixture"])


if __name__ == "__main__":
    unittest.main()
