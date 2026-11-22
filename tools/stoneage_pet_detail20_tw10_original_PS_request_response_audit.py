"""PET-DETAIL20 source-bound TW1 native PS request, queue, socket send and response replay.

Read-only validation against the lawfully possessed original Taiwanese PC retail ZIP.
Does not open sockets, run the original client, publish game bytes or emulate server.
Requires GNU objdump and Python 3.11+.
"""
import argparse
import hashlib
import json
import re
import struct
import subprocess
import tempfile
import zipfile
from pathlib import Path

ZIP_BYTES = 372626292
ZIP_SHA = "3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24"
EXE_BYTES = 425984
EXE_SHA = "cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
WINDOWS = {
    "selected_material_slot_ascii_formatter": (0x424571, 0x4245e5, "85c1e69d5f639fdeab01b9e568799400a471a76e4cb9398ce7f1ef95c9a9ca62"),
    "pet_skill_request_caller": (0x4245e5, 0x424627, "45767c3aecf5678c18537126258d919bb41acc367f3a455bc57016267fe8e6de"),
    "PS_request_serializer": (0x419090, 0x419141, "d908a1b6f8061bfe3a2d7377b422db58e3708998fa87de65c8d07d91131b6c0d"),
    "packet_frame_finalize": (0x41b3f0, 0x41b47a, "fb554968556c36df7142f9ae185f674e7d9276cee7fc08b4910b8fc54c1d9f90"),
    "send_callback_registration": (0x42ebd2, 0x42ebeb, "ad8f0a998c1b8ee6e782445fd9c26d46e8a24cc1c93589a59a6110af24752321"),
    "outbound_buffer_append": (0x42eca0, 0x42eceb, "5d2043b8df3090d02c92291a34d86a128500b14e504a29009eacb7901239edae"),
    "socket_send_invocation": (0x42eb1f, 0x42eb45, "6e6b4afea3acf22d2bfea1715b5f5f633a85e56bcd7eaada67c0c09b2f9d4c94"),
    "PS_inbound_dispatch": (0x41a50c, 0x41a5a7, "65e9fa49cfbfcd4fb67a0d19b1e0e3587e8d4ae807a080d2ad1b8f6c81b8c975"),
    "PS_response_handler": (0x433030, 0x43306d, "33909af3ba14e9bee92a38b821ddf2680d237b1c0f6d1c43aee12b1831eb545a"),
}
OPCODES = {
    0x42458e: "68a4c34500", 0x424594: "e8af410200",
    0x4245d5: "83c320", 0x4245d9: "81fbd4cf7b01",
    0x424607: "50", 0x424612: "e8794affff", 0x42461a: "8935745a7e01",
    0x419095: "6834984500", 0x41909b: "e8e0230000",
    0x419118: "e8d31f0000", 0x419138: "e8b3220000",
    0x41b46e: "ff15e0984500", 0x42ebde: "68a0ec4200",
    0x42ebe3: "e828c0feff", 0x41ac14: "c705e0984500d0b34100",
    0x41ac22: "a3e0984500", 0x42ecaf: "8b1520de7e01",
    0x42eccd: "8dba341e7f01", 0x42eb2d: "68341e7f01",
    0x42eb33: "e82e990100", 0x448466: "ff2554224500",
    0x41a50c: "be34984500", 0x41a592: "e8998a0100",
    0x43303c: "c705745a7e0100000000", 0x433046: "751e",
    0x43304c: "68c4c94500", 0x43305e: "e82d60fdff",
}
ASM = {
    0x42457e:"cmp DWORD PTR [ebx],esi",
    0x424580:"jl 0x4245d1",
    0x42458e:"push 0x45c3a4",
    0x424594:"call 0x448748",
    0x4245cc:"mov esi,0x1",
    0x4245d1:"mov edx,DWORD PTR [esp+0x18]",
    0x4245d5:"add ebx,0x20",
    0x4245d9:"cmp ebx,0x17bcfd4",
    0x424603:"lea eax,[esp+0x1c]",
    0x424607:"push eax",
    0x42460d:"push 0x0",
    0x424612:"call 0x419090",
    0x42461a:"mov DWORD PTR ds:0x17e5a74,esi",
    0x419090:"mov eax,ds:0x4598e8",
    0x419095:"push 0x459834",
    0x41909b:"call 0x41b480",
    0x4190ad:"push ecx",
    0x4190af:"call 0x41b0b0",
    0x4190f5:"call 0x41b0b0",
    0x419118:"call 0x41b0f0",
    0x419127:"call 0x41b060",
    0x419138:"call 0x41b3f0",
    0x41b3f0:"mov al,ds:0x179b258",
    0x41b43d:"call 0x41b4e0",
    0x41b46e:"call DWORD PTR ds:0x4598e0",
    0x42ebde:"push 0x42eca0",
    0x42ebe3:"call 0x41ac10",
    0x41ac14:"mov DWORD PTR ds:0x4598e0,0x41b3d0",
    0x41ac22:"mov ds:0x4598e0,eax",
    0x42eca0:"mov eax,ds:0x17ede1c",
    0x42ecaf:"mov edx,DWORD PTR ds:0x17ede20",
    0x42eccd:"lea edi,[edx+0x17f1e34]",
    0x42ece1:"mov ds:0x17ede20,eax",
    0x42eb2d:"push 0x17f1e34",
    0x42eb33:"call 0x448466",
    0x448466:"jmp DWORD PTR ds:0x452254",
    0x41a50c:"mov esi,0x459834",
    0x41a544:"jne 0x41a5a7",
    0x41a54f:"call 0x41b120",
    0x41a55f:"push eax",
    0x41a570:"push edx",
    0x41a581:"call 0x41b120",
    0x41a592:"call 0x433030",
    0x433030:"mov eax,DWORD PTR [esp+0x8]",
    0x43303c:"mov DWORD PTR ds:0x17e5a74,0x0",
    0x433046:"jne 0x433066",
    0x43304c:"push 0x45c9c4",
    0x43305e:"call 0x409090",
    0x433066:"add esp,0x100",
}
LITERALS = {
    "protocol_tag_PS":(0x459834,b"PS\x00"),
    "material_slot_formatter":(0x45c3a4,b"%d|\x00"),
    "client_zero_response_message":(0x45c9c4,"失敗！".encode("cp950")+b"\x00"),
}

