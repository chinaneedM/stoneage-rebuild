import unittest

from tools.stoneage_transport_core_model import (
    AIR_LOOP_MS, WAIT_LOOP_MS, TransportState, actual_boarding_checker,
    air_set_point_effect,
    air_special_boarding_extensions_reachable_from_generic_join,
    allow_items_present, boarding_check, bus_set_point_effect, depart,
    finish_terminal, individual_client_leave_consumes_pickupitem, init_state,
    normal_terminal_consumes_pickupitem, pickup_allow_items,
    reach_current_target, route_point_count, stone_cost, wait_departure_ready,
)

class TransportCoreTests(unittest.TestCase):
    def test_route_point_count(self):
        self.assertEqual(route_point_count("1,2;3,4;5,6"), 3)

    def test_init_defaults(self):
        s = init_state(kind="bus", route_count=2, selected_route=1,
                       selected_route_points=4, now=10)
        self.assertEqual((s.mode, s.routepoint, s.roundtrip, s.waittime), (0, 2, 0, 180))

    def test_reverse_init_uses_count_minus_one(self):
        s = init_state(kind="bus", route_count=1, selected_route=1,
                       selected_route_points=5, now=0, reverse=1)
        self.assertEqual((s.routepoint, s.roundtrip), (4, 1))

    def test_wait_departure_is_strict(self):
        s = TransportState(kind="bus", current_time=10, waittime=20)
        self.assertFalse(wait_departure_ready(s, 30))
        self.assertTrue(wait_departure_ready(s, 31))

    def test_depart_sets_fast_loop(self):
        r = depart(TransportState(kind="air"))
        self.assertEqual(r["state"].mode, 1)
        self.assertEqual(r["loop_interval_ms"], AIR_LOOP_MS)

    def test_forward_terminal_detected_after_last_point(self):
        r = reach_current_target(
            TransportState(kind="bus", routepoint=3, roundtrip=0), 3, 100
        )
        self.assertTrue(r["terminal"])
        self.assertEqual(r["state"].mode, 3)

    def test_reverse_walks_index_down(self):
        r = reach_current_target(
            TransportState(kind="bus", routepoint=3, roundtrip=1), 5, 100
        )
        self.assertEqual(r["state"].routepoint, 2)

    def test_terminal_wait_is_strict_three_seconds(self):
        s = TransportState(kind="bus", mode=3, current_time=10)
        self.assertFalse(finish_terminal(
            s, now=13, new_route=1, new_route_points=5
        )["changed"])
        self.assertTrue(finish_terminal(
            s, now=14, new_route=1, new_route_points=5
        )["changed"])

    def test_terminal_toggles_roundtrip_and_discharges(self):
        s = TransportState(
            kind="bus", mode=3, routepoint=6, roundtrip=0, current_time=10
        )
        r = finish_terminal(s, now=14, new_route=2, new_route_points=7)
        self.assertEqual((r["state"].roundtrip, r["state"].routepoint), (1, 6))
        self.assertTrue(r["discharge_whole_transport_party"])
        self.assertEqual(r["loop_interval_ms"], WAIT_LOOP_MS)

    def test_air_oneway_immediately_restarts(self):
        s = TransportState(
            kind="air", mode=3, routepoint=5, roundtrip=0,
            current_time=0, oneway=1
        )
        r = finish_terminal(s, now=4, new_route=1, new_route_points=6)
        self.assertEqual(r["state"].mode, 1)
        self.assertEqual(r["loop_interval_ms"], AIR_LOOP_MS)

    def test_air_floor_change_warps_vehicle_and_passengers(self):
        r = air_set_point_effect(
            current_floor=1, point=(2, 10, 20), passenger_count=3
        )
        self.assertEqual(r["vehicle_warp"], (2, 10, 20))
        self.assertEqual(r["passengers_warped"], 3)

    def test_air_same_floor_only_updates_target(self):
        r = air_set_point_effect(
            current_floor=2, point=(2, 10, 20), passenger_count=3
        )
        self.assertIsNone(r["vehicle_warp"])

    def test_bus_point_never_floor_warps(self):
        self.assertIsNone(bus_set_point_effect((10, 20))["vehicle_warp"])

    def test_allow_duplicates_reuse_one_item_during_boarding(self):
        self.assertTrue(allow_items_present([5, 5], [5]))

    def test_pickup_duplicates_require_multiple_copies(self):
        r = pickup_allow_items([5, 5], [5], pickup_enabled=True)
        self.assertFalse(r["success"])
        self.assertEqual(r["deleted_slots"], (0,))

    def test_pickup_failure_does_not_rollback(self):
        r = pickup_allow_items([5, 9], [5, 7], pickup_enabled=True)
        self.assertFalse(r["success"])
        self.assertEqual(r["slots"], (None, 7))

    def test_missing_needstone_is_free(self):
        self.assertEqual(stone_cost(None, 100), 0)
        self.assertEqual(stone_cost(-1, 100), 0)

    def test_negative_non_sentinel_needstone_adds_gold(self):
        self.assertEqual(stone_cost(-5, 10), -5)
        r = boarding_check(
            in_front=True, transport_mode=0, player_party_none=True,
            has_party_capacity=True, gold=10, needstone=-5
        )
        self.assertEqual(r["gold_after"], 15)

    def test_boarding_gate_order_denied_before_allow(self):
        r = boarding_check(
            in_front=True, transport_mode=0, player_party_none=True,
            has_party_capacity=True, denied_ids=[1], allow_ids=[2],
            item_slots=[1], gold=100
        )
        self.assertEqual(r["reason"], "denied_item")
        self.assertEqual(r["trace"], ("denied_item",))

    def test_boarding_wares_gate_is_active(self):
        r = boarding_check(
            in_front=True, transport_mode=0, player_party_none=True,
            has_party_capacity=True, wares_allowed=False, gold=100
        )
        self.assertEqual(r["reason"], "wares_blocked")

    def test_boarding_level_gate(self):
        r = boarding_check(
            in_front=True, transport_mode=0, player_party_none=True,
            has_party_capacity=True, player_level=9, needlevel=10, gold=100
        )
        self.assertEqual(r["reason"], "level_too_low")

    def test_boarding_deducts_stone_before_join_main(self):
        r = boarding_check(
            in_front=True, transport_mode=0, player_party_none=True,
            has_party_capacity=True, player_level=10, needlevel=10,
            gold=100, needstone=30
        )
        self.assertTrue(r["success"])
        self.assertEqual(r["gold_after"], 70)
        self.assertEqual(r["next"], "char_join_party_main")

    def test_air_and_bus_generic_join_use_bus_checker(self):
        self.assertEqual(actual_boarding_checker("bus"), "NPC_BusCheckJoinParty")
        self.assertEqual(actual_boarding_checker("air"), "NPC_BusCheckJoinParty")

    def test_air_special_checks_not_on_generic_join_path(self):
        r = air_special_boarding_extensions_reachable_from_generic_join()
        self.assertFalse(r["NPC_AirCheckJoinParty_called"])
        self.assertFalse(r["air_delitem_on_generic_boarding"])
        self.assertFalse(r["air_maxlevel_on_generic_boarding"])

    def test_terminal_discharge_does_not_consume_pickupitem(self):
        self.assertFalse(normal_terminal_consumes_pickupitem())

    def test_individual_client_leave_consumes_pickupitem(self):
        self.assertTrue(individual_client_leave_consumes_pickupitem())

if __name__ == "__main__":
    unittest.main()
