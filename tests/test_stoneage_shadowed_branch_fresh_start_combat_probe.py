import unittest

from tools.stoneage_shadowed_branch_fresh_start_combat_probe import (
    _coordinate_valid_ordinals,
    _max_physical_damage,
    _player_profiles,
)


class FreshStartCombatProbeTests(unittest.TestCase):

    def test_coordinate_valid_ordinals_select_only_reachable_rows(self):
        text="""StoneAge shadowed-branch fresh-start coordinate reachability — R1
FRESH_START_COORDINATE_WITNESS|ordinal=1|reachable=1|warp_hops=4
FRESH_START_COORDINATE_WITNESS|ordinal=2|reachable=0|warp_hops=-1
FRESH_START_COORDINATE_WITNESS|ordinal=3|reachable=1|warp_hops=2
"""
        self.assertEqual(_coordinate_valid_ordinals(text),frozenset({1,3}))

    def test_max_physical_damage_uses_legal_top_roll(self):
        # Below defense, source RAND(0,1) permits one point.
        self.assertEqual(_max_physical_damage(5,10.0),1)
        # Strong attack must produce a positive legal maximum.
        self.assertGreater(_max_physical_damage(20,1.4),0)

    def test_player_profiles_stay_on_legal_twenty_point_frontier(self):
        rows=list(_player_profiles())
        self.assertEqual(len(rows),21*4)
        for strength,dexterity,stats,elements in rows:
            self.assertEqual(strength+dexterity,20)
            self.assertEqual(sum(elements),100)
            self.assertGreaterEqual(stats["attack_power"],0)
            self.assertGreaterEqual(stats["quick"],0)


if __name__=="__main__":
    unittest.main()
