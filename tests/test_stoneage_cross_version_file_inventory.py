"""Synthetic fixtures only; no copyrighted client or server payload."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from stoneage_cross_version_file_inventory import scan, normalize_name, family


class InventoryTests(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)

    def specimen(self, path, sid, kind="directory", source_class="UNVERIFIED_CANDIDATE"):
        return {"sample_id": sid, "local_path": str(path), "kind": kind,
                "source_class": source_class, "evidence_ref": "synthetic-test",
                "region": "TEST", "claimed_version": "UNKNOWN"}

    def scan(self, *samples):
        return scan({"schema": "stoneage.cross_version_input_r1", "samples": list(samples)})

    def test_exact_cross_build_dedup_and_changed_same_path(self):
        a, b = self.root / "first", self.root / "second"
        for p in (a, b):
            (p / "data").mkdir(parents=True)
            (p / "data" / "spr_1.bin").write_bytes(b"same")
        (a / "data" / "NPC.dat").write_bytes(b"one")
        (b / "data" / "NPC.dat").write_bytes(b"two")
        out = self.scan(self.specimen(a, "TW10"), self.specimen(b, "BRIDGE25"))
        self.assertEqual(out["totals"], {
            "samples": 2, "file_occurrences": 4, "unique_exact_blobs": 3,
            "cross_sample_duplicate_blobs": 1, "changed_same_path_count": 1})
        self.assertEqual(out["changed_same_path"][0]["normalized_path"], "data/npc.dat")
        self.assertFalse(out["qualification"]["official_authenticity_inferred"])

    def test_directory_and_zip_byte_equivalence(self):
        d, z = self.root / "tree", self.root / "old.zip"
        (d / "graphics").mkdir(parents=True)
        (d / "graphics" / "frame.bin").write_bytes(b"original")
        with zipfile.ZipFile(z, "w") as out:
            out.writestr("graphics/frame.bin", b"original")
        r = self.scan(self.specimen(d, "a"), self.specimen(z, "b", "zip"))
        self.assertEqual(r["totals"]["unique_exact_blobs"], 1)
        self.assertEqual(r["samples"][0]["manifest_sha256"], r["samples"][1]["manifest_sha256"])

    def test_unsafe_paths_rejected(self):
        for name in ("../escape", "dir/../file", "/root/x", "C:\\temp\\a",
                     "bad//path", "one/./two", "a\x00b", "a\nb"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                normalize_name(name)

    def test_zip_traversal_rejected(self):
        z = self.root / "bad.zip"
        with zipfile.ZipFile(z, "w") as out:
            out.writestr("../escape.txt", b"x")
        with self.assertRaisesRegex(ValueError, "unsafe"):
            self.scan(self.specimen(z, "a", "zip"))

    def test_duplicate_windows_path_rejected(self):
        z = self.root / "repeat.zip"
        with zipfile.ZipFile(z, "w") as out:
            out.writestr("Pet.dat", b"a")
            out.writestr("pet.dat", b"b")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.scan(self.specimen(z, "a", "zip"))

    def test_directory_symlink_rejected(self):
        d = self.root / "tree"
        d.mkdir()
        (d / "file.txt").write_bytes(b"f")
        (d / "link.txt").symlink_to(d / "file.txt")
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.scan(self.specimen(d, "a"))

    def test_claimed_official_status_cannot_be_invented(self):
        d = self.root / "tree"
        d.mkdir()
        (d / "file.txt").write_bytes(b"f")
        with self.assertRaisesRegex(ValueError, "source class"):
            self.scan(self.specimen(d, "a", source_class="CERTIFIED_OFFICIAL_BY_TOOL"))

    def test_duplicate_sample_ids_rejected(self):
        d = self.root / "tree"
        d.mkdir()
        (d / "file.txt").write_bytes(b"f")
        with self.assertRaisesRegex(ValueError, "repeated"):
            self.scan(self.specimen(d, "a"), self.specimen(d, "a"))

    def test_output_is_metadata_not_original_bytes(self):
        d = self.root / "secret_source_location"
        d.mkdir()
        (d / "sa.bin").write_bytes(b"copyrighted mock data")
        output = json.dumps(self.scan(self.specimen(d, "a")))
        self.assertNotIn("copyrighted mock data", output)
        self.assertNotIn("secret_source_location", output)

    def test_file_family_is_hint_not_species_identity(self):
        self.assertEqual(family("data/spr_1.bin"), "GRAPHICS_OR_ANIMATION_CONTAINER")
        self.assertEqual(family("maps/first.dat"), "POSSIBLE_MAP_OR_DATA")
        self.assertEqual(family("stoneage.exe"), "EXECUTABLE_DO_NOT_RUN")


if __name__ == "__main__":
    unittest.main()
