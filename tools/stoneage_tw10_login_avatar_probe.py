"""Bounded original-binary login/avatar callsite inventory, derived metadata only.

This does not execute the client, draw imagery, infer a complete state machine,
or call a table value a character identity merely because it looks plausible.
"""
from __future__ import annotations
import argparse
import collections
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
            i=c['linear_index']; window=insns[max(0,i-36):i+1]
            # Restrict to the nearest control-flow boundary; this is an observed
            # instruction window, never an assertion that all pushes are args.
            boundary=max((j for j,x in enumerate(window[:-1]) if x.mnemonic=='ret' or x.mnemonic.startswith('j')),default=-1)
            window=window[boundary+1:]
            pushes=[];reads=[]
            for x in window[:-1]:
                if not x.id: continue
                if x.mnemonic=='push':
                    pushes.append({'site_rva':x.address-base,'operand':x.op_str,
                        'immediate':x.operands[0].imm if x.operands[0].type==X86_OP_IMM else None})
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
    return {'schema':'stoneage.tw10.login_avatar.static_callsite.r1',
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
