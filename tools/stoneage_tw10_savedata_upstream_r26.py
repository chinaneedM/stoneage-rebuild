"""Original R26 CALL-supported contexts; conditional expressions, not runtime.

Direct CALL syntax supports a bounded entry candidate, not all callers or an
executed function. SETE composition and LEA/SHL arithmetic are mathematical
models conditioned on candidate instruction links. They never execute historic
code, evaluate original globals or admit ABI/heap/native-save effects.
"""
import argparse,hashlib,json,tempfile
from pathlib import Path
from capstone.x86 import X86_REG_EFLAGS,X86_OP_REG,X86_OP_MEM,X86_OP_IMM
from tools.stoneage_tw10_savedata_upstream_r25 import inspect_verified as inspect_r25,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_upstream_r25_guard import validate as validate_r25
from tools.stoneage_tw10_savedata_reachdefs_r14 import bounded_graph
from tools.stoneage_tw10_savedata_write_shapes_r17 import candidate_sources,operand_shape
from tools.stoneage_tw10_savedata_provenance_r10 import reaches as flag_reaches,semantic_definition
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row

SCHEMA='tw10-r26-original-call-root-partial-affine-inputs'
STATUS='PINNED_ORIGINAL_CONDITIONAL_STATIC_EXPRESSIONS_NATIVE_IO_OPEN'
PRIOR_SHA256='3f345e590290eb3f30962e4640f3eec23458fc8fa67c22118b7ef832a5595282'
BINDINGS=((0x49864,0x499c3),(0x49e5f,0x4a09c))
CREATE_ROOT=0x499c3;SETE=0x499d0;PUSH=0x499d3
REALLOC_ROOT=0x4a09c;COMPARE=0x4a0ab;LEA=0x4a0af;SHIFT=0x4a0b3;SIZE_PUSH=0x4a0b6
QUERY=((COMPARE,'eax'),(COMPARE,'ecx'),(LEA,'ecx'),(SHIFT,'eax'),(SIZE_PUSH,'eax'))
FLAGS=('actual_function_entries_proven','all_incoming_callers_proven','original_runtime_paths_proven',
       'actual_sete_flags_or_result_known','actual_realloc_global_values_known','abi_argument_roles_proven',
       'actual_heap_allocation_size_or_success_proven','heap_or_crt_owner_proven','caller_effects_admitted',
       'native_filename_handle_buffer_link_proven','native_save_schema_proven','native_io_executed','original_bytes_published')

def conditional_sete_model(before):
    tokens=before.get('reaching_candidates',[])
    zero=(before.get('query_site_in_candidate_graph') is True and before.get('candidates_truncated') is False
          and len(tokens)==1 and tokens[0].get('origin')=='definition'
          and (tokens[0].get('semantic') or {}).get('kind')=='constant_assignment'
          and tokens[0]['semantic'].get('constant')==0 and tokens[0]['semantic'].get('width_bits')==32)
    return {'kind':'conditional_eax_low_byte_sete','preserved_mask':4294967040,'condition_flag':'zf',
            'low_byte_choices':[0,1],'pre_eax_unique_zero_candidate':zero,
            'conditional_possible_values':[0,1] if zero else None,
            'whole_runtime_value_known':False,'abi_or_heap_flag_role_proven':False}

def eval_sete_model(eax,zf):
    """Synthetic-only reference arithmetic, never invoked on original state."""
    return ((eax&0xffffff00)|(1 if zf else 0))&0xffffffff

def graph_meta(dec,root):
    nodes,edges,front,cap=bounded_graph(dec,root,max_span=192,max_nodes=128)
    return nodes,edges,{'root_rva':root,'nodes':len(nodes),'edges':len(edges),'node_cap':cap,
                         'frontier':[{'reason':why,'rva':at} for why,at in front],
                         'entry_or_executed_path_proven':False,'structural_call_return_assumption_only':True}

def create_context(dec,sections,root=CREATE_ROOT,site=SETE,push=PUSH):
    ins=dec.at(site)
    if (ins is None or ins.mnemonic not in ('sete','setz') or len(ins.operands)!=1
        or ins.operands[0].type!=X86_OP_REG or ins.reg_name(ins.operands[0].reg)!='al'
        or ins.operands[0].size!=1):raise ValueError('R26 SETE AL identity')
    nodes,edges,meta=graph_meta(dec,root)
    if site not in nodes or push not in nodes:raise ValueError('R26 supported create context misses SETE/PUSH')
    tokens=sorted(flag_reaches(nodes,edges,root,X86_REG_EFLAGS).get(site,()),key=lambda t:(t[1],t[0]))
    before=candidate_sources(dec,site,'eax',sections,root)
    return {'graph':meta,'sete_rva':site,'push_rva':push,
            'destination':operand_shape(ins,ins.operands[0],sections,dec.base),
            'eax_before_sete':before,'eax_before_push':candidate_sources(dec,push,'eax',sections,root),
            'flag_sources':[{'origin':kind,'rva':at,'semantic':semantic_definition(nodes[at],X86_REG_EFLAGS,sections,dec.base) if kind=='definition' else None} for kind,at in tokens[:24]],
            'flag_sources_truncated':len(tokens)>24,'conditional_model':conditional_sete_model(before),
            'actual_flag_value_known':False,'call_argument_or_return_effect_admitted':False}

