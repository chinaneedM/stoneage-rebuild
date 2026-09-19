import io
import struct
import unittest
import zipfile

from tools.stoneage_sourceforge_zip_index_probe import (
    ARCHIVES,
    classify,
    parse_central_directory,
    parse_eocd_tail,
)


class SourceForgeZipIndexProbeTests(unittest.TestCase):
    def make_zip(self):
        out = io.BytesIO()
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("StoneAge/stoneage.exe", b"MZ" + b"\0" * 64)
            zf.writestr("StoneAge/data/real.bin", b"data")
            zf.writestr("launcher/custom_launcher.exe", b"MZ")
        return out.getvalue()

    def test_candidate_set_is_bounded(self):
        self.assertEqual(
            ARCHIVES,
            (
                "patch_0.zip",
                "patch_1.zip",
                "patch_2.zip",
                "patch_3.zip",
                "patch_4.zip",
                "patch_5.zip",
            ),
        )

    def test_parse_classic_zip_central_directory(self):
        blob = self.make_zip()
        tail = blob[-min(len(blob), 128 * 1024):]
        eocd = parse_eocd_tail(tail, len(blob))
        start = eocd["central_offset"]
        central = blob[start:start + eocd["central_size"]]
        entries = parse_central_directory(central, eocd["entries"])
        names = [entry.name for entry in entries]
        self.assertEqual(eocd["entries"], 3)
        self.assertIn("StoneAge/stoneage.exe", names)
        self.assertIn("StoneAge/data/real.bin", names)
        self.assertEqual(classify("StoneAge/stoneage.exe"), "exact-target")
        self.assertEqual(classify("StoneAge/data/real.bin"), "archaeology")
        self.assertEqual(classify("launcher/custom_launcher.exe"), "contamination-marker")

    def test_reject_multi_disk_eocd(self):
        # Minimal EOCD with disk_number=1.
        eocd = struct.pack("<4s4H2LH", b"PK\x05\x06", 1, 0, 0, 0, 0, 0, 0)
        with self.assertRaisesRegex(ValueError, "multi-disk"):
            parse_eocd_tail(eocd, len(eocd))

    def test_non_target_filename_is_not_promoted(self):
        self.assertEqual(classify("docs/stone.txt"), "")
        self.assertEqual(classify("unrelated/patch_notes.txt"), "")


if __name__ == "__main__":
    unittest.main()
