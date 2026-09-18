import unittest

from tools.stoneage_player_birth_model import (
    HOMETOWNS,
    birth_state,
    unified_malinasi_spawn,
)


class PlayerBirthModelTests(unittest.TestCase):
    def test_four_hometowns(self):
        self.assertEqual(len(HOMETOWNS), 4)
        self.assertEqual(
            [row["village"] for row in HOMETOWNS],
            ["萨姆吉尔村", "玛丽娜丝村", "加加村", "卡鲁它那村"],
        )

    def test_baseline_elder_coordinates(self):
        self.assertEqual(
            [
                (row["elder_floor"], row["elder_x"], row["elder_y"])
                for row in HOMETOWNS
            ],
            [(1006, 15, 22), (2006, 20, 16), (3006, 21, 16), (4006, 14, 20)],
        )

    def test_starter_enemy_id_is_hometown_plus_one(self):
        for hometown in range(4):
            with self.subTest(hometown=hometown):
                state = birth_state(hometown)
                self.assertEqual(state["starter_enemy_id"], hometown + 1)
                self.assertEqual(state["starter_pet_level"], 1)

    def test_hometown_sets_elder_and_savepoint_bit(self):
        for hometown in range(4):
            with self.subTest(hometown=hometown):
                state = birth_state(hometown)
                self.assertEqual(state["last_talk_elder"], hometown)
                self.assertEqual(state["savepoint_bit"], 1 << hometown)

    def test_rejects_invalid_hometown(self):
        for hometown in (-1, 4, 99):
            with self.subTest(hometown=hometown):
                with self.assertRaises(ValueError):
                    birth_state(hometown)

    def test_later_unified_malinasi_override_preserves_origin_bit(self):
        state = unified_malinasi_spawn(3)
        self.assertEqual(
            (state["elder_floor"], state["elder_x"], state["elder_y"]),
            (2006, 20, 16),
        )
        self.assertEqual(state["last_talk_elder"], 1)
        self.assertEqual(state["savepoint_bit"], 1 << 3)
        self.assertEqual(state["starter_enemy_id"], 4)


if __name__ == "__main__":
    unittest.main()
