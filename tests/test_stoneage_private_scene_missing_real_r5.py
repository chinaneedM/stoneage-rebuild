import unittest
import hashlib
import struct
from tools.stoneage_private_scene_missing_real_r5 import ROWS, get_rows, rgba_candidate

class TwoMissingSourceTests(unittest.TestCase):
    def test_exact_distinct_and_nonoverlapping_ranges(self):
        self.assertEqual([x[0] for x in ROWS],[5009,5015])
        self.assertTrue(ROWS[0][2]+ROWS[0][3] < ROWS[1][2])
    def test_no_fake_adrn(self):
        with self.assertRaisesRegex(ValueError,"ADRN identity"):
            get_rows(bytes(80*234564))
    def test_wrong_rgba_geometry_rejected(self):
        with self.assertRaisesRegex(ValueError,"dimensions"):
            rgba_candidate(bytes(2),2,2,bytes(768))
    def test_reserved_palette_not_inferred(self):
        self.assertIsNone(rgba_candidate(bytes([4]),1,1,bytes(768)))
        self.assertIsNone(rgba_candidate(bytes([255]),1,1,bytes(768)))
    def test_bottom_up_and_transparency(self):
        rgb=bytes(a for i in range(256) for a in (i,i,i))
        x=rgba_candidate(bytes([0,16,17,18]),2,2,rgb)
        self.assertEqual(x, bytes([17,17,17,255,18,18,18,255,0,0,0,0,16,16,16,255]))
    def test_black_168_is_opaque(self):
        rgb=bytes(768)
        self.assertEqual(rgba_candidate(bytes([168]),1,1,rgb),bytes([0,0,0,255]))
    def test_all_original_record_pins(self):
        self.assertTrue(all(len(x[-1])==64 for x in ROWS))
        self.assertEqual(ROWS[0][6:8], (64,47))
        self.assertEqual(ROWS[1][6:8], (64,47))
if __name__=="__main__": unittest.main()
