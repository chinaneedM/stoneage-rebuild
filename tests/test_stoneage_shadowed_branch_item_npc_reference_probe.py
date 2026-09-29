import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from tools.stoneage_shadowed_branch_item_npc_reference_probe import (
    _argument_fields,
    _contains_integer_token,
    analyze,
    emit,
)


class _Reachability:
    reached_floor_ids = frozenset({100, 200})


class KeyItemNpcReferenceProbeTests(unittest.TestCase):

    def test_exact_integer_token_boundary(self):
        self.assertTrue(_contains_integer_token(b"LV>10&ITEM=20", 20))
        self.assertTrue(_contains_integer_token(b"20,30", 20))
        self.assertFalse(_contains_integer_token(b"120", 20))
        self.assertFalse(_contains_integer_token(b"201", 20))

    def test_argument_field_split(self):
        self.assertEqual(
            _argument_fields(b"FREE:LV>1&ITEM=20|AddItem:20\nX:abc"),
            (
                (b"FREE", b"LV>1&ITEM=20"),
                (b"AddItem", b"20"),
                (b"X", b"abc"),
            ),
        )

    @patch(
        "tools.stoneage_shadowed_branch_item_npc_reference_probe."
        "_locate_key_item",
        return_value=(20, 0),
    )
    @patch(
        "tools.stoneage_shadowed_branch_item_npc_reference_probe."
        "load_ordered_runtime_reachability",
        return_value=_Reachability(),
    )
    def test_reachable_reference_classes_are_aggregated_without_target_id(
        self,
        _runtime,
        _target,
    ):
        with tempfile.TemporaryDirectory() as td:
            npc = Path(td)
            (npc / "templates").write_bytes(
                b"NPCTEMPLATE\n"
                b"{\nTemplateName=W\nFunctionSet=WarpMan\n}\n"
                b"{\nTemplateName=E\nFunctionSet=EventMan\n}\n"
            )
            (npc / "creates").write_bytes(
                b"NPCCREATE\n"
                b"{\nFloorId=100\nBornCenter=1,1\nEnemy=W|file:w.arg\n}\n"
                b"{\nFloorId=200\nBornCenter=1,1\nEnemy=E|file:e.arg\n}\n"
            )
            (npc / "w.arg").write_bytes(b"FREE:LV>1&ITEM=20|WARP:820,1,1\n")
            (npc / "e.arg").write_bytes(b"AddItem:20|Other:120\n")

            audit = analyze(npc)
            classes = {
                (row.function_set, row.field_key): row
                for row in audit.classes
            }
            self.assertIn(("WarpMan", "FREE"), classes)
            self.assertIn(("EventMan", "AddItem"), classes)
            self.assertEqual(audit.matching_create_rows, 2)
            self.assertEqual(audit.matching_field_occurrences, 2)

            buffer = io.StringIO()
            with redirect_stdout(buffer):
                emit(audit)
            report = buffer.getvalue()
            self.assertIn("function=EventMan|field=AddItem", report)
            self.assertNotIn("ITEM=20", report)
            self.assertNotIn("AddItem:20", report)


if __name__ == "__main__":
    unittest.main()
