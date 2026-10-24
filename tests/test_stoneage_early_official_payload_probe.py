import unittest
from unittest.mock import Mock

from tools.stoneage_early_official_payload_probe import (
    TARGETS, classify, public_url, sniff_prefix, probe, MAX_PREFIX
)


class FakeResponse:
    status = 206
    headers = {"Content-Type": "application/octet-stream", "Content-Range": "bytes 0-4095/1000000"}
    def __init__(self, url, data): self.url, self.data = url, data
    def __enter__(self): return self
    def __exit__(self, *a): pass
    def read(self, amount): return self.data[:amount]
    def geturl(self): return self.url


class PrefixProbeTest(unittest.TestCase):
    def test_exact_documented_endpoints(self):
        self.assertEqual(len(TARGETS), 4)
        self.assertEqual(len({t[1] for t in TARGETS}), 4)
        self.assertIn("/down/sa_demo.exe", TARGETS[1][1])
        self.assertIn("stoneage.zip", TARGETS[2][1])

    def test_magic_and_html_gate(self):
        self.assertEqual(sniff_prefix(b"MZ" + b"0"*50), "MZ_PE_CANDIDATE")
        self.assertEqual(sniff_prefix(b"PK\x03\x04ABC"), "ZIP_CANDIDATE")
        self.assertEqual(sniff_prefix(b"<!doctype html><html>"), "HTML_NOT_INSTALLER")
        self.assertEqual(sniff_prefix(b""), "EMPTY")

    def test_public_url(self):
        for u in ("http://127.0.0.1/data", "http://localhost/file", "file:///etc/passwd",
                  "http://192.168.1.1/", "http://[::1]/x", "http://a:b@example.com/file"):
            self.assertFalse(public_url(u))
        self.assertTrue(public_url(TARGETS[0][1]))

    def test_no_fraudulent_full_payload_from_magic(self):
        url = TARGETS[0][1]
        mocked = Mock()
        mocked.open.return_value = FakeResponse(url, b"MZ" + b"\0" * 1024)
        x = probe(*TARGETS[0], opener=mocked)
        self.assertEqual(x["qualification"], "BINARY_PREFIX_ONLY_REQUIRES_COMPLETE_BYTES")
        self.assertIsNone(x["complete_original_sha256"])
        self.assertFalse(x["complete_body_downloaded"])
        self.assertFalse(x["official_clean_client_verified"])
        self.assertLessEqual(x["sample_bytes"], MAX_PREFIX)

    def test_html_not_binary(self):
        url = TARGETS[0][1]
        mocked = Mock()
        mocked.open.return_value = FakeResponse(url, b"<html>not a game</html>")
        x = probe(*TARGETS[0], opener=mocked)
        self.assertEqual(x["qualification"], "NON_BINARY_OR_UNCLASSIFIED")

    def test_redirect_not_an_authenticated_original(self):
        url = TARGETS[0][1]
        mocked = Mock()
        mocked.open.return_value = FakeResponse("https://other.invalid/file.exe", b"MZabc")
        x = probe(*TARGETS[0], opener=mocked)
        self.assertEqual(x["qualification"], "CROSS_HOST_UNQUALIFIED")

    def test_status_404_not_recovered(self):
        self.assertEqual(classify(404, "MZ_PE_CANDIDATE", TARGETS[0][1], TARGETS[0][1], 4096),
                         "NOT_RETRIEVED")


if __name__ == "__main__":
    unittest.main()
