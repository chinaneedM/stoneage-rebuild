"""Mutation-backed provenance and synthetic read-only digest controls."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from tools.stoneage_wayi_85_archive_chain import MANIFEST, validate, hash_local_candidate


class W85ArchiveEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_metadata_valid(self):
        self.assertEqual(len(validate(self.data)), 6)

    def test_no_fake_hash(self):
        x = copy.deepcopy(self.data)
        x["assembled_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            validate(x)

    def test_no_original_equivalence(self):
        x = copy.deepcopy(self.data)
        x["original_publisher_binary_equivalence_verified"] = True
        with self.assertRaises(ValueError):
            validate(x)

    def test_no_original_8_0_runtime(self):
        x = copy.deepcopy(self.data)
        x["authentic_pet_runtime_verified"] = True
        with self.assertRaises(ValueError):
            validate(x)

    def test_no_early_version(self):
        x = copy.deepcopy(self.data)
        x["early_jss_or_taiwan_v1_equivalence_verified"] = True
        with self.assertRaises(ValueError):
            validate(x)

    def test_duplicate_mediafire_id(self):
        x = copy.deepcopy(self.data)
        x["parts"][1]["key"] = x["parts"][0]["key"]
        with self.assertRaises(ValueError):
            validate(x)

    def test_missing_part(self):
        x = copy.deepcopy(self.data)
        x["parts"].pop()
        with self.assertRaises(ValueError):
            validate(x)

    def test_fake_byte_size(self):
        x = copy.deepcopy(self.data)
        x["parts"][0]["byte_size"] = 200000000
        with self.assertRaises(ValueError):
            validate(x)

    def test_offline_synthetic_hash_only(self):
        with tempfile.TemporaryDirectory() as d:
            cat = b""
            for item in self.data["parts"]:
                payload = ("SYNTHETIC_" + str(item["part"])).encode()
                (Path(d) / item["filename"]).write_bytes(payload)
                cat += payload
            report = hash_local_candidate(self.data, d)
            self.assertEqual(report["concatenation_sha256"], hashlib.sha256(cat).hexdigest())
            self.assertFalse(report["original_binary_equivalence_verified"])
            self.assertFalse(report["runtime_verified"])

    def test_local_missing_part_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            for item in self.data["parts"][:-1]:
                (Path(d) / item["filename"]).write_bytes(b"a")
            with self.assertRaisesRegex(ValueError, "Missing"):
                hash_local_candidate(self.data, d)


if __name__ == "__main__":
    unittest.main()
