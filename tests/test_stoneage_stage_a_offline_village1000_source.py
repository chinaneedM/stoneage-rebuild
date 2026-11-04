"""Source-only conservation of 1000-village NPC CREATE/scene atlas."""
from collections import Counter
import json
from pathlib import Path
import unittest

R=Path(__file__).resolve().parents[1]/"research"/"recovered"
def source(name):
    return json.loads((R/name).read_text(encoding="utf-8"))
class OfflineVillage1000SourceAtlas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=source("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-02-VILLAGE1000-NPC-SOURCE-BRIDGE-R1.json")
        cls.p=source("STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json")
    def test_full_original_source_bridge(self):
        a,p=self.a,self.p
        src=[r for r in p["create_rows"] if r[5]==1000]
        self.assertEqual(len(src),len(a["rows"]))
        self.assertEqual(len(src),78)
        self.assertEqual(a["original_source_rar_sha256"],p["original_rar_sha256"])
        files={r[0]:r for r in p["source_files"]}
        key=lambda r:(r["source_file"],r["original_block_ordinal"])
        rows={key(r):r for r in a["rows"]}
        self.assertEqual(len(rows),78)
        for old in src:
            with self.subTest(path=old[0],ordinal=old[1]):
                v=rows[(old[0],old[1])]
                self.assertEqual(v["original_block_sha256"],old[4])
                self.assertEqual(v["source_sha256"],files[old[0]][2])
                self.assertEqual(v["source_graphicname"],old[6])
                self.assertEqual(v["original_name_sha256"],old[14])
                self.assertEqual(v["source_function_token"],old[11])
                self.assertEqual(len(v["source_references"]),len(old[15]))
                for ref,oldref in zip(v["source_references"],old[15]):
                    self.assertEqual([ref["path"],ref["qualification"],ref["sha256"]],oldref)
                if old[8] or old[7]:
                    self.assertEqual(v["coordinate_anchor"],(old[8] or old[7])[:2])
                else:
                    self.assertIn(old[0],["my/tiancai/transfer.create","sa60/newbie/newbie.create"])
                    self.assertEqual(v["source_anchor_kind"],"borncenter_verified_direct_original_20261104")
        self.assertEqual(rows[("my/tiancai/transfer.create",0)]["coordinate_anchor"],[94,102])
        self.assertEqual(rows[("sa60/newbie/newbie.create",0)]["coordinate_anchor"],[48,62])
    def test_observation_boundary(self):
        a=self.a;v=a["private_O34_original_source_window"]; self.assertEqual(v,[48,92,72,132])
        rows=a["rows"]
        self.assertEqual(len({r["source_file"] for r in rows}),18)
        self.assertEqual(sum(r["in_prior_O34_window"] for r in rows),18)
        self.assertEqual(sum(not r["in_prior_O34_window"] for r in rows),60)
        for r in rows:
            x,y=r["coordinate_anchor"]
            self.assertTrue(0<=x<160 and 0<=y<160)
            self.assertEqual(r["in_prior_O34_window"],v[0]<=x<=v[2] and v[1]<=y<=v[3])
        self.assertEqual(Counter(r["source_function_token"] for r in rows)["npcgen_warp"],32)
        self.assertEqual(sum(len(r["source_references"]) for r in rows),39)
    def test_no_promoted_historical_claims(self):
        a=self.a
        self.assertTrue(a["scope"].startswith("LATER_PRESERVED_COMMUNITY"))
        self.assertTrue(all(value is False for value in a["source_evidence_limits"].values()))
        self.assertEqual(a["stage_a"],"7_PARTIAL_2_OPEN")
        self.assertEqual(a["stage_b"],"GATED")
        self.assertEqual(a["R79"],"PAUSED_NON_BLOCKING")
        self.assertIsNone(a["overall_percent"])
        self.assertNotIn("raw_dialogue",a)
        self.assertNotIn("original_pixels",a)
        self.assertNotIn("private_source_zip_payload",a)
        self.assertTrue(all("source_message_text" not in r for r in a["rows"]))
    def test_private_browser_claim_narrow(self):
        p=self.a["private_browser_probe"]
        self.assertEqual([p["records"],p["inside_window"],p["warp_function_token"]],[78,18,32])
        self.assertEqual([p["javascript_errors"],p["external_http_requests"]],[0,0])
        self.assertEqual(p["page_file_navigation"],"BLOCKED_BY_ADMINISTRATOR_NOT_CLAIMED")
if __name__=="__main__":unittest.main()
