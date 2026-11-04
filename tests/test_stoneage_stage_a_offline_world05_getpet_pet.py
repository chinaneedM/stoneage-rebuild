"""WORLD05 derived-only cross-check: GETPET -> enemy instance -> template -> SPR.
This test cannot replay private original RAR bytes or native gameplay.
"""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1] / "research" / "recovered"
def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

class World05SourceGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = load("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-05-GETPET-INSTANCE-TEMPLATE-SPR-R1.json")
        cls.quest = load("STONEAGE-INTEGRATION01-NPC-PET-QUEST-ITEM-MAP-SOURCE-GRAPH-R1.json")
        cls.pet = load("STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json")
        cls.by = {k: {r[1]: r for r in cls.pet["source_rows"][k]}
                  for k in ("enemy.txt", "enemy2.txt", "enemybase.txt", "enemybase2.txt")}
        cls.spr = {}
        for row in cls.pet["source_rows"]["spradrn_5.bin"]:
            cls.spr.setdefault(row[1], []).append(row)

    def test_original_getpet_create_script_source_is_conserved(self):
        original = self.quest["source_GetPet_CREATE_QUEST_script_AND_floor_joins"]
        rows = self.world["CREATE_QUEST_GETPET_rows"]
        self.assertEqual((len(rows), len(set(x["QUEST_script_path"] for x in rows))), (24, 23))
        self.assertEqual(len(original), len(rows))
        for row, src in zip(rows, original):
            self.assertEqual((row["original_CREATE_file"], row["CREATE_ordinal"],
                              row["CREATE_block_sha256"], row["QUEST_script_path"],
                              row["QUEST_script_original_sha256"], row["CREATE_floor_id"],
                              row["GETPET_original_script_line_numbers"],
                              row["GETPET_numeric_literals_in_source_order"],
                              row["source_origin_class"]),
                             (src["original_CREATE_file"], src["original_CREATE_ordinal"],
                              src["source_CREATE_block_sha256"], src["script_path"],
                              src["script_original_sha256"], src["floor_id"],
                              src["source_GETPET_command_lines"],
                              src["source_GETPET_numeric_literals_ordered"],
                              src["source_quest_origin_class"]))
        self.assertEqual(sum(len(x["GETPET_numeric_literals_in_source_order"]) for x in rows), 41)
        self.assertEqual(sorted(set(i for x in rows for i in x["GETPET_numeric_literals_in_source_order"])),
                         [x["source_GETPET_literal_numeric"] for x in self.world["GETPET_instance_template_graph"]])

    def test_real_instance_foreign_key_not_same_number_template_join(self):
        rows = self.world["GETPET_instance_template_graph"]
        self.assertEqual(len(rows), 36)
        direct_collisions = 0
        for r in rows:
            number = r["source_GETPET_literal_numeric"]
            ea, eb = self.by["enemy.txt"][number], self.by["enemy2.txt"][number]
            self.assertNotEqual(number, ea[2])
            self.assertEqual(ea[2], eb[2])
            for name, instance, base in (("A", ea, self.by["enemybase.txt"][ea[2]]),
                                         ("B", eb, self.by["enemybase2.txt"][eb[2]])):
                d = r["enemy_instance_" + name]
                t = r["template_" + name]
                self.assertEqual([d["source_row_1based"], d["instance_id"],
                                  d["reference_template_id"], d["normalized_fields_sha256"]],
                                 [instance[0], instance[1], instance[2], instance[4]])
                self.assertEqual([t["source_row_1based"], t["template_id"], t["graphic_id"],
                                  t["PETFLG"], t["normalized_fields_sha256"]],
                                 [base[0], base[1], base[2], base[3], base[16]])
            self.assertEqual(r["template_A"]["graphic_id"], r["template_B"]["graphic_id"])
            sprite = self.spr[r["template_A"]["graphic_id"]]
            self.assertEqual(len(sprite), 1)
            self.assertEqual(r["preserved_SPR_index"]["exact_index_occurrences"], 1)
            self.assertEqual(r["preserved_SPR_index"]["source_record_ordinal"], sprite[0][0])
            self.assertEqual(r["direct_numeric_template_id_collision_in_A"],
                             number in self.by["enemybase.txt"])
            if number in self.by["enemybase.txt"]:
                direct_collisions += 1
                self.assertNotEqual(self.by["enemybase.txt"][number][1],
                                    r["template_A"]["template_id"])
        self.assertEqual(direct_collisions, 26)
        self.assertEqual(self.by["enemy.txt"][54][2], 91)
        self.assertEqual(self.by["enemybase.txt"][91][2], 100287)
        self.assertNotEqual(self.by["enemybase.txt"][54][2], 100287)

    def test_all_3_conflicting_petflag_values_and_no_master_promotion(self):
        rows = self.world["GETPET_instance_template_graph"]
        conflicts = [(r["source_GETPET_literal_numeric"], r["template_A"]["template_id"],
                      r["template_A"]["PETFLG"], r["template_B"]["PETFLG"],
                      r["template_A"]["graphic_id"])
                     for r in rows if r["template_A"]["PETFLG"] != r["template_B"]["PETFLG"]]
        self.assertEqual(conflicts, [(1479, 718, 1, 0, 100451),
                                     (1481, 719, 1, 0, 100401),
                                     (1483, 720, 1, 0, 100432)])
        self.assertEqual(self.world["summary"]["instance_row_hash_different_between_alternatives"], 36)
        self.assertEqual(self.world["summary"]["template_row_hash_identical_between_alternatives"], 1)
        self.assertEqual(self.world["summary"]["PETFLG_source_conflicts"], 3)
        self.assertEqual([x["template_id"] for x in self.world["alternate_PETFLG_conflicts"]],
                         [718, 719, 720])

    def test_historical_status_and_rights_boundaries(self):
        w = self.world
        self.assertEqual(w["provenance"]["parent_RAR_sha256"],
                         self.pet["preserved_original_rar"]["sha256"])
        self.assertEqual(w["stage_A"], "7_PARTIAL_2_OPEN")
        self.assertEqual((w["stage_B"], w["wiki"], w["R79"]), ("GATED", "GATED", "PAUSED_NON_BLOCKING"))
        self.assertIsNone(w["overall_percent"])
        self.assertFalse(w["evidence_limits"]["original_bytes_reopened_in_this_unit"])
        self.assertTrue(all(v for k, v in w["evidence_limits"].items()
                            if k != "original_bytes_reopened_in_this_unit"))
        for row in w["GETPET_instance_template_graph"]:
            self.assertNotIn("original_name", row)
            self.assertNotIn("original_pixel", row)
        self.assertEqual(w["historical_CURRENT_Git_blob_sha"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")

if __name__ == "__main__":
    unittest.main()
