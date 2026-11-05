"""Frozen WORLD09 projection and separate later C evidence.

WORLD23 establishes that the old catalog deduplicated/reordered raw fields.
These archived 718 references are not literal positions or original order;
the corrected source-position tests live in WORLD23. Preserve the old receipt.
"""
from pathlib import Path
import hashlib
import json
import os
import unittest

ROOT = Path(__file__).resolve().parents[1] / "research" / "recovered"
SOURCE = "STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json"
OUTPUT = "STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-09-GETRANDITEM-SOURCE-SLOTS-R1.json"
BLOB = "7a9cc7ea6d76bfdae367c580db4ce6fcb42d7d15"


def load(filename):
    return json.loads((ROOT / filename).read_text(encoding="utf-8"))


class World09RandomItem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = load(SOURCE)
        cls.new = load(OUTPUT)

    def test_frozen_50_block_projection_and_archive_shas(self):
        rows = [x for x in self.old["source_event_blocks"] if x["source_operations"].get("GetRandItem")]
        expected = [{
            "script_path": x["script_path"],
            "source_file_sha256": x["source_file_sha"],
            "block_ordinal": x["script_block_ordinal"],
            "type_line": x["source_type_line"],
            "source_section_sha256": x["source_section_decoded_cp950_normalized_UTF8_sha256"],
            "source_type": x["raw_type"],
            "original_item_candidates_ordered": x["item_numeric_refs"]["GetRandItem"],
            "quest_origin": x["origin_class"],
        } for x in rows]
        self.assertEqual(self.new["original_getranditem_blocks"], expected)
        self.assertEqual(len(expected), 50)
        self.assertEqual(len({x["script_path"] for x in expected}), 33)
        self.assertEqual(sum(len(x["original_item_candidates_ordered"]) for x in expected), 718)
        self.assertEqual(len({v for x in expected for v in x["original_item_candidates_ordered"]}), 328)
        self.assertEqual((sum(x["source_type"] == "ACCEPT" for x in expected), sum(x["source_type"] == "MESSAGE" for x in expected)), (46, 4))
        self.assertTrue(all(x["quest_origin"] == "UNRESOLVED" for x in expected))
        self.assertTrue(all(len(x["original_item_candidates_ordered"]) == len(set(x["original_item_candidates_ordered"])) > 0 for x in expected))
        self.assertTrue(all("GetItem" not in x["source_operations"] for x in rows))

    def test_itemset_presence_and_provenance_guards(self):
        ids = {v for x in self.new["original_getranditem_blocks"] for v in x["original_item_candidates_ordered"]}
        scope = self.old["item_references_from_parsed_event_blocks"]
        self.assertTrue(ids.issubset(set(scope["both_tables"])))
        self.assertEqual(self.new["counts"]["distinct_IDs_in_both_original_candidate_itemsets"], 328)
        self.assertEqual(self.new["counts"]["distinct_IDs_in_later_only_itemset"], 0)
        self.assertEqual(self.new["counts"]["distinct_IDs_missing_both_original_candidate_itemsets"], 0)
        self.assertEqual(self.new["source_original_script_graph"]["git_blob_sha"], "52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2")
        self.assertEqual(self.new["code_static_source"]["git_blob_sha"], BLOB)
        self.assertTrue(all(self.new["bounded_uncertainties"].values()))
        self.assertEqual(self.new["stage_A"], "7_PARTIAL_2_OPEN")
        self.assertEqual((self.new["stage_B"], self.new["wiki"], self.new["R79"]), ("GATED", "GATED", "PAUSED_NON_BLOCKING"))
        self.assertIsNone(self.new["overall_percent"])
        self.assertEqual(self.new["full_historical_CURRENT_git_blob"], "c89e0e33537990aa2132b47c40fef49a985a935c")

    def test_exact_fixed_later_C_when_supplied(self):
        filename = os.environ.get("STONEAGE_WORLD09_PINNED_EXCHANGE")
        if not filename:
            self.skipTest("No pinned later C file in local workspace")
        raw = Path(filename).read_bytes()
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()
        self.assertEqual(sha, BLOB)
        s = raw.decode("latin-1")
        function = s[s.index("BOOL NPC_RandItemGet(int meidex,int talker,int rand_j,char *buf)"): ]
        for term in (
            "if(rand_j == 0)", "randitem = rand()%rand_j",
            "if(randitem == 0) randitem = rand_j",
            'getStringFromIndexWithDelim(buf , "," , randitem',
            "ITEM_makeItemAndRegist( atoi( buff2))",
            "CHAR_addItemSpecificItemIndex( talker, itemindex)",
            "ITEM_endExistItemsOne( itemindex)",
        ):
            self.assertIn(term, function)
        self.assertIn('NPC_Util_GetStrFromStrWithDelim( buff, "GetRandItem"', s)
        self.assertIn("NPC_RandItemGet( meindex, talker, rand_j,buf)", s)


if __name__ == "__main__":
    unittest.main()
