import io
import json
import unittest
import zipfile
from tools.stoneage_tw10_cn50_static_visual_custody import blob_sha, sha256, verify_zip


def pack(members):
    out=io.BytesIO()
    with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED) as z:
        for name,payload in members.items():
            z.writestr(name,payload)
    return out.getvalue()


class StaticVisualCustodyTests(unittest.TestCase):
    def setUp(self):
        self.raw=json.dumps({"status":"101_OF_101_ACTUAL_ORIGINAL_BITMAP_RECORDS_IDENTICAL_BOTH_VERSIONS",
                             "counts":{"direct_original_id_matches":101,"rd_sha_equal":101,
                                       "map_collision_attr_raw_hash_equal":101,
                                       "verified_named_npcs":0}}).encode()
    def test_positive(self):
        package=pack({"direct-cn50-tw10-static-r1.json":self.raw})
        result=verify_zip(package,self.raw)
        self.assertEqual(result["zip_sha256"],sha256(package))
        self.assertEqual(len(blob_sha(self.raw)),40)
    def test_mutations(self):
        good="direct-cn50-tw10-static-r1.json"
        for entries,raw in [
            ({good:self.raw+b" "},self.raw),
            ({good:self.raw,"extra.bin":b"x"},self.raw),
            ({"renamed.json":self.raw},self.raw),
            ({good:b'{"status":"BAD"}'},b'{"status":"BAD"}'),
        ]:
            with self.subTest(names=list(entries)), self.assertRaises(ValueError):
                verify_zip(pack(entries),raw)
    def test_fabricated_named_npc_rejected(self):
        bogus=json.loads(self.raw)
        bogus["counts"]["verified_named_npcs"]=1
        raw=json.dumps(bogus).encode()
        with self.assertRaises(ValueError):
            verify_zip(pack({"direct-cn50-tw10-static-r1.json":raw}),raw)
