import hashlib
import io
import json
import tempfile
import threading
import unittest
from pathlib import Path

from tools.stoneage_tw10_archive_parallel_download import (
    download_parallel, ranges, _allowed_source, DEFAULT_WORKERS
)
from tools.stoneage_tw10_archive_chunk_download import (
    ITEM, FILE, ARCHIVE_SIZE
)

SRC = "https://ia804111.us.archive.org/0/items/" + ITEM + "/" + FILE


class FakeResponse:
    status = 206
    def __init__(self, data, start, end, total, status=206, redirect=None,
                 content_range=None):
        self.body = io.BytesIO(data)
        self.status = status
        self.headers = {"Content-Range": content_range
                        if content_range is not None
                        else f"bytes {start}-{end}/{total}"}
        self.url = redirect or SRC

    def read(self, count):
        return self.body.read(count)

    def geturl(self):
        return self.url

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class ParallelArchiveTests(unittest.TestCase):
    def test_ranges_do_not_overlap_and_last_is_truncated(self):
        self.assertEqual(ranges(75, 13), [
            (0, 12), (13, 25), (26, 38), (39, 51), (52, 64), (65, 74)])

    def test_parallel_reconstructs_exact_hash_pinned_bytes(self):
        payload = b"independent-Taiwan-source-test!" * 8
        lock = threading.Lock()
        observed = set()
        def opener(request, timeout):
            start, end = map(int, request.headers["Range"][6:].split("-"))
            with lock:
                observed.add((start, end))
            return FakeResponse(payload[start:end+1], start, end, len(payload))
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "transient.rar"
            result = download_parallel(SRC, out, size=len(payload),
                                       md5=hashlib.md5(payload).hexdigest(),
                                       sha1=hashlib.sha1(payload).hexdigest(),
                                       chunk_size=17, workers=5, opener=opener)
            self.assertTrue(result["verified"])
            self.assertEqual(out.read_bytes(), payload)
            self.assertEqual(observed, set(ranges(len(payload), 17)))
            self.assertEqual(result["range_count"], len(observed))

    def test_wrong_hash_deletes_original_bytes(self):
        payload = b"abc" * 4
        def opener(request, timeout):
            s, e = map(int, request.headers["Range"][6:].split("-"))
            return FakeResponse(payload[s:e+1], s, e, len(payload))
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "original.rar"
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                download_parallel(SRC, out, size=len(payload),
                                  md5="0" * 32, sha1=hashlib.sha1(payload).hexdigest(),
                                  chunk_size=4, workers=3, opener=opener)
            self.assertFalse(out.exists())

    def test_untrusted_redirect_does_not_produce_archive(self):
        def opener(request, timeout):
            s, e = map(int, request.headers["Range"][6:].split("-"))
            return FakeResponse(b"x" * (e-s+1), s, e, 4,
                                redirect="https://evil.example.invalid/source")
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"original.rar"
            with self.assertRaisesRegex(ValueError, "untrusted"):
                download_parallel(SRC,out,size=4,chunk_size=4,
                                  md5="0"*32,sha1="0"*40,opener=opener)
            self.assertFalse(out.exists())

    def test_server_ignoring_ranges_is_rejected(self):
        def opener(request, timeout):
            s,e=map(int, request.headers["Range"][6:].split("-"))
            return FakeResponse(b"ABCD",s,e,4,status=200)
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"original.rar"
            with self.assertRaisesRegex(ValueError, "byte range"):
                download_parallel(SRC,out,size=4,chunk_size=4,
                                  md5="0"*32,sha1="0"*40,opener=opener)
            self.assertFalse(out.exists())

    def test_truncated_range_is_not_silently_accepted(self):
        def opener(request,timeout):
            s,e=map(int,request.headers["Range"][6:].split("-"))
            return FakeResponse(b"",s,e,4)
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"original.rar"
            with self.assertRaisesRegex(ValueError, "range transport failed"):
                download_parallel(SRC,out,size=4,chunk_size=4,
                                  md5="0"*32,sha1="0"*40,opener=opener)
            self.assertFalse(out.exists())

    def test_insecure_or_unapproved_sources(self):
        bad=["http://ia804111.us.archive.org/0/items/"+ITEM+"/"+FILE,
             "https://evil.example/0/items/"+ITEM+"/"+FILE,
             SRC+"?token=steal", SRC.replace("/0/items/", "/0/data/"),
             "https://ia804111.us.archive.org:8080/0/items/"+ITEM+"/"+FILE]
        for url in bad:
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    _allowed_source(url)

    def test_refuse_existing_destination(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"original.rar"
            out.write_bytes(b"preserved")
            with self.assertRaisesRegex(ValueError,"existing"):
                download_parallel(SRC,out,size=3)
            self.assertEqual(out.read_bytes(),b"preserved")

    def test_fail_closed_bounds(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"original.rar"
            for kwargs in (
                {"size":ARCHIVE_SIZE+1},{"workers":17},{"workers":0},
                {"chunk_size":17*1024*1024},{"max_seconds":901}):
                with self.subTest(kwargs=kwargs):
                    with self.assertRaisesRegex(ValueError,"bounds"):
                        download_parallel(SRC,out,**kwargs)
            self.assertFalse(out.exists())

    def test_pin_format(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"original.rar"
            with self.assertRaisesRegex(ValueError,"pin format"):
                download_parallel(SRC,out,md5="xyz")
            self.assertFalse(out.exists())


if __name__=="__main__":
    unittest.main()
