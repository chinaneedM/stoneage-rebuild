"""R60: contemporaneous player guides, never original TW1.0 server claims."""
import json
from pathlib import Path
import unittest

PATH = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-CN2003-VILLAGE-TRAVEL-RECORD-SOURCE-R1.json"

class TestCn2003VillageTravelSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(PATH.read_text(encoding="utf-8"))

    def test_source_scope(self):
        d = self.d
        self.assertEqual(d["task"], "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-60")
        self.assertEqual([s["id"] for s in d["sources"]], ["S1", "S2", "S3"])
        self.assertTrue(all("PLAYER_GUIDE" in s["kind"] for s in d["sources"]))
        self.assertTrue(all(s["original_http_sha256"] is None and not s["original_http_archived"] for s in d["sources"]))

    def test_services_and_capacity_not_initial_tw10(self):
        d = self.d
        self.assertEqual(len(d["village_service_classes"]), 7)
        self.assertEqual(len({v["id"] for v in d["village_service_classes"]}), 7)
        c = d["capacity_claims_s1"]
        self.assertEqual([c["carried_pets"], c["carried_items"]], [5, 15])
        self.assertEqual([c["initial_stored_pets"], c["initial_stored_items"]], [5, 10])
        self.assertEqual(c["initial_stored_pets"]+5*c["additional_stored_pets_per_rebirth"], c["claimed_5_rebirth_stored_pets"])
        self.assertEqual(c["initial_stored_items"]+5*c["additional_stored_items_per_rebirth"], c["claimed_5_rebirth_stored_items"])
        self.assertFalse(c["original_build_verified"])

    def test_cross_guide_quantity_conflicts_are_unresolved(self):
        by = {r["id"]:r for r in self.d["record_point_comparison"]}
        self.assertEqual(len(by), 12)
        expected = {"MARINAS":(1,2),"KOAO":(2,1),"KARUTANA":(1,2)}
        self.assertEqual({r["id"] for r in by.values() if r["relation"]=="CONTRADICT_QUANTITY"},set(expected))
        for rid,(a,b) in expected.items():
            self.assertEqual((by[rid]["s1"]["qty"], by[rid]["s2"]["qty"]), (a,b))
            self.assertEqual(by[rid]["s1"]["item"],by[rid]["s2"]["item"])
        self.assertEqual(len([r for r in by.values() if r["relation"]=="AGREE_OFFERING_ONLY"]),8)
        self.assertEqual(by["CHIKAKA"]["relation"],"S2_UNSPECIFIED")
        self.assertIsNone(by["CHIKAKA"]["s2"]["qty"])
        self.assertIsNone(by["CHIKAKA"]["s2"]["item"])

    def test_coordinates_and_fares_are_not_original_runtime(self):
        self.assertTrue(all("record_xy" in r["s1"] and "world_xy_candidates" in r["s2"] for r in self.d["record_point_comparison"]))
        self.assertFalse(self.d["negative_claims"]["source_xy_frames_equivalent"])
        modes={m["id"]:m for m in self.d["transport_modes"]}
        self.assertEqual(len(modes),5)
        self.assertEqual(modes["MAMMOTH_BUS"]["claims"]["stop_minutes"],3)
        self.assertEqual(modes["MAMMOTH_BUS"]["claims"]["ticket_stone_range"],[20,30])
        self.assertEqual(modes["GAMI_AIR"]["claims"]["fare_stone"],1000)
        self.assertEqual(modes["SPIRIT_FEATHER"]["claims"]["ordinary_feather_stone"],2000)
        self.assertEqual(modes["SUBSEA_ROUTE"]["claims"]["reported_npc_toll_stone"],300)
        self.assertEqual(modes["GOLDEN_FLIGHT"]["claims"]["reported_quest_level_min"],80)

    def test_money_guides_do_not_create_hard_gates(self):
        rows=self.d["economy_guide_s3"]
        self.assertEqual({v["id"] for v in rows},{"SELL_MEAT","MAMMOTH_DELIVERY","CAPTURE_TRADE_PETS"})
        self.assertTrue(all(not v["hard_level_gate_proven"] for v in rows))

    def test_boundaries_and_reopening(self):
        d=self.d
        self.assertEqual(len(d["material_conflicts"]),8)
        self.assertTrue(all(v["resolved"] is False for v in d["material_conflicts"]))
        self.assertTrue(all(v is False for v in d["negative_claims"].values()))
        self.assertEqual(d["next"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-61")

if __name__=="__main__":
    unittest.main()
