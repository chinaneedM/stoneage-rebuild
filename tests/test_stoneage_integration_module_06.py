"""INTEGRATION06: source-bound MAP1300 versus failed DAT and six NPC source refs."""
import hashlib
import json
from pathlib import Path
import unittest

BASE = Path(__file__).resolve().parents[1] / "research/recovered"
SOURCES = {
    "map": [
        "STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json",
        "03675ee98d391f9ef0246315b2426f2a8b721fd3"
    ],
    "q05": [
        "STONEAGE-QUEST05-598-ORIGINAL-CREATE-FLOOR-MAP-AND-WARP-CROSSWALK-R1.json",
        "b004e488e1d0a93ca7c14eb90abb584b23f341fe"
    ],
    "q19": [
        "STONEAGE-QUEST19-MARJU-POST-TREASUREBAG-SOURCE-R1.json",
        "ea0dc007016e4857550b76a1073cdbbd7975f00c"
    ],
    "q25": [
        "STONEAGE-QUEST25-FOUR-ISLAND-TOUR-ROUTES-SOURCE-R1.json",
        "a52b4e5519912ac7e46e1f892cc01515861cf2e8"
    ],
    "q27": [
        "STONEAGE-QUEST27-AXE-LETTER-EVENT3-5-SOURCE-R1.json",
        "0054d4d716f99f56d58fc1a1729d70275b823e44"
    ],
    "q31": [
        "STONEAGE-QUEST31-FOUR-VILLAGE-EVENT09-12-SOURCE-R1.json",
        "0a17857fc55fd5884963d1c00ffeb292ebc9f59b"
    ]
}
OUTPUT = BASE / "STONEAGE-INTEGRATION06-MAP1300-MAP-DAT-SIX-CREATE-SOURCE-R1.json"

def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

def original_sources():
    d = {}
    for key,(name,sha) in SOURCES.items():
        raw=(BASE/name).read_bytes()
        assert git_blob(raw)==sha, key+" original pinned Git blob changed"
        d[key]=json.loads(raw)
    return d

class Original1300CrossModuleSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.published=json.loads(OUTPUT.read_text(encoding="utf-8"))
        cls.inputs=original_sources()

    def test_01_MAP_source_is_two_identical_qualified_original_rows(self):
        m=self.inputs["map"]
        rows=sorted((x for x in m["original_decoded_source_rows"] if x[1]=="1300.MAP"),key=lambda x:x[0])
        self.assertEqual([x[0] for x in rows],[0,1])
        self.assertEqual([x[2] for x in rows],[20008,20008])
        self.assertEqual(len({x[3] for x in rows}),1)
        self.assertEqual([x[6:8] for x in rows],[[100,100],[100,100]])
        self.assertEqual([x["original_sha256"] for x in self.published["original_MAP_rows"]],[x[3] for x in rows])

    def test_02_DAT_is_recorded_failed_member_not_a_proven_absence(self):
        m=self.inputs["map"]
        rows=[x for x in m["source_extraction_errors_not_reclassified_as_corruption"] if x[1]=="1300.DAT"]
        self.assertEqual(rows,[[0,"1300.DAT",60008,0,"File CRC error"]])
        self.assertEqual(self.published["original_DAT_extraction_errors"][0]["expected_original_member_bytes"],60008)
        self.assertFalse(self.published["conclusions"]["source_DAT_corruption_proven"])
        self.assertFalse(self.published["conclusions"]["DAT_absent_from_parent_RAR"])
        self.assertFalse(self.published["conclusions"]["fully_qualified_1300_DAT_currently"])

    def test_03_same_source_archive_and_six_exact_CREATE_references(self):
        d=self.inputs["q05"]
        self.assertEqual(d["source_original_mixed25_RAR_sha256"],self.inputs["map"]["original_rar_sha256"])
        f=next(x for x in d["floors"] if x["source_floor_id"]==1300)
        self.assertEqual((f["source_CREATE_ref_count"],f["map_status"]),(6,"NO_MATCHING_DAT_IN_955"))
        self.assertIsNone(f["source_DAT_sha256"])
        src=[x for x in d["source_CREATE_references"] if x["source_floor_id"]==1300]
        self.assertEqual(len(src),6)
        expected=self.published["floor1300_source_create_records"]
        self.assertEqual([(x["source_CREATE_file"],x["source_CREATE_block_ordinal"],x["source_parameter_file"],x["source_parameter_sha256"]) for x in src],
          [(x["create_path"],x["create_block_ordinal"],x["parameter_path"],x["parameter_sha256"]) for x in expected])
        self.assertEqual([x["cohort"] for x in src],["QUEST01"]*4+["QUEST03"]*2)
        self.assertEqual(len({x["source_parameter_file"] for x in src}),5)

    def test_04_four_existing_quest_reports_confirm_source_floor_only(self):
        edges=self.published["source_bound_relationships"]
        q19=next(x for x in self.inputs["q19"]["npc_placements"] if x["script"]==edges["QUEST19"]["parameter_path"])
        self.assertEqual((q19["floor"],q19["graphic_alias"],q19["spawn_xy"]),(1300,16046,[70,51]))
        q25=next(x for x in self.inputs["q25"]["source_creates"] if x["script_path"]==edges["QUEST25"]["parameter_path"])
        self.assertEqual((q25["floor"],q25["graphic_alias"],q25["borncorner"][:2]),(1300,16068,[65,26]))
        q27=next(x for x in self.inputs["q27"]["source_creates"] if x["script_path"]==edges["QUEST27"]["parameter_path"])
        self.assertEqual((q27["floor"],q27["graphic_alias"],q27["borncorner"][:2]),(1300,16048,[18,42]))
        q31=next(x for x in self.inputs["q31"]["source_create_records"] if x["script_path"]==edges["QUEST31"]["parameter_path"])
        self.assertEqual((q31["floor"],q31["graphic_alias"],q31["borncorner_original_four_numbers"][:2]),(1300,16206,[65,65]))

    def test_05_cross_report_qualifications_stay_original_and_nonruntime(self):
        self.assertEqual([x["map_status"] for x in self.inputs["q25"]["source_map_metadata_reused"] if x["source_floor_id"]==1300],["NO_MATCHING_DAT_IN_955"])
        self.assertEqual([x["map_status"] for x in self.inputs["q27"]["source_map_metadata_reused"] if x["source_floor_id"]==1300],["NO_MATCHING_DAT_IN_955"])
        self.assertFalse(self.inputs["q31"]["unresolved_map_1300"]["original_map_proven_absent"])
        self.assertFalse(self.published["conclusions"]["native_NPC_spawn_seen"])
        self.assertFalse(self.published["conclusions"]["original_1300_world_rendered"])
        self.assertFalse(self.published["conclusions"]["early_official_same_deployment"])
        self.assertEqual(self.published["status"],"SOURCE_BOUNDED_PARTIAL")

if __name__=="__main__":
    unittest.main()
