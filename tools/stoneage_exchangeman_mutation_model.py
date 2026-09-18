#!/usr/bin/env python3
"""Deterministic control-flow model for StoneAge ExChangeMan mutation/accept paths."""

from dataclasses import dataclass
from typing import Mapping, Optional, Sequence

from tools.stoneage_exchangeman_condition_model import c_atoi, event_cost, get_arg_field


@dataclass(frozen=True)
class CapacityProjection:
    allowed: bool
    empty_slots: int
    projected_net_slots: int
    reason: str


def _csv(value: Optional[str]):
    return [] if value is None or value == "" else value.split(",")


def _field(argstr: str, key: str) -> Optional[str]:
    return get_arg_field(argstr, key)


def _selected_event_branch(argstr: str, one_based_index: int) -> str:
    event = _field(argstr, "EVENT")
    if not event:
        return ""
    parts = event.split(",")
    if one_based_index < 1 or one_based_index > len(parts):
        return ""
    return parts[one_based_index - 1]


def _notdel_ids(argstr: str):
    return {c_atoi(x) for x in _csv(_field(argstr, "NotDel"))}


def item_capacity_projection(
    argstr: str,
    *,
    mode: int,
    event_branch_index: int,
    carried_item_ids: Sequence[Optional[int]],
) -> CapacityProjection:
    """Mirror NPC_ItemFullCheck's slot arithmetic, including its loop-index bug."""
    carried = tuple(carried_item_ids)
    empty = sum(x is None for x in carried)
    maxitem = 0

    delete = _field(argstr, "DelItem")
    if delete:
        if "EVDEL" in delete:
            branch = _selected_event_branch(argstr, int(event_branch_index))
            excluded = _notdel_ids(argstr)
            for term in branch.split("&"):
                if "ITEM" not in term or "=" not in term:
                    continue
                rhs = term.split("=", 1)[1]
                if "*" in rhs:
                    item_s, count_s = rhs.split("*", 1)
                    item_id = c_atoi(item_s)
                    if item_id in excluded:
                        continue
                    maxitem -= c_atoi(count_s)
                else:
                    item_id = c_atoi(rhs)
                    if item_id in excluded:
                        continue
                    maxitem -= sum(x == item_id for x in carried)
        else:
            # Source reuses i for both CSV position and inventory scan.
            # Once a non-star token is processed, i exits at CHAR_MAXITEMHAVE
            # and the outer CSV loop normally terminates.
            for token in _csv(delete):
                if "*" in token:
                    _, count_s = token.split("*", 1)
                    maxitem -= c_atoi(count_s)
                    continue
                item_id = c_atoi(token)
                maxitem -= sum(x == item_id for x in carried)
                break

    rand_cnt = 0
    rand_value = _field(argstr, "GetRandItem")
    if rand_value is not None and int(mode) == 0:
        rand_cnt = 1
        if maxitem == 0 and empty == 0:
            return CapacityProjection(False, empty, maxitem, "random_item_no_room")

    getitem = _field(argstr, "GetItem")
    if getitem is not None and int(mode) == 0:
        for token in _csv(getitem):
            if "*" in token:
                _, count_s = token.split("*", 1)
                maxitem += c_atoi(count_s)
            else:
                maxitem += 1
        maxitem += rand_cnt
        if empty < maxitem:
            return CapacityProjection(False, empty, maxitem, "projected_item_full")

    return CapacityProjection(True, empty, maxitem, "ok")


def delitem_scan_domain(*, starred: bool, break_flag: bool, pile_enabled: bool = True):
    """Report the actual item-slot domain selected by NPC_EventDelItem."""
    if starred and pile_enabled and not break_flag:
        return "carried_only"
    return "all_item_slots"


def evdel_nonstar_effective_item_id(configured_item_id: int, *, pile_enabled: bool = True):
    """Active _ITEM_PILENUMS branch passes -1 for non-star EVDEL deletion."""
    return -1 if pile_enabled else int(configured_item_id)


def source_pet_random_choice(candidate_count: int, first_empty_slot: int, rand_value: int):
    """Mirror AddPet/AddEgg's reuse of first-empty slot as CSV token index.

    The legacy delimiter helper treats index 0 as a successful empty result.
    Therefore a first empty pet slot of 0 still advances through the whole
    candidate list. Starting beyond the list can, however, leave a modulus
    wider than the configured candidate count.
    """
    candidate_count = int(candidate_count)
    i = int(first_empty_slot)

    def token_exists(index):
        if index == 0:
            return True
        return 1 <= index <= candidate_count

    while token_exists(i):
        i += 1
    i -= 1
    if i == 0:
        raise ZeroDivisionError("source rand()%0 hazard")
    selected = int(rand_value) % i + 1
    if selected > candidate_count:
        return None
    return selected


