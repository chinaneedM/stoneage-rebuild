"""PET-DETAIL19: authenticate original Taiwan 1.0 PC inventory selection and local action gating.

Private original ZIP mandatory; read-only, never exports copyrighted original bytes.
GNU objdump required for independent instruction replay.
"""
import argparse, hashlib, json, re, struct, subprocess, tempfile, zipfile
from pathlib import Path

ZIP_SHA = "3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24"
EXE_SHA = "cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
WINDOWS = {
    "inventory_selection_and_skill_gate": (0x42a7cd,0x42a8cd,"691ef346108b99f49c09409337506165b5ebfdbc9c997569aa6383513f330922"),
    "selected_item_count_and_UI_transition": (0x42a8fb,0x42a954,"20bf075e876b6f317f2851de478a3c4244c0592fd8f602626e83111f92cfb388"),
    "twenty_item_slot_render_loop": (0x42a988,0x42aa9f,"47431cfabb3a3bc385d3a3c58d785d2d480fef401cfb0ef4fe5809b92f9f0420"),
}
OPCODES = {
    0x42a7d3:"8d04b6",0x42a7d6:"c1e003",0x42a7d9:"2bc6",0x42a7db:"c1e002",
    0x42a7de:"6683b8188a7f0101",0x42a7ec:"83fe05",0x42a7fc:"a802",
    0x42a819:"ba05000000",0x42a81e:"b9f4cd7b01",0x42a823:"833901",
    0x42a828:"83c120",0x42a82c:"81f9d4cf7b01",0x42a836:"c1e205",
    0x42a83f:"c1e605",0x42a8fb:"b8f4cd7b01",0x42a900:"833801",
    0x42a905:"43",0x42a906:"83c020",0x42a909:"3dd4cf7b01",
    0x42a910:"83fb02",0x42a913:"7c73",0x42a91a:"a900000010",
    0x42a921:"3500000010",0x42a926:"b914000000",0x42aa94:"83fd14",
}
ASM = {
    0x42a7cd:"mov esi,DWORD PTR [esp+0x14]",
    0x42a7d3:"lea eax,[esi+esi*4]",0x42a7d6:"shl eax,0x3",
    0x42a7d9:"sub eax,esi",0x42a7db:"shl eax,0x2",
    0x42a7de:"cmp WORD PTR [eax+0x17f8a18],0x1",0x42a7e6:"jne 0x42a8e4",
    0x42a7ec:"cmp esi,0x5",0x42a7f5:"mov ax,WORD PTR [eax+0x17f8ab2]",
    0x42a7fc:"test al,0x2",0x42a819:"mov edx,0x5",
    0x42a81e:"mov ecx,0x17bcdf4",0x42a823:"cmp DWORD PTR [ecx],0x1",
    0x42a828:"add ecx,0x20",0x42a82b:"inc edx",
    0x42a82c:"cmp ecx,0x17bcfd4",0x42a836:"shl edx,0x5",
    0x42a839:"mov edi,DWORD PTR [edx+0x17bcd54]",0x42a83f:"shl esi,0x5",
    0x42a8fb:"mov eax,0x17bcdf4",0x42a900:"cmp DWORD PTR [eax],0x1",
    0x42a905:"inc ebx",0x42a906:"add eax,0x20",
    0x42a909:"cmp eax,0x17bcfd4",0x42a910:"cmp ebx,0x2",
    0x42a913:"jl 0x42a988",0x42a91a:"test eax,0x10000000",
    0x42a91f:"jne 0x42a988",0x42a921:"xor eax,0x10000000",
    0x42a926:"mov ecx,0x14",
    0x42a93a:"rep stos DWORD PTR es:[edi],eax",
    0x42a94f:"call 0x425340",0x42a954:"call 0x43ffe0",
    0x42aa93:"inc ebp",0x42aa94:"cmp ebp,0x14",
    0x42aa9b:"jl 0x42a420",
}

def verify_private_source(path):
    path=Path(path)
    assert path.stat().st_size==372626292
    with path.open("rb") as f:
        assert hashlib.file_digest(f,"sha256").hexdigest()==ZIP_SHA
    with zipfile.ZipFile(path) as z:
        assert len(z.infolist())==379
        assert z.getinfo("source/sa_3.exe").CRC==0x3453fd16
        exe=z.read("source/sa_3.exe")
    assert len(exe)==425984 and hashlib.sha256(exe).hexdigest()==EXE_SHA
    pe=struct.unpack_from("<I",exe,0x3c)[0]
    assert exe[pe:pe+4]==b"PE\x00\x00"
    opt=pe+24
    assert struct.unpack_from("<H",exe,opt)[0]==0x10b
    base=struct.unpack_from("<I",exe,opt+28)[0]
    assert base==0x400000
    count=struct.unpack_from("<H",exe,pe+6)[0]
    table=opt+struct.unpack_from("<H",exe,pe+20)[0]
    sections=[]
    for i in range(count):
        vs,va,rs,raw=struct.unpack_from("<IIII",exe,table+40*i+8)
        sections.append((base+va,min(vs,rs),raw))
    def read(va,n):
        for start,size,off in sections:
            if start<=va and va+n<=start+size:
                return exe[off+va-start:off+va-start+n]
        raise AssertionError("no original PE bytes at "+hex(va))
    for name,(a,b,expected) in WINDOWS.items():
        assert hashlib.sha256(read(a,b-a)).hexdigest()==expected,name
    for va,expected in OPCODES.items():
        assert read(va,len(bytes.fromhex(expected))).hex()==expected,hex(va)
    with tempfile.TemporaryDirectory() as td:
        x=Path(td)/"private_original.exe"
        x.write_bytes(exe)
        output=subprocess.run(["objdump","-d","-Mintel",str(x)],
                              capture_output=True,text=True,check=True).stdout
    decoded={}
    for line in output.splitlines():
        m=re.match(r"^\s*([0-9a-f]+):\s+(?:[0-9a-f]{2}\s+)+\s*\t?(.*)$",line)
        if m:
            decoded[int(m.group(1),16)]=" ".join(m.group(2).strip().lower().split())
    for va,expected in ASM.items():
        assert decoded.get(va)==expected.lower(),hex(va)
    assert (0x17bcfd4-0x17bcdf4)//32==15
    assert (5*8-1)*4==156
    return {
        "original_zip_exe_sha256_verified":True,
        "code_window_SHA_verified":len(WINDOWS),
        "raw_instruction_opcode_verified":len(OPCODES),
        "independent_disassembly_anchors_verified":len(ASM),
        "native_inventory_slot_record_stride_bytes":156,
        "client_local_UI_slot_stride_bytes":32,
        "visible_inventory_slot_count":20,
        "eligible_selection_indices_inclusive":[5,19],
        "eligible_selection_slot_count":15,
        "local_pretransition_selected_entries_minimum":2,
        "server_recipe_material_minimum_proven":False,
        "original_official_server_pet_skill_master":None,
        "actual_server_W_packet":None,
        "original_client_executed":False,
        "original_copyright_binary_published":False,
    }

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("authenticated_private_original_TW1_zip")
    print(json.dumps(verify_private_source(p.parse_args().authenticated_private_original_TW1_zip),
                     ensure_ascii=False,indent=2))
