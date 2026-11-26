"""R4: export remaining exact TW85 portrait candidates and a bounded full-motion batch.

Only private encrypted image packages may leave the runner. No game execution,
official identity inference, or plaintext commercial images in public Git.
"""
import argparse, base64, hashlib, io, json, mmap, secrets, zipfile
from pathlib import Path
from tools.stoneage_pet_atlas_r3_visual_reuse import build as reuse, PINS_R3
from tools.stoneage_pet_high_first_57_coverage import blob, gzrows, PINS
from tools.stoneage_pet_high_first_66_motion_inheritance import EXTRA, sequence_tables
from tools.stoneage_pet_high_first_tw85_pixels import COLS, SOURCE_FILES, qualify_pair, original_check
from tools.stoneage_pet_high_first_60_source_pixels import summarize_carrier, CARRIER
from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_scene07_independent_pixels import independent_rd
from tools.stoneage_original_observation_lab import gray_png

def sha(x):return hashlib.sha256(x).hexdigest()
def load(p):return json.loads(p.read_bytes())
def require(ok,msg):
    if not ok:raise ValueError(msg)

def plan():
    old=reuse()
    late=load(PINS_R3["later"][0]); pr=load(PINS_R3["portraits"][0])
    selected={str(i):pr["observations"][str(i)] for rr in pr["aliases"].values() for i,n in rr if str(i) not in old["available_portraits"]}
    require(len(selected)==384,"portrait count drift")
    for r in selected.values():
        require(r["grade"]=="STRICT_PIXEL_RECEIPT" and r["pixel_sha256"] is not None,"not strict portrait")
    # Deterministic first batch of complete, strict high-version groups not
    # already playable from R3. Include the historically named 雷帝斯洛 group.
    good={int(i):g for i,g in late["groups"].items() if g["status"]=="STRICT_COMPLETE" and i not in old["available_motion"]}
    require(1185 in good,"named demonstration group absent")
    ids=[1185]+[i for i in sorted(good) if i!=1185][:31]
    groups={i:dict(graphic=good[i]["graphic"],animation_headers=0) for i in ids}
    for g in gzrows(PINS["groups"][0]):
        i=int(g["index"])
        if i in groups:
            require((int(g["spr_no"]),g["segment_sha256"])==(groups[i]["graphic"],good[i]["spr_sha256"]),"SPR group drift")
            groups[i]["animation_headers"]=int(g["anim_count"])
    seq=sequence_tables(groups,EXTRA["tw85_animation"][0],PINS["frames"][0])
    numbers={f[0] for x in seq.values() for a in x.values() for f in a["frames"] if f[0] is not None}
    refs={}
    for r in gzrows(PINS["native"][0]):
        n=int(r["bitmapno"])
        if n in numbers:
            require(n not in refs,"ambiguous motion bitmap")
            refs[n]=dict(index=int(r["index"]),bitmap=n,offset=int(r["adder"]),size=int(r["size"]),width=int(r["width"]),height=int(r["height"]),adrn_sha256=r["record_sha256"],rd_sha256=r["rd_sha256"])
    require(set(refs)==numbers,"missing motion RD")
    return selected,groups,seq,refs,good

