#!/usr/bin/env python3
"""Deterministic reference model for the active StoneAge NPCEnemy core."""

from dataclasses import dataclass
from typing import Optional, Sequence

DEFAULT_REVIVAL_SECONDS = 120
NORMAL_ENEMY_LIMIT = 10
GYM_ENEMY_LIMIT = 64

@dataclass(frozen=True)
class EnemySpec:
    enemy_id: int
    valid: bool = True
    big: bool = False

@dataclass(frozen=True)
class FreeState:
    level: int = 1
    equipment_ids: tuple[int, ...] = ()
    end_flags: frozenset[int] = frozenset()
    now_flags: frozenset[int] = frozenset()

def normalize_entype(value: int) -> int:
    value = int(value)
    return value if value in (1, 2) else 0

def normalize_dieact(value: int) -> int:
    return 1 if int(value) == 1 else 0

def normalize_onebattle(value: int) -> int:
    return 1 if int(value) == 1 else 0

def revival_seconds(value: Optional[int]) -> int:
    return DEFAULT_REVIVAL_SECONDS if value is None or int(value) == -1 else int(value)

def trigger_allowed(entype: int, trigger: str) -> bool:
    entype = normalize_entype(entype)
    if trigger == "walk":
        return entype != 1
    if trigger == "talk":
        return entype != 0
    raise ValueError("trigger must be walk or talk")

def required_items_present(required_ids: Sequence[int], item_slots: Sequence[Optional[int]]) -> bool:
    held = tuple(x for x in item_slots if x is not None)
    for item_id in list(required_ids)[: len(item_slots)]:
        if int(item_id) not in held:
            return False
    return True

def normal_enemy_formation(candidates: Sequence[EnemySpec]) -> tuple[int, ...]:
    table: list[Optional[EnemySpec]] = [None] * (NORMAL_ENEMY_LIMIT + 1)
    insert = 0
    bigcnt = 0
    for spec in list(candidates)[:NORMAL_ENEMY_LIMIT]:
        if not spec.valid:
            continue
        cur = spec
        if cur.big:
            if bigcnt >= 5:
                continue
            if insert > 4:
                target = None
                for j in range(5):
                    existing = table[j]
                    if existing is None:
                        break
                    if not existing.big:
                        target = j
                        break
                if target is None:
                    continue
                table[insert] = table[target]
                table[target] = cur
            else:
                table[insert] = cur
            bigcnt += 1
        else:
            table[insert] = cur
        insert += 1
        if insert >= NORMAL_ENEMY_LIMIT:
            break
    return tuple(x.enemy_id for x in table[:insert] if x is not None)

def gym_enemy_formation(
    enemy_candidates: Sequence[EnemySpec],
    pet_candidates: Sequence[EnemySpec] = (),
    *,
    enemy_pick: int = 0,
    pet_pick: int = 0,
) -> tuple[int, ...]:
    main = [x.enemy_id for x in list(enemy_candidates)[:GYM_ENEMY_LIMIT] if x.valid]
    if not main:
        return ()
    out = [main[int(enemy_pick) % len(main)]]
    pets = [x.enemy_id for x in list(pet_candidates)[:GYM_ENEMY_LIMIT] if x.valid]
    if pets:
        out.append(pets[int(pet_pick) % len(pets)])
    return tuple(out)

def battle_mode(gym: int) -> dict:
    gym = int(gym)
    if gym > 0:
        return {
            "battle_create_mode": 2,
            "baselevel": gym,
            "norisk": True,
            "skin_leader_from_npc": True,
        }
    return {
        "battle_create_mode": 1,
        "baselevel": 0,
        "norisk": False,
        "skin_leader_from_npc": False,
    }

def encounter_route(
    *,
    image_visible: bool,
    entype: int,
    trigger: str,
    required_item_ids: Sequence[int] = (),
    item_slots: Sequence[Optional[int]] = (),
    onebattle: int = 0,
    same_npc_battle_active: bool = False,
    party_client: bool = False,
    askbattle_prompt: bool = False,
) -> dict:
    trace = []
    if not image_visible:
        return {"accepted": False, "route": "hidden", "trace": tuple(trace)}
    trace.append("trigger_gate")
    if not trigger_allowed(entype, trigger):
        return {"accepted": False, "route": "denied_trigger", "trace": tuple(trace)}
    if required_item_ids:
        trace.append("item_gate")
        if not required_items_present(required_item_ids, item_slots):
            return {"accepted": False, "route": "denied_item", "trace": tuple(trace)}
    if normalize_onebattle(onebattle) and same_npc_battle_active:
        trace.append("onebattle_gate")
        return {"accepted": False, "route": "already_battling", "trace": tuple(trace)}
    if party_client:
        trace.append("party_client_skip")
        return {"accepted": True, "route": "party_client_no_battle", "trace": tuple(trace)}
    if askbattle_prompt:
        trace.append("askbattle_prompt")
        return {"accepted": False, "route": "prompt", "trace": tuple(trace)}
    trace.append("battle_in")
    return {"accepted": True, "route": "battle", "trace": tuple(trace)}

