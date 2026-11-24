"""Read only bounded original preserved members for residual pet acquisition.
All alternate table joins are counterfactual, not official deployed configuration.
No original payload or dialogue is exported.
"""
import argparse, collections, json, re, tempfile
from pathlib import Path
from tools import stoneage_pet_high_first_40_acquisition as r40
from tools import stoneage_preserved_item_shop_r44 as sparse
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'research/pets'
R=ROOT/'research/recovered'
PINS={
 'prev':(P/'PET-HIGH-FIRST-49-DATED-PC-ACQUISITION-GAP-R1.json','3ae127ef6bee449a472b7b4323b09f930e1c8684'),
 'master':(P/'PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json','fec03646d7c7e4e287f9347c306119cc626d6abf'),
 'pet10':(R/'STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json','25a37aeb134fb180e322e7dc335029b7374452d8'),
 'world20':(R/'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-20-ENCOUNTER-HABITAT-SOURCE-R1.json','f7203fd28bc1f8cb9d1edf08d08579123df053e9'),
 'old45':(P/'PET-HIGH-FIRST-45-BULK-ACQUISITION-R1.json','5273e2c3f6a71fa9ea8a2f7b51139f280a9e9808'),
 'r18':(R/'STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json','f4ac9b805724bcd847c9632cad3c35bc4309a526'),
 'char01':(R/'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json','a088b61a3212f7049e7793f587123ffb29bebad7'),
}
TABLES=['encount.txt','group1.txt','group.txt','enemy.txt','enemy2.txt']
NPCS=['my/vipshop/vippetshop.arg','my/vipshop/vippetshop1.arg','my/vipshop/vippetshop2.arg','my/vipshop/vippetshop5.arg','sa60/newbie/petmaster','sa60/newbie/m_tiger']
def load():
    d={}
    for k,(p,s) in PINS.items():
        raw=p.read_bytes();assert r40.git_blob(raw)==s,k
        d[k]=json.loads(raw)
    return d
def unique(rows,col):
    out={}
    for line,a in rows:
        k=r40.num(a[col]);assert k not in out,(k,line)
        out[k]=(line,a)
    return out
