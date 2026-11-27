"""R25: bounded CN85 runtime-projection residual source extraction.
No game executable execution; encrypted private artifacts only.
"""
import argparse,collections,hashlib,mmap,shutil,struct,tempfile
from pathlib import Path
from tools import stoneage_pet_atlas_r13_cn85_original as r13
from tools import stoneage_pet_atlas_r18_cn85_native_residual as r18
from tools.stoneage_pet_atlas_r13_cn85_original import (
    transfer,native,secure,parse_adrn_record,gray_png,sha,load,stable,group_sequences,pixel,PINS
)
from tools import stoneage_pet_atlas_r24_cn85_compatible_residual as r24
COVERAGE_SHA="d8b81a24033f7bf48a0329ae91f8de912e7334127b346c257cfe6c88b7801235"
GROUPS=(102,1655,1656,1657,1666,1671,1672,1705)
TARGET_RANGES=((8590,8592),(126235,126238),(232475,232476),(283639,283640),(500059,500451),(500453,500817),(500825,500860))
TARGETS={i for a,b in TARGET_RANGES for i in range(a,b+1)}
def plan():
    d,p,rows,faces,old,exact,ordinal,slot,groups=r13.plan()
    d18,p18,rr,old18,groups18=r18.plan()
    d24,p24,old24,groups24=r24.plan()
    assert d==d18==d24 and p==p18==p24 and groups==groups18==groups24
    prior=set(old)|set(old18)|set(old24)
    assert len(prior)==1504 and len(GROUPS)==8 and not (set(GROUPS)&prior)
    assert len(TARGETS)==805 and 284436 not in TARGETS and 284476 not in TARGETS
    assert all(0<=i<len(groups) and int(groups[i]["index"])==i for i in GROUPS)
    return d,p,list(GROUPS),groups
