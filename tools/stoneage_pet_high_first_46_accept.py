"""Independent replay of PET46 evidence selection, all 349 existing source rows."""
import collections,json,hashlib
from pathlib import Path
from tools import stoneage_pet_source_lookup as lookup
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/pets/PET-HIGH-FIRST-46-ACQUISITION-GAP-MATRIX-R1.json'
def pinned(path,sha):
    raw=(ROOT/path).read_bytes()
    assert lookup.blob(raw)==sha,path
    return json.loads(raw)
def compare(t,table):
    hits=[(i,x) for i,x in enumerate(table) if x[1]==t['template_id']]
    if not hits:return dict(row_index=None,status='NO_SAME_ID',projected_differences=None)
    (i,b),=hits
    pairs={'graphic':(t['graphic'],b[2]),'pet_flag':(t['pet_flag'],b[3]),'initnum':(t['initnum'],int(b[4])),
           'lvup_literal':(t['lvup_literal'],b[5]),'base':(t['base'],list(map(int,b[6:10]))),'elements':(t['elements'],list(map(int,b[10:14]))),
           'skill_slot_capacity':(t['skill_slot_capacity'],b[14]),'skill_slots':(t['skill_slots'],b[15])}
    return dict(row_index=i,status='EXACT_SHARED_ROW' if b[16]==t['row_sha256'] else 'SAME_ID_NONIDENTICAL_ROW',row_sha256=b[16],
                projected_differences={k:dict(claimed_tw75=a,saved_mixed25=b) for k,(a,b) in pairs.items() if a!=b})
