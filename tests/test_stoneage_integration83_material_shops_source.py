"""Source-bounded acceptance of 1009/4009 material shop original evidence.

Public tests replay source-derived IDs/hashes/negative evidence; no private
commercial scripts, DAT, PNG, or engine runtime is included in this repository.
"""
from __future__ import annotations
import copy
import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/recovered/STONEAGE-INTEGRATION83-1009-4009-ORIGINAL-MATERIAL-SHOP-2D-SOURCE-R1.json'
HEX = re.compile(r'^[0-9a-f]{64}$')


def require(condition, why):
    if not condition:
        raise ValueError(why)


def audit(d):
    t = d['totals']
    require(d['schema'] == 'stoneage.integration83.original_1009_4009_five_material_stalls_cross_carrier_icon_source.r1', 'schema')
    require(d['historical_CURRENT_STATE_original_blob_unchanged'] == 'c89e0e33537990aa2132b47c40fef49a985a935c', 'CURRENT blob')
    p = d['source_archives']
    require(p['NPC_saved_subset']['sha256'] == 'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f', 'NPC source')
    require(p['ITEM_saved_subset']['sha256'] == 'cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa', 'item source')
    require((p['NPC_saved_subset']['members'],p['ITEM_saved_subset']['members'])==(2205,838), 'original member counts')
    require(p['NPC_saved_subset']['all_crc_verified'] is True and p['ITEM_saved_subset']['all_crc_verified'] is True, 'original CRC custody')
    shops=d['shops']; items=d['items']; images=d['images'];pairs=d['paired_stalls']
    require(len(shops)==len(d['creates'])==10, 'ten original CREATEs')
    require(len(items)==123 and len(images)==49 and len(pairs)==5, 'join cardinalities')
    require(Counter(s['floor_id'] for s in shops)=={1009:5,4009:5}, 'two source floors')
    require(len({s['original_arg_path'] for s in shops})==10, 'original argument paths')
    require(len({s['original_CREATE_block_SHA256'] for s in shops})==10, 'distinct original CREATE blocks')
    require(len({s['original_arg_SHA256'] for s in shops})==10, 'distinct original argument source SHA')
    require(all(HEX.fullmatch(s['original_arg_SHA256']) for s in shops), 'source SHA format')
    create_by_arg={c['original_arg_path']:c for c in d['creates']}
    byfloor={(s['floor_id'],int(s['original_arg_path'].split('_')[-1])):s for s in shops}
    occurrence_count=0; singles=0;ranges=0;range_candidates=0
    all_ids=set()
    for s in shops:
        require(s['enemy_original_source_shape']=='npcgen_shop|file:', 'not a real npcgen_shop')
        require(s['original_itemlist_is_native_runtime_inventory_proven'] is False, 'range uncertainty')
        require(HEX.fullmatch(s['original_CREATE_block_SHA256']), 'original CREATE hash')
        require(HEX.fullmatch(s['source_ItemList_token_SHA256']), 'ItemList hash')
        c=create_by_arg[s['original_arg_path']]
        require(s['original_CREATE_block_SHA256']==c['original_CREATE_block_SHA256'], 'CREATE link')
        require(s['original_CREATE_block_byte_start_inclusive']<s['original_CREATE_block_byte_end_exclusive'], 'CREATE byte range')
        require(s['borncorner_original_raw'].split(',')[0:2]==['27',s['original_arg_path'].split('_')[-1]], 'source coordinate path consistency')
        require(s['dir_original_raw']==6, 'original direction source')
        toks=[x.strip() for x in s['original_ItemList_raw_text'].split(',')]
        require(toks==[x['source_token'] for x in s['original_token_evidence']], 'source list lexical order')
        vals=[]
        for x in s['original_token_evidence']:
            if x['evidence']=='EXPLICIT_SINGLE_ID_IN_ORIGINAL_TEXT':
                require('id' in x and x['source_token']==str(x.get('id')), 'explicit source token')
                vals.append(x['id']);singles+=1
            elif x['evidence']=='RANGE_INCLUSIVE_INTERPRETATION_ONLY':
                lo,hi=x['low'],x['high'];require(x['source_token']==f'{lo}-{hi}' and 0 <= lo <= hi and hi-lo<100,'range literal')
                vals+=list(range(lo,hi+1));ranges+=1;range_candidates+=hi-lo+1
            else:raise ValueError('silently promoted source token kind')
        require(vals==s['candidate_item_IDs_in_source_order'], 'source candidate integer ordering')
        require(len(vals)==len(set(vals)), 'duplicate in one source')
        require(len(vals)==s['source_direct_single_ID_count']+s['source_range_assumption_candidate_occurrences'], 'source appearance partition')
        occurrence_count+=len(vals);all_ids.update(vals)
    require((singles,ranges,range_candidates,occurrence_count)==(6,32,256,262), 'explicit vs hypothesis totals')
    require(len(all_ids)==123 and all_ids=={x['original_item_id'] for x in items}, 'all original item IDs')
    require(t['source_ItemList_direct_explicit_ID_occurrences']==singles, 'total explicit')
    require(t['source_ItemList_range_token_count']==ranges, 'total source ranges')
    require(t['source_ItemList_range_inclusive_interpretation_occurrences_not_proven_to_be_runtime_stock']==range_candidates, 'total range candidates')
    require(t['sum_source_direct_plus_hypothesized_occurrences_not_native_sale_count']==occurrence_count, 'total appearances')
    require(t['unique_original_item_IDs_across_both_floors']==123, 'total unique')
    for a in pairs:
        s1=byfloor.get((1009,a['location_y']));s2=byfloor.get((4009,a['location_y']))
        require(bool(s1 and s2), 'five matches')
        require(a['floor1009_argpath']==s1['original_arg_path'] and a['floor4009_argpath']==s2['original_arg_path'], 'argument pairs')
        require(s1['original_ItemList_raw_text']==s2['original_ItemList_raw_text'], 'same source syntax not stock execution')
        require(s1['original_arg_SHA256']!=s2['original_arg_SHA256'], 'different source bytes even if same lists')
        require(s1['graphicname_original_raw']==s2['graphicname_original_raw'], 'same raw graphic field')
        require(a['same_original_native_runtime_stock_proven'] is False and a['same_original_NPC_identity_or_visual_proven'] is False, 'negative pair boundaries')
    image_by_alias={v['image_number_alias_from_itemset']:v for v in images}
    require(len(image_by_alias)==49, '49 source image aliases')
    status_id=Counter();status_alias=Counter()
    for x in items:
        require(HEX.fullmatch(x['both_original_94field_rows_identical_SHA256']), 'full original item-row hash')
        require(x['original_native_item_effect_and_availability_proven'] is False, 'no runtime effect')
        a=x['original_itemset_graphic_alias'];require(a in image_by_alias, 'item to image alias')
        st=image_by_alias[a]['TW1_retail_source_status'];require(st==x['source_image_status_in_TW1_separate_retail_carrier'],'source status consistent')
        require('original_itemset_type_column19_literal' in x,'source item type kept literal')
        status_id[st]+=1
    for x in images:
        s=x['TW1_retail_source_status'];status_alias[s]+=1
        if s=='VERIFIED_ORIGINAL_RD_INDEXED_PIXELS':
            for k in ('original_ADRN_record_SHA256','original_RD_SHA256','original_indexed_pixel_SHA256','candidate_RGBA_SHA256','private_original_PNG_SHA256'):
                require(HEX.fullmatch(x[k]), 'actual source digit '+k)
            require(x['new_original_RD_decode_this_batch'] is False, 'no invented new bitmap extraction')
            require(x['PNG_width']>0 and x['PNG_height']>0, 'PNG size')
        else:
            require(s in ('DECODING_FAILED','NOT_IN_RETAIL_INDEX'), 'source gap type')
            require('private_original_PNG_SHA256' not in x,'no PNG from missing original')
    require(status_id=={'VERIFIED_ORIGINAL_RD_INDEXED_PIXELS':117,'DECODING_FAILED':4,'NOT_IN_RETAIL_INDEX':2}, 'source bound 117+6 items')
    require(status_alias=={'VERIFIED_ORIGINAL_RD_INDEXED_PIXELS':45,'DECODING_FAILED':2,'NOT_IN_RETAIL_INDEX':2}, 'source bound 45+4 aliases')
    require(t['unique_aliases_with_existing_source_verified_TW1_original_RD_pixels']==45, 'unique verified original candidate pixels')
    require(t['unique_original_item_IDs_TW1_retail_verified_existing_RD_PNG_candidate']==117, 'verified image-linked source IDs')
    require(t['unique_original_item_IDs_TW1_decode_failed']==4 and t['unique_original_item_IDs_TW1_index_missing']==2, 'six original visual gaps')
    b=d['negative_evidence'];require(b['original_native_market_execution'] is False and b['original_shop_purchase_and_selling_executed'] is False,'no native execution')
    require(b['original_runtime_itemlist_range_semantics'] is None and b['same_official_deployment_of_itemset_and_TW1_retail'] is False, 'source/version limits')
    require(b['TW1_retail_source_original_RD_decode_new_this_batch']==0, 'no actual new RD')
    require(d['private_delivery_receipt']['unique_saved_original_pngs_in_private_package']==45,'private archived pixels')
    require(HEX.fullmatch(d['private_delivery_receipt']['sha256']),'private package sha')
    return True


