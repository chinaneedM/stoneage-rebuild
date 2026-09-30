#!/usr/bin/env python3
"""Fail-closed bridge from enemy-AI wa slot selection to battle commands.

Only the three stable descendant pet-skill handlers whose command encoding is
fully state-free are admitted here:
- PETSKILL_None         -> BATTLE_COM_NONE(target)
- PETSKILL_NormalAttack -> BATTLE_COM_ATTACK(target)
- PETSKILL_NormalGuard  -> BATTLE_COM_GUARD(target)

Every other callback remains outside this bridge even when it belongs to the
15-handler stable common pet-skill family, because those handlers require
additional OPTION parsing, COM3 state, setup effects, or downstream execution
contracts.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_GUARD,
    BATTLE_COM_NONE,
    BattleCommand,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)


NONE = "PETSKILL_None"
NORMAL_ATTACK = "PETSKILL_NormalAttack"
NORMAL_GUARD = "PETSKILL_NormalGuard"
BASIC_AI_CALLBACKS = frozenset({NONE, NORMAL_ATTACK, NORMAL_GUARD})


@dataclass(frozen=True)
class EnemyAiPetSkillCommand:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    command: BattleCommand


def resolve_enemy_ai_basic_petskill_command(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiPetSkillCommand:
    """Resolve one source-shaped PETSKILL_Use slot for the basic AI subset."""

    skill_slot = int(skill_slot)
    target_slot = int(target_slot)
    if not 0 <= skill_slot < 7:
        raise ValueError("enemy AI pet-skill slot must be in 0..6")
    if not 0 <= target_slot < 10:
        raise ValueError("enemy AI pet-skill target must be in player-side 0..9")

    slots = tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots) != 7:
        raise ValueError(
            "enemy template lacks authoritative seven-slot pet-skill identity"
        )
    skill_id = int(slots[skill_slot])
    if skill_id <= 0:
        raise ValueError(
            f"enemy AI selected empty pet-skill slot {skill_slot}"
        )
    if skill_id not in petskill_runtime.skills:
        raise ValueError(
            f"enemy AI selected unresolved pet-skill ID {skill_id}"
        )

    entry: Recovered25PetSkillEntry = petskill_runtime.skills[skill_id]
    if entry.function_name == NONE:
        command = BattleCommand(
            BATTLE_COM_NONE,
            command2=target_slot,
        )
    elif entry.function_name == NORMAL_ATTACK:
        command = BattleCommand(
            BATTLE_COM_ATTACK,
            command2=target_slot,
        )
    elif entry.function_name == NORMAL_GUARD:
        # The fixed handler writes COM2 as well even though ordinary guard does
        # not consume it as a damage target.
        command = BattleCommand(
            BATTLE_COM_GUARD,
            command2=target_slot,
        )
    else:
        raise ValueError(
            "enemy AI selected pet-skill callback outside basic execution "
            f"subset: {entry.function_name}"
        )

    return EnemyAiPetSkillCommand(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=skill_id,
        callback=entry.function_name,
        command=command,
    )
