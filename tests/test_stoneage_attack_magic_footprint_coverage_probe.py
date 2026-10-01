import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_attack_magic_footprint_coverage_probe import analyze


def record(matrix):
    values = [0] * 18 + [x for row in matrix for x in row]
    return struct.pack("<33I", *values)


class AttackMagicFootprintCoverageProbeTests(unittest.TestCase):
    def test_synthetic_singleton_coverage_and_open_population(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td)
            center = (
                (0, 0, 0, 0, 0),
                (0, 0, 1, 0, 0),
                (0, 0, 0, 0, 0),
            )
            whole_one = (
                (0, 0, 1, 0, 0),
                (0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0),
            )
            (data / "attmagic.bin").write_bytes(
                record(center)
                + record(center)
                + record(whole_one)
                + record(whole_one)
            )
            (data / "magic.txt").write_bytes(
                b"N,C,F,O,301,1,1,0,0\n"
                b"N,C,F,O,305,1,1,0,1\n"
            )
            result = analyze(data)
            self.assertEqual(result["magic_index_count"], 2)
            self.assertEqual(result["present"], 2)
            self.assertEqual(result["total_scenarios"], 20)
            self.assertEqual(result["portable"], 20)
            self.assertEqual(result["multi"], 0)
            self.assertEqual(result["empty"], 0)
            self.assertFalse(result["complete"])


if __name__ == "__main__":
    unittest.main()
