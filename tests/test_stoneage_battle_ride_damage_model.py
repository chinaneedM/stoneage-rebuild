import unittest

from tools.stoneage_battle_ride_damage_model import (
    apply_ride_damage,
    apply_ride_heal,
    combo_ride_damage_split,
    immediate_reaction_ride_split,
    ordinary_ride_damage_split,
    ride_pet_lookup_allowed,
)


class BattleRideDamageModelTests(unittest.TestCase):
    def test_common_ride_lookup_is_player_only(self):
        self.assertTrue(ride_pet_lookup_allowed(rider_kind="player"))
        self.assertFalse(ride_pet_lookup_allowed(rider_kind="pet"))
        self.assertFalse(ride_pet_lookup_allowed(rider_kind="enemy"))

    def test_ordinary_split_preserves_plus_one_allocation(self):
        split=ordinary_ride_damage_split(
            100,rider_defense_power=60,pet_defense_power=40,pet_hp=100
        )
        self.assertEqual((split.rider_amount,split.pet_amount),(41,60))
        self.assertEqual(split.rider_amount+split.pet_amount,101)

    def test_ordinary_split_clamps_both_work_powers_to_one(self):
        split=ordinary_ride_damage_split(
            10,rider_defense_power=0,pet_defense_power=0,pet_hp=100
        )
        self.assertEqual((split.rider_amount,split.pet_amount),(6,5))

    def test_immediate_reaction_split_uses_raw_work_powers(self):
        split=immediate_reaction_ride_split(
            100,rider_defense_power=60,pet_defense_power=40,pet_hp=100
        )
        self.assertEqual((split.rider_amount,split.pet_amount),(41,60))
        with self.assertRaises(ValueError):
            immediate_reaction_ride_split(
                10,rider_defense_power=0,pet_defense_power=0,pet_hp=100
            )

    def test_combo_split_uses_distinct_no_plus_one_formula(self):
        split=combo_ride_damage_split(
            100,rider_defense_power=60,pet_defense_power=40,pet_hp=100
        )
        self.assertEqual((split.rider_amount,split.pet_amount),(40,60))

    def test_combo_minimum_rider_share_does_not_rebalance_pet(self):
        split=combo_ride_damage_split(
            1,rider_defense_power=1000,pet_defense_power=1,pet_hp=100
        )
        self.assertEqual((split.rider_amount,split.pet_amount),(1,1))

    def test_dead_ride_pet_stops_sharing(self):
        split=ordinary_ride_damage_split(
            50,rider_defense_power=60,pet_defense_power=40,pet_hp=0
        )
        self.assertFalse(split.shared)
        self.assertEqual((split.rider_amount,split.pet_amount),(50,0))

    def test_pet_death_unmounts_and_sets_petfall(self):
        split=ordinary_ride_damage_split(
            100,rider_defense_power=60,pet_defense_power=40,pet_hp=20
        )
        result=apply_ride_damage(
            split,rider_hp=100,rider_max_hp=100,pet_hp=20,pet_max_hp=100
        )
        self.assertEqual(result.rider_hp_after,59)
        self.assertEqual(result.pet_hp_after,0)
        self.assertTrue(result.unmounted)
        self.assertTrue(result.petfall)

    def test_absorb_heal_caps_rider_and_pet_independently(self):
        split=immediate_reaction_ride_split(
            100,rider_defense_power=60,pet_defense_power=40,pet_hp=50
        )
        result=apply_ride_heal(
            split,rider_hp=90,rider_max_hp=100,pet_hp=50,pet_max_hp=80
        )
        self.assertEqual(result.rider_hp_after,100)
        self.assertEqual(result.pet_hp_after,80)
        self.assertFalse(result.unmounted)


if __name__ == "__main__":
    unittest.main()
