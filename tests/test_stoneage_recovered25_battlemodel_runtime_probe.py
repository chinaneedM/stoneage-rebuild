"""Synthetic orchestration controls; exact bundle evidence runs separately in CI."""
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tests.test_stoneage_battlemodel_admission import fixture, spawned
from tools import stoneage_enemy_ai_battlemodel_bridge as bridge
from tools import stoneage_recovered25_battlemodel_runtime_probe as probe
from tools.stoneage_tw10_25_bridge_model import PetTemplateBridge
from tools import stoneage_recovered25_local_runtime_stack_smoke as stack_smoke
from tools.stoneage_local_runtime_session_coordinator import LocalRuntimeSessionCoordinator, EnemyAiCommonCommandBatch
from tools.stoneage_battle_round_model import BattleCommand, BATTLE_COM_GUARD, BATTLE_COM_NONE
from tools.stoneage_battle_status_model import BaseBattleStatusState


class RecoveredBattleModelGoldenTests(unittest.TestCase):
    def setUp(self):
        runtime, identities = fixture()
        self.templates = {}
        for tempno in (1178, 1179):
            t = spawned(tempno).template
            self.templates[tempno] = PetTemplateBridge(
                tempno, t.graphic_id, None, t.ai, 0, 0, 0, 0, 3, (638,),
                skill_slot_ids=t.skill_slot_ids, base_vital=t.base_vital,
                base_strength=t.base_strength, base_toughness=t.base_toughness,
                base_dexterity=t.base_dexterity)
        self.stack = SimpleNamespace(petskill_runtime=runtime,
                                     enemybase_runtime=SimpleNamespace(templates=self.templates))
        pin = patch.object(bridge, "EXPECTED_ROW_IDENTITIES", identities)
        pin.start()
        self.addCleanup(pin.stop)

    def test_sixty_synthetic_controls_execute_real_persistent_coordinator(self):
        # Only the recovered-data-only preliminary census is bypassed. The
        # actual submission, loop, profit binder and re-admission execute.
        with patch.object(probe, "analyze_admission"):
            self.assertEqual(probe.run_runtime_golden(self.stack), 60)

    def test_twelve_current_identity_mutations_reject_without_commit(self):
        self.assertEqual(probe.run_identity_pressure(self.stack), 12)

    def ai_case(self, scenario="status_success"):
        context, action, kwargs = probe.build_witness(self.stack, tempno=1178,
            charset=probe.PROFILE_BIG5, source="iris", scenario=scenario)
        context, kwargs = probe.ai_witness(context, action, kwargs)
        return context, kwargs

    def ai_run(self, context, kwargs, stack=None):
        return LocalRuntimeSessionCoordinator(stack or self.stack, None).resolve_persistent_battlemodel_round_with_enemy_ai(context, **kwargs)

    def reject_unchanged(self, context, kwargs, pattern, stack=None):
        before = repr(context)
        with self.assertRaisesRegex((ValueError, TypeError), pattern):
            self.ai_run(context, kwargs, stack)
        self.assertEqual(repr(context), before)

    def test_ai_profiles_and_execution_inputs_cover_only_selected_actors(self):
        context, kwargs = self.ai_case()
        for inputs in ({}, {"player": kwargs["battlemodel_inputs_by_enemy_id"]["enemy"]},
                       {**kwargs["battlemodel_inputs_by_enemy_id"], "ghost": kwargs["battlemodel_inputs_by_enemy_id"]["enemy"]}):
            with self.subTest(inputs=tuple(inputs)):
                self.reject_unchanged(context, dict(kwargs, battlemodel_inputs_by_enemy_id=inputs), "profile")
        self.reject_unchanged(context, dict(kwargs, enemy_mode_rolls={"enemy": 1}), "non-selected")
        self.reject_unchanged(context, dict(kwargs, battlemodel_inputs_by_enemy_id={"enemy": object()}), "typed")

    def test_ai_hit_rng_rejects_extra_missing_wrong_actor_and_suppressed_consumption(self):
        context, kwargs = self.ai_case()
        inputs = kwargs["battlemodel_inputs_by_enemy_id"]["enemy"]
        for draws in (inputs.draws[:-1], inputs.draws + (inputs.draws[-1],)):
            with self.subTest(draws=len(draws)):
                self.reject_unchanged(context, dict(kwargs, battlemodel_inputs_by_enemy_id={"enemy": replace(inputs, draws=draws)}), "RNG|draw")
        self.reject_unchanged(context, dict(kwargs, attack_rolls={"enemy": object()}), "non-ATTACK")
        state = context.persistent_battle_state
        statuses = dict(state.base_status_runtime_by_participant_id)
        statuses["enemy"] = replace(statuses["enemy"], status=BaseBattleStatusState(sleep=2))
        sleeping = replace(context, persistent_battle_state=replace(state, base_status_runtime_by_participant_id=statuses))
        self.reject_unchanged(sleeping, kwargs, "unused BattleModel RNG")

    def test_ai_guard_preserves_base_behavior_and_rejects_unused_target_rng(self):
        context, kwargs = self.ai_case()
        guard = dict(kwargs, enemy_mode_rolls={"enemy": 1}, enemy_target_rolls={}, battlemodel_inputs_by_enemy_id={})
        _, result = self.ai_run(context, guard)
        self.assertFalse(any(e.battlemodel_skill_id for e in result.round.events))
        self.assertEqual(result.after.hp_by_participant_id["player"], 10000)
        self.reject_unchanged(context, dict(guard, enemy_target_rolls={"enemy": 0}), "unused enemy AI target RNG")
        spawn = context.spawned_enemies[0]
        deterministic = replace(context, spawned_enemies=(SimpleNamespace(template=spawn.template, participant=spawn.participant,
            variant=SimpleNamespace(tactics=1, tactics_option=probe.CONTROLLED_AI_OPTION.replace("at:1;1;1", "at:1;1;2"))),))
        self.reject_unchanged(deterministic, kwargs, "unused enemy AI target RNG")

    def test_ai_identity_rechecks_all_rows_and_current_positive_placement(self):
        context, kwargs = self.ai_case()
        for skill_id in (638, 641, 649, 650):
            rows = dict(self.stack.petskill_runtime.skills)
            rows[skill_id] = replace(rows[skill_id], option_bytes=rows[skill_id].option_bytes + b"drift")
            self.reject_unchanged(context, kwargs, "identity drift", SimpleNamespace(petskill_runtime=replace(self.stack.petskill_runtime, skills=rows)))
        spawn = context.spawned_enemies[0]
        drifted = replace(context, spawned_enemies=(SimpleNamespace(template=replace(spawn.template, base_strength=41),
            participant=spawn.participant, variant=spawn.variant),))
        self.reject_unchanged(drifted, kwargs, "identity drift")
        # Choosing another wa slot cannot borrow ID638's execution inputs.
        wrongslot = replace(context, spawned_enemies=(SimpleNamespace(template=spawn.template, participant=spawn.participant,
            variant=SimpleNamespace(tactics=1, tactics_option="at:1;1;1|wa:1;0;0;0;0;0;0")),))
        self.reject_unchanged(wrongslot, dict(kwargs, enemy_mode_rolls={"enemy": 1}), "empty pet-skill slot")

    def test_loaded_variant_goldens_use_all_sixty_cases_without_control_fallback(self):
        variants = {tempno: SimpleNamespace(enemy_id=tempno, tempno=tempno, tactics=1,
            tactics_option=probe.CONTROLLED_AI_OPTION) for tempno in (1178, 1179)}
        self.stack.encounter_runtime = SimpleNamespace(enemies=variants)
        with patch("builtins.print"):
            rows = probe.run_recovered_ai_goldens(self.stack)
        self.assertEqual([row["cases"] for row in rows], [30, 30])
        self.assertEqual([row["witness_enemy_id"] for row in rows], [1178, 1179])
        variants[1178].tactics_option = "at:1;1;1|wa:0;0;0;0;0;0;0"
        with patch("builtins.print"):
            rows = probe.run_recovered_ai_goldens(self.stack)
        self.assertEqual([row["cases"] for row in rows], [0, 30])
        self.assertIsNone(rows[0]["witness_enemy_id"])
        self.assertEqual(rows[0]["variant_admissions"][0]["rejection_reasons"], ["wa_index2_zero_weight"])
        variants[1178].tactics = 2
        with patch("builtins.print"):
            rows = probe.run_recovered_ai_goldens(self.stack)
        self.assertEqual(rows[0]["variant_admissions"][0]["rejection_reasons"], ["unsupported_tactics_mode"])
        self.assertEqual(rows[0]["cases"], 0)

    def test_ai_caller_cannot_override_enemy_commands_or_widen_death_scope(self):
        context, kwargs = self.ai_case("normal_death")
        inputs = kwargs["battlemodel_inputs_by_enemy_id"]["enemy"]
        self.reject_unchanged(context, dict(kwargs, player_side_commands={**kwargs["player_side_commands"], "enemy": BattleCommand(BATTLE_COM_GUARD)}), "player side")
        self.reject_unchanged(context, dict(kwargs, battlemodel_inputs_by_enemy_id={"enemy": replace(inputs, scope=probe.BATTLEMODEL_ORDINARY_SCOPE_R1)}), "death requires")

    def test_ai_equipment_and_unproved_source_profiles_stay_closed(self):
        context, kwargs = self.ai_case()
        inputs = kwargs["battlemodel_inputs_by_enemy_id"]["enemy"]
        profiles = dict(inputs.physical_context.profiles)
        profiles[10] = replace(profiles[10], no_dodge=True)
        equipped = replace(inputs, physical_context=replace(inputs.physical_context, profiles=profiles))
        self.reject_unchanged(context, dict(kwargs, battlemodel_inputs_by_enemy_id={"enemy": equipped}), "equipment")
        for changes in ({"profile": "cp950"}, {"source_profile": "original-build"}):
            with self.assertRaisesRegex(ValueError, "explicit charset/source"):
                replace(inputs, **changes)

    def test_ai_batch_binds_actor_target_setup_and_freezes_submission_map(self):
        context, kwargs = self.ai_case()
        co = LocalRuntimeSessionCoordinator(self.stack, None)
        batch = co._build_persistent_enemy_common_batch(context, mode_rolls_by_enemy_id={"enemy": 2},
            target_rolls_by_enemy_id={"enemy": 0}, allow_battlemodel_skill=True,
            battlemodel_profiles_by_enemy_id={"enemy": (probe.PROFILE_BIG5, "iris")})
        submission = batch.battlemodel_submissions["enemy"]
        self.assertEqual((submission.skill_slot, submission.skill_id, submission.source_target_carrier), (2, 638, 0))
        self.assertEqual(submission.powers_before, (100, 80, 60))
        with self.assertRaises(TypeError):
            batch.battlemodel_submissions["enemy"] = submission
        for commands, effects in (({"enemy": BattleCommand(BATTLE_COM_GUARD)}, batch.setup_effects),
                                  ({"enemy": BattleCommand(BATTLE_COM_NONE, 5)}, batch.setup_effects),
                                  (batch.commands, {})):
            with self.assertRaisesRegex(ValueError, "carrier|drift"):
                EnemyAiCommonCommandBatch(commands, effects, battlemodel_submissions=batch.battlemodel_submissions)

    def test_corrupt_golden_exit_order_is_detected(self):
        golden = json.loads(probe.GOLDEN_PATH.read_text())
        golden["scenarios"]["owner_pet_ultimate"]["ultimate_exits"].reverse()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "golden.json"
            path.write_text(json.dumps(golden))
            with patch.object(probe, "analyze_admission"), self.assertRaisesRegex(ValueError, "golden drift"):
                probe.run_runtime_golden(self.stack, golden_path=path)

    def test_wrong_complete_file_hash_rejects_before_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "fixture.txt").write_bytes(b"unverified preservation input")
            with patch.object(probe, "load_recovered25_petskill_runtime",
                              return_value=replace(self.stack.petskill_runtime, source_file="fixture.txt")), \
                 patch.object(probe, "_active_enemybase_path", return_value=root / "fixture.txt"), \
                 self.assertRaisesRegex(ValueError, "complete recovered BattleModel file identity drift"):
                probe.verify_files(root, None)

    def test_cli_reports_counts_returned_by_stack_run(self):
        class ReachedExistingReport(Exception):
            pass
        output = []
        def record(*values):
            text = " ".join(str(v) for v in values)
            if text == "SEMANTIC_SOURCE_VERSION|recovered25":
                raise ReachedExistingReport
            output.append(text)
        args = ["stack-smoke"]
        for flag in ("--client-dat-dir", "--npc-dir", "--setup", "--server-data-dir",
                     "--server-map-root", "--mapset", "--client-adrn"):
            args.extend((flag, "/controlled/path"))
        with patch.object(sys, "argv", args), \
             patch.object(stack_smoke, "run", return_value=(None,) * 11 + (60, 12)), \
             patch("builtins.print", side_effect=record), self.assertRaises(ReachedExistingReport):
            stack_smoke.main()
        self.assertIn("BATTLEMODEL_STACK_GOLDEN|cases=60|templates=2|charsets=2|source_profiles=3", output)
        self.assertIn("BATTLEMODEL_STACK_IDENTITY_PRESSURE|rejections=12", output)
        self.assertIn("BATTLEMODEL_STACK_SELECTED_AI_CONTROL|cases=60|controlled_tactics_option=1", output)


if __name__ == "__main__":
    unittest.main()
