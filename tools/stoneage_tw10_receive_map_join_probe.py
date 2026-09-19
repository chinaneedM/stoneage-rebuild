#!/usr/bin/env python3
"""Join Taiwan v1.0 Winsock recv to LSSPROTO dispatch and map handlers.

Derived metadata only. The accepted retail image is transient in CI.
"""

from __future__ import annotations

import argparse
import collections
from pathlib import Path
import tempfile

from capstone.x86 import X86_OP_IMM

from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from tools.stoneage_tw10_mapcache_binary_probe import (
    image_layout,
    referenced_absolute_values,
    rva_to_offset,
)
from tools.stoneage_tw10_protocol_handoff_probe import (
    backward_paths,
    callback_cfg_probe,
    direct_rel32_call_sites,
    exact_iat_opcode_sites,
    linear_slice_calls,
    md,
    operand_summary,
    section_name_for_va,
)
from tools.stoneage_tw10_exact_xref_probe import (
    decode_forward_node,
    expand_from_exact_root,
    raw_text_pointer_hits,
    recover_xref_instruction,
)

DECODE_HELPERS = (0x1B140, 0x1B4C0)
LOGIN_CALLBACKS = {
    "ClientLogin": 0x2F200,
    "CreateNewChar": 0x31E90,
    "CharDelete": 0x31F90,
    "CharLogin": 0x2F530,
    "CharList": 0x2F320,
    "CharLogout": 0x2F610,
}
DISPATCH_RVA_MIN = 0x18000
DISPATCH_RVA_MAX = 0x1B000
SHORT_PROTOCOLS = ("MC", "M", "C", "CA")
MAP_XREF_RVAS = (0x1D846, 0x1DA50, 0x1DDA0, 0x21306, 0x21721, 0x218FE)
MAP_CALLBACKS = {
    "MC": 0x30D20,
    "M": 0x30EF0,
}
DEEP_GRAPH_DEPTH = 10
DEEP_GRAPH_NODES = 160
MAP_SEMANTIC_NODES = {
    "M": 0x1DA40,
    "MC": 0x1DD90,
}
FILE_MODE_LITERALS = ("rb+", "r+b", "rb", "wb", "wb+", "w+b")


