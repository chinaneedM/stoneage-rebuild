"""Synthetic, copyright-free evidence tests for private artifact custody."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from tools.stoneage_private_archive_custody import archive, load_manifest, verify_receipt, SCHEMA


class PrivateArchiveCustodyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.private = self.root / "private"
        self.private.mkdir()
        self.src = self.root / "test-source.bin"
        self.data = b"STONEAGE-TEST-ONLY" * 5 + b"\x00"
        self.src.write_bytes(self.data)
        self.input = {
            "schema": SCHEMA, "archive_id": "synthetic-test",
            "files": [{"asset_id": "synthetic-source",
                       "source_path": str(self.src),
                       "expected_bytes": len(self.data),
                       "expected_sha256": hashlib.sha256(self.data).hexdigest(),
                       "occurrences": [
                           {"sample_id": "TW10", "relative_path": "assets/a.bin"},
                           {"sample_id": "CN50", "relative_path": "assets/copy.bin"}
                       ]}]}

    def load(self, manifest=None):
        path = self.root / "input.json"
        path.write_text(json.dumps(self.input if manifest is None else manifest), encoding="utf-8")
        return load_manifest(path)

    def test_gate_and_full_readback(self):
        obj = self.load()
        with self.assertRaisesRegex(ValueError, "acknowledgement"):
            archive(obj, self.private, chunk_bytes=9)
        receipt_path = archive(obj, self.private, chunk_bytes=9, confirmed=True, max_object_bytes=9)
        receipt = json.loads(receipt_path.read_text())
        self.assertEqual(verify_receipt(self.private, receipt)["status"], "FULL_READBACK_VERIFIED")
        self.assertFalse(receipt["provider_retention_verified"])
        self.assertFalse(receipt["named_pet_npc_quest_inferred"])
        self.assertNotIn(str(self.src), receipt_path.read_text())
        self.assertEqual(len(receipt["files"][0]["occurrences"]), 2)
        self.assertGreater(len(receipt["files"][0]["parts"]), 1)
        with self.assertRaisesRegex(ValueError, "receipt already exists"):
            archive(obj, self.private, 9, True)

    def test_source_digest_mutation_rejected_without_receipt(self):
        obj = self.load()
        self.src.write_bytes(self.data + b"tamper")
        with self.assertRaisesRegex(ValueError, "original source hash/size"):
            archive(obj, self.private, 8, True)
        self.assertFalse((self.private / "receipts" / "synthetic-test.json").exists())

    def test_chunk_mutation_detected(self):
        receipt_path = archive(self.load(), self.private, 11, True)
        receipt = json.loads(receipt_path.read_text())
        first = receipt["files"][0]["parts"][0]
        obj = self.private / "objects" / first["sha256"][:2] / first["sha256"]
        obj.write_bytes(b"corruption")
        with self.assertRaisesRegex(ValueError, "part readback mismatch"):
            verify_receipt(self.private, receipt)

    def test_duplicate_content_preserves_independent_occurrences(self):
        obj = self.load()
        second = copy.deepcopy(obj["files"][0])
        second["asset_id"] = "another-id"
        second["occurrences"] = [{"sample_id": "JP", "relative_path": "other.bin"}]
        obj["files"].append(second)
        receipt = json.loads(archive(obj, self.private, 16, True).read_text())
        self.assertEqual(receipt["files"][0]["parts"], receipt["files"][1]["parts"])
        self.assertEqual(len(list((self.private / "objects").glob("*/*"))), len(set(x["sha256"] for x in receipt["files"][0]["parts"])))
        self.assertEqual(verify_receipt(self.private, receipt)["files"], 2)

    def test_manifest_traversal_and_missing_occurrences_rejected(self):
        x = copy.deepcopy(self.input)
        x["files"][0]["occurrences"][0]["relative_path"] = "../outside"
        with self.assertRaisesRegex(ValueError, "unsafe occurrence"):
            self.load(x)
        x = copy.deepcopy(self.input)
        x["files"][0]["occurrences"] = []
        with self.assertRaisesRegex(ValueError, "occurrences"):
            self.load(x)
        x = copy.deepcopy(self.input)
        x["files"].append(copy.deepcopy(x["files"][0]))
        with self.assertRaisesRegex(ValueError, "unique asset id"):
            self.load(x)

    def test_object_size_limit_and_durability_boundary(self):
        with self.assertRaisesRegex(ValueError, "object limit"):
            archive(self.load(), self.private, 20, True, max_object_bytes=8)
        receipt = json.loads(archive(self.load(), self.private, 7, True).read_text())
        receipt["provider_retention_verified"] = True
        # A local readback is still not a provider retention proof.
        self.assertFalse(verify_receipt(self.private, receipt)["provider_retention_verified"])


if __name__ == "__main__":
    unittest.main()
