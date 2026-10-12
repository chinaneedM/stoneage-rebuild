"""Fail-closed R14 source-custody and independently pinned static boundary guard."""
import argparse
import json
from pathlib import Path

SCHEMA = "tw10-r14-bounded-conditional-reaching-definitions"
STATUS = "ORIGINAL_STATIC_BOUNDED_INPUTS_FUNCTION_OWNERSHIP_RUNTIME_OPEN"
FLAGS = ["actual_function_entry_proven","branch_feasibility_proven","caller_effects_admitted","complete_register_values_proven","filename_api_link_proven","fixed_128_byte_schema_proven","frame_or_stack_ownership_proven","global_effects_admitted","global_initialization_proven","handle_buffer_size_link_proven","heapalloc_size_or_ownership_proven","native_io_executed","original_bytes_published"]
EXPECTED_INPUTS = [
    (0x49dec, "ebx", "definition", 0x49de8),
    (0x4943c, "eax", "entry", 0x4943c),
    (0x4944a, "eax", "unknown_call", 0x49444),
    (0x49457, "esi", "unknown_call", 0x49444),
    (0x49463, "eax", "unknown_call", 0x4945d),
]
EXPECTED_ANCHORS = (0x49d93, 0x4943c)
EXPECTED_CALLS = ((0x49e5f, 0x49e6e), (0x49444, 0x4945d, 0x4946f))
# Call barrier counts are checked independently against pinned report below.
EXPECTED_COUNTS = ((139, 158, 27, 2), (48, 53, 6, 3))

def unique_pairs(rows):
    obj={}
    for k,v in rows:
        if k in obj: raise ValueError("duplicate JSON field")
        obj[k]=v
    return obj

def validate(raw):
    if not isinstance(raw, str) or len(raw.encode("utf-8"))>12000:
        raise ValueError("report byte cap")
    try:
        data=json.loads(raw,object_pairs_hook=unique_pairs)
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid JSON") from exc
    if type(data) is not dict or set(data)!=(set(FLAGS)|{
        "schema","status","runtime_sha256","savedata_sha256",
        "prior_r13_status","regions","static_scope"}):
        raise ValueError("root schema keys")
    if data["schema"]!=SCHEMA or data["status"]!=STATUS:
        raise ValueError("schema or status")
    if data["runtime_sha256"]!="cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a" or data["savedata_sha256"]!="5b26f54a9723cd2c5275f964457094fdf1fc33ca086cdaf55bb5350dfb04f3f9":
        raise ValueError("original hash identity")
    if data["prior_r13_status"]!="PINNED_ORIGINAL_STATIC_MUTATION_CANDIDATES_NO_NAMED_EFFECTS" or data["static_scope"]!="two-instruction-anchors-bounded-cfg-not-complete-functions":
        raise ValueError("provenance and static scope")
    if any(data[k] is not False for k in FLAGS):
        raise ValueError("forbidden runtime/ownership promotion")
    regions=data["regions"]
    if type(regions) is not list or len(regions)!=2:
        raise ValueError("region count")
    all_inputs=[]
    for i,row in enumerate(regions):
        if type(row) is not dict or set(row)!={
            "all_incoming_edges_proven","anchor_is_verified_function_entry",
            "anchor_rva","branch_sites","call_barrier_sites",
            "call_fallthrough_is_structural_only","edge_count","frontier",
            "inputs","node_count","node_limit_hit"}:
            raise ValueError("region keys")
        if row["anchor_rva"]!=EXPECTED_ANCHORS[i] or row["anchor_is_verified_function_entry"] is not False or row["all_incoming_edges_proven"] is not False or row["call_fallthrough_is_structural_only"] is not True or row["node_limit_hit"] is not False:
            raise ValueError("region boundary status")
        if (row["node_count"],row["edge_count"],len(row["branch_sites"]),len(row["call_barrier_sites"]))!=EXPECTED_COUNTS[i]:
            raise ValueError("bounded graph metrics")
        if type(row["branch_sites"]) is not list or row["branch_sites"]!=sorted(set(row["branch_sites"])):
            raise ValueError("branch sites")
        if type(row["call_barrier_sites"]) is not list or row["call_barrier_sites"]!=sorted(set(row["call_barrier_sites"])):
            raise ValueError("call sites")
        if not all(type(x) is int and row["anchor_rva"]<=x<row["anchor_rva"]+384 for x in row["branch_sites"]+row["call_barrier_sites"]):
            raise ValueError("site outside bounded graph")
        if type(row["frontier"]) is not list or len(row["frontier"])>192:
            raise ValueError("frontier shape")
        for edge in row["frontier"]:
            if type(edge) is not dict or set(edge)!={"rva","reason"} or edge["reason"] not in {"out_of_window","decode_gap","indirect_jump","node_cap"} or type(edge["rva"]) is not int:
                raise ValueError("frontier gap")
        if type(row["inputs"]) is not list or len(row["inputs"])!=(1 if i==0 else 4):
            raise ValueError("query count")
        for q in row["inputs"]:
            if type(q) is not dict or set(q)!={"site_rva","register","reachable_in_bounded_graph","reaching_sources","register_value_known"}:
                raise ValueError("query shape")
            if q["reachable_in_bounded_graph"] is not True or q["register_value_known"] is not False or type(q["reaching_sources"]) is not list or len(q["reaching_sources"])!=1:
                raise ValueError("unknown register value not preserved")
            s=q["reaching_sources"][0]
            if type(s) is not dict or set(s)!={"origin","rva","semantic"}:
                raise ValueError("source shape")
            if s["origin"]=="unknown_call" and s["rva"] not in row["call_barrier_sites"]:
                raise ValueError("unproven call barrier")
            if s["origin"]=="entry" and s["rva"]!=row["anchor_rva"]:
                raise ValueError("entry")
            if s["origin"]=="definition" and (type(s["semantic"]) is not dict or
                 s["semantic"]!={"constant":None,"kind":"register_copy",
                                 "memory_input":None,"register_inputs":["eax"],"width_bits":32}):
                raise ValueError("semantic register copy")
            if s["origin"]!="definition" and s["semantic"] is not None:
                raise ValueError("unknown source semantics")
            all_inputs.append((q["site_rva"],q["register"],s["origin"],s["rva"]))
    if all_inputs!=EXPECTED_INPUTS:
        raise ValueError("site and source identity")
    if regions[0]["frontier"]!=[{"reason":"out_of_window","rva":302867},{"reason":"out_of_window","rva":302872},{"reason":"out_of_window","rva":303255}]:
        raise ValueError("helper graph exterior")
    if regions[1]["frontier"]!=[]:
        raise ValueError("global bounded frontier")
    if regions[0]["call_barrier_sites"]!=[302687,302702] or regions[1]["call_barrier_sites"]!=[300100,300125,300143]:
        raise ValueError("exact call barriers")
    return {"query_count":len(all_inputs),"regions":2,"native_io_executed":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--report",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(validate(args.report.read_text()),sort_keys=True))

if __name__=="__main__":
    main()