def steal_items(item_slots: Sequence[Optional[int]], target_ids: Sequence[int]) -> dict:
    slots = list(item_slots)
    deleted = []
    found = 0
    for target in list(target_ids)[: len(item_slots)]:
        for j, item_id in enumerate(slots):
            if item_id is not None and int(item_id) == int(target):
                slots[j] = None
                deleted.append(j)
                found += 1
                break
        if not found:
            break
    return {"slots": tuple(slots), "deleted_slots": tuple(deleted), "found_count": found}

def steal_phase(steal_value: Optional[int]) -> str:
    if steal_value is None:
        return "none"
    if int(steal_value) == 0:
        return "after_battle_created"
    if int(steal_value) == 1:
        return "after_win"
    return "none"

def old_death_action(dieact: int, *, revival: int = DEFAULT_REVIVAL_SECONDS) -> dict:
    if normalize_dieact(dieact) == 0:
        return {
            "action": "hide_then_revive",
            "image_after": 0,
            "event_type_after": "alternative",
            "loop_interval_ms": 5000,
            "revival_seconds": int(revival),
        }
    return {"action": "warp_winning_entries", "discharge_party_before_warp": True}

def revival_ready(now_seconds: int, death_seconds: int, revival: int) -> bool:
    return int(now_seconds) > int(death_seconds) + int(revival)

def _relation(actual: int, expected: int, op: str) -> bool:
    if op == "=":
        return actual == expected
    if op == "<":
        return actual < expected
    if op == ">":
        return actual > expected
    if op == "!=":
        return actual != expected
    return False

def eval_active_free_term(term: str, state: FreeState) -> bool:
    op = None
    for candidate in ("!=", "<", ">", "="):
        if candidate in term:
            op = candidate
            left, right = term.split(candidate, 1)
            break
    if op is None:
        return False
    try:
        value = int(right.strip())
    except ValueError:
        value = 0
    key = left.strip()
    if key == "LV":
        return _relation(int(state.level), value, op)
    if key == "EQUIT":
        if op == "=":
            return value in state.equipment_ids
        if op == "!=":
            return value not in state.equipment_ids
        return any(_relation(int(item), value, op) for item in state.equipment_ids)
    if key == "ENDEV":
        present = value in state.end_flags
        return (not present) if op == "!=" else present
    if key == "NOWEV":
        present = value in state.now_flags
        return (not present) if op == "!=" else present
    return False

def eval_active_free_expression(expr: str, state: FreeState) -> bool:
    for branch in expr.split(","):
        terms = [term.strip() for term in branch.split("&") if term.strip()]
        if terms and all(eval_active_free_term(term, state) for term in terms):
            return True
    return False

def choose_new_warp_segment(
    segments: Sequence[dict],
    state: FreeState,
    *,
    warp_pick: int = 0,
) -> Optional[dict]:
    for seg in segments:
        if not seg.get("newevent"):
            continue
        free = seg.get("free")
        if not free or not eval_active_free_expression(str(free), state):
            continue
        warps = list(seg.get("warps") or ())[:15]
        if not warps:
            continue
        chosen = warps[int(warp_pick) % len(warps)]
        if int(chosen[0]) <= 0:
            chosen = warps[0]
        party = not bool(seg.get("checkparty_false"))
        return {
            "warp": tuple(map(int, chosen)),
            "party": party,
            "run_event_action": party,
        }
    return None

def new_warp_application(*, party_flag: bool, is_party_leader: bool, party_member_count: int) -> dict:
    if party_flag:
        return {
            "mode": "individual",
            "discharge_party": True,
            "warped_count": 1,
            "early_return": False,
        }
    if is_party_leader:
        return {
            "mode": "whole_party",
            "discharge_party": False,
            "warped_count": int(party_member_count),
            "early_return": True,
        }
    return {
        "mode": "skip_nonleader",
        "discharge_party": False,
        "warped_count": 0,
        "early_return": False,
    }