def affine_model(lea,shift,pre_shift):
    a=lea['operands'];b=shift['operands'];tokens=pre_shift.get('reaching_candidates',[])
    linked=(len(tokens)==1 and tokens[0].get('origin')=='definition' and tokens[0].get('rva')==lea['site_rva']
            and pre_shift.get('query_site_in_candidate_graph') is True and pre_shift.get('candidates_truncated') is False)
    geom=a[1].get('geometry',{}) if len(a)==2 else {}
    qualified=(linked and lea['class']=='lea' and shift['class'] in ('shl','sal') and len(a)==2 and len(b)==2
               and a[0].get('register')=='eax' and a[0].get('width_bytes')==4 and a[1].get('kind')=='memory'
               and geom.get('base_register')=='ecx' and geom.get('index_register')=='ecx'
               and geom.get('segment_register') is None and geom.get('displacement_region') is None
               and geom.get('index_scale') in (1,2,4,8)
               and type(geom.get('relative_field_offset')) is int and b[0].get('register')=='eax'
               and b[0].get('width_bytes')==4 and b[1].get('kind')=='immediate')
    count=(b[1]['constant']&31) if qualified else None
    factor=(1<<count) if qualified else None
    return {'kind':'conditional_ecx_affine_u32' if qualified else 'unqualified_composition',
            'unique_lea_to_shift_candidate':linked,'shift_count':count,'modulus':4294967296 if qualified else None,
            'multiplier':((1+geom['index_scale'])*factor)&0xffffffff if qualified else None,
            'bias':(geom['relative_field_offset']*factor)&0xffffffff if qualified else None,
            'evaluated_original_result':None,'actual_ecx_value_known':False,'allocation_size_or_abi_role_proven':False}

def realloc_context(dec,sections,root=REALLOC_ROOT,queries=QUERY,lea_site=LEA,shift_site=SHIFT):
    nodes,edges,meta=graph_meta(dec,root)
    rows=[{'site_rva':site,'register':reg,'candidate_source':candidate_sources(dec,site,reg,sections,root),
           'actual_value_known':False} for site,reg in queries]
    def shape(at):
        ins=dec.at(at)
        if ins is None or at not in nodes:raise ValueError('R26 scalar missing from supported graph')
        return {'site_rva':at,'class':ins.mnemonic,'operands':[operand_shape(ins,o,sections,dec.base) for o in ins.operands]}
    lea,shift=shape(lea_site),shape(shift_site)
    pre=next(q['candidate_source'] for q in rows if (q['site_rva'],q['register'])==(shift_site,'eax'))
    return {'graph':meta,'inputs':rows,'lea_shape':lea,'shift_shape':shift,
            'conditional_affine_model':affine_model(lea,shift,pre),
            'actual_comparison_outcome_known':False,'caller_return_or_heap_effect_admitted':False}

def inspect_verified(runtime,savedata):
    prior=inspect_r25(runtime,savedata);validate_r25(prior)
    digest=hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()
    if digest!=PRIOR_SHA256:raise ValueError('R25 exact original report changed')
    calls={(r['site_rva'],r['target_rva']) for r in prior['linear_boundary_callers']['samples'] if r['kind']=='call'}
    if not set(BINDINGS)<=calls:raise ValueError('R25 direct CALL candidate support changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for sec,raw in zip(sections,pe.sections):sec['characteristics']=int(raw.Characteristics)
    t=next(s for s in sections if s['name']=='.text');dec=Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base)
    binding=[]
    for site,root in BINDINGS:
        identity=call_identity(dec,site,imports,sections)
        if identity['kind']!='direct' or identity['direct_target_rva']!=root:raise ValueError('R26 original CALL identity')
        binding.append({'call_rva':site,'target_candidate_rva':root,'identity':identity,'supported_by_r25_original_scan':True,
                        'runtime_entry_or_call_effect_admitted':False})
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r25_exact_original_revalidated':True,'r25_exact_report_sha256':digest,'static_only':True,
            'caller_bindings':binding,'create_context':create_context(dec,sections),
            'realloc_context':realloc_context(dec,sections),**{k:False for k in FLAGS}}

def main():
    p=argparse.ArgumentParser();p.add_argument('--bin',type=Path,required=True)
    image,rows,_,_=find_rows(p.parse_args().bin)
    try:
        files={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe,saved=Path(td)/'sa_3.exe',Path(td)/'savedata.dat'
            extract_row(image,files[RUNTIME_PATH],exe);extract_row(image,files[SAVEDATA_PATH],saved)
            report=inspect_verified(exe.read_bytes(),saved.read_bytes())
    finally:image.close()
    print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
