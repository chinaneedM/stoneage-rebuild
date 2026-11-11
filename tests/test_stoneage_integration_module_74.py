"""INTEGRATION74 public original-source replay; private original imagery stays out of CI."""
import copy
import hashlib
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
REC = ROOT / 'research/recovered'
REPORT = REC / 'STONEAGE-INTEGRATION74-YUANZANG-TWO-TW1-FULL-MOTION-SOURCE-R1.json'
O85 = REC / 'STONEAGE-O85-YUANZANG-DIALOGUE-BATTLE-SOURCE-R1.json'
PET15 = REC / 'STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json'
PET07 = REC / 'STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json'
HEX = re.compile(r'^[0-9a-f]{64}$')

def load(p):
    return json.loads(p.read_text(encoding='utf-8'))

def validate(r):
    assert r['schema']=='stoneage.integration74.yuanzang_original_source_to_TW1_motion_crosscarrier.r1'
    assert r['fresh_start']['current_blob']=='c89e0e33537990aa2132b47c40fef49a985a935c'
    assert r['fresh_start']['current_bytes']==2709173
    assert r['fresh_start']['main_head']=='ad2e6efd586231eff46e016b4a99539f1d316b76'
    assert r['fresh_start']['main_tree']=='8fc03d5627cfa395b83fe284ce3b5345e194b1fe'
    assert r['fresh_start']['main_actions_success']==26
    assert r['original_TW1_private_retail_zip_size']==372626292
    assert r['original_TW1_private_retail_zip_SHA256']=='3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24'
    assert r['original_TW1_zip_member_CRC_total']==379
    assert r['private_mixed25_npc_zip_member_CRC_total']==2205
    assert {f['path'] for f in r['reread_original_mixed25_npc_source_files']}=={'npc/100/sb_ganzo.create','npc/100/sb_ganzo.template','npc/100/sb_ganzo.arg'}
    old=r['existing_O85_original_later_mixed25_npc_evidence']
    assert old['npc_create_floor']==100 and old['npc_create_borncenter_four']==[472,297,1,1]
    assert old['npc_create_graphic_alias']==old['npc_template_type']==100401
    assert old['arg_ordered_enemy_instance_ids']==[253,254]
    assert [(x['enemy_id'],x['template_id'],x['source_template_graphic']) for x in old['original_two_instance_and_template_records']]==[(253,500,100401),(254,501,100280)]
    assert [(x['enemy_name'],x['template_name']) for x in old['original_two_instance_and_template_records']]==[('壞心眼的願藏','壞心眼的願藏'),('呼拔雄','呼拔吉')]
    assert old['mixed25_server_and_TW1_official_client_same_historical_deployment_proven'] is False
    groups=r['TW1_original_SPR_groups']
    assert len(groups)==2 and [g['graphic_numeric_candidate'] for g in groups]==[100280,100401]
    assert [(g['source_original_sequences'],g['source_frame_positions'],g['source_distinct_bitmap_keys']) for g in groups]==[(56,288,232),(104,496,344)]
    assert [g['full_original_SPR_segment_SHA256'] for g in groups]==['d2e12702aacf131e513a56a752be544b69256e17928c4ba041e816f0dc162198','0284af96efdff07da2b5b73ccc3f8a84a2a4158e9c653e3a4f3977293f3ec2a4']
    assert [g['source_directions'] for g in groups]==[list(range(8))]*2
    assert [g['source_actions'] for g in groups]==[[0,1,2,3,4,9,10],list(range(13))]
    assert [g['actual_RD_statuses'] for g in groups]==[{'strict':232},{'strict':343,'bounded_terminal_zero_outside_canvas':1}]
    assert all(len(g['source_sequences'])==g['source_original_sequences'] for g in groups)
    assert all(len({(s['direction'],s['action']) for s in g['source_sequences']})==g['source_original_sequences'] for g in groups)
    for g in groups:
        assert sum(x['frame_count'] for x in g['source_sequences'])==g['source_frame_positions']
        assert len(set(n for s in g['source_sequences'] for n in s['ordered_frame_bitmap_numbers']))==g['source_distinct_bitmap_keys']
        for i,s in enumerate(g['source_sequences']):
            assert s['ordinal']==i and len(s['ordered_frame_bitmap_numbers'])==s['frame_count']>0
            assert HEX.fullmatch(s['ordered_frames_SHA256'])
    rows=r['original_TW1_redecoded_RD_bitmap_receipts']
    assert len(rows)==576 and [x['adrn_physical_bitmap_no'] for x in rows]==sorted({x['adrn_physical_bitmap_no'] for x in rows})
    assert {x['adrn_physical_bitmap_no'] for x in rows}=={n for g in groups for s in g['source_sequences'] for n in s['ordered_frame_bitmap_numbers']}
    assert [x['adrn_physical_bitmap_no'] for x in rows if x['status']!='strict']==[82729]
    assert all(x['decoded_count']==x['canvas_count']+(x['status']!='strict') for x in rows)
    assert all(HEX.fullmatch(x[k]) for x in rows for k in ('record_sha256','RD_sha256','decoded_index_SHA256','pal1_candidate_PNG_sha256'))
    assert all(0<x['width']<400 and 0<x['height']<400 and x['RD_bytes']>=16 for x in rows)
    totals=r['totals'];assert (totals['original_animation_sequences'],totals['original_frame_positions'],totals['distinct_original_RD_bitmap_keys'])==(160,784,576)
    assert totals['unique_bitmaps_new_relative_to_prior_PET15']==totals['native_new_pets_identified']==0
    assert totals['private_PNG_candidates_recreated_this_work_unit']==576
    c=r['private_custody'];assert c['zip_size']==1826064 and c['zip_member_count']==581 and c['zip_all_member_CRC_verified'] is True
    assert c['independent_library_roundtrip_verified'] and c['independent_library_byte_comparison_equal']
    assert c['independent_library_recheck_CRC_members']==581 and HEX.fullmatch(c['zip_SHA256'])
    assert not c['private_bitmap_bytes_in_public_git'] and not c['private_NPC_source_bytes_in_public_git']
    assert r['source_validation']['prior_PET07_overlapping_original_bitmaps_checked']==31
    assert r['source_validation']['prior_PET07_three_original_binary_fields_same'] and r['source_validation']['prior_PET07_recreated_PNGs_match_RGBA_after_decode']
    assert r['source_validation']['prior_PET07_png_encoding_changes_only'] and r['source_validation']['prior_PET07_same_binary_PNG_encoding_count']==0
    assert r['private_observer_validation']['animation_selector_pairs_checked']==160
    assert r['private_observer_validation']['source_javascript_runtime_errors']==r['private_observer_validation']['source_external_network_requests']==0
    assert not r['private_observer_validation']['file_or_localhost_direct_navigation_success_claimed']
    assert not any(r['not_proven'].values())
    assert r['status']=={'stage_A':{'PARTIAL':7,'OPEN':2},'stage_B':'GATED','wiki':'GATED','R79':'PAUSED_NON_BLOCKING','overall_percent':None}
    assert r['crosscarrier_research_only'] is True
    return True

class OriginalYuanzangBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=load(REPORT); cls.o=load(O85); cls.pet=load(PET15); cls.pet07=load(PET07)

    def test_complete_source_contract(self):
        self.assertTrue(validate(self.r))

    def test_original_O85_NPC_and_two_enemy_template_ids(self):
        old=self.r['existing_O85_original_later_mixed25_npc_evidence']
        bridge=self.o['bridge_NPC']
        self.assertEqual((bridge['original_create_floor'],bridge['original_borncenter_four'],bridge['original_graphic_name_number'],bridge['combat_arg']['ordered_enemy_ids']),
                         (old['npc_create_floor'],old['npc_create_borncenter_four'],old['npc_create_graphic_alias'],old['arg_ordered_enemy_instance_ids']))
        for new in old['original_two_instance_and_template_records']:
            inst=next(x for x in self.o['enemy_instance_to_template'] if x['original_id']==new['enemy_id'])
            temp=next(x for x in self.o['enemy_instance_to_template'] if x['original_id']==new['template_id'])
            self.assertEqual((inst['template_id'],inst['name'],temp['name'],temp['source_graphic_number'],inst['source_row_without_line_ending_sha256'],temp['source_row_without_line_ending_sha256']),
                             (new['template_id'],new['enemy_name'],new['template_name'],new['source_template_graphic'],new['source_instance_row_SHA256'],new['source_template_row_SHA256']))
        for f in self.r['reread_original_mixed25_npc_source_files']:
            o=next(x for x in self.o['original_source_manifest'] if x['path'].endswith(f['path']))
            self.assertEqual((o['source_bytes'],o['source_sha256']),(f['bytes'],f['sha256']))

    def test_public_pet15_complete_animation_scope_without_inventing_new_pet(self):
        for g in self.r['TW1_original_SPR_groups']:
            p=next(x for x in self.pet['groups'] if x['graphic']==g['graphic_numeric_candidate'])
            self.assertEqual((p['group_index'],p['segment_sha256'],p['source_sequences'],p['frame_positions'],p['distinct_bitmaps'],p['source_directions'],p['source_actions']),
                             (g['original_TW1_SPRADRN_index'],g['full_original_SPR_segment_SHA256'],g['source_original_sequences'],g['source_frame_positions'],g['source_distinct_bitmap_keys'],g['source_directions'],g['source_actions']))
            # Mixed25 has PETFLG=1 on other templates sharing these image numbers: not pet species identity.
            self.assertTrue(any(x[2]==1 for rows in p['mixed25_same_number_rows'].values() for x in rows))
            self.assertTrue(any(x[2]==0 for rows in p['mixed25_same_number_rows'].values() for x in rows))

    def test_full_160_animation_records_independently_from_archived_TW1_frame_tables(self):
        from tools.stoneage_pet15_tw10_full_motion import selected_motion
        raw=selected_motion(graphics=[100280,100401])
        self.assertEqual(len(raw),2)
        for original,pub in zip(raw,self.r['TW1_original_SPR_groups']):
            self.assertEqual(original['graphic'],pub['graphic_numeric_candidate'])
            self.assertEqual(len(original['sequences']),len(pub['source_sequences']))
            for s,p in zip(original['sequences'],pub['source_sequences']):
                self.assertEqual((s['index'],s['direction'],s['action'],s['duration']),
                                 (p['ordinal'],p['direction'],p['action'],p['duration_raw']))
                self.assertEqual([f[0] for f in s['frames']],p['ordered_frame_bitmap_numbers'])
                self.assertEqual(hashlib.sha256(json.dumps(s['frames'],separators=(',',':')).encode()).hexdigest(),p['ordered_frames_SHA256'])

    def test_prior_PET07_original_RD_subset_identity_and_bounded_source(self):
        old={x[0]:x for x in self.pet07['source_actual_pixel_receipts']}
        overlap=0
        for x in self.r['original_TW1_redecoded_RD_bitmap_receipts']:
            row=old.get(x['adrn_physical_bitmap_no'])
            if row is None:continue
            overlap+=1
            self.assertEqual((x['adrn_record_index'],x['RD_sha256'],x['decoded_index_SHA256']),tuple(row[i] for i in (1,2,3)))
        self.assertEqual(overlap,31)
        self.assertIn(82729,[x['bitmap'] for x in self.pet07['source_undecodable_actual_RD_blocks']])
        self.assertEqual(self.pet['source_bitmap_statuses']['terminal_zero_outside_canvas'],5)

    def test_negative_swap_enemy_identity_without_original_master(self):
        d=copy.deepcopy(self.r);d['existing_O85_original_later_mixed25_npc_evidence']['original_two_instance_and_template_records'][1]['template_name']='呼拔雄'
        with self.assertRaises(AssertionError):validate(d)

    def test_negative_convert_primitive_frame_positions_to_unique_bitmaps(self):
        d=copy.deepcopy(self.r);d['TW1_original_SPR_groups'][0]['source_frame_positions']=232
        with self.assertRaises(AssertionError):validate(d)

    def test_negative_erase_original_bounded_RD_record(self):
        d=copy.deepcopy(self.r);next(x for x in d['original_TW1_redecoded_RD_bitmap_receipts'] if x['adrn_physical_bitmap_no']==82729)['status']='strict'
        with self.assertRaises(AssertionError):validate(d)

    def test_negative_early_version_same_deployment_promotion(self):
        d=copy.deepcopy(self.r);d['not_proven']['same_official_deployment']=True
        with self.assertRaises(AssertionError):validate(d)

    def test_negative_invent_new_pet_or_original_image(self):
        d=copy.deepcopy(self.r);d['totals']['unique_bitmaps_new_relative_to_prior_PET15']=576
        with self.assertRaises(AssertionError):validate(d)

    def test_negative_unverified_localhost_browser_navigation(self):
        d=copy.deepcopy(self.r);d['private_observer_validation']['file_or_localhost_direct_navigation_success_claimed']=True
        with self.assertRaises(AssertionError):validate(d)

    def test_negative_remove_source_sequence(self):
        d=copy.deepcopy(self.r);d['TW1_original_SPR_groups'][1]['source_sequences'].pop()
        with self.assertRaises(AssertionError):validate(d)

if __name__=='__main__':unittest.main()
