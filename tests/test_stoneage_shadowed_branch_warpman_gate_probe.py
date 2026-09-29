import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.stoneage_shadowed_branch_warpman_gate_probe import (
    CONDITION_DEPENDENT,
    PAYABLE,
    UNCONDITIONALLY_FREE,
    _free_structure,
    analyze,
)


class _Orphan:
    def __init__(self, floor_id):
        self.floor_id = floor_id


class _Reachability:
    reached_floor_ids = frozenset({811})
    orphan_rows = (_Orphan(820),)


def _fixture(root: Path, arg: bytes) -> None:
    (root / "templates").write_bytes(
        b"NPCTEMPLATE\n"
        b"{\nTemplateName=W\nFunctionSet=WarpMan\n}\n"
    )
    (root / "creates").write_bytes(
        b"NPCCREATE\n"
        b"{\nFloorId=811\nBornCenter=1,1\n"
        b"Enemy=W|file:w.arg\n}\n"
    )
    (root / "w.arg").write_bytes(arg)


class ShadowedBranchWarpManGateProbeTests(unittest.TestCase):

    @patch(
        "tools.stoneage_shadowed_branch_warpman_gate_probe."
        "load_ordered_runtime_reachability",
        return_value=_Reachability(),
    )
    def test_allfree_ingress_is_classified_without_retaining_payload(
        self,
        _runtime,
    ):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _fixture(
                root,
                b"WARP:820,1,1|FREE:ALLFREE|FreeMsg:secret text\n",
            )
            audit = analyze(root)
            self.assertEqual(len(audit.rows), 1)
            row = audit.rows[0]
            self.assertEqual(row.source_floor, 811)
            self.assertEqual(row.destination_floor, 820)
            self.assertEqual(row.ordinary_route_class, UNCONDITIONALLY_FREE)
            self.assertTrue(row.free_allfree)
            self.assertFalse(row.warp_msg_required)
            self.assertEqual(row.free_or_groups, 1)
            self.assertEqual(row.free_condition_atoms, 1)
            self.assertEqual(row.free_condition_kinds, ("OTHER",))

    @patch(
        "tools.stoneage_shadowed_branch_warpman_gate_probe."
        "load_ordered_runtime_reachability",
        return_value=_Reachability(),
    )
    def test_payable_and_condition_dependent_paths_are_distinguished(
        self,
        _runtime,
    ):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _fixture(
                root,
                b"WARP:820,1,1|FREE:EVENT1|PayMsg:x|MONEY:100\n",
            )
            audit = analyze(root)
            self.assertEqual(
                audit.rows[0].ordinary_route_class,
                PAYABLE,
            )

            (root / "w.arg").write_bytes(
                b"WARP:820,1,1|FREE:EVENT1|NomalMsg:x\n"
            )
            audit = analyze(root)
            self.assertEqual(
                audit.rows[0].ordinary_route_class,
                CONDITION_DEPENDENT,
            )

    def test_free_structure_exposes_only_semantic_condition_kinds(self):
        groups, atoms, kinds = _free_structure(
            b"FREE:ITEM>123&ENDEV=456,LV>10|WARP:820,1,1"
        )
        self.assertEqual(groups, 2)
        self.assertEqual(atoms, 3)
        self.assertEqual(kinds, ("EVENT_END", "ITEM", "LEVEL"))

    @patch(
        "tools.stoneage_shadowed_branch_warpman_gate_probe."
        "load_ordered_runtime_reachability",
        return_value=_Reachability(),
    )
    def test_random_destination_set_preserves_target_occurrence_count(
        self,
        _runtime,
    ):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _fixture(
                root,
                b"WARP:820,1,1;500,2,2;820,3,3|FREE:ALLFREE\n",
            )
            row = analyze(root).rows[0]
            self.assertEqual(row.destination_count, 3)
            self.assertEqual(row.target_occurrences, 2)


if __name__ == "__main__":
    unittest.main()
