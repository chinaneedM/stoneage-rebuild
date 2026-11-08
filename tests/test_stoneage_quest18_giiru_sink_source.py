"""QUEST18 published source-bounded numeric/identity crosswalk checks. No proprietary bytes required."""
import collections
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))
def report():
    return load("research/recovered/STONEAGE-QUEST18-GIIRU-SINK-SOURCE-R1.json")
def earlier():
    return load("research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json")

class Quest18SourceBounds(unittest.TestCase):
    def test_exact_existing_create_and_script_sha(self):
        r, q = report(), earlier()
        cr = [x for x in q["source_creation_references"] if x["create_source_path"] == r["original_create"]["path"]]
        self.assertEqual(len(cr), 12)
        self.assertEqual({x["create_source_sha"] for x in cr}, {r["original_create"]["sha256"]})
        scripts = {x["path"]: x for x in r["original_script_rows"]}
        self.assertEqual(len(scripts), 11)
        self.assertEqual({x["original_script_path"] for x in cr}, set(scripts))
        old = {x["path"]:x for x in q["source_scripts"]}
        for path, row in scripts.items():
            self.assertEqual(old[path]["original_sha256"], row["original_sha256"])
            self.assertEqual(old[path]["original_size"], row["original_bytes"])
            self.assertEqual(old[path]["actual_block_type_counts"], row["type_counts"])
        self.assertEqual([x["original_script_path"] for x in cr].count("giiru/event/sink/sink06"), 2)
        self.assertEqual(sum(x["event_blocks"] for x in scripts.values()), 79)

    def test_all_79_old_block_provenance_and_operations(self):
        r, q = report(), earlier()
        paths = {x["path"] for x in r["original_script_rows"]}
        selected = [x for x in q["source_event_blocks"] if x["script_path"] in paths]
        self.assertEqual(len(selected),79)
        per_script = collections.Counter(x["script_path"] for x in selected)
        commands = collections.Counter()
        for x in selected:
            self.assertTrue(x["source_section_decoded_cp950_normalized_UTF8_sha256"])
            for name in r["original_source_command_totals"]:
                commands[name] += x["source_operations"].get(name, 0)
        for x in r["original_script_rows"]:
            self.assertEqual(per_script[x["path"]],x["event_blocks"])
        self.assertEqual(dict(commands),r["original_source_command_totals"])

    def test_real_numeric_warp_lists_not_executed_routes(self):
        r, maps = report(), load("research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json")
        patterns = r["repeated_NpcWarp_lists"]
        count = sum(x["literal_NpcWarp_count"] for x in patterns)
        candidates = sum(x["literal_NpcWarp_count"]*len(x["one_verified_repeated_candidate_list"]) for x in patterns)
        triples = {tuple(t) for x in patterns for t in x["one_verified_repeated_candidate_list"]}
        self.assertEqual((count,candidates,len(triples)),(37,220,26))
        self.assertEqual(sorted({f for f,_,_ in triples}),r["warp_result"]["unique_destination_floors"])
        for floor, x, y in triples:
            geometry = maps["maps"][str(floor)]["geometry"]
            self.assertTrue(0 <= x < geometry[0] and 0 <= y < geometry[1])
        for actor in r["active_changeevent_npc_rows"]:
            if actor["floor"] in [300]: continue
            w,h = maps["maps"][str(actor["floor"])]["geometry"]
            self.assertTrue(0<=actor["xy"][0]<w and 0<=actor["xy"][1]<h)
        self.assertNotIn("300", maps["maps"])

    def test_item_ids_against_both_public_original_row_hashes(self):
        r=report()
        rows={}
        for part in range(1,8):
            path=f"research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{part:02d}-R1.json"
            for row in load(path)["rows"]:
                rows[row[0]]=row
        ids=r["item_result"]["source_ids"]
        self.assertEqual(len(ids),44)
        for item in ids:
            row=rows[item]
            self.assertIsNotNone(row[1])
            self.assertEqual(row[1],row[2])
            self.assertEqual(row[3],row[4])
            if item==2614:
                self.assertNotEqual(row[8],"REAL_RD_DECODED_CROSS_CARRIER")
            else:
                self.assertEqual(row[8],"REAL_RD_DECODED_CROSS_CARRIER")
        v=r["item_result"]["water_vessel_item_id_to_literal_fullness"]
        self.assertEqual(v["2710"],v["2714"])
        self.assertEqual(v["2711"],v["2715"])
        self.assertNotEqual(v["2709"],v["2710"])

    def test_unreferenced_siblings_and_false_official_promotion(self):
        r,q=report(),earlier()
        for basename in r["original_create"]["source_only_unreferenced_siblings"]:
            path="giiru/event/sink/"+basename
            self.assertFalse(any(x["original_script_path"]==path for x in q["source_creation_references"]))
        self.assertTrue(r["existing_source_index"]["not_newly_discovered_events"])
        for k in ("native_NPC_world_entry","native_quest_transaction","native_NpcWarp_selection_or_collision","TW1_official_same_deployment","original_JSS1999_identity"):
            self.assertFalse(r["boundaries"][k])
        self.assertIsNone(r["boundaries"]["overall_percent"])

if __name__=="__main__":
    unittest.main()
