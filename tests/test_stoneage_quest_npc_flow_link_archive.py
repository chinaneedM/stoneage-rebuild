"""Independent archival replay of source-tested anonymous same-EventEnd joins."""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import unittest

from tools.stoneage_quest_npc_flow_link_probe import (
    git_blob, validate_report, TARGET_IDS, PREVIOUS_BLOB,
)

REPORT = Path("research/recovered/STONEAGE-QUEST-NPC-FLOW-CI-DERIVED-R1.json")
RECEIPT = Path("research/recovered/STONEAGE-QUEST-NPC-FLOW-ACCEPTANCE-R1.json")
PREVIOUS = Path("research/recovered/STONEAGE-QUEST-NPC-ITEM-CI-DERIVED-R1.json")
PROBE = Path("tools/stoneage_quest_npc_flow_link_probe.py")


class QuestNpcFlowArchiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = REPORT.read_bytes()
        cls.data = json.loads(cls.raw)
        cls.receipt = json.loads(RECEIPT.read_bytes())
        cls.previous = json.loads(PREVIOUS.read_bytes())

    def test_raw_bytes_hash_and_permanent_git_blob(self):
        receipt = self.receipt
        self.assertEqual(len(self.raw), receipt["raw_json_bytes"])
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), receipt["raw_json_sha256"])
        self.assertEqual(git_blob(self.raw), receipt["permanent_git_blob"])
        self.assertTrue(receipt["raw_json_byte_equal_to_artifact_member"])
        self.assertTrue(receipt["zip_sha256_verified_independently"])

    def test_source_tested_extractor_and_previous_evidence(self):
        self.assertEqual(git_blob(PROBE.read_bytes()), self.receipt["extractor_git_blob"])
        self.assertEqual(git_blob(PREVIOUS.read_bytes()), PREVIOUS_BLOB)
        self.assertEqual(self.receipt["source_bundle_sha256"], self.data["source_bundle_sha256"])

    def test_role_ledger_is_exactly_previous_49(self):
        self.assertTrue(validate_report(self.data))
        actual = Counter()
        for row in self.data["same_eventend_records"]:
            for pair in row["item_role_pairs"]:
                actual[(pair["item_id"], pair["role"])] += row["placement_instances"]
        previous = Counter()
        for row in self.previous["typed_reference_classes"]:
            previous[(row["item_id"], row["role"])] += row["occurrences"]
        self.assertEqual(actual, previous)
        self.assertEqual(sum(actual.values()), 49)
        self.assertEqual(set(self.data["target_ids"]), set(TARGET_IDS))

    def test_no_execution_early_server_or_new_game_promotion(self):
        for key in ("original_taiwan_v1_binding_proven", "original_server_executed",
                    "full_npc_or_dialogue_recovered", "runtime_code_changed", "stage_a_accepted"):
            self.assertIs(self.data[key], False)
        self.assertEqual(self.data["stage_b_gate"], "GATED")

    def test_mutated_role_or_count_rejected(self):
        data = copy.deepcopy(self.data)
        data["counts"]["typed_field_occurrences"] += 1
        with self.assertRaises(ValueError):
            validate_report(data)
        if self.data["same_eventend_records"]:
            data = copy.deepcopy(self.data)
            data["same_eventend_records"][0]["item_role_pairs"][0]["item_id"] = 19999
            with self.assertRaises(ValueError):
                validate_report(data)

    def test_anti_false_closure_receipt(self):
        self.assertEqual(self.receipt["status"], "SOURCE_BOUNDED_ONLY")
        self.assertTrue(self.receipt["original_client_server_data_not_committed"])
        self.assertFalse(self.receipt["historical_transaction_replayed"])
        self.assertFalse(self.receipt["taiwan_v1_original_id_recovered"])


if __name__ == "__main__":
    unittest.main()
