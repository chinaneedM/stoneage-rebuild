#!/usr/bin/env python3
"""Bounded emulation of the JSS SaUpdate manifest-line helper at RVA 0x1F80.

The hash-pinned archived SaUpdate executable is fetched transiently. The report
retains only synthetic input/output behavior and bounded execution metadata; no
executable bytes or raw disassembly are retained.
"""

from __future__ import annotations

import hashlib
import struct

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256, TIMESTAMP, parse_pe_layout
from tools.stoneage_jss_saupdate_token_emulation_probe import c_string, map_image
from tools.stoneage_tw10_technical_probe import pe_sections

FUNC_RVA = 0x1F80
MAX_INSNS = 4000
STACK_BASE = 0x11000000
STACK_SIZE = 0x10000
SCRATCH_BASE = 0x21000000
SCRATCH_SIZE = 0x20000
SENTINEL = 0x31000000

CASES = (
    ("colon-five", "EXE:12:file.exe:1234:tail", 0x3A, (1,2,3,4,5,6)),
    ("colon-empty", "A::C", 0x3A, (1,2,3,4)),
    ("colon-spaces", "MESSAGE:hello world:with spaces", 0x3A, (1,2,3,4)),
    ("lf-three", "line1\nline2\nline3", 0x0A, (1,2,3,4)),
    ("crlf-three", "line1\r\nline2\r\nline3", 0x0A, (1,2,3)),
)


def clean(value, limit=700):
    text = str(value if value is not None else "")
    text = text.replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def emulate_case(data, layout, image_base, text, delimiter, field_index, max_len=0x400):
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    map_image(uc, data, layout, image_base)
    uc.mem_map(STACK_BASE, STACK_SIZE)
    uc.mem_map(SCRATCH_BASE, SCRATCH_SIZE)
    uc.mem_map(SENTINEL, 0x1000)

    dest = SCRATCH_BASE + 0x100
    src = SCRATCH_BASE + 0x4000
    source = text.encode("ascii") + b"\0"
    uc.mem_write(src, source)
    uc.mem_write(dest, b"\xCC" * 0x2000)

    esp = STACK_BASE + STACK_SIZE - 0x200
    frame = struct.pack(
        "<IIIIII",
        SENTINEL,
        src,
        int(delimiter) & 0xFF,
        int(field_index),
        int(max_len),
        dest,
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
    eax = uc.reg_read(UC_X86_REG_EAX) & 0xFFFFFFFF
    out = c_string(uc.mem_read(dest, 0x1000)).decode("ascii", "replace")
    return {
        "output": out,
        "eax": eax,
        "eip": eip,
        "returned": eip == SENTINEL,
        "instructions": counter["n"],
    }


def main():
    print("StoneAge JSS SaUpdate manifest-line helper emulation — R1")
    print("SCOPE|rva-0x1f80|synthetic-line-tokenization|bounded-x86-emulation|derived-output-only")

    status, final, headers, data = get_bounded(
        replay_url({"timestamp": TIMESTAMP, "original": ORIGINAL}), timeout=20
    )
    sha = hashlib.sha256(data).hexdigest()
    print(f"FETCH|status={status}|bytes={len(data)}|sha256={sha}|final={clean(final)}")
    if sha != KNOWN_SHA256:
        print(f"RESOLUTION|HASH_MISMATCH|expected={KNOWN_SHA256}")
        return

    layout = parse_pe_layout(data)
    image_base = pe_sections(data)["image_base"]
    print(f"FUNCTION|rva=0x{FUNC_RVA:x}|image_base=0x{image_base:x}|external_calls=0")

    successes = 0
    failures = 0
    for label, text, delimiter, indexes in CASES:
        for field_index in indexes:
            try:
                result = emulate_case(
                    data, layout, image_base, text, delimiter, field_index
                )
            except Exception as exc:
                failures += 1
                print(
                    f"CASE_ERROR|label={label}|delimiter=0x{delimiter:02x}|"
                    f"index={field_index}|input={clean(text)}|"
                    f"kind={type(exc).__name__}|message={clean(exc)}"
                )
                continue
            if not result["returned"]:
                failures += 1
                print(
                    f"CASE_BOUNDED|label={label}|delimiter=0x{delimiter:02x}|"
                    f"index={field_index}|input={clean(text)}|"
                    f"eip=0x{result['eip']:x}|instructions={result['instructions']}|returned=0"
                )
                continue
            successes += 1
            print(
                f"CASE|label={label}|delimiter=0x{delimiter:02x}|index={field_index}|"
                f"input={clean(text)}|output={clean(result['output'])}|"
                f"eax=0x{result['eax']:x}|instructions={result['instructions']}|returned=1"
            )

    # Test whether the fourth argument constrains output length. This is safe
    # because the destination scratch allocation is intentionally oversized.
    for max_len in (1,4,8):
        result = emulate_case(
            data, layout, image_base, "ABCDEFGHIJ:tail", 0x3A, 1, max_len=max_len
        )
        print(
            f"MAXLEN_CASE|max_len={max_len}|input=ABCDEFGHIJ:tail|"
            f"output={clean(result['output'])}|returned={int(result['returned'])}"
        )

    print(
        f"RESOLUTION|MANIFEST_LINE_HELPER_EMULATED|successes={successes}|"
        f"failures={failures}|binary-not-committed"
    )


if __name__ == "__main__":
    main()
