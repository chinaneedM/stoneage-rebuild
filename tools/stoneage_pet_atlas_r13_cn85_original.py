"""R13 authenticated CN85 portraits and source-separated motion candidates."""
import argparse,collections,hashlib,json,mmap,shutil,struct,tempfile
from pathlib import Path
from tools import stoneage_pet_high_first_122_cn85_complete_transfer as transfer
from tools import stoneage_pet_high_first_124_cn85_native_album as native
from tools import stoneage_pet_atlas_r4_private_source as secure
from tools.stoneage_tw10_resource_metadata import parse_adrn_record
from tools.stoneage_rd_codec import decode_rd_block,parse_rd_header,RDDecodeError
from tools.stoneage_scene07_independent_pixels import independent_rd
from tools.stoneage_pet_high_first_68_rd_boundary import diagnose,BOUND
from tools.stoneage_pet11_tw10_capture_sprite_source import rd_indices
from tools.stoneage_original_observation_lab import gray_png
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research/pets"
PINS={
"PET-HIGH-FIRST-122-CN85-COMPLETE-TRANSFER-R1.json":"a6ed895e5b6b18ebaa1c02e809da5a17937dd176",
"PET-HIGH-FIRST-124-CN85-NATIVE-ALBUM-R1.json":"17a42f4de1d9e508b580c88de70bb012d7e03c9b",
"PET-CN50-CN85-SPR-INHERITANCE-R1.json":"26763873998c93075342028752c40074fe472934"}
def sha(x):return hashlib.sha256(x).hexdigest()
def load(path,pin=None):
    raw=path.read_bytes()
    if pin:assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==pin,path
    return json.loads(raw)
