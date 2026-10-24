import unittest
from tools import stoneage_tw10_graphic_upstream_p2b as m
class NativeSourceBoundary(unittest.TestCase):
    def test_all_previous_sources_and_101_rows(self):
        x=m.context()
        self.assertEqual((x["static_candidate_count"],x["id_first"],x["id_last"]),(101,5846,5946))
        self.assertTrue(x["all_keys_in_verified_static_selector_interval"])
    def test_untrusted_executable_rejected_before_disassembly(self):
        for x in (b"",b"MZ"+b"\0"*425982,b"synthetic"):
            with self.assertRaises(ValueError): m.scan(x)
if __name__=="__main__": unittest.main()
