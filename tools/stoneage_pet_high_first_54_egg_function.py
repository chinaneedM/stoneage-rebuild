"""Inspect the fixed preserved executable statically; publish derived metadata only."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from tools import stoneage_preserved_item_shop_r44 as sparse
from tools.stoneage_pet_high_first_51_accept import GMSV_SHA

TARGET = "_NPC_EventAddEgg"
ADDRESS = 4896128
NPC_REPORT_SHA = "254dbb336efb194a0c10e4801c0a5ea091839133e5db2c0f7af860c545ae58a1"
NPC_REPORT_BLOB = "0b0e787110e95b17d1593be7534d25c9a9d191ce"

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def static_probe(path):
    symbols={}
    for line in subprocess.check_output(["nm","-P","-n",str(path)],text=True).splitlines():
        parts=line.split()
        if len(parts)>=3 and parts[1] in ("T","t"):
            symbols[parts[0]]=int(parts[2],16)
    assert symbols[TARGET]==ADDRESS
    end=min(a for a in symbols.values() if a>ADDRESS)
    assert 0<end-ADDRESS<65536
    by_addr={}
    for name,a in symbols.items():
        by_addr.setdefault(a,[]).append(name)
    all_dis=subprocess.check_output(["objdump","-d","-w","--no-show-raw-insn",str(path)],text=True,errors="replace")
    ins=[]
    for line in all_dis.splitlines():
        m=re.match(r"^\s*([0-9a-fA-F]+):\s*([a-z][a-z0-9.]*)\s*(.*?)\s*$",line)
        if m:
            ins.append((int(m[1],16),m[2],m[3]))
    body=[x for x in ins if ADDRESS<=x[0]<end]
    assert body and body[0][0]==ADDRESS
    callers=[]
    calls=[]
    immediate_candidates=[]
    selected_ids={1045,1140,1145,2055,2474,2479,101489,101760}
    sorted_addr=sorted(by_addr)
    import bisect
    for addr,mnemonic,operand in ins:
        if mnemonic.startswith(("call","jmp")):
            dest=re.match(r"^([0-9a-fA-F]+)\s*(?:<[^>]+>)?",operand)
            if dest:
                d=int(dest[1],16)
                if d==ADDRESS and not ADDRESS<=addr<end:
                    n=bisect.bisect_right(sorted_addr,addr)-1
                    callers.append({"site":addr,"opcode_class":mnemonic,"containing_symbols":sorted(by_addr[sorted_addr[n]]) if n>=0 else []})
                if ADDRESS<=addr<end and (mnemonic.startswith("call") or not ADDRESS<=d<end):
                    calls.append({"site":addr,"opcode_class":mnemonic,"destination":d,"symbol_candidates":sorted(by_addr.get(d,[]))})
        if ADDRESS<=addr<end:
            for tok in re.findall(r"\$0x([0-9a-fA-F]+)\b",operand):
                val=int(tok,16)
                if val in selected_ids:
                    immediate_candidates.append({"site":addr,"numeric_literal":val})
    # Literal symbol-address references (possibly data, not direct call semantics).
    raw=path.read_bytes()
    address_bytes=ADDRESS.to_bytes(4,"little")
    offsets=[m.start() for m in re.finditer(re.escape(address_bytes),raw)]
    return {"function":TARGET,"start_address":ADDRESS,"next_text_symbol_address":end,"next_text_symbols":sorted(by_addr[end]),
            "body_instruction_count":len(body),"body_mnemonic_counts":dict(Counter(x[1] for x in body)),
            "body_disassembly_sha256":sha("\n".join(f"{a:x}:{m}:{o}" for a,m,o in body).encode()),
            "direct_calls_or_external_jumps":calls,"direct_incoming_calls_or_jumps":callers,
            "literal_address_file_offsets":offsets,"target_id_immediate_candidates":immediate_candidates,
            "function_boundary_is_symbol_interval":True,"indirect_call_resolution_complete":False,
            "hatch_result_verified":False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prior",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    prior=a.prior.read_bytes()
    assert len(prior)==427240 and sha(prior)==NPC_REPORT_SHA
    assert hashlib.sha1(b"blob "+str(len(prior)).encode()+b"\0"+prior).hexdigest()==NPC_REPORT_BLOB
    j=json.loads(prior)
    assert j["exe"]["symbol_candidates"]==[{"address":ADDRESS,"symbol":TARGET}]
    assert len(j["npc_hits"])==765 and not any(x["typed_reference_candidates"] for x in j["npc_hits"])
    assert sum(bool(x["numeric_collisions"]) for x in j["npc_hits"])==33
    assert Counter(t for x in j["npc_hits"] for t in x["cp950_term_labels"])=={"合成":730,"飼料":1,"融合":1}
    receipt={}
    sparse.EXPECTED={"gmsv.exe":(1897867,GMSV_SHA)}
    with tempfile.TemporaryDirectory(prefix="pet54-static-") as d:
        root=Path(d)
        raw=sparse.acquire(root,receipt,"unar")["gmsv.exe"]
        assert sha(raw)==GMSV_SHA
        exe=root/"original.exe"
        exe.write_bytes(raw)
        result=static_probe(exe)
    report={"schema":"stoneage.pet54.egg_function_static_probe.r1","prior_report_git_blob":NPC_REPORT_BLOB,
            "prior_report_sha256":NPC_REPORT_SHA,"prior_job":138707808416,"prior_run":45467953788,
            "prior_artifact":14956965438,"prior_zip_sha256":"bbef41bff6900b8fc3709e7352f6c404fadf0846fd82e9234eb6241defd47b72",
            "executable_sha256":GMSV_SHA,"executable_receipt":receipt,"probe":result,
            "runtime_executed":False,"original_payload_published":False,"official_acquisition_closed":0}
    out=(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()
    a.output.write_bytes(out)
    print("PET54_FUNCTION",json.dumps(result,ensure_ascii=False,separators=(",",":")))
    print("PET54_FUNCTION_REPORT",len(out),sha(out),hashlib.sha1(b"blob "+str(len(out)).encode()+b"\0"+out).hexdigest())

if __name__=="__main__":
    main()
