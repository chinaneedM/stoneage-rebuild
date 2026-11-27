"""R24: authenticated CN85 extraction for exactly the R23 residual 501 groups.

Reuses R13 extent/pixel/receipt pipeline; no new PE custody or execution.
Private encrypted outputs only; original palette, runtime motion selection and
official identity remain unverified.
"""
import argparse,collections,hashlib,mmap,struct,tempfile,shutil,time
from pathlib import Path
from tools import stoneage_pet_atlas_r13_cn85_original as r13
from tools import stoneage_pet_atlas_r18_cn85_native_residual as r18
from tools.stoneage_pet_atlas_r13_cn85_original import transfer,native,secure,parse_adrn_record,gray_png,sha,load,stable,group_sequences,pixel,PINS

CROSSWALK_SHA="6ed4f391bfbd92ccf0dbf0f7c77f5ee6d2231ce09b12b1d0cbb4d268ee256cf9"
SELECTION_SHA="f0b69eb6a5d3d9078cb7672bd744ba098fa0a2ab4ca2819017a13cdaf0c936dd"
KEY_PAIRS_SHA="e90411d58c8e231037d3e47f720908ba6d6e5a7b4a1cf22f8c90a9dd1c26b8c4"
RANGES=((685,686),(723,725),(730,742),(773,834),(1041,1042),(1079,1081),(1086,1095),(1185,1186),(1216,1216),(1253,1253),(1258,1272),(1291,1304),(1306,1306),(1336,1388),(1419,1420),(1424,1424),(1427,1430),(1432,1654),(1658,1665),(1667,1670),(1673,1681),(1685,1692),(1695,1698),(1701,1704),(1706,1709),(1712,1716),(1721,1722),(1732,1772))

def plan():
    d,p,rows,faces,old13,exact,ordinal,slot,groups=r13.plan()
    _,_,_,old18,_=r18.plan()
    old=set(old13)|set(old18)
    assert len(old13)==740 and len(old18)==263 and len(old)==1003
    ids=[i for a,b in RANGES for i in range(a,b+1)]
    assert len(ids)==len(set(ids))==501 and ids==sorted(ids)
    assert not old.intersection(ids)
    assert all(0<=i<len(groups) and int(groups[i]["index"])==i for i in ids)
    assert sha(stable(ids).encode())==SELECTION_SHA
    assert sha(stable([[i,int(groups[i]["spr_no"])] for i in ids]).encode())==KEY_PAIRS_SHA
    assert len(set(ids)-{1291,1292,1293,1294})==497
    return d,p,ids,groups

def bounded_transfer(cap,dst,*,fetch=None,total=None,chunk=None,limit=2400):
    """Retry zero/partial transport failures; never accept unauthenticated bytes."""
    fetch=fetch or transfer.old.fetch_range
    total=total or transfer.old.p.TOTAL
    chunk=chunk or transfer.old.CHUNK
    started=time.monotonic()
    deadline=started+limit
    attempts=[]
    dst.touch()
    def read(start,end):
        assert dst.stat().st_size==start
        result=fetch(cap["replay_url"],dst,start,end,deadline)
        attempts.append(result)
        exact=(result["result"]=="EXACT_BYTES" and
               result["bytes"]==end-start+1 and dst.stat().st_size==end+1)
        if not exact:
            with dst.open("r+b") as f:f.truncate(start)
        return exact
    # A second full request is useful only if the first returned no bytes.
    complete=read(0,total-1)
    if not complete and attempts[-1]["bytes"]==0 and time.monotonic()<deadline:
        complete=read(0,total-1)
    if not complete:
        # Use only exact, validated, contiguous range responses, never splice
        # a partly read range into the next attempt. At most two per range.
        for start in range(0,total,chunk):
            end=min(start+chunk,total)-1
            success=False
            for _ in range(2):
                if time.monotonic()>=deadline:break
                if read(start,end):
                    success=True
                    break
            if not success:break
        complete=dst.stat().st_size==total
    info=transfer.old.hash_file(dst)
    return dict(attempts=attempts,elapsed_seconds=round(time.monotonic()-started,1),
                **info,complete=complete and info["bytes"]==total,
                cdx_digest_matches=info["sha1_base32"]==cap["cdx"]["digest"])

