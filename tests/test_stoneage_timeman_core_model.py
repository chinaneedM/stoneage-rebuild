import unittest

from tools.stoneage_timeman_core_model import (
    LSTIME_HOURS_PER_DAY,
    LSTIME_SECONDS_PER_DAY,
    active_at_hour,
    alternate_graphic,
    can_talk,
    choose_message_variant,
    init_model,
    message_key_for_mode,
    resolve_time_rule,
    scaled_hour_from_day_seconds,
    state_for_hour,
    watch_transition,
)


class TimeManCoreTests(unittest.TestCase):
    def test_time_scale(self):
        self.assertEqual(LSTIME_SECONDS_PER_DAY, 5400)
        self.assertEqual(LSTIME_HOURS_PER_DAY, 1024)
        self.assertEqual(scaled_hour_from_day_seconds(0), 0)
        self.assertEqual(scaled_hour_from_day_seconds(5399), 1023)

    def test_resolve_known_rules(self):
        self.assertEqual(resolve_time_rule("ALLNOON"), ("ALLNOON", 701, 300))
        self.assertEqual(resolve_time_rule("AFTER"), ("AFTER", 126, 300))

    def test_unknown_rule_fails_init(self):
        self.assertFalse(init_model(
            base_graphic=1, time_value="UNKNOWN"
        )["success"])

    def test_missing_change_defaults_hidden(self):
        self.assertEqual(alternate_graphic(None), 9999)

    def test_cls_substring_hides(self):
        self.assertEqual(alternate_graphic("ABC_CLS_X"), 9999)

    def test_numeric_change_graphic(self):
        self.assertEqual(alternate_graphic("12345"), 12345)

    def test_allnight_strict_boundaries(self):
        self.assertFalse(active_at_hour(301, 700, 301))
        self.assertTrue(active_at_hour(301, 700, 302))
        self.assertTrue(active_at_hour(301, 700, 699))
        self.assertFalse(active_at_hour(301, 700, 700))

    def test_allnoon_wraps_and_is_strict(self):
        self.assertFalse(active_at_hour(701, 300, 701))
        self.assertTrue(active_at_hour(701, 300, 702))
        self.assertTrue(active_at_hour(701, 300, 1023))
        self.assertFalse(active_at_hour(701, 300, 0))
        self.assertTrue(active_at_hour(701, 300, 1))
        self.assertTrue(active_at_hour(701, 300, 299))
        self.assertFalse(active_at_hour(701, 300, 300))

    def test_free_has_hour_zero_gap(self):
        self.assertFalse(active_at_hour(0, 1024, 0))
        self.assertTrue(active_at_hour(0, 1024, 1))
        self.assertTrue(active_at_hour(0, 1024, 1023))

    def test_active_uses_original_and_main_message(self):
        state = state_for_hour(
            original_graphic=10, alternate=9999,
            born=301, dead=700, hour=500,
        )
        self.assertEqual(state["mode"], 0)
        self.assertEqual(state["graphic"], 10)
        self.assertEqual(state["message_key"], "main_msg")

    def test_inactive_uses_alternate_and_change_message(self):
        state = state_for_hour(
            original_graphic=10, alternate=20,
            born=301, dead=700, hour=100,
        )
        self.assertEqual(state["mode"], 1)
        self.assertEqual(state["graphic"], 20)
        self.assertEqual(state["message_key"], "change_msg")

    def test_watch_does_not_broadcast_if_graphic_already_target(self):
        out = watch_transition(
            current_now_graphic=10, original_graphic=10, alternate=20,
            born=301, dead=700, hour=500,
        )
        self.assertFalse(out["changed"])
        self.assertFalse(out["broadcast"])

    def test_watch_broadcasts_on_graphic_change(self):
        out = watch_transition(
            current_now_graphic=20, original_graphic=10, alternate=20,
            born=301, dead=700, hour=500,
        )
        self.assertTrue(out["changed"])
        self.assertTrue(out["broadcast"])
        self.assertEqual(out["now_graphic_after"], 10)

    def test_hidden_graphic_cannot_talk(self):
        self.assertFalse(can_talk(
            base_graphic=9999, is_player=True,
            face_or_near=True, in_front=True,
        ))

    def test_visible_player_can_talk_when_geometry_passes(self):
        self.assertTrue(can_talk(
            base_graphic=10, is_player=True,
            face_or_near=True, in_front=True,
        ))

    def test_mode_message_keys(self):
        self.assertEqual(message_key_for_mode(0), "main_msg")
        self.assertEqual(message_key_for_mode(1), "change_msg")

    def test_message_variant_selection(self):
        self.assertEqual(choose_message_variant("a,b,c", pick=4), "b")

    def test_init_is_lazy_until_watch(self):
        out = init_model(
            base_graphic=10, time_value="ALLNIGHT", change_no=None
        )
        self.assertTrue(out["success"])
        self.assertFalse(out["mode_explicitly_initialized"])
        self.assertFalse(out["now_graphic_explicitly_initialized"])
        self.assertTrue(out["first_time_state_change_requires_watch"])


if __name__ == "__main__":
    unittest.main()
