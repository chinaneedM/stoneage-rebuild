#!/usr/bin/env python3
"""Bounded static first-transfer stack and cross-callee surface. Never runs PE."""
from __future__ import annotations
import argparse
from collections import deque
import json
from pathlib import Path
import tempfile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_GRP_CALL, CS_GRP_JUMP, CS_GRP_RET
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_ESP, X86_REG_INVALID
from tools.stoneage_tw10_savedata_instruction_probe import (
    verify_hash, validate_word, RUNTIME_SHA256, SAVEDATA_SHA256,
    WORD_RVAS, EXPECTED_STRING_RVA)
from tools.stoneage_tw10_savedata_entrygraph_r4 import explore
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import FILE_APIS, RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

MAX_PREFIX = 64
MAX_DEPTH = 4
MAX_NODES = 4096
MAX_EVENTS = 64
SCHEMA = 'tw10-savedata-r6-first-transfer-cross-callee'
STATUS = 'BOUNDED_STATIC_ARGUMENT_CANDIDATES_NOT_NATIVE_IO'
STOPS = {'branch', 'return', 'terminal', 'decode_gap', 'outside_text', 'prefix_limit', 'call'}

class Decoder:
    def __init__(self, raw, text_rva, base):
        self.raw, self.lo, self.hi, self.base = raw, text_rva, text_rva+len(raw), base
        self.md = Cs(CS_ARCH_X86, CS_MODE_32)
        self.md.detail = True
    def at(self, rva):
        if not self.lo <= rva < self.hi:
            return None
        p = rva-self.lo
        ins = next(self.md.disasm(self.raw[p:p+15], self.base+rva, count=1), None)
        return ins if ins and rva+ins.size <= self.hi else None

def direct_target(ins, base):
    if len(ins.operands)==1 and ins.operands[0].type==X86_OP_IMM:
        return (int(ins.operands[0].imm)-base) & 0xffffffff
    return None

def import_transfer(ins, imports):
    # Only actual absolute memory-indirect transfers. Immediate targets are
    # executable addresses, not an IAT dereference; wrappers are explored.
    if ins.mnemonic not in ('call','jmp') or len(ins.operands)!=1:
        return None
    op=ins.operands[0]
    if op.type==X86_OP_MEM and op.mem.base==X86_REG_INVALID and op.mem.index==X86_REG_INVALID:
        return imports.get(int(op.mem.disp) & 0xffffffff)
    return None

def first_transfer(dec, site, target_va, imports, max_prefix=MAX_PREFIX):
    """Physical stack offset only, not a function ABI or interprocedural proof.

    Stop at first control transfer. Invalidate on any memory write or unsupported
    ESP effect; do not infer through branch joins, aliasing, calls or stack frames.
    """
    if type(max_prefix) is not int or not 1<=max_prefix<=MAX_PREFIX:
        raise ValueError('prefix bound')
    first=dec.at(site)
    if (not first or first.mnemonic!='push' or len(first.operands)!=1
            or first.operands[0].type!=X86_OP_IMM
            or (int(first.operands[0].imm)&0xffffffff)!=target_va):
        raise ValueError('site is not expected filename push')
    rva=site+first.size; slot=0; precise=True; count=1
    result={'stop':None,'transfer_rva':None,'direct_target_rva':None,
            'import_api':None,'filename_stack_slot':None,'stack_tracking_precise':False,
            'prefix_nodes':count}
    for _ in range(max_prefix-1):
        ins=dec.at(rva)
        if ins is None:
            result['stop']='outside_text' if not dec.lo<=rva<dec.hi else 'decode_gap'
            break
        count+=1
        if ins.group(CS_GRP_CALL) or ins.group(CS_GRP_JUMP):
            result['stop']='call' if ins.group(CS_GRP_CALL) else 'branch'
            result['transfer_rva']=rva
            result['direct_target_rva']=direct_target(ins,dec.base)
            match=import_transfer(ins,imports)
            result['import_api']=match[1] if match and match[1] in FILE_APIS else None
            break
        if ins.group(CS_GRP_RET):
            result['stop']='return'; break
        if ins.mnemonic in ('int','int3','into','ud2','hlt','iret','iretd'):
            result['stop']='terminal'; break
        if ins.mnemonic=='push' and ins.operands[0].size==4 and precise:
            slot+=1
        elif (ins.mnemonic=='pop' and ins.operands[0].type==X86_OP_REG
              and ins.operands[0].reg!=X86_REG_ESP and ins.operands[0].size==4 and precise):
            slot-=1
            if slot<0: precise=False
        else:
            _, writes=ins.regs_access()
            if X86_REG_ESP in writes or any(op.type==X86_OP_MEM and op.access & 2 for op in ins.operands):
                precise=False
        rva+=ins.size
    else:
        result['stop']='prefix_limit'
    result['prefix_nodes']=count
    # Slots are reported only immediately before CALL, never as branch arguments.
    if result['stop']=='call' and precise and 0<=slot<MAX_PREFIX:
        result['filename_stack_slot']=slot
        result['stack_tracking_precise']=True
    return result

