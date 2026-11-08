"""INTEGRATION09: original static source joins only, never assert playable native path."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/recovered/STONEAGE-INTEGRATION09-REPRESENTATIVE-PLAYER-CONTENT-CHAIN-R1.json"
def blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class RepresentativeContentChain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(OUT.read_text("utf-8"))
        cls.src = {}
        for key, pin in cls.r["source_pins"].items():
            p = ROOT / pin["path"]
            raw = p.read_bytes()
            assert blob_sha(raw) == pin["git_blob_sha"], (key, p)
            cls.src[key] = json.loads(raw)

    def test_01_qualified_indoor_outdoor_DAT_not_simulated_map(self):
        r=self.r["map_evidence"]
        v=self.src["s15"]["views"]
        for floor, key in [(1001,"indoor_1001"),(1000,"outdoor_1000")]:
            src=next(x for x in v if x["floor"]==floor)
            self.assertEqual(r[key]["DAT_sha256"],src["source_DAT_sha256"])
            self.assertEqual(r[key]["dimensions"],[src["width"],src["height"]])
        self.assertEqual(r["outdoor_1000"]["DAT_sha256"],self.src["i08"]["floor_1000_original_DAT"]["sha256"])
        self.assertEqual(r["outdoor_1000"]["source_Q05_CREATE_subcohort_count"],len(self.src["i08"]["source_creates"]))

    def test_02_original_warp_pair_symmetry_not_executed(self):
        pair=self.src["s15"]["doorway_pair"]
        old=self.r["verified_static_relationships"]["preserved_warp_pair"]
        self.assertEqual(len(pair),2)
        for entry in pair:
            key="forward" if entry["source_floor"]==1001 else "reverse"
            a=old[key]
            self.assertEqual((a["floor"],a["xy"],a["destination_floor"],a["destination_xy"],a["original_block_sha256"]),
                             (entry["source_floor"],entry["source_xy"],entry["destination_floor"],entry["destination_xy"],entry["source_block"]["block_sha256"]))
        self.assertEqual((old["forward"]["xy"],old["forward"]["destination_xy"]),([10,15],[63,99]))
        self.assertFalse(old["native_traversal_proven"])

    def test_03_original_townperson_is_outside_Q05_special_subset(self):
        source=self.src["s22"]
        node=self.r["verified_static_relationships"]["nearby_townperson"]
        self.assertEqual(node["xy"],source["target"]["xy"])
        self.assertEqual(node["source_block_sha256"],source["target"]["create_block_sha256"])
        self.assertEqual(node["exact_message_sha256"],source["message"]["sha256"])
        self.assertEqual(node["coordinate_difference_from_outdoor_warp_landing"],[0,4])
        self.assertFalse(node["in_Q05_19_CREATE_subset"])
        self.assertFalse(any(x.get("borncorner_int4") and x["borncorner_int4"][:2]==node["xy"]
                             for x in self.src["i08"]["source_creates"]))
        self.assertFalse(source["native_dialogue_execution_verified"])

    def test_04_Q25_quest_routes_are_source_relationships_not_walkability(self):
        original={x["label"]:x for x in self.src["q25"]["routes"]}
        nodes=self.r["verified_static_relationships"]["floor1000_existing_task_nodes"]
        for label in ("C","D"):
            src=original[label]
            row=nodes["Q25_"+label]
            self.assertEqual((row["registration_floor"],row["registration_xy"],row["registration_script"]),
                             (src["registration"]["floor"],src["registration"]["borncorner"][:2],src["registration"]["script_path"]))
            self.assertEqual((row["finish_floor"],row["finish_xy"],row["finish_script"]),
                             (src["finish"]["floor"],src["finish"]["borncorner"][:2],src["finish"]["script_path"]))
            self.assertEqual(row["original_checkpoint_source_count"],len(src["checkpoints"]))
            self.assertFalse(row["native_quest_completion_proven"])

    def test_05_Q26_two_source_creates_and_flag2_not_reinterpreted(self):
        old=self.r["verified_static_relationships"]["floor1000_existing_task_nodes"]["Q26_exchange_pair"]
        for floor,key in [(1000,"floor1000"),(2000,"floor2000")]:
            src=next(x for x in self.src["q26"]["source_creates"] if x["floor"]==floor)
            self.assertEqual((old[key]["floor"],old[key]["xy"],old[key]["script"],old[key]["block_sha256"]),
                             (floor,src["borncorner"][:2],src["script_path"],src["block_sha256"]))
        self.assertEqual(old["original_flag2_control_rows"],len(self.src["q26"]["source_flag2_controls"]))
        self.assertFalse(old["flag2_runtime_meaning_verified"])

    def test_06_1300_real_MAP_six_CREATE_but_no_DAT(self):
        info=self.src["i06"]
        target=self.r["map_evidence"]["blocked_1300"]
        floor=next(x for x in self.src["i07"]["floors"] if x["floor_id"]==1300)
        self.assertEqual(target["source_CREATE_count"],len(info["floor1300_source_create_records"]))
        self.assertEqual(target["source_CREATE_count"],floor["quest05_source_CREATE_count"])
        self.assertEqual(target["source_i07_status"],floor["source_DAT_status"])
        self.assertEqual(target["known_DAT_read_failure"],info["original_DAT_extraction_errors"][0]["error_tag"])
        self.assertFalse(target["verified_DAT"])

    def test_07_historical_native_execution_and_percentage_remain_unproven(self):
        x=self.r["missing_for_native_play"]
        self.assertTrue(all(v is False for v in x.values()))
        self.assertEqual(self.r["status"],"SOURCE_BOUNDED_PARTIAL")
        self.assertIsNone(self.r["overall_percent"])
        self.assertEqual(self.r["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertFalse(self.r["verified_static_relationships"]["floor1000_existing_task_nodes"]["INTEGRATION05_existing_GetPet_literate"]["actually_delivered_in_native_game"])

if __name__=="__main__":
    unittest.main()
