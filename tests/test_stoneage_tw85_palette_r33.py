"""Adversarial R33 source-value guards."""
import unittest,json,copy
from tools import stoneage_tw85_palette_r33 as r
class R33Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.raw=r.load()
    def test_report_source_replay(self):
        self.assertEqual(len(r.check()["original_palette_pairs_exact"]),16)
    def test_count(self):
        a,b,_,_=r.derive(self.raw)
        self.assertEqual((len(a),len(b)),(16,8))
    def test_palette_sha_tampering(self):
        raw=copy.deepcopy(self.raw);key=list(r.SOURCES)[0];v=json.loads(raw[key])
        t=next(x for x in v["inspection"]["inventory"]["samples"][0]["files"] if x["path"].lower().endswith("/pal/palet_0.sap"))
        t["sha256"]="0"*64;raw[key]=json.dumps(v)
        with self.assertRaisesRegex(ValueError,"digest differs"):r.derive(raw)
    def test_frame_sha_tampering(self):
        raw=copy.deepcopy(self.raw);key=list(r.SOURCES)[4];v=json.loads(raw[key])
        v["frames"][3]["source_RD_sha256"]="0"*64;raw[key]=json.dumps(v)
        with self.assertRaisesRegex(ValueError,"RD digest"):r.derive(raw)
    def test_p2b_semantic_claim_tampering(self):
        raw=copy.deepcopy(self.raw);key=list(r.SOURCES)[2];v=json.loads(raw[key])
        v["actual_scene_palette_selection_proven"]=True;raw[key]=json.dumps(v)
        with self.assertRaisesRegex(ValueError,"runtime selection"):r.derive(raw)
