import unittest

from tools.stoneage_attack_magic_model import (
    ATTACK_MAGIC_TARGET_INDEX,
    BATTLE_COM_S_ATTACK_MAGIC,
    PROFILE_BISMARCK,
    PROFILE_GAVIN_IRIS,
    PROFILE_RECOVERED25,
    build_magic_direct_use_request,
    command3_high,
    command3_low,
    encode_attack_magic_command,
    parse_source_shaped_option,
    remap_attack_magic_target,
)


class StoneAgeAttackMagicModelTests(unittest.TestCase):
    def test_parse_source_shaped_magic_then_item(self):
        parsed = parse_source_shaped_option("magic=301 item=19647")
        self.assertTrue(parsed["magic_marker"])
        self.assertEqual(parsed["magic"], 301)
        self.assertTrue(parsed["item_marker_after_magic"])
        self.assertEqual(parsed["item"], 19647)

    def test_item_before_magic_is_not_the_handler_item(self):
        parsed = parse_source_shaped_option("item=9 magic=301")
        self.assertEqual(parsed["magic"], 301)
        self.assertFalse(parsed["item_marker_after_magic"])
        self.assertIsNone(parsed["item"])

    def test_recovered25_encodes_explicit_magic_and_item(self):
        cmd = encode_attack_magic_command(
            12,
            "magic=301 item=19647",
            profile=PROFILE_RECOVERED25,
        )
        self.assertEqual(cmd.command1, BATTLE_COM_S_ATTACK_MAGIC)
        self.assertEqual(cmd.command2, 12)
        self.assertEqual(command3_low(cmd.command3), 301)
        self.assertEqual(command3_high(cmd.command3), 19647)
        self.assertEqual(cmd.high_source, "explicit_item")

    def test_recovered25_rejects_missing_item(self):
        with self.assertRaises(ValueError):
            encode_attack_magic_command(
                0,
                "magic=313",
                profile=PROFILE_RECOVERED25,
            )

    def test_gavin_iris_keeps_source_default_item_but_not_missing_magic_cursor(self):
        cmd = encode_attack_magic_command(
            0,
            "magic=313",
            profile=PROFILE_GAVIN_IRIS,
        )
        self.assertEqual(command3_low(cmd.command3), 313)
        self.assertEqual(command3_high(cmd.command3), 19659)
        with self.assertRaises(ValueError):
            encode_attack_magic_command(
                0,
                "item=19659",
                profile=PROFILE_GAVIN_IRIS,
            )

    def test_bismarck_preserves_high_residue_and_ignores_item_marker(self):
        cmd = encode_attack_magic_command(
            3,
            "magic=305 item=19651",
            profile=PROFILE_BISMARCK,
            prior_high=77,
        )
        self.assertEqual(command3_low(cmd.command3), 305)
        self.assertEqual(command3_high(cmd.command3), 77)
        self.assertEqual(cmd.item_index, 77)
        self.assertEqual(cmd.high_source, "preserved_residue")

    def test_fixed_target_table_and_rewrite(self):
        self.assertEqual(len(ATTACK_MAGIC_TARGET_INDEX), 25)
        self.assertEqual(remap_attack_magic_target(301, 12), 12)
        self.assertEqual(remap_attack_magic_target(303, 2), 26)
        self.assertEqual(remap_attack_magic_target(303, 12), 25)
        self.assertEqual(remap_attack_magic_target(305, 12), 20)
        self.assertEqual(
            remap_attack_magic_target(305, 12, open_e_petskill=True),
            21,
        )

    def test_direct_use_request_keeps_item_and_remaps_target(self):
        cmd = encode_attack_magic_command(
            12,
            "magic=303 item=19649",
            profile=PROFILE_RECOVERED25,
        )
        req = build_magic_direct_use_request(cmd)
        self.assertEqual(req.magic_id, 303)
        self.assertEqual(req.source_target, 12)
        self.assertEqual(req.target, 25)
        self.assertEqual(req.target_area, 26)
        self.assertEqual(req.item_index, 19649)


if __name__ == "__main__":
    unittest.main()
