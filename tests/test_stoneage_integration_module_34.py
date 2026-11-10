"""INTEGRATION34: preserve verified private TW1 artwork against a different-era GetPet numeric alias."""
import hashlib,json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research/recovered/STONEAGE-INTEGRATION34-GETPET95-CROSSCARRIER-ORIGINAL-PIXEL-R1.json"

def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()

class Crosscarrier100394(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(R.read_text(encoding="utf-8"))
        cls.sources={}
        for k,ref in cls.r["upstream"].items():
            raw=(ROOT/ref["path"]).read_bytes()
            assert git_blob(raw)==ref["git_blob"],k
            cls.sources[k]=json.loads(raw)

    def test_unmodified_full_current_and_two_original_private_files(self):
        state=self.r["remote_baseline"]
        self.assertEqual((state["main"],state["tree"]),
                         ("3013519551953c787c98b9fe3265528bc9e293a9","55b1d01dd463a002d7dcb35eae04135dba8c4a1b"))
        b=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertGreaterEqual(len(b),state["CURRENT_bytes"])
        self.assertEqual(git_blob(b[:state["CURRENT_bytes"]]),state["CURRENT_original_git_blob"])
        p=self.r["private_artifacts_retrieved_and_verified"]
        self.assertEqual((p["PET07_private_HTML"]["bytes"],p["PET07_private_original_RD_receipts"]["bytes"]),
                         (15123277,1617404))
        self.assertEqual(p["PET07_private_HTML"]["sha256"],"58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76")
        self.assertEqual(p["PET07_private_original_RD_receipts"]["sha256"],
                         "b5ad2e58930afbe90604a1d72e3c17ab0adea446e7c118be775e3973315e6cb4")
        self.assertEqual(p["PET07_private_HTML"]["actual_embedded_PNGs_redecoded_and_sha_verified"],16)

    def test_getpet_95_was_already_published_no_new_original_command(self):
        old=self.sources["i33"]
        self.assertEqual(old["same_community_RAR_PET10_numeric_candidate"]["original_script_GetPet_literal"],"95")
        found=[r for r in self.sources["i05"]["rows"] if r["source_script_path"]=="sainasu/event/event15_1"]
        self.assertEqual(len(found),1)
        self.assertEqual(found[0]["original_GetPet_numeric_literals_ordered"],[95])
        self.assertTrue(self.r["source_evidence"]["original_earlier_I05_GetPet95_occurrence_already_known"])

    def test_two_community_templates_and_original_spr_index_are_not_TW1_identity(self):
        e=self.r["source_evidence"]
        p=self.sources["pet10"]["source_rows"]
        self.assertEqual(e["original_community_PET10_template_95_primary"],
                         next(x for x in p["enemybase.txt"] if x[1]==95))
        self.assertEqual(e["original_community_PET10_template_95_alternative"],
                         next(x for x in p["enemybase2.txt"] if x[1]==95))
        self.assertEqual(e["same_community_PET10_spr_index_row"],
                         next(x for x in p["spradrn_5.bin"] if x[1]==100394))
        self.assertEqual([e[k][2] for k in ("original_community_PET10_template_95_primary",
                         "original_community_PET10_template_95_alternative")],[100394,100394])
        self.assertEqual(e["same_community_PET10_spr_index_row"][:2],[360,100394])
        self.assertNotEqual(e["original_community_PET10_template_95_primary"][-1],
                            e["original_community_PET10_template_95_alternative"][-1])

    def test_TW1_PET07_and_PET09_existing_original_source(self):
        e=self.r["source_evidence"]
        g=next(x for x in self.sources["pet07"]["source_groups"] if x[0]==100394)
        self.assertEqual(e["original_TW1_PET07_selected_source_group_row"],g)
        self.assertEqual((g[0],g[1],g[3],g[4],g[6]),(100394,360,56,23,16))
        self.assertEqual(e["original_TW1_PET09_coverage_row"],
                         next(x for x in self.sources["pet09"]["candidate_rows"] if x[0]==100394))
        self.assertEqual(e["original_TW1_PET09_coverage_row"][3],"TW1_PET07_PRIVATE_PIXELS")
        self.assertEqual([x["action"] for x in e["original_tw1_selected_sequences"]],[0,2,1])
        self.assertEqual([x["direction"] for x in e["original_tw1_selected_sequences"]],[0,0,0])
        self.assertEqual([len(x["frames"]) for x in e["original_tw1_selected_sequences"]],[8,13,2])
        self.assertEqual([x["duration_raw"] for x in e["original_tw1_selected_sequences"]],[1200,1500,1000])
        self.assertEqual(e["selected_frame_positions"],23)
        self.assertEqual(e["selected_distinct_actual_bitmap_ids"],16)

    def test_16_private_png_full_sha_match_preexisting_original_RD_receipts(self):
        e=self.r["source_evidence"]
        bitmap=[f for s in e["original_tw1_selected_sequences"] for f in s["frames"]]
        indexed={x[0]:x for x in self.sources["pet07"]["source_actual_pixel_receipts"]}
        self.assertEqual(len(bitmap),23)
        self.assertEqual(len(set(bitmap)),16)
        self.assertEqual(sorted(set(bitmap)),list(range(107883,107899)))
        rows=e["original_tw1_bitmap_receipts"]
        self.assertEqual([r["bitmap"] for r in rows],sorted(set(bitmap)))
        self.assertEqual(sum(r["frame_positions_in_selected_sequences"] for r in rows),23)
        for r in rows:
            old=indexed[r["bitmap"]]
            self.assertEqual((r["tw1_adrn_original_source_index"],r["original_RD_sha256"],
                              r["decoded_original_index_pixel_sha256"],r["RD_flag"],
                              r["original_pixel_dimensions"],r["private_candidate_Palet1_PNG_sha256"]),
                             (old[1],old[2],old[3],old[4],[old[5],old[6]],old[8]))
            self.assertTrue(r["re_read_private_png_sha256_matched"])
            self.assertTrue(r["fully_decoded_private_png_dimensions_match_original_RD"])
        self.assertEqual(self.r["private_artifacts_retrieved_and_verified"]["graphic_private_png_bytes_recovered_from_existing_gallery"],71187)

    def test_explicitly_no_same_build_or_original_gameplay_upgrade(self):
        b=self.r["limits"]
        self.assertTrue(b["tw1_graphic_100394_has_actual_original_pixel_evidence"])
        self.assertTrue(b["tw1_selected_3_sequences_only_not_full_56_animations"])
        for k in ("same_original_source_byte_image_across_community_and_tw1_verified",
                  "script_GetPet95_yields_pet_with_template_95_in_native_runtime_verified",
                  "pet_sports_name_or_native_species_identity_verified",
                  "script_and_TW1_original_pixels_from_same_deployment_verified",
                  "original_client_or_server_was_executed_this_round",
                  "original_animation_timing_and_native_palette_proven",
                  "original_image_or_HTML_published_in_git","original_quest_reward_delivered"):
            self.assertFalse(b[k],k)
        self.assertEqual((b["stage_A"],b["stage_B_wiki"],b["R79"],b["overall_percent"]),
                         ("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))

if __name__=="__main__":
    unittest.main()
