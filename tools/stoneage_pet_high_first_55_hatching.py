"""PET55: replay pinned comparison bytes and bounded original executable symbol probe."""
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from tools import stoneage_preserved_item_shop_r44 as sparse
from tools.stoneage_pet_high_first_51_accept import GMSV_SHA

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/pets/PET-HIGH-FIRST-55-LATER-FUSION-HATCHING-R1.json"
TARGETS=("NPC_EventAddEgg","NPC_DoPetFusion","PETFUSION_AddEgg","PETFUSION_SetNewEgg",
         "ITEM_useFusionEditBase","PET_CheckIncubate","EVOLUTION_createPetFromEnemyIndex",
         "CHAR_ResetPoolPetEgg","CHAR_ResetPetEggFusionTime","PET_getEvolutionAns")
def gitblob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def verify_comparison(report):
    c=report["comparison"]; prefix="https://raw.githubusercontent.com/"+c["repository"]+"/"+c["commit"]+"/"
    data={}; receipts={}
    for path,pin in c["git_blobs"].items():
        with urllib.request.urlopen(prefix+path,timeout=45) as response:
            raw=response.read()
        assert gitblob(raw)==pin,(path,gitblob(raw))
        data[path]=raw
        receipts[path]={"git_blob":pin,"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
    def has(path,*tokens):
        for t in tokens:
            assert t.encode() in data[path],(path,t)
    npc="gmsv/src/npc/npc_petfusion.c"; enemy="gmsv/src/char/enemy.c"; item="gmsv/src/item/item_event.c"
    has(npc,"PETFUSION_getIndexForChar","NPC_getFusionTableForBase","PETFUSION_DelPet","ADDEGGID","PETFUSION_AddEgg","PETFUSION_SetNewEgg")
    has(enemy,"ENEMY_ID ) == petID","ENEMY_TEMPNO ) == petID","CHAR_FUSIONINDEX, PetCode","CHAR_FUSIONRAISE, 40",
        "CHAR_FUSIONBEIT, 1","CHAR_FUSIONRAISE, 0","anhour*2.5","anhour*2","& 0xFF) - 6","& 0xFF) - 5",
        "EVOLUTION_createPetFromEnemyIndex","PET_getEvolutionAns","CHAR_LOOPINTERVAL] = 60000")
    has(item,"CHAR_FUSIONRAISE, --raise","CHAR_FUSIONTIMELIMIT, nowTime","EVOLUTION_createPetFromEnemyIndex",
        "CHAR_FUSIONRAISE) <= 0","time_l + anhour","deltime*60")
    has("gmsv/src/include/pet.h","60*60")
    has("gmsv/src/char/pet.c","PET_CheckIncubateLoop","CHAR_LOOPINTERVAL] = 60000")
    has("gmsv/src/function.c","PET_CheckIncubateLoop","PET_CheckIncubate","ITEM_useFusionEditBase")
    has("gmsv/src/char/char.c","CHAR_ResetPoolPetEgg","CHAR_ResetPetEggFusionTime","CHAR_FUSIONTIMELIMIT, nowTime")
    assert b"FUSIONRAISE" not in data["gmsv/src/char/pet_event.c"]
    flags=data["gmsv/src/include/version.h"].splitlines()
    for flag in c["feature_flags"]["defined"]:
        assert any(re.match(rb"^\s*#define\s+"+flag.encode()+rb"\b",line) for line in flags),flag
    for flag in c["feature_flags"]["commented"]:
        assert any(re.match(rb"^\s*//\s*#define\s+"+flag.encode()+rb"\b",line) for line in flags),flag
        assert not any(re.match(rb"^\s*#define\s+"+flag.encode()+rb"\b",line) for line in flags),flag
    args=data["gmsv/data/npc/sa50/petfusion/petfusion.arg"]
    assert [int(x) for x in re.findall(rb"(?m)^ADDEGGID:(\d+)",args)]==[2055,1045]
    create=data["gmsv/data/npc/sa50/petfusion/petfusion.create"]
    assert sorted(set(map(int,re.findall(rb"floorid=(\d+)",create))))==[2000,4000,7000]
    inst=data["gmsv/data/enemy1.txt"].splitlines()
    templates=data["gmsv/data/enemybase1.txt"].splitlines()
    for row in c["config"]["rows"]:
        i=inst[row["instance_line"]-1].split(b",")
        t=templates[row["template_line"]-1].split(b",")
        assert (int(i[3]),int(i[4]),int(t[6]),int(t[36]))==(row["instance"],row["template"],row["template"],row["graphic"])
    return receipts
def original_probe():
    receipt={}
    sparse.EXPECTED={"gmsv.exe":(1897867,GMSV_SHA)}
    with tempfile.TemporaryDirectory(prefix="pet55-") as d:
        root=Path(d); raw=sparse.acquire(root,receipt,"unar")["gmsv.exe"]
        assert hashlib.sha256(raw).hexdigest()==GMSV_SHA
        exe=root/"original.exe"; exe.write_bytes(raw)
        symbols={}
        for line in subprocess.check_output(["nm","-P","-n",str(exe)],text=True).splitlines():
            p=line.split()
            if len(p)>=3 and p[1] in ("T","t"):
                symbols[p[0]]=int(p[2],16)
        assert symbols["_NPC_EventAddEgg"]==4896128
        by_addr={}
        for name,a in symbols.items(): by_addr.setdefault(a,[]).append(name)
        addresses=sorted(by_addr)
        ins=[]
        for line in subprocess.check_output(["objdump","-d","-w","--no-show-raw-insn",str(exe)],text=True,errors="replace").splitlines():
            m=re.match(r"^\s*([0-9a-fA-F]+):\s*([a-z][a-z0-9.]*)\s*(.*?)\s*$",line)
            if m: ins.append((int(m[1],16),m[2],m[3]))
        results=[]
        for target in TARGETS:
            matches=[n for n in symbols if n.lstrip("_")==target]
            entry={"target":target,"exact_symbols":matches,"status":"NOT_FOUND_IN_TEXT_SYMBOL_TABLE" if not matches else "STATIC_SYMBOL_INTERVAL","intervals":[]}
            for name in matches:
                start=symbols[name]; end=next(a for a in addresses if a>start)
                body=[x for x in ins if start<=x[0]<end]
                assert body and body[0][0]==start and end-start<65536
                calls=[]; literals=[]
                for i,(site,op,arg) in enumerate(body):
                    if not op.startswith("call"): continue
                    m=re.match(r"^([0-9a-fA-F]+)\s*(?:<[^>]+>)?",arg)
                    if not m: continue
                    dest=int(m[1],16); names=sorted(by_addr.get(dest,[]))
                    calls.append({"site":site,"destination":dest,"symbols":names})
                    if any(re.search(r"CHAR_(get|set)(Work)?Int",n) for n in names):
                        # Candidate preceding immediates only; not proof of ABI or field index.
                        literals.append({"call_site":site,"preceding_immediate_candidates":[{"site":s,"values":[int(v,16) for v in re.findall(r"\$0x([0-9a-fA-F]+)\b",a)]} for s,o,a in body[max(0,i-8):i] if re.search(r"\$0x[0-9a-fA-F]+",a)]})
                entry["intervals"].append({"symbol":name,"start":start,"end":end,"instruction_count":len(body),
                    "body_sha256":hashlib.sha256("\n".join(f"{s:x}:{o}:{a}" for s,o,a in body).encode()).hexdigest(),
                    "direct_calls":calls,"field_index_candidate_windows":literals})
            results.append(entry)
        return {"executable_sha256":GMSV_SHA,"receipt":receipt,"symbols":results,
                "field_offsets_verified":False,"indirect_control_flow_complete":False,"runtime_executed":False}
def main():
    p=argparse.ArgumentParser(); p.add_argument("--output",type=Path,required=True); a=p.parse_args()
    report=json.loads(REPORT.read_text())
    assert report["strict_gap_count"]==67 and report["official_acquisition_closed"]==0
    assert not report["actual_hatching_verified"] and not report["original"]["same_deployment_bridge"]
    prior=(ROOT/report["original"]["prior_report"]).read_bytes()
    assert gitblob(prior)==report["original"]["prior_blob"]
    result={"schema":"stoneage.pet55.source_replay.r1","comparison_receipts":verify_comparison(report),"original":original_probe(),
            "official_acquisition_closed":0,"actual_hatching_verified":False,"original_assets_published":False}
    a.output.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    print("PET55",len(result["comparison_receipts"]),[(x["target"],x["status"]) for x in result["original"]["symbols"]])
if __name__=="__main__":
    main()
