"""Independent PET42 original-member receipt and cross-carrier replay."""
import json, urllib.request
from pathlib import Path
from tools import stoneage_pet_high_first_40_acquisition as r40
from tools.stoneage_pet_high_first_42_verify import verify as verify_index
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'research/pets'
def verify():
    index=verify_index()
    raw=(P/'PET-HIGH-FIRST-42-ORIGINAL-MEMBER-REPLAY-R1.json').read_bytes()
    assert len(raw)==82025 and r40.sha(raw)=='d0139127c20357f051ceb45390bb2185d5d8ea9972677ac864337cdfde1ab4a0'
    assert r40.git_blob(raw)=='779077c98b745f6045733d4ba1410768e989f73e'
    d=json.loads(raw);r=d['member_receipt']
    assert len(r['members'])==d['original_member_count']==26
    assert r['headers_visited']==7954 and r['range_requests']==len(r['range_receipts'])==184
    assert r['actual_range_bytes']==sum(x['bytes'] for x in r['range_receipts'])==12013836 and not r['whole_archive_or_parts_rehashed']
    inv={x['path']:(x['size'],x['sha256']) for x in json.loads(r40.R18.read_bytes())['all_server_occurrences']}
    members={}
    for x in r['members']:
        path=x['path'].split('/SA2.5服務端/gmsv/',1)[1]
        assert path not in members and not x['flags']&(1|2|4|16) and x['extractor']=='unar'
        assert (x['bytes'],x['sha256'])==(r40.PINS.get(path) or inv[path.removeprefix('data/')])
        members[path]=x
    assert set(members)=={'setup.cf','data/enemy.txt','data/enemybase.txt',*('data/npc/'+s['path'] for s in index['scripts'])}
    cross_raw=(P/'PET-HIGH-FIRST-42-EXACT-TEMPLATE-CROSSWALK-R1.json').read_bytes()
    assert r40.git_blob(cross_raw)=='c6667a6190283f4ec3ad3813c570357b18906ccc'
    cross=json.loads(cross_raw);t_raw=(P/'PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json').read_bytes()
    assert r40.git_blob(t_raw)==cross['pins']['tw75']=='fec03646d7c7e4e287f9347c306119cc626d6abf'
    assert r40.git_blob((P/'PET-HIGH-FIRST-42-REWARD-INSTANCE-INDEX-R1.json').read_bytes())==cross['pins']['reward_index']
    ts=json.loads(t_raw)['pet_flag_1_field_projections']
    assert len(index['rows'])==len(d['rows'])==len(cross['rows'])==36
    for i,(a,b,c) in enumerate(zip(index['rows'],d['rows'],cross['rows'])):
        assert (a['award_instance_id'],a['template_id'],a['graphic'])==(b['award_instance_id'],b['template_id'],b['graphic'])==(c['award_instance_id'],c['template_id'],c['graphic'])
        assert b['instance_level']==[1,1] and b['instance_pet_flag']==b['template_pet_flag']==a['template_pet_flag']==1
        assert b['instance_line']>=a['instance_nonempty_row'] and b['template_line']>=a['template_nonempty_row']
        t=ts[c['tw75_row_index']]
        assert c['reward_row_index']==i and (t['template_id'],t['graphic'],t['row_sha256'])==(a['template_id'],a['graphic'],a['template_row_fields_sha256'])
        assert t['row_sha256']==c['shared_template_row_sha256'] and t['name']==b['template_name']==c['template_original_name']
        assert c['tw10_candidate']==a['tw10_candidate']
        assert c['tw10_name_exact']==(None if c['tw10_candidate'] is None else c['tw10_candidate']['client_name']==t['name'])
        assert not c['official_same_deployment_verified']
    assert cross['counts']=={'exact_template_row_joins':36,'tw10_graphic_only':33,'tw10_exact_name':31,'tw10_name_conflicts':2,'no_tw10_graphic':3}
    assert {c['template_original_name'] for c in cross['rows'] if c['tw10_candidate'] is None}=={'瑪蕾菲雅','迪歐','魯烏'}
    assert {c['template_original_name'] for c in cross['rows'] if c['tw10_name_exact'] is False}=={'卡拉寶斯','愛麗兒隊的加美'}
    assert len(d['scripts'])==len(index['scripts'])==23
    for a,b in zip(index['scripts'],d['scripts']):
        assert a['path']==b['path'] and members['data/npc/'+a['path']]['sha256']==a['script_sha256']
        assert [c['line'] for c in b['commands']]==a['source_lines']
        assert [n for c in b['commands'] for n in c['numeric_literals']]==a['ordered_numeric_literals']
        for c in b['commands']:
            (block,)=[v for v in a['blocks'] if v['ordinal']==c['block_ordinal']]
            assert block['type']==c['block_type'] and block['type_line']<c['line']<c['source_block_end']
            assert [int(x) for x in c['raw_numeric_tokens'].split(',')]==c['numeric_literals']
    s={x['path']:x['commands'] for x in d['scripts']}
    assert [c['numeric_literals'] for c in s['seimu/event/event02_1']]==[[93],[341]]
    assert s['seimu/event/event02_1'][0]['fields']['event']==['LV>0&PET=25-221*1&PET=25-222*1&ITEM=2607&NOWEV=35']
    assert s['seimu/event/event02_1'][1]['fields']['delpet']==['EVDEL']
    for path,cond,ids in (
        ('jaruga/event/oev_ed1','LV>0&ITEM=2564',[358,96,328,309,365]),
        ('jaruga/event/oev_edb','LV>0&ITEM=2564&ENDEV=2',[338,360,366,482,482,78]),
        ('sainasu/event/oev_edc','LV>0&ITEM=2587&ENDEV=17',[48,94,350,482]),
        ('sainasu/event/oev_edd','LV>0&ITEM=2587',[76,309,361,96])):
        (c,)=s[path];assert c['block_type']=='MESSAGE' and c['fields']['event']==[cond] and c['numeric_literals']==ids
    assert not any((d['runtime_executed'],d['actual_awards_verified'],d['original_payload_published'],cross['official_deployment_verified'])) and cross['official_species_count'] is None
    # Later fixed implementation demonstrates a MESSAGE path may call reward logic.
    # This is not proof of same-build runtime or probability.
    url='https://raw.githubusercontent.com/gavinlinasd/StoneAge/1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56/gmsv/src/npc/npc_exchangeman.c'
    with urllib.request.urlopen(url,timeout=45) as resp: code=resp.read(2_000_001)
    assert len(code)<=2_000_000 and r40.git_blob(code)=='5d74290ed6f27163e0698b4375d5dc5e187c77c4'
    msg=code[code.index(b'strstr( buf2, "MESSAGE")'):];msg=msg[:msg.index(b'#ifdef _ANGEL_SUMMON')]
    assert b'"NomalMsg"' in msg and b'NPC_AcceptDel( meindex, talker, 0)' in msg
    accept=code[code.index(b'BOOL NPC_AcceptDel(int meindex,int talker,int mode )'):];accept=accept[:accept.index(b'BOOL NPC_EventAddPet(int meindex, int talker, char *buff2,int mode)')]
    assert b'"GetPet"' in accept and b'NPC_EventAddPet( meindex, talker, buff2,1)' in accept
    print('PET42 original replay: 26 verified member receipts; 36 Lv1 double-flag instances; 36 exact template fingerprints; 25 static commands. No live issue proof.')
if __name__=='__main__':verify()
