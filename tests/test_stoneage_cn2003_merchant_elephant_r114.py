#!/usr/bin/env python3
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from stoneage_cn2003_merchant_elephant_r114 import validate

D=json.loads((ROOT/"research/recovered/STONEAGE-CN2003-MERCHANT-ELEPHANT-R114.json").read_text(encoding="utf-8"))

class R114Boundaries(unittest.TestCase):
    def bad(self, mutation):
        d=copy.deepcopy(D)
        mutation(d)
        with self.assertRaises((AssertionError,ValueError,KeyError,TypeError)):
            validate(d)

    def test_valid(self): self.assertTrue(validate(D))
    def test_date(self): self.bad(lambda d:d["sources"][0].update(publication_date="2002-06-30"))
    def test_fake_source_bytes(self): self.bad(lambda d:d["sources"][0].update(original_article_html_sha256="assumed"))
    def test_operator_master(self): self.bad(lambda d:d["sources"][0].update(official_server_implementation_authenticated=True))
    def test_sina_index_not_independent(self): self.bad(lambda d:d["sources"][1].update(independent_contemporary_server_eyewitness=True))
    def test_2004_index_not_original_build(self): self.bad(lambda d:d["sources"][1].update(original_2003_release_build_authenticated=True))
    def test_later_repost_not_original(self): self.bad(lambda d:d["sources"][2].update(independent_original_2003_witness=True))
    def test_no_tw10(self): self.bad(lambda d:d["edition"].update(jss1999_or_tw10_identity_proven=True))
    def test_no_exact_build(self): self.bad(lambda d:d["edition"].update(confirmed_original_client_build="6.0.0"))
    def test_no_quest_master(self): self.bad(lambda d:d["edition"].update(original_operator_quest_master_proven=True))
    def test_level_55_only_recommended(self): self.bad(lambda d:d["quest"].update(level55="REQUIRED"))
    def test_feathers_only_recommended(self): self.bad(lambda d:d["quest"].update(feather_status="MANDATORY_TWO"))
    def test_npc_original_id_unknown(self): self.bad(lambda d:d["quest"]["request_location"].update(original_npc_id=54))
    def test_coordinate_preserved(self): self.bad(lambda d:d["quest"]["request_location"].update(coordinate_original="54,76"))
    def test_npc_variant_preserved(self): self.bad(lambda d:d["quest"].update(npc_return_spelling="盖落比"))
    def test_not_proven_same_id(self): self.bad(lambda d:d["quest"].update(original_npc_identity_equivalence_verified=True))
    def test_target_level(self): self.bad(lambda d:d["quest"]["capture_location"].update(target_level_reported=55))
    def test_no_original_pet_id(self): self.bad(lambda d:d["quest"]["capture_location"].update(original_pet_species_id=2345))
    def test_no_server_item_consumption(self): self.bad(lambda d:d["quest"].update(original_cargo_consumption_transaction_verified=True))
    def test_loyalty_10_not_formula(self): self.bad(lambda d:d["quest"].update(actual_original_loyalty_effect_verified=True))
    def test_original_item_id_unknown(self): self.bad(lambda d:d["quest"].update(original_reward_item_id=7))
    def test_hp_tip_not_capture_formula(self): self.bad(lambda d:d["quest"].update(capture_advice_hp_below_100="FORMULA_PROVEN"))
    def test_no_quest_save_field(self): self.bad(lambda d:d["quest"].update(original_save_state_fields=["flag"] ))
    def test_images_not_authenticated(self): self.bad(lambda d:d["evidence_boundary"].update(original_nine_image_bytes_captured=True))
    def test_no_source_visual_join(self): self.bad(lambda d:d["evidence_boundary"].update(same_build_spr_or_npc_visual_join=123))
    def test_no_server_runtime(self): self.bad(lambda d:d["evidence_boundary"].update(original_server_script_or_runtime_trace="PASS"))
    def test_no_percent(self): self.bad(lambda d:d["evidence_boundary"].update(overall_restoration_percentage=98))
    def test_no_entity_promotion(self): self.bad(lambda d:d.update(archive_record_not_original_entity_count=False))

if __name__=="__main__": unittest.main()
