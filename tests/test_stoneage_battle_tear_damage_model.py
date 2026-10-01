import unittest

from tools.stoneage_battle_tear_damage_model import (
    battle_tear_callback_setup,
    c_atoi,
    resolve_battle_tear_pre_damage_sub,
)


class BattleTearDamageModelTests(unittest.TestCase):
    def test_callback_fixed_work_power_scaling_and_skill_array(self):
        setup=battle_tear_callback_setup(
            fixed_strength=101,fixed_toughness=101,skill_array=615
        )
        self.assertEqual(setup.attack_power,90)
        self.assertEqual(setup.defense_power,80)
        self.assertEqual(setup.skill_array,615)

    def test_source_atoi_grammar(self):
        self.assertEqual(c_atoi("  +25tail"),25)
        self.assertEqual(c_atoi("-30"),-30)
        self.assertEqual(c_atoi("x50"),0)

    def test_positive_wound_damage_is_added_to_physical_damage(self):
        r=resolve_battle_tear_pre_damage_sub(
            option_text="50",
            attack_seq_damage=100,
            attack_seq_result="normal",
            damage_react_active=False,
            same_side=False,
            prevent_same_side=True,
            target_hp=600,target_max_hp=1000,target_kind="player",
        )
        self.assertEqual(r.wound_basis,400)
        self.assertEqual(r.wound_damage,200)
        self.assertEqual(r.damage_after,300)

    def test_ride_pet_missing_hp_is_added_for_player_target(self):
        r=resolve_battle_tear_pre_damage_sub(
            option_text="50",
            attack_seq_damage=100,
            attack_seq_result="normal",
            damage_react_active=False,
            same_side=False,
            prevent_same_side=False,
            target_hp=800,target_max_hp=1000,target_kind="player",
            ride_pet_hp=500,ride_pet_max_hp=1000,
        )
        self.assertEqual(r.wound_basis,700)
        self.assertEqual(r.wound_damage,350)
        self.assertEqual(r.damage_after,450)

    def test_full_hp_target_zeroes_positive_physical_damage(self):
        r=resolve_battle_tear_pre_damage_sub(
            option_text="50",
            attack_seq_damage=123,
            attack_seq_result="normal",
            damage_react_active=False,
            same_side=False,
            prevent_same_side=False,
            target_hp=1000,target_max_hp=1000,target_kind="player",
        )
        self.assertTrue(r.applied)
        self.assertTrue(r.zeroed_physical_damage)
        self.assertEqual(r.damage_after,0)

    def test_dodge_or_damage_react_skips_tear_mutation(self):
        for result,react in (("dodge",False),("normal",True)):
            r=resolve_battle_tear_pre_damage_sub(
                option_text="50",
                attack_seq_damage=77,
                attack_seq_result=result,
                damage_react_active=react,
                same_side=False,
                prevent_same_side=False,
                target_hp=500,target_max_hp=1000,target_kind="player",
            )
            self.assertFalse(r.applied)
            self.assertEqual(r.damage_after,77)

    def test_same_side_prevention_is_compile_profile_specific(self):
        kwargs=dict(
            option_text="50",attack_seq_damage=80,
            attack_seq_result="normal",damage_react_active=False,
            same_side=True,target_hp=500,target_max_hp=1000,
            target_kind="player",
        )
        blocked=resolve_battle_tear_pre_damage_sub(
            **kwargs,prevent_same_side=True
        )
        active=resolve_battle_tear_pre_damage_sub(
            **kwargs,prevent_same_side=False
        )
        self.assertEqual(blocked.damage_after,80)
        self.assertEqual(active.damage_after,330)


if __name__=="__main__":
    unittest.main()
