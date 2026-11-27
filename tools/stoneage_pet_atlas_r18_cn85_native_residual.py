"""R18: one authenticated CN85 read for residual motion, anomaly bytes, and private PE custody.
Original executables never executed; no plaintext original material in public artifacts.
"""
import argparse,base64,collections,hashlib,io,json,mmap,secrets,struct,tempfile,zipfile
from pathlib import Path
from tools import stoneage_pet_atlas_r13_cn85_original as r13
from tools import stoneage_pet_high_first_122_cn85_complete_transfer as transfer
from tools import stoneage_pet_high_first_124_cn85_native_album as native
from tools import stoneage_pet_atlas_r4_private_source as secure
from tools.stoneage_tw10_resource_metadata import parse_adrn_record
from tools.stoneage_original_observation_lab import gray_png
P=r13.P
ANOMALIES={7339,8603,8614,8619,283656,283663,283669,284524}
REF="PET-WHOLE-REVIEW-RESIDUAL-VISUAL-R1.json"
PIN="320dbf690fc184434659debe7c60408a62135454"
KEY="d0429134219d9e95b2d080825389227d3c17718d"
def plan():
    d,p,rows,faces,old,exact,ordinal,slot,groups=r13.plan()
    w=r13.load(P/REF,PIN)
    rr=[x for x in w["cn85_rows"] if x["grade"]=="TW85_NAME_VARIANT_EXACT_FACE_RD_SPR"]
    assert len(rr)==70 and r13.sha(r13.stable(rr).encode())=="41c0b6eb555a5f771ae258d30f4402cc964f9fc9a3b7d785fe46253ca4624685"
    ids=set()
    for row in rr:
        for variant in row["tw85"]:
            for g in variant["groups"]:
                i=g["cn_group"];assert i==g["tw_group"] and i not in old
                assert int(groups[i]["spr_no"])==g["number"] and groups[i]["segment_sha256"]==g["sha256"]
                ids.add(i)
    assert len(ids)==263
    return d,p,rr,sorted(ids),groups
