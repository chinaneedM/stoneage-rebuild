"""Typed, bounded BattleModel inputs for the existing ordinary round driver.

No round-model import: the ordinary driver owns command/status timing and
passes current work to the accepted physical loop. Normal death and newly
lethal ultimate/Exit each require their explicit profit integration scope.
Living reflected ultimate flags remain outside the admitted domain.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_enemy_ai_battlemodel_bridge import EnemyAiBattleModelSubmission
from tools.stoneage_battlemodel_hit_loop import (
    BattleModelDraw, BattleModelEntry, ITEMCRUSH_HIT_LOOP_SCOPE_R1, _int,
)
from tools.stoneage_battlemodel_physical_attackseq import (
    BattleModelPhysicalContext, execute_battlemodel_physical_loop,
)
from tools.stoneage_battlemodel_itemcrush_model import BattleModelItemCrushContext

BATTLEMODEL_ORDINARY_SCOPE_R1 = "nonlethal_base_round_empty_equipment_ID638_R1"
BATTLEMODEL_LETHAL_PROFIT_SCOPE_R1 = (
    "lethal_normal_profit_base_round_empty_equipment_ID638_R1"
)
BATTLEMODEL_ULTIMATE_EXIT_SCOPE_R1 = (
    "lethal_ultimate_exit_profit_base_round_empty_equipment_ID638_R1"
)
_BATTLEMODEL_ROUND_SCOPES_R1 = frozenset({
    BATTLEMODEL_ORDINARY_SCOPE_R1,
    BATTLEMODEL_LETHAL_PROFIT_SCOPE_R1,
    BATTLEMODEL_ULTIMATE_EXIT_SCOPE_R1,
})
_BATTLEMODEL_DEATH_SCOPES_R1 = frozenset({
    BATTLEMODEL_LETHAL_PROFIT_SCOPE_R1,
    BATTLEMODEL_ULTIMATE_EXIT_SCOPE_R1,
})


@dataclass(frozen=True)
class BattleModelRoundAction:
    scope: str
    submission: EnemyAiBattleModelSubmission
    physical_context: BattleModelPhysicalContext
    itemcrush_context: BattleModelItemCrushContext
    opposing_slot_order: tuple[int, ...]
    paralysis_resistance_by_slot: Mapping[int, int]
    draws: tuple[BattleModelDraw, ...]

    def __post_init__(self):
        if self.scope not in _BATTLEMODEL_ROUND_SCOPES_R1:
            raise ValueError("explicit bounded BattleModel ordinary scope required")
        if not isinstance(self.submission, EnemyAiBattleModelSubmission):
            raise TypeError("typed BattleModel submission required")
        if not isinstance(self.physical_context, BattleModelPhysicalContext):
            raise TypeError("typed physical context required")
        if not isinstance(self.itemcrush_context, BattleModelItemCrushContext):
            raise TypeError("typed empty-equipment ItemCrush context required")
        order = self.opposing_slot_order
        if type(order) is not tuple or len(set(order)) != len(order):
            raise ValueError("explicit unique opposing slot order required")
        for slot in order:
            _int(slot, "opposing slot", 0, 9)
        resistances = dict(self.paralysis_resistance_by_slot)
        for slot, value in resistances.items():
            _int(slot, "resistance slot", 0, 19)
            _int(value, "paralysis resistance", -(2**31), 2**31-1)
        if type(self.draws) is not tuple or any(not isinstance(d, BattleModelDraw) for d in self.draws):
            raise TypeError("typed chronological BattleModel draw tuple required")
        object.__setattr__(self, "paralysis_resistance_by_slot", MappingProxyType(resistances))


def execute_current_battlemodel_round_action(
    action: BattleModelRoundAction, *, actor_slot: int, by_slot, hp_by_slot,
    status_runtime, damage_react_state, ultimate_overkill, guarding_slots,
    cleared_command_ids, ultimate_marked_slots, exited_slots, battle_abio,
):
    """Read dynamic work after the ordinary actor's status tick, without RNG replay."""
    entries = {slot: BattleModelEntry(
        p.participant_id, p.kind, hp_by_slot[slot], p.max_hp,
        action.paralysis_resistance_by_slot[slot],
        status_runtime=status_runtime[p.participant_id],
        reaction=damage_react_state[p.participant_id],
        accumulated_overkill=ultimate_overkill[p.participant_id],
        command_cleared=p.participant_id in cleared_command_ids,
        ultimate_flag=bool(ultimate_marked_slots.get(slot, 0)),
        abio=battle_abio.get(p.participant_id, False),
        target_check_allowed=slot not in exited_slots,
    ) for slot, p in by_slot.items()}
    living = tuple(slot for slot in action.opposing_slot_order if entries[slot].live_target)
    if not living:
        if action.draws:
            raise ValueError("BattleModel no-target action cannot consume RNG")
        return None
    context = replace(action.physical_context, profiles={
        slot: replace(profile, command="guard" if slot in guarding_slots else "none",
            quick=(entries[slot].status_runtime.work_quick
                   if entries[slot].status_runtime.work_quick is not None else profile.quick))
        for slot, profile in action.physical_context.profiles.items()
    })
    flags = tuple(bool(ultimate_marked_slots.get(s, 0)) for s in range(20))
    result = execute_battlemodel_physical_loop(action.submission, actor_slot=actor_slot,
        execution_scope=ITEMCRUSH_HIT_LOOP_SCOPE_R1, entries=entries,
        initial_living_slots=living, draws=action.draws, context=context,
        source_pet_guard_flags=flags, itemcrush_context=action.itemcrush_context)
    ultimate_entries = tuple(
        (s,e) for s,e in result.entries.items() if e.ultimate_flag
    )
    if ultimate_entries:
        if action.scope != BATTLEMODEL_ULTIMATE_EXIT_SCOPE_R1:
            raise ValueError(
                "BattleModel ultimate flags require explicit ultimate-exit scope"
            )
        if any(
            entries[s].hp <= 0 or e.hp > 0
            for s,e in ultimate_entries
        ):
            raise ValueError(
                "BattleModel ultimate-exit scope requires a newly lethal ultimate flag"
            )
    normal_death = any(
        entries[s].hp > 0 and e.hp == 0
        for s, e in result.entries.items()
    )
    if normal_death and action.scope not in _BATTLEMODEL_DEATH_SCOPES_R1:
        raise ValueError("BattleModel death requires explicit lethal-profit scope")
    return result
