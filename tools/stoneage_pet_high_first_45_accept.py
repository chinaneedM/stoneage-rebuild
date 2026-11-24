"""PET45 independent graph acceptance: preserve source scopes and verify full route join."""
import argparse, collections, hashlib, json
from pathlib import Path
from tools.stoneage_pet_high_first_45_source import PINS, load
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/pets/PET-HIGH-FIRST-45-BULK-ACQUISITION-R1.json'
def index(rows,key):
    d={key(x):x for x in rows}
    assert len(d)==len(rows)
    return d
def static(d):
    w=d['world20'];p=d['pet10'];c=d['tw75']
    base=index(p['source_rows']['enemybase.txt'],lambda x:x[1])
    e=index(w['source_enemy_instances'],lambda x:x['id'])
    t=index(w['source_templates'],lambda x:x['id'])
    # Build the reverse group-to-area relation separately from the source replay.
    locations=collections.defaultdict(list)
    for a in w['source_areas']:
        for slot,gid,weight,status in a['group_slots']:
            if status=='GROUP_FOUND' and weight and int(weight)>0:
                locations[gid].append((a['id'],slot,int(weight)))
    routes=collections.defaultdict(collections.Counter)
    for g in w['source_resolved_groups']:
        assert len({s[1] for s in g['enemy_slots']})==len(g['enemy_slots'])
        for slot,eid,weight,status in g['enemy_slots']:
            if status!='INSTANCE_FOUND' or not weight or int(weight)<=0:continue
            tid=e[eid]['template'];b=base[tid];x=t[tid]
            assert (x['graphic'],x['raw_petflag'])==(b[2],b[3])
            if b[3]!=1:continue
            for area,gs,gw in locations[g['id']]:
                routes[tid][(area,gs,g['id'],slot,eid,gw,int(weight))]+=1
    exact={x['template_id'] for x in c['pet_flag_1_field_projections'] if x['template_id'] in base and x['row_sha256']==base[x['template_id']][16]}
    assert len(exact)==440 and len(routes)==129 and len(exact&routes.keys())==123
    assert sum(sum(v.values()) for v in routes.values())==2587
    assert sum(sum(routes[k].values()) for k in exact&routes.keys())==2473
    assert sum(not x[2] for a in w['source_areas'] for x in a['group_slots'])==9
    assert sum(not x[2] for g in w['source_resolved_groups'] for x in g['enemy_slots'])==4
    assert len(w['missing_group_ids_selected_group1_only'])==31 and len(w['inverted_coordinate_area_ids'])==12
    return base,e,t,routes,exact
