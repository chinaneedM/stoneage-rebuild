#!/usr/bin/env python3
"""Reference model for StoneAge field warp / portal transitions.

The core path models the fixed legacy overlap Warp NPC and the shared
CHAR_warpToSpecificPoint primitive. Later mapwarp/no-exit variants are exposed
separately so they cannot be mistaken for the early/core mechanism.
"""

PARTY_NONE = 0
PARTY_LEADER = 1
PARTY_CLIENT = 2


def parse_legacy_warp_arg(arg):
    """Parse the classic 'floor|x|y|optional-time' Warp NPC argument."""
    parts = str(arg).split("|")
    if len(parts) < 3:
        return None
    try:
        floor, x, y = (int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        return None
    time_token = parts[3] if len(parts) >= 4 else None
    return {
        "destination": (floor, x, y),
        "time_token": time_token,
    }


def legacy_warp_init(arg, *, destination_valid):
    """Mirror the non-FREEMORE fixed Warp NPC initialization boundary."""
    parsed = parse_legacy_warp_arg(arg)
    if parsed is None or not bool(destination_valid):
        return {"ok": False, "enabled": False}
    return {
        "ok": True,
        "enabled": True,
        "destination": parsed["destination"],
        "invisible": True,
        "overable": True,
        "attackable": False,
    }


def overlap_warp_triggered(
    *,
    mover_is_player,
    action_is_walk,
    previous_xy,
    event_xy,
):
    """NPC_WarpWatch fires after a player actually enters the Warp NPC cell."""
    if not mover_is_player or not action_is_walk:
        return False
    if tuple(previous_xy) == tuple(event_xy):
        return False
    return True


def apply_warp(
    *,
    current_position,
    destination,
    destination_valid,
    party_mode=PARTY_NONE,
    character_type="player",
    encounter_min_before=None,
    encounter_max_before=None,
    encounter_min_at_destination=-1,
    encounter_max_at_destination=-1,
    map_objmove_ok=True,
    follow_pet_present=False,
):
    """Model _CHAR_warpToSpecificPoint at its durable state-transition boundary.

    A MAP_objmove failure is logged by the old source after character/object
    coordinates have already been assigned; it is not rolled back.
    """
    if not destination_valid:
        return {
            "ok": False,
            "position": tuple(current_position),
            "mutated": False,
        }

    out = {
        "ok": True,
        "position": tuple(destination),
        "mutated": True,
        "map_objmove_ok": bool(map_objmove_ok),
        "rolled_back_on_map_objmove_failure": False,
        "encounter_min": encounter_min_before,
        "encounter_max": encounter_max_before,
        "iswarp": None,
        "follow_pet_destination": None,
    }
    if encounter_min_at_destination != -1:
        out["encounter_min"] = encounter_min_at_destination
    if encounter_max_at_destination != -1:
        out["encounter_max"] = encounter_max_at_destination

    if character_type == "player":
        if int(party_mode) != PARTY_CLIENT:
            out["iswarp"] = True
        if follow_pet_present:
            out["follow_pet_destination"] = tuple(destination)
    return out


def legacy_overlap_direct_targets(triggering_actor):
    """Classic overlap Warp NPC directly warps only the actor that triggered it.

    Party followers may subsequently enter the same cell via normal follow
    walking and independently trigger the Warp NPC.
    """
    return (triggering_actor,)


def warpman_targets(*, talker, party_mode, leader=None, leader_party=()):
    """Dialogue WarpMan explicitly projects a destination over the party."""
    party_mode = int(party_mode)
    if party_mode == PARTY_NONE:
        return (talker,)
    if party_mode == PARTY_LEADER:
        return tuple(x for x in leader_party if x is not None)
    if party_mode == PARTY_CLIENT:
        if leader is None:
            return ()
        return tuple(x for x in leader_party if x is not None)
    return (talker,)


def later_mapwarppoint_targets(*, triggering_actor, party_mode, party_members=()):
    """Later _MAP_WARPPOINT handler: trigger actor, plus leader's valid members."""
    targets = [triggering_actor]
    if int(party_mode) == PARTY_LEADER:
        for member in tuple(party_members)[1:]:
            if member is not None and member not in targets:
                targets.append(member)
    return tuple(targets)


def later_mapwarppoint_resolution(
    *,
    source_position,
    recorded_source,
    destination,
    destination_valid,
):
    """Later mapwarp.txt path verifies source tuple and target coordinate."""
    if tuple(source_position) != tuple(recorded_source):
        return {"ok": False, "reason": "source_mismatch"}
    if not destination_valid:
        return {"ok": False, "reason": "invalid_destination"}
    if int(destination[0]) == 777:
        return {"ok": False, "reason": "floor_777_suppressed"}
    return {"ok": True, "destination": tuple(destination)}


def pack_later_noexit_point(floor, x, y):
    """Literal _MAP_NOEXIT representation used by the fixed descendants."""
    return (int(floor) << 16) + (int(x) << 8) + int(y)


def unpack_later_noexit_point(point):
    point = int(point)
    return (
        (point >> 16) & 0xFFFFFF,
        (point >> 8) & 0xFF,
        point & 0xFF,
    )


def later_noexit_redirect(
    *,
    current_position,
    elder_position,
    configured_exit,
    map_type,
    destination_floor_exists,
):
    """Model the later login-only _MAP_NOEXIT branch after appear handling.

    If map_type >= 0, the elder point is kept only when its floor equals
    map_type; otherwise the configured exit is used. With map_type < 0 the
    elder position remains preferred. Invalid resulting floors leave current
    login coordinates unchanged.
    """
    current = tuple(current_position)
    elder = tuple(elder_position) if elder_position is not None else None
    configured = tuple(configured_exit)

    candidate = elder
    if int(map_type) >= 0:
        if elder is None or elder[0] != int(map_type):
            candidate = configured

    if candidate is None or not bool(destination_floor_exists):
        return current
    return candidate


def login_redirect_order(
    *,
    saved_position,
    appear_floor_member,
    elder_position,
    noexit_entries,
):
    """Expose source ordering: appear redirect runs before later _MAP_NOEXIT."""
    current = tuple(saved_position)
    events = []

    if appear_floor_member and elder_position is not None:
        current = tuple(elder_position)
        events.append("appear_to_elder")

    entry = noexit_entries.get(current[0])
    if entry is not None:
        current = later_noexit_redirect(
            current_position=current,
            elder_position=elder_position,
            configured_exit=entry["configured_exit"],
            map_type=entry["map_type"],
            destination_floor_exists=entry.get("destination_floor_exists", True),
        )
        events.append("noexit")

    return {"position": current, "events": tuple(events)}
