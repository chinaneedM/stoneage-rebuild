"""Bounded original TW1.0 graphic writer data-origin review.

This report is a local syntactic source analysis, not a proof of object
identity or packet provenance. Proprietary original bytes never enter Git.
"""
import argparse
import hashlib
import json
import re
import tempfile
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/"research/recovered/STONEAGE-TW10-GRAPHIC-UPSTREAM-CANDIDATES-P2B-R1.json"
OLD_GIT_BLOB="a9adc6a94e8e062b730e0114df581c7b4ad20d62"
EXE_SHA="cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
DISC_SHA="905ee6ad89b8ca7f55a5c1132eede99a15ee7cb1b868f9b0b398fb0c76cfd159"
EXPECTED=[0x54cb,0x65ab,0x672b,0x7142,0x7466,0x7611,0x856d,0x10b8d,0x10c43,0x10ea5]

def need(ok,msg):
    if not ok: raise ValueError(msg)

def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def parents():
    raw=OLD.read_bytes()
    need(git_blob(raw)==OLD_GIT_BLOB,"upstream research source blob changed")
    d=json.loads(raw)
    need(d["source_run"]["conclusion"]=="success" and d["source_run"]["original_source_reacquired"] is True,"original run not authenticated")
    need(d["original_exe_sha256"]==EXE_SHA,"source exe pin mismatch")
    need(d["boundaries"]["direct_instruction_disp_is_proven_same_object"] is False and d["boundaries"]["named_pet_spr"] is False,"source epistemic boundary changed")
    source=d["facts"]["native_write_candidates"]
    need([r[0] for r in source]==EXPECTED and len({x[0] for x in source})==10,"source writer register inventory drift")
    return {int(rva):sha for rva,sha in source}

def classify(last):
    if last is None: return "NO_LOCAL_ASSIGNMENT"
    mn,ops=last["mnemonic"],last["operands"]
    if mn in ("mov","movzx","movsx","lea"):
        rhs=ops.split(",",1)[1].strip() if "," in ops else ""
        if "ptr [esp" in rhs or "ptr [ebp" in rhs:
            return "STACK_FRAME_MEMORY"
        if "ptr [" in rhs: return "OTHER_MEMORY"
        if rhs.startswith("0x") or rhs.lstrip("-").isdigit(): return "IMMEDIATE"
        return "REGISTER_OR_LEA"
    if mn in ("add","sub","imul","shl","shr","and","or","xor","inc","dec"): return "COMPUTED_OR_BITWISE"
    if mn in ("pop",): return "STACK_POP"
    return "OTHER"

def local_definition(seq, index, reg, max_before=15):
    # Deliberately lexical. Jumps, aliases, calls and basic-block boundaries
    # prevent this from being an actual reaching-definitions proof.
    for dist in range(1,min(max_before,index)+1):
        ins=seq[index-dist]
        parts=ins.op_str.split(",",1)
        if parts and parts[0].strip()==reg and ins.mnemonic in (
            "mov","movzx","movsx","lea","add","sub","imul","xor","or",
            "and","shl","shr","inc","dec","pop"):
            return {"distance_instructions":dist,"rva":ins.address-0x400000,
                    "mnemonic":ins.mnemonic,"operands":ins.op_str,
                    "has_branch_between":any(x.mnemonic.startswith("j") or x.mnemonic in ("ret","call") for x in seq[index-dist+1:index]),
                    "source_class":classify({"mnemonic":ins.mnemonic,"operands":ins.op_str})}
    return None

