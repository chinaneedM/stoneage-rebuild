"""Offline validation of permanent three-name source projection, not server execution."""
import argparse
import hashlib
import json
from pathlib import Path
from tools.stoneage_preserved_pet_template_r39 import EXPECTED, PREFIX, NAMES, need
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'research/recovered/STONEAGE-PRESERVED-PET-TEMPLATE-SOURCE-R39.json'

def validate(report):
 need(report['schema']=='stoneage.preserved_pet_template_source.r39','schema')
 need(report['status']=='ORIGINAL_CONFIG_AND_TEMPLATE_SHA_CRC_MATCH','actual source acquired')
 need(report['source_scope']=='COMMUNITY_MIXED25_SAME_ARCHIVE_SERVER_SUBTREE_NOT_AUTHENTICATED_OFFICIAL_OR_SAME_DEPLOYED_BUILD','bounded source scope')
 for k in ('original_payload_published','original_program_executed'):need(report[k] is False,k)
 need(report['new_official_clients']==0,'no official authentication')
 receipt=report['receipt'];need(receipt['whole_package_rehashed'] is False,'whole archive not rehashed')
 need(0<receipt['headers_visited']<=10000,'finite header walk')
 ranges=receipt['range_receipts'];need(len(ranges)==receipt['range_requests']<=256,'range request budget')
 need(sum(r['bytes'] for r in ranges)==receipt['actual_range_bytes']<=16*1024*1024,'source byte budget')
 seen=set()
 for r in ranges:
  need(r['part'] in (1,2) and r['end']-r['start']+1==r['bytes'] and r['start']>=0,'exact source ranges')
  need((r['part'],r['start']) not in seen,'no duplicate cache receipt');seen.add((r['part'],r['start']))
  need(len(r['sha256'])==64,'range digest')
 members=receipt['members'];need(len(members)==2,'two source files')
 for path,(size,digest) in EXPECTED.items():
  found=[m for m in members if m['name']==PREFIX+path];need(len(found)==1,'unique member')
  m=found[0];need((m['bytes'],m['sha256'])==(size,digest),'old original whole file identity')
  need(m['flags']&(1|2|4|16)==0 and m['extractor_returncode']==0,'independent static extraction')
  need(m['compressed_bytes']<=1024*1024 and m['data_offset']>m['header_offset'],'bounded original header')
 material=report['material']
 need(material['configured_enemybase_path']=='./data/enemybase.txt','original configured table')
 need(material['all_template_rows']==988 and material['field_count_distribution']=={'56':988},'old full table extents')
 need(material['distinct_name_tokens']==662 and len(material['cp950_big5_different_names'])==2,'old independent encoding audit')
 need(material['selected_name_queries']==list(NAMES),'three fixed queries')
 for k in ('original_server_executed','same_client_server_build_proven','client_sprite_binding_proven','official_species_master_authenticated'):
  need(material[k] is False,k)
 need(material['numeric_semantics']=='COLUMN_7_TEMPNO_COLUMN_37_IMGNUMBER_COLUMN_38_PETFLG_FROM_PREEXISTING_DESCENDANT_PREFIX_NOT_NATIVE_BUILD_PROOF','field semantics boundary')
 selected=material['selected_rows'];need(0<len(selected)<=48,'finite nonempty actual material')
 need(len({r['line'] for r in selected})==len(selected),'original row positions retained')
 for row in selected:
  need(row['name'] in NAMES and row['byte_offset']>=0 and row['line']>0,'selected original occurrence')
  for key in ('template_number_column_7','graphic_field_column_37','pet_flag_column_38'):need(type(row[key]) is int,'strict numeric facts')
  need(row['name_token_sha256']==hashlib.sha256(row['name'].encode('cp950')).hexdigest(),'selected exact original name bytes')
  need(len(row['row_sha256'])==64,'row fingerprint')
 need(material['unmatched_name_queries']==[n for n in NAMES if not any(r['name']==n for r in selected)],'all query outcomes preserved')
 return material

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,default=SOURCE);args=parser.parse_args()
 raw=args.source.read_bytes()
 need(hashlib.sha256(raw).hexdigest()=='09dc73e801f5020059812acb71b1db6d41e8987a3730ee2126348ee349a24d3b','exact original archived report bytes')
 material=validate(json.loads(raw))
 print(json.dumps({'status':'PASS','rows':material['all_template_rows'],'selected_occurrences':len(material['selected_rows']),
 'official_species_master_authenticated':False,'same_client_server_build_proven':False},ensure_ascii=False))
if __name__=='__main__':main()
