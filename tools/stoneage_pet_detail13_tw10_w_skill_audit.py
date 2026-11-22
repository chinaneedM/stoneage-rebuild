"""PET-DETAIL13: privately replay the original TW1 W skill memory evidence.

Usage: python tools/stoneage_pet_detail13_tw10_w_skill_audit.py /path/to/P3H.zip
Source binaries remain private. This never executes the game or emits opcodes.
"""
import hashlib
import json
import re
import struct
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/"research/pets/PET-DETAIL-EVIDENCE13-TW10-ORIGINAL-W-SKILL-UI-BRIDGE-R1.json"

def sha_stream(path):
    h=hashlib.sha256()
    with open(path,"rb") as stream:
        for block in iter(lambda: stream.read(4*1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def normalize(s):
    return re.sub(r"\s+"," ",s.strip().lower())

def audit(archive,receipt_path=RECEIPT):
    d=json.loads(Path(receipt_path).read_text(encoding="utf-8"))
    source=d["source"]
    archive=Path(archive)
    if archive.stat().st_size!=source["private_archive_bytes"] or sha_stream(archive)!=source["private_archive_sha256"]:
        raise ValueError("Private original archive mismatch")
    with zipfile.ZipFile(archive) as z:
        if len(z.infolist())!=source["zip_members"]:
            raise ValueError("Original archive member count mismatch")
        info=z.getinfo(source["original_member"])
        if format(info.CRC,"08x")!=source["original_member_crc32"]:
            raise ValueError("Original PE member CRC mismatch")
        raw=z.read(info)
    if len(raw)!=source["original_member_size"] or hashlib.sha256(raw).hexdigest()!=source["original_member_sha256"]:
        raise ValueError("Original PE SHA mismatch")
    for w in d["private_replay"]["source_windows"]:
        a,b=w["start"],w["end"]
        if a<0 or b>len(raw) or a>=b or hashlib.sha256(raw[a:b]).hexdigest()!=w["sha256"]:
            raise ValueError("Original window SHA mismatch: "+w["id"])
    pe=struct.unpack_from("<I",raw,0x3c)[0]
    if raw[:2]!=b"MZ" or raw[pe:pe+4]!=b"PE\x00\x00":
        raise ValueError("Not original PE image")
    opt=pe+24
    if struct.unpack_from("<H",raw,opt)[0]!=0x10b:
        raise ValueError("Unexpected PE32 optional header")
    base=struct.unpack_from("<I",raw,opt+28)[0]
    sect_at=opt+struct.unpack_from("<H",raw,pe+20)[0]
    sections=[]
    for n in range(struct.unpack_from("<H",raw,pe+6)[0]):
        p=sect_at+40*n
        name=raw[p:p+8].split(b"\0")[0].decode("ascii")
        virt_size,virt_addr,file_size,file_at=struct.unpack_from("<IIII",raw,p+8)
        sections.append((name,base+virt_addr,virt_size,file_at,file_size))
    if not any(name==".text" and v==0x401000 and off==0x1000 for name,v,_,off,_ in sections):
        raise ValueError("Original .text section mapping mismatch")
    def file_offset(va):
        for _,v,length,fo,sz in sections:
            if v<=va<v+min(length,sz): return fo+va-v
        raise ValueError("Address outside original PE section")
    for spec in d["private_replay"]["independent_u32_displacement_checks"]:
        va=int(spec["va"],16)
        actual=struct.unpack_from("<I",raw,file_offset(va)+spec["within_instruction"])[0]
        if actual!=int(spec["expected_u32"],16):
            raise ValueError("Native source displacement mismatch at "+hex(va))
    with tempfile.TemporaryDirectory() as tmp:
        exe=Path(tmp)/"source-verified.exe"
        exe.write_bytes(raw)
        dis=subprocess.run(["objdump","-d","-Mintel",str(exe)],check=True,capture_output=True,text=True).stdout
    instructions={}
    for line in dis.splitlines():
        match=re.match(r"^\s*([0-9a-f]+):\s+(?:[0-9a-f]{2}\s+)+\s*\t?(.+)$",line)
        if match: instructions[int(match.group(1),16)]=normalize(match.group(2))
    for spec in d["private_replay"]["disassembler_instruction_checks"]:
        va=int(spec["va"],16)
        if instructions.get(va)!=spec["normalized_instruction"]:
            raise ValueError("Independent PE disassembly mismatch at "+hex(va))
    w=d["W_original_native"]
    if w["skill_rows_per_pet"]*w["skill_row_bytes"]!=w["per_pet_bytes"]:
        raise ValueError("Original W layout contract invalid")
    return {
      "source_exe_sha_verified":True,
      "source_windows_verified":len(d["private_replay"]["source_windows"]),
      "independent_disassembler_checks":len(d["private_replay"]["disassembler_instruction_checks"]),
      "independent_original_byte_displacements":len(d["private_replay"]["independent_u32_displacement_checks"]),
      "skill_rows_per_pet":w["skill_rows_per_pet"],
      "skill_bytes_per_row":w["skill_row_bytes"],
      "official_pet_birth_skills_proven":False,
      "native_executable_executed":False
    }

if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python stoneage_pet_detail13_tw10_w_skill_audit.py /private/P3H.zip")
    print(json.dumps(audit(sys.argv[1]),ensure_ascii=False,indent=2))
