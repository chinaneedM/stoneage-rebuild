"""Public-only source-bound guard for INTEGRATION12. No commercial images or Pillow."""
import json
import pathlib
import unittest
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
NEW = ROOT / "research/recovered/STONEAGE-INTEGRATION12-HOTORU-TWO-ROOMS-SOURCE-JOINS-R1.json"
OLD = ROOT / "research/recovered/STONEAGE-INTEGRATION11-FLOOR1300-SOURCE-SCENE-R1.json"

class Integration12Public(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(NEW.read_text(encoding="utf-8"))
        cls.o = json.loads(OLD.read_text(encoding="utf-8"))

    def test_prior_warp_line_identity(self):
        old = {r["line"]: r for r in self.o["mapwarp_rows"]}
        self.assertEqual([r["line"] for r in self.r["original_warp_rows"]], list(range(1479, 1489)))
        for r in self.r["original_warp_rows"]:
            x = old[r["line"]]
            self.assertEqual((r["source"], r["target"], r["row_sha256"], r["exact_reverse"]),
                             (x["source"], x["target"], x["row_sha256"], x["exact_reverse"]))
            self.assertEqual(len(x["same_tuple_create"]), 1)
            self.assertEqual((r["create_path"], r["create_ordinal"], r["create_sha256"]),
                             (x["same_tuple_create"][0]["path"], x["same_tuple_create"][0]["ordinal"],
                              x["same_tuple_create"][0]["block_sha256"]))
            self.assertTrue(r["exact_reverse"])

    def test_room_dimensions_and_source_pins(self):
        self.assertEqual(self.r["rooms"]["1306"]["dimensions"], [40, 30])
        self.assertEqual(self.r["rooms"]["1310"]["dimensions"], [30, 30])
        self.assertEqual(self.r["basis"]["prior_integration11_blob"],
                         "3a3d601d9c40a322871ae4996893012d2f2dd3ef")
        for floor, room in self.r["rooms"].items():
            self.assertEqual(room["client_DAT"]["sha256"], self.o["linked_DAT"][floor]["sha256"])
            self.assertEqual(room["client_DAT"]["bytes"], self.o["linked_DAT"][floor]["bytes"])
            self.assertEqual(room["client_DAT"]["bytes"], 8+6*room["dimensions"][0]*room["dimensions"][1])
            self.assertEqual(room["server_LS2MAP"]["bytes"], 44+4*room["dimensions"][0]*room["dimensions"][1])
            self.assertEqual(room["server_LS2MAP"]["layer_u16_endian"], "big")
            self.assertEqual(room["observed_image_candidates"]["uncovered_references"], 0)
            self.assertGreater(room["observed_image_candidates"]["draw_references"], 0)
        self.assertEqual((len(self.r["rooms"]["1306"]["source_create"]),len(self.r["rooms"]["1310"]["source_create"])),(6,3))

    def test_duplicate_door_not_silently_collapsed(self):
        edges = self.r["original_warp_rows"]
        self.assertEqual(len(edges), 10)
        self.assertEqual(Counter(e["source"][0] for e in edges)[1306], 3)
        duplicate = [e for e in edges if e["source"] == [1306,21,21]]
        self.assertEqual({tuple(e["target"]) for e in duplicate}, {(1300,53,26),(1300,54,26)})
        self.assertEqual({(tuple(e["source"]),tuple(e["target"])) for e in edges},
                         {(tuple(x["source"]),tuple(x["target"])) for x in self.o["mapwarp_rows"]
                          if 1306 in (x["source"][0],x["target"][0]) or
                             1310 in (x["source"][0],x["target"][0])})

    def test_server_layer_differences_and_object_gap(self):
        elder=self.r["rooms"]["1306"]
        shop=self.r["rooms"]["1310"]
        self.assertEqual(elder["layer_comparison"][0]["changed"], 0)
        self.assertEqual(elder["layer_comparison"][1]["server_to_client_differences"], [[2,0,71]])
        self.assertEqual(shop["layer_comparison"][1]["server_to_client_differences"], [[2,0,4],[16073,0,1]])
        self.assertEqual(shop["server_only_object_cell"], {"xy":[16,15],"value":16073,"client_value":0})

    def test_shop_21_primary_missing_are_not_repaired_by_assumption(self):
        s=self.r["shop_itemset_conflict"]
        self.assertEqual(s["actual_create_xy"], [16,16])
        self.assertNotEqual(s["actual_create_xy"], s["filename_suffix_xy"])
        self.assertEqual(len(s["item_list"]), 16)
        self.assertEqual(len(s["limit_item_ids"]), 21)
        self.assertEqual(s["primary_missing_count"],len(s["limit_item_ids"]))
        self.assertEqual(s["alternate_missing_count"],0)
        self.assertEqual(s["special_item_ids"],list(range(1582,1587)))
        self.assertEqual(s["source_rate_strings"]["buy_rate"],"200.0")

    def test_evidence_boundaries_are_explicitly_negative(self):
        self.assertTrue(all(v is False for v in self.r["limits"].values()))
        self.assertFalse(self.r["provenance"]["parent_rar_fully_reread_this_work_unit"])
        self.assertEqual(self.r["provenance"]["private_evidence_zip"]["members"],31)
        self.assertEqual(self.r["provenance"]["independent_private_local_checks"],208)
        self.assertEqual(sum(r["observed_image_candidates"]["draw_references"] for r in self.r["rooms"].values()),393)

if __name__ == "__main__":
    unittest.main()
