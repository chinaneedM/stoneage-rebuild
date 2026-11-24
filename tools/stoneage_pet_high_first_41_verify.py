"""Verify archived original-member custody and source-scoped PET41 catalogue links."""
import json, urllib.request
from pathlib import Path
from tools import stoneage_pet_high_first_40_acquisition as r40
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'research/pets'
def verify():
    raw=(P/'PET-HIGH-FIRST-41-MIXED25-ACQUISITION-R1.json').read_bytes()
    d=json.loads(raw);c=json.loads((P/'PET-HIGH-FIRST-41-ACQUISITION-CROSSWALK-R1.json').read_bytes())
    a=c['archive'];q=d['projection'];r=d['member_receipt']
    assert len(raw)==a['raw_json_bytes']==240995 and r40.sha(raw)==a['raw_json_sha256'] and r40.git_blob(raw)==a['derived_git_blob']
    assert a['api_zip_sha256']==a['independent_zip_sha256'] and a['conclusion']=='success'
    assert len(r['members'])==d['original_member_count']==31
    assert r['headers_visited']==7954 and r['range_requests']==len(r['range_receipts'])==184
    assert r['actual_range_bytes']==sum(x['bytes'] for x in r['range_receipts'])==12013836 and not r['whole_archive_or_parts_rehashed']
    invraw=r40.R18.read_bytes();assert r40.git_blob(invraw)==d['source_inventory_blob']
    inv={x['path']:(x['size'],x['sha256']) for x in json.loads(invraw)['all_server_occurrences']}
    members={}
    for x in r['members']:
        path=x['path'].split('/SA2.5服務端/gmsv/',1)[1]
        assert path not in members and not x['flags'] & (1|2|4|16) and x['extractor']=='unar'
        assert (x['bytes'],x['sha256'])==(r40.PINS.get(path) or inv[path.removeprefix('data/')])
        members[path]=x
    expected={'setup.cf','data/enemybase.txt','data/enemy.txt','data/group1.txt','data/encount.txt'}
    expected.update('data/'+k for k in inv if k.startswith(('npc/quiz/','npc/giiru/event/sink/')) and not k.lower().endswith('.bak'))
    assert set(members)==expected
    graw=(P/'PET-HIGH-FIRST-19C-QUEST-AND-GIFT-WITNESSES-R1.json').read_bytes()
    assert r40.git_blob(graw)==d['guide_blob']
    guide=json.loads(graw)['rows'];assert len(guide)==q['guide_rows']==58
    gs={t['graphic'] for g in guide for t in g['templates']}
    assert len(gs)==q['candidate_graphic_count']==57
    rows=q['capture_candidates'];assert len(rows)==145 and len({x['template']['id'] for x in rows})==145
    assert {x['template']['graphic'] for x in rows}==gs
    assert q['table_counts']==[988,2087,1257,660]
    assert sum(x['positive_routes'] for x in rows)==660 and sum(x['double_pet_flag_routes'] for x in rows)==636
    assert sum(len(x['lv1_routes']) for x in rows)==33
    assert sum(x['template']['pet_flag']==1 for x in rows)==86
    assert sum(bool(x['double_pet_flag_routes']) for x in rows)==43 and sum(bool(x['lv1_routes']) for x in rows)==29
    def exact_positions(field):
        return {g['guide_pos'] for x in rows if x[field] for g in x['guide_graphic_candidates'] if g['comparison_template_id']==x['template']['id']}
    assert len(exact_positions('double_pet_flag_routes'))==38 and len(exact_positions('lv1_routes'))==29
    for x in rows:
        t=x['template'];assert 0<=len(x['lv1_routes'])<=x['double_pet_flag_routes']<=x['positive_routes']
        assert not x['double_pet_flag_routes'] or t['pet_flag']==1
        assert all(v['template']==t['id'] and v['instance_pet_flag']==v['template_pet_flag']==1 and v['level'][0]<=1<=v['level'][1] and min(v['weights'])>0 and v['floor'] in x['floor_ids'] for v in x['lv1_routes'])
        expect=[{'guide_pos':g['pos'],'guide_name':g['source_name'],'comparison_template_id':v['id'],'claim':g['claim']} for g in guide for v in g['templates'] if v['graphic']==t['graphic']]
        assert x['guide_graphic_candidates']==expect
    awards=q['award_commands'];assert len(awards)==3
    expect={14:(12,100255,'NOWEV=44&ITEM=2753',44,[(810,[28,16,28,16]),(850,[28,16,28,16])]),
            351:(302,100372,'ENDEV=44&NOWEV=47&ITEM=2759',47,[(812,[32,24,32,24])]),
            352:(303,100373,'ENDEV=44&NOWEV=45&ITEM=2759',45,[])}
    # Independent fixed later comparison bytes. Same semantics do not certify an original official deployment.
    base='https://raw.githubusercontent.com/gavinlinasd/StoneAge/1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56/gmsv/'
    pins={'data/enemy1.txt':'bf245a391adeace09915b6e425754b54ab69a8f6','data/enemybase1.txt':'a19a508975e3a982fada323861b35b2edab79349',
          'data/npc/quiz/equiz_02':'52de56ec4085df7c3716be5abc3042221112bbfc','data/npc/quiz/equiz_04':'f5ba36616d72bdae829d86f9a3d38ea0f68a3b6d',
          'data/npc/giiru/event/sink/equiz_04':'add69b328d8977d7072654a4117ae43d19fac415'}
    later={}
    for path,pin in pins.items():
        with urllib.request.urlopen(base+path,timeout=45) as response: buf=response.read(2_000_001)
        assert len(buf)<=2_000_000 and r40.git_blob(buf)==pin,path
        later[path]=buf
    ei=r40.idx(r40.rows(later['data/enemy1.txt'],34,3),3)
    bi=r40.idx(r40.rows(later['data/enemybase1.txt'],56,6),6)
    for x in awards:
        aid=x['award_instance_id'];tid,gfx,condition,flag,creates=expect[aid]
        assert x['instance_matches']==x['template_matches']==1
        assert x['instance']['template_id']==x['template']['id']==tid and x['template']['graphic']==gfx
        assert x['instance']['level']==[1,1] and x['instance']['pet_flag']==x['template']['pet_flag']==1
        assert x['fields']['event']==[condition] and x['fields']['endsetflg']==[str(flag)] and x['fields']['type']==['ACCEPT']
        assert [(v['floor'],v['corner']) for v in x['create_references']]==creates
        assert len(ei[aid])==len(bi[tid])==1
        e=ei[aid][0][1];b=bi[tid][0][1]
        assert int(e[4])==tid and int(b[36])==gfx and r40.level(e)==[1,1]
        # Verify instruction and event condition in same source block; no raw dialogue published.
        script=later['data/'+x['path']]; blocks=script.lower().split(b'eventend')
        matches=[v for v in blocks if ('getpet:'+str(aid)).encode() in v]
        assert len(matches)==1 and ('event:'+condition).lower().encode() in matches[0] and ('endsetflg:'+str(flag)).encode() in matches[0]
        print('later comparison',aid,tid,gfx,'flags',int(e[13]),int(b[37]))
    tw=json.loads((P/'PET-DETAIL-EVIDENCE31-TW10-FIELD-COVERAGE-R1.json').read_bytes())['records']
    assert len(c['rows'])==57
    for x in c['rows']:
        (t,)=[v for v in tw if v['pet_id']==x['pet_id']]
        gfx=t['client_graphic'];assert (gfx,t['client_name_original'])==(x['tw10_graphic'],x['original_client_name'])
        assert x['archive_template_row_indices']==[i for i,v in enumerate(rows) if v['template']['graphic']==gfx]
        assert x['award_row_indices']==[i for i,v in enumerate(awards) if v['template']['graphic']==gfx]
        assert not x['official_tw10_acquisition_verified'] and x['official_tw10_native_stats'] is None and x['official_first_release_date'] is None
    assert {x['tw10_graphic'] for x in c['rows']}==gs
    assert not any((d['official_deployment_verified'],d['original_payload_published'],q['map_bytes_read'],q['actual_awards_verified'],q['runtime_executed'],c['official_deployment_verified'],c['original_assets_published'],c['runtime_executed'])) and c['official_species_count'] is None
    print('PET41: 31 exact members, 145 templates, 636 double-flag routes, 33 Lv1 routes, three static rewards; official deployment OPEN.')
if __name__=='__main__':verify()
