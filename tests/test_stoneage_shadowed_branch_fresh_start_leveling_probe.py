import unittest

from tools.stoneage_shadowed_branch_fresh_start_leveling_probe import (
    _normalized_level_range,
    _positive_exp_mode,
)


class FreshStartLevelingProbeTests(unittest.TestCase):

    def test_computed_enemy_exp_is_positive_for_positive_level_domain(self):
        enemy={
            "lv_min":1,
            "lv_max":3,
            "exp":-1,
        }
        self.assertEqual(_normalized_level_range(enemy),(1,3))
        self.assertEqual(_positive_exp_mode(enemy),"COMPUTED_MIN_ONE")

    def test_positive_override_is_accepted(self):
        enemy={
            "lv_min":5,
            "lv_max":5,
            "exp":10,
        }
        self.assertEqual(_positive_exp_mode(enemy),"POSITIVE_OVERRIDE")

    def test_zero_override_is_not_positive_source(self):
        enemy={
            "lv_min":1,
            "lv_max":1,
            "exp":0,
        }
        self.assertIsNone(_positive_exp_mode(enemy))

    def test_zero_minimum_uses_declared_maximum(self):
        enemy={
            "lv_min":0,
            "lv_max":7,
            "exp":-1,
        }
        self.assertEqual(_normalized_level_range(enemy),(7,7))


if __name__=="__main__":
    unittest.main()
