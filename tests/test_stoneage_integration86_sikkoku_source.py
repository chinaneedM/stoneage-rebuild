"""Public metadata-only tests. These do NOT access commercial original data.
Source provenance, native execution, and genuine same-build identity remain separate.
"""
import json
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/recovered/STONEAGE-INTEGRATION86-SIKKOKU-SOURCE-2D-R1.json'
DATA = json.loads(SOURCE.read_text(encoding='utf-8'))

class SikkokuEvidenceContracts(unittest.TestCase):
    def test_01_schema_and_current_bounded_base(self):
        self.assertTrue(DATA['schema'].startswith('stoneage.integration86.sikkoku'))
        self.assertEqual(DATA['provenance']['remote_main_head_at_start'], '58e182f27a3404c99c32d9c3aaa18e1ecf386a16')
        self.assertEqual(DATA['provenance']['preserved_current_state_blob'], 'c89e0e33537990aa2132b47c40fef49a985a935c')
    def test_02_private_original_sources_have_precise_sha_and_crc_counts(self):
        p=DATA['provenance']
        self.assertEqual(p['original_private_mixed25_npc_members_crc_verified'], 2205)
        self.assertEqual(p['original_private_itemset_members_crc_verified'], 838)
        for key in ['original_private_mixed25_npc_zip_sha256','original_private_itemset_zip_sha256','original_private_tw1_pet07_html_sha256']:
            self.assertRegex(p[key],r'^[0-9a-f]{64}$')
    def test_03_original_two_create_files_and_exact_ten_records(self):
        c=DATA['npc_create_records']
        self.assertEqual(len(c),10)
        self.assertEqual(len([x for x in c if 'npc/giiru/' in x['original_create_file']]),8)
        self.assertEqual(len([x for x in c if x['original_create_file']=='npc/300/sb_sikkoku.create']),2)
    def test_04_five_archaeologists_on_distinct_actual_floors(self):
        c=DATA['npc_create_records'][:5]
        self.assertEqual([x['floorid'] for x in c],[32002,32006,32009,32014,32016])
        self.assertTrue(all(x['name_original']=='考古家' for x in c))
    def test_05_keep_spirit_king_and_nurses_separate(self):
        c=DATA['npc_create_records']
        self.assertEqual((c[5]['name_original'],c[5]['floorid']),('精靈王',32021))
        self.assertEqual([(x['name_original'],x['floorid']) for x in c[6:8]],[('護士',32014),('護士',32007)])
        self.assertNotEqual(c[5]['enemy_literal'],c[6]['enemy_literal'])
    def test_06_battle_guards_not_rebranded_as_quest_characters(self):
        c=DATA['npc_create_records'][8:]
        self.assertEqual([(x['floorid'],x['graphicname_original']) for x in c],[(32010,100389),(32020,100374)])
        self.assertEqual(set(x['enemy_literal'].split('|')[0] for x in c),{'sb_skr','sb_skt'})
    def test_07_source_create_byte_offsets_and_sha_uniqueness(self):
        blocks=DATA['npc_create_records'];self.assertEqual(len(set(x['original_create_block_sha256'] for x in blocks)),10)
        for x in blocks:
            self.assertGreater(x['original_byte_offset_end_exclusive'],x['original_byte_offset_start'])
            self.assertRegex(x['original_create_block_sha256'],r'^[0-9a-f]{64}$')
            self.assertEqual(x['config_status'],'STATIC_CREATE_NOT_PROVEN_SPAWN')
            self.assertTrue(x['referenced_file_exists_in_private_NPC_zip']) if x.get('direct_file_target') else None
    def test_08_source_five_archaeology_event_files_and_event_count(self):
        ev=DATA['source_events'];self.assertEqual(len(ev),DATA['counts']['event_TYPE_blocks'])
        self.assertEqual({x['source_file'].split('/')[-1] for x in ev},{f'sikkoku0{i}' for i in range(1,6)})
        self.assertEqual(len(ev),16)
    def test_09_original_event_block_sha_and_byte_offsets(self):
        for e in DATA['source_events']:
            self.assertRegex(e['original_event_block_sha256'],r'^[0-9a-f]{64}$')
            self.assertLess(e['original_byte_start'],e['original_byte_end_exclusive'])
            self.assertIn(e['type'],['MESSAGE','ACCEPT'])
    def test_10_five_original_headers_not_all_floors(self):
        n=DATA['negative_evidence'];self.assertTrue(n['five_sikkoku01_to_05_original_headers_all_contain_16th_floor_text'])
        self.assertFalse(n['original_16th_floor_header_matches_all_CREATE_floors'])
        self.assertEqual(n['archeologists_actually_created_on_floors'],[32002,32006,32009,32014,32016])
    def test_11_crucial_event_requirement_and_deletion_mismatch(self):
        n=DATA['negative_evidence']
        self.assertEqual(n['event_53_accept_item_IDs'],[2701,2707,2735,2770])
        self.assertEqual(n['event_53_DelItem_item_IDs'],[2701,2702,2703,2704])
        self.assertFalse(n['sets_exactly_equal']);self.assertEqual(n['set_intersection_count'],1)
    def test_12_exact_one_ACCEPT_reward_not_assumed_executed(self):
        hits=[x for x in DATA['source_events'] if x['source_file'].endswith('sikkoku05') and x['type']=='ACCEPT']
        self.assertEqual(len(hits),1);self.assertEqual(hits[0]['event_no'],'53')
        self.assertEqual(hits[0]['GetItem_literal_values'],['20570,20571,20572'])
        self.assertEqual(hits[0]['DelItem_literal_values'],['2701*1,2702*1,2703*1,2704*1'])
        self.assertFalse(DATA['negative_evidence']['original_gameplay_awarded_or_warps_tested'])
    def test_13_three_rewards_are_B_only_not_blank_eternal_nonexistence(self):
        rows={x['original_item_id']:x for x in DATA['item_id_source_rows']}
        self.assertEqual(DATA['negative_evidence']['reward_IDs_missing_in_original_itemset_A_but_present_B'],[20570,20571,20572])
        for i in [20570,20571,20572]:
            self.assertNotIn('itemset.txt',rows[i]['original_row_instances'])
            self.assertIn('itemset0710.txt',rows[i]['original_row_instances'])
    def test_14_keep_two_ten_arg_versions_distinct_and_source_target(self):
        x=DATA['ten_arg_distinct_source_paths'];self.assertEqual(x['actual_create_referenced'],'npc/777/ten.arg')
        self.assertNotEqual(x['actual_sha256'],x['nonreferenced_sha256']);self.assertFalse(x['files_identical'])
        self.assertTrue(x['actual_source_text_pet_second_rebirth_mountability_warning_present'])
    def test_15_original_battle_parameters_are_only_static(self):
        b=DATA['battle_NPCEnemy_argument_records'];self.assertEqual(len(b),2)
        self.assertEqual([(x['warpfl_source'],x['warpx_source'],x['warpy_source']) for x in b],[(32011,56,36),(32021,29,57)])
        self.assertEqual([len(x['enemyno_literals']) for x in b],[5,10])
        self.assertTrue(all(x['native_win_warp_trigger_proven'] is False for x in b))
    def test_16_item_ids_and_source_94_col_sha_receipts(self):
        a=DATA['item_id_source_rows'];self.assertEqual(len(a),19)
        self.assertEqual(sum(len(x['original_row_instances']) for x in a),35)
        self.assertEqual(len(set(x['original_item_id'] for x in a)),19)
        self.assertTrue(all(x['source_field_count']==94 and len(x['original_line_sha256'])==64 for y in a for x in y['original_row_instances'].values()))
    def test_17_source_item_images_preserve_actual_pixel_gaps(self):
        a=DATA['original_TW1_source_item_RD_PNG_candidates'];self.assertEqual(len(a),19)
        self.assertEqual(sum(x['source_qualifying_pixel'] for x in a),16)
        self.assertEqual(sorted(x['original_image_alias'] for x in a if not x['source_qualifying_pixel']),[20241,24314,24315])
        self.assertEqual(DATA['negative_evidence']['original_TW1_index_missing_candidate_item_aliases'],[20241,24314,24315])
    def test_18_original_verified_candidate_2d_png_sha(self):
        a=DATA['original_TW1_source_item_RD_PNG_candidates']
        for x in a:
            if x['source_qualifying_pixel']:
                self.assertRegex(x['original_png_sha256'],r'^[0-9a-f]{64}$')
                self.assertEqual(len(x['dimensions']),2)
                self.assertTrue(all(y>0 for y in x['dimensions']))
    def test_19_three_actual_source_TW1_spr_pixels_not_species(self):
        a=DATA['original_TW1_source_native_SPR_PNG_candidates'];self.assertEqual(len(a),3)
        self.assertEqual([(x['numeric_graphic_key'],x['source_bitmap']) for x in a],[(100451,92185),(100389,105739),(100374,122515)])
        self.assertTrue(all(not x['same_deployment_mixed25'] for x in a))
    def test_20_counts_are_not_new_pets_or_original_runtime(self):
        c=DATA['counts'];self.assertEqual(c['total_source_TW1_distinct_2D_candidate_png'],19)
        self.assertEqual(c['new_original_RD_decodes'],0)
        self.assertFalse(DATA['provenance']['native_game_client_or_server_executed'])
        self.assertFalse(DATA['provenance']['TW1_and_community_mixed25_same_official_deployment_proven'])
    def test_21_private_custody_manifest_only_not_original_file_payloads(self):
        q=DATA['private_custody'];self.assertEqual(q['members'],35)
        self.assertEqual(q['individual_manifest_member_sha_verified'],34)
        self.assertEqual(q['TW1_original_source_candidate_PNG_members'],19)
        self.assertRegex(q['sha256'],r'^[0-9a-f]{64}$')
        self.assertFalse(DATA['private_original_asset_bytes_published'])
        text=SOURCE.read_text(encoding='utf-8')
        self.assertNotIn('NomalWindowMsg:',text)
        self.assertNotIn('askbattlemsg1:',text)
        self.assertNotIn('original_94_columns',text)

if __name__=='__main__':unittest.main()
