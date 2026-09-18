import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_exchangeman_usage_probe import analyze, emit


TEMPLATE = b"""NPCTEMPLATE
{
templatename=ExA
functionset=ExChangeMan
}
{
templatename=Other
functionset=Warp
}
"""

CREATE = b"""NPCCREATE
{
floorid=1
borncenter=1,1,1,1
enemy=ExA|file:args/ex.arg
}
{
floorid=1
borncenter=1,1,1,1
enemy=ExA|EventEnd|EventNo:2|EVENT:LV>10&ITEM=20*2,NOWEV!=3|TYPE:MESSAGE|GetItem:99|GetRandItem:50,51|EventEnd
}
{
floorid=1
borncenter=1,1,1,1
enemy=Other|file:args/other.arg
}
"""

ARG = b"""EventEnd
EventNo:1
EVENT:ITEM=10,ITEM=20
TYPE:ACCEPT
DelItem:10,20
GetStone:100
DelStone:10
EndSetFlg:1
CleanFlg:2
EventEnd
"""


class ExChangeManUsageProbeTests(unittest.TestCase):
    def build(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        (root / "args").mkdir()
        (root / "all.template").write_bytes(TEMPLATE)
        (root / "world.create").write_bytes(CREATE)
        (root / "args/ex.arg").write_bytes(ARG)
        (root / "args/other.arg").write_text("secret payload", encoding="utf-8")
        return td, root

    def test_resolves_only_exchangeman_refs_and_secondary_files(self):
        td, root = self.build()
        try:
            r = analyze(root)
            c = r["counts"]
            self.assertEqual(c["template_names_exchangeman"], 1)
            self.assertEqual(c["create_refs_exchangeman"], 2)
            self.assertEqual(c["create_refs_file_argument"], 1)
            self.assertEqual(c["create_refs_inline_argument"], 1)
            self.assertEqual(c["event_blocks_nonempty"], 2)
            self.assertEqual(c["event_segments_total"], 6)
            self.assertEqual(c["quirk_capable_delitem_loop_index_truncation"], 1)
            self.assertEqual(c["quirk_capable_getstone_delstone_nonnet"], 1)
            self.assertEqual(c["blocks_getitem_and_random"], 1)
            self.assertEqual(c["quirk_live_lv_not_equal"], 0)
            self.assertEqual(c["quirk_live_nowev_not_equal"], 1)
            self.assertEqual(c["quirk_live_item_relational"], 0)
            self.assertEqual(c["quirk_live_image_relational"], 0)
            self.assertEqual(c["quirk_live_pet_not_equal"], 0)
            self.assertEqual(c["endset_type_accept"], 1)
        finally:
            td.cleanup()

    def test_condition_families_and_operators_are_aggregated(self):
        td, root = self.build()
        try:
            r = analyze(root)
            self.assertGreaterEqual(r["family_terms"]["ITEM"], 3)
            self.assertEqual(r["family_terms"]["LV"], 1)
            self.assertEqual(r["family_terms"]["NOWEV"], 1)
            self.assertGreaterEqual(r["op_terms"]["="], 3)
            self.assertEqual(r["op_terms"][">"], 1)
            self.assertEqual(r["op_terms"]["!="], 1)
        finally:
            td.cleanup()

    def test_output_does_not_retain_payload_values(self):
        td, root = self.build()
        try:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(analyze(root))
            text = out.getvalue()
            self.assertNotIn("ExA", text)
            self.assertNotIn("args/ex.arg", text)
            self.assertNotIn("GetItem:99", text)
            self.assertNotIn("ITEM=20", text)
            self.assertNotIn("secret payload", text)
            self.assertIn("KEY_BLOCK|GetItem|1", text)
        finally:
            td.cleanup()

    def test_missing_secondary_file_is_counted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "x.template").write_bytes(
                b"NPCTEMPLATE\n{\ntemplatename=ExA\nfunctionset=ExChangeMan\n}\n"
            )
            (root / "x.create").write_bytes(
                b"NPCCREATE\n{\nfloorid=1\nborncenter=1,1,1,1\nenemy=ExA|file:missing.arg\n}\n"
            )
            r = analyze(root)
            self.assertEqual(r["counts"]["argument_files_missing"], 1)

    def test_duplicate_exchangeman_template_name_is_marked_ambiguous(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "x.template").write_bytes(
                b"""NPCTEMPLATE
{
templatename=Same
functionset=ExChangeMan
}
{
templatename=Same
functionset=Warp
}
"""
            )
            (root / "x.create").write_bytes(
                b"NPCCREATE\n{\nfloorid=1\nborncenter=1,1,1,1\nenemy=Same|EventEnd|EventNo:1|EVENT:LV=1|EventEnd\n}\n"
            )
            r = analyze(root)
            self.assertEqual(r["counts"]["template_names_exchangeman_ambiguous"], 1)
            self.assertEqual(r["counts"]["create_refs_exchangeman_ambiguous"], 1)


if __name__ == "__main__":
    unittest.main()
