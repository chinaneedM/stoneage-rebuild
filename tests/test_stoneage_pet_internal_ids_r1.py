"""Independent immutable PET catalog numbers and source observation IDs; forbid fake official promotions."""
import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
class PETIndependentIdentifierContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=load("research/pets/PET-ID-REGISTRY-R1.json")
        cls.progress=load("research/pets/PET-PROGRESS-R1.json")
        cls.profile=load("research/pets/profiles/TW10-G100250-WULI.json")
        cls.source=load("research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
        cls.names=load("research/recovered/STONEAGE-PET126W-TW10-CN50-ALL-124-ORIGINAL-PC-NAME-VARIANTS-R1.json")
    def test_stable_separate_catalog_and_source_ids(self):
        r=self.registry
        self.assertEqual(r["policy"]["next_unassigned_catalog_pet_id"],"PET-000002")
        self.assertEqual(r["counts"]["assigned_catalog_pet_ids"],1)
        self.assertEqual(r["counts"]["source_observation_rows"],124)
        self.assertEqual(r["counts"]["unassigned_source_observations"],123)
        self.assertIsNone(r["counts"]["global_original_classic_pc_pet_count"])
        cats=r["catalog_entries"];self.assertEqual(len(cats),1)
        self.assertEqual(cats[0]["catalog_pet_id"],"PET-000001")
        self.assertFalse(cats[0]["historically_verified_official_species"])
        self.assertIsNone(cats[0]["official_server_pet_id"])
        self.assertEqual(cats[0]["observations"],["OBS-TW10-0001"])
        self.assertEqual(self.profile["profile_id"],cats[0]["catalog_pet_id"])
        self.assertEqual(self.profile["internal_id_system"]["source_observation_ids"],cats[0]["observations"])
        self.assertEqual(self.profile["internal_id_system"]["legacy_key"],"TW10-G100250")
        self.assertEqual(self.progress["existing_details"][0]["profile_id"],"PET-000001")
        self.assertEqual(self.progress["per_pet_profile_counts"]["individual_detailed_profiles"],1)
    def test_124_observations_mirror_exact_tw10_source_not_124_species(self):
        r=self.registry;observations=r["source_observations"]
        self.assertEqual(len(observations),124)
        self.assertEqual(len({x["observation_id"] for x in observations}),124)
        self.assertEqual(len({x["source_key"] for x in observations}),124)
        self.assertEqual(len({x["source_graphic_number"] for x in observations}),124)
        self.assertEqual(len({x["assigned_catalog_pet_id"] for x in observations if x["assigned_catalog_pet_id"]}),1)
        for i,(o,s,n) in enumerate(zip(observations,self.source["records"],self.names["records"])):
            self.assertEqual(o["observation_id"],"OBS-TW10-"+str(i+1).zfill(4))
            self.assertEqual(o["source_album_ordinal"],i)
            self.assertEqual(o["source_key"],"TW10-G"+str(s["graphic_number"]))
            self.assertEqual(o["client_name_literal"],s["name_as_written"])
            self.assertEqual(o["source_graphic_number"],s["graphic_number"])
            self.assertEqual(o["source_row_sha256"],s["source_row_sha256"])
            self.assertEqual(o["source_spr_segment_sha256"],s["spr_original_segment_sha256"])
            self.assertEqual(o["cn50_preserved_compiled_name_corroboration"],n["cn50_preserved_compiled_literal"])
            self.assertFalse(o["official_live_release_verified"])
            self.assertFalse(o["cn50_qualified_as_official_pressing"])
            self.assertEqual(o["assigned_catalog_pet_id"],"PET-000001" if i==0 else None)
            self.assertNotEqual(o["observation_id"],o["assigned_catalog_pet_id"])
        self.assertFalse(r["boundaries"]["do_not_count_album_rows_as_official_live_species"] is False)
        self.assertTrue(r["boundaries"]["do_not_sum_tw10_and_cn50_entries"])
        self.assertEqual(r["cross_version_identity_relations"],[])
    def test_progress_and_public_rules_align(self):
        p=self.progress; r=self.registry
        self.assertEqual(p["internal_id_registry"]["allocated_pet_catalog_ids"],len(r["catalog_entries"]))
        self.assertEqual(p["internal_id_registry"]["tw10_source_observation_ids"],len(r["source_observations"]))
        self.assertEqual(p["internal_id_registry"]["source_observations_without_pet_catalog_number"],123)
        self.assertEqual(p["internal_id_registry"]["next_free_catalog_id"],"PET-000002")
        self.assertFalse(self.profile["actual_official_pet_identity"]["official_living_pet_release_proven"])
        self.assertIsNone(self.profile["actual_official_pet_identity"]["source_pet_id"])
        self.assertEqual(r["boundaries"]["current_state_original_sha"],p["boundaries"]["current_state_immutable_blob"])
        idx=(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8")
        self.assertIn("PET-000001",idx);self.assertIn("OBS-TW10-0124",idx)
        self.assertEqual(len(re.findall(r"^\| \d+ \| .*? \| OBS-TW10-\d{4} \|",idx,re.M)),124)
        self.assertIn("PET-000001",(ROOT/"docs/pets/TW10-G100250-WULI.md").read_text(encoding="utf-8"))
        self.assertIn("永久",(ROOT/"docs/pets/ID-SCHEME.md").read_text(encoding="utf-8"))
if __name__=="__main__":unittest.main()
