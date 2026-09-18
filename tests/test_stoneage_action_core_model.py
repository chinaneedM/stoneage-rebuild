import unittest

from tools.stoneage_action_core_model import (
    ACTION_TO_KEY,
    action_has_state_mutation,
    msgcol_initialization_status,
    normal_is_invalid_action_fallback,
    recovered_25_surface,
    talked_response_key,
    watch_response_key,
)


class ActionCoreTests(unittest.TestCase):
    def test_action_table_has_eleven_watch_actions(self):
        self.assertEqual(len(ACTION_TO_KEY), 11)

    def test_talk_uses_normal_only_for_player_in_front(self):
        self.assertEqual(
            talked_response_key(
                is_player=True,
                in_front_one=True,
                normal_configured=True,
            ),
            "normal",
        )
        self.assertIsNone(
            talked_response_key(
                is_player=False,
                in_front_one=True,
                normal_configured=True,
            )
        )
        self.assertIsNone(
            talked_response_key(
                is_player=True,
                in_front_one=False,
                normal_configured=True,
            )
        )

    def test_talk_silent_if_normal_missing(self):
        self.assertIsNone(
            talked_response_key(
                is_player=True,
                in_front_one=True,
                normal_configured=False,
            )
        )

    def test_watch_requires_character_player_and_face_to_face(self):
        common = {
            "action": "attack",
            "configured_keys": {"attack"},
        }
        self.assertIsNone(
            watch_response_key(
                object_is_character=False,
                is_player=True,
                face_to_face_one=True,
                **common,
            )
        )
        self.assertIsNone(
            watch_response_key(
                object_is_character=True,
                is_player=False,
                face_to_face_one=True,
                **common,
            )
        )
        self.assertIsNone(
            watch_response_key(
                object_is_character=True,
                is_player=True,
                face_to_face_one=False,
                **common,
            )
        )

    def test_watch_routes_exact_supported_action(self):
        self.assertEqual(
            watch_response_key(
                object_is_character=True,
                is_player=True,
                face_to_face_one=True,
                action="nod",
                configured_keys={"nod"},
            ),
            "nod",
        )

    def test_unsupported_action_has_no_normal_fallback(self):
        self.assertIsNone(
            watch_response_key(
                object_is_character=True,
                is_player=True,
                face_to_face_one=True,
                action="walk",
                configured_keys={"normal"},
            )
        )
        self.assertFalse(normal_is_invalid_action_fallback())

    def test_missing_action_key_is_silent(self):
        self.assertIsNone(
            watch_response_key(
                object_is_character=True,
                is_player=True,
                face_to_face_one=True,
                action="attack",
                configured_keys={"normal"},
            )
        )

    def test_no_state_mutation(self):
        self.assertFalse(action_has_state_mutation())

    def test_msgcol_is_not_deterministic_from_literal_source(self):
        status = msgcol_initialization_status(1)
        self.assertEqual(status["configured_value"], 1)
        self.assertFalse(status["deterministic_from_fixed_source"])
        self.assertEqual(status["reason"], "uninitialized_argstr_read")

    def test_recovered_surface_is_complete(self):
        surface = recovered_25_surface()
        self.assertEqual(surface["refs"], 8)
        self.assertEqual(surface["msgcol_configured_value"], 1)
        self.assertEqual(len(surface["all_response_keys_present"]), 12)


if __name__ == "__main__":
    unittest.main()
