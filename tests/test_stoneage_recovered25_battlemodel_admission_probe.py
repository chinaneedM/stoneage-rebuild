from contextlib import redirect_stdout
from dataclasses import replace
import hashlib
import io
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tests.test_stoneage_battlemodel_admission import fixture, spawned
from tests.test_stoneage_2battletimid_runtime import RAW_OPTION
from tools import stoneage_enemy_ai_battlemodel_bridge as bridge
from tools import stoneage_recovered25_battlemodel_admission_probe as probe
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry, Recovered25PetSkillRuntime,
)


class RecoveredBattleModelAdmissionProbeTests(unittest.TestCase):
    def setUp(self):
        runtime, identities = fixture()
        rows = dict(runtime.skills)
        # Semantically equivalent independent control, distinct OPTION identity.
        raw = "5|4|麻|1|30|攻%-3e1|101867 101868|control".encode("big5")
        rows[638] = replace(rows[638], option_bytes=raw)
        identities[638] = (*identities[638][:4], len(raw), hashlib.sha256(raw).hexdigest())
        rows[636] = Recovered25PetSkillEntry(636, 1, 7, 2, 10000, "PETSKILL_2BattleTimid", RAW_OPTION)
        self.runtime = Recovered25PetSkillRuntime(rows, "petskill")
        self.enemies = SimpleNamespace(templates={1178: spawned().template, 1179: spawned(1179).template})
        for tempno, graphic in ((178, 101872), (179, 101873)):
            self.enemies.templates[tempno] = SimpleNamespace(
                tempno=tempno, graphic_id=graphic, skill_slot_ids=(0, 0, 636, 0, 0, 0, 0),
            )
        identity_patch = patch.object(bridge, "EXPECTED_ROW_IDENTITIES", identities)
        identity_patch.start()
        self.addCleanup(identity_patch.stop)

    def test_checks_all_conditional_admissions_and_corrected_timid_slots(self):
        self.assertEqual(probe.analyze_admission(self.runtime, self.enemies), (24, 4))

    def test_rejects_extra_callback_placements_anywhere_in_table(self):
        self.enemies.templates[2000] = SimpleNamespace(skill_slot_ids=(0, 641, 0, 0, 0, 0, 0))
        with self.assertRaisesRegex(ValueError, "placement drift"):
            probe.analyze_admission(self.runtime, self.enemies)

    def test_rejects_shifted_real_timid_column_before_runtime_gate(self):
        self.enemies.templates[178].skill_slot_ids = (0, 0, 0, 636, 0, 0, 0)
        with self.assertRaisesRegex(ValueError, "2BattleTimid.*placement drift"):
            probe.analyze_admission(self.runtime, self.enemies)

    def test_cli_hashes_runtime_basename_in_data_directory_and_emits_only_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            content = b"independent controlled full-file witness"
            (data / "petskill").write_bytes(content)
            digest = hashlib.sha256(content).hexdigest()
            output = io.StringIO()
            with patch("sys.argv", ["probe", "--data-dir", str(data)]), \
                 patch.object(probe, "load_recovered25_petskill_runtime", return_value=self.runtime), \
                 patch.object(probe, "load_recovered25_enemybase_runtime", return_value=self.enemies), \
                 patch.object(probe, "EXPECTED_PETSKILL_SHA256", digest), redirect_stdout(output):
                probe.main()
            self.assertIn("battlemodel_conditional_admissions=24", output.getvalue())
            self.assertIn("2battletimid_corrected_admissions=4", output.getvalue())
            self.assertNotIn("control|", output.getvalue())
            self.assertNotIn("攻", output.getvalue())
            with patch("sys.argv", ["probe", "--data-dir", str(data)]), \
                 patch.object(probe, "load_recovered25_petskill_runtime", return_value=self.runtime), \
                 self.assertRaisesRegex(ValueError, "complete recovered25"):
                probe.main()


if __name__ == "__main__":
    unittest.main()
