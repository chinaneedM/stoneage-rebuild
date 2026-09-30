#!/usr/bin/env python3
"""Fail-closed bridge from enemy-AI wa slot selection to battle commands.

Executable subsets are added only when both the fixed handler-side command
encoding and the downstream reconstructed battle-round contract are closed.

Currently supported:
- PETSKILL_None
- PETSKILL_NormalAttack
- PETSKILL_NormalGuard
- PETSKILL_StatusChange (explicit opt-in dispatcher branch)

All other stable-common and macro-gated callbacks remain fail-closed.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_GUARD,
    BATTLE_COM_NONE,
    BattleCommand,
    BattleCommandSetupEffects,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_petskill_core_model import (
    parse_status_skill,
    status_change_command,
)
from tools.stoneage_petskill_round_bridge import (
    bridge_stable_pet_skill_command,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)


NONE = "PETSKILL_None"
NORMAL_ATTACK = "PETSKILL_NormalAttack"
NORMAL_GUARD = "PETSKILL_NormalGuard"
STATUS_CHANGE = "PETSKILL_StatusChange"

BASIC_AI_CALLBACKS = frozenset({NONE, NORMAL_ATTACK, NORMAL_GUARD})
STATUS_TOKENS_TRADITIONAL = ("全", "毒", "麻", "眠", "石", "醉", "亂")
STATUS_TOKENS_SIMPLIFIED = ("全", "毒", "麻", "眠", "石", "醉", "乱")


@dataclass(frozen=True)
class EnemyAiPetSkillCommand:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    command: BattleCommand
    setup_effects: BattleCommandSetupEffects = BattleCommandSetupEffects()


def _resolved_entry(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> tuple[int, int, Recovered25PetSkillEntry]:
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
    return skill_slot, target_slot, petskill_runtime.skills[skill_id]


def resolve_enemy_ai_basic_petskill_command(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiPetSkillCommand:
    """Resolve one source-shaped PETSKILL_Use slot for the basic AI subset."""

    skill_slot, target_slot, entry = _resolved_entry(
        spawned,
        skill_slot=skill_slot,
        target_slot=target_slot,
        petskill_runtime=petskill_runtime,
    )
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
        skill_id=int(entry.skill_id),
        callback=entry.function_name,
        command=command,
    )


def resolve_enemy_ai_supported_petskill_command(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
    allow_status_change: bool = False,
) -> EnemyAiPetSkillCommand:
    """Dispatch only callbacks whose full execution boundary is admitted."""

    _, _, entry = _resolved_entry(
        spawned,
        skill_slot=skill_slot,
        target_slot=target_slot,
        petskill_runtime=petskill_runtime,
    )
    if entry.function_name in BASIC_AI_CALLBACKS:
        return resolve_enemy_ai_basic_petskill_command(
            spawned,
            skill_slot=skill_slot,
            target_slot=target_slot,
            petskill_runtime=petskill_runtime,
        )
    if entry.function_name == STATUS_CHANGE and bool(allow_status_change):
        return resolve_enemy_ai_statuschange_petskill_command(
            spawned,
            skill_slot=skill_slot,
            target_slot=target_slot,
            petskill_runtime=petskill_runtime,
        )
    raise ValueError(
        "enemy AI selected pet-skill callback outside admitted execution "
        f"subset: {entry.function_name}"
    )


def _status_tokens_for_option(option_text: str) -> tuple[str, ...]:
    for tokens in (STATUS_TOKENS_TRADITIONAL, STATUS_TOKENS_SIMPLIFIED):
        parsed = parse_status_skill(option_text, tokens)
        if bool(parsed["matched"]):
            return tokens
    raise ValueError(
        "recovered StatusChange OPTION does not match fixed common status tokens"
    )


def resolve_enemy_ai_statuschange_petskill_command(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiPetSkillCommand:
    """Resolve recovered PETSKILL_StatusChange into the closed round seam.

    The OPTION text is admitted only under strict CP950/Big5 agreement.
    FIXSTR/FIXTOUGH are reconstructed from the preserved enemy birth state,
    matching CHAR_initcharWorkInt's pre-equipment fixed-stat formulas.
    """

    skill_slot, target_slot, entry = _resolved_entry(
        spawned,
        skill_slot=skill_slot,
        target_slot=target_slot,
        petskill_runtime=petskill_runtime,
    )
    if entry.function_name != STATUS_CHANGE:
        raise ValueError(
            "enemy AI selected pet-skill callback outside StatusChange "
            f"execution subset: {entry.function_name}"
        )

    option_text = entry.unambiguous_cp950_big5_option()
    status_tokens = _status_tokens_for_option(option_text)

    birth = spawned.birth
    projection_fn = getattr(birth, "combat_projection", None)
    if not callable(projection_fn):
        raise ValueError(
            "StatusChange execution requires recovered enemy birth projection"
        )
    projection = projection_fn()
    if "attack" not in projection or "defense" not in projection:
        raise ValueError(
            "enemy birth projection lacks fixed attack/defense values"
        )

    payload = status_change_command(
        target_slot,
        option_text,
        status_tokens,
        fixed_attack=int(projection["attack"]),
        fixed_defense=int(projection["defense"]),
    )
    submission = bridge_stable_pet_skill_command(payload)
    return EnemyAiPetSkillCommand(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=int(entry.skill_id),
        callback=entry.function_name,
        command=submission.battle_command,
        setup_effects=submission.setup_effects,
    )
