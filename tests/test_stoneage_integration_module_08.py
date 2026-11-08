"""INTEGRATION08: test source qualification only; do not claim native game movement."""
from __future__ import annotations
import hashlib
import json
from collections import Counter
from pathlib import Path
import unittest

REC = Path(__file__).resolve().parents[1] / "research" / "recovered"
OUT = REC / "STONEAGE-INTEGRATION08-FLOOR1000-19-CREATE-ORIGINAL-SOURCE-R1.json"

def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

class Floor1000QualifiedSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(OUT.read_text("utf8"))
        cls.data = {}
        for key, pin in cls.r["source_pins"].items():
            file = REC / Path(pin["path"]).name
            raw = file.read_bytes()
            assert git_blob(raw) == pin["git_blob_sha"], key
            cls.data[key] = json.loads(raw)
        cls.rows = cls.r["source_creates"]
        cls.q = cls.data["q"]
        cls.ch = cls.data["ch"]
        cls.original_creates = {(r[0],r[1]):r for r in cls.ch["create_rows"]}
        cls.original_files = {r[0]:r for r in cls.ch["source_files"]}

    def test_01_exact_source_archive_boundary_and_DAT(self):
        self.assertEqual(self.q["source_original_mixed25_RAR_sha256"],self.ch["original_rar_sha256"])
        self.assertEqual(self.ch["original_rar_sha256"],self.r["source_parent_RAR_sha256"])
        old=self.data["map"]["source_three_floors"]["1000"]
        self.assertEqual(self.r["floor_1000_original_DAT"],
            dict(sha256=old["dat_sha256"],bytes=old["dat_bytes"],width=160,height=160,
                 cells=25600,original_source=old["source_origin"]))

    def test_02_all_19_exact_SHA_scope_and_original_parameters(self):
        refs=self.q["source_CREATE_references"]
        self.assertEqual(len(self.rows),19)
        self.assertEqual(len({r["q05_ref_index"] for r in self.rows}),19)
        for r in self.rows:
            q=refs[r["q05_ref_index"]]
            c=self.original_creates[(r["create_file"],r["create_ordinal"])]
            self.assertEqual(c[5],1000)
            sha=self.original_files[r["create_file"]][2] if r["sha_scope"]=="WHOLE_CREATE_FILE" else c[4]
            self.assertEqual(sha,q["source_CREATE_sha256"])
            self.assertEqual((r["original_block_sha256"],r["graphic_alias"],r["borncorner_int4"],
                r["borncenter_int4"],r["createnum_int"],r["direction_original_int"]),
                (c[4],c[6],c[7],c[8],c[9],c[10]))
            self.assertEqual((r["original_param_file"],r["original_param_sha256"]),
                (c[15][0][0],c[15][0][2]))
            self.assertEqual(q["source_parameter_file"],r["original_param_file"])

    def test_03_classify_original_functions_not_NPC_populations(self):
        x=self.r["summary"]
        self.assertEqual(x["by_cohort"],{"QUEST01":7,"QUEST02":2,"QUEST03":10})
        self.assertEqual(x["by_source_function"],{"npcgen_changeevent":7,"npcgen_warp":2,"npcgen_timeman":10})
        self.assertEqual(x["distinct_original_graphic_aliases"],18)

    def test_04_borncorner_and_borncenter_cannot_be_silently_interchanged(self):
        x=self.r["summary"]
        self.assertEqual((x["with_original_borncorner_int4"],x["with_original_borncenter_int4"],
                          x["without_borncorner_but_with_borncenter"],
                          x["without_either_original_location_field"]),(17,2,1,1))
        corner=[r for r in self.rows if r["borncorner_int4"] is not None]
        self.assertEqual(len({tuple(r["borncorner_int4"][:2]) for r in corner}),17)
        self.assertTrue(all(c["borncorner_int4"]==[c["borncorner_int4"][0],
                            c["borncorner_int4"][1],c["borncorner_int4"][0],
                            c["borncorner_int4"][1]] for c in corner))
        self.assertTrue(x["all_borncorner_xy_inside_original_DIM"])
        self.assertTrue(all(0<=r["borncorner_int4"][0]<160 and
                            0<=r["borncorner_int4"][1]<160 for r in corner))
        self.assertIsNone(next(r for r in self.rows if r["original_param_file"]=="sa60/newbie/fighter")["borncenter_int4"])

    def test_05_QUEST25_three_existing_script_CREATEs_not_new_quests(self):
        before=self.data["q25"]["source_creates"]
        report=self.r["already_verified_crossmodule_spot_checks"]["QUEST25"]
        self.assertEqual(len(report),3)
        for z in report:
            v=next(x for x in before if x["floor"]==1000 and x["create_path"]==z["create_file"]
                   and x["create_ordinal"]==z["ordinal"])
            self.assertEqual((v["block_sha256"],v["script_path"],v["borncorner"]),
                (z["block_sha256"],z["script_path"],z["borncorner"]))
            p=next(x for x in self.rows if x["create_file"]==z["create_file"] and x["create_ordinal"]==z["ordinal"])
            self.assertEqual(p["original_block_sha256"],z["block_sha256"])

    def test_06_QUEST26_one_shell_flower_source_on_this_floor(self):
        before=self.data["q26"]["source_creates"]
        report=self.r["already_verified_crossmodule_spot_checks"]["QUEST26"]
        self.assertEqual(len(report),1)
        v=next(x for x in before if x["floor"]==1000)
        self.assertEqual((v["block_sha256"],v["script_path"],v["borncorner"]),
                         (report[0]["block_sha256"],report[0]["script_path"],report[0]["borncorner"]))
        self.assertIn(v["script_path"],[x["original_param_file"] for x in self.rows])

    def test_07_one_existing_GetPet_source_not_native_delivery(self):
        b=self.r["already_verified_crossmodule_spot_checks"]["INTEGRATION05"]
        self.assertEqual(len(b),1)
        prior=next(x for x in self.data["i05"]["rows"] if x["source_floor_id"]==1000)
        self.assertEqual(b[0]["original_GetPet_literals"],prior["original_GetPet_numeric_literals_ordered"])
        self.assertFalse(b[0]["actually_rewarded"])

    def test_08_13_14_TW1_numeric_candidates_not_100_percent_pixels(self):
        f=next(x for x in self.data["vis"]["per_floor_source_qualification"] if x["floor_id"]==1000)
        z=f["original_TW10_RD_pixel_candidate_join"]
        self.assertEqual((z["nonzero_numeric_references"],z["tw10_verified_RD_numeric_candidate_references"],
                          z["unmatched_tw10_verified_RD_references"]),(26324,26310,14))
        self.assertEqual(self.r["summary"]["prior_TW1_cross_carrier_unmatched_image_references"],14)
        self.assertTrue(self.r["source_rendering_qualification"]["TW1_RD_is_only_cross_carrier_numeric_candidate"])

    def test_09_no_false_natively_running_or_official_identity(self):
        self.assertFalse(self.r["limits"]["original_client_running"])
        self.assertFalse(self.r["limits"]["original_quest_or_warp_executed"])
        self.assertFalse(self.r["limits"]["actual_early_official_same_deployment_proven"])
        self.assertFalse(self.r["source_rendering_qualification"]["original_collision_or_walkable_route_proven"])
        self.assertEqual(self.r["status"],"SOURCE_BOUNDED_PARTIAL")
        self.assertIsNone(self.r["limits"]["overall_percent"])

if __name__=="__main__":
    unittest.main()
