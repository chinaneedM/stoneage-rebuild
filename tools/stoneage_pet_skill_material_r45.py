"""Offline integrity replay of six source-qualified original pet-skill records."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from tools.stoneage_preserved_pet_skill_r45 import EXPECTED,PREFIX,SCOPE,INT_NAMES,SELECTION,skill_config,need

ROOT=Path(__file__).resolve().parents[1]
REPORT='research/recovered/STONEAGE-PRESERVED-PET-SKILL-SOURCE-R45.json'
REPORT_SHA='8cb12a7f5dd4ec0ffd39a9112446f82b1583f8cbeb8ced75b8c87c9d7421e914'
CUSTODY='research/recovered/STONEAGE-PRESERVED-PET-SKILL-CUSTODY-R45.json'
CROSSWALK='research/recovered/STONEAGE-PET-SKILL-NAME-MODEL-CROSSWALK-R45.json'
PRIOR_PINS={
 'research/recovered/STONEAGE-25-PETSKILL-PRESSURE-R1.txt':'2e1d9b57ef9d88696ae0e0db7ad5120ecca3d48fc01d0ccc5f77281cfd448994',
 'tools/stoneage_recovered25_petskill_runtime.py':'3816d984de08b3bae1a4b8a4880ede71e29ab786064e62f9fb3245cf081c63dc'}


def pin(raw):
 return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
         'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}


def replay(d):
 need(set(d)=={'schema','source_scope','status','official_tw10_skills_authenticated',
  'original_server_executed','raw_table_comment_option_or_script_published','receipt','material'},'unexpected report/raw payload')
 need(d['schema']=='stoneage.preserved_pet_skill_source.r45' and d['source_scope']==SCOPE,'source scope')
 need(d['status']=='TWO_ORIGINAL_MEMBERS_DUAL_DECODE_SHA_CRC_AND_SIX_NAMES_QUALIFIED','actual source not qualified')
 need(type(d['official_tw10_skills_authenticated']) is int and d['official_tw10_skills_authenticated']==0 and
      d['original_server_executed'] is False and d['raw_table_comment_option_or_script_published'] is False,'evidence promotion')
 receipt=d['receipt'];members=receipt['members']
 need(len(members)==2 and {m['path'] for m in members}=={PREFIX+p for p in EXPECTED},'both original source members')
 for m in members:
  need((m['bytes'],m['sha256'])==EXPECTED[m['path'][len(PREFIX):]],'complete original member identity')
  need(m['flags']&(1|2|4|16)==0 and 0<=m['header_offset']<m['data_offset']<m['data_offset']+m['compressed_bytes']<=361255180,'independent original archive extent')
  need(m['unar_return_code']==0 and m['independent_decoded_bytes_equal'] is True and
       type(m['libarchive_version_number']) is int and m['libarchive_version_number']>0,'actual independent decoding')
 ranges=receipt['range_receipts']
 need(len(ranges)==receipt['range_requests']<=256 and sum(r['bytes'] for r in ranges)==receipt['actual_range_bytes']<=16*1024*1024,'source range budget')
 need(len({(r['part'],r['start']) for r in ranges})==len(ranges),'duplicate range accounting')
 for r in ranges:
  need(r['part'] in (1,2) and r['end']-r['start']+1==r['bytes'],'original HTTP range extent')
 need(receipt['whole_archive_or_parts_rehashed'] is False and
      receipt['same_http_bytes_two_decompressors_not_two_network_acquisitions'] is True,'source acquisition promotion')
 m=d['material']
 need(set(m)=={'configured_skill_paths_as_written','normalized_configured_skill_path','all_original_rows',
  'all_unique_skill_ids','field_count_distribution','raw_name_token_count','callback_token_count',
  'trailing_field_equals_callback_rows','integer_column_counts','selected_rule','selected_rows','column_semantics',
  'cost_is_mp_or_training_price_proven','original_callback_execution_proven',
  'original_learning_npc_or_species_eligibility_proven'},'unexpected material/raw payload')
 config=m['configured_skill_paths_as_written'];raw=b'\n'.join(k.encode()+b'='+v.encode() for k,v in config.items())
 need(skill_config(raw)==config and m['normalized_configured_skill_path']=='data/petskill.txt','configured table alternatives')
 need((m['all_original_rows'],m['all_unique_skill_ids'],m['raw_name_token_count'],m['callback_token_count'])==(147,147,146,69),'preexisting full-table extent')
 need(m['field_count_distribution']=={'12':147} and m['trailing_field_equals_callback_rows']==4,'twelve-column/trailing preservation boundary')
 need(set(m['integer_column_counts'])=={'FIELD','TARGET','COST','ILLEGAL'},'integer column namespace')
 for counts in m['integer_column_counts'].values():
  need(sum(counts.values())==147 and all(re.fullmatch(r'-?\d+',k) and type(v) is int and v>0 for k,v in counts.items()),'full integer column counts')
 need(m['selected_rule']==SELECTION and len(m['selected_rows'])==6,'finite preselected six rows')
 seen=set();positions=[]
 for i,row in enumerate(m['selected_rows']):
  need(set(row)=={'source_order','physical_line','byte_offset','row_sha256','name','callback','numeric_fields','non_name_text_fingerprints'},'unexpected selected payload')
  need(row['source_order']==i and row['physical_line']>0 and 0<=row['byte_offset']<15112,'selected original occurrence')
  positions.append((row['physical_line'],row['byte_offset']))
  need(re.fullmatch('[a-f0-9]{64}',row['row_sha256']) is not None,'whole original row digest')
  name=row['name'];text=name['text_cp950_big5'];need(0<len(text)<=48,'bounded original display name')
  encoded=text.encode('cp950');need(encoded.decode('big5')==text and name['token']=={'bytes':len(encoded),'sha256':hashlib.sha256(encoded).hexdigest()},'original display-name fingerprint')
  values=row['numeric_fields'];need(set(values)==set(INT_NAMES) and all(type(v) is int for v in values.values()),'six-string integer-prefix schema')
  need(0<=values['ID']<=1000000 and values['ID'] not in seen,'skill identity including zero');seen.add(values['ID'])
  need(re.fullmatch('[A-Za-z_][A-Za-z_0-9]*',row['callback']) is not None,'original callback declaration')
  fingerprints=row['non_name_text_fingerprints'];need(set(fingerprints)=={'comment','option','free','kindcode','trailing_preserved_column'},'original text-field coverage')
  for fp in fingerprints.values():need(set(fp)=={'bytes','sha256'} and type(fp['bytes']) is int and fp['bytes']>=0 and re.fullmatch('[a-f0-9]{64}',fp['sha256']) is not None,'original text fingerprint extent')
 need(positions==sorted(positions) and len(set(positions))==6,'original row order or duplicates')
 need(m['column_semantics']=='DESCENDANT_CFREE6_PREFIX_NOT_THIS_BINARY_LOADER_PROOF','native schema promotion')
 for flag in ('cost_is_mp_or_training_price_proven','original_callback_execution_proven','original_learning_npc_or_species_eligibility_proven'):
  need(m[flag] is False,'gameplay rule/eligibility promotion')
 return {'original_rows':147,'named_occurrences':6,'selected_ids':[r['numeric_fields']['ID'] for r in m['selected_rows']],
         'official_tw10_skills_authenticated':0,'two_decompressors_equal':True}


def parse_prior_pressure(raw):
 by_id={}
 for number,line in enumerate(raw.decode('utf-8').splitlines(),1):
  if not line.startswith('RANK|'):continue
  fields=dict(token.split('=',1) for token in line.split('|')[1:])
  ids=[int(v) for v in fields['ids'].split(',')]
  for skill_id in ids:
   need(skill_id>0 and skill_id not in by_id,'ambiguous/non-positive prior enemy skill reference')
   by_id[skill_id]={'prior_report_line':number,'line_sha256':hashlib.sha256(line.encode()).hexdigest(),
    'declared_callback':fields['callback'],'family_skill_ids':ids,
    'callback_family_positive_slot_uses':int(fields['slot_uses']),
    'prior_model_status':fields['status']}
 return by_id


def decimal_option_witness(fp):
 # A finite exact one-byte preimage witness, not a general OPTION interpreter.
 if fp=={'bytes':0,'sha256':hashlib.sha256(b'').hexdigest()}:
  return {'kind':'EMPTY_ORIGINAL_OPTION','integer':None}
 if fp['bytes']==1:
  matches=[n for n in range(10) if hashlib.sha256(str(n).encode()).hexdigest()==fp['sha256']]
  if len(matches)==1:return {'kind':'EXACT_ONE_BYTE_DECIMAL_LENGTH_AND_SHA_WITNESS','integer':matches[0]}
 return {'kind':'NOT_DECODED','integer':None}


def model_crosswalk(source_rows,prior,stable):
 result=[]
 for row in source_rows:
  skill_id=row['numeric_fields']['ID'];callback=row['callback'];old=prior.get(skill_id)
  if old is not None:need(old['declared_callback']==callback,'prior/source skill ID-to-callback conflict')
  result.append({'source_order':row['source_order'],'source_row_sha256':row['row_sha256'],
   'original_display_name':row['name']['text_cp950_big5'],'original_skill_id':skill_id,
   'original_declared_callback':callback,'stable_common_reference_model_available':callback in stable,
   'option_decimal_witness':decimal_option_witness(row['non_name_text_fingerprints']['option']),
   'prior_positive_enemy_reference':old,'original_execution_or_learning_eligibility_inferred':False})
 return result


def build_crosswalk():
 from tools.stoneage_recovered25_petskill_runtime import STABLE_COMMON_CALLBACKS
 pins={}
 for path,expected in PRIOR_PINS.items():
  raw=(ROOT/path).read_bytes();need(hashlib.sha256(raw).hexdigest()==expected,'prior source identity')
  pins[path]=pin(raw)
 source_raw=(ROOT/REPORT).read_bytes();need(hashlib.sha256(source_raw).hexdigest()==REPORT_SHA,'source report identity')
 source=json.loads(source_raw);replay(source)
 prior=parse_prior_pressure((ROOT/next(iter(PRIOR_PINS))).read_bytes())
 rows=model_crosswalk(source['material']['selected_rows'],prior,STABLE_COMMON_CALLBACKS)
 return {'schema':'stoneage.pet_skill_name_model_crosswalk.r45','source_report':pin(source_raw),
  'prior_source_pins':pins,'selected_row_count':len(rows),'rows':rows,
  'prior_positive_enemy_referenced_rows':sum(r['prior_positive_enemy_reference'] is not None for r in rows),
  'stable_common_model_rows':sum(r['stable_common_reference_model_available'] for r in rows),
  'prior_family_slot_use_counts_are_not_per_skill_or_new_execution':True,
  'id_zero_absence_from_positive_enemy_report_does_not_mean_missing_skill':True,
  'new_original_runtime_or_training_rules_added':0,'official_tw10_skills_authenticated':0,
  'overall_restoration_percent':None}


def verify_custody():
 c=json.loads((ROOT/CUSTODY).read_text())
 saved=c['raw_source_report'];need(pin((ROOT/saved['path']).read_bytes())=={k:saved[k] for k in ('bytes','sha256','git_blob')},'archived original JSON identity')
 first=c['source_attempts'][0];saved=first['raw_report']
 need(pin((ROOT/saved['path']).read_bytes())=={k:saved[k] for k in ('bytes','sha256','git_blob')},'first failed source report was changed')
 need(first['report_status']=='ORIGINAL_MEMBERS_ACQUIRED_DERIVATION_PENDING' and c['source_attempts'][1]['report_status']=='TWO_ORIGINAL_MEMBERS_DUAL_DECODE_SHA_CRC_AND_SIX_NAMES_QUALIFIED','source failure rewritten')
 need(c['raw_report_equal_to_timestamp_stripped_source_log'] is True,'original source log/report mismatch')
 for path,identity in c['source_extractor_and_dependencies'].items():
  need(pin((ROOT/path).read_bytes())==identity,'actual source-tested extraction/dependency drift')
 return True


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--write-crosswalk',action='store_true');args=parser.parse_args()
 verify_custody();raw=(ROOT/REPORT).read_bytes()
 need(hashlib.sha256(raw).hexdigest()==REPORT_SHA,'exact original derived report SHA')
 result=replay(json.loads(raw));crosswalk=build_crosswalk()
 encoded=json.dumps(crosswalk,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
 if args.write_crosswalk:(ROOT/CROSSWALK).write_text(encoded)
 else:need((ROOT/CROSSWALK).read_text()==encoded,'exact six-name model crosswalk replay')
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
