"""R25 original boundary/caller candidates and SETE/new-anchor provenance.

The complete raw .text linear decode is still a candidate universe, not executed
instructions or verified function ownership. Decode gaps, indirect callers and
opaque CALL effects remain explicit. No historical program or raw payload leaves
this nonexecuting probe. No ABI, native-save, CRT or heap-owner promotion.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from capstone import CS_GRP_CALL,CS_GRP_JUMP
from capstone.x86 import X86_OP_REG,X86_REG_EFLAGS
from tools.stoneage_tw10_savedata_upstream_r24 import (
    inspect_verified as inspect_r24,prefix_audit,RUNTIME_SHA256,SAVEDATA_SHA256)
from tools.stoneage_tw10_savedata_upstream_r24_guard import validate as validate_r24
from tools.stoneage_tw10_savedata_reachdefs_r14 import bounded_graph
from tools.stoneage_tw10_savedata_write_shapes_r17 import candidate_sources,operand_shape
from tools.stoneage_tw10_savedata_provenance_r10 import reaches as flag_reaches,semantic_definition
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder,direct_target
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row

SCHEMA='tw10-r25-original-boundary-callers-sete-inputs'
STATUS='PINNED_ORIGINAL_CONDITIONAL_STATIC_ONLY_NATIVE_IO_OPEN'
PRIOR_SHA256='71a781bd740845d388284ea68fa3e271ef5c5b6eac556f4e487d4eaaa0047af1'
RANGES=((0x499a0,0x49a20),(0x4a050,0x4a0b4))
BOUNDARIES=(0x499ff,0x49a00,0x4a0a1,0x4a0a0,0x499d0,0x4a0af,0x4a0b3)
STARTS=(("HeapAlloc",0x499ff,0x49a0c),("HeapReAlloc",0x4a0a1,0x4a0c4))
SETE=0x499d0
PUSH=0x499d3
SETE_ANCHORS=(0x499b0,0x499c0)
MAX_SAMPLES=64
FLAGS=('true_function_entries_proven','all_incoming_callers_proven','linear_decode_is_execution',
       'original_runtime_path_proven','stack_abi_roles_proven','full_sete_eax_result_known',
       'shifted_ecx_runtime_value_known','heap_owner_or_success_proven','caller_effects_admitted',
       'native_filename_io_link_proven','native_save_schema_proven','native_io_executed',
       'original_bytes_published')

def linear_boundary_callers(dec,boundaries=BOUNDARIES,ranges=RANGES):
    if len(boundaries)>32 or len(set(boundaries))!=len(boundaries):raise ValueError('R25 boundary cap/duplicate')
    if len(ranges)>4 or any(b<=a for a,b in ranges):raise ValueError('R25 target range')
    spans={q:None for q in boundaries};samples=[];count=0;indirect=0;decoded=0;gap=0;pos=dec.lo
    while pos<dec.hi:
        ins=dec.at(pos)
        if ins is None:gap+=1;pos+=1;continue
        end=pos+ins.size;decoded+=1
        for q in boundaries:
            if pos<=q<end:spans[q]={'query_rva':q,'instruction_start_rva':pos,'instruction_end_rva':end,'is_linear_decode_boundary':q==pos}
        if ins.group(CS_GRP_CALL) or ins.group(CS_GRP_JUMP):
            target=direct_target(ins,dec.base)
            if target is None:indirect+=1
            elif any(a<=target<b for a,b in ranges):
                count+=1
                if len(samples)<MAX_SAMPLES:
                    kind='call' if ins.group(CS_GRP_CALL) else ('jump' if ins.mnemonic in ('jmp','ljmp') else 'conditional_jump')
                    samples.append({'site_rva':pos,'target_rva':target,'kind':kind,'executed_or_true_entry_proven':False})
        pos=end
    return {'scope':'full_raw_text_linear_candidates_not_executed_paths','text_start_rva':dec.lo,'text_end_rva':dec.hi,'text_bytes':dec.hi-dec.lo,
            'decoded_instructions':decoded,'decode_gap_bytes':gap,'boundary_queries':[spans[q] or {'query_rva':q,'instruction_start_rva':None,'instruction_end_rva':None,'is_linear_decode_boundary':False} for q in boundaries],
            'target_ranges':[{'start_rva':a,'end_rva':b} for a,b in ranges],
            'direct_transfer_candidate_count':count,'samples':samples,'samples_truncated':count>MAX_SAMPLES,
            'indirect_transfers_not_resolved':indirect,'all_incoming_callers_covered':False,
            'complete_runtime_instruction_alignment_proven':False}

def start_probe(dec,sections,name,root,call):
    nodes,edges,front,cap=bounded_graph(dec,root,max_span=192,max_nodes=128)
    return {'name':name,'root_rva':root,'call_rva':call,'nodes':len(nodes),'edges':len(edges),
            'call_in_candidate_graph':call in nodes,'node_cap':cap,
            'frontier':[{'reason':why,'rva':at} for why,at in front],
            'prefix':prefix_audit(dec,sections,root,call),
            'true_entry_or_actual_path_proven':False,'original_stack_values_proven':False}

def sete_frontier(dec,sections,anchors=SETE_ANCHORS,site=SETE,push=PUSH):
    ins=dec.at(site)
    if (ins is None or ins.mnemonic not in ('sete','setz') or len(ins.operands)!=1
        or ins.operands[0].type!=X86_OP_REG or ins.reg_name(ins.operands[0].reg)!='al'
        or ins.operands[0].size!=1):raise ValueError('R25 exact SETE AL identity')
    rows=[]
    for root in anchors:
        nodes,edges,front,cap=bounded_graph(dec,root,max_span=192,max_nodes=128)
        tokens=sorted(flag_reaches(nodes,edges,root,X86_REG_EFLAGS).get(site,()),key=lambda t:(t[1],t[0]))
        rows.append({'anchor_rva':root,'site_in_candidate_graph':site in nodes,'nodes':len(nodes),'edges':len(edges),
                     'node_cap':cap,'flag_sources':[{'origin':kind,'rva':at,'semantic':semantic_definition(nodes[at],X86_REG_EFLAGS,sections,dec.base) if kind=='definition' else None} for kind,at in tokens[:24]],
                     'flag_sources_truncated':len(tokens)>24,
                     'eax_before_partial_write':candidate_sources(dec,site,'eax',sections,root),
                     'eax_before_push':candidate_sources(dec,push,'eax',sections,root),
                     'whole_eax_composed_value_proven':False,'actual_zf_known':False})
    return {'site_rva':site,'push_rva':push,'one_byte_destination':operand_shape(ins,ins.operands[0],sections,dec.base),
            'upper_24_bits_not_written_by_sete':True,'whole_eax_return_or_argument_known':False,'candidate_contexts':rows}

def inspect_verified(runtime,savedata):
    prior=inspect_r24(runtime,savedata);validate_r24(prior)
    digest=hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()
    if digest!=PRIOR_SHA256:raise ValueError('R24 exact original derivative changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,_=image_layout(p)
    for sec,raw in zip(sections,pe.sections):sec['characteristics']=int(raw.Characteristics)
    t=next(s for s in sections if s['name']=='.text')
    dec=Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base)
    queries=[{'site_rva':site,'register':reg,'candidate_source':candidate_sources(dec,site,reg,sections,STARTS[1][1]),'runtime_input_value_proven':False}
             for site,reg in ((0x4a0ab,'eax'),(0x4a0ab,'ecx'),(0x4a0af,'ecx'))]
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r24_exact_original_revalidated':True,'r24_exact_report_sha256':digest,'static_only':True,
            'linear_boundary_callers':linear_boundary_callers(dec),
            'new_start_candidates':[start_probe(dec,sections,*row) for row in STARTS],
            'sete_partial_frontier':sete_frontier(dec,sections),'realloc_new_anchor_inputs':queries,
            **{k:False for k in FLAGS}}

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