def export(out,pub):
    d,p,selected,groups=plan()
    key=pub.read_bytes();assert hashlib.sha1(b"blob "+str(len(key)).encode()+b"\0"+key).hexdigest()==r18.KEY
    exact=ordinal=slot=set()
    cap=load(transfer.old.p.R117)["results"][0]
    a=load(transfer.old.prev.REPORT)["results"][0]
    assert cap["cdx"]==a["cdx"]==d["capture"]
    out.mkdir(parents=True,exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="cn85-r25-") as tmp:
        root=Path(tmp);archive=root/"StoneAge.zip"
        t=transfer.transfer(cap,archive)
        print("R25_TRANSFER="+stable(t),flush=True)
        assert t["complete"] and t["cdx_digest_matches"] and t["sha256"]==d["transfer"]["sha256"]
        assert transfer.old.inspect_zip(archive,root,cap,a)==d["zip_members"]
        rr=transfer.old.extract(root,a)
        known={x["name"]:x for x in d["selected_resources"]}
        assert len(rr)==6 and all(x["result"]=="EXTRACTED_SIZE_VERIFIED" and x["sha256"]==known[x["name"]]["sha256"] for x in rr)
        real,receipt=native.extract_real(root,a);assert receipt==p["real_receipt"]
        paths={x.name:x for x in (root/"selected").rglob("*") if x.is_file()}
        body=paths["spr_155.bin"].read_bytes();index=paths["spradrn_155.bin"].read_bytes()
        motions=group_sequences(body,index,groups,selected,exact,ordinal,slot)
        raw_wanted={f[0] for g in motions.values() for s in g["sequences"] for f in s["frames"] if f[0] is not None}
        wanted=raw_wanted|TARGETS
        adrn=paths["adrn_185.bin"].read_bytes();assert len(adrn)==36719200
        by=collections.defaultdict(list)
        for i in range(len(adrn)//80):
            n=struct.unpack_from("<I",adrn,i*80)[0]
            if n in wanted:by[n].append(i)
        files={n:dict(bytes=known[n]["bytes"],sha256=known[n]["sha256"]) for n in ("adrn_185.bin","spr_155.bin","spradrn_155.bin")}
        files["real_185.bin"]={k:receipt[k] for k in ("bytes","sha256")}
        def make(i,mm,folder):
            raw=adrn[i*80:(i+1)*80];x=parse_adrn_record(raw);off,size,w,h=x["adder"],x["size"],x["width"],x["height"]
            row=dict(index=i,bitmap=x["bitmapno"],alias=x["map_number"],width=w,height=h,size=size,offset=off,xoff=x["xoff"],yoff=x["yoff"],adrn_sha256=sha(raw),rd_sha256=None,path=None,png_sha256=None,indexed_pixel_sha256=None)
            if not 0<=off<=len(mm) or not 16<=size<=len(mm)-off:return dict(row,grade="SOURCE_EXTENT_UNRESOLVED")
            block=mm[off:off+size];row["rd_sha256"]=sha(block)
            grade,px,diag=pixel(block,w,h);row.update(grade=grade,decode_evidence=diag)
            if px is not None:
                n=f"bitmap-{i}.png";png=gray_png(px,w,h);(folder/n).write_bytes(png)
                row.update(path=n,png_sha256=sha(png),indexed_pixel_sha256=sha(px))
            return row
        def emit(batch,folder,report):
            (folder/"receipt.json").write_text(stable(report),encoding="utf-8")
            e=secure.seal(folder,pub,out/f"batch-{batch}")
            print("R25_BATCH="+stable(dict(batch=batch,summary=report["summary"],cipher_sha256=e["cipher_sha256"])),flush=True)
            shutil.rmtree(folder)
        common=dict(schema="stoneage.pet.atlas_r25.cn85_runtime_projection_residual.r1",source_files=files,source_archive_sha256=t["sha256"],source_pins=PINS|{r18.REF:r18.PIN},r24_projection_coverage_sha256=COVERAGE_SHA,static_runtime_projection_only=True,official_identity_verified=False,native_selector_verified=False,original_palette_runtime_verified=False,original_assets_published=False)
        with real.open("rb") as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as mm:
            for b,start in enumerate(range(0,len(selected),50),1):
                ids=selected[start:start+50];folder=root/f"motion-{b}";folder.mkdir()
                nums=raw_wanted|TARGETS
                links={str(n):by.get(n,[]) for n in sorted(nums)}
                indexes=sorted({i for rr in links.values() for i in rr});images={str(i):make(i,mm,folder) for i in indexes}
                report=dict(common,batch=b,groups=ids,motion_groups={str(i):motions[i] for i in ids},runtime_target_ids=sorted(TARGETS),raw_frame_ids=sorted(raw_wanted),runtime_target_missing=[n for n in sorted(TARGETS) if not links[str(n)]],bitmap_candidates=links,bitmaps=images,summary=dict(groups=len(ids),bitmaps=len(images),bitmap_numbers=len(nums),missing_numbers=sum(not v for v in links.values()),ambiguous_numbers=sum(len(v)>1 for v in links.values()),grades=dict(collections.Counter(q["grade"] for q in images.values())),sequences=sum(len(motions[i]["sequences"]) for i in ids),frame_positions=sum(len(s["frames"]) for i in ids for s in motions[i]["sequences"])))
                emit(b,folder,report)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--plan-only",action="store_true")
    ap.add_argument("--output",type=Path)
    ap.add_argument("--public-key",type=Path)
    args=ap.parse_args();r13.selftest()
    _,_,ids,groups=plan()
    print("R25_PLAN="+stable(dict(groups=ids,count=len(ids),batches=1,prior_groups=1504,target_ids=sorted(TARGETS),target_count=len(TARGETS),source_receipt=PINS["PET-HIGH-FIRST-122-CN85-COMPLETE-TRANSFER-R1.json"],r24_projection_coverage_sha256=COVERAGE_SHA)),flush=True)
    if not args.plan_only:
        assert args.output and args.public_key
        export(args.output,args.public_key)
if __name__=="__main__":main()
