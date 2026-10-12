import json
import socket
import unittest
from urllib.error import HTTPError, URLError

from tools.stoneage_tw10_archive_transport_preflight import (
    ARCHIVE_MD5, ARCHIVE_SHA1, FILE, META_LIMIT, RANGE_LIMIT,
    Signal, metadata_summary, probe, range_class, run,
)


class FakeResponse:
    status = 206
    def __init__(self, content=b"", headers=None, status=206):
        self.content = content
        self.headers = headers or {}
        self.status = status
        self.index = 0

    def read(self, count):
        out = self.content[self.index:self.index + count]
        self.index += len(out)
        return out

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


def meta(**override):
    d = {"files": [{"name": FILE, "size": "54321",
                     "md5": ARCHIVE_MD5, "sha1": ARCHIVE_SHA1}],
         "dir": "/0/items/stoneage_tw_2000_win",
         "server": "ia804111.us.archive.org",
         "workable_servers": ["ia804111.us.archive.org",
                              "evil.example.net", "ia800999.us.archive.org"]}
    d.update(override)
    return json.dumps(d).encode()


class TestArchiveTransportPreflight(unittest.TestCase):
    def test_exact_metadata_identity_and_server_allowlist(self):
        m = metadata_summary(meta())
        self.assertTrue(m["parse_ok"])
        self.assertTrue(m["file_found"])
        self.assertTrue(m["md5_matches_pinned"])
        self.assertTrue(m["sha1_matches_pinned"])
        self.assertEqual(m["candidate_server_count"], 2)
        self.assertEqual(m["server"], "ia804111.us.archive.org")
        self.assertTrue(m["valid_storage_directory"])
        self.assertEqual(m["storage_directory"], "/0/items/stoneage_tw_2000_win")

    def test_untrusted_storage_directory_is_rejected(self):
        d = json.loads(meta())
        d["dir"] = "/0/items/stoneage_tw_2000_win/../../other"
        m = metadata_summary(json.dumps(d).encode())
        self.assertFalse(m["valid_storage_directory"])
        self.assertEqual(m["storage_directory"], "")

    def test_wrong_item_storage_directory_is_rejected(self):
        d = json.loads(meta())
        d["dir"] = "/4/items/other"
        self.assertFalse(metadata_summary(json.dumps(d).encode())
                         ["valid_storage_directory"])

    def test_bad_directory_skips_storage_probe(self):
        d = json.loads(meta())
        d["dir"] = "/private/data"
        calls = []
        def opener(request, timeout):
            calls.append(request.full_url)
            if "/metadata/" in request.full_url:
                return FakeResponse(json.dumps(d).encode(), status=200)
            return FakeResponse(b"\x00", status=206)
        result = run(opener=opener)
        self.assertEqual(len(calls), 3)
        self.assertNotIn("storage_server_range",
                         [probe["name"] for probe in result["probes"]])

    def test_metadata_mismatch_does_not_pass(self):
        d = json.loads(meta())
        d["files"][0]["md5"] = "0" * 32
        d["files"][0]["sha1"] = "0" * 40
        m = metadata_summary(json.dumps(d).encode())
        self.assertFalse(m["md5_matches_pinned"])
        self.assertFalse(m["sha1_matches_pinned"])

    def test_capped_or_invalid_metadata_does_not_claim_identity(self):
        self.assertFalse(metadata_summary(meta(), capped=True)["parse_ok"])
        self.assertFalse(metadata_summary(b"{")["parse_ok"])
        self.assertFalse(metadata_summary(b"{}")["parse_ok"])

    def test_sample_is_bounded_even_if_range_ignored(self):
        def opener(request, timeout):
            self.assertEqual(request.get_header("Range"), "bytes=0-4095")
            return FakeResponse(b"Z" * (RANGE_LIMIT + 8000), status=200)
        s, body = probe("canonical_range", "https://archive.org/x",
                        "GET", opener=opener)
        self.assertEqual(len(body), RANGE_LIMIT)
        self.assertEqual(s.bytes_read, RANGE_LIMIT)
        self.assertTrue(s.capped)
        self.assertEqual(range_class(s), "RANGE_IGNORED")

    def test_partial_http_signal_requires_content_range(self):
        signal = Signal("canonical_range", "responded", status=206,
                        content_range="bytes 0-4095/12000")
        self.assertEqual(range_class(signal), "PARTIAL_CONFIRMED")
        self.assertEqual(range_class(Signal("x", "responded", 206)), "UNRESOLVED")

    def test_head_must_read_nothing(self):
        def opener(request, timeout):
            self.assertEqual(request.get_method(), "HEAD")
            return FakeResponse(b"raw copyrighted bytes", status=200)
        s, body = probe("canonical_head", "https://archive.org/x",
                        "HEAD", opener=opener)
        self.assertEqual(body, b"")
        self.assertEqual(s.bytes_read, 0)

    def test_http_404_is_not_success(self):
        def opener(request, timeout):
            raise HTTPError("https://archive.org/x", 404, "not found", {}, None)
        s, body = probe("canonical_range", "https://archive.org/x",
                        "GET", opener=opener)
        self.assertEqual(s.status, 404)
        self.assertEqual(s.outcome, "http_error")
        self.assertEqual(body, b"")

    def test_timeout_has_no_exception_or_byte_leak(self):
        def opener(request, timeout):
            raise socket.timeout("internal URL and key")
        s, body = probe("canonical_head", "https://archive.org/x",
                        "HEAD", opener=opener)
        self.assertEqual(s.outcome, "transport_error")
        self.assertEqual(body, b"")
        self.assertNotIn("internal URL", str(s))

    def test_cap_validation_precedes_network(self):
        with self.assertRaises(ValueError):
            probe("metadata", "https://archive.org/x", "GET", cap=META_LIMIT + 1)
        with self.assertRaises(ValueError):
            probe("canonical_range", "https://archive.org/x", "GET", cap=100)

    def test_full_run_does_not_publish_body_or_claim_binary_verification(self):
        calls = []
        def opener(request, timeout):
            calls.append(request.full_url)
            if "/metadata/" in request.full_url:
                return FakeResponse(meta(), status=200)
            if request.get_method() == "HEAD":
                return FakeResponse(status=200)
            return FakeResponse(b"\x00PROPRIETARY\xff" * 300,
                                headers={"Content-Range": "bytes 0-4095/54321"}, status=206)
        result = run(opener=opener)
        raw = json.dumps(result)
        self.assertEqual(len(calls), 4)
        self.assertIn("/0/items/stoneage_tw_2000_win/CD_DIC.rar", calls[-1])
        self.assertNotIn("PROPRIETARY", raw)
        self.assertEqual(result["canonical_range_capability"], "PARTIAL_CONFIRMED")
        self.assertFalse(result["original_client_hash_verified"])
        self.assertEqual(result["admission"], "TRANSPORT_SIGNALS_ONLY")


if __name__ == "__main__":
    unittest.main()