def cross_callee(dec, root, imports, max_nodes=MAX_NODES, max_depth=MAX_DEPTH):
    """Possible direct call/branch surfaces with balanced *depth*, not returns.

    CALL fallthrough is conditional on returning; RET does not connect to callers.
    No address-radius restriction. States include call depth, with bounded recursion.
    File API adjacency is independent of filename/handle/buffer provenance.
    """
    if type(max_nodes) is not int or not 1<=max_nodes<=MAX_NODES or type(max_depth) is not int or not 0<=max_depth<=MAX_DEPTH:
        raise ValueError('cross-callee bounds')
    q=deque([(root,0)]); seen=set(); events={}; gaps=0; depth_stops=0
    while q and len(seen)<max_nodes:
        rva,depth=q.popleft()
        if (rva,depth) in seen: continue
        ins=dec.at(rva)
        if ins is None: continue
        seen.add((rva,depth))
        match=import_transfer(ins,imports)
        if match and match[1] in FILE_APIS:
            key=(rva,match[1])
            events[key]=min(depth,events.get(key,depth))
            if len(events)>MAX_EVENTS: raise ValueError('file API event bound exceeded')
        if ins.group(CS_GRP_RET) or ins.mnemonic in ('int','int3','into','ud2','hlt','iret','iretd'): continue
        if ins.group(CS_GRP_CALL) or ins.group(CS_GRP_JUMP):
            target=direct_target(ins,dec.base)
            if target is None:
                if match is None: gaps+=1
            elif dec.lo<=target<dec.hi:
                if ins.group(CS_GRP_CALL):
                    if depth<max_depth: q.append((target,depth+1))
                    else: depth_stops+=1
                else: q.append((target,depth))
            if ins.group(CS_GRP_CALL) or ins.mnemonic not in ('jmp','ljmp'):
                q.append((rva+ins.size,depth))
        else: q.append((rva+ins.size,depth))
    pending=any(state not in seen and dec.at(state[0]) is not None for state in q)
    return {'visited_states':len(seen),'node_limit_hit':pending,
            'depth_limit_stops':depth_stops,'unresolved_indirect_transfers':gaps,
            'api_events':[{'rva':rva,'api':api,'min_call_depth':depth}
                          for (rva,api),depth in sorted(events.items())]}

def inspect_verified(runtime, savedata):
    verify_hash(runtime,RUNTIME_SHA256,'sa_3.exe')
    verify_hash(savedata,SAVEDATA_SHA256,'savedata.dat')
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/'sa_3.exe'; path.write_bytes(runtime)
        data,pe,base,sections,imports=image_layout(path)
    text=next(s for s in sections if s['name']=='.text')
    raw=data[text['raw']:text['raw']+text['raw_size']]
    if len(raw)!=text['raw_size']: raise ValueError('truncated text')
    graph=explore(raw,text['rva'],base,int(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
    if graph['limit_hit'] or len(graph['visited'])!=31665 or len(graph['edges'])!=35092:
        raise ValueError('accepted R4 graph changed')
    dec=Decoder(raw,text['rva'],base); sites=[]
    for word in WORD_RVAS:
        validate_word(data,sections,word,base+EXPECTED_STRING_RVA)
        site=word-1
        if site not in graph['visited']: raise ValueError('R4 site absent')
        prefix=first_transfer(dec,site,base+EXPECTED_STRING_RVA,imports)
        target=prefix['direct_target_rva']
        surface=cross_callee(dec,target,imports) if target is not None and dec.lo<=target<dec.hi else None
        sites.append({'word_rva':word,'push_rva':site,'first_transfer':prefix,'cross_callee':surface})
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,
            'savedata_sha256':SAVEDATA_SHA256,'sites':sites,
            'filename_api_argument_proven':False,'handle_buffer_size_link_proven':False,
            'native_io_executed':False,'fixed_128_byte_schema_proven':False,
            'original_bytes_published':False}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--bin',type=Path,required=True); args=p.parse_args()
    img,rows,_,_=find_rows(args.bin)
    try:
        paths={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe=Path(td)/'sa_3.exe'; saved=Path(td)/'savedata.dat'
            extract_row(img,paths[RUNTIME_PATH],exe); extract_row(img,paths[SAVEDATA_PATH],saved)
            result=inspect_verified(exe.read_bytes(),saved.read_bytes())
    finally: img.close()
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__': main()
