"""Replay bounded PET47 source joins; manual historical claims remain human-transcribed."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p,sha=None):
    b=(ROOT/p).read_bytes()
    if sha: assert hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==sha,p
    return json.loads(b)
def main():
    r=load('research/pets/PET-HIGH-FIRST-47-PERIOD-ACQUISITION-GAP-R1.json')
    d={p:load(p,s) for p,s in r['input_git_blobs'].items()}
    gap={x['tw75_row_index']:x for x in d['research/pets/PET-HIGH-FIRST-46-ACQUISITION-GAP-MATRIX-R1.json']['rows'] if x['gap_state']=='NO_QUALIFIED_ACQUISITION_REFERENCE_IN_THIS_BATCH'}
    master=d['research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json']['pet_flag_1_field_projections']
    assert len(gap)==102
    hit=set(); conflicts=set()
    for x in r['period_links']:
        i=x['tw75_row_index']; g=gap[i]; t=master[i]
        assert (g['template_id'],g['name'],g['graphic'],g['row_sha256'])==(x['template_id'],x['master_name'],x['graphic'],x['row_sha256'])
        assert x['master_elements']==t['elements'] and x['selected_table_status']==g['selected_table']['status']
        assert i not in hit|conflicts
        if x['printed_elements']==t['elements']:
            assert x['qualification']=='NAME_ELEMENT_COMPATIBLE_PERIOD_PLAYER_CLAIM_NOT_SAME_DEPLOYMENT'
            hit.add(i)
        else:
            assert x['qualification']=='NAME_MATCH_ELEMENT_CONFLICT_DO_NOT_ASSIGN'
            conflicts.add(i)
        assert not x['official_acquisition_verified'] and x['official_first_release'] is None
    contexts=[]
    for src in r['prior_reports_reviewed']:
        j=d[src['path']]; rows=j.get('rows',j.get('records'))
        assert len(rows)==src['rows_reviewed']
        start=len(contexts)
        for k,x in enumerate(rows):
            names=[x.get(q) for q in ('name','original_name','catalogue_name','recollection_name')]+x.get('spellings',[])
            for i,g in gap.items():
                if g['name'] in names:
                    contexts.append(dict(source_row_index=k,tw75_row_index=i,template_id=g['template_id'],name=g['name'],role=x['role'],group=x['group'],qualification='CONTEXT_NOT_QUALIFIED_ACQUISITION'))
        assert len(contexts)-start==src['matched_source_template_pairs']
    assert r['context_only_links']==contexts
    assert r['remaining_gap_row_indices']==[i for i in gap if i not in hit]
    s=r['summary']
    assert (len(hit),len(conflicts),len(contexts))==(19,2,8)
    assert s['compatible_claim_rows']==len(hit) and s['element_conflict_rows']==len(conflicts)
    assert s['remaining_without_compatible_claim']==len(gap)-len(hit)
    assert s['compatible_same_id_nonidentical_rows']==sum(gap[i]['selected_table']['status']=='SAME_ID_NONIDENTICAL_ROW' for i in hit)
    assert s['official_acquisition_closed']==0 and s['official_new_species'] is None
    assert not r['official_same_deployment_verified'] and not r['original_assets_published']
    print('PET47 bounded source join replay PASS',s)
if __name__=='__main__':main()
