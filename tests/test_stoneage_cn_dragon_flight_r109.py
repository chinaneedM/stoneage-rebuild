import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("r109", ROOT/"tools/stoneage_cn_dragon_flight_r109.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
original = json.loads(mod.PATH.read_text(encoding="utf-8"))

class TestR109(unittest.TestCase):
    def test_original(self):
        self.assertTrue(mod.verify(copy.deepcopy(original)))
    def rejected(self, change):
        d = copy.deepcopy(original)
        change(d)
        with self.assertRaises((AssertionError, KeyError, IndexError)):
            mod.verify(d)
    def test_fake_source_sha(self):
        self.rejected(lambda d: d["sources"][0].__setitem__("raw_html_sha256","fabricated"))
    def test_fake_archive(self):
        self.rejected(lambda d: d["sources"][1].__setitem__("archival_capture","fake"))
    def test_operator_promotion(self):
        self.rejected(lambda d: d["sources"][0].__setitem__("provenance_class","OPERATOR_PRIMARY"))
    def test_build_promotion(self):
        self.rejected(lambda d: d["version_constraints"].__setitem__("s2_title_claim_is_build_proof",True))
    def test_early_promotion(self):
        self.rejected(lambda d: d["version_constraints"].__setitem__("early_taiwan_1_0_lineage_proven",True))
    def test_collapse_level(self):
        self.rejected(lambda d: d["claim_crosswalk"]["required_levels"].__setitem__("shared_runtime_threshold",80))
    def test_erase_three(self):
        self.rejected(lambda d: d["claim_crosswalk"]["flyer_delivery_count"]["S1_three_claims"].clear())
    def test_erase_one(self):
        self.rejected(lambda d: d["claim_crosswalk"]["flyer_delivery_count"]["S1_one_claims"].clear())
    def test_claim_one_resolved(self):
        self.rejected(lambda d: d["claim_crosswalk"]["flyer_delivery_count"].__setitem__("S1_actual_consumption",1))
    def test_apply_later_rules_earlier(self):
        self.rejected(lambda d: d["claim_crosswalk"]["flyer_delivery_count"].__setitem__("cross_version_retroactive_resolution",True))
    def test_fake_npc_id(self):
        self.rejected(lambda d: d["records"][0].__setitem__("original_npc_id",123))
    def test_claim_caption_pixels(self):
        self.rejected(lambda d: d["records"][4].__setitem__("caption_visual_acquired",True))
    def test_pet_master_promotion(self):
        self.rejected(lambda d: d["records"][5].__setitem__("all_original_species_ids",[1,2,3,4]))
    def test_fake_server_script(self):
        self.rejected(lambda d: d["records"][7].__setitem__("server_state_machine",{"final":"DONE"}))
    def test_fake_travel(self):
        self.rejected(lambda d: d["records"][8].__setitem__("actual_travel_proven",True))
    def test_canon_promotion(self):
        self.rejected(lambda d: d["records"][9].__setitem__("official_canonical_status","FACT"))
    def test_wrong_fare(self):
        self.rejected(lambda d: d["claim_crosswalk"]["transport"].__setitem__("S1_reported_repeat_fare_stone",100000))
    def test_false_completion(self):
        self.rejected(lambda d: d["continuation"].__setitem__("overall_restoration_percent",100))
    def test_missing_record(self):
        self.rejected(lambda d: d["records"].pop())
    def test_identity_merge(self):
        self.rejected(lambda d: d["records"][0].__setitem__("game_ids",[1]))

if __name__ == "__main__":
    unittest.main()
