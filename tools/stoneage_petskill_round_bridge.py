#!/usr/bin/env python3
"""Bridge stable pet-skill command payloads into the reconstructed round core.

The pet-skill model mirrors command-handler parsing and immediate work-state
mutations. This bridge converts those already-recovered outputs into the
numeric COM1/COM2/COM3 boundary plus explicit setup effects consumed by the
round resolver. It does not parse PETSKILL_OPTION text itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any

from tools.stoneage_battle_round_model import (
    BATTLE_COM_GUARD,
    BATTLE_COM_S_GUARDIAN_ATTACK,
    BATTLE_COM_S_STATUSCHANGE,
    BattleCommand,
    BattleCommandSetupEffects,
    pack_battle_command3,
)


@dataclass(frozen=True)
class StablePetSkillRoundSubmission:
    source_command: str
    battle_command: BattleCommand
    setup_effects: BattleCommandSetupEffects


def bridge_stable_pet_skill_command(
    payload: Mapping[str, Any],
    *,
    actor_slot: int | None = None,
) -> StablePetSkillRoundSubmission:
    """Convert supported stable pet-skill command-handler output.

    Supported common handlers are the two branches currently executed by the
    reconstructed ordinary physical round:
    - PETSKILL_Guardian -> S_GUARDIAN_ATTACK or ordinary GUARD + registration
    - PETSKILL_StatusChange -> S_STATUSCHANGE with LOW=status/HIGH=turn
    """
    if not isinstance(payload,Mapping):
        raise TypeError("pet-skill command payload must be a mapping")
    if not bool(payload.get("accepted",False)):
        raise ValueError("rejected pet-skill command cannot enter a battle round")

    source_command=str(payload.get("command",""))
    target=int(payload.get("target",-1))

    if source_command=="S_GUARDIAN_ATTACK":
        battle_command=BattleCommand(
            BATTLE_COM_S_GUARDIAN_ATTACK,
            command2=target,
        )
    elif source_command=="GUARD" and bool(payload.get("guardian_flag",False)):
        # The pinned common PETSKILL_Guardian defensive branch writes ordinary
        # BATTLE_COM_GUARD, leaving the guardian registration outside COM1.
        battle_command=BattleCommand(
            BATTLE_COM_GUARD,
            command2=target,
        )
    elif source_command=="S_STATUSCHANGE":
        if "low" not in payload or "high" not in payload:
            raise ValueError("S_STATUSCHANGE requires recovered low/high COM3")
        battle_command=BattleCommand(
            BATTLE_COM_S_STATUSCHANGE,
            command2=target,
            command3=pack_battle_command3(
                low=int(payload["low"]),
                high=int(payload["high"]),
            ),
        )
    else:
        raise ValueError(
            f"pet-skill command is outside recovered round bridge: "
            f"{source_command!r}"
        )

    guardian_flag=bool(payload.get("guardian_flag",False))
    guardian_for_slot=payload.get("guardian_for_slot")
    if guardian_for_slot is not None:
        guardian_for_slot=int(guardian_for_slot)

    if guardian_flag:
        if actor_slot is None:
            raise ValueError("Guardian bridge requires explicit actor_slot")
        actor_slot=int(actor_slot)
        if not 0 <= actor_slot < 20:
            raise ValueError("Guardian actor_slot must be in 0..19")
        payload_guardian_slot=payload.get("guardian_slot")
        if (
            payload_guardian_slot is not None
            and int(payload_guardian_slot) != actor_slot
        ):
            raise ValueError(
                "Guardian payload slot does not match authoritative actor_slot"
            )

    effects=BattleCommandSetupEffects(
        attack_power=(
            None
            if payload.get("attack_power") is None
            else int(payload["attack_power"])
        ),
        defense_power=(
            None
            if payload.get("defense_power") is None
            else int(payload["defense_power"])
        ),
        guardian_flag=guardian_flag,
        guardian_for_slot=guardian_for_slot,
        guardian_barrier=int(payload.get("guardian_barrier",0)),
    )
    return StablePetSkillRoundSubmission(
        source_command=source_command,
        battle_command=battle_command,
        setup_effects=effects,
    )
