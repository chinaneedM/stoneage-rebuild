"""Positive safe-inspection plus negative false-provenance regression gates."""
import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from tools.stoneage_late_client_archive_probe import (
    LEDGER_PATH, _zip_unsafe, inspect_archive, validate_ledger,
)

class SourceOnlyClientCandidateGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def candidate(self, data, name):
        return next(x for x in data["candidates"] if x["id"] == name)

    def test_current_ledger_is_source_only(self):
        validate_ledger(self.ledger)

    def test_cannot_promote_mainland_operator_domain_to_taiwan(self):
        data = json.loads(json.dumps(self.ledger))
        self.candidate(data, "CN-WAYI-SA8-8016")["operator_region_context"] = "TAIWAN_OPERATOR_2005"
        with self.assertRaisesRegex(ValueError, "region admission drift"):
            validate_ledger(data)

    def test_cannot_promote_8_5_install_bundle_as_8_0(self):
        data = json.loads(json.dumps(self.ledger))
        self.candidate(data, "TW-YANG-2012-SIXPART")["version_attribution"] = "TW_8_0_CONFIRMED"
        with self.assertRaises(ValueError):
            validate_ledger(data)

    def test_cannot_pretend_binary_was_obtained(self):
        data = json.loads(json.dumps(self.ledger))
        self.candidate(data, "CN-WAYI-SA8-8016")["bytes_verified"] = True
        with self.assertRaisesRegex(ValueError, "Unverified binary"):
            validate_ledger(data)

    def test_cannot_invent_sha256(self):
        data = json.loads(json.dumps(self.ledger))
        self.candidate(data, "TW-YANG-2012-SIXPART")["sha256"] = "a" * 64
        with self.assertRaisesRegex(ValueError, "Invented byte hash"):
            validate_ledger(data)

    def test_missing_sixth_volume_is_rejected(self):
        data = json.loads(json.dumps(self.ledger))
        self.candidate(data, "TW-YANG-2012-SIXPART")["historical_carriers"].pop()
        with self.assertRaisesRegex(ValueError, "multipart exclusion"):
            validate_ledger(data)

    def test_zip_path_attacks_are_detected(self):
        for s in ("/absolute/file", "../escape", "safe/../../evil", "C:/Windows/file", "C:\\Windows\\file"):
            self.assertTrue(_zip_unsafe(s), s)
        self.assertFalse(_zip_unsafe("normal/assets/spr_115.bin"))

    def test_probe_uses_actual_bytes_for_digest_without_execution(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "specimen.rar"
            raw = b"Rar!\x1a\x07\x00" + b"arbitrary synthetic test bytes"
            f.write_bytes(raw)
            result = inspect_archive(f)
            self.assertEqual(result["sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(result["magic_family"], "RAR4")
            self.assertFalse(result["provenance_verified"])
            self.assertFalse(result["pet_runtime_verified"])

    def test_zip_members_not_extracted(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "synthetic.zip"
            with zipfile.ZipFile(path, "w") as zf:
                zf.writestr("../bad.txt", "not unpacked")
                zf.writestr("data/real_136.bin", "not original game data")
            result = inspect_archive(path)
            self.assertEqual(result["magic_family"], "ZIP")
            self.assertEqual(result["member_count"], 2)
            self.assertEqual(result["zip_unsafe_member_names"], ["../bad.txt"])
            self.assertFalse((Path(d) / "bad.txt").exists())
            self.assertFalse((Path(d) / "data/real_136.bin").exists())

    def test_real_magic_headers_not_textual_backslash_escapes(self):
        for raw, family in (
            (bytes([0x52,0x61,0x72,0x21,0x1a,0x07,0x00]), "RAR4"),
            (bytes([0x52,0x61,0x72,0x21,0x1a,0x07,0x01,0x00]), "RAR5"),
            (bytes([0x50,0x4b,0x03,0x04,0x00,0x00,0x00,0x00]), "ZIP"),
            (bytes([0x4d,0x5a,0x00,0x00]), "PE_OR_DOS_MZ"),
        ):
            with tempfile.TemporaryDirectory() as d:
                f = Path(d) / "candidate"
                f.write_bytes(raw)
                self.assertEqual(inspect_archive(f)["magic_family"], family)

if __name__ == "__main__":
    unittest.main()
