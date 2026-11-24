"""PET43: authenticate exchange templates, configured items and message reward controls."""
import argparse, collections, json, re, tempfile, urllib.request
from pathlib import Path
from tools import stoneage_pet_high_first_40_acquisition as r40
from tools import stoneage_preserved_item_shop_r44 as sparse
from tools.stoneage_itemset_schema_probe import INDEX
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'research/pets'
SOURCE='https://raw.githubusercontent.com/gavinlinasd/StoneAge/1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56/gmsv/'
PINS={'src/npc/npc_exchangeman.c':'5d74290ed6f27163e0698b4375d5dc5e187c77c4','src/char/enemy.c':'65e5a2e352253a214407f07425427f539db5e863','src/util.c':'c1e0530194839585281288750fd37a566997f812'}
PATHS=['seimu/event/event02_1','jaruga/event/oev_ed1','jaruga/event/oev_edb','sainasu/event/oev_edc','sainasu/event/oev_edd']
IDS=[221,222,558,292,293]
def code_semantics():
    code={}
    for p,sha in PINS.items():
        with urllib.request.urlopen(SOURCE+p,timeout=45) as resp:raw=resp.read(2_000_001)
        assert len(raw)<=2_000_000 and r40.git_blob(raw)==sha,p
        code[p]=raw
    n,e,u=(code[p] for p in PINS)
    # Scope each check to the actual later implementation, not forward declarations.
    def section(raw,start,end):
        x=raw[raw.index(start):];return x[:x.index(end)]
    pet=section(n,b'BOOL NPC_PetLvCheck(int meindex,int talker,char *buf,int mode)\r\n',b'int NPC_PetLvCheckType2(') if b'BOOL NPC_PetLvCheck(int meindex,int talker,char *buf,int mode)\r\n' in n else section(n,b'BOOL NPC_PetLvCheck(int meindex,int talker,char *buf,int mode)\n',b'int NPC_PetLvCheckType2(')
    for x in (b'CHAR_PETID',b'CHAR_ENDEVENT',b'CHAR_LV',b'loop = atoi( buf3)',b'loop == cnt',b'NPC_EventBigSmallLastCheck'):assert x in pet,x
    spawn=section(e,b'int ENEMY_createPetFromEnemyIndex( int charaindex, int array)',b'CharNew.data[CHAR_CRITIAL]')
    assert b'ENEMYTEMP_getEnemyTempArray( array)' in spawn and b'CHAR_PETID' in spawn and b'E_T_TEMPNO' in spawn
    add=section(n,b'BOOL NPC_EventAddPet(int meindex, int talker, char *buff2,int mode)',b'BOOL NPC_EventAddEgg(')
    for x in (b'i = rand()%i + 1',b'ENEMY_getInt( i, ENEMY_ID) == enemyid',b'ENEMY_createPetFromEnemyIndex( talker, i)'):assert x in add,x
    cmp=section(n,b'BOOL NPC_EventBigSmallLastCheck(int point1,int mypoint,int flg)',b'void NPC_MsgDisp(')
    assert b'point1 == mypoint' in cmp
    msg=section(n,b'strstr( buf2, "MESSAGE")',b'#ifdef _ANGEL_SUMMON')
    assert b'"NomalMsg"' in msg and b'NPC_AcceptDel( meindex, talker, 0)' in msg
    delete=section(n,b'BOOL NPC_AcceptDel(int meindex,int talker,int mode )',b'BOOL NPC_EventAddPet(int meindex, int talker, char *buff2,int mode)')
    for x in (b'"EVDEL"',b'getStringFromIndexWithDelim( buf5, ",",evcnt',b'NPC_PetLvCheckType2',b'NPC_EventDelPet',b'cnt == petcnt',b'NPC_EventAddPet( meindex, talker, buff2,1)'):assert x in delete,x
    assert b'BOOL getStringFromIndexWithDelim_body(' in u and b'if( i == index - 1 )' in u
    return dict(source_commit='1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56',git_blobs=PINS,predicate_namespace='CHAR_PETID_FROM_E_T_TEMPNO',reward_namespace='ENEMY_ID',equality='LEVEL_EQUALS',quantity='COUNT_OF_MATCHING_PETS',normal_pet_event_mode=0,evdel='MATCHED_COMMA_BRANCH_PET_TERMS',message_can_dispatch_reward=True,random_selection='RAND_MODULO_LIST_LENGTH_ONE_BASED',official_same_deployment_verified=False,runtime_executed=False)
