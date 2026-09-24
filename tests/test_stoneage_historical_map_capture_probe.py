import struct
import unittest

from tools.stoneage_historical_map_capture_probe import (
    CAPTURES, MAP_RE, map_entry_index, map_manifest_digest, mtime_day,
    parse_map_dat, signature, seven_zip_command
)


class HistoricalMapCaptureProbeTests(unittest.TestCase):
    def test_capture_timestamps_are_pinned(self):
        self.assertEqual(CAPTURES[0][0],"20030623234451")
        self.assertEqual(CAPTURES[1][0],"20031210092426")

    def test_map_path_shape(self):
        self.assertIsNotNone(MAP_RE.search("foo/map/123.dat"))
        self.assertIsNone(MAP_RE.search("foo/map/test.dat"))

    def test_archive_entry_helpers(self):
        entries=(
            {"Path":"map/1000.dat","Size":"10","CRC":"AAAA","Modified":"2002-11-08 12:00:00"},
            {"Path":"readme.txt","Size":"1"},
        )
        rows,dups=map_entry_index(entries)
        self.assertEqual(sorted(rows),[1000])
        self.assertEqual(dups,())
        self.assertEqual(mtime_day(rows[1000]["modified"]),"2002-11-08")
        self.assertEqual(len(map_manifest_digest(rows)),64)

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

    def test_archive_tool_resolver_returns_command(self):
        self.assertTrue(seven_zip_command())


if __name__=="__main__":
    unittest.main()
