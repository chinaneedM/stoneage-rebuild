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

if __name__=="__main__":
    unittest.main()
