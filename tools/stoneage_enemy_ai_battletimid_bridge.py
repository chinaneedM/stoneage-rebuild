#!/usr/bin/env python3
"""Recovered25 enemy-AI PETSKILL_BattleTimid semantic boundary.

Recovered skill ID 606 is kept distinct from the descendant callback's
LOW(COM3) pet-skill array identity. No historical numeric COM1 or array index
is assigned by this bridge.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_battletimid_model import (
    CALLBACK_NAME,
    COMMAND_NAME,
    BattleTimidSetup,
    resolve_battletimid_setup,
    validate_common_runtime_domain,
    resolve_battletimid_post_damage,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime

RECOVERED25_BATTLETIMID_IDS=(606,)


@dataclass(frozen=True)
class EnemyAiBattleTimidSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    setup: BattleTimidSetup
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self) -> None:
        participant_id=str(self.participant_id)
        skill_slot=int(self.skill_slot)
        skill_id=int(self.skill_id)
        target=int(self.source_target_slot)
        if not participant_id:
            raise ValueError("BattleTimid participant id must be non-empty")
        if not 0 <= skill_slot < 7:
            raise ValueError("BattleTimid skill slot must be in 0..6")
        if skill_id not in RECOVERED25_BATTLETIMID_IDS:
            raise ValueError("BattleTimid skill-id outside recovered25 set")
        if self.callback != CALLBACK_NAME:
            raise ValueError("BattleTimid callback drift")
        if not 0 <= target < 10:
            raise ValueError(
                "BattleTimid R1 target must be opposite-side player slot 0..9"
            )
        validate_common_runtime_domain(opposite_side=True)
        if not isinstance(self.setup,BattleTimidSetup):
            raise TypeError("BattleTimid setup has wrong type")
        if not self.setup.accepted or self.setup.rejected_player:
            raise ValueError("BattleTimid enemy submission must have accepted setup")
        if int(self.setup.target_slot) != target:
            raise ValueError("BattleTimid setup/source target drift")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("BattleTimid semantic command-name drift")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"skill_slot",skill_slot)
        object.__setattr__(self,"skill_id",skill_id)
        object.__setattr__(self,"source_target_slot",target)

    def post_damage(self, *, draw: int, damage: int, target_is_pet: bool):
        return resolve_battletimid_post_damage(
            draw=int(draw),
            damage=int(damage),
            target_is_pet=bool(target_is_pet),
        )


def resolve_enemy_ai_battletimid_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
    fixed_strength: int,
    fixed_toughness: int,
    fixed_dex: int,
) -> EnemyAiBattleTimidSubmission:
    skill_slot=int(skill_slot)
    target_slot=int(target_slot)
    if not 0 <= skill_slot < 7:
        raise ValueError("enemy AI BattleTimid skill slot must be in 0..6")
    if not 0 <= target_slot < 10:
        raise ValueError(
            "enemy AI BattleTimid target must be opposite-side player slot 0..9"
        )

    rows=tuple(sorted(
        (
            entry for entry in petskill_runtime.skills.values()
            if entry.function_name==CALLBACK_NAME
        ),
        key=lambda entry:int(entry.skill_id),
    ))
    if tuple(int(entry.skill_id) for entry in rows) != RECOVERED25_BATTLETIMID_IDS:
        raise ValueError(
            "recovered25 BattleTimid callback population must be exactly ID 606"
        )

    slots=tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots)!=7:
        raise ValueError(
            "enemy template lacks authoritative seven-slot pet-skill identity"
        )
    skill_id=int(slots[skill_slot])
    if skill_id != 606:
        raise ValueError(
            "enemy AI selected skill slot outside recovered25 BattleTimid ID"
        )

    entry=petskill_runtime.skills[skill_id]
    if (
        int(entry.field)!=1
        or int(entry.target)!=6
        or int(entry.cost)!=2
        or int(entry.illegal)!=3000
        or bytes(entry.option_bytes)!=b""
    ):
        raise ValueError("recovered25 BattleTimid row metadata/OPTION drift")

    # The source callback writes an array identity into LOW(COM3), but no
    # recovered25 proof maps external ID 606 to that internal array index.
    # Zero is therefore an explicit modern carrier placeholder, never a
    # historical array-index assertion.
    setup=resolve_battletimid_setup(
        actor_is_player=False,
        target_slot=target_slot,
        skill_array=0,
        packed_com3_before=0,
        fixed_str=int(fixed_strength),
        fixed_tough=int(fixed_toughness),
        fixed_dex=int(fixed_dex),
    )
    return EnemyAiBattleTimidSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=skill_id,
        callback=entry.function_name,
        source_target_slot=target_slot,
        setup=setup,
    )
