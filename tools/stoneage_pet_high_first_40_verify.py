"""Replay PET40 fixed public source and immutable derived archive report."""
import hashlib,json,urllib.request
from pathlib import Path
from tools.stoneage_pet_high_first_40_acquisition import project,git_blob,sha,PINS
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'research/pets/PET-HIGH-FIRST-40-MIXED25-ACQUISITION-R1.json'
B=ROOT/'research/pets/PET-HIGH-FIRST-40-ACQUISITION-CROSSWALK-R1.json'
def verify():
    raw=A.read_bytes();d=json.loads(raw);r=json.loads(B.read_bytes())
    a=r['archive_source'];p=r['public_source']
    assert len(raw)==a['raw_json_bytes']==114585 and sha(raw)==a['raw_json_sha256'] and git_blob(raw)==a['derived_git_blob']
    assert a['api_zip_sha256']==a['independent_zip_sha256'] and a['conclusion']=='success'
    assert not d['official_deployment_verified'] and not d['runtime_executed'] and not d['original_payload_published']
    receipt=d['member_receipt']
    assert len(receipt['members'])==a['original_member_count']==14
    assert sum(x['bytes'] for x in receipt['range_receipts'])==a['range_bytes']==12013836 and len(receipt['range_receipts'])==a['range_requests']==184
    assert not receipt['whole_archive_or_parts_rehashed']
    invraw=(ROOT/'research/recovered/STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json').read_bytes()
    assert git_blob(invraw)==d['source_inventory_git_blob']
    inv={x['path']:(x['size'],x['sha256']) for x in json.loads(invraw)['all_server_occurrences']}
    for x in receipt['members']:
        name=x['path'].split('/SA2.5服務端/gmsv/',1)[1]
        expected=PINS.get(name) or inv[name.removeprefix('data/')]
        assert (x['bytes'],x['sha256'])==tuple(expected)
        assert not x['flags'] & (1|2|4|16) and x['extractor']=='unar'
    sources={}
    for path,pin in p['input_git_blobs'].items():
        url='https://raw.githubusercontent.com/'+p['repo']+'/'+p['commit']+'/gmsv/'+path
        with urllib.request.urlopen(url,timeout=45) as response: source=response.read(2_000_001)
        assert len(source)<=2_000_000 and git_blob(source)==pin,path
        sources[path]=source
    q=project(sources,'gb18030','enemybase1.txt','enemy1.txt')
    mixed=d['projection']
    assert mixed['table_counts']==r['archive_table_counts']==[988,2087,1257,660]
    assert q['table_counts']==p['table_counts']==[1816,2958,1392,1197]
    # Data-layer hash equivalence, not name or deployment equivalence.
    mm={x['path']:x for x in mixed['maps']}
    pp={x['path']:x for x in q['maps']}
    for x in r['map_comparisons']:
        name=x['path'];a1=mm[name];b1=pp[name]
        assert x['public_git_blob']==p['input_git_blobs'][name]
        assert sha(sources[name])==x['public_sha256']==b1['sha256']
        assert a1['sha256']==x['mixed_sha256']
        assert a1['planes_sha256']==b1['planes_sha256']==x['map']['planes_sha256']
        assert a1['header_sha256']!=b1['header_sha256']==x['map']['header_sha256']
        assert [a1[k] for k in ('floor','width','height')]==[b1[k] for k in ('floor','width','height')]
        assert not x['whole_equal'] and x['map']['plane_payload_equal'] and not x['map']['header_equal']
    assert len(mm)==len(pp)==len(r['map_comparisons'])==5
    pos=lambda x:[y for y in x['routes'] if y['instance_pet_flag']==y['template_pet_flag']==1]
    is1=lambda x:x['level'][0]<=1<=x['level'][1]
    am,bm=pos(mixed),pos(q)
    assert len(mixed['routes'])==len(am)==70 and len(q['routes'])==95 and len(bm)==79
    assert sum(map(is1,am))==6 and sum(map(is1,bm))==7
    for row in r['rows']:
        tid=row['ordinary_template_id'];gfx=row['tw10_graphic']
        assert [x['id'] for x in mixed['templates'] if x['graphic']==gfx]==row['archive_template_ids']
        assert [x['id'] for x in q['templates'] if x['graphic']==gfx]==row['public_template_ids']
        ar=[x for x in am if x['template']==tid];br=[x for x in bm if x['template']==tid]
        assert len(ar)==row['archive_positive_reference_count'] and sum(map(is1,ar))==row['archive_lv1_reference_count']
        assert len(br)==row['public_positive_reference_count'] and sum(map(is1,br))==row['public_lv1_reference_count']
        ix=[i for i,x in enumerate(mixed['routes']) if x['template']==tid and x['instance_pet_flag']==x['template_pet_flag']==1 and is1(x)]
        assert ix==row['archive_lv1_route_indices']
        assert sorted({mixed['routes'][i]['floor'] for i in ix})==row['archive_lv1_floors']
        assert not row['official_tw10_acquisition_verified'] and row['official_tw10_native_stats'] is None and row['official_first_release_date'] is None
    for x in (mixed,q):
        z=x['quest']
        assert z['award_id']==484 and z['award_instance']['template']==315 and z['award_instance']['level']==[1,1]
        assert z['award_template']['graphic']==100430 and z['award_template']['elements']==[0,0,50,50] and z['award_template']['base']==[20,28,20,32]
        assert z['award_template']['initnum']==30 and z['award_template']['lvup']=='4.50' and z['award_template']['skill_slots']==[1,2,None,None,None,None,None]
        assert z['completion_flag']==72 and z['condition']=='ENDEV=4&ENDEV=69&ENDEV=70&ENDEV=71&NOWEV=72'
        assert z['battle']['warp']==[30670,15,9] and z['battle']['dieact']==1
        assert [(y['floor'],y['corner']) for y in z['create']]==[(30689,[46,29,46,29]),(30670,[15,5,15,5])]
    exchange=sources['src/npc/npc_exchangeman.c']
    assert b'"GetPet"' in exchange and b'NPC_EventAddPet(' in exchange
    assert b'ENEMY_getInt( i, ENEMY_ID) == enemyid' in exchange and b'ENEMY_createPetFromEnemyIndex( talker, i)' in exchange
    assert b'ENEMYTEMP_getEnemyTempArray( array)' in sources['src/char/enemy.c']
    assert not r['official_deployment_verified'] and not r['original_assets_published'] and r['official_species_count'] is None
    print('PET40: 14 exact archived members, 5 shared map payloads, 70/79 source-local positive references, 484 -> 315 quest reward, official deployment remains OPEN.')
if __name__=='__main__':verify()
