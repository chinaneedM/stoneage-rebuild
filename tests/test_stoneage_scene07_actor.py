"""Source-bound parsing failures must reject misleading animation joins."""
import copy
from pathlib import Path
import struct
import tempfile
import unittest
from tools.stoneage_private_scene_actor_r7 import select_animations,resolve_bitmaps,authenticate,sha,export

def fixture():
    raw=bytearray()
    for direction in range(8):
        for action in (2,6):
            raw.extend(struct.pack('<HHII',direction,action,1000,2))
            raw.extend(struct.pack('<IhhH',123,-3,7,4))
            raw.extend(struct.pack('<IhhH',124,0,0,0))
    return struct.pack('<IIHH',100000,0,16,2),bytes(raw)

class SourceBoundaries(unittest.TestCase):
    def test_exact_positions_signed_offsets_and_sound_preserved(self):
        index,raw=fixture();g=select_animations(index,raw,(100000,))[0]
        self.assertEqual(g['animations'][0]['frames'][0],[123,-3,7,4])
        a=g['animations'][0]
        self.assertEqual(a['source_animation_span_sha256'],sha(raw[a['header_offset']:a['end_offset']]))
    def test_duplicate_group_does_not_choose_last(self):
        index,raw=fixture()
        with self.assertRaisesRegex(ValueError,'ambiguous'):select_animations(index+index,raw,(100000,))
    def test_duplicate_selector_does_not_fake_missing_direction(self):
        index,raw=fixture();b=bytearray(raw);struct.pack_into('<HH',b,32,0,2)
        with self.assertRaisesRegex(ValueError,'ambiguous'):select_animations(index,b,(100000,))
    def test_sentinel_is_not_bitmap(self):
        index,raw=fixture();b=bytearray(raw);struct.pack_into('<I',b,12,0xffffffff)
        with self.assertRaisesRegex(ValueError,'sentinel'):select_animations(index,b,(100000,))
    def test_truncated_group_and_unaccounted_suffix_rejected(self):
        index,raw=fixture()
        for value in (raw[:-1],raw+b'\0'):
            with self.subTest(length=len(value)),self.assertRaises(ValueError):select_animations(index,value,(100000,))
    def test_oversized_frame_read_refused(self):
        index,raw=fixture();b=bytearray(raw);struct.pack_into('<I',b,8,0xffffffff)
        with self.assertRaisesRegex(ValueError,'frame source range'):select_animations(index,b,(100000,))
    def test_duplicate_physical_id_and_out_of_bounds_rd_rejected(self):
        row=struct.pack('<7i',123,16,20,-32,-24,2,2)+bytes(52)
        self.assertEqual(resolve_bitmaps(row,{123},36)[123]['xoff'],-32)
        for data,size in [(row+row,36),(row,35)]:
            with self.subTest(size=size),self.assertRaises(ValueError):resolve_bitmaps(data,{123},size)
    def test_unknown_bitmap_is_not_filled(self):
        with self.assertRaisesRegex(ValueError,'ambiguous'):resolve_bitmaps(bytes(80),{123},100)
    def test_source_same_size_mutation_and_symlink_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source';p.write_bytes(b'abcd');authenticate(p,(4,sha(b'abcd')))
            p.write_bytes(b'abce')
            with self.assertRaisesRegex(ValueError,'SHA'):authenticate(p,(4,sha(b'abcd')))
            q=Path(d)/'link';q.symlink_to(p)
            with self.assertRaisesRegex(ValueError,'extent'):authenticate(q,(4,sha(b'abce')))
    def test_output_in_public_repo_rejected_before_source_reads(self):
        with self.assertRaisesRegex(ValueError,'public Git'):export(Path('/missing'),Path('/missing'),Path(__file__).resolve().parents[1]/'bad-output')

if __name__=='__main__':unittest.main()
