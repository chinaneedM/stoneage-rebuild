import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError
from tools.stoneage_tw10_archive_chunk_download import (
    ARCHIVE_SIZE, FILE, ITEM, approved_source, download_pinned
)
from tools.stoneage_tw10_archive_transport_preflight import ARCHIVE_MD5, ARCHIVE_SHA1


class Response:
    status = 206

    def __init__(self, data, content_range="", code=206, url=None):
        self.data = io.BytesIO(data)
        self.headers = {"Content-Range": content_range}
        self.status = code
        self.url = url

    def read(self, size):
        return self.data.read(size)

    def geturl(self):
        return self.url or ("https://ia804111.us.archive.org/0/items/"
                            + ITEM + "/" + FILE)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


SRC = "https://ia804111.us.archive.org/0/items/" + ITEM + "/" + FILE


class Tests(unittest.TestCase):
    def test_approved_catalog_path_and_exact_identity(self):
        d = {"files":[{"name":FILE, "size":str(ARCHIVE_SIZE),
                       "md5":ARCHIVE_MD5, "sha1":ARCHIVE_SHA1}],
             "dir":"/0/items/"+ITEM,
             "server":"ia804111.us.archive.org"}
        def opener(req, timeout):
            self.assertIn("/metadata/", req.full_url)
            r = Response(json.dumps(d).encode(), code=200)
            return r
        self.assertEqual(approved_source(opener), SRC)

    def test_catalog_rejects_wrong_archive_hash(self):
        d = {"files":[{"name":FILE, "size":str(ARCHIVE_SIZE),
                       "md5":"0"*32, "sha1":ARCHIVE_SHA1}],
             "dir":"/0/items/"+ITEM,
             "server":"ia804111.us.archive.org"}
        def opener(req, timeout):
            return Response(json.dumps(d).encode(), code=200)
        with self.assertRaisesRegex(ValueError, "identity/path"):
            approved_source(opener)

    def test_download_exact_ranges_and_both_hashes(self):
        data = b"StoneAge-research-fixture" * 3
        reqs=[]
        def opener(req, timeout):
            self.assertEqual(req.get_method(), "GET")
            start, end = map(int, req.headers["Range"].removeprefix("bytes=").split("-"))
            reqs.append((start,end))
            return Response(data[start:end+1],
                            f"bytes {start}-{end}/{len(data)}")
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"original.rar"
            result=download_pinned(SRC,p,size=len(data),
                   md5=hashlib.md5(data).hexdigest(),
                   sha1=hashlib.sha1(data).hexdigest(),chunk_size=13,
                   opener=opener)
            self.assertTrue(result["verified"])
            self.assertEqual(p.read_bytes(),data)
            self.assertEqual(reqs,[(0,12),(13,25),(26,38),(39,51),(52,64),(65,77)])

    def test_hash_mismatch_unlinks_transient_file(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"source.rar"
            def opener(req, timeout):
                return Response(b"abc", "bytes 0-2/3")
            with self.assertRaisesRegex(ValueError,"hash mismatch"):
                download_pinned(SRC,p,size=3,md5="0"*32,
                                sha1=hashlib.sha1(b"abc").hexdigest(),
                                opener=opener)
            self.assertFalse(p.exists())

    def test_range_ignored_is_rejected_not_resumed(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"source.rar"
            def opener(req, timeout):
                return Response(b"abc", "bytes 0-2/3", code=200)
            with self.assertRaisesRegex(ValueError, "byte range"):
                download_pinned(SRC,p,size=3,md5="0"*32,sha1="0"*40,opener=opener)
            self.assertFalse(p.exists())

    def test_wrong_range_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"source.rar"
            def opener(req, timeout):
                return Response(b"abc", "bytes 1-3/3")
            with self.assertRaisesRegex(ValueError, "byte range"):
                download_pinned(SRC,p,size=3,md5="0"*32,sha1="0"*40,opener=opener)
            self.assertFalse(p.exists())

    def test_redirect_to_untrusted_host_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"source.rar"
            def opener(req, timeout):
                return Response(b"abc", "bytes 0-2/3",
                                url="https://example.org/0/items/"+ITEM+"/"+FILE)
            with self.assertRaisesRegex(ValueError, "untrusted"):
                download_pinned(SRC,p,size=3,md5="0"*32,sha1="0"*40,opener=opener)
            self.assertFalse(p.exists())

    def test_wrong_host_rejected_before_open(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"source.rar"
            with self.assertRaisesRegex(ValueError, "unapproved"):
                download_pinned("https://evil.example/0/items/"+ITEM+"/"+FILE,p,size=3)
            self.assertFalse(p.exists())

    def test_out_of_bounds_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"source.rar"
            with self.assertRaisesRegex(ValueError, "bounds"):
                download_pinned(SRC,p,size=ARCHIVE_SIZE+1)
            with self.assertRaisesRegex(ValueError, "bounds"):
                download_pinned(SRC,p,size=3,chunk_size=100000000)
            self.assertFalse(p.exists())

    def test_no_overwriting_existing_file(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"original.rar"
            p.write_bytes(b"protect")
            with self.assertRaisesRegex(ValueError, "overwrite"):
                download_pinned(SRC,p,size=3)
            self.assertEqual(p.read_bytes(), b"protect")


if __name__=="__main__":
    unittest.main()
