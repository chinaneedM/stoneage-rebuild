import unittest
from tools.stoneage_tw10_mapcache_binary_probe import offset_to_rva, likely_function_window

class TaiwanV10MapCacheBinaryProbeTests(unittest.TestCase):
    def test_offset_to_rva(self):
        sections=[{"name":".text","raw":0x400,"raw_size":0x200,"rva":0x1000,"vsize":0x200}]
        self.assertEqual(offset_to_rva(sections,0x420),(0x1020,".text"))
        self.assertEqual(offset_to_rva(sections,0x100),(None,""))

if __name__=="__main__":
    unittest.main()
