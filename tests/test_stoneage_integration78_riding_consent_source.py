"""Public-only source-bound conservation tests for INTEGRATION78.

No copyrighted original game bitmap/script is included; passing tests do not
certify the original game or historical runtime execution.
"""
from __future__ import annotations
import json
import re
import unittest
from collections import Counter
from pathlib import Path

REPORT = Path(__file__).resolve().parents[1] / 'research/recovered/STONEAGE-INTEGRATION78-RIDING-CONSENT-ORIGINAL-ITEM-PIXEL-SOURCE-R1.json'
HEX64 = re.compile(r'^[0-9a-f]{64}$')

class RidingConsentSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_text(encoding='utf-8'))

    def test_source_carriers_pinned_and_originals_not_in_git(self):
        c=self.r['private_carriers']; n=c['original_NPC_community_mixed25_archive']; i=c['previous_item01_private_catalog_archive']
        self.assertEqual((n['members'],n['crc_pass'],n['bytes']), (2205,2205,995176))
        self.assertEqual((i['members'],i['crc_pass'],i['bytes']), (838,838,5868386))
        self.assertTrue(HEX64.fullmatch(n['sha256'])); self.assertTrue(HEX64.fullmatch(i['catalog_json_sha256']))
        self.assertFalse(self.r['evidence_limits']['private_original_source_PNG_and_scripts_published_to_public_git'])

    def test_all_16_original_line_identities_stay_in_source_B_only(self):
        rows=self.r['consent_item_rows']
        self.assertEqual(len(rows),16)
        ids=[x['id'] for x in rows]
        self.assertEqual(len(set(ids)),16)
        self.assertEqual(sorted(ids),sorted(self.r['source_itemset0710_consent_ids']))
        self.assertEqual(self.r['source_itemset_A_consent_ids'],[])
        self.assertEqual(self.r['item_row_count_16_later_table_only'],16)
        self.assertTrue(all(x['source_itemset0710_present'] and not x['source_itemset_txt_present'] for x in rows))
        self.assertTrue(all(x['original_itemset_file']=='gmsv/data/itemset0710.txt' for x in rows))
        self.assertTrue(all(x['graphic_alias']==24176 and x['original_source_line']>0 and HEX64.fullmatch(x['source_line_sha256']) for x in rows))

    def test_source_roles_form_one_nonduplicating_partition(self):
        roles=Counter(x['relation'] for x in self.r['consent_item_rows'])
        self.assertEqual(dict(roles),self.r['consent_role_counts'])
        self.assertEqual(roles,Counter({'TRAINER_AND_LETTER_MENU':4,'LETTER_MENU_ONLY':5,'SPECIAL_MOUNT_ARG':1,'SOURCE_ROW_ONLY':6}))
        self.assertEqual(self.r['source_shop_argument_direct_memberships_total'],0)

    def test_four_original_trainer_NPC_source_blocks(self):
        a=self.r['NPC_static_create']['riding_trainer']
        self.assertEqual(len(a),4)
        self.assertEqual([x['family'] for x in a],[1,2,3,4])
        self.assertEqual([x['floor'] for x in a],[1040,2030,3030,4030])
        self.assertEqual([x['graphic'] for x in a],[16017,16002,16002,16002])
        self.assertTrue(all('conff:family/riderman.conf' in x['enemy'] for x in a))
        self.assertTrue(all(HEX64.fullmatch(x['source_block_sha256']) and x['source_span'][0]<x['source_span'][1] for x in a))

    def test_four_original_secretary_NPC_source_blocks(self):
        a=self.r['NPC_static_create']['letter_secretary']
        self.assertEqual(len(a),4)
        self.assertEqual([x['family'] for x in a],[1,2,3,4])
        self.assertEqual([x['floor'] for x in a],[1041,2031,3031,4031])
        self.assertEqual([x['graphic'] for x in a],[16065,16065,16027,16030])
        self.assertTrue(all('conff:family/fmletter.conf' in x['enemy'] for x in a))

    def test_four_tuition_windows_and_legacy_letter_fields(self):
        q=self.r['NPC_original_config']['riding_trainer_windows']
        self.assertEqual([x['winno'] for x in q],[110,120,130,140])
        self.assertEqual([x['takegold'] for x in q],[5000,10000,15000,20000])
        self.assertTrue(all(x['letter_items']==[19005,19006,19007,19008] for x in q))
        self.assertEqual(self.r['NPC_original_config']['trainer_letter_item_ids'],[19005,19006,19007,19008])
        self.assertFalse(self.r['NPC_original_config']['source_training_runtime_replayed_this_round'])

    def test_nine_letter_menu_entries_do_not_become_nine_trainers(self):
        maker=self.r['NPC_original_config']['fmletter_producer_window']
        self.assertEqual(maker['winno'],20)
        self.assertEqual(maker['letter_items'],[19005,19006,19007,19008,20224,20225,20226,20227,20228])
        self.assertEqual(len(maker['letter_items']),9)
        self.assertEqual(len(self.r['NPC_static_create']['riding_trainer']),4)

    def test_special_mount_item_20296_not_promoted_to_native_grant(self):
        x=self.r['NPC_original_config']
        self.assertEqual(len(self.r['NPC_static_create']['special_mount_family']),1)
        self.assertEqual(len(self.r['NPC_static_create']['special_mount_sa60']),1)
        self.assertEqual(len(x['rider_arg_variants']),3)
        self.assertTrue(all(v['contains_conditional_item_id']==20296 and v['contains_literal_trans_values']==[5,6] for v in x['rider_arg_variants'].values()))
        self.assertEqual(x['rider_arg_variants']['npc/family/rider.arg']['sha256'],x['rider_arg_variants']['npc/sa60/rider.arg.bak']['sha256'])
        self.assertEqual([row['id'] for row in self.r['consent_item_rows'] if row['relation']=='SPECIAL_MOUNT_ARG'],[20296])
        self.assertEqual(self.r['evidence_limits']['original_fmletter_creation_or_training_execution'],'OPEN')

    def test_shared_original_retained_pixel_is_cross_carrier_only(self):
        p=self.r['single_shared_tw1_pixel_candidate']
        self.assertEqual((p['image_number_alias'],p['tw1_real_physical_bitmap_number']),(24176,6840))
        self.assertEqual((p['source_width'],p['source_height'],p['original_RD_bytes']),(52,44,1524))
        self.assertEqual(p['candidate_png_bytes'],2786)
        self.assertEqual(p['candidate_png_sha256'],'82334c031191fb20b31f6a469a9a9985dac36592ba362defc8ed0b9a15a06572')
        self.assertEqual(p['unique_original_RD_new_this_round'],0)
        self.assertEqual(self.r['private_carriers']['prior_TW1_retail_RD_source_record']['this_round_original_REAL_bytes_decoded'],0)
        self.assertEqual(self.r['evidence_limits']['TW1_retail_icon_was_riding_consent_in_original_TW1_server'],'OPEN')

    def test_distinct_voucher_lacks_qualified_TW1_icon(self):
        q=self.r['voucher_contrast_20833']
        self.assertEqual((q['id'],q['graphic_alias']),(20833,24371))
        self.assertTrue(q['present_in_both_tables'])
        self.assertFalse(q['qualified_retail_RD'])
        self.assertEqual(q['retail_original_alias_matches'],0)
        self.assertTrue(q['not_equivalent_to_consent_without_evidence'])
        self.assertNotIn(20833,self.r['source_itemset0710_consent_ids'])

    def test_same_deployment_and_runtime_stay_unproven(self):
        q=self.r['evidence_limits']
        for k in ['historical_same_deployment_of_community_NPC_itemset_and_TW1_retail_client','original_fmletter_creation_or_training_execution','source_file_itemset0710_date_and_build']:
            self.assertEqual(q[k],'OPEN')
        self.assertEqual(q['new_unique_original_image_discovery_this_round'],0)
        self.assertIsNone(self.r['stage']['overall_percent'])
        self.assertEqual([self.r['stage']['stage_a_partial'],self.r['stage']['stage_a_open']],[7,2])

    def test_large_historical_current_not_replaced_by_new_report(self):
        p=self.r['source_baseline']
        self.assertEqual(p['historical_current_blob'],'c89e0e33537990aa2132b47c40fef49a985a935c')
        self.assertEqual(p['historical_current_size_bytes'],2709173)
        self.assertTrue(REPORT.stat().st_size<100000)

if __name__=='__main__': unittest.main()
