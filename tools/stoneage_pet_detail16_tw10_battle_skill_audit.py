"""PET-DETAIL16: original classic PC TW1 native skill-ID and battle dispatch source replay.

Pass a lawfully held authenticated private retail ZIP. This script reads it
locally and reports only checks/counts; it never exports executable bytes.
Do not use later community server game files as replacements.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import tempfile
import zipfile

ZIP_SHA = "3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24"
EXE_SHA = "cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
WINDOWS = {
    "battle_target_dispatch": (0x403390, 0x4033e5, "5a13a34ac6cc492f072dbc3a7fd8e151beb4cb00ba22fcd8edf507682be450c8"),
    "battle_W_field_menu": (0x40380f, 0x403a31, "34187bbdb739e689cd864310a889d7e106ed49fc48a8b948fe5d5ab9a2590683"),
    "battle_target_secondary": (0x403e5e, 0x403e95, "2e0dc5dcb4585f8bdad4d9a37f04300fbb52594f27a8ec17b0f9dc81583b315e"),
    "cross_pet_skill_id_lookup": (0x4250d0, 0x425129, "563a05c8fcef9739fab0deb3d7d00dcf06ffc1353f2b8d49ab6ce806d9f4bbb4"),
    "battle_skill_name_read": (0x4047cb, 0x404804, "437e906d535f584cf6304624773b6b5d9d06e7c5ece64f4dd2edc9a8c514a14d"),
    "caller_skill_id_200_201": (0x42a850, 0x42a895, "84e60a7500a56b406cd2fadc3acec8d20dbbb2c8ecf918f39f0a4dd49d894827"),
    "status_field_context": (0x427ce0, 0x427d30, "e9916bb0da6ed5d791f93a852baa9de15f09b14bd9a4176ca3bb32026a8eb3cc"),
}
ASM = {
    0x4033cd: "movsx eax,WORD PTR [ecx*2+0x17f7aee]",
    0x4033de: "jmp DWORD PTR [eax*4+0x4036d4]",
    0x403815: "mov edx,DWORD PTR [ecx*4+0x17f7698]",
    0x4038a5: "mov edi,DWORD PTR [ecx*4+0x17f7698]",
    0x4038d3: "cmp WORD PTR [edx+0x17f7ae8],0x1",
    0x4039c1: "cmp WORD PTR [edx*2+0x17f7aec],0x2",
    0x4039e2: "mov edx,DWORD PTR [ecx*4+0x17f7698]",
    0x4039f9: "lea eax,[eax*2+0x17f7aec]",
    0x403a06: "cmp WORD PTR [eax],0x2",
    0x403a0d: "add eax,0x6a",
    0x403b91: "cmp WORD PTR [ecx*2+0x17f7aec],0x2",
    0x403e80: "movsx ecx,WORD PTR [esi*2+0x17f7aee]",
    0x4047f0: "lea edx,[ecx*2+0x17f7af0]",
    0x4250d8: "mov edi,0x17f7698",
    0x4250dd: "mov ebx,0x17f7aea",
    0x4250e7: "cmp WORD PTR [edi+0x28],ax",
    0x4250ed: "mov esi,DWORD PTR [edi]",
    0x4250f7: "cmp WORD PTR [ecx-0x2],ax",
    0x4250fd: "movsx eax,WORD PTR [ecx]",
    0x425109: "inc edx",
    0x42510a: "add ecx,0x6a",
    0x42510d: "cmp edx,esi",
    0x425111: "add ebx,0x2e6",
    0x425117: "add edi,0x6c",
    0x42511a: "cmp ebx,0x17f8968",
    0x425120: "jl 0x4250e7",
    0x425122: "xor eax,eax",
    0x42a85a: "push 0xc9",
    0x42a85f: "call 0x4250d0",
    0x42a883: "push 0xc8",
    0x42a888: "call 0x4250d0",
    0x427cf2: "cmp WORD PTR [ecx+0x17f7aec],0x1",
}
OPERANDS = {
    0x4033cd: (4, 0x17f7aee),
    0x403815: (3, 0x17f7698),
    0x4039c1: (4, 0x17f7aec),
    0x4039e2: (3, 0x17f7698),
    0x4039f9: (3, 0x17f7aec),
    0x403b91: (4, 0x17f7aec),
    0x403e80: (4, 0x17f7aee),
    0x4047f0: (3, 0x17f7af0),
    0x4250d8: (1, 0x17f7698),
    0x4250dd: (1, 0x17f7aea),
    0x42511a: (2, 0x17f8968),
    0x42a85a: (1, 201),
    0x42a883: (1, 200),
    0x427cf2: (3, 0x17f7aec),
}

def file_sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(4 << 20), b""):
            h.update(b)
    return h.hexdigest()

def norm(s):
    return re.sub(r"\s+", " ", s.strip().lower())

def verify_private_retail_zip(path):
    path = Path(path)
    assert path.stat().st_size == 372626292, "retail archive size mismatch"
    assert file_sha(path) == ZIP_SHA, "retail archive digest mismatch"
    with zipfile.ZipFile(path) as z:
        assert len(z.infolist()) == 379
        b = z.read("source/sa_3.exe")
        assert z.getinfo("source/sa_3.exe").CRC == 0x3453fd16
    assert len(b) == 425984 and hashlib.sha256(b).hexdigest() == EXE_SHA
    pe = struct.unpack_from("<I", b, 0x3c)[0]
    assert b[pe:pe+4] == b"PE\0\0"
    opt = pe + 24
    assert struct.unpack_from("<H", b, opt)[0] == 0x10b
    image_base = struct.unpack_from("<I", b, opt+28)[0]
    assert image_base == 0x400000
    n = struct.unpack_from("<H", b, pe+6)[0]
    sect_at = opt + struct.unpack_from("<H", b, pe+20)[0]
    sections = []
    for i in range(n):
        at = sect_at + 40*i
        vsize, virt, rsize, raw = struct.unpack_from("<IIII", b, at+8)
        sections.append((image_base+virt, vsize, rsize, raw))
    def source_offset(va):
        for v, vsize, rsize, raw in sections:
            if v <= va < v + min(vsize, rsize):
                return raw + va-v
        raise AssertionError("native VA not in raw PE section")
    for name, (start, stop, h) in WINDOWS.items():
        source = b[source_offset(start):source_offset(stop-1)+1]
        assert hashlib.sha256(source).hexdigest() == h, name
    for va, (skip, operand) in OPERANDS.items():
        actual = struct.unpack_from("<I", b, source_offset(va)+skip)[0]
        assert actual == operand, hex(va)
    with tempfile.TemporaryDirectory() as td:
        exe = Path(td) / "authenticated_local_only.exe"
        exe.write_bytes(b)
        asm = subprocess.run(
            ["objdump", "-d", "-Mintel", str(exe)],
            capture_output=True, text=True, check=True).stdout
    lines = {}
    pattern = re.compile(r"^\s*([0-9a-f]+):\s+(?:[0-9a-f]{2}\s+)+\s*\t?(.+)$")
    for line in asm.splitlines():
        m = pattern.match(line)
        if m:
            lines[int(m.group(1),16)] = m.group(2)
    for va, expected in ASM.items():
        assert norm(lines.get(va, "")) == norm(expected), hex(va)
    assert 5 * 742 == 3710 and 0x17f7aea + 3710 == 0x17f8968
    return {
        "private_original_exe_sha_checked": True,
        "independent_windows": len(WINDOWS),
        "independent_native_disassembler_anchors": len(ASM),
        "independent_original_byte_operands": len(OPERANDS),
        "native_ID_references": [200, 201],
        "original_client_game_executed": False,
        "original_official_pet_birth_skills_confirmed": 0,
    }

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("authenticated_private_retail_zip")
    args = p.parse_args()
    print(json.dumps(verify_private_retail_zip(
        args.authenticated_private_retail_zip), ensure_ascii=False, indent=2))
