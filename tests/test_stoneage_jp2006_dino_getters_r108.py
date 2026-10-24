import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("r108", ROOT / "tools/stoneage_jp2006_dino_getters_r108.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
ORIGINAL = json.loads(mod.PATH.read_text(encoding="utf-8"))

class TestR108(unittest.TestCase):
    def test_clean(self):
        self.assertTrue(mod.verify(copy.deepcopy(ORIGINAL)))

    def reject(self, edit):
        value = copy.deepcopy(ORIGINAL)
        edit(value)
        with self.assertRaises(AssertionError):
            mod.verify(value)

    def test_invent_raw_hash(self):
        self.reject(lambda d: d["source"].__setitem__("actual_raw_html_sha256", "fake"))
    def test_pretend_operator_original(self):
        self.reject(lambda d: d["source"].__setitem__("operator_original_html", "found"))
    def test_invent_npc_name(self):
        self.reject(lambda d: d["records"][1]["npc_names_as_written"].append("GM"))
    def test_invent_npc_coordinates(self):
        self.reject(lambda d: d["records"][1].__setitem__("coordinates", [10,20]))
    def test_invent_species(self):
        self.reject(lambda d: d["records"][2]["eligible_species_names"].append("Unknown"))
    def test_invent_exact_points(self):
        self.reject(lambda d: d["records"][2].__setitem__("tier_point_values", [1,2,3]))
    def test_invent_threshold(self):
        self.reject(lambda d: d["records"][3].__setitem__("point_target_value", 100))
    def test_promote_comparison_algorithm(self):
        self.reject(lambda d: d["records"][3].__setitem__("threshold_comparator_executable", ">"))
    def test_promote_granted_reward(self):
        self.reject(lambda d: d["records"][3].__setitem__("actual_reward_granted", True))
    def test_cross_server_conflation(self):
        self.reject(lambda d: d["records"][3].__setitem__("aggregation_scope", "ALL_SERVERS"))
    def test_invent_handoff_success(self):
        self.reject(lambda d: d["records"][1].__setitem__("successful_handoff_observed", True))
    def test_invent_original_build(self):
        self.reject(lambda d: d["records"][0].__setitem__("client_build", "1999/TW1"))
    def test_delete_unknown_record(self):
        self.reject(lambda d: d["records"].pop())
    def test_early_version_promotion(self):
        self.reject(lambda d: d["records"][0].__setitem__("version_profile", "V1_DIRECT"))
    def test_partial_stage_promotion(self):
        self.reject(lambda d: d["continuation"].__setitem__("stage_a", "ALL_CLOSED"))

if __name__ == "__main__":
    unittest.main()
