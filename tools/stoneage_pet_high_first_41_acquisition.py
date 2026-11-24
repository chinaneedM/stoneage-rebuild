"""PET41: bounded original mixed25 pet acquisition census and quiz award replay."""
import argparse, collections, json, re, tempfile
from pathlib import Path
from tools import stoneage_pet_high_first_40_acquisition as r40
from tools import stoneage_preserved_item_shop_r44 as sparse

ROOT=Path(__file__).resolve().parents[1]
GUIDE=ROOT/'research/pets/PET-HIGH-FIRST-19C-QUEST-AND-GIFT-WITNESSES-R1.json'
BASES=('enemybase.txt','enemy.txt','group1.txt','encount.txt')
PREFIXES=('npc/quiz/','npc/giiru/event/sink/')
def ascii_value(raw):
    return raw.decode('ascii','strict')
def source_id(a,i):
    return r40.num(a[i])
def derive(members,guide,selected):
    data={k.removeprefix('data/'):v for k,v in members.items()}
    setup=r40.kv(data['setup.cf'],b'=')
    for k,v in zip((b'enemybasefile',b'enemyfile',b'groupfile',b'encountfile'),BASES):
        assert r40.one(setup,k)[1].endswith(b'/'+v.encode()) or r40.one(setup,k)[1]==v.encode()
    # All source-specific graphic candidates, never a TW1 identity admission test.
    r40.GRAPHICS={t['graphic'] for g in guide['rows'] for t in g['templates']}
    table=r40.tables(*(data[k] for k in BASES),'cp950')
    ti=r40.idx(r40.rows(data['enemybase.txt'],56,6),6)
    ei=r40.idx(r40.rows(data['enemy.txt'],34,3),3)
    candidates=collections.defaultdict(list)
    for g in guide['rows']:
        for t in g['templates']:
            candidates[t['graphic']].append({'guide_pos':g['pos'],'guide_name':g['source_name'],'comparison_template_id':t['id'],'claim':g['claim']})
    rows=[]
    for t in table['templates']:
        route=[v for v in table['routes'] if v['template']==t['id']]
        eligible=[v for v in route if v['instance_pet_flag']==v['template_pet_flag']==1]
        lv1=[v for v in eligible if v['level'][0]<=1<=v['level'][1]]
        rows.append({'template':t,'guide_graphic_candidates':candidates[t['graphic']],
          'positive_routes':len(route),'double_pet_flag_routes':len(eligible),
          'lv1_routes':lv1,'floor_ids':sorted({v['floor'] for v in eligible})})
    creations=[]
    for p in selected:
        if not p.endswith('.create'):continue
        raw=data[p]
        for m in re.finditer(rb'(?ms)^\{\s*\r?\n(.*?)^\}\s*$',raw):
            d=r40.kv(m[1],b'=')
            if not d.get(b'enemy') or not d.get(b'floorid') or not d.get(b'borncorner'):continue
            v=r40.one(d,b'enemy')[1]
            match=re.search(rb'(?:^|\|)file:([^|\s]+)',v)
            if not match:continue
            target='npc/'+ascii_value(match[1])
            if target not in selected:continue
            creations.append({'path':p,'line':raw[:m.start()].count(b'\n')+1,'target':target,
              'floor':r40.num(r40.one(d,b'floorid')[1]),
              'corner':list(map(r40.num,r40.one(d,b'borncorner')[1].split(b',')))})
    awards=[]
    for p in selected:
        if p.endswith('.create'):continue
        raw=data[p]
        lines=raw.splitlines()
        for i,line in enumerate(lines):
            m=re.fullmatch(rb'\s*GetPet\s*:\s*(\d+)\s*',line,re.I)
            if not m:continue
            aid=int(m[1])
            start=next((n for n in range(i,-1,-1) if re.match(rb'\s*EventNo\s*:',lines[n],re.I)),None)
            end=next((n for n in range(i+1,len(lines)) if re.fullmatch(rb'\s*EventEnd\s*',lines[n],re.I)),None)
            d=r40.kv(b'\n'.join(lines[start:end+1])) if start is not None and end is not None else {}
            fields={}
            for k in (b'eventno',b'type',b'event',b'endsetflg',b'getitem',b'delitem',b'delpet'):
                if k in d:fields[k.decode()]=[ascii_value(v) for _,v in d[k]]
            result={'path':p,'line':i+1,'award_instance_id':aid,'block_start':None if start is None else start+1,
                    'block_end':None if end is None else end+1,'fields':fields,
                    'create_references':[c for c in creations if c['target']==p],
                    'instance_matches':len(ei.get(aid,[]))}
            if len(ei.get(aid,[]))==1:
                el,e=ei[aid][0];tid=source_id(e,4)
                result.update(instance={'line':el,'id':aid,'template_id':tid,'name':e[0].decode('cp950'),'level':r40.level(e),'pet_flag':source_id(e,13)},template_matches=len(ti.get(tid,[])))
                if len(ti.get(tid,[]))==1:
                    bl,b=ti[tid][0];graphic=source_id(b,36)
                    result['template']={'line':bl,'id':tid,'name':b[0].decode('cp950'),'graphic':graphic,'pet_flag':source_id(b,37),
                    'elements':list(map(r40.num,b[15:19])),'base':list(map(r40.num,b[9:13])),'initnum':source_id(b,7),'lvup':ascii_value(b[8]),'skill_slots':[r40.num(v) if v else None for v in b[25:32]]}
                    result['guide_graphic_candidates']=candidates.get(graphic,[])
            awards.append(result)
    return {'table_counts':table['table_counts'],'guide_rows':len(guide['rows']),
      'candidate_graphic_count':len(r40.GRAPHICS),'capture_candidates':rows,'award_commands':awards,
      'map_bytes_read':False,'actual_awards_verified':False,'runtime_executed':False}
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    inv=json.loads(r40.R18.read_bytes());by={r['path']:r for r in inv['all_server_occurrences']}
    selected=sorted(k for k in by if k.startswith(PREFIXES) and not k.lower().endswith('.bak'))
    assert len(selected)==26,selected
    sparse.EXPECTED={ 'setup.cf':r40.PINS['setup.cf'], **{'data/'+k:(by[k]['size'],by[k]['sha256']) for k in (*BASES,*selected)}}
    receipt={}
    with tempfile.TemporaryDirectory(prefix='pet41-private-') as work:
        members=sparse.acquire(Path(work),receipt,'unar')
        projection=derive(members,json.loads(GUIDE.read_bytes()),selected)
    out={'schema':'stoneage.pet41.mixed25.award_capture.r1','scope':'PRESERVED_MIXED25_NOT_OFFICIAL_DEPLOYMENT',
      'source_inventory_blob':r40.git_blob(r40.R18.read_bytes()),'guide_blob':r40.git_blob(GUIDE.read_bytes()),
      'original_member_count':len(members),'member_receipt':receipt,'projection':projection,
      'original_payload_published':False,'official_deployment_verified':False}
    raw=json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n';a.output.write_text(raw)
    print('PET41_META',json.dumps({k:v for k,v in out.items() if k not in ('projection','member_receipt')},ensure_ascii=False,separators=(',',':')))
    print('PET41_CUSTODY',json.dumps({k:v for k,v in receipt.items() if k!='range_receipts'},ensure_ascii=False,separators=(',',':')))
    print('PET41_RANGES',json.dumps(receipt['range_receipts'],ensure_ascii=False,separators=(',',':')))
    for k,v in projection.items():
        if isinstance(v,list):
            for row in v:print('PET41_ROW',k,json.dumps(row,ensure_ascii=False,separators=(',',':')))
        else:print('PET41_VALUE',k,json.dumps(v,ensure_ascii=False,separators=(',',':')))
    print('PET41_REPORT_SHA256',r40.sha(raw.encode()))
if __name__=='__main__':main()
