"""PET54: source-only scan of original preserved NPC members and executable.
No original script, dialogue or executable bytes are published or executed.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import tempfile
from tools import stoneage_pet_high_first_51_source as previous
from tools import stoneage_preserved_item_shop_r44 as sparse
from tools.stoneage_pet_high_first_51_accept import GMSV_SHA

INSTANCE_IDS = {2055, 2474, 2479}
TEMPLATE_IDS = {1045, 1140, 1145}
NAMES = ("寵物蛋", "美拉蛋", "美拉", "孵化", "融合", "合成", "飼料")
ASCII = re.compile(rb"egg|hatch|petmix|mixpet|petfusion|fusionpet|breed", re.I)
SYMBOL = re.compile(r"egg|hatch|petmix|mixpet|petfusion|fusionpet|breed|mela|meila", re.I)

def scan(originals, creation):
    hits = []
    for path, raw in sorted(originals.items()):
        if not path.startswith("npc/"):
            continue
        for n, line in enumerate(raw.splitlines(), 1):
            if line.lstrip().startswith((b"#", b"//")):
                continue
            nums = {int(x) for x in previous.NUMBER.findall(line)}
            fields = []
            for field in previous.FIELD.finditer(line):
                key, value = field[1].lower(), field[2].strip()
                if key not in previous.INSTANCE_FIELDS | previous.TEMPLATE_FIELDS:
                    continue
                target = INSTANCE_IDS if key in previous.INSTANCE_FIELDS else TEMPLATE_IDS
                if key == b"vippet":
                    value = value.split(b",", 1)[0].strip()
                if previous.NUMERIC_LIST.fullmatch(value):
                    exact = {int(x) for x in value.split(b",")} & target
                    if exact:
                        fields.append({"field":key.decode(),"ids":sorted(exact)})
            terms = [name for name in NAMES if name.encode("cp950") in line]
            matches = sorted({x.decode("ascii").lower() for x in ASCII.findall(line)})
            if fields or terms or matches or nums & (INSTANCE_IDS | TEMPLATE_IDS):
                hits.append({"path":path,"line":n,"line_sha256":previous.digest(line.strip()),
                             "file_sha256":previous.digest(raw),"created_npc_references":creation[path.removeprefix("npc/")],
                             "typed_reference_candidates":fields,"cp950_term_labels":terms,"ascii_term_labels":matches,
                             "numeric_collisions":sorted(nums & (INSTANCE_IDS | TEMPLATE_IDS))})
    return hits

def executable():
    receipt = {}
    sparse.EXPECTED = {"gmsv.exe":(1897867,GMSV_SHA)}
    with tempfile.TemporaryDirectory(prefix="pet54-exe-") as d:
        root = Path(d)
        raw = sparse.acquire(root,receipt,"unar")["gmsv.exe"]
        p = root / "gmsv-probe.exe"
        p.write_bytes(raw)
        nm = subprocess.check_output(["nm","-P","-n",str(p)],text=True)
        matches=[]
        for line in nm.splitlines():
            fields=line.split()
            if len(fields)>=3 and SYMBOL.search(fields[0]):
                matches.append({"symbol":fields[0],"address":int(fields[2],16)})
        strings = {k:{"ascii":raw.lower().count(k.lower().encode()),"utf16le":raw.lower().count(k.lower().encode("utf-16le"))}
                   for k in ("egg","hatch","petmix","mixpet","petfusion","fusionpet","breed","mela","meila")}
    return {"sha256":GMSV_SHA,"bytes":len(raw),"symbol_candidates":matches,"substring_counts":strings,
            "receipt":receipt,"runtime_executed":False}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    data,_,_,_=previous.input_context()
    originals,custody=previous.unpack_all(previous.expected_members(data))
    assert len(originals)==2207
    creation=Counter(ref[0] for row in data["char01"]["create_rows"] for ref in row[-1])
    hits=scan(originals,creation)
    # Independent plain numeric lexical conservation over the same source bytes.
    expected={(p,n) for p,raw in originals.items() if p.startswith("npc/")
              for n,line in enumerate(raw.splitlines(),1) if not line.lstrip().startswith((b"#",b"//"))
              and {int(x) for x in previous.NUMBER.findall(line)} & (INSTANCE_IDS|TEMPLATE_IDS)}
    assert {(x["path"],x["line"]) for x in hits if x["numeric_collisions"]}==expected
    result={"schema":"stoneage.pet54.original_egg_reference_probe.r1","custody":custody,
            "instance_ids":sorted(INSTANCE_IDS),"template_ids":sorted(TEMPLATE_IDS),
            "npc_hits":hits,"exe":executable(),"official_acquisition_closed":0,
            "hatch_result_verified":False,"original_payload_published":False,"runtime_executed":False}
    raw=(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()
    args.output.write_bytes(raw)
    print("PET54_NPC",len(hits),sum(bool(x["typed_reference_candidates"]) for x in hits),
          sum(bool(x["cp950_term_labels"]) for x in hits))
    print("PET54_EXE",json.dumps({k:v for k,v in result["exe"].items() if k!="receipt"},ensure_ascii=False))
    for x in hits:
        if x["typed_reference_candidates"] or x["cp950_term_labels"] or x["ascii_term_labels"]:
            print("PET54_HIT",json.dumps(x,ensure_ascii=False,separators=(",",":")))
    print("PET54_REPORT",len(raw),previous.digest(raw),previous.pet50.source.r40.git_blob(raw))

if __name__=="__main__":
    main()
