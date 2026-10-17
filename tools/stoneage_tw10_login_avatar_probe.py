"""Bounded original-binary login/avatar callsite inventory, derived metadata only.

This does not execute the client, draw imagery, infer a complete state machine,
or call a table value a character identity merely because it looks plausible.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import tempfile

RUNTIME_SHA256 = 'cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a'
# String-header xrefs are original observations, not assumed function entries.
ANCHORS = {
 'ClientLogin': (0x19365, 0x2f200),
 'CreateNewChar': (0x193d5, 0x31e90),
 'CharDelete': (0x195c5, 0x31f90),
 'CharLogin': (0x19615, 0x2f530),
 'CharList': (0x19665, 0x2f320),
}

def need(ok, message):
    if not ok: raise ValueError(message)

def select_calls(rows, header_rva, max_back=32):
    """Candidate entry addresses only: no prologue inference from mere proximity."""
    return [r for r in rows if header_rva-max_back <= r['target_rva'] <= header_rva]

def push_source(window, index, base):
    """Syntactic last-register-write source, never an actual memory value.

    Refuse arithmetic, control transfers, calls and non-absolute addressing;
    do not guess through a clobbered register or combine separate paths.
    """
    from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG
    ins=window[index]; op=ins.operands[0]
    if op.type==X86_OP_IMM:
        return {'kind':'immediate_operand','value':op.imm,'runtime_value_verified':False}
    if op.type!=X86_OP_REG:return {'kind':'unresolved','runtime_value_verified':False}
    reg=op.reg
    for prev in reversed(window[:index]):
        if not prev.id or prev.mnemonic=='call' or prev.mnemonic.startswith('j'):
            break
        _,written=prev.regs_access()
        family=lambda n: {'eax':'a','ax':'a','al':'a','ah':'a','ebx':'b','bx':'b','bl':'b','bh':'b','ecx':'c','cx':'c','cl':'c','ch':'c','edx':'d','dx':'d','dl':'d','dh':'d'}.get(n,n)
        if not any(family(prev.reg_name(w))==family(ins.reg_name(reg)) for w in written):continue
        if (prev.mnemonic=='mov' and len(prev.operands)==2 and
            prev.operands[0].type==X86_OP_REG and prev.operands[0].reg==reg):
            src=prev.operands[1]
            if src.type==X86_OP_MEM and not src.mem.base and not src.mem.index and src.mem.disp>=base:
                return {'kind':'absolute_memory_load','load_site_rva':prev.address-base,
                    'address_rva':src.mem.disp-base,'width_bytes':src.size,'runtime_value_verified':False}
            if src.type==X86_OP_IMM:
                return {'kind':'immediate_assignment','load_site_rva':prev.address-base,
                    'value':src.imm,'runtime_value_verified':False}
        break
    return {'kind':'unresolved','runtime_value_verified':False}

def inspect_runtime(runtime):
    need(hashlib.sha256(runtime).hexdigest() == RUNTIME_SHA256, 'unaccepted sa_3.exe SHA256')
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    from capstone.x86 import X86_OP_IMM, X86_OP_MEM
    from tools.stoneage_tw10_mapcache_binary_probe import image_layout, rva_to_offset
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime)
        data, pe, base, sections, imports = image_layout(p)
    text=next(s for s in sections if s['name']=='.text')
    md=Cs(CS_ARCH_X86,CS_MODE_32);md.detail=True
    # Linear sweep stops at invalid instructions; skipdata prevents treating the
    # resulting prefix as the whole executable. Candidates still need CFG review.
    md.skipdata=True
    insns=list(md.disasm(data[text['raw']:text['raw']+text['raw_size']],base+text['rva']))
    calls=[]
    for i, ins in enumerate(insns):
        if ins.id and ins.mnemonic=='call' and ins.operands and ins.operands[0].type==X86_OP_IMM:
            calls.append({'site_rva':ins.address-base,'target_rva':ins.operands[0].imm-base,'linear_index':i})
    groups={}
    for name,(header,callback) in ANCHORS.items():
        candidates=select_calls(calls,header)
        need(bool(candidates), 'no bounded direct sender-call candidates '+name)
        rows=[]
        for c in candidates:
            i=c['linear_index']; window=insns[max(0,i-80):i+1]
            # Restrict to the nearest control-flow boundary; this is an observed
            # instruction window, never an assertion that all pushes are args.
            boundary=max((j for j,x in enumerate(window[:-1]) if x.mnemonic=='ret' or x.mnemonic.startswith('j')),default=-1)
            window=window[boundary+1:]
            pushes=[];reads=[]
            for wi,x in enumerate(window[:-1]):
                if not x.id: continue
                if x.mnemonic=='push':
                    pushes.append({'site_rva':x.address-base,'operand':x.op_str,
                        'immediate':x.operands[0].imm if x.operands[0].type==X86_OP_IMM else None,
                        'static_source':push_source(window,wi,base)})
                for op in x.operands:
                    if op.type==X86_OP_MEM and not op.mem.base and not op.mem.index and op.mem.disp>=base:
                        rva=op.mem.disp-base; off=rva_to_offset(sections,rva)
                        reads.append({'site_rva':x.address-base,'address_rva':rva,'file_backed':off is not None})
            rows.append({'site_rva':c['site_rva'],'target_rva':c['target_rva'],
                'bounded_push_operands':pushes,'absolute_memory_operands':reads,
                'window_instruction_count':len(window),'argument_values_proven':False,
                'candidate_only':True})
        off=rva_to_offset(sections,callback);need(off is not None,'callback not file-backed')
        # Only summarize a bounded prefix's direct calls and branch destinations.
        prefix=list(md.disasm(data[off:off+384],base+callback))
        stop=next((i for i,x in enumerate(prefix) if x.mnemonic=='ret'),len(prefix)-1)
        prefix=prefix[:stop+1]
        callback_calls=[{'site_rva':x.address-base,'target_rva':x.operands[0].imm-base}
            for x in prefix if x.id and x.mnemonic=='call' and x.operands[0].type==X86_OP_IMM]
        groups[name]={'original_header_xref_rva':header,'receive_callback_rva':callback,
            'sender_entry_candidates':sorted(set(r['target_rva'] for r in rows)),
            'sender_callsites':rows,'callback_linear_prefix_direct_calls':callback_calls,
            'callback_prefix_is_complete_cfg':False}
    # These globals are selected by reversed x86 pushes + EARLY_LINEAGE
    # signature only; builder stack-field evidence is emitted independently.
    selectors={}
    for label,target in [('lineage_body_candidate',0x13f719c),('lineage_face_candidate',0x13f79ac)]:
        writers=[]
        for i,ins in enumerate(insns):
            if not ins.id or not ins.operands:continue
            dst=ins.operands[0]
            if dst.type!=X86_OP_MEM or dst.mem.base or dst.mem.index or dst.mem.disp!=base+target:continue
            if not (dst.access & 2):continue
            window=insns[max(0,i-12):i+1]
            boundaries=[j for j,x in enumerate(window[:-1]) if x.mnemonic=='ret' or x.mnemonic.startswith('j')]
            window=window[(max(boundaries)+1 if boundaries else 0):]
            operations=[]
            for x in window:
                if not x.id:continue
                operands=[]
                for op in x.operands:
                    if op.type==X86_OP_IMM:operands.append({'kind':'imm','value':op.imm})
                    elif op.type==X86_OP_MEM:
                        operands.append({'kind':'mem','base':x.reg_name(op.mem.base),'index':x.reg_name(op.mem.index),
                            'scale':op.mem.scale,'displacement':op.mem.disp,'width':op.size})
                    else:operands.append({'kind':'register','name':x.reg_name(op.reg)})
                operations.append({'site_rva':x.address-base,'mnemonic':x.mnemonic,'operands':operands})
            writers.append({'write_site_rva':ins.address-base,'bounded_operand_operations':operations})
        selectors[label]={'address_rva':target,'file_backed':rva_to_offset(sections,target) is not None,
            'write_candidates':writers,'actual_value_verified':False,'semantic_name_evidence':'EARLY_LINEAGE_AND_CDECL_POSITION_CANDIDATE'}
    builder=[]
    off=rva_to_offset(sections,0x193d0)
    body=list(md.disasm(data[off:off+0x1f0],base+0x193d0))
    for i,x in enumerate(body):
        if not x.id or x.mnemonic!='call' or x.operands[0].type!=X86_OP_IMM:continue
        target=x.operands[0].imm-base
        if target not in (0x1b0b0,0x1b0f0):continue
        operands=[]
        for y in body[max(0,i-6):i]:
            if not y.id:continue
            for op in y.operands:
                if op.type==X86_OP_MEM:
                    operands.append({'site_rva':y.address-base,'base':y.reg_name(op.mem.base),
                        'index':y.reg_name(op.mem.index),'displacement':op.mem.disp,'width':op.size})
        builder.append({'callsite_rva':x.address-base,'helper_type':'int' if target==0x1b0b0 else 'string',
            'preceding_memory_operands':operands})
    return {'schema':'stoneage.tw10.login_avatar.static_callsite.r1',
        'builder_field_helper_calls':builder,'avatar_selector_write_candidates':selectors,
        'runtime_sha256':RUNTIME_SHA256,'image_base':base,
        'method':'linear-sweep direct-call candidates within 32 bytes before fixed protocol header xrefs; bounded operand metadata; no complete CFG or runtime trace',
        'protocols':groups,'original_program_executed':False,'historical_screen_layout_verified':False,
        'body_face_selector_values_verified':False,'original_character_roster_complete':False,
        'historical_server_behavior_verified':False,'stage_b_started':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bin',type=Path,required=True);a=ap.parse_args()
    from tools.stoneage_tw10_technical_probe import find_rows,extract_row
    image,rows,_,_=find_rows(a.bin)
    try:
        row=next(r for r in rows if r['path']=='StoneAge/sa_3.exe' and not r['is_dir'])
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'sa_3.exe';extract_row(image,row,p);report=inspect_runtime(p.read_bytes())
    finally:image.close()
    print(json.dumps(report,ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
