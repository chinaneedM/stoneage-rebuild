"""Independent offline acceptance of the bounded R42 preserved-NPC source metadata.

No original dialogue/raw NPC payload is required or permitted in Git.
"""
import copy
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'research/recovered/STONEAGE-PRESERVED-GENKOU-THIRD-SOURCE-R42.json'
R41=ROOT/'research/recovered/STONEAGE-PRESERVED-NPC-DELTA-SOURCE-R41.json'
PINS={
 'sb_kbu.arg':(258,'433d17a58869147f91cacc57487795d7686b53415872f0694aba02dbc869502b'),
 'sb_geno.create':(573,'5aec44349ae3a6071b0882fd40d693f3bf1e7bdaf9ba489ac3ffbc89e26331f1'),
 'sb_geno.template':(321,'76a826f1022276dfa9590e5ad51c6a96e9c88146a2fc39790c2cc60cbed60e2d'),
 'sb_kgi.arg':(281,'61c2aefca26c9d84db061f34c66c74b980006cac915fe732394f753daddbd586')}
KBU_ENEMIES=[1272,1277,1277,1280,1280,1278,1273,1273,1275,1275]
KGI_ENEMIES=[1271,1274,1274,1281,1281,1276,1279,1279,1276,1276]
def check(condition,message):
 if not condition:raise ValueError('R42_REJECT: '+message)

