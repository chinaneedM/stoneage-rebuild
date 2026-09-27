import unittest
from tools.stoneage_tw10_savedata_pointer_probe import (
    all_occurrences, section_for_va, NEIGHBOR_RADIUS
)

class TestTw10SavedataPointerProbe(unittest.TestCase):
    def test_occurrences(self):
        self.assertEqual(all_occurrences(b"abcabc", b"abc"), (0,3))
        self.assertEqual(all_occurrences(b"abc", b"x"), ())

    def test_section_lookup(self):
        sections=[{"name":".data","rva":0x6000,"vsize":0x1000,"raw_size":0x800}]
        self.assertEqual(section_for_va(sections,0x400000,0x406123),(".data",0x123))
        self.assertEqual(section_for_va(sections,0x400000,0x405fff),("",-1))

    def test_radius_is_bounded(self):
        self.assertEqual(NEIGHBOR_RADIUS,0x800)

if __name__=="__main__":
    unittest.main()
