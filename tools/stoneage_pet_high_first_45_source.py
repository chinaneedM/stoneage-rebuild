"""PET45: high-version first bulk acquisition, with only two missing original fields reaccessed."""
import argparse, collections, json, tempfile
from pathlib import Path
from tools import stoneage_pet_high_first_40_acquisition as r40
from tools import stoneage_preserved_item_shop_r44 as sparse
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'research/pets'
R=ROOT/'research/recovered'
PINS={
 'world20':(R/'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-20-ENCOUNTER-HABITAT-SOURCE-R1.json','f7203fd28bc1f8cb9d1edf08d08579123df053e9'),
 'pet10':(R/'STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json','25a37aeb134fb180e322e7dc335029b7374452d8'),
 'tw75':(P/'PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json','fec03646d7c7e4e287f9347c306119cc626d6abf'),
 'r41':(P/'PET-HIGH-FIRST-41-MIXED25-ACQUISITION-R1.json','746107dc2265e66629d64419fb039934de9baa11'),
 'r42':(P/'PET-HIGH-FIRST-42-EXACT-TEMPLATE-CROSSWALK-R1.json','c6667a6190283f4ec3ad3813c570357b18906ccc'),
 'r17':(P/'PET-HIGH-FIRST-17-COMPARISON-SKILL-ENCOUNTER-R1.json','63af501ab483770c5c58cb2d62152ab8923dcc2b'),
}
def load():
    d={}
    for k,(p,s) in PINS.items():
        raw=p.read_bytes();assert r40.git_blob(raw)==s,k
        d[k]=json.loads(raw)
    return d
def unique(rows,key):
    out={}
    for row in rows:
        k=key(row);assert k not in out,k
        out[k]=row
    return out
