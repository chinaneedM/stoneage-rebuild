"""R39: exact mask, bounded symbolic stack tokens and native read caller.

Original bytes are inspected, never executed. A symbolic PUSH/slot token under
explicit stack assumptions does not establish an original argument/handle value.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from capstone.x86 import X86_OP_MEM
from tools.stoneage_tw10_savedata_native_io_r38 import (
    inspect_verified as inspect_r38, ROOT, READS, SCALARS, RUNTIME_SHA256,
    SAVEDATA_SHA256, stack_states, state_summary, FLAGS as R38_FLAGS,
)
from tools.stoneage_tw10_savedata_native_io_r38_guard import validate as validate_r38
from tools.stoneage_tw10_savedata_native_io_r37 import (
    instruction_row, full_width_model, operand_registers, PARENT,
)
from tools.stoneage_tw10_savedata_native_io_r36 import closure
from tools.stoneage_tw10_savedata_native_io_r30 import composition, graph_meta
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_upstream_r23 import local_push_suffix
from tools.stoneage_tw10_savedata_write_shapes_r17 import operand_shape
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = "tw10-r39-original-mask-symbolic-slots-native-read-caller"
STATUS = "PINNED_ORIGINAL_CONDITIONAL_TOKENS_NATIVE_READ_PAYLOAD_SAVE_OPEN"
PRIOR_SHA256 = "eeecbfcf18b59c9b1198ea8e17a0428ab73a6d604ba36253dee661a65da53099"
MASK = 0x4e81f
READ_CALL = 0x4edb0
READ_ROOT = 0x4a8dc
MAX_DEFS = 16
MAX_COMPARE = 8
FLAGS = tuple(R38_FLAGS) + (
    "symbolic_token_establishes_actual_caller_helper_value_binding",
    "native_read_caller_stack_signature_establishes_abi_roles",
    "native_read_buffer_payload_or_savedata_length128_proven",
    "native_read_callee_result_or_executed_io_proven",
)

def prefix_audit(evidence, read, bridge, writes):
    """Union of bounded structural prefixes; unknown aliases block tokens."""
    effects, edges = evidence["effects"], evidence["edges"]
    states, _, limit = stack_states(effects, edges, ROOT)
    site = read["site_rva"]
    prefix = (closure(edges, ROOT) & closure(edges, site, True)) - {site}
    target = bridge["callee_entry_esp_relative_offset"]
    mems = [op for op in read["operands"] if op.get("kind") == "memory"]
    width = mems[0]["width_bytes"] if len(mems) == 1 else None
    entries, unknown = [], []
    for eff in effects:
        at = eff["site_rva"]
        if at not in prefix:
            continue
        delta = state_summary(states, at, limit)["unique_conditional_esp_delta"]
        if eff["syntax_class"] in ("opaque_call", "unknown_esp_write"):
            unknown.append({"site_rva": at, "kind": eff["syntax_class"]})
        if eff["syntax_class"] == "push":
            size = eff["operand_width_bytes"]
            start = delta - size if delta is not None else None
            entries.append({"site_rva": at, "kind": "implicit_push_write",
                            "entry_relative_start": start, "width_bytes": size,
                            "possible_alias_or_unknown_offset": start is None})
    for w in writes:
        at, op = w["site_rva"], w["operand"]
        if at not in prefix:
            continue
        geo = op.get("geometry") or {}
        delta = state_summary(states, at, limit)["unique_conditional_esp_delta"]
        safe = (geo.get("base_register") == "esp" and geo.get("index_register") is None
                and geo.get("segment_register") is None and delta is not None
                and type(geo.get("relative_field_offset")) is int)
        start = delta + geo["relative_field_offset"] if safe else None
        entries.append({"site_rva": at, "kind": "explicit_memory_write",
                        "entry_relative_start": start, "width_bytes": op["width_bytes"],
                        "possible_alias_or_unknown_offset": not safe})
    entries.sort(key=lambda e:(e["site_rva"],e["kind"]))
    overlaps = []
    for w in entries:
        start = w["entry_relative_start"]
        if start is not None and type(target) is int and type(width) is int:
            if start < target + width and target < start + w["width_bytes"]:
                overlaps.append(w["site_rva"])
    clear = bool(bridge["conditional_hardware_slot_candidate"] and not limit and not unknown
                 and not overlaps and not any(w["possible_alias_or_unknown_offset"] for w in entries))
    ops = read["operands"]
    dest = ops[0] if ops else {}
    push = bridge["matching_push_operand_shape"] or {}
    token = (clear and read["mnemonic"] == "mov" and dest.get("kind") == "register"
             and dest.get("width_bytes") == width == push.get("width_bytes")
             and push.get("kind") == "register")
    return {"read_site_rva": site, "prefix_node_rvas": sorted(prefix),
            "target_entry_relative_start": target, "target_width_bytes": width,
            "modeled_prefix_write_candidates": entries, "overlapping_write_sites": sorted(set(overlaps)),
            "unknown_prefix_effect_candidates": unknown,
            "no_bounded_prefix_overwrite_candidate": clear,
            "conditional_symbolic_register_token_candidate": bool(token),
            "source_push_rva": bridge["matching_suffix_push_rva"] if token else None,
            "source_caller_register_symbol": push.get("register") if token else None,
            "destination_callee_register_symbol": dest.get("register") if token else None,
            "requires_prior_32bit_stack_and_near_call_conditions": True,
            "bounded_candidate_prefix_only": True,
            "actual_original_contents_argument_value_alias_owner_proven": False}

def helper_surface(dec, sections, prior):
    nodes, edges, front, hit = candidate_graph(dec, ROOT)
    mask = instruction_row(dec, sections, nodes, MASK)
    shift = instruction_row(dec, sections, nodes, SCALARS[1])
    mask["conditional_full_width_model"] = full_width_model(mask)
    inputs = input_surface(dec, sections, nodes, edges, ROOT, {(MASK,"esi"),(SCALARS[1],"esi")})
    source = next(q for q in inputs["queries"] if (q["site_rva"],q["register"]) == (SCALARS[1],"esi"))
    expr = composition({"site_rva":MASK,"class":mask["mnemonic"],"operands":mask["operands"]},
                       {"site_rva":SCALARS[1],"class":shift["mnemonic"],"operands":shift["operands"]},source)
    writes = [{"site_rva":at,"operand_index":i,"operand":operand_shape(ins,op,sections,dec.base)}
              for at,ins in sorted(nodes.items()) for i,op in enumerate(ins.operands)
              if op.type == X86_OP_MEM and op.access & 2]
    evidence = {"effects":prior["stack_effect_candidates"],"edges":prior["bounded_edges"]}
    return {"root_candidate_rva":ROOT,"graph":graph_meta(nodes,edges,front,hit),
            "mask_shape":mask,"shift_shape":shift,"input_sources":inputs,"conditional_composition":expr,
            "prior_stack_evidence":evidence,"prior_stack_read_shapes":prior["callee_stack_read_shapes"],
            "prior_slot_bridges":prior["conditional_slot_bridges"],"explicit_write_shapes":writes,
            "prefix_token_audits":[prefix_audit(evidence,row,bridge,writes) for row,bridge in
                                   zip(prior["callee_stack_read_shapes"],prior["conditional_slot_bridges"])],
            "actual_helper_value_index_table_or_handle_owner_proven":False}

def read_caller(dec, sections, imports):
    nodes, edges, front, hit = candidate_graph(dec, PARENT)
    ident = call_identity(dec,READ_CALL,imports,sections)
    if READ_CALL not in nodes or ident["kind"] != "direct" or ident["direct_target_rva"] != READ_ROOT:
        raise ValueError("R39 original ReadFile-context caller identity")
    suffix = local_push_suffix(dec,sections,0x4ed33,READ_CALL)
    queries={(READ_CALL,r) for r in ("eax","ebx","ecx","esi","edi","ebp")}
    pushes=[]
    for p in suffix["pushes"]:
        regs=operand_registers(p["input"])
        queries.update((p["site_rva"],r) for r in regs)
        pushes.append({**p,"input_query_registers":regs,"actual_abi_role_value_or_buffer_length_proven":False})
    comparisons=[instruction_row(dec,sections,nodes,at) for at,ins in sorted(nodes.items())
                 if READ_CALL+5 <= at < READ_CALL+48 and ins.mnemonic in ("cmp","test")]
    for row in comparisons[:MAX_COMPARE]:
        queries.update((row["site_rva"],r) for r in row["input_query_registers"])
    inputs=input_surface(dec,sections,nodes,edges,PARENT,queries)
    defs=sorted({s["rva"] for q in inputs["queries"]
                 if any(q["site_rva"]==p["site_rva"] and q["register"] in p["input_query_registers"] for p in pushes)
                 for s in q["reaching_candidates"] if s["origin"]=="definition"})
    shapes=[instruction_row(dec,sections,nodes,at) for at in defs[:MAX_DEFS]]
    for row in shapes:
        queries.update((row["site_rva"],r) for r in row["input_query_registers"])
    inputs=input_surface(dec,sections,nodes,edges,PARENT,queries)
    return {"root_candidate_rva":PARENT,"graph":graph_meta(nodes,edges,front,hit),
            "read_context_call_identity":ident,"read_context_candidate_rva":READ_ROOT,
            "pre_call_suffix":suffix,"push_candidates":pushes,"input_sources":inputs,
            "push_definition_count":len(defs),"push_definition_shapes":shapes,
            "push_definitions_truncated":len(defs)>MAX_DEFS,
            "postcall_compare_count":len(comparisons),"postcall_compare_shapes":comparisons[:MAX_COMPARE],
            "postcall_compares_truncated":len(comparisons)>MAX_COMPARE,
            "actual_callee_abi_buffer_payload_length_or_return_proven":False}

def derive(dec, sections, imports, prior):
    if prior.get("schema") != "tw10-r38-original-conditional-esp-slots-shared-store-inputs":
        raise ValueError("R39 prerequisite schema")
    pn,pe,pf,pc=candidate_graph(dec,PARENT)
    caller_sources=input_surface(dec,sections,pn,pe,PARENT,{(0x4ed47,"esi"),(0x4ed48,"ebx")})
    return {"schema":SCHEMA,"status":STATUS,"runtime_sha256":RUNTIME_SHA256,"savedata_sha256":SAVEDATA_SHA256,
            "r38_exact_original_revalidated":True,"r38_exact_report_sha256":PRIOR_SHA256,"static_only":True,
            "helper_mask_and_tokens":helper_surface(dec,sections,prior),
            "helper_caller_push_sources":caller_sources,"native_read_caller":read_caller(dec,sections,imports),
            **{flag:False for flag in FLAGS}}

def inspect_verified(runtime,savedata):
    prior=inspect_r38(runtime,savedata);validate_r38(prior)
    digest=hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()
    if digest != PRIOR_SHA256:raise ValueError("R39 R38 exact original derivative changed")
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for sec,raw in zip(sections,pe.sections):sec['characteristics']=int(raw.Characteristics)
    code=next(s for s in sections if s['name']=='.text')
    dec=Decoder(data[code['raw']:code['raw']+code['raw_size']],code['rva'],base)
    return derive(dec,sections,imports,prior)

def main():
    p=argparse.ArgumentParser();p.add_argument('--bin',type=Path,required=True)
    image,rows,_,_=find_rows(p.parse_args().bin)
    try:
        files={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe,save=Path(td)/'sa_3.exe',Path(td)/'savedata.dat'
            extract_row(image,files[RUNTIME_PATH],exe);extract_row(image,files[SAVEDATA_PATH],save)
            result=inspect_verified(exe.read_bytes(),save.read_bytes())
    finally:image.close()
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
