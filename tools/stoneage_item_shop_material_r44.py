"""Offline integrity and evidence-boundary replay of finite R44 source metadata."""
import argparse
import hashlib
import json
from pathlib import Path
from tools.stoneage_preserved_item_shop_r44 import EXPECTED, PREFIX, SCOPE, NUMBER_FIELDS, need

ROOT=Path(__file__).resolve().parents[1]
REPORT='research/recovered/STONEAGE-PRESERVED-ITEM-SHOP-SOURCE-R44.json'
REPORT_SHA='1d825c30192b088f0b1f14aba1b2a306644b618be5a6d60bf5fa2e78595dab0e'


def replay(d):
 need(set(d)=={'schema','source_scope','status','official_tw10_items_authenticated','original_server_executed',
              'original_payload_or_dialogue_published','receipt','material'},'unexpected report payload/schema')
 need(d['schema']=='stoneage.preserved_item_shop_source.r44' and d['source_scope']==SCOPE,'source scope')
 need(d['status']=='THREE_ORIGINAL_MEMBERS_SHA_CRC_AND_FINITE_NAMED_INVENTORY_QUALIFIED','source not acquired/qualified')
 need(type(d['official_tw10_items_authenticated']) is int and d['official_tw10_items_authenticated']==0 and
      d['original_server_executed'] is False and d['original_payload_or_dialogue_published'] is False,'evidence promotion')
 receipt=d['receipt'];members=receipt['members']
 need(len(members)==3 and {m['path'] for m in members}=={PREFIX+p for p in EXPECTED},'original source coverage')
 for m in members:
  key=m['path'][len(PREFIX):]
  need((m['bytes'],m['sha256'])==EXPECTED[key],'original source SHA/extent')
  need(m['flags']&(1|2|4|16)==0,'dependent/encrypted source')
  need(0<=m['header_offset']<m['data_offset']<m['data_offset']+m['compressed_bytes']<=361255180,'original archive extent')
  need(0<=m['crc32']<2**32,'original CRC extent')
 ranges=receipt['range_receipts'];need(len(ranges)==receipt['range_requests']<=256,'source range count')
 need(sum(r['bytes'] for r in ranges)==receipt['actual_range_bytes']<=16*1024*1024,'source range budget')
 need(len({(r['part'],r['start']) for r in ranges})==len(ranges),'duplicate source range accounting')
 for r in ranges:need(r['bytes']==r['end']-r['start']+1 and r['part'] in (1,2),'source range extent')
 need(receipt['whole_archive_or_parts_rehashed'] is False,'whole archive rehash claim')
 m=d['material'];need(set(m)=={'configured_itemset_keys','arg_keys_in_source_order','arg_value_fingerprints','inventory_tokens','inventory','rate_fields','original_item_rows','original_unique_template_ids','selected_rule','selected_items','numeric_field_semantics','computed_runtime_prices','source_arg_is_authenticated_original_shop_execution'},'unexpected material payload')
 need((m['original_item_rows'],m['original_unique_template_ids'])==(13252,13252),'full original table count')
 need(m['configured_itemset_keys']=={k:'data/itemset.txt' for k in ('itemset3file','itemset4file','itemset5file','itemset6file')},'configured original table')
 need(len(m['arg_keys_in_source_order'])==len(set(m['arg_keys_in_source_order'])) and
      set(m['arg_keys_in_source_order'])==set(m['arg_value_fingerprints']),'ARG field occurrence coverage')
 tokens=m['inventory_tokens'];need(0<len(tokens)<=100,'inventory token bounds')
 for lo,hi in tokens:need(0<=lo<=hi<=1000000,'inventory range qualification')
 inventory=m['inventory'];occ=inventory['listed_defined_occurrences']
 need(inventory['limit']==33 and inventory['undefined_ids_are_skipped'] is True and
      inventory['model_is_original_runtime'] is False,'descendant inventory model scope')
 need(inventory['descendant_model_visible_occurrences']==occ[:33] and
      inventory['descendant_model_truncated_occurrences']==occ[33:],'model cap/occurrence conservation')
 for x in occ:
  need(0<=x['token_index']<len(tokens),'stock token source')
  lo,hi=tokens[x['token_index']];need(lo<=x['item_id']<=hi,'stock ID outside source token')
 need(occ==sorted(occ,key=lambda x:(x['token_index'],x['item_id'])) and
      len({(x['token_index'],x['item_id']) for x in occ})==len(occ),'ordered within-token occurrences')
 need(m['selected_rule']=='FIRST_SIX_DEFINED_VISIBLE_OCCURRENCES_BEFORE_NAME_DECODING','name selection bias')
 selected=m['selected_items'];need(len(selected)==min(6,len(occ)) and len(selected)>0,'finite selected sample')
 for rank,row in enumerate(selected,1):
  need(row['model_visible_rank']==rank and
       (row['token_index'],row['item_id'])==(occ[rank-1]['token_index'],occ[rank-1]['item_id']),'selected occurrence mismatch')
  need(set(row)=={'model_visible_rank','token_index','item_id','physical_line','byte_offset','row_sha256','names','numeric_fields'},'unexpected selected raw payload')
  need(row['physical_line']>0 and 0<=row['byte_offset']<3392473,'original selected row location')
  need(set(row['names'])=={'name','secretname'},'selected name fields')
  for name in row['names'].values():
   text=name['text_cp950_big5'];need(0<len(text)<=48,'bounded item name')
   raw=text.encode('cp950');need(raw.decode('big5')==text,'selected name encoding mismatch')
   need(hashlib.sha256(raw).hexdigest()==name['bytes_sha256'],'selected original name fingerprint')
  values=row['numeric_fields'];need(set(values)==set(NUMBER_FIELDS),'numeric field set')
  need(all(v is None or type(v) is int for v in values.values()) and values['id']==row['item_id'],'numeric ID/field mismatch')
 need(m['numeric_field_semantics']=='EXISTING_DESCENDANT94_COLUMN_SCHEMA_NOT_ORIGINAL_BINARY_LOADER_PROOF','numeric schema scope')
 need(set(m['rate_fields'])=={'buy_rate','sell_rate'},'rate field coverage')
 for key,rate in m['rate_fields'].items():
  if rate['present']:
   raw=rate['raw_decimal'].encode('ascii');need(key in m['arg_value_fingerprints'] and m['arg_value_fingerprints'][key]=={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},'original rate fingerprint')
  else:need(rate['raw_decimal'] is None and key not in m['arg_value_fingerprints'],'absent rate was invented')
 need(m['computed_runtime_prices'] is None and m['source_arg_is_authenticated_original_shop_execution'] is False,'runtime execution or price promotion')
 return {'source_members':3,'original_item_rows':13252,'named_occurrences':len(selected),
         'listed_defined_occurrences':len(occ),'visible_model_occurrences':min(33,len(occ)),
         'official_tw10_items_authenticated':0}


def verify_custody():
 custody=json.loads((ROOT/'research/recovered/STONEAGE-PRESERVED-ITEM-SHOP-CUSTODY-R44.json').read_text())
 def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
 for attempt in custody['source_attempts']:
  saved=attempt['raw_report'];raw=(ROOT/saved['path']).read_bytes()
  need(pin(raw)=={k:saved[k] for k in ('bytes','sha256','git_blob')},'custody original JSON identity')
 for path,expected in custody['source_extractor_and_schema_pins'].items():
  need(pin((ROOT/path).read_bytes())==expected,'source-tested extractor/schema drift')
 need(custody['source_attempts'][0]['material_status']=='NOT_ACQUIRED' and
      custody['source_attempts'][1]['material_status']=='THREE_ORIGINAL_MEMBERS_SHA_CRC_AND_FINITE_NAMED_INVENTORY_QUALIFIED','failure was rewritten')
 return True


def main():
 parser=argparse.ArgumentParser();parser.parse_args()
 verify_custody()
 raw=(ROOT/REPORT).read_bytes();need(hashlib.sha256(raw).hexdigest()==REPORT_SHA,'exact archived source report SHA')
 print(json.dumps(replay(json.loads(raw)),ensure_ascii=False))

if __name__=='__main__':main()
