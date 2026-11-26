import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import stoneage_pet_offline_atlas as atlas

class AtlasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=atlas.payload()

    def test_all_existing_primary_source_positions(self):
        d=self.data
        self.assertEqual(len(d["rows"]), 5924)
        self.assertEqual(d["summary"]["literal_labels"], 1046)
        self.assertEqual(d["summary"]["unlabelled_source_occurrences"], 16)
        self.assertEqual(len(d["sources"]), 98)
        self.assertFalse(d["historically_complete"])
        self.assertFalse(d["original_pixels_included"])
        self.assertIsNone(d["official_species_count"])
        self.assertTrue(all(not x["official_same_deployment_identity_verified"] for x in d["rows"]))
        self.assertEqual(len({(x["source"],tuple(x["pointer"])) for x in d["rows"]}),5924)

    def test_versioned_field_access(self):
        d=self.data
        tw=[x for x in d["rows"] if x["source"]=="tw10"]
        late=[x for x in d["rows"] if x["source"]=="tw75"]
        self.assertEqual(len(tw),124)
        self.assertEqual(len(d["profiles"]),124)
        self.assertEqual({k for k,v in d["profiles"].items() if v["git_blob"] != v["historical_audit_git_blob"]}, set(atlas.PORTRAIT_SUPERSESSIONS))
        for k in atlas.PORTRAIT_SUPERSESSIONS:
            f=d["profiles"][k]["profile"]["appearance"]
            self.assertIsNone(f["portrait"]["source_rd_bitmap_number"])
            self.assertEqual(len(f["cross_version_original_portrait_rd_candidates"]["TW85_saved_PC_higher_variants"]),2)
        w=d["profiles"]["PET-000001"]["profile"]
        self.assertEqual(w["names"]["original_client"],"烏力")
        self.assertEqual(w["appearance"]["graphic_number"],100250)
        self.assertEqual(w["appearance"]["action_sequences"]["source_sequences"],56)
        self.assertIsNone(w["combat_stats"]["initial_stat_ranges"]["minimum"]["derived_hp"])
        self.assertIsNone(w["acquisition"]["original_capture"]["map_name"])
        self.assertFalse(w["status"]["all_fields_historically_complete"])
        self.assertEqual(len(late),467)
        self.assertTrue(all("field_reference" in x["detail"] for x in tw))
        self.assertTrue(all({"conditional_lv1_panel","conditional_per_level_internal","elements","skill_slots","saved_mixed25_acquisition"} <= set(x["detail"]) for x in late))
        self.assertTrue(all(x["source"] in d["sources"] for x in d["rows"]))
        self.assertTrue(all(l["source"] in d["sources"] for x in d["rows"] for l in x["linked_records"]))

    def test_late_source_profiles(self):
        p=self.data["late_profiles"]
        self.assertEqual(len(p),467)
        self.assertEqual(len({x["original_name"] for x in p.values()}),438)
        self.assertEqual(sum(x["comparison_grade"]=="EXACT_SHARED_TEMPLATE_ROW" for x in p.values()),440)
        self.assertEqual(sum(x["comparison_grade"]=="SAME_ID_NONIDENTICAL_ROW" for x in p.values()),26)
        self.assertEqual(sum(x["comparison_grade"]=="NO_SAME_ID_IN_SELECTED_MIXED25_TABLE" for x in p.values()),1)
        self.assertEqual(sum(len(x["saved_named_skill_slots"]) for x in p.values()),941)
        self.assertEqual(sum(bool(x["positive_routes"]) for x in p.values()),123)
        self.assertEqual(sum(any(r["instance_pet_flag"]==1 for r in x["positive_routes"]) for x in p.values()),118)
        self.assertEqual(sum(any(r["instance_pet_flag"]==1 and r["level"][0]<=1<=r["level"][1] for r in x["positive_routes"]) for x in p.values()),94)
        self.assertEqual(sum(x["saved_reward_instance_id"] is not None for x in p.values()),36)
        self.assertTrue(all(all(v is None for v in x["formal_fields"].values()) for x in p.values()))
        self.assertTrue(all(not x["official_identity_verified"] and not x["original_pixels_included"] for x in p.values()))
        w=p["TW75-TEMPLATE-1"]
        self.assertEqual(w["original_name"],"烏力")
        self.assertEqual(w["conditional_panel_level1"],[[12,18],[1,2],[1,3],[2,3]])
        self.assertEqual(len(w["positive_routes"]),65)
        self.assertEqual(w["saved_named_skill_slots"][0]["name"],"攻擊")
        self.assertTrue(all("rectangle" in r and "instance_id" in r and "area_source_line" in r for r in w["positive_routes"]))
        self.assertIsNone(w["conditional_panel_total_growth"])

    def test_safe_offline_serialization(self):
        hostile={"name":"</script><script>alert(1)</script>&"}
        encoded=atlas.safe_json(hostile)
        self.assertNotIn("<",encoded)
        self.assertEqual(json.loads(encoded),hostile)
        self.assertIn("connect-src 'none'",atlas.PAGE)
        self.assertEqual(atlas.PAGE.count("__DATA__"),1)

if __name__=="__main__":
    unittest.main()
