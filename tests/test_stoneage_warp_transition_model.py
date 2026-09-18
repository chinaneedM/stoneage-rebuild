import unittest

from tools.stoneage_warp_transition_model import (
    PARTY_CLIENT,
    PARTY_LEADER,
    PARTY_NONE,
    apply_warp,
    later_mapwarppoint_resolution,
    later_mapwarppoint_targets,
    later_noexit_redirect,
    legacy_overlap_direct_targets,
    legacy_warp_init,
    login_redirect_order,
    overlap_warp_triggered,
    pack_later_noexit_point,
    parse_legacy_warp_arg,
    unpack_later_noexit_point,
    warpman_targets,
)


class WarpTransitionModelTests(unittest.TestCase):
    def test_legacy_pipe_arg_parses_destination(self):
        out = parse_legacy_warp_arg("200|10|11|N")
        self.assertEqual(out["destination"], (200, 10, 11))
        self.assertEqual(out["time_token"], "N")

    def test_legacy_warp_init_rejects_invalid_destination(self):
        out = legacy_warp_init("200|10|11", destination_valid=False)
        self.assertFalse(out["ok"])
        self.assertFalse(out["enabled"])

    def test_legacy_warp_init_is_invisible_and_overable(self):
        out = legacy_warp_init("200|10|11", destination_valid=True)
        self.assertTrue(out["ok"])
        self.assertTrue(out["invisible"])
        self.assertTrue(out["overable"])
        self.assertFalse(out["attackable"])

    def test_overlap_warp_requires_player_walk_into_event_cell(self):
        self.assertTrue(
            overlap_warp_triggered(
                mover_is_player=True,
                action_is_walk=True,
                previous_xy=(9, 10),
                event_xy=(10, 10),
            )
        )
        self.assertFalse(
            overlap_warp_triggered(
                mover_is_player=True,
                action_is_walk=True,
                previous_xy=(10, 10),
                event_xy=(10, 10),
            )
        )
        self.assertFalse(
            overlap_warp_triggered(
                mover_is_player=False,
                action_is_walk=True,
                previous_xy=(9, 10),
                event_xy=(10, 10),
            )
        )

    def test_invalid_destination_fails_before_warp_mutation(self):
        out = apply_warp(
            current_position=(100, 1, 2),
            destination=(200, 3, 4),
            destination_valid=False,
        )
        self.assertFalse(out["ok"])
        self.assertFalse(out["mutated"])
        self.assertEqual(out["position"], (100, 1, 2))

    def test_valid_warp_updates_encounter_bounds_only_when_lookup_succeeds(self):
        out = apply_warp(
            current_position=(100, 1, 2),
            destination=(200, 3, 4),
            destination_valid=True,
            encounter_min_before=5,
            encounter_max_before=20,
            encounter_min_at_destination=-1,
            encounter_max_at_destination=60,
        )
        self.assertEqual(out["position"], (200, 3, 4))
        self.assertEqual(out["encounter_min"], 5)
        self.assertEqual(out["encounter_max"], 60)

    def test_map_objmove_failure_is_not_rolled_back_by_old_warp_primitive(self):
        out = apply_warp(
            current_position=(100, 1, 2),
            destination=(200, 3, 4),
            destination_valid=True,
            map_objmove_ok=False,
        )
        self.assertTrue(out["ok"])
        self.assertEqual(out["position"], (200, 3, 4))
        self.assertFalse(out["map_objmove_ok"])
        self.assertFalse(out["rolled_back_on_map_objmove_failure"])

    def test_non_client_player_sets_iswarp_and_follow_pet_warps(self):
        out = apply_warp(
            current_position=(100, 1, 2),
            destination=(200, 3, 4),
            destination_valid=True,
            party_mode=PARTY_LEADER,
            follow_pet_present=True,
        )
        self.assertTrue(out["iswarp"])
        self.assertEqual(out["follow_pet_destination"], (200, 3, 4))

    def test_party_client_does_not_set_iswarp_flag_in_primitive(self):
        out = apply_warp(
            current_position=(100, 1, 2),
            destination=(200, 3, 4),
            destination_valid=True,
            party_mode=PARTY_CLIENT,
        )
        self.assertIsNone(out["iswarp"])

    def test_legacy_overlap_warp_does_not_directly_project_over_party(self):
        self.assertEqual(legacy_overlap_direct_targets("leader"), ("leader",))

    def test_warpman_explicitly_projects_destination_over_party(self):
        party = ("leader", "m1", None, "m2")
        self.assertEqual(
            warpman_targets(
                talker="leader",
                party_mode=PARTY_LEADER,
                leader="leader",
                leader_party=party,
            ),
            ("leader", "m1", "m2"),
        )
        self.assertEqual(
            warpman_targets(
                talker="m1",
                party_mode=PARTY_CLIENT,
                leader="leader",
                leader_party=party,
            ),
            ("leader", "m1", "m2"),
        )
        self.assertEqual(
            warpman_targets(
                talker="solo",
                party_mode=PARTY_NONE,
                leader_party=(),
            ),
            ("solo",),
        )

    def test_later_mapwarppoint_leader_explicitly_warps_members(self):
        self.assertEqual(
            later_mapwarppoint_targets(
                triggering_actor="leader",
                party_mode=PARTY_LEADER,
                party_members=("leader", "m1", None, "m2"),
            ),
            ("leader", "m1", "m2"),
        )

    def test_later_mapwarppoint_validates_source_and_destination(self):
        self.assertEqual(
            later_mapwarppoint_resolution(
                source_position=(100, 1, 2),
                recorded_source=(100, 9, 9),
                destination=(200, 3, 4),
                destination_valid=True,
            )["reason"],
            "source_mismatch",
        )
        self.assertEqual(
            later_mapwarppoint_resolution(
                source_position=(100, 1, 2),
                recorded_source=(100, 1, 2),
                destination=(777, 3, 4),
                destination_valid=True,
            )["reason"],
            "floor_777_suppressed",
        )

    def test_later_noexit_pack_uses_eight_bit_xy_fields(self):
        point = pack_later_noexit_point(123, 0x1FF, 0x2AA)
        floor, x, y = unpack_later_noexit_point(point)
        self.assertEqual(floor, 123)
        self.assertEqual(x, 0xFF)
        self.assertEqual(y, 0xAA)

    def test_later_noexit_uses_configured_exit_when_elder_floor_mismatches_type(self):
        out = later_noexit_redirect(
            current_position=(500, 1, 1),
            elder_position=(1006, 15, 22),
            configured_exit=(200, 8, 9),
            map_type=1006,
            destination_floor_exists=True,
        )
        self.assertEqual(out, (1006, 15, 22))

        fallback = later_noexit_redirect(
            current_position=(500, 1, 1),
            elder_position=(2006, 20, 16),
            configured_exit=(200, 8, 9),
            map_type=1006,
            destination_floor_exists=True,
        )
        self.assertEqual(fallback, (200, 8, 9))

    def test_appear_redirect_precedes_later_noexit_lookup(self):
        out = login_redirect_order(
            saved_position=(500, 1, 1),
            appear_floor_member=True,
            elder_position=(1006, 15, 22),
            noexit_entries={
                500: {
                    "configured_exit": (200, 8, 9),
                    "map_type": 1006,
                    "destination_floor_exists": True,
                }
            },
        )
        self.assertEqual(out["position"], (1006, 15, 22))
        self.assertEqual(out["events"], ("appear_to_elder",))


if __name__ == "__main__":
    unittest.main()
