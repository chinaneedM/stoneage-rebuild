"""Derive source-local pet encounter and task award metadata. No game execution."""
import argparse, collections, hashlib, json, re, struct, tempfile, urllib.request
from pathlib import Path
from tools import stoneage_preserved_item_shop_r44 as sparse

ROOT=Path(__file__).resolve().parents[1]
R18=ROOT/'research/recovered/STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json'
PINS={
 'setup.cf':(9715,'b4936c103efb7b3cad359e5c85c7965187306883a68c0be712ece6c374e3b12d'),
 'data/map/giiru/dungeon/sikkoku/dan_3-20-09':(14444,'5317e4ee9beb285f10b59c8efeae1039d070177be66c344259a57fc6d91ef62e'),
 'data/map/giiru/dungeon/sikkoku/dan_3-20-11':(14444,'191f292e4cacf40cc77074f5a4349b66ed7da3969b321639b3b8bb9cd90d8024'),
 'data/map/king/30670':(3644,'5e7dda73a5a82dfff17c8ede6718d649bed6a06ce4192c76ccfc84a8ce7f016a'),
 'data/map/king/30689':(14444,'fcea6306a3948d08c3fd75945cd4e7c5a13dfebb573d841ef3c68fc74b25a89c'),
 'data/map/king/30692':(25644,'e379ab278e7e420662eb794c9212749a0c96b57d608a3f95a5d7344b5abe8192'),
}
NAMES=['enemybase.txt','enemy.txt','group1.txt','encount.txt','npc/king/event69_24','npc/king/event69_23.arg','npc/king/event69_alpha.create','npc/king/event69_23.template']
TIDS={31,85,86,87,315,623,663,697,711,1240,2018}
GRAPHICS={100263,100389,100390,100391,100430}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def git_blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def num(raw):return int(raw) if raw.strip() else -1
def rows(raw,min_width,idcol):
    result=[]
    for line,raw_line in enumerate(raw.splitlines(),1):
        if not raw_line.strip() or raw_line.lstrip().startswith(b'#'):continue
        a=[x.strip() for x in raw_line.split(b',')]
        if len(a)<min_width or not re.fullmatch(rb'-?\d+',a[idcol]):
            raise ValueError('unqualified source row: '+str(line))
        result.append((line,a))
    return result
def idx(rows,col):
    d=collections.defaultdict(list)
    for line,a in rows:d[num(a[col])].append((line,a))
    return d
def level(a):
    x,y=num(a[5]),num(a[6])
    if x==0:x=y
    return [min(x,y),max(x,y)]
def tables(base,enemy,group,enc,codec):
    b,e,g,c=[rows(raw,w,i) for raw,w,i in [(base,56,6),(enemy,34,3),(group,24,1),(enc,30,0)]]
    bi,ei,gi=idx(b,6),idx(e,3),idx(g,1)
    templates=[]
    for line,a in b:
        if num(a[36]) not in GRAPHICS:continue
        templates.append(dict(line=line,id=num(a[6]),name=a[0].decode(codec),graphic=num(a[36]),pet_flag=num(a[37]),elements=list(map(num,a[15:19])),base=list(map(num,a[9:13])),initnum=num(a[7]),lvup=a[8].decode('ascii'),skill_slots=[num(v) if v else None for v in a[25:32]]))
    ids={x['id'] for x in templates}
    instances=[]
    for line,a in e:
        if num(a[4]) in ids:
            instances.append(dict(line=line,id=num(a[3]),template=num(a[4]),name=a[0].decode(codec),level=level(a),pet_flag=num(a[13])))
    routes=[]
    for line,a in c:
        floor=num(a[1])
        for k,(gid,gw) in enumerate(zip(map(num,a[10:20]),map(num,a[20:30]))):
            if gid<0 or gw<=0 or len(gi.get(gid,[]))!=1:continue
            gl,gr=gi[gid][0]
            resolved=[v for v in map(num,gr[4:14]) if v>=0 and len(ei.get(v,[]))==1]
            if not resolved or len(resolved)!=len(set(resolved)):continue
            for slot,(eid,ew) in enumerate(zip(map(num,gr[4:14]),map(num,gr[14:24]))):
                if ew<=0 or len(ei.get(eid,[]))!=1:continue
                el,inst=ei[eid][0];tid=num(inst[4])
                if tid not in ids or len(bi.get(tid,[]))!=1:continue
                routes.append(dict(floor=floor,rect=list(map(num,a[2:6])),encounter_index=num(a[0]),encounter_line=line,group=gid,group_line=gl,group_slot=k,enemy=eid,enemy_line=el,enemy_slot=slot,template=tid,level=level(inst),instance_pet_flag=num(inst[13]),template_pet_flag=num(bi[tid][0][1][37]),weights=[gw,ew],group_item_gates=list(map(num,gr[2:4])),event_fields=list(map(num,a[30:33])),encounter_rate_fields=list(map(num,a[6:8]))))
    return dict(table_counts=[len(b),len(e),len(g),len(c)],widths=[dict(collections.Counter(len(a) for _,a in z)) for z in (b,e,g,c)],templates=templates,instances=instances,routes=routes)
def kv(raw,delim=b':'):
    d=collections.defaultdict(list)
    for line,s in enumerate(raw.splitlines(),1):
        if s.lstrip().startswith(b'#') or delim not in s:continue
        k,v=s.split(delim,1)
        d[k.strip().lower()].append((line,v.strip()))
    return d
