"""Negative mutation controls for June6 alleged VIP disc source-only evidence."""
import copy
import json
import unittest
from tools.stoneage_tw80_vip_june6_source_gate import LEDGER, validate

class VipJune6GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(LEDGER.read_text(encoding="utf-8"))

    def reject(self, change):
        d = copy.deepcopy(self.doc)
        change(d)
        with self.assertRaises(ValueError):
            validate(d)

    def test_valid_source_only(self):
        self.assertEqual(validate(self.doc),"TW80_VIP_JUNE6_REPOST_BOUNDARY_PASS")
    def test_reject_headline_drift(self):
        self.reject(lambda d:d["lead"].update(headline="Official 8.0 installer available"))
    def test_reject_pretend_2005_notice(self):
        self.reject(lambda d:d["lead"].update(original_2005_operator_notice_retrieved=True))
    def test_reject_official_promotion(self):
        self.reject(lambda d:d["lead"].update(status="OFFICIAL_2005_CONFIRMED"))
    def test_reject_invented_sha(self):
        self.reject(lambda d:d["lead"].update(original_installer_sha256="a"*64))
    def test_reject_imaged_disc(self):
        self.reject(lambda d:d["lead"].update(original_disc_image_retrieved=True))
    def test_reject_missing_parent(self):
        self.reject(lambda d:d["lineage"].pop(0))
    def test_reject_false_parent_retrieval(self):
        self.reject(lambda d:d["lineage"][0].update(retrieved_original=True))
    def test_reject_renamed_parent(self):
        self.reject(lambda d:d["lineage"][0].update(url="https://wayi.com.tw/official-news"))
    def test_reject_independent_copy(self):
        self.reject(lambda d:d["lineage"][1].update(independently_verified=True))
    def test_reject_vip_date_vs_release(self):
        self.reject(lambda d:d["channels"][1].update(date="2005-06-08"))
    def test_reject_june4_giveaway_proven(self):
        self.reject(lambda d:d["channels"][0].update(physical_disc_authenticated=True))
    def test_reject_june6_delivery_proven(self):
        self.reject(lambda d:d["claims"].update(claimed_posting_proves_mailing=True))
    def test_reject_same_discs_asserted(self):
        self.reject(lambda d:d["claims"].update(vip_disc_identical_to_event_or_retail_disc=True))
    def test_reject_unverified_pet(self):
        self.reject(lambda d:d["claims"].update(original_pet_packet127_verified=True))
    def test_reject_early_era_promoted(self):
        self.reject(lambda d:d["claims"].update(taiwan10_or_jss1999_promoted=True))
    def test_reject_engine_transition(self):
        self.reject(lambda d:d["claims"].update(engine_transition=True))
    def test_reject_pressure(self):
        self.reject(lambda d:d["pressure"].update(open=17,bounded_closed=2466))
    def test_reject_new_unreviewed_claim(self):
        self.reject(lambda d:d["claims"].update(disc_mailing_confirmed=False))

if __name__ == "__main__":
    unittest.main()
