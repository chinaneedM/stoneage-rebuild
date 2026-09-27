import unittest

from tools.stoneage_tw10_gameplay_callback_probe import find_ascii_rvas, image_c_string, shared_direct_targets


class TaiwanGameplayCallbackProbeTests(unittest.TestCase):

    def test_image_c_string_reads_ascii_at_image_rva(self):
        data = b"HEADER" + b"%X|%X\\0" + b"TAIL"
        sections = [{
            "name": ".data",
            "rva": 0x1000,
            "vsize": len(data),
            "raw_size": len(data),
            "raw": 0,
        }]
        self.assertEqual(image_c_string(data, sections, 0x1006), "%X|%X")
        self.assertIsNone(image_c_string(data, sections, 0x5000))

    def test_find_ascii_rvas_maps_raw_offsets_back_to_image_rvas(self):
        data = b"HEAD%X|%X\\0TAIL%X|%X\\0"
        sections = [{
            "name": ".data",
            "rva": 0x2000,
            "vsize": len(data),
            "raw_size": len(data),
            "raw": 0,
        }]
        self.assertEqual(find_ascii_rvas(data, sections, "%X|%X"), [0x2004, 0x2010])

    def test_shared_direct_targets(self):
        cfgs = {
            "S": {"direct_calls": {0x1000: 9, 0x2000: 2}},
            "C": {"direct_calls": {0x1000: 4, 0x3000: 1}},
            "I": {"direct_calls": {0x1000: 7, 0x2000: 3}},
        }
        got = shared_direct_targets(cfgs)
        self.assertEqual(got[0x1000], {"S": 9, "C": 4, "I": 7})
        self.assertEqual(got[0x2000], {"S": 2, "I": 3})
        self.assertNotIn(0x3000, got)


if __name__ == "__main__":
    unittest.main()
