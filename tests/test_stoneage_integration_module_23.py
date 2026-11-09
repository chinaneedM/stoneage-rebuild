"""INTEGRATION23: public source-only replay; proprietary originals remain private."""
import copy,hashlib,json,re,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]/'research'/'recovered'
NAME='STONEAGE-INTEGRATION23-THREE-VILLAGE-ELEVEN-SHOPS-SOURCE-R1.json'
SHOP='STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-224-SOURCE-ITEMLISTS-191-CREATE-REFERENCES-R1.json'
MAP='STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json'
I17='STONEAGE-INTEGRATION17-THREE-PET-ROOMS-SOURCE-R1.json'
PINS={SHOP:'3bde3b7df43725f28cdac355823667a0ba87e9b1',MAP:'137580e7c25aadf3d679b6ebfb5080b79912cc4f',I17:'e716f01bbf7d08be2e13654909282a198f5334dd'}
FLOORS=(1001,1002,1301,1302,1401,1402)
ORD={1001:[1,2],1002:[3],1301:[51,52],1302:[53,107],1401:[68,69],1402:[70,108]}
DIFF={1001:4,1002:30,1301:0,1302:0,1401:34,1402:1}
LS={1001:'9271eeb71b6d894e47cc5e67e62fcbad648d7fec73ecb50d6fc271cc299cfbdc',1002:'5fe2ffa114a182e2e3503fc853aca1318d9941751ce815044bdfe7d5e6847a2b',1301:'6e9fda66f6e729824cff722820689ed12242d7866a28af89fb348ca781ff6b90',1302:'ed92bc47e61f96796a7f885c69394dc61f585f1ada33fd37eccd72c0f7c9a8c1',1401:'c493132235a8f294424a0999b5c3a3cfc333f7c5afae78955cd647247b029832',1402:'ed22f51b99eb48e7e8f5a45725330596907dd1964a61dfdc4a66ed595fd12aee'}
LIMIT2421='4de61929a1a45a7449f8f96f26f96c57b60bfd47a983c96a447726d6a0d6207d'
def load():
 d={}
 for f,sha in PINS.items():
  raw=(R/f).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==sha, f
  d[f]=json.loads(raw)
 return json.loads((R/NAME).read_bytes()),d[SHOP],d[MAP]