def _ok(outcomes: Mapping[str, bool], key: str) -> bool:
    return bool(outcomes.get(key, True))


def _getitem_count(argstr: str) -> int:
    total = 0
    value = _field(argstr, "GetItem")
    if value is None:
        return 0
    for token in _csv(value):
        if "*" in token:
            _, count_s = token.split("*", 1)
            total += c_atoi(count_s)
        else:
            total += 1
    return total


def event_add_trace(
    argstr: str,
    *,
    mode: int,
    level: int,
    gold: int,
    carried_item_ids: Sequence[Optional[int]],
    event_branch_index: int,
    post_delete_empty_slots: Optional[int] = None,
    outcomes: Optional[Mapping[str, bool]] = None,
):
    """Model NPC_EventAdd ordering and failure propagation.

    Item/pet creation internals are delegated to their own subsystem models; this
    routine models ExChangeMan's sequencing, checks and ignored return values.
    """
    outcomes = outcomes or {}
    trace = []
    projection = item_capacity_projection(
        argstr,
        mode=mode,
        event_branch_index=event_branch_index,
        carried_item_ids=carried_item_ids,
    )
    trace.append("item_capacity_preflight")
    if not projection.allowed:
        return {"success": False, "reason": projection.reason, "gold_after": int(gold), "trace": tuple(trace)}

    delstone = _field(argstr, "DelStone")
    if delstone is not None:
        cost = event_cost(delstone, int(level))
        trace.append("delstone_affordability_check")
        if int(gold) - cost < 0:
            return {"success": False, "reason": "insufficient_stone", "gold_after": int(gold), "trace": tuple(trace)}

    if _field(argstr, "pet_skill") is not None and int(mode) == 0:
        trace.append("pet_skill_ui")
        return {"success": True, "reason": "pet_skill_early_return", "gold_after": int(gold), "trace": tuple(trace)}

    effective_mode = 0 if int(mode) == 2 else int(mode)
    if int(mode) == 2:
        trace.append("mode2_rewritten_to_mode0_after_preflight")

    if _field(argstr, "GetPet") is not None and effective_mode == 0:
        trace.append("add_pet_event_marked")
        if not _ok(outcomes, "add_pet"):
            return {"success": False, "reason": "add_pet_failed", "gold_after": int(gold), "trace": tuple(trace)}

    if _field(argstr, "GetEgg") is not None and effective_mode == 0:
        trace.append("add_egg_event_marked")
        if not _ok(outcomes, "add_egg"):
            return {"success": False, "reason": "add_egg_failed", "gold_after": int(gold), "trace": tuple(trace)}

    if _field(argstr, "DelItem") is not None:
        trace.append("delete_delitem_ignored_return")

    gold_after = int(gold)
    if delstone is not None:
        gold_after -= event_cost(delstone, int(level))
        trace.append("deduct_stone")

    rand_value = _field(argstr, "GetRandItem")
    rand_present = rand_value is not None
    rand_called = False
    getitem = _field(argstr, "GetItem")

    if getitem is not None:
        if effective_mode == 0:
            needed = _getitem_count(argstr) + (1 if rand_present else 0)
            free_after = projection.empty_slots if post_delete_empty_slots is None else int(post_delete_empty_slots)
            trace.append("post_delete_item_capacity_check")
            if free_after < needed:
                return {"success": False, "reason": "post_delete_item_full", "gold_after": gold_after, "trace": tuple(trace)}
            if rand_present:
                trace.append("grant_random_item_ignored_return")
                rand_called = True
            trace.append("grant_getitem_checked_return")
            if not _ok(outcomes, "add_item"):
                return {"success": False, "reason": "add_item_failed", "gold_after": gold_after, "trace": tuple(trace)}
        elif effective_mode == 1:
            trace.append("delete_getitem_list_ignored_return")

    if rand_present and not rand_called and effective_mode == 0:
        free_after = projection.empty_slots if post_delete_empty_slots is None else int(post_delete_empty_slots)
        trace.append("standalone_random_item_capacity_check")
        if free_after == 0:
            return {"success": False, "reason": "post_delete_item_full", "gold_after": gold_after, "trace": tuple(trace)}
        trace.append("grant_random_item_ignored_return")

    if _field(argstr, "DelPet") is not None and effective_mode == 0:
        trace.append("delete_pet_guarded_feature")
        if not _ok(outcomes, "del_pet"):
            return {"success": False, "reason": "del_pet_failed", "gold_after": gold_after, "trace": tuple(trace)}

    return {"success": True, "reason": "ok", "gold_after": gold_after, "trace": tuple(trace)}


