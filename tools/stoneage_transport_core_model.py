#!/usr/bin/env python3
"""Deterministic reference model for the common StoneAge Bus/Airplane transport core."""

from dataclasses import dataclass, replace
from typing import Optional, Sequence

BUS_LOOP_MS = 200
AIR_LOOP_MS = 100
WAIT_LOOP_MS = 5000
DEFAULT_WAIT_SECONDS = 180

@dataclass(frozen=True)
class TransportState:
    kind: str
    mode: int = 0
    routepoint: int = 2
    roundtrip: int = 0
    current_route: int = 1
    current_time: int = 0
    waittime: int = DEFAULT_WAIT_SECONDS
    oneway: int = 0

def loop_ms(kind: str) -> int:
    if kind == "bus":
        return BUS_LOOP_MS
    if kind == "air":
        return AIR_LOOP_MS
    raise ValueError("kind must be bus or air")

def route_point_count(route: str) -> int:
    return len(route.split(";")) if route != "" else 1

def init_state(*, kind: str, route_count: int, selected_route: int,
               selected_route_points: int, now: int,
               waittime: Optional[int] = None, reverse: int = 0,
               oneway: Optional[int] = None) -> TransportState:
    if int(route_count) < 1:
        raise ValueError("fixed source expects at least one route")
    if not 1 <= int(selected_route) <= int(route_count):
        raise ValueError("selected route out of range")
    wait = DEFAULT_WAIT_SECONDS if waittime is None or int(waittime) == -1 else int(waittime)
    ow = 0 if oneway is None or int(oneway) == -1 else int(oneway)
    point, roundtrip = 2, 0
    if int(reverse) == 1:
        if int(selected_route_points) <= 0:
            raise ValueError("reverse initialization requires a nonempty route")
        point = int(selected_route_points) - 1
        roundtrip = 1
    return TransportState(
        kind=kind, mode=0, routepoint=point, roundtrip=roundtrip,
        current_route=int(selected_route), current_time=int(now),
        waittime=wait, oneway=ow,
    )

def wait_departure_ready(state: TransportState, now: int) -> bool:
    return int(state.current_time) + int(state.waittime) < int(now)

