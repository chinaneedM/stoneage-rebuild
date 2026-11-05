"""Verify the published Jaja logging source joins and literal branch fields."""
from hashlib import sha256
import json
from pathlib import Path
import unittest


RECOVERED = Path(__file__).resolve().parents[1] / "research/recovered"
WORLD15 = RECOVERED / "STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-15-VILLAGE-EXIT-ENCOUNTER-SOURCE-R1.json"
WORLD16 = RECOVERED / "STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-16-JAJA-LOGGING-RETURN-SOURCE-R1.json"


class JajaLoggingReturnTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(WORLD16.read_bytes())
        cls.encounter = json.loads(WORLD15.read_bytes())

    def test_three_npc_member_receipts_and_the_world15_parent(self):
        report = self.report
        registry = json.loads((RECOVERED / "STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json").read_bytes())
        registered = {r["path"]: r for r in registry["all_server_occurrences"]}
        self.assertEqual(report["archive_sha256"], self.encounter["archive_sha256"])
        self.assertEqual(report["world15_sha256"], sha256(WORLD15.read_bytes()).hexdigest())
        for source in report["members"].values():
            self.assertEqual(source["bytes"], registered[source["path"]]["size"])
            self.assertEqual(source["sha256"], registered[source["path"]]["sha256"])
            self.assertRegex(source["crc32"], r"^[a-f0-9]{8}$")

    def test_create_links_the_exact_merchant_to_the_script(self):
        placement = self.report["placement"]
        self.assertEqual(placement["name"], "木材商人賽尚")
        self.assertEqual(placement["floor"], 3000)
        self.assertEqual(placement["borncorner"], [114, 69, 114, 69])
        self.assertEqual(placement["graphics_field"], 16000)
        self.assertEqual(placement["create_block_number"], 5)
        self.assertEqual(placement["template_key"], "changeevent")
        self.assertEqual(placement["functionset"], "ExChangeMan")
        self.assertEqual("npc/" + placement["script_relative_path"],
                         self.report["members"]["script"]["path"])
        self.assertEqual(sum(r["village"] == placement["floor"] and 88 in r["area_ids"]
                             for r in self.encounter["arrivals"]), 10)

    def test_positive_wood_branches_preserve_source_order_and_literals(self):
        records = self.report["records"]
        self.assertEqual(len(records), 17)
        self.assertTrue(all(r["event_number"] == -1 for r in records))
        self.assertTrue(all(a["end_line"] < b["start_line"] for a, b in zip(records, records[1:])))
        self.assertEqual([r["type"] for r in records], ["MESSAGE"] + ["ACCEPT"] * 15 + ["REQUEST"])
        amounts = [20000, 16000, 12000, 10000, 8000, 7200, 6400, 5600,
                   4800, 4000, 3200, 2400, 1600, 400]
        for quantity, amount, row in zip(range(14, 0, -1), amounts, records[1:15]):
            self.assertEqual(row["predicate"], f"ITEM=2478&ITEM=2468*{quantity}")
            self.assertEqual(row["get_stone"], amount)
            self.assertEqual(row["get_items"], ["2481"] if quantity == 14 else [])
            self.assertEqual(row["del_items"], ["2468", "2478"] + ([] if quantity == 12 else ["2467"]))

    def test_message_no_wood_and_request_are_separate(self):
        records = self.report["records"]
        message, no_wood, request = records[0], records[-2], records[-1]
        self.assertEqual((message["predicate"], message["del_items"]), ("ITEM!=2478&ITEM=2468", []))
        self.assertEqual((no_wood["predicate"], no_wood["del_items"]), ("ITEM=2478&ITEM!=2468", ["2478"]))
        self.assertEqual((request["predicate"], request["del_items"], request["get_items"]),
                         ("ITEM=2467", ["2467*1"], ["2478*1"]))
        self.assertTrue(all(r["get_stone"] is None for r in (message, no_wood, request)))

    def test_permit_and_wood_use_the_same_original_item_rows(self):
        records = self.report["source_item_rows"]
        self.assertEqual(set(records), {"2467", "2468", "2478", "2481"})
        for key, old in self.encounter["logging_relation"]["items"].items():
            self.assertEqual(records[key], {k: old[k] for k in ("name", "line", "line_sha256")})
        self.assertEqual(records["2467"]["name"], "巴爾的推薦書")
        self.assertEqual(records["2481"]["name"], "杉的手環")
        self.assertEqual(self.report["bounds"], {
            "historical_official_deployment_proven": False, "native_branch_selection_proven": False,
            "native_inventory_or_payout_execution_proven": False, "tail_hit_rule_proven": False,
            "quest_origin": "UNRESOLVED",
        })
