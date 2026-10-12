"""Bounded synthetic/verified-static helper return effects, never an ABI guess.

A helper summary can qualify only when every modeled path returns with its
original return word, known stack delta, no omitted CALL/alias/memory effects
and no state cap. This tool alone admits no historical helper or native IO.
"""
from collections import deque,Counter
from capstone import CS_GRP_CALL,CS_GRP_JUMP,CS_GRP_RET
from capstone.x86 import X86_REG_EAX,X86_REG_EBX,X86_REG_ECX,X86_REG_EDX,X86_REG_ESI,X86_REG_EDI,X86_REG_EBP,X86_REG_ESP,X86_OP_IMM,X86_OP_MEM
from tools.stoneage_tw10_savedata_argtrace_r7 import State,step,stack,address,MAX_STATES
from tools.stoneage_tw10_savedata_dataflow_r6 import direct_target
REGISTERS=(X86_REG_EAX,X86_REG_EBX,X86_REG_ECX,X86_REG_EDX,X86_REG_ESI,X86_REG_EDI,X86_REG_EBP)
RETURN_WORD=('return_word',0)
MAX_RETURNS=32
GAPS={'outside_text','decode_gap','unsummarized_call','indirect_jump','terminal',
      'unsupported_return','unsupported_stack','unsupported_memory','alias_write','caller_memory_write'}

def summarize(dec,root,max_states=MAX_STATES):
    if type(max_states) is not int or not 1<=max_states<=MAX_STATES: raise ValueError('state bound')
    initial={r:('initial_register',r) for r in REGISTERS};initial[X86_REG_ESP]=('stack',0)
    q=deque([(root,State(initial,{0:RETURN_WORD}))]);seen=set();returns=set();gaps=Counter();edges=set()
    def enqueue(source,rva,s):
        edges.add((source,(rva,s.signature())));q.append((rva,s))
    while q and len(seen)<max_states:
        rva,s=q.popleft();key=(rva,s.signature())
        if key in seen:continue
        if not dec.lo<=rva<dec.hi:gaps['outside_text']+=1;continue
        ins=dec.at(rva)
        if ins is None:gaps['decode_gap']+=1;continue
        seen.add(key)
        if ins.group(CS_GRP_RET):
            if ins.mnemonic!='ret' or len(ins.operands)>1 or (ins.operands and ins.operands[0].type!=X86_OP_IMM):
                gaps['unsupported_return']+=1;continue
            sp=stack(s);cleanup=int(ins.operands[0].imm) if ins.operands else 0
            kept=tuple(dec.md.reg_name(r) for r in REGISTERS if s.regs.get(r)==initial[r])
            returns.add((rva,sp,cleanup,sp is not None and s.cells.get(sp)==RETURN_WORD,kept))
            if len(returns)>MAX_RETURNS:raise ValueError('return cap')
            continue
        if ins.group(CS_GRP_CALL):gaps['unsummarized_call']+=1;continue
        if ins.mnemonic in ('int','int3','into','ud2','hlt','iret','iretd','sysenter','sysexit','syscall','sysret','in','out'):
            gaps['terminal']+=1;continue
        if ins.group(CS_GRP_JUMP):
            target=direct_target(ins,dec.base)
            if target is None:gaps['indirect_jump']+=1;continue
            branch=s.clone()
            for r in ins.regs_access()[1]:branch.regs.pop(r,None)
            enqueue(key,target,branch.clone())
            if ins.mnemonic not in ('jmp','ljmp'):enqueue(key,rva+ins.size,branch.clone())
            continue
        # Relative addresses >=4 belong to the caller argument/frame region.
        # A register/return-only summary cannot silently omit mutations there.
        caller_write=False
        for op in ins.operands:
            if op.type==X86_OP_MEM and op.access & 2:
                pos=address(op,s)
                if pos is not None and pos+op.size>4: caller_write=True
        if ins.mnemonic=='push' and stack(s) is not None and stack(s)>4:
            caller_write=True
        if caller_write:
            gaps['caller_memory_write']+=1;continue
        n,gap=step(ins,s,None)
        if gap:gaps[gap]+=1
        else:enqueue(key,rva+ins.size,n)
    # Drain-only duplicate states do not count as truncation. Outstanding unseen
    # states still prevent any complete return-effect summary.
    cap=any((rva,s.signature()) not in seen for rva,s in q)
    indegree={v:0 for v in seen};neighbors={}
    for src,dst in edges:
        if src in seen and dst in seen:
            indegree[dst]+=1;neighbors.setdefault(src,[]).append(dst)
    acyclic=deque(v for v,n in indegree.items() if n==0);removed=0
    while acyclic:
        src=acyclic.popleft();removed+=1
        for dst in neighbors.get(src,()):
            indegree[dst]-=1
            if indegree[dst]==0:acyclic.append(dst)
    cycle=removed<len(seen)
    paths=[{'rva':rva,'pre_ret_stack_delta':sp,'ret_cleanup_bytes':cleanup,
            'return_word_preserved':word,'preserved_registers':list(kept)}
           for rva,sp,cleanup,word,kept in sorted(returns,key=lambda v:(v[0],v[1] if v[1] is not None else -1,v[2],v[3],v[4]))]
    qualified=(bool(paths) and not gaps and not cap and not cycle and all(p['pre_ret_stack_delta']==0 and p['return_word_preserved'] for p in paths))
    # Different callee cleanup values cannot be hidden behind one effect summary.
    cleanup_values=sorted({p['ret_cleanup_bytes'] for p in paths})
    qualified=qualified and len(cleanup_values)==1
    common=sorted(set.intersection(*(set(p['preserved_registers']) for p in paths))) if paths else []
    return {'schema':'tw10-r8-bounded-helper-return-effects','root_rva':root,
            'visited_states':len(seen),'state_limit_hit':cap,'control_flow_cycle':cycle,'gaps':dict(sorted(gaps.items())),
            'return_paths':paths,'common_preserved_registers':common,
            'uniform_ret_cleanup_bytes':cleanup_values[0] if len(cleanup_values)==1 else None,
            'qualifies_modeled_return_effect_summary':qualified,
            'original_helper_accepted':False,'native_io_executed':False}