def derive(members):
    old=json.loads((P/'PET-HIGH-FIRST-42-ORIGINAL-MEMBER-REPLAY-R1.json').read_bytes())
    old_scripts={s['path']:s['commands'] for s in old['scripts']}
    setup=r40.kv(members['setup.cf'],b'=')
    assert r40.one(setup,b'enemybasefile')[1].endswith(b'/enemybase.txt') or r40.one(setup,b'enemybasefile')[1]==b'enemybase.txt'
    assert all(r40.one(setup,k)[1]==b'data/itemset.txt' for k in (b'itemset3file',b'itemset4file',b'itemset5file',b'itemset6file'))
    bases=r40.idx(r40.rows(members['data/enemybase.txt'],56,6),6)
    templates=[]
    for tid in IDS:
        ((line,b),)=bases[tid]
        assert int(b[37])==1
        templates.append(dict(template_id=tid,line=line,name=b[0].decode('cp950'),graphic=int(b[36]),pet_flag=int(b[37]),elements=list(map(int,b[15:19])),base=list(map(int,b[9:13])),initnum=int(b[7]),lvup=b[8].decode('ascii'),skill_slots=[int(x) if x else None for x in b[25:32]]))
    itemrows,count=sparse.parse_items(members['data/itemset.txt']);assert count==13252
    items=[]
    for id in (2564,2587,2607):
        line,off,body,b=itemrows[id]
        items.append(dict(id=id,line=line,source_body_sha256=r40.sha(body),name=b[INDEX['name']].decode('cp950'),secretname=b[INDEX['secretname']].decode('cp950'),graphic=int(b[INDEX['imagenumber']]),cost=int(b[INDEX['cost']]),type=int(b[INDEX['type']]),level=int(b[INDEX['level']])))
    scripts=[]
    for path in PATHS:
        raw=members['data/npc/'+path];lines=raw.splitlines()
        commands=[]
        for c in old_scripts[path]:
            i=c['line']-1
            assert lines[i].strip().split(b':',1)[1].strip().decode('ascii')==c['raw_numeric_tokens']
            start=next(j for j in range(i,-1,-1) if re.match(rb'\s*EventNo\s*:',lines[j],re.I))
            block=r40.kv(b'\n'.join(lines[start:c['source_block_end']]))
            fields={}
            for k in (b'event',b'delpet',b'delitem',b'endsetflg',b'getranditem'):
                if k in block:
                    fields[k.decode()]=[v.decode('ascii') for _,v in block[k]]
            for k,v in c['fields'].items():
                if k in fields:assert fields[k]==v
            commands.append(dict(line=c['line'],block_type=c['block_type'],numeric_literals=c['numeric_literals'],fields=fields,nomalmsg_present=b'nomalmsg' in block,nomalmsg_value_sha256=[r40.sha(v) for _,v in block.get(b'nomalmsg',[])],token_multiplicity=dict(sorted(collections.Counter(c['numeric_literals']).items())),actual_award_verified=False))
        scripts.append(dict(path=path,script_sha256=r40.sha(raw),commands=commands))
    return dict(templates=templates,items=items,scripts=scripts,configured_item_rows=count)
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    semantics=code_semantics()
    inv={r['path']:r for r in json.loads(r40.R18.read_bytes())['all_server_occurrences']}
    selected=['enemybase.txt','itemset.txt',*['npc/'+p for p in PATHS]]
    sparse.EXPECTED={'setup.cf':r40.PINS['setup.cf'],**{'data/'+k:(inv[k]['size'],inv[k]['sha256']) for k in selected}}
    receipt={}
    with tempfile.TemporaryDirectory(prefix='pet43-private-') as work:
        members=sparse.acquire(Path(work),receipt,'unar')
        result=derive(members)
    out=dict(schema='stoneage.pet43.exchange_semantics.r1',scope='SAVED_MIXED25_AND_LATER_FIXED_CODE_NOT_OFFICIAL_DEPLOYMENT',original_member_count=len(members),member_receipt=receipt,code_semantics=semantics,projection=result,original_payload_published=False,runtime_executed=False,official_deployment_verified=False)
    raw=json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n';a.output.write_text(raw)
    print('PET43_META',json.dumps({k:v for k,v in out.items() if k not in ('member_receipt','projection')},ensure_ascii=False,separators=(',',':')))
    print('PET43_CUSTODY',json.dumps({k:v for k,v in receipt.items() if k!='range_receipts'},ensure_ascii=False,separators=(',',':')))
    print('PET43_RANGES',json.dumps(receipt['range_receipts'],ensure_ascii=False,separators=(',',':')))
    for k,v in result.items():
        if isinstance(v,list):
            for row in v:print('PET43_ROW',k,json.dumps(row,ensure_ascii=False,separators=(',',':')))
        else:print('PET43_VALUE',k,json.dumps(v))
    print('PET43_REPORT_SHA256',r40.sha(raw.encode()))
if __name__=='__main__':main()
