"""PET-DETAIL18 original TW1 v1.0 PC 200/201 to original UI text, private-only replay."""
import argparse,hashlib,json,re,struct,subprocess,tempfile,zipfile
from pathlib import Path
ZIP_SHA="3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24"
EXE_SHA="cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
WINDOWS={
"ability_gate_control":(0x42a7f5,0x42a8cd,"947a172be0d4085a85ba2831dc28a9955c26178b625e4e986e1fc36b1fb492fe"),
"label_select_draw":(0x42aa22,0x42aa93,"92d65024ddc2cbe5596fa4cf3326d77043727df0900b83d15c3de13b2f0240fa"),
"display_string_queue":(0x40ced0,0x40cf5e,"4ab5393abbea7bbb0cedf354efed59fe74c085efd27654d9b7bb0b3cb43dacbd")}
OPCODES={
0x42a856:"a804",0x42a858:"7429",0x42a85a:"68c9000000",0x42a85f:"e86ca8ffff",
0x42a867:"83f801",0x42a876:"c70602000000",0x42a883:"68c8000000",
0x42a888:"e843a8ffff",0x42a890:"83f801",0x42a8b4:"752e",0x42a8c0:"c70601000000",
0x42a98c:"bf01000000",0x42aa27:"8b8854cd7b01",0x42aa3a:"3bcf",
0x42aa4c:"68acc44500",0x42aa59:"e87224feff",0x42aa63:"83f902",
0x42aa76:"68a4c44500",0x42aa83:"e84824feff",0x40cf39:"f2ae",
0x40cf48:"f3a5",0x40cf52:"f3a4"}
ASM={
0x42a856:"test al,0x4",0x42a858:"je 0x42a883",
0x42a85a:"push 0xc9",0x42a85f:"call 0x4250d0",
0x42a876:"mov DWORD PTR [esi],0x2",0x42a883:"push 0xc8",
0x42a888:"call 0x4250d0",0x42a8c0:"mov DWORD PTR [esi],0x1",
0x42aa4c:"push 0x45c4ac",0x42aa59:"call 0x40ced0",
0x42aa76:"push 0x45c4a4",0x42aa83:"call 0x40ced0"}
LABELS=(
(200,"合成",1,0x45c4ac,0x42aa4c,"9b6f1ebf7f2efbd6e6595da8ca2b340e8fccf86db55ae55570d7f5c1672eb7fb"),
(201,"料理",2,0x45c4a4,0x42aa76,"8f4829124d8a77cf79a0c91ff1133a99c1720e89807ce5fe508f7745665cb91b"))

def verify_private(path):
 p=Path(path)
 assert p.stat().st_size==372626292
 with p.open("rb") as f:
  assert hashlib.file_digest(f,"sha256").hexdigest()==ZIP_SHA
 with zipfile.ZipFile(p) as z:
  assert len(z.infolist())==379
  assert z.getinfo("source/sa_3.exe").CRC==0x3453fd16
  b=z.read("source/sa_3.exe")
 assert len(b)==425984 and hashlib.sha256(b).hexdigest()==EXE_SHA
 pe=struct.unpack_from("<I",b,0x3c)[0]
 assert b[pe:pe+4]==b"PE\x00\x00"
 opt=pe+24;imagebase=struct.unpack_from("<I",b,opt+28)[0]
 assert imagebase==0x400000
 count=struct.unpack_from("<H",b,pe+6)[0]
 ptr=opt+struct.unpack_from("<H",b,pe+20)[0]
 sections=[]
 for i in range(count):
  sz,va,rsize,raw=struct.unpack_from("<IIII",b,ptr+40*i+8)
  sections.append((imagebase+va,min(sz,rsize),raw))
 def source(va,n):
  for start,sz,raw in sections:
   if start<=va and va+n<=start+sz:return b[raw+va-start:raw+va-start+n]
  raise AssertionError(hex(va))
 for name,(a,z,h) in WINDOWS.items():
  assert hashlib.sha256(source(a,z-a)).hexdigest()==h,name
 for va,op in OPCODES.items():
  assert source(va,len(bytes.fromhex(op))).hex()==op,hex(va)
 for sid,label,state,va,xref,sha in LABELS:
  s=label.encode("cp950")+b"\x00"*4
  assert source(va,len(s))==s and hashlib.sha256(s).hexdigest()==sha
  address=struct.pack("<I",va)
  assert b.count(address)==1 and source(xref+1,4)==address
 with tempfile.TemporaryDirectory() as temp:
  exe=Path(temp)/"original_private.exe";exe.write_bytes(b)
  asm=subprocess.run(["objdump","-d","-Mintel",str(exe)],capture_output=True,text=True,check=True).stdout
 decoded={}
 for line in asm.splitlines():
  m=re.match(r"^\s*([0-9a-f]+):\s+(?:[0-9a-f]{2}\s+)+\s*\t?(.*)$",line)
  if m:decoded[int(m.group(1),16)]=" ".join(m.group(2).strip().lower().split())
 for va,expected in ASM.items():assert decoded.get(va)==expected.lower(),hex(va)
 return {"private_source_sha256_verified":True,"code_windows_verified":3,
         "raw_opcode_checks":len(OPCODES),"independent_disassembler_anchor_checks":len(ASM),
         "native_UI_operation_labels":{str(i):{"label":s,"state":st} for i,s,st,_,_,_ in LABELS},
         "original_official_server_skill_names":None,"original_born_pet_skills":None,
         "client_executed":False,"private_commercial_bytes_published":False}
if __name__=="__main__":
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("authenticated_private_original_TW1_zip")
 print(json.dumps(verify_private(p.parse_args().authenticated_private_original_TW1_zip),ensure_ascii=False,indent=2))