def seal_original(files,report,pub,out):
    # Explicit allowlist of exact authenticated program and anomaly members.
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes,serialization
    allow=set(transfer.PROGRAMS)|{"StoneageNg.dll","receipt.json"}|{f"rd-{i}.bin" for i in ANOMALIES}
    assert set(files)|{"receipt.json"}==allow
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w",compression=zipfile.ZIP_DEFLATED) as z:
        for n,b in sorted(files.items()):z.writestr(n,b)
        z.writestr("receipt.json",r13.stable(report).encode())
    raw=buf.getvalue();key=AESGCM.generate_key(bit_length=256);nonce=secrets.token_bytes(12)
    aad=b"stoneage-pet-atlas-r18-private-originals"
    enc=AESGCM(key).encrypt(nonce,raw,aad)
    public=serialization.load_pem_public_key(pub.read_bytes())
    wrapped=public.encrypt(key,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    out.mkdir()
    (out/"private.enc").write_bytes(enc)
    e=dict(schema="stoneage.pet.atlas_r18.private_original_envelope.r1",cipher_sha256=r13.sha(enc),plain_sha256=r13.sha(raw),plain_bytes=len(raw),cipher_bytes=len(enc),nonce=base64.b64encode(nonce).decode(),wrapped_key=base64.b64encode(wrapped).decode(),aad=aad.decode())
    (out/"envelope.json").write_text(r13.stable(e))
    return e
def export(out,pub):
    d,p,rr,ids,groups=plan()
    b=pub.read_bytes();assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==KEY
    cap=r13.load(transfer.old.p.R117)["results"][0]
    a=r13.load(transfer.old.prev.REPORT)["results"][0]
    assert cap["cdx"]==a["cdx"]==d["capture"]
    out.mkdir(parents=True,exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="cn85-r18-") as tmp:
        root=Path(tmp);archive=root/"StoneAge.zip"
        t=transfer.transfer(cap,archive)
        print("R18_TRANSFER="+r13.stable(t),flush=True)
        assert t["complete"] and t["cdx_digest_matches"] and t["sha256"]==d["transfer"]["sha256"]
        assert transfer.old.inspect_zip(archive,root,cap,a)==d["zip_members"]
        rs=transfer.old.extract(root,a)
        known={x["name"]:x for x in d["selected_resources"]}
        assert len(rs)==6 and all(x["result"]=="EXTRACTED_SIZE_VERIFIED" and x["sha256"]==known[x["name"]]["sha256"] for x in rs)
        paths={x.name:x for x in (root/"selected").rglob("*") if x.is_file()}
        originals={"StoneageNg.dll":paths["StoneageNg.dll"].read_bytes()}
        for n in transfer.PROGRAMS:
            r,path=transfer.select(root,a,n)
            assert path and r["sha256"]==known[n]["sha256"]
            originals[n]=path.read_bytes()
        for n,b in originals.items():assert len(b)==known[n]["bytes"] and r13.sha(b)==known[n]["sha256"]
        programs={}
        for n in transfer.PROGRAMS:
            # Recompute the original table row and literal witnesses without executing PE.
            row=next(x for x in p["analysis"]["programs"] if x["program"]==n)
            programs[n]=dict(sha256=r13.sha(originals[n]),bytes=len(originals[n]),table_start=row["table_start"],table_end=row["table_end"],table_sha256=r13.sha(originals[n][row["table_start"]:row["table_end"]]))
            assert programs[n]["table_sha256"]==row["table_sha256"]
        real,rec=native.extract_real(root,a);assert rec==p["real_receipt"]
        body=paths["spr_155.bin"].read_bytes();index=paths["spradrn_155.bin"].read_bytes()
        motions=r13.group_sequences(body,index,groups,ids,set(),set(),set())
        wanted={f[0] for g in motions.values() for s in g["sequences"] for f in s["frames"] if f[0] is not None}
        adrn=paths["adrn_185.bin"].read_bytes();assert len(adrn)==36719200
        by=collections.defaultdict(list)
        for i in range(len(adrn)//80):
            n=struct.unpack_from("<I",adrn,i*80)[0]
            if n in wanted:by[n].append(i)
        source_files={n:dict(bytes=known[n]["bytes"],sha256=known[n]["sha256"]) for n in ("adrn_185.bin","spr_155.bin","spradrn_155.bin")}
        source_files["real_185.bin"]={k:rec[k] for k in ("bytes","sha256")}
        common=dict(schema="stoneage.pet.atlas_r18.cn85_residual.r1",source_files=source_files,source_archive_sha256=t["sha256"],source_pins=r13.PINS|{REF:PIN},official_identity_verified=False,native_selector_verified=False,original_palette_runtime_verified=False,original_assets_published=False)
        def block(i,mm):
            raw=adrn[i*80:(i+1)*80];x=parse_adrn_record(raw);off,size,w,h=x["adder"],x["size"],x["width"],x["height"]
            assert 0<=off<=len(mm) and 16<=size<=len(mm)-off
            data=mm[off:off+size]
            row=dict(index=i,bitmap=x["bitmapno"],alias=x["map_number"],width=w,height=h,size=size,offset=off,xoff=x["xoff"],yoff=x["yoff"],adrn_sha256=r13.sha(raw),rd_sha256=r13.sha(data))
            return row,data
        with real.open("rb") as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as mm:
            anomalies=[]
            for i in sorted(ANOMALIES):
                row,data=block(i,mm);grade,px,diag=r13.pixel(data,row["width"],row["height"])
                assert px is None and grade in ("RD_LENGTH_DISCREPANCY","NONPOSITIVE_OR_OVERSIZE_GEOMETRY")
                originals[f"rd-{i}.bin"]=data
                anomalies.append(dict(row,grade=grade,decode_evidence=diag))
            e=seal_original(originals,dict(common,programs=programs,anomalies=anomalies,member_hashes={n:dict(bytes=len(b),sha256=r13.sha(b)) for n,b in originals.items()}),pub,out/"originals")
            print("R18_PRIVATE_ORIGINALS="+r13.stable(dict(programs=len(originals)-len(ANOMALIES),anomalies=len(anomalies),cipher_sha256=e["cipher_sha256"])),flush=True)
            for batch,start in enumerate(range(0,len(ids),53),1):
                selected=ids[start:start+53];folder=root/f"motion-{batch}";folder.mkdir()
                nums={f[0] for i in selected for s in motions[i]["sequences"] for f in s["frames"] if f[0] is not None}
                links={str(n):by.get(n,[]) for n in sorted(nums)}
                images={}
                for i in sorted({i for rr in links.values() for i in rr}):
                    row,data=block(i,mm);grade,px,diag=r13.pixel(data,row["width"],row["height"])
                    row.update(grade=grade,decode_evidence=diag,path=None,png_sha256=None,indexed_pixel_sha256=None)
                    if px is not None:
                        n=f"bitmap-{i}.png";png=gray_png(px,row["width"],row["height"]);(folder/n).write_bytes(png)
                        row.update(path=n,png_sha256=r13.sha(png),indexed_pixel_sha256=r13.sha(px))
                    images[str(i)]=row
                summary=dict(groups=len(selected),bitmaps=len(images),bitmap_numbers=len(nums),missing_numbers=sum(not v for v in links.values()),ambiguous_numbers=sum(len(v)>1 for v in links.values()),grades=dict(collections.Counter(q["grade"] for q in images.values())),sequences=sum(len(motions[i]["sequences"]) for i in selected),frame_positions=sum(len(s["frames"]) for i in selected for s in motions[i]["sequences"]))
                report=dict(common,batch=batch,groups=selected,motion_groups={str(i):dict(motions[i],exact_tw85_spr_reference=True) for i in selected},bitmap_candidates=links,bitmaps=images,summary=summary)
                (folder/"receipt.json").write_text(r13.stable(report),encoding="utf-8")
                e=secure.seal(folder,pub,out/f"batch-{batch}")
                print("R18_BATCH="+r13.stable(dict(batch=batch,summary=summary,cipher_sha256=e["cipher_sha256"])),flush=True)
                import shutil
                shutil.rmtree(folder)
def main():
    a=argparse.ArgumentParser();a.add_argument("--plan-only",action="store_true");a.add_argument("--output",type=Path);a.add_argument("--public-key",type=Path);args=a.parse_args()
    r13.selftest()
    _,_,rr,ids,_=plan()
    print("R18_PLAN="+r13.stable(dict(positions=len(rr),groups=len(ids),batches=5,anomalies=sorted(ANOMALIES))),flush=True)
    if not args.plan_only:
        assert args.output and args.public_key
        export(args.output,args.public_key)
if __name__=="__main__":main()
