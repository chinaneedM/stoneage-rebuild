import unittest

from tools.stoneage_riderman_core_model import (
    RECOVERED_TUITION,
    common_mount_gate,
    dismount_apply,
    family_revenue_share,
    mount_apply,
    trainer_gate,
    trainer_transaction,
    transmigration_preserves_learnride,
)


class RidermanCoreTests(unittest.TestCase):
    def test_recovered_tuition(self):
        self.assertEqual(
            RECOVERED_TUITION,
            {6: 5000, 7: 10000, 8: 15000, 9: 20000},
        )

    def test_beginner_blocks_if_already_40(self):
        self.assertEqual(
            trainer_gate(40, 6)["reason"], "already_learned"
        )

    def test_beginner_has_no_previous_tier_requirement(self):
        self.assertTrue(trainer_gate(0, 6)["allowed"])

    def test_intermediate_requires_40(self):
        self.assertEqual(
            trainer_gate(39, 7)["reason"], "missing_prerequisite"
        )
        self.assertTrue(trainer_gate(40, 7)["allowed"])

    def test_advanced_requires_80(self):
        self.assertEqual(
            trainer_gate(79, 8)["reason"], "missing_prerequisite"
        )
        self.assertTrue(trainer_gate(80, 8)["allowed"])

    def test_early_special_requires_exactly_120(self):
        self.assertTrue(trainer_gate(120, 9, "gavin")["allowed"])
        self.assertEqual(
            trainer_gate(121, 9, "gavin")["reason"], "already_learned"
        )
        self.assertEqual(
            trainer_gate(119, 9, "iriselia")["reason"],
            "missing_prerequisite",
        )

    def test_bismarck_special_accepts_120_through_200(self):
        self.assertTrue(trainer_gate(120, 9, "bismarck")["allowed"])
        self.assertTrue(trainer_gate(150, 9, "bismarck")["allowed"])
        self.assertTrue(trainer_gate(200, 9, "bismarck")["allowed"])
        self.assertEqual(
            trainer_gate(201, 9, "bismarck")["reason"],
            "already_learned",
        )

    def test_bismarck_200_can_pay_again(self):
        out = trainer_transaction(
            learnride=200, gold=50000, action=9, tuition=20000,
            lineage="bismarck"
        )
        self.assertTrue(out["success"])
        self.assertEqual(out["learnride_after"], 200)
        self.assertEqual(out["gold_after"], 30000)

    def test_insufficient_stone_is_atomic(self):
        out = trainer_transaction(
            learnride=40, gold=9999, action=7, tuition=10000
        )
        self.assertFalse(out["success"])
        self.assertEqual(out["learnride_after"], 40)
        self.assertEqual(out["gold_after"], 9999)

    def test_success_deducts_then_writes_threshold(self):
        out = trainer_transaction(
            learnride=40, gold=20000, action=7, tuition=10000
        )
        self.assertTrue(out["success"])
        self.assertEqual(out["gold_after"], 10000)
        self.assertEqual(out["learnride_after"], 80)
        self.assertEqual(out["events"][:2], ("deduct_stone", "set_learnride"))

    def test_family_share_is_one_fifth(self):
        self.assertEqual(family_revenue_share(15000), 3000)
        out = trainer_transaction(
            learnride=80, gold=20000, action=8, tuition=15000,
            matching_village_family=True,
        )
        self.assertEqual(out["family_credit"], 3000)

    def test_common_mount_training_gate(self):
        result = common_mount_gate(
            valid_character=True, battle_free=True, valid_pet=True,
            already_riding=False, learnride=40, pet_level=41,
            pet_loyalty=100, player_level=40, direct_mapping_exists=True,
        )
        self.assertEqual(result["reason"], "training_limit")

    def test_common_mount_loyalty_gate(self):
        result = common_mount_gate(
            valid_character=True, battle_free=True, valid_pet=True,
            already_riding=False, learnride=80, pet_level=40,
            pet_loyalty=99, player_level=40, direct_mapping_exists=True,
        )
        self.assertEqual(result["reason"], "loyalty")

    def test_common_mount_player_level_gap(self):
        result = common_mount_gate(
            valid_character=True, battle_free=True, valid_pet=True,
            already_riding=False, learnride=80, pet_level=46,
            pet_loyalty=100, player_level=40, direct_mapping_exists=True,
        )
        self.assertEqual(result["reason"], "player_level_gap")

    def test_common_mount_requires_direct_mapping(self):
        result = common_mount_gate(
            valid_character=True, battle_free=True, valid_pet=True,
            already_riding=False, learnride=80, pet_level=40,
            pet_loyalty=100, player_level=40, direct_mapping_exists=False,
        )
        self.assertEqual(result["reason"], "no_ride_mapping")

    def test_common_mount_accepts_equal_training_limit(self):
        result = common_mount_gate(
            valid_character=True, battle_free=True, valid_pet=True,
            already_riding=False, learnride=40, pet_level=40,
            pet_loyalty=100, player_level=40, direct_mapping_exists=True,
        )
        self.assertTrue(result["allowed"])

    def test_mount_mutation(self):
        out = mount_apply(pet_slot=2, ride_graphic=123)
        self.assertEqual(out["ridepet_after"], 2)
        self.assertEqual(out["base_image_after"], 123)
        self.assertTrue(out["recompute_parameters"])

    def test_dismount_restores_basebase_image(self):
        out = dismount_apply(base_base_image=100001)
        self.assertEqual(out["ridepet_after"], -1)
        self.assertEqual(out["base_image_after"], 100001)

    def test_transmigration_preserves_training(self):
        self.assertTrue(transmigration_preserves_learnride())


if __name__ == "__main__":
    unittest.main()
