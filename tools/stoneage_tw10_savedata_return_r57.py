"""Pure full-inventory wrapper return/branch/source syntax; never evaluates bytes."""
from tools.stoneage_tw10_savedata_native_io_r52 import reaches,focus,flag_context,REGS

def analyze(c):
    rows=c['instruction_shapes'];edges=c['bounded_edges'];root=c['root_candidate_rva']
    if [r['site_rva'] for r in rows]!=c['bounded_node_rvas'] or len(rows)>256:raise ValueError('R57 complete inventory')
    maps={reg:reaches(rows,edges,root,reg,False) for reg in REGS}
    rets=[r for r in rows if r['mnemonic'] in ('ret','retf')]
    branches=[r for r in rows if r['mnemonic'].startswith('j') and r['mnemonic'] not in ('jmp','ljmp')]
    return {'return_contexts':[{'shape':r,'eax_source_graph':focus(rows,maps,[(r['site_rva'],'eax')]),'actual_return_value_or_error_convention_proven':False} for r in rets],
      'predicate_contexts':[flag_context(rows,edges,r['site_rva']) for r in branches],
      'division_shapes':[r for r in rows if r['mnemonic'] in ('div','idiv')],
      'explicit_memory_write_shapes':[r for r in rows if any(o.get('kind')=='memory' and o.get('decoder_write') for o in r['operands'])],
      'opaque_call_sites':[r['site_rva'] for r in rows if r['mnemonic']=='call'],
      'raw_decoder_sources_without_architecture_overlay':True,'memory_contents_alias_and_opaque_callee_effects_known':False,
      'actual_written_count_close_flush_or_persistence_proven':False}
