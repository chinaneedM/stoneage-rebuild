import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from tools.stoneage_shadowed_branch_item_shop_acquisition_probe import (
    _shop_item_visibility,
    analyze,
    emit,
)


class _Orphan:
    def __init__(self, floor_id):
        self.floor_id = floor_id


class _Reachability:
    reached_floor_ids = frozenset({811, 1000})
    orphan_rows = (_Orphan(820),)


def _item_row(item_id: int) -> bytes:
    fields = [b""] * 17
    fields[16] = str(item_id).encode("ascii")
    return b",".join(fields)


def _fixture(root: Path, *, shop_list: bytes) -> tuple[Path, Path, Path]:
    data = root / "data"
    npc = data / "npc"
    npc.mkdir(parents=True)

    (npc / "templates").write_bytes(
        b"NPCTEMPLATE\n"
        b"{\nTemplateName=W\nFunctionSet=WarpMan\n}\n"
        b"{\nTemplateName=S\nFunctionSet=ItemShop\n}\n"
    )
    (npc / "creates").write_bytes(
        b"NPCCREATE\n"
        b"{\nFloorId=811\nBornCenter=1,1\nEnemy=W|file:w.arg\n}\n"
        b"{\nFloorId=1000\nBornCenter=2,2\nEnemy=S|file:s.arg\n}\n"
    )
    (npc / "w.arg").write_bytes(
        b"WARP:820,1,1|FREE:LV>10&LV<100&ITEM=20|PayMsg:x|MONEY:-1\n"
    )
    (npc / "s.arg").write_bytes(
        b"ItemList:" + shop_list + b"|buy_rate:1.0|main_msg:x\n"
    )

    (data / "itemset.txt").write_bytes(
        b"\n".join(_item_row(i) for i in range(1, 50)) + b"\n"
    )
    setup = root / "setup.cf"
    setup.write_bytes(
        b"MAXLEVEL=140\nitemset3file=data/itemset.txt\n"
    )
    return npc, setup, data


class ShadowedBranchItemShopAuditTests(unittest.TestCase):

    def test_item_list_range_and_33_entry_truncation(self):
        catalog = frozenset(range(1, 50))
        listed, visible, rank = _shop_item_visibility(
            b"1-40",
            20,
            catalog,
        )
        self.assertTrue(listed)
        self.assertTrue(visible)
        self.assertEqual(rank, 20)

        listed, visible, rank = _shop_item_visibility(
            b"1-40",
            35,
            catalog,
        )
        self.assertTrue(listed)
        self.assertFalse(visible)
        self.assertIsNone(rank)

    def test_undefined_items_do_not_consume_shop_slots(self):
        catalog = frozenset({10, 20, 30})
        listed, visible, rank = _shop_item_visibility(
            b"1-100",
            30,
            catalog,
        )
        self.assertTrue(listed)
        self.assertTrue(visible)
        self.assertEqual(rank, 3)

    @patch(
        "tools.stoneage_shadowed_branch_item_shop_acquisition_probe."
        "load_ordered_runtime_reachability",
        return_value=_Reachability(),
    )
    def test_reachable_shop_witness_is_reported_without_item_id(
        self,
        _runtime,
    ):
        with tempfile.TemporaryDirectory() as td:
            npc, setup, data = _fixture(Path(td), shop_list=b"10,15-25")
            audit = analyze(npc, setup, data)
            self.assertEqual(audit.counts["target_visible_shops"], 1)
            self.assertEqual(audit.counts["target_listed_shops"], 1)

            buffer = io.StringIO()
            with redirect_stdout(buffer):
                emit(audit)
            report = buffer.getvalue()
            self.assertIn("normal_purchase_surface=1", report)
            self.assertIn("item_id_withheld=1", report)
            self.assertNotIn("ITEM=20", report)
            self.assertNotIn("item_id=20", report)
            self.assertNotIn("15-25", report)

    @patch(
        "tools.stoneage_shadowed_branch_item_shop_acquisition_probe."
        "load_ordered_runtime_world_reachability",
        create=True,
    )
    def test_placeholder(self, _unused):
        # Keep unittest discovery explicit; semantic coverage is above.
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
