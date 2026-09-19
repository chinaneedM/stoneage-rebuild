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
    callback_cfg_probe,
    direct_rel32_call_sites,
    exact_iat_opcode_sites,
    linear_slice_calls,
    md,
    operand_summary,
    section_name_for_va,
)
from tools.stoneage_tw10_exact_xref_probe import (
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
            graph = expand_from_exact_root(data, base, sections, imports, site_va)
            print(
                f"WSOCK_RECV_GRAPH|n={n}|nodes={len(graph)}|"
                f"max_depth={max((node['depth'] for node in graph.values()), default=0)}"
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

        for rva in MAP_XREF_RVAS:
            print(f"MAP_FILE_XREF|rva=0x{rva:x}")
    finally:
        img.close()
        td.cleanup()


if __name__ == "__main__":
    main()