def one(d,key):
    vals=d[key]
    if len(vals)!=1:raise ValueError('missing or duplicate field '+repr(key))
    return vals[0]
def quest(event,create,battle,template):
    d=kv(event);award_line,award=one(d,b'getpet')
    block=event.splitlines()
    # Bound exact event block containing GetPet.
    start=max(i for i in range(award_line) if block[i].strip().startswith(b'EventNo:'))
    end=next(i for i in range(award_line-1,len(block)) if block[i].strip()==b'EventEnd')
    q=kv(b'\n'.join(block[start:end+1]))
    c=[]
    for m in re.finditer(rb'(?ms)^\{\s*\r?\n(.*?)^\}\s*$',create):
        dd=kv(m[1],b'=')
        if not dd.get(b'enemy'):continue
        val=one(dd,b'enemy')[1]
        if b'king/event69_24' not in val and b'king/event69_23.arg' not in val:continue
        c.append(dict(line=create[:m.start()].count(b'\n')+1,floor=num(one(dd,b'floorid')[1]),corner=list(map(num,one(dd,b'borncorner')[1].split(b','))),graphic=num(one(dd,b'graphicname')[1]),argument=val.decode('ascii')))
    bt=kv(battle);dt=kv(template,b'=')
    assert len(c)==2
    return dict(award_id=num(award),award_line=award_line,block_start=start+1,block_end=end+1,condition=one(q,b'event')[1].decode('ascii'),type=one(q,b'type')[1].decode('ascii'),completion_flag=num(one(q,b'endsetflg')[1]),pet_full_message_present=bool(q.get(b'petfullmsg')),create=c,battle=dict(dieact=num(one(bt,b'dieact')[1]),warp=[num(one(bt,k)[1]) for k in (b'warpfl',b'warpx',b'warpy')],enemy_ids=list(map(num,one(bt,b'enemyno')[1].split(b','))),functionset=one(dt,b'functionset')[1].decode('ascii')))
def map_header(raw,path,codec):
    assert raw[:6]==b'LS2MAP'
    floor=struct.unpack_from('>H',raw,6)[0];w,h=struct.unpack_from('>HH',raw,40)
    assert len(raw)==44+4*w*h
    return dict(path=path,floor=floor,width=w,height=h,name=raw[8:39].split(b'\0',1)[0].decode(codec),sha256=sha(raw),header_sha256=sha(raw[:44]),planes_sha256=sha(raw[44:]))
def project(sources,codec,base_name,enemy_name):
    setup=kv(sources['setup.cf'],b'=')
    selections={k.decode():one(setup,k)[1].decode('ascii') for k in (b'enemyfile',b'enemybasefile',b'groupfile',b'encountfile',b'npcdir')}
    for k,v in {'enemyfile':enemy_name,'enemybasefile':base_name,'groupfile':'group1.txt','encountfile':'encount.txt'}.items():assert selections[k].endswith('/'+v) or selections[k]==v
    q=quest(*[sources['data/npc/king/'+p] for p in ('event69_24','event69_alpha.create','event69_23.arg','event69_23.template')])
    d=tables(*[sources['data/'+p] for p in (base_name,enemy_name,'group1.txt','encount.txt')],codec)
    match=[x for x in d['instances'] if x['id']==q['award_id']]
    assert len(match)==1
    q['award_instance']=match[0]
    match=[x for x in d['templates'] if x['id']==q['award_instance']['template']]
    assert len(match)==1
    q['award_template']=match[0]
    return dict(config=selections,quest=q,maps=[map_header(raw,k,codec) for k,raw in sorted(sources.items()) if k.startswith('data/map/')],**d)
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    inv=json.loads(R18.read_bytes());by={r['path']:r for r in inv['all_server_occurrences']}
    sparse.EXPECTED={**PINS,**{'data/'+k:(by[k]['size'],by[k]['sha256']) for k in NAMES}}
    receipt={}
    with tempfile.TemporaryDirectory(prefix='pet40-private-') as work:
        data=sparse.acquire(Path(work),receipt,'unar')
        out=dict(schema='stoneage.pet40.mixed25.member_replay.r1',scope='SAVED_MIXED25_NOT_OFFICIAL_DEPLOYMENT',source_inventory_git_blob=git_blob(R18.read_bytes()),original_member_count=len(data),member_receipt=receipt,projection=project(data,'cp950','enemybase.txt','enemy.txt'),original_payload_published=False,runtime_executed=False,official_deployment_verified=False)
    raw=json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n';a.output.write_text(raw)
    # Log small bounded metadata separately, never raw files or dialogue.
    print('PET40_SUMMARY',json.dumps({k:v for k,v in out.items() if k not in ('projection','member_receipt')},ensure_ascii=False,separators=(',',':')))
    print('PET40_CUSTODY',json.dumps({k:v for k,v in receipt.items() if k!='range_receipts'},ensure_ascii=False,separators=(',',':')))
    print('PET40_RANGE_RECEIPTS',json.dumps(receipt.get('range_receipts',[]),ensure_ascii=False,separators=(',',':')))
    for k,v in out['projection'].items():
        if isinstance(v,list):
            for row in v:print('PET40_ROW',k,json.dumps(row,ensure_ascii=False,separators=(',',':')))
        else:print('PET40_VALUE',k,json.dumps(v,ensure_ascii=False,separators=(',',':')))
    print('PET40_REPORT_SHA256',sha(raw.encode()))
if __name__=='__main__':main()
