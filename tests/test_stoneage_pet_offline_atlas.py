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

    def test_safe_offline_serialization(self):
        hostile={"name":"</script><script>alert(1)</script>&"}
        encoded=atlas.safe_json(hostile)
        self.assertNotIn("<",encoded)
        self.assertEqual(json.loads(encoded),hostile)
        self.assertIn("connect-src 'none'",atlas.PAGE)
        self.assertEqual(atlas.PAGE.count("__DATA__"),1)

if __name__=="__main__":
    unittest.main()
