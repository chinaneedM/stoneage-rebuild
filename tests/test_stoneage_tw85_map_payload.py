import hashlib
from pathlib import Path
import struct
import tempfile
import unittest
from tools.stoneage_tw85_map_payload import analyze, parse


class MapPayloadTests(unittest.TestCase):
    def data(self):
        return struct.pack('<II6H', 2, 1, 10, 20, 0, 5, 1, 1)

    def test_planes_preserve_order_and_distinct_hashes(self):
        row = parse(self.data())
        self.assertEqual((row['width'], row['height'], row['cells']), (2, 1, 2))
        self.assertEqual([p['nonzero_cells'] for p in row['planes']], [2, 1, 2])
        self.assertEqual(row['planes'][2]['most_frequent'], [{'value': 1, 'cells': 2}])
        self.assertEqual(row['planes'][0]['sha256'], hashlib.sha256(struct.pack('<2H', 10, 20)).hexdigest())

    def test_invalid_layouts(self):
        for raw in (b'', self.data()[:-1], self.data()+b'\0', struct.pack('>II6H', 2, 1, 10, 20, 0, 5, 1, 1),
                    struct.pack('<II', 0, 1), struct.pack('<II', 2**31, 2**31)):
            with self.subTest(raw=raw[:8]), self.assertRaises(ValueError):
                parse(raw)

    def test_inventory_hash_and_exact_set(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'map').mkdir()
            path = root/'map/100.dat'
            path.write_bytes(self.data())
            expected = [{'path': 'map/100.dat', 'bytes': 20, 'sha256': hashlib.sha256(self.data()).hexdigest()}]
            self.assertEqual(analyze(root, expected)[0]['status'], 'EXACT_LAYOUT_MATCH')
            (root/'map/bgm.dat').write_bytes(b'auxiliary')
            self.assertEqual(len(analyze(root, expected)), 1)
            path.write_bytes(self.data()[:-2]+b'\0\0')
            with self.assertRaises(ValueError):
                analyze(root, expected)
            path.write_bytes(self.data())
            (root/'map/101.dat').write_bytes(self.data())
            with self.assertRaises(ValueError):
                analyze(root, expected)
            (root/'map/101.dat').unlink()
            with self.assertRaises(ValueError):
                analyze(root, expected+expected)
            path.unlink()
            with self.assertRaises(ValueError):
                analyze(root, expected)

    def test_qualified_unknown_layout_stays_unresolved(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'map').mkdir()
            (root/'map/1.dat').write_bytes(b'unknown')
            rows = analyze(root, [{'path': 'map/1.dat', 'bytes': 7, 'sha256': hashlib.sha256(b'unknown').hexdigest()}])
            self.assertEqual(rows[0]['status'], 'LAYOUT_UNRESOLVED')
            self.assertNotIn('planes', rows[0])


if __name__ == '__main__':
    unittest.main()
