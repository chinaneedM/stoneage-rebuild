"""Bounded original Genkou third guard argument material, source pass R42.

Reads four small archived NPC files only after pinned original SHA/CRC; publishes
hashes, non-dialogue numeric fields and bounded differences, never original prose.
"""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
from tools import stoneage_preserved_npc_delta_r41 as r41

ORIGINAL_KGI=('sb_kgi.arg',281,'61c2aefca26c9d84db061f34c66c74b980006cac915fe732394f753daddbd586')
SCOPE='PRESERVED_COMMUNITY_MIXED25_GENKOU_ARGUMENT_NOT_OFFICIAL_OR_SAME_BUILD'
def sha(b): return hashlib.sha256(b).hexdigest()

def fingerprint(raw):
    text=raw.decode('cp950','strict')
    fields=r41.decode_fields(text)
    r41.need(fields is not None and len(fields)>0,'unknown NPC ARG grammar must be reported not ignored')
    keys=[f['key'] for f in fields]
    r41.need(len(keys)==len(set(keys)),'duplicate ARG key cannot be flattened')
    return {'bytes':len(raw),'sha256':sha(raw),'codec':'cp950',
      'strict_decode':True,'unicode_sha256':sha(text.encode('utf-8')),
      'unicode_chars':len(text),'lf':raw.count(b'\n'),'crlf':raw.count(b'\r\n'),
      'keys_in_order':keys,'fields':fields,'original_dialogue_published':False}

def finite_diff(kbu,kgi):
    a=fingerprint(kbu);b=fingerprint(kgi)
    am={f['key']:f for f in a['fields']};bm={f['key']:f for f in b['fields']}
    shared=[k for k in a['keys_in_order'] if k in bm]
    changed=[k for k in shared if am[k]['value_utf8_sha256']!=bm[k]['value_utf8_sha256']]
    result={'old_kbu':a,'third_kgi':b,'raw_equal':kbu==kgi,
      'common_prefix_bytes':next((i for i,(x,y) in enumerate(zip(kbu,kgi)) if x!=y),min(len(kbu),len(kgi))),
      'different_overlapping_byte_offsets':sum(x!=y for x,y in zip(kbu,kgi)),
      'length_difference_kgi_minus_kbu':len(kgi)-len(kbu),
      'shared_keys_in_kbu_order':shared,
      'kbu_only_keys':[k for k in a['keys_in_order'] if k not in bm],
      'kgi_only_keys':[k for k in b['keys_in_order'] if k not in am],
      'changed_fields':changed,
      'unchanged_fields':[k for k in shared if k not in changed],
      'numeric_differences':[
         {'field':k,'kbu':am[k]['numbers'],'kgi':bm[k]['numbers']}
         for k in shared if am[k].get('numbers')!=bm[k].get('numbers')
         and ('numbers' in am[k] or 'numbers' in bm[k])],
      'full_text_or_payload_published':False}
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--sealed',type=Path,required=True)
    args=p.parse_args()
    report={'schema':'stoneage.preserved_genkou_third_guard.r42.source',
      'status':'NOT_ACQUIRED','source_scope':SCOPE,
      'original_server_executed':False,'official_same_build_authenticated':False,
      'origin_class':'ORIGIN_UNRESOLVED','verified_base_quests_added':0,
      'full_raw_npc_script_published':False,'receipt':{}}
    try:
        with tempfile.TemporaryDirectory(prefix='stoneage-r42-') as tmp:
            original=dict(r41.EXPECTED)
            r41.EXPECTED={**original,ORIGINAL_KGI[0]:(ORIGINAL_KGI[1],ORIGINAL_KGI[2])}
            members=r41.acquire(Path(tmp),report['receipt'])
            r41.need(set(members)==set(r41.EXPECTED),'all four original small members present')
            r41.need(report['receipt']['actual_range_bytes']<=16*1024*1024,'source exceeded bounded HTTP range allowance')
            report['argument_comparison']=finite_diff(members['sb_kbu.arg'],members['sb_kgi.arg'])
            report['source_config_member_pins']={
              k:{'length':len(members[k]),'sha256':sha(members[k])}
              for k in ('sb_geno.create','sb_geno.template')}
            report['third_guard_original_reference']={
                'source':'R41 original sb_geno.create third block',
                'floorid':11214,'borncenter':[41,36,1,1],
                'graphicname':100343,
                'source_argument':'100/sb_kgi.arg',
                'statement_kind':'ORIGINAL_PRESERVED_CONFIG_NOT_RUNTIME'}
            report['private_transfer']=r41.seal(members,Path(tmp),args.sealed)
            report['status']='FOUR_ORIGINAL_NPC_FILES_SHA_CRC_QUALIFIED'
    except Exception as exc:
        report['error']={'type':type(exc).__name__,'message':str(exc)[:300]}
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print('R42_METADATA_BEGIN')
    print(args.output.read_text(),end='')
    print('R42_METADATA_END')
if __name__=='__main__':main()
