"""Original-only R9 nested helper/store geometry/intraprocedural loop surface.

Structural CALL fallthroughs assume a return for topology only. They never
resume R7 argument tracing or establish branch feasibility/native memory IO.
"""
from collections import deque
import argparse,json,tempfile
from pathlib import Path
from capstone import CS_GRP_CALL,CS_GRP_JUMP,CS_GRP_RET
from capstone.x86 import X86_OP_MEM,X86_REG_INVALID
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder,direct_target
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_helper_original_r8 import inspect_verified as inspect_r8,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row
ROOT=0x4b8a4
NESTED=0x4918f
STORE=0x4b903
MAX_NODES=256
MAX_SPAN=1024
SCHEMA='tw10-r9-original-helper-frontier'
STATUS='PINNED_ORIGINAL_NESTED_HELPER_STORE_AND_LOOP_SURFACE_ONLY'

def region_for_va(sections,base,va):
    rva=(va & 0xffffffff)-base
    for s in sections:
        if s['rva']<=rva<s['rva']+max(s['raw_size'],s['vsize']):
            return {'section':s['name'],'displacement_rva':rva,
                    'raw_backed':rva-s['rva']<s['raw_size'],
                    'writable':bool(s.get('characteristics',0)&0x80000000)}
    return None

def store_geometry(dec,site,sections):
    ins=dec.at(site)
    # Explicit recognized integer stores; never trust decoder access bits alone.
    if ins is None or ins.mnemonic not in ('mov','xchg','add','sub','and','or','xor','inc','dec'):
        raise ValueError('selected store is not recognized integer write')
    if not ins.operands or ins.operands[0].type!=X86_OP_MEM:raise ValueError('selected store lacks destination memory')
    op=ins.operands[0];m=op.mem
    if m.segment!=X86_REG_INVALID:raise ValueError('segmented store outside R9 geometry')
    displacement=int(m.disp)&0xffffffff
    mapped=region_for_va(sections,dec.base,displacement)
    absolute=m.base==X86_REG_INVALID and m.index==X86_REG_INVALID
    return {'store_rva':site,'write_width_bytes':op.size,
            'base_register':ins.reg_name(m.base) if m.base else None,
            'index_register':ins.reg_name(m.index) if m.index else None,
            'index_scale':int(m.scale),'displacement_region':mapped,
            'absolute_effective_rva':mapped['displacement_rva'] if absolute and mapped else None,
            'effective_address_fully_known':bool(absolute and mapped),
            'table_or_object_ownership_proven':False}

def loop_components(nodes,edges):
    """SCCs in structural address graph; no path-condition execution claim."""
    adjacency={n:[] for n in nodes}
    reverse={n:[] for n in nodes}
    for a,b in edges:
        if a in nodes and b in nodes:adjacency[a].append(b);reverse[b].append(a)
    visited=set();order=[]
    for root in sorted(nodes):
        if root in visited:continue
        stack=[(root,False)]
        while stack:
            n,done=stack.pop()
            if done:order.append(n);continue
            if n in visited:continue
            visited.add(n);stack.append((n,True))
            stack.extend((v,False) for v in adjacency[n] if v not in visited)
    seen=set();out=[]
    for root in reversed(order):
        if root in seen:continue
        component=set();work=[root]
        while work:
            n=work.pop()
            if n in seen:continue
            seen.add(n);component.add(n);work.extend(reverse[n])
        if len(component)>1 or (root,root) in edges:out.append(component)
    return sorted(out,key=lambda c:min(c))

def structural_surface(dec,root,max_nodes=MAX_NODES,span=MAX_SPAN):
    if type(max_nodes) is not int or not 1<=max_nodes<=MAX_NODES or type(span) is not int or not 1<=span<=MAX_SPAN:
        raise ValueError('structural bounds')
    q=deque([root]);nodes={};edges=set();calls=set();branches={};outside=set();indirect=set()
    while q and len(nodes)<max_nodes:
        rva=q.popleft()
        if rva in nodes:continue
        if not root<=rva<root+span or dec.at(rva) is None:outside.add(rva);continue
        ins=dec.at(rva);nodes[rva]=ins
        if ins.group(CS_GRP_RET) or ins.mnemonic in ('int','int3','into','ud2','hlt','iret','iretd'):continue
        succ=[]
        if ins.group(CS_GRP_CALL):
            calls.add(rva);succ.append(rva+ins.size) # CONDITIONAL returned-call topology ONLY.
        elif ins.group(CS_GRP_JUMP):
            target=direct_target(ins,dec.base)
            if target is None:indirect.add(rva)
            else:succ.append(target)
            if ins.mnemonic not in ('jmp','ljmp'):
                branches[rva]={'rva':rva,'condition':ins.mnemonic,'target_rva':target,'fallthrough_rva':rva+ins.size}
                succ.append(rva+ins.size)
        else:succ.append(rva+ins.size)
        for dst in set(succ):edges.add((rva,dst));q.append(dst)
    pending=any(v not in nodes for v in q)
    loops=[]
    for comp in loop_components(set(nodes),edges):
        loops.append({'node_count':len(comp),'min_rva':min(comp),'max_rva':max(comp),
                      'conditional_branches':[branches[n] for n in sorted(comp) if n in branches],
                      'call_return_assumptions':len(comp&calls)})
    return {'root_rva':root,'nodes':len(nodes),'edges':len(edges),'limit_hit':pending,
            'outside_or_decode_gap_count':len(outside),'indirect_jump_count':len(indirect),
            'call_return_assumptions':len(calls),'loops':loops,
            'runtime_loop_conditions_proven':False,'caller_resumption_admitted':False}

def inspect_verified(runtime,savedata):
    r8=inspect_r8(runtime,savedata);h=r8['helper']
    if (h['visited_states']!=44 or len(h['return_paths'])!=2 or h['qualifies_modeled_return_effect_summary']
        or not any(g['rva']==0x4b8e2 and g['direct_target_rva']==NESTED for g in h['gap_sites'])
        or not any(g['rva']==STORE and g['reason']=='alias_write' for g in h['gap_sites'])):
        raise ValueError('accepted original R8 frontier changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,_=image_layout(p)
    for s,raw_sec in zip(sections,pe.sections):s['characteristics']=int(raw_sec.Characteristics)
    t=next(s for s in sections if s['name']=='.text');raw=data[t['raw']:t['raw']+t['raw_size']]
    if len(raw)!=t['raw_size']:raise ValueError('text truncated')
    dec=Decoder(raw,t['rva'],base)
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r8_verified_helper_states':44,'nested_helper':summarize(dec,NESTED),
            'store':store_geometry(dec,STORE,sections),'structural_parent':structural_surface(dec,ROOT),
            'nested_helper_effects_admitted':False,'caller_resumption_admitted':False,
            'filename_api_link_proven':False,'handle_buffer_size_link_proven':False,
            'native_io_executed':False,'fixed_128_byte_schema_proven':False,'original_bytes_published':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--bin',type=Path,required=True);args=p.parse_args()
    img,rows,_,_=find_rows(args.bin)
    try:
        paths={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe=Path(td)/'sa_3.exe';save=Path(td)/'savedata.dat'
            extract_row(img,paths[RUNTIME_PATH],exe);extract_row(img,paths[SAVEDATA_PATH],save)
            report=inspect_verified(exe.read_bytes(),save.read_bytes())
    finally:img.close()
    print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
