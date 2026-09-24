#!/usr/bin/env python3
"""Derive helper-call and parameter semantics from archived JSS SaUpdate.

This probe stays at a bounded semantic level:
- direct callers and argument sources for selected internal helpers;
- observed stack-parameter slots inside each helper;
- compare/test + conditional-branch shapes involving those slots;
- first-party string references inside helper bodies.

No executable bytes or disassembly text are retained.
"""

from __future__ import annotations

import collections
import hashlib

from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_EBP, X86_REG_ESP

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256, TIMESTAMP, parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import parse_imports
from tools.stoneage_jss_saupdate_http_flow_probe import import_thunks
from tools.stoneage_jss_saupdate_function_flow_probe import (
    disassemble_text,
    function_summary,
    resolve_call,
)
from tools.stoneage_jss_saupdate_call_args_probe import (
    ascii_strings,
    stack_args,
)
from tools.stoneage_tw10_mapcache_binary_probe import referenced_absolute_values
from tools.stoneage_tw10_technical_probe import pe_sections

HELPERS = (
    (0x25D0, "resource-generation-scan"),
    (0x31B0, "launch-control-prep"),
    (0x3610, "post-download-state"),
    (0x3C60, "update-state-sequence"),
)

MAX_ARGS = 12


def clean(value, limit=1200):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def direct_internal_target(ins):
    if ins.mnemonic != "call" or not ins.operands:
        return None
    op = ins.operands[0]
    if op.type != X86_OP_IMM:
        return None
    return int(op.imm) & 0xFFFFFFFF


def stack_param_slots(insns, start_idx, end_idx):
    """Return positive EBP slots touched inside one function."""
    rows = collections.Counter()
    examples = collections.defaultdict(list)
    for idx in range(start_idx, end_idx + 1):
        ins = insns[idx]
        for op_index, op in enumerate(ins.operands):
            if op.type != X86_OP_MEM or op.mem.base != X86_REG_EBP or op.mem.disp < 8:
                continue
            disp = int(op.mem.disp)
            rows[disp] += 1
            if len(examples[disp]) < 8:
                examples[disp].append((ins.address, ins.mnemonic, op_index))
    return rows, examples


def raw_esp_slots(insns, start_idx, end_idx):
    """Raw ESP-relative memory slots for leaf/no-frame helpers.

    These are not automatically called arguments because ESP may move. They are
    emitted only as structural evidence for reconstructing the leaf helper ABI.
    """
    rows = collections.Counter()
    examples = collections.defaultdict(list)
    for idx in range(start_idx, end_idx + 1):
        ins = insns[idx]
        for op_index, op in enumerate(ins.operands):
            if op.type != X86_OP_MEM or op.mem.base != X86_REG_ESP:
                continue
            disp = int(op.mem.disp)
            rows[disp] += 1
            if len(examples[disp]) < 12:
                examples[disp].append((ins.address, ins.mnemonic, op_index))
    return rows, examples


def helper_branches(insns, start_idx, end_idx, image_base):
    """Emit only compare/test/branch metadata, never operand text."""
    out = []
    for idx in range(start_idx, end_idx + 1):
        ins = insns[idx]
        if ins.mnemonic not in {"cmp", "test"}:
            continue
        param_slots = set()
        immediates = []
        registers = []
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_EBP and op.mem.disp >= 8:
                param_slots.add(int(op.mem.disp))
            elif op.type == X86_OP_IMM:
                immediates.append(int(op.imm) & 0xFFFFFFFF)
            elif op.type == X86_OP_REG:
                registers.append(ins.reg_name(op.reg))
        branch = None
        if idx + 1 <= end_idx:
            nxt = insns[idx + 1]
            if nxt.mnemonic.startswith("j") and nxt.mnemonic != "jmp":
                target = ""
                if nxt.operands and nxt.operands[0].type == X86_OP_IMM:
                    target = f"0x{(int(nxt.operands[0].imm) & 0xFFFFFFFF)-image_base:x}"
                branch = (nxt.mnemonic, target)
        if param_slots or immediates:
            out.append(
                {
                    "rva": ins.address - image_base,
                    "mnemonic": ins.mnemonic,
                    "params": tuple(sorted(param_slots)),
                    "immediates": tuple(immediates),
                    "registers": tuple(registers),
                    "branch": branch,
                }
            )
    return tuple(out)


