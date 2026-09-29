import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.stoneage_shadowed_branch_key_item_nonshop_probe import (
    _drop_witnesses,
    _group_gate_class,
    _npc_reward_witnesses,
    analyze,
)


class _Reachability:
    reached_floor_ids = frozenset({100, 811})


def _encount_row(floor=100, group_id=500, weight=100):
    vals=[1,floor,0,0,10,10,1,10,5,1]
    vals += [group_id] + [-1]*9
    vals += [weight] + [-1]*9
    vals += [0,0,0]
    return ",".join(map(str,vals))


def _group_row(
    group_id=500,
    appear=-1,
    notappear=-1,
    enemy_id=700,
    weight=100,
):
    vals=[group_id,appear,notappear]
    vals += [enemy_id]+[-1]*9
    vals += [weight]+[-1]*9
    return "G,"+",".join(map(str,vals))


def _enemy_row(enemy_id=700,target=20,prob=125):
    nums=[
        enemy_id, 900, 1, 5, 1, 1, 0, 10, 0, 0, 1,
    ]
    nums += [target]+[-1]*9
    nums += [prob]+[0]*9
    return "E,S,W,"+",".join(map(str,nums))


def _item_row(item_id):
    fields=[b""]*94
    fields[16]=str(item_id).encode()
    return b",".join(fields)


def _data_fixture(root, *, appear=-1, notappear=-1):
    data=root/"data"; data.mkdir()
    (data/"encount.txt").write_text(_encount_row()+"\n",encoding="ascii")
    (data/"group.txt").write_text(
        _group_row(appear=appear,notappear=notappear)+"\n",
        encoding="ascii",
    )
    (data/"enemy.txt").write_text(_enemy_row()+"\n",encoding="ascii")
    # Minimal enemybase file: the existing chain analyzer tolerates the active
    # item/drop join even when enemybase probing has no useful rows.
    (data/"enemybase.txt").write_text("",encoding="ascii")
    (data/"itemset.txt").write_bytes(_item_row(20)+b"\n")
    setup=root/"setup.cf"
    setup.write_text(
        "encountfile=data/encount.txt\n"
        "groupfile=data/group.txt\n"
        "enemyfile=data/enemy.txt\n"
        "enemybasefile=data/enemybase.txt\n"
        "itemset3file=data/itemset.txt\n",
        encoding="ascii",
    )
    return data,setup


class KeyItemNonshopProbeTests(unittest.TestCase):

    def test_group_gate_class_separates_circular_and_non_circular(self):
        self.assertEqual(_group_gate_class(-1,-1,20),"UNGATED")
        self.assertEqual(
            _group_gate_class(20,-1,20),
            "CIRCULAR_REQUIRES_TARGET",
        )
        self.assertEqual(
            _group_gate_class(-1,20,20),
            "TARGET_ABSENCE_ALLOWED",
        )
        self.assertEqual(
            _group_gate_class(30,-1,20),
            "REQUIRES_OTHER_ITEM",
        )

    def test_reachable_positive_drop_chain_is_a_witness(self):
        with tempfile.TemporaryDirectory() as td:
            data,setup=_data_fixture(Path(td))
            rows=_drop_witnesses(
                data_dir=data,
                setup=setup,
                target_item=20,
                reached_floors={100},
            )
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0].floor_id,100)
            self.assertEqual(rows[0].group_gate_class,"UNGATED")
            self.assertEqual(rows[0].probability_class,"POSITIVE")

    def test_circular_group_gate_is_preserved(self):
        with tempfile.TemporaryDirectory() as td:
            data,setup=_data_fixture(Path(td),appear=20)
            rows=_drop_witnesses(
                data_dir=data,
                setup=setup,
                target_item=20,
                reached_floors={100},
            )
            self.assertEqual(len(rows),1)
            self.assertEqual(
                rows[0].group_gate_class,
                "CIRCULAR_REQUIRES_TARGET",
            )

    def test_reachable_additem_is_joined_to_action_run_function_set(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            npc=root/"npc"; npc.mkdir()
            (npc/"templates").write_bytes(
                b"NPCTEMPLATE\n"
                b"{\nTemplateName=R\nFunctionSet=MakePair\n}\n"
            )
            (npc/"creates").write_bytes(
                b"NPCCREATE\n"
                b"{\nFloorId=100\nBornCenter=1,1\n"
                b"Enemy=R|file:r.arg\n}\n"
            )
            (npc/"r.arg").write_bytes(
                b"FREE:LV>1|AddItem:20,30|FreeMsg:x\n"
            )
            rows,hits,missing=_npc_reward_witnesses(
                npc_dir=npc,
                target_item=20,
                reached_floors={100},
            )
            self.assertEqual(missing,0)
            self.assertEqual(hits,1)
            self.assertEqual(len(rows),1)
            self.assertTrue(rows[0].action_run_covered)
            self.assertEqual(rows[0].function_set,"makepair")

    @patch(
        "tools.stoneage_shadowed_branch_key_item_nonshop_probe."
        "load_ordered_runtime_reachability",
        return_value=_Reachability(),
    )
    @patch(
        "tools.stoneage_shadowed_branch_key_item_nonshop_probe."
        "_locate_key_item",
        return_value=(20,0),
    )
    def test_analyze_combines_drop_and_reward_surfaces(
        self,
        _key,
        _reachability,
    ):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            data,setup=_data_fixture(root)
            npc=data/"npc"; npc.mkdir()
            (npc/"templates").write_bytes(
                b"NPCTEMPLATE\n"
                b"{\nTemplateName=R\nFunctionSet=MakePair\n}\n"
            )
            (npc/"creates").write_bytes(
                b"NPCCREATE\n"
                b"{\nFloorId=100\nBornCenter=1,1\n"
                b"Enemy=R|file:r.arg\n}\n"
            )
            (npc/"r.arg").write_bytes(b"AddItem:20\n")
            audit=analyze(npc,setup,data)
            self.assertEqual(audit.counts["drop_witnesses"],1)
            self.assertEqual(audit.counts["npc_reward_witnesses"],1)
            self.assertEqual(
                audit.counts["npc_action_run_covered_witnesses"],
                1,
            )


if __name__=="__main__":
    unittest.main()
