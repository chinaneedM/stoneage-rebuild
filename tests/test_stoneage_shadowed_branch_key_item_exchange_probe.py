import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.stoneage_shadowed_branch_key_item_exchange_probe import (
    _event_atom,
    _item_terms,
    _record_award,
    analyze,
)


class _Reach:
    reached_floor_ids=frozenset({100,811})


class ExchangeProbeTests(unittest.TestCase):

    def test_item_terms_support_quantity_syntax(self):
        self.assertEqual(_item_terms(b"20,30*2"),((20,1),(30,2)))

    def test_event_atom_classifies_item_quantity_requirement(self):
        self.assertEqual(_event_atom(b"ITEM=20*2"),("ITEM","=",20))
        self.assertEqual(_event_atom(b"LV>10"),("LV",">",10))

    def test_record_award_separates_target_from_other_prerequisites(self):
        record=(
            b"TYPE:ACCEPT|EVENT:LV>10&ITEM=30*2|"
            b"DelItem:40*1|GetItem:20,50|EventNo:9|ThanksMsg:x"
        )
        row=_record_award(record,20,100)
        self.assertIsNotNone(row)
        self.assertFalse(row.target_required_by_event)
        self.assertFalse(row.target_deleted)
        self.assertEqual(row.other_item_prerequisite_refs,2)
        self.assertEqual(row.other_item_reward_refs,1)
        self.assertEqual(row.event_keys,("ITEM","LV"))

    @patch(
        "tools.stoneage_shadowed_branch_key_item_exchange_probe."
        "_locate_key_item",
        return_value=(20,0),
    )
    @patch(
        "tools.stoneage_shadowed_branch_key_item_exchange_probe."
        "load_ordered_runtime_reachability",
        return_value=_Reach(),
    )
    def test_analyze_finds_reachable_exchange_award(self,_reach,_key):
        with tempfile.TemporaryDirectory() as td:
            npc=Path(td)
            (npc/"templates").write_bytes(
                b"NPCTEMPLATE\n"
                b"{\nTemplateName=X\nFunctionSet=ExChangeMan\n}\n"
            )
            (npc/"creates").write_bytes(
                b"NPCCREATE\n"
                b"{\nFloorId=100\nBornCenter=1,1\n"
                b"Enemy=X|file:x.arg\n}\n"
            )
            (npc/"x.arg").write_bytes(
                b"EventEnd|TYPE:ACCEPT|EVENT:LV>1|GetItem:20|"
                b"EventNo:1|ThanksMsg:x|EventEnd"
            )
            audit=analyze(npc)
            self.assertEqual(audit.matching_create_rows,1)
            self.assertEqual(len(audit.awards),1)
            self.assertEqual(audit.awards[0].floor_id,100)


if __name__=="__main__":
    unittest.main()
