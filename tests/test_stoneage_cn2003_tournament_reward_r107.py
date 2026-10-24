import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("r107", ROOT/"tools/stoneage_cn2003_tournament_reward_r107.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
original = json.loads(mod.PATH.read_text(encoding="utf-8"))

class TestR107(unittest.TestCase):
    def test_original(self):
        self.assertTrue(mod.verify(copy.deepcopy(original)))

    def rejected(self, edit):
        data = copy.deepcopy(original)
        edit(data)
        with self.assertRaises(AssertionError):
            mod.verify(data)

    def test_provenance_promotion_rejected(self):
        self.rejected(lambda d: d["source"].__setitem__("actual_raw_html_sha256","invented"))

    def test_original_npc_id_rejected(self):
        self.rejected(lambda d: d["records"][0].__setitem__("npc_original_id",123))

    def test_universal_reward_rejected(self):
        self.rejected(lambda d: d["records"][2].__setitem__("eligibility_predicate",True))

    def test_success_promotion_rejected(self):
        self.rejected(lambda d: d["records"][2].__setitem__("real_transaction_observed",True))

    def test_deadline_conflict_erasure_rejected(self):
        self.rejected(lambda d: d["records"][3].__setitem__("deadline_conflict","RESOLVED"))

    def test_suppressed_alternative_rejected(self):
        self.rejected(lambda d: d["records"][3]["site_deadline_claims"].pop())

    def test_early_version_promotion_rejected(self):
        self.rejected(lambda d: d["records"][1].__setitem__("version_profile","V1_DIRECT"))

    def test_reward_species_promotion_rejected(self):
        self.rejected(lambda d: d["records"][1].__setitem__("pet_species_id",9))

if __name__ == "__main__":
    unittest.main()
