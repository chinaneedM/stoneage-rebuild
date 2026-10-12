"""Strict original R15 derived-only caller/stack provenance and copy-safe custody."""
import argparse,json
from pathlib import Path
SCHEMA="tw10-r15-original-upstream-frame-and-opaque-call-frontier"
STATUS="PINNED_ORIGINAL_STATIC_PROVENANCE_NO_NAMED_EFFECTS"
FLAGS=["actual_function_entry_proven","frame_setup_ownership_proven","register_values_fully_known","global_initialization_proven","opaque_call_effects_resolved","branch_feasibility_proven","caller_effects_admitted","native_io_executed","fixed_128_byte_schema_proven","filename_api_link_proven","handle_buffer_size_link_proven","original_bytes_published"]
EXPECTED_CALL_SITES=(0x49444,0x4945d,0x4946f,0x49e5f,0x49e6e)
EXPECTED_TARGETS=(0x484c0,0x484c0,0x49900,0x4a09c,0x4a14d)
EXPECTED_QUERIES=((0x49de8,"eax",0x49de3),(0x49dca,"ebp",0x49d94),
                  (0x49dec,"ebp",0x49d94),(0x49dec,"esp",0x49da9))
HELPER_FRAME=(302483,302484,302486,302500,302501,302505,302687,302701,302702,302707,302857,302862)
GLOBAL_FRAME=(300097,300099,300100,300105,300113,300116,300118,300125,300130,300138,300141,300143,300148,300229,300230)
ROOT_KEYS=set(FLAGS)|{"schema","status","runtime_sha256","savedata_sha256",
  "bounded_graph_entry_not_proven","call_fallthrough_structural_only",
  "call_surfaces","exact_local_register_definitions_not_effective_values",
  "global_frame_write_candidates","global_outside_edges",
  "helper_frame_write_candidates","helper_outside_edges",
  "r14_global_nodes","r14_helper_nodes","upstream_inputs"}

def unique(rows):
    o={}
    for k,v in rows:
        if k in o:raise ValueError("duplicate JSON field")
        o[k]=v
    return o

def validate(raw):
    if not isinstance(raw,str) or len(raw.encode("utf-8"))>40000:raise ValueError("oversized report")
    try:o=json.loads(raw,object_pairs_hook=unique)
    except (TypeError,ValueError) as e:raise ValueError("invalid JSON") from e
    if type(o) is not dict or set(o)!=ROOT_KEYS:raise ValueError("unexpected report keys")
    if o["schema"]!=SCHEMA or o["status"]!=STATUS:raise ValueError("schema/status")
    if o["runtime_sha256"]!="cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a" or o["savedata_sha256"]!="5b26f54a9723cd2c5275f964457094fdf1fc33ca086cdaf55bb5350dfb04f3f9":
        raise ValueError("wrong original hashes")
    if any(o[k] is not False for k in FLAGS):raise ValueError("unsupported semantic promotion")
    if any(o[k] is not True for k in ("bounded_graph_entry_not_proven","call_fallthrough_structural_only","exact_local_register_definitions_not_effective_values")):
        raise ValueError("unknown graph boundaries")
    if (o["r14_helper_nodes"],o["r14_global_nodes"],o["helper_outside_edges"],o["global_outside_edges"])!=(139,48,3,0):
        raise ValueError("R14 original fixed graph identity changed")
    calls=o["call_surfaces"]
    if type(calls) is not list or len(calls)!=5:raise ValueError("CALL count")
    for i,c in enumerate(calls):
        if type(c) is not dict or set(c)!={"call_rva","callee_effect_summary_admitted",
               "calling_convention_proven","direct_target_rva","import_identity",
               "import_slot_association_proven","kind","memory_target",
               "register_target","returned_value_proven","runtime_target_or_effects_proven",
               "runtime_transfer_proven"}:raise ValueError("CALL geometry")
        if c["call_rva"]!=EXPECTED_CALL_SITES[i] or c["direct_target_rva"]!=EXPECTED_TARGETS[i] or c["kind"]!="direct":
            raise ValueError("CALL identity")
        if any(c[k] is not False for k in ("callee_effect_summary_admitted","calling_convention_proven","returned_value_proven","runtime_target_or_effects_proven","runtime_transfer_proven","import_slot_association_proven")):
            raise ValueError("unproved callee effects")
        if any(c[k] is not None for k in ("import_identity","memory_target","register_target")):
            raise ValueError("unproved IAT/indirect identity")
    qs=o["upstream_inputs"]
    if type(qs) is not list or len(qs)!=4:raise ValueError("query count")
    for i,x in enumerate(qs):
        if type(x) is not dict or set(x)!={"fully_known_value","origins","query_site_rva","register","verified_entry_to_query_path"}:raise ValueError("query shape")
        site,reg,defsite=EXPECTED_QUERIES[i]
        if x["query_site_rva"]!=site or x["register"]!=reg or x["fully_known_value"] is not False or x["verified_entry_to_query_path"] is not False:
            raise ValueError("upstream identity/promotion")
        if type(x["origins"]) is not list or len(x["origins"])!=1:raise ValueError("upstream source count")
        source=x["origins"][0]
        if set(source)!={"kind","rva","semantic"} or source["kind"]!="definition" or source["rva"]!=defsite:
            raise ValueError("reaching definition identity")
        sem=source["semantic"]
        if i==0:
            if sem!={"constant":None,"kind":"memory_load",
                "memory_input":{"base_register":None,
                   "displacement_region":{"displacement_rva":0x172186c,"raw_backed":False,"section":".data","writable":True},
                   "index_register":None,"index_scale":1,
                   "relative_field_offset":None,"segment_register":None,"width_bytes":4},
                "register_inputs":[],"width_bits":32}:raise ValueError("EAX load origin")
        elif i<3:
            if sem!={"constant":None,"kind":"register_copy","memory_input":None,
                      "register_inputs":["esp"],"width_bits":32}:raise ValueError("EBP prologue origin")
        elif sem is not None:raise ValueError("unmodeled ESP semantic")
    for key,expected in (("helper_frame_write_candidates",HELPER_FRAME),("global_frame_write_candidates",GLOBAL_FRAME)):
        items=o[key]
        if type(items) is not list or [x.get("rva") for x in items]!=list(expected):
            raise ValueError("frame candidate addresses")
        for item in items:
            if set(item)!={"rva","writes_ebp","writes_esp"}:raise ValueError("frame candidate keys")
            if item["writes_ebp"] is not (key=="helper_frame_write_candidates" and item["rva"]==0x49d94):
                raise ValueError("EBP frame candidate")
            if item["writes_esp"] is not (not item["writes_ebp"]):
                raise ValueError("ESP frame candidate")
    return {"upstream_input_count":4,"opaque_call_count":5,
            "semantic_effects_admitted":False,"native_io_executed":False}

def main():
    p=argparse.ArgumentParser();p.add_argument("--report",type=Path,required=True)
    print(json.dumps(validate(p.parse_args().report.read_text()),sort_keys=True))
if __name__=="__main__":main()
