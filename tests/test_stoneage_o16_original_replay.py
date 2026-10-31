"""Synthetic extent tests only; no private game data in public CI."""
import unittest
from tools.stoneage_o16_original_replay import manifest


class ManifestExtentTests(unittest.TestCase):
    def test_interleaved_source_order(self):
        rows = manifest(b'0:2:battle00.sab\r\n2:3:Palet_1.sap\r\n5:2:battle01.sab\r\n', b'abcdefg')
        self.assertEqual(rows, [(0, 2, 'battle00.sab'), (2, 3, 'Palet_1.sap'), (5, 2, 'battle01.sab')])

    def test_invalid_extents_and_paths(self):
        cases = {
            'gap': b'0:2:battle00.sab\n3:4:Palet_1.sap\n',
            'overlap': b'0:3:battle00.sab\n2:5:Palet_1.sap\n',
            'past_end': b'0:8:battle00.sab\n',
            'unclaimed_tail': b'0:6:battle00.sab\n',
            'zero_length': b'0:0:battle00.sab\n0:7:Palet_1.sap\n',
            'same_name': b'0:2:battle00.sab\n2:5:battle00.sab\n',
            'path_escape': b'0:7:../battle00.sab\n',
            'negative_offset': b'-1:7:battle00.sab\n',
            'blank': b'',
        }
        for label, raw in cases.items():
            with self.subTest(label=label), self.assertRaises(ValueError):
                manifest(raw, b'abcdefg')


if __name__ == '__main__':
    unittest.main()
