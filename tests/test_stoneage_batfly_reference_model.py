import unittest

from tools.stoneage_batfly_reference_model import (
    BatFlyTarget,
    resolve_batfly_effect,
    resolve_batfly_setup,
)


class BatFlyReferenceTests(unittest.TestCase):
    def test_callback_setup_only_rewrites_low_skill_and_target(self):
        result=resolve_batfly_setup(
            target_slot=7,
            skill_array=633,
            packed_com3_before=0x12340000,
        )
        self.assertEqual(result.target_slot,7)
        self.assertEqual(result.packed_com3,0x12340279)
        self.assertTrue(result.command_written)
        self.assertTrue(result.target_written)
        self.assertTrue(result.mode_written)
        self.assertTrue(result.skill_written)

    def test_unmounted_drain_is_ten_percent_with_minimum_one(self):
        expected={
            1:(0,1),
            9:(8,1),
            10:(9,1),
            19:(18,1),
            20:(18,2),
            99:(90,9),
            100:(90,10),
        }
        for hp,(after,drain) in expected.items():
            with self.subTest(hp=hp):
                result=resolve_batfly_effect(
                    attacker_hp=1,
                    attacker_max_hp=1000,
                    targets=(BatFlyTarget(hp),),
                ).targets[0]
                self.assertEqual(
                    (result.character_hp_after,result.character_drain),
                    (after,drain),
                )
                self.assertEqual(result.ride_pet_drain,0)

    def test_mounted_target_splits_five_percent_to_rider_and_ride_pet(self):
        result=resolve_batfly_effect(
            attacker_hp=1,
            attacker_max_hp=1000,
            targets=(BatFlyTarget(100,ride_pet_hp=80),),
        ).targets[0]
        self.assertEqual(
            (
                result.character_hp_after,
                result.character_drain,
                result.ride_pet_hp_after,
                result.ride_pet_drain,
            ),
            (95,5,76,4),
        )
        self.assertFalse(result.ride_pet_fell)

    def test_mounted_minimum_one_can_drop_one_hp_ride_pet(self):
        result=resolve_batfly_effect(
            attacker_hp=1,
            attacker_max_hp=1000,
            targets=(BatFlyTarget(19,ride_pet_hp=1),),
        ).targets[0]
        self.assertEqual(result.character_drain,1)
        self.assertEqual(result.ride_pet_drain,1)
        self.assertEqual(result.ride_pet_hp_after,0)
        self.assertTrue(result.ride_pet_fell)

    def test_nonpositive_ride_state_falls_back_to_unmounted_branch(self):
        result=resolve_batfly_effect(
            attacker_hp=1,
            attacker_max_hp=1000,
            targets=(BatFlyTarget(100,ride_pet_hp=0),),
        ).targets[0]
        self.assertEqual(result.character_drain,10)
        self.assertEqual(result.ride_pet_drain,0)

    def test_drains_sum_across_entire_target_side(self):
        result=resolve_batfly_effect(
            attacker_hp=100,
            attacker_max_hp=1000,
            targets=(
                BatFlyTarget(100),
                BatFlyTarget(100,ride_pet_hp=100),
                BatFlyTarget(9),
            ),
        )
        self.assertEqual(result.total_drain,21)
        self.assertEqual(result.attacker_hp_after,121)
        self.assertEqual(result.applied_heal,21)
        self.assertEqual(result.reported_heal,21)

    def test_exact_cap_keeps_reported_heal_but_overflow_cap_reports_zero(self):
        exact=resolve_batfly_effect(
            attacker_hp=90,
            attacker_max_hp=100,
            targets=(BatFlyTarget(100),),
        )
        self.assertEqual(
            (exact.attacker_hp_after,exact.applied_heal,exact.reported_heal),
            (100,10,10),
        )

        overflow=resolve_batfly_effect(
            attacker_hp=95,
            attacker_max_hp=100,
            targets=(BatFlyTarget(100),),
        )
        self.assertEqual(
            (
                overflow.attacker_hp_after,
                overflow.applied_heal,
                overflow.reported_heal,
            ),
            (100,5,0),
        )

    def test_living_target_domain_is_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"living-target"):
            resolve_batfly_effect(
                attacker_hp=1,
                attacker_max_hp=100,
                targets=(BatFlyTarget(0),),
            )


if __name__=="__main__":
    unittest.main()
