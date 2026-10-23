"""Negative evidence regression tests for Japan 2003 revival chronology R95."""
import copy
import json
import unittest
from tools.stoneage_jp2003_revival_trade_map_source import P,verify

class JP2003RevivalPressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(P.read_text(encoding="utf-8"))
    def reject(self, mut):
        data=copy.deepcopy(self.d)
        mut(data)
        with self.assertRaises(AssertionError): verify(data)
    def test_source_baseline(self):
        self.assertTrue(verify(self.d))
    def test_new_trade_window_not_1999_original_or_runtime(self):
        self.reject(lambda x:x["version_promotion_guards"].update(original_1999_jss_trade_ui_absent_verified=True))
        self.reject(lambda x:x["version_promotion_guards"].update(original_2003_trade_window_runtime_verified=True))
    def test_reported_trade_not_certified(self):
        self.reject(lambda x:x["claims"][5].update(reported_state="LIVE_TRANSACTION_TESTED"))
        self.reject(lambda x:x["version_promotion_guards"].update(same_build_trade_protocol_or_ack_verified=True))
    def test_later_maps_and_avatars_not_december_launch(self):
        self.reject(lambda x:x["claims"][6].update(reported_state="DEPLOYED_IN_BETA"))
        self.reject(lambda x:x["version_promotion_guards"].update(new_maps_in_december_beta_verified=True))
    def test_betastart_announcement_not_execution(self):
        self.reject(lambda x:x["version_promotion_guards"].update(beta_started_on_dec16_directly_observed=True))
        self.reject(lambda x:x["ordered_announcement_dates"][1].update(reported="2003-12-16"))
    def test_original_jss_and_tw10_isolated(self):
        self.reject(lambda x:x["version_promotion_guards"].update(original_1999_jss_and_2003_jp_same_build=True))
        self.reject(lambda x:x["version_promotion_guards"].update(tw10_interaction_semantics_promoted=True))
    def test_korean_and_riding_only_speculation(self):
        self.reject(lambda x:x["claims"][2].update(reported_state="COMPANY_CONFIRMED"))
        self.reject(lambda x:x["version_promotion_guards"].update(player_pet_riding_in_2003_build_verified=True))
    def test_no_new_gallery_credit_or_jpeg_replay(self):
        self.reject(lambda x:x["cross_reference"].update(gallery_extra_images_fetched_in_R95=True))
        self.reject(lambda x:x["cross_reference"].update(trade_window_observable_in_first_two_R63_frames=True))
    def test_source_not_immaculately_authenticated(self):
        self.reject(lambda x:x["sources"][0].update(raw_html_bytes_authenticated=True))
        self.reject(lambda x:x["sources"][2].update(original_build_sha="fake"))
    def test_stage_gates_and_extra_fields(self):
        self.reject(lambda x:x["acceptance"].update(stage_a_accepted=True))
        self.reject(lambda x:x["acceptance"].update(overall_restoration_percentage=100))
        self.reject(lambda x:x.update(original_trade_transaction_count=1))


    def test_referenced_r63_evidence_is_not_silently_replaced(self):
        import hashlib
        from pathlib import Path
        path=P.parents[2] / "docs/specs/STONEAGE-JP2003-BATTLE-FIELD-VISUAL-SOURCE-R1.md"
        raw=path.read_bytes()
        gitsha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
        self.assertEqual(gitsha,"63b274f5bc8e1508eb1e8f9dfe2a1e27544ea093")
        self.assertFalse(self.d["cross_reference"]["trade_window_observable_in_first_two_R63_frames"])
    def test_published_r95_ci_and_immutable_derived_source_receipt(self):
        import hashlib
        from pathlib import Path
        receipt=P.parents[2] / "research/recovered/STONEAGE-JP2003-REVIVAL-TRADE-MAP-ACCEPTANCE-R95.json"
        raw=receipt.read_bytes()
        digest=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
        self.assertEqual(digest,"28d3285fc9c0c47c388b763686d4fb45e77c545c")
        info=json.loads(raw.decode("utf-8"))
        self.assertEqual(info["original_source_derived_json"]["git_blob_sha1"],
                         "c491542dbeb7523169615482bfbfefff728ea9f5")
        self.assertEqual(info["original_source_derived_json"]["utf8_bytes"], P.stat().st_size)
        self.assertEqual(info["candidate_dedicated_source_ci"]["run_id"], 39958828076)
        self.assertEqual(info["candidate_dedicated_source_ci"]["test_methods"], 10)
        self.assertEqual(info["main_publication_ci"]["dedicated_run_id"], 39959563014)
        cand=info["candidate_continuity_ci"]["run_ids"]
        main=info["main_publication_ci"]["run_ids"]
        self.assertEqual((len(cand),len(set(cand))), (9,9))
        self.assertEqual((len(main),len(set(main))), (11,11))
        self.assertTrue(set(cand).isdisjoint(set(main)))
        self.assertTrue(info["candidate_continuity_ci"]["all_success"])
        self.assertTrue(info["main_publication_ci"]["all_success"])
        self.assertFalse(info["artifact_check"]["source_original_html_zip_present"])
        self.assertFalse(info["artifact_check"]["source_original_jpeg_zip_present"])
        self.assertEqual(info["artifact_check"]["main_dedicated_artifact_count"],0)
        self.assertTrue(all(z["full_prefix_preserved"] for z in info["document_preservation"]))
        self.assertFalse(info["negative_limits"]["trade_window_action_ack_verified"])
        self.assertFalse(info["negative_limits"]["stage_a_accepted"])
        self.assertIsNone(info["negative_limits"]["overall_restoration_percentage"])
        self.assertEqual(info["next"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-96")

if __name__=="__main__":
    unittest.main()
