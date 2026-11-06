"""Public PET11 cross-acceptance; private TW1 original bytes are NOT in CI."""
from pathlib import Path
import json
import struct
import unittest

from tools.stoneage_pet11_tw10_capture_sprite_source import (
    ZIP_BYTES,ZIP_SHA,MEMBERS,MIXED_SHA,KEYS,records,rd_indices,
)

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'research/recovered'
CURRENT=BASE/'STONEAGE-PET-MODULE-11-TW10-CAPTURE-SPR-ORIGINAL-496-PIXEL-SOURCE-R1.json'
BRIDGE=BASE/'STONEAGE-STAGE-A-WORLD37-R2B3-CAPTURE-ORIGINAL-SPR-BRIDGE-R1.json'
OLD=BASE/'STONEAGE-O63-FOUR-TIGER-SPR-SOURCE-R1.json'

class PET11OriginalPixels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=json.loads(CURRENT.read_text(encoding='utf-8'))
        cls.b=json.loads(BRIDGE.read_text(encoding='utf-8'))
        cls.o=json.loads(OLD.read_text(encoding='utf-8'))

    def test_original_tw1_member_source_sha_against_private_replay_tool(self):
        q=self.p['qualified_original_carrier']
        self.assertEqual((q['original_private_zip_bytes'],q['original_private_zip_sha256']), (ZIP_BYTES,ZIP_SHA))
        self.assertTrue(q['ZIP_all_CRC_pass'])
        self.assertEqual(q['ZIP_members'],379)
        for n,(size,digest) in MEMBERS.items():
            self.assertEqual(q['original_members'][n],{'bytes':size,'sha256':digest})
        self.assertEqual(q['community_mixed25_index_member_sha256'],MIXED_SHA)
        self.assertIn('COMMUNITY',q['mixed25_index_source'])

    def test_capture_numeric_keys_two_only_and_preserve_petflag_zero(self):
        links=self.p['capture_candidate_links']
        self.assertEqual([(x['compiled_char_int_key53'],x['original_source_graphic_no'],x['source_PETFLG']) for x in links],[(524,100329,1),(8,100355,0)])
        original={x['source_char_int_key53']:x for x in self.b['rows']}
        for x in links:
            entry=original[x['compiled_char_int_key53']]
            self.assertEqual(entry['configured_enemybase_column37_graphic_number'],x['original_source_graphic_no'])
            self.assertEqual(entry['configured_enemybase_column38_PETFLG'],x['source_PETFLG'])
            self.assertIsNotNone(entry['preserved_original_spradrn_5_match'])
            self.assertTrue(x['same_12byte_SPRADRN_record_in_TW1_and_mixed25'])
            self.assertFalse(x['original_pet_species_runtime_mapping_verified'])
        self.assertEqual(len(links),2)

    def test_animation_groups_source_conservation_and_prior_o63(self):
        groups=self.p['actual_original_sprite_source']['groups']
        self.assertEqual([x['spr_no'] for x in groups],list(KEYS))
        self.assertEqual([(x['original_tw1_index'],x['original_mixed25_index']) for x in groups],[(303,303),(325,325)])
        self.assertEqual([(x['original_source_segment_bytes'],x['original_frame_positions'],x['source_distinct_bitmap_keys']) for x in groups],[(5472,480,248),(7072,640,248)])
        self.assertEqual([x['original_animation_sequences'] for x in groups],[56,56])
        self.assertEqual([(x['strict_rd_complete'],x['bounded_original_source_canvas_prefix']) for x in groups],[(247,1),(248,0)])
        expected_sound=[{'62':8,'10001':8},{'60':8,'10001':8}]
        self.assertEqual([x['original_source_sound_field_counts'] for x in groups],expected_sound)
        old=next(x for x in self.o['groups'] if x['spr_no']==100329)
        self.assertEqual(groups[0]['original_source_segment_sha256'],old['original_tw10_full_segment_sha256'])
        self.assertEqual(groups[0]['original_frame_positions'],old['original_tw10_frame_positions'])
        self.assertEqual(groups[0]['original_source_segment_bytes'],old['original_tw10_derived_segment_length'])
        self.assertEqual(groups[0]['source_distinct_bitmap_keys'],old['original_tw10_distinct_nonzero_bitmap_keys'])
        for x in groups:
            for field in ('original_adrn_record_sha256_sequence_sha256','original_rd_sha256_sequence_sha256','canvas_index_sha256_sequence_sha256','original_source_segment_sha256','source_index_record_sha256'):
                self.assertRegex(x[field],r'^[0-9a-f]{64}$')

    def test_original_rd_decode_strict_failure_is_not_reclassified(self):
        src=self.p['actual_original_sprite_source']
        t=src['totals']
        self.assertEqual([t[x] for x in ('original_animation_sequences','original_frame_positions','distinct_original_RD_source_bitmaps','strict_complete_RD_decode','one_pixel_terminal_transparent_overrun_bounded_prefix')],[112,1120,496,495,1])
        q=src['one_strict_RD_failure_preserved']
        self.assertEqual((q['bitmapno'],q['source_real_offset'],q['source_size']), (113576,270905985,3548))
        self.assertEqual((q['decoded_count'],q['canvas_count']), (9201,9200))
        self.assertEqual((q['last_RLE_opcode_hex'],q['last_packet_before_pixel_count'],q['last_packet_after_pixel_count']),('c2',9199,9201))
        self.assertFalse(q['strict_rd'])
        self.assertFalse(q['native_executable_overrun_handling_verified'])
        self.assertEqual(src['source_aggregate_sha256']['sorted_original_496_ADRN_record_sha256_text_chain'],'1245476bd583b3829a1a7d7d16b7a718b119df1f9ecec9a05bf48057c6305a8b')
        self.assertEqual(src['source_aggregate_sha256']['sorted_original_496_RD_sha256_text_chain'],'6992e10e16142e4421451dc982b30a290a40766f2cb9221435507457df005097')
        self.assertEqual(src['source_aggregate_sha256']['sorted_496_canvas_index_pixel_sha256_text_chain'],'f755aa4ea320c2e5219ad74f8284136382cbbc00b635300aeb84bf51a79b6fdd')

    def test_private_observation_qualified_and_game_not_claimed(self):
        p=self.p
        self.assertEqual(p['starting_git']['historical_current_blob_unchanged'],'c89e0e33537990aa2132b47c40fef49a985a935c')
        t=p['private_delivery']
        self.assertEqual((t['bytes'],t['zip_sha256'],t['ZIP_members']),(4618141,'d6f7c1e832833bf7bc00c5c870ba76debddbd447c52ca546cb4fcc72a45dbd5f',3))
        self.assertTrue(t['all_ZIP_CRC_verified'] and t['saved_private_library'] and t['downloaded_from_private_library_and_full_byte_equal_verified'])
        self.assertFalse(t['Chromium_original_html_runtime_test_passed'])
        self.assertFalse(t['original_proprietary_PNG_HTML_and_text_in_public_Git'])
        e=p['evidence_boundaries']
        for k in ('WORLD37_R2C_dynamic_capture_tail_closed','mixed25_spr_5_original_frame_bytes_verified','TW1_and_mixed25_exact_spradrn_12bytes_proves_same_historical_deployment','exact_native_original_palette_and_row_orientation_proven','original_client_or_server_executed','original_source_assets_committed_to_public_repo'):
            self.assertFalse(e[k],k)
        self.assertEqual(e['stage_A'],'7_PARTIAL_2_OPEN')
        self.assertEqual(e['stage_B_and_wiki'],'GATED')
        self.assertIsNone(e['overall_restoration_percent'])

    def test_synthetic_terminal_c2_protection_and_12byte_format(self):
        data=b'RD\x01\x00'+struct.pack('<III',1,1,17)+b'\xc2'
        self.assertEqual(rd_indices(data),(1,1,b'\x00',2,False))
        self.assertEqual(rd_indices(data[:-1]+b'\xc1'),(1,1,b'\x00',1,True))
        with self.assertRaises(ValueError):rd_indices(data[:-1]+b'\xc3')
        with self.assertRaises(ValueError):rd_indices(b'XX'+data[2:])
        self.assertEqual(records(struct.pack('<IIHH',100329,2070766,56,16)),[(100329,2070766,56,16)])
        with self.assertRaises(ValueError):records(b'broken')

if __name__=='__main__':unittest.main()