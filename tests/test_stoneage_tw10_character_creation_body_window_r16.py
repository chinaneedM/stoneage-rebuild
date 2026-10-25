"""Prove the bounded window never turns a numeric coincidence into identity."""
import unittest
from tools.stoneage_tw10_character_creation_body_window_r16 import classify_window

class CharacterBodyWindowTests(unittest.TestCase):
    def test_keeps_candidate_and_identity_separate(self):
        values = [100000, 100250, 125995, 132767, 132768, 0] + [9] * 26
        rows = classify_window(values, {100000, 100250})
        self.assertEqual(len(rows), 32)
        self.assertTrue(rows[0]["matches_original_spr_group_key"])
        self.assertTrue(rows[1]["within_compiled_animation_key_interval"])
        self.assertFalse(rows[4]["within_compiled_animation_key_interval"])
        self.assertTrue(rows[3]["within_compiled_animation_key_interval"])
        self.assertTrue(all(not x["same_build_role_or_portrait_verified"] for x in rows))
        self.assertTrue(all(not x["runtime_selected_index_verified"] for x in rows))

    def test_no_guessed_table_length(self):
        with self.assertRaisesRegex(ValueError, "invalid window"):
            classify_window([100000], {100000})

    def test_refuses_invalid_values(self):
        with self.assertRaisesRegex(ValueError, "invalid window"):
            classify_window([-1] + [0]*31, set())
        with self.assertRaisesRegex(ValueError, "invalid window"):
            classify_window([0xffffffff+1] + [0]*31, set())

if __name__ == "__main__":
    unittest.main()
