"""Source-bound replay only: no proprietary original scripts, bitmap bytes, or gameplay claims."""
import copy
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'research/recovered/STONEAGE-INTEGRATION103-FOUR-VILLAGE-EXPRESS-CARGO-ORIGINAL-2D-R1.json'
CHAR01 = ROOT / 'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
MAP04 = ROOT / 'research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json'
ITEM01 = ROOT / 'research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def verify(data):
    older = load(CHAR01)
    mp = load(MAP04)
    ids = load(ITEM01)
    prov = data['source_provenance']
    counts = data['source_counts']
    assert prov['older_source_index_CHAR01_git_blob'] == 'a088b61a3212f7049e7793f587123ffb29bebad7'
    assert prov['older_source_index_MAP04_git_blob'] == '1ef8c004179128ea44ffa4fb4259748bc8c83911'
    assert prov['older_public_ITEM01_ID_shard_02_git_blob'] == 'b91bc8335db508998f4595144ce371979ea8c849'
    assert prov['source_CREATE_full_sha256'] == '2fb4ab28ab89452ebe89e8fcc72c2d942c6d6460b24efb8bdb2278317caf7c5e'
    assert prov['source_private_NPC_ZIP_sha256'] == 'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f'
    assert prov['source_ITEM01_private_derived_catalog_zip_sha256'] == 'cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa'
    assert prov['source_TW1_mammoth_prior_INTEG91_ZIP_sha256'] == 'a0bf3d9875a9aee50e35a21c7154c45f2c39fd0d9bf5eed8d4ce3af1b692d878'
    assert prov['source_CREATE_full_bytes'] == 4397
    assert prov['source_CREATE_original_byte_span_SHA_validated'] == 26
    assert prov['distinct_original_handler_bytes_sha_CP950_validated'] == 12
    assert counts['CREATE_blocks'] == 26 and counts['handler_files'] == 12
    assert counts['npcgen_by_type'] == {'npcgen_shop':4,'npcgen_limitshop':4,'npcgen_warpman':8,'npcgen_mugon':10}
    assert counts['original_same_file_numeric_directed_pairings'] == 12
    assert counts['same_SOURCE_static_8_DAT_header_qualified_CREATE_points'] == 26
    assert counts['prior_distinct_original_DAT_SHA_contents'] == 7

    source_files = {r[0]: r for r in older['source_files']}
    source_rows = [r for r in older['create_rows'] if r[0] == 'genout/unsoya_1.create']
    source_rows.sort(key=lambda r: r[1])
    rows = data['CREATE_rows_numeric_and_SHA_only']
    assert len(rows) == len(source_rows) == 26
    assert source_files['genout/unsoya_1.create'][1:3] == [4397,prov['source_CREATE_full_sha256']]
    for a,b in zip(rows,source_rows):
        assert a['ordinal'] == b[1]
        assert a['source_byte_range_exclusive'] == b[2:4]
        assert a['original_CREATE_block_sha256'] == b[4]
        assert a['floor_id'] == b[5]
        assert a['graphicname_numeric_not_proven_identity'] == b[6]
        assert a['borncorner_original_x1_y1_x2_y2'] == b[7]
        assert a['npcgen_template'] == b[11]
        if a['argument_original_path'] is not None:
            assert source_files[a['argument_original_path']][2] == a['argument_source_sha256']
            assert any(a['argument_original_path'] in entry[0] and a['argument_source_sha256'] == entry[2] for entry in b[15])
        else:
            assert a['argument_source_sha256'] is None
    assert Counter(r['npcgen_template'] for r in rows) == counts['npcgen_by_type']
    assert sum(r['graphicname_numeric_not_proven_identity']==100355 for r in rows) == 10

    handlers = data['original_handler_source_param_numeric_only']
    assert len(handlers)==12 and len(set(x['path'] for x in handlers))==12
    assert Counter(x['kind'] for x in handlers)=={'EXPRESSMAN':4,'LIMITSHOP':4,'NEWWARPMAN':4}
    assert sum(x['bytes'] for x in handlers)==prov['handler_total_original_bytes']
    for h in handlers:
        assert h['sha256']==source_files[h['path']][2]
        assert h['bytes']==source_files[h['path']][1]
        if h['kind']=='NEWWARPMAN':
            assert h['original_numbered_TALKEVENT_count']==7
        else:
            assert h['original_numbered_TALKEVENT_count']==0
    assert sorted(x for h in handlers for x in h['original_AddItem_numeric_tokens']) == [2622,2623,2624,2625]
    handler_map = {x['path']:x for x in handlers}

    datmap = {r[0]:dict(zip(mp['per_floor_source_row_columns'],r)) for r in mp['per_floor_source_rows']}
    floors = data['prior_original_DAT_header_source_qualification']
    assert len(floors)==8 and len(set(x['original_DAT_sha256_FROM_PRIOR_MAP04'] for x in floors))==7
    assert sum(x['CONFIG_count'] for x in floors)==26
    for fl in floors:
        r=datmap[fl['original_DAT_filename']]
        assert fl['original_DAT_sha256_FROM_PRIOR_MAP04']==r['source_full_file_SHA256']
        assert fl['original_DAT_bytes_FROM_PRIOR']==r['source_file_bytes']
        assert fl['header_wh']==[r['original_header_width'],r['original_header_height']]
        refs=[x for x in rows if x['floor_id']==fl['floor_id']]
        assert len(refs)==fl['CONFIG_count']==fl['CONFIG_points_in_header']
        assert all(0<=x['borncorner_original_x1_y1_x2_y2'][0]<fl['header_wh'][0] and 0<=x['borncorner_original_x1_y1_x2_y2'][1]<fl['header_wh'][1] for x in refs)

    shard_rows={r[0]:r for r in ids['rows']}
    provenance_items=data['original_itemset_ID_SHAs_from_prior_catalog_and_public_shard']
    assert sorted(x['item_id'] for x in provenance_items)==list(range(2402,2414))
    for item in provenance_items:
        r=shard_rows[item['item_id']]
        assert r[1]==r[2]==item['source_a_original_complete_row_sha256']==item['source_b_original_complete_row_sha256']
        assert r[3]==r[4]==item['original_image_alias_number']==16071
        assert r[5]==item['original_itemset_raw_price_not_actual_courier_fee']
        assert r[6]==item['original_itemset_raw_type']=='16'
        assert r[8]==r[9]=='REAL_RD_DECODED_CROSS_CARRIER'
        assert r[10]==[]

    nodes=data['source_location_floor_labels_derived_private_original_itemset']
    assert set(nodes)=={'薩姆吉爾','瑪麗娜絲','加加','卡魯它那'}
    edges=data['static_source_cargo_item_origin_destination_JOIN_not_runnable_routes']
    assert len(edges)==12 and {x['cargo_item_id'] for x in edges}==set(range(2402,2414))
    assert len({(x['source_origin_name_from_private_itemset_description_short'],x['source_destination_name_from_private_itemset_description_short']) for x in edges})==12
    for edge in edges:
        origin=edge['source_origin_name_from_private_itemset_description_short']
        dest=edge['source_destination_name_from_private_itemset_description_short']
        assert origin in nodes and dest in nodes and origin!=dest
        assert edge['sender_SERVICE_floor']==nodes[origin]['send_floor']
        assert edge['receiver_SERVICE_floor']==nodes[dest]['receive_floor']
        assert edge['same_source_EXPRESSMAN_ItemList_file']==nodes[origin]['send_handler']
        assert edge['same_source_LIMITSHOP_LimitItemNo_file']==nodes[dest]['receive_handler']
        assert edge['cargo_item_id'] in handler_map[edge['same_source_EXPRESSMAN_ItemList_file']]['original_item_list_IDs']
        assert edge['cargo_item_id'] in handler_map[edge['same_source_LIMITSHOP_LimitItemNo_file']]['original_limit_item_IDs']
        assert edge['itemset_original_line_sha256']==shard_rows[edge['cargo_item_id']][1]
        assert edge['visual_alias']==16071
    assert all(sum(x['source_origin_name_from_private_itemset_description_short']==n for x in edges)==3 for n in nodes)
    assert all(sum(x['source_destination_name_from_private_itemset_description_short']==n for x in edges)==3 for n in nodes)
    assert data['original_2D_TW1_cross_carrier_candidate_reused_and_private']['reused_private_color_candidate_png_sha256']=='602c03644de8acbe126d25ea08c60d3179e149ee17228d71c8d335d6e8b641df'
    assert data['original_2D_TW1_cross_carrier_candidate_reused_and_private']['reused_existing_mammoth_first_frame_candidate_png_sha256']=='3aafe8871c60ae0e13589bf21b72508716bc6d8059bf4f3a36932ec56cfbf1a1'
    bounds=data['source_scope_negative']
    for k,v in bounds.items():
        assert v is False or v is None or v == 0, (k,v)
    assert data['baseline']['original_CURRENT_state_sha1']=='c89e0e33537990aa2132b47c40fef49a985a935c'
    assert data['baseline']['original_CURRENT_bytes']==2709173
    assert data['historical_stage']['Stage_A']=='7 PARTIAL + 2 OPEN'
    assert data['historical_stage']['Stage_B']=='GATED'
    assert data['historical_stage']['R79']=='PAUSED_NON_BLOCKING'
    assert 'source_description' not in json.dumps(data,ensure_ascii=False)

