import unittest

from tools.stoneage_windowman_core_model import (
    button_index,
    interaction_allowed,
    parsed_but_inert_fields,
    recovered_25_active_control_fields,
    route_button,
    unparsed_placeholder_fields,
    validate_button_definition,
)


class WindowmanCoreTests(unittest.TestCase):
    def test_select_button_mapping(self):
        self.assertEqual(
            button_index(window_is_select=True, data="1"), 6
        )
        self.assertEqual(
            button_index(window_is_select=True, data="7"), 12
        )
        self.assertIsNone(
            button_index(window_is_select=True, data="8")
        )

    def test_nonselect_button_priority(self):
        # OK wins because the source tests flags in fixed order.
        self.assertEqual(
            button_index(
                window_is_select=False,
                select_flags=1 | 4,
            ),
            0,
        )

    def test_unused_button_does_nothing(self):
        out = route_button(button_used=False, gotowin=2)
        self.assertFalse(out["routed"])
        self.assertFalse(out["state_mutation"])

    def test_plain_gotowin_routes(self):
        out = route_button(button_used=True, gotowin=7)
        self.assertTrue(out["routed"])
        self.assertEqual(out["target"], 7)
        self.assertFalse(out["state_mutation"])

    def test_have_item_condition_blocks_if_missing(self):
        out = route_button(
            button_used=True,
            checkhaveitem=10,
            haveitemgotowin=2,
            item_ids=(11,),
        )
        self.assertEqual(out["reason"], "required_item_missing")

    def test_have_item_condition_routes_if_present(self):
        out = route_button(
            button_used=True,
            checkhaveitem=10,
            haveitemgotowin=2,
            item_ids=(10,),
        )
        self.assertEqual(out["target"], 2)

    def test_donthave_condition_blocks_if_present(self):
        out = route_button(
            button_used=True,
            checkdonthaveitem=10,
            donthaveitemgotowin=3,
            item_ids=(10,),
        )
        self.assertEqual(out["reason"], "forbidden_item_present")

    def test_donthave_condition_routes_if_absent(self):
        out = route_button(
            button_used=True,
            checkdonthaveitem=10,
            donthaveitemgotowin=3,
            item_ids=(11,),
        )
        self.assertEqual(out["target"], 3)

    def test_second_condition_overwrites_first_target(self):
        out = route_button(
            button_used=True,
            checkhaveitem=10,
            haveitemgotowin=2,
            checkdonthaveitem=20,
            donthaveitemgotowin=3,
            item_ids=(10,),
        )
        self.assertEqual(out["target"], 3)

    def test_validation_accepts_gotowin(self):
        self.assertTrue(validate_button_definition(gotowin=2))

    def test_validation_accepts_complete_condition_pair(self):
        self.assertTrue(
            validate_button_definition(
                checkhaveitem=10,
                haveitemgotowin=2,
            )
        )

    def test_validation_rejects_incomplete_condition(self):
        self.assertFalse(
            validate_button_definition(checkhaveitem=10)
        )

    def test_take_and_give_are_parsed_but_inert(self):
        self.assertEqual(
            parsed_but_inert_fields(), ("takeitem", "giveitem")
        )

    def test_warp_and_battle_are_placeholders_not_parser_keys(self):
        self.assertEqual(
            unparsed_placeholder_fields(), ("warp", "battle")
        )

    def test_recovered_surface_is_only_gotowin(self):
        self.assertEqual(
            recovered_25_active_control_fields(), ("gotowin",)
        )

    def test_interaction_geometry(self):
        self.assertTrue(
            interaction_allowed(
                is_player=True,
                in_front_one=True,
                callback_distance=1,
            )
        )
        self.assertFalse(
            interaction_allowed(
                is_player=True,
                in_front_one=True,
                callback_distance=2,
            )
        )


if __name__ == "__main__":
    unittest.main()