def paused_resume_ready(state: TransportState, now: int) -> bool:
    return int(state.current_time) + (int(state.waittime) // 3) < int(now)

def terminal_turnaround_ready(state: TransportState, now: int) -> bool:
    return int(state.current_time) + 3 < int(now)

def depart(state: TransportState) -> dict:
    return {
        "state": replace(state, mode=1),
        "loop_interval_ms": loop_ms(state.kind),
        "send_start_to_passengers": True,
    }

def reach_current_target(state: TransportState, route_points: int, now: int) -> dict:
    step = -1 if int(state.roundtrip) == 1 else 1
    next_point = int(state.routepoint) + step
    if 1 <= next_point <= int(route_points):
        return {"state": replace(state, routepoint=next_point), "terminal": False}
    return {
        "state": replace(state, routepoint=next_point, mode=3, current_time=int(now)),
        "terminal": True,
        "send_end_to_passengers": True,
    }

def finish_terminal(state: TransportState, *, now: int,
                    new_route: int, new_route_points: int) -> dict:
    if not terminal_turnaround_ready(state, now):
        return {"changed": False, "state": state}
    roundtrip = int(state.roundtrip) ^ 1
    if roundtrip == 1:
        routepoint = int(new_route_points) - 1
    else:
        routepoint = int(state.routepoint) + 1
    mode, interval = 0, WAIT_LOOP_MS
    if state.kind == "air" and int(state.oneway) == 1 and roundtrip == 1:
        mode, interval = 1, AIR_LOOP_MS
    return {
        "changed": True,
        "state": replace(
            state, current_route=int(new_route), roundtrip=roundtrip,
            routepoint=routepoint, current_time=int(now), mode=mode,
        ),
        "discharge_whole_transport_party": True,
        "loop_interval_ms": interval,
    }

def air_set_point_effect(*, current_floor: int,
                         point: tuple[int, int, int],
                         passenger_count: int) -> dict:
    floor, x, y = map(int, point)
    if floor != int(current_floor):
        return {
            "vehicle_warp": (floor, x, y),
            "passengers_warped": int(passenger_count),
            "target_xy": (x, y),
        }
    return {"vehicle_warp": None, "passengers_warped": 0, "target_xy": (x, y)}

def bus_set_point_effect(point: tuple[int, int]) -> dict:
    x, y = map(int, point)
    return {"vehicle_warp": None, "passengers_warped": 0, "target_xy": (x, y)}

def denied_item_clear(denied_ids: Sequence[int],
                      item_slots: Sequence[Optional[int]]) -> bool:
    held = {int(x) for x in item_slots if x is not None}
    return not any(int(item) in held for item in denied_ids)

def allow_items_present(allow_ids: Sequence[int],
                        item_slots: Sequence[Optional[int]]) -> bool:
    held = tuple(int(x) for x in item_slots if x is not None)
    return all(int(item) in held for item in allow_ids)

def pickup_allow_items(allow_ids: Sequence[int],
                       item_slots: Sequence[Optional[int]], *,
                       pickup_enabled: bool) -> dict:
    slots = list(item_slots)
    deleted = []
    for required in allow_ids:
        found_slot = None
        for i, value in enumerate(slots):
            if value is not None and int(value) == int(required):
                found_slot = i
                if pickup_enabled:
                    slots[i] = None
                    deleted.append(i)
                break
        if found_slot is None:
            return {
                "success": False,
                "slots": tuple(slots),
                "deleted_slots": tuple(deleted),
            }
    return {
        "success": True,
        "slots": tuple(slots),
        "deleted_slots": tuple(deleted),
    }

def stone_cost(needstone: Optional[int], gold: int) -> int:
    if needstone is None or int(needstone) == -1:
        return 0
    cost = int(needstone)
    return cost if int(gold) >= cost else -1

def boarding_check(*, in_front: bool, transport_mode: int,
                   player_party_none: bool, has_party_capacity: bool,
                   denied_ids: Sequence[int] = (),
                   allow_ids: Sequence[int] = (),
                   item_slots: Sequence[Optional[int]] = (),
                   wares_allowed: bool = True,
                   player_level: int = 1,
                   needlevel: Optional[int] = None,
                   gold: int = 0,
                   needstone: Optional[int] = None) -> dict:
    trace = []
    if not in_front:
        return {"success": False, "reason": "not_in_front", "gold_after": int(gold), "trace": tuple(trace)}
    if int(transport_mode) != 0:
        return {"success": False, "reason": "transport_not_waiting", "gold_after": int(gold), "trace": tuple(trace)}
    if not player_party_none:
        return {"success": False, "reason": "already_in_party", "gold_after": int(gold), "trace": tuple(trace)}
    if not has_party_capacity:
        return {"success": False, "reason": "transport_full", "gold_after": int(gold), "trace": tuple(trace)}

    trace.append("denied_item")
    if not denied_item_clear(denied_ids, item_slots):
        return {"success": False, "reason": "denied_item", "gold_after": int(gold), "trace": tuple(trace)}

    trace.append("wares")
    if not wares_allowed:
        return {"success": False, "reason": "wares_blocked", "gold_after": int(gold), "trace": tuple(trace)}

    trace.append("allow_item")
    if not allow_items_present(allow_ids, item_slots):
        return {"success": False, "reason": "missing_allow_item", "gold_after": int(gold), "trace": tuple(trace)}

    trace.append("min_level")
    if needlevel is not None and int(needlevel) != -1 and int(player_level) < int(needlevel):
        return {"success": False, "reason": "level_too_low", "gold_after": int(gold), "trace": tuple(trace)}

    trace.append("stone")
    cost = stone_cost(needstone, gold)
    if cost == -1:
        return {"success": False, "reason": "insufficient_stone", "gold_after": int(gold), "trace": tuple(trace)}

    return {
        "success": True,
        "reason": "eligible",
        "gold_after": int(gold) - cost,
        "stone_delta": -cost,
        "trace": tuple(trace),
        "next": "char_join_party_main",
    }

def actual_boarding_checker(kind: str) -> str:
    if kind not in ("bus", "air"):
        raise ValueError("kind must be bus or air")
    return "NPC_BusCheckJoinParty"

def normal_terminal_consumes_pickupitem() -> bool:
    return False

def individual_client_leave_consumes_pickupitem() -> bool:
    return True

def air_special_boarding_extensions_reachable_from_generic_join() -> dict:
    return {
        "NPC_AirCheckJoinParty_called": False,
        "air_delitem_on_generic_boarding": False,
        "air_maxlevel_on_generic_boarding": False,
    }
