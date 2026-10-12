"""TW1.0 R18 original-derived conditional CALL, alias and CFG frontiers.

Original archive/runtime bytes remain transient and original PE is never run.
This tool proves only pinned instruction shapes and conservative graph candidates;
it never admits runtime effects, actual values, function entries or save format.
"""
import argparse
import json
import tempfile
from pathlib import Path
from capstone import CS_GRP_CALL, CS_GRP_JUMP, CS_GRP_RET
from capstone.x86 import X86_OP_MEM, X86_OP_REG
from tools.stoneage_tw10_savedata_write_shapes_r17 import (
    inspect_verified as inspect_r17, RUNTIME_SHA256, SAVEDATA_SHA256,
    WRITES, GLOBAL, GAP, operand_shape,
)
from tools.stoneage_tw10_savedata_frontier_r12 import (
    call_identity, linear_references,
)
from tools.stoneage_tw10_savedata_reachdefs_r14 import (
    bounded_graph, HELPER_ANCHOR,
)
from tools.stoneage_tw10_savedata_inputs_r11 import reaches, semantic
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_argtrace_r7 import State, step, stack, address
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = "tw10-r18-original-upstream-call-alias-cfg-frontier"
STATUS = "PINNED_CONDITIONAL_STATIC_SOURCE_PATH_AND_EFFECTS_OPEN"
EAX_CALL = 0x49a0c
EAX_WRITE = 0x49a2c
ECX_LOAD = 0x49d72
EBX_WRITE = 0x49e88
SECOND_GLOBAL = 0x1721878
IMUL_ROOT = 0x484c0
IMUL_SITE = GAP
FLAGS = (
    "original_function_entries_proven", "executed_control_flow_proven",
    "call_return_effects_admitted", "global_runtime_values_proven",
    "global_initialization_proven", "global_ownership_proven",
    "effective_caller_frame_proven", "nested_call_effects_admitted",
    "caller_resumption_admitted", "filename_to_createfile_proven",
    "handle_buffer_length_link_proven", "fixed_128_byte_format_proven",
    "native_save_io_executed", "original_assets_published",
)

def upstream_call(dec, imports, sections, call_rva=EAX_CALL, root=0x49a00,
                  query_site=EAX_WRITE):
    nodes, edges, front, cap = bounded_graph(
        dec, root, max_span=192, max_nodes=128)
    if call_rva not in nodes or query_site not in nodes:
        raise ValueError("R17 EAX CALL/write not in bounded local graph")
    identity = call_identity(dec, call_rva, imports, sections)
    target = identity["direct_target_rva"]
    effect = None
    if identity["kind"] == "direct" and target is not None and dec.lo <= target < dec.hi:
        effect = summarize(dec, target, max_states=96)
    return {
        "call_site_rva": call_rva,
        "write_site_rva": query_site,
        "call_identity": identity,
        "direct_callee_model": effect,
        "candidate_graph_anchor_rva": root,
        "candidate_graph_nodes": len(nodes),
        "candidate_graph_edges": len(edges),
        "candidate_graph_frontier": [{"reason": reason, "rva": at}
                                     for reason, at in front],
        "candidate_graph_node_limit_hit": cap,
        "candidate_anchor_verified_entry": False,
        "call_fallthrough_structural_only": True,
        "eax_after_call_known": False,
        "callee_summary_admitted": False,
        "original_return_value_proven": False,
    }

def global_alias_probe(dec, sections, read_site=ECX_LOAD,
                       global_rva=SECOND_GLOBAL):
    ins = dec.at(read_site)
    if not ins or ins.mnemonic != "mov" or len(ins.operands) != 2:
        raise ValueError("R17 ECX source load syntax changed")
    dst, src = ins.operands
    if (dst.type != X86_OP_REG or ins.reg_name(dst.reg) != "ecx"
            or dst.size != 4 or src.type != X86_OP_MEM or src.size != 4
            or src.mem.base or src.mem.index or src.mem.segment
            or ((int(src.mem.disp) & 0xffffffff) - dec.base) & 0xffffffff != global_rva):
        raise ValueError("distinct R17 ECX global load changed")
    scan = linear_references(dec, targets=(global_rva,))
    row = scan["globals"][0]
    return {
        "read_site_rva": read_site,
        "source_operand": operand_shape(ins, src, sections, dec.base),
        "global_reference_candidates": scan,
        "original_global_identity_proven": True,
        "global_value_known": False,
        "alias_reference_coverage_complete": False,
        "runtime_initialized": False,
        "same_object_as_primary_global_proven": False,
    }

