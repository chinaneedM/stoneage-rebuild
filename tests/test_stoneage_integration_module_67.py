"""INTEGRATION67 public provenance joins. No original commercial bytes required."""
import copy
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research/recovered'
def read(name):
    return json.loads((REC/name).read_text(encoding='utf-8'))
def valid(r,q,w,p):
    assert r['schema']=='stoneage.integration67.spirit_king_three_getpet_tw1_original_pixel_candidates.r1'
    assert r['initial_remote']['preserved_current_blob']=='c89e0e33537990aa2132b47c40fef49a985a935c'
    assert r['evidence_scope']['official_same_build_deployment_proven'] is False
    assert r['evidence_scope']['original_pet_species_identified'] is False
    assert r['evidence_scope']['original_reward_execution_observed'] is False
    assert r['evidence_scope']['actual_native_palette_selection_verified'] is False
    assert r['private_copyright_material_in_public_git'] is False
    assert r['counts']=={'original_getpet_commands':3,'distinct_same_carrier_enemy_ids':3,'distinct_source_tw1_sprite_candidate_groups':3,'existing_tw1_action_direction_sequences_rechecked':9,'existing_source_ordered_frame_positions_rechecked':74,'existing_distinct_original_tw1_PNG_rechecked':48,'existing_png_equal_pet07_current_candidate':48,'prior_palette_variant_applied':0,'new_original_RD_binary_decodes':0,'original_gameplay_runs':0}
    assert (r['private_custody']['zip_bytes'],r['private_custody']['members'])==(437505,56)
    assert re.fullmatch('[a-f0-9]{64}',r['private_custody']['zip_sha256'])
    qfiles={x['path']:x for x in q['source_event_scripts']}
    wrows={x['getpet_integer']:x for x in w['original_enemy_instance_to_template_lookups']}
    wfiles={x['path']:x for x in w['source_GetPet_scripts_and_event_blocks']}
    groups={x[0]:x for x in p['source_groups']}
    pixels={x[0]:x for x in p['source_actual_pixel_receipts']}
    expected=[('king/event69_1',355,100376,34),('king/event69_24',484,100430,18),('king/event69_7',1479,100451,120)]
    counts=0; frames=0; bitmaps=[]
    for x,expected_row in zip(r['original_pet_reward_source_joins'],expected):
        path,inst,graphic,line=expected_row
        assert (x['script'],x['original_getpet_instance_id'],x['tw1_numeric_graphic_candidate'],x['original_GetPet_line_number'])==expected_row
        old=qfiles[path]
        assert x['source_script_sha256']==old['sha256']
        assert x['source_script_bytes']==old['bytes']
        ev=old['events'][x['source_event_ordinal']]
        assert ev['section_sha256']==x['source_event_section_sha256']
        assert x['source_condition_literal']==ev['condition_literal']
        assert ev['commands']['GetPet']==[str(inst)]
        wold=wrows[inst]
        assert x['enemy_master_line_sha256']==wold['enemy_master_line_sha256']
        assert x['template_master_line_sha256']==wold['template_master_line_sha256']
        assert x['template_id']==wold['template_id_via_enemy_field4']
        assert x['tw1_numeric_graphic_candidate']==wold['original_template_graphic_id']
        command=next(c for c in wfiles[path]['commands'] if c['getpet_line']==line)
        assert command['getpet_line_sha256']==x['original_GetPet_line_sha256']
        assert command['raw_integer_tokens_in_order']==[inst]
        oldg=groups[graphic]
        assert (x['tw1_source_spr_group_index'],x['tw1_original_spr_group_sha256'])==(oldg[1],oldg[2])
        assert len(x['original_distinct_bitmap_numbers'])==len(set(x['original_distinct_bitmap_numbers']))==oldg[6]==16
        assert len(x['source_selected_sequences'])==len(oldg[5])==3
        for y,prev in zip(x['source_selected_sequences'],oldg[5]):
            assert [y['action'],y['direction'],y['frame_occurrences'],y['source_ordered_bitmap_u32le_sha256'],y['source_duration_word']]==prev
            frames+=y['frame_occurrences'];counts+=1
        assert x['original_selected_frame_occurrences']==sum(s['frame_occurrences'] for s in x['source_selected_sequences'])
        bitmaps.extend(x['original_distinct_bitmap_numbers'])
    assert len(bitmaps)==len(set(bitmaps))==48
    assert frames==74 and counts==9
    assert [x['bitmap'] for x in r['source_actual_TW1_original_pixel_receipts']]==sorted(bitmaps)
    for row in r['source_actual_TW1_original_pixel_receipts']:
        old=pixels[row['bitmap']]
        assert (row['source_tw1_original_RD_sha256'],row['source_tw1_original_decoded_pixel_sha256'],row['source_tw1_palette1_candidate_PNG_sha256'],row['width'],row['height'],row['source_RD_flag'])==(old[2],old[3],old[8],old[5],old[6],old[4])
        assert re.fullmatch('[a-f0-9]{64}',row['source_tw1_palette1_candidate_PNG_sha256'])
    return True

class Integration67(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=read('STONEAGE-INTEGRATION67-SPIRIT-KING-THREE-GETPET-TW1-ORIGINAL-PIXELS-R1.json')
        cls.q=read('STONEAGE-QUEST29-SPIRIT-KING-EVENT69-SOURCE-R1.json')
        cls.w=read('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-21-GETPET-QUEST-BRANCHES-R1.json')
        cls.p=read('STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json')
    def test_exact_source_link(self):
        self.assertTrue(valid(self.r,self.q,self.w,self.p))
    def test_reject_unverified_original_deployment(self):
        x=copy.deepcopy(self.r);x['evidence_scope']['official_same_build_deployment_proven']=True
        with self.assertRaises(AssertionError):valid(x,self.q,self.w,self.p)
    def test_reject_wrong_enemy_template(self):
        x=copy.deepcopy(self.r);x['original_pet_reward_source_joins'][0]['template_id']+=1
        with self.assertRaises(AssertionError):valid(x,self.q,self.w,self.p)
    def test_reject_wrong_original_getpet_line(self):
        x=copy.deepcopy(self.r);x['original_pet_reward_source_joins'][1]['original_GetPet_line_sha256']='0'*64
        with self.assertRaises(AssertionError):valid(x,self.q,self.w,self.p)
    def test_reject_changed_sprite_frame_order_sha(self):
        x=copy.deepcopy(self.r);x['original_pet_reward_source_joins'][2]['source_selected_sequences'][0]['source_ordered_bitmap_u32le_sha256']='0'*64
        with self.assertRaises(AssertionError):valid(x,self.q,self.w,self.p)
    def test_reject_bitmap_substitution(self):
        x=copy.deepcopy(self.r);x['original_pet_reward_source_joins'][0]['original_distinct_bitmap_numbers'][0]=999999
        with self.assertRaises(AssertionError):valid(x,self.q,self.w,self.p)
    def test_reject_unqualified_palette(self):
        x=copy.deepcopy(self.r);x['source_actual_TW1_original_pixel_receipts'][0]['source_tw1_palette1_candidate_PNG_sha256']='0'*64
        with self.assertRaises(AssertionError):valid(x,self.q,self.w,self.p)
    def test_reject_fake_new_decode(self):
        x=copy.deepcopy(self.r);x['counts']['new_original_RD_binary_decodes']=1
        with self.assertRaises(AssertionError):valid(x,self.q,self.w,self.p)

if __name__=='__main__': unittest.main()
