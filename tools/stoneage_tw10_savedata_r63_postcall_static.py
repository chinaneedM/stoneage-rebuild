"""R63 narrowly scoped TW1.0 original-static post-WriteFile instruction snapshot.

The original runtime is a transient input only; this tool decodes instruction
geometry, never executes PE/Win32 APIs or parses any historical savedata bytes.
No native result, ABI preservation or successful persistence is inferred.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph
from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA="tw10-r63-original-postwritefile-static-operand-window"
ROOT=0x4C5B4
SITES=((0x4C68C,0x4C692),(0x4C6F1,0x4C6F7))
RUNTIME_SHA="cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
BEFORE=32
AFTER=48
MAX_WINDOW_ROWS=48

def need(ok,why):
    if not ok:
        raise ValueError("R63 static postcall evidence: "+why)

def window(nodes,edges,call,post,row):
    """Build a small connected-address snapshot, not an executed CFG path."""
    need(call in nodes and post in nodes and post>call, "both call/post roots in accepted bounded graph")
    hits=sorted(a for a in nodes if call-BEFORE<=a<=post+AFTER)
    need(2<=len(hits)<=MAX_WINDOW_ROWS and call in hits and post in hits,"bounded window")
    local_edges=sorted([list(x) for x in edges if x[0] in hits and x[1] in hits])
    shapes=[row(at) for at in hits]
    need([x["site_rva"] for x in shapes]==hits,"complete local rows")
    for x in shapes:
        need(isinstance(x["mnemonic"],str) and x["mnemonic"] and
             isinstance(x["operands"],list) and
             x["actual_instruction_effect_or_value_known"] is False,
             "raw decoded syntax never asserts original runtime effects")
        need(not any(k in x for k in ("bytes","raw_binary","source_code","original_payload")),
             "no original raw code")
    need(any(a==call and b==post for a,b in local_edges),
         "direct CALL-continuation edge (return assumption only)")
    return {
       "call_rva":call,"postcall_rva":post,
       "window_address_lower":call-BEFORE,
       "window_address_upper":post+AFTER,
       "decoded_instruction_rows":shapes,
       "bounded_local_edges":local_edges,
       "postcall_instruction":next(x for x in shapes if x["site_rva"]==post),
       "syntactic_call_continuation_edge":True,
       "actual_callee_return_or_native_effect_proven":False,
       "actual_eax_return_register_value_proven":False,
       "actual_flags_or_branch_feasibility_proven":False
    }

def inspect_verified(runtime):
    need(hashlib.sha256(runtime).hexdigest()==RUNTIME_SHA,"accepted TW1.0 original runtime SHA256")
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"sa_3.exe"
        p.write_bytes(runtime)
        data,pe,base,sections,imports=image_layout(p)
    for meta,sec in zip(sections,pe.sections):
        meta["characteristics"]=int(sec.Characteristics)
    text=next(s for s in sections if s["name"]==".text")
    dec=Decoder(data[text["raw"]:text["raw"]+text["raw_size"]],text["rva"],base)
    nodes,edges,front,cap=candidate_graph(dec,ROOT)
    need(len(nodes)==139 and len(edges)==156 and not front and not cap,
         "exact accepted R28 bounded native root")
    reports=[]
    for call,post in SITES:
        ins=dec.at(call)
        need(ins is not None and ins.mnemonic=="call" and ins.size==post-call,
             "exact original postcall address")
        ident=call_identity(dec,call,imports,sections)
        need(ident["kind"]=="memory_indirect" and
             ident["import_identity"]=={"dll":"KERNEL32.dll","name":"WriteFile","iat_rva":0x520A4} and
             ident["runtime_target_or_effects_proven"] is False,
             "exact original import slot and unresolved runtime effects")
        result=window(nodes,edges,call,post,
                      lambda at:instruction_row(dec,sections,nodes,at))
        result["import_name"]="WriteFile"
        result["import_slot_rva"]=0x520A4
        result["native_api_result_eax_or_bytecount_proven"]=False
        reports.append(result)
    return {
      "schema":SCHEMA,
      "runtime_sha256":RUNTIME_SHA,
      "original_executable_executed":False,
      "original_savedata_payload_read_or_published":False,
      "candidate_root_rva":ROOT,
      "candidate_graph_nodes":len(nodes),
      "candidate_graph_edges":len(edges),
      "bounded_call_return_assumption_only":True,
      "sites":reports,
      "actual_abi_or_register_stack_memory_preservation_proven":False,
      "actual_native_writefile_return_count_or_success_proven":False,
      "actual_buffer_flush_close_or_disk_persistence_proven":False,
      "original_savedata_schema_migration_or_server_authority_proven":False,
      "next":"Independent immutable derivative guard and reverse predecessor/flag audit; never promote decoded postcall syntax to historical native I/O."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--bin",type=Path,required=True,
                   help="Authenticated original TW1.0 STONEAGE.bin, transient only")
    a=p.parse_args()
    image,rows,_,_=find_rows(a.bin)
    try:
        candidates={r["path"]:r for r in rows if not r["is_dir"]}
        need(RUNTIME_PATH in candidates,"authenticated original runtime file present")
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"sa_3.exe"
            extract_row(image,candidates[RUNTIME_PATH],out)
            result=inspect_verified(out.read_bytes())
    finally:
        image.close()
    print(json.dumps(result,sort_keys=True))

if __name__=="__main__":
    main()
