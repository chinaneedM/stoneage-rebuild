"""Pure conditional writer topology/stack inventory; never consumes original bytes."""
from tools.stoneage_tw10_savedata_application_r51 import stack,coordinates,same

def analyze(caller,processors):
    rows=caller['instruction_shapes'];edges=caller['bounded_edges'];root=caller['root_candidate_rva']
    by={r['site_rva']:r for r in rows}
    if [r['site_rva'] for r in rows]!=caller['bounded_node_rvas']:raise ValueError('writer complete inventory')
    states,cap=stack(rows,edges,root)
    calls=caller['call_contexts'];sites=[c['site_rva'] for c in calls]
    if sites!=sorted(set(sites)) or sites!=[r['site_rva'] for r in rows if r['mnemonic']=='call']:raise ValueError('writer complete calls')
    out=[]
    for p in processors:
        site=p['caller_site_rva'];call=next((c for c in calls if c['site_rva']==site),None)
        if call is None or call['identity']['direct_target_rva']!=p['root_candidate_rva'] or site>=0x40064:raise ValueError('writer processor linkage')
        rs=p['instruction_shapes'];es=p['bounded_edges'];pr=p['root_candidate_rva']
        if [r['site_rva'] for r in rs]!=p['bounded_node_rvas']:raise ValueError('processor complete inventory')
        ps,limited=stack(rs,es,pr)
        out.append({'caller_site_rva':site,'root_candidate_rva':pr,
          'entry_coordinates':coordinates(rs,es,pr,call['physical_push_suffix']['pushes']),
          'return_candidates':[{'site_rva':r['site_rva'],'conditional_stack_delta_before_ret':ps.get(r['site_rva'])} for r in rs if r['mnemonic']=='ret'],
          'stack_limit_hit':limited,'division_sites':[r['site_rva'] for r in rs if r['mnemonic'] in ('div','idiv')],
          'not_sites':[r['site_rva'] for r in rs if r['mnemonic']=='not'],
          'call_sites':[r['site_rva'] for r in rs if r['mnemonic']=='call'],
          'actual_inverse_or_argument_values_proven':False})
    if len({x['caller_site_rva'] for x in out})!=len(out):raise ValueError('duplicate processor')
    return {'processor_surfaces':out,'caller_entry_stack_limit_hit':cap,
      'caller_conditional_entry_deltas':[{'site_rva':a,'delta':states.get(a)} for a in sites],
      'global_actual_values_normalization_migration_or_persistence_proven':False,
      'historical_writer_equals_r53_invented_inverse_proven':False}
