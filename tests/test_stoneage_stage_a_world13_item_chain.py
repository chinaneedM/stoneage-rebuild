"""WORLD13: source-derived two-script item graph, preservation and evidence limits."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1] / "research" / "recovered"
NAMES = ["sainasu/event/nevent01_2", "sainasu/event/nevent01_1"]


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


class TwoScriptItemChain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = load("STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json")
        cls.report = load("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-13-TWO-SCRIPT-ITEM-CHAIN-R1.json")
        cls.items = {}
        for shard in range(1, 8):
            source = load(f"item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{shard:02d}-R1.json")
            for row in source["rows"]:
                self_id = row[0]
                if self_id in cls.items:
                    raise AssertionError(f"duplicate item id {self_id}")
                cls.items[self_id] = row

    def test_exact_source_create_and_condition_provenance(self):
        old = self.old
        for source in self.report["sources"]:
            path = source["path"]
            manifest, = [x for x in old["source_scripts"] if x["path"] == path]
            for old_key, new_key in (("original_size", "original_size"), ("original_sha256", "original_sha256"),
                                     ("original_crc32", "original_crc32"), ("source_control_lines", "source_control_lines"),
                                     ("quest_origin", "origin")):
                self.assertEqual(source[new_key], manifest[old_key])
            creates = [x for x in old["source_creation_references"] if x["original_script_path"] == path]
            expected_creates = [{k: x[k] for k in ("create_source_path", "create_source_sha",
                               "create_brace_ordinal", "floorid", "borncenter_numeric", "graphic_alias_numeric")}
                                for x in creates]
            self.assertEqual(source["create_references"], expected_creates)
            blocks = [x for x in old["source_event_blocks"] if x["script_path"] == path]
            expected_blocks = [{
                "ordinal": b["script_block_ordinal"], "type": b["raw_type"],
                "event_number": b["event_number"], "source_type_line": b["source_type_line"],
                "source_section_sha256": b["source_section_decoded_cp950_normalized_UTF8_sha256"],
                "condition_sha256": b["condition_expression_decoded_cp950_UTF8_sha256"],
                "condition_keywords": b["condition_keywords"],
                "predicate_item_ids": b["item_numeric_refs"].get("predicate_ITEM", []),
                "del_item_ids": b["item_numeric_refs"].get("DelItem", []),
                "get_item_ids": b["item_numeric_refs"].get("GetItem", []),
            } for b in blocks]
            self.assertEqual(source["blocks"], expected_blocks)
        self.assertEqual([s["path"] for s in self.report["sources"]], NAMES)

    def test_actual_cross_script_ID_positions_and_negative_npc_position(self):
        first, second = self.report["sources"]
        get = lambda s: sorted({i for b in s["blocks"] for i in b["get_item_ids"]})
        delete = lambda s: sorted({i for b in s["blocks"] for i in b["del_item_ids"]})
        self.assertEqual(delete(first), self.report["initial_item_ids"])
        self.assertEqual(get(first), self.report["intermediate_item_ids"])
        self.assertEqual(delete(second), self.report["intermediate_item_ids"])
        self.assertEqual(get(second), self.report["final_output_item_ids"])
        self.assertEqual(delete(first), list(range(2569, 2575)))
        self.assertEqual(get(first), [2432, 2433, 2434])
        self.assertEqual(get(second), [2435, 2436, 2437, 11863, 11872, 11873, 11874])
        for row in self.report["bridge_links"]:
            self.assertEqual(row["producer_script"], first["path"])
            self.assertEqual(row["consumer_script"], second["path"])
            item = row["item_id"]
            self.assertEqual(row["producer_block_ordinals"],
                             [b["ordinal"] for b in first["blocks"] if item in b["get_item_ids"]])
            self.assertEqual(row["consumer_block_ordinals"],
                             [b["ordinal"] for b in second["blocks"] if item in b["del_item_ids"]])
        self.assertEqual([r["item_id"] for r in self.report["bridge_links"]], [2432, 2433, 2434])
        self.assertEqual({r["floorid"] for s in self.report["sources"] for r in s["create_references"]},
                         {2000, 4000})
        self.assertTrue(all(r["borncenter_numeric"] is None for s in self.report["sources"] for r in s["create_references"]))

    def test_item_row_SHA_graphic_alias_and_qualifier_exact(self):
        idset = sorted(set(self.report["initial_item_ids"] + self.report["intermediate_item_ids"]
                           + self.report["final_output_item_ids"]))
        self.assertEqual([r["id"] for r in self.report["item_rows"]], idset)
        for r in self.report["item_rows"]:
            row = self.items[r["id"]]
            for k, v in (("source_a_complete_row_sha256", row[1]),
                         ("source_b_complete_row_sha256", row[2]),
                         ("source_a_image_alias", row[3]), ("source_b_image_alias", row[4]),
                         ("source_a_TW1_RD_qualification", row[8]),
                         ("source_b_TW1_RD_qualification", row[9]),
                         ("cross_table_changed_column_positions", row[10])):
                self.assertEqual(r[k], v)
            self.assertEqual(row[1], row[2])
            self.assertEqual(row[3], row[4])
            self.assertEqual(row[9], "REAL_RD_DECODED_CROSS_CARRIER")
            self.assertEqual(row[10], [])
        self.assertEqual(len(idset), 16)

    def test_counts_and_no_premature_official_or_gameplay_claims(self):
        s = self.report["sources"]
        b = [a for x in s for a in x["blocks"]]
        expected = dict(script_files=len(s), create_references=sum(len(x["create_references"]) for x in s),
                        source_control_blocks=len(b), accept_blocks=sum(x["type"] == "ACCEPT" for x in b),
                        message_blocks=sum(x["type"] == "MESSAGE" for x in b),
                        del_item_positions=sum(len(x["del_item_ids"]) for x in b),
                        get_item_positions=sum(len(x["get_item_ids"]) for x in b),
                        input_distinct_ids=len(self.report["initial_item_ids"]),
                        bridge_distinct_ids=len(self.report["intermediate_item_ids"]),
                        final_output_distinct_ids=len(self.report["final_output_item_ids"]),
                        all_distinct_item_ids=len(self.report["item_rows"]),
                        distinct_item_image_aliases=len({r["source_b_image_alias"] for r in self.report["item_rows"]}),
                        qualified_RD_candidates=sum(r["source_b_TW1_RD_qualification"] == "REAL_RD_DECODED_CROSS_CARRIER"
                                                    for r in self.report["item_rows"]))
        self.assertEqual(self.report["counts"], expected)
        self.assertEqual((expected["source_control_blocks"], expected["accept_blocks"], expected["message_blocks"]),
                         (13, 12, 1))
        self.assertTrue(all(x["origin"] == "UNRESOLVED" for x in s))
        guards = self.report["qualification"]
        self.assertTrue(all(v is True for k, v in guards.items()
                            if k not in ("original_asset_or_script_text_published",
                                         "original_archive_reopened_this_turn", "native_game_executed")))
        self.assertFalse(any(guards[k] for k in ("original_asset_or_script_text_published",
                                                "original_archive_reopened_this_turn", "native_game_executed")))
        self.assertEqual(self.report["continuity"]["preserved_current_blob"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual((self.report["stage_A"], self.report["stage_B"], self.report["wiki"], self.report["R79"]),
                         ("7_PARTIAL_2_OPEN", "GATED", "GATED", "PAUSED_NON_BLOCKING"))
        self.assertIsNone(self.report["overall_percent"])


if __name__ == "__main__":
    unittest.main()
