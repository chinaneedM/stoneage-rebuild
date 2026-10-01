#!/usr/bin/env python3
"""Recovered25 enemy-AI AttackMagic command-submission boundary.

This bridge intentionally returns the existing AttackMagicCommand envelope,
not BattleCommand. Command code 2002 is still outside the ordinary round
command enum/resolver until the round-time magic-state adapter is closed.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_attack_magic_model import (
    BATTLE_COM_S_ATTACK_MAGIC,
    PROFILE_RECOVERED25,
    AttackMagicCommand,
    MagicDirectUseRequest,
    build_magic_direct_use_request,
    command3_high,
    command3_low,
    encode_attack_magic_command,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_attack_magic_runtime import (
    NONPLAYER_ITEM_ROLE,
    Recovered25AttackMagicRuntime,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillRuntime,
)


ATTACK_MAGIC_CALLBACK="PETSKILL_AttackMagic"


@dataclass(frozen=True)
class EnemyAiAttackMagicSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    command: AttackMagicCommand
    direct_use_request: MagicDirectUseRequest
    nonplayer_item_runtime_role: str = NONPLAYER_ITEM_ROLE

    def __post_init__(self) -> None:
        if int(self.command.command1) != BATTLE_COM_S_ATTACK_MAGIC:
            raise ValueError("enemy AttackMagic submission command drift")
        if self.callback != ATTACK_MAGIC_CALLBACK:
            raise ValueError("enemy AttackMagic submission callback drift")
        if self.nonplayer_item_runtime_role != NONPLAYER_ITEM_ROLE:
            raise ValueError("enemy AttackMagic item runtime-role drift")


def resolve_enemy_ai_attack_magic_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
    attack_magic_runtime: Recovered25AttackMagicRuntime,
) -> EnemyAiAttackMagicSubmission:
    """Resolve one enemy wa[] AttackMagic selection through COM1/2/3."""
    skill_slot=int(skill_slot)
    target_slot=int(target_slot)
    if not 0 <= skill_slot < 7:
        raise ValueError("enemy AI AttackMagic skill slot must be in 0..6")
    if not 0 <= target_slot < 10:
        raise ValueError("enemy AI AttackMagic target must be player-side 0..9")

    slots=tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots) != 7:
        raise ValueError(
            "enemy template lacks authoritative seven-slot pet-skill identity"
        )
    skill_id=int(slots[skill_slot])
    if skill_id <= 0:
        raise ValueError(
            f"enemy AI selected empty AttackMagic pet-skill slot {skill_slot}"
        )
    try:
        petskill=petskill_runtime.skills[skill_id]
    except KeyError as exc:
        raise ValueError(
            f"enemy AI selected unresolved pet-skill ID {skill_id}"
        ) from exc
    if petskill.function_name != ATTACK_MAGIC_CALLBACK:
        raise ValueError(
            "enemy AI selected pet-skill callback outside AttackMagic "
            f"submission boundary: {petskill.function_name}"
        )
    try:
        indexed=attack_magic_runtime.entries[skill_id]
    except KeyError as exc:
        raise ValueError(
            f"AttackMagic runtime lacks selected skill ID {skill_id}"
        ) from exc

    command=encode_attack_magic_command(
        target_slot,
        petskill.ascii_option(),
        profile=PROFILE_RECOVERED25,
    )
    if int(command.magic_id) != int(indexed.magic_id):
        raise ValueError("AttackMagic command/runtime magic-id drift")
    if int(command.item_index) != int(indexed.item_config_id):
        raise ValueError("AttackMagic command/runtime item-config drift")
    if command3_low(command.command3) != int(indexed.magic_id):
        raise ValueError("AttackMagic COM3 low-half drift")
    if command3_high(command.command3) != int(indexed.item_config_id):
        raise ValueError("AttackMagic COM3 high-half provenance drift")

    request=build_magic_direct_use_request(command)
    if int(request.magic_id) != int(indexed.magic_id):
        raise ValueError("AttackMagic DirectUse magic-id drift")
    if int(request.source_target) != target_slot:
        raise ValueError("AttackMagic DirectUse source-target drift")

    return EnemyAiAttackMagicSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=skill_id,
        callback=petskill.function_name,
        command=command,
        direct_use_request=request,
    )
