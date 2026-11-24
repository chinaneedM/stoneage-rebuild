"""Verify PET42's immutable-source reward instance join. Never infer live awards."""
import json
from pathlib import Path
from tools import stoneage_pet_high_first_40_acquisition as r40
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'research/pets'
R=ROOT/'research/recovered'
FILES={
 'i05':R/'STONEAGE-INTEGRATION05-GETPET-QUEST-MAP-ORIGINAL-SOURCE-GRAPH-R1.json',
 'pet10':R/'STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json',
 'quest':R/'STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json',
 'guide':P/'PET-HIGH-FIRST-19C-QUEST-AND-GIFT-WITNESSES-R1.json',
 'tw10':P/'PET-DETAIL-EVIDENCE31-TW10-FIELD-COVERAGE-R1.json'}
INDEX=P/'PET-HIGH-FIRST-42-REWARD-INSTANCE-INDEX-R1.json'
def verify():
    report=json.loads(INDEX.read_bytes()); d={}
    for k,p in FILES.items():
        raw=p.read_bytes();assert r40.git_blob(raw)==report['source_pins'][k],k
        d[k]=json.loads(raw)
    I,P10,Q,G,T=(d[k] for k in FILES)
    assert I['source_RAR_sha256']==P10['preserved_original_rar']['sha256']==Q['source']['original_RAR_sha256']==report['rar_sha256']
    a=json.loads((P/'PET-HIGH-FIRST-41-MIXED25-ACQUISITION-R1.json').read_bytes())
    members={x['path'].rsplit('/',1)[-1]:x for x in a['member_receipt']['members']}
    for f in ('enemy.txt','enemybase.txt'):
        assert members[f]['sha256']==P10['verified_original_archive_members'][f]['sha256']
    assert members['setup.cf']['sha256']==r40.PINS['setup.cf'][1]
    assert a['projection']['table_counts'][:2]==[988,2087]
    ir=I['rows']; assert len(ir)==24
    for r in ir:
        assert sum(s['path']==r['source_script_path'] and s['original_sha256']==r['source_script_original_sha256'] for s in Q['source_scripts'])==1
    ids=sorted({n for r in ir for n in r['original_GetPet_numeric_literals_ordered']})
    assert ids==[r['award_instance_id'] for r in report['rows']] and len(ids)==36
    for r in report['rows']:
        id=r['award_instance_id'];(e,)=[v for v in P10['source_rows']['enemy.txt'] if v[1]==id];assert e[3]==1
        (b,)=[v for v in P10['source_rows']['enemybase.txt'] if v[1]==e[2]]
        assert (r['template_id'],r['graphic'],r['template_pet_flag'])==tuple(b[1:4])
        assert (r['instance_nonempty_row'],r['instance_row_fields_sha256'])==(e[0],e[4])
        assert (r['template_nonempty_row'],r['template_row_fields_sha256'])==(b[0],b[16])
        assert (r['base_fields'],r['initnum'],r['lvup'],r['elements'],r['skill_slots'])==(b[6:10],b[4],b[5],b[10:14],b[15])
        tw=[v for v in T['records'] if v['client_graphic']==b[2]]
        expected=None if not tw else {'pet_id':tw[0]['pet_id'],'client_name':tw[0]['client_name_original'],'graphic':b[2]}
        assert len(tw)<=1 and r['tw10_candidate']==expected
        assert r['period_guide_candidates']==[{'position':v['pos'],'name':v['source_name'],'claim':v['claim']} for v in G['rows'] if any(z['graphic']==b[2] and z['id']==b[1] for z in v['templates'])]
        assert r['script_refs']==[{'i05_row_index':i,'path':v['source_script_path'],'floor':v['source_floor_id'],'occurrences':v['original_GetPet_numeric_literals_ordered'].count(id),'script_sha256':v['source_script_original_sha256'],'map_grade':v['qualifying_DAT_grade']} for i,v in enumerate(ir) if id in v['original_GetPet_numeric_literals_ordered']]
        assert r['instance_pet_flag'] is None and r['instance_level'] is None and not r['actual_award_verified'] and not r['official_same_deployment_verified']
    ss=report['scripts']
    assert [s['path'] for s in ss]==list(dict.fromkeys(r['source_script_path'] for r in ir))
    for s in ss:
        refs=[i for i,r in enumerate(ir) if r['source_script_path']==s['path']]
        assert refs==s['i05_row_indices']
        for i in refs:
            r=ir[i];assert (s['source_lines'],s['ordered_numeric_literals'],s['script_sha256'])==(r['original_GetPet_commands_source_lines'],r['original_GetPet_numeric_literals_ordered'],r['source_script_original_sha256'])
        assert s['blocks']==[{'ordinal':b['script_block_ordinal'],'type':b['raw_type'],'type_line':b['source_type_line'],'event_number':b['event_number'],'end_flags':b['end_set_flags'],'condition_sha256':b['condition_expression_decoded_cp950_UTF8_sha256'],'block_sha256':b['source_section_decoded_cp950_normalized_UTF8_sha256']} for b in Q['source_event_blocks'] if b['script_path']==s['path'] and b['source_operations'].get('GetPet')]
    rr=report['rows']
    counts={'source_create_refs':len(ir),'unique_scripts':len(ss),'source_getpet_lines':sum(len(s['source_lines']) for s in ss),'distinct_instance_ids':len(ids),'distinct_templates':len({r['template_id'] for r in rr}),'distinct_graphics':len({r['graphic'] for r in rr}),'tw10_graphic_candidates':sum(r['tw10_candidate'] is not None for r in rr),'no_tw10_graphic_candidates':sum(r['tw10_candidate'] is None for r in rr),'exact_guide_template_graphic_candidates':sum(bool(r['period_guide_candidates']) for r in rr),'template_pet_flag_1':sum(r['template_pet_flag']==1 for r in rr),'accept_blocks':sum(b['type']=='ACCEPT' for s in ss for b in s['blocks']),'message_blocks':sum(b['type']=='MESSAGE' for s in ss for b in s['blocks']),'script_numeric_occurrences':sum(len(s['ordered_numeric_literals']) for s in ss)}
    assert counts==report['counts']=={'source_create_refs':24,'unique_scripts':23,'source_getpet_lines':25,'distinct_instance_ids':36,'distinct_templates':36,'distinct_graphics':36,'tw10_graphic_candidates':33,'no_tw10_graphic_candidates':3,'exact_guide_template_graphic_candidates':32,'template_pet_flag_1':36,'accept_blocks':21,'message_blocks':4,'script_numeric_occurrences':40}
    assert {r['graphic'] for r in rr if r['tw10_candidate'] is None}=={100401,100432,100451}
    assert next(s for s in ss if s['path']=='jaruga/event/oev_edb')['ordered_numeric_literals']==[338,360,366,482,482,78]
    assert not any(report[k] for k in ('original_members_newly_read','official_deployment_verified','actual_awards_verified','original_assets_published')) and report['official_species_count'] is None and report['instance_level_and_pet_flag_unverified']
    print('PET42 exact derived replay: 36 instance/template joins, 23 source scripts, 25 GetPet lines, 40 numeric occurrences, 4 MESSAGE blocks.')
    return report
if __name__=='__main__':verify()
