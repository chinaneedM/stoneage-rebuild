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
from tools.stoneage_tw10_exact_xref_probe import (
    decode_forward_node,
    raw_text_pointer_hits,
    recover_xref_instruction,
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
    decode_node_instructions,
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
SERVER_INFO_RVA = 0x2E950
SERVER_TABLE_RVA = 0x13F5E40
SERVER_RECORD_SIZE = 193
SERVER_SLOT_COUNT = 10
SERVER_IP_OFFSET = 1
SERVER_PORT_OFFSET = 129
SERVER_NAME_TABLE_RVA = 0x588B0
SERVER_NAME_RECORD_SIZE = 64
SELECT_SERVER_INDEX_RVA = 0x5C860
CMDLINE_BUFFER_RVA = 0x139B758
CONNECT_RESET_RVA = 0x2EE20
CONNECT_GAME_RVA = 0x2EE2C
SERVER_LOOKUP_WINDOW_RVA = 0x2E840
SERVER_WRITER_RANGE_START_RVA = 0x2E800
SERVER_WRITER_RANGE_END_RVA = 0x2E950
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


def data_displacements(ins, base, sections):
    out = set()
    for op in ins.operands:
        if op.type != X86_OP_MEM:
            continue
        value = int(op.mem.disp) & 0xFFFFFFFF
        sec = section_for_va(base, sections, value)
        if sec is not None and sec["name"] in {".data", ".rdata", ".bss"}:
            out.add(value)
    return out


def server_table_refs(instructions, base):
    table_lo = base + SERVER_TABLE_RVA
    table_hi = table_lo + SERVER_RECORD_SIZE
    out = []
    for ins in instructions:
        for op_index, op in enumerate(ins.operands):
            if op.type != X86_OP_MEM:
                continue
            disp = int(op.mem.disp) & 0xFFFFFFFF
            if table_lo <= disp < table_hi:
                is_write = (
                    op_index == 0
                    and ins.mnemonic
                    in {
                        "mov", "movsx", "movzx", "stosb", "stosd", "stosw",
                        "add", "sub", "or", "and", "xor", "inc", "dec"
                    }
                )
                out.append(
                    {
                        "ins": ins,
                        "op_index": op_index,
                        "disp": disp,
                        "offset": disp - table_lo,
                        "base_reg": ins.reg_name(op.mem.base) if op.mem.base else "",
                        "index_reg": ins.reg_name(op.mem.index) if op.mem.index else "",
                        "scale": int(op.mem.scale),
                        "write": is_write,
                    }
                )
    return out


def exact_pointer_refs(data, base, sections, target_rva):
    target_va = base + target_rva
    rows = []
    for hit in raw_text_pointer_hits(data, base, sections, target_va):
        ins = recover_xref_instruction(data, base, sections, hit, target_va)
        if ins is None:
            rows.append((hit["ptr_rva"], None))
        else:
            rows.append((hit["ptr_rva"], ins))
    return rows


def nontext_server_table_pointer_stores(data, base, sections):
    lo = base + SERVER_TABLE_RVA
    hi = lo + SERVER_RECORD_SIZE * SERVER_SLOT_COUNT
    rows = []
    for sec in sections:
        if sec["name"] == ".text" or sec["raw_size"] < 4:
            continue
        blob = data[sec["raw"]:sec["raw"] + sec["raw_size"]]
        for rel in range(0, len(blob) - 3):
            value = int.from_bytes(blob[rel:rel + 4], "little")
            if lo <= value <= hi:
                rows.append(
                    {
                        "section": sec["name"],
                        "storage_rva": sec["rva"] + rel,
                        "target_rva": value - base,
                    }
                )
    return rows


def raw_server_table_range_refs(data, base, sections):
    text_sec = next((sec for sec in sections if sec["name"] == ".text"), None)
    if text_sec is None:
        return []
    blob = data[text_sec["raw"]:text_sec["raw"] + text_sec["raw_size"]]
    lo = base + SERVER_TABLE_RVA
    hi = lo + SERVER_RECORD_SIZE * SERVER_SLOT_COUNT
    rows = []
    seen = set()
    for rel in range(0, max(0, len(blob) - 3)):
        value = int.from_bytes(blob[rel:rel + 4], "little")
        if not (lo <= value <= hi):
            continue
        ptr_rva = text_sec["rva"] + rel
        key = (ptr_rva, value)
        if key in seen:
            continue
        seen.add(key)
        hit = {
            "ptr_file_offset": text_sec["raw"] + rel,
            "ptr_rva": ptr_rva,
            "ptr_va": base + ptr_rva,
        }
        decoder = md()
        candidates = []
        for back in range(0, 16):
            start = hit["ptr_file_offset"] - back
            if start < 0:
                continue
            rva = file_offset_to_rva(sections, start)
            if isinstance(rva, tuple):
                rva = rva[0]
            if rva is None:
                continue
            decoded = list(decoder.disasm(data[start:min(len(data), start + 24)], base + rva, count=1))
            if not decoded:
                continue
            ins = decoded[0]
            if not (start <= hit["ptr_file_offset"] and hit["ptr_file_offset"] + 4 <= start + ins.size):
                continue
            if value not in set(referenced_absolute_values(ins)):
                continue
            preds = predecessor_candidates(data, base, sections, ins.address)
            candidates.append((len(preds), back, ins))
        candidates.sort(key=lambda x: (-x[0], x[1], x[2].size))
        rows.append((ptr_rva, value, candidates))
    return rows


def exact_pointer_ref_candidates(data, base, sections, target_rva):
    target_va = base + target_rva
    rows = []
    decoder = md()
    for hit in raw_text_pointer_hits(data, base, sections, target_va):
        ptr_off = hit["ptr_file_offset"]
        candidates = []
        for back in range(0, 16):
            start = ptr_off - back
            if start < 0:
                continue
            rva = file_offset_to_rva(sections, start)
            if isinstance(rva, tuple):
                rva = rva[0]
            if rva is None:
                continue
            blob = data[start:min(len(data), start + 24)]
            decoded = list(decoder.disasm(blob, base + rva, count=1))
            if not decoded:
                continue
            ins = decoded[0]
            if not (start <= ptr_off and ptr_off + 4 <= start + ins.size):
                continue
            refs = set(referenced_absolute_values(ins))
            if target_va not in refs:
                continue
            preds = predecessor_candidates(data, base, sections, ins.address)
            candidates.append((back, len(preds), ins))
        rows.append((hit["ptr_rva"], sorted(candidates, key=lambda x: (-x[1], x[0], x[2].size))))
    return rows


def forward_context(data, base, sections, start_va, limit=64):
    off = rva_to_offset(sections, start_va - base)
    if off is None:
        return []
    sec = section_for_va(base, sections, start_va)
    if sec is None:
        return []
    end = min(len(data), sec["raw"] + sec["raw_size"], off + 512)
    decoder = md()
    out = []
    for ins in decoder.disasm(data[off:end], start_va, count=limit):
        out.append(ins)
        if ins.mnemonic.startswith("ret"):
            break
    return out


def linear_context(data, base, sections, start_va, max_bytes=0x600, limit=500):
    off = rva_to_offset(sections, start_va - base)
    if off is None:
        return []
    sec = section_for_va(base, sections, start_va)
    if sec is None:
        return []
    end = min(len(data), sec["raw"] + sec["raw_size"], off + max_bytes)
    return list(md().disasm(data[off:end], start_va, count=limit))


def direct_calls_into_rva_range(data, base, sections, start_rva, end_rva):
    sec = next((s for s in sections if s["name"] == ".text"), None)
    if sec is None:
        return []
    blob = data[sec["raw"]:sec["raw"] + sec["raw_size"]]
    rows = []
    for rel in range(0, max(0, len(blob) - 5)):
        if blob[rel] != 0xE8:
            continue
        disp = int.from_bytes(blob[rel + 1:rel + 5], "little", signed=True)
        site_va = base + sec["rva"] + rel
        target_va = (site_va + 5 + disp) & 0xFFFFFFFF
        target_rva = target_va - base
        if start_rva <= target_rva < end_rva:
            rows.append((site_va, target_va))
    return sorted(set(rows))


def static_cstr_at_rva(data, sections, rva, maxlen):
    off = rva_to_offset(sections, rva)
    if off is None:
        return None
    raw = data[off:min(len(data), off + maxlen)]
    end = raw.find(b"\x00")
    if end >= 0:
        raw = raw[:end]
    if not raw:
        return ""
    if any(b < 0x20 or b > 0x7E for b in raw):
        return "<non-ascii>"
    return raw.decode("ascii", "replace")


def function_data_globals(data, base, sections, imports, rva):
    va = base + rva
    node = decode_forward_node(data, base, sections, imports, va)
    if node is None:
        return None, collections.Counter()
    globals_seen = collections.Counter()
    for ins in decode_node_instructions(data, base, sections, va, node.get("end_va", va)):
        for value in data_displacements(ins, base, sections):
            globals_seen[value] += 1
    return node, globals_seen


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
                            if ins.mnemonic in {"push", "mov", "movsx", "movzx", "lea", "call", "cmp", "test"}:
                                print(
                                    f"DEEP_ARG_INS|api={api}|n={n}|order={order}|"
                                    f"instruction_rva=0x{ins.address-base:x}|mnemonic={clean(ins.mnemonic)}|"
                                    f"ops={clean(enhanced_ops(ins,data,base,sections))}"
                                )

        reset_ctx = forward_context(
            data, base, sections, base + CONNECT_RESET_RVA, limit=16
        )
        reset_callers = direct_rel32_call_sites(data, base, sections, base + CONNECT_RESET_RVA)
        print(
            f"CONNECT_RESET|start_rva=0x{CONNECT_RESET_RVA:x}|"
            f"instructions={len(reset_ctx)}|callers={len(reset_callers)}"
        )
        for caller in reset_callers:
            print(f"CONNECT_RESET_CALLER|callsite_rva=0x{caller-base:x}")
        for order, ins in enumerate(reset_ctx, 1):
            print(
                f"CONNECT_RESET_INS|order={order}|instruction_rva=0x{ins.address-base:x}|"
                f"mnemonic={clean(ins.mnemonic)}|ops={clean(enhanced_ops(ins,data,base,sections))}"
            )

        game_ctx = linear_context(
            data, base, sections, base + CONNECT_GAME_RVA, max_bytes=0x520, limit=420
        )
        game_callers = direct_rel32_call_sites(data, base, sections, base + CONNECT_GAME_RVA)
        print(
            f"CONNECT_GAME|start_rva=0x{CONNECT_GAME_RVA:x}|"
            f"instructions={len(game_ctx)}|callers={len(game_callers)}"
        )
        for caller in game_callers:
            print(f"CONNECT_GAME_CALLER|callsite_rva=0x{caller-base:x}")
        for order, ins in enumerate(game_ctx, 1):
            api = network_event(ins, imports, thunk_api)
            branch = ins.mnemonic.startswith("j") or ins.mnemonic.startswith("ret")
            if api or branch or ins.mnemonic in {
                "mov", "movsx", "movzx", "lea", "push", "call", "cmp", "test",
                "add", "sub", "imul", "shl", "shr", "xor", "and", "or"
            }:
                extra = f"|api={api}" if api else ""
                print(
                    f"CONNECT_GAME_INS|order={order}|instruction_rva=0x{ins.address-base:x}|"
                    f"mnemonic={clean(ins.mnemonic)}|ops={clean(enhanced_ops(ins,data,base,sections))}{extra}"
                )

        writer_calls = direct_calls_into_rva_range(
            data, base, sections, SERVER_WRITER_RANGE_START_RVA, SERVER_WRITER_RANGE_END_RVA
        )
        print(
            f"SERVER_WRITER_CALL_TARGETS|start_rva=0x{SERVER_WRITER_RANGE_START_RVA:x}|"
            f"end_rva=0x{SERVER_WRITER_RANGE_END_RVA:x}|calls={len(writer_calls)}"
        )
        for n, (site_va, target_va) in enumerate(writer_calls, 1):
            print(
                f"SERVER_WRITER_CALL|n={n}|callsite_rva=0x{site_va-base:x}|"
                f"target_rva=0x{target_va-base:x}"
            )
            paths = deep_backward_paths(data, base, sections, site_va)
            if paths:
                path = paths[0]
                print(
                    f"SERVER_WRITER_ARG_PATH|n={n}|instructions={len(path)}|"
                    f"start_rva=0x{path[0].address-base:x}"
                )
                for order, prev in enumerate(path, 1):
                    if prev.mnemonic in {"push", "mov", "movsx", "movzx", "lea", "call", "cmp", "test"}:
                        print(
                            f"SERVER_WRITER_ARG_INS|n={n}|order={order}|"
                            f"instruction_rva=0x{prev.address-base:x}|mnemonic={clean(prev.mnemonic)}|"
                            f"ops={clean(enhanced_ops(prev,data,base,sections))}"
                        )

        lookup_ctx = linear_context(
            data, base, sections, base + SERVER_LOOKUP_WINDOW_RVA, max_bytes=0x120, limit=180
        )
        print(
            f"SERVER_LOOKUP_WINDOW|start_rva=0x{SERVER_LOOKUP_WINDOW_RVA:x}|"
            f"instructions={len(lookup_ctx)}"
        )
        for order, ins in enumerate(lookup_ctx, 1):
            if ins.mnemonic.startswith("j") or ins.mnemonic.startswith("ret") or ins.mnemonic in {
                "mov", "movsx", "movzx", "lea", "push", "call", "cmp", "test",
                "add", "sub", "imul", "shl", "shr", "xor", "and", "or",
                "rep movsb", "rep movsd"
            }:
                print(
                    f"SERVER_LOOKUP_INS|order={order}|instruction_rva=0x{ins.address-base:x}|"
                    f"mnemonic={clean(ins.mnemonic)}|ops={clean(enhanced_ops(ins,data,base,sections))}"
                )

        cmd_refs = exact_pointer_refs(data, base, sections, CMDLINE_BUFFER_RVA)
        print(
            f"CMDLINE_BUFFER_XREFS|target_rva=0x{CMDLINE_BUFFER_RVA:x}|count={len(cmd_refs)}"
        )
        for n, (ptr_rva, ins) in enumerate(cmd_refs, 1):
            if ins is None:
                print(
                    f"CMDLINE_BUFFER_XREF|n={n}|pointer_rva=0x{ptr_rva:x}|decoded=0"
                )
                continue
            print(
                f"CMDLINE_BUFFER_XREF|n={n}|pointer_rva=0x{ptr_rva:x}|decoded=1|"
                f"instruction_rva=0x{ins.address-base:x}|mnemonic={clean(ins.mnemonic)}|"
                f"ops={clean(enhanced_ops(ins,data,base,sections))}"
            )
            paths = deep_backward_paths(data, base, sections, ins.address)
            path = next((candidate for candidate in paths if candidate), None)
            if path:
                print(
                    f"CMDLINE_BUFFER_BACKTRACE|n={n}|instructions={len(path)}|"
                    f"start_rva=0x{path[0].address-base:x}"
                )
                for order, prev in enumerate(path, 1):
                    if prev.mnemonic in {
                        "push", "mov", "movsx", "movzx", "lea", "call", "cmp", "test"
                    }:
                        print(
                            f"CMDLINE_BUFFER_PREV|n={n}|order={order}|"
                            f"instruction_rva=0x{prev.address-base:x}|mnemonic={clean(prev.mnemonic)}|"
                            f"ops={clean(enhanced_ops(prev,data,base,sections))}"
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

        server_node, server_globals = function_data_globals(
            data, base, sections, imports, SERVER_INFO_RVA
        )
        if server_node is None:
            print(f"SERVER_INFO_MISSING|rva=0x{SERVER_INFO_RVA:x}")
        else:
            callers = direct_rel32_call_sites(data, base, sections, base + SERVER_INFO_RVA)
            print(
                f"SERVER_INFO|rva=0x{SERVER_INFO_RVA:x}|instructions={server_node['instructions']}|"
                f"direct_targets={len(server_node['internal'])}|callers={len(callers)}|"
                f"data_globals={len(server_globals)}|end_reason={server_node['end_reason']}"
            )
            for caller in callers:
                print(f"SERVER_INFO_CALLER|callsite_rva=0x{caller-base:x}")
            for value, count in sorted(server_globals.items()):
                print(
                    f"SERVER_INFO_GLOBAL|rva=0x{value-base:x}|section={section_for_va(base,sections,value)['name']}|refs={count}"
                )
            for order, ins in enumerate(
                decode_node_instructions(
                    data, base, sections, base + SERVER_INFO_RVA, server_node.get("end_va", base + SERVER_INFO_RVA)
                ),
                1,
            ):
                print(
                    f"SERVER_INFO_INS|order={order}|instruction_rva=0x{ins.address-base:x}|"
                    f"mnemonic={clean(ins.mnemonic)}|ops={clean(enhanced_ops(ins,data,base,sections))}"
                )

        table_refs = server_table_refs(instructions, base)
        print(
            f"SERVER_TABLE|rva=0x{SERVER_TABLE_RVA:x}|record_size={SERVER_RECORD_SIZE}|"
            f"refs={len(table_refs)}|writes={sum(1 for row in table_refs if row['write'])}|"
            f"select_index_rva=0x{SELECT_SERVER_INDEX_RVA:x}"
        )
        table_sec = section_for_va(base, sections, base + SERVER_TABLE_RVA)
        table_off = rva_to_offset(sections, SERVER_TABLE_RVA)
        if table_sec is not None:
            print(
                f"SERVER_TABLE_STORAGE|section={table_sec['name']}|section_rva=0x{table_sec['rva']:x}|"
                f"raw_size={table_sec['raw_size']}|vsize={table_sec['vsize']}|"
                f"offset_in_section={SERVER_TABLE_RVA-table_sec['rva']}|"
                f"file_backed={int(table_off is not None)}"
            )
        print(
            f"SERVER_LAYOUT_INFERENCE|slots={SERVER_SLOT_COUNT}|record_size={SERVER_RECORD_SIZE}|"
            f"used_offset=0|ip_offset={SERVER_IP_OFFSET}|ip_span={SERVER_PORT_OFFSET-SERVER_IP_OFFSET}|"
            f"port_offset={SERVER_PORT_OFFSET}|port_span={SERVER_RECORD_SIZE-SERVER_PORT_OFFSET}"
        )
        for slot in range(SERVER_SLOT_COUNT):
            row_rva = SERVER_TABLE_RVA + slot * SERVER_RECORD_SIZE
            host = static_cstr_at_rva(data, sections, row_rva + SERVER_IP_OFFSET, SERVER_PORT_OFFSET-SERVER_IP_OFFSET)
            port = static_cstr_at_rva(data, sections, row_rva + SERVER_PORT_OFFSET, SERVER_RECORD_SIZE-SERVER_PORT_OFFSET)
            print(
                f"SERVER_SLOT_INITIAL|slot={slot}|mapped={int(host is not None and port is not None)}|"
                f"host={clean(host if host is not None else '<unmapped>',160)}|"
                f"port={clean(port if port is not None else '<unmapped>',80)}"
            )

        for slot in range(SERVER_SLOT_COUNT):
            name = static_cstr_at_rva(
                data, sections, SERVER_NAME_TABLE_RVA + slot * SERVER_NAME_RECORD_SIZE,
                SERVER_NAME_RECORD_SIZE
            )
            print(
                f"SERVER_NAME_SLOT_INITIAL|slot={slot}|"
                f"name={clean(name if name is not None else '<unmapped>',160)}"
            )
        app_label = static_cstr_at_rva(data, sections, 0x59184, 96)
        print(
            f"SERVER_TITLE_LABEL|rva=0x59184|text={clean(app_label if app_label is not None else '<unmapped>',160)}"
        )

        indirect_rows = nontext_server_table_pointer_stores(data, base, sections)
        print(f"SERVER_TABLE_NON_TEXT_POINTERS|count={len(indirect_rows)}")
        for n, rowptr in enumerate(indirect_rows, 1):
            print(
                f"SERVER_TABLE_NON_TEXT_POINTER|n={n}|section={rowptr['section']}|"
                f"storage_rva=0x{rowptr['storage_rva']:x}|target_rva=0x{rowptr['target_rva']:x}"
            )
            storage_refs = exact_pointer_refs(data, base, sections, rowptr["storage_rva"])
            print(
                f"SERVER_TABLE_POINTER_STORAGE_XREFS|n={n}|storage_rva=0x{rowptr['storage_rva']:x}|"
                f"count={len(storage_refs)}"
            )
            for xno, (ptr_rva, ins) in enumerate(storage_refs, 1):
                if ins is None:
                    print(
                        f"SERVER_TABLE_POINTER_STORAGE_XREF|n={n}|xref={xno}|"
                        f"pointer_rva=0x{ptr_rva:x}|decoded=0"
                    )
                else:
                    print(
                        f"SERVER_TABLE_POINTER_STORAGE_XREF|n={n}|xref={xno}|"
                        f"pointer_rva=0x{ptr_rva:x}|decoded=1|"
                        f"instruction_rva=0x{ins.address-base:x}|mnemonic={clean(ins.mnemonic)}|"
                        f"ops={clean(enhanced_ops(ins,data,base,sections))}"
                    )

        range_rows = raw_server_table_range_refs(data, base, sections)
        print(
            f"SERVER_TABLE_RANGE_XREFS|start_rva=0x{SERVER_TABLE_RVA:x}|"
            f"end_rva=0x{SERVER_TABLE_RVA + SERVER_RECORD_SIZE * SERVER_SLOT_COUNT:x}|"
            f"raw_hits={len(range_rows)}"
        )
        for n, (ptr_rva, value, candidates) in enumerate(range_rows, 1):
            offset = value - (base + SERVER_TABLE_RVA)
            slot = offset // SERVER_RECORD_SIZE if offset < SERVER_RECORD_SIZE * SERVER_SLOT_COUNT else SERVER_SLOT_COUNT
            field_offset = offset % SERVER_RECORD_SIZE if offset < SERVER_RECORD_SIZE * SERVER_SLOT_COUNT else 0
            if candidates:
                pred_count, back, best = candidates[0]
                print(
                    f"SERVER_TABLE_RANGE_XREF|n={n}|pointer_rva=0x{ptr_rva:x}|"
                    f"target_rva=0x{value-base:x}|offset={offset}|slot={slot}|field_offset={field_offset}|"
                    f"candidates={len(candidates)}|best_rva=0x{best.address-base:x}|"
                    f"predecessors={pred_count}|back={back}|mnemonic={clean(best.mnemonic)}|"
                    f"ops={clean(enhanced_ops(best,data,base,sections))}"
                )
            else:
                print(
                    f"SERVER_TABLE_RANGE_XREF|n={n}|pointer_rva=0x{ptr_rva:x}|"
                    f"target_rva=0x{value-base:x}|offset={offset}|slot={slot}|field_offset={field_offset}|"
                    f"candidates=0"
                )

        exact_targets = (
            ("table_base", SERVER_TABLE_RVA),
            ("table_end", SERVER_TABLE_RVA + SERVER_RECORD_SIZE * SERVER_SLOT_COUNT),
            ("ip_field_0", SERVER_TABLE_RVA + SERVER_IP_OFFSET),
            ("port_field_0", SERVER_TABLE_RVA + SERVER_PORT_OFFSET),
            ("select_index", SELECT_SERVER_INDEX_RVA),
        )
        for label, target_rva in exact_targets:
            rows_exact = exact_pointer_refs(data, base, sections, target_rva)
            print(
                f"EXACT_DATA_XREFS|label={label}|target_rva=0x{target_rva:x}|count={len(rows_exact)}"
            )
            for n, (ptr_rva, ins) in enumerate(rows_exact, 1):
                if ins is None:
                    print(
                        f"EXACT_DATA_XREF|label={label}|n={n}|pointer_rva=0x{ptr_rva:x}|decoded=0"
                    )
                    continue
                print(
                    f"EXACT_DATA_XREF|label={label}|n={n}|pointer_rva=0x{ptr_rva:x}|decoded=1|"
                    f"instruction_rva=0x{ins.address-base:x}|mnemonic={clean(ins.mnemonic)}|"
                    f"ops={clean(enhanced_ops(ins,data,base,sections))}"
                )

            candidate_rows = exact_pointer_ref_candidates(data, base, sections, target_rva)
            for n, (ptr_rva, candidates) in enumerate(candidate_rows, 1):
                print(
                    f"EXACT_XREF_CANDIDATES|label={label}|n={n}|pointer_rva=0x{ptr_rva:x}|"
                    f"count={len(candidates)}"
                )
                for cno, (back, pred_count, candidate) in enumerate(candidates, 1):
                    print(
                        f"EXACT_XREF_CANDIDATE|label={label}|n={n}|candidate={cno}|"
                        f"instruction_rva=0x{candidate.address-base:x}|back={back}|"
                        f"predecessors={pred_count}|mnemonic={clean(candidate.mnemonic)}|"
                        f"ops={clean(enhanced_ops(candidate,data,base,sections))}"
                    )

            if label in {"table_base", "select_index"}:
                for n, (_, ins) in enumerate(rows_exact, 1):
                    if ins is None:
                        continue
                    context = forward_context(data, base, sections, ins.address, limit=72)
                    print(
                        f"XREF_FORWARD_CONTEXT|label={label}|n={n}|"
                        f"start_rva=0x{ins.address-base:x}|instructions={len(context)}"
                    )
                    for order, ctx in enumerate(context, 1):
                        if ctx.mnemonic in {
                            "mov", "movsx", "movzx", "lea", "push", "call", "cmp", "test",
                            "rep movsb", "rep movsd", "rep stosb", "rep stosd", "stosb", "stosd",
                            "add", "sub", "imul", "shl", "shr", "xor", "and", "or"
                        }:
                            print(
                                f"XREF_FORWARD_INS|label={label}|n={n}|order={order}|"
                                f"instruction_rva=0x{ctx.address-base:x}|mnemonic={clean(ctx.mnemonic)}|"
                                f"ops={clean(enhanced_ops(ctx,data,base,sections))}"
                            )
        for n, row in enumerate(table_refs, 1):
            ins = row["ins"]
            print(
                f"SERVER_TABLE_REF|n={n}|instruction_rva=0x{ins.address-base:x}|"
                f"mnemonic={clean(ins.mnemonic)}|op_index={row['op_index']}|"
                f"field_offset={row['offset']}|base_reg={clean(row['base_reg'])}|"
                f"index_reg={clean(row['index_reg'])}|scale={row['scale']}|"
                f"write={int(row['write'])}|ops={clean(enhanced_ops(ins,data,base,sections))}"
            )

        # Test whether the known waei.bin code path actually joins networking or
        # touches the same server-table globals / record region.
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
            server_global_set = set(server_globals)
            table_lo = base + SERVER_TABLE_RVA
            table_hi = table_lo + SERVER_RECORD_SIZE
            for node_va, node in sorted(graph.items()):
                insns = decode_node_instructions(
                    data, base, sections, node_va, node.get("end_va", node_va)
                )
                for ins2 in insns:
                    for value in data_displacements(ins2, base, sections):
                        if value in server_global_set:
                            print(
                                f"WAEI_SERVER_GLOBAL_JOIN|occurrence={occurrence}|"
                                f"node_rva=0x{node_va-base:x}|depth={node.get('depth',0)}|"
                                f"instruction_rva=0x{ins2.address-base:x}|global_rva=0x{value-base:x}"
                            )
                    for op in ins2.operands:
                        if op.type != X86_OP_MEM:
                            continue
                        disp = int(op.mem.disp) & 0xFFFFFFFF
                        if table_lo <= disp < table_hi:
                            print(
                                f"WAEI_SERVER_TABLE_JOIN|occurrence={occurrence}|"
                                f"node_rva=0x{node_va-base:x}|depth={node.get('depth',0)}|"
                                f"instruction_rva=0x{ins2.address-base:x}|"
                                f"field_offset={disp-table_lo}|mnemonic={clean(ins2.mnemonic)}"
                            )

    finally:
        img.close()
        td.cleanup()


if __name__ == "__main__":
    main()
