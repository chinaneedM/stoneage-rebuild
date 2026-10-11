"""Mutation tests for contemporary release, announced rollout and mirrored binary boundaries."""
import copy
import json
import unittest

from tools.stoneage_tw80_tw85_chronology_gate import MANIFEST, validate


class ChronologyGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def mutated(self, setter):
        value = copy.deepcopy(self.data)
        setter(value)
        with self.assertRaises(ValueError):
            validate(value)

    def test_valid_timeline(self):
        self.assertEqual(validate(self.data), "TW80_TW85_DATED_CLAIMS_BOUNDARY_PASS")

    def test_september_not_first_pet_subsystem(self):
        self.mutated(lambda v: v["assertions"].update(pet_system_first_introduced_september_2005=True))

    def test_2006_filename_not_release_date(self):
        self.mutated(lambda v: v["assertions"].update(filename_20060616_is_verified_release_date=True))

    def test_2006_public_test_not_full_release(self):
        self.mutated(lambda v: v["assertions"].update(june21_2006_is_all_server_formal_85_launch=True))

    def test_2006_first_server_rollout_remains_scheduled(self):
        self.mutated(lambda v: v["assertions"].update(july05_85_server_rollout_observed_verified=True))

    def test_2006_full_server_rollout_remains_scheduled(self):
        self.mutated(lambda v: v["assertions"].update(july12_85_server_rollout_observed_verified=True))

    def test_taiwan_8_0_date_swap_fails(self):
        self.mutated(lambda v: v["events"][0].update(date="2006-06-08"))

    def test_taiwan_8_5_wrong_version_fails(self):
        self.mutated(lambda v: v["events"][4].update(family="TW_8_0"))

    def test_8_5_press_source_swap_fails(self):
        self.mutated(lambda v: v["events"][4].update(source="https://gnn.gamer.com.tw/detail.php?sn=20167"))

    def test_press_not_executable(self):
        self.mutated(lambda v: v["events"][0].update(original_executable_bytes_verified=True))

    def test_no_fake_sha256(self):
        self.mutated(lambda v: v.update(original_tw85_installer_sha256="0" * 64))

    def test_no_paired_packet_promotion(self):
        self.mutated(lambda v: v.update(original_packet127_observed=True))

    def test_no_early_version_promotion(self):
        self.mutated(lambda v: v.update(early_1999_or_tw10_pet_proven=True))

    def test_no_pressure_promotion(self):
        self.mutated(lambda v: v["pressure"].update(open=17,bounded_closed=2466))

    def test_no_claimed_official_8_5_mirror(self):
        self.mutated(lambda v: v["assertions"].update(wayi85_community_mirror_operator_binary_verified=True))


if __name__ == "__main__":
    unittest.main()