def export(source,acquisition,private,out):
    portraits,groups,seq,refs,good=plan()
    require(summarize_carrier(load(acquisition))==summarize_carrier(load(CARRIER)),"carrier mismatch")
    qualify_pair(source)
    for n in ("adrn_158.bin","real_158.bin"):original_check(source/n,SOURCE_FILES[n])
    private.mkdir(parents=True,exist_ok=False)
    adrn=(source/"adrn_158.bin").read_bytes()
    def one(r,real,kind):
        i=r["index"];raw=adrn[i*80:(i+1)*80]
        n,off,size,_,_,w,h,alias=COLS.unpack(raw)
        require((n,off,size,w,h,sha(raw))==tuple(r[k] for k in ("bitmap","offset","size","width","height","adrn_sha256")),"ADRN mismatch")
        require(0<=off and 16<=size<=len(real)-off and 0<w*h<=1000000 and w>0 and h>0,"bad extent")
        if kind=="portrait":require(alias==r["alias"],"portrait alias mismatch")
        block=real[off:off+size];require(sha(block)==r["rd_sha256"],"RD mismatch")
        h0,px=decode_rd_block(block,authoritative_block_size=size)
        require((h0["width_s"],h0["height_s"],px)==independent_rd(block) and (w,h)==(h0["width_s"],h0["height_s"]),"dual decoder mismatch")
        if kind=="portrait":require(sha(px)==r["pixel_sha256"],"prior indexed pixel mismatch")
        path=f"{kind}-{i}.png";png=gray_png(px,w,h);(private/path).write_bytes(png)
        return dict(index=i,bitmap=n,alias=alias,width=w,height=h,size=size,rd_sha256=sha(block),adrn_sha256=sha(raw),indexed_pixel_sha256=sha(px),png_sha256=sha(png),path=path)
    with (source/"real_158.bin").open("rb") as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as real:
        p={k:one(r,real,"portrait") for k,r in portraits.items()}
        m={str(n):one(r,real,"motion") for n,r in refs.items()}
    motions={}
    for i,x in seq.items():
        motions[str(i)]=dict(graphic=groups[i]["graphic"],spr_sha256=good[i]["spr_sha256"],all_source_sequences=len(x),
                             sequences=[dict(index=k,**a) for k,a in x.items() if a["frames"] and all(f[0] is not None for f in a["frames"])])
    d=dict(schema="stoneage.pet.atlas_r4.private_source_receipt.r1",portraits=p,motion_bitmaps=m,motion_groups=motions,
           source_files={n:dict(bytes=s,sha256=h) for n,(s,h) in SOURCE_FILES.items()},
           official_identity_verified=False,original_palette_runtime_verified=False,original_assets_published=False,
           summary=dict(new_portrait_rows=len(p),motion_groups=len(motions),motion_bitmaps=len(m),playable_sequences=sum(len(x["sequences"]) for x in motions.values()),
                        source_sequences=sum(x["all_source_sequences"] for x in motions.values()),frame_positions=sum(len(a["frames"]) for x in motions.values() for a in x["sequences"])))
    (private/"receipt.json").write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(",",":")),encoding="utf-8")
    return d

def seal(private,public,out):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes,serialization
    out.mkdir(parents=True,exist_ok=False)
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w",compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(private.iterdir()):
            require(p.is_file() and not p.is_symlink() and (p.name=="receipt.json" or p.suffix==".png"),"unsafe private package")
            z.write(p,p.name)
    raw=buf.getvalue();pub=serialization.load_pem_public_key(public.read_bytes())
    key=AESGCM.generate_key(bit_length=256);nonce=secrets.token_bytes(12);aad=b"stoneage-pet-atlas-r4-private-source"
    enc=AESGCM(key).encrypt(nonce,raw,aad)
    wrapped=pub.encrypt(key,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    (out/"private.enc").write_bytes(enc)
    envelope=dict(schema="stoneage.pet.atlas_r4.envelope.r1",cipher_sha256=sha(enc),plain_sha256=sha(raw),plain_bytes=len(raw),cipher_bytes=len(enc),nonce=base64.b64encode(nonce).decode(),wrapped_key=base64.b64encode(wrapped).decode(),aad=aad.decode())
    (out/"envelope.json").write_text(json.dumps(envelope,sort_keys=True))
    return envelope

def main():
    p=argparse.ArgumentParser();p.add_argument("--plan-only",action="store_true");p.add_argument("--source",type=Path);p.add_argument("--acquisition",type=Path);p.add_argument("--private",type=Path);p.add_argument("--public-key",type=Path);p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.plan_only:
        p0,g,s,r,_=plan();print("R4_PLAN",len(p0),len(g),len(r),flush=True);return
    require(all((a.source,a.acquisition,a.private,a.public_key,a.output)),"required paths missing")
    d=export(a.source,a.acquisition,a.private,a.output)
    e=seal(a.private,a.public_key,a.output)
    print("R4_SOURCE_SUMMARY="+json.dumps(d["summary"],sort_keys=True),flush=True)
    print("R4_ENVELOPE_SHA256="+e["cipher_sha256"],flush=True)
if __name__=="__main__":main()
