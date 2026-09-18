import unittest

from tools.stoneage_item_use_equip_model import (
    ARM,
    BASE_EQUIP_SLOTS,
    DECORATION1,
    DECORATION2,
    HEAD,
    ITEM_DISH,
    ITEM_OTHER,
    choose_use_equip_slot,
    direct_equip_to_equip_allowed,
    direct_move_packet_allowed,
    equip_level_gate,
    item_use_route,
    move_bag_to_bag,
    move_bag_to_equip,
    move_equip_to_bag,
    resolve_use_request,
)


def item(item_id, item_type, equip_place, level=0):
    return {
        "id": item_id,
        "type": item_type,
        "equip_place": equip_place,
        "level": level,
    }


class ItemUseEquipModelTests(unittest.TestCase):
    def test_baseline_has_five_equipment_slots(self):
        self.assertEqual(BASE_EQUIP_SLOTS, 5)

    def test_item_use_routes_only_other_and_dish_to_usefunc(self):
        self.assertEqual(item_use_route(ITEM_OTHER), "use_callback")
        self.assertEqual(item_use_route(ITEM_DISH), "use_callback")
        self.assertEqual(item_use_route("sword"), "equip")

    def test_equipment_use_does_not_call_usefunc(self):
        out = resolve_use_request(
            alive=True,
            item_valid=True,
            item_type="armor",
            usefunc_present=True,
        )
        self.assertEqual(out["route"], "equip")
        self.assertFalse(out["calls_usefunc"])

    def test_other_without_usefunc_is_nothing_happens(self):
        out = resolve_use_request(
            alive=True,
            item_valid=True,
            item_type=ITEM_OTHER,
            usefunc_present=False,
        )
        self.assertEqual(out["route"], "nothing_happens")
        self.assertFalse(out["calls_usefunc"])

    def test_dead_character_cannot_use_item(self):
        out = resolve_use_request(
            alive=False,
            item_valid=True,
            item_type=ITEM_DISH,
        )
        self.assertFalse(out["accepted"])
        self.assertEqual(out["reason"], "dead")

    def test_direct_inventory_move_packet_is_blocked_in_battle(self):
        self.assertFalse(direct_move_packet_allowed(True))
        self.assertTrue(direct_move_packet_allowed(False))

    def test_unreborn_level_gate_and_reborn_bypass(self):
        self.assertFalse(equip_level_gate(20, 10, 0))
        self.assertTrue(equip_level_gate(10, 10, 0))
        self.assertTrue(equip_level_gate(99, 1, 1))

    def test_bag_to_equip_displaces_old_item_detach_then_attach(self):
        old = item(1, "helmet", HEAD, 1)
        new = item(2, "helmet", HEAD, 5)
        out = move_bag_to_equip(
            equipment=(old, None, None, None, None),
            bag=(new, None),
            bag_index=0,
            equip_slot=HEAD,
            player_level=10,
        )
        self.assertTrue(out["moved"])
        self.assertEqual(out["equipment"][HEAD]["id"], 2)
        self.assertEqual(out["bag"][0]["id"], 1)
        self.assertEqual(out["events"], (("detach", 1), ("attach", 2)))
        self.assertTrue(out["recompute_parameters"])
        self.assertTrue(out["status_refresh"])

    def test_wrong_declared_equip_slot_is_rejected(self):
        sword = item(3, "sword", ARM, 1)
        out = move_bag_to_equip(
            equipment=(None,) * 5,
            bag=(sword,),
            bag_index=0,
            equip_slot=HEAD,
            player_level=10,
        )
        self.assertFalse(out["moved"])
        self.assertEqual(out["reason"], "wrong_slot")

    def test_decoration_slots_allow_two_different_types_but_reject_same_type(self):
        charm = item(10, "charm", DECORATION1)
        ring = item(11, "ring", DECORATION1)
        second_charm = item(12, "charm", DECORATION1)

        out = move_bag_to_equip(
            equipment=(None, None, None, charm, None),
            bag=(ring,),
            bag_index=0,
            equip_slot=DECORATION2,
            player_level=1,
        )
        self.assertTrue(out["moved"])

        bad = move_bag_to_equip(
            equipment=(None, None, None, charm, None),
            bag=(second_charm,),
            bag_index=0,
            equip_slot=DECORATION2,
            player_level=1,
        )
        self.assertFalse(bad["moved"])
        self.assertEqual(bad["reason"], "duplicate_decoration_type")

    def test_item_use_auto_selects_decoration_slot(self):
        charm = item(10, "charm", DECORATION1)
        ring = item(11, "ring", DECORATION1)
        equipment = (None, None, None, charm, None)
        self.assertEqual(
            choose_use_equip_slot(DECORATION1, ring["type"], equipment),
            DECORATION2,
        )

    def test_equip_to_empty_bag_detaches(self):
        sword = item(20, "sword", ARM)
        out = move_equip_to_bag(
            equipment=(None, None, sword, None, None),
            bag=(None, None),
            equip_slot=ARM,
            bag_index=0,
            player_level=10,
        )
        self.assertTrue(out["moved"])
        self.assertIsNone(out["equipment"][ARM])
        self.assertEqual(out["bag"][0]["id"], 20)
        self.assertEqual(out["events"], (("detach", 20),))

    def test_equip_to_occupied_bag_is_recursive_replacement_not_overwrite(self):
        sword = item(20, "sword", ARM)
        axe = item(21, "axe", ARM)
        out = move_equip_to_bag(
            equipment=(None, None, sword, None, None),
            bag=(axe,),
            equip_slot=ARM,
            bag_index=0,
            player_level=10,
        )
        self.assertTrue(out["moved"])
        self.assertEqual(out["equipment"][ARM]["id"], 21)
        self.assertEqual(out["bag"][0]["id"], 20)
        self.assertEqual(out["events"], (("detach", 20), ("attach", 21)))

    def test_bag_to_bag_swaps_and_direct_equip_to_equip_is_rejected(self):
        first = item(30, ITEM_OTHER, -1)
        second = item(31, ITEM_DISH, -1)
        out = move_bag_to_bag((first, second), 0, 1)
        self.assertEqual(out["bag"][0]["id"], 31)
        self.assertEqual(out["bag"][1]["id"], 30)
        self.assertFalse(direct_equip_to_equip_allowed())


if __name__ == "__main__":
    unittest.main()
