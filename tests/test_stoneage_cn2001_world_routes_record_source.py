"""R96 independent source-contract boundary regressions."""
import copy
import json
import unittest
from tools.stoneage_cn2001_world_routes_record_source import P,verify

class R96WorldRouteRecords(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(P.read_text(encoding="utf-8"))
    def reject(self, fn):
        v=copy.deepcopy(self.d);fn(v)
        with self.assertRaises(AssertionError):verify(v)
    def test_source_pinned(self):
        self.assertTrue(verify(self.d))
    def test_nonoriginal_webpage(self):
        self.reject(lambda d:d["sources"][0].update(original_html_authenticated=True))
        self.reject(lambda d:d["sources"][1].update(exact_game_build="TW1.0"))
    def test_original_stoneage_map_not_inferred(self):
        self.reject(lambda d:d["geography"].update(original_map_ids=[1,2,3,4]))
        self.reject(lambda d:d["geography"].update(passage_endpoints_identified=True))
    def test_island_and_birthplace_not_projected(self):
        self.reject(lambda d:d["geography"]["islands"].reverse())
        self.reject(lambda d:d["birthplaces"][0].update(island="北岛"))
    def test_player_recommendations_not_gates(self):
        self.reject(lambda d:d["suggested_routes"][0].update(strict_game_gate=True))
        self.reject(lambda d:d["suggested_routes"][1]["stops"].reverse())
    def test_first_meat_record_not_generic(self):
        self.reject(lambda d:d["statue_record_claims"][2].update(all_statues_same_meat=True))
        self.reject(lambda d:d["statue_record_claims"][2].update(count=1))
    def test_record_is_not_save_ack(self):
        self.reject(lambda d:d["statue_record_claims"][1].update(actual_save_reentry_trace=True))
        self.reject(lambda d:d["statue_record_claims"][3].update(entire_game_has_no_other_record_points=True))
    def test_pass_cost_not_every_passage(self):
        self.reject(lambda d:d["transport"].update(all_three_passages_same_gate=True))
        self.reject(lambda d:d["transport"].update(original_pass_item_id=300))
    def test_cave_status_not_silent_repair(self):
        self.reject(lambda d:d["elemental_caves"][3].update(reported_status="称已开放"))
        self.reject(lambda d:d["elemental_caves"][0].update(original_operation_log_verified=True))
    def test_cross_version_and_deployment_blocked(self):
        self.reject(lambda d:d["cross_reference"].update(same_version_as_r95_jp2003_verified=True))
        self.reject(lambda d:d["evidence_guards"].update(s1_cave_status_server_deployment_verified=True))
    def test_stage_unchanged(self):
        self.reject(lambda d:d["publication"].update(stage_a_closed=True))
        self.reject(lambda d:d["publication"].update(overall_restoration_percent=100))
        self.reject(lambda d:d.update(original_server_map_ids=[200,300]))

if __name__=="__main__":
    unittest.main()
