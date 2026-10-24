import gzip
import struct
import tempfile
from pathlib import Path
import unittest
from tools.stoneage_cn50_spr_metadata import export_cn50_spr


def group(spr_no,offset):
    return struct.pack("<IIHH",spr_no,offset,1,0)


class MainlandSpriteOrderingTests(unittest.TestCase):
    def test_swapped_original_index_records_preserve_physical_spans(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            body=struct.pack("<HHII",0,11,0,0)+struct.pack("<HHII",1,12,0,0)
            (p/"spr.bin").write_bytes(body)
            # Logical groups deliberately refer to physical data out of order.
            (p/"idx.bin").write_bytes(group(100101,12)+group(100100,0))
            obj=export_cn50_spr(p/"idx.bin",p/"spr.bin",
                p/"groups.gz",p/"animations.gz",p/"frames.gz")
            self.assertEqual(obj["nonmonotonic_index_offset_transitions"],1)
            self.assertEqual(obj["groups"],2)
            self.assertEqual(obj["animations"],2)
            with gzip.open(p/"groups.gz","rt") as f:
                lines=f.readlines()
            self.assertIn("100101\t12\t",lines[1])
            self.assertIn("100100\t0\t",lines[2])

    def test_segment_gap_is_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            (p/"idx.bin").write_bytes(group(100100,0))
            (p/"spr.bin").write_bytes(struct.pack("<HHII",0,11,0,0)+b"junk")
            with self.assertRaises(ValueError):
                export_cn50_spr(p/"idx.bin",p/"spr.bin",
                                  p/"groups.gz",p/"animations.gz",p/"frames.gz")

    def test_offset_outside_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            (p/"idx.bin").write_bytes(group(100100,10000))
            (p/"spr.bin").write_bytes(b"abc")
            with self.assertRaises(ValueError):
                export_cn50_spr(p/"idx.bin",p/"spr.bin",
                                  p/"groups.gz",p/"animations.gz",p/"frames.gz")
