"""R46 source report/original NPC interpretation adversarial offline tests."""
from copy import deepcopy
import json
import unittest
from tools.stoneage_healing_npc_material_r46 import (
  verified_source_bytes, material_from_source, replay,validate
)

class HealingNPCSourceReplays(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=verified_source_bytes()
        cls.source=json.loads(cls.raw)
    def test_original_derived_replay(self):
        self.assertEqual(replay()["status"],"PASS")
    def test_all_actual_selected_names_and_corners(self):
        m=material_from_source(self.raw)
        records=m["bounded_first_three_creation_rows"]
        self.assertEqual([r["name_original_cp950_big5"] for r in records],["家族小護士"]*3)
        self.assertEqual([r["floorid_original"] for r in records],[1041,2031,3031])
        self.assertEqual([r["borncorner_original_four_ints"] for r in records],[[4,8,4,8],[13,8,13,8],[2,9,2,9]])
        self.assertEqual(m["source_file_original_creation_blocks"],4)
        self.assertIs(m["fourth_create_block_fields_analyzed_this_package"],False)
        self.assertEqual(m["official_tw10_npc_authenticated"],0)
    def mutate_fail(self,f):
        d=deepcopy(self.source)
        f(d)
        with self.assertRaises(ValueError):
            validate(d)
    def test_cannot_promote_run_or_same_build(self):
        self.mutate_fail(lambda d:d.__setitem__("official_tw10_npc_authenticated",1))
        self.mutate_fail(lambda d:d["material"].__setitem__("npc_function_bound_to_healer_runtime_proven",True))
        self.mutate_fail(lambda d:d["material"].__setitem__("same_build_with_taiwan_1_0_proven",True))
    def test_cannot_change_original_name(self):
        self.mutate_fail(lambda d:d["material"]["selected_creation_occurrences"][0]["block_field_fingerprints"][-2].__setitem__("original_name","家族醫院"))
    def test_cannot_rewrite_origin_or_fourth_block(self):
        self.mutate_fail(lambda d:d.__setitem__("origin_class","BASE_GAME_QUEST"))
        self.mutate_fail(lambda d:d["material"].__setitem__("original_creation_block_count",3))
    def test_cannot_delete_third_or_duplicate_records(self):
        self.mutate_fail(lambda d:d["material"]["selected_creation_occurrences"].pop())
        self.mutate_fail(lambda d:d["material"]["selected_creation_occurrences"][1].__setitem__("source_block_order",0))
    def test_exact_original_geometry(self):
        self.mutate_fail(lambda d:next(x for x in d["material"]["selected_creation_occurrences"][2]["block_field_fingerprints"] if x["key"]=="borncorner").__setitem__("integer_values",[0,0,0,0]))
    def test_original_declared_token_not_executed_function(self):
        self.mutate_fail(lambda d:next(x for x in d["material"]["selected_creation_occurrences"][0]["block_field_fingerprints"] if x["key"]=="enemy").__setitem__("declared_reference_token","NPCHealer"))
        self.mutate_fail(lambda d:d["material"]["selected_creation_occurrences"][0].__setitem__("original_service_executed",True))
    def test_source_custody_retains_strict_http206_accounting(self):
        self.mutate_fail(lambda d:d["receipt"].__setitem__("range_requests",183))
        self.mutate_fail(lambda d:d["receipt"]["range_receipts"][0].__setitem__("sha256","0"*64))
    def test_source_proprietary_body_never_written(self):
        self.mutate_fail(lambda d:d["material"].__setitem__("original_dialogue_or_script_body_published",True))
        self.mutate_fail(lambda d:d["material"]["selected_creation_occurrences"][0]["block_field_fingerprints"][0].__setitem__("raw_value","copyrighted"))

if __name__=="__main__":
    unittest.main()
