"""INTEGRATION58 public source-only three Poru maps / dragon reward / independent TW1 PNG receipts."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-INTEGRATION58-PORU-THREE-MAP-DRAGON-FLAG63-TW1-32-PIXELS-R1.json"

def git_blob_sha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()

class TestStoneageIntegration58(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT.read_text(encoding="utf-8"))
        cls.source={}
        for key,src in cls.r["qualified_public_source_git_blobs"].items():
            b=(ROOT/src["path"]).read_bytes()
            assert git_blob_sha(b)==src["sha"], "prior source changed: "+key
            cls.source[key]=json.loads(b)

    def test_full_original_current_retained(self):
        s=self.r["original_history_retained"]
        b=(ROOT/s["path"]).read_bytes()
        self.assertEqual(len(b),2709173)
        self.assertEqual(git_blob_sha(b),s["blob"])
        self.assertFalse(s["edited"])

    def test_three_actual_mixed25_original_DATS_and_source_cells(self):
        q=self.source["quest24"]
        records=self.r["original_mixed25_three_real_DAT_NPC_and_script_connections"]
        self.assertEqual([x["original_DAT"]["floor"] for x in records],[5509,5510,5511])
        self.assertEqual([x["source_center_point"]["raw_three_u16"] for x in records],[[407,0,49152],[4206,0,49152],[4204,0,49152]])
        for x in records:
            m=next(y for y in q["original_scene_observations"] if y["floor"]==x["original_DAT"]["floor"])
            p=next(y for y in m["source_points"] if y["modern_marker_id"]==x["source_marker"])
            self.assertEqual(x["source_center_point"],p)
            self.assertEqual(x["original_DAT"]["sha256"],m["original_DAT_sha256"])
            self.assertEqual(x["original_DAT"]["bytes"],m["original_DAT_bytes"])
            self.assertEqual(x["original_DAT"]["geometry"],m["geometry"])
            self.assertEqual(x["original_DAT"]["prior_candidate_full_canvas_RGBA_sha256"],m["three_candidate_RGBA_sha256"]["combined"])
            self.assertEqual(x["original_DAT"]["bytes"],8+6*m["geometry"][0]*m["geometry"][1])

    def test_exact_source_create_and_argument_hashes(self):
        q=self.source["quest24"]
        records=self.r["original_mixed25_three_real_DAT_NPC_and_script_connections"]
        for x in records:
            c=next(y for y in q["source_creates"] if y["marker_id"]==x["source_marker"])
            self.assertEqual(x["source_NPC_CREATE"],c)
            self.assertEqual(x["source_argument_file"],next(y for y in q["source_manifest"] if y["path"]==c["argument_paths"][0]))
            self.assertEqual(c["floor"],x["original_DAT"]["floor"])
            self.assertEqual(c["borncenter"][:2],x["source_center_point"]["xy"])
        self.assertEqual([x["source_NPC_CREATE"]["graphic_alias"] for x in records],[100388,100388,100373])
        self.assertEqual([x["source_NPC_CREATE"]["source_template_token"] for x in records],["npcgen_warpman","changeevent","changeevent"])

    def test_source_warp_and_free_are_static_not_native_executed(self):
        r=self.r["original_mixed25_event_and_reward_static_source"]
        q=self.source["quest24"]
        self.assertEqual(r["source_warpman_5509"],next(x for x in q["actual_source_warpman_parameters"] if x["path"]=="poru/wpm_5509_35_35"))
        self.assertEqual(r["source_warpman_5509"]["source_values"]["WARP"],"5510,16,49")
        self.assertEqual(r["source_warpman_5509"]["source_values"]["FREE"],"ITEM=2414")
        self.assertFalse(r["source_warpman_5509"]["actual_warp_or_fee_executed"])

    def test_source_flag63_boss_static_event_reward_and_pet_alias(self):
        q=self.source["quest24"]
        r=self.r["original_mixed25_event_and_reward_static_source"]
        self.assertEqual(r["original_flag63_existing_source"],q["flag63_bridge"])
        self.assertEqual(r["source_boss_script"],next(x for x in q["source_scripts"] if x["path"]=="poru/boy04"))
        self.assertEqual(r["source_middle_event"],next(x for x in q["source_scripts"] if x["path"]=="poru/wpm_5510_16_50"))
        self.assertEqual(r["original_flag63_existing_source"]["original_provider_commands"],{"GetPet":["352"],"EndSetFlg":["63"]})
        self.assertEqual(r["original_flag63_existing_source"]["original_GetPet_352_existing_WORLD21_lookup"]["original_template_graphic_id"],100373)
        self.assertFalse(r["original_flag63_existing_source"]["original_flag_saved_or_reward_delivered"])
        self.assertTrue(r["source_flags_only_not_executed"])

    def test_early_tw1_original_SPR_group_matches_prior_pet07_and_pet15(self):
        p7=self.source["pet07"];p15=self.source["pet15"]
        groups=self.r["independent_tw1_SPR_two_graphic_groups_32_original_PNG_receipts"]
        self.assertEqual([x["graphic"] for x in groups],[100388,100373])
        for x in groups:
            g=x["graphic"]
            old=next(y for y in p7["source_groups"] if y[0]==g)
            old15=next(y for y in p15["groups"] if y["graphic"]==g)
            self.assertEqual(x["original_tw1_retail_source_SPR_group"],old)
            self.assertEqual(x["prior_pet15_full_SPR_confirmation"]["segment_sha256"],old15["segment_sha256"])
            self.assertEqual(old[2],old15["segment_sha256"])
            self.assertEqual(x["prior_pet15_full_SPR_confirmation"]["fully_observable_sequences"],old15["fully_observable_sequences"])
            self.assertEqual(old[5][0][0],0)

    def test_all_32_original_retail_png_public_receipt_shas(self):
        p7=self.source["pet07"]
        report=self.r
        groups=report["independent_tw1_SPR_two_graphic_groups_32_original_PNG_receipts"]
        expected={100388:18,100373:14}
        frame_counts={100388:52,100373:27}
        all_ids=[]
        for x in groups:
            g=x["graphic"];group=x["original_tw1_retail_source_SPR_group"]
            ids=x["actual_early_original_PNG_bitmap_ids_with_private_b64_source_sha_rechecked"]
            rows=x["prior_public_original_RD_and_PNG_source_receipts"]
            self.assertEqual(len(ids),expected[g])
            self.assertEqual(group[6],expected[g])
            self.assertEqual(group[4],frame_counts[g])
            self.assertEqual(ids,sorted(set(ids)))
            self.assertEqual(len(rows),len(ids))
            for bid,row in zip(ids,rows):
                self.assertEqual(bid,row[0])
                self.assertEqual(row,next(r for r in p7["source_actual_pixel_receipts"] if r[0]==bid))
                self.assertEqual(row[0],row[1])
                self.assertEqual(len(row[2]),64)
                self.assertEqual(len(row[3]),64)
                self.assertEqual(len(row[8]),64)
                self.assertGreater(row[5],0)
                self.assertGreater(row[6],0)
            all_ids.extend(ids)
        self.assertEqual(len(set(all_ids)),32)
        self.assertEqual(report["counts"]["tw1_selected_source_frame_positions_in_order"],79)
        self.assertEqual(report["counts"]["tw1_original_PNG_total_actual_bytes"],41816+66920)

    def test_private_source_custody_and_strict_public_limit(self):
        p=self.r["private_original_bytes_custody"]
        self.assertEqual((p["original_quest24"]["bytes"],p["original_quest24"]["members"]),(23451751,578))
        self.assertEqual((p["original_pet07_catalog"]["bytes"],p["original_pet07_prior_RD_source_receipt"]["bytes"]),(15123277,1617404))
        a=p["integration58_selected_private_archive"]
        self.assertEqual((a["bytes"],a["members"],a["actual_private_tw1_original_PNGs_reopened"]),(8265963,47,32))
        self.assertEqual(a["sha256"],"a6262443dabe1181e2ebbbab99fca3e31b98cd316d2d67f17e290a0d2a8892a2")
        self.assertTrue(a["independently_redownloaded_full_SHA_CRC_and_32_PNG_sha_checked"])
        self.assertFalse(a["public_git"])
        self.assertTrue(a["contains_proprietary_NPC_DAT_and_PNG"])
        self.assertEqual(self.r["counts"]["raw_proprietary_artifacts_published_in_git"],0)

    def test_exact_stopping_boundary_native_execution_and_stage_B_gated(self):
        c=self.r["counts"]
        self.assertEqual((c["original_community_DAT_files_whole_byte_sha_replayed_this_work"],c["original_community_NPC_CREATE_blocks_reopened_and_joined"],c["tw1_original_PNGs_read_and_image_decoded_this_work"]),(3,3,32))
        for key in ["tw1_original_RD_raw_bytes_reopened_this_round","newly_decoded_original_RD_blocks","actual_native_original_client_execution","actual_native_original_server_execution","original_npc_warp_executed","original_quest_63_reward_delivered","historical_same_client_server_deployment_proven","raw_proprietary_artifacts_published_in_git"]:
            self.assertEqual(c[key],0)
        self.assertFalse(self.r["historical_carrier_boundaries"]["historical_first_release_identified"])
        self.assertGreaterEqual(len(self.r["negative_evidence_guardrails"]),9)
        self.assertEqual(self.r["stage"]["stage_B"],"GATED")
        self.assertIsNone(self.r["stage"]["overall_percent"])

if __name__=="__main__":
    unittest.main()
