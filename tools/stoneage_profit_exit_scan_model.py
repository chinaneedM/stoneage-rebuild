"""Immutable, bounded feature-off PvE death scan; no command-driver admission.

One owner, explicit non-mail roster, no items/ride and one non-pet profit
recipient. HP, ISDIE and ultimate are separate inputs. Penalty fields record
requested deltas, not clamped character attributes. Numeric original ABI and
notifications are deliberately outside this engine-neutral adapter.
"""
from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_battle_core_model import (
    BattleNormalDeathInputs, BattleUltimateDeathInputs, battle_exp_from_enemy,
    resolve_battle_normal_death_penalty, resolve_battle_ultimate_death_penalty,
)
from tools.stoneage_default_pet_exit_model import DefaultPetExitAuthority
from tools.stoneage_battle_status_model import (
    BASE_STATUS_ORDER, BaseBattleStatusRuntime, BaseBattleStatusState,
)
from tools.stoneage_nocast_runtime_state import NocastRoundOverlay


STATUS_ORDER = BASE_STATUS_ORDER + ("weaken", "deep_poison", "barrier", "nocast")


@dataclass(frozen=True)
class ProfitExitCharacter:
    participant_id: str
    kind: str
    level: int
    hp: int
    occupied_slot: int | None
    isdie: bool = False
    ultimate: bool = False
    valid: bool = True
    death_count: int = 0
    variable_ai_delta: int = 0
    charm_delta: int = 0
    dead_pet_count: int = 0
    pending_exp: int = 0
    kill_count: int = 0
    reward_exp: int = 0
    enemy_ultimate: bool = False
    status_counters: tuple[int, ...] = (0,) * 10
    battle_mode: str = "battle"
    battle_index: int = 0
    command: int = 0
    escape: int = 0

    def __post_init__(self):
        if type(self.participant_id) is not str or not self.participant_id:
            raise ValueError("explicit participant identity required")
        if self.kind not in {"player", "pet", "enemy"}:
            raise ValueError("unsupported profit/exit character kind")
        if self.battle_mode not in {"none", "battle", "final"}:
            raise ValueError("unsupported semantic battle mode")
        if self.occupied_slot is not None and (
            type(self.occupied_slot) is not int or not 0 <= self.occupied_slot < 20
        ):
            raise ValueError("explicit SIDE_OFFSET10 slot required")
        if type(self.status_counters) is not tuple or len(self.status_counters) != 10:
            raise ValueError("all ten original status counters required")
        for value in self.status_counters:
            if type(value) is not int or not 0 <= value < 2**31:
                raise ValueError("status counters require nonnegative int32")
        for name in ("level", "hp", "death_count", "dead_pet_count", "pending_exp",
                     "kill_count", "reward_exp", "battle_index", "command", "escape",
                     "variable_ai_delta", "charm_delta"):
            value = getattr(self, name)
            if type(value) is not int or not -(2**31) <= value < 2**31:
                raise ValueError(f"{name} requires signed int32")
        if self.level < 1 or any(getattr(self, n) < 0 for n in (
            "death_count", "dead_pet_count", "pending_exp", "kill_count", "reward_exp"
        )):
            raise ValueError("invalid level/count/EXP")
        for name in ("isdie", "ultimate", "valid", "enemy_ultimate"):
            if type(getattr(self, name)) is not bool:
                raise ValueError(f"explicit boolean {name} required")
        if not self.valid and self.occupied_slot is not None:
            raise ValueError("invalid character cannot occupy an entry")


@dataclass(frozen=True)
class ProfitExitSnapshot:
    characters: Mapping[str, ProfitExitCharacter]
    authority: DefaultPetExitAuthority
    player_side: int
    no_risk: bool = False
    elder_destination: tuple[int, int, int] | None = None

    def __post_init__(self):
        chars = dict(self.characters)
        if not isinstance(self.authority, DefaultPetExitAuthority):
            raise TypeError("explicit default-pet authority required")
        if self.player_side not in (0, 1) or type(self.player_side) is not int:
            raise ValueError("explicit player side0/1 required")
        if type(self.no_risk) is not bool:
            raise ValueError("explicit no-risk boolean required")
        if self.elder_destination is not None and (
            type(self.elder_destination) is not tuple or len(self.elder_destination) != 3
            or any(type(v) is not int or not 0 <= v < 2**31 for v in self.elder_destination)
        ):
            raise ValueError("controlled elder destination or None required")
        occupied = set()
        for pid, c in chars.items():
            if not isinstance(c, ProfitExitCharacter) or pid != c.participant_id:
                raise ValueError("character map identity drift")
            if c.occupied_slot is not None:
                if c.occupied_slot in occupied:
                    raise ValueError("duplicate entry occupancy")
                occupied.add(c.occupied_slot)
                side, pos = divmod(c.occupied_slot, 10)
                if c.kind in {"player", "pet"} and side != self.player_side:
                    raise ValueError("owned characters must occupy player side")
                if c.kind == "player" and pos >= 5:
                    raise ValueError("owner requires lower entry0..4")
                if c.kind == "pet" and pos < 5:
                    raise ValueError("pet requires entry5..9")
                if c.kind == "enemy" and side == self.player_side:
                    raise ValueError("enemy must occupy opposite side")
        a = self.authority
        if len(a.owned_pet_ids) > 5:
            raise ValueError("non-mail roster exceeds original five slots")
        if {pid for pid, c in chars.items() if c.kind == "player"} != {a.owner_id}:
            raise ValueError("adapter admits exactly one explicit owner")
        if {pid for pid, c in chars.items() if c.kind == "pet"} != set(a.owned_pet_ids):
            raise ValueError("pet set must match complete non-mail owned roster")
        if any(not chars[pid].valid for pid in (a.owner_id,) + a.owned_pet_ids):
            raise ValueError("owner and owned roster require valid characters")
        if dict(a.occupied_pet_slots) != {
            pid: chars[pid].occupied_slot for pid in a.owned_pet_ids
            if chars[pid].occupied_slot is not None
        }:
            raise ValueError("authority/actual pet occupancy drift")
        object.__setattr__(self, "characters", MappingProxyType(chars))


