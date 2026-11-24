"""Independent PET43 archival receipt and derived semantic verification."""
import collections,json
from pathlib import Path
from tools import stoneage_pet_high_first_40_acquisition as r40
from tools.stoneage_pet_high_first_43_source import code_semantics
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'research/pets'
def read(path,pin):
    raw=path.read_bytes();assert r40.git_blob(raw)==pin,path
    return json.loads(raw)
def main():
    raw=(P/'PET-HIGH-FIRST-43-ORIGINAL-EXCHANGE-SEMANTICS-R1.json').read_bytes()
    assert len(raw)==53236 and r40.sha(raw)=='d28e25ef06cec149c6797223aa525023230e19a97897bf594b730ca80b65b3de' and r40.git_blob(raw)=='8ede61a53c670a883bb7824e1d5f410d0b76463a'
    d=json.loads(raw);r=d['member_receipt'];p=d['projection']
    assert r['headers_visited']==7954 and r['range_requests']==len(r['range_receipts'])==186 and r['actual_range_bytes']==sum(x['bytes'] for x in r['range_receipts'])==12144908
    assert len(r['members'])==d['original_member_count']==8 and not r['whole_archive_or_parts_rehashed']
    inv={x['path']:(x['size'],x['sha256']) for x in json.loads(r40.R18.read_bytes())['all_server_occurrences']}
    members={}
    for x in r['members']:
        name=x['path'].split('/SA2.5服務端/gmsv/',1)[1]
        assert name not in members and x['extractor']=='unar' and not x['flags']&(1|2|4|16)
        assert (x['bytes'],x['sha256'])==(r40.PINS.get(name) or inv[name.removeprefix('data/')])
        members[name]=x
    assert set(members)=={'setup.cf','data/enemybase.txt','data/itemset.txt',*('data/npc/'+s['path'] for s in p['scripts'])}
    previous=read(P/'PET-HIGH-FIRST-42-ORIGINAL-MEMBER-REPLAY-R1.json','779077c98b745f6045733d4ba1410768e989f73e')
    prior={s['path']:s['commands'] for s in previous['scripts']}
    assert len(p['scripts'])==5 and sum(len(s['commands']) for s in p['scripts'])==6
    for s in p['scripts']:
        assert members['data/npc/'+s['path']]['sha256']==s['script_sha256']
        for c,b in zip(s['commands'],prior[s['path']],strict=True):
            assert (c['line'],c['block_type'],c['numeric_literals'])==(b['line'],b['block_type'],b['numeric_literals'])
            assert all(c['fields'][k]==v for k,v in b['fields'].items())
            assert c['token_multiplicity']=={str(k):v for k,v in collections.Counter(c['numeric_literals']).items()}
            assert not c['nomalmsg_present'] and c['nomalmsg_value_sha256']==[] and not c['actual_award_verified']
    s={v['path']:v['commands'] for v in p['scripts']}
    assert s['jaruga/event/oev_edb'][0]['token_multiplicity']['482']==2
    assert len(s['jaruga/event/oev_edb'][0]['numeric_literals'])==6
    assert s['jaruga/event/oev_edb'][0]['fields']['getranditem']==['255,352,769,1062,68,1063,58,68,2565,2566']
    assert s['sainasu/event/oev_edd'][0]['fields']['getranditem']==s['jaruga/event/oev_edb'][0]['fields']['getranditem']
    assert {n for v in p['scripts'] for c in v['commands'] for n in c['numeric_literals']}=={93,341,358,96,328,309,365,338,360,366,482,78,48,94,350,76,361}
    pet10=read(ROOT/'research/recovered/STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json','25a37aeb134fb180e322e7dc335029b7374452d8')
    assert [x['template_id'] for x in p['templates']]==[221,222,558,292,293]
    assert [x['name'] for x in p['templates']]==['克邦凱斯','加克拉','剋剋洛斯','剋剋洛斯','霍爾克']
    for t in p['templates']:
        (b,)=[b for b in pet10['source_rows']['enemybase.txt'] if b[1]==t['template_id']]
        assert t['graphic']==b[2] and t['pet_flag']==b[3]==1
        assert t['elements']==list(map(int,b[10:14])) and t['base']==list(map(int,b[6:10]))
        assert t['initnum']==int(b[4]) and t['lvup']==b[5] and t['skill_slots']==b[15]
    items=read(ROOT/'research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json','b91bc8335db508998f4595144ce371979ea8c849')
    assert p['configured_item_rows']==13252
    assert [(i['id'],i['name']) for i in p['items']]==[(2564,'通過證明石'),(2587,'檢查石'),(2607,'火難的戒指')]
    for i in p['items']:
        (a,)=[a for a in items['rows'] if a[0]==i['id']]
        assert i['source_body_sha256']==a[1]==a[2] and i['graphic']==a[3]==a[4]
        assert (i['cost'],i['type'],i['level'])==tuple(map(int,a[5:8]))
    assert d['code_semantics']==code_semantics()
    assert not any((d['original_payload_published'],d['runtime_executed'],d['official_deployment_verified']))
    print('PET43: 8 member receipts, 5 templates, 3 exact item rows, 6 reward controls, 17 distinct IDs; NomalMsg absent, NomalWindowMsg unresolved; no official probability.')
if __name__=='__main__':main()
