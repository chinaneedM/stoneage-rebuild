#!/usr/bin/env python3
"""Reference model for the convergent five-player StoneAge party/formation core."""

PARTY_NONE = 0
PARTY_LEADER = 1
PARTY_CLIENT = 2

PARTY_MAX = 5
BATTLE_PLAYER_MAX = 5
PET_BATTLE_OFFSET = 5
BATTLE_ENTRY_MAX = 10


def _normalize_slot(value):
    if value is None:
        return None
    value = int(value)
    return None if value == -1 else value


def normalize_slots(slots):
    values = tuple(_normalize_slot(v) for v in slots)
    if len(values) != PARTY_MAX:
        raise ValueError("baseline party roster must contain exactly five slots")
    return values


def first_empty_member_slot(slots):
    """Mirror CHAR_getEmptyPartyArray: slot 0 is leader-only, scan 1..4."""
    values = normalize_slots(slots)
    for index in range(1, PARTY_MAX):
        if values[index] is None:
            return index
    return -1


def join_member(leader_id, slots, leader_mode, member_id):
    """Apply the stable CHAR_JoinParty_Main roster mutation."""
    leader_id = int(leader_id)
    member_id = int(member_id)
    values = list(normalize_slots(slots))
    leader_mode = int(leader_mode)

    if leader_mode not in (PARTY_NONE, PARTY_LEADER):
        raise ValueError("target must normalize to a standalone character or leader")
    if member_id == leader_id:
        raise ValueError("leader cannot join itself as a client")
    if member_id in values:
        raise ValueError("member already present")

    slot = first_empty_member_slot(values)
    if slot < 0:
        raise ValueError("party full")

    first_join = leader_mode == PARTY_NONE
    if first_join:
        values[0] = leader_id
        leader_mode = PARTY_LEADER
    elif values[0] != leader_id:
        raise ValueError("leader mode requires slot 0 to contain the leader")

    values[slot] = member_id
    return {
        "leader_mode": leader_mode,
        "slots": tuple(values),
        "joined_slot": slot,
        "first_join": first_join,
        "member_mode": PARTY_CLIENT,
        "member_leader_pointer": leader_id,
    }


def client_leave(leader_id, slots, member_id):
    """Apply the common client-leave behavior without compacting party slots.

    When the last client leaves, the leader's logical mode becomes NONE while
    raw slot 0 can remain the leader's own index, matching the preserved code.
    """
    leader_id = int(leader_id)
    member_id = int(member_id)
    values = list(normalize_slots(slots))
    if values[0] != leader_id:
        raise ValueError("slot 0 must contain the leader")

    try:
        slot = values.index(member_id, 1)
    except ValueError as exc:
        raise ValueError("member not present") from exc

    values[slot] = None
    any_clients = any(v is not None for v in values[1:])
    return {
        "leader_mode": PARTY_LEADER if any_clients else PARTY_NONE,
        "slots": tuple(values),
        "left_slot": slot,
        "member_mode": PARTY_NONE,
        "member_leader_pointer": None,
        "party_still_active": any_clients,
    }


def leader_disband(slots):
    """Leader discharge clears every ordinary party slot."""
    values = normalize_slots(slots)
    removed = tuple(v for v in values if v is not None)
    return {
        "slots": (None,) * PARTY_MAX,
        "leader_mode": PARTY_NONE,
        "removed_members": removed,
    }


def resolve_party_leader(character_id, party_mode, party_index1):
    """Resolve the common leader identity used by party-aware code."""
    character_id = int(character_id)
    party_mode = int(party_mode)
    if party_mode == PARTY_LEADER:
        return character_id
    if party_mode == PARTY_CLIENT:
        if party_index1 is None or int(party_index1) < 0:
            return None
        return int(party_index1)
    if party_mode == PARTY_NONE:
        return None
    raise ValueError("unknown party mode")


def same_party(
    first_id, first_mode, first_leader_pointer,
    second_id, second_mode, second_leader_pointer,
):
    """Mirror the parent comparison used before party-aware PvP creation."""
    p0 = resolve_party_leader(first_id, first_mode, first_leader_pointer)
    p1 = resolve_party_leader(second_id, second_mode, second_leader_pointer)
    return p0 is not None and p0 == p1


def field_follow_chain(slots):
    """Return the slot-ordered follow-the-leader chain, skipping holes."""
    values = normalize_slots(slots)
    ordered = tuple(v for v in values if v is not None)
    return tuple(zip(ordered, ordered[1:]))


def direct_walk_allowed(party_mode, movement_mode):
    """Clients may turn, but ordinary direct positional walking is suppressed."""
    party_mode = int(party_mode)
    movement_mode = int(movement_mode)
    if movement_mode not in (0, 1):
        raise ValueError("movement_mode must be 0 (walk) or 1 (turn)")
    if party_mode == PARTY_CLIENT and movement_mode == 0:
        return False
    return True


def _pet_can_enter(pet):
    if pet is None:
        return False
    if not bool(pet.get("valid", True)):
        return False
    if bool(pet.get("dead", False)):
        return False
    return int(pet.get("hp", 0)) > 0


def battle_projection(slots, default_pet_by_player=None, member_battle_mode=None):
    """Project the field roster into the common 10-slot player-side layout.

    Valid party members are compacted into player battle slots 0..4 in field
    party-slot order. Each valid default pet is paired at player_slot + 5.
    Members in a non-none battle mode are skipped, matching PartyNewEntry's
    ordinary member gate. The initiating slot-0 player is always projected.
    """
    values = normalize_slots(slots)
    default_pet_by_player = default_pet_by_player or {}
    member_battle_mode = member_battle_mode or {}

    ordered_players = []
    for source_slot, player in enumerate(values):
        if player is None:
            continue
        if source_slot > 0 and member_battle_mode.get(player, "none") != "none":
            continue
        ordered_players.append((source_slot, player))

    if len(ordered_players) > BATTLE_PLAYER_MAX:
        raise ValueError("baseline battle player capacity exceeded")

    entries = [None] * BATTLE_ENTRY_MAX
    reset_default_pet = []
    placements = []

    for player_slot, (source_slot, player) in enumerate(ordered_players):
        entries[player_slot] = ("player", player)
        pet = default_pet_by_player.get(player)
        pet_slot = None
        if pet is not None:
            if _pet_can_enter(pet):
                pet_slot = player_slot + PET_BATTLE_OFFSET
                entries[pet_slot] = ("pet", int(pet["id"]))
            else:
                reset_default_pet.append(player)
        placements.append(
            {
                "field_party_slot": source_slot,
                "player": player,
                "battle_player_slot": player_slot,
                "battle_pet_slot": pet_slot,
            }
        )

    return {
        "entries": tuple(entries),
        "placements": tuple(placements),
        "reset_default_pet_for": tuple(reset_default_pet),
    }
