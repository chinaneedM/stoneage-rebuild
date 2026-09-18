import unittest

from tools.stoneage_pet_capture_model import (
    ACTIVE_CAPTURE_MP_COST,
    MAX_PETS,
    NOMINAL_CAPTURE_MPDOWN_ARGUMENT,
    capture_basic_gate,
    capture_roll_success,
    capture_score,
    captured_pet_state,
    consume_required_items_on_success,
    effective_success_roll_count,
    first_empty_pet_slot,
    required_items_satisfied,
    resolve_capture_attempt,
)


def enemy_state():
    return {
        "base_image": 12345,
        "hp": 17,
        "mp": 8,
        "max_mp": 10,
        "vital": 1200,
        "strength": 900,
        "toughness": 800,
        "dexterity": 700,
        "luck": 3,
        "fire": 20,
        "water": 0,
        "earth": 80,
        "wind": 0,
        "skill_slots": 4,
        "mod_ai": 7,
        "level": 12,
        "poison": 2,
        "paralysis": 0,
        "sleep": 3,
        "stone": 0,
        "drunk": 0,
        "confusion": 0,
        "rare": 1,
        "pet_rank": 5,
        "pet_id": 321,
        "critical": 4,
        "counter": 6,
        "pet_skills": (10, 20, 30, -1, -1, -1, -1),
        "alloc_point": 11,
        "name": "target",
    }


class PetCaptureModelTests(unittest.TestCase):
    def test_basic_gate_and_pick_all_pet_bypass(self):
        self.assertEqual(
            capture_basic_gate(
                target_is_enemy=False,
                target_pet_flag=1,
                attacker_level=10,
                target_level=10,
            ),
            (False, "target_not_enemy"),
        )
        self.assertEqual(
            capture_basic_gate(
                target_is_enemy=True,
                target_pet_flag=0,
                attacker_level=10,
                target_level=10,
            ),
            (False, "target_not_capturable"),
        )
        self.assertEqual(
            capture_basic_gate(
                target_is_enemy=True,
                target_pet_flag=1,
                attacker_level=10,
                target_level=16,
            ),
            (False, "target_level_too_high"),
        )
        self.assertEqual(
            capture_basic_gate(
                target_is_enemy=True,
                target_pet_flag=1,
                attacker_level=10,
                target_level=99,
                pick_all_pet=True,
            ),
            (True, "ok"),
        )

    def test_exact_source_score_formula(self):
        score = capture_score(
            attacker_charm=60,
            attacker_level=10,
            attacker_dex=30,
            attacker_luck=5,
            target_level=10,
            target_dex=15,
            target_capture_default=30,
            target_hp=10,
            target_max_hp=100,
        )
        self.assertAlmostEqual(score, 54.0)

    def test_sleep_temp_modifier_cap_and_strict_random_boundary(self):
        score = capture_score(
            attacker_charm=60,
            attacker_level=10,
            attacker_dex=30,
            attacker_luck=5,
            target_level=10,
            target_dex=15,
            target_capture_default=30,
            target_hp=10,
            target_max_hp=100,
            temp_capture_mod=40,
            target_sleep=1,
        )
        self.assertEqual(score, 99.0)
        self.assertTrue(capture_roll_success(score, 98))
        self.assertFalse(capture_roll_success(score, 99))
        self.assertFalse(capture_roll_success(score, 100))
        self.assertEqual(effective_success_roll_count(score), 98)

    def test_source_has_no_lower_score_clamp(self):
        score = capture_score(
            attacker_charm=50,
            attacker_level=1,
            attacker_dex=0,
            attacker_luck=-100,
            target_level=99,
            target_dex=150,
            target_capture_default=0,
            target_hp=100,
            target_max_hp=100,
        )
        self.assertLess(score, 0)
        self.assertEqual(effective_success_roll_count(score), 0)
        self.assertFalse(capture_roll_success(score, 1))

    def test_required_items_and_success_consumption_delete_all_matching_copies(self):
        required = (100, 200)
        inventory = (100, 200, 200, 300)
        self.assertTrue(required_items_satisfied(required, inventory))
        remaining, consumed = consume_required_items_on_success(required, inventory)
        self.assertEqual(remaining, (300,))
        self.assertEqual(consumed, (100, 200, 200))

    def test_five_pet_slots_use_first_empty_slot(self):
        self.assertEqual(MAX_PETS, 5)
        self.assertEqual(first_empty_pet_slot((11, None, 33, -1, 55)), 1)
        self.assertEqual(first_empty_pet_slot((11, 22, 33, 44, 55)), -1)

    def test_full_roster_can_fail_after_successful_probability_roll_without_item_consumption(self):
        out = resolve_capture_attempt(
            target_is_enemy=True,
            target_pet_flag=1,
            attacker_level=10,
            target_level=10,
            attacker_charm=60,
            attacker_dex=30,
            attacker_luck=5,
            target_dex=15,
            target_capture_default=30,
            target_hp=10,
            target_max_hp=100,
            target_sleep=0,
            temp_capture_mod=5,
            pick_all_pet=False,
            required_item_ids=(100,),
            inventory_item_ids=(100, 300),
            pet_slots=(1, 2, 3, 4, 5),
            roll=1,
        )
        self.assertFalse(out["success"])
        self.assertEqual(out["reason"], "pet_slots_full")
        self.assertEqual(out["temp_capture_mod_after"], 0)
        self.assertEqual(out["inventory_after"], (100, 300))
        self.assertEqual(out["consumed_items"], ())

    def test_success_copies_current_enemy_state_not_enemy_exp(self):
        pet = captured_pet_state(enemy_state(), owner_getpetcount=8, pet_slot=2)
        self.assertEqual(pet["which_type"], "pet")
        self.assertEqual(pet["hp"], 17)
        self.assertEqual(pet["sleep"], 3)
        self.assertEqual(pet["level"], 12)
        self.assertEqual(pet["pet_skills"][0:3], (10, 20, 30))
        self.assertEqual(pet["pet_get_level"], 12)
        self.assertEqual(pet["owner_pet_slot"], 2)
        self.assertEqual(pet["owner_getpetcount"], 9)
        self.assertTrue(pet["enemy_exits_battle"])
        self.assertFalse(pet["exp_copied_from_enemy"])
        self.assertTrue(pet["max_exp_recomputed_from_level"])
        self.assertEqual(pet["variable_ai"], 0)

    def test_nominal_mpdown_argument_is_in_active_noop_path(self):
        self.assertEqual(NOMINAL_CAPTURE_MPDOWN_ARGUMENT, 20)
        self.assertEqual(ACTIVE_CAPTURE_MP_COST, 0)


if __name__ == "__main__":
    unittest.main()