def verify(d,data):
    base,e,t,routes,exact=static(d);w=d['world20'];p=data['projection']
    assert data['schema']=='stoneage.pet45.high_first_bulk_acquisition.r1'
    assert data['input_git_blobs']=={k:v[1] for k,v in PINS.items()}
    assert not data['original_payload_published']
    for k in ('original_game_executed','official_same_deployment_verified','official_capture_verified'):assert p[k] is False
    receipt=data['member_receipt'];members=receipt['members']
    assert data['original_member_count']==len(members)==2
    assert receipt['headers_visited']==7954
    assert receipt['range_requests']==len(receipt['range_receipts'])
    assert receipt['actual_range_bytes']==sum(v['bytes'] for v in receipt['range_receipts'])
    assert not receipt['whole_archive_or_parts_rehashed']
    prior={x['path']:x for x in d['r41']['member_receipt']['members']}
    seen=set()
    for m in members:
        name=m['path'].rsplit('/',1)[-1];assert name not in seen
        seen.add(name);pin=w['source_files'][name]
        assert (m['bytes'],m['sha256'])==(pin['size_bytes'],pin['sha256'])
        assert m['extractor']=='unar' and not m['flags']&(1|2|4|16)
        assert all(m[k]==prior[m['path']][k] for k in ('bytes','sha256','crc32','header_sha256','compressed_payload_sha256'))
    assert seen=={'enemy.txt','encount.txt'}
    instances=index(p['instance_metadata'],lambda x:x['id']);areas=index(p['area_metadata'],lambda x:x['id'])
    assert instances.keys()==e.keys()
    assert len(instances)==719 and len(areas)==660
    for i,x in instances.items():
        b=e[i];lo,hi=map(int,b['raw_level_fields_5_6'])
        expected=sorted((hi if lo==0 else lo,hi))
        assert (x['template_id'],x['source_line'],x['raw_level_fields'],x['level'])==(b['template'],b['source_line'],[lo,hi],expected)
        assert type(x['pet_flag']) is int
    for a in w['source_areas']:
        x=areas[a['id']]
        assert (x['source_line'],x['floor'],x['raw_rectangle'])==(a['source_line'],a['floor'],a['raw_rectangle'])
        assert x['raw_rate_fields']==[int(v) if v else -1 for v in a['raw_fields_6_9'][:2]]
        assert len(x['raw_event_fields'])==3 and all(type(v) is int for v in x['raw_event_fields'])
        assert x['inverted_rectangle']==(a['id'] in w['inverted_coordinate_area_ids'])
    report_routes=index(p['mixed25_template_routes'],lambda x:x['template_id'])
    assert report_routes.keys()==routes.keys()
    for tid,x in report_routes.items():
        assert x['graphic']==base[tid][2] and x['source_template_row_sha256']==base[tid][16]
        assert collections.Counter(map(tuple,x['routes']))==routes[tid]
    c=d['tw75']['pet_flag_1_field_projections']
    r41={x['template']['id'] for x in d['r41']['projection']['capture_candidates']}
    r42={x['template_id'] for x in d['r42']['rows']}
    r17=index(d['r17']['rows'],lambda x:x['template_id'])
    assert len(p['claimed_tw75_rows'])==len(c)==467
    for i,(x,b) in enumerate(zip(p['claimed_tw75_rows'],c,strict=True)):
        tid=b['template_id'];m=base.get(tid);match=tid in exact
        rr=list(routes[tid].elements()) if match and tid in routes else []
        eligible=[r for r in rr if instances[r[4]]['pet_flag']==1]
        lv1=[r for r in eligible if instances[r[4]]['level'][0]<=1<=instances[r[4]]['level'][1]]
        assert (x['tw75_row_index'],x['template_id'],x['graphic'],x['tw75_row_sha256'])==(i,tid,b['graphic'],b['row_sha256'])
        assert x['mixed25_template_row_index']==(m[0]-1 if m else None)
        assert x['match_status']==('EXACT_SHARED_TEMPLATE_ROW' if match else 'SAME_ID_NONIDENTICAL_ROW' if m else 'NO_SAME_ID_IN_SELECTED_MIXED25_TABLE')
        assert (x['positive_route_count'],x['double_pet_flag_route_count'],x['lv1_double_flag_route_count'])==(len(rr),len(eligible),len(lv1))
        assert x['double_flag_floor_ids']==sorted({areas[r[0]]['floor'] for r in eligible})
        assert (x['previous_r41_template'],x['previous_r42_reward_template'])==(tid in r41,tid in r42)
        assert x['r17_later_comparison_positive_reference_count']==r17[tid]['positive_reference_count']
        assert x['official_acquisition_verified'] is False
    s=p['summary'];rows=p['claimed_tw75_rows']
    expected={'claimed_rows':467,'exact_shared_rows':440,'exact_shared_positive_templates':123,'mixed25_positive_templates':129,'exact_shared_double_flag_templates':sum(x['double_pet_flag_route_count']>0 for x in rows),'exact_shared_lv1_double_flag_templates':sum(x['lv1_double_flag_route_count']>0 for x in rows),'exact_positive_without_r41_or_r42':sum(x['positive_route_count']>0 and not x['previous_r41_template'] and not x['previous_r42_reward_template'] for x in rows),'mixed25_positive_routes':2587,'blank_area_group_weight_slots':9,'blank_group_enemy_weight_slots':4,'missing_group_ids':w['missing_group_ids_selected_group1_only'],'inverted_area_ids':w['inverted_coordinate_area_ids']}
    assert s==expected
    print('PET45 independently verified',json.dumps(s,ensure_ascii=False,sort_keys=True))
