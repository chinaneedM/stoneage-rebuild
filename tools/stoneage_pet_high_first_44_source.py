"""PET44: reaccess only the four MESSAGE reward scripts; publish derived control metadata."""
import argparse, collections, json, re, tempfile, urllib.request
from pathlib import Path
from tools import stoneage_pet_high_first_40_acquisition as r40
from tools import stoneage_preserved_item_shop_r44 as sparse
from tools.stoneage_pet_high_first_43_source import SOURCE, PINS
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'research/pets'
PATHS=['jaruga/event/oev_ed1','jaruga/event/oev_edb','sainasu/event/oev_edc','sainasu/event/oev_edd']
def load(path,sha):
    raw=path.read_bytes()
    assert r40.git_blob(raw)==sha,path
    return json.loads(raw)
def code_semantics():
    name='src/npc/npc_exchangeman.c'
    with urllib.request.urlopen(SOURCE+name,timeout=45) as resp:
        raw=resp.read(2_000_001)
    assert len(raw)<=2_000_000 and r40.git_blob(raw)==PINS[name]
    lines=raw.splitlines()
    def bounded(lo,hi,tokens):
        segment=b'\n'.join(lines[lo-1:hi])
        for token in tokens:assert token in segment,(lo,hi,token)
    bounded(367,475,[b'"NomalMsg"',b'"NomalWindowMsg"',b'#ifdef _NEWEVENT',b'"NomalWindowMsg1"',b'WINDOW_BUTTONTYPE_NEXT',b'NPC_AcceptDel( meindex, talker,0)'])
    bounded(2342,2440,[b'case 99:',b'"NomalWindowMsg1"',b'"NomalWindowMsg2"',b'"NomalWindowMsg%d"',b'WINDOW_BUTTONTYPE_NEXT',b'NPC_AcceptDel( meindex, talker,0)'])
    bounded(3210,3217,[b'"GetPet"',b'NPC_EventAddPet( meindex, talker, buff2,1)',b'return FALSE'])
    bounded(3279,3291,[b'"GetRandItem"',b'rand_j++',b'NPC_RandItemGet( meindex, talker, rand_j, buff2);'])
    bounded(3390,3477,[b'CHAR_MAXPETHAVE',b'i = rand()%i + 1;',b'ENEMY_createPetFromEnemyIndex',b'CHAR_ENDEVENT'])
    rand_start=next(i for i,x in enumerate(lines) if x.startswith(b'BOOL NPC_RandItemGet(int meidex,'))
    rand_end=next(i for i in range(rand_start+1,len(lines)) if lines[i]==b'}')
    item=b'\n'.join(lines[rand_start:rand_end+1])
    for token in (b'randitem = rand()%rand_j;',b'if(randitem == 0) randitem = rand_j;',b'ITEM_makeItemAndRegist',b'CHAR_addItemSpecificItemIndex',b'return FALSE'):
        assert token in item,token
    return {'source_commit':'1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56','git_blob':PINS[name],
        'window_primary_only':'DIRECT_ACCEPTDEL_BEFORE_DISPLAY_IN_LATER_CODE',
        'window_secondary_with_NEWEVENT':'NEXT_WINDOW_CALLBACK_CASE_99_CAN_ACCEPTDEL',
        'acceptdel_reward_order':['GetPet','GetRandItem','GetItem'],
        'pet_failure_returns_before_item':True,'rand_item_return_checked_by_acceptdel':False,
        'random_item_selection':'RAND_MODULO_LIST_LENGTH_ZERO_MAPS_TO_LAST',
        'random_pet_selection':'RAND_MODULO_LIST_LENGTH_ONE_BASED','runtime_executed':False,'official_same_deployment_verified':False}
