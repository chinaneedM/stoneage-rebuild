"""R59 derived-only bounded CFG witness; no original execution or native semantics."""
import argparse, hashlib, json
from pathlib import Path
from collections import deque
SHA="04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8"
SCHEMA="tw10-r59-structural-native-and-close-bypass-witness"

def need(cond,msg):
    if not cond: raise ValueError("R59 "+msg)

def path(c,ret,required=(),excluded=()):
    nodes=c["bounded_node_rvas"]; root=c["root_candidate_rva"]
    need(len(nodes)==len(set(nodes)) and root in nodes and ret in nodes,"nodes")
    need(not (set(required)&set(excluded)) and set(required+tuple(excluded))<=set(nodes),"scope")
    adj={a:[] for a in nodes}
    for a,b in c["bounded_edges"]:
        need(a in adj and b in adj and b not in adj[a],"edge")
        adj[a].append(b)
    for values in adj.values(): values.sort()
    bits={a:1<<i for i,a in enumerate(sorted(required))}
    q=deque([(root,bits.get(root,0))]); prev={q[0]:None}
    target=(1<<len(bits))-1
    while q:
        x=q.popleft();a,mask=x
        if a==ret and mask==target:
            out=[]
            while x is not None: out.append(x[0]);x=prev[x]
            return list(reversed(out))
        for b in adj[a]:
            if b in excluded: continue
            nxt=(b,mask|bits.get(b,0))
            if nxt not in prev: prev[nxt]=(a,mask);q.append(nxt)
    return None

def derive(d):
    need(d.get("schema")=="tw10-r58-original-rooted-shared-close-helper-static-inventory" and d.get("static_only") is True,"source")
    for flag in ("native_code_executed","original_bytes_published","actual_native_flush_close_or_persistence_proven","actual_helper_result_or_error_convention_proven"):
        need(d.get(flag) is False,"native claim "+flag)
    cs=d.get("contexts",[])
    need(len(cs)==2 and [c["root_candidate_rva"] for c in cs]==[0x4a657,0x4a53e],"roots")
    for c in cs:
        g=c["graph"]
        need(c["bounded_graph_complete"] is True and g["frontier"]==[] and g["node_limit_hit"] is False and g["nodes"]==len(c["bounded_node_rvas"]) and g["edges"]==len(c["bounded_edges"]) and c["actual_path_or_callee_effects_proven"] is False,"bounded graph")
    shared,close=cs
    for c,ret in ((shared,0x4a6b2),(close,0x4a5f0)):
        need(any(r["site_rva"]==ret and r["mnemonic"]=="ret" for r in c["instruction_shapes"]),"RET")
    calls={x["site_rva"]:x["identity"] for x in shared["call_contexts"]}
    need(calls[0x4a683]["kind"]=="direct" and calls[0x4a683]["direct_target_rva"]==0x4c5b4,"native candidate")
    indirects=[x["site_rva"] for x in close["call_contexts"] if x["identity"]["kind"]=="memory_indirect" and x["identity"].get("direct_target_rva") is None]
    need(indirects==[0x4a5a3,0x4a5ad],"indirect barriers")
    via=path(shared,0x4a6b2,required=(0x4a683,))
    bypass=path(shared,0x4a6b2,excluded=(0x4a683,))
    no_indirect=path(close,0x4a5f0,excluded=tuple(indirects))
    each={hex(a):path(close,0x4a5f0,required=(a,)) for a in indirects}
    need(via is not None and bypass is not None and no_indirect is not None and all(each.values()),"graph structural alternatives")
    return {"schema":SCHEMA,"source_sha256":SHA,"shared_root":0x4a657,
      "native_candidate_target":0x4c5b4,"native_call_site":0x4a683,
      "shared_path_through_native_call":via,"shared_path_bypassing_native_call":bypass,
      "close_root":0x4a53e,"indirect_opaque_sites":indirects,
      "close_path_bypassing_both_indirect_calls":no_indirect,
      "close_paths_visiting_each_indirect_call":each,
      "call_fallthrough_structural_assumption_only":True,
      "branch_predicates_or_actual_path_feasibility_proven":False,
      "native_WriteFile_called_result_flush_close_persistence_proven":False,
      "original_code_or_Windows_API_executed":False}

def load(raw):
    need(len(raw)==124989 and hashlib.sha256(raw).hexdigest()==SHA,"immutable report digest")
    return derive(json.loads(raw))

def main():
    p=argparse.ArgumentParser();p.add_argument("--r58",type=Path,required=True);p.add_argument("--verify",type=Path)
    a=p.parse_args();d=load(a.r58.read_bytes())
    if a.verify:
        need(json.dumps(d,sort_keys=True)==json.dumps(json.loads(a.verify.read_text()),sort_keys=True),"replay changed")
        print("TW10_R59_STATIC_STRUCTURAL_BYPASS=PASS; NATIVE_PERSISTENCE=OPEN")
    else:print(json.dumps(d,sort_keys=True))
if __name__=="__main__":main()
