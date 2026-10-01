#!/usr/bin/env python3
"""Fail-closed bridge from enemy-AI wa slot selection to battle commands.

Executable subsets are added only when both the fixed handler-side command
encoding and the downstream reconstructed battle-round contract are closed.

Currently supported:
- PETSKILL_None
- PETSKILL_NormalAttack
- PETSKILL_NormalGuard
- PETSKILL_GuardBreak (explicit opt-in dispatcher branch)
- PETSKILL_ContinuationAttack (explicit opt-in dispatcher branch)
- PETSKILL_ChargeAttack (explicit opt-in dispatcher branch)
- PETSKILL_NoGuard (explicit opt-in dispatcher branch)
- PETSKILL_Mighty (explicit opt-in dispatcher branch)
- PETSKILL_PowerBalance (explicit opt-in dispatcher branch)
- PETSKILL_StatusChange (explicit opt-in dispatcher branch)
- PETSKILL_EarthRound (explicit opt-in dispatcher branch)
- PETSKILL_Abduct (explicit opt-in dispatcher branch)

All other stable-common and macro-gated callbacks remain fail-closed.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_GUARD,
    BATTLE_COM_NONE,
    BattleCommand,
    BattleCommandSetupEffects,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_petskill_core_model import (
    abduct_ai_threshold,
    abduct_command,
    charge_attack_command,
    continuation_attack_command,
    charge_execution_step,
    earth_round_command,
    guard_break_command,
    mighty_command,
    no_guard_command,
    parse_status_skill,
    power_balance_command,
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
GUARD_BREAK = "PETSKILL_GuardBreak"
CONTINUATION_ATTACK = "PETSKILL_ContinuationAttack"
CHARGE_ATTACK = "PETSKILL_ChargeAttack"
NO_GUARD = "PETSKILL_NoGuard"
MIGHTY = "PETSKILL_Mighty"
POWER_BALANCE = "PETSKILL_PowerBalance"
STATUS_CHANGE = "PETSKILL_StatusChange"
EARTH_ROUND = "PETSKILL_EarthRound"
ABDUCT = "PETSKILL_Abduct"

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
    abduct_ai_threshold: int | None = None


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
    allow_power_balance: bool = False,
    allow_mighty: bool = False,
    allow_guard_break: bool = False,
    allow_continuation_attack: bool = False,
    allow_charge_attack: bool = False,
    allow_no_guard: bool = False,
    allow_abduct: bool = False,
    allow_earth_round: bool = False,
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
    if entry.function_name == GUARD_BREAK and bool(allow_guard_break):
        return resolve_enemy_ai_guardbreak_petskill_command(
            spawned,
            skill_slot=skill_slot,
            target_slot=target_slot,
            petskill_runtime=petskill_runtime,
        )
    if (
        entry.function_name == CONTINUATION_ATTACK
        and bool(allow_continuation_attack)
    ):
        return resolve_enemy_ai_continuationattack_petskill_command(
            spawned,
            skill_slot=skill_slot,
            target_slot=target_slot,
            petskill_runtime=petskill_runtime,
        )
    if entry.function_name == CHARGE_ATTACK and bool(allow_charge_attack):
        return resolve_enemy_ai_chargeattack_petskill_command(
            spawned,
            skill_slot=skill_slot,
            target_slot=target_slot,
            petskill_runtime=petskill_runtime,
        )
    if entry.function_name == NO_GUARD and bool(allow_no_guard):
        return resolve_enemy_ai_noguard_petskill_command(
            spawned,
            skill_slot=skill_slot,
            target_slot=target_slot,
            petskill_runtime=petskill_runtime,
        )
    if entry.function_name == MIGHTY and bool(allow_mighty):
        return resolve_enemy_ai_mighty_petskill_command(
            spawned,
            skill_slot=skill_slot,
            target_slot=target_slot,
            petskill_runtime=petskill_runtime,
        )
    if entry.function_name == POWER_BALANCE and bool(allow_power_balance):
        return resolve_enemy_ai_powerbalance_petskill_command(
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
    if entry.function_name == EARTH_ROUND and bool(allow_earth_round):
        return resolve_enemy_ai_earthround_petskill_command(
            spawned,
            skill_slot=skill_slot,
            target_slot=target_slot,
            petskill_runtime=petskill_runtime,
        )
    if entry.function_name == ABDUCT and bool(allow_abduct):
        return resolve_enemy_ai_abduct_petskill_command(
            spawned,
            skill_slot=skill_slot,
            target_slot=target_slot,
            petskill_runtime=petskill_runtime,
        )
    raise ValueError(
        "enemy AI selected pet-skill callback outside admitted execution "
        f"subset: {entry.function_name}"
    )


def _recovered_earthround_attack_percents(
    petskill_runtime: Recovered25PetSkillRuntime,
) -> dict[int,int]:
    """Validate the one-row recovered25 EarthRound OPTION population."""

    rows=tuple(
        entry
        for entry in petskill_runtime.skills.values()
        if entry.function_name == EARTH_ROUND
    )
    if len(rows) != 1:
        raise ValueError(
            "recovered25 EarthRound runtime must contain exactly one callback ID"
        )
    entry=rows[0]
    option_text=entry.unambiguous_cp950_big5_option()
    attack=re.search(
        r"攻%\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))",
        option_text,
    )
    if attack is None:
        raise ValueError(
            "recovered25 EarthRound OPTION lacks proven numeric 攻% marker"
        )
    percent=float(attack.group(1))
    if percent != 90.0:
        raise ValueError(
            "recovered25 EarthRound attack percent drifted from 90"
        )
    return {int(entry.skill_id):int(percent)}


def resolve_enemy_ai_earthround_petskill_command(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiPetSkillCommand:
    """Resolve recovered PETSKILL_EarthRound into phase-1 command state."""

    skill_slot,target_slot,entry=_resolved_entry(
        spawned,
        skill_slot=skill_slot,
        target_slot=target_slot,
        petskill_runtime=petskill_runtime,
    )
    if entry.function_name != EARTH_ROUND:
        raise ValueError(
            "enemy AI selected pet-skill callback outside EarthRound "
            f"execution subset: {entry.function_name}"
        )
    percents=_recovered_earthround_attack_percents(petskill_runtime)
    attack_percent=int(percents[int(entry.skill_id)])
    option_text=entry.unambiguous_cp950_big5_option()
    payload=earth_round_command(
        target_slot,
        option_text,
        prior_com3=0,
    )
    if int(payload.get("com3",-1)) != attack_percent:
        raise ValueError("EarthRound reconstructed COM3 percent drift")
    submission=bridge_stable_pet_skill_command(payload)
    return EnemyAiPetSkillCommand(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=int(entry.skill_id),
        callback=entry.function_name,
        command=submission.battle_command,
        setup_effects=submission.setup_effects,
    )


def _recovered_abduct_thresholds(
    petskill_runtime: Recovered25PetSkillRuntime,
) -> dict[int,int]:
    """Validate the hard-probed recovered25 Abduct OPTION population.

    The pinned bundle has exactly two enemy-referenced Abduct IDs.  Both OPTION
    payloads are ASCII; exactly one begins with an integer; source atoi results
    are exactly {0,80}.  Admission is denied if a different runtime drifts from
    that recovered population.
    """

    rows=tuple(
        entry
        for entry in petskill_runtime.skills.values()
        if entry.function_name == ABDUCT
    )
    if len(rows) != 2:
        raise ValueError(
            "recovered25 Abduct runtime must contain exactly two callback IDs"
        )
    thresholds={}
    leading_count=0
    positive_count=0
    for entry in rows:
        if not entry.option_bytes.isascii():
            raise ValueError(
                "recovered25 Abduct OPTION must stay in proven ASCII subset"
            )
        option_text=entry.option_bytes.decode("ascii")
        leading=re.match(r"\s*([+-]?\d+)",option_text)
        if leading is not None:
            leading_count += 1
        value=int(abduct_ai_threshold(option_text))
        if value > 0:
            positive_count += 1
        thresholds[int(entry.skill_id)]=value
    if sorted(thresholds.values()) != [0,80]:
        raise ValueError(
            "recovered25 Abduct atoi threshold set drifted from {0,80}"
        )
    if leading_count != 1 or positive_count != 1:
        raise ValueError(
            "recovered25 Abduct leading/positive OPTION population drift"
        )
    return thresholds


def resolve_enemy_ai_abduct_petskill_command(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiPetSkillCommand:
    """Resolve recovered PETSKILL_Abduct into fixed S_ABDUCT command state."""

    skill_slot,target_slot,entry=_resolved_entry(
        spawned,
        skill_slot=skill_slot,
        target_slot=target_slot,
        petskill_runtime=petskill_runtime,
    )
    if entry.function_name != ABDUCT:
        raise ValueError(
            "enemy AI selected pet-skill callback outside Abduct "
            f"execution subset: {entry.function_name}"
        )
    thresholds=_recovered_abduct_thresholds(petskill_runtime)
    threshold=int(thresholds[int(entry.skill_id)])

    # _PETSKILL_OPTIMUM loads rows directly at their skill-ID table index, so
    # PETSKILL_getPetskillArray(id) resolves the fixed handler LOW(COM3) array
    # back to this recovered skill ID.
    payload=abduct_command(
        target_slot,
        skill_array=int(entry.skill_id),
        prior_high=0,
    )
    if int(payload.get("low",-1)) != int(entry.skill_id):
        raise ValueError("Abduct reconstructed skill-array identity drift")
    if int(payload.get("high",-1)) != 0:
        raise ValueError("Abduct inactive COM3 high-half drift")
    submission=bridge_stable_pet_skill_command(payload)
    return EnemyAiPetSkillCommand(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=int(entry.skill_id),
        callback=entry.function_name,
        command=submission.battle_command,
        setup_effects=submission.setup_effects,
        abduct_ai_threshold=threshold,
    )


def resolve_enemy_ai_noguard_petskill_command(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiPetSkillCommand:
    """Resolve recovered PETSKILL_NoGuard into same-round cross-action state."""

    skill_slot, target_slot, entry = _resolved_entry(
        spawned,
        skill_slot=skill_slot,
        target_slot=target_slot,
        petskill_runtime=petskill_runtime,
    )
    if entry.function_name != NO_GUARD:
        raise ValueError(
            "enemy AI selected pet-skill callback outside NoGuard "
            f"execution subset: {entry.function_name}"
        )

    option_text=entry.unambiguous_cp950_big5_option()
    dodge=re.search(r"避%\s*([+-]?\d+)",option_text)
    counter=re.search(r"擊%\s*([+-]?\d+)",option_text)
    critical=re.search(r"心%\s*([+-]?\d+)",option_text)
    if (
        dodge is None
        or counter is None
        or critical is None
        or "击%" in option_text
    ):
        raise ValueError(
            "recovered NoGuard OPTION is outside closed traditional "
            "dodge/counter/critical numeric grammar"
        )
    dodge_value=int(dodge.group(1))
    counter_value=int(counter.group(1))
    critical_value=int(critical.group(1))
    if not (
        30 <= dodge_value <= 50
        and 50 <= counter_value <= 70
        and 20 <= critical_value <= 40
    ):
        raise ValueError(
            "recovered NoGuard OPTION values are outside proven ranges"
        )

    payload=no_guard_command(
        target_slot,
        option_text,
        counter_marker="擊%",
        prior_high=0,
    )
    if int(payload.get("high",0)) != dodge_value:
        raise ValueError("NoGuard parsed dodge modifier drift")
    expected_low=(counter_value << 8) + critical_value
    if int(payload.get("low",-1)) != expected_low:
        raise ValueError("NoGuard packed counter/critical drift")

    submission=bridge_stable_pet_skill_command(payload)
    return EnemyAiPetSkillCommand(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=int(entry.skill_id),
        callback=entry.function_name,
        command=submission.battle_command,
        setup_effects=submission.setup_effects,
    )


def resolve_enemy_ai_continuationattack_petskill_command(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiPetSkillCommand:
    """Resolve recovered PETSKILL_ContinuationAttack into S_RENZOKU."""

    skill_slot, target_slot, entry = _resolved_entry(
        spawned,
        skill_slot=skill_slot,
        target_slot=target_slot,
        petskill_runtime=petskill_runtime,
    )
    if entry.function_name != CONTINUATION_ATTACK:
        raise ValueError(
            "enemy AI selected pet-skill callback outside ContinuationAttack "
            f"execution subset: {entry.function_name}"
        )
    if not entry.option_bytes.isascii():
        raise ValueError(
            "recovered ContinuationAttack OPTION is outside proven ASCII subset"
        )
    option_text=entry.option_bytes.decode("ascii")
    leading=re.match(r"\s*([+-]?\d+)",option_text)
    if leading is None:
        raise ValueError(
            "recovered ContinuationAttack OPTION lacks leading attack count"
        )
    count=int(leading.group(1))
    if not 2 <= count <= 5:
        raise ValueError(
            "recovered ContinuationAttack count is outside proven 2..5 range"
        )

    # The fixed handler writes LOW(COM3) and preserves HIGH.  S_RENZOKU
    # execution consumes only LOW; recovered runtime therefore starts the
    # inactive high half at zero rather than inventing prior COM3 residue.
    payload=continuation_attack_command(
        target_slot,
        option_text,
        prior_high=0,
    )
    if int(payload.get("low",-1)) != count:
        raise ValueError("ContinuationAttack parsed hit-count drift")
    if int(payload.get("high",-1)) != 0:
        raise ValueError("ContinuationAttack inactive COM3 high-half drift")

    submission=bridge_stable_pet_skill_command(payload)
    return EnemyAiPetSkillCommand(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=int(entry.skill_id),
        callback=entry.function_name,
        command=submission.battle_command,
        setup_effects=submission.setup_effects,
    )


def resolve_enemy_ai_chargeattack_petskill_command(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiPetSkillCommand:
    """Resolve recovered PETSKILL_ChargeAttack into persistent charge state."""

    skill_slot, target_slot, entry = _resolved_entry(
        spawned,
        skill_slot=skill_slot,
        target_slot=target_slot,
        petskill_runtime=petskill_runtime,
    )
    if entry.function_name != CHARGE_ATTACK:
        raise ValueError(
            "enemy AI selected pet-skill callback outside ChargeAttack "
            f"execution subset: {entry.function_name}"
        )

    option_text = entry.unambiguous_cp950_big5_option()
    leading = re.match(r"\s*([+-]?\d+)", option_text)
    attack = re.search(r"攻%\s*([+-]?\d+)", option_text)
    if leading is None or attack is None:
        raise ValueError(
            "recovered ChargeAttack OPTION is outside closed wait/attack "
            "numeric grammar"
        )
    wait_count = int(leading.group(1))
    if not 1 <= wait_count <= 10:
        raise ValueError(
            "recovered ChargeAttack wait count is outside closed 1..10 range"
        )

    birth = spawned.birth
    projection_fn = getattr(birth, "combat_projection", None)
    if not callable(projection_fn):
        raise ValueError(
            "ChargeAttack execution requires recovered enemy birth projection"
        )
    projection = projection_fn()
    if "attack" not in projection:
        raise ValueError("enemy birth projection lacks fixed attack value")

    payload = dict(charge_attack_command(target_slot, option_text))
    if int(payload.get("low", -1)) != wait_count:
        raise ValueError("ChargeAttack parsed wait count drift")
    if int(payload.get("high", 0)) != int(attack.group(1)):
        raise ValueError("ChargeAttack parsed attack percent drift")

    ready = charge_execution_step(
        remaining=0,
        attack_percent=int(payload["high"]),
        fixed_attack=int(projection["attack"]),
        attack_modifier=0,
    )
    if not bool(ready.get("ready")) or ready.get("attack_power") is None:
        raise ValueError("ChargeAttack ready-power reconstruction failed")
    payload["charge_ready_attack_power"] = int(ready["attack_power"])

    submission = bridge_stable_pet_skill_command(payload)
    return EnemyAiPetSkillCommand(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=int(entry.skill_id),
        callback=entry.function_name,
        command=submission.battle_command,
        setup_effects=submission.setup_effects,
    )


def resolve_enemy_ai_guardbreak_petskill_command(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiPetSkillCommand:
    """Resolve recovered PETSKILL_GuardBreak into its dedicated physical seam."""

    skill_slot, target_slot, entry = _resolved_entry(
        spawned,
        skill_slot=skill_slot,
        target_slot=target_slot,
        petskill_runtime=petskill_runtime,
    )
    if entry.function_name != GUARD_BREAK:
        raise ValueError(
            "enemy AI selected pet-skill callback outside GuardBreak "
            f"execution subset: {entry.function_name}"
        )

    if not entry.option_bytes.isascii():
        raise ValueError(
            "recovered GuardBreak OPTION is outside proven ASCII-only subset"
        )
    option_text=entry.option_bytes.decode("ascii")
    if "攻%" in option_text:
        raise ValueError(
            "ASCII-only GuardBreak subset unexpectedly contains attack marker"
        )

    projection_fn=getattr(spawned.birth,"combat_projection",None)
    if not callable(projection_fn):
        raise ValueError(
            "GuardBreak execution requires recovered enemy birth projection"
        )
    projection=projection_fn()
    if "attack" not in projection:
        raise ValueError("enemy birth projection lacks fixed attack value")

    payload=guard_break_command(
        target_slot,
        option_text,
        fixed_attack=int(projection["attack"]),
    )
    submission=bridge_stable_pet_skill_command(payload)
    return EnemyAiPetSkillCommand(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=int(entry.skill_id),
        callback=entry.function_name,
        command=submission.battle_command,
        setup_effects=submission.setup_effects,
    )


def resolve_enemy_ai_mighty_petskill_command(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiPetSkillCommand:
    """Resolve recovered PETSKILL_Mighty into the ordinary physical seam."""

    skill_slot, target_slot, entry = _resolved_entry(
        spawned,
        skill_slot=skill_slot,
        target_slot=target_slot,
        petskill_runtime=petskill_runtime,
    )
    if entry.function_name != MIGHTY:
        raise ValueError(
            "enemy AI selected pet-skill callback outside Mighty "
            f"execution subset: {entry.function_name}"
        )

    option_text = entry.unambiguous_cp950_big5_option()
    if (
        "倍" not in option_text
        or "避" not in option_text
        or re.search(
            r"倍\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+)",
            option_text,
        ) is None
        or re.search(r"避\s*[+-]?\d+", option_text) is None
    ):
        raise ValueError(
            "recovered Mighty OPTION is outside closed multiplier/dodge "
            "numeric grammar"
        )

    payload = mighty_command(target_slot, option_text)
    submission = bridge_stable_pet_skill_command(payload)
    return EnemyAiPetSkillCommand(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=int(entry.skill_id),
        callback=entry.function_name,
        command=submission.battle_command,
        setup_effects=submission.setup_effects,
    )


def resolve_enemy_ai_powerbalance_petskill_command(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiPetSkillCommand:
    """Resolve recovered PETSKILL_PowerBalance into the ordinary attack seam."""

    skill_slot, target_slot, entry = _resolved_entry(
        spawned,
        skill_slot=skill_slot,
        target_slot=target_slot,
        petskill_runtime=petskill_runtime,
    )
    if entry.function_name != POWER_BALANCE:
        raise ValueError(
            "enemy AI selected pet-skill callback outside PowerBalance "
            f"execution subset: {entry.function_name}"
        )

    option_text = entry.unambiguous_cp950_big5_option()
    if (
        "攻%" not in option_text
        or "防%" not in option_text
        or "敏%" in option_text
    ):
        raise ValueError(
            "recovered PowerBalance OPTION is outside closed attack/defense "
            "marker grammar"
        )

    birth = spawned.birth
    projection_fn = getattr(birth, "combat_projection", None)
    if not callable(projection_fn):
        raise ValueError(
            "PowerBalance execution requires recovered enemy birth projection"
        )
    projection = projection_fn()
    if "attack" not in projection or "defense" not in projection:
        raise ValueError(
            "enemy birth projection lacks fixed attack/defense values"
        )

    payload = power_balance_command(
        target_slot,
        option_text,
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
