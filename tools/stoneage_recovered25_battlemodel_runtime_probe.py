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
from tools.stoneage_recovered25_petskill_pressure_probe import analyze_runtime_objects as analyze_pressure
from tools.stoneage_battlemodel_hit_loop import BattleModelDraw
from tools.stoneage_battlemodel_physical_attackseq import (
    PHYSICAL_SCOPE_R1, BattleModelPhysicalContext, BattleModelPhysicalProfile,
)
from tools.stoneage_battlemodel_itemcrush_model import BattleModelItemCrushContext, EmptyEquipmentParticipant
from tools.stoneage_battlemodel_round_action import (
    BATTLEMODEL_ORDINARY_SCOPE_R1, BATTLEMODEL_LETHAL_PROFIT_SCOPE_R1,
    BATTLEMODEL_ULTIMATE_EXIT_SCOPE_R1, BattleModelRoundAction, BattleModelSelectedRoundInputs,
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
from tools.stoneage_enemy_ai_model import parse_normal_enemy_ai_options, resolve_common_normal_enemy_ai, EnemyAiTarget
from tools.stoneage_recovered25_encounter_runtime import load_recovered25_encounter_runtime
from tools.stoneage_encount_chain_probe import configured_file, setup_values

EXPECTED_ENEMYBASE_SHA256 = "1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7"
GOLDEN_PATH = Path(__file__).resolve().parents[1] / "game/STONEAGE-BATTLEMODEL-RUNTIME-GOLDEN-R1.json"
# Independent normal-AI control, never represented as recovered TACTICSOPTION.
CONTROLLED_AI_OPTION = "at:1;1;1|gu:1|wa:0;0;1;0;0;0;0"
AI_FILE_HASHES = {
    "enemyfile": ("enemy*.txt", "cc7418d3b6726f1c458fef9e44a24696d05f076b67c62a56ed2293e26ae63bb6"),
    "groupfile": ("group*.txt", "4a02f2a3fa3d2dcf5589d8a2a560313c35d5a0a7e5e0589cc8df5f7df159ea8f"),
    "encountfile": ("encount*.txt", "70bbd997d98508a0587df183b5bdd48222ff42db91bf21bea632e0ed6f2fea87"),
}


def verify_ai_files(data_dir, setup):
    config = setup_values(setup)
    for key, (pattern, expected) in AI_FILE_HASHES.items():
        path = configured_file(data_dir, config, key, [pattern])
        if path is None or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("complete recovered BattleModel AI file identity drift")


def selected_inputs(action):
    return BattleModelSelectedRoundInputs(
        action.submission.profile, action.submission.source_profile, action.scope,
        action.physical_context, action.itemcrush_context, action.opposing_slot_order,
        action.paralysis_resistance_by_slot, action.draws)


def ai_witness(context, action, kwargs, *, variant=None):
    """Keep all work/physical/RNG inputs; derive submission from normal AI."""
    original = context.spawned_enemies[0]
    variant = variant or SimpleNamespace(tactics=1, tactics_option=CONTROLLED_AI_OPTION)
    spawned = SimpleNamespace(template=original.template, participant=original.participant, variant=variant)
    context = replace(context, spawned_enemies=(spawned,))
    options = parse_normal_enemy_ai_options(variant.tactics_option)
    if options.skill_weights[2] <= 0 or options.enemy_attack_ai_random_override is not None:
        raise ValueError("BattleModel AI witness requires supported positive wa index2")
    mode = (options.attack_weight + options.guard_weight + options.magic_weight
            + options.escape_weight + sum(options.skill_weights[:2]))
    result = dict(kwargs)
    result.pop("battlemodel_actions_by_participant_id")
    commands = result.pop("commands")
    result.update(player_side_commands={pid: c for pid, c in commands.items() if pid != "enemy"},
                  enemy_mode_rolls={"enemy": mode},
                  enemy_target_rolls={"enemy": 0} if options.target_selection == 1 else {},
                  battlemodel_inputs_by_enemy_id={"enemy": selected_inputs(action)})
    return context, result


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
                    ai_context, ai_kwargs = ai_witness(context, action, kwargs)
                    ai_before = repr(ai_context)
                    # Random target index0 in the independent control selects
                    # player slot0. Compare the complete result with an explicit
                    # action carrying that exact scheduling target as well.
                    expected_submission = replace(action.submission, source_target_carrier=0)
                    selected_kwargs = dict(kwargs,
                        commands={**kwargs["commands"], "enemy": BattleCommand(BATTLE_COM_NONE, 0)},
                        battlemodel_actions_by_participant_id={"enemy": replace(action, submission=expected_submission)})
                    _, selected_direct = LocalRuntimeSessionCoordinator(stack, None).resolve_persistent_attack_wait_round(
                        context, **selected_kwargs)
                    ai_next, ai_result = LocalRuntimeSessionCoordinator(stack, None).resolve_persistent_battlemodel_round_with_enemy_ai(
                        ai_context, **ai_kwargs)
                    # The normal selector may choose a different scheduling
                    # carrier; type5 owns its own hit-target plan. Semantic
                    # source order and all persistent writes must still agree.
                    if (semantic_result(ai_result, charset=charset, scenario=scenario) != wanted
                            or ai_result != selected_direct
                            or repr(ai_context) != ai_before
                            or ai_next.persistent_battle_state != selected_direct.after):
                        raise ValueError("BattleModel selected normal-AI golden drift")
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


def run_recovered_ai_goldens(stack, *, position=None):
    """Census active variants and execute real normal options where supported.

    This proves active variant-to-selection composition with controlled work;
    natural encounter area/group/spawn reachability remains a separate gate.
    """
    results = []
    golden = json.loads(GOLDEN_PATH.read_text())["scenarios"]
    for tempno in (1178, 1179):
        variants = sorted((v for v in stack.encounter_runtime.enemies.values() if v.tempno == tempno),
                          key=lambda v: v.enemy_id)
        eligible = []
        for variant in variants:
            if variant.tactics != 1:
                continue
            options = parse_normal_enemy_ai_options(variant.tactics_option)
            if (options.skill_weights[2] > 0 and options.enemy_attack_ai_random_override is None
                    and options.target_selection in (1, 2, 3)):
                eligible.append(variant)
        count = 0
        chosen = eligible[0] if eligible else None
        if chosen is not None:
            for charset in (PROFILE_BIG5, PROFILE_UTF8):
                for source in BASE_STATUS_LITERALS_BY_SOURCE:
                    for scenario, expected in golden.items():
                        context, action, kwargs = build_witness(stack, tempno=tempno, charset=charset,
                            source=source, scenario=scenario, position=position)
                        ai_context, ai_kwargs = ai_witness(context, action, kwargs, variant=chosen)
                        state = context.persistent_battle_state
                        targets = tuple(EnemyAiTarget(slot=state.slots[p.participant_id], participant_id=p.participant_id,
                            kind=p.kind, hp=p.hp) for p in (state.session.player, *state.session.allied_pets))
                        decision = resolve_common_normal_enemy_ai(chosen.tactics_option, targets,
                            mode_roll=ai_kwargs["enemy_mode_rolls"]["enemy"],
                            target_roll=ai_kwargs["enemy_target_rolls"].get("enemy"))
                        if decision is None or decision.kind != "skill" or decision.skill_slot != 2:
                            raise ValueError("recovered BattleModel normal-AI selection drift")
                        target = decision.target_slot
                        reference_kwargs = dict(kwargs,
                            commands={**kwargs["commands"], "enemy": BattleCommand(BATTLE_COM_NONE, target)},
                            battlemodel_actions_by_participant_id={"enemy": replace(action,
                                submission=replace(action.submission, source_target_carrier=target))})
                        coordinator = LocalRuntimeSessionCoordinator(stack, None)
                        _, reference = coordinator.resolve_persistent_attack_wait_round(context, **reference_kwargs)
                        before = repr(ai_context)
                        next_context, actual = coordinator.resolve_persistent_battlemodel_round_with_enemy_ai(ai_context, **ai_kwargs)
                        wanted = dict(expected, player_paralysis=0,
                            pre_tick_player_paralysis=int(scenario == "status_success" and charset == PROFILE_BIG5))
                        if (actual != reference or semantic_result(actual, charset=charset, scenario=scenario) != wanted
                                or repr(ai_context) != before or next_context.persistent_battle_state != reference.after):
                            raise ValueError("recovered BattleModel selected AI result drift")
                        count += 1
        results.append(dict(tempno=tempno, active_variants=len(variants),
            eligible_normal_variants=len(eligible), witness_enemy_id=None if chosen is None else chosen.enemy_id,
            option_utf8_sha256=None if chosen is None else hashlib.sha256(chosen.tactics_option.encode()).hexdigest(),
            cases=count))
    print("BATTLEMODEL_RECOVERED_NORMAL_AI|" + json.dumps(results, sort_keys=True, separators=(",", ":")))
    print("COUNT|battlemodel_recovered_normal_ai_goldens=" + str(sum(row["cases"] for row in results)))
    return results


def verify_complete_pressure(stack):
    """Recount the entire loaded population while keeping BattleModel OPEN."""
    result = analyze_pressure(stack.petskill_runtime, stack.enemybase_runtime)
    closed = sum(row["slot_uses"] for row in result["rows"] if row["status"] == "closed_runtime")
    pending = sum(row["slot_uses"] for row in result["rows"] if row["status"] == "open")
    ub = sum(row["slot_uses"] for row in result["rows"] if row["status"] == "historical_ub")
    model = tuple(row for row in result["rows"] if row["callback"] == "PETSKILL_BattleModel")
    if (result["total_positive_slot_uses"] != 2486 or result["unresolved_skill_ids"]
            or (closed, pending, ub) != (2461, 22, 3) or len(model) != 1
            or model[0] != {"callback": "PETSKILL_BattleModel", "skill_ids": (638,),
                            "slot_uses": 2, "templates": 2, "status": "open"}):
        raise ValueError("BattleModel complete verified pressure ledger drift")
    return {"total": 2486, "closed": closed, "open": pending, "historical_ub": ub}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path)
    args = parser.parse_args()
    verify_files(args.data_dir, args.setup)
    verify_ai_files(args.data_dir, args.setup)
    stack = SimpleNamespace(
        petskill_runtime=load_recovered25_petskill_runtime(data_dir=args.data_dir, setup=args.setup),
        enemybase_runtime=load_recovered25_enemybase_runtime(data_dir=args.data_dir, setup=args.setup),
        encounter_runtime=load_recovered25_encounter_runtime(data_dir=args.data_dir, setup=args.setup))
    count = run_runtime_golden(stack)
    run_recovered_ai_goldens(stack)
    pressure = run_identity_pressure(stack)
    ledger = verify_complete_pressure(stack)
    print(f"COUNT|battlemodel_recovered_persistent_coordinator_goldens={count}")
    print(f"COUNT|battlemodel_selected_normal_ai_controls={count}")
    print(f"COUNT|battlemodel_current_identity_rejections={pressure}")
    print("PRESSURE|" + "|".join(f"{key}={value}" for key, value in ledger.items()))
    print("RESOLUTION|RECOVERED25_BATTLEMODEL_RUNTIME_GOLDEN_PASS")
    print("BOUNDARY|controlled_work_and_normal_AI_option_original_build_encounter_membership_OPEN")


if __name__ == "__main__":
    main()
