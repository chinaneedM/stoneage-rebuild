"""O5 original-resource acceptance is source-only; never load proprietary art in CI."""
import copy
import unittest

from tools import stoneage_o5_source_contract as o5


class O5DerivedEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w, cls.r13, cls.r15, cls.o4 = o5.load()

    def test_valid_archived_private_original_evidence(self):
        r = o5.validate(self.w, self.r13, self.r15, self.o4)
        self.assertEqual(r["pet_original_frame_occurrences"], 352)
        self.assertEqual(r["pet_unique_source_PNGs"], 208)
        self.assertFalse(r["original_game_world_entered"])

    def test_seven_map_png_ids_are_immutable_bounded_source_join(self):
        self.assertEqual(self.w["source_join"]["original_identical_png_keys"],
                         [5000,5001,5002,5005,5007,5009,5015])
        self.assertTrue(all(str(k) in self.r15["resources"] for k in o5.EXPECTED_KEYS))
        self.assertEqual(self.r15["views"][0]["source_DAT_sha256"],
                         self.w["source_join"]["floor_1001_map_DAT_sha256"])

    def test_original_pet_group_frame_counts_and_repeated_positions(self):
        frames=[f[0] for g in self.r13["groups"] for a in g["animations"] for f in a["frames"]]
        self.assertEqual(len(frames),352)
        self.assertEqual(len(set(frames)),208)
        self.assertEqual(len(frames)-len(set(frames)),144)

    def test_source_durations_are_uninterpreted_words_not_fps(self):
        self.assertEqual(self.w["pet_source"]["duration_words_original_not_ms"],
                         {"100250":1000,"100251":1000,"100252":1400})
        self.assertFalse(self.w["historical_limits"]["original_frame_timing_ms_or_fps_authenticated"])

    def test_original_world_and_species_claims_are_not_promoted(self):
        self.assertFalse(any(self.w["historical_limits"].values()))
        self.assertFalse(self.r13["official_species_identity_authenticated"])
        self.assertFalse(self.r13["same_deployed_build_proven"])
        self.assertTrue(self.w["source_join"]["not_authenticated_same_retail_game_world"])

    def test_public_CI_only_reads_derived_and_not_private_sources(self):
        self.assertTrue(self.w["public_ci_reads_only_derived_metadata"])
        self.assertFalse(self.w["private_output"]["raw_original_png_DAT_RD_NPC_HTML_in_public_git"])
        self.assertEqual(self.w["actual_private_browser"]["external_http_requests"],0)

    def test_negative_wrong_DAT_source_sha(self):
        w=copy.deepcopy(self.w)
        w["source_join"]["floor_1001_map_DAT_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"DAT identity"):
            o5.validate(w,self.r13,self.r15,self.o4)

    def test_negative_wrong_original_png_identity_claim(self):
        w=copy.deepcopy(self.w)
        w["source_join"]["all_seven_original_png_sha256_equal"]=False
        with self.assertRaisesRegex(ValueError,"seven PNG"):
            o5.validate(w,self.r13,self.r15,self.o4)

    def test_negative_source_anim_bitmap_occurrence_removed(self):
        r=copy.deepcopy(self.r13)
        r["groups"][0]["animations"][0]["frames"].pop()
        with self.assertRaisesRegex(ValueError,"position counts"):
            o5.validate(self.w,r,self.r15,self.o4)

    def test_negative_false_bitmap_identity_count(self):
        w=copy.deepcopy(self.w)
        w["pet_source"]["unique_original_bitmap_pngs"]=209
        with self.assertRaisesRegex(ValueError,"unique bitmap"):
            o5.validate(w,self.r13,self.r15,self.o4)

    def test_negative_nonexistent_legacy_native_execution(self):
        w=copy.deepcopy(self.w)
        w["historical_limits"]["original_game_world_entered"]=True
        with self.assertRaisesRegex(ValueError,"unsupported original native"):
            o5.validate(w,self.r13,self.r15,self.o4)

    def test_negative_false_same_retail_world_deployment(self):
        w=copy.deepcopy(self.w)
        w["source_join"]["not_authenticated_same_retail_game_world"]=False
        with self.assertRaisesRegex(ValueError,"retail world claim"):
            o5.validate(w,self.r13,self.r15,self.o4)

    def test_negative_false_private_browser_success(self):
        w=copy.deepcopy(self.w)
        w["actual_private_browser"]["external_http_requests"]=1
        with self.assertRaisesRegex(ValueError,"browser claim"):
            o5.validate(w,self.r13,self.r15,self.o4)

    def test_negative_o4_old_independent_pixel_fingerprint_drift(self):
        w=copy.deepcopy(self.w)
        w["actual_private_browser"]["preserved_O4_independent_map_pixel_differences"]=5
        with self.assertRaisesRegex(ValueError,"original map pixel proof"):
            o5.validate(w,self.r13,self.r15,self.o4)


if __name__=="__main__":
    unittest.main()
