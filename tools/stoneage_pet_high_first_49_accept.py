"""Replay PET49 joins; manual historical transcription is not raw HTML verification."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p,sha=None):
    b=(ROOT/p).read_bytes()
    if sha: assert hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==sha,p
    return json.loads(b)
def main():
    r=load('research/pets/PET-HIGH-FIRST-49-DATED-PC-ACQUISITION-GAP-R1.json')
    d={p:load(p,s) for p,s in r['input_git_blobs'].items()}
    prev=d['research/pets/PET-HIGH-FIRST-48-LEGACY-PC-ACQUISITION-GAP-R1.json']['remaining_gap_row_indices']
    gap={x['tw75_row_index']:x for x in d['research/pets/PET-HIGH-FIRST-46-ACQUISITION-GAP-MATRIX-R1.json']['rows']}
    master=d['research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json']['pet_flag_1_field_projections']
    sources={x['id'] for x in r['sources']}
    assert len(prev)==74 and len(set(prev))==74
    hit=set()
    for x in r['rows']:
        i=x['tw75_row_index'];g=gap[i];m=master[i]
        assert i in prev and i not in hit
        assert (g['template_id'],g['name'],g['graphic'],g['row_sha256'])==(x['template_id'],x['master_name'],x['graphic'],x['row_sha256'])
        assert x['master_elements']==x['source_elements']==m['elements']
        assert x['selected_table_status']==g['selected_table']['status']
        assert x['qualification']=='COMPATIBLE_HISTORICAL_ACQUISITION_REFERENCE_NOT_SAME_DEPLOYMENT'
        assert not x['official_acquisition_verified'] and x['official_first_release'] is None
        assert all(z['source_id'] in sources for z in x['refs'])
        hit.add(i)
    assert hit=={106,116,315,319,321,392,456}
    bulls=[x for x in r['rows'] if x['kind']=='AMBIGUOUS_TWO_TEMPLATES_REWARD']
    assert len(bulls)==2 and {x['template_id'] for x in bulls}=={169,1051} and bulls[0]['refs']==bulls[1]['refs']
    ctx=set()
    for x in r['context']:
        i=x['tw75_row_index']; assert i in prev and i not in hit|ctx
        assert x['template_id']==gap[i]['template_id'] and x['name']==gap[i]['name']
        assert x['qualification']=='CONTEXT_OR_INCOMPLETE_OR_CONFLICT_NOT_QUALIFIED'
        assert all(z['source_id'] in sources for z in x['refs'])
        ctx.add(i)
    assert r['remaining_gap_row_indices']==[i for i in prev if i not in hit]
    assert len(hit)==7 and len({x['master_name'] for x in r['rows']})==6 and len(ctx)==15 and len(r['remaining_gap_row_indices'])==67
    assert r['summary']==dict(input_remaining=74,compatible_reference_rows=7,distinct_compatible_names=6,context_rows=15,remaining_without_compatible_reference=67,official_acquisition_closed=0,official_new_species=None)
    assert not r['official_same_deployment_verified'] and not r['original_assets_published']
    print('PET49 bounded dated PC reference joins PASS',r['summary'])
if __name__=='__main__':main()