def rooms(q,shop,maps):
 assert q['schema']=='stoneage.integration23.three_village_eleven_original_shop_CONFIGs_source.r1'
 assert q['source_only_shop_total']==11
 assert q['parent_source_sha256']['RAR']==shop['source_original_mixed25_community_RAR_SHA256']
 assert q['original_shop_create_file_sha256']=='d540e9a1354a0f82839cd30ab315a6dee4a3b0299744a0f63ae5ee461c5b587b'
 assert q['original_mapwarp_sha256']=='b7b50f42efa8e5a3f740d49a8d0c01cbf994d1bb66151b16ff5b5e7c14e7595c'
 assert [r['floor'] for r in q['six_rooms']]==list(FLOORS)
 by={x['path']:x for x in shop['shop_argument_rows']};assert len(by)==len(shop['shop_argument_rows'])
 roles=[];items=[];literal=range_tokens=0
 for r in q['six_rooms']:
  floor=r['floor'];orig=maps['maps'][str(floor)]
  assert r['original_DAT_sha256']==orig['source_sha256']
  assert r['original_LS2MAP_sha256']==LS[floor]
  assert r['original_DAT_map_geometry']==orig['geometry']==[30,30]
  assert r['verified_TW1_tile_candidate_placements']==orig['draw_positions']
  assert r['distinct_TW1_tile_candidate_aliases']==orig['unique_draw_aliases']
  assert r['verified_full_combined_RGBA_sha256']==orig['frame_RGBA_sha256']['combined']
  assert r['server_vs_client_layers_changed_cells']==[0,DIFF[floor]]
  assert r['same_source_changed_pairs_only']==(['client_u16_0__server_u16_2'] if DIFF[floor] else [])
  assert [x['original_CREATE_ordinal_within_shop_m'] for x in r['shop_configs']]==ORD[floor]
  for s in r['shop_configs']:
   assert s['source_DAT_three_u16_at_create'][-1]==49152
   old=by[s['original_parameter_path']]
   assert s['original_parameter_sha256']==old['source_sha256']
   assert s['raw_buy_rate']==old['source_buy_rate_text']
   assert s['raw_sell_rate']==old['source_sell_rate_text']
   ids=[x['original_item_id'] for x in s['items']]
   # Old ITEM01 derived catalog sorts some IDs; original private CP950 order is preserved.
   assert sorted(ids)==sorted(old['expanded_candidate_IDs_not_proven_runtime'])
   assert len(ids)==len(old['expanded_candidate_IDs_not_proven_runtime'])
   for x in s['items']:
    for k in ('both_original_itemset_rows_sha256','verified_TW10_candidate_PNG_sha256','verified_TW10_candidate_RGBA_sha256'):
     assert re.fullmatch('[0-9a-f]{64}',x[k])
   items.extend(s['items']);role=s['shop_role_original'];roles.append(role)
   if role=='MATERIAL_SHOP_NAME_ONLY_LIMIT_TYPE_EMPTY':
    assert floor in (1302,1402)
    tokens=s['original_range_expression_tokens'];assert len(tokens)==2
    assert s['original_LimitItemType_literal']==''
    assert s['original_LimitItemNo_literal']==','.join(tokens)
    assert old['range_expressions_literal']==[[int(t.split('-')[0]),int(t.split('-')[1])] for t in tokens]
    assert old['explicit_numeric_item_ID_count']==s['original_ItemList_count']==0
    assert s['range_expansion_candidate_count']==len(ids)==16
    assert all(x['item_id_membership_evidence']=='RANGE_INCLUSIVE_CANDIDATE_NOT_NATIVE_PROVEN' for x in s['items'])
    range_tokens+=len(tokens)
   else:
    assert role in ('OFFENCE','DEFENCE','ACCESSORY')
    assert old['explicit_numeric_item_ID_count']==s['original_ItemList_count']==len(ids)
    assert s['original_LimitItemType_literal']==role
    assert s['range_expansion_candidate_count']==0
    assert not s['original_range_expression_tokens']
    assert all(x['item_id_membership_evidence']=='EXPLICIT_ORIGINAL_ITEMLIST_ID' for x in s['items'])
    literal+=len(ids)
    if (floor,role)==(1302,'ACCESSORY'):
     assert s['original_LimitItemNo_literal']=='2421' and 2421 not in ids
     j=s['separate_original_LimitItemNo_original_itemset_source_join']
     assert j['literal_original_limit_item_ID']==2421 and j['source_two_original_itemset_rows_sha256']==LIMIT2421
     assert j['absent_from_original_explicit_ItemList'] and not j['field_native_purchase_or_limit_semantics_verified']
    else:
     assert s['original_LimitItemNo_literal']==''
     assert s['separate_original_LimitItemNo_original_itemset_source_join'] is None
 assert len(roles)==11
 assert [roles.count(x) for x in ('OFFENCE','DEFENCE','ACCESSORY','MATERIAL_SHOP_NAME_ONLY_LIMIT_TYPE_EMPTY')]==[3,3,3,2]
 m=q['metrics']
 assert literal==m['literal_original_ItemList_explicit_ID_mentions']==109
 assert range_tokens==m['original_ItemList_range_expression_tokens']==4
 assert m['candidate_expanded_IDs_from_four_ranges_not_native_verified']==32
 assert len(items)==m['verified_original_itemset_both_table_rows']==m['selected_item_rows_with_same_sha_in_both_tables']==141
 assert len({x['original_item_id'] for x in items})==m['different_original_item_IDs']==139
 assert len({x['source_image_alias_numeric'] for x in items})==m['source_ready_candidate_item_RD_aliases_distinct']==94
 assert m['source_ready_candidate_original_map_tile_aliases_distinct']==104
 return True

def edges(q):
 e=q['original_directed_warp_rows'];assert len(e)==q['metrics']['original_directed_mapwarp_rows']==26
 pairs={(tuple(x['start']),tuple(x['target'])) for x in e};assert len(pairs)==26
 missing=[]
 for x in e:
  assert re.fullmatch('[0-9a-f]{64}',x['row_sha256_CP950_line'])
  reverse=(tuple(x['target']),tuple(x['start'])) in pairs
  assert x['explicit_reverse_in_selected_mapwarp'] is reverse
  if not reverse:missing.append({'start':x['start'],'target':x['target'],'source_line':x['original_line']})
  for field,point in [('source_original_DAT_three_u16','start'),('target_original_DAT_three_u16','target')]:
   floor=x[point][0];assert floor in FLOORS+(1000,1300,1400)
   if floor in (1000,1300):assert x[field] is None
   else:assert isinstance(x[field],list) and len(x[field])==3 and x[field][-1]==49155
 assert q['metrics']['original_warp_rows_with_explicit_reverse']==24
 assert q['metrics']['original_warp_rows_without_explicit_reverse']==2
 assert missing==q['unpaired_source_directions']
 assert [x['start'] for x in missing]==[[1000,63,98],[1000,67,107]]
 assert [x['target'] for x in missing]==[[1001,10,15],[1002,10,15]]
 for f in ('1000','1300'):
  assert q['exterior_original_DAT_qualifications'][f]['three_u16_values'] is None
  assert q['exterior_original_DAT_qualifications'][f]['status'].startswith('NAMED_IN_WARP_BUT_NO_READABLE')
 assert re.fullmatch('[0-9a-f]{64}',q['exterior_original_DAT_qualifications']['1400']['source_sha256'])
 return True

