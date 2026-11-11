"""INTEGRATION62: original quest GetPet -> same-source enemy instance/template -> saved TW1 real RD pixels.
This CI tests public derivative evidence only, never copyrighted source images or native execution.
"""
import hashlib
import json
import struct
import unittest
from pathlib import Path

P=Path(__file__).resolve().parents[1]/"research"/"recovered"
NEW=P/"STONEAGE-INTEGRATION62-QUEST30-TWO-GETPET-TW1-29-RD-PIXELS-R1.json"
QUEST=P/"STONEAGE-QUEST30-DINOSAUR-COLLECTOR-EVENT35-SOURCE-R1.json"
PET=P/"STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json"
ART=P/"STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json"

class OriginalTwoPetRewardsSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads(NEW.read_text(encoding="utf-8"))
        cls.quest=json.loads(QUEST.read_text(encoding="utf-8"))
        cls.pet=json.loads(PET.read_text(encoding="utf-8"))
        cls.art=json.loads(ART.read_text(encoding="utf-8"))
        cls.rows=cls.report["source_qualified_two_rewards"]

    def test_original_quest_getpet_control_is_not_a_new_event(self):
        self.assertEqual([(x["source_GetPet_ID"],x["original_event_ordinal"]) for x in self.rows],[(93,0),(341,4)])
        self.assertTrue(self.report["GetPet_instance_relations_previously_known_in_QUEST30_and_WORLD21"])
        for x in self.rows:
            events=[e for e in self.quest["source_script"]["events"]
                    if str(x["source_GetPet_ID"]) in e["commands"].get("GetPet",[])]
            self.assertEqual(len(events),1)
            self.assertEqual(events[0]["section_sha256"],x["original_event_section_sha256"])
            self.assertEqual(self.quest["source_script"]["sha256"],x["original_quest_script_sha256"])
            self.assertEqual(self.quest["source_NPC_create"]["source_block_sha256"],
                             self.report["source_QUEST30_NPC_CREATE"]["original_create_block_sha256"])

    def test_both_community_instance_tables_key_by_id_not_physical_line(self):
        for x in self.rows:
            instance=x["source_GetPet_ID"]; template=x["same_source_template_ID"]
            for key,original in [("enemy.txt","original_enemy_primary"),("enemy2.txt","original_enemy_alternative")]:
                sources=[r for r in self.pet["source_rows"][key] if r[1]==instance]
                self.assertEqual(sources,[x[original]])
                self.assertEqual(sources[0][2],template)
                self.assertNotEqual(sources[0][0],instance)
            self.assertNotEqual(x["original_enemy_primary"][-1],x["original_enemy_alternative"][-1])

    def test_both_original_template_variants_with_different_sha(self):
        for x in self.rows:
            template=x["same_source_template_ID"]
            graphic=x["crosscarrier_early_TW1_graphic_number"]
            for table,key in [("enemybase.txt","original_template_primary"),("enemybase2.txt","original_template_alternative")]:
                matches=[r for r in self.pet["source_rows"][table] if r[1]==template]
                self.assertEqual(matches,[x[key]])
                self.assertEqual(matches[0][2],graphic)
                self.assertEqual(matches[0][3],1)
            self.assertEqual(x["original_template_primary"][2:-1],x["original_template_alternative"][2:-1])
            self.assertNotEqual(x["original_template_primary"][-1],x["original_template_alternative"][-1])

    def test_original_spr_group_and_all_six_true_frame_orders(self):
        for x in self.rows:
            graphic=x["crosscarrier_early_TW1_graphic_number"]
            gs=[g for g in self.art["source_groups"] if g[0]==graphic]
            self.assertEqual(len(gs),1)
            g=gs[0]
            self.assertEqual(g[1],x["original_TW1_SPR_group_index"])
            self.assertEqual(g[2],x["original_TW1_SPR_full_segment_sha256"])
            self.assertEqual(g[3],x["original_TW1_full_animation_count"])
            self.assertEqual(g[4],x["original_frame_positions_count"])
            self.assertEqual(g[6],x["source_distinct_bitmap_count"])
            self.assertEqual([s["action"] for s in x["original_selected_three_action_direction0_sequences"]],[0,2,1])
            for s in x["original_selected_three_action_direction0_sequences"]:
                matches=[v for v in g[5] if v[0]==s["action"] and v[1]==s["direction"]]
                self.assertEqual(len(matches),1)
                old=matches[0];nums=s["frames"]
                self.assertEqual(len(nums),old[2])
                self.assertEqual(s["original_sequence_sha256_uint32le"],old[3])
                self.assertEqual(s["original_duration_word"],old[4])
                raw=struct.pack("<"+"I"*len(nums),*nums)
                self.assertEqual(hashlib.sha256(raw).hexdigest(),old[3])

    def test_all_29_original_rd_and_png_hashes_from_source_index(self):
        pixel={r[0]:r for r in self.art["source_actual_pixel_receipts"]}
        distinct_count=0
        frame_count=0
        for x in self.rows:
            frames=[i for s in x["original_selected_three_action_direction0_sequences"] for i in s["frames"]]
            unique=list(dict.fromkeys(frames))
            self.assertEqual(unique,x["source_bitmap_numbers_first_appearance"])
            self.assertEqual(len(unique),x["source_distinct_bitmap_count"])
            self.assertTrue(all(n in pixel for n in unique))
            original_lines=[f"{n}:{pixel[n][2]}:{pixel[n][8]}:{pixel[n][5]}x{pixel[n][6]}" for n in unique]
            canonical="\n".join(original_lines)
            self.assertEqual(hashlib.sha256(canonical.encode("utf-8")).hexdigest(),x["public_original_RD_PNG_aggregate_sha256"])
            self.assertTrue(all(len(pixel[n][2])==64 and len(pixel[n][8])==64 for n in unique))
            distinct_count+=len(unique)
            frame_count+=len(frames)
        self.assertEqual([x["source_distinct_bitmap_count"] for x in self.rows],[13,16])
        self.assertEqual([x["original_frame_positions_count"] for x in self.rows],[21,25])
        self.assertEqual((distinct_count,frame_count),(29,46))

    def test_preserve_prior_item_discrepancy_and_missing_native_evidence(self):
        self.assertEqual(self.report["source_item2607_conflict_still_open"],
                         self.quest["source_2607_item_row"]["source_record_discrepancy"])
        self.assertFalse(self.quest["boundaries"]["original_game_or_server_executed"])
        self.assertEqual(self.report["private_source_replay"]["original_TW1_PNG_full_SHA_dimension_verified"],29)
        self.assertEqual(self.report["private_source_replay"]["original_selected_SPR_sequences_uint32le_SHA_verified"],6)
        self.assertEqual(self.report["private_source_replay"]["new_original_RD_binary_decodes"],0)
        self.assertTrue(self.report["private_source_replay"]["private_Library_uploaded_and_independent_full_SHA_CRC_reread"])
        self.assertEqual(self.report["private_source_replay"]["new_private_ZIP_sha256"],
                         "e075d132aa5ad0a4da25ecb8aaf325785f676291c588b0702173b7216db61cc1")
        for key,value in self.report["negative_bounds"].items():
            self.assertFalse(value,key)
        self.assertEqual(self.report["upstream_public_blobs"]["full_unchanged_CURRENT"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(self.report["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertEqual(self.report["stage_B_wiki"],"GATED")
        self.assertIsNone(self.report["overall_percent"])

if __name__=="__main__":
    unittest.main()