def clean(v, limit=900):
    s = " ".join(str(v if v is not None else "").split())
    return "".join(ch for ch in s if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def file_offset_to_rva(sections, off):
    for sec in sections:
        if sec["raw"] <= off < sec["raw"] + sec["raw_size"]:
            return sec["rva"] + (off - sec["raw"])
    return None


def all_string_xrefs(data, base, sections, text):
    needle = text.encode("ascii") + b"\x00"
    rows = []
    pos = 0
    occurrence = 0
    while True:
        pos = data.find(needle, pos)
        if pos < 0:
            break
        occurrence += 1
        rva = file_offset_to_rva(sections, pos)
        if rva is not None:
            va = base + rva
            for hit in raw_text_pointer_hits(data, base, sections, va):
                ins = recover_xref_instruction(data, base, sections, hit, va)
                if ins is not None:
                    rows.append((occurrence, rva, ins))
        pos += 1
    return rows


def exact_recv_business_sites(data, base, sections, imports):
    out = []
    for iat_va, (dll, name) in imports.items():
        if dll.lower() != "wsock32.dll" or name.lower() != "recv":
            continue
        for kind, site_va in exact_iat_opcode_sites(data, base, sections, iat_va):
            if kind == "call":
                out.append((iat_va, site_va, site_va, False))
            elif kind == "jmp":
                callers = direct_rel32_call_sites(data, base, sections, site_va)
                for caller in callers:
                    out.append((iat_va, caller, site_va, True))
    uniq = {}
    for row in out:
        uniq[(row[0], row[1])] = row
    return [uniq[k] for k in sorted(uniq)]


def deep_call_graph(data, base, sections, imports, root_va, max_depth=DEEP_GRAPH_DEPTH, max_nodes=DEEP_GRAPH_NODES):
    queue = collections.deque([(root_va, 0)])
    nodes = {}
    while queue and len(nodes) < max_nodes:
        va, depth = queue.popleft()
        if va in nodes:
            nodes[va]["depth"] = min(nodes[va]["depth"], depth)
            continue
        node = decode_forward_node(data, base, sections, imports, va)
        if node is None:
            continue
        node["depth"] = depth
        nodes[va] = node
        if depth >= max_depth:
            continue
        for target in node["internal"]:
            if target not in nodes:
                queue.append((target, depth + 1))
    return nodes


def graph_map_xref_hits(graph, base):
    hits = []
    for node_va, node in graph.items():
        start_rva = node_va - base
        end_rva = node.get("end_va", node_va) - base
        if end_rva < start_rva:
            start_rva, end_rva = end_rva, start_rva
        for xref_rva in MAP_XREF_RVAS:
            if start_rva <= xref_rva <= end_rva + 8:
                hits.append((node_va, node.get("depth", 0), xref_rva))
    return sorted(set(hits))


def literal_vas(data, base, sections, literals):
    out = {}
    for literal in literals:
        needle = literal.encode("ascii") + b"\x00"
        vas = set()
        pos = 0
        while True:
            pos = data.find(needle, pos)
            if pos < 0:
                break
            rva = file_offset_to_rva(sections, pos)
            if rva is not None:
                vas.add(base + rva)
            pos += 1
        out[literal] = vas
    return out


def node_literal_hits(data, base, sections, node_va, node, values):
    hits = []
    insns = decode_node_instructions(data, base, sections, node_va, node.get("end_va", node_va))
    for ins in insns:
        refs = set(referenced_absolute_values(ins))
        for label, vas in values.items():
            if refs.intersection(vas):
                hits.append((ins.address, label))
    return sorted(set(hits))


def edge_calls_to(graph, target_va):
    out = []
    for node_va, node in graph.items():
        for callsite, target in node["call_order"]:
            if target == target_va:
                out.append((node_va, callsite, node.get("depth", 0)))
    return sorted(set(out))


def graph_dispatch_window_nodes(graph, base):
    out = []
    for node_va, node in graph.items():
        rva = node_va - base
        if DISPATCH_RVA_MIN <= rva < DISPATCH_RVA_MAX:
            out.append((rva, node.get("depth", 0)))
    return sorted(out)


def decode_node_instructions(data, base, sections, start_va, end_va):
    off = rva_to_offset(sections, start_va - base)
    end_off = rva_to_offset(sections, end_va - base)
    if off is None:
        return []
    if end_off is None or end_off < off:
        end_off = min(len(data), off + 0x800)
    else:
        end_off = min(len(data), end_off + 16)
    return list(md().disasm(data[off:end_off], start_va, count=300))


def graph_protocol_refs(data, base, sections, graph, targets):
    hits = []
    for node_va, node in graph.items():
        insns = decode_node_instructions(
            data, base, sections, node_va, node.get("end_va", node_va)
        )
        for ins in insns:
            vals = set(referenced_absolute_values(ins))
            for label, vas in targets.items():
                if vals.intersection(vas):
                    hits.append((node_va, ins.address, label))
    return sorted(set(hits))


def summarize_helper(data, base, sections, imports, rva):
    va = base + rva
    cfg = callback_cfg_probe(data, base, sections, imports, va)
    callers = direct_rel32_call_sites(data, base, sections, va)
    print(
        f"DECODE_HELPER|rva=0x{rva:x}|callers={len(callers)}|"
        f"blocks={cfg['blocks']}|instructions={cfg['instructions']}|"
        f"direct_targets={len(cfg['direct'])}|import_api_kinds={len(cfg['api'])}|"
        f"globals={len(cfg['globals'])}"
    )
    for target, count in sorted(cfg["direct"].items()):
        print(
            f"DECODE_HELPER_CALL|helper_rva=0x{rva:x}|target_rva=0x{target-base:x}|calls={count}"
        )
    off = rva_to_offset(sections, rva)
    if off is not None:
        for order, ins in enumerate(md().disasm(data[off:off+0x100], va, count=18), 1):
            print(
                f"DECODE_HELPER_INS|helper_rva=0x{rva:x}|order={order}|"
                f"instruction_rva=0x{ins.address-base:x}|mnemonic={clean(ins.mnemonic)}|"
                f"ops={clean(operand_summary(ins,base,sections))}"
            )
            if ins.mnemonic.startswith("ret"):
                break


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", required=True)
    args = ap.parse_args()

    print("StoneAge Taiwan v1.0 receive/map join probe — R1")
    print("SCOPE|ephemeral-verified-disc|recv-dispatch-map-join|derived-only")

    img, rows, layout, joliet = find_rows(args.bin)
    td = tempfile.TemporaryDirectory()
    root = Path(td.name)
    try:
        by_path = {r["path"]: r for r in rows if not r["is_dir"]}
        row = by_path.get("StoneAge/sa_3.exe")
        if row is None:
            raise SystemExit("sa_3.exe missing")
        exe = root / "sa_3.exe"
        extract_row(img, row, exe)
        data, pe, base, sections, imports = image_layout(exe)

        print(
            f"RUNTIME|bytes={exe.stat().st_size}|image_base=0x{base:x}|"
            f"imports={len(imports)}|layout={layout}|joliet={int(joliet)}"
        )

        for rva in DECODE_HELPERS:
            summarize_helper(data, base, sections, imports, rva)

        for name, rva in LOGIN_CALLBACKS.items():
            callers = direct_rel32_call_sites(data, base, sections, base + rva)
            print(f"LOGIN_CALLBACK|name={name}|rva=0x{rva:x}|direct_callers={len(callers)}")

        target_vas = {}
        for label in ("ClientLogin", "CharLogin", "ProcGet"):
            rows2 = all_string_xrefs(data, base, sections, label)
            vas = set()
            needle = label.encode("ascii") + b"\x00"
            pos = 0
            while True:
                pos = data.find(needle, pos)
                if pos < 0:
                    break
                rva = file_offset_to_rva(sections, pos)
                if rva is not None:
                    vas.add(base + rva)
                pos += 1
            target_vas[label] = vas
            print(
                f"PROTOCOL_TARGET|name={label}|occurrences={len(vas)}|decoded_xrefs={len(rows2)}"
            )

        recv_sites = exact_recv_business_sites(data, base, sections, imports)
        print(f"WSOCK_RECV|business_calls={len(recv_sites)}")
        for n, (iat_va, site_va, thunk_va, via_thunk) in enumerate(recv_sites, 1):
            print(
                f"WSOCK_RECV_CALL|n={n}|callsite_rva=0x{site_va-base:x}|"
                f"iat_rva=0x{iat_va-base:x}|via_thunk={int(via_thunk)}|"
                f"thunk_rva=0x{thunk_va-base:x}"
            )
            graph = deep_call_graph(data, base, sections, imports, site_va)
            print(
                f"WSOCK_RECV_GRAPH|n={n}|nodes={len(graph)}|"
                f"max_depth={max((node['depth'] for node in graph.values()), default=0)}"
            )
            for dispatch_rva, depth in graph_dispatch_window_nodes(graph, base):
                print(
                    f"WSOCK_RECV_DISPATCH_WINDOW|n={n}|node_rva=0x{dispatch_rva:x}|depth={depth}"
                )
            root_node = graph.get(site_va)
            if root_node is not None:
                for order, (callsite, target) in enumerate(root_node["call_order"], 1):
                    print(
                        f"WSOCK_RECV_ROOT_CALL|n={n}|order={order}|"
                        f"callsite_rva=0x{callsite-base:x}|target_rva=0x{target-base:x}"
                    )
            for node_va, ins_va, label in graph_protocol_refs(
                data, base, sections, graph, target_vas
            ):
                print(
                    f"WSOCK_RECV_PROTOCOL_JOIN|n={n}|protocol={label}|"
                    f"node_rva=0x{node_va-base:x}|instruction_rva=0x{ins_va-base:x}"
                )

        short_candidates = []
        for label in SHORT_PROTOCOLS:
            refs = all_string_xrefs(data, base, sections, label)
            print(f"SHORT_PROTOCOL|name={label}|decoded_xrefs={len(refs)}")
            for occurrence, string_rva, ins in refs:
                irva = ins.address - base
                in_dispatch = DISPATCH_RVA_MIN <= irva < DISPATCH_RVA_MAX
                print(
                    f"SHORT_PROTOCOL_XREF|name={label}|occurrence={occurrence}|"
                    f"string_rva=0x{string_rva:x}|instruction_rva=0x{irva:x}|"
                    f"mnemonic={clean(ins.mnemonic)}|dispatch_window={int(in_dispatch)}"
                )
                if in_dispatch and ins.mnemonic == "mov":
                    short_candidates.append((ins.address, label, string_rva))

        short_candidates.sort()
        print(f"MAP_PROTOCOL_DISPATCH_CANDIDATES|count={len(short_candidates)}")
        for idx, (start_va, label, string_rva) in enumerate(short_candidates):
            next_va = (
                short_candidates[idx + 1][0]
                if idx + 1 < len(short_candidates)
                else min(base + DISPATCH_RVA_MAX, start_va + 0x220)
            )
            if next_va <= start_va:
                continue
            insns, calls = linear_slice_calls(data, base, sections, start_va, next_va)
            print(
                f"MAP_PROTOCOL_SLICE|name={label}|start_rva=0x{start_va-base:x}|"
                f"end_rva=0x{next_va-base:x}|bytes={next_va-start_va}|"
                f"instructions={len(insns)}|direct_calls={len(calls)}"
            )
            for order, (callsite, target) in enumerate(calls, 1):
                print(
                    f"MAP_PROTOCOL_SLICE_CALL|name={label}|order={order}|"
                    f"callsite_rva=0x{callsite-base:x}|target_rva=0x{target-base:x}"
                )

        map_string_rows = all_string_xrefs(data, base, sections, r"map\%d.dat")
        map_string_vas = set()
        needle = b"map\\%d.dat\x00"
        pos = 0
        while True:
            pos = data.find(needle, pos)
            if pos < 0:
                break
            srva = file_offset_to_rva(sections, pos)
            if srva is not None:
                map_string_vas.add(base + srva)
            pos += 1
        print(
            f"MAP_STRING|occurrences={len(map_string_vas)}|decoded_xrefs={len(map_string_rows)}"
        )

        for name, callback_rva in MAP_CALLBACKS.items():
            root_va = base + callback_rva
            graph = deep_call_graph(data, base, sections, imports, root_va)
            print(
                f"MAP_CALLBACK_GRAPH|name={name}|rva=0x{callback_rva:x}|nodes={len(graph)}|"
                f"max_depth={max((node['depth'] for node in graph.values()), default=0)}"
            )
            root_node = graph.get(root_va)
            if root_node is not None:
                for order, (callsite, target) in enumerate(root_node["call_order"], 1):
                    print(
                        f"MAP_CALLBACK_ROOT_CALL|name={name}|order={order}|"
                        f"callsite_rva=0x{callsite-base:x}|target_rva=0x{target-base:x}"
                    )
            for node_va, depth, xref_rva in graph_map_xref_hits(graph, base):
                print(
                    f"MAP_CALLBACK_XREF_JOIN|name={name}|node_rva=0x{node_va-base:x}|"
                    f"depth={depth}|map_xref_rva=0x{xref_rva:x}"
                )
            for node_va, node in sorted(graph.items()):
                insns = decode_node_instructions(
                    data, base, sections, node_va, node.get("end_va", node_va)
                )
                for ins in insns:
                    vals = set(referenced_absolute_values(ins))
                    if vals.intersection(map_string_vas):
                        print(
                            f"MAP_CALLBACK_STRING_JOIN|name={name}|node_rva=0x{node_va-base:x}|"
                            f"depth={node.get('depth',0)}|instruction_rva=0x{ins.address-base:x}"
                        )
            direct_targets = collections.Counter()
            for node in graph.values():
                direct_targets.update(node["internal"])
            for target, count in sorted(direct_targets.items()):
                if count > 1 or target == root_va:
                    continue
                trva = target - base
                if any(abs(trva - xr) < 0x400 for xr in MAP_XREF_RVAS):
                    print(
                        f"MAP_CALLBACK_NEAR_TARGET|name={name}|target_rva=0x{trva:x}|calls={count}"
                    )

        mode_vas = literal_vas(data, base, sections, FILE_MODE_LITERALS)
        for name, semantic_rva in MAP_SEMANTIC_NODES.items():
            root_va = base + MAP_CALLBACKS[name]
            graph = deep_call_graph(data, base, sections, imports, root_va)
            target_va = base + semantic_rva
            node = graph.get(target_va)
            if node is None:
                print(f"MAP_SEMANTIC_NODE_MISSING|name={name}|rva=0x{semantic_rva:x}")
                continue
            print(
                f"MAP_SEMANTIC_NODE|name={name}|rva=0x{semantic_rva:x}|depth={node.get('depth',0)}|"
                f"instructions={node['instructions']}|direct_targets={len(node['internal'])}|"
                f"end_reason={node['end_reason']}"
            )
            for ins_va, mode in node_literal_hits(
                data, base, sections, target_va, node, mode_vas
            ):
                print(
                    f"MAP_SEMANTIC_MODE|name={name}|node_rva=0x{semantic_rva:x}|"
                    f"instruction_rva=0x{ins_va-base:x}|mode={mode}"
                )
            for parent_va, callsite_va, depth in edge_calls_to(graph, target_va):
                paths = backward_paths(data, base, sections, callsite_va)
                ranked = sorted(
                    paths,
                    key=lambda path: (
                        -sum(1 for ins in path if ins.mnemonic == "push"),
                        -len(path),
                    ),
                )
                best = ranked[0] if ranked else []
                pushes = [ins for ins in best if ins.mnemonic == "push"]
                print(
                    f"MAP_SEMANTIC_CALL|name={name}|target_rva=0x{semantic_rva:x}|"
                    f"parent_rva=0x{parent_va-base:x}|callsite_rva=0x{callsite_va-base:x}|"
                    f"parent_depth={depth}|best_path_instructions={len(best)}|pushes={len(pushes)}"
                )
                for order, ins in enumerate(pushes, 1):
                    print(
                        f"MAP_SEMANTIC_ARG|name={name}|order={order}|"
                        f"instruction_rva=0x{ins.address-base:x}|"
                        f"ops={clean(operand_summary(ins,base,sections))}"
                    )

        for rva in MAP_XREF_RVAS:
            print(f"MAP_FILE_XREF|rva=0x{rva:x}")
    finally:
        img.close()
        td.cleanup()


if __name__ == "__main__":
    main()
