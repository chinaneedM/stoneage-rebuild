"""Evidence-bounded same-EventEnd join tests: no cross-event inference."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import tempfile
import unittest

from tools.stoneage_quest_npc_flow_link_probe import (
    aggregate, event_record_roles, validate_report, git_blob, PREVIOUS_BLOB,
)


def fixture(root: Path, records: bytes):
    (root/"template.npc").write_bytes(
        b"NPCTEMPLATE\n{\ntemplatename=E\nfunctionset=ExChangeMan\n}\n"
    )
    (root/"create.npc").write_bytes(
        b"NPCCREATE\n{\nenemy=E|" + records + b"\n}\n"
    )


class SameEventEndTests(unittest.TestCase):
    def test_mixed_item_actions_have_single_record_witness(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            fixture(root,b"GetItem:2465|DelItem:2478|EVENT:ITEM=2478&LV>30|EventEnd")
            a=aggregate(root)
            self.assertTrue(validate_report(a))
            self.assertEqual(a["counts"]["typed_field_occurrences"],3)
            self.assertEqual(a["counts"]["same_record_multi_item_patterns"],1)
            self.assertEqual(a["counts"]["same_record_multi_role_patterns"],1)
            roles={(p["item_id"],p["role"]) for p in a["same_eventend_records"][0]["item_role_pairs"]}
            self.assertEqual(roles,{(2465,"EXCHANGE_GET_CANDIDATE"),(2478,"EXCHANGE_DEL_CANDIDATE"),(2478,"EXCHANGE_ITEM_PREDICATE")})

    def test_no_cross_eventend_splicing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            fixture(root,b"GetItem:2465|EventEnd|DelItem:2478|EVENT:ITEM=2478|EventEnd")
            a=aggregate(root)
            self.assertEqual(a["counts"]["same_record_multi_item_patterns"],0)
            self.assertEqual(a["counts"]["same_record_multi_role_patterns"],1)
            self.assertEqual(a["counts"]["anonymous_typed_records"],2)

    def test_numeric_alias_and_free_not_qualified(self):
        observations=list(event_record_roles(b"GetItem:12465|DelItem:24780|FREE:2465|EVENT:LV=30|EventEnd"))
        self.assertEqual(observations,[])

    def test_repeated_same_record_counts_source_placements(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            fixture(root,b"GetItem:2481|DelItem:2478|EventEnd")
            (root/"create.npc").write_bytes(
                b"NPCCREATE\n{\nenemy=E|GetItem:2481|DelItem:2478|EventEnd\nenemy=E|GetItem:2481|DelItem:2478|EventEnd\n}\n"
            )
            a=aggregate(root)
            self.assertEqual(a["counts"]["anonymous_typed_records"],1)
            self.assertEqual(a["counts"]["typed_field_occurrences"],4)
            self.assertEqual(a["same_eventend_records"][0]["placement_instances"],2)

    def test_reject_old_ledger_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            fixture(root,b"GetItem:2465|EventEnd")
            previous=json.loads(Path("research/recovered/STONEAGE-QUEST-NPC-ITEM-CI-DERIVED-R1.json").read_bytes())
            with self.assertRaises(ValueError):
                aggregate(root,previous=previous)

    def test_reject_execution_promotion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            fixture(root,b"GetItem:2465|DelItem:2478|EventEnd")
            data=aggregate(root)
            data["original_server_executed"]=True
            with self.assertRaises(ValueError):
                validate_report(data)

    def test_reject_false_multi_item_assertion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            fixture(root,b"GetItem:2465|EventEnd")
            a=aggregate(root)
            a["same_eventend_records"][0]["multi_item_same_record"]=True
            with self.assertRaises(ValueError):
                validate_report(a)

    def test_reject_role_count_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            fixture(root,b"DelItem:2484|GetItem:2481|EventEnd")
            a=aggregate(root)
            a["counts"]["typed_field_occurrences"]+=1
            with self.assertRaises(ValueError):
                validate_report(a)

    def test_pinned_prior_derived_hash(self):
        raw=Path("research/recovered/STONEAGE-QUEST-NPC-ITEM-CI-DERIVED-R1.json").read_bytes()
        self.assertEqual(git_blob(raw), PREVIOUS_BLOB)


if __name__=="__main__":
    unittest.main()