def transfer_selftest():
    import base64
    payload=b"abcdefghij"
    cap={"replay_url":"synthetic","cdx":{"digest":base64.b32encode(hashlib.sha1(payload).digest()).decode()}}
    calls=[]
    def fake(url,dst,start,end,deadline):
        calls.append((start,end))
        # Both full attempts time out at zero; first partial range is rolled back.
        data=b"" if end==9 and start==0 else (payload[start:start+1] if len(calls)==3 else payload[start:end+1])
        with dst.open("ab") as f:f.write(data)
        return dict(start=start,end=end,bytes=len(data),result="EXACT_BYTES" if len(data)==end-start+1 else "ACCESS_ERROR")
    with tempfile.TemporaryDirectory() as t:
        dst=Path(t)/"synthetic"
        r=bounded_transfer(cap,dst,fetch=fake,total=10,chunk=4)
        assert r["complete"] and r["cdx_digest_matches"] and dst.read_bytes()==payload
        assert calls==[(0,9),(0,9),(0,3),(0,3),(4,7),(8,9)]
        def fail(url,dst,start,end,deadline):
            with dst.open("ab") as f:f.write(b"x")
            return dict(start=start,end=end,bytes=1,result="ACCESS_ERROR")
        r=bounded_transfer(cap,Path(t)/"failed",fetch=fail,total=10,chunk=4)
        assert not r["complete"] and not r["cdx_digest_matches"] and r["bytes"]==0
        assert len(r["attempts"])==3
    print("R24_TRANSPORT_SELFTEST_PASS",flush=True)

def export(out,pub):
    d,p,selected,groups=plan()
    raw=pub.read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==r18.KEY
    cap=load(transfer.old.p.R117)["results"][0]
    a=load(transfer.old.prev.REPORT)["results"][0]
    assert cap["cdx"]==a["cdx"]==d["capture"]
    out.mkdir(parents=True,exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="cn85-r24-") as tmp:
        root=Path(tmp);archive=root/"StoneAge.zip"
        t=bounded_transfer(cap,archive)
        print("R24_TRANSFER="+stable(t),flush=True)
        assert t["complete"] and t["cdx_digest_matches"] and t["sha256"]==d["transfer"]["sha256"]
        assert transfer.old.inspect_zip(archive,root,cap,a)==d["zip_members"]
        rr=transfer.old.extract(root,a)
        known={x["name"]:x for x in d["selected_resources"]}
        assert len(rr)==6 and all(x["result"]=="EXTRACTED_SIZE_VERIFIED" and x["sha256"]==known[x["name"]]["sha256"] for x in rr)
        real,receipt=native.extract_real(root,a);assert receipt==p["real_receipt"]
        paths={x.name:x for x in (root/"selected").rglob("*") if x.is_file()}
        body=paths["spr_155.bin"].read_bytes();index=paths["spradrn_155.bin"].read_bytes()
        motions=group_sequences(body,index,groups,selected,set(),set(),set())
        wanted={f[0] for g in motions.values() for s in g["sequences"] for f in s["frames"] if f[0] is not None}
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
            print("R24_BATCH="+stable(dict(batch=batch,summary=report["summary"],cipher_sha256=e["cipher_sha256"])),flush=True)
            shutil.rmtree(folder)
        common=dict(schema="stoneage.pet.atlas_r24.cn85_remaining.r1",source_files=files,source_archive_sha256=t["sha256"],source_pins=PINS|{r18.REF:r18.PIN},crosswalk_sha256=CROSSWALK_SHA,selection_sha256=SELECTION_SHA,official_identity_verified=False,native_selector_verified=False,original_palette_runtime_verified=False,original_assets_published=False)
        with real.open("rb") as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as mm:
            for b,start in enumerate(range(0,len(selected),51),1):
                ids=selected[start:start+51];folder=root/f"motion-{b}";folder.mkdir()
                nums={f[0] for i in ids for s in motions[i]["sequences"] for f in s["frames"] if f[0] is not None}
                links={str(n):by.get(n,[]) for n in sorted(nums)}
                indexes=sorted({i for rr in links.values() for i in rr});images={str(i):make(i,mm,folder) for i in indexes}
                report=dict(common,batch=b,groups=ids,motion_groups={str(i):motions[i] for i in ids},bitmap_candidates=links,bitmaps=images,summary=dict(groups=len(ids),bitmaps=len(images),bitmap_numbers=len(nums),missing_numbers=sum(not v for v in links.values()),ambiguous_numbers=sum(len(v)>1 for v in links.values()),grades=dict(collections.Counter(q["grade"] for q in images.values())),sequences=sum(len(motions[i]["sequences"]) for i in ids),frame_positions=sum(len(s["frames"]) for i in ids for s in motions[i]["sequences"])))
                emit(b,folder,report)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--plan-only",action="store_true")
    ap.add_argument("--output",type=Path)
    ap.add_argument("--public-key",type=Path)
    args=ap.parse_args()
    r13.selftest()
    transfer_selftest()
    _,_,ids,groups=plan()
    print("R24_PLAN="+stable(dict(groups=len(ids),batches=10,old_disjoint=1003,selection_sha256=SELECTION_SHA,key_pairs_sha256=KEY_PAIRS_SHA)),flush=True)
    if not args.plan_only:
        assert args.output and args.public_key
        export(args.output,args.public_key)

if __name__=="__main__":
    main()
