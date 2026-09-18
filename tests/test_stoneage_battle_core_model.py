import math
import unittest

from tools.stoneage_battle_core_model import (
    ENEMY, PET, PLAYER,
    critical_bonus,
    critical_per_10000,
    dodge_per_10000,
    early_action_value,
    early_item_action_value,
    effective_defense_newpower,
    effective_defense_preserved_old,
    guard_damage,
    guard_multiplier,
    initiative_total,
    physical_base_damage,
    raw_counter_basis,
    battle_exp_from_enemy,
    ride_pet_exp_from_enemy,
)


class BattleCoreModelTests(unittest.TestCase):
    def test_older_action_value_profile(self):
        self.assertEqual(early_action_value(80,0),100)
        self.assertEqual(early_action_value(80,30),70)
        with self.assertRaises(ValueError):
            early_action_value(80,31)
        self.assertEqual(early_item_action_value(80,30),85)
        self.assertEqual(initiative_total(80,20,False),80)
        self.assertEqual(initiative_total(80,20,True),100)

    def test_defense_profiles_are_kept_separate(self):
        self.assertAlmostEqual(effective_defense_newpower(100),70.0)
        self.assertAlmostEqual(effective_defense_newpower(100,True),140.0)
        self.assertAlmostEqual(
            effective_defense_preserved_old(100,50,40),
            59.0,
        )

    def test_piecewise_damage(self):
        self.assertEqual(physical_base_damage(60,70,1),1)
        self.assertEqual(physical_base_damage(70,70,4),4)
        self.assertEqual(physical_base_damage(100,70,0),53)
        self.assertEqual(physical_base_damage(100,70,12),65)

    def test_guard_distribution_edges(self):
        cases={
            1:0.0,25:0.0,26:0.1,50:0.1,51:0.2,70:0.2,
            71:0.3,85:0.3,86:0.4,95:0.4,96:0.5,100:0.5,
        }
        for roll,mult in cases.items():
            self.assertEqual(guard_multiplier(roll),mult)
        self.assertEqual(guard_damage(101,26),10)

    def test_dodge_relationship_modifier(self):
        # player -> non-player reduces defender DEX to 60%.
        per=dodge_per_10000(
            100,100,0,
            attacker_type=PLAYER,defender_type=ENEMY,
        )
        expected=int(math.sqrt((100-60)/0.02)*(60/100)*100)
        self.assertEqual(per,expected)
        self.assertLessEqual(per,7500)

    def test_critical_relationship_and_bonus(self):
        per=critical_per_10000(
            100,100,attacker_luck=0,weapon_critical=0,
            attacker_type=PLAYER,defender_type=ENEMY,
        )
        expected=int(math.sqrt((100-60)/0.09)*100)
        self.assertEqual(per,expected)
        self.assertEqual(critical_bonus(100,50,25),100)

    def test_battle_exp_level_gap_decay(self):
        base=1500
        self.assertEqual(battle_exp_from_enemy(base,5,10),1500)
        self.assertEqual(battle_exp_from_enemy(base,15,10),1500)
        self.assertEqual(battle_exp_from_enemy(base,16,10),1400)
        self.assertEqual(battle_exp_from_enemy(base,29,10),100)
        self.assertEqual(battle_exp_from_enemy(base,30,10),1)
        self.assertEqual(battle_exp_from_enemy(base,60,10),1)

    def test_ride_pet_exp_applies_sixty_percent_after_decay(self):
        base=1500
        self.assertEqual(ride_pet_exp_from_enemy(base,10,10),900)
        self.assertEqual(ride_pet_exp_from_enemy(base,29,10),60)
        self.assertEqual(ride_pet_exp_from_enemy(base,30,10),0)

    def test_counter_is_only_raw_basis(self):
        value=raw_counter_basis(
            100,100,attacker_type=PLAYER,defender_type=ENEMY)
        self.assertGreater(value,0)
        # The final counter probability also needs weapon matchup and luck.
        self.assertIsInstance(value,int)


if __name__=="__main__":
    unittest.main()
