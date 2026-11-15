"""Public source-bound 10 original Taiwan 1.0 sprite candidate provenance checks.

Checks can verify only published source-derived receipts. Private original commercial
SPR/REAL bytes and preview pixels are intentionally absent from GitHub Actions.
"""
from __future__ import annotations
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-INTEGRATION116-TEN-NPC-ORIGINAL-TW10-2D-R1.json'
CHAR04 = ROOT / 'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-04-SAME-CARRIER-GRAPHIC-FUNCTION-JOIN-R1.json'
PET15 = ROOT / 'research/recovered/STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json'
CHAR11 = ROOT / 'research/recovered/STONEAGE-CHAR11-TW10-REMAINING-BODY-MOTION-R1.json'
INTEG115 = ROOT / 'research/recovered/STONEAGE-INTEGRATION115-TW10-FIVE-GATE-BREEDER-ACTUAL-ORIGINAL-2D-R1.json'
EXPECT = [100405,100406,100433,100434,100438,100444,100446,100456,100457,100461]


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def git_blob_sha(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


class TestOriginalSourceQualifiedTenSpriteGroups(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load(REPORT)
        cls.char=load(CHAR04)
        cls.pet=load(PET15)
        cls.body=load(CHAR11)
        cls.prev=load(INTEG115)
        cls.groups=cls.d['source_groups']

    def test_01_real_parent_unchanged_git_blob(self):
        self.assertEqual(git_blob_sha(CHAR04.read_bytes()),'1c564b07e829bce8360f57e63d32866c03e225e3')
        self.assertEqual(self.d['cross_carrier_later_source']['public_PARENT_CHAR04_Git_blob'],git_blob_sha(CHAR04.read_bytes()))

    def test_02_no_duplicate_prior_full_motion_group(self):
        prior=set(x['graphic'] for x in self.pet['groups'])|set(self.body['group_keys'])|set(x['graphic_no'] for x in self.prev['five_groups'])
        self.assertFalse(set(EXPECT)&prior)
        self.assertEqual([x['graphic'] for x in self.groups],EXPECT)
        self.assertTrue(self.d['source_duplicate_avoidance']['ten_not_in_prior_PET15_CHAR11_INTEGRATION115_source_group_lists'])

    def test_03_exact_ten_remaining_same_numeric_source_group_candidates(self):
        parent=self.char['indexed_graphic_source_summary']
        valid={x[0] for x in parent if x[0] >=100240 and x[0]<=100463}
        prior=set(x['graphic'] for x in self.pet['groups'])|set(self.body['group_keys'])|set(x['graphic_no'] for x in self.prev['five_groups'])
        self.assertEqual(valid-prior,set(EXPECT))

    def test_04_actual_source_41_config_occurrences_recomputed(self):
        rows=self.char['create_source_rows'];count=0
        for group in self.groups:
            raw=[r for r in rows if r[3]==group['graphic']]
            meta=group['independent_source_create_reference'];count+=len(raw)
            self.assertEqual(len(raw),meta['occurrences'])
            self.assertEqual(sorted({r[0] for r in raw}),sorted(meta['source_create_paths']))
            function_counts={}
            for r in raw:function_counts[r[2]]=function_counts.get(r[2],0)+1
            self.assertEqual(function_counts,meta['function_counts'])
        self.assertEqual(count,41)
        self.assertEqual(self.d['cross_carrier_later_source']['source_create_rows_referencing_ten_numeric_ids'],41)

    def test_05_original_SPR_indexes_and_full_group_hash_receipts(self):
        parent={r[0]:r[1] for r in self.char['indexed_graphic_source_summary']}
        for g in self.groups:
            self.assertEqual(parent[g['graphic']],[g['original_SPR_index']])
            self.assertEqual(g['full_original_action_direction_sequence_count'],104)
            self.assertEqual(g['source_direction_codes'],list(range(8)))
            self.assertEqual(g['source_action_codes'],list(range(13)))
            for key in ['original_SPRADRN_record_sha256','source_SPR_segment_sha256','all_bitmap_ids_sorted_sha256','original_RD_sha256_concatenation_sha256','source_original_pixel_sha256_concatenation_sha256']:
                self.assertEqual(len(g[key]),64)
                int(g[key],16)
            self.assertGreater(g['source_SPR_segment_bytes'],0)
            self.assertEqual(g['source_index_records_nseq'],104)

    def test_06_frame_reference_and_bitmap_accounting(self):
        obs=self.d['actual_original_2d_observations']
        self.assertEqual(len(self.groups),10)
        self.assertEqual(obs['source_animation_sequences'],1040)
        self.assertEqual(sum(g['original_spr_frame_positions'] for g in self.groups),5280)
        self.assertEqual(obs['original_frame_reference_occurrences'],5280)
        self.assertEqual(sum(g['source_original_bitmap_keys_distinct'] for g in self.groups),3416)
        self.assertEqual(sum(g['source_RD_actual_read_independent_decode_count'] for g in self.groups),3416)
        self.assertEqual(obs['cross_group_distinct_original_RD_bitmap_blocks_actual_read'],3272)
        self.assertLess(obs['cross_group_distinct_original_RD_bitmap_blocks_actual_read'],3416)
        self.assertEqual(obs['original_SPR_sentinel_positions'],0)
        self.assertEqual(obs['original_valid_frame_bitmap_occurrences'],5280)

    def test_07_strict_vs_two_qualified_bounded_anomalies(self):
        obs=self.d['actual_original_2d_observations']
        self.assertEqual((obs['source_strict_full_RD_decoded_twice'],obs['source_qualified_terminal_zero_bounded_only']),(3270,2))
        self.assertEqual(obs['source_failed_RD_double_decode'],0)
        self.assertEqual(3270+2,obs['cross_group_distinct_original_RD_bitmap_blocks_actual_read'])
        anomalies={g['graphic']:g['source_RD_bounded_count'] for g in self.groups if g['source_RD_bounded_count']}
        self.assertEqual(anomalies,{100406:1,100457:1})
        self.assertEqual(sum(g['source_RD_strict_count']+g['source_RD_bounded_count'] for g in self.groups),3416)
        self.assertEqual(sorted(x['source_bitmap_id'] for x in self.d['bounded_original_RD_pixel_prefix_only']),[84257,92899])
        self.assertTrue(all(x['not_strict'] for x in self.d['bounded_original_RD_pixel_prefix_only']))
        self.assertTrue(all(x['terminal_zero_only_not_arbitrary_clipping'] for x in self.d['bounded_original_RD_pixel_prefix_only']))

    def test_08_member_full_SHA_matches_previous_authenticated_retail(self):
        src=self.d['authentic_original_retail'];parent=self.pet
        self.assertEqual(src['source_private_zip_sha256'],parent['source_archive_sha256'])
        self.assertEqual(src['source_private_zip_bytes'],372626292)
        self.assertEqual(src['ZIP_members_CRC_verified'],379)
        self.assertEqual(src['complete_original_SPR_group_count'],464)
        self.assertEqual(src['original_ADRN_rows'],125996)
        for n in ('spradrn_1.bin','spr_1.bin','adrn_1.bin','real_1.bin','Palet_1.sap'):
            self.assertEqual([src['source_original_members'][n][k] for k in ('bytes','sha256')],parent['source_members'][n])
        self.assertEqual(src['source_original_members']['Palet_0.sap']['bytes'],708)
        self.assertEqual(len(src['source_original_members']['Palet_0.sap']['sha256']),64)

    def test_09_source_disjointness_and_no_fake_NPC_identity(self):
        s=self.d['cross_carrier_later_source'];limits=self.d['limits']
        self.assertIn('MIXED25',s['carrier'])
        self.assertNotEqual(s['carrier'],self.d['authentic_original_retail']['carrier'])
        self.assertTrue(s['source_create_occurrences_are_not_41_independent_NPC_person_identities'])
        for key in ('proven_new_historical_NPC_species_identity','same_client_server_historical_deployment','original_native_client_exec','original_native_npc_battle_shop_teleport_or_warp_executed','official_TW10_NPC_name_from_mixed25_source','original_TW10_palette_selection_verified','images_or_full_commercial_source_published'):
            self.assertIs(limits[key],False,key)

    def test_10_original_private_custody_without_binary_publication(self):
        private=self.d['private_visual_observation']
        self.assertEqual(private['private_archive_bytes'],620703)
        self.assertEqual(private['private_archive_sha256'],'2d7bb1aab1184ff92f350b90ee3b2ec7be1d33ab95ef71ba74ab4b1165a4db92')
        self.assertEqual(private['private_member_crc_verified'],5)
        self.assertTrue(private['private_library_roundtrip_same_SHA256'])
        self.assertFalse(private['source_original_commercial_image_bytes_published'])
        self.assertFalse(private['contains_complete_original_commercial_RD_or_SPR_binaries'])
        self.assertTrue(private['contains_private_original_pixel_candidate_previews'])

    def test_11_preserve_historical_current_state_and_open_issues(self):
        self.assertEqual(self.d['original_FULL_CURRENT_blob_preserved'],'c89e0e33537990aa2132b47c40fef49a985a935c')
        self.assertEqual(self.d['original_FULL_CURRENT_bytes_preserved'],2709173)
        lim=self.d['limits'];self.assertEqual(lim['stage_A'],'7_PARTIAL_2_OPEN')
        self.assertEqual(lim['stage_B_and_wiki'],'GATED')
        self.assertEqual(lim['R79'],'PAUSED_NON_BLOCKING')
        self.assertIsNone(lim['overall_percent'])

    def test_12_no_client_execution_or_paletted_pixel_claim_from_ci(self):
        obs=self.d['actual_original_2d_observations']
        self.assertFalse(obs['native_palette_selection_proven'])
        self.assertEqual(obs['independent_RLE_bytewise_pixel_agreement'],3272)
        self.assertFalse(self.d['limits']['original_animation_duration_units_known'])
        self.assertTrue(self.d['new_exact_candidate_and_main_Actions_success_only_after_live_GitHub_check'])


if __name__=='__main__':unittest.main()