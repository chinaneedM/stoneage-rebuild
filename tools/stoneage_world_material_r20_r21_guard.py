"""Verify durable exact metadata custody and keep unavailable entity/runtime claims open."""
import json
import lzma
from tools.stoneage_map_resource_content_r21 import ROOT,need,fingerprint,replay

def check():
    base=ROOT/'research/recovered'
    c=json.loads((base/'STONEAGE-FOUR-MAP-RESOURCE-CUSTODY-R21.json').read_bytes())
    a=c['durable_archive'];packed=(ROOT/a['path']).read_bytes();need(fingerprint(packed)=={k:a[k] for k in ('bytes','sha256','git_blob')},'compressed archive custody')
    raw=lzma.decompress(packed);need(fingerprint(raw)==c['raw_json'],'exact raw JSON bytes restored')
    r=json.loads(raw);replay(r)
    s=c['summary_file'];need(fingerprint((ROOT/s['path']).read_bytes())=={k:s[k] for k in ('bytes','sha256','git_blob')},'summary custody')
    summary=json.loads((ROOT/s['path']).read_bytes())
    need(summary['raw_source_json']==c['raw_json'] and summary['no_runtime_selection_or_named_entity_promotion'] is True,'summary boundaries')
    for m,short in zip(r['maps'],summary['maps']):
        need((m['floor_token'],m['width'],m['height'])==(short['floor_token'],short['width'],short['height']),'summary map identity')
        for p,q in zip(m['planes'][:2],short['planes']):
            need(q['ordinal']==p['ordinal'] and q['distinct_map_values_including_zero']==len(p['histogram']),'summary plane identity')
            for profile,values in q['profiles'].items():
                need(values=={k:p['resource_value_comparisons'][profile][k] for k in values},'summary material values')
    need(len(summary['maps'])==4 and [v['map_value'] for v in summary['selected_material_values']]==[4,2,8326],'finite summary selections')
    for item in summary['selected_material_values']:
        value=item['map_value'];uses=[];observed={}
        for m in r['maps']:
            for p in m['planes'][:2]:
                if value in dict(p['histogram']):
                    uses.append({'floor_token':m['floor_token'],'ordinal':p['ordinal'],'cells':dict(p['histogram'])[value]})
                    for profile,j in p['resource_value_comparisons'].items():
                        row=next(row for row in j['rows'] if row['map_value']==value)
                        projected=sorted([{'source_index':v['source_index'],'physical_bitmapno':v['physical_bitmapno'],
                            'rd_sha256':v['content_sha256']} for v in row['candidates']],key=lambda v:(v['source_index'],v['physical_bitmapno'],v['rd_sha256']))
                        if profile in observed:need(observed[profile]==projected,'inconsistent resource projection')
                        observed[profile]=projected
        need(item['actual_map_occurrences']==uses and item['profile_occurrences']==observed,'selected material summary differs')
    r20=json.loads((base/'STONEAGE-EARLY-WORLD-ENTITY-SOURCE-R20.json').read_bytes())
    for p,f in r20['source_pins'].items():need(fingerprint((ROOT/p).read_bytes())==f,'R20 previous-source pin')
    need(r20['new_original_named_entity_mappings']==0 and r20['original_client_executed'] is False and
        r20['overall_restoration_percent'] is None and r20['bounded_outcome']=='OPEN_NO_NEW_AUTHENTICATED_SAME_BUILD_ENTITY_SOURCE','R20 evidence stop')
    for p,f in c['full_startup_files'].items():
        # README is additive; immutable full historical startup prefix remains exact.
        b=(ROOT/p).read_bytes()[:f['bytes']];need(fingerprint(b)==f,'historical startup prefix lost')
    need(c['source_run']['status']=='completed' and c['source_run']['conclusion']=='success' and
        all(j['status']=='completed' and j['conclusion']=='success' for j in c['source_jobs']),'actual source acceptance')
    need(c['new_authenticated_named_entities']==0 and c['original_client_executed'] is False and
        c['overall_restoration_percent'] is None,'bounded material result')
    print('R20_SOURCE_STOP_AND_R21_EXACT_XZ_CUSTODY=PASS; ORIGINAL_NAMES_RUNTIME_NOT_PROMOTED')

if __name__=='__main__':check()
