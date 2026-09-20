import unittest

from tools.stoneage_player_growth_model import (
    INTERNAL_PER_DISPLAY_POINT,
    LEGACY_CUMULATIVE_EXP,
    PER_LEVEL_EXP,
    PLAYER_LEVELUP_CHARM_DELTA,
    POINTS_PER_LEVEL,
    award_free_points,
    base_derived_stats,
    displayed_stat,
    resolve_player_exp_transition,
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

    def test_exp_profiles_share_below_threshold_behavior(self):
        legacy=resolve_player_exp_transition(
            5,100,200,1000,
            profile=LEGACY_CUMULATIVE_EXP,
        )
        per_level=resolve_player_exp_transition(
            5,100,200,1000,
            profile=PER_LEVEL_EXP,
        )
        self.assertEqual((legacy.end_level,legacy.end_exp,legacy.next_max_exp),(5,300,1000))
        self.assertEqual((per_level.end_level,per_level.end_exp,per_level.next_max_exp),(5,300,1000))
        self.assertEqual(legacy.levels_gained,0)
        self.assertEqual(per_level.levels_gained,0)

    def test_legacy_cumulative_profile_keeps_total_exp_on_level_up(self):
        r=resolve_player_exp_transition(
            5,900,200,1000,
            profile=LEGACY_CUMULATIVE_EXP,
            next_max_exp_by_level={6:1500},
        )
        self.assertEqual((r.end_level,r.end_exp,r.next_max_exp),(6,1100,1500))
        self.assertEqual(r.free_stat_points_delta,3)
        self.assertEqual(r.charm_delta,PLAYER_LEVELUP_CHARM_DELTA)
        self.assertEqual(r.duel_point_delta,60)

    def test_per_level_profile_consumes_crossed_requirement(self):
        r=resolve_player_exp_transition(
            5,900,200,1000,
            profile=PER_LEVEL_EXP,
            next_max_exp_by_level={6:500},
        )
        self.assertEqual((r.end_level,r.end_exp,r.next_max_exp),(6,100,500))
        self.assertEqual(r.free_stat_points_delta,3)
        self.assertEqual(r.charm_delta,2)
        self.assertEqual(r.duel_point_delta,60)

    def test_multi_level_transition_preserves_once_per_result_charm_rule(self):
        legacy=resolve_player_exp_transition(
            5,900,1000,1000,
            profile=LEGACY_CUMULATIVE_EXP,
            next_max_exp_by_level={6:1500,7:2200},
        )
        self.assertEqual((legacy.end_level,legacy.end_exp,legacy.next_max_exp),(7,1900,2200))
        self.assertEqual(legacy.levels_gained,2)
        self.assertEqual(legacy.free_stat_points_delta,6)
        self.assertEqual(legacy.charm_delta,2)
        self.assertEqual(legacy.duel_point_delta,130)

        per_level=resolve_player_exp_transition(
            5,900,700,1000,
            profile=PER_LEVEL_EXP,
            next_max_exp_by_level={6:500,7:800},
        )
        self.assertEqual((per_level.end_level,per_level.end_exp,per_level.next_max_exp),(7,100,800))
        self.assertEqual(per_level.levels_gained,2)
        self.assertEqual(per_level.free_stat_points_delta,6)
        self.assertEqual(per_level.charm_delta,2)
        self.assertEqual(per_level.duel_point_delta,130)

    def test_threshold_crossing_requires_explicit_future_threshold(self):
        with self.assertRaisesRegex(ValueError,'missing next max EXP'):
            resolve_player_exp_transition(
                5,900,100,1000,
                profile=LEGACY_CUMULATIVE_EXP,
            )
        with self.assertRaisesRegex(ValueError,'missing next max EXP'):
            resolve_player_exp_transition(
                5,900,100,1000,
                profile=PER_LEVEL_EXP,
            )
    def test_no_points_and_bad_stat_are_rejected(self):
        with self.assertRaises(ValueError):
            spend_free_point(0,0,0,0,0,0)
        with self.assertRaises(ValueError):
            spend_free_point(0,0,0,0,1,4)


if __name__=="__main__":
    unittest.main()
