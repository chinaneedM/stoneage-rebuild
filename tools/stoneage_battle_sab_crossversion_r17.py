"""Lossless TW1.0 vs mixed2.5 battle SAB exact-content occurrences.

Replay archived source-derived file manifests, not executable payloads.
The contemporary notice is a later reprint, not proof of those files' identity.
"""
from __future__ import annotations
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-BATTLE-SAB-CROSSVERSION-R17.json'
SOURCES={
 'tw':{'path':'research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt','git_blob':'564233902b10c60760d4f93b1ea65d4dd1469206','profile':'TW10_AUTHENTICATED_RETAIL'},
 'mixed':{'path':'research/recovered/STONEAGE-25-GAMEPLAY-DATA-INVENTORY-R1.txt','git_blob':'47157f638cce7023727035981da11f1faecc9c78','profile':'MIXED25_UNVERIFIED_COMMUNITY_PRESERVATION'}
}
NOTICE={
 'later_republication_url':'https://www.shiqi.tv/shiqi79.htm',
 'republication_date':'2015-12-21',
 'attributed_operator_notice_date':'2001-05-10',
 'attributed_operator':'Beijing Waei',
 'attributed_download_names':['battlemap218.sab','battlemap219.sab'],
 'actual_preserved_mixed_names':['battle218.sab','battle219.sab'],
 'notice_is_original_2001_source_bytes':False,
 'same_file_proven':False,
 'runtime_battle_mapping_proven':False,
 'claim':'A 2015 retrospective repost alleges an operator request for battle map downloads during the Mainland rebirth rollout; filenames differ from preserved client listing and original update payload has not been verified'
}

def need(x,msg):
    if not x:raise ValueError(msg)

def git_blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def source_lines(key):
    info=SOURCES[key]
    data=(ROOT/info['path']).read_bytes()
    need(git_blob(data)==info['git_blob'], 'source Git blob changed: '+key)
    return data.decode('utf-8').splitlines()

def parse(lines,key):
    out=[]
    for line in lines:
        if key=='tw':
            if not line.startswith('BATTLE_SAB_RECORD|'):continue
            parts=dict(x.split('=',1) for x in line.split('|')[1:])
            path=parts['path'];size=int(parts['size'])
            digest=parts['payload_sha256']
            need(parts['header_hex']=='53414220' and int(parts['tile_count'])==400, 'original TW10 SAB header marker changed')
        else:
            if not line.startswith('CANDIDATE|client|battle_progression|battleMap/'):continue
            words=line.split('|')
            need(len(words)>=7 and words[5]=='.sab','mixed item fields changed')
            path=words[3];size=int(words[4]);digest=words[6]
        m=re.fullmatch(r'(?:StoneAge/data/battlemap|battleMap)/battle(\d+)\.sab',path)
        need(m is not None, 'unexpected physical SAB path: '+path)
        need(size==804 and re.fullmatch('[0-9a-f]{64}',digest) is not None,'malformed original source digest')
        out.append(dict(id=int(m.group(1)),path=path,size=size,sha256=digest))
    out.sort(key=lambda x:x['id'])
    need([x['id'] for x in out]==list(range(len(out))), 'missing/duplicate SAB path index')
    need(len(out)==(218 if key=='tw' else 220),'historical source file count changed')
    return out

