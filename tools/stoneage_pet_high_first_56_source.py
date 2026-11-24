"""PET56 source replay for five special roles and all remaining 67 target references."""
import argparse, hashlib, json, re, urllib.request
from pathlib import Path
from tools import stoneage_pet_high_first_51_source as prior
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research/pets"
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def comparison(j):
    c=j["later_source"]; data={}; pins={}
    for path,pin in c["pins"].items():
        with urllib.request.urlopen("https://raw.githubusercontent.com/"+c["repo"]+"/"+c["commit"]+"/"+path,timeout=40) as f: raw=f.read()
        assert blob(raw)==pin
        data[path]=raw; pins[path]={"git_blob":pin,"sha256":sha(raw),"bytes":len(raw)}
    def line(path,n):return data[path].splitlines()[n-1]
    inst="gmsv/data/enemy1.txt"; base="gmsv/data/enemybase1.txt"
    for r in j["rows"]:
        i=line(inst,r["later_instance_line"]).split(b","); t=line(base,r["later_template_line"]).split(b",")
        assert (int(i[3]),int(i[4]),list(map(int,i[5:7])),int(i[13]))==(r["instance"],r["template"],r["level"],1)
        assert (int(t[6]),int(t[36]),int(t[25]))==(r["template"],r["graphic"],1)
        assert list(map(int,t[15:19]))==r["elements"]
    z="gmsv/data/npc/eden1/zoo2/"; m="gmsv/data/npc/eden1/zoo1/manager82_01"
    checks=[(z+"event83_19",72,b"GetPet:1733"),(z+"event83_19",60,b"EVENT:ITEM=19714&NOWEV=83&NOWEV=82&ENDEV=81&NOWEV=71"),(z+"event83a.create",191,b"enemy=changeevent|file:eden1/zoo2/event83_19"),(z+"event83_1a",107,b"DelPet:PET>0-758"),(z+"event83_1a",125,b"DelPet:PET>0-854"),(m,13,b"EVENT:ENDEV=81&NOWEV=82&PET=1-905&PET=1-786&PET>0-854"),(m,17,b"DelPet:PET=1-905*1,PET=1-786*1,PET>0-854*1"),(m,19,b"GetPet:1563")]
    for path,n,expected in checks: assert line(path,n).strip()==expected,(path,n)
    i=line(inst,1143).split(b",");assert (int(i[3]),int(i[4]))==(1563,730)
    return pins
def scan(originals,ids,templates):
    # Distinct typed syntaxes, not every numeral on a line.
    direct=re.compile(rb"(?i)(?:^|[|{])\s*(GetPet|AddPet|EnemyNo|EnemyPetNo|VipPet)\s*[:=]\s*(\d+(?:\s*,\s*\d+)*)")
    predicates=re.compile(rb"(?i)\bPET\s*(?:>=|<=|=|>|<)\s*\d+\s*-\s*(\d+)(?!\d)")
    hits=[]; collisions=0
    for path,raw in sorted(originals.items()):
        if not path.startswith("npc/"):continue
        for n,line in enumerate(raw.splitlines(),1):
            if line.lstrip().startswith((b"#",b"//")):continue
            nums={int(v) for v in re.findall(rb"(?<!\d)\d+(?!\d)",line)}
            if not nums&(ids|templates):continue
            collisions+=1
            fields=[]
            for m in direct.finditer(line):
                found=sorted({int(v) for v in re.findall(rb"\d+",m[2])}&ids)
                if found:fields.append({"field":m[1].decode().lower(),"instance_ids":found})
            for m in predicates.finditer(line):
                tid=int(m[1])
                if tid in templates:fields.append({"field":"PET_LEVEL_TEMPLATE_PREDICATE","template_id":tid})
            if fields:hits.append({"path":path,"line":n,"line_sha256":sha(line.strip()),"file_sha256":sha(raw),"fields":fields})
    return {"lexical_collision_lines":collisions,"typed_candidate_lines":hits,"typed_candidate_count":len(hits)}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);a=p.parse_args()
    j=json.loads((P/"PET-HIGH-FIRST-56-SPECIAL-ROLE-PREFLIGHT-R1.json").read_bytes())
    pins=comparison(j)
    data,_,_,_=prior.input_context()
    old=json.loads((P/"PET-HIGH-FIRST-50-ORIGINAL-ACQUISITION-R1.json").read_bytes())
    records=old["projection"]["records"]
    assert len(records)==67
    ids={i["instance_id"] for row in records for i in row["source_pairs"][0]["instances"]}
    templates={row["template_id"] for row in records}
    assert len(templates)==67
    for r in j["rows"]:
        row=next(x for x in records if x["tw75_row_index"]==r["position"])
        assert row["template_id"]==r["template"] and row["graphic"]==r["graphic"]
        assert any(i["instance_id"]==r["instance"] and i["level"]==r["level"] for i in row["source_pairs"][0]["instances"])
    expected=prior.expected_members(data)
    assert len(expected)==2207
    absent=["npc/"+p.removeprefix("gmsv/data/npc/") for p in j["later_source"]["pins"] if "/npc/" in p]
    assert not any(p in expected for p in absent)
    originals,custody=prior.unpack_all(expected)
    assert len(originals)==2207
    found=scan(originals,ids,templates)
    result={"schema":"stoneage.pet56.original_all_residual_typed_reference_probe.r1","comparison_receipts":pins,"original_receipt":custody,"original_later_paths_absent":absent,"target_template_ids":sorted(templates),"target_selected_instance_ids":sorted(ids),"scan":found,"official_acquisition_closed":0,"original_payload_published":False,"runtime_executed":False}
    a.output.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    print("PET56",len(pins),len(templates),len(ids),found["lexical_collision_lines"],found["typed_candidate_count"])
    for hit in found["typed_candidate_lines"]:print("PET56_HIT",json.dumps(hit,ensure_ascii=False,separators=(",",":")))
if __name__=="__main__":main()
