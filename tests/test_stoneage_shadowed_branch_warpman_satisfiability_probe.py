import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import (
    _clause_witness,
    _configured_itemset_paths,
    _configured_maxlevel,
    _item_ids,
    emit,
    parse_free_predicates,
    analyze,
)


class _Orphan:
    def __init__(self, floor_id):
        self.floor_id = floor_id


class _Reachability:
    reached_floor_ids = frozenset({811})
    orphan_rows = (_Orphan(820),)


def _item_row(item_id: int) -> bytes:
    fields = [b""] * 17
    fields[16] = str(item_id).encode("ascii")
    return b",".join(fields)


def _fixture(root: Path, free: bytes) -> tuple[Path, Path, Path]:
    npc = root / "data" / "npc"
    npc.mkdir(parents=True)
    (npc / "templates").write_bytes(
        b"NPCTEMPLATE\n"
        b"{\nTemplateName=W\nFunctionSet=WarpMan\n}\n"
    )
    (npc / "creates").write_bytes(
        b"NPCCREATE\n"
        b"{\nFloorId=811\nBornCenter=1,1\n"
        b"Enemy=W|file:w.arg\n}\n"
    )
    (npc / "w.arg").write_bytes(
        b"WARP:820,1,1|FREE:" + free + b"|PayMsg:x|MONEY:-1\n"
    )
    (root / "data" / "itemset.txt").write_bytes(
        _item_row(10) + b"\n" + _item_row(20) + b"\n"
    )
    setup = root / "setup.cf"
    setup.write_bytes(
        b"MAXLEVEL=140\n"
        b"itemset3file=data/itemset.txt\n"
        b"itemset4file=data/itemset.txt\n"
    )
    return npc, setup, root / "data"


class WarpManFreeDomainProbeTests(unittest.TestCase):

    def test_parser_preserves_key_operator_pairing_but_not_in_report(self):
        clauses = parse_free_predicates(
            b"LV>10&ITEM=20&ITEM<30,LV!=99"
        )
        self.assertEqual(len(clauses), 2)
        self.assertEqual(
            [(atom.key, atom.operator, atom.operand) for atom in clauses[0]],
            [("LV", ">", 10), ("ITEM", "=", 20), ("ITEM", "<", 30)],
        )
        self.assertEqual(
            (clauses[1][0].key, clauses[1][0].operator),
            ("LV", "!="),
        )

    def test_level_atoms_share_one_level_and_item_atoms_are_independent(self):
        clauses = parse_free_predicates(
            b"LV>100&LV<120&ITEM=10&ITEM=20"
        )
        witness = _clause_witness(
            clauses[0],
            maxlevel=140,
            item_ids=frozenset({10, 20}),
        )
        self.assertTrue(witness.satisfiable)

        contradictory = parse_free_predicates(b"LV>120&LV<100")[0]
        witness = _clause_witness(
            contradictory,
            maxlevel=140,
            item_ids=frozenset({10}),
        )
        self.assertFalse(witness.satisfiable)
        self.assertFalse(witness.atoms[0].witness)
        self.assertFalse(witness.atoms[1].witness)

    def test_active_item_catalog_and_maxlevel_are_read_from_recovered_shapes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            data = root / "data"
            data.mkdir()
            (data / "itemset.txt").write_bytes(
                _item_row(7) + b"\n" + _item_row(19) + b"\n"
            )
            setup = root / "setup.cf"
            setup.write_bytes(
                b"# comment\nMAXLEVEL=140 # capped\n"
                b"itemset3file=data/itemset.txt\n"
                b"itemset6file=data\\itemset.txt\n"
            )
            self.assertEqual(_configured_maxlevel(setup), 140)
            paths = _configured_itemset_paths(setup, data)
            self.assertEqual(paths, (data / "itemset.txt",))
            self.assertEqual(_item_ids(paths), frozenset({7, 19}))

    @patch(
        "tools.stoneage_shadowed_branch_warpman_satisfiability_probe."
        "load_ordered_runtime_reachability",
        return_value=_Reachability(),
    )
    def test_end_to_end_domain_witness_omits_operand_values(
        self,
        _runtime,
    ):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc, setup, data = _fixture(
                root,
                b"LV>10&ITEM=20&ITEM<30",
            )
            audit = analyze(npc, setup, data)
            self.assertEqual(len(audit.rows), 1)
            self.assertTrue(audit.rows[0].satisfiable)
            self.assertEqual(audit.counts["atoms"], 3)
            self.assertEqual(audit.counts["unsupported_atoms"], 0)

            buffer = io.StringIO()
            with redirect_stdout(buffer):
                emit(audit)
            report = buffer.getvalue()
            self.assertIn("domain_satisfiable=1", report)
            self.assertIn("key=LV|operator=>", report)
            self.assertIn("key=ITEM|operator==", report)
            self.assertNotIn("operand=", report)
            self.assertNotIn("ITEM=20", report)
            self.assertNotIn("LV>10", report)

    @patch(
        "tools.stoneage_shadowed_branch_warpman_satisfiability_probe."
        "load_ordered_runtime_reachability",
        return_value=_Reachability(),
    )
    def test_missing_catalog_witness_keeps_route_unproven(
        self,
        _runtime,
    ):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc, setup, data = _fixture(root, b"ITEM=999")
            audit = analyze(npc, setup, data)
            self.assertFalse(audit.rows[0].satisfiable)
            self.assertEqual(audit.counts["atoms_without_domain_witness"], 1)


if __name__ == "__main__":
    unittest.main()