@dataclass(frozen=True)
class ProfitExitEffect:
    kind: str
    participant_id: str
    value: int


@dataclass(frozen=True)
class ProfitExitScanResult:
    before: ProfitExitSnapshot
    after: ProfitExitSnapshot
    processed_death_ids: tuple[str, ...]
    status_cleared_ids: tuple[str, ...]
    effects: tuple[ProfitExitEffect, ...]
    warp_requests: tuple[tuple[str, tuple[int, int, int]], ...]


def resolve_profit_exit_scan(snapshot: ProfitExitSnapshot, *, recipient_id: str) -> ProfitExitScanResult:
    """Settle one explicit profit boundary in side/slot order, never event order."""
    if not isinstance(snapshot, ProfitExitSnapshot):
        raise TypeError("typed profit/exit snapshot required")
    chars = dict(snapshot.characters)
    recipient = chars.get(recipient_id)
    if recipient is None or not recipient.valid or recipient.occupied_slot is None:
        raise ValueError("profit recipient requires an actual valid entry")
    if recipient.kind == "pet":
        raise ValueError("pet/party/ride profit recipients require additional native vectors")
    authority = snapshot.authority
    processed, cleared, effects, warps = [], [], [], []

    def note(kind, pid, value):
        effects.append(ProfitExitEffect(kind, pid, value))

    def change(pid, **values):
        chars[pid] = replace(chars[pid], **values)

    def selection_read():
        selected = authority.selected_pet_id
        # The roster tuple retains original slot order in this reduced domain.
        value = -1 if selected is None else authority.owned_pet_ids.index(selected)
        note("selection_read", authority.owner_id, value)
        return selected

    def loyalty(pid, delta):
        change(pid, variable_ai_delta=chars[pid].variable_ai_delta + delta)
        note("variable_ai_delta", pid, delta)

    def clear_status(pid):
        change(pid, status_counters=(0,) * 10, isdie=False)
        for _ in STATUS_ORDER:
            note("status_clear", pid, 0)
        note("isdie", pid, 0)
        cleared.append(pid)

    def exit_entry(pid):
        note("exit_request", pid, 0)
        c = chars[pid]
        if c.occupied_slot is None:
            return
        slot = c.occupied_slot
        change(pid, occupied_slot=None, escape=0, battle_mode="final", battle_index=-1)
        if c.kind == "enemy":
            change(pid, valid=False)
        elif c.kind == "player":
            # This adapter only calls player Exit after the scan has set ISDIE.
            change(pid, hp=1, isdie=False)
            note("isdie", pid, 0)
            note("hp", pid, 1)
            for pet in authority.owned_pet_ids:
                if chars[pet].occupied_slot == slot + 5:
                    change(pet, occupied_slot=None, battle_mode="none", battle_index=-1)
            clear_status(pid)
            for pet in authority.owned_pet_ids:
                p = chars[pet]
                if p.isdie or p.hp <= 0:
                    change(pet, hp=1, isdie=False)
                    note("isdie", pet, 0)
                    note("hp", pet, 1)
                change(pet, battle_mode="none")
                clear_status(pet)

    for slot in range(20):
        pid = next((pid for pid, c in chars.items() if c.occupied_slot == slot), None)
        if pid is None:
            continue
        c = chars[pid]
        if not c.valid or c.hp > 0 or c.isdie:
            continue
        if recipient.kind == "player" and slot // 10 != snapshot.player_side:
            award = battle_exp_from_enemy(c.reward_exp, recipient.level, c.level)
            r = chars[recipient_id]
            change(recipient_id, pending_exp=r.pending_exp + award, kill_count=r.kill_count + 1)
            change(pid, reward_exp=0)
        change(pid, isdie=True, death_count=c.death_count + 1)
        processed.append(pid)
        note("isdie", pid, 1)
        note("death_count", pid, c.death_count + 1)
        if c.kind == "player" and c.ultimate:
            selected = selection_read()
            if selected is not None:
                exit_entry(selected)
        if c.kind in {"player", "pet"}:
            inputs = dict(victim_kind=c.kind, victim_level=c.level,
                          owner_level=chars[authority.owner_id].level,
                          no_risk=snapshot.no_risk,
                          default_pet_present=authority.selected_pet_id is not None)
            penalty = (resolve_battle_ultimate_death_penalty(BattleUltimateDeathInputs(**inputs))
                       if c.ultimate else
                       resolve_battle_normal_death_penalty(BattleNormalDeathInputs(**inputs)))
            if c.kind == "player" and not snapshot.no_risk:
                change(pid, charm_delta=c.charm_delta + penalty.player_charm_delta)
                note("charm_delta", pid, penalty.player_charm_delta)
                selected = selection_read()
                if selected is not None:
                    loyalty(selected, penalty.default_pet_variable_ai_delta)
            elif c.kind == "pet":
                if c.ultimate:
                    authority = replace(authority, selected_pet_id=None)
                    note("selection_write", authority.owner_id, -1)
                if not snapshot.no_risk:
                    loyalty(pid, penalty.victim_pet_variable_ai_delta)
                if penalty.owner_dead_pet_count_delta:
                    owner = authority.owner_id
                    count = chars[owner].dead_pet_count + penalty.owner_dead_pet_count_delta
                    change(owner, dead_pet_count=count)
                    note("dead_pet_count", owner, count)
            if not c.ultimate and penalty.clears_victim_command:
                change(pid, command=0)
        if c.ultimate:
            if c.kind == "player" and snapshot.elder_destination is not None:
                warps.append((pid, snapshot.elder_destination))
                note("warp_request", pid, snapshot.elder_destination[0])
            if c.kind == "enemy":
                change(pid, enemy_ultimate=True)
            exit_entry(pid)
    authority = replace(authority, occupied_pet_slots={
        pid: chars[pid].occupied_slot for pid in authority.owned_pet_ids
        if chars[pid].occupied_slot is not None
    })
    after = replace(snapshot, characters=chars, authority=authority)
    return ProfitExitScanResult(snapshot, after, tuple(processed), tuple(cleared), tuple(effects), tuple(warps))


