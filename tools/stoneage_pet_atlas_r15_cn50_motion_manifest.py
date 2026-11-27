"""R15: replay accepted CN50 native SPR tables into a delivery-ready metadata manifest.
No original pixel extraction, no pixel availability or runtime claim.
"""
import argparse,collections,gzip,hashlib,json,struct
from pathlib import Path
from tools import stoneage_pet_high_first_100_cn50_full_motion as pre
from tools.stoneage_pet_high_first_57_coverage import ROOT,blob,gzrows
from tools.stoneage_pet_high_first_66_motion_inheritance import sequence_tables
P=ROOT/"research/pets"
PINS={
"PET-HIGH-FIRST-100-CN50-FULL-MOTION-PREFLIGHT-R1.json.gz":"3b2a0b8fd7a3bf1a750138188b789552d69ce16f",
"PET-HIGH-FIRST-100-CI-OBSERVED-R1.json":"889c5daba817edcd6cdaa33e2058b0b1882fd27c",
"PET-HIGH-FIRST-101-CN50-ORIGINAL-RD-R1.json":"f7a50af4bb440008a227d1522d65004dd38a58a6",
"PET-HIGH-FIRST-101-CN50-MOTION-PROJECTION-R1.json":"02b686d84c6c3dc4aba19e4444fd5af2e623a01d"}
def sha(b):return hashlib.sha256(b).hexdigest()
def read(n):
    b=(P/n).read_bytes();assert blob(b)==PINS[n],n
    return json.loads(gzip.decompress(b) if n.endswith(".gz") else b)
def stable(d):return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
def replay(ss):
    out=bytearray()
    for j,a in enumerate(ss):
        assert a["index"]==j and a["count"]==len(a["frames"])
        out.extend(struct.pack("<HHII",a["direction"],a["action"],a["duration"],a["count"]))
        for n,x,y,sound in a["frames"]:
            assert n is None or 0<=n<0xffffffff
            out.extend(struct.pack("<IhhH",0xffffffff if n is None else n,x,y,sound))
    return bytes(out)
def selftest():
    a=dict(index=0,direction=2,action=4,duration=500,count=2,frames=[[7,-1,2,73],[None,0,0,0]])
    expected=bytes.fromhex("02000400f40100000200000007000000ffff02004900ffffffff000000000000")
    assert replay([a])==expected
    assert replay([dict(a,frames=[[7,-1,2,74],[None,0,0,0]])])!=expected
