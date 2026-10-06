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


if __name__ == "__main__":
    unittest.main()
