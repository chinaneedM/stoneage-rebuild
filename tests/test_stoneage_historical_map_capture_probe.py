import struct
import unittest

from tools.stoneage_historical_map_capture_probe import (
    CAPTURES, MAP_RE, parse_map_dat, signature
)


class HistoricalMapCaptureProbeTests(unittest.TestCase):
    def test_capture_timestamps_are_pinned(self):
        self.assertEqual(CAPTURES[0][0],"20030623234451")
        self.assertEqual(CAPTURES[1][0],"20031210092426")

    def test_map_path_shape(self):
        self.assertIsNotNone(MAP_RE.search("foo/map/123.dat"))
        self.assertIsNone(MAP_RE.search("foo/map/test.dat"))

    def test_three_plane_parser(self):
        width,height=2,1
        values=(1,2,3,4,5,6)
        raw=struct.pack("<II6H",width,height,*values)
        meta=parse_map_dat(raw)
        self.assertEqual(meta["width"],2)
        self.assertEqual(meta["cells"],2)
        self.assertEqual(meta["tile_nonzero"],2)
        self.assertEqual(meta["parts_max"],4)
        self.assertEqual(meta["event_max"],6)

    def test_signature(self):
        self.assertEqual(signature(b"MZ"+b"\0"*10),"pe-mz")
        self.assertEqual(signature(b"PK\x03\x04abc"),"zip")


if __name__=="__main__":
    unittest.main()
