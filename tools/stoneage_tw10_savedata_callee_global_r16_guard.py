"""Fail-closed exact R16 original-derived static boundaries and artifact custody."""
import argparse,json
from pathlib import Path
SCHEMA="tw10-r16-original-bounded-callee-and-third-global"
STATUS="PINNED_ORIGINAL_CONDITIONAL_HELPER_AND_GLOBAL_REFERENCES_EFFECTS_OPEN"
FLAGS=["call_arguments_resolved","call_results_resolved","caller_context_equivalence_proven","callee_effects_admitted","actual_function_entries_proven","global_runtime_initialization_proven","global_actual_value_proven","original_native_io_proven","original_save_format_proven","heapalloc_ownership_proven","original_bytes_published"]
EXPECTED_ROOTS=[(0x484c0,144,5,"unsupported_memory",False,[(0x484c7,None)]),
                (0x49900,80,5,"unsummarized_call",False,[(0x49909,0x4e2a8),(0x49912,0x4e2e1)]),
                (0x4a09c,80,21,"unsummarized_call",False,[(0x4a0c4,None),(0x4a0f8,None)]),
                (0x4a14d,80,22,"alias_write",True,[(0x4a17d,None)])]
CALL_SITES=[[0x49444,0x484c0],[0x4945d,0x484c0],
            [0x4946f,0x49900],[0x49e5f,0x4a09c],[0x49e6e,0x4a14d]]
GLOBAL_SITES=[("write_candidate",0x49a2c),("write_candidate",0x49d78),
              ("read_candidate",0x49de3),("write_candidate",0x49e88)]
EXPECTED_KEYS=set(FLAGS)|{"schema","status","runtime_sha256","savedata_sha256",
    "r15_source_call_sites","r15_upstream_global_rva","callee_frontiers",
    "third_global_references","static_only","callee_summaries_not_context_qualified"}
def unique(pairs):
    out={}
    for k,v in pairs:
        if k in out:raise ValueError("duplicate field")
        out[k]=v
    return out

def validate(raw):
    if not isinstance(raw,str) or len(raw.encode("utf-8"))>65000:
        raise ValueError("oversized report")
    try:doc=json.loads(raw,object_pairs_hook=unique)
    except (TypeError,ValueError) as e:raise ValueError("invalid JSON") from e
    if type(doc) is not dict or set(doc)!=EXPECTED_KEYS:raise ValueError("root keys")
    if doc["schema"]!=SCHEMA or doc["status"]!=STATUS:raise ValueError("original schema")
    if doc["runtime_sha256"]!="cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a" or doc["savedata_sha256"]!="5b26f54a9723cd2c5275f964457094fdf1fc33ca086cdaf55bb5350dfb04f3f9":
        raise ValueError("original SHA256")
    if any(doc[f] is not False for f in FLAGS) or doc["static_only"] is not True or doc["callee_summaries_not_context_qualified"] is not True:
        raise ValueError("forbidden runtime/effect promotion")
    if doc["r15_source_call_sites"]!=CALL_SITES or doc["r15_upstream_global_rva"]!=0x172186c:
        raise ValueError("R15 pinned sites/global changed")
    fronts=doc["callee_frontiers"]
    if type(fronts) is not list or len(fronts)!=len(EXPECTED_ROOTS):
        raise ValueError("callee count")
    for row,(root,cap,visited,gap,cycle,sites) in zip(fronts,EXPECTED_ROOTS):
        if type(row) is not dict or set(row)!={"root_rva","state_cap","summary",
            "function_entry_proven","original_callee_effects_admitted",
            "calling_convention_proven","caller_specific_values_proven",
            "original_runtime_path_proven"}:
            raise ValueError("callee keys")
        if row["root_rva"]!=root or row["state_cap"]!=cap or any(row[k] is not False for k in (
            "function_entry_proven","original_callee_effects_admitted",
            "calling_convention_proven","caller_specific_values_proven",
            "original_runtime_path_proven")):
            raise ValueError("callee status")
        summary=row["summary"]
        if type(summary) is not dict or set(summary)!={"common_preserved_registers",
            "control_flow_cycle","gap_sites","gaps","native_io_executed",
            "original_helper_accepted","qualifies_modeled_return_effect_summary",
            "return_paths","root_rva","schema","state_limit_hit",
            "uniform_ret_cleanup_bytes","visited_states"}:
            raise ValueError("summary keys")
        if summary["root_rva"]!=root or summary["schema"]!="tw10-r8-bounded-helper-return-effects" or summary["visited_states"]!=visited or summary["state_limit_hit"] is not False or summary["control_flow_cycle"] is not cycle:
            raise ValueError("original bounded state/cycle")
        if any(summary[k] is not False for k in ("native_io_executed",
             "original_helper_accepted","qualifies_modeled_return_effect_summary")):
            raise ValueError("unsafe summary promotion")
        if summary["return_paths"]!=[] or summary["common_preserved_registers"]!=[] or summary["uniform_ret_cleanup_bytes"] is not None:
            raise ValueError("return path invented")
        if summary["gaps"]!={gap:len(sites)}:
            raise ValueError("gap evidence")
        if summary["gap_sites"]!=[
            {"direct_target_rva":target,"occurrences":1,"reason":gap,"rva":site}
            for site,target in sites]:
            raise ValueError("nested original gap sites")
    scan=doc["third_global_references"]
    if type(scan) is not dict or set(scan)!={"all_indirect_references_covered",
         "decode_gap_bytes","decoded_instructions","globals","scope","text_bytes"}:
        raise ValueError("reference scan keys")
    if scan["scope"]!="linear_text_decode_candidates_not_reachable_execution" or scan["all_indirect_references_covered"] is not False or (scan["decoded_instructions"],scan["decode_gap_bytes"],scan["text_bytes"])!=(104229,8,331776):
        raise ValueError("static text reference universe")
    if type(scan["globals"]) is not list or len(scan["globals"])!=1:
        raise ValueError("global count")
    g=scan["globals"][0]
    if type(g) is not dict or set(g)!={"counts","global_rva",
        "runtime_initialization_proven","samples","samples_truncated"}:
        raise ValueError("global fields")
    if g["global_rva"]!=0x172186c or g["runtime_initialization_proven"] is not False or g["samples_truncated"] is not False:
        raise ValueError("unknown global initiation")
    if g["counts"]!={"address_candidate":0,"read_candidate":1,
                       "unknown_candidate":0,"write_candidate":3}:
        raise ValueError("candidate evidence counts")
    if g["samples"]!=[{"kind":kind,"rva":site} for kind,site in GLOBAL_SITES]:
        raise ValueError("exact original global references")
    return {"callee_count":4,"original_qualified_callees":0,
            "global_write_candidates":3,"native_io_executed":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--report",type=Path,required=True)
    print(json.dumps(validate(p.parse_args().report.read_text()),sort_keys=True))
if __name__=="__main__":
    main()