def candidate_ebx_graph(dec, sections, root=HELPER_ANCHOR,
                        site=EBX_WRITE):
    nodes, edges, frontier, capped = bounded_graph(dec, root)
    tokens = []
    if site in nodes:
        token_set = reaches(nodes, edges, root, "ebx").get(site, set())
        for origin, at in sorted(token_set, key=lambda x: (x[1], x[0]))[:32]:
            tokens.append({
                "origin": origin,
                "rva": at,
                "semantic": semantic(nodes[at], "ebx", sections, dec.base)
                            if origin == "definition" else None,
            })
    return {
        "anchor_rva": root, "write_site_rva": site,
        "reached_in_R14_helper_graph": site in nodes,
        "nodes": len(nodes), "edges": len(edges),
        "frontier": [{"reason": why, "rva": at} for why, at in frontier],
        "state_limit_hit": capped, "source_candidates": tokens,
        "source_candidates_truncated": bool(site in nodes and len(
            reaches(nodes, edges, root, "ebx").get(site, set())) > 32),
        "actual_function_entry_proven": False,
        "all_incoming_edges_proven": False,
        "call_fallthrough_structural_only": True,
        "value_known": False, "feasible_path_proven": False,
    }

def imul_stack_prefix(dec, root=IMUL_ROOT, site=IMUL_SITE, max_steps=16):
    """Symbolic linear prefix; do not infer a caller frame or actual stack."""
    if not 1 <= max_steps <= 16:
        raise ValueError("prefix bounds")
    state = State()
    at = root
    visited = []
    halt_reason = None
    for _ in range(max_steps):
        ins = dec.at(at)
        if ins is None:
            halt_reason = "decode_or_outside_text"
            break
        if at == site:
            memories = [op for op in ins.operands if op.type == X86_OP_MEM]
            if ins.mnemonic != "imul" or len(memories) != 1:
                raise ValueError("R17 IMUL site changed")
            position = address(memories[0], state)
            return {
                "candidate_entry_rva": root, "imul_site_rva": site,
                "prefix_sites": visited, "stopped_at_original_memory_gap": True,
                "modeled_stack_offset_of_memory_operand": position,
                "stack_offset_model_is_conditional_only": True,
                "real_esp_or_caller_frame_proven": False,
                "effective_memory_value_proven": False,
                "register_multiplier_value_proven": False,
                "callee_effect_summary_admitted": False,
                "halt_reason": None,
            }
        if ins.group(CS_GRP_CALL) or ins.group(CS_GRP_JUMP) or ins.group(CS_GRP_RET):
            halt_reason = "control_transfer_barrier"
            break
        next_state, reason = step(ins, state, None)
        if reason is not None:
            halt_reason = reason
            break
        visited.append(at)
        at += ins.size
        state = next_state
    else:
        halt_reason = "prefix_bound"
    return {
        "candidate_entry_rva": root, "imul_site_rva": site,
        "prefix_sites": visited, "stopped_at_original_memory_gap": False,
        "modeled_stack_offset_of_memory_operand": None,
        "stack_offset_model_is_conditional_only": True,
        "real_esp_or_caller_frame_proven": False,
        "effective_memory_value_proven": False,
        "register_multiplier_value_proven": False,
        "callee_effect_summary_admitted": False,
        "halt_reason": halt_reason,
    }

def inspect_static(dec, sections, imports):
    return {
        "eax_call_barrier": upstream_call(dec, imports, sections),
        "secondary_global": global_alias_probe(dec, sections),
        "ebx_graph": candidate_ebx_graph(dec, sections),
        "imul_stack": imul_stack_prefix(dec),
    }

def inspect_verified(runtime, savedata):
    r17 = inspect_r17(runtime, savedata)
    if ([x["site_rva"] for x in r17["writes"]] != list(WRITES)
            or r17["writes"][0]["local_source_frontier"]["reaching_candidates"][0]
            != {"origin": "unknown_call", "rva": EAX_CALL, "semantic": None}
            or r17["writes"][1]["local_source_frontier"]["reaching_candidates"][0]["rva"]
            != ECX_LOAD
            or r17["callee_memory_gap"]["site_rva"] != IMUL_SITE
            or r17["callee_memory_gap"]["mnemonic_class"] != "imul"):
        raise ValueError("R17 pinned original static frontier changed")
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "sa_3.exe"
        p.write_bytes(runtime)
        data, pe, base, sections, imports = image_layout(p)
    for sec, raw in zip(sections, pe.sections):
        sec["characteristics"] = int(raw.Characteristics)
    text_sec = next(s for s in sections if s["name"] == ".text")
    dec = Decoder(data[text_sec["raw"]:text_sec["raw"] + text_sec["raw_size"]],
                  text_sec["rva"], base)
    report = inspect_static(dec, sections, imports)
    return {
        "schema": SCHEMA, "status": STATUS,
        "runtime_sha256": RUNTIME_SHA256, "savedata_sha256": SAVEDATA_SHA256,
        "r17_original_identity_revalidated": True,
        "original_static_only": True,
        **report, **{f: False for f in FLAGS},
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin", type=Path, required=True)
    args = parser.parse_args()
    image, rows, _, _ = find_rows(args.bin)
    try:
        files = {r["path"]:r for r in rows if not r["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe = Path(td) / "sa_3.exe"
            save = Path(td) / "savedata.dat"
            extract_row(image, files[RUNTIME_PATH], exe)
            extract_row(image, files[SAVEDATA_PATH], save)
            result = inspect_verified(exe.read_bytes(), save.read_bytes())
    finally:
        image.close()
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