def verify_original_retail_zip(path):
    path = Path(path)
    assert path.stat().st_size == ZIP_BYTES
    with path.open("rb") as stream:
        assert hashlib.file_digest(stream,"sha256").hexdigest() == ZIP_SHA
    with zipfile.ZipFile(path) as archive:
        assert len(archive.infolist()) == 379
        member = archive.getinfo("source/sa_3.exe")
        assert member.CRC == 0x3453fd16
        exe = archive.read(member)
    assert len(exe) == EXE_BYTES and hashlib.sha256(exe).hexdigest() == EXE_SHA

    pe = struct.unpack_from("<I",exe,0x3c)[0]
    assert exe[pe:pe+4] == b"PE\x00\x00"
    opt = pe+24
    assert struct.unpack_from("<H",exe,opt)[0] == 0x10b
    base = struct.unpack_from("<I",exe,opt+28)[0]
    assert base == 0x400000
    count = struct.unpack_from("<H",exe,pe+6)[0]
    table = opt+struct.unpack_from("<H",exe,pe+20)[0]
    sections = []
    for i in range(count):
        vsize,rva,rsize,file_offset = struct.unpack_from("<IIII",exe,table+40*i+8)
        sections.append((base+rva,min(vsize,rsize),file_offset))

    def read_va(va,count):
        for begin,size,offset in sections:
            if begin <= va and va+count <= begin+size:
                return exe[offset+va-begin:offset+va-begin+count]
        raise AssertionError("PE raw section missing " + hex(va))

    for key,(start,end,sha) in WINDOWS.items():
        assert hashlib.sha256(read_va(start,end-start)).hexdigest() == sha,key
    for va,op in OPCODES.items():
        assert read_va(va,len(bytes.fromhex(op))).hex() == op,hex(va)
    for label,(va,raw) in LITERALS.items():
        assert read_va(va,len(raw)) == raw,label

    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)/"private_tw10.exe"
        temp.write_bytes(exe)
        disasm = subprocess.run(
            ["objdump","-d","-Mintel",str(temp)],
            capture_output=True,text=True,check=True).stdout
        import_table = subprocess.run(
            ["objdump","-p",str(temp)],
            capture_output=True,text=True,check=True).stdout
    addresses = {}
    for line in disasm.splitlines():
        found=re.match(r"^\s*([0-9a-f]+):\s+(?:[0-9a-f]{2}\s+)+\s*\t?(.*)$",line)
        if found:
            addresses[int(found.group(1),16)] = " ".join(found.group(2).strip().lower().split())
    for va,expected in ASM.items():
        assert addresses.get(va) == expected.lower(),hex(va)

    # Original WSOCK32 import is by ordinal. Match the actual imported thunk
    # at 0x452254, not a guess based on external server packet definitions.
    assert "DLL Name: WSOCK32.dll" in import_table
    assert re.search(r"(?m)^\s*00052254\s+19\s+<none>",import_table)
    assert read_va(0x448466,6).hex()=="ff2554224500"
    return {
       "authenticated_private_original_sha256":EXE_SHA,
       "original_code_sha_windows_checked":len(WINDOWS),
       "original_raw_opcode_checks":len(OPCODES),
       "original_objdump_instruction_anchors":len(ASM),
       "original_CP950_and_ascii_literals":len(LITERALS),
       "PS_selected_index_format":"%d|",
       "PS_request_serializer_va":"0x419090",
       "PS_response_handler_va":"0x433030",
       "original_WSOCK32_send_import_ordinal":19,
       "original_WSOCK32_send_thunk_va":"0x448466",
       "zero_response_client_message":"失敗！",
       "actual_online_server_request_observed":False,
       "actual_original_server_response_observed":False,
       "original_client_runtime_executed":False,
       "original_commercial_bytes_published":False,
    }

if __name__=="__main__":
    args=argparse.ArgumentParser(description=__doc__)
    args.add_argument("lawfully_held_private_TW10_retail_zip")
    value=args.parse_args()
    print(json.dumps(verify_original_retail_zip(value.lawfully_held_private_TW10_retail_zip),
                     ensure_ascii=False,indent=2))