def validate(report,r41):
 check(report['schema']=='stoneage.preserved_genkou_third_guard.r42.source','schema')
 check(report['status']=='FOUR_ORIGINAL_NPC_FILES_SHA_CRC_QUALIFIED','actual acquisition')
 check(report['source_scope']=='PRESERVED_COMMUNITY_MIXED25_GENKOU_ARGUMENT_NOT_OFFICIAL_OR_SAME_BUILD','carrier qualification')
 for key,expect in [('original_server_executed',False),('official_same_build_authenticated',False),
                    ('origin_class','ORIGIN_UNRESOLVED'),('verified_base_quests_added',0),
                    ('full_raw_npc_script_published',False)]:
  check(report[key]==expect,key)
 check('error' not in report,'unresolved acquisition error')
 receipts=report['receipt']
 check(receipts['headers_visited']==7954,'whole directory traversed')
 check(0<receipts['actual_range_bytes']<=16*1024*1024,'bounded source HTTP bytes')
 check(not receipts['whole_package_rehashed'],'not a bulk re-download')
 members=receipts['members']
 check(len(members)==4 and len({x['name'] for x in members})==4,'four distinct original references')
 seen={}
 for entry in members:
  check(entry['name'].startswith('石器2.5客戶端+服務端+登入器/SA2.5服務端/gmsv/data/npc/100/'),'original carrier path')
  name=entry['name'].rsplit('/',1)[-1]
  check(name in PINS,'unlisted original member')
  check((entry['bytes'],entry['sha256'])==PINS[name],'complete original raw member SHA')
  check(0<=entry['crc32']<=0xffffffff and entry['compressed_bytes']>0,'CRC and payload')
  check(entry['extractor_returncode']==0,'original extraction result')
  seen[name]=entry
 check(set(seen)==set(PINS),'no member omitted')
 for name in ('sb_geno.create','sb_geno.template'):
  check(report['source_config_member_pins'][name]=={'length':PINS[name][0],'sha256':PINS[name][1]},'source config SHA')
 check(r41['status']=='THREE_ORIGINAL_NPC_SHA_CRC_MATCH_MODERN_DELTA_DERIVED','R41 source status')
 delta=report['argument_comparison'];old=delta['old_kbu'];new=delta['third_kgi']
 check((old['bytes'],old['sha256'])==PINS['sb_kbu.arg'],'old arg length SHA')
 check((new['bytes'],new['sha256'])==PINS['sb_kgi.arg'],'new arg length SHA')
 check(old['codec']==new['codec']=='cp950' and old['strict_decode'] and new['strict_decode'],'strict codec')
 prior=next(x for x in r41['argument_delta']['decode_candidates'] if x['codec']=='cp950')
 check(old['fields']==prior['fields'],'R41 old complete numeric and hashed field evidence')
 for profile in (old,new):
  check(profile['original_dialogue_published'] is False,'proprietary dialogue')
  check(profile['keys_in_order']==[f['key'] for f in profile['fields']],'field sequence')
  check(len(set(profile['keys_in_order']))==len(profile['fields']),'duplicate field')
  check(profile['crlf']==0 and profile['lf']==len(profile['fields']),'line break preservation')
  check(all(len(f['value_utf8_sha256'])==64 for f in profile['fields']),'non-numeric fingerprint integrity')
 def as_map(v):return {x['key']:x for x in v['fields']}
 a=as_map(old);b=as_map(new);shared=[key for key in old['keys_in_order'] if key in b]
 check(delta['shared_keys_in_kbu_order']==shared,'shared field positions')
 check(delta['kbu_only_keys']==['time'],'old-only time')
 check(delta['kgi_only_keys']==['warpfl','warpx','warpy'],'new-only warp fields')
 changed=[key for key in shared if a[key]['value_utf8_sha256']!=b[key]['value_utf8_sha256']]
 check(delta['changed_fields']==changed==['askbattlemsg1','dieact','enemyno'],'full changed-field list')
 check(delta['unchanged_fields']==[key for key in shared if key not in changed],'unchanged fields')
 for key,nums in [('entype',[2]),('dieact',[0]),('enemyno',KBU_ENEMIES),('time',[180]),('onebattle',[0])]:
  check(a[key]['numbers']==nums,'old '+key)
 for key,nums in [('entype',[2]),('dieact',[1]),('enemyno',KGI_ENEMIES),('warpfl',[11215]),('warpx',[9]),('warpy',[16]),('onebattle',[0])]:
  check(b[key]['numbers']==nums,'third '+key)
 differences=[{'field':k,'kbu':a[k].get('numbers'),'kgi':b[k].get('numbers')} for k in shared
              if a[k].get('numbers')!=b[k].get('numbers') and
              ('numbers' in a[k] or 'numbers' in b[k])]
 check(delta['numeric_differences']==differences,'all numeric deviations')
 check(not delta['raw_equal'] and delta['length_difference_kgi_minus_kbu']==23,'distinct arguments')
 check(delta['full_text_or_payload_published'] is False,'no original dialogue contents')
 third=report['third_guard_original_reference']
 check(third['floorid']==11214 and third['borncenter']==[41,36,1,1] and
       third['graphicname']==100343 and third['source_argument']=='100/sb_kgi.arg','original configuration linkage')
 check(third['statement_kind']=='ORIGINAL_PRESERVED_CONFIG_NOT_RUNTIME','not a runtime route')
 check(report['private_transfer']['private_payload_in_public_git'] is False,'no private artifact in public Git')
 check(report['private_transfer']['recipient_certificate_sha256']=='f4975ae7879cb1509c4394d9aebced753f5a642cda37f9bb740a2c0263b6d179','pinned recipient cert')
 check(report['private_transfer']['plaintext_zip_bytes']>0 and report['private_transfer']['ciphertext_bytes']>0,'private source transfer evidence')
 return {'accepted':True,'material':'THIRD_GUARD_ARG_NUMERIC_AND_FIELD_DELTA','original_files_verified':4,
  'kgi_bytes':281,'kgi_warp_fields':[11215,9,16],'raw_enemyno_occurrences':10,
  'authentic_official_base_quest_added':0,'runtime_executed':False,
  'source_run':40456016963,'source_job':122029396896}

if __name__=='__main__':
 print(json.dumps(validate(json.loads(SOURCE.read_text()),json.loads(R41.read_text())),sort_keys=True))