def build():
    tw=parse(source_lines('tw'),'tw')
    mixed=parse(source_lines('mixed'),'mixed')
    need([x['id'] for x in mixed[len(tw):]]==[218,219], 'the two mixed-only index IDs changed')
    equal=sum(a['sha256']==b['sha256'] for a,b in zip(tw,mixed))
    groups=defaultdict(list)
    for name,rows in (('tw10',tw),('mixed25',mixed)):
        for x in rows:
            groups[x['sha256']].append(dict(profile=name,id=x['id']))
    duplicated=[dict(sha256=key,occurrences=value) for key,value in sorted(groups.items()) if len(value)>1]
    return {
      'schema':'stoneage.crossversion.battle_sab_source_records.r17',
      'material_task':'OFFICIAL-NAMED-CONTENT-MATERIAL-ROTATION-17',
      'source_profiles':SOURCES,
      'source_scope':'TW10 actual authenticated retail-derived SAB records + a later mixed2.5 preserved community client folder; NOT two authenticated official builds',
      'classification':'DERIVED_NUMERIC_RESOURCE_CONTENT_LINK_NO_NPC_PET_OR_QUEST_IDENTITY',
      'shared_index_range':[0,217],
      'original_tw10_file_count':len(tw),'mixed25_file_count':len(mixed),
      'same_index_sha256_equal_count':equal,
      'same_index_sha256_diff_count':len(tw)-equal,
      'mixed25_only_numeric_ids':[x['id'] for x in mixed[len(tw):]],
      'all_occurrence_count':len(tw)+len(mixed),
      'all_unique_sha256_count':len(groups),
      'duplicate_content_groups':duplicated,
      'original_byte_count_committed':0,
      'original_source_files_deleted':0,
      'no_original_deployment_or_runtime_proven':True,
      'notice_context':NOTICE,
      'findings':{
        'inventory_membership_verified':True,'cross_version_same_content_proven':False,
        'all_official_versions_recovered':False,
        'original_npc_ids_recovered':0,'original_quest_server_records_recovered':0,
        'original_pet_names_recovered':0,
        'source_grade':'S_FOR_PRIOR_AUTHENTICATED_TW10_INVENTORY_BOUNDED_ARCHIVE_FOR_MIXED25_SECONDARY_FOR_2001_NOTICE',
        'next':'EARLY-OFFICIAL-SERVER-MASTER-DATA-SOURCE-18_OR_EXACT_DOWNLOAD_PAYLOAD_CARRIER'
      },
      'occurrences':[dict(profile='tw10',**x) for x in tw]+[dict(profile='mixed25',**x) for x in mixed]
    }

def validate(doc):
    need(doc==build(), 'permanent cross-version archive not equal to exact original source manifests')
    need(doc['all_occurrence_count']==438 and doc['all_unique_sha256_count']==436,'lossless dedup invariant')
    need(doc['same_index_sha256_equal_count']==0 and doc['same_index_sha256_diff_count']==218,'the matched IDs are NOT identical bytes')
    need(doc['mixed25_only_numeric_ids']==[218,219], 'mixed-only suffix')
    need(doc['duplicate_content_groups']==[
      {'sha256':'a328637919ac10ae6a977efcd0b272913b4d7b0c34e31af2fa84cf867dd8e1d6','occurrences':[{'profile':'tw10','id':145},{'profile':'tw10','id':146}]},
      {'sha256':'b3e6c9a3c3dd7375d4898ab4f8e1a5e2c684f60a0ab9c045e95fcd4c20b33476','occurrences':[{'profile':'mixed25','id':145},{'profile':'mixed25','id':146}]}
    ], 'repeated entries cannot be collapsed by numeric ID or source profile')
    context=doc['notice_context']
    need(context['attributed_download_names']!=context['actual_preserved_mixed_names'] and not context['same_file_proven'], '2001 reprint falsely upgraded to file identity')
    for flag in ['cross_version_same_content_proven','all_official_versions_recovered']:
        need(doc['findings'][flag] is False, 'unproven claim promoted '+flag)
    for name in ['original_npc_ids_recovered','original_quest_server_records_recovered','original_pet_names_recovered']:
        need(doc['findings'][name]==0, 'unproven historical identity')
    need(doc['original_byte_count_committed']==0 and doc['original_source_files_deleted']==0, 'copyright/original evidence deletion')
    return doc

if __name__=='__main__':
    x=build()
    validate(x)
    print(json.dumps({'schema':x['schema'],
     'original_tw10_file_count':x['original_tw10_file_count'],
     'mixed25_file_count':x['mixed25_file_count'],
     'same_index_sha256_diff_count':x['same_index_sha256_diff_count'],
     'unique_sha256_count':x['all_unique_sha256_count'],
     'source_byte_deletions':x['original_source_files_deleted']},sort_keys=True))