def audit(raw):
    need(len(raw)==425984 and hashlib.sha256(raw).hexdigest()==EXE_SHA,"not exact authenticated retail EXE")
    pins=parents()
    import pefile
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32
    pe=pefile.PE(data=raw,fast_load=True)
    need(pe.OPTIONAL_HEADER.ImageBase==0x400000,"unexpected image base")
    cs=Cs(CS_ARCH_X86,CS_MODE_32)
    sites={}
    section_counts=[]
    for sec in pe.sections:
        if not sec.Characteristics & 0x20000000: continue
        decoded=list(cs.disasm(sec.get_data(),0x400000+sec.VirtualAddress))
        section_counts.append({"rva":sec.VirtualAddress,"decoded_count":len(decoded)})
        index={i.address-0x400000:k for k,i in enumerate(decoded)}
        for rva,pin in pins.items():
            if rva not in index: continue
            k=index[rva]; ins=decoded[k]
            pos=pe.get_offset_from_rva(rva)
            need(hashlib.sha256(raw[pos:pos+ins.size]).hexdigest()==pin,"original instruction hash not reproduced")
            need(ins.mnemonic=="mov" and "+ 0x124" in ins.op_str,"source no longer contains a direct 0x124 store")
            left,right=[x.strip() for x in ins.op_str.split(",",1)]
            need(left.startswith("dword ptr [") and right in ("eax","ecx","edx"),"not a direct register-to-graphic-field candidate")
            target=re.search(r"\[(e[a-z]{2}) \+ 0x124\]",left)
            need(target is not None,"unexpected register-based target pointer")
            src=local_definition(decoded,k,right)
            ptr=local_definition(decoded,k,target.group(1),40)
            before=decoded[max(0,k-4):k]
            after=decoded[k+1:k+4]
            sites[rva]={
                "rva":rva,"instruction_sha256":pin,"store_register":right,
                "object_base_register":target.group(1),
                "source_lexical_definition":src,
                "object_base_lexical_definition":ptr,
                "context_before":[{"rva":i.address-0x400000,"mnemonic":i.mnemonic,"operands":i.op_str} for i in before],
                "context_after":[{"rva":i.address-0x400000,"mnemonic":i.mnemonic,"operands":i.op_str} for i in after],
                "proves_this_is_original_R101_selector_object":False,
                "proves_protocol_or_named_entity":False}
    need(sorted(sites)==EXPECTED,"bounded writer site missing or additional branch decoded")
    classes=Counter(s["source_lexical_definition"]["source_class"] if s["source_lexical_definition"] else "NO_LOCAL_ASSIGNMENT" for s in sites.values())
    boundary={
        "lexical_previous_register_assignment_is_control_flow_proof":False,
        "same_base_register_means_same_object_across_functions":False,
        "all_writes_verified_to_reach_R101_object_0x124":False,
        "network_packet_to_graphic_id_authenticated":False,
        "original_server_identity_table_available":False,
        "named_npc_or_pet_species_confirmed":False,
        "gameplay_runtime_executed":False,
        "overall_restoration_percent":None,
    }
    return {
        "schema":"stoneage.tw10.p2b.original-writer-classification.r1",
        "authentic_exe_sha256":EXE_SHA,
        "parent_report_git_blob":OLD_GIT_BLOB,
        "method":"SOURCE_BYTE_PINNED_STATIC_LEXICAL_NEIGHBORHOOD",
        "decoded_executable_sections":section_counts,
        "writer_sites":[sites[i] for i in EXPECTED],
        "local_source_class_counts":dict(sorted(classes.items())),
        "source_class_count_is_not_number_of_entities":True,
        "boundaries":boundary,
        "next":"Stop expanding generic write-site audit without authenticated same-build object/packet/name linkage; redirect to independent official named visual or server master evidence."
    }

def main():
    ap=argparse.ArgumentParser()
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--exe",type=Path)
    g.add_argument("--disc",type=Path)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    if a.exe: original=a.exe.read_bytes()
    else:
        need(hashlib.sha256(a.disc.read_bytes()).hexdigest()==DISC_SHA,"wrong original disc SHA")
        from tools.stoneage_tw10_technical_probe import find_rows,extract_row
        im,rows,_,_=find_rows(a.disc)
        try:
            entry=next(r for r in rows if r["path"]=="StoneAge/sa_3.exe")
            with tempfile.TemporaryDirectory() as d:
                dst=Path(d)/"native.exe"
                extract_row(im,entry,dst)
                original=dst.read_bytes()
        finally: im.close()
    report=audit(original)
    a.out.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("P2B WRITER CLASSES",json.dumps(report["local_source_class_counts"],sort_keys=True),"NAME RELATION OPEN")

if __name__=="__main__":main()
