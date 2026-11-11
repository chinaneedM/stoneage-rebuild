"""INTEGRATION73 public derived evidence audit; does not load proprietary original assets."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research'/'recovered'
REPORT=REC/'STONEAGE-INTEGRATION73-SAMUGIRU-SOURCE-12-ORIGINAL-ITEM-PIXELS-R1.json'
ITEM=REC/'item-module-01'
SHARDS=('01','04','05','07')
SCHEMA='stoneage.integration73.samugiru_five_gems_and_hero_blessing_source_bound_original_pixel_crosswalk.r1'
ITEM_IDS=[1501,1512,12667,12507,12849,18538,18539,18540,18541,18542,18537,18543]
ALIASES=[23014,23007,24451,24422,24406,24067,24066,24065,24064,24068,22038,24053]
BITMAPS=[6550,6543,6618,6589,6573,6777,6776,6775,6774,6778,6505,6763]

def load(p):return json.loads(p.read_text(encoding='utf-8'))

def check(d):
    assert d['schema']==SCHEMA
    assert d['fresh_remote']['preserved_full_CURRENT_git_blob']=='c89e0e33537990aa2132b47c40fef49a985a935c'
    assert d['fresh_remote']['preserved_full_CURRENT_bytes']==2709173
    assert d['fresh_remote']['full_CURRENT_unchanged'] is True
    scopes=d['source_scopes']
    assert 'COMMUNITY_MIXED25' in scopes['NPC_and_original_item_rows']
    assert 'TAIWAN_1_0' in scopes['real_RD_pixels']
    assert scopes['item_and_pixel_same_official_deployment_proven'] is False
    assert scopes['original_quest_native_execution'] is False
    assert scopes['origin_classification']=='ORIGIN_UNRESOLVED'
    cr=d['original_create_to_script_links']
    assert len(cr)==2
    assert [(x['source_create_file'],x['floor_id'],x['borncenter_raw'],x['graphic_alias'],x['linked_original_script']) for x in cr]==[
        ('poru/hero.create',5501,[43,5,1,1],100036,'poru/samugiru'),
        ('poru/samugiru01.create',1013,[14,16,1,1],16009,'poru/girl')]
    assert all(len(x['original_block_sha256'])==64 for x in cr)
    fs=d['original_source_files']
    assert [x['path'] for x in fs]==['poru/hero.create','poru/samugiru01.create','poru/samugiru','poru/girl','poru/samugiru_test']
    assert all(x['bytes']>100 and len(x['sha256'])==64 and len(x['crc32'])==8 for x in fs)
    assert len({x['sha256'] for x in fs})==5
    ev=d['original_event_blocks_static_source']
    assert len(ev)==17
    a=[x for x in ev if x['source_script']=='poru/samugiru']
    b=[x for x in ev if x['source_script']=='poru/girl']
    assert len(a)==10 and len(b)==7
    assert [x['source_ordinal'] for x in a]==list(range(10))
    assert [x['source_ordinal'] for x in b]==list(range(7))
    assert [x['literal_type'] for x in a]==['MESSAGE']+['ACCEPT']*5+['MESSAGE']*4
    assert [x['literal_type'] for x in b]==['ACCEPT']*6+['MESSAGE']
    assert all(x['literal_eventno']==-1 and len(x['original_block_sha256'])==64 for x in ev)
    assert all(x['source_line_end_inclusive_1based']>=x['source_line_start_1based'] for x in ev)
    for e in a[1:6]:
        assert e['literal_NpcWarp'] and len(e['literal_NpcWarp'][0].split(','))==11
        assert 'NOWEV=63' in e['literal_event_condition']
    assert all('ENDEV=63' in e['literal_event_condition'] for e in b)
    pairs=d['source_limited_derived_relationships']['samugiru_five_explicit_one_item_input_to_gem_outputs']
    assert pairs==[[1501,18538],[1512,18539],[12667,18540],[12507,18541],[12849,18542]]
    for i,(inp,out) in enumerate(pairs):
        branch=a[i+1]
        assert branch['literal_GetItem']==[str(out)]
        assert branch['literal_DelItem']==[f'{inp}*1']
    assert b[0]['literal_DelItem']==['18538,18539,18540,18541,18542']
    assert b[0]['literal_GetItem']==['18537,18543*5']
    for i,k in enumerate(range(18538,18543),start=1):
        assert b[i]['literal_GetItem']==['18543'] and b[i]['literal_DelItem']==[str(k)]
    r=d['source_limited_derived_relationships']
    assert r['girl_five_gems_all_required_in_first_ACCEPT']==list(range(18538,18543))
    assert r['girl_first_ACCEPT_getitem_literal']=='18537,18543*5'
    assert r['girl_single_gem_ACCEPT_count']==5
    assert r['girl_single_gem_getitem_literal']=='18543'
    assert r['source_samugiru_test_is_present_but_direct_CREATE_links']==0
    assert r['source_test_filename_does_not_prove_runtime_inactive'] is True
    assert r['samugiru_event_predicate']=='NOWEV=63' and r['girl_event_predicate']=='ENDEV=63'
    assert r['different_literal_event_predicates_must_not_be_collapsed'] is True
    assert r['samugiru_NpcWarp_literal_candidate_positions_per_ACCEPT']==11
    assert not r['NpcWarp_randomness_or_execution_proven'] and not r['native_event_priority_or_item_transaction_proven']
    items=d['cross_source_12_item_pixel_candidates']
    assert [x['item_id'] for x in items]==ITEM_IDS
    assert [x['original_item_image_alias'] for x in items]==ALIASES
    assert [x['tw1_physical_bitmap_number'] for x in items]==BITMAPS
    assert len(set(ALIASES))==len(set(BITMAPS))==12
    assert all(x['original_itemset_A_row_SHA256']==x['original_itemset_B_row_SHA256'] for x in items)
    assert all(x['tw1_width']>0 and x['tw1_height']>0 for x in items)
    assert all(not x['cross_carrier_same_official_deployment_proven'] for x in items)
    assert all(len(x[k])==64 for x in items for k in ('original_itemset_A_row_SHA256','tw1_actual_original_RD_SHA256','tw1_original_indexed_pixel_SHA256','tw1_saved_candidate_RGBA_SHA256','tw1_saved_candidate_PNG_SHA256'))
    src=d['independent_private_source_replay']
    assert src['original_NPC_zip_CRC_verified_members']==2205
    assert src['original_ITEM_zip_CRC_verified_members']==838
    assert src['selected_original_item94_rows_verified']==24
    assert src['existing_saved_real_PNG_sha_and_size_verified']==12
    assert src['new_raw_retail_REAL_RD_decodes']==0 and src['original_native_script_runs']==0
    priv=d['private_original_custody']
    assert priv['private_archive_members']==31
    assert priv['private_archive_bytes']>0 and len(priv['private_archive_sha256'])==64
    assert priv['CRC_all_pass'] is True and priv['independent_library_readback_verified'] is True
    assert priv['copyright_originals_published_on_GitHub'] is False
    assert d['status']=={'stage_A':{'PARTIAL':7,'OPEN':2},'stage_B':'GATED','wiki':'GATED','R79':'PAUSED_NON_BLOCKING','overall_percent':None}
    assert all(x is False for x in d['not_proven'].values())

class Integration73PublicAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load(REPORT)
        cls.older={row[0]:row for num in SHARDS for row in load(ITEM/f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{num}-R1.json')['rows']}
    def test_source_bound_contract(self):check(self.d)
    def test_original_item_source_rows_match_existing_immutable_public_shards(self):
        for x in self.d['cross_source_12_item_pixel_candidates']:
            old=self.older[x['item_id']]
            self.assertEqual(old[1:5],[x['original_itemset_A_row_SHA256'],x['original_itemset_B_row_SHA256'],x['original_item_image_alias'],x['original_item_image_alias']])
            self.assertEqual(old[8:10],['REAL_RD_DECODED_CROSS_CARRIER']*2)
    def test_replay_original_five_exchange_inputs_in_order(self):
        events=[x for x in self.d['original_event_blocks_static_source'] if x['source_script']=='poru/samugiru' and x['literal_type']=='ACCEPT']
        self.assertEqual([(b['literal_DelItem'],b['literal_GetItem']) for b in events],[( [f'{a}*1'],[str(c)] ) for a,c in [[1501,18538],[1512,18539],[12667,18540],[12507,18541],[12849,18542]]])
    def test_girl_combined_and_single_exchange_are_separate(self):
        x=[v for v in self.d['original_event_blocks_static_source'] if v['source_script']=='poru/girl' and v['literal_type']=='ACCEPT']
        self.assertEqual((x[0]['literal_DelItem'],x[0]['literal_GetItem']),(['18538,18539,18540,18541,18542'],['18537,18543*5']))
        self.assertEqual([v['literal_DelItem'][0] for v in x[1:]],list(map(str,range(18538,18543))))
    def test_negative_reward_multiplier_must_not_change(self):
        d=copy.deepcopy(self.d);d['original_event_blocks_static_source'][10]['literal_GetItem']=['18537,18543*1']
        with self.assertRaises(AssertionError):check(d)
    def test_negative_do_not_promote_cross_carrier_to_same_official_deployment(self):
        d=copy.deepcopy(self.d);d['cross_source_12_item_pixel_candidates'][0]['cross_carrier_same_official_deployment_proven']=True
        with self.assertRaises(AssertionError):check(d)
    def test_negative_do_not_mix_alias_and_physical_bitmap(self):
        d=copy.deepcopy(self.d);d['cross_source_12_item_pixel_candidates'][5]['tw1_physical_bitmap_number']=24067
        with self.assertRaises(AssertionError):check(d)
    def test_negative_do_not_merge_nowev_with_endev(self):
        d=copy.deepcopy(self.d);d['source_limited_derived_relationships']['girl_event_predicate']='NOWEV=63'
        with self.assertRaises(AssertionError):check(d)
    def test_negative_keep_source_create_floor_and_exact_center(self):
        d=copy.deepcopy(self.d);d['original_create_to_script_links'][1]['floor_id']=5501
        with self.assertRaises(AssertionError):check(d)
    def test_negative_keep_test_source_unreferenced_within_examined_CREATE(self):
        d=copy.deepcopy(self.d);d['source_limited_derived_relationships']['source_samugiru_test_is_present_but_direct_CREATE_links']=1
        with self.assertRaises(AssertionError):check(d)
    def test_negative_no_native_execution_or_new_rd_claim(self):
        d=copy.deepcopy(self.d);d['independent_private_source_replay']['new_raw_retail_REAL_RD_decodes']=12
        with self.assertRaises(AssertionError):check(d)
    def test_negative_no_private_originals_in_public_git(self):
        d=copy.deepcopy(self.d);d['private_original_custody']['copyright_originals_published_on_GitHub']=True
        with self.assertRaises(AssertionError):check(d)

if __name__=='__main__':unittest.main()