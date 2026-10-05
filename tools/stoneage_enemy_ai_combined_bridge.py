#!/usr/bin/env python3
"""Recovered25 enemy-AI PETSKILL_Combined submission boundary.

This module closes only the data/selection handoff:
enemy seven-slot identity -> exact recovered Combined row -> one explicit
reduced rand index -> selected recovered magic crosslink.

It deliberately does not execute the selected magic and does not assign an
original numeric COM1 identity.  DirectUse itemnum is retained as the fixed
source value zero.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re

from tools.stoneage_combined_model import (
    CALLBACK_NAME,
    COMMAND_NAME,
    CombinedSelection,
    resolve_combined_selection,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_combined_magic_probe import (
    EXPECTED_EXACT_MAGIC_ROWS,
)
from tools.stoneage_recovered25_combined_probe import EXPECTED_EXACT_ROWS
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillRuntime,
)
from tools.stoneage_combined_direct_magic_model import (
    resolve_combined_direct_magic_route,
)

RECOVERED25_COMBINED_CALLBACK_IDS=(627,629,630,632,637,646,648)
RECOVERED25_COMBINED_EXECUTABLE_IDS=(627,632,637)


@dataclass(frozen=True)
class CombinedMagicCrosslink:
    magic_id:int
    function_name:str
    field:int
    target:int
    target_deadflg:int
    idx:int | None
    direct_item_index:int=0

    def __post_init__(self)->None:
        if int(self.magic_id) <= 0:
            raise ValueError("Combined selected magic ID must be positive")
        if not str(self.function_name).startswith("MAGIC_"):
            raise ValueError("Combined selected magic function drift")
        if int(self.direct_item_index) != 0:
            raise ValueError("Combined fixed DirectUse itemnum must stay zero")


@dataclass(frozen=True)
class EnemyAiCombinedSubmission:
    participant_id:str
    skill_slot:int
    skill_id:int
    callback:str
    source_target_slot:int
    selection:CombinedSelection
    magic:CombinedMagicCrosslink
    semantic_command_name:str=COMMAND_NAME

    def __post_init__(self)->None:
        participant_id=str(self.participant_id)
        skill_slot=int(self.skill_slot)
        skill_id=int(self.skill_id)
        target=int(self.source_target_slot)
        if not participant_id:
            raise ValueError("Combined participant id must be non-empty")
        if not 0 <= skill_slot < 7:
            raise ValueError("Combined skill slot must be in 0..6")
        if skill_id not in RECOVERED25_COMBINED_EXECUTABLE_IDS:
            raise ValueError("Combined skill ID is not positively referenced")
        if self.callback != CALLBACK_NAME:
            raise ValueError("Combined callback drift")
        if not 0 <= target < 10:
            raise ValueError(
                "Combined R1 source target must be player-side slot 0..9"
            )
        if not isinstance(self.selection,CombinedSelection):
            raise TypeError("Combined selection has wrong type")
        if int(self.selection.target_slot) != target:
            raise ValueError("Combined selection/source target drift")
        if int(self.selection.rng_draws_consumed) != 1:
            raise ValueError("Combined selection must consume exactly one draw")
        if not isinstance(self.magic,CombinedMagicCrosslink):
            raise TypeError("Combined magic crosslink has wrong type")
        if int(self.magic.magic_id) != int(self.selection.selected_magic_id):
            raise ValueError("Combined selected magic/crosslink drift")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("Combined semantic command-name drift")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"skill_slot",skill_slot)
        object.__setattr__(self,"skill_id",skill_id)
        object.__setattr__(self,"source_target_slot",target)

    def direct_magic_route(self, **witnesses):
        """Resolve the conditional MP/return seam after callback selection.

        This owns no effect mutation or RNG and does not close ordered battle
        execution. In particular Nocast cannot refund selection's earlier draw.
        """
        effects = {
            "MAGIC_Recovery": "recovery",
            "MAGIC_StatusChange": "status_change",
            "MAGIC_StatusRecovery": "status_recovery",
            "MAGIC_AttReverse": "att_reverse",
        }
        try:
            effect = effects[self.magic.function_name]
        except KeyError as exc:
            raise ValueError("Combined magic is outside positive ordinary wrapper boundary") from exc
        return resolve_combined_direct_magic_route(
            effect=effect, target_slot=self.source_target_slot, **witnesses,
        )


def _ascii_int(token:bytes):
    token=bytes(token).strip()
    if not re.fullmatch(rb"[+-]?\d+",token):
        return None
    return int(token.decode("ascii"),10)


def _option_structure(raw:bytes):
    raw=bytes(raw)
    parts=raw.split(b"|")
    marker=parts[0] if parts else b""
    declared=_ascii_int(parts[1]) if len(parts)>1 else None
    effective=None if declared is None else min(int(declared),10)
    tokens=()
    ints=()
    if effective is not None and effective>0:
        tokens=tuple(parts[2:2+effective])
        ints=tuple(_ascii_int(token) for token in tokens)
    well=bool(
        effective is not None
        and effective>0
        and len(parts)>=2+effective
        and len(ints)==effective
        and all(value is not None for value in ints)
    )
    return (
        hashlib.sha256(marker).hexdigest(),
        declared,
        effective,
        tuple(int(value) for value in ints if value is not None),
        well,
    )


def _validate_exact_population(
    petskill_runtime:Recovered25PetSkillRuntime,
):
    rows=tuple(sorted(
        (
            entry for entry in petskill_runtime.skills.values()
            if entry.function_name==CALLBACK_NAME
        ),
        key=lambda entry:int(entry.skill_id),
    ))
    ids=tuple(int(entry.skill_id) for entry in rows)
    if ids != RECOVERED25_COMBINED_CALLBACK_IDS:
        raise ValueError(
            "recovered25 Combined callback population must be exactly "
            "627/629/630/632/637/646/648"
        )

    expected_by_id={int(row[0]):row for row in EXPECTED_EXACT_ROWS}
    if tuple(sorted(expected_by_id)) != RECOVERED25_COMBINED_CALLBACK_IDS:
        raise ValueError("Combined pinned exact-row evidence drift")

    by_id={}
    for entry in rows:
        expected=expected_by_id[int(entry.skill_id)]
        raw=bytes(entry.option_bytes)
        marker_sha,declared,effective,magic_ids,well=_option_structure(raw)
        actual=(
            int(entry.skill_id),
            int(entry.field),
            int(entry.target),
            int(entry.cost),
            int(entry.illegal),
            len(raw),
            hashlib.sha256(raw).hexdigest(),
            b"\0" in raw,
            marker_sha,
            declared,
            effective,
            magic_ids,
            well,
        )
        pinned=(
            int(expected[0]),
            int(expected[1]),
            int(expected[2]),
            int(expected[3]),
            int(expected[4]),
            int(expected[6]),
            str(expected[7]),
            bool(expected[8]),
            str(expected[9]),
            expected[10],
            expected[11],
            tuple(int(x) for x in expected[12]),
            bool(expected[13]),
        )
        if actual != pinned:
            raise ValueError(
                f"recovered25 Combined exact row drift for ID {entry.skill_id}"
            )
        by_id[int(entry.skill_id)]=(entry,declared,magic_ids)
    return by_id


def _magic_crosslink(magic_id:int)->CombinedMagicCrosslink:
    magic_id=int(magic_id)
    expected={int(row[0]):row for row in EXPECTED_EXACT_MAGIC_ROWS}
    if len(expected)!=19:
        raise ValueError("Combined exact magic crosslink population drift")
    row=expected.get(magic_id)
    if row is None:
        raise ValueError(
            f"Combined selected magic {magic_id} lacks exact recovered crosslink"
        )
    return CombinedMagicCrosslink(
        magic_id=magic_id,
        function_name=str(row[1]),
        field=int(row[3]),
        target=int(row[4]),
        target_deadflg=int(row[5]),
        idx=None if row[6] is None else int(row[6]),
        direct_item_index=0,
    )


def resolve_enemy_ai_combined_submission(
    spawned:SpawnedEnemy,
    *,
    skill_slot:int,
    target_slot:int,
    petskill_runtime:Recovered25PetSkillRuntime,
    draw_index:int,
)->EnemyAiCombinedSubmission:
    """Resolve one positively referenced recovered25 Combined selection.

    draw_index is the already-reduced historical rand()%effective_count value.
    No Python RNG is owned by this bridge.
    """
    skill_slot=int(skill_slot)
    target_slot=int(target_slot)
    if not 0 <= skill_slot < 7:
        raise ValueError("enemy AI Combined skill slot must be in 0..6")
    if not 0 <= target_slot < 10:
        raise ValueError(
            "enemy AI Combined target must be player-side slot 0..9"
        )
    if not isinstance(petskill_runtime,Recovered25PetSkillRuntime):
        raise TypeError("Combined bridge requires recovered25 pet-skill runtime")

    by_id=_validate_exact_population(petskill_runtime)
    slots=tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots)!=7:
        raise ValueError(
            "enemy template lacks authoritative seven-slot pet-skill identity"
        )
    skill_id=int(slots[skill_slot])
    if skill_id not in RECOVERED25_COMBINED_EXECUTABLE_IDS:
        raise ValueError(
            "enemy AI selected Combined slot outside positively referenced "
            "recovered25 IDs 627/632/637"
        )
    entry,declared,magic_ids=by_id[skill_id]
    selection=resolve_combined_selection(
        target_slot=target_slot,
        declared_count=int(declared),
        magic_ids=tuple(magic_ids),
        draw_index=draw_index,
    )
    magic=_magic_crosslink(selection.selected_magic_id)
    return EnemyAiCombinedSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=skill_id,
        callback=entry.function_name,
        source_target_slot=target_slot,
        selection=selection,
        magic=magic,
    )
