import unittest

from tools.stoneage_savepoint_elder_model import (
    BUILTIN_ELDERS,
    ELDER_INDEX_START,
    MAX_ELDERS,
    begin_savepoint_talk,
    bismarck_interaction_allowed,
    confirm_savepoint_unlock,
    get_elder_position,
    legacy_interaction_allowed,
    new_elder_registry,
    old_login_appear_return,
    ordinary_birth_state,
    register_dynamic_elder,
    return_point_resolution,
    savepoint_persistence_policy,
    signed_shift_is_portable,
    source_savepoint_flag_is_set,
)


class SavepointElderModelTests(unittest.TestCase):
    def test_ordinary_birth_sets_position_last_elder_and_unlock_bit(self):
        state = ordinary_birth_state(2)
        self.assertEqual(state["position"], BUILTIN_ELDERS[2])
        self.assertEqual(state["last_talk_elder"], 2)
        self.assertTrue(source_savepoint_flag_is_set(state["savepoint_mask"], 2))
        self.assertIsNone(ordinary_birth_state(4))

    def test_dynamic_elder_registration_starts_at_four_and_caps_below_128(self):
        registry = new_elder_registry()
        self.assertEqual(ELDER_INDEX_START, 4)
        self.assertEqual(MAX_ELDERS, 128)
        self.assertFalse(
            register_dynamic_elder(
                registry, elder_id=3, floor=9, x=8, y=7, coordinate_valid=True
            )
        )
        self.assertTrue(
            register_dynamic_elder(
                registry, elder_id=4, floor=9, x=8, y=7, coordinate_valid=True
            )
        )
        self.assertEqual(get_elder_position(registry, 4), (9, 8, 7))
        self.assertFalse(
            register_dynamic_elder(
                registry, elder_id=128, floor=9, x=8, y=7, coordinate_valid=True
            )
        )

    def test_invalid_coordinate_rejects_dynamic_registration(self):
        registry = new_elder_registry()
        before = get_elder_position(registry, 10)
        self.assertFalse(
            register_dynamic_elder(
                registry,
                elder_id=10,
                floor=900,
                x=1,
                y=2,
                coordinate_valid=False,
            )
        )
        self.assertEqual(get_elder_position(registry, 10), before)

    def test_unregistered_in_range_slot_resolves_static_zero_tuple(self):
        registry = new_elder_registry()
        resolved = return_point_resolution(registry, last_talk_elder=40)
        self.assertTrue(resolved["lookup_ok"])
        self.assertEqual(resolved["position"], (0, 0, 0))
        self.assertFalse(resolved["registered_nonzero"])

    def test_out_of_range_elder_lookup_fails(self):
        registry = new_elder_registry()
        self.assertIsNone(get_elder_position(registry, -1))
        self.assertIsNone(get_elder_position(registry, 128))

    def test_noitem_unlocks_before_branch_and_activates_immediately(self):
        out = begin_savepoint_talk(
            savepoint_mask=1,
            last_talk_elder=0,
            elder_id=6,
            noitem=True,
            requirement_available=False,
        )
        self.assertEqual(out["stage"], "activated")
        self.assertEqual(out["last_talk_elder"], 6)
        self.assertTrue(source_savepoint_flag_is_set(out["savepoint_mask"], 6))

    def test_locked_point_with_requirement_offers_confirmation_without_mutation(self):
        out = begin_savepoint_talk(
            savepoint_mask=1,
            last_talk_elder=0,
            elder_id=5,
            requirement_available=True,
        )
        self.assertEqual(out["stage"], "confirmation")
        self.assertTrue(out["needs_confirmation"])
        self.assertEqual(out["last_talk_elder"], 0)
        self.assertFalse(source_savepoint_flag_is_set(out["savepoint_mask"], 5))

    def test_locked_point_without_requirement_does_not_activate(self):
        out = begin_savepoint_talk(
            savepoint_mask=1,
            last_talk_elder=0,
            elder_id=5,
            requirement_available=False,
        )
        self.assertEqual(out["stage"], "requirements_missing")
        self.assertEqual(out["last_talk_elder"], 0)

    def test_confirmation_only_mutates_after_successful_requirement_consumption(self):
        denied = confirm_savepoint_unlock(
            savepoint_mask=1,
            last_talk_elder=0,
            elder_id=5,
            confirmed=True,
            requirement_consume_success=False,
        )
        self.assertFalse(denied["activated"])
        self.assertEqual(denied["last_talk_elder"], 0)

        ok = confirm_savepoint_unlock(
            savepoint_mask=1,
            last_talk_elder=0,
            elder_id=5,
            confirmed=True,
            requirement_consume_success=True,
        )
        self.assertTrue(ok["activated"])
        self.assertEqual(ok["last_talk_elder"], 5)
        self.assertTrue(source_savepoint_flag_is_set(ok["savepoint_mask"], 5))

    def test_old_login_appear_membership_redirects_to_last_elder(self):
        registry = new_elder_registry()
        register_dynamic_elder(
            registry, elder_id=7, floor=500, x=11, y=12, coordinate_valid=True
        )
        kept = old_login_appear_return(
            registry,
            saved_position=(999, 3, 4),
            last_talk_elder=7,
            appear_floor_member=False,
        )
        self.assertEqual(kept["position"], (999, 3, 4))
        self.assertFalse(kept["redirected"])

        redirected = old_login_appear_return(
            registry,
            saved_position=(999, 3, 4),
            last_talk_elder=7,
            appear_floor_member=True,
        )
        self.assertEqual(redirected["position"], (500, 11, 12))
        self.assertTrue(redirected["redirected"])

    def test_old_login_exposes_invalid_last_elder_instead_of_inventing_fallback(self):
        registry = new_elder_registry()
        out = old_login_appear_return(
            registry,
            saved_position=(999, 3, 4),
            last_talk_elder=999,
            appear_floor_member=True,
        )
        self.assertTrue(out["redirected"])
        self.assertFalse(out["lookup_ok"])
        self.assertIsNone(out["position"])

    def test_fixed_lineages_have_different_interaction_gates(self):
        self.assertTrue(
            legacy_interaction_allowed(in_front=False, dead=True, same_cell=True)
        )
        self.assertFalse(
            legacy_interaction_allowed(in_front=False, dead=False, same_cell=False)
        )
        self.assertTrue(bismarck_interaction_allowed(distance=2, dead=False))
        self.assertFalse(bismarck_interaction_allowed(distance=1, dead=True))
        self.assertFalse(bismarck_interaction_allowed(distance=3, dead=False))

    def test_registry_capacity_and_savepoint_bit_capacity_are_not_equivalent(self):
        self.assertTrue(signed_shift_is_portable(30, int_bits=32))
        self.assertFalse(signed_shift_is_portable(31, int_bits=32))
        self.assertFalse(signed_shift_is_portable(127, int_bits=32))

    def test_savepoint_immediate_persistence_is_versioned(self):
        old = savepoint_persistence_policy("gavinlinasd")
        self.assertTrue(old["immediate_save_on_activation"])
        self.assertFalse(old["unlock"])
        self.assertTrue(old["duplicate_save_on_revisit_observed"])

        later = savepoint_persistence_policy("bismarck", char_is_save=True)
        self.assertFalse(later["immediate_save_on_activation"])
        self.assertTrue(later["conditional_revisit_save"])
        self.assertFalse(later["unlock"])


if __name__ == "__main__":
    unittest.main()
