import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_map_timeline_compare import (
    lineage_code,
    pair_summary,
    plane_diffs,
)
from tools.stoneage_historical_map_25_compare import index_numeric_maps

def dat(tile=100,parts=101,event=1):
    return struct.pack("<II3H",1,1,tile,parts,event)

class MapTimelineCompareTests(unittest.TestCase):
    def test_lineage_codes(self):
        def row(h): return {"sha256":h}
        self.assertEqual(lineage_code(row("a"),row("a"),row("a")),"STABLE_ALL")
        self.assertEqual(lineage_code(row("a"),row("a"),row("b")),"JUNE_DEC_SAME_THEN_CHANGED")
        self.assertEqual(lineage_code(row("a"),row("b"),row("b")),"CHANGED_BY_DEC_THEN_STABLE")
        self.assertEqual(lineage_code(row("a"),row("b"),row("a")),"DEC_ONLY_DIVERGENCE")
        self.assertEqual(lineage_code(row("a"),row("b"),row("c")),"THREE_DISTINCT")

    def test_pair_and_plane_diffs(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); a=root/"a"; b=root/"b"; a.mkdir(); b.mkdir()
            (a/"1.DAT").write_bytes(dat(100,101,1))
            (b/"1.DAT").write_bytes(dat(100,102,2))
            ar,_=index_numeric_maps(a); br,_=index_numeric_maps(b)
            pair=pair_summary(ar,br)
            self.assertEqual(pair["different"],[1])
            diff=plane_diffs(ar[1],br[1])
            self.assertEqual(diff["tile"],0)
            self.assertEqual(diff["parts"],1)
            self.assertEqual(diff["event"],1)

if __name__=="__main__":
    unittest.main()
