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


    def test_postpublication_custody_receipt_immutable(self):
        import hashlib
        receipt_path=P.parents[2]/"research/recovered/STONEAGE-CN2001-WORLD-ROUTES-RECORD-ACCEPTANCE-R96.json"
        rb=receipt_path.read_bytes()
        sha=hashlib.sha1(b"blob "+str(len(rb)).encode()+b"\0"+rb).hexdigest()
        self.assertEqual(sha,"6177f182e1cf257a0302aacde786730f66352ca6")
        r=json.loads(rb.decode("utf-8"))
        self.assertEqual(r["task"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-96")
        self.assertEqual(r["content"]["commit"],"94f08deefbf82da05cba51f9b6699adbfd485deb")
        self.assertEqual(r["docs"]["commit"],"9386c6f3147796b9b1a55c0fbe22c8fe5006437c")
        sb=P.read_bytes()
        self.assertEqual(hashlib.sha1(b"blob "+str(len(sb)).encode()+b"\0"+sb).hexdigest(),r["permanent_derived_source"]["sha1_git_blob"])
        self.assertFalse(r["permanent_derived_source"]["historical_original_html"])
        self.assertFalse(r["permanent_derived_source"]["exact_original_build_verified"])
        self.assertEqual(r["candidate_content_validation"]["run_id"],39961754440)
        self.assertEqual(r["candidate_content_validation"]["job_id"],120441214658)
        self.assertEqual(r["candidate_content_validation"]["test_methods"],11)
        self.assertEqual(r["candidate_content_validation"]["conclusion"],"success")
        cand=r["candidate_docs_validation"]["run_ids"]
        main=r["main_docs_validation"]["run_ids"]
        self.assertEqual((len(cand),len(set(cand)),len(main),len(set(main))),(9,9,11,11))
        self.assertTrue(set(cand).isdisjoint(set(main)))
        self.assertTrue(r["candidate_docs_validation"]["all_success"])
        self.assertTrue(r["main_docs_validation"]["all_success"])
        self.assertEqual(r["main_docs_validation"]["dedicated_run_id"],39962313604)
        self.assertEqual(r["main_docs_validation"]["dedicated_job_id"],120443120286)
        self.assertEqual(r["publication"]["compare_ahead_by"],2)
        self.assertEqual(r["publication"]["compare_behind_by"],0)
        self.assertTrue(r["publication"]["main_fast_forward_non_force"])
        for item in r["historical_prefix"]:
            self.assertTrue(item["old_prefix_retained"])
            self.assertEqual(len(item["old"]),40)
            self.assertEqual(len(item["new"]),40)
        self.assertEqual(len(r["historical_prefix"]),3)
        self.assertEqual(r["ci_artifacts"]["candidate_dedicated_artifact_count"],0)
        self.assertEqual(r["ci_artifacts"]["main_dedicated_artifact_count"],0)
        self.assertFalse(r["ci_artifacts"]["raw_source_html_zip_saved"])
        self.assertFalse(r["ci_artifacts"]["raw_image_zip_saved"])
        self.assertFalse(r["ci_artifacts"]["derived_report_zip_saved"])
        self.assertTrue(all(v is False for k,v in r["claim_boundaries"].items() if k!="overall_restoration_percentage"))
        self.assertIsNone(r["claim_boundaries"]["overall_restoration_percentage"])
        self.assertEqual(r["next"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-97")

if __name__=="__main__":
    unittest.main()