def derive(d,members):
    w,p,c,a,q,l=(d[k] for k in PINS)
    assert w['setup_selected']=={'encounter':'encount.txt','group':'group1.txt','enemy':'enemy.txt','template':'enemybase.txt'}
    assert w['original_archive_sha256']==p['preserved_original_rar']['sha256']
    for name in ('enemy.txt','encount.txt'):
        raw=members['data/'+name];pin=w['source_files'][name]
        assert (len(raw),r40.sha(raw))==(pin['size_bytes'],pin['sha256'])
    e_raw=members['data/enemy.txt'];a_raw=members['data/encount.txt']
    ei=r40.idx(r40.rows(e_raw,34,3),3);ai=r40.idx(r40.rows(a_raw,33,0),0)
    assert sum(map(len,ei.values()))==2087 and sum(map(len,ai.values()))==660
    bases=unique(p['source_rows']['enemybase.txt'],lambda x:x[1])
    prior_instances=unique(p['source_rows']['enemy.txt'],lambda x:x[1])
    groups=unique(w['source_resolved_groups'],lambda x:x['id'])
    enemies=unique(w['source_enemy_instances'],lambda x:x['id'])
    templates=unique(w['source_templates'],lambda x:x['id'])
    assert len(bases)==988 and len(prior_instances)==2087
    instance_rows={}
    for eid,e in enemies.items():
        ((line,b),)=ei[eid]
        assert (line,int(b[4]),[v.decode('ascii') for v in b[5:7]])==(e['source_line'],e['template'],e['raw_level_fields_5_6'])
        assert prior_instances[eid][2]==e['template']
        instance_rows[eid]={'id':eid,'template_id':e['template'],'source_line':line,'pet_flag':int(b[13]),'level':r40.level(b),'raw_level_fields':list(map(int,b[5:7]))}
    area_rows={}
    for area in w['source_areas']:
        ((line,b),)=ai[area['id']]
        assert (line,int(b[1]),list(map(int,b[2:6])))==(area['source_line'],area['floor'],area['raw_rectangle'])
        assert [x.decode('ascii') for x in b[6:10]]==area['raw_fields_6_9']
        assert all((int(b[10+slot]),int(b[20+slot]))==(gid,int(weight)) for slot,gid,weight,_ in area['group_slots'])
        area_rows[area['id']]={'id':area['id'],'source_line':line,'floor':area['floor'],'raw_rectangle':area['raw_rectangle'],'raw_event_fields':list(map(r40.num,b[30:33])),'raw_rate_fields':list(map(r40.num,b[6:8])),'inverted_rectangle':area['id'] in w['inverted_coordinate_area_ids']}
    routes=collections.defaultdict(list)
    for area in w['source_areas']:
        for slot,gid,gw,status in area['group_slots']:
            if status!='GROUP_FOUND' or int(gw)<=0:continue
            g=groups[gid]
            for es,eid,ew,estatus in g['enemy_slots']:
                if estatus!='INSTANCE_FOUND' or int(ew)<=0:continue
                e=instance_rows[eid];t=templates[e['template_id']];b=bases[t['id']]
                assert (t['graphic'],t['raw_petflag'])==(b[2],b[3])
                if t['raw_petflag']!=1:continue
                routes[t['id']].append([area['id'],slot,gid,es,eid,int(gw),int(ew)])
    assert len(routes)==129
    comparison=unique(l['rows'],lambda x:x['template_id'])
    r41={x['template']['id'] for x in a['projection']['capture_candidates']}
    r42={x['template_id'] for x in q['rows']}
    rows=[]
    for i,t in enumerate(c['pet_flag_1_field_projections']):
        tid=t['template_id'];b=bases.get(tid)
        exact=b is not None and b[16]==t['row_sha256']
        if exact:assert (b[2],b[3])==(t['graphic'],1)
        match='EXACT_SHARED_TEMPLATE_ROW' if exact else 'SAME_ID_NONIDENTICAL_ROW' if b else 'NO_SAME_ID_IN_SELECTED_MIXED25_TABLE'
        # Nonidentical IDs are not treated as a qualified source acquisition link.
        rr=routes.get(tid,[]) if exact else []
        eligible=[v for v in rr if instance_rows[v[4]]['pet_flag']==1]
        lv1=[v for v in eligible if instance_rows[v[4]]['level'][0]<=1<=instance_rows[v[4]]['level'][1]]
        rows.append(dict(tw75_row_index=i,template_id=tid,graphic=t['graphic'],tw75_row_sha256=t['row_sha256'],mixed25_template_row_index=b[0]-1 if b else None,match_status=match,positive_route_count=len(rr),double_pet_flag_route_count=len(eligible),lv1_double_flag_route_count=len(lv1),double_flag_floor_ids=sorted({area_rows[v[0]]['floor'] for v in eligible}),previous_r41_template=tid in r41,previous_r42_reward_template=tid in r42,r17_later_comparison_positive_reference_count=comparison[tid]['positive_reference_count'],official_acquisition_verified=False))
    assert len(rows)==467 and sum(r['match_status']=='EXACT_SHARED_TEMPLATE_ROW' for r in rows)==440
    assert sum(r['positive_route_count']>0 for r in rows)==123
    # Keep mixed25-only or mismatched IDs in their own source namespace too.
    all_routes=[{'template_id':tid,'graphic':bases[tid][2],'source_template_row_sha256':bases[tid][16],'routes':rr} for tid,rr in sorted(routes.items())]
    return {'claimed_tw75_rows':rows,'mixed25_template_routes':all_routes,'route_columns':['area_id','area_group_slot','group_id','group_enemy_slot','enemy_instance_id','area_group_weight','group_enemy_weight'],'instance_metadata':list(instance_rows.values()),'area_metadata':list(area_rows.values()),'summary':{'claimed_rows':len(rows),'exact_shared_rows':440,'exact_shared_positive_templates':123,'mixed25_positive_templates':len(routes),'exact_shared_double_flag_templates':sum(r['double_pet_flag_route_count']>0 for r in rows),'exact_shared_lv1_double_flag_templates':sum(r['lv1_double_flag_route_count']>0 for r in rows),'exact_positive_without_r41_or_r42':sum(r['positive_route_count']>0 and not r['previous_r41_template'] and not r['previous_r42_reward_template'] for r in rows),'mixed25_positive_routes':sum(map(len,routes.values())),'missing_group_ids':w['missing_group_ids_selected_group1_only'],'inverted_area_ids':w['inverted_coordinate_area_ids']},'original_game_executed':False,'official_same_deployment_verified':False,'official_capture_verified':False}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    d=load();w=d['world20']
    inv={r['path']:r for r in json.loads(r40.R18.read_bytes())['all_server_occurrences']}
    names=['enemy.txt','encount.txt']
    sparse.EXPECTED={'data/'+k:(inv[k]['size'],inv[k]['sha256']) for k in names}
    receipt={}
    with tempfile.TemporaryDirectory(prefix='pet45-private-') as work:
        members=sparse.acquire(Path(work),receipt,'unar')
        result=derive(d,members)
    out=dict(schema='stoneage.pet45.high_first_bulk_acquisition.r1',scope='MIXED25_SAVED_CONFIGURATION_AND_CLAIMED_TW75_EXACT_ROW_NOT_OFFICIAL_DEPLOYMENT',input_git_blobs={k:s for k,(p,s) in PINS.items()},member_receipt=receipt,original_member_count=len(members),projection=result,original_payload_published=False)
    raw=json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n';args.output.write_text(raw,encoding='utf-8')
    print('PET45_SUMMARY',json.dumps(result['summary'],ensure_ascii=False,separators=(',',':')))
    print('PET45_REPORT_SHA256',r40.sha(raw.encode()),'GIT_BLOB',r40.git_blob(raw.encode()),'BYTES',len(raw.encode()))
if __name__=='__main__':main()