def accept_del_trace(
    argstr: str,
    *,
    mode: int,
    level: int,
    gold: int,
    max_gold: int,
    carried_item_ids: Sequence[Optional[int]],
    event_branch_index: int,
    outcomes: Optional[Mapping[str, bool]] = None,
):
    """Model NPC_AcceptDel ordering and non-transactional failure behavior."""
    outcomes = outcomes or {}
    trace = []
    projection = item_capacity_projection(
        argstr,
        mode=mode,
        event_branch_index=event_branch_index,
        carried_item_ids=carried_item_ids,
    )
    trace.append("item_capacity_preflight")
    if not projection.allowed:
        return {"success": False, "reason": projection.reason, "gold_after": int(gold), "trace": tuple(trace)}

    delstone = _field(argstr, "DelStone")
    if delstone is not None:
        cost = event_cost(delstone, int(level))
        trace.append("delstone_affordability_check")
        if int(gold) - cost < 0:
            return {"success": False, "reason": "insufficient_stone", "gold_after": int(gold), "trace": tuple(trace)}

    getstone = _field(argstr, "GetStone")
    if getstone is not None:
        amount = c_atoi(getstone)
        trace.append("getstone_cap_check")
        if int(gold) + amount >= int(max_gold):
            return {"success": False, "reason": "stone_cap", "gold_after": int(gold), "trace": tuple(trace)}

    if _field(argstr, "pet_skill") is not None and int(mode) == 0:
        trace.append("pet_skill_ui")
        return {"success": True, "reason": "pet_skill_early_return", "gold_after": int(gold), "trace": tuple(trace)}

    gold_after = int(gold)

    if _field(argstr, "DelPet") is not None:
        trace.append("delete_pet")
        if not _ok(outcomes, "del_pet"):
            return {"success": False, "reason": "del_pet_failed", "gold_after": gold_after, "trace": tuple(trace)}

    if getstone is not None:
        gold_after += c_atoi(getstone)
        trace.append("add_stone")

    if _field(argstr, "GetPet") is not None:
        trace.append("add_pet_unmarked")
        if not _ok(outcomes, "add_pet"):
            return {"success": False, "reason": "add_pet_failed", "gold_after": gold_after, "trace": tuple(trace)}

    if _field(argstr, "GetEgg") is not None:
        trace.append("add_egg_unmarked")
        if not _ok(outcomes, "add_egg"):
            return {"success": False, "reason": "add_egg_failed", "gold_after": gold_after, "trace": tuple(trace)}

    if _field(argstr, "DelItem") is not None:
        trace.append("delete_delitem_ignored_return")

    if delstone is not None:
        gold_after -= event_cost(delstone, int(level))
        trace.append("deduct_stone")

    if _field(argstr, "GetRandItem") is not None:
        trace.append("grant_random_item_ignored_return")

    if _field(argstr, "GetItem") is not None:
        trace.append("grant_getitem_ignored_return")

    trace.append("recompute_player_parameters")
    return {"success": True, "reason": "ok", "gold_after": gold_after, "trace": tuple(trace)}


def apply_flag_mutations(
    *,
    now_flags=(),
    end_flags=(),
    event_no: int = -1,
    prime_now: bool = False,
    end_set=(),
    clean=(),
):
    """Model the common ExChangeMan flag helpers used after successful mutation."""
    now = set(int(x) for x in now_flags)
    end = set(int(x) for x in end_flags)
    trace = []

    if prime_now and int(event_no) != -1:
        now.add(int(event_no))
        trace.append(("set_now", int(event_no)))

    if tuple(end_set):
        if int(event_no) != -1:
            # NPC_NowEventSetFlgCls is a blind XOR toggle, not a safe clear.
            if int(event_no) in now:
                now.remove(int(event_no))
            else:
                now.add(int(event_no))
            trace.append(("toggle_now", int(event_no)))
        for value in end_set:
            end.add(int(value))
            trace.append(("set_end", int(value)))

    for value in clean:
        value = int(value)
        now.discard(value)
        end.discard(value)
        trace.append(("clear_now_and_end_if_present", value))

    return {"now_flags": frozenset(now), "end_flags": frozenset(end), "trace": tuple(trace)}