def verify_floors(data):
    def pinned(path,sha):
        raw=(ROOT/path).read_bytes()
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==sha,path
        return raw
    f=json.loads(pinned('research/pets/PET-HIGH-FIRST-45-FLOOR-REFERENCES-R1.json','fa15a2a93ed820160571aef28294c029d5196666'))
    m=json.loads(pinned('research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json','1ef8c004179128ea44ffa4fb4259748bc8c83911'))
    names=pinned('research/recovered/STONEAGE-25-STABLE-MAP-NAMES-R1.txt','8c9e3a73cbf9a8054d5a0ad82d57582d8535b6e3').decode('utf-8')
    assert f['source_git_blobs']=={'world20':PINS['world20'][1],'map04':'1ef8c004179128ea44ffa4fb4259748bc8c83911','later_recovered_names':'8c9e3a73cbf9a8054d5a0ad82d57582d8535b6e3','pet45':'5273e2c3f6a71fa9ea8a2f7b51139f280a9e9808'}
    assert m['provenance']['original_mixed25_community_RAR_sha256']=='d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'
    dat={int(x[0].removesuffix('.dat')):(i,x) for i,x in enumerate(m['per_floor_source_rows'])}
    assert len(dat)==955
    ns={}
    for i,line in enumerate(names.splitlines(),1):
        if not line.startswith('MAP_NAME|'):continue
        n=dict(s.split('=',1) for s in line.split('|')[1:])
        key=int(n['floor']);assert key not in ns
        ns[key]=(i,n)
    p=data['projection'];area=index(p['area_metadata'],lambda x:x['id'])
    floor_ids=sorted({area[r[0]]['floor'] for x in p['mixed25_template_routes'] for r in x['routes']})
    assert len(floor_ids)==281 and [x['floor_id'] for x in f['rows']]==floor_ids
    for row in f['rows']:
        k=row['floor_id']
        if k in dat:
            i,x=dat[k]
            assert row['same_archive_dat']==dict(source_row_index=i,filename=x[0],sha256=x[2],width=x[3],height=x[4],qualification='SAME_ARCHIVE_FILE_NOT_NATIVE_RUNTIME')
        else:assert row['same_archive_dat'] is None
        if k in ns and ns[k][1]['status']=='RESOLVED_BIG5_CP950_CONSENSUS':
            i,n=ns[k]
            assert row['later_recovered_name']==dict(source_line=i,source_escaped_name=n['name'],display_name_candidate=n['name'].split('%7C')[0],raw_sha256=n['raw_sha256'],qualification='RECOVERED_FLOOR_NAME_REFERENCE_NOT_SAME_DEPLOYMENT')
        else:assert row['later_recovered_name'] is None
    assert f['summary']=={'floor_count':281,'same_archive_dat_count':266,'recovered_name_reference_count':267}
    assert sum(x['same_archive_dat'] is not None for x in f['rows'])==266
    assert sum(x['later_recovered_name'] is not None for x in f['rows'])==267
    assert not f['official_same_deployment_verified'] and not f['official_capture_verified']
    print('PET45 floor references: 281 / 266 same archive DAT / 267 separate recovered names')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path,default=REPORT);ap.add_argument('--sha256');ap.add_argument('--static',action='store_true');a=ap.parse_args()
    d=load()
    if a.static:
        static(d);print('PET45 static graph: 467/440/123, 129 mixed25 templates, 2587 positive slots; 9+4 blank slots excluded.');return
    raw=a.report.read_bytes()
    if a.sha256:assert hashlib.sha256(raw).hexdigest()==a.sha256
    data=json.loads(raw)
    verify(d,data)
    if a.report==REPORT:verify_floors(data)
if __name__=='__main__':main()
