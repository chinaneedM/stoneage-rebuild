import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_npcenemy_usage_probe import analyze, emit


TEMPLATE = b"""NPCTEMPLATE
{
templatename=E
functionset=NPCEnemy
}
{
templatename=O
functionset=Warp
}
"""

CREATE = b"""NPCCREATE
{
floorid=1
borncenter=1,1,1,1
enemy=E|file:args/e.arg
enemy=O|file:args/o.arg
}
"""

ARG = b"""enemyno:1,2,3
entype:2
dieact:1
onebattle:1
gym:10
item:5,5
noitem:8
B_evend:1,2
B_evnow:3
steal:0
askbattlemsg1:secret
NEWNPCENEMY
OVER
NEWEVENT
FREE:LV>10&ITEM=5,NOWEV!=3
WARP:1,2,3;4,5,6
CHECKPARTY:FALSE
OVER
"""


class NPCEnemyUsageProbeTests(unittest.TestCase):
    def build(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        (root / "args").mkdir()
        (root / "all.template").write_bytes(TEMPLATE)
        (root / "world.create").write_bytes(CREATE)
        (root / "args/e.arg").write_bytes(ARG)
        (root / "args/o.arg").write_text("ignored", encoding="utf-8")
        return td, root

    def test_core_modes_and_shapes(self):
        td, root = self.build()
        try:
            r = analyze(root)
            c = r["counts"]
            self.assertEqual(c["create_refs_npcenemy"], 1)
            self.assertEqual(c["argument_files_resolved"], 1)
            self.assertEqual(r["mode_counts"]["encounter_walk_or_talk"], 1)
            self.assertEqual(r["mode_counts"]["dieact_warp"], 1)
            self.assertEqual(r["mode_counts"]["onebattle_exclusive"], 1)
            self.assertEqual(r["mode_counts"]["battle_gym_mode"], 1)
            self.assertEqual(r["mode_counts"]["steal_before_battle"], 1)
            self.assertEqual(c["item_list_duplicate_value_blocks"], 1)
            self.assertEqual(c["askbattle_prompt_blocks"], 1)
        finally:
            td.cleanup()

    def test_new_warp_and_free_expression_are_structurally_counted(self):
        td, root = self.build()
        try:
            r = analyze(root)
            c = r["counts"]
            self.assertEqual(c["newnpcenemy_blocks"], 1)
            self.assertEqual(c["over_segments_newevent"], 1)
            self.assertEqual(c["over_segments_with_free"], 1)
            self.assertEqual(c["over_segments_with_warp"], 1)
            self.assertEqual(c["over_segments_checkparty"], 1)
            self.assertEqual(r["free_family_terms"]["LV"], 1)
            self.assertEqual(r["free_family_terms"]["ITEM"], 1)
            self.assertEqual(r["free_family_terms"]["NOWEV"], 1)
            self.assertEqual(r["free_operator_terms"][">"], 1)
            self.assertEqual(r["free_operator_terms"]["="], 1)
            self.assertEqual(r["free_operator_terms"]["!="], 1)
        finally:
            td.cleanup()

    def test_list_length_histograms_do_not_expose_values(self):
        td, root = self.build()
        try:
            r = analyze(root)
            self.assertEqual(r["length_hist"][("enemyno", 3)], 1)
            self.assertEqual(r["length_hist"][("item", 2)], 1)
            self.assertEqual(r["length_hist"][("B_evend", 2)], 1)
        finally:
            td.cleanup()

    def test_output_has_no_payload_identity(self):
        td, root = self.build()
        try:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(analyze(root))
            text = out.getvalue()
            self.assertIn("MODE_BLOCK|encounter_walk_or_talk|1", text)
            self.assertIn("LIST_LENGTH|enemyno|length=3|blocks=1", text)
            self.assertNotIn("args/e.arg", text)
            self.assertNotIn("askbattlemsg1:secret", text)
            self.assertNotIn("FREE:LV>10", text)
            self.assertNotIn("WARP:1,2,3", text)
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
