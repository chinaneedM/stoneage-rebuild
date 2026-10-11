"""Mutation controls for actual-vs-planned disc and third-party mirror claims."""
import copy
import json
import unittest
from tools.stoneage_tw80_disc_mirror_identity_gate import LEDGER, validate

class DiscMirrorGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads(LEDGER.read_text(encoding="utf-8"))

    def reject(self, fn):
        value = copy.deepcopy(self.base)
        fn(value)
        with self.assertRaises(ValueError):
            validate(value)

    def test_valid_source_only_ledger(self):
        self.assertEqual(validate(self.base), "TW80_DISC_MIRROR_IDENTITY_BOUNDARY_PASS")

    def test_june4_disc_plan_not_delivered(self):
        self.reject(lambda d: d["claims"].update(june4_disc_was_actually_handed_out=True))

    def test_june3_source_not_august_fan(self):
        self.reject(lambda d: d["records"][0].update(source=d["records"][2]["source"]))

    def test_prelaunch_date_not_release_date(self):
        self.reject(lambda d: d["records"][0].update(event_date="2005-06-08"))

    def test_launch_article_not_executable(self):
        self.reject(lambda d: d["records"][1].update(bytes_verified=True))

    def test_new_mirror_not_2005_publisher(self):
        self.reject(lambda d: d["claims"].update(dler_mirror_is_authenticated_taiwan_publisher_2005=True))

    def test_2006_not_2005(self):
        self.reject(lambda d: d["records"][2].update(date="2005-06-08"))

    def test_mirror_not_official_domain(self):
        self.reject(lambda d: d["records"][2].update(carrier_url="http://download.wayi.com.tw/Stoneage80.exe"))

    def test_mirror_not_same_as_disc(self):
        self.reject(lambda d: d["claims"].update(dler_mirror_is_bit_identical_to_june2005_disc=True))

    def test_80_name_not_binary_metadata(self):
        self.reject(lambda d: d["claims"].update(filename_80_proves_original_exe_version=True))

    def test_75_program_not_80_runtime(self):
        self.reject(lambda d: d["claims"].update(sa_7505_7507_prove_8_0_runtime=True))

    def test_web_error_not_http404(self):
        self.reject(lambda d: d["claims"].update(read_error_proves_http404=True))

    def test_no_invented_sha(self):
        self.reject(lambda d: d["records"][2].update(sha256="f"*64))

    def test_no_actual_pet_runtime(self):
        self.reject(lambda d: d["claims"].update(original_pet_packet127_verified=True))

    def test_no_early_jss_promotion(self):
        self.reject(lambda d: d["claims"].update(early_taiwan10_or_jss1999_feature_promoted=True))

    def test_original_pressure_retained(self):
        self.reject(lambda d: d["pressure"].update(open=17,bounded_closed=2466))

    def test_missing_context_is_rejected(self):
        self.reject(lambda d: d["records"][2].update(reported="private server"))

    def test_duplicate_is_not_independent(self):
        self.reject(lambda d: d["records"].__setitem__(0,copy.deepcopy(d["records"][2])))

    def test_claims_cannot_expand_silently(self):
        self.reject(lambda d: d["claims"].update(actual_binary_received=False))

if __name__ == "__main__":
    unittest.main()
