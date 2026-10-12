#!/usr/bin/env python3
"""Conditional static filename provenance until unsummarized CALL/alias gaps.

No arbitrary call-return ABI assumption: caller continuation stops at CALL.
Direct callees are entered with the modeled physical stack and return address.
Branch outcomes remain conditional; no original execution or bytes are emitted.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque, Counter
import argparse
import json
from pathlib import Path
import tempfile
from capstone import CS_GRP_CALL, CS_GRP_JUMP, CS_GRP_RET
from capstone.x86 import X86_OP_REG, X86_OP_MEM, X86_OP_IMM, X86_REG_ESP, X86_REG_EBP, X86_REG_INVALID
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder, direct_target, first_transfer
from tools.stoneage_tw10_savedata_instruction_probe import (
    RUNTIME_SHA256,SAVEDATA_SHA256,WORD_RVAS,EXPECTED_STRING_RVA,verify_hash,validate_word)
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row

MAX_STATES=2048
MAX_DEPTH=6
MAX_SLOTS=16
MAX_EVENTS=64
SCHEMA='tw10-savedata-r7-conditional-filename-prefix'
STATUS='STATIC_PREFIX_ARGUMENT_CANDIDATES_NATIVE_IO_OPEN'
FILENAME=('filename',0)
UNKNOWN=None
STOP_NAMES={'decode_gap','unsupported_stack','unsupported_memory','unresolved_transfer',
            'call_return_summary_missing','depth_limit','return','terminal','alias_write','outside_text'}

@dataclass
class State:
    regs: dict=field(default_factory=lambda:{X86_REG_ESP:('stack',0)})
    cells: dict=field(default_factory=lambda:{4:FILENAME})
    def clone(self): return State(dict(self.regs),dict(self.cells))
    def signature(self): return (tuple(sorted(self.regs.items())),tuple(sorted(self.cells.items())))


def address(op,state):
    m=op.mem
    if m.segment!=X86_REG_INVALID or m.index!=X86_REG_INVALID: return None
    value=state.regs.get(m.base)
    if value and value[0]=='stack': return value[1]+int(m.disp)
    return None


def value(op,state,target_va):
    if op.size!=4: return None
    if op.type==X86_OP_REG: return state.regs.get(op.reg)
    if op.type==X86_OP_IMM: return FILENAME if int(op.imm)&0xffffffff==target_va else None
    if op.type==X86_OP_MEM:
        pos=address(op,state)
        return state.cells.get(pos) if pos is not None else None
    return None


def put(op,val,state):
    if op.size!=4: return False
    if op.type==X86_OP_REG:
        if val is None: state.regs.pop(op.reg,None)
        else: state.regs[op.reg]=val
        return True
    if op.type==X86_OP_MEM:
        pos=address(op,state)
        if pos is None: return False
        # Overlapping writes invalidate all affected cells, including unaligned.
        for cell in list(state.cells):
            if cell<pos+4 and cell+4>pos: del state.cells[cell]
        if val is not None: state.cells[pos]=val
        return True
    return False


def stack(state):
    sp=state.regs.get(X86_REG_ESP)
    return sp[1] if sp and sp[0]=='stack' else None


def strict_import(ins,imports):
    if ins.mnemonic not in ('call','jmp') or len(ins.operands)!=1: return None
    o=ins.operands[0]
    if (o.type==X86_OP_MEM and o.size==4 and o.mem.segment==X86_REG_INVALID
        and o.mem.base==X86_REG_INVALID and o.mem.index==X86_REG_INVALID):
        return imports.get(int(o.mem.disp)&0xffffffff)
    return None


def step(ins,state,target_va):
    """Modeled copies/frame arithmetic only; unknown alias stores stop the path."""
    s=state.clone(); ops=ins.operands; name=ins.mnemonic
    if name=='push' and len(ops)==1 and ops[0].size==4:
        sp=stack(s)
        if sp is None: return None,'unsupported_stack'
        val=value(ops[0],s,target_va); sp-=4
        for cell in list(s.cells):
            if cell<sp+4 and cell+4>sp: del s.cells[cell]
        if val is not None: s.cells[sp]=val
        s.regs[X86_REG_ESP]=('stack',sp); return s,None
    if name=='pop' and len(ops)==1 and ops[0].type==X86_OP_REG and ops[0].reg!=X86_REG_ESP and ops[0].size==4:
        sp=stack(s)
        if sp is None: return None,'unsupported_stack'
        val=s.cells.pop(sp,None)
        put(ops[0],val,s); s.regs[X86_REG_ESP]=('stack',sp+4); return s,None
    if name=='mov' and len(ops)==2:
        val=value(ops[1],s,target_va)
        if put(ops[0],val,s):
            if stack(s) is None: return None,'unsupported_stack'
            return s,None
        if ops[0].type==X86_OP_MEM: return None,'alias_write'
    if name=='lea' and len(ops)==2 and ops[0].type==X86_OP_REG and ops[0].size==4 and ops[1].type==X86_OP_MEM:
        pos=address(ops[1],s); put(ops[0],('stack',pos) if pos is not None else None,s)
        return (s,None) if stack(s) is not None else (None,'unsupported_stack')
    if name in ('add','sub') and len(ops)==2 and ops[0].type==X86_OP_REG and ops[0].size==4 and ops[1].type==X86_OP_IMM:
        v=s.regs.get(ops[0].reg)
        if v and v[0]=='stack':
            delta=int(ops[1].imm)*(1 if name=='add' else -1)
            put(ops[0],('stack',v[1]+delta),s); return s,None
    if name=='leave':
        fp=s.regs.get(X86_REG_EBP)
        if not fp or fp[0]!='stack': return None,'unsupported_stack'
        val=s.cells.pop(fp[1],None)
        if val is None: s.regs.pop(X86_REG_EBP,None)
        else: s.regs[X86_REG_EBP]=val
        s.regs[X86_REG_ESP]=('stack',fp[1]+4); return s,None
    # Capstone register-write widths must be handled conservatively: a partial
    # write cannot retain an old full-register filename/stack pointer label.
    _,writes=ins.regs_access()
    for reg in writes:
        rn=ins.reg_name(reg)
        for known in list(s.regs):
            kn=ins.reg_name(known)
            family={'eax':{'eax','ax','al','ah'},'ebx':{'ebx','bx','bl','bh'},
                    'ecx':{'ecx','cx','cl','ch'},'edx':{'edx','dx','dl','dh'},
                    'esi':{'esi','si'},'edi':{'edi','di'},'ebp':{'ebp','bp'},'esp':{'esp','sp'}}
            if rn==kn or rn in family.get(kn,set()): s.regs.pop(known,None)
    if any(o.type==X86_OP_MEM and o.access & 2 for o in ops): return None,'alias_write'
    if stack(s) is None: return None,'unsupported_stack'
    return s,None


def trace(dec,root,target_va,imports,max_states=MAX_STATES,max_depth=MAX_DEPTH):
    if type(max_states) is not int or not 1<=max_states<=MAX_STATES or type(max_depth) is not int or not 0<=max_depth<=MAX_DEPTH:
        raise ValueError('trace bounds')
    q=deque([(root,0,State())]); seen=set(); calls=set(); apis=set(); gaps=Counter()
    while q and len(seen)<max_states:
        rva,depth,s=q.popleft(); key=(rva,depth,s.signature())
        if key in seen: continue
        if not dec.lo<=rva<dec.hi: gaps['outside_text']+=1; continue
        ins=dec.at(rva)
        if ins is None: gaps['decode_gap']+=1; continue
        seen.add(key)
        if ins.group(CS_GRP_RET): gaps['return']+=1; continue
        if ins.mnemonic in ('int','int3','into','ud2','hlt','iret','iretd'):
            gaps['terminal']+=1; continue
        if ins.group(CS_GRP_CALL) or ins.group(CS_GRP_JUMP):
            sp=stack(s)
            slots=tuple(i for i in range(MAX_SLOTS) if sp is not None and s.cells.get(sp+4*i)==FILENAME)
            imported=strict_import(ins,imports); target=direct_target(ins,dec.base)
            if imported and ins.mnemonic=='jmp':
                # Import tail jump retains the existing CALL return address.
                slots=tuple(i for i in range(MAX_SLOTS) if sp is not None and s.cells.get(sp+4+4*i)==FILENAME)
            if imported:
                if imported[1] in ('CreateFileA','ReadFile','WriteFile'):
                    apis.add((rva,imported[1],depth,slots))
                # Imported return/out-buffer effects are not summarized.
                gaps['call_return_summary_missing']+=1
            elif ins.group(CS_GRP_CALL):
                calls.add((rva,target,depth,slots))
                gaps['call_return_summary_missing']+=1
                if target is None: gaps['unresolved_transfer']+=1
                elif depth>=max_depth: gaps['depth_limit']+=1
                elif sp is not None:
                    child=s.clone()
                    for cell in list(child.cells):
                        if cell<sp and cell+4>sp-4: del child.cells[cell]
                    child.regs[X86_REG_ESP]=('stack',sp-4)
                    q.append((target,depth+1,child))
                else: gaps['unsupported_stack']+=1
            elif target is None: gaps['unresolved_transfer']+=1
            else:
                branch=s.clone()
                for reg in ins.regs_access()[1]: branch.regs.pop(reg,None)
                q.append((target,depth,branch.clone()))
                if ins.mnemonic not in ('jmp','ljmp'): q.append((rva+ins.size,depth,branch.clone()))
            if len(calls)+len(apis)>MAX_EVENTS: raise ValueError('trace event cap')
            continue
        next_state,gap=step(ins,s,target_va)
        if gap: gaps[gap]+=1
        else: q.append((rva+ins.size,depth,next_state))
    return {'visited_states':len(seen),'state_limit_hit':bool(q),
            'gaps':dict(sorted(gaps.items())),
            'calls':[{'rva':rva,'target_rva':target,'depth':d,'filename_stack_slots':list(slots)}
                     for rva,target,d,slots in sorted(calls,key=lambda r:(r[0],r[2],r[1] or -1,r[3]))],
            'api_candidates':[{'rva':rva,'api':api,'depth':d,'filename_stack_slots':list(slots)}
                              for rva,api,d,slots in sorted(apis)],
            'CreateFileA_filename_slot0_candidate':any(api=='CreateFileA' and slots and slots[0]==0 for _,api,_,slots in apis)}


def inspect_verified(runtime,savedata):
    verify_hash(runtime,RUNTIME_SHA256,'sa_3.exe'); verify_hash(savedata,SAVEDATA_SHA256,'savedata.dat')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe'; p.write_bytes(runtime); data,pe,base,sections,imports=image_layout(p)
    t=next(s for s in sections if s['name']=='.text'); raw=data[t['raw']:t['raw']+t['raw_size']]
    if len(raw)!=t['raw_size']: raise ValueError('text truncated')
    dec=Decoder(raw,t['rva'],base)
    for word in WORD_RVAS:
        validate_word(data,sections,word,base+EXPECTED_STRING_RVA)
        first=first_transfer(dec,word-1,base+EXPECTED_STRING_RVA,imports)
        if first['direct_target_rva']!=0x487ba or first['filename_stack_slot']!=0 or first['prefix_nodes']!=2:
            raise ValueError('R6 seed identity changed')
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,
            'savedata_sha256':SAVEDATA_SHA256,'seed_callee_rva':0x487ba,
            'seed':'FOUR_R6_PHYSICAL_STACK_SLOT0_DIRECT_CALLS_ENTER_WITH_FILENAME_AT_ESP_PLUS4',
            'trace':trace(dec,0x487ba,base+EXPECTED_STRING_RVA,imports),
            'actual_path_feasibility_proven':False,'complete_filename_api_link_proven':False,
            'handle_buffer_size_link_proven':False,'native_io_executed':False,
            'fixed_128_byte_schema_proven':False,'original_bytes_published':False}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--bin',type=Path,required=True); args=p.parse_args()
    img,rows,_,_=find_rows(args.bin)
    try:
        paths={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe=Path(td)/'sa_3.exe'; save=Path(td)/'savedata.dat'
            extract_row(img,paths[RUNTIME_PATH],exe); extract_row(img,paths[SAVEDATA_PATH],save)
            report=inspect_verified(exe.read_bytes(),save.read_bytes())
    finally: img.close()
    print(json.dumps(report,sort_keys=True))
if __name__=='__main__': main()
