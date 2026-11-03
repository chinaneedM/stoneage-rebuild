"""ITEM01 source-derived archival checks; GitHub CI never executes old game or reads private commercial originals."""
import collections
import copy
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research'/'recovered'
SUMMARY=REC/'STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-TWO-ORIGINAL-ITEMSETS-AND-TW1-RD-SUMMARY-R1.json'
SHOPS=REC/'STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-224-SOURCE-ITEMLISTS-191-CREATE-REFERENCES-R1.json'
SHARDS=[REC/'item-module-01'/f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{i:02d}-R1.json' for i in range(1,8)]
HEX=re.compile(r'^[0-9a-f]{64}$')
RD={'REAL_RD_DECODED_CROSS_CARRIER','TW1_INDEX_NOT_FOUND','TW1_RD_DECODE_FAILED'}
COLS=['item_id','source_a_complete_row_sha256_if_present','source_b_complete_row_sha256','source_a_image_no_if_present','source_b_image_no','source_b_cost_raw','source_b_type_raw','source_b_level_raw','source_a_TW1_RD_qualification_if_present','source_b_TW1_RD_qualification','source_original_94_columns_changed_if_a_present']


def verify(summary,shops,shards):
    assert summary['schema'].endswith('original_two_itemsets_cross_carrier_RD_inventory.r1')
    p=summary['provenance']; a=summary['source_tables']['a']; b=summary['source_tables']['b'];d=summary['cross_table'];rd=summary['original_TW1_retail_RD_pixel_source'];shop=summary['original_shop_source'];bounds=summary['bounds']
    assert HEX.fullmatch(p['mixed25_community_RAR_sha256'])
    assert p['mixed25_RAR_original_members']==7952
    assert p['itemset_a']['source_size_bytes']==3392473 and p['itemset_b']['source_size_bytes']==3668487
    for nm in ('itemset_a','itemset_b'):
        assert HEX.fullmatch(p[nm]['sha256'])
    for nm in ('TW1_retail_original_P3H_sha256','TW1_original_ADRN_sha256','TW1_original_REAL_sha256','TW1_original_Palet1_sha256'):
        assert HEX.fullmatch(p[nm])
    assert p['same_original_official_deployment_of_itemsets_and_retail_art_proven'] is False
    assert p['community_archive_certified_official_clean_build'] is False
    assert a['rows']==13254 and b['rows']==13915
    assert a['original_94_columns_per_line'] and b['original_94_columns_per_line']
    assert a['strict_cp950_roundtrip'] and b['strict_cp950_roundtrip']
    assert (d['source_common_id_count'],d['original_rows_whole_sha_equal'],d['original_rows_whole_sha_different'],d['source_b_only_ids_count'],d['source_a_only_ids_count'])==(13254,4303,8951,661,0)
    assert {int(k):v for k,v in d['raw_changed_zero_based_column_frequency'].items()}=={2:2,3:1,17:8,30:8935,31:8935,57:206}
    assert all(d[f'common_IDs_changed_{col}']==0 for col in ('cost_col18','type_col19','level_col22'))
    assert rd['distinct_image_number_alias_candidates_union']==1667
    assert (rd['ADRN_unique_record_found'],rd['ADRN_not_found'],rd['RD_fully_decoded'],rd['RD_decode_failed'])==(836,831,832,4)
    assert rd['RD_decode_failed_aliases']==[24077,24137,24138,24140]
    assert rd['MAP04_independent_actual_RD_original_SHA_and_indexed_pixel_SHA_matches']==20
    assert rd['png_colors_and_vertical_flip_are_modern_candidate_not_native_certified'] is True
    for k in ('native_client_executed_this_batch','native_server_executed_this_batch','true_original_shop_sale_observed','official_TW1_itemset_source_authenticated','full_historical_all_version_item_population_closed'):
        assert bounds[k] is False,k
    assert bounds['no_original_commercial_table_rows_published_in_public_git'] is True
    assert bounds['no_original_sprite_RD_or_PNG_published_in_public_git'] is True
    assert bounds['overall_percent'] is None and bounds['R79']=='PAUSED_NON_BLOCKING'
    allids=set(); rows=[];counter=collections.Counter();imcounts={'a':collections.Counter(),'b':collections.Counter()};imgs={'a':set(),'b':set()};colchanges=collections.Counter()
    assert len(shards)==7
    for i,sh in enumerate(shards,1):
        assert sh['schema'].endswith('derived_numeric_rows_without_original_text_or_art.r1') and sh['shard']==i
        assert sh['column_labels']==COLS
        assert sh['source_itemset_rows_sha256_provenance']==p['itemset_a']['sha256']
        assert sh['source_itemset0710_rows_sha256_provenance']==p['itemset_b']['sha256']
        assert len(sh['rows'])==(1915 if i==7 else 2000)
        for row in sh['rows']:
            assert len(row)==11 and len(set(row[:1]))==1
            id,oldsha,newsha,oldimg,newimg,price,typev,level,status_old,status_new,changed=row
            assert isinstance(id,int) and id>=0 and id not in allids
            assert HEX.fullmatch(newsha) and isinstance(newimg,int) and isinstance(price,str) and isinstance(typev,str) and isinstance(level,str)
            assert status_new in RD and isinstance(changed,(list,type(None)))
            if oldsha is None:
                assert oldimg is None and status_old is None and changed is None;counter['extra']+=1
            else:
                assert HEX.fullmatch(oldsha) and isinstance(oldimg,int) and status_old in RD and isinstance(changed,list)
                assert bool(changed)==(oldsha!=newsha)
                if 17 in changed:assert oldimg!=newimg
                else:assert oldimg==newimg
                colchanges.update(changed)
                counter['same' if oldsha==newsha else 'changed']+=1
                imcounts['a'][status_old]+=1;imgs['a'].add(oldimg)
            imcounts['b'][status_new]+=1;imgs['b'].add(newimg)
            allids.add(id);rows.append(row)
    assert len(rows)==13915 and allids==set(x[0] for x in rows)
    assert [r[0] for r in rows]==sorted(allids)
    assert counter=={'same':4303,'changed':8951,'extra':661}
    assert colchanges==collections.Counter({2:2,3:1,17:8,30:8935,31:8935,57:206})
    assert len(imgs['a'])==1401 and len(imgs['b'])==1667
    for ver,report in (('a',a),('b',b)):
        expected=report['image_link_evidence_for_item_rows']
        assert imcounts[ver]['REAL_RD_DECODED_CROSS_CARRIER']==expected['VERIFIED_ORIGINAL_RD_INDEXED_PIXELS']
        assert imcounts[ver]['TW1_INDEX_NOT_FOUND']==expected['NOT_IN_RETAIL_INDEX']
        assert imcounts[ver]['TW1_RD_DECODE_FAILED']==expected['DECODING_FAILED']
        assert sum(imcounts[ver].values())==report['rows']
    assert shops['schema'].endswith('original_npcgen_shop_static_source_only.r1')
    assert shops['source_original_mixed25_community_RAR_SHA256']==p['mixed25_community_RAR_sha256']
    assert shops['not_certified_official_client_or_native_shop_runtime'] is True
    assert shops['ranges_parsed_only_as_candidate_inclusive_intervals'] is True
    x=shops['shop_argument_rows'];cre=shops['npcgen_shop_creation_rows'];assert (len(x),len(cre))==(224,191)
    paths={};candidate_ids=set();old_table_ids={r[0] for r in rows if r[1] is not None}
    assert len({c['path'] for c in x})==224
    for c in x:
        assert HEX.fullmatch(c['source_sha256']) and HEX.fullmatch(c['raw_ItemList_expression_sha256'])
        assert isinstance(c['expanded_candidate_IDs_not_proven_runtime'],list)
        assert c['expanded_candidate_IDs_not_proven_runtime']==sorted(set(c['expanded_candidate_IDs_not_proven_runtime']))
        for lo,hi in c['range_expressions_literal']:
            assert 0<=lo<=hi and all(id in c['expanded_candidate_IDs_not_proven_runtime'] for id in range(lo,hi+1))
        candidate_ids.update(c['expanded_candidate_IDs_not_proven_runtime'])
        assert set(c['later_table_only_IDs'])<=set(c['expanded_candidate_IDs_not_proven_runtime'])-old_table_ids
        assert all(id in allids for id in c['expanded_candidate_IDs_not_proven_runtime'])
        paths[c['path']]=c
    assert sum(c['explicit_numeric_item_ID_count'] for c in x)==1588
    assert sum(len(c['range_expressions_literal']) for c in x)==136
    assert len(candidate_ids)==1210 and len(candidate_ids-old_table_ids)==45
    assert sum(len(c['expanded_candidate_IDs_not_proven_runtime'])==0 for c in x)==1
    assert shop['ItemList_files']==224 and shop['ItemList_nonempty_files']==223
    assert shop['actual_npcgen_shop_create_source_refs']==191
    assert shop['referenced_argument_original_files_present']==191
    assert shop['referenced_argument_with_ItemList']==189
    assert shop['distinct_referenced_argument_paths']==186
    assert len({c['argument_path'] for c in cre})==186
    for c in cre:
        assert HEX.fullmatch(c['create_full_sha256']) and HEX.fullmatch(c['argument_sha256'])
        assert c['argument_has_itemlist']==(c['argument_path'] in paths)
        assert isinstance(c['create_path'],str) and c['create_path']
    assert summary['auxiliary_non_itemset_originals']['itematom_source_rows']==83
    assert summary['auxiliary_non_itemset_originals']['bmitem_source_rows']==36
    assert summary['auxiliary_non_itemset_originals']['gambleitems_source_rows']==24
    assert summary['auxiliary_non_itemset_originals']['magic_source_rows']==181
    private=summary['private_observer_custody']
    assert private['bytes']==5868386 and private['zip_members']==838
    assert HEX.fullmatch(private['sha256'])
    assert private['actual_TW1_RD_source_PNG_count']==832 and private['complete_catalog_candidate_B_item_ID_records']==13915
    assert private['uploaded_to_library_and_full_raw_byte_SHA_zip_CRC_roundtrip_verified'] is True
    assert private['actual_native_legacy_client_execution'] is False
    assert private['original_asset_rights_restricted_private'] is True
    assert summary['preserved_historical_current_state_blob_sha']=='c89e0e33537990aa2132b47c40fef49a985a935c'
    assert len(summary['public_derived_ID_shards'])==7
    assert [(z[0],z[1],z[2],z[3]) for z in summary['public_derived_ID_shards']]==[(i,2000 if i!=7 else 1915,shards[i-1]['rows'][0][0],shards[i-1]['rows'][-1][0]) for i in range(1,8)]
    assert all(HEX.fullmatch(x[4]) for x in summary['public_derived_ID_shards'])
    assert summary['next'].startswith('ITEM_EQUIPMENT_SHOP_MODULE_02')
    return True

class Item01Acceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary=json.loads(SUMMARY.read_text());cls.shops=json.loads(SHOPS.read_text());cls.shards=[json.loads(p.read_text()) for p in SHARDS]
    def test_source_derived_full_13915_IDs_and_224_shops(self):self.assertTrue(verify(self.summary,self.shops,self.shards))
    def test_seven_exact_public_shard_blob_sha256(self):
        for path,record in zip(SHARDS,self.summary['public_derived_ID_shards']):
            with open(path,'rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
            self.assertEqual(actual,record[4])
    def test_reject_duplicate_item_id_across_shards(self):
        a=copy.deepcopy(self.shards);a[1]['rows'][0][0]=a[0]['rows'][-1][0]
        with self.assertRaises(AssertionError):verify(self.summary,self.shops,a)
    def test_reject_incorrect_source_row_identity(self):
        a=copy.deepcopy(self.shards);a[0]['rows'][0][2]='bad_sha'
        with self.assertRaises(AssertionError):verify(self.summary,self.shops,a)
    def test_reject_corrupt_graphic_alias_pixel_qualification(self):
        a=copy.deepcopy(self.shards);a[0]['rows'][0][9]='VERIFIED_OFFICIAL_ITEM_RENDERING'
        with self.assertRaises(AssertionError):verify(self.summary,self.shops,a)
    def test_reject_source_range_as_native_shop_execution(self):
        s=copy.deepcopy(self.shops);s['ranges_parsed_only_as_candidate_inclusive_intervals']=False
        with self.assertRaises(AssertionError):verify(self.summary,s,self.shards)
    def test_reject_miscounted_later_only_661_IDs(self):
        v=copy.deepcopy(self.summary);v['cross_table']['source_b_only_ids_count']=660
        with self.assertRaises(AssertionError):verify(v,self.shops,self.shards)
    def test_reject_same_official_deployment_claim(self):
        v=copy.deepcopy(self.summary);v['provenance']['same_original_official_deployment_of_itemsets_and_retail_art_proven']=True
        with self.assertRaises(AssertionError):verify(v,self.shops,self.shards)
    def test_reject_native_shop_sale_claim(self):
        v=copy.deepcopy(self.summary);v['bounds']['true_original_shop_sale_observed']=True
        with self.assertRaises(AssertionError):verify(v,self.shops,self.shards)
    def test_reject_false_private_ZIP_cloud_readback(self):
        v=copy.deepcopy(self.summary);v['private_observer_custody']['uploaded_to_library_and_full_raw_byte_SHA_zip_CRC_roundtrip_verified']=False
        with self.assertRaises(AssertionError):verify(v,self.shops,self.shards)
    def test_reject_4_unresolved_RD_decode_failures_as_success(self):
        v=copy.deepcopy(self.summary);v['original_TW1_retail_RD_pixel_source']['RD_decode_failed']=0
        with self.assertRaises(AssertionError):verify(v,self.shops,self.shards)
    def test_reject_missing_original_shop_argument_link(self):
        s=copy.deepcopy(self.shops);s['npcgen_shop_creation_rows'][0]['argument_sha256']='0'
        with self.assertRaises(AssertionError):verify(self.summary,s,self.shards)

if __name__=='__main__':unittest.main()
