import unittest

from tools.stoneage_battletimid_model import (
    BattleTimidSourceDomain,
    resolve_battletimid_post_damage,
    resolve_battletimid_setup,
    validate_common_runtime_domain,
)


class BattleTimidModelTests(unittest.TestCase):
    def test_enemy_setup_preserves_low_half_and_fixed_ratios(self):
        result=resolve_battletimid_setup(
            actor_is_player=False,
            target_slot=13,
            skill_array=0x12345,
            packed_com3_before=0x56780002,
            fixed_str=101,
            fixed_tough=99,
            fixed_dex=103,
        )
        self.assertTrue(result.accepted)
        self.assertEqual(result.target_slot,13)
        self.assertEqual(result.packed_com3,0x56782345)
        self.assertEqual(
            (result.attack_power,result.defence_power,result.quick),
            (70,39,82),
        )

    def test_player_actor_is_rejected_before_setup(self):
        result=resolve_battletimid_setup(
            actor_is_player=True,
            target_slot=1,
            skill_array=606,
            packed_com3_before=0x12340000,
            fixed_str=100,
            fixed_tough=100,
            fixed_dex=100,
        )
        self.assertFalse(result.accepted)
        self.assertTrue(result.rejected_player)
        self.assertEqual(result.packed_com3,0x12340000)

    def test_rand_draw_is_consumed_even_when_damage_cannot_force_exit(self):
        result=resolve_battletimid_post_damage(
            draw=0,damage=1,target_is_pet=False,
        )
        self.assertFalse(result.forced_exit)
        self.assertEqual(result.rng_draws_consumed,1)

    def test_pet_forced_exit_branch(self):
        result=resolve_battletimid_post_damage(
            draw=14,damage=2,target_is_pet=True,
        )
        self.assertTrue(result.forced_exit)
        self.assertTrue(result.pet_default_exit)
        self.assertTrue(result.owner_default_pet_cleared)
        self.assertFalse(result.player_battle_exit)
        self.assertFalse(result.party_discharged)

    def test_nonpet_forced_exit_branch(self):
        result=resolve_battletimid_post_damage(
            draw=0,damage=100,target_is_pet=False,
        )
        self.assertTrue(result.forced_exit)
        self.assertTrue(result.player_battle_exit)
        self.assertTrue(result.party_discharged)
        self.assertFalse(result.pet_default_exit)

    def test_threshold_is_strictly_below_fifteen(self):
        self.assertFalse(resolve_battletimid_post_damage(
            draw=15,damage=2,target_is_pet=False,
        ).forced_exit)
        self.assertTrue(resolve_battletimid_post_damage(
            draw=14,damage=2,target_is_pet=False,
        ).forced_exit)

    def test_same_side_domain_remains_open(self):
        validate_common_runtime_domain(opposite_side=True)
        with self.assertRaises(BattleTimidSourceDomain):
            validate_common_runtime_domain(opposite_side=False)

    def test_invalid_reduced_rand_draw_is_rejected(self):
        for draw in (-1,100,1.0):
            with self.assertRaises(BattleTimidSourceDomain):
                resolve_battletimid_post_damage(
                    draw=draw,damage=2,target_is_pet=False,
                )


if __name__=="__main__":
    unittest.main()
