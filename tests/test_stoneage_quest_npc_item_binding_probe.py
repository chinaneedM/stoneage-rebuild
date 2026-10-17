"""Synthetic grammar and evidence-promotion guards for bounded NPC item binding."""
from __future__ import annotations
import json
from pathlib import Path
import tempfile
import unittest

from tools.stoneage_quest_npc_item_binding_probe import (
    TARGET_IDS, analyze, argument_bytes, event_items, exact_items,
    semantic_hits, validate_output,
)

ITEM = Path("research/recovered/STONEAGE-QUEST-ITEM-CI-DERIVED-R1.json")


class QuestNpcItemBindingTests(unittest.TestCase):
    def test_exact_item_tokens_only(self):
        self.assertEqual(exact_items(b"2465,2478*2,2481"), {2465, 2478, 2481})
        self.assertEqual(exact_items(b"12465,24650,-2465,2465junk,other2465"), set())

    def test_event_grammar_and_free_are_not_awards(self):
        self.assertEqual(event_items(b"LV>20&ITEM=2478,FREE=2465&ITEM!=20197"), {2478, 20197})
        self.assertEqual(event_items(b"FREE=2465,STUFF2465=1,ITEM=2465suffix"), set())

    def test_exchangeman_direction_and_predicate_are_separate(self):
        hits = {(item, role) for item, role, _ in semantic_hits(
            "ExChangeMan", b"GetItem:2465|DelItem:2478|EVENT:ITEM=2478&LV>20|EventEnd"
        )}
        self.assertEqual(hits, {
            (2465, "EXCHANGE_GET_CANDIDATE"),
            (2478, "EXCHANGE_DEL_CANDIDATE"),
            (2478, "EXCHANGE_ITEM_PREDICATE"),
        })

    def test_itemshop_never_promoted_to_quest_reward(self):
        hits = {(i, r) for i, r, _ in semantic_hits("ItemShop", b"GetItem:2465|ITEM:2478|FREE:2481")}
        self.assertNotIn((2465, "EXCHANGE_GET_CANDIDATE"), hits)
        self.assertEqual(hits, {(2465, "STRUCTURED_FIELD_UNQUALIFIED"), (2478, "ITEMSHOP_CATALOG_ONLY")})

    def test_action_only_fixed_descendant_candidate(self):
        self.assertEqual(
            [(i, r) for i, r, _ in semantic_hits("WarpMan", b"AddItem:2481")],
            [(2481, "ACTION_ADDITEM_CANDIDATE")],
        )
        self.assertEqual(
            [(i, r) for i, r, _ in semantic_hits("AlienFunction", b"AddItem:2481")],
            [(2481, "STRUCTURED_FIELD_UNQUALIFIED")],
        )

    def test_missing_and_unsafe_files_are_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(argument_bytes(root, b"file:missing.txt")[1], "MISSING_FILE")
            self.assertEqual(argument_bytes(root, b"file:../escape.txt")[1], "UNSAFE_PATH")
            self.assertEqual(argument_bytes(root, b"GetItem:2465"), (b"GetItem:2465", "INLINE"))

    def test_archived_candidate_contract_fixes_five_ids(self):
        report = json.loads(ITEM.read_text(encoding="utf-8"))
        from tools.stoneage_quest_npc_item_binding_probe import validate_candidate_report
        validate_candidate_report(report)
        self.assertEqual(len(TARGET_IDS), 5)

    def test_synthetic_npc_reference_join(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "template.npc").write_bytes(
                b"NPCTEMPLATE\n{\ntemplatename=TX\nfunctionset=ExChangeMan\n}\n"
                b"{\ntemplatename=SHOP\nfunctionset=ItemShop\n}\n"
            )
            (root / "create.npc").write_bytes(
                b"NPCCREATE\n{\nenemy=TX|GetItem:2465|DelItem:2478|EVENT:ITEM=2478|EventEnd\n"
                b"enemy=SHOP|item:20197\n}\n"
            )
            report = json.loads(ITEM.read_text(encoding="utf-8"))
            out = analyze(root, report)
            self.assertTrue(validate_output(out))
            rows = {(x["item_id"], x["role"]) for x in out["typed_reference_classes"]}
            self.assertIn((2465, "EXCHANGE_GET_CANDIDATE"), rows)
            self.assertIn((2478, "EXCHANGE_DEL_CANDIDATE"), rows)
            self.assertIn((20197, "ITEMSHOP_CATALOG_ONLY"), rows)
            self.assertFalse(out["original_taiwan_1_0_npc_binding_proven"])

    def test_promotion_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = json.loads(ITEM.read_text(encoding="utf-8"))
            out = analyze(root, report)
            out["actual_reward_or_removal_execution_proven"] = True
            with self.assertRaises(ValueError):
                validate_output(out)


if __name__ == "__main__":
    unittest.main()