@dataclass(frozen=True)
class ProfitExitStatusProjection:
    base_runtime: Mapping[str, BaseBattleStatusRuntime]
    overlay: NocastRoundOverlay | None
    recalculation_required_ids: tuple[str, ...]


def project_profit_exit_status_clear(result: ProfitExitScanResult, *,
                                    base_runtime: Mapping[str, BaseBattleStatusRuntime],
                                    overlay: NocastRoundOverlay | None) -> ProfitExitStatusProjection:
    """Clear admitted counters; invalidate cached powers and request recalculation.

    This does not invent complianceParameter internals or a replacement quick
    value. The caller must finish recalculation before another command. NC
    notification state is retained: feature-off native evidence is no packet
    certificate. Deep poison/unmodeled active statuses are explicitly rejected.
    """
    base = dict(base_runtime)
    late = None if overlay is None else dict(overlay.runtime_by_participant_id)
    for pid in result.status_cleared_ids:
        source = result.before.characters[pid].status_counters
        if source[7] != 0:
            raise ValueError("deep poison is outside the admitted modern status schema")
        if pid not in base or not isinstance(base[pid], BaseBattleStatusRuntime):
            raise ValueError("clear requires complete typed base-status runtime")
        if tuple(getattr(base[pid].status, n) for n in BASE_STATUS_ORDER) != source[:6]:
            raise ValueError("base status does not match scan boundary snapshot")
        if late is None:
            if source[6] or source[8] or source[9]:
                raise ValueError("late counters require an explicit overlay")
        else:
            if pid not in late:
                raise ValueError("clear requires complete late-status overlay")
            runtime = late[pid]
            if runtime.unmodeled_status_active:
                raise ValueError("unmodeled active status cannot be silently cleared")
            if (runtime.weaken_counter, runtime.barrier_counter, runtime.counter) != (source[6], source[8], source[9]):
                raise ValueError("overlay counters do not match scan boundary snapshot")
            late[pid] = replace(runtime, counter=0, barrier_counter=0, weaken_counter=0,
                                weaken_active_at_visit=False, barrier_active_at_visit=False,
                                prepared_weaken_powers=None)
        base[pid] = replace(base[pid], status=BaseBattleStatusState())
    return ProfitExitStatusProjection(MappingProxyType(base),
        None if late is None else NocastRoundOverlay(late), result.status_cleared_ids)
