"""WORLD06 actual TW10 original pixel receipts + WORLD05 derived quest candidate links.
Public CI is derived-only; private images and native game do not run here.
"""
from collections import Counter
from pathlib import Path
import json, unittest
R = Path(__file__).resolve().parents[1] / "research" / "recovered"
def read(filename):
    return json.loads((R/filename).read_text(encoding="utf-8"))
class World06OriginalPixels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w=read("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-06-TW10-GETPET-ORIGINAL-PIXEL-BRIDGE-R1.json")
        cls.w05=read("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-05-GETPET-INSTANCE-TEMPLATE-SPR-R1.json")
        cls.pet=read("STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json")
        cls.cross=read("STONEAGE-PET-MODULE-09-CROSSCARRIER-ORIGINAL-MATERIAL-RECEIPTS-R1.json")
    def test_exact_original_RD_bitmap_shas_against_PRIOR_PET07_public_receipts(self):
        p={r[0]:r for r in self.pet["source_actual_pixel_receipts"]}
        g={r[0]:r for r in self.pet["source_groups"]}
        c={r[0]:r for r in self.cross["candidate_rows"]}
        q={r["source_GETPET_literal_numeric"]:r for r in self.w05["GETPET_instance_template_graph"]}
        rows=self.w["visual_witnesses"]
        self.assertEqual(len(rows),36)
        self.assertEqual([r["original_QUEST_GETPET_numeric"] for r in rows], sorted(q))
        self.assertEqual(len({r["TW10_original_RD_sha256"] for r in rows}),36)
        for r in rows:
            id=r["original_QUEST_GETPET_numeric"]
            orig=q[id]
            self.assertEqual([r["original_instance_reference_template_numeric"],r["original_community_mixed25_source_graphic_numeric"]],
                             [orig["template_A"]["template_id"],orig["template_A"]["graphic_id"]])
            self.assertEqual(orig["template_A"]["graphic_id"],orig["template_B"]["graphic_id"])
            gr=g[r["original_community_mixed25_source_graphic_numeric"]]
            self.assertEqual([r["TW10_original_SPR_group_index"],r["TW10_original_SPR_segment_SHA256"],r["TW10_original_animation_records"]],
                             [gr[1],gr[2],gr[3]])
            self.assertIn(r["TW10_qualified_source_selected_action"], [sq[0] for sq in gr[5] if sq[1]==0])
            bitmap=p[r["TW10_actual_original_RD_bitmap_ID"]]
            self.assertEqual((r["TW10_original_RD_sha256"],r["TW10_original_decoded_index_pixels_sha256"],
                              r["TW10_original_RD_dimensions"],r["TW10_qualifying_Palet1_candidate_PNG_sha256"],r["TW10_original_RD_flag"]),
                             (bitmap[2],bitmap[3],[bitmap[5],bitmap[6]],bitmap[8],bitmap[4]))
            self.assertEqual(r["TW10_pixel_custody_class"],c[gr[0]][3])
            self.assertEqual(r["TW10_pixel_custody_class"],"TW1_PET07_PRIVATE_PIXELS")
            self.assertEqual(r["TW10_source_selected_direction"],0)
    def test_unrenderable_sequence_and_old_gallery_candidate_sha_are_not_promoted(self):
        w=self.w;rows=w["visual_witnesses"]
        self.assertEqual(Counter(r["TW10_qualified_source_selected_action"] for r in rows),{0:33,2:3})
        self.assertEqual([(r["original_community_mixed25_source_graphic_numeric"],r["TW10_actual_original_RD_bitmap_ID"]) for r in rows if r["specific_exception"]],
                         [(100329,113521),(100330,113769),(100401,82737)])
        x=self.pet["source_renderable_sequences_excluded"]
        self.assertIn({"graphic":100401,"sequence_id":"100401-0-0","original_frame_positions":26,
                       "invalid_source_bitmap_ids":[82729]},x)
        self.assertIn(82729,{r["bitmap"] for r in self.pet["source_undecodable_actual_RD_blocks"]})
        self.assertEqual(w["summary"]["legacy_PET06_gallery_action0_first_frame_mismatches_skipped"],2)
        self.assertEqual(w["summary"]["additional_original_TW10_RD_blocks_redecoded_directly_from_REAL_in_this_unit"],0)
    def test_history_and_private_assets_stay_separate(self):
        w=self.w
        self.assertEqual(w["source_index_git_blobs"]["WORLD05"],"e4496d75236ef1050c4761fab8dcb3a2719da884")
        self.assertEqual(w["private_evidence_sha_receipts"]["newly_private_WORLD06_36_candidate_PNG_SHA256"],
                         "411665dc6a2a9aa1bf46fc60ff864f3e518b15ab3bb41a7be5a492684b5aa396")
        negative_claim_keys = {
            "historical_TW10_and_later_community_mixed25_same_build_proven",
            "cross_carrier_pet_name_identity_proven",
            "original_QUEST_GETPET_execution_or_reward_proven",
            "original_client_rendering_palette_or_action_timing_proven",
            "original_TW10_source_assets_published_to_Git",
        }
        self.assertTrue(all(not w["boundaries"][key] for key in negative_claim_keys))
        self.assertTrue(all(value for key, value in w["boundaries"].items()
                            if key not in negative_claim_keys))
        self.assertFalse(w["boundaries"]["historical_TW10_and_later_community_mixed25_same_build_proven"])
        self.assertEqual(w["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertEqual([w["stage_B"],w["wiki"],w["R79"]],["GATED","GATED","PAUSED_NON_BLOCKING"])
        self.assertIsNone(w["overall_percent"])
        self.assertEqual(w["preserved_historical_CURRENT_Git_blob"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")
        for r in w["visual_witnesses"]:
            self.assertNotIn("original_base64_image",r)
            self.assertNotIn("original_pixel_rgba",r)
if __name__=="__main__":
    unittest.main()
