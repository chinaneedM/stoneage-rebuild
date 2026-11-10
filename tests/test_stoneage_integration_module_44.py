"""Public Git-derived source guards for the private Jaruga A1 visual recovery.

This CI never holds original DAT, RD, proprietary PNG, scripts or native executables.
"""
import copy
import hashlib
import json
from pathlib import Path
import unittest

DATA = Path(__file__).resolve().parents[1] / "research" / "recovered"

def load(name):
    raw = (DATA / name).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()
    return json.loads(raw), blob

class Integration44A1SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r, _ = load("STONEAGE-INTEGRATION44-JARUGA-A1-ORIGINAL-SOURCE-PIXELS-R1.json")
        cls.q, cls.qblob = load("STONEAGE-QUEST25-FOUR-ISLAND-TOUR-ROUTES-SOURCE-R1.json")
        cls.i41, cls.i41blob = load("STONEAGE-INTEGRATION41-JARUGA-ROUTE-B-CHECKPOINTS-SOURCE-R1.json")
        cls.i42, cls.i42blob = load("STONEAGE-INTEGRATION42-JARUGA-REGISTRATION-ORIGINAL-TILES-R1.json")
        cls.i43, cls.i43blob = load("STONEAGE-INTEGRATION43-JARUGA-A6-FINISH-SOURCE-BOUNDARY-R1.json")
        cls.a = next(x for x in cls.q["routes"] if x["label"]=="A")
        cls.a1 = next(x for x in cls.a["checkpoints"] if x["number"]==1)

    def validate_boundaries(self, row):
        self.assertEqual(row["stage_A"], {"PARTIAL":7,"OPEN":2})
        self.assertEqual(row["stage_B"], "GATED")
        self.assertEqual(row["wiki"], "GATED")
        self.assertEqual(row["R79"], "PAUSED_NON_BLOCKING")
        self.assertIsNone(row["overall_percent"])
        self.assertTrue(row["boundaries"])
        for value in row["boundaries"].values():
            self.assertIs(value,False)

    def test_exact_prior_git_blob_inputs(self):
        self.assertEqual(self.r["source_git_blobs"], {
            "QUEST25":self.qblob,"INTEGRATION41":self.i41blob,
            "INTEGRATION42":self.i42blob,"INTEGRATION43":self.i43blob})
        self.assertEqual(self.r["current_preserved_blob"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")

    def test_a1_true_create_script_path_coordinates_and_proof(self):
        src=self.a1["source"];new=self.r["A1_source"]
        for target,original in [("floor","floor"),("borncorner","borncorner"),
          ("create_path","create_path"),("create_ordinal","create_ordinal"),
          ("graphic_alias","graphic_alias"),("template_path","template_path"),
          ("functionset","functionset"),("script_path","script_path")]:
            self.assertEqual(new[target],src[original])
        self.assertEqual(new["create_block_sha256"],src["block_sha256"])
        self.assertEqual(new["borncorner"],[99,64,99,64])
        self.assertEqual((new["proof_incoming"],new["proof_outgoing"]),
                         (self.a1["incoming_item"],self.a1["outgoing_item"]))
        self.assertEqual((new["proof_incoming"],new["proof_outgoing"]),(2552,2553))

    def test_static_five_type_source_segments_never_native_execution(self):
        src=self.r["A1_source"]
        old=next(x for x in self.q["source_scripts"] if x["path"]==src["script_path"])
        self.assertEqual(src["script_sha256"],old["sha256"])
        self.assertEqual(len(src["script_events"]),len(old["events"]))
        for n,e in zip(src["script_events"],old["events"]):
            self.assertEqual(n["ordinal"],e["ordinal"])
            self.assertEqual(n["condition"],e["condition_literal"])
            self.assertEqual(n["section_sha256"],e["section_sha256"])
            self.assertEqual(n["commands"],e["commands"])
        self.assertEqual(src["script_events"][0]["commands"],
                         {"GetItem":["2553"],"DelItem":["2552"]})
        self.assertEqual(src["script_events"][0]["condition"],"LV>0&ITEM=2552")
        self.assertFalse(self.r["boundaries"]["native_quest_reward_execution_verified"])

    def test_map3000_identity_bound_to_original_I41_DAT(self):
        original=next(m for m in self.i41["map_files"] if m["floor"]==3000)
        self.assertEqual(self.r["verified_original_members"]["mixed25_map3000_DAT"],
                         original["sha256"])
        self.assertEqual(self.r["actual_map_A1_window"]["dimensions"],[150,150])
        self.assertEqual(self.r["actual_map_A1_window"]["center"],[99,64])
        self.assertEqual(self.r["actual_map_A1_window"]["bounds"],[94,59,104,69])
        self.assertEqual(self.r["actual_map_A1_window"]["grid_cells"],121)
        self.assertEqual(self.r["actual_map_A1_window"]["center_three_u16"],
                         [2022,32,49152])
        self.assertEqual(self.r["actual_map_A1_window"]["gt99_occurrences"],132)
        self.assertEqual(self.r["actual_map_A1_window"]["distinct_aliases"],73)
        self.assertEqual(self.r["actual_map_A1_window"]["low_1_to_99_values"],24)
        self.assertEqual(self.r["actual_map_A1_window"]["unmatched_gt99_occurrences"],0)
        self.assertEqual(self.i42["full_floor_3000"]["source_dimensions"],[150,150])

    def test_8335_original_RD_matches_earlier_catalogue_not_unproven_physical_alias(self):
        a,b=self.r["pixel_sources"]["new_RD"]
        self.assertEqual(a["alias"],8335)
        self.assertEqual(a["physical"],3583)
        self.assertEqual(a["offset"],5411670)
        self.assertEqual(a["bytes"],1659)
        self.assertEqual(a["RD_sha256"],
                         "fa8c5402b421f3084cec8f8f56bcf4ec6b11b50835878926f0e275867c22c4a6")
        self.assertEqual(a["RGBA_sha256"],
                         "3ad23908f6767cdfde706f1274c6e137c190a102ab356d958d7c98709f51d67a")
        self.assertEqual(b["alias"],16068)
        self.assertEqual(b["physical"],5914)
        self.assertEqual(b["dimensions"],[32,78])
        self.assertEqual(b["offset"],25056189)
        self.assertEqual(b["bytes"],1694)
        self.assertNotEqual(a["RD_sha256"],b["RD_sha256"])
        self.assertEqual(self.r["pixel_sources"]["previous_I41_original_RGBA_aliases"]+
                         self.r["pixel_sources"]["previous_MAP04_original_RGBA_aliases"]+
                         self.r["pixel_sources"]["current_TW1_REAL_double_decoded_map_aliases"],73)
        self.assertFalse(self.r["boundaries"]["original_NPC_actor_direction_verified"])

    def test_private_source_and_archived_replay_custody(self):
        archive=self.r["archive_SHA256"]
        self.assertEqual(archive["INTEGRATION41"],self.i41["source_archives"]["INTEGRATION41"]["sha256"]
                         if "INTEGRATION41" in self.i41["source_archives"] else self.i41["private_archive"]["sha256"])
        self.assertEqual(archive["INTEGRATION42"],self.i42["private_archive"]["sha256"])
        self.assertEqual(archive["TW1_P3H"],self.i41["source_archives"]["P3H"]["sha256"])
        self.assertEqual(archive["MAP04"],self.i41["source_archives"]["MAP04"]["sha256"])
        self.assertEqual(self.r["private_custody"]["zip_SHA256"],
                         "330e3568d9cba88ed8f42ffa410a29b7f40021aa3860e003fbc6ddc400114df1")
        self.assertEqual(self.r["private_custody"]["private_full_derived_JSON_SHA256"],
                         "9d99db924be7a4bebda3a8133974527f2b84d50f5b7c727079e2dbf7053a62e2")
        self.assertTrue(self.r["private_custody"]["Library_upload_and_readback_exact_SHA"])
        self.assertEqual(self.r["private_custody"]["private_independent_replay"],
                         {"cells":121,"source_high_refs":132,"distinct_aliases":73,
                          "low_unknown":24,"full_RGBA_modes":3})

    def test_pixel_hashes_are_bounded_to_modern_compositor(self):
        cand=self.r["candidate_scene"]
        self.assertEqual(cand["size"],[736,745])
        self.assertEqual(cand["actual_source_ref_occurrences"],132)
        self.assertTrue(cand["Pillow_vs_NumPy_full_RGBA_equal"])
        self.assertEqual(len(set(cand["frames_RGBA_SHA256"].values())),3)
        self.assertFalse(self.r["boundaries"]["original_scene_palette_layer_collision_verified"])
        self.assertFalse(self.r["boundaries"]["same_official_deployment_verified"])
        self.assertFalse(self.r["boundaries"]["private_binary_or_pixel_published"])

    def test_negative_evidence_must_fail_when_tampered(self):
        self.validate_boundaries(self.r)
        for forbidden in ("original_client_executed","same_official_deployment_verified",
                          "native_quest_reward_execution_verified","original_map4000_recovered"):
            t=copy.deepcopy(self.r)
            t["boundaries"][forbidden]=True
            with self.assertRaises(AssertionError):
                self.validate_boundaries(t)
        t=copy.deepcopy(self.r)
        t["overall_percent"]=100
        with self.assertRaises(AssertionError):
            self.validate_boundaries(t)

if __name__=="__main__":unittest.main()
