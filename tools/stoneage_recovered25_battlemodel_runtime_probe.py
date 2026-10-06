"""Derived-only ID638 golden through current recovered templates and coordinator.

The preservation bundle supplies all OPTION/template bytes. Work, position and
RNG are explicit experiments, not claims about historical spawn/AI selection.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

from tools.stoneage_battlemodel_reference_model import (
    BASE_STATUS_LITERALS_BY_SOURCE, PROFILE_BIG5, PROFILE_UTF8,
)
from tools.stoneage_enemy_ai_battlemodel_bridge import resolve_enemy_ai_battlemodel_submission
from tools.stoneage_recovered25_battlemodel_admission_probe import analyze_admission
from tools.stoneage_recovered25_battlemodel_probe import EXPECTED_PETSKILL_SHA256
from tools.stoneage_recovered25_enemybase_runtime import (
    _active_enemybase_path, load_recovered25_enemybase_runtime,
)
from tools.stoneage_recovered25_petskill_runtime import load_recovered25_petskill_runtime
from tools.stoneage_battlemodel_hit_loop import BattleModelDraw
from tools.stoneage_battlemodel_physical_attackseq import (
    PHYSICAL_SCOPE_R1, BattleModelPhysicalContext, BattleModelPhysicalProfile,
)
from tools.stoneage_battlemodel_itemcrush_model import BattleModelItemCrushContext, EmptyEquipmentParticipant
from tools.stoneage_battlemodel_round_action import (
    BATTLEMODEL_ORDINARY_SCOPE_R1, BATTLEMODEL_LETHAL_PROFIT_SCOPE_R1,
    BATTLEMODEL_ULTIMATE_EXIT_SCOPE_R1, BattleModelRoundAction,
)
from tools.stoneage_battle_round_model import (
    BATTLE_COM_NONE, BATTLE_COM_WAIT, BattleCommand, BattleCommandSetupEffects,
    BattleCombatProfile, PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL,
)
from tools.stoneage_battle_status_model import BaseBattleStatusRuntime
from tools.stoneage_battle_guardian_model import GuardianRegistration
from tools.stoneage_battle_state_model import begin_persistent_battle, resolve_persistent_ordinary_round
from tools.stoneage_singleplayer_battle import BattleParticipant, BattleSession
from tools.stoneage_singleplayer_domain import EncounterRequest, EnemyVariantId, PetTemplateId, MapPosition
from tools.stoneage_local_runtime_session_coordinator import LocalRuntimeBattleContext, LocalRuntimeSessionCoordinator

EXPECTED_ENEMYBASE_SHA256 = "1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7"
GOLDEN_PATH = Path(__file__).resolve().parents[1] / "game/STONEAGE-BATTLEMODEL-RUNTIME-GOLDEN-R1.json"


def verify_files(data_dir: Path, setup: Path | None) -> None:
    runtime = load_recovered25_petskill_runtime(data_dir=data_dir, setup=setup)
    for path, expected in ((data_dir / runtime.source_file, EXPECTED_PETSKILL_SHA256),
                           (_active_enemybase_path(data_dir, setup), EXPECTED_ENEMYBASE_SHA256)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("complete recovered BattleModel file identity drift")


def build_witness(stack, *, tempno, charset, source, scenario, position=None):
    """Build explicit reduced work; template and skill identity remain untouched."""
    with_pet = scenario in {"owner_pet_ultimate", "pet_only_ultimate"}
    hp = 1 if scenario == "normal_death" else 10 if scenario == "owner_pet_ultimate" else 10000
    player = BattleParticipant("player", "player", "player", 10, hp,
                              500 if scenario == "normal_death" else hp, 100, 10, 40, None)
    enemy = BattleParticipant("enemy", "enemy", "enemy", 10, 500, 500, 100, 80, 60, None)
    actors = {0: player, 10: enemy}
    if with_pet:
        actors[5] = replace(player, participant_id="pet", kind="pet", hp=10,
                            max_hp=10, source_pet_slot=0)
    spawned = SimpleNamespace(template=stack.enemybase_runtime.templates[tempno], participant=enemy)
    submission = resolve_enemy_ai_battlemodel_submission(
        spawned, skill_slot=2, target_slot=5, petskill_runtime=stack.petskill_runtime,
        profile=charset, source_profile=source, powers_before=(100, 80, 60))
    guardians = {0: GuardianRegistration(5)} if with_pet else {}
    physical = BattleModelPhysicalContext(PHYSICAL_SCOPE_R1, "newpower_70pct", {
        slot: BattleModelPhysicalProfile(p.participant_id, p.level, 100, 0, p.defense,
                                       p.quick, (0, 0, 0, 0), fixed_vital=p.fixed_vital)
        for slot, p in actors.items()}, guardians)
    item = BattleModelItemCrushContext(source, "legacy", 400000, 2147483647, {
        slot: EmptyEquipmentParticipant(p.participant_id, p.kind, p.level, (-1,) * 5)
        for slot, p in actors.items()})
    draws = []
    status_known = submission.option_shape.status_known
    for i in range(4):
        if i >= (2 if with_pet else 1):
            draws.append(BattleModelDraw(i, "target_selection", 0))
        hits = (i in (0, 2) if scenario == "owner_pet_ultimate" else
                i in (0, 2, 3) if scenario == "pet_only_ultimate" else
                i == 0 if scenario == "normal_death" else True)
        if not hits:
            continue
        success = scenario == "status_success" and status_known
        if not success or i == 0:
            draws.append(BattleModelDraw(i, "attackseq_dodge", 10000))
        draws.extend((BattleModelDraw(i, "attackseq_critical", 10000),
                      BattleModelDraw(i, "attackseq_damage", 2)))
        surviving = scenario in {"status_success", "status_fail"} or (scenario == "pet_only_ultimate" and i != 0)
        if surviving:
            draws.append(BattleModelDraw(i, "itemcrush_check", 400000))
            if status_known and (not success or i == 0):
                draws.append(BattleModelDraw(i, "status", 1 if success else 100))
    scope = (BATTLEMODEL_LETHAL_PROFIT_SCOPE_R1 if scenario == "normal_death" else
             BATTLEMODEL_ULTIMATE_EXIT_SCOPE_R1 if with_pet else BATTLEMODEL_ORDINARY_SCOPE_R1)
    action = BattleModelRoundAction(scope, submission, physical, item,
                                   (0, 5) if with_pet else (0,),
                                   {slot: 0 for slot in actors}, tuple(draws))
    position = position or MapPosition(2000, 10, 10)
    encounter = EncounterRequest(position, 1, 1, EnemyVariantId(10), PetTemplateId(tempno), 10, 1)
    session = BattleSession(position, encounter, player, (actors[5],) if with_pet else (), (enemy,))
    state = begin_persistent_battle(session, slots={p.participant_id: s for s, p in actors.items()},
        default_pet_slot=0 if with_pet else None,
        base_status_runtime_by_participant_id={p.participant_id: BaseBattleStatusRuntime(work_quick=p.quick)
                                             for p in actors.values()})
    context = LocalRuntimeBattleContext("battlemodel-golden", "recovered25", 1, position,
        frozenset(), "controlled-work-payload", session, (spawned,), state)
    kwargs = dict(commands={p.participant_id: BattleCommand(BATTLE_COM_NONE, 5)
                            if s == 10 else BattleCommand(BATTLE_COM_WAIT) for s, p in actors.items()},
                  initiative_random_subtracts={p.participant_id: 0 for p in actors.values()},
                  profiles={p.participant_id: BattleCombatProfile(100, 0, 0, 0, 0, 0) for p in actors.values()},
                  attack_rolls={}, defense_profile="newpower_70pct", tie_break_order=tuple(p.participant_id for p in actors.values()),
                  battlemodel_actions_by_participant_id={"enemy": action})
    return context, action, kwargs


def semantic_result(result, *, charset, scenario):
    boundaries = tuple(b for b in result.round.profit_boundaries
                       if b.boundary_kind == PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL)
    if len(boundaries) != 1 or len(result.profit_scan_settlement.steps) != 1:
        raise ValueError("BattleModel must own exactly one command-tail whole scan")
    boundary = boundaries[0]
    if any(result.round.events[i].battlemodel_skill_id != 638 for i in boundary.trigger_event_indexes):
        raise ValueError("BattleModel boundary borrowed unrelated action")
    after = result.after
    hp = after.hp_by_participant_id
    death = scenario == "normal_death"
    owner_exit = scenario == "owner_pet_ultimate"
    expected_hp = 0 if death else 1 if owner_exit else None
    if expected_hp is not None and hp["player"] != expected_hp:
        raise ValueError("BattleModel golden player HP drift")
    if expected_hp is None and not 0 < hp["player"] < 10000:
        raise ValueError("BattleModel surviving player HP drift")
    if "pet" in hp and hp["pet"] != (1 if owner_exit else 0):
        raise ValueError("BattleModel golden pet HP drift")
    loops = tuple(e.battlemodel_loop_resolution for e in result.round.events
                  if e.battlemodel_loop_resolution is not None)
    if len(loops) != 1:
        raise ValueError("BattleModel golden requires one complete hit loop")
    loop = loops[0]
    pre_tick_paralysis = loop.entries[0].status_runtime.status.paralysis
    expected_pre_tick = int(scenario == "status_success" and charset == PROFILE_BIG5)
    if pre_tick_paralysis != expected_pre_tick:
        raise ValueError("BattleModel pre-tick charset/status golden drift")
    # The later player WAIT ticks away the one-turn paralysis; observing only
    # final status would make Big5 and UTF8 falsely look equivalent.
    expected_paralysis = 0
    paralysis = after.base_status_runtime_by_participant_id["player"].status.paralysis
    if paralysis != expected_paralysis:
        raise ValueError("BattleModel charset/status golden drift")
    return {
        "processed_deaths": list(after.profit_processed_death_ids),
        "scan_deaths": list(result.profit_scan_settlement.steps[0].result.processed_death_ids),
        "ultimate_exits": list(result.round.ultimate_exited_participant_ids),
        "default_pet_slot": after.default_pet_slot,
        "ultimate_by_slot": {str(s): k for s, k in boundary.ultimate_kind_by_slot.items()},
        "player_paralysis": paralysis,
        "pre_tick_player_paralysis": pre_tick_paralysis,
        "hp_write_slots": [e.actual_defender_slot for e in loop.events if e.hp_loss > 0],
        "turn": after.turn,
    }


def run_runtime_golden(stack, *, position=None, golden_path=GOLDEN_PATH):
    analyze_admission(stack.petskill_runtime, stack.enemybase_runtime)
    golden = json.loads(golden_path.read_text())
    if golden["schema"] != "stoneage.battlemodel-runtime-golden.r1":
        raise ValueError("BattleModel golden schema drift")
    count = 0
    for tempno in (1178, 1179):
        for charset in (PROFILE_BIG5, PROFILE_UTF8):
            for source in BASE_STATUS_LITERALS_BY_SOURCE:
                for scenario, expected in golden["scenarios"].items():
                    context, action, kwargs = build_witness(stack, tempno=tempno, charset=charset,
                                                           source=source, scenario=scenario, position=position)
                    before = repr(context)
                    direct = resolve_persistent_ordinary_round(context.persistent_battle_state, **kwargs,
                        command_setup_effects_by_participant_id={"enemy": BattleCommandSetupEffects(
                            attack_power=action.submission.setup.powers[0], defense_power=action.submission.setup.powers[1])},
                        guardian_registrations_by_defender_slot=action.physical_context.guardians)
                    next_context, result = LocalRuntimeSessionCoordinator(stack, None).resolve_persistent_attack_wait_round(context, **kwargs)
                    observed = semantic_result(result, charset=charset, scenario=scenario)
                    wanted = dict(expected)
                    wanted["player_paralysis"] = 0
                    wanted["pre_tick_player_paralysis"] = int(scenario == "status_success" and charset == PROFILE_BIG5)
                    if observed != wanted or direct != result:
                        raise ValueError(f"BattleModel recovered golden drift: {tempno}/{charset}/{source}/{scenario}")
                    if repr(context) != before or next_context.persistent_battle_state != direct.after:
                        raise ValueError("BattleModel coordinator mutated input or lost state")
                    count += 1
    if count != 60:
        raise ValueError("BattleModel recovered golden scenario population drift")
    return count


def run_identity_pressure(stack):
    """Replay a valid action against drifted CURRENT data, with no digest patch."""
    count = 0
    for tempno in (1178, 1179):
        context, _action, kwargs = build_witness(stack, tempno=tempno, charset=PROFILE_BIG5,
                                               source="iris", scenario="owner_pet_ultimate")
        candidates = []
        for skill_id in (638, 641, 649, 650):
            rows = dict(stack.petskill_runtime.skills)
            rows[skill_id] = replace(rows[skill_id], option_bytes=rows[skill_id].option_bytes + b"x")
            candidates.append((context, SimpleNamespace(petskill_runtime=replace(stack.petskill_runtime, skills=rows))))
        current = context.spawned_enemies[0]
        for field, value in (("base_strength", current.template.base_strength + 1),
                             ("skill_slot_ids", (638, 0, 0, 0, 0, 0, 0))):
            bad = SimpleNamespace(template=replace(current.template, **{field: value}), participant=current.participant)
            candidates.append((replace(context, spawned_enemies=(bad,)), stack))
        for bad_context, bad_stack in candidates:
            before = repr(bad_context)
            try:
                LocalRuntimeSessionCoordinator(bad_stack, None).resolve_persistent_attack_wait_round(bad_context, **kwargs)
            except ValueError:
                if repr(bad_context) != before:
                    raise ValueError("BattleModel rejected identity drift mutated input")
                count += 1
            else:
                raise ValueError("BattleModel current row/template/slot drift was admitted")
    if count != 12:
        raise ValueError("BattleModel identity-pressure coverage drift")
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path)
    args = parser.parse_args()
    verify_files(args.data_dir, args.setup)
    stack = SimpleNamespace(
        petskill_runtime=load_recovered25_petskill_runtime(data_dir=args.data_dir, setup=args.setup),
        enemybase_runtime=load_recovered25_enemybase_runtime(data_dir=args.data_dir, setup=args.setup))
    count = run_runtime_golden(stack)
    pressure = run_identity_pressure(stack)
    print(f"COUNT|battlemodel_recovered_persistent_coordinator_goldens={count}")
    print(f"COUNT|battlemodel_current_identity_rejections={pressure}")
    print("RESOLUTION|RECOVERED25_BATTLEMODEL_RUNTIME_GOLDEN_PASS")
    print("BOUNDARY|controlled_work_and_explicit_selection_original_build_AI_OPEN")


if __name__ == "__main__":
    main()
