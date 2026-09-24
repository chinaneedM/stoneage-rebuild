import tempfile
import struct
import unittest
from pathlib import Path

from tools.stoneage_historical_map_25_compare import (
    compare,
    compatibility_against_profile,
)


def dat(width=1,height=1,base=1):
    values=(base,base+1,base+2)
    return struct.pack("<II3H",width,height,*values)


class HistoricalMap25CompareTests(unittest.TestCase):
    def test_identity_and_only_sets(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); a=root/"a"; b=root/"b"; a.mkdir(); b.mkdir()
            (a/"1.DAT").write_bytes(dat(base=1))
            (b/"1.dat").write_bytes(dat(base=1))
            (a/"2.DAT").write_bytes(dat(base=2))
            (b/"3.DAT").write_bytes(dat(base=3))
            result=compare(a,b)
            self.assertEqual(result["same"],[1])
            self.assertEqual(result["only_a"],[2])
            self.assertEqual(result["only_b"],[3])

    def test_difference_by_hash(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); a=root/"a"; b=root/"b"; a.mkdir(); b.mkdir()
            (a/"1.DAT").write_bytes(dat(base=1))
            (b/"1.DAT").write_bytes(dat(base=9))
            result=compare(a,b)
            self.assertEqual(result["different"],[1])


    def test_profile_compatibility_transition(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); a=root/"a"; b=root/"b"; a.mkdir(); b.mkdir()
            (a/"1.DAT").write_bytes(dat(base=100))
            (b/"1.DAT").write_bytes(dat(base=200))
            result=compare(a,b)
            a_status=compatibility_against_profile(result["a"][1],{100,101})
            b_status=compatibility_against_profile(result["b"][1],{100,101})
            self.assertEqual(a_status,(True,[]))
            self.assertEqual(b_status,(False,[200,201]))

if __name__=="__main__":
    unittest.main()
