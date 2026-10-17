"""Permanent, source-bounded Quest NPC item metadata acceptance gates."""
import copy
import hashlib
import json
from pathlib import Path
import unittest

from tools.stoneage_quest_npc_item_binding_probe import validate_output, TARGET_IDS

SOURCE = Path("tools/stoneage_quest_npc_item_binding_probe.py")
REPORT = Path("research/recovered/STONEAGE-QUEST-NPC-ITEM-CI-DERIVED-R1.json")
RECEIPT = Path("research/recovered/STONEAGE-QUEST-NPC-ITEM-ACCEPTANCE-R1.json")


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class QuestNpcItemArchiveAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = REPORT.read_bytes()
        cls.data = json.loads(cls.raw)
        cls.receipt = json.loads(RECEIPT.read_bytes())

    def test_fixed_source_extractor_hash(self):
        self.assertEqual(git_blob(SOURCE.read_bytes()), self.receipt["source_probe_blob"])
        self.assertEqual(self.receipt["source_head"], "c4474916add4ed3d4e867ba13d14c47e76dca86b")

    def test_raw_archive_byte_identity(self):
        self.assertEqual(len(self.raw), self.receipt["raw_bytes"])
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), self.receipt["raw_sha256"])
        self.assertEqual(git_blob(self.raw), self.receipt["permanent_git_blob"])
        self.assertTrue(self.receipt["independently_downloaded_artifact_zip_and_compared_raw_member"])
        self.assertTrue(self.receipt["exact_archive_raw_git_blob_identity"])

    def test_bounded_semantic_replay(self):
        self.assertTrue(validate_output(self.data))
        self.assertEqual(self.data["target_ids"], list(TARGET_IDS))
        self.assertEqual(self.data["counts"]["typed_item_field_occurrences"], 49)
        self.assertEqual(sum(x["occurrences"] for x in self.data["typed_reference_classes"]), 49)
        self.assertEqual(len(self.data["typed_reference_classes"]), 10)
        self.assertFalse(any(x["item_id"] == 20197 for x in self.data["typed_reference_classes"]))
        self.assertEqual(self.data["coverage_limits"]["missing_argument_files"], 15)
        self.assertEqual(self.data["coverage_limits"]["ambiguous_templates"], 30)
        self.assertFalse(self.data["original_taiwan_1_0_npc_binding_proven"])

    def test_evidence_promotion_mutation_rejected(self):
        copy_data = copy.deepcopy(self.data)
        copy_data["actual_reward_or_removal_execution_proven"] = True
        with self.assertRaises(ValueError):
            validate_output(copy_data)

    def test_wrong_item_role_mutation_rejected(self):
        copy_data = copy.deepcopy(self.data)
        copy_data["typed_reference_classes"][0]["item_id"] = 20198
        with self.assertRaises(ValueError):
            validate_output(copy_data)
        copy_data = copy.deepcopy(self.data)
        copy_data["typed_reference_classes"][0]["role"] = "ORIGINAL_SERVER_EXECUTED"
        with self.assertRaises(ValueError):
            validate_output(copy_data)


if __name__ == "__main__":
    unittest.main()
