"""Public numeric / hash-only historical source replay; no proprietary source bytes."""
from __future__ import annotations
import copy
import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / 'research/recovered/STONEAGE-INTEGRATION104-31900-ITEM-GATE-DAT-SOURCE-R1.json'

def load():
    return json.loads(RECEIPT.read_text(encoding='utf-8'))

def validate(d):
    assert d['schema']=='stoneage.integration104_giiru_31900_original_gate_and_DAT_source_bounded_r1'
    c=d['source_create_rows_original_BYTE_SHA_numeric_only'];h=d['source_handlers_original_byte_sha_and_CP950_only']
    w=d['static_warp_source_literally_NUMERIC_NOT_RUNTIME'];f=d['source_qualified_original_DAT_headers_previous_only']
    items=d['source_original_ITEM_two_table_rows_and_separate_TW1_cross_source']
    imgs=d['separate_previous_TW1_retail_source_image_PNG_hashes_only'];ct=d['counts'];b=d['source_contradiction_preserved_verbatim_numeric']
    assert len(c)==ct['CREATE_rows']==47
    assert sorted(x['ordinal'] for x in c)==list(range(47))
    assert len(set(tuple(x['original_byte_span']) for x in c))==47
    assert len(h)==ct['original_handlers_really_read_sha_cp950']==18
    assert len(w)==ct['source_warp_static_routes']==16
    assert len(f)==ct['source_qualified_DAT_headers_reused']==9
    assert Counter(x['template'] for x in c)=={'npcgen_mugon':27,'npcgen_warpman':14,'npcgen_man':3,'npcgen_warp':2,'npcgen_signboard':1}
    assert len(set(x['floor'] for x in c))==6
    assert sorted(set(x['floor'] for x in c)|set(x['target_floor'] for x in w))==sorted(x['floor'] for x in f)
    byfloor={x['floor']:x for x in f}
    assert len(byfloor)==9
    for a in f:
        assert a['original_DAT_bytes']==8+6*a['header_width']*a['header_height']
        assert re.fullmatch(r'[0-9a-f]{64}',a['original_DAT_sha256'])
        assert a['source_CREATE_count']==sum(x['floor']==a['floor'] for x in c)
        assert a['source_WARP_target_count']==sum(x['target_floor']==a['floor'] for x in w)
    for a in c:
        assert re.fullmatch(r'[0-9a-f]{64}',a['original_CREATE_block_sha256'])
        assert a['original_byte_span'][0]<a['original_byte_span'][1]
        assert a['borncorner_xyxy'][:2]==a['borncorner_xyxy'][2:]
        q=byfloor[a['floor']];x,y=a['borncorner_xyxy'][:2]
        assert a['source_xy_in_qualified_DAT_header_dimensions']==(0<=x<q['header_width'] and 0<=y<q['header_height'])
    assert ct['source_CREATE_coordinates_in_DAT_bounds']==46
    assert ct['source_CREATE_coordinates_OUT_of_DAT_bounds']==1
    assert [x['ordinal'] for x in c if not x['source_xy_in_qualified_DAT_header_dimensions']]==[3]
    assert b==[{'block_ordinal':3,'floor':31902,'source_xy':[9,67],'DAT_dimensions':[15,10],'violation':'ORIGINAL_SOURCE_XY_OUT_OF_BOUND_FOR_QUALIFIED_DAT_HEADER'}]
    assert len({x['private_path'] for x in h})==18
    assert sum(x['original_bytes'] for x in h)==ct['original_handler_bytes_really_read']==4249
    assert all(x['CP950_strict_roundtrip'] for x in h)
    assert all(re.fullmatch(r'[0-9a-f]{64}',x['original_sha256']) for x in h)
    assert sorted(x['referenced_original_handler_sha256'] for x in c if x['referenced_original_handler_sha256'])==sorted(x['original_sha256'] for x in h)
    assert sorted(x['source_ordinal'] for x in w)==sorted(x['ordinal'] for x in c if x['template'] in ('npcgen_warp','npcgen_warpman'))
    assert len({(x['source_floor'],*x['source_xy'],x['target_floor'],*x['target_xy']) for x in w})==16
    for x in w:
        floor=byfloor[x['target_floor']]
        assert x['target_in_qualified_DAT_bounds']==(0<=x['target_xy'][0]<floor['header_width'] and 0<=x['target_xy'][1]<floor['header_height'])
        assert x['target_DAT_sha256']==floor['original_DAT_sha256']
        src=c[x['source_ordinal']]
        assert src['floor']==x['source_floor'] and src['borncorner_xyxy'][:2]==x['source_xy']
        assert src['referenced_original_handler_sha256']==x['original_handler_sha256']
    assert all(x['target_in_qualified_DAT_bounds'] for x in w)
    guarded2548=[x for x in w if x['source_FREE_ITEM_number']==2548]
    guarded2549=[x for x in w if x['source_FREE_ITEM_number']==2549]
    plain=[x for x in w if x['source_FREE_ITEM_number'] is None]
    assert len(guarded2548)==ct['source_13_warpman_delitem2548']==13
    assert all(x['source_floor']==31910 and x['source_DelItem_literal_ID_and_count']==[2548,1] and x['source_MONEY_literal']==-1 for x in guarded2548)
    assert len(guarded2549)==ct['source_1_warpman_FREE_item2549_no_DelItem']==1
    assert guarded2549[0]['source_floor']==31903 and guarded2549[0]['source_DelItem_literal_ID_and_count'] is None
    assert len(plain)==ct['source_2_inline_warp_no_argument_file']==2
    assert all(x['source_DelItem_literal_ID_and_count'] is None and x['original_handler_path'] is None for x in plain)
    assert sorted(x['item_ID'] for x in items)==[2548,2549]
    assert sorted(x['original_numeric_image_alias'] for x in items)==[24058,24112]
    assert sorted(map(int,imgs))==[24051,24058,24112]
    for a in items:
        assert a['original_itemset_a_complete_row_sha256']==a['original_itemset_b_complete_row_sha256']
        assert a['two_source_original_lines_byte_equal'] is True
        assert a['separate_TW1_original_RD_candidate_PNG_sha256']==imgs[str(a['original_numeric_image_alias'])]['sha256']
    assert ct['source_static_mugon_numeric_graphicname_24051_configurations']==27
    assert ct['source_original_IMAGE_new_RD_decode']==ct['source_original_DAT_new_read']==0
    assert d['historical_current_original_git_blob']=='c89e0e33537990aa2132b47c40fef49a985a935c'
    assert d['historical_current_original_bytes']==2709173
    assert d['Stage_A']=='7 PARTIAL + 2 OPEN' and d['Stage_B']=='GATED' and d['wiki']=='GATED'
    assert d['R79']=='PAUSED_NON_BLOCKING'
    assert all(x is False for k,x in d['source_negative_bounds'].items() if k!='historical_overall_completion_percentage')
    assert d['source_negative_bounds']['historical_overall_completion_percentage'] is None