def derive(members):
    old=load(P/'PET-HIGH-FIRST-43-ORIGINAL-EXCHANGE-SEMANTICS-R1.json','8ede61a53c670a883bb7824e1d5f410d0b76463a')
    prior=load(P/'PET-HIGH-FIRST-42-ORIGINAL-MEMBER-REPLAY-R1.json','779077c98b745f6045733d4ba1410768e989f73e')
    previous={s['path']:s for s in old['projection']['scripts']}
    blocks={s['path']:s['commands'] for s in prior['scripts']}
    rows=[]
    for path in PATHS:
        raw=members['data/npc/'+path];s=previous[path]
        assert r40.sha(raw)==s['script_sha256']
        lines=raw.splitlines()
        (c,)=s['commands'];(p,)=blocks[path]
        i=c['line']-1
        assert p['line']==c['line'] and p['block_type']==c['block_type']=='MESSAGE'
        start=next(j for j in range(i,-1,-1) if re.match(rb'\s*EventNo\s*:',lines[j],re.I))
        end=next(j for j in range(i,len(lines)) if lines[j].strip().lower()==b'eventend')
        assert end+1==p['source_block_end']
        block=r40.kv(b'\n'.join(lines[start:end+1]))
        assert r40.one(block,b'type')[1].upper()==b'MESSAGE'
        for k,v in c['fields'].items():assert [x.decode('ascii') for _,x in block[k.encode()]]==v,(path,k)
        assert [int(n) for n in r40.one(block,b'getpet')[1].split(b',')]==c['numeric_literals']
        keys=sorted(k for k in block if re.fullmatch(rb'nomal(?:window)?msg[0-9]*',k))
        window={k.decode():[{'line':start+n,'value_bytes':len(v),'value_sha256':r40.sha(v)} for n,v in block[k]] for k in keys}
        assert b'nomalmsg' not in block
        present=b'nomalwindowmsg' in block
        follow=b'nomalwindowmsg1' in block
        route=('LATER_NEWEVENT_CALLBACK_CANDIDATE' if follow else 'LATER_DIRECT_ACCEPTDEL_CANDIDATE') if present else 'NO_QUALIFIED_WINDOW_ROUTE'
        items=[int(n) for n in r40.one(block,b'getranditem')[1].split(b',')]
        rows.append({'path':path,'script_sha256':s['script_sha256'],'block_start':start+1,'block_end':end+1,'getpet_line':i+1,'window_field_fingerprints':window,
            'later_code_route_candidate':route,'primary_window_present':present,'secondary_window_present':follow,
            'pet_slots':c['numeric_literals'],'random_item_slots':items,
            'pet_slot_counts':dict(collections.Counter(c['numeric_literals'])),'item_slot_counts':dict(collections.Counter(items)),
            'condition_fields':c['fields'],'actual_award_verified':False,'official_probability_verified':False})
    return rows
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    semantics=code_semantics()
    inv={r['path']:r for r in json.loads(r40.R18.read_bytes())['all_server_occurrences']}
    sparse.EXPECTED={'data/npc/'+p:(inv['npc/'+p]['size'],inv['npc/'+p]['sha256']) for p in PATHS}
    receipt={}
    with tempfile.TemporaryDirectory(prefix='pet44-private-') as work:
        members=sparse.acquire(Path(work),receipt,'unar')
        rows=derive(members)
    out=dict(schema='stoneage.pet44.window_reward_controls.r1',scope='SAVED_MIXED25_AND_FIXED_LATER_CODE_NOT_OFFICIAL_DEPLOYMENT',original_member_count=len(members),member_receipt=receipt,code_semantics=semantics,rows=rows,original_payload_published=False,runtime_executed=False,official_deployment_verified=False)
    raw=json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n';a.output.write_text(raw,encoding='utf-8')
    print('PET44_META',json.dumps({k:v for k,v in out.items() if k not in ('member_receipt','rows')},ensure_ascii=False,separators=(',',':')))
    print('PET44_CUSTODY',json.dumps({k:v for k,v in receipt.items() if k!='range_receipts'},ensure_ascii=False,separators=(',',':')))
    print('PET44_RANGES',json.dumps(receipt['range_receipts'],ensure_ascii=False,separators=(',',':')))
    for row in rows:print('PET44_ROW',json.dumps(row,ensure_ascii=False,separators=(',',':')))
    print('PET44_REPORT_SHA256',r40.sha(raw.encode()))
if __name__=='__main__':main()
