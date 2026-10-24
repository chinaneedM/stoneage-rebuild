"""Source-bound Taiwan 1.0 graphic field x86 reference probe. No original client execution."""
import argparse,hashlib,json,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXE="cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
DISC="905ee6ad89b8ca7f55a5c1132eede99a15ee7cb1b868f9b0b398fb0c76cfd159"
WINDOW="0d671aab30706ec4392ceca9a575078079b10e8876ba36d175186e414f097a5b"
R101="b6e0dd1482a675d49d005fb947c1873b0776ba25289c1c03f3ac259fa54ddd92"
R99="21d49800a1191f87a006aaa5af4a6f7975f91bf7"
P2B="23d1a0fb85ac7a83f92cdfb9757618e85e36f9a9"
def need(cond,err):
    if not cond: raise ValueError(err)
def blob(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def context():
    ps=["STONEAGE-TW10-NPC-STATIC-RESOURCE-JOIN-R99.json","STONEAGE-TW10-CN50-DIRECT-STATIC-VISUAL-P2B-R1.json","STONEAGE-TW10-ANIMATION-SELECTOR-R101.json"]
    data=[(ROOT/"research/recovered"/p).read_bytes() for p in ps]
    need(blob(data[0])==R99 and blob(data[1])==P2B and hashlib.sha256(data[2]).hexdigest()==R101,"parent source identity mismatch")
    a,b,c=[json.loads(x) for x in data]
    ids=[r["bitmapno"] for r in a["rows"]]
    need(ids==list(range(5846,5947))==[r["bitmap_id"] for r in b["records"]],"101 actual records mismatched")
    need(all(x["rd_block_sha256"]==y["rd_sha256"] and x["map_number"]==y["original_map_resource_number"] for x,y in zip(a["rows"],b["records"])),"raw resource ancestry mismatch")
    need(all(x["npc_name"] is None and x["original_npc_id"] is None and not x["drawn_npc_role_verified"] for x in a["rows"]),"unverified NPC name was promoted")
    need(all(x["original_npc_name"] is None and x["original_pet_species_id"] is None for x in b["records"]),"unverified entity was promoted")
    cc=c["compiled_contract"]
    need(cc["object_graphic_offset"]==0x124 and cc["selected_bitmap_offset"]==0x80 and cc["animation_lower_inclusive"]==100000 and cc["low_graphic_clears_at_or_below"]==99,"R101 native selector contract drift")
    need(c["boundaries"]["same_build_packet_to_object_graphic_path_proven"] is False and c["boundaries"]["named_npc_to_spr_proven"] is False,"missing upstream promoted")
    return {"r99_blob":R99,"p2b_blob":P2B,"r101_sha256":R101,"static_candidate_count":len(ids),"id_first":ids[0],"id_last":ids[-1],"all_keys_in_verified_static_selector_interval":all(99<x<100000 for x in ids)}
def authenticate(raw):
    need(len(raw)==425984 and hashlib.sha256(raw).hexdigest()==EXE,"untrusted exe")
    need(hashlib.sha256(raw[0x3c380:0x3c5b8]).hexdigest()==WINDOW,"R101 native window changed")
def scan(raw):
    authenticate(raw)
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32,CS_AC_READ,CS_AC_WRITE
    from capstone.x86 import X86_OP_MEM
    import pefile
    pe=pefile.PE(data=raw,fast_load=True)
    need(pe.OPTIONAL_HEADER.ImageBase==0x400000,"source image base changed")
    md=Cs(CS_ARCH_X86,CS_MODE_32);md.detail=True
    hits=[];sections=[]
    for sec in pe.sections:
        if not sec.Characteristics & 0x20000000: continue
        seq=list(md.disasm(sec.get_data(),0x400000+sec.VirtualAddress))
        sections.append({"rva":sec.VirtualAddress,"decoded":len(seq)})
        for i,ins in enumerate(seq):
            for n,op in enumerate(ins.operands):
                if op.type!=X86_OP_MEM or op.mem.disp not in (0x124,0x80): continue
                rva=ins.address-0x400000
                off=pe.get_offset_from_rva(rva)
                hits.append({"rva":rva,"displacement":op.mem.disp,"operand_index":n,
                    "operand_read":bool(op.access & CS_AC_READ),"operand_write":bool(op.access & CS_AC_WRITE),
                    "source_instruction_sha256":hashlib.sha256(raw[off:off+ins.size]).hexdigest(),
                    "instruction":ins.mnemonic+" "+ins.op_str,
                    "nearby":[{"rva":x.address-0x400000,"instruction":x.mnemonic+" "+x.op_str} for x in seq[max(0,i-2):i+3]]})
    need(sum(s["decoded"] for s in sections)>1000,"executable code not decoded")
    need(any(h["displacement"]==0x124 and 0x3c380<=h["rva"]<0x3c5b8 for h in hits),"known original selector anchor absent")
    return {"sections":sections,"candidate_references":hits,"reference_count":len(hits),"candidate_direct_writes_0x124":sum(h["displacement"]==0x124 and h["operand_write"] for h in hits)}
def inspect(raw):
    joined=context(); native=scan(raw)
    return {"schema":"stoneage.tw10.graphic-upstream.p2b.r1","exe_sha256":EXE,"method":"ORIGINAL_X86_DISASSEMBLY_NO_EXECUTION",
            "physical_context":joined,"native":native,"unproven":{
                "displacement_matches_are_proven_object_writes":True,
                "packet_to_object_graphic_field":True,"named_npc_bitmap":True,"named_pet_spr":True,
                "server_master":True,"overall_restoration_percent":None},
            "next":"Disambiguate candidate writes, require same-build identity before promoting pet/NPC."}
def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--exe",type=Path);g.add_argument("--disc",type=Path)
    ap.add_argument("--write",type=Path,required=True);args=ap.parse_args()
    if args.exe: raw=args.exe.read_bytes()
    else:
        need(hashlib.sha256(args.disc.read_bytes()).hexdigest()==DISC,"untrusted disc")
        from tools.stoneage_tw10_technical_probe import find_rows,extract_row
        image,rows,_,_=find_rows(args.disc)
        try:
            row=next(x for x in rows if x["path"]=="StoneAge/sa_3.exe")
            with tempfile.TemporaryDirectory() as t:
                f=Path(t)/"source.bin";extract_row(image,row,f);raw=f.read_bytes()
        finally: image.close()
    d=inspect(raw);args.write.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Source-bound x86 references:",d["native"]["reference_count"],"; named entity identity remains OPEN")
if __name__=="__main__": main()
