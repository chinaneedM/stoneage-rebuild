#!/usr/bin/env python3
"""Trace Taiwan v1.0 server selection and endpoint provenance.

The accepted retail disc is transient in CI. Only derived addresses, call shapes,
network-looking literals, and provenance relationships are emitted.
"""

from __future__ import annotations

import argparse
import collections
from pathlib import Path
import re
import tempfile

from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from tools.stoneage_tw10_mapcache_binary_probe import (
    disassemble_text,
    image_layout,
    imported_call,
    referenced_absolute_values,
    rva_to_offset,
)
from tools.stoneage_tw10_protocol_handoff_probe import (
    backward_paths,
    direct_rel32_call_sites,
    exact_iat_opcode_sites,
    md,
    operand_summary,
    predecessor_candidates,
)
from tools.stoneage_tw10_receive_map_join_probe import (
    all_string_xrefs,
    deep_call_graph,
    file_offset_to_rva,
)

NETWORK_APIS = (
    "WSAStartup",
    "socket",
    "htons",
    "inet_addr",
    "gethostbyname",
    "connect",
    "select",
    "recv",
    "send",
    "closesocket",
)
ENDPOINT_APIS = ("socket", "htons", "inet_addr", "gethostbyname", "connect")
WAEI_XREF_RVA = 0xD4F2
LOCAL_BEFORE = 130
LOCAL_AFTER = 35
MAX_ARG_PATHS = 3
DEEP_BACKTRACE = 42
DEEP_BACKTRACE_PATHS = 24


