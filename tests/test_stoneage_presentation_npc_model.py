import unittest

from tools.stoneage_presentation_npc_model import (
    mic_delivery,
    mic_family_branch,
    mic_init_shape,
    mic_recipient_allowed,
    mic_talker_allowed,
    presentation_classes_mutate_player_core_state,
    recovered_25_shape,
    signboard_can_open,
    signboard_render_mode,
    townpeople_can_talk,
    townpeople_choose,
    townpeople_variant_count,
)


class PresentationNPCModelTests(unittest.TestCase):
    def test_signboard_requires_player_within_one(self):
        self.assertTrue(signboard_can_open(is_player=True, distance=1))
        self.assertFalse(signboard_can_open(is_player=True, distance=2))
        self.assertFalse(signboard_can_open(is_player=False, distance=0))

    def test_signboard_manor_placeholder_mode(self):
        self.assertEqual(
            signboard_render_mode("a%manorid:1%b"),
            "manor_placeholder",
        )
        self.assertEqual(signboard_render_mode("plain"), "plain")

    def test_townpeople_requires_player_in_front_three(self):
        self.assertTrue(
            townpeople_can_talk(is_player=True, in_front_three=True)
        )
        self.assertFalse(
            townpeople_can_talk(is_player=True, in_front_three=False)
        )

    def test_townpeople_random_variant_shape(self):
        self.assertEqual(townpeople_variant_count("a,b,c"), 3)
        self.assertEqual(
            townpeople_choose("a,b,c", pick=4)["message"], "b"
        )

    def test_townpeople_noarg_is_not_defined_as_empty_text(self):
        self.assertIsNone(townpeople_variant_count(None))
        out = townpeople_choose(None)
        self.assertFalse(out["deterministic"])
        self.assertEqual(
            out["reason"],
            "source_uses_uninitialized_buffer_when_arg_missing",
        )

    def test_mic_pipe_shape_is_scoped_mode(self):
        out = mic_init_shape("1|2|3|4|5|6|7|0")
        self.assertTrue(out["pipe_scoped"])
        self.assertEqual(out["token_count"], 8)
        self.assertEqual(out["mode"], 0)

    def test_mic_no_pipe_sets_mode_one(self):
        out = mic_init_shape("FREE")
        self.assertFalse(out["pipe_scoped"])
        self.assertEqual(out["mode"], 1)

    def test_mic_free_bypasses_face_requirement(self):
        self.assertTrue(
            mic_talker_allowed(
                is_player=True, free=True, face_to_face_one=False
            )
        )
        self.assertFalse(
            mic_talker_allowed(
                is_player=True, free=False, face_to_face_one=False
            )
        )

    def test_mic_recipient_always_requires_same_floor(self):
        self.assertFalse(
            mic_recipient_allowed(
                same_floor=False,
                scoped_mode=False,
            )
        )

    def test_mic_scoped_recipient_requires_rectangle(self):
        self.assertFalse(
            mic_recipient_allowed(
                same_floor=True,
                scoped_mode=True,
                inside_rectangle=False,
            )
        )
        self.assertTrue(
            mic_recipient_allowed(
                same_floor=True,
                scoped_mode=True,
                inside_rectangle=True,
            )
        )

    def test_mic_wind_window_suppressed_in_battle(self):
        self.assertEqual(
            mic_delivery(wind=True, recipient_in_battle=False),
            {"send_chat": True, "send_window": True},
        )
        self.assertEqual(
            mic_delivery(wind=True, recipient_in_battle=True),
            {"send_chat": True, "send_window": False},
        )

    def test_mic_family_branch_requires_both_conditions(self):
        self.assertTrue(
            mic_family_branch(
                family_flag_nonzero=True,
                family_role_matches=True,
            )
        )
        self.assertFalse(
            mic_family_branch(
                family_flag_nonzero=False,
                family_role_matches=True,
            )
        )

    def test_no_player_core_state_mutation(self):
        self.assertFalse(presentation_classes_mutate_player_core_state())

    def test_recovered_shape(self):
        shape = recovered_25_shape()
        self.assertEqual(shape["SignBoard"]["resolved"], 181)
        self.assertEqual(shape["TownPeople"]["missing_files"], 15)
        self.assertEqual(shape["TownPeople"]["noarg"], 7)
        self.assertEqual(shape["Mic"]["wind"], 0)
        self.assertEqual(shape["Mic"]["family_flag_nonzero"], 0)


if __name__ == "__main__":
    unittest.main()