def bounds(q):
 assert q['initial_main_head']=='06351789fe21e875f25d293c0ae592c43ff028f8'
 assert q['initial_main_tree']=='3fed55a1994804eb406e4b9fedad025bfff6f3de'
 assert q['preserved_historical_current_blob']=='c89e0e33537990aa2132b47c40fef49a985a935c'
 assert q['Stage_A']=='7_PARTIAL_2_OPEN' and q['Stage_B_wiki']=='GATED' and q['R79']=='PAUSED_NON_BLOCKING'
 assert q['overall_percent'] is None
 for k in ('cross_version_same_official_deployment_proven','native_shop_or_warp_transaction_executed','retail_TW1_candidate_bitmap_is_original_mixed25_runtime_selection_proven','source_original_proprietary_bytes_published_to_Git'):
  assert q[k] is False
 assert q['private_OBSERVER']['browser_execution_claimed'] is False
 assert q['private_delivery']['zip_bytes']==5219008 and q['private_delivery']['zip_member_count']==136
 assert q['private_delivery']['zip_sha256']=='7cab6cf75184331c4f09a7525c0081956b21c641a1ec487b0ec93b4e4d49c4b0'
 assert q['private_delivery']['persistent_Library_upload_verified'] and q['private_delivery']['library_roundtrip_whole_zip_SHA256_and_all_136_CRC_verified']
 assert q['source_bound_unreferenced_argument_path']['counted_as_one_of_selected_eleven_original_CREATEs'] is False
 assert q['source_only_limit_item_1302']['runtime_semantics_including_buy_sell_exclusion_unknown']
 return True

class Integration23(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.q,cls.shop,cls.maps=load()
 def test_source_map_eleven_shops_and_item_membership(self):self.assertTrue(rooms(self.q,self.shop,self.maps))
 def test_exact_26_directed_warps(self):self.assertTrue(edges(self.q))
 def test_no_invented_exterior_cell(self):
  q=copy.deepcopy(self.q);next(x for x in q['original_directed_warp_rows'] if x['start'][0]==1000)['source_original_DAT_three_u16']=[0,0,49155]
  with self.assertRaises(AssertionError):edges(q)
 def test_material_ranges_not_explicit_sold_32_items(self):
  q=copy.deepcopy(self.q);s=next(s for r in q['six_rooms'] for s in r['shop_configs'] if s['shop_role_original'].startswith('MATERIAL_'))
  s['original_ItemList_count']=16
  with self.assertRaises(AssertionError):rooms(q,self.shop,self.maps)
 def test_1302_nonlisted_2421_never_inserted(self):
  q=copy.deepcopy(self.q);s=next(s for r in q['six_rooms'] if r['floor']==1302 for s in r['shop_configs'] if s['shop_role_original']=='ACCESSORY')
  s['items'].append(s['items'][-1].copy());s['items'][-1]['original_item_id']=2421
  with self.assertRaises(AssertionError):rooms(q,self.shop,self.maps)
 def test_no_mutated_origin_CREATE(self):
  q=copy.deepcopy(self.q);q['six_rooms'][0]['shop_configs'][0]['original_CREATE_ordinal_within_shop_m']=999
  with self.assertRaises(AssertionError):rooms(q,self.shop,self.maps)
 def test_no_mutated_scene_pixel(self):
  q=copy.deepcopy(self.q);q['six_rooms'][0]['verified_full_combined_RGBA_sha256']='0'*64
  with self.assertRaises(AssertionError):rooms(q,self.shop,self.maps)
 def test_private_artifacts_and_no_native_claim(self):
  self.assertTrue(bounds(self.q));q=copy.deepcopy(self.q);q['native_shop_or_warp_transaction_executed']=True
  with self.assertRaises(AssertionError):bounds(q)
if __name__=='__main__':unittest.main()
