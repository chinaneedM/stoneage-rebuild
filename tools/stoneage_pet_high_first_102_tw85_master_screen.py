"""PET102: bounded, authenticated TW85 client content screen, never execute originals.

Exact signatures probe limited candidate layouts; no hit does not exclude other
layouts, encryption, computed values or the missing live server master.
"""
import argparse
from collections import defaultdict, Counter
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile
from tools.stoneage_pet_high_first_tw85_native import MANIFEST, EXPECTED_PROGRAMS, parse_pe, sha
from tools.stoneage_pet_high_first_tw85_unpacked import full_aligned_album_grid
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research/pets"
CAT=P/"PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json"
GRID=P/"PET-HIGH-FIRST-TW85-ORIGINAL-PE-ALBUM-GRID-R1.json"
CENSUS=P/"PET-HIGH-FIRST-14-TW85-SPECIAL-RD-AND-MASTER-CENSUS-R1.json"
PINS={MANIFEST:"18a68c9d4275763ef0ed7a347cca940cffe0fee2",CAT:"fec03646d7c7e4e287f9347c306119cc626d6abf",GRID:"7fb8eceba23dea6dc90ebb18e404d6e837210eaf",CENSUS:"75b393d27e11851bf564967b907ce25b4a8d30a2"}
TOKENS=("enemybase","enemy.txt","enemy2.txt","petskill","petabi","initnum","lvuppoint","basevital","basestr","basetgh","basedex","allocpoint","album_","album_50","album_13","savedata.dat","auto.dat","data_1.bin","AISetting.dat","recvdata.txt","recvtime.txt")
SMALL={"AISetting.dat","auto.dat","channel.dat","chathis.dat","chatreg.dat","data_1.bin","mail.dat","savedata.dat","recvdata.txt","recvtime.txt","battletxt_2.txt","soundaddr_3.txt"}
def blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def stable(x):
    return (json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(",",":"))+"\n").encode()
def inputs():
    d={}
    for p,h in PINS.items():
        raw=p.read_bytes(); assert blob(raw)==h,p
        d[p]=json.loads(raw)
    return d
def patterns(rows):
    out=defaultdict(list)
    for r in rows:
        ident,graphic=r["template_id"],r["graphic"]
        base=r["base"]; el=r["elements"]; init=r["initnum"]
        # Probe explicit, limited record layouts, not an assumed client ABI.
        for label,values in (("ID_GRAPHIC_BASE", [ident,graphic,*base]),
                             ("GRAPHIC_ID_BASE",[graphic,ident,*base]),
                             ("GRAPHIC_BASE_ELEMENTS_INIT",[graphic,*base,*el,init]),
                             ("ID_GRAPHIC_BASE_ELEMENTS_INIT",[ident,graphic,*base,*el,init])):
            if not all(isinstance(v,int) and 0<=v<=0xffffffff for v in values): continue
            out[(label+"_U32LE",struct.pack("<"+"I"*len(values),*values))].append(ident)
            if all(v<=65535 for v in values):
                out[(label+"_U16LE",struct.pack("<"+"H"*len(values),*values))].append(ident)
        if all(isinstance(v,int) and 0<=v<=255 for v in [*base,*el,init]) and 0<=graphic<=0xffffffff:
            out[("GRAPHIC_U32_BASE_ELEMENTS_INIT_U8",struct.pack("<I",graphic)+bytes([*base,*el,init]))].append(ident)
    return out
def offsets(raw,needle):
    pos=-1; out=[]
    while True:
        pos=raw.find(needle,pos+1)
        if pos<0:return out
        out.append(pos)
        # A pathological repeated pattern is not a trustworthy table anchor.
        if len(out)>10000:raise ValueError("too many identical hits")
def scan(raw,patterns):
    token_hits=[]
    for token in TOKENS:
        for enc in ("ascii","utf-16le"):
            hits=offsets(raw.lower(),token.lower().encode(enc))
            if hits:token_hits.append(dict(token=token,encoding=enc,offsets=hits))
    hits=[]
    for (layout,needle),ids in patterns.items():
        loc=offsets(raw,needle)
        if loc:
            hits.append(dict(layout=layout,signature_sha256=sha(needle),length=len(needle),template_ids=sorted(ids),offsets=loc))
    # Only offsets separated by a fixed record stride in the same explicit
    # layout, for three distinct single-template hits, merit closer inspection.
    anchors=defaultdict(dict)
    for h in hits:
        if len(h["template_ids"])==1:
            for p in h["offsets"]:
                anchors[h["layout"]][p]=h["template_ids"][0]
    runs=[]
    for layout,by_pos in anchors.items():
        for start,tid in sorted(by_pos.items()):
            for stride in range(12,257,4):
                if start-stride in by_pos:continue
                seq=[tid]; at=start+stride
                while at in by_pos and len(seq)<467:
                    seq.append(by_pos[at]);at+=stride
                if len(seq)>=3 and len(set(seq))>=3:
                    runs.append(dict(layout=layout,start=start,stride=stride,template_ids=seq))
    return dict(token_hits=token_hits,signature_hits=hits,three_distinct_template_stride_candidates=runs)