def main():
    m,d=lookup.load();report=d['hf46'];pins=report['input_git_blobs']
    aliases={'r17':'tw75_comparison','r42':'hf42_cross'}
    for k,sha in pins.items():
        if k=='pet10':continue
        assert m['sources'][aliases.get(k,k)]['git_blob']==sha,k
    p=pinned('research/recovered/STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json',pins['pet10'])
    rows=report['rows'];a=d['hf45']['projection']['claimed_tw75_rows'];catalog=d['tw75']['pet_flag_1_field_projections']
    assert len(rows)==349 and [x['tw75_row_index'] for x in rows]==[i for i,x in enumerate(a) if not x['double_pet_flag_route_count']]
    assert len(pins)==15
    q25={'RANDOM_REDEMPTION_OPTION','FUTURE_DATED_SHOP_EXAMPLE','OPERATOR_CURRENT_TENSE_SHOP_CLAIM','CONTEMPORANEOUS_OPERATOR_PRESENT_TENSE_VIP_SHOP'}
    q26={'CIRCUS_REWARD_ALREADY_NAMED_IN_2011','CIRCUS_REWARD','HONOR_SHOP_EXCHANGE','LEGACY_FUSED_WHITE_SEAHORSE','WILD_CAPTURABLE_OPERATOR_CLAIM','WILD_CAPTURABLE_OPERATOR_CLAIM_SKILL_一击必杀','CN85_REWARD_REPEATED_2011_PET86','CN25_REWARD','PROMISED_PET_REWARD','TASK_ACQUISITION_DESCRIPTION'}
    for x in rows:
        i=x['tw75_row_index'];t=catalog[i];tid=t['template_id']
        assert (x['template_id'],x['name'],x['graphic'],x['row_sha256'])==(tid,t['name'],t['graphic'],t['row_sha256'])
        assert x['selected_table']==compare(t,p['source_rows']['enemybase.txt'])
        assert x['alternate_table']==compare(t,p['source_rows']['enemybase2.txt'])
        assert x['selected_positive_route_count']==a[i]['positive_route_count'] and not x['selected_double_flag_route_count']
        exact=lambda v:(v['template_id'],v['graphic'],v['row_sha256'])==(tid,t['graphic'],t['row_sha256'])
        q=[j for j,y in enumerate(d['hf42_cross']['rows']) if y['tw75_row_index']==i and y['shared_template_row_sha256']==t['row_sha256']]
        assert x['quest_reward_exact_row_indices']==q
        (j,y),=[(j,y) for j,y in enumerate(d['tw75_comparison']['rows']) if y['template_id']==tid]
        z=dict(row_index=j,status=y['comparison_status'],positive_reference_count=y['positive_reference_count'],lv1_positive_reference_count=y['lv1_positive_reference_count'])
        assert x['later_comparison']==z
        guide=[dict(row_index=j,claim=y['claim'],name_variant_only=y['name_variant_only'],source_pos=y['pos']) for j,y in enumerate(d['hf19c']['rows']) if any(v['id']==tid and v['graphic']==t['graphic'] for v in y['templates'])]
        assert x['period_guide_refs']==guide
        capsule=[dict(row_index=j,acquisition=y['acquisition']) for j,y in enumerate(d['hf20']['rows']) if any(exact(v) for v in y['master'])]
        assert x['capsule_refs']==capsule
        refs=[]
        for j,y in enumerate(d['hf19']['rows']):
            if (y['template_id'],y['master_graphic'],y['master_row_sha256'])==(tid,t['graphic'],t['row_sha256']):
                refs.append(dict(source='hf19',row_index=j,qualification='EXACT_MASTER_FINGERPRINT_PERIOD_SOURCE_ASSOCIATION_NOT_AWARD',source_ids=y['source_ids']))
        for j,y in enumerate(d['hf24']['rows']):
            if any(exact(v) for v in y['source_candidates']['claimed_tw75_master']):
                refs.append(dict(source='hf24',row_index=j,qualification='EXACT_MASTER_FINGERPRINT_NAMED_PROMOTION',role=y['kind'],acquisition_kind=(y.get('acquisition') or {}).get('kind')))
        for k,role,qualified in [('hf25','source_class',q25),('hf26_27','role',q26)]:
            for j,y in enumerate(d[k]['rows']):
                if any(exact(v) for v in (y.get('direct') or {}).get('claimed_tw75_templates',[])):
                    refs.append(dict(source=k,row_index=j,qualification='EXACT_MASTER_FINGERPRINT_ACQUISITION_CLAIM' if y[role] in qualified else 'EXACT_MASTER_FINGERPRINT_CONTEXT_ONLY',role=y[role]))
        for j,y in enumerate(d['fusion2003']['records']):
            if y['displayed_name']==t['name']:refs.append(dict(source='fusion2003',row_index=j,qualification='EXACT_PRINTED_NAME_ONLY_FUSION_PANEL_NOT_TEMPLATE_ID'))
        for k in ('hf34','hf35','hf36'):
            for j,y in enumerate(d[k]['rows']):
                if y['name']==t['name'] and not y.get('role','').startswith('UNQUALIFIED_') and (y.get('acquisition') or (y.get('claim') or {}).get('acquisition')):
                    refs.append(dict(source=k,row_index=j,qualification='EXACT_NAME_ONLY_ACQUISITION_WITNESS_NOT_TEMPLATE_ID',role=(y.get('acquisition') or {}).get('kind',y.get('role'))))
        assert x['additional_refs']==refs,(i,x['additional_refs'],refs)
        cat=[]
        if q:cat.append('EXACT_SAVED_QUEST_REWARD')
        if z['positive_reference_count']>0:cat.append('LATER_EXACT_TAIL_POSITIVE_REFERENCE' if z['status']=='EXACT_NONNAME_50_FIELD_TAIL' else 'LATER_DIFFERENT_TAIL_POSITIVE_REFERENCE')
        if any(y['claim'] not in {'UNKNOWN_IN_2001_GUIDE','CN_APPEARANCE_UNCONFIRMED'} for y in guide):cat.append('PERIOD_GUIDE_ACQUISITION_CLAIM')
        if capsule:cat.append('CAPSULE_EXACT_MASTER_FINGERPRINT')
        if any(y['qualification'] in {'EXACT_MASTER_FINGERPRINT_ACQUISITION_CLAIM','EXACT_MASTER_FINGERPRINT_NAMED_PROMOTION'} for y in refs):cat.append('PERIOD_EXACT_MASTER_ACQUISITION_CLAIM')
        if any(y['source']=='hf19' for y in refs):cat.append('PERIOD_EXACT_MASTER_SOURCE_ASSOCIATION')
        if any(y['source']=='fusion2003' for y in refs):cat.append('FUSION_PRINTED_NAME_ONLY')
        if any(y['qualification']=='EXACT_NAME_ONLY_ACQUISITION_WITNESS_NOT_TEMPLATE_ID' for y in refs):cat.append('PERIOD_NAME_ONLY_ACQUISITION_CLAIM')
        assert x['evidence_categories']==cat
        assert x['gap_state']==('SAVED_TASK_REWARD_CONFIGURED_NOT_EXECUTED' if q else 'OTHER_SOURCE_REFERENCES_NOT_OFFICIAL_ACQUISITION' if cat else 'NO_QUALIFIED_ACQUISITION_REFERENCE_IN_THIS_BATCH')
        assert not x['official_acquisition_verified'] and x['official_first_release'] is None
    C=collections.Counter
    s=report['summary']
    assert s['gap_rows']==len(rows)
    assert s['selected_match_states']==C(x['selected_table']['status'] for x in rows)=={'EXACT_SHARED_ROW':322,'NO_SAME_ID':1,'SAME_ID_NONIDENTICAL_ROW':26}
    assert s['alternate_match_states']==C(x['alternate_table']['status'] for x in rows)
    assert s['evidence_category_counts']==C(y for x in rows for y in x['evidence_categories'])
    assert s['gap_state_counts']==C(x['gap_state'] for x in rows)=={'NO_QUALIFIED_ACQUISITION_REFERENCE_IN_THIS_BATCH':102,'OTHER_SOURCE_REFERENCES_NOT_OFFICIAL_ACQUISITION':234,'SAVED_TASK_REWARD_CONFIGURED_NOT_EXECUTED':13}
    assert s['additional_source_reference_counts']==C(y['source'] for x in rows for y in x['additional_refs'])
    assert s['selected_mismatched_projected_fields']==C('PROJECTED_FIELDS_DIFFER' if x['selected_table']['projected_differences'] else 'PROJECTED_FIELDS_EQUAL_FULL_ROW_DIFFERS' for x in rows if x['selected_table']['status']=='SAME_ID_NONIDENTICAL_ROW')
    assert not any(x['alternate_table']['status']=='EXACT_SHARED_ROW' for x in rows if x['selected_table']['status']!='EXACT_SHARED_ROW')
    assert report['official_species_count'] is None and not report['official_same_deployment_verified']
    print('PET46 independent source replay:',json.dumps(s,ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
