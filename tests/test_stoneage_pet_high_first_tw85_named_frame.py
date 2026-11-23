"""PET10 source-only negative guards for historically observed R30 frames and PET09 original names."""
import copy
import json
from pathlib import Path
import unittest
from tools.stoneage_pet_high_first_tw85_named_private_frame_join import ROOT, build, load

class TestPet10NamedPriorRealPixels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = load()
        cls.record = build(cls.sources)

    def test_named_original_sprite_and_frame_proof(self):
        r = self.record
        self.assertEqual(r["schema"], "stoneage.pet.high_first_10.tw85_named_previously_private_decoded_frames.r1")
        self.assertEqual(r["scope"], "CLASSIC_PC_ONLY")
        self.assertEqual(r["original_client_local_name_cp950"], "雷帝斯洛")
        self.assertEqual(r["local_source_entry_key"], "TW85-SOURCE-SPR-101501")
        self.assertEqual((r["original_spr_graphic_number_not_official_pet_id"],
                          r["original_spr_physical_index"],r["raw_animation_index"]),
                         (101501, 1185, 1))
        self.assertEqual(set(r["original_executable_routes"]), {"sa.exe","sb.exe","sc.exe","sd.exe"})
        self.assertEqual([x["original_bitmapno"] for x in r["previously_privately_decoded_original_frames"]],
                         list(range(303039,303047)))
        self.assertEqual(r["evidence_limits"]["earlier_private_pixel_observation_run"],40329157425)

    def test_portrait_separate_from_animation_and_unverified_pet_fields(self):
        r=self.record
        self.assertEqual(r["original_portrait_source"]["logical_alias"],28429)
        self.assertEqual(r["original_portrait_source"]["physical_original_bitmapno"],303372)
        self.assertEqual(r["original_portrait_source"]["source_dimensions"],[96,104])
        self.assertFalse(r["original_portrait_source"]["already_privately_decoded_portrait_pixels"])
        self.assertFalse(r["original_portrait_source"]["original_runtime_default_portrait_selector_proven"])
        self.assertEqual(r["evidence_limits"]["previous_original_palette_indices_privately_decoded_and_observed"],8)
        self.assertEqual(r["evidence_limits"]["new_original_pixels_decoded_in_pet10"],0)
        self.assertFalse(r["evidence_limits"]["original_private_images_published_in_git"])
        self.assertFalse(r["evidence_limits"]["official_live_pet_species_or_release_confirmed"])
        self.assertTrue(all(v is None for v in r["historical_unverified_fields"].values()))
        self.assertFalse(self.sources["source"]["named_pet_or_avatar_verified"])

    def test_original_private_pixel_evidence_immutability(self):
        actual=self.record["previously_privately_decoded_original_frames"]
        self.assertEqual(len({z["source_rd_sha256"] for z in actual}),8)
        self.assertEqual(len({z["previously_private_observed_gray_png_sha256"] for z in actual}),8)
        for z in actual:
            for key in ("source_rd_sha256","source_adrn_sha256",
                        "previously_private_decoded_index_pixel_sha256",
                        "previously_private_observed_gray_png_sha256"):
                self.assertEqual(len(z[key]),64)

    def test_mismatched_name_sprite_or_private_pixels_rejected(self):
        for kind in ("name","spr","rd","png"):
            changed=copy.deepcopy(self.sources)
            if kind=="name":
                row=next(x for x in changed["pet09"]["records"]
                         if x["tw85_original_spr_no_not_official_pet_id"]==101501)
                row["original_native_program_routes"]["sd.exe"]["original_name_cp950"]="地人龍"
            elif kind=="spr":
                row=next(x for x in changed["pet09"]["records"]
                         if x["tw85_original_spr_no_not_official_pet_id"]==101501)
                row["original_physical_sprite_occurrences"][0]["original_full_spr_segment_sha256"]="0"*64
            elif kind=="rd":
                changed["source"]["frames"][0]["source_RD_sha256"]="0"*64
            else:
                changed["receipt"]["private_grayscale_png_sha256"][0]="0"*64
            with self.assertRaises(ValueError):
                build(changed)

    def test_report_matches_exact_source_replay(self):
        saved=(ROOT/"research/pets/PET-HIGH-FIRST-TW85-NAMED-PRIVATE-FRAMES-R1.json").read_text(encoding="utf-8")
        self.assertEqual(saved,json.dumps(build(),ensure_ascii=False,sort_keys=True,indent=2)+"\n")

    def test_bounded_2003_2004_classic_pc_sources(self):
        path=ROOT/"research/pets/PET-HIGH-FIRST-10-CLASSIC-PC-PERIOD-RAIDISILUO-R1.json"
        data=json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["schema"],"stoneage.pet.high_first_10.classic_pc_period_player_and_vendor_name_evidence.r1")
        self.assertEqual(data["scope"],"CLASSIC_2D_PC_ONLY")
        self.assertEqual(data["target_tw85_saved_local_graphic_source_key"],"TW85-SOURCE-SPR-101501")
        self.assertEqual(data["cross_region_source_link"],
                         "EXACT_CHINESE_NAME_MATCH_NOT_SAME_OPERATOR_OR_DEPLOYMENT_PROOF")
        docs=data["dated_documents"]
        self.assertEqual([x["document_date"] for x in docs],
                         ["2003-08-25","2004-01-17","2004-12-01"])
        self.assertEqual(len({x["url"] for x in docs}),3)
        self.assertTrue(docs[0]["url"].startswith("https://news.17173.com/z/stoneage/"))
        self.assertTrue(docs[1]["url"].startswith("https://news.17173.com/z/stoneage/"))
        self.assertTrue(docs[2]["url"].startswith("https://product.zol.com.cn/xinhuanet/"))
        self.assertEqual(docs[0]["reported_alias"],"无魔")
        self.assertEqual(docs[2]["product_pet_alias"],"无魔兽")
        self.assertTrue(data["boundary"]["not_a_mobile_or_private_server_source"])
        self.assertFalse(data["boundary"]["single_cross_region_official_species_identity_claimed"])
        self.assertFalse(data["boundary"]["these_documents_prove_first_world_release_date"])
        self.assertEqual(data["boundary"]["new_official_live_species_count_by_this_record"],0)
        self.assertTrue(all(d["source_directly_names"]=="雷帝斯洛" for d in docs))

if __name__=="__main__":
    unittest.main()