def selftest():
    r=dict(template_id=7,graphic=100250,base=[20,12,15,25],elements=[80,20,0,0],initnum=10)
    p=patterns([r])
    k=next(k for k in p if k[0]=="ID_GRAPHIC_BASE_U32LE")
    raw=b"xalbum_50\x00"+k[1]+b"END"
    s=scan(raw,p)
    assert any(h["token"]=="album_50" for h in s["token_hits"])
    assert any(h["template_ids"]==[7] and h["layout"]==k[0] for h in s["signature_hits"])
    assert not s["three_distinct_template_stride_candidates"]
    assert not scan(b"xyz",p)["signature_hits"]
    synthetic=[dict(r,template_id=i,graphic=100250+i) for i in (1,2,3)]
    q=patterns(synthetic)
    records=[struct.pack("<6I",v["template_id"],v["graphic"],*v["base"])+b"\xff"*8 for v in synthetic]
    assert any(h["stride"]==32 and h["template_ids"]==[1,2,3] for h in scan(b"".join(records),q)["three_distinct_template_stride_candidates"])
    print("PET102_SELFTEST_OK")
def observe(source):
    d=inputs(); catalog=d[CAT]["pet_flag_1_field_projections"]
    assert len(catalog)==467
    sigs=patterns(catalog)
    expected={Path(v["path"]).name:v for v in d[MANIFEST]["inspection"]["inventory"]["samples"][0]["files"] if Path(v["path"]).name in set(EXPECTED_PROGRAMS)|SMALL}
    assert set(expected)==set(EXPECTED_PROGRAMS)|SMALL
    census={Path(v["path"]).name:v for v in d[CENSUS]["master_census"]["non_map_data_files"]}
    for name in SMALL:assert (expected[name]["sha256"],expected[name]["size"])==(census[name]["sha256"],census[name]["bytes"])
    results={}
    with tempfile.TemporaryDirectory(prefix="pet102-static-") as tmp:
        for name,e in sorted(expected.items()):
            path=source/e["path"]; raw=path.read_bytes()
            assert len(raw)==e["size"] and sha(raw)==e["sha256"],name
            row=dict(path=e["path"],original_bytes=len(raw),original_sha256=sha(raw))
            if name in EXPECTED_PROGRAMS:
                pe=parse_pe(raw); assert pe["status"]=="PE_PARSED_NOT_EXECUTED",name
                row["packed_pe_sections"]=[s["name"] for s in pe["sections"]]
                if any(s["name"].startswith("UPX") for s in pe["sections"]):
                    dest=Path(tmp)/name
                    subprocess.run(["upx","-d","-q","-o",str(dest),str(path)],check=True,timeout=120,capture_output=True)
                    raw=dest.read_bytes(); assert len(raw)<=40*1024*1024
                    row["representation"]="STATIC_UPX_UNPACKED"
                else:row["representation"]="ORIGINAL_UNPACKED_PE"
                if name in d[GRID]["programs"]:
                    g=d[GRID]["programs"][name]
                    assert (len(raw),sha(raw))==(g["unpacked_bytes"],g["unpacked_sha256"]),name
                row["pe_sections"]=parse_pe(raw)["sections"]
                if name in ("Startup.exe","StoneAge2.exe"):
                    g=full_aligned_album_grid(raw)
                    row["known_album_grid_probe"]={k:v for k,v in g.items() if k not in ("named_source_records","unqualified_source_records")}
            else:row["representation"]="ORIGINAL_NONMAP_DATA"
            row.update(scanned_bytes=len(raw),scanned_sha256=sha(raw),**scan(raw,sigs))
            results[name]=row
    summary=dict(files=len(results),bytes_scanned=sum(v["scanned_bytes"] for v in results.values()),signature_layouts=sorted({k[0] for k in sigs}),distinct_signatures=len(sigs),token_hit_files=sum(bool(v["token_hits"]) for v in results.values()),signature_hit_files=sum(bool(v["signature_hits"]) for v in results.values()),stride_candidate_files=sum(bool(v["three_distinct_template_stride_candidates"]) for v in results.values()))
    return dict(schema="stoneage.pet102.tw85.embedded_master_screen.r1",source_pins={str(p.relative_to(ROOT)):h for p,h in PINS.items()},scope="Known limited text/binary signatures only; no server master absence proof, no official identity, no original program execution.",files=results,summary=summary,official_closures=0,original_assets_published=False,original_program_executed=False)
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source-root",type=Path);ap.add_argument("--output",type=Path);ap.add_argument("--self-test",action="store_true")
    a=ap.parse_args();selftest()
    if a.self_test:return
    if not a.source_root or not a.output:ap.error("source-root and output required")
    r=observe(a.source_root);a.output.write_bytes(stable(r));print("PET102_SUMMARY="+json.dumps(r["summary"],sort_keys=True),flush=True)
if __name__=="__main__":main()
