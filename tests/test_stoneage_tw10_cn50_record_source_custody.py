import io
import json
import unittest
import zipfile
from tools.stoneage_tw10_cn50_record_source_custody import blob_sha,sha256,verify_zip


def pack(members):
    out=io.BytesIO()
    with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED) as w:
        for name,payload in members.items():
            w.writestr(name,payload)
    return out.getvalue()


class CustodyTests(unittest.TestCase):
    def setUp(self):
        self.raw=json.dumps({"result":"DERIVED_RECORD_LEVEL_DIFF_OF_REACQUIRED_ORIGINAL_RESOURCE_BYTES"}).encode()

    def test_exact_archive(self):
        archive=pack({"report.json":self.raw})
        report=verify_zip(archive,self.raw)
        self.assertEqual(report["raw_sha256"],sha256(self.raw))
        self.assertEqual(report["zip_sha256"],sha256(archive))
        self.assertEqual(len(blob_sha(self.raw)),40)

    def test_mutation_rejected(self):
        with self.assertRaises(ValueError):
            verify_zip(pack({"report.json":self.raw+b"x"}),self.raw)
        with self.assertRaises(ValueError):
            verify_zip(pack({"report.json":self.raw,"other.bin":b"x"}),self.raw)
        with self.assertRaises(ValueError):
            verify_zip(pack({"unexpected.exe":self.raw}),self.raw)
        bad=b'{"result":"NO_ORIGINAL_IO"}'
        with self.assertRaises(ValueError):
            verify_zip(pack({"report.json":bad}),bad)