class TestIntegration104(unittest.TestCase):
    def test_00_public_replay(self):validate(load())
    def test_01_floor_header_source_conflict_is_not_erased(self):
        a=load();a['source_create_rows_original_BYTE_SHA_numeric_only'][3]['borncorner_xyxy']=[9,7,9,7]
        with self.assertRaises(AssertionError):validate(a)
    def test_02_unverified_warp_destination_rejected(self):
        a=load();a['static_warp_source_literally_NUMERIC_NOT_RUNTIME'][0]['target_xy']=[999,999]
        with self.assertRaises(AssertionError):validate(a)
    def test_03_key2548_not_erased(self):
        a=load();next(x for x in a['static_warp_source_literally_NUMERIC_NOT_RUNTIME'] if x['source_FREE_ITEM_number']==2548)['source_DelItem_literal_ID_and_count']=None
        with self.assertRaises(AssertionError):validate(a)
    def test_04_key2549_not_false_consume(self):
        a=load();next(x for x in a['static_warp_source_literally_NUMERIC_NOT_RUNTIME'] if x['source_FREE_ITEM_number']==2549)['source_DelItem_literal_ID_and_count']=[2549,1]
        with self.assertRaises(AssertionError):validate(a)
    def test_05_source_tw1_not_merged(self):
        a=load();a['source_original_ITEM_two_table_rows_and_separate_TW1_cross_source'][0]['original_numeric_image_alias']=24051
        with self.assertRaises(AssertionError):validate(a)
    def test_06_source_block_identity_mutation_fails(self):
        a=load();a['source_create_rows_original_BYTE_SHA_numeric_only'][1]['original_CREATE_block_sha256']='BAD'
        with self.assertRaises(AssertionError):validate(a)
    def test_07_source_handler_sha_mutation_fails(self):
        a=load();a['source_handlers_original_byte_sha_and_CP950_only'][1]['original_sha256']='f'*64
        with self.assertRaises(AssertionError):validate(a)
    def test_08_DAT_dimension_counterexample_fails(self):
        a=load();next(x for x in a['source_qualified_original_DAT_headers_previous_only'] if x['floor']==31902)['header_height']=68
        with self.assertRaises(AssertionError):validate(a)
    def test_09_no_official_runtime_claim(self):
        a=load();a['source_negative_bounds']['original_client_or_server_runtime_started']=True
        with self.assertRaises(AssertionError):validate(a)
    def test_10_no_new_original_RD_claim(self):
        a=load();a['counts']['source_original_IMAGE_new_RD_decode']=1
        with self.assertRaises(AssertionError):validate(a)
    def test_11_no_unfounded_completion_percent(self):
        a=load();a['source_negative_bounds']['historical_overall_completion_percentage']=0.75
        with self.assertRaises(AssertionError):validate(a)

if __name__=='__main__':unittest.main()