def stable(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def plan():
    d,p,c=[load(P/n,h) for n,h in PINS.items()]
    assert d["original_client_verified"] and p["original_client_reacquired"]
    assert d["transfer"]["sha256"]==p["transfer"]["sha256"]=="747dfd8d44274d5d128c2784ed32462eb1930861160003445ec6f7cfe827e843"
    rows=p["analysis"]["resource_links"]["rows"]
    exact={g["cn85_exact_positions"][0] for x in c["rows"] for g in x["groups"] if len(g["cn85_exact_positions"])==1}
    ordinal={i for x in rows for i in x["ordinal_spr_group_indices"]}
    slot={i for x in rows for i in x["slot_spr_group_indices"]}
    selected=sorted(exact|ordinal|slot)
    faces={v["adrn_index"]:v for x in rows for v in x["face_map_number_candidates"]}
    assert len(rows)==548 and len(faces)==552 and len(exact)==594 and len(ordinal)==349 and len(slot)==322 and len(selected)==740
    groups=d["analysis"]["spr"]["group_rows"];assert len(groups)==1837
    assert all(int(g["index"])==i for i,g in enumerate(groups))
    for x in c["rows"]:
        for g in x["groups"]:
            i,=g["cn85_exact_positions"];assert groups[i]["segment_sha256"]==g["sha256"] and int(groups[i]["spr_no"])==g["number"]
    return d,p,rows,faces,selected,exact,ordinal,slot,groups
def group_sequences(body,index,groups,selected,exact,ordinal,slot):
    out={}
    for i in selected:
        row=groups[i];num,start,count,reserved=struct.unpack_from("<IIHH",index,i*12)
        end=int(row["end_offset"])
        assert (num,start,count,reserved)==tuple(int(row[k]) for k in ("spr_no","offset","anim_count","reserved"))
        assert 0<=start<end<=len(body) and sha(body[start:end])==row["segment_sha256"]
        pos=start;seq=[]
        for j in range(count):
            assert pos+12<=end
            direction,action,duration,n=struct.unpack_from("<HHII",body,pos);pos+=12
            assert pos+10*n<=end
            frames=[]
            for _ in range(n):
                b,x,y,sound=struct.unpack_from("<IhhH",body,pos);pos+=10
                frames.append([None if b==0xffffffff else b,x,y,sound])
            seq.append(dict(index=j,direction=direction,action=action,duration=duration,count=n,frames=frames))
        assert pos==end
        out[i]=dict(graphic=num,spr_sha256=row["segment_sha256"],exact_cn50_spr=i in exact,ordinal_candidate=i in ordinal,slot_candidate=i in slot,all_source_sequences=count,sequences=seq,native_selector_verified=False)
    return out
def pixel(block,w,h):
    if w<=0 or h<=0 or w*h>1000000:return "NONPOSITIVE_OR_OVERSIZE_GEOMETRY",None,None
    try:hd=parse_rd_header(block)
    except RDDecodeError:return "INVALID_RD_HEADER",None,None
    if (hd["width_s"],hd["height_s"])!=(w,h):return "RD_GEOMETRY_MISMATCH",None,hd
    if hd["stored_size"]!=len(block):return "RD_LENGTH_DISCREPANCY",None,hd
    try:
        a,b=decode_rd_block(block,authoritative_block_size=len(block))
        c=independent_rd(block)
        if (w,h,b)!=c:return "DECODER_DISAGREEMENT",None,hd
        return "STRICT_PIXEL_RECEIPT",b,hd
    except (RDDecodeError,ValueError):
        if hd["flag"]==1:
            diag=diagnose(block,w,h)
            if diag["status"]==BOUND:
                aa,bb,px,n,strict=rd_indices(block)
                assert (aa,bb,n,strict,sha(px))==(w,h,w*h+1,False,diag["canvas_prefix_sha256"])
                return "BOUNDED_CANVAS_RECEIPT",px,diag
        return "STRICT_DECODE_REJECTED",None,hd
def selftest():
    def rd(w,h,payload,size=None):return b"RD"+bytes([1,0])+struct.pack("<iiI",w,h,size if size is not None else 16+len(payload))+payload
    assert pixel(rd(2,2,bytes([4,1,2,3,4])),2,2)[:2]==("STRICT_PIXEL_RECEIPT",bytes([1,2,3,4]))
    assert pixel(rd(2,2,bytes([3,1,2,3,0xc2])),2,2)[:2]==("BOUNDED_CANVAS_RECEIPT",bytes([1,2,3,0]))
    assert pixel(rd(2,2,bytes([4,1,2,3,4]),999),2,2)[0]=="RD_LENGTH_DISCREPANCY"
    assert pixel(rd(2,-2,b""),2,-2)[0]=="NONPOSITIVE_OR_OVERSIZE_GEOMETRY"
    print("R13_SELFTEST_PASS",flush=True)
def export(out,pub):
    d,p,rows,faces,selected,exact,ordinal,slot,groups=plan()
    cap=load(transfer.old.p.R117)["results"][0]
    a=load(transfer.old.prev.REPORT)["results"][0]
    assert cap["cdx"]==a["cdx"]==d["capture"]
    out.mkdir(parents=True,exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="cn85-r13-") as tmp:
        root=Path(tmp);archive=root/"StoneAge.zip"
        t=transfer.transfer(cap,archive)
        print("R13_TRANSFER="+stable(t),flush=True)
        assert t["complete"] and t["cdx_digest_matches"] and t["sha256"]==d["transfer"]["sha256"]
        assert transfer.old.inspect_zip(archive,root,cap,a)==d["zip_members"]
        rr=transfer.old.extract(root,a)
        known={x["name"]:x for x in d["selected_resources"]}
        assert len(rr)==6 and all(x["result"]=="EXTRACTED_SIZE_VERIFIED" and x["sha256"]==known[x["name"]]["sha256"] for x in rr)
        real,receipt=native.extract_real(root,a);assert receipt==p["real_receipt"]
        paths={x.name:x for x in (root/"selected").rglob("*") if x.is_file()}
        body=paths["spr_155.bin"].read_bytes();index=paths["spradrn_155.bin"].read_bytes()
        motions=group_sequences(body,index,groups,selected,exact,ordinal,slot)
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
            print("R13_BATCH="+stable(dict(batch=batch,summary=report["summary"],cipher_sha256=e["cipher_sha256"])),flush=True)
            shutil.rmtree(folder)
        common=dict(schema="stoneage.pet.atlas_r13.cn85_original.r1",source_files=files,source_archive_sha256=t["sha256"],source_pins=PINS,official_identity_verified=False,native_selector_verified=False,original_palette_runtime_verified=False,original_assets_published=False)
        with real.open("rb") as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as mm:
            folder=root/"portraits";folder.mkdir()
            images={}
            for i,v in sorted(faces.items()):
                q=make(i,mm,folder)
                assert (q["bitmap"],q["offset"],q["size"],q["width"],q["height"],q["rd_sha256"])==tuple(v[k] for k in ("bitmapno","offset","size","width","height","rd_sha256"))
                images[str(i)]=q
            emit(0,folder,dict(common,batch=0,portrait_positions=rows,bitmaps=images,summary=dict(positions=len(rows),bitmaps=len(images),grades=dict(collections.Counter(q["grade"] for q in images.values())))))
            for b,start in enumerate(range(0,len(selected),62),1):
                ids=selected[start:start+62];folder=root/f"motion-{b}";folder.mkdir()
                nums={f[0] for i in ids for s in motions[i]["sequences"] for f in s["frames"] if f[0] is not None}
                links={str(n):by.get(n,[]) for n in sorted(nums)}
                indexes=sorted({i for rr in links.values() for i in rr});images={str(i):make(i,mm,folder) for i in indexes}
                report=dict(common,batch=b,groups=ids,motion_groups={str(i):motions[i] for i in ids},bitmap_candidates=links,bitmaps=images,summary=dict(groups=len(ids),bitmaps=len(images),bitmap_numbers=len(nums),missing_numbers=sum(not v for v in links.values()),ambiguous_numbers=sum(len(v)>1 for v in links.values()),grades=dict(collections.Counter(q["grade"] for q in images.values())),sequences=sum(len(motions[i]["sequences"]) for i in ids),frame_positions=sum(len(s["frames"]) for i in ids for s in motions[i]["sequences"])))
                emit(b,folder,report)
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--plan-only",action="store_true");ap.add_argument("--output",type=Path);ap.add_argument("--public-key",type=Path);args=ap.parse_args();selftest()
    _,_,rows,faces,selected,exact,ordinal,slot,_=plan()
    print("R13_PLAN="+stable(dict(positions=len(rows),portraits=len(faces),groups=selected,exact_cn50_groups=sorted(exact),ordinal_candidates=sorted(ordinal),slot_candidates=sorted(slot),batches=12)),flush=True)
    if not args.plan_only:
        assert args.output and args.public_key
        export(args.output,args.public_key)
if __name__=="__main__":main()
