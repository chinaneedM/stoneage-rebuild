"""Synthetic negative tests for offline installed-client chronology separation."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from tools.stoneage_client_snapshot_transition_audit import scan_tree, compare_trees


class SnapshotTransitionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.before = self.base / "install"
        self.after = self.base / "updated"
        self.before.mkdir()
        self.after.mkdir()

    def write(self, folder, filename, value):
        p = folder / filename
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(value)

    def test_change_add_remove_unchanged(self):
        self.write(self.before, "sa.exe", b"base")
        self.write(self.before, "data/real_1.bin", b"same")
        self.write(self.before, "old.ini", b"gone")
        self.write(self.after, "sa.exe", b"updated")
        self.write(self.after, "data/real_1.bin", b"same")
        self.write(self.after, "new.ini", b"new")
        result = compare_trees(scan_tree(self.before), scan_tree(self.after))
        self.assertEqual(result["added"], ["new.ini"])
        self.assertEqual(result["removed"], ["old.ini"])
        self.assertEqual(result["modified"], ["sa.exe"])
        self.assertEqual(result["unchanged_count"], 1)
        self.assertFalse(result["source_version_verified"])
        self.assertFalse(result["complete_original_patch_sequence_verified"])

    def test_nontrivial_file_hash(self):
        self.write(self.before, "data/blob", b"abc" * 400000)
        snap = scan_tree(self.before)
        self.assertEqual(snap["files"]["data/blob"]["sha256"], hashlib.sha256(b"abc" * 400000).hexdigest())
        self.assertEqual(snap["total_bytes"], 1200000)

    def test_same_content_stable_digest(self):
        self.write(self.before, "abc.dat", b"1")
        self.write(self.before, "d/ef.dat", b"2")
        self.write(self.after, "d/ef.dat", b"2")
        self.write(self.after, "abc.dat", b"1")
        b, a = scan_tree(self.before), scan_tree(self.after)
        self.assertEqual(b["manifest_sha256"], a["manifest_sha256"])
        self.assertEqual(compare_trees(b,a)["unchanged_count"], 2)

    def test_mismatched_case_unsupported_on_windows(self):
        self.write(self.before,"SA.EXE",b"1")
        self.write(self.before,"sa.exe",b"2")
        with self.assertRaisesRegex(ValueError, "case-colliding"):
            scan_tree(self.before)

    def test_empty_rejected(self):
        with self.assertRaisesRegex(ValueError,"Empty"):
            scan_tree(self.before)

    def test_no_directory(self):
        with self.assertRaisesRegex(ValueError,"directory"):
            scan_tree(self.base / "missing")

    def test_symlink_file_rejected(self):
        self.write(self.before,"good",b"x")
        (self.before / "bad").symlink_to(self.before / "good")
        with self.assertRaisesRegex(ValueError,"Symlinks"):
            scan_tree(self.before)

    def test_symlink_directory_rejected(self):
        self.write(self.before,"good",b"x")
        (self.before / "linked").symlink_to(self.after, target_is_directory=True)
        with self.assertRaisesRegex(ValueError,"Symlinks"):
            scan_tree(self.before)

    def test_symlink_root_rejected(self):
        self.write(self.before,"good",b"x")
        root = self.base / "rootlink"
        root.symlink_to(self.before, target_is_directory=True)
        with self.assertRaisesRegex(ValueError,"symlink"):
            scan_tree(root)

    def test_byte_difference_detected_even_same_size(self):
        self.write(self.before,"sa.exe",b"aaa")
        self.write(self.after,"sa.exe",b"bbb")
        self.assertEqual(compare_trees(scan_tree(self.before),scan_tree(self.after))["modified"],["sa.exe"])

    def test_folder_name_does_not_certify_version(self):
        self.write(self.before,"TW_OFFICIAL_8_0.exe",b"fake")
        self.write(self.after,"TW_OFFICIAL_8_0.exe",b"fake")
        r = compare_trees(scan_tree(self.before),scan_tree(self.after))
        self.assertFalse(r["official_publisher_verified"])
        self.assertFalse(r["original_pet_opcode127_runtime_verified"])

    def test_no_executable_launch_or_copy(self):
        self.write(self.before,"sa.exe",b"MZsynthetic")
        self.write(self.after,"sa.exe",b"MZsynthetic")
        compare_trees(scan_tree(self.before),scan_tree(self.after))
        self.assertEqual((self.before/"sa.exe").read_bytes(), b"MZsynthetic")
        self.assertEqual((self.after/"sa.exe").read_bytes(), b"MZsynthetic")

    def test_filename_with_newline_rejected(self):
        self.write(self.before,"sa\nbad",b"X")
        with self.assertRaisesRegex(ValueError,"Unsupported"):
            scan_tree(self.before)


if __name__ == "__main__":
    unittest.main()
