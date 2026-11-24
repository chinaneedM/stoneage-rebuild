"""Replay PET48 template joins; source descriptions are human-reviewed, not raw HTML replay."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p,sha=None):
    b=(ROOT/p).read_bytes()
    if sha: assert hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==sha,p
    return json.loads(b)
def main():
    r=load('research/pets/PET-HIGH-FIRST-48-LEGACY-PC-ACQUISITION-GAP-R1.json')
    d={p:load(p,s) for p,s in r['input_git_blobs'].items()}
    prev=d['research/pets/PET-HIGH-FIRST-47-PERIOD-ACQUISITION-GAP-R1.json']['remaining_gap_row_indices']
    gap={x['tw75_row_index']:x for x in d['research/pets/PET-HIGH-FIRST-46-ACQUISITION-GAP-MATRIX-R1.json']['rows']}
    master=d['research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json']['pet_flag_1_field_projections']
    sources={s['id'] for s in r['sources']}
    hit=set()
    assert len(prev)==83 and len(set(prev))==83
    for x in r['rows']:
        i=x['tw75_row_index'];g=gap[i];m=master[i]
        assert i in prev and i not in hit and x['source_id'] in sources
        assert (g['template_id'],g['name'],g['graphic'],g['row_sha256'])==(x['template_id'],x['master_name'],x['graphic'],x['row_sha256'])
        assert x['master_elements']==x['printed_elements']==m['elements']
        assert x['selected_table_status']==g['selected_table']['status']
        assert x['qualification']=='NAME_ELEMENT_COMPATIBLE_LEGACY_REFERENCE_NOT_SAME_DEPLOYMENT'
        assert not x['official_acquisition_verified'] and x['official_first_release'] is None
        hit.add(i)
    for x in r['context']:
        i=x['tw75_row_index'];assert i in prev and i not in hit and x['source_id'] in sources
        assert x['template_id']==gap[i]['template_id'] and x['qualification']=='CONTEXT_OR_CONFLICT_NOT_QUALIFIED'
    assert r['remaining_gap_row_indices']==[i for i in prev if i not in hit]
    assert len(hit)==9 and len(r['remaining_gap_row_indices'])==74
    assert r['summary']==dict(reviewed_residual=83,compatible_reference_rows=9,remaining_without_compatible_reference=74,official_acquisition_closed=0,official_new_species=None)
    assert not r['official_same_deployment_verified'] and not r['original_assets_published']
    print('PET48 bounded source joins PASS',r['summary'])
if __name__=='__main__':main()