def clean(v, limit=700):
    s = " ".join(str(v if v is not None else "").split())
    return "".join(ch for ch in s if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def section_for_va(base, sections, va):
    rva = va - base
    for sec in sections:
        if sec["rva"] <= rva < sec["rva"] + max(sec["vsize"], sec["raw_size"]):
            return sec
    return None


def ascii_at_va(data, base, sections, va, maxlen=128):
    sec = section_for_va(base, sections, va)
    if sec is None:
        return ""
    off = rva_to_offset(sections, va - base)
    if off is None:
        return ""
    raw = data[off:min(len(data), off + maxlen)]
    end = raw.find(b"\x00")
    if end >= 0:
        raw = raw[:end]
    if not raw or any(b < 0x20 or b > 0x7E for b in raw):
        return ""
    try:
        return raw.decode("ascii")
    except Exception:
        return ""


def enhanced_ops(ins, data, base, sections):
    parts = []
    for op in ins.operands:
        if op.type == X86_OP_IMM:
            value = int(op.imm) & 0xFFFFFFFF
            text = ascii_at_va(data, base, sections, value)
            if text:
                parts.append(f"imm:0x{value-base:x}:str:{clean(text,120)}")
            else:
                parts.append(f"imm:0x{value:x}")
        elif op.type == X86_OP_REG:
            parts.append(f"reg:{ins.reg_name(op.reg)}")
        elif op.type == X86_OP_MEM:
            mem = op.mem
            if mem.base == 0 and mem.index == 0:
                value = int(mem.disp) & 0xFFFFFFFF
                text = ascii_at_va(data, base, sections, value)
                if text:
                    parts.append(f"memabs:0x{value-base:x}:str:{clean(text,120)}")
                else:
                    sec = section_for_va(base, sections, value)
                    parts.append(f"memabs:0x{value-base:x}:{sec['name'] if sec else ''}")
            else:
                b = ins.reg_name(mem.base) if mem.base else ""
                x = ins.reg_name(mem.index) if mem.index else ""
                parts.append(f"mem:{b}:{x}:{int(mem.scale)}:{int(mem.disp)}")
        else:
            parts.append(f"op:{op.type}")
    return ",".join(parts)


def deep_backward_paths(data, base, sections, target_va):
    frontier = [(target_va, [])]
    complete = []
    for _ in range(DEEP_BACKTRACE):
        nxt = []
        for cursor, rev_path in frontier:
            preds = predecessor_candidates(data, base, sections, cursor)
            if not preds:
                complete.append(list(reversed(rev_path)))
                continue
            for pred in preds:
                nxt.append((pred.address, rev_path + [pred]))
                if len(nxt) >= DEEP_BACKTRACE_PATHS:
                    break
            if len(nxt) >= DEEP_BACKTRACE_PATHS:
                break
        if not nxt:
            break
        frontier = nxt[:DEEP_BACKTRACE_PATHS]
    complete.extend(list(reversed(path)) for _, path in frontier)
    uniq = {}
    for path in complete:
        key = tuple(ins.address for ins in path)
        uniq[key] = path
    return sorted(
        uniq.values(),
        key=lambda p: (-len(p), -sum(1 for ins in p if ins.mnemonic == "push")),
    )[:DEEP_BACKTRACE_PATHS]


def wsock_business_calls(data, base, sections, imports):
    result = collections.defaultdict(list)
    thunk_api = {}
    for iat_va, (dll, name) in imports.items():
        if dll.lower() != "wsock32.dll" or name not in NETWORK_APIS:
            continue
        for kind, site_va in exact_iat_opcode_sites(data, base, sections, iat_va):
            if kind == "jmp":
                thunk_api[site_va] = name
                callers = direct_rel32_call_sites(data, base, sections, site_va)
                for caller in callers:
                    result[name].append((caller, site_va, iat_va, True))
            elif kind == "call":
                result[name].append((site_va, site_va, iat_va, False))
    for name in result:
        seen = {}
        for row in result[name]:
            seen[(row[0], row[1], row[2])] = row
        result[name] = [seen[k] for k in sorted(seen)]
    return result, thunk_api


def direct_target(ins):
    if ins.mnemonic not in {"call", "jmp"}:
        return None
    for op in ins.operands:
        if op.type == X86_OP_IMM:
            return int(op.imm) & 0xFFFFFFFF
    return None


def network_event(ins, imports, thunk_api):
    imp = imported_call(ins, imports)
    if imp and imp[0].lower() == "wsock32.dll":
        return imp[1]
    target = direct_target(ins)
    if target in thunk_api:
        return thunk_api[target]
    return None


def endpoint_literals(data):
    values = set()
    for m in re.finditer(rb"[\x20-\x7e]{4,160}\x00", data):
        raw = m.group(0)[:-1]
        try:
            text = raw.decode("ascii")
        except Exception:
            continue
        low = text.lower()
        ipv4 = re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", text)
        valid_ip = False
        if ipv4:
            try:
                valid_ip = all(0 <= int(p) <= 255 for p in text.split("."))
            except Exception:
                valid_ip = False
        hostish = (
            "." in text
            and len(text) <= 100
            and any(ch.isalpha() for ch in text)
            and any(k in low for k in ("waei", "hwaei", "stoneage", "server", "wgs", ".com", ".net", ".tw"))
        )
        if valid_ip or hostish or low == "waei.bin":
            values.add((m.start(), text))
    return sorted(values)


def graph_business_hits(graph, base, business):
    sites = {}
    for api, rows in business.items():
        for site_va, thunk_va, iat_va, via_thunk in rows:
            sites[site_va] = api
    hits = []
    for node_va, node in graph.items():
        start = node_va
        end = node.get("end_va", node_va) + 8
        for site_va, api in sites.items():
            if start <= site_va <= end:
                hits.append((node_va, node.get("depth",0), site_va, api))
    return sorted(set(hits))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", required=True)
    args = ap.parse_args()

    print("StoneAge Taiwan v1.0 server-selection probe — R1")
    print("SCOPE|ephemeral-verified-disc|winsock-endpoint-provenance|derived-only")

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
        text_sec, instructions = disassemble_text(data, base, sections)
        index_by_va = {ins.address: i for i, ins in enumerate(instructions)}

        print(
            f"RUNTIME|bytes={exe.stat().st_size}|image_base=0x{base:x}|"
            f"text_rva=0x{text_sec['rva']:x}|text_bytes={text_sec['raw_size']}|"
            f"imports={len(imports)}|layout={layout}|joliet={int(joliet)}"
        )

        business, thunk_api = wsock_business_calls(data, base, sections, imports)
        for api in NETWORK_APIS:
            rows_api = business.get(api, [])
            print(f"WSOCK_API|name={api}|business_calls={len(rows_api)}")
            for n, (site_va, thunk_va, iat_va, via_thunk) in enumerate(rows_api, 1):
                print(
                    f"WSOCK_CALL|api={api}|n={n}|callsite_rva=0x{site_va-base:x}|"
                    f"thunk_rva=0x{thunk_va-base:x}|iat_rva=0x{iat_va-base:x}|"
                    f"via_thunk={int(via_thunk)}"
                )

                if api in ENDPOINT_APIS:
                    paths = backward_paths(data, base, sections, site_va)[:MAX_ARG_PATHS]
                    for pno, path in enumerate(paths, 1):
                        print(
                            f"ARG_PATH|api={api}|n={n}|path={pno}|instructions={len(path)}|"
                            f"pushes={sum(1 for ins in path if ins.mnemonic == 'push')}"
                        )
                        for order, ins in enumerate(path, 1):
                            if ins.mnemonic in {"push", "mov", "lea", "call"}:
                                print(
                                    f"ARG_INS|api={api}|n={n}|path={pno}|order={order}|"
                                    f"instruction_rva=0x{ins.address-base:x}|mnemonic={clean(ins.mnemonic)}|"
                                    f"ops={clean(enhanced_ops(ins,data,base,sections))}"
                                )

                    deep_paths = deep_backward_paths(data, base, sections, site_va)
                    if deep_paths:
                        path = deep_paths[0]
                        print(
                            f"DEEP_ARG_PATH|api={api}|n={n}|instructions={len(path)}|"
                            f"pushes={sum(1 for ins in path if ins.mnemonic == 'push')}|"
                            f"start_rva=0x{path[0].address-base:x}"
                        )
                        for order, ins in enumerate(path, 1):
                            if ins.mnemonic in {"push", "mov", "lea", "call", "cmp", "test"}:
                                print(
                                    f"DEEP_ARG_INS|api={api}|n={n}|order={order}|"
                                    f"instruction_rva=0x{ins.address-base:x}|mnemonic={clean(ins.mnemonic)}|"
                                    f"ops={clean(enhanced_ops(ins,data,base,sections))}"
                                )

        for off, text in endpoint_literals(data):
            rva = file_offset_to_rva(sections, off)
            print(
                f"NET_LITERAL|file_offset=0x{off:x}|rva={'' if rva is None else hex(rva)}|"
                f"text={clean(text,160)}"
            )

        # For every connect business call, emit nearby WSOCK call order from the
        # full .text disassembly. This distinguishes independent networking clusters.
        for n, (connect_va, _, _, _) in enumerate(business.get("connect", []), 1):
            idx = index_by_va.get(connect_va)
            if idx is None:
                continue
            lo = max(0, idx - LOCAL_BEFORE)
            hi = min(len(instructions), idx + LOCAL_AFTER + 1)
            events = []
            for ins in instructions[lo:hi]:
                api = network_event(ins, imports, thunk_api)
                if api:
                    events.append((ins.address, api))
            print(
                f"CONNECT_CLUSTER|n={n}|callsite_rva=0x{connect_va-base:x}|"
                f"window_instructions={hi-lo}|network_events={len(events)}"
            )
            for order, (addr, api) in enumerate(events, 1):
                print(
                    f"CONNECT_EVENT|n={n}|order={order}|instruction_rva=0x{addr-base:x}|api={api}"
                )

        # Test whether the known waei.bin code path actually joins networking.
        waei_rows = all_string_xrefs(data, base, sections, "waei.bin")
        print(f"WAEI_BIN|decoded_xrefs={len(waei_rows)}")
        for occurrence, string_rva, ins in waei_rows:
            graph = deep_call_graph(data, base, sections, imports, ins.address, max_depth=12, max_nodes=220)
            print(
                f"WAEI_GRAPH|occurrence={occurrence}|xref_rva=0x{ins.address-base:x}|"
                f"nodes={len(graph)}|max_depth={max((node['depth'] for node in graph.values()),default=0)}"
            )
            for node_va, depth, site_va, api in graph_business_hits(graph, base, business):
                print(
                    f"WAEI_NETWORK_JOIN|occurrence={occurrence}|api={api}|"
                    f"node_rva=0x{node_va-base:x}|depth={depth}|callsite_rva=0x{site_va-base:x}"
                )

    finally:
        img.close()
        td.cleanup()


if __name__ == "__main__":
    main()
