import gzip
from pathlib import Path
import struct
import tempfile
import unittest

from tools.stoneage_tw10_resource_metadata import (
    export_adrn,
    export_spr,
    parse_adrn_record,
    parse_spreadrn_record,
)


class TaiwanV10ResourceMetadataTests(unittest.TestCase):
    def test_parse_adrn_record(self):
        head = struct.pack("<IIIiiii", 123, 456, 32, -2, 3, 16, 8)
        rec = head + bytes(range(52))
        row = parse_adrn_record(rec)
        self.assertEqual(row["bitmapno"], 123)
        self.assertEqual(row["adder"], 456)
        self.assertEqual(row["size"], 32)
        self.assertEqual(row["xoff"], -2)
        self.assertEqual(row["yoff"], 3)
        self.assertEqual(row["width"], 16)
        self.assertEqual(row["height"], 8)
        self.assertEqual(len(row["attr_sha256"]), 64)

    def test_parse_spreadrn_record(self):
        rec = struct.pack("<IIHH", 100123, 4567, 89, 7)
        self.assertEqual(parse_spreadrn_record(rec), (100123, 4567, 89, 7))

    def test_export_adrn_and_spr(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            real = root / "real.bin"
            adrn = root / "adrn.bin"

            block1 = b"RD" + bytes([1, 0]) + struct.pack("<iiI", 2, 2, 20) + b"ABCD"
            block2 = b"RD" + bytes([0, 0]) + struct.pack("<iiI", 1, 2, 18) + b"EF"
            real.write_bytes(block1 + block2)
            adrn.write_bytes(
                struct.pack("<IIIiiii", 100, 0, len(block1), 0, 0, 2, 2)
                + bytes(52)
                + struct.pack(
                    "<IIIiiii", 101, len(block1), len(block2), 1, -1, 1, 2
                )
                + bytes([1]) * 52
            )

            out1 = root / "adrn1.tsv.gz"
            metrics = export_adrn(adrn, real, out1)
            self.assertEqual(metrics["records"], 2)
            self.assertEqual(metrics["bitmapnos"], 2)
            self.assertEqual(metrics["contiguous_transitions"], 1)
            self.assertEqual(metrics["real_bytes"], len(block1) + len(block2))
            with gzip.open(out1, "rt", encoding="utf-8") as f:
                rows = f.read().splitlines()
            self.assertEqual(len(rows), 3)
            self.assertTrue(rows[1].startswith("0\t100\t0\t20\t"))
            self.assertTrue(rows[2].startswith("1\t101\t20\t18\t"))

            # A second export must be byte-for-byte deterministic.
            out2 = root / "adrn2.tsv.gz"
            export_adrn(adrn, real, out2)
            self.assertEqual(out1.read_bytes(), out2.read_bytes())

            spr = root / "spr.bin"
            spreadrn = root / "spradrn.bin"
            anim = struct.pack("<HHII", 3, 9, 120, 2)
            frame1 = struct.pack("<IhhH", 100, -4, 5, 8)
            frame2 = struct.pack("<IhhH", 0xFFFFFFFF, 1, -2, 10001)
            spr.write_bytes(anim + frame1 + frame2)
            spreadrn.write_bytes(struct.pack("<IIHH", 100000, 0, 1, 0))

            group_out = root / "groups.tsv.gz"
            anim_out = root / "animations.tsv.gz"
            frame_out = root / "frames.tsv.gz"
            sm = export_spr(spreadrn, spr, group_out, anim_out, frame_out)
            self.assertEqual(sm["groups"], 1)
            self.assertEqual(sm["animations"], 1)
            self.assertEqual(sm["frames"], 2)
            self.assertEqual(sm["sentinel_frames"], 1)
            self.assertEqual(sm["exact_group_spans"], 1)

            with gzip.open(group_out, "rt", encoding="utf-8") as f:
                group_rows = f.read().splitlines()
            with gzip.open(anim_out, "rt", encoding="utf-8") as f:
                anim_rows = f.read().splitlines()
            with gzip.open(frame_out, "rt", encoding="utf-8") as f:
                frame_rows = f.read().splitlines()
            self.assertEqual(len(group_rows), 2)
            self.assertEqual(len(anim_rows), 2)
            self.assertEqual(len(frame_rows), 3)
            self.assertTrue(frame_rows[2].endswith("\t1"))


if __name__ == "__main__":
    unittest.main()
