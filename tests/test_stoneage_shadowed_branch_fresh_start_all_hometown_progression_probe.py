import unittest
from tools.stoneage_shadowed_branch_fresh_start_combat_probe import _coordinate_valid_ordinals
from tools.stoneage_shadowed_branch_fresh_start_all_hometown_progression_probe import (
    _report_has,_synthetic_all_hometown_coordinate_report,
)

class AllHometownFreshStartProgressionProbeTests(unittest.TestCase):
    def test_synthetic_report_admits_all_four_normal_hometowns(self):
        self.assertEqual(
            _coordinate_valid_ordinals(_synthetic_all_hometown_coordinate_report()),
            frozenset({1,2,3,4}),
        )

    def test_report_flag_requires_exact_line(self):
        text="X|witness=0\nFRESH_START_ALL_FAILED_HOMETOWNS_WARPMAN_EXECUTION_PREREQUISITES|witness=1\n"
        self.assertTrue(_report_has(text,"FRESH_START_ALL_FAILED_HOMETOWNS_WARPMAN_EXECUTION_PREREQUISITES|witness=1"))
        self.assertFalse(_report_has(text,"X|witness=1"))

if __name__=="__main__":
    unittest.main()
