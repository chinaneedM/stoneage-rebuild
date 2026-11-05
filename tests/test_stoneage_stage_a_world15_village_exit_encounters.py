"""Check the public static joins without requiring proprietary archive members."""
from collections import Counter
from hashlib import sha1
import json
from pathlib import Path
import unittest


RECOVERED = Path(__file__).resolve().parents[1] / "research/recovered"
WORLD12 = RECOVERED / "STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-12-THREE-VILLAGE-WARP-SOURCE-R1.json"
WORLD15 = RECOVERED / "STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-15-VILLAGE-EXIT-ENCOUNTER-SOURCE-R1.json"
R18 = RECOVERED / "STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json"


class VillageExitEncounterSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(WORLD15.read_bytes())
        cls.world12 = json.loads(WORLD12.read_bytes())

    def test_source_receipts_match_earlier_exact_archive_inventory(self):
        inventory = json.loads(R18.read_bytes())
        expected = {row["path"]: row for row in inventory["all_server_occurrences"]}
        report = self.report
        self.assertEqual(report["archive_sha256"], self.world12["original_archive_sha256"])
        self.assertEqual(report["archive_sha256"], inventory["source_parent"]["source_package_sha256"])
        members = report["verified_members"]
        self.assertEqual(set(members), {
            "setup.cf", "encount.txt", "group1.txt", "group.txt", "enemy.txt",
            "enemybase.txt", "itemset.txt",
        })
        for filename, row in members.items():
            with self.subTest(filename=filename):
                if filename == "setup.cf":
                    self.assertEqual(row["bytes"], 9715)
                    self.assertEqual(row["sha256"], "b4936c103efb7b3cad359e5c85c7965187306883a68c0be712ece6c374e3b12d")
                else:
                    self.assertTrue(row["archive_member"].endswith(f"/gmsv/data/{filename}"))
                    self.assertEqual(row["bytes"], expected[filename]["size"])
                    self.assertEqual(row["sha256"], expected[filename]["sha256"])
                self.assertRegex(row["crc32"], r"^[a-f0-9]{8}$")

    def test_every_outdoor_exit_is_the_exact_world12_record(self):
        data = WORLD12.read_bytes()
        self.assertEqual(sha1(f"blob {len(data)}\0".encode() + data).hexdigest(),
                         self.report["world12_git_blob"])
        expected = [(r["floor"], r["xy"], r["destination"], r["create_block_sha256"])
                    for r in self.world12["routes"] if r["destination"][0] in {100, 200}]
        actual = [(r["village"], r["exit_xy"], r["destination"], r["create_block_sha256"])
                  for r in self.report["arrivals"]]
        self.assertEqual(actual, expected)
        self.assertEqual(Counter(r[0] for r in actual), {2000: 8, 3000: 10, 4000: 4})

    def test_each_arrival_replays_all_containing_rectangles(self):
        areas = self.report["area_rectangles"]
        self.assertEqual(len(areas), 158)
        self.assertEqual(len({area["id"] for area in areas}), len(areas))
        self.assertEqual([a["id"] for a in areas if a["rectangle"][0] > a["rectangle"][2]], [94])
        expected = {2000: [28, 36, 64], 3000: [87, 88], 4000: [95]}
        for arrival in self.report["arrivals"]:
            floor, x, y = arrival["destination"]
            actual = []
            for area in areas:
                left, top, right, bottom = area["rectangle"]
                if (floor == area["floor"] and min(left, right) <= x <= max(left, right)
                        and min(top, bottom) <= y <= max(top, bottom)):
                    actual.append(area["id"])
            self.assertEqual(actual, arrival["area_ids"])
            self.assertEqual(actual, expected[arrival["village"]])

    def test_group_and_enemy_slots_close_without_filling_group_799(self):
        report = self.report
        matched = {area["id"]: area["group_slots"] for area in report["matched_area_fields"]}
        self.assertEqual(set(matched), {area for r in report["arrivals"] for area in r["area_ids"]})
        self.assertEqual(matched[36], [])
        self.assertEqual(matched[87][-1], [6, 799, 45])
        self.assertEqual(report["setup_file_selections"]["groupfile"], "./data/group1.txt")
        self.assertEqual(report["group_799_alternate_table_matches"], 0)
        groups, enemies, templates = (report[k] for k in ("groups", "enemies", "templates"))
        self.assertEqual(set(groups), {str(k) for slots in matched.values() for _, k, _ in slots})
        self.assertEqual(len(groups), 24)
        self.assertEqual({k: len(v) for k, v in groups.items() if len(v) != 1}, {"799": 0})
        self.assertEqual(set(enemies), {str(k) for rows in groups.values() for row in rows
                                        for _, k, _ in row["enemy_slots"]})
        self.assertEqual(set(templates), {str(row["template"]) for rows in enemies.values() for row in rows})
        self.assertEqual((len(enemies), len(templates)), (19, 9))
        self.assertTrue(all(len(rows) == 1 for rows in (*enemies.values(), *templates.values())))

    def test_logging_gate_and_reward_stay_in_the_selected_source_tables(self):
        report = self.report
        relation = report["logging_relation"]
        self.assertEqual([relation[k] for k in ("area", "group", "appearance_item", "enemy", "template")],
                         [88, 414, 2478, 563, 531])
        area = next(a for a in report["matched_area_fields"] if a["id"] == 88)
        self.assertEqual(area["group_slots"][-1], [4, 414, 3])
        group, = report["groups"]["414"]
        self.assertEqual(group["item_gate_fields"], [2478, -1])
        self.assertEqual(group["enemy_slots"], [[1, 563, 1]])
        enemy, = report["enemies"]["563"]
        self.assertEqual((enemy["template"], enemy["pet_flag"]), (531, 0))
        self.assertEqual(relation["template_name"], "木")
        self.assertEqual(relation["enemy_drop_slots"], [[1, 2468, 700]])
        self.assertEqual({k: item["name"] for k, item in relation["items"].items()},
                         {"2478": "採伐許可證", "2468": "良質的木材"})
        self.assertTrue(all(report["setup_file_selections"][f"itemset{i}file"] == "data/itemset.txt"
                            for i in (3, 4, 5, 6)))

    def test_source_limits_are_explicit(self):
        self.assertEqual(self.report["source_scope"], "LATER_COMMUNITY_MIXED25_SAME_PRESERVED_ARCHIVE_STATIC")
        self.assertEqual(self.report["bounds"], {
            "native_area_selection_proven": False, "native_encounter_executed": False,
            "official_same_deployment_proven": False, "raw_weights_are_probabilities": False,
            "world12_DAT_reread_successfully": False,
        })