def derive(d,m):
    p=d['pet10'];w=d['world20'];old=d['old45']['projection']
    targets=[(i,d['master']['pet_flag_1_field_projections'][i]) for i in d['prev']['remaining_gap_row_indices']]
    assert len(targets)==67 and len({t['template_id'] for _,t in targets})==67
    setup=r40.kv(m['setup.cf'],b'=')
    for key,val in ((b'enemyfile','enemy.txt'),(b'enemybasefile','enemybase.txt'),(b'groupfile','group1.txt'),(b'encountfile','encount.txt')):
        v=r40.one(setup,key)[1].decode('ascii');assert v==val or v.endswith('/'+val),(key,v)
    for n in TABLES:
        pin=w['source_files'].get(n) or p['verified_original_archive_members'][n]
        assert r40.sha(m['data/'+n])==pin['sha256'],n
    enc=unique(r40.rows(m['data/encount.txt'],33,0),0)
    assert len(enc)==660
    area_slots=collections.defaultdict(list)
    for aid,(line,a) in enc.items():
        for s in range(10):
            gid,gw=r40.num(a[10+s]),r40.num(a[20+s])
            if gid>=0 and gw>0:
                area_slots[gid].append([aid,line,r40.num(a[1]),s,gw])
    groups={}
    for f,n in [('group1.txt',1257),('group.txt',1220)]:
        groups[f]=unique(r40.rows(m['data/'+f],24,1),1)
        assert len(groups[f])==n,f
    pairs=[('enemybase.txt','enemy.txt',2087),('enemybase2.txt','enemy2.txt',1494)]
    instances={}; bases={}
    for bn,en,n in pairs:
        bases[bn]={x[1]:x for x in p['source_rows'][bn]}
        width=34 if en=='enemy.txt' else 33
        assert p['verified_original_archive_members'][en]['field_counts']=={str(width):n}
        raw=unique(r40.rows(m['data/'+en],width,3),3)
        assert len(raw)==n and all(len(a)==width for _,a in raw.values()),en
        prior={x[1]:x for x in p['source_rows'][en]}
        assert prior.keys()==raw.keys() and all(prior[k][2]==int(a[4]) for k,(_,a) in raw.items())
        instances[en]=raw
    records=[]
    target_ids={t['template_id'] for _,t in targets}
    for i,t in targets:
        tid=t['template_id'];item=dict(tw75_row_index=i,template_id=tid,name=t['name'],graphic=t['graphic'],row_sha256=t['row_sha256'],source_pairs=[])
        for bn,en,_ in pairs:
            b=bases[bn].get(tid)
            match='ABSENT' if b is None else 'EXACT_ROW' if b[16]==t['row_sha256'] else 'SAME_ID_DIFFERENT_ROW'
            inst={eid:dict(instance_id=eid,physical_line=line,pet_flag=int(a[13]),level=r40.level(a),raw_level_fields=list(map(int,a[5:7]))) for eid,(line,a) in instances[en].items() if int(a[4])==tid}
            pair=dict(base=bn,enemy=en,match=match,base_row_sha256=b[16] if b else None,base_pet_flag=b[3] if b else None,instances=list(inst.values()),group_variants=[])
            for gn,gt in groups.items():
                refs=[]
                for gid,(line,a) in gt.items():
                    for slot in range(10):
                        eid,ew=r40.num(a[4+slot]),r40.num(a[14+slot])
                        if eid not in inst:continue
                        refs.append(dict(group_id=gid,group_line=line,slot=slot,enemy_id=eid,enemy_weight=ew,positive_area_slots=area_slots[gid] if ew>0 else []))
                positive=sum(len(x['positive_area_slots']) for x in refs)
                double=sum(len(x['positive_area_slots']) for x in refs if b and b[3]==1 and inst[x['enemy_id']]['pet_flag']==1)
                lv1=sum(len(x['positive_area_slots']) for x in refs if b and b[3]==1 and inst[x['enemy_id']]['pet_flag']==1 and inst[x['enemy_id']]['level'][0]<=1<=inst[x['enemy_id']]['level'][1])
                selected=bn=='enemybase.txt' and gn=='group1.txt'
                if selected and match=='EXACT_ROW':
                    assert (positive,double,lv1)==tuple(old['claimed_tw75_rows'][i][k] for k in ('positive_route_count','double_pet_flag_route_count','lv1_double_flag_route_count'))
                pair['group_variants'].append(dict(group=gn,configuration='SELECTED' if selected else 'ALTERNATE_NOT_SELECTED',group_memberships=refs,positive_routes=positive,double_flag_routes=double,lv1_double_flag_routes=lv1))
            item['source_pairs'].append(pair)
        records.append(item)
    # Scan numeric tokens only, never publish raw commercial text.
    # Shop field tokens are lexical matches until loader namespace verified.
    all_instances=collections.defaultdict(list)
    for x in records:
        for pair in x['source_pairs']:
            if pair['base']!='enemybase.txt':continue
            for ins in pair['instances']:
                all_instances[ins['instance_id']].append(x['template_id'])
    files=[]
    char=d['char01'];known={x[0]:x for x in char['source_files']}
    for f in NPCS:
        raw=m['data/npc/'+f];k=known[f];assert (len(raw),r40.sha(raw))==(k[1],k[2])
        creates=[dict(path=x[0],ordinal=x[1],block_sha256=x[4],floor=x[5],template=x[11]) for x in char['create_rows'] if any(v[0]==f for v in x[-1])]
        matches=[];keys=collections.Counter()
        for line_no,line in enumerate(raw.splitlines(),1):
            line=line.strip()
            if not line or line.startswith(b'#'):continue
            found=re.match(rb'^([A-Za-z_][A-Za-z_0-9 ]{0,40})\s*[:=]\s*(.*)$',line)
            if found:
                key=found[1].decode('ascii').strip();val=found[2]
            else:
                key='UNKEYED';val=line
            keys[key]+=1
            nums=[int(x) for x in re.findall(rb'(?<![0-9])-?[0-9]+(?![0-9])',val)]
            ins=[n for n in nums if n in all_instances]
            tids=[n for n in nums if n in target_ids]
            if ins or tids:
                # GetPet syntax is source-defined but actual award, conditions,
                # and even active NPC deployment remain unverified.
                matches.append(dict(line=line_no,key=key,source_line_sha256=r40.sha(line),matching_instance_tokens=ins,matching_template_tokens=tids,qualification='GETPET_INSTANCE_LITERAL_CANDIDATE' if key.lower()=='getpet' and re.fullmatch(rb'[0-9, \t]+',val) else 'NUMERIC_LEXICAL_MATCH_NAMESPACE_UNVERIFIED'))
        files.append(dict(path=f,source_sha256=k[2],source_bytes=k[1],create_refs=creates,key_counts=dict(keys),candidate_lines=matches))
    s=dict(target_rows=len(records),selected_exact_with_instance=sum(x['source_pairs'][0]['match']=='EXACT_ROW' and bool(x['source_pairs'][0]['instances']) for x in records),selected_with_instance=sum(bool(x['source_pairs'][0]['instances']) for x in records),alternate_exact_with_instance=sum(x['source_pairs'][1]['match']=='EXACT_ROW' and bool(x['source_pairs'][1]['instances']) for x in records),alternate_exact_positive_double_templates=sum(any(p['match']=='EXACT_ROW' and v['configuration']=='ALTERNATE_NOT_SELECTED' and v['double_flag_routes'] for p in x['source_pairs'] for v in p['group_variants']) for x in records),npc_member_count=len(files),npc_candidate_lines=sum(len(f['candidate_lines']) for f in files))
    return dict(records=records,npc_source_files=files,summary=s,official_acquisition_verified=False,official_species_count=None,runtime_executed=False,alternate_config_deployed=False)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);a=ap.parse_args()
    d=load();inv={x['path']:x for x in d['r18']['all_server_occurrences']}
    names=TABLES+['npc/'+n for n in NPCS]
    sparse.EXPECTED={'setup.cf':r40.PINS['setup.cf'],**{'data/'+k:(inv[k]['size'],inv[k]['sha256']) for k in names}}
    receipt={}
    with tempfile.TemporaryDirectory(prefix='pet50-private-') as tmp:
        data=sparse.acquire(Path(tmp),receipt,'unar')
        projection=derive(d,data)
    out=dict(schema='stoneage.pet50.original_alternate_acquisition.r1',scope='PRESERVED_MIXED25_NOT_OFFICIAL_DEPLOYMENT',input_git_blobs={k:s for k,(_,s) in PINS.items()},original_member_count=len(data),member_receipt=receipt,projection=projection,original_payload_published=False)
    raw=json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    a.output.write_text(raw,encoding='utf-8')
    print('PET50_SUMMARY',json.dumps(projection['summary'],ensure_ascii=False))
    for x in projection['records']:
        print('PET50_ROW',json.dumps(dict(i=x['tw75_row_index'],id=x['template_id'],name=x['name'],pairs=[dict(base=p['base'],match=p['match'],instances=p['instances'],routes=[(v['group'],v['positive_routes'],v['double_flag_routes'],v['lv1_double_flag_routes']) for v in p['group_variants']]) for p in x['source_pairs']]),ensure_ascii=False,separators=(',',':')))
    for f in projection['npc_source_files']:
        print('PET50_NPC',json.dumps(f,ensure_ascii=False,separators=(',',':')))
    print('PET50_CUSTODY',json.dumps(dict(headers=receipt['headers_visited'],requests=receipt['range_requests'],bytes=receipt['actual_range_bytes'],members=receipt['members']),ensure_ascii=False,separators=(',',':')))
    print('PET50_REPORT',len(raw.encode()),r40.sha(raw.encode()),r40.git_blob(raw.encode()))
if __name__=='__main__':main()
