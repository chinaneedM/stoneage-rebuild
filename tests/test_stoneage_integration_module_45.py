"""INTEGRATION45 public-source regression: original DAT/CREATE/quest links and negative gates.

No private original assets are required or exposed by this test.
"""
import hashlib
import json
from pathlib import Path
import unittest

DATA = Path(__file__).resolve().parents[1] / "research" / "recovered"

def load(name):
    raw=(DATA/name).read_bytes()
    blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()
    return json.loads(raw),blob

class ThreeJarugaSourceWindowsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r,_=load("STONEAGE-INTEGRATION45-JARUGA-A3-A7-A11-ORIGINAL-SOURCE-SCENES-R1.json")
        cls.q,cls.qblob=load("STONEAGE-QUEST25-FOUR-ISLAND-TOUR-ROUTES-SOURCE-R1.json")
        cls.i41,cls.i41blob=load("STONEAGE-INTEGRATION41-JARUGA-ROUTE-B-CHECKPOINTS-SOURCE-R1.json")
        cls.map04,cls.map04blob=load("STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json")
        cls.i44,cls.i44blob=load("STONEAGE-INTEGRATION44-JARUGA-A1-ORIGINAL-SOURCE-PIXELS-R1.json")
        cls.qroute=next(x for x in cls.q["routes"] if x["label"]=="A")
        cls.scripts={x["path"]:x for x in cls.q["source_scripts"]}

    def test_immutable_sources_and_preserved_current(self):
        self.assertEqual(self.r["upstream_derived_git_blobs"],
            {"QUEST25":self.qblob,"I41":self.i41blob,"MAP04":self.map04blob,"I44":self.i44blob})
        self.assertEqual(self.r["preserved_historical_CURRENT"],
            {"blob":"c89e0e33537990aa2132b47c40fef49a985a935c","bytes":2709173,"changed":False})

    def test_three_actual_original_DAT_floors_and_raw_coordinates(self):
        expected={3:(20105,[25,49],[20,44,30,54],[403,0,49152],68,27,67),
                  7:(20301,[238,118],[233,113,243,123],[4304,0,49152],126,49,25),
                  11:(20601,[5,11],[0,6,10,16],[4003,0,49152],70,34,123)}
        self.assertEqual([s["checkpoint"] for s in self.r["sites"]],[3,7,11])
        old_map={x["floor"]:x for x in self.i41["map_files"]}
        for site in self.r["sites"]:
            floor,xy,bounds,center,refs,uniq,low=expected[site["checkpoint"]]
            self.assertEqual(site["original_DAT"]["floor"],floor)
            self.assertEqual(site["original_DAT"]["sha256"],old_map[floor]["sha256"])
            self.assertEqual(site["original_DAT"]["bytes"],old_map[floor]["bytes"])
            window=site["source_window"]
            self.assertEqual((window["center"],window["bounds_inclusive"],
                              window["original_three_u16_at_center"]),(xy,bounds,center))
            self.assertEqual((window["original_cells"],window["gt99_placements"],
                              window["distinct_qualified_aliases"],window["low_1_to_99_not_drawn"]),
                             (121,refs,uniq,low))
            self.assertEqual(window["unknown_gt99"],0)

    def test_create_six_original_TYPE_segments_and_proof_literals(self):
        for site in self.r["sites"]:
            old=next(x for x in self.qroute["checkpoints"] if x["number"]==site["checkpoint"])
            cfg=old["source"];src=site["original_CREATE"];scr=site["original_script"]
            self.assertEqual(src["ordinal"],cfg["create_ordinal"])
            self.assertEqual(src["block_sha256"],cfg["block_sha256"])
            self.assertEqual(src["borncorner"],cfg["borncorner"])
            self.assertEqual(src["graphic_alias"],cfg["graphic_alias"])
            self.assertEqual(src["template"],cfg["template_path"])
            self.assertEqual(src["functionset"],"ExChangeMan")
            previous=self.scripts[cfg["script_path"]]
            self.assertEqual((scr["path"],scr["bytes"],scr["sha256"],scr["event_count"]),
                             (previous["path"],previous["bytes"],previous["sha256"],len(previous["events"])))
            self.assertEqual(scr["event_count"],6)
            self.assertEqual(scr["event_sections"],[
                {"ordinal":ev["ordinal"],"condition":ev["condition_literal"],"section_sha256":ev["section_sha256"],
                 "commands":ev["commands"]} for ev in previous["events"]])
            self.assertEqual(site["original_proof"],
                {"required":old["incoming_item"],"reward_literal":old["outgoing_item"],
                 "condition":old["condition_literal"]})
            first=scr["event_sections"][0]
            self.assertEqual(first["commands"]["DelItem"],[str(old["incoming_item"])])
            self.assertEqual(first["commands"]["GetItem"],[str(old["outgoing_item"])])

    def test_original_image_catalogue_not_physical_bitmap_name_fallback(self):
        aliases=self.r["original_pixel_aliases_union"]
        self.assertEqual(len(aliases),108)
        self.assertEqual(len(set(aliases)),108)
        map04={row[0] for row in self.map04["source_TW1_real_RD_rows"]}
        i41={int(k) for k in self.i41["map_pixel_sources"]}
        self.assertTrue(all(x in map04 or x in i41 for x in aliases))
        self.assertEqual(self.r["per_site_alias_count_sum"],110)
        self.assertEqual(sum(s["source_window"]["distinct_qualified_aliases"] for s in self.r["sites"]),110)
        for s in self.r["sites"]:
            w=s["source_window"]
            self.assertEqual(w["qualified_aliases_from_I41"]+w["qualified_aliases_from_MAP04"],
                             w["distinct_qualified_aliases"])
        self.assertEqual([sum(s["source_window"][x] for s in self.r["sites"]) for x in
                          ("qualified_aliases_from_I41","qualified_aliases_from_MAP04")],[53,57])

    def test_modern_nine_full_RGBA_witnesses(self):
        scenes=self.r["sites"]
        self.assertEqual(len(scenes),3)
        for s in scenes:
            f=s["modern_observation"]["independent_full_RGBA_matches"]
            self.assertEqual(set(f),{"plane0","plane1","combined"})
            self.assertEqual(len({x for x in f.values()}),3)
            self.assertTrue(all(len(x)==64 for x in f.values()))
            self.assertFalse(s["modern_observation"]["original_native_layer_or_palette_verified"])
        count=self.r["counts"]
        self.assertEqual((count["original_DAT_windows"],count["original_source_map_cells"],
                          count["high_gt99_image_placements"],count["deduplicated_source_aliases"],
                          count["independent_pixel_canvases_replayed"]),(3,363,264,108,9))
        self.assertEqual(count["original_low_value_refs_not_drawn"],215)

    def test_new_TW1_16067_and_prior_TW1_16068_witness(self):
        new=self.r["actually_recovered_TW1_16067"]
        self.assertEqual((new["logical_alias"],new["ordinal"],new["physical_bitmap"],new["offset"],
                          new["bytes"],new["dimensions"]),(16067,5913,5913,25054495,1694,[32,78]))
        self.assertEqual(new["RD_sha256"],"8dc805589a31d6627aae8df214f587ae08dd9b6d277bfb0d494e7d44292cddd0")
        self.assertEqual(new["RGBA_sha256"],"8b145e29b42a9bc1f6cb4d2b56366862b5a0d53f98117b33c584cf8ebfd55667")
        self.assertTrue(new["RD_two_independent_decoders_match"])
        prior=self.i44["pixel_sources"]["new_RD"][1]
        self.assertEqual(self.r["TW1_16068_rechecked"]["RD_sha256"],prior["RD_sha256"])
        self.assertEqual(self.r["TW1_16068_rechecked"]["RGBA_sha256"],prior["RGBA_sha256"])
        self.assertFalse(self.r["original_source_scopes"]["official_same_deployment_proven"])

    def test_private_custody_receipts_and_no_gameplay_promotions(self):
        p=self.r["private_source_only_immutable_receipt"]
        self.assertEqual((p["archive_bytes"],p["archive_members"]),(5098689,132))
        self.assertEqual(p["archive_sha256"],"a705e963612ce24177940feebe9f7d4225a4bbc83af2197624af31bb5350d018")
        self.assertEqual(p["full_private_source_derived_JSON_sha256"],"f054f24869c107566c33eda3487bf5b56e586a4adb9535ede84a35741cf90312")
        self.assertTrue(p["whole_archive_Library_readback_verified"])
        self.assertTrue(p["all_archive_CRC_verified"])
        self.assertEqual(len(self.r["actual_private_archive_verifications"]),5)
        self.assertTrue(all(x["CRC_valid"] for x in self.r["actual_private_archive_verifications"]))
        self.assertTrue(all(value is False for value in self.r["negative_evidence_gates"].values()))
        self.assertEqual(self.r["status"],{
            "Stage_A":{"PARTIAL":7,"OPEN":2},"Stage_B":"GATED",
            "wiki":"GATED","R79":"PAUSED_NON_BLOCKING","overall_percent":None})

if __name__=="__main__":unittest.main()