def helper_string_refs(insns, start_idx, end_idx, strings, image_base):
    out = []
    seen = set()
    for idx in range(start_idx, end_idx + 1):
        ins = insns[idx]
        for value in referenced_absolute_values(ins):
            text = strings.get(value)
            if text is None:
                continue
            rec = (ins.address - image_base, value - image_base, text)
            if rec not in seen:
                seen.add(rec)
                out.append(rec)
    return tuple(out)


def helper_calls(insns, start_idx, end_idx, image_base, imports, thunks):
    out = []
    for idx in range(start_idx, end_idx + 1):
        call = resolve_call(insns[idx], image_base, imports, thunks)
        if call is None:
            continue
        kind, dll, name = call
        out.append((insns[idx].address - image_base, kind, dll, name))
    return tuple(out)


def generation_selector_summary(callers):
    """Summarize arg1 immediates passed to 0x25d0."""
    values = []
    for _, args in callers:
        if not args:
            continue
        source = args[0][1]
        if source and source.startswith("imm:0x"):
            try:
                values.append(int(source.split("0x", 1)[1], 16))
            except ValueError:
                pass
    return tuple(values)


def main():
    print("StoneAge JSS SaUpdate helper-semantics probe — R1")
    print("SCOPE|direct-callers+argument-sources+parameter-slots+branch-shapes|derived-only|no-disassembly-retained")

    status, final, headers, data = get_bounded(
        replay_url({"timestamp": TIMESTAMP, "original": ORIGINAL}),
        timeout=20,
    )
    sha = hashlib.sha256(data).hexdigest()
    print(f"FETCH|status={status}|bytes={len(data)}|sha256={sha}|final={clean(final)}")
    if sha != KNOWN_SHA256:
        print(f"RESOLUTION|HASH_MISMATCH|expected={KNOWN_SHA256}")
        return

    layout = parse_pe_layout(data)
    pe = pe_sections(data)
    image_base = pe["image_base"]
    imports = parse_imports(data, layout, image_base)
    thunks = import_thunks(data, layout, imports)
    sec, insns = disassemble_text(data, layout, image_base)
    strings = ascii_strings(data, layout, image_base)
    by_addr = {ins.address: idx for idx, ins in enumerate(insns)}

    print(
        f"PE|image_base=0x{image_base:x}|instructions={len(insns)}|"
        f"strings={len(strings)}|imports={len(imports)}"
    )

    all_callers = collections.defaultdict(list)
    helper_vas = {image_base + rva: (rva, label) for rva, label in HELPERS}
    for idx, ins in enumerate(insns):
        target = direct_internal_target(ins)
        if target not in helper_vas:
            continue
        rva, label = helper_vas[target]
        args = stack_args(insns, idx, strings, max_args=MAX_ARGS)
        all_callers[rva].append((ins.address - image_base, args))

    total_callers = 0
    for helper_rva, label in HELPERS:
        idx = by_addr.get(image_base + helper_rva)
        if idx is None:
            print(f"HELPER|label={label}|rva=0x{helper_rva:x}|decoded=0")
            continue
        f = function_summary(insns, idx, image_base, imports, thunks, strings)
        start_idx = by_addr.get(image_base + f["start_rva"])
        end_idx = by_addr.get(image_base + f["end_rva"])
        if start_idx is None or end_idx is None:
            print(f"HELPER|label={label}|rva=0x{helper_rva:x}|decoded=0|reason=boundary-index")
            continue

        callers = all_callers.get(helper_rva, [])
        total_callers += len(callers)
        slots, examples = stack_param_slots(insns, start_idx, end_idx)
        branches = helper_branches(insns, start_idx, end_idx, image_base)
        refs = helper_string_refs(insns, start_idx, end_idx, strings, image_base)
        calls = helper_calls(insns, start_idx, end_idx, image_base, imports, thunks)

        print(
            f"HELPER|label={label}|rva=0x{helper_rva:x}|decoded=1|"
            f"function_start_rva=0x{f['start_rva']:x}|function_end_rva=0x{f['end_rva']:x}|"
            f"boundary={f['boundary']}|instructions={f['instructions']}|"
            f"direct_callers={len(callers)}|parameter_slots={len(slots)}|"
            f"branch_facts={len(branches)}|string_refs={len(refs)}|calls={len(calls)}"
        )

        for order, (call_rva, args) in enumerate(callers, 1):
            print(
                f"CALLER|helper={label}|order={order}|call_rva=0x{call_rva:x}|"
                f"stack_args={len(args)}"
            )
            for arg_index, (push_va, source) in enumerate(args, 1):
                print(
                    f"CALL_ARG|helper={label}|call_rva=0x{call_rva:x}|index={arg_index}|"
                    f"push_rva=0x{push_va-image_base:x}|source={clean(source)}"
                )

        for disp, count in sorted(slots.items()):
            print(
                f"PARAM_SLOT|helper={label}|ebp_disp=+0x{disp:x}|arg_index={(disp-4)//4}|"
                f"accesses={count}"
            )
            for rva_va, mnemonic, op_index in examples[disp]:
                print(
                    f"PARAM_USE|helper={label}|ebp_disp=+0x{disp:x}|"
                    f"rva=0x{rva_va-image_base:x}|mnemonic={clean(mnemonic)}|operand_index={op_index}"
                )

        if helper_rva == 0x3C60:
            esp_rows, esp_examples = raw_esp_slots(insns, start_idx, end_idx)
            print(
                f"RAW_ESP_SLOTS|helper={label}|unique={len(esp_rows)}|"
                f"values={','.join(f'{x:+#x}' for x in sorted(esp_rows))}"
            )
            for disp, count in sorted(esp_rows.items()):
                print(
                    f"RAW_ESP_SLOT|helper={label}|disp={disp:+#x}|accesses={count}"
                )
                for rva_va, mnemonic, op_index in esp_examples[disp]:
                    print(
                        f"RAW_ESP_USE|helper={label}|disp={disp:+#x}|"
                        f"rva=0x{rva_va-image_base:x}|mnemonic={clean(mnemonic)}|operand_index={op_index}"
                    )

        for row in branches:
            branch_name = row["branch"][0] if row["branch"] else ""
            branch_target = row["branch"][1] if row["branch"] else ""
            print(
                f"BRANCH_FACT|helper={label}|rva=0x{row['rva']:x}|op={row['mnemonic']}|"
                f"param_slots={','.join(f'+0x{x:x}' for x in row['params'])}|"
                f"immediates={','.join(f'0x{x:x}' for x in row['immediates'])}|"
                f"registers={','.join(row['registers'])}|branch={clean(branch_name)}|"
                f"target_rva={clean(branch_target)}"
            )

        for order, (ins_rva, string_rva, text_value) in enumerate(refs, 1):
            print(
                f"STRING_REF|helper={label}|order={order}|ins_rva=0x{ins_rva:x}|"
                f"string_rva=0x{string_rva:x}|text={clean(text_value)}"
            )

        for order, (call_rva, kind, dll, name) in enumerate(calls, 1):
            print(
                f"HELPER_CALL|helper={label}|order={order}|call_rva=0x{call_rva:x}|"
                f"kind={kind}|dll={clean(dll)}|target={clean(name)}"
            )

        if helper_rva == 0x25D0:
            selectors = generation_selector_summary(callers)
            print(
                f"GENERATION_CALLERS|count={len(callers)}|"
                f"immediate_selectors={','.join(str(x) for x in selectors)}|"
                f"unique_selectors={','.join(str(x) for x in sorted(set(selectors)))}"
            )

    print(
        "RESOLUTION|HELPER_SEMANTICS_DERIVED|"
        f"helpers={len(HELPERS)}|direct_callers={total_callers}|binary-not-committed"
    )


if __name__ == "__main__":
    main()
