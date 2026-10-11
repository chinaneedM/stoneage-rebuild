"""Mutation-driven tests for cross-region/era filename misidentification."""
import copy
import json
import unittest

from tools.stoneage_tw80_late_carrier_quarantine import LEDGER, validate


class CarrierQuarantineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid = json.loads(LEDGER.read_text(encoding="utf-8"))

    def reject(self, change):
        data = copy.deepcopy(self.valid)
        change(data)
        with self.assertRaises(ValueError):
            validate(data)

    def test_accepted_source_only_negative_controls(self):
        self.assertEqual(validate(self.valid), "TW80_LATE_CARRIER_NEGATIVE_CONTROLS_PASS")

    def test_source_swap_is_not_allowed(self):
        self.reject(lambda d: d["leads"][0].update(source="https://download.wayi.com.tw/"))

    def test_2007_third_party_ip_not_2005_taiwan_host(self):
        self.reject(lambda d: d["leads"][0].update(historical_url="https://download.wayi.com.tw/StoneAge8.0setup.exe"))

    def test_2007_wrong_date(self):
        self.reject(lambda d: d["leads"][0].update(source_date="2005-06-08"))

    def test_region_reclassification(self):
        self.reject(lambda d: d["leads"][0].update(region_evidence="TAIWAN_WAYI_2005_OFFICIAL"))

    def test_reused_name_no_binary_identity(self):
        self.reject(lambda d: d["assertions"].update(matching_filename_proves_same_binary=True))

    def test_private_patch_is_not_clean(self):
        self.reject(lambda d: d["assertions"].update(post_install_community_patching_preserves_clean_snapshot=True))

    def test_one_late_candidate_not_official(self):
        self.reject(lambda d: d["leads"][1].update(original_publisher_binary_verified=True))

    def test_no_claimed_sha(self):
        self.reject(lambda d: d["leads"][2].update(sha256="a" * 64))

    def test_no_2016_sourceforge_retro_dating(self):
        self.reject(lambda d: d["leads"][2].update(source_date="2005-06-08"))

    def test_no_2016_original_binary_promotion(self):
        self.reject(lambda d: d["assertions"].update(sourceforge_2016_source_is_2005_taiwan_client=True))

    def test_no_official_8_0_admission(self):
        self.reject(lambda d: d["assertions"].update(official_taiwan_2005_8_0_binary_admitted=True))

    def test_no_native_packet_admission(self):
        self.reject(lambda d: d["assertions"].update(genuine_paired_pet_opcode127_runtime_admitted=True))

    def test_no_early_feature_promotion(self):
        self.reject(lambda d: d["assertions"].update(early_jss1999_or_tw10_pet_membership_admitted=True))

    def test_pressure_kept_open(self):
        self.reject(lambda d: d["pressure"].update(open=17, bounded_closed=2466))

    def test_not_even_fake_payload_retrieval(self):
        self.reject(lambda d: d["leads"][0].update(payload_retrieved=True))

    def test_duplicate_cannot_stand_in_for_other_source(self):
        self.reject(lambda d: d["leads"].__setitem__(1, copy.deepcopy(d["leads"][0])))

    def test_unknown_claim_forbidden(self):
        self.reject(lambda d: d["assertions"].update(certified_by_filename=False))

    def test_source_comment_required(self):
        self.reject(lambda d: d["leads"][2].update(source_statement=""))


if __name__ == "__main__":
    unittest.main()
