import unittest

from tools.stoneage_tw10_discmaster_mapcache_probe import (
    SIGNATURES, MAP_NAME_RE, result_rows, search_url
)


class TaiwanV1DiscMasterMapcacheProbeTests(unittest.TestCase):
    def test_signatures_include_runtime_and_taiwan_marker(self):
        values=dict(SIGNATURES)
        self.assertEqual(values["runtime"],"sa_3.exe")
        self.assertEqual(values["taiwan-marker"],"waei.bin")
        self.assertEqual(values["graphics-index"],"adrn_1.bin")

    def test_map_path_shape_is_strict(self):
        self.assertIsNotNone(MAP_NAME_RE.search("StoneAge/map/100.dat"))
        self.assertIsNotNone(MAP_NAME_RE.search(r"StoneAge\map\42.dat"))
        self.assertIsNone(MAP_NAME_RE.search("StoneAge/data/map100.dat"))
        self.assertIsNone(MAP_NAME_RE.search("StoneAge/map/foo.dat"))

    def test_search_url_uses_recovered_schema_and_item_filter(self):
        url=search_url(q="map",qfields="name",itemid=123,extension=".dat",limit=1000)
        self.assertIn("qfields=name",url)
        self.assertIn("mode=deep",url)
        self.assertIn("outputAs=json",url)
        self.assertIn("itemid=123",url)
        self.assertIn("extension=.dat",url)

    def test_nested_result_rows_are_found(self):
        sample=[{"itemid":7,"itemName":"disc","fileid":"StoneAge/sa_3.exe","filename":"sa_3.exe"}]
        rows=result_rows(sample)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["itemid"],7)


if __name__=="__main__":
    unittest.main()
