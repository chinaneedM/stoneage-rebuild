"""PET15: bounded native RD control-flow evidence, no original executable execution."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
from collections import Counter, deque

from tools import stoneage_pet_high_first_tw85_special as prev
from tools import stoneage_pet_high_first_tw85_pixels as pix
from tools.stoneage_pet_high_first_tw85_native import MANIFEST, parse_pe

TARGET = pix.ROOT / 'research/pets/PET-HIGH-FIRST-15-TW85-NATIVE-RD-CONTROL-FLOW-R1.json'
ANCHOR = 586653
WINDOW = '260c61375a81adb6c6f79737b8c5496348bc7594c6fd9ff60ef81c1504bcedda'
SCOPE = 'PRESERVED_TW85_NATIVE_STATIC_BOUNDED_RD_CONTROL_FLOW'
MAX_FORWARD = 1536
MAX_BACK = 128


def prior():
    return json.loads(prev.TARGET.read_bytes())


def original(source_root, temp):
    g = json.loads(prev.ALBUM.read_bytes())['programs']['sa.exe']
    entry = next(x for x in json.loads(MANIFEST.read_bytes())['inspection']['inventory']['samples'][0]['files']
                 if Path(x['path']).name == 'sa.exe')
    packed = source_root / entry['path']
    if pix.sha(packed.read_bytes()) != g['packed_sha256']:
        raise ValueError('source packed drift')
    plain = temp / 'pet15-unpacked-sa.exe'
    subprocess.run(['upx','-d','-q','-o',str(plain),str(packed)],check=True,timeout=120)
    raw = plain.read_bytes()
    if pix.sha(raw) != g['unpacked_sha256']:
        raise ValueError('source unpacked drift')
    return raw


def static_probe(raw):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_GRP_JUMP, CS_GRP_RET, CS_GRP_CALL
    from capstone.x86_const import X86_OP_IMM, X86_OP_MEM
    sections = parse_pe(raw)['sections']
    sec = next(x for x in sections if x['virtual_address'] <= ANCHOR < x['virtual_address']+x['raw_size'])
    base = sec['virtual_address']
    body = raw[sec['file_offset']:sec['file_offset']+sec['raw_size']]
    off = ANCHOR-base
    if pix.sha(body[off:off+380]) != WINDOW:
        raise ValueError('PET14 anchor changed')
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True
    low, high = ANCHOR-MAX_BACK, ANCHOR+MAX_FORWARD
    # Traverse only decoded direct branches in bounded original code; do not execute it.
    todo = deque([ANCHOR]); seen = {}; edges = []; exits = []
    while todo:
        at = todo.popleft()
        if at in seen:
            continue
        if not low <= at < high:
            exits.append({'rva':at,'reason':'OUTSIDE_WINDOW'})
            continue
        ins = next(md.disasm(body[at-base:at-base+15], at, count=1),None)
        if ins is None:
            exits.append({'rva':at,'reason':'NOT_DECODED'})
            continue
        seen[at]=ins
        if len(seen)>600:
            raise ValueError('bounded instruction limit')
        following = at+ins.size
        dests=[]
        if ins.group(CS_GRP_RET):
            exits.append({'rva':at,'reason':'RETURN'})
        elif ins.group(CS_GRP_JUMP):
            if ins.operands and ins.operands[0].type==X86_OP_IMM:
                dests.append((ins.operands[0].imm,'BRANCH'))
            else:
                exits.append({'rva':at,'reason':'INDIRECT_JUMP'})
            if ins.mnemonic!='jmp':
                dests.append((following,'FALLTHROUGH'))
        elif ins.mnemonic in ('int3','ud2','hlt'):
            exits.append({'rva':at,'reason':'TERMINAL'})
        else:
            dests.append((following,'FALLTHROUGH'))
        for to,kind in dests:
            edges.append((at,to,kind))
            todo.append(to)
    facts = []
    for at,ins in sorted(seen.items()):
        # Derived operand facts only, not a full disassembly or source bytes.
        if (ins.mnemonic in ('cmp','test','mul','imul','and','shr','shl','sar','sal','movzx','movsx','add','sub','lea')
            or ins.group(CS_GRP_JUMP) or ins.group(CS_GRP_RET) or ins.group(CS_GRP_CALL)
            or ins.mnemonic.startswith(('rep','stos','movs')) or
            (ins.mnemonic=='mov' and any(x.type==X86_OP_MEM for x in ins.operands))):
            ops=[]
            for x in ins.operands:
                if x.type==X86_OP_IMM:
                    ops.append({'imm':x.imm,'size':x.size})
                elif x.type==X86_OP_MEM:
                    ops.append({'base':ins.reg_name(x.mem.base),'index':ins.reg_name(x.mem.index),
                                'disp':x.mem.disp,'scale':x.mem.scale,'size':x.size})
                else:
                    ops.append({'reg':ins.reg_name(x.reg),'size':x.size})
            facts.append({'rva':at,'operation':ins.mnemonic,'operands':ops})
    branches=[{'from':a,'to':b,'kind':k} for a,b,k in edges if k=='BRANCH']
    # Search exact backward 128-byte prefix for potential prologue; candidate only.
    prefix=body[off-MAX_BACK:off]
    prologues=[ANCHOR-MAX_BACK+i for i in range(len(prefix)-2) if prefix[i:i+3]==b'\x55\x8b\xec']
    return {'anchor_rva':ANCHOR,'anchor_window_sha256':WINDOW,
            'bounded_window_sha256':pix.sha(body[off-MAX_BACK:off+MAX_FORWARD]),
            'reachable_instruction_count':len(seen),'operation_counts':dict(Counter(i.mnemonic for i in seen.values())),
            'branch_edges':branches,'exits':sorted(exits,key=lambda x:(x['rva'],x['reason'])),
            'candidate_prologue_rvas':prologues,'operand_facts':facts,
            'original_executable_executed':False}


def build(source_root,temp):
    raw=original(source_root,temp)
    p=prior()
    return {'scope':SCOPE,'source_executable_sha256':pix.sha(raw),
            'prior_receipt_sha256':pix.sha(prev.TARGET.read_bytes()),
            'native':static_probe(raw),
            'prior_special_summary':{'one_extra_zero':sum(x.get('excess_bytes')==1 and x.get('excess_all_zero') is True for x in p['observations'].values()),
              'header_only':sum(x['status']=='HEADER_ONLY_NONPOSITIVE_DIMENSION' for x in p['observations'].values())},
            'native_rendered_pixels_verified':False,'official_pet_master_verified':False,
            'original_assets_published':False,'native_complete_groups_before_interpretation':510}


def verify(report):
    p=prior()
    n=report['native']
    if report['scope']!=SCOPE or report['prior_receipt_sha256']!=pix.sha(prev.TARGET.read_bytes()) or report['source_executable_sha256']!=p['native_static']['unpacked_sha256']:
        raise ValueError('source provenance')
    if n['anchor_rva']!=ANCHOR or n['anchor_window_sha256']!=WINDOW or not 1<=n['reachable_instruction_count']<=600:
        raise ValueError('native bounded anchor')
    if not all(ANCHOR-MAX_BACK<=x['rva']<ANCHOR+MAX_FORWARD for x in n['operand_facts']):
        raise ValueError('unbounded evidence')
    if n['original_executable_executed'] or any(report[k] for k in ('native_rendered_pixels_verified','official_pet_master_verified','original_assets_published')):
        raise ValueError('unsupported promotion')
    if report['prior_special_summary']!={'one_extra_zero':8,'header_only':2} or report['native_complete_groups_before_interpretation']!=510:
        raise ValueError('prior status drift')
    return {'reachable_instructions':n['reachable_instruction_count'],'derived_facts':len(n['operand_facts']),
            'branches':len(n['branch_edges']),'exits':n['exits'],'prior_special_summary':report['prior_special_summary']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path)
    p.add_argument('--temp',type=Path)
    a=p.parse_args()
    r=build(a.source_root,a.temp) if a.source_root else json.loads(TARGET.read_bytes())
    print(json.dumps(verify(r),sort_keys=True))
    if a.source_root:
        TARGET.write_text(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+'\n')

if __name__=='__main__':
    main()