class TestIntegration103(unittest.TestCase):
    def test_positive_source_replay(self): verify(load(DATA))
    def test_reject_unsupported_same_deployment(self):
        a=load(DATA);a['source_scope_negative']['early_official_TW1_JSS1999_CN182_same_server_deployment_proven']=True
        with self.assertRaises(AssertionError):verify(a)
    def test_reject_invented_native_delivery(self):
        a=load(DATA);a['source_scope_negative']['historical_actual_delivery_travel_or_purchase_observed']=True
        with self.assertRaises(AssertionError):verify(a)
    def test_reject_modified_cargo_item(self):
        a=load(DATA);a['static_source_cargo_item_origin_destination_JOIN_not_runnable_routes'][0]['cargo_item_id']=99999
        with self.assertRaises(AssertionError):verify(a)
    def test_reject_incorrect_endpoint(self):
        a=load(DATA);a['static_source_cargo_item_origin_destination_JOIN_not_runnable_routes'][0]['receiver_SERVICE_floor']=99999
        with self.assertRaises(AssertionError):verify(a)
    def test_reject_FABRICATED_original_CREATE_byte_hash(self):
        a=load(DATA);a['CREATE_rows_numeric_and_SHA_only'][0]['original_CREATE_block_sha256']='0'*64
        with self.assertRaises(AssertionError):verify(a)
    def test_reject_wrong_item_row_sha(self):
        a=load(DATA);a['original_itemset_ID_SHAs_from_prior_catalog_and_public_shard'][0]['source_a_original_complete_row_sha256']='0'*64
        with self.assertRaises(AssertionError):verify(a)
    def test_reject_new_RD_decode_claim(self):
        a=load(DATA);a['source_scope_negative']['new_original_2D_RD_decoded']=1
        with self.assertRaises(AssertionError):verify(a)
    def test_reject_bogus_MAP04_header_and_sha(self):
        a=load(DATA);a['prior_original_DAT_header_source_qualification'][0]['original_DAT_sha256_FROM_PRIOR_MAP04']='bad'
        with self.assertRaises(AssertionError):verify(a)
    def test_reject_double_count_alias_same_DAT(self):
        a=load(DATA);a['source_counts']['prior_distinct_original_DAT_SHA_contents']=8
        with self.assertRaises(AssertionError):verify(a)

if __name__=='__main__': unittest.main()
