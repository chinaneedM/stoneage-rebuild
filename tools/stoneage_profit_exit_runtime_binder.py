"""Fail-closed runtime binder from actual profit boundaries to whole-scan R1.

This adapter deliberately accepts only the canonical SIDE_OFFSET10 subset that
is already represented by the immutable native-matched ProfitExitSnapshot:
one owner on player entry0..4, owned battle pets on entry5..9, enemies on the
opposite side, no ride/items, and one non-pet profit recipient per boundary.

Unsupported modern layouts and unresolved command groupings are not coerced.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping, Sequence

from tools.stoneage_battle_round_model import (
    OrdinaryProfitBoundarySnapshot,
    OrdinaryRoundEvent,
    PROFIT_BOUNDARY_ORDINARY_PER_HIT,
    PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL,
)
from tools.stoneage_battle_status_model import (
    BASE_STATUS_ORDER,
    BaseBattleStatusRuntime,
)
from tools.stoneage_default_pet_exit_model import DefaultPetExitAuthority
from tools.stoneage_nocast_runtime_state import NocastRoundOverlay
from tools.stoneage_profit_exit_scan_model import (
    ProfitExitCharacter,
    ProfitExitSnapshot,
    ProfitExitScanResult,
    ProfitExitStatusProjection,
    project_profit_exit_status_clear,
    resolve_profit_exit_scan,
)
from tools.stoneage_singleplayer_battle import BattleSession


SUPPORTED_PROFIT_BOUNDARY_KINDS = frozenset({
    PROFIT_BOUNDARY_ORDINARY_PER_HIT,
    PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL,
})


class ProfitBoundaryUnsupported(ValueError):
    """The runtime boundary is outside the currently native-shaped subset."""


@dataclass(frozen=True)
class ProfitBoundaryScanStep:
    boundary_index: int
    recipient_id: str
    result: ProfitExitScanResult
    status_projection: ProfitExitStatusProjection | None


@dataclass(frozen=True)
class ProfitBoundaryScanSettlement:
    steps: tuple[ProfitBoundaryScanStep, ...]
    final_snapshot: ProfitExitSnapshot
    final_processed_death_ids: tuple[str, ...]


def _participants(session: BattleSession):
    values=(session.player,)+tuple(session.allied_pets)+tuple(session.enemies)
    result={str(p.participant_id):p for p in values}
    if len(result)!=len(values):
        raise ValueError("battle session participant identities must be unique")
    return result


def _merged_base_runtime(
    boundary: OrdinaryProfitBoundarySnapshot,
    persistent: Mapping[str,BaseBattleStatusRuntime],
    participant_ids: set[str],
) -> Mapping[str,BaseBattleStatusRuntime]:
    values=dict(persistent)
    values.update(boundary.base_status_runtime_by_participant_id)
    if set(values)!=participant_ids:
        missing=sorted(participant_ids-set(values))
        extra=sorted(set(values)-participant_ids)
        raise ProfitBoundaryUnsupported(
            f"profit boundary base-status coverage mismatch; missing={missing}, extra={extra}"
        )
    return MappingProxyType(values)


def _merged_overlay(
    boundary: OrdinaryProfitBoundarySnapshot,
    persistent: NocastRoundOverlay | None,
    participant_ids: set[str],
) -> NocastRoundOverlay | None:
    if persistent is None and boundary.nocast_overlay is None:
        return None
    values={}
    if persistent is not None:
        values.update(persistent.runtime_by_participant_id)
    if boundary.nocast_overlay is not None:
        values.update(boundary.nocast_overlay.runtime_by_participant_id)
    if set(values)!=participant_ids:
        missing=sorted(participant_ids-set(values))
        extra=sorted(set(values)-participant_ids)
        raise ProfitBoundaryUnsupported(
            f"profit boundary late-status coverage mismatch; missing={missing}, extra={extra}"
        )
    return NocastRoundOverlay(values)


def _status_counters(
    participant_id: str,
    base_runtime: Mapping[str,BaseBattleStatusRuntime],
    overlay: NocastRoundOverlay | None,
) -> tuple[int,...]:
    base=base_runtime[participant_id].status
    common=tuple(int(getattr(base,name)) for name in BASE_STATUS_ORDER)
    if overlay is None:
        late=(0,0,0,0)
    else:
        runtime=overlay.runtime_by_participant_id[participant_id]
        if runtime.unmodeled_status_active:
            raise ProfitBoundaryUnsupported(
                "unmodeled active late status is outside canonical profit scan"
            )
        late=(
            int(runtime.weaken_counter),
            0,  # deep poison remains outside the admitted modern schema
            int(runtime.barrier_counter),
            int(runtime.counter),
        )
    return common+late


def _canonical_authority(
    session: BattleSession,
    boundary: OrdinaryProfitBoundarySnapshot,
) -> DefaultPetExitAuthority:
    owner_id=str(session.player.participant_id)
    authorities=dict(boundary.default_pet_authorities_by_owner_id)
    if set(authorities)!={owner_id}:
        raise ProfitBoundaryUnsupported(
            "canonical profit scan requires exactly one explicit owner authority"
        )
    authority=authorities[owner_id]
    expected=tuple(str(p.participant_id) for p in session.allied_pets)
    if authority.owned_pet_ids!=expected:
        raise ProfitBoundaryUnsupported(
            "canonical profit scan requires exact ordered non-mail owned roster"
        )
    if len(expected)>5:
        raise ProfitBoundaryUnsupported("canonical owned roster exceeds five pets")
    return authority


def _recipient_id(
    boundary: OrdinaryProfitBoundarySnapshot,
    events: Sequence[OrdinaryRoundEvent],
    participants,
) -> str:
    indexes=tuple(boundary.trigger_event_indexes)
    try:
        trigger=tuple(events[index] for index in indexes)
    except IndexError as exc:
        raise ValueError("profit boundary trigger index outside round events") from exc

    if boundary.boundary_kind==PROFIT_BOUNDARY_ORDINARY_PER_HIT:
        if len(trigger)!=1:
            raise ProfitBoundaryUnsupported(
                "ordinary per-hit profit boundary must reference one event"
            )
        event=trigger[0]
        if event.is_combo or event.is_counter or event.battlemodel_skill_id is not None:
            raise ProfitBoundaryUnsupported(
                "ordinary canonical boundary excludes combo/counter/BattleModel event"
            )
        recipients=(
            tuple(str(pid) for pid in event.profit_participant_ids)
            if event.profit_participant_ids
            else (str(event.participant_id),)
        )
    elif boundary.boundary_kind==PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL:
        if not trigger or any(event.battlemodel_skill_id!=638 for event in trigger):
            raise ProfitBoundaryUnsupported(
                "BattleModel command-tail boundary requires only skill638 events"
            )
        actor_ids={str(event.participant_id) for event in trigger}
        if len(actor_ids)!=1:
            raise ProfitBoundaryUnsupported(
                "BattleModel command-tail boundary crossed actor identities"
            )
        if trigger[-1].result not in {"battlemodel_action","battlemodel_no_target"}:
            raise ProfitBoundaryUnsupported(
                "BattleModel command-tail lacks terminal action witness"
            )
        recipients=tuple(actor_ids)
    else:
        raise ProfitBoundaryUnsupported(
            f"unsupported profit boundary grouping: {boundary.boundary_kind}"
        )

    if len(recipients)!=1:
        raise ProfitBoundaryUnsupported(
            "canonical whole-scan binder admits one profit recipient"
        )
    recipient_id=recipients[0]
    if recipient_id not in participants:
        raise ValueError("profit recipient is not in battle session")
    if participants[recipient_id].kind=="pet":
        raise ProfitBoundaryUnsupported(
            "pet/party profit recipients require additional native vectors"
        )
    if recipient_id not in set(boundary.occupied_participant_id_by_slot.values()):
        raise ProfitBoundaryUnsupported(
            "profit recipient is not an occupied entry at this boundary"
        )
    return recipient_id


def _canonical_layout(
    session: BattleSession,
    boundary: OrdinaryProfitBoundarySnapshot,
    authority: DefaultPetExitAuthority,
    participants,
) -> None:
    occupied=dict(boundary.occupied_participant_id_by_slot)
    if len(set(occupied.values()))!=len(occupied):
        raise ValueError("profit boundary occupancy duplicates participant")
    reverse={pid:slot for slot,pid in occupied.items()}
    owner_id=str(session.player.participant_id)
    owner_slot=reverse.get(owner_id)
    if owner_slot is None or not 0<=int(owner_slot)<5:
        raise ProfitBoundaryUnsupported(
            "canonical owner must occupy player entry0..4"
        )
    for pet_id in authority.owned_pet_ids:
        slot=reverse.get(pet_id)
        if slot is not None and not 5<=int(slot)<10:
            raise ProfitBoundaryUnsupported(
                "canonical active owned pet must occupy player entry5..9"
            )
    for enemy in session.enemies:
        pid=str(enemy.participant_id)
        slot=reverse.get(pid)
        if slot is not None and not 10<=int(slot)<20:
            raise ProfitBoundaryUnsupported(
                "canonical enemy must occupy opposite SIDE_OFFSET10 entry"
            )
    for slot,pid in occupied.items():
        if pid not in participants:
            raise ValueError("profit boundary occupancy references unknown participant")
        participant=participants[pid]
        if participant.kind=="player" and not 0<=int(slot)<5:
            raise ProfitBoundaryUnsupported("player occupancy is not canonical")
        if participant.kind=="pet" and not 5<=int(slot)<10:
            raise ProfitBoundaryUnsupported("pet occupancy is not canonical")
        if participant.kind=="enemy" and not 10<=int(slot)<20:
            raise ProfitBoundaryUnsupported("enemy occupancy is not canonical")
    if dict(authority.occupied_pet_slots)!={
        pet_id:reverse[pet_id]
        for pet_id in authority.owned_pet_ids
        if pet_id in reverse
    }:
        raise ValueError("boundary authority and actual canonical pet occupancy drift")


def _bind_snapshot(
    *,
    session: BattleSession,
    boundary: OrdinaryProfitBoundarySnapshot,
    persistent_hp_by_participant_id: Mapping[str,int],
    pending_exp_by_participant_id: Mapping[str,int],
    pending_pet_variable_ai_by_participant_id: Mapping[str,int],
    pending_player_charm_delta: int,
    pending_player_dead_pet_count_delta: int,
    base_status_runtime_by_participant_id: Mapping[str,BaseBattleStatusRuntime],
    nocast_overlay: NocastRoundOverlay | None,
    no_risk: bool,
    previous: ProfitExitSnapshot | None,
) -> tuple[ProfitExitSnapshot, Mapping[str,BaseBattleStatusRuntime], NocastRoundOverlay | None]:
    participants=_participants(session)
    ids=set(participants)
    authority=_canonical_authority(session,boundary)
    _canonical_layout(session,boundary,authority,participants)
    base_runtime=_merged_base_runtime(
        boundary,base_status_runtime_by_participant_id,ids
    )
    late_overlay=_merged_overlay(boundary,nocast_overlay,ids)

    occupied={
        str(pid):int(slot)
        for slot,pid in boundary.occupied_participant_id_by_slot.items()
    }
    prior_processed=set(boundary.prior_processed_death_ids)
    if not prior_processed.issubset(ids):
        raise ValueError("profit boundary processed death references unknown participant")

    chars={}
    for pid,participant in participants.items():
        prior=None if previous is None else previous.characters[pid]
        slot=occupied.get(pid)
        hp=(
            int(boundary.hp_by_slot[slot])
            if slot is not None
            else int(
                persistent_hp_by_participant_id.get(
                    pid,
                    participant.hp if prior is None else prior.hp,
                )
            )
        )
        valid=True if prior is None else bool(prior.valid)
        battle_mode=("battle" if slot is not None else ("none" if prior is None else prior.battle_mode))
        battle_index=(-1 if slot is None else int(slot))
        chars[pid]=ProfitExitCharacter(
            participant_id=pid,
            kind=str(participant.kind),
            level=int(participant.level),
            hp=hp,
            occupied_slot=slot,
            isdie=pid in prior_processed,
            ultimate=bool(
                slot is not None
                and int(boundary.ultimate_kind_by_slot.get(slot,0))>0
            ),
            valid=valid,
            death_count=0 if prior is None else int(prior.death_count),
            variable_ai_delta=(
                int(pending_pet_variable_ai_by_participant_id.get(pid,0))
                if prior is None else int(prior.variable_ai_delta)
            ),
            charm_delta=(
                int(pending_player_charm_delta)
                if prior is None and participant.kind=="player"
                else (0 if prior is None else int(prior.charm_delta))
            ),
            dead_pet_count=(
                int(pending_player_dead_pet_count_delta)
                if prior is None and participant.kind=="player"
                else (0 if prior is None else int(prior.dead_pet_count))
            ),
            pending_exp=(
                int(pending_exp_by_participant_id.get(pid,0))
                if prior is None else int(prior.pending_exp)
            ),
            kill_count=0 if prior is None else int(prior.kill_count),
            reward_exp=(
                int(participant.reward_exp or 0)
                if participant.kind=="enemy"
                else 0
            ),
            enemy_ultimate=False if prior is None else bool(prior.enemy_ultimate),
            status_counters=_status_counters(pid,base_runtime,late_overlay),
            battle_mode=battle_mode,
            battle_index=battle_index,
            command=0 if prior is None else int(prior.command),
            escape=0 if prior is None else int(prior.escape),
        )
    return (
        ProfitExitSnapshot(
            MappingProxyType(chars),
            authority,
            player_side=0,
            no_risk=bool(no_risk),
            elder_destination=None,
        ),
        base_runtime,
        late_overlay,
    )


def supports_profit_boundary_scan(
    *,
    session: BattleSession,
    boundaries: Sequence[OrdinaryProfitBoundarySnapshot],
    events: Sequence[OrdinaryRoundEvent],
    persistent_hp_by_participant_id: Mapping[str,int],
    pending_exp_by_participant_id: Mapping[str,int],
    pending_pet_variable_ai_by_participant_id: Mapping[str,int],
    pending_player_charm_delta: int,
    pending_player_dead_pet_count_delta: int,
    base_status_runtime_by_participant_id: Mapping[str,BaseBattleStatusRuntime],
    nocast_overlay: NocastRoundOverlay | None,
    initial_processed_death_ids: Sequence[str],
    no_risk: bool,
    battle_exited_participant_ids: Sequence[str]=(),
    ultimate_exited_participant_ids: Sequence[str]=(),
) -> bool:
    if not boundaries:
        return False
    if session.ride_pet is not None:
        return False
    if any(tuple(enemy.reward_items) for enemy in session.enemies):
        return False
    if battle_exited_participant_ids or ultimate_exited_participant_ids:
        return False
    if any(boundary.boundary_kind not in SUPPORTED_PROFIT_BOUNDARY_KINDS for boundary in boundaries):
        return False
    try:
        settlement=resolve_profit_boundary_scans(
            session=session,
            boundaries=boundaries,
            events=events,
            persistent_hp_by_participant_id=persistent_hp_by_participant_id,
            pending_exp_by_participant_id=pending_exp_by_participant_id,
            pending_pet_variable_ai_by_participant_id=pending_pet_variable_ai_by_participant_id,
            pending_player_charm_delta=pending_player_charm_delta,
            pending_player_dead_pet_count_delta=pending_player_dead_pet_count_delta,
            base_status_runtime_by_participant_id=base_status_runtime_by_participant_id,
            nocast_overlay=nocast_overlay,
            initial_processed_death_ids=initial_processed_death_ids,
            no_risk=no_risk,
        )
    except ProfitBoundaryUnsupported:
        return False
    return bool(settlement.steps)


def resolve_profit_boundary_scans(
    *,
    session: BattleSession,
    boundaries: Sequence[OrdinaryProfitBoundarySnapshot],
    events: Sequence[OrdinaryRoundEvent],
    persistent_hp_by_participant_id: Mapping[str,int],
    pending_exp_by_participant_id: Mapping[str,int],
    pending_pet_variable_ai_by_participant_id: Mapping[str,int],
    pending_player_charm_delta: int,
    pending_player_dead_pet_count_delta: int,
    base_status_runtime_by_participant_id: Mapping[str,BaseBattleStatusRuntime],
    nocast_overlay: NocastRoundOverlay | None,
    initial_processed_death_ids: Sequence[str],
    no_risk: bool,
) -> ProfitBoundaryScanSettlement:
    boundaries=tuple(boundaries)
    if not boundaries:
        raise ProfitBoundaryUnsupported("profit scan requires at least one boundary")
    if session.ride_pet is not None:
        raise ProfitBoundaryUnsupported("ride profit composition remains outside binder")
    if any(tuple(enemy.reward_items) for enemy in session.enemies):
        raise ProfitBoundaryUnsupported("item-bearing enemies remain outside binder")
    participants=_participants(session)
    expected=tuple(sorted(str(pid) for pid in initial_processed_death_ids))
    previous=None
    steps=[]

    for index,boundary in enumerate(boundaries):
        if boundary.boundary_kind not in SUPPORTED_PROFIT_BOUNDARY_KINDS:
            raise ProfitBoundaryUnsupported(
                f"unsupported profit boundary grouping: {boundary.boundary_kind}"
            )
        actual_prior=tuple(sorted(boundary.prior_processed_death_ids))
        if actual_prior!=expected:
            raise ValueError(
                "profit boundary processed-death chronology drift: "
                f"expected={expected}, actual={actual_prior}"
            )
        snapshot,base_runtime,late_overlay=_bind_snapshot(
            session=session,
            boundary=boundary,
            persistent_hp_by_participant_id=persistent_hp_by_participant_id,
            pending_exp_by_participant_id=pending_exp_by_participant_id,
            pending_pet_variable_ai_by_participant_id=pending_pet_variable_ai_by_participant_id,
            pending_player_charm_delta=pending_player_charm_delta,
            pending_player_dead_pet_count_delta=pending_player_dead_pet_count_delta,
            base_status_runtime_by_participant_id=base_status_runtime_by_participant_id,
            nocast_overlay=nocast_overlay,
            no_risk=no_risk,
            previous=previous,
        )
        recipient=_recipient_id(boundary,events,participants)
        result=resolve_profit_exit_scan(snapshot,recipient_id=recipient)
        projection=(
            None
            if not result.status_cleared_ids
            else project_profit_exit_status_clear(
                result,
                base_runtime=base_runtime,
                overlay=late_overlay,
            )
        )
        expected=tuple(sorted(
            pid for pid,char in result.after.characters.items()
            if char.valid and char.occupied_slot is not None and char.isdie
        ))
        previous=result.after
        steps.append(ProfitBoundaryScanStep(index,recipient,result,projection))

    return ProfitBoundaryScanSettlement(
        tuple(steps),
        previous,
        expected,
    )


def accounting_from_scan(
    settlement: ProfitBoundaryScanSettlement,
    *,
    exp_recipient_ids: Sequence[str],
    allied_pet_ids: Sequence[str],
    player_id: str,
):
    chars=settlement.final_snapshot.characters
    player_id=str(player_id)
    if player_id not in chars or chars[player_id].kind!="player":
        raise ValueError("scan accounting requires explicit player character")
    pending_exp={
        str(pid):int(chars[str(pid)].pending_exp)
        for pid in exp_recipient_ids
    }
    pending_variable_ai={
        str(pid):int(chars[str(pid)].variable_ai_delta)
        for pid in allied_pet_ids
    }
    return (
        MappingProxyType(pending_exp),
        MappingProxyType(pending_variable_ai),
        int(chars[player_id].charm_delta),
        int(chars[player_id].dead_pet_count),
    )
