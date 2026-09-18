import unittest

from tools.stoneage_party_formation_model import (
    BATTLE_ENTRY_MAX,
    PARTY_CLIENT,
    PARTY_LEADER,
    PARTY_MAX,
    PARTY_NONE,
    PET_BATTLE_OFFSET,
    battle_projection,
    client_leave,
    direct_walk_allowed,
    field_follow_chain,
    first_empty_member_slot,
    join_member,
    leader_disband,
    same_party,
)


class PartyFormationModelTests(unittest.TestCase):
    def test_common_baseline_is_five_party_members_and_ten_battle_entries(self):
        self.assertEqual(PARTY_MAX, 5)
        self.assertEqual(BATTLE_ENTRY_MAX, 10)
        self.assertEqual(PET_BATTLE_OFFSET, 5)

    def test_first_join_promotes_target_to_leader_and_reserves_slot_zero(self):
        out = join_member(10, (None, None, None, None, None), PARTY_NONE, 20)
        self.assertEqual(out["leader_mode"], PARTY_LEADER)
        self.assertEqual(out["slots"], (10, 20, None, None, None))
        self.assertEqual(out["joined_slot"], 1)
        self.assertTrue(out["first_join"])
        self.assertEqual(out["member_mode"], PARTY_CLIENT)
        self.assertEqual(out["member_leader_pointer"], 10)

    def test_join_fills_first_hole_without_compaction(self):
        slots = (10, 20, None, 40, None)
        self.assertEqual(first_empty_member_slot(slots), 2)
        out = join_member(10, slots, PARTY_LEADER, 30)
        self.assertEqual(out["slots"], (10, 20, 30, 40, None))
        self.assertEqual(out["joined_slot"], 2)

    def test_client_leave_preserves_holes_and_last_leave_only_changes_logical_mode(self):
        out = client_leave(10, (10, 20, 30, 40, None), 30)
        self.assertEqual(out["slots"], (10, 20, None, 40, None))
        self.assertEqual(out["leader_mode"], PARTY_LEADER)
        self.assertTrue(out["party_still_active"])

        last = client_leave(10, (10, 20, None, None, None), 20)
        self.assertEqual(last["leader_mode"], PARTY_NONE)
        self.assertEqual(last["slots"], (10, None, None, None, None))
        self.assertFalse(last["party_still_active"])

    def test_leader_disband_clears_all_slots(self):
        out = leader_disband((10, 20, None, 40, None))
        self.assertEqual(out["slots"], (None, None, None, None, None))
        self.assertEqual(out["leader_mode"], PARTY_NONE)
        self.assertEqual(out["removed_members"], (10, 20, 40))

    def test_field_follow_chain_uses_party_slot_order_and_skips_holes(self):
        self.assertEqual(
            field_follow_chain((10, None, 30, 40, None)),
            ((10, 30), (30, 40)),
        )

    def test_clients_cannot_direct_walk_but_can_turn(self):
        self.assertFalse(direct_walk_allowed(PARTY_CLIENT, 0))
        self.assertTrue(direct_walk_allowed(PARTY_CLIENT, 1))
        self.assertTrue(direct_walk_allowed(PARTY_LEADER, 0))
        self.assertTrue(direct_walk_allowed(PARTY_NONE, 0))

    def test_battle_projection_compacts_players_and_pairs_default_pets_plus_five(self):
        out = battle_projection(
            (10, None, 30, 40, None),
            default_pet_by_player={
                10: {"id": 101, "valid": True, "dead": False, "hp": 20},
                30: {"id": 301, "valid": True, "dead": False, "hp": 1},
                40: {"id": 401, "valid": True, "dead": False, "hp": 99},
            },
        )
        self.assertEqual(
            out["entries"],
            (
                ("player", 10),
                ("player", 30),
                ("player", 40),
                None,
                None,
                ("pet", 101),
                ("pet", 301),
                ("pet", 401),
                None,
                None,
            ),
        )
        self.assertEqual(
            [p["field_party_slot"] for p in out["placements"]],
            [0, 2, 3],
        )
        self.assertEqual(
            [p["battle_player_slot"] for p in out["placements"]],
            [0, 1, 2],
        )

    def test_invalid_or_dead_default_pet_is_not_auto_replaced(self):
        out = battle_projection(
            (10, 20, None, None, None),
            default_pet_by_player={
                10: {"id": 101, "valid": True, "dead": True, "hp": 0},
                20: {"id": 201, "valid": False, "dead": False, "hp": 10},
            },
        )
        self.assertEqual(out["entries"][5:], (None, None, None, None, None))
        self.assertEqual(out["reset_default_pet_for"], (10, 20))

    def test_member_already_in_battle_is_skipped_but_order_of_others_is_preserved(self):
        out = battle_projection(
            (10, 20, 30, 40, None),
            member_battle_mode={20: "init", 30: "none", 40: "none"},
        )
        self.assertEqual(out["entries"][0:3], (("player", 10), ("player", 30), ("player", 40)))

    def test_same_party_parent_resolution(self):
        self.assertTrue(
            same_party(10, PARTY_LEADER, None, 20, PARTY_CLIENT, 10)
        )
        self.assertTrue(
            same_party(20, PARTY_CLIENT, 10, 30, PARTY_CLIENT, 10)
        )
        self.assertFalse(
            same_party(10, PARTY_NONE, None, 20, PARTY_NONE, None)
        )


if __name__ == "__main__":
    unittest.main()
