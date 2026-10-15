"""Independent all-path caller ESP algebra, separate from concrete R56 model."""
import argparse,json
from collections import deque
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r56 import validate as primary

def geometry(rows,edges,root,helper_delta=-4132,opaque_stack_preserved=False):
    by={r['site_rva']:r for r in rows};adj={a:[] for a in by}
    if root not in by or len(by)!=len(rows) or len(rows)>256:raise ValueError('R56 algebra inventory')
    for a,b in edges:
        if a not in by or b not in by:raise ValueError('R56 algebra edge')
        adj[a].append(b)
    states={root:0};q=deque([root]);steps=0
    while q and steps<8192:
        at=q.popleft();r=by[at];m=r['mnemonic'];o=r['operands'];delta=0
        if m=='call':delta=helper_delta if at==0x40025 else 0 if at==0x4005a or opaque_stack_preserved is True else None
        elif m in ('push','pop'):
            delta=(-4 if m=='push' else 4) if len(o)==1 and o[0]['width_bytes']==4 and not(m=='pop' and o[0].get('register')=='esp') else None
        elif m in ('add','sub') and len(o)==2 and o[0].get('register')=='esp':
            v=o[1].get('constant');delta=v*(1 if m=='add' else -1) if type(v) is int and 0<=v<=65536 else None
        elif set(r['decoder_written_registers'])&{'esp','sp','spl'}:delta=None
        value=states[at]+delta if type(states[at]) is int and type(delta) is int else None
        for b in adj[at]:
            new=value if b not in states or states[b]==value else None
            if b not in states or states[b]!=new:states[b]=new;q.append(b)
        steps+=1
    if q:raise ValueError('R56 algebra update bound')
    return states

def validate(d,raw54,raw55):
    primary(d,raw54,raw55);rows=d['complete_caller_instruction_shapes'];edges=d['caller_bounded_edges'];states=geometry(rows,edges,0x40020,opaque_stack_preserved=True)
    if set(states)!={r['site_rva'] for r in rows}:raise ValueError('R56 algebra reachability')
    for w in d['invented_verification']['witness_preinstruction_esp_relative_entry']:
        if states[w['site_rva']]!=w['esp_delta']:raise ValueError('R56 algebra concrete-witness mismatch')
    for r in rows:
        if r['mnemonic']=='ret' and states[r['site_rva']]!=0:raise ValueError('R56 conditional caller exit geometry')
    unknown=geometry(rows,edges,0x40020)
    if unknown[0x40069] is None or any(unknown[a] is not None for a in (0x40080,0x40090,0x40095)):raise ValueError('R56 unknown opaque stack propagation')
    return len(states)

def main():
    p=argparse.ArgumentParser();p.add_argument('--r54',type=Path,required=True);p.add_argument('--r55',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    if any(x.stat().st_size>1000000 for x in (a.r54,a.r55,a.report)):raise ValueError('R56 algebra input bound')
    n=validate(json.loads(a.report.read_text()),a.r54.read_bytes(),a.r55.read_bytes());print('TW10_R56_INDEPENDENT_CALLER_ALGEBRA=PASS; SITES='+str(n)+'; ACTUAL_NATIVE_PERSISTENCE=OPEN')
if __name__=='__main__':main()
