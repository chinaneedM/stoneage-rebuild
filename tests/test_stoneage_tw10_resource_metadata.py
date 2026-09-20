import gzip
from pathlib import Path
import struct
import tempfile
import unittest

from tools.stoneage_tw10_resource_metadata import (
    export_adrn,
    export_spr,
    parse_adrn_record,
    parse_map_attr,
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

    def test_parse_map_attr_and_adrn_collision_fields(self):
        attr = struct.pack(
            "<BBH18h3H2xI",
            3,
            4,
            205,
            7,
            *range(1, 18),
            101,
            102,
            103,
            12345,
        )
        parsed = parse_map_attr(attr)
        self.assertEqual(parsed["atari_x"], 3)
        self.assertEqual(parsed["atari_y"], 4)
        self.assertEqual(parsed["hit_raw"], 205)
        self.assertEqual(parsed["hit_flag"], 5)
        self.assertEqual(parsed["priority_type"], 2)
        self.assertEqual(parsed["height_flag"], 7)
        self.assertEqual(parsed["effect2"], 17)
        self.assertEqual(parsed["damy_a"], 101)
        self.assertEqual(parsed["map_number"], 12345)

        head = struct.pack("<IIIiiii", 9, 20, 32, -1, 2, 16, 8)
        row = parse_adrn_record(head + attr)
        self.assertEqual(row["bitmapno"], 9)
        self.assertEqual(row["map_number"], 12345)
        self.assertEqual(row["hit_flag"], 5)

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
                + struct.pack(
                    "<BBH18h3H2xI",
                    1, 1, 1, *([1] * 18), 1, 1, 1, 0,
                )
            )

            out1 = root / "adrn1.tsv.gz"
            collision1 = root / "collision1.tsv.gz"
            metrics = export_adrn(adrn, real, out1, collision1)
            self.assertEqual(metrics["records"], 2)
            self.assertEqual(metrics["bitmapnos"], 2)
            self.assertEqual(metrics["contiguous_transitions"], 1)
            self.assertEqual(metrics["real_bytes"], len(block1) + len(block2))
            with gzip.open(out1, "rt", encoding="utf-8") as f:
                rows = f.read().splitlines()
            with gzip.open(collision1, "rt", encoding="utf-8") as f:
                collision_rows = f.read().splitlines()
            self.assertEqual(len(rows), 3)
            self.assertTrue(rows[1].startswith("0\t100\t0\t20\t"))
            self.assertTrue(rows[2].startswith("1\t101\t20\t18\t"))
            self.assertEqual(len(collision_rows), 1)

            # Verify map-number mapping and last-record-wins semantics.
            real_collision = root / "real_collision.bin"
            adrn_collision = root / "adrn_collision.bin"
            cb1 = b"RD" + bytes([0, 0]) + struct.pack("<iiI", 1, 1, 17) + b"A"
            cb2 = b"RD" + bytes([0, 0]) + struct.pack("<iiI", 1, 1, 17) + b"B"
            real_collision.write_bytes(cb1 + cb2)
            ca1 = struct.pack(
                "<BBH18h3H2xI",
                1, 2, 0, 0, *([0] * 17), 0, 0, 0, 500,
            )
            ca2 = struct.pack(
                "<BBH18h3H2xI",
                3, 4, 201, 5, *([0] * 17), 0, 0, 0, 500,
            )
            adrn_collision.write_bytes(
                struct.pack("<IIIiiii", 10, 0, len(cb1), 0, 0, 1, 1)
                + ca1
                + struct.pack(
                    "<IIIiiii", 11, len(cb1), len(cb2), 0, 0, 1, 1
                )
                + ca2
            )
            collision_out = root / "collision.tsv.gz"
            cm = export_adrn(
                adrn_collision,
                real_collision,
                root / "collision_adrn.tsv.gz",
                collision_out,
            )
            self.assertEqual(cm["collision_map_numbers"], 1)
            self.assertEqual(cm["collision_duplicate_map_numbers"], 1)
            with gzip.open(collision_out, "rt", encoding="utf-8") as f:
                mapped_rows = f.read().splitlines()
            self.assertEqual(len(mapped_rows), 2)
            self.assertEqual(
                mapped_rows[1],
                "500\t1\t11\t3\t4\t201\t1\t2\t5",
            )

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
