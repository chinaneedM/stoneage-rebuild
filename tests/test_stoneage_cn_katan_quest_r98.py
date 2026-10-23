"""R98 source assertions and adversarial negative evidence guards."""
import copy
import json
import unittest
from tools.stoneage_cn_katan_quest_r98 import P,verify

class R98KatanContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(P.read_text(encoding="utf-8"))
    def bad(self, fn):
        x=copy.deepcopy(self.d);fn(x)
        with self.assertRaises(AssertionError):verify(x)
    def test_positive(self):
        self.assertTrue(verify(self.d))
    def test_no_backdated_official_build(self):
        self.bad(lambda d:d["sources"][0].update(original_game_build="JSS1999"))
        self.bad(lambda d:d["sources"][1].update(original_publication_bytes_verified=True))
    def test_dont_unify_south_coordinates(self):
        self.bad(lambda d:d["npc_search"].update(s2_player_search_south_coordinate=198))
        self.bad(lambda d:d["npc_search"].update(exact_spawn_locations=[[259,198]]))
    def test_first_fish_order(self):
        self.bad(lambda d:d["quest"]["fish_stage"].update(first_pair=["加格","加克拉"]))
    def test_second_bird_order(self):
        self.bad(lambda d:d["quest"]["bird_stage"].update(second_pair=["奇宝","霍尔克"]))
    def test_level35_is_advice_not_gate(self):
        self.bad(lambda d:d["quest"].update(suggested_level_is_hard_server_gate=True))
    def test_unresolved_reissue_disagreement(self):
        self.bad(lambda d:d["conflicts"][2].update(resolved=True))
        self.bad(lambda d:d["conflicts"][2].update(server_recovery_contract="guaranteed reissue"))
    def test_ring_names_not_same_id(self):
        self.bad(lambda d:d["quest"]["bird_stage"].update(intermediate_item_s1="火鸡的戒指"))
        self.bad(lambda d:d["quest"]["bird_stage"].update(item_equivalence_proven=True))
    def test_intermediate_fish_ring_not_safely_named(self):
        self.bad(lambda d:d["quest"]["fish_stage"].update(intermediate_item_s1="火鸡的戒指"))
    def test_no_server_ack(self):
        self.bad(lambda d:d["quest"]["fish_stage"].update(original_give_back_transaction_proven=True))
        self.bad(lambda d:d["quest"]["bird_stage"].update(original_second_cycle_execution_proven=True))
    def test_no_screenshot_authenticity(self):
        self.bad(lambda d:d["illustrated_guide"].update(article_specific_image_bytes_verified=True))
        self.bad(lambda d:d["illustrated_guide"].update(npc_pixels_identified=True))
    def test_original_pet_ids_absent(self):
        self.bad(lambda d:d["npcs"][0].update(native_npc_id=108))
    def test_do_not_promote_reprints(self):
        self.bad(lambda d:d["dedup"].update(modern_reposts_counted_as_independent_sources=True))
    def test_no_stage_b_or_percent(self):
        self.bad(lambda d:d["publication"].update(stage_a_closed=True))
        self.bad(lambda d:d["publication"].update(overall_restoration_percent=98))
    def test_no_injected_authority_field(self):
        self.bad(lambda d:d.update(original_server_execution="pass"))

if __name__=="__main__":unittest.main()
