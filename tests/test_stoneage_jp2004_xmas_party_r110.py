import copy, json, importlib.util, unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("r110",root/"tools/stoneage_jp2004_xmas_party_r110.py")
r110=importlib.util.module_from_spec(spec)
spec.loader.exec_module(r110)
orig=json.loads(r110.PATH.read_text(encoding="utf-8"))

class TestR110(unittest.TestCase):
    def test_original(self): self.assertTrue(r110.verify(copy.deepcopy(orig)))
    def rejected(self,change):
        d=copy.deepcopy(orig);change(d)
        with self.assertRaises((AssertionError, KeyError, TypeError)):
            r110.verify(d)
    def test_fake_source_bytes(self): self.rejected(lambda d:d["sources"][0].__setitem__("actual_html_bytes",123))
    def test_fake_operator_first_party(self): self.rejected(lambda d:d["sources"][1].__setitem__("first_party_authorship",True))
    def test_invent_archive_sha(self): self.rejected(lambda d:d["sources"][1].__setitem__("actual_html_sha256","f"*64))
    def test_pretend_direct_webpage(self): self.rejected(lambda d:d["source_relationship"].__setitem__("first_party_webpage_access","ARCHIVED"))
    def test_operator_label_collapse(self): self.rejected(lambda d:d["source_relationship"].__setitem__("operator_identity_fully_reconciled",True))
    def test_build_projection(self): self.rejected(lambda d:d["source_relationship"].__setitem__("original_taiwan_v1_0_equivalence",True))
    def test_no_adult_gate(self): self.rejected(lambda d:d["observations"]["christmas"].__setitem__("s1_required_quest",None))
    def test_extra_village(self): self.rejected(lambda d:d["observations"]["christmas"]["s2_four_villages"].append("キヌイ"))
    def test_made_up_reward(self): self.rejected(lambda d:d["observations"]["christmas"].__setitem__("reward_item_ids",[12]))
    def test_santa_identity_join(self): self.rejected(lambda d:d["observations"]["christmas"].__setitem__("independent_identification_of_santa_and_santa_girl_same_entity",True))
    def test_unrestricted_inference(self): self.rejected(lambda d:d["records"][2].__setitem__("free_for_everyone_verified",True))
    def test_npc_id(self): self.rejected(lambda d:d["records"][0].__setitem__("original_npc_id",9))
    def test_invent_four_maps(self): self.rejected(lambda d:d["records"][1].__setitem__("not_four_new_maps",False))
    def test_misstate_confusion(self): self.rejected(lambda d:d["observations"]["combat_patch"].__setitem__("confusion_damage",1))
    def test_wrong_damage(self): self.rejected(lambda d:d["records"][3].__setitem__("reported_non_confused_damage",2))
    def test_original_v1_promotion(self): self.rejected(lambda d:d["records"][3].__setitem__("same_as_TW10_runtime",True))
    def test_new_year_effect(self): self.rejected(lambda d:d["records"][4].__setitem__("fortune_effect_on_state","PLUS_LUCK"))
    def test_unified_operator(self): self.rejected(lambda d:d["records"][5].__setitem__("unified_company_role","GAMANIA"))
    def test_historical_completion(self): self.rejected(lambda d:d["continuation"].__setitem__("overall_restoration_percent",100))
    def test_missing_row(self): self.rejected(lambda d:d["records"].pop())

if __name__=="__main__": unittest.main()
