"""Verify SCENE12 controlled scene-viewer witness scope without public original sprites."""
import argparse, hashlib, json, re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE_LEN=1150992
SOURCE_SHA='00e7565587e009c3e44bcffa1523ab4018886d637aaef1e04749dc01637628d4'
REPORT=ROOT/'research/recovered/STONEAGE-SCENE12-CONTROLLED-OBSERVER-COVERAGE-R1.json'
R9=ROOT/'research/recovered/STONEAGE-SCENE09-NATIVE-ORDER-R9.json'

def need(ok, reason):
    if not ok: raise ValueError(reason)

def select_case(cases, anchor, pet, direction, human_bitmap, pet_bitmap):
    found=[c for c in cases if c['anchor']==list(anchor) and c['pet_spr']==pet and c['direction']==direction]
    need(len(found)<=1,'duplicate controlled case')
    if not found:return 'NO_CONTROLLED_R9_CASE', None
    c=found[0]
    need([a['token'] for a in c['actors']]==['human','pet'],'actor identities')
    if [a['bitmapno'] for a in c['actors']] != [human_bitmap, pet_bitmap]:
        return 'SOURCE_FRAME_DIFFERS_FROM_R9_CASE', None
    return 'EXACT_CONTROLLED_R9_NOT_LIVE_RUNTIME', c

EXPECTED={
  'schema':'stoneage.scene12.private_observer_controlled_input_scope.r1',
  'verified_source_sha256':SOURCE_SHA,'verified_source_bytes':SOURCE_LEN,
  'R9_controlled_unique_case_keys':48,'case_keys_by_pet':{'100250':32,'100251':8,'100252':8},
  'center_anchor_case_keys':24,'exact_source_bitmap_pair_frame_states':56,
  'exact_source_bitmap_pair_by_pet':{'100250':32,'100251':8,'100252':16},
  'viewer_source_anchor_pet_direction_frame_states':6400,'unwitnessed_viewer_states':6344,
  'fallback_is_modern_explicit_only':True,'controlled_case_is_original_world_execution':False,
  'original_full_frame_phase_order_proven':False,'original_client_launched':False,
  'official_pet_species_authenticated':False,'percent_restored':None,
}

def validate(report, r9):
    need(r9['schema']=='stoneage.controlled_actor_parts_order.r9','R9 source schema')
    need(r9['original_world_entered'] is False and r9['complete_original_frame_phase_order_proven'] is False,'R9 original limits')
    cases=r9['cases']
    need(len(cases)==48 and r9['case_count']==48,'R9 case count')
    keys=[(tuple(c['anchor']),c['pet_spr'],c['direction']) for c in cases]
    need(len(set(keys))==48,'R9 unique witness tuples')
    need(Counter(c['pet_spr'] for c in cases)=={100250:32,100251:8,100252:8},'R9 by-pet cases')
    need(sum(c['anchor']==[15,15] for c in cases)==24,'center cases')
    need(set(report)==set(EXPECTED),'source-safe report field set')
    for k,v in EXPECTED.items():need(type(report[k])==type(v) and report[k]==v,'R12 unsupported claim: '+k)
    need(report['exact_source_bitmap_pair_frame_states']+report['unwitnessed_viewer_states']==6400,'state conservation')
    return {'public_R9_cases':48,'exact_controlled_inputs':56,'private_original_pngs_in_CI':False}

def audit_private(path):
    raw=Path(path).read_bytes()
    need(len(raw)==SOURCE_LEN and hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'private source whole-file SHA')
    m=re.search(rb'<script id="evidence" type="application/json">(.*?)</script>',raw,re.S)
    need(m is not None,'private source evidence pack')
    pack=json.loads(m.group(1))
    cases=pack['actor_order_evidence']['cases']
    need(len(cases)==48 and pack['pet_evidence']['original_world_entered'] is False,'private source historical limits')
    groups={g['spr_no']:g for g in pack['actors']['groups']}
    need(set(groups)=={100000,100250,100251,100252},'source actor groups')
    exact=Counter()
    for c in cases:
        h=next(x for x in groups[100000]['animations'] if x['action']==2 and x['direction']==c['direction'])
        p=next(x for x in groups[c['pet_spr']]['animations'] if x['action']==2 and x['direction']==c['direction'])
        for i,frame in enumerate(p['frames']):
            tag,_=select_case(cases,c['anchor'],c['pet_spr'],c['direction'],h['frames'][i%len(h['frames'])][0],frame[0])
            if tag=='EXACT_CONTROLLED_R9_NOT_LIVE_RUNTIME':exact[c['pet_spr']]+=1
    need(dict(exact)=={100250:32,100251:8,100252:16},'original source bitmap-pair replay')
    return {'private_source_SHA_verified':True,'exact_controlled_input_matches':sum(exact.values()),'original_game_world_entered':False}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--private-html',type=Path)
    a=ap.parse_args()
    report=json.loads(REPORT.read_text(encoding='utf-8'))
    r9=json.loads(R9.read_text(encoding='utf-8'))
    result=validate(report,r9)
    if a.private_html:result['private']=audit_private(a.private_html)
    else:result['private']='NOT_RUN_NO_PRIVATE_SOURCE_IN_CI'
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
