"""Bounded ID638 handoff to an already ordered base-command round.

This experimental seam preserves the current hit-loop state and cancels
already prepared commands. It does not commit PersistentBattleState, perform
profit/ultimate exits, or enable the ordinary coordinator's AI dispatcher.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK, BATTLE_COM_GUARD, BATTLE_COM_NONE, BATTLE_COM_WAIT,
    BattleCommand, PreparedBattleRound,
)
from tools.stoneage_battle_status_model import active_base_status_names
from tools.stoneage_battlemodel_hit_loop import (
    BattleModelEntry, BattleModelDraw, BattleModelHitLoopResolution,
    ITEMCRUSH_HIT_LOOP_SCOPE_R1, _int,
)
from tools.stoneage_battlemodel_itemcrush_model import BattleModelItemCrushContext
from tools.stoneage_battlemodel_physical_attackseq import (
    BattleModelPhysicalContext, execute_battlemodel_physical_loop,
)
from tools.stoneage_enemy_ai_battlemodel_bridge import EnemyAiBattleModelSubmission

PREPARED_HANDOFF_SCOPE_R1 = "base_commands_prepared_empty_equipment_ID638_R1"
_BASE = frozenset({BATTLE_COM_ATTACK, BATTLE_COM_GUARD, BATTLE_COM_NONE, BATTLE_COM_WAIT})


def reset_battlemodel_round_flags(entries: Mapping[int, BattleModelEntry]):
    """Explicit new-preparation boundary; status/HP/reactions/overkill survive.

    Only use when preparing a NEW round after exit/profit settlement. This
    does not reactivate exited participants or decide their battle occupancy.
    """
    current = dict(entries)
    for slot, entry in current.items():
        _int(slot, "entry slot", 0, 19)
        if not isinstance(entry, BattleModelEntry):
            raise TypeError("typed BattleModel entries required")
        current[slot] = replace(entry, command_cleared=False, ultimate_flag=False)
    return MappingProxyType(current)


@dataclass(frozen=True)
class BattleModelPreparedHandoff:
    prepared: PreparedBattleRound
    entries: Mapping[int, BattleModelEntry]
    slots: Mapping[str, int]
    completed_prefix: tuple[str, ...]
    commands_by_participant_id: Mapping[str, BattleCommand]
    guarding_slots: frozenset[int]
    source_pet_guard_flags: tuple[bool, ...]
    loop: BattleModelHitLoopResolution

    def ordinary_continuation(self) -> PreparedBattleRound:
        """Full slot graph with completed actors disabled, without re-sorting.

        Caller must supply this handoff's current status/reaction/overkill
        snapshots to resolve_ordinary_round. Ultimate flag propagation and
        exit/profit scheduling are not yet integrated: fail closed on flags.
        """
        if any(self.source_pet_guard_flags):
            raise ValueError("ultimate flags require exit/profit integration before ordinary continuation")
        if any(event.hp_loss > 0 and event.actual_defender_slot is not None
               and self.entries[event.actual_defender_slot].hp == 0 for event in self.loop.events):
            raise ValueError("BattleModel death requires profit integration before ordinary continuation")
        done = set(self.completed_prefix)
        ordered = tuple(replace(entry, command=replace(entry.command, input_complete=False))
                        if entry.participant.participant_id in done else entry
                        for entry in self.prepared.ordered_entries)
        return _view(self.prepared, ordered)

    @property
    def status_runtime_by_participant_id(self):
        return MappingProxyType({entry.participant_id: entry.status_runtime
                                 for entry in self.entries.values()})

    @property
    def reaction_by_participant_id(self):
        return MappingProxyType({entry.participant_id: entry.reaction
                                 for entry in self.entries.values()})

    @property
    def overkill_by_participant_id(self):
        return MappingProxyType({entry.participant_id: entry.accumulated_overkill
                                 for entry in self.entries.values()})


def _view(prepared, ordered):
    executable = tuple(entry for entry in ordered if entry.ready_to_execute)
    return PreparedBattleRound(ordered, executable,
        tuple(entry for entry in executable if not entry.command.produces_action),
        prepared.tie_break_was_required)


def execute_battlemodel_prepared_handoff(
    prepared: PreparedBattleRound, submission: EnemyAiBattleModelSubmission, *,
    scope: str, slots: Mapping[str, int], entries: Mapping[int, BattleModelEntry],
    completed_prefix: tuple[str, ...], initial_living_slots: tuple[int, ...],
    draws: tuple[BattleModelDraw, ...], physical_context: BattleModelPhysicalContext,
    itemcrush_context: BattleModelItemCrushContext,
    source_pet_guard_flags: tuple[bool, ...],
) -> BattleModelPreparedHandoff:
    """Execute the next symbolic BattleModel actor, then update prepared work.

    Its prepared COM1 must be NONE, an explicit internal carrier ONLY; the
    typed submission supplies the symbolic identity, never a guessed enum.
    completed_prefix is the authoritative already-executed ordered prefix.
    Entries are the current work snapshot at that cursor, not original HP.
    Existing clearing remains round-local and is never inferred from status.
    """
    if scope != PREPARED_HANDOFF_SCOPE_R1:
        raise ValueError("explicit prepared handoff scope required")
    if not isinstance(prepared, PreparedBattleRound):
        raise TypeError("typed prepared round required")
    if not isinstance(submission, EnemyAiBattleModelSubmission):
        raise TypeError("typed BattleModel submission required")
    if not isinstance(physical_context, BattleModelPhysicalContext):
        raise TypeError("typed physical context required")
    if not isinstance(itemcrush_context, BattleModelItemCrushContext):
        raise TypeError("typed empty-equipment ItemCrush context required")
    current, slot_map = dict(entries), dict(slots)
    ordered = prepared.ordered_entries
    ids = tuple(entry.participant.participant_id for entry in ordered)
    if len(set(ids)) != len(ids) or set(ids) != set(slot_map):
        raise ValueError("prepared participant/slot coverage mismatch")
    if len(set(slot_map.values())) != len(slot_map) or set(slot_map.values()) != set(current):
        raise ValueError("prepared slot/entry coverage mismatch")
    if type(completed_prefix) is not tuple or completed_prefix != ids[:len(completed_prefix)]:
        raise ValueError("completed actions must be the exact ordered prefix")
    cursor = len(completed_prefix)
    if cursor >= len(ids) or ids[cursor] != submission.participant_id:
        raise ValueError("BattleModel must be the next unexecuted prepared actor")
    for entry in ordered:
        pid = entry.participant.participant_id
        slot = _int(slot_map[pid], "prepared slot", 0, 19)
        work = current[slot]
        if not isinstance(work, BattleModelEntry):
            raise TypeError("typed current entries required")
        if (work.participant_id, work.kind, work.max_hp) != (pid, entry.participant.kind, entry.participant.max_hp):
            raise ValueError("prepared/current participant identity drift")
        if entry.participant.side != ("player" if slot < 10 else "enemy"):
            raise ValueError("prepared participant crossed battle sides")
        if entry.command.command1 not in _BASE or entry.combo_id:
            raise ValueError("prepared handoff admits only noncombo base commands")
    actor_slot = slot_map[submission.participant_id]
    actor = current[actor_slot]
    carrier = ordered[cursor].command
    if carrier.command1 != BATTLE_COM_NONE:
        raise ValueError("symbolic BattleModel requires explicit internal NONE carrier")
    if (not carrier.input_complete or not actor.live_target or actor.command_cleared
        or active_base_status_names(actor.status_runtime.status)):
        raise ValueError("prepared BattleModel actor is not executable at this cursor")
    if set(physical_context.profiles) != set(current):
        raise ValueError("physical profiles must exactly cover prepared entries")
    # Command is read from prepared work, not caller-supplied physical labels.
    # Hit-loop command_cleared suppresses GUARD immediately within this call.
    commands = {pid: next(e.command for e in ordered if e.participant.participant_id == pid)
                for pid in ids}
    for slot, work in current.items():
        if work.command_cleared:
            commands[work.participant_id] = replace(commands[work.participant_id], command1=BATTLE_COM_NONE)
    context = replace(physical_context, profiles={
        slot: replace(profile, command="guard" if commands[current[slot].participant_id].command1 == BATTLE_COM_GUARD else "none")
        for slot, profile in physical_context.profiles.items()
    })
    loop = execute_battlemodel_physical_loop(submission, actor_slot=actor_slot,
        execution_scope=ITEMCRUSH_HIT_LOOP_SCOPE_R1, entries=current,
        initial_living_slots=initial_living_slots, draws=draws, context=context,
        itemcrush_context=itemcrush_context, source_pet_guard_flags=source_pet_guard_flags)
    for slot in loop.cleared_command_slots:
        pid = loop.entries[slot].participant_id
        commands[pid] = replace(commands[pid], command1=BATTLE_COM_NONE)
    updated = tuple(replace(entry,
        participant=replace(entry.participant, hp=loop.entries[slot_map[entry.participant.participant_id]].hp),
        command=commands[entry.participant.participant_id]) for entry in ordered)
    flags = list(source_pet_guard_flags)
    for slot, work in loop.entries.items():
        flags[slot] = work.ultimate_flag
    return BattleModelPreparedHandoff(_view(prepared, updated), loop.entries,
        MappingProxyType(slot_map), completed_prefix + (submission.participant_id,),
        MappingProxyType(commands), frozenset(slot_map[pid] for pid, command in commands.items()
            if command.command1 == BATTLE_COM_GUARD and loop.entries[slot_map[pid]].hp > 0),
        tuple(flags), loop)