class Original1009And4009Source(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(SOURCE.read_text(encoding='utf-8'))

    def test_actual_source_derived_contract(self):
        self.assertTrue(audit(self.d))

    def test_original_item_range_not_equal_direct_stock(self):
        self.assertEqual(sum(s['source_direct_single_ID_count'] for s in self.d['shops']),6)
        self.assertEqual(sum(s['source_range_assumption_candidate_occurrences'] for s in self.d['shops']),256)

    def test_two_different_original_arg_files_for_same_five_lists(self):
        self.assertEqual(len(self.d['paired_stalls']),5)

    def test_six_missing_TW1_original_item_pixels_preserved(self):
        rows=[(r['original_item_id'],r['original_itemset_graphic_alias']) for r in self.d['items'] if r['source_image_status_in_TW1_separate_retail_carrier']!='VERIFIED_ORIGINAL_RD_INDEXED_PIXELS']
        self.assertEqual(rows,[(2612,24298),(2613,24316),(12042,24137),(12043,24137),(12044,24138),(12045,24138)])

    def test_cannot_silently_infer_native_stock(self):
        d=copy.deepcopy(self.d);d['negative_evidence']['original_runtime_itemlist_range_semantics']=True
        with self.assertRaises(ValueError):audit(d)

    def test_cannot_silently_assert_official_same_deployment(self):
        d=copy.deepcopy(self.d);d['negative_evidence']['same_official_deployment_of_itemset_and_TW1_retail']=True
        with self.assertRaises(ValueError):audit(d)

    def test_reject_changed_original_create_span(self):
        d=copy.deepcopy(self.d);d['creates'][0]['original_CREATE_block_SHA256']='0'*64
        with self.assertRaises(ValueError):audit(d)

    def test_reject_range_off_by_one(self):
        d=copy.deepcopy(self.d); x=next(s for s in d['shops'] if s['source_range_token_count']);x['candidate_item_IDs_in_source_order'].pop()
        with self.assertRaises(ValueError):audit(d)

    def test_reject_false_direct_token(self):
        d=copy.deepcopy(self.d);x=next(s for s in d['shops'] if s['source_range_token_count']);x['original_token_evidence'][0]['evidence']='EXPLICIT_SINGLE_ID_IN_ORIGINAL_TEXT'
        with self.assertRaises(ValueError):audit(d)

    def test_reject_dropped_candidate_item_id(self):
        d=copy.deepcopy(self.d);d['items'].pop()
        with self.assertRaises(ValueError):audit(d)

    def test_reject_faked_png_sha_on_missing_original(self):
        d=copy.deepcopy(self.d);x=next(x for x in d['images'] if x['TW1_retail_source_status']!='VERIFIED_ORIGINAL_RD_INDEXED_PIXELS');x['private_original_PNG_SHA256']='0'*64
        with self.assertRaises(ValueError):audit(d)

    def test_reject_fake_new_RD_decode_count(self):
        d=copy.deepcopy(self.d);d['negative_evidence']['TW1_retail_source_original_RD_decode_new_this_batch']=1
        with self.assertRaises(ValueError):audit(d)

    def test_reject_changed_private_package_hash(self):
        d=copy.deepcopy(self.d);d['private_delivery_receipt']['sha256']='not-a-hash'
        with self.assertRaises(ValueError):audit(d)


if __name__=='__main__':
    unittest.main()
