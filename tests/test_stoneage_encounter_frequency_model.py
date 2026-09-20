import unittest

from tools.stoneage_encounter_frequency_model import (
    EncounterFrequencyState,
    refresh_frequency_bounds,
    resolve_frequency_step,
)
from tools.stoneage_tw10_25_encounter_bridge import EncounterAreaBridge


def area(prob_min=5, prob_max=8):
    return EncounterAreaBridge.from_encount(
        {
            "INDEX": 1,
            "FLOOR": 1000,
            "X1": 0,
            "Y1": 0,
            "X2": 10,
            "Y2": 10,
            "PROB_MIN": prob_min,
            "PROB_MAX": prob_max,
            "ENEMY_MAX": 3,
            "ZORDER": 1,
        }
    )


class EncounterFrequencyModelTests(unittest.TestCase):
    def test_area_refresh_replaces_bounds_but_missing_lookup_keeps_previous(self):
        state = EncounterFrequencyState(current=2, minimum=1, maximum=3)
        refreshed = refresh_frequency_bounds(state, area(5, 8))
        self.assertEqual(refreshed.current, 2)
        self.assertEqual(refreshed.minimum, 5)
        self.assertEqual(refreshed.maximum, 8)
        self.assertEqual(refresh_frequency_bounds(refreshed, None), refreshed)

    def test_current_is_clamped_to_min_before_roll(self):
        state = EncounterFrequencyState(current=0, minimum=5, maximum=8)
        decision = resolve_frequency_step(state, roll=5)
        self.assertEqual(decision.clamped_current, 5)
        self.assertFalse(decision.roll_hit)
        self.assertEqual(decision.after.current, 6)

    def test_miss_increments_up_to_max(self):
        state = EncounterFrequencyState(current=7, minimum=5, maximum=8)
        miss = resolve_frequency_step(state, roll=119)
        self.assertEqual(miss.after.current, 8)

        maxed = resolve_frequency_step(miss.after, roll=119)
        self.assertEqual(maxed.after.current, 8)

    def test_unsuppressed_hit_resets_to_minimum(self):
        state = EncounterFrequencyState(current=8, minimum=5, maximum=8)
        hit = resolve_frequency_step(state, roll=7, encounter_enabled=True)
        self.assertTrue(hit.roll_hit)
        self.assertTrue(hit.encounter_triggered)
        self.assertFalse(hit.encounter_suppressed)
        self.assertEqual(hit.after.current, 5)

    def test_warp_suppressed_hit_neither_resets_nor_increments(self):
        state = EncounterFrequencyState(current=8, minimum=5, maximum=8)
        hit = resolve_frequency_step(state, roll=7, encounter_enabled=False)
        self.assertTrue(hit.roll_hit)
        self.assertFalse(hit.encounter_triggered)
        self.assertTrue(hit.encounter_suppressed)
        self.assertEqual(hit.after.current, 8)

    def test_warp_suppressed_miss_still_increments(self):
        state = EncounterFrequencyState(current=6, minimum=5, maximum=8)
        miss = resolve_frequency_step(state, roll=119, encounter_enabled=False)
        self.assertFalse(miss.roll_hit)
        self.assertFalse(miss.encounter_triggered)
        self.assertFalse(miss.encounter_suppressed)
        self.assertEqual(miss.after.current, 7)

    def test_ineligible_step_clamps_but_does_not_roll_or_increment(self):
        state = EncounterFrequencyState(current=0, minimum=5, maximum=8)
        decision = resolve_frequency_step(state, roll=None, eligible=False)
        self.assertEqual(decision.clamped_current, 5)
        self.assertIsNone(decision.roll)
        self.assertEqual(decision.after.current, 5)

    def test_roll_range_is_exact_modulo_120_domain(self):
        state = EncounterFrequencyState(current=5, minimum=5, maximum=8)
        resolve_frequency_step(state, roll=0)
        resolve_frequency_step(state, roll=119)
        with self.assertRaises(ValueError):
            resolve_frequency_step(state, roll=-1)
        with self.assertRaises(ValueError):
            resolve_frequency_step(state, roll=120)

    def test_probability_above_120_is_preserved_as_always_hit(self):
        state = EncounterFrequencyState(current=130, minimum=130, maximum=150)
        decision = resolve_frequency_step(state, roll=119)
        self.assertTrue(decision.roll_hit)
        self.assertTrue(decision.encounter_triggered)
        self.assertEqual(decision.after.current, 130)


if __name__ == "__main__":
    unittest.main()
