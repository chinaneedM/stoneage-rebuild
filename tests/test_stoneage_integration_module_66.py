"""Public-number and SHA test; does not require or publish original game assets."""
import copy,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'research/recovered/STONEAGE-INTEGRATION66-FOUR-ISLAND-TOUR-15-PET-TW1-ORIGINAL-PIXELS-R1.json'
Q=ROOT/'research/recovered/STONEAGE-QUEST25-FOUR-ISLAND-TOUR-ROUTES-SOURCE-R1.json'
P=ROOT/'research/recovered/STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json'
HEX=re.compile(r'^[a-f0-9]{64}$')
def check(r,q,p):
    assert r['schema']=='stoneage.integration66.four_island_tour_pet_reward_tw1_pixels_source_bounded.r1'
    assert r['evidence_scope']['official_same_deployment_proven'] is False
    assert r['evidence_scope']['reward_probability_proven'] is False
    assert r['evidence_scope']['native_game_execution_observed'] is False
    assert r['private_original_png_or_npc_text_published'] is False
    assert (r['private_custody']['zip_members'],r['private_custody']['zip_bytes'])==(242,1182803)
    assert HEX.fullmatch(r['private_custody']['zip_sha256'])
    scripts={s['path']:s for s in q['source_scripts']}
    enemies={e['getpet_integer']:e for e in q['existing_WORLD21_instance_links']}
    seen=[]
    for rrow,qr in zip(r['route_terminal_sources'],q['routes']):
        assert rrow['route']==qr['label']
        assert rrow['finish_source_script']==qr['finish']['script_path']
        assert rrow['finish_create_block_sha256']==qr['finish']['block_sha256']
        assert rrow['source_finish_floor']==qr['finish']['floor']
        script=scripts[rrow['finish_source_script']]
        assert script['sha256']==rrow['source_script_sha256']
        event=script['events'][rrow['source_event_ordinal']]
        assert event['section_sha256']==rrow['source_event_section_sha256']
        ids=[int(v) for v in event['commands']['GetPet'][0].split(',')]
        assert ids==rrow['original_GetPet_order']
        assert [e['source_instance_id'] for e in rrow['occurrences']]==ids
        for i,row in enumerate(rrow['occurrences']):
            old=enemies[row['source_instance_id']]
            assert row['position']==i+1
            assert row['same_source_template_id']==old['template_id_via_enemy_field4']
            assert row['cross_carrier_tw1_graphic_number']==old['original_template_graphic_id']
            seen.append(row)
    assert [r['route'] for r in r['route_terminal_sources']]==list('ABCD')
    assert [x['source_instance_id'] for x in r['route_terminal_sources'][1]['occurrences']].count(482)==2
    assert len(seen)==19 and len(set(x['source_instance_id'] for x in seen))==15
    source_groups={g[0]:g for g in p['source_groups']}
    source_pixels={x[0]:x for x in p['source_actual_pixel_receipts']}
    graphics=list(dict.fromkeys(x['cross_carrier_tw1_graphic_number'] for x in seen))
    assert len(graphics)==15 and graphics==[x['graphic_number'] for x in r['candidate_graphics']]
    numbers=set(); frames=0; count_seq=0
    for g in r['candidate_graphics']:
        old=source_groups[g['graphic_number']]
        assert (g['tw1_source_group_index'],g['tw1_full_animated_group_sha256'])==(old[1],old[2])
        assert len(g['bitmap_numbers'])==len(set(g['bitmap_numbers']))==g['unique_original_bitmaps_in_selected_actions']==old[6]
        assert set(g['bitmap_numbers']).issubset(source_pixels)
        numbers.update(g['bitmap_numbers'])
        assert len(g['source_sequences'])==len(old[5])==3
        for x,y in zip(g['source_sequences'],old[5]):
            assert [x['action'],x['direction'],x['frame_occurrences'],x['source_ordered_bitmap_u32le_sha256'],x['source_duration_word']]==y
            assert HEX.fullmatch(x['source_ordered_bitmap_u32le_sha256'])
            count_seq+=1;frames+=x['frame_occurrences']
    assert len(numbers)==236 and frames==347 and count_seq==45
    assert [x['bitmap'] for x in r['pixel_source_receipts']]==sorted(numbers)
    prior=[]
    for x in r['pixel_source_receipts']:
        raw=source_pixels[x['bitmap']]
        assert (x['tw1_original_rd_sha256'],x['pet07_current_candidate_png_sha256'],x['width'],x['height'])==(raw[2],raw[8],raw[5],raw[6])
        assert HEX.fullmatch(x['gallery_png_sha256'])
        if x['gallery_variant']=='PRIOR_PET06_PNG':
            assert x['gallery_png_sha256']!=raw[8]
            prior.append(x['bitmap'])
        else:
            assert x['gallery_variant']=='PET07_CURRENT_PNG' and x['gallery_png_sha256']==raw[8]
    assert prior==list(range(113515,113521))
    assert r['counts']=={'source_routes':4,'source_GetPet_occurrences':19,'distinct_mixed25_enemy_instance_numbers':15,'distinct_TW1_numeric_graphic_candidate_groups':15,'actual_existing_TW1_action_direction_sequences_rechecked':45,'actual_existing_TW1_frame_positions_rechecked':347,'actual_existing_TW1_distinct_bitmap_PNG_rechecked':236,'gallery_png_matched_pet07_current_candidate':230,'gallery_png_matched_documented_prior_pet06_variant':6,'new_original_rd_binary_decodes_this_work':0,'native_commercial_client_or_server_executions':0}
    return True
class Integration66Evidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(R.read_text());cls.q=json.loads(Q.read_text());cls.p=json.loads(P.read_text())
    def test_validated_source_graph(self):
        self.assertTrue(check(self.r,self.q,self.p))
    def test_reject_duplicate_lost(self):
        x=copy.deepcopy(self.r);x['route_terminal_sources'][1]['original_GetPet_order'].remove(482)
        with self.assertRaises(AssertionError):check(x,self.q,self.p)
    def test_reject_same_deployment_promotion(self):
        x=copy.deepcopy(self.r);x['evidence_scope']['official_same_deployment_proven']=True
        with self.assertRaises(AssertionError):check(x,self.q,self.p)
    def test_reject_wrong_action_frames(self):
        x=copy.deepcopy(self.r);x['candidate_graphics'][0]['source_sequences'][0]['source_ordered_bitmap_u32le_sha256']='0'*64
        with self.assertRaises(AssertionError):check(x,self.q,self.p)
    def test_reject_unqualified_palette(self):
        x=copy.deepcopy(self.r);next(t for t in x['pixel_source_receipts'] if t['bitmap']==113515)['gallery_variant']='PET07_CURRENT_PNG'
        with self.assertRaises(AssertionError):check(x,self.q,self.p)
    def test_reject_new_decodes_without_source(self):
        x=copy.deepcopy(self.r);x['counts']['new_original_rd_binary_decodes_this_work']=1
        with self.assertRaises(AssertionError):check(x,self.q,self.p)
if __name__=='__main__':unittest.main()
