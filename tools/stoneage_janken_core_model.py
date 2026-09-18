#!/usr/bin/env python3
"""Deterministic reference model for the fixed-descendant StoneAge Janken core."""

from collections import Counter
from dataclasses import dataclass
from typing import Optional, Sequence

@dataclass(frozen=True)
class EntryToken:
    item_id: int
    quantity: Optional[int] = None

def parse_item_tokens(spec: str) -> tuple[EntryToken, ...]:
    if not spec:
        return ()
    out=[]
    for raw in spec.split(","):
        if "*" in raw:
            item,count=raw.split("*",1)
            out.append(EntryToken(int(item or 0),int(count or 0)))
        else:
            out.append(EntryToken(int(raw or 0),None))
    return tuple(out)

def entry_check(tokens: Sequence[EntryToken], item_ids: Sequence[int]) -> bool:
    """Every token checks the original inventory independently."""
    counts=Counter(int(x) for x in item_ids)
    for token in tokens:
        need=1 if token.quantity is None else int(token.quantity)
        if counts[int(token.item_id)] < need:
            return False
    return True

def entry_delete(tokens: Sequence[EntryToken], item_ids: Sequence[int]) -> dict:
    """Delete in source order; a plain token deletes every remaining copy."""
    items=list(map(int,item_ids))
    deleted=[]
    for token in tokens:
        if token.quantity is None:
            for i,value in enumerate(items):
                if value==int(token.item_id):
                    deleted.append(value)
                    items[i]=None
        else:
            count=0
            for i,value in enumerate(items):
                if value==int(token.item_id):
                    deleted.append(value)
                    items[i]=None
                    count+=1
                    if count==int(token.quantity):
                        break
    return {
        "items_after":tuple(x for x in items if x is not None),
        "deleted_count":len(deleted),
        "deleted_ids":tuple(deleted),
    }

def start_after_yes(entry_spec: Optional[str], item_ids: Sequence[int]) -> dict:
    """Mirror selectWindow case 1, including the failed-check fallthrough."""
    events=[]
    if entry_spec is not None:
        tokens=parse_item_tokens(entry_spec)
        enough=entry_check(tokens,item_ids)
        if not enough:
            events.append("send_no_item_window")
        deletion=entry_delete(tokens,item_ids)
        events.append("delete_entry_items")
        items_after=deletion["items_after"]
        deleted_count=deletion["deleted_count"]
    else:
        enough=True
        items_after=tuple(map(int,item_ids))
        deleted_count=0
    events.append("send_janken_selection")
    return {
        "continues_to_game":True,
        "entry_check_passed":enough,
        "items_after":items_after,
        "deleted_count":deleted_count,
        "events":tuple(events),
    }

def player_hand_from_selection(selection: int) -> int:
    if int(selection)==3:
        return 0
    if int(selection)==5:
        return 1
    if int(selection)==7:
        return 2
    return -1

def judge(selection: int, npc_hand: int) -> str:
    player=player_hand_from_selection(selection)
    npc=int(npc_hand)%3
    if player < 0 or player==npc:
        return "tie"
    if (player,npc) in ((2,0),(0,1),(1,2)):
        return "win"
    return "lose"

def result_flow(selection: int, npc_hand: int, *,
                win_item_configured: bool = False,
                lose_item_configured: bool = False,
                reward_add_succeeds: bool = True,
                win_warp: Optional[tuple[int,int,int]] = None,
                lose_warp: Optional[tuple[int,int,int]] = None) -> dict:
    result=judge(selection,npc_hand)
    if result=="tie":
        return {
            "result":"tie",
            "events":("send_tie_selection",),
            "warp":None,
        }

    events=[]
    reward_configured=(
        win_item_configured if result=="win" else lose_item_configured
    )
    if reward_configured:
        events.append("attempt_reward_item_ignored_return")

    warp=win_warp if result=="win" else lose_warp
    events.append("warp_player")
    events.append("set_result_action")
    events.append("send_result_window")
    return {
        "result":result,
        "reward_configured":reward_configured,
        "reward_add_succeeds":bool(reward_add_succeeds),
        "warp":warp,
        "events":tuple(events),
    }

def warp_tuple(value: str) -> tuple[int,int,int]:
    parts=value.split(",")
    def atoi(index):
        if index>=len(parts):
            return 0
        try:
            return int(parts[index].strip())
        except ValueError:
            return 0
    return (atoi(0),atoi(1),atoi(2))