def build():
    pf,observed,residual,final=[read(n) for n in PINS]
    assert pf["summary"]==observed["summary"]
    assert residual["summary"]==final["summary"]
    assert sha((P/next(iter(PINS))).read_bytes())==observed["gzip_sha256"]
    assert len(pf["positions"])==305 and len(pf["groups"])==594
    assert len(pf["bitmap_refs"])==142268 and len(residual["observations"])==90
    for k in ("groups","animations","frames","manifest","adrn"):pre.read(k)
    assert pf["source_manifest"]==pre.obj("manifest")["source"]
    groups={int(i):{k:v[k] for k in ("graphic","sha256","animation_headers")} for i,v in pf["groups"].items()}
    native={}
    for g in gzrows(pre.path("groups")):
        i=int(g["index"])
        if i in groups:
            assert i not in native
            assert (int(g["spr_no"]),g["segment_sha256"],int(g["anim_count"]))==(groups[i]["graphic"],groups[i]["sha256"],groups[i]["animation_headers"])
            native[i]=g
    assert native.keys()==groups.keys()
    sequences=sequence_tables(groups,pre.path("animations"),pre.path("frames"))
    # Per-content expected pixel hash when previously recorded. TW10 aggregate
    # scope has no per-row pixel digest; preserve that evidence distinction.
    expected={};providers=collections.defaultdict(list)
    def add(row,source,ref,digest,grade,size="size"):
        key=(row["rd_sha256"],int(row[size]),int(row["width"]),int(row["height"]))
        if key not in needed:return
        assert len(bytes.fromhex(digest))==32
        v=(grade,digest)
        assert expected.setdefault(key,v)==v,(source,ref,key)
        providers[key].append([source,ref])
    needed={pre.key(b["native_candidates"][0]) for b in pf["bitmap_refs"].values()}
    for k,b in pre.obj("cn_receipt")["cn50_observed_blocks"].items():
        add(b,"CN50_PET11",int(k),b["index_pixels_sha256"],"STRICT","rd_bytes")
    for k,b in pre.obj("tw67")["observations"].items():
        if b["status"]=="DUAL_DECODED_INDEX_PIXELS":add(b,"TW85_PET67",int(k),b["index_pixels_sha256"],"STRICT")
    for k,b in pre.obj("tw68")["observations"].items():
        add(b,"TW85_PET68_BOUNDED",int(k),b["canvas_prefix_sha256"],"BOUNDED")
    for k,b in pre.obj("tw71")["observations"].items():
        if b["grade"]=="STRICT_PIXEL_RECEIPT":add(b,"TW85_PET71",int(k),b["strict"]["index_pixels_sha256"],"STRICT")
        elif b["grade"]=="BOUNDED_CANVAS_RECEIPT":add(b,"TW85_PET71_BOUNDED",int(k),b["boundary"]["canvas_prefix_sha256"],"BOUNDED")
    for k,b in residual["observations"].items():
        assert b["status"]=="DUAL_DECODED_INDEX_PIXELS"
        add(b,"CN50_PET101",int(k),b["index_pixels_sha256"],"STRICT")
    bitmaps={};counts=collections.Counter()
    for n,v in pf["bitmap_refs"].items():
        row,=v["native_candidates"];assert int(n)==row["bitmap"]
        key=pre.key(row)
        g="BOUNDED" if v["grade"]==pre.BOUNDED else "STRICT"
        if v["grade"]==pre.NEED:
            q=residual["observations"][str(row["index"])]
            assert all(q[k]==row[k] for k in row)
        else:assert v["grade"] in (pre.STRICT,pre.BOUNDED)
        pix=expected.get(key)
        assert pix is None or pix[0]==g
        if pix is None:assert v["receipt"]["source"]=="TW10_PET15_STRICT_SCOPE"
        counts[g]+=1;counts["WITH_EXPECTED_PIXEL_SHA" if pix else "AGGREGATE_SCOPE_ONLY"]+=1
        bitmaps[n]=dict(native=row,grade=g,expected_pixel_sha256=pix[1] if pix else None,prior_receipt=v["receipt"],content_receipt_providers=providers[key],actual_png_delivery_verified=False)
    assert counts["STRICT"]==142240 and counts["BOUNDED"]==28
    result={};frames=collections.Counter();seqgrades=collections.Counter()
    for i,g in groups.items():
        ss=[dict(index=j,**a) for j,a in sequences[i].items()]
        raw=replay(ss);n=native[i];assert sha(raw)==g["sha256"] and len(raw)==int(n["end_offset"])-int(n["offset"]),i
        for a in ss:
            grades=[bitmaps[str(f[0])]["grade"] if f[0] is not None else "SENTINEL" for f in a["frames"]]
            frames.update(grades)
            # Mixed sentinel sequences preserve all original positions.
            material=[v for v in grades if v!="SENTINEL"]
            grade="SENTINEL_ONLY" if not material else "BOUNDED_COMPLETE" if "BOUNDED" in material else "STRICT_COMPLETE"
            seqgrades[grade]+=1
            a["receipt_grade"]=grade
        result[str(i)]=dict(g,source_offset=int(n["offset"]),source_end_offset=int(n["end_offset"]),sequences=ss)
    assert dict(seqgrades)==residual["summary"]["sequence_grade"]
    assert frames["STRICT"]==272892 and frames["BOUNDED"]==40
    assert {str(f[0]) for g in result.values() for a in g["sequences"] for f in a["frames"] if f[0] is not None}==set(bitmaps)
    summary=dict(positions=305,groups=len(result),bitmaps=len(bitmaps),bitmap_receipt_grades=dict(counts),sequence_receipt_grades=dict(seqgrades),frame_positions=dict(frames),actual_png_delivery_verified=False,official_closures=0)
    return dict(schema="stoneage.pet.atlas_r15.cn50_native_motion_manifest.r1",source_pins=PINS|{p:h for p,h in pre.PINS.values()},source_manifest=pf["source_manifest"],positions=pf["positions"],groups=result,bitmaps=bitmaps,summary=summary,original_assets_published=False,original_runtime_verified=False,official_identity_verified=False)
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path);p.add_argument("--selftest",action="store_true");a=p.parse_args();selftest()
    if a.selftest:return
    assert a.output
    d=build();b=gzip.compress(stable(d),compresslevel=6,mtime=0);a.output.write_bytes(b)
    print("R15_SUMMARY="+stable(d["summary"]).decode(),flush=True)
    print("R15_GZIP_SHA256="+sha(b),flush=True)
if __name__=="__main__":main()
