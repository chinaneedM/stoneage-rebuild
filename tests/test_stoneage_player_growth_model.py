import unittest

from tools.stoneage_player_growth_model import (
    INTERNAL_PER_DISPLAY_POINT,
    POINTS_PER_LEVEL,
    award_free_points,
    base_derived_stats,
    displayed_stat,
    spend_free_point,
)


class PlayerGrowthModelTests(unittest.TestCase):
    def test_internal_display_scale(self):
        self.assertEqual(INTERNAL_PER_DISPLAY_POINT,100)
        self.assertEqual(displayed_stat(100),1)
        self.assertEqual(displayed_stat(1234),12)

    def test_three_free_points_per_level(self):
        self.assertEqual(POINTS_PER_LEVEL,3)
        self.assertEqual(award_free_points(0,1),3)
        self.assertEqual(award_free_points(2,3),11)

    def test_spend_one_point_adds_one_displayed_stat(self):
        result=spend_free_point(1000,2000,3000,4000,5,1)
        self.assertEqual(result,(1000,2100,3000,4000,4))

    def test_base_derived_formula(self):
        r=base_derived_stats(
            vital=1000,
            strength=2000,
            toughness=3000,
            dexterity=4000,
        )
        self.assertEqual(r["fix_vital"],10)
        self.assertEqual(r["fix_dex"],40)
        self.assertEqual(r["fix_str"],26)
        self.assertEqual(r["fix_tough"],35)
        self.assertEqual(r["attack_power"],26)
        self.assertEqual(r["defence_power"],35)
        self.assertEqual(r["quick"],40)
        self.assertEqual(r["max_hp"],130)

    def test_fractional_cross_contributions_truncate(self):
        base=base_derived_stats(100,0,0,0)
        self.assertEqual(base["fix_str"],0)
        self.assertEqual(base["fix_tough"],0)
        self.assertEqual(base["max_hp"],4)

        ten_vital=base_derived_stats(1000,0,0,0)
        self.assertEqual(ten_vital["fix_str"],1)
        self.assertEqual(ten_vital["fix_tough"],1)

    def test_no_points_and_bad_stat_are_rejected(self):
        with self.assertRaises(ValueError):
            spend_free_point(0,0,0,0,0,0)
        with self.assertRaises(ValueError):
            spend_free_point(0,0,0,0,1,4)


if __name__=="__main__":
    unittest.main()
