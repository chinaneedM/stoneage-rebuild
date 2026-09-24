#!/usr/bin/env python3
"""Bounded emulation of the no-import JSS SaUpdate token helper at RVA 0x3c60.

The exact archived SaUpdate bytes are fetched transiently. Only deterministic
input/output examples and register summaries are emitted. No executable bytes or
instruction text are retained.
"""

from __future__ import annotations

import hashlib
import struct

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_EAX, UC_X86_REG_EIP

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256, TIMESTAMP, parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import rva_to_offset
from tools.stoneage_tw10_technical_probe import pe_sections

FUNC_RVA = 0x3C60
MAX_INSNS = 2000
STACK_BASE = 0x10000000
STACK_SIZE = 0x10000
SCRATCH_BASE = 0x20000000
SCRATCH_SIZE = 0x10000
SENTINEL = 0x30000000

CASES = (
    "alpha beta gamma",
    "alpha:beta:gamma",
    "alpha\tbeta\tgamma",
    "  alpha : beta\tgamma  ",
    "realbin:12",
    "one::three",
    "one two",
)


def clean(value, limit=700):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def c_string(data):
    data = bytes(data)
    end = data.find(b"\0")
    if end < 0:
        end = len(data)
    return data[:end]


def map_image(uc, data, layout, image_base):
    # The image's highest RVA is below 0x500000 in this artifact; derive the
    # bound instead of hard-coding it.
    high = 0x1000
    for sec in layout["sections"]:
        high = max(high, sec["vaddr"] + max(sec["vsize"], sec["raw_size"]))
    size = (high + 0xFFF) & ~0xFFF
    uc.mem_map(image_base, size)
    for sec in layout["sections"]:
        raw_start = sec["raw_ptr"]
        raw_end = min(len(data), raw_start + sec["raw_size"])
        if raw_end > raw_start:
            uc.mem_write(image_base + sec["vaddr"], data[raw_start:raw_end])
    return size


def emulate_case(data, layout, image_base, text, field_index, max_len=0x400):
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    map_image(uc, data, layout, image_base)
    uc.mem_map(STACK_BASE, STACK_SIZE)
    uc.mem_map(SCRATCH_BASE, SCRATCH_SIZE)
    uc.mem_map(SENTINEL, 0x1000)

    dest = SCRATCH_BASE + 0x100
    src = SCRATCH_BASE + 0x1000
    source = text.encode("ascii") + b"\0"
    uc.mem_write(src, source)
    uc.mem_write(dest, b"\xCC" * 0x800)

    esp = STACK_BASE + STACK_SIZE - 0x100
    frame = struct.pack(
        "<IIIII",
        SENTINEL,
        dest,
        int(field_index),
        src,
        int(max_len),
    )
    uc.mem_write(esp, frame)
    uc.reg_write(UC_X86_REG_ESP, esp)

    counter = {"n": 0}
    def hook_code(emu, address, size, user_data):
        counter["n"] += 1
        if counter["n"] > MAX_INSNS:
            emu.emu_stop()
            raise RuntimeError("instruction bound exceeded")
    uc.hook_add(UC_HOOK_CODE, hook_code)

    uc.emu_start(image_base + FUNC_RVA, SENTINEL, count=MAX_INSNS)
    eip = uc.reg_read(UC_X86_REG_EIP) & 0xFFFFFFFF
    out = c_string(uc.mem_read(dest, 0x400))
    eax = uc.reg_read(UC_X86_REG_EAX) & 0xFFFFFFFF
    return {
        "out": out.decode("ascii", "replace"),
        "eax": eax,
        "eip": eip,
        "returned": eip == SENTINEL,
        "instructions": counter["n"],
    }


def main():
    print("StoneAge JSS SaUpdate token-helper emulation probe — R1")
    print("SCOPE|exact-no-import-helper|bounded-x86-emulation|synthetic-inputs|derived-output-only")

    status, final, headers, data = get_bounded(
        replay_url({"timestamp": TIMESTAMP, "original": ORIGINAL}), timeout=20
    )
    sha = hashlib.sha256(data).hexdigest()
    print(f"FETCH|status={status}|bytes={len(data)}|sha256={sha}|final={clean(final)}")
    if sha != KNOWN_SHA256:
        print(f"RESOLUTION|HASH_MISMATCH|expected={KNOWN_SHA256}")
        return

    layout = parse_pe_layout(data)
    pe = pe_sections(data)
    image_base = pe["image_base"]
    off = rva_to_offset(layout, FUNC_RVA)
    if off is None:
        print("RESOLUTION|FUNCTION_RVA_UNMAPPED")
        return
    print(f"FUNCTION|rva=0x{FUNC_RVA:x}|image_base=0x{image_base:x}|external_calls=0")

    successes = 0
    failures = 0
    for case_no, text in enumerate(CASES, 1):
        for field in (1, 2, 3, 4):
            try:
                result = emulate_case(data, layout, image_base, text, field)
            except Exception as exc:
                failures += 1
                print(
                    f"CASE_ERROR|case={case_no}|field={field}|input={clean(text)}|"
                    f"kind={type(exc).__name__}|message={clean(exc)}"
                )
                continue
            if not result["returned"]:
                failures += 1
                print(
                    f"CASE_BOUNDED|case={case_no}|field={field}|input={clean(text)}|"
                    f"eip=0x{result['eip']:x}|eax=0x{result['eax']:x}|"
                    f"instructions={result['instructions']}|returned=0"
                )
                continue
            successes += 1
            print(
                f"CASE|case={case_no}|field={field}|input={clean(text)}|"
                f"output={clean(result['out'])}|eax=0x{result['eax']:x}|"
                f"instructions={result['instructions']}|returned=1"
            )

    print(
        f"RESOLUTION|TOKEN_HELPER_EMULATED|successes={successes}|failures={failures}|"
        f"binary-not-committed"
    )


if __name__ == "__main__":
    main()
