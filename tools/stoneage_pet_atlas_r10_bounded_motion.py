"""R10: bounded original canvas recovery, retaining strict rejection and geometry gaps."""
import argparse,gzip,json,mmap,shutil
from collections import Counter
from pathlib import Path
from tools import stoneage_pet_atlas_r4_private_source as r4
from tools.stoneage_pet_atlas_r3_visual_reuse import build as reuse,PINS_R3
from tools.stoneage_pet_high_first_57_coverage import PINS,gzrows,blob,ROOT
from tools.stoneage_pet_high_first_66_motion_inheritance import EXTRA,sequence_tables
from tools.stoneage_pet_high_first_tw85_pixels import COLS,SOURCE_FILES,qualify_pair,original_check
from tools.stoneage_pet_high_first_60_source_pixels import summarize_carrier,CARRIER
from tools import stoneage_pet_high_first_68_rd_boundary as boundary
from tools import stoneage_pet_high_first_71_bulk_named_pixels as prior
from tools.stoneage_pet11_tw10_capture_sprite_source import rd_indices
from tools.stoneage_rd_codec import decode_rd_block,parse_rd_header
from tools.stoneage_scene07_independent_pixels import independent_rd
from tools.stoneage_original_observation_lab import gray_png
BATCH_SIZE=24
BATCH_COUNT=4
STRICT=prior.STRICT
BOUNDED=prior.BOUNDED
UNRESOLVED=prior.UNRESOLVED
def key(r):return tuple(r[k] for k in ("rd_sha256","size","width","height"))
def pin(p,h):
    assert blob(p.read_bytes())==h,p
    return p
def plan():
    late=r4.load(pin(*PINS_R3["later"]))
    old=reuse()["available_motion"]
    bounded={int(i):g for i,g in late["groups"].items() if g["status"]=="BOUNDED_COMPLETE"}
    unresolved={int(i):g for i,g in late["groups"].items() if g["status"]=="NO_COMPLETE_SEQUENCE"}
    already=sorted(i for i in bounded if str(i) in old)
    assert len(bounded)==93 and len(already)==4 and len(bounded)-len(already)==89
    assert set(unresolved)=={1369,1541}
    good=bounded|unresolved
    ids=sorted(good)
    groups={i:dict(graphic=good[i]["graphic"],animation_headers=good[i]["animation_headers"]) for i in ids}
    for k in ("groups","frames","native"):
        pin(*PINS[k])
    pin(*EXTRA["tw85_animation"])
    for g in gzrows(PINS["groups"][0]):
        i=int(g["index"])
        if i in groups:assert (int(g["spr_no"]),g["segment_sha256"],int(g["anim_count"]))==(groups[i]["graphic"],good[i]["spr_sha256"],groups[i]["animation_headers"])
    seq=sequence_tables(groups,EXTRA["tw85_animation"][0],PINS["frames"][0])
    numbers={f[0] for x in seq.values() for a in x.values() for f in a["frames"] if f[0] is not None}
    refs={}
    for r in gzrows(PINS["native"][0]):
        n=int(r["bitmapno"])
        if n in numbers:
            assert n not in refs
            refs[n]=dict(index=int(r["index"]),bitmap=n,offset=int(r["adder"]),size=int(r["size"]),width=int(r["width"]),height=int(r["height"]),adrn_sha256=r["record_sha256"],rd_sha256=r["rd_sha256"])
    assert set(refs)==numbers
    # Earlier bounded receipts may qualify another physical row only by exact RD content and geometry.
    known={}
    def add(x,b):
        v=dict(full_stream_sha256=b["full_stream_sha256"],canvas_prefix_sha256=b["canvas_prefix_sha256"],terminal_command=b["terminal_command"])
        assert known.setdefault(key(x),v)==v
    for x in r4.load(pin(boundary.RECEIPT,"3648e9b85a85cdb95b6c5207c548de8ecf177d5a"))["observations"].values():
        assert x["status"]==boundary.BOUND
        add(x,x)
    raw=json.loads(gzip.decompress(pin(prior.RECEIPT,"157cdf72e74ecb328a15e16771cb36e18735ca08").read_bytes()))
    for x in raw["observations"].values():
        if x["grade"]==BOUNDED:
            prior.verify_result(x)
            add(x,x["boundary"])
    del raw
    geo=r4.load(pin(ROOT/"research/pets/PET-HIGH-FIRST-72-GEOMETRY-RESIDUAL-SUMMARY-R1.json","c329ba84c0b7cc50a6284fdcdd7e858d156e3b5e"))
    geometry={x["bitmap"]:x for x in geo["geometry_records"]}
    assert set(geometry)=={322863,344133}<=numbers
    for n,r in refs.items():
        if n in geometry:
            g=geometry[n]
            assert all(r[k]==g[k] for k in ("index","bitmap","offset","size","width","height","adrn_sha256","rd_sha256"))
            r["grade"]=UNRESOLVED
        elif key(r) in known:r.update(grade=BOUNDED,boundary=known[key(r)])
        else:r["grade"]=STRICT
    for i in ids:
        counts=Counter(refs[f[0]]["grade"] for v in seq[i].values() for f in v["frames"] if f[0] is not None)
        assert dict(counts)==good[i]["frame_grades"],(i,counts,good[i]["frame_grades"])
    return ids,groups,seq,refs,good,already
def classification(a,refs):
    nums=[f[0] for f in a["frames"] if f[0] is not None]
    if not nums:return "sentinel_sequences"
    if any(refs[n]["grade"]==UNRESOLVED for n in nums):return "unresolved_sequences"
    if len(nums)!=len(a["frames"]):return "mixed_sequences"
    if any(refs[n]["grade"]==BOUNDED for n in nums):return "bounded_sequences"
    return "sequences"
CATEGORIES=("sequences","bounded_sequences","mixed_sequences","sentinel_sequences","unresolved_sequences")
def summary(ids,seq,refs):
    numbers={f[0] for i in ids for a in seq[i].values() for f in a["frames"] if f[0] is not None}
    return dict(group_count=len(ids),bitmaps=len(numbers),bitmap_grades=dict(Counter(refs[n]["grade"] for n in numbers)),sequences=sum(len(seq[i]) for i in ids),sequence_classes=dict(Counter(classification(a,refs) for i in ids for a in seq[i].values())),frame_positions=sum(len(a["frames"]) for i in ids for a in seq[i].values()),frame_grades=dict(Counter(refs[f[0]]["grade"] if f[0] is not None else "SENTINEL" for i in ids for a in seq[i].values() for f in a["frames"])))
def export(source,acquisition,private,public,out):
    ids,groups,seq,refs,good,already=plan()
    assert summarize_carrier(r4.load(acquisition))==summarize_carrier(r4.load(CARRIER))
    qualify_pair(source)
    for n in ("adrn_158.bin","real_158.bin"):original_check(source/n,SOURCE_FILES[n])
    private.mkdir(parents=True,exist_ok=False);out.mkdir(parents=True,exist_ok=False)
    adrn=(source/"adrn_158.bin").read_bytes()
    def one(r,real,folder):
        i=r["index"];raw=adrn[i*80:(i+1)*80]
        n,off,size,_,_,w,h,alias=COLS.unpack(raw)
        assert (n,off,size,w,h,r4.sha(raw))==tuple(r[k] for k in ("bitmap","offset","size","width","height","adrn_sha256"))
        assert 0<=off and 16<=size<=len(real)-off
        block=real[off:off+size];assert r4.sha(block)==r["rd_sha256"]
        row=dict(index=i,bitmap=n,alias=alias,width=w,height=h,size=size,rd_sha256=r4.sha(block),adrn_sha256=r4.sha(raw),grade=r["grade"])
        if r["grade"]==UNRESOLVED:
            hd=parse_rd_header(block)
            assert (w,h,size,hd["width_s"],hd["height_s"],hd["stored_size"])==(4,h,16,4,h,16) and h<0 and hd["flag"]==1
            assert prior.diagnose(block,w,h)["grade"]==UNRESOLVED
            return dict(**row,path=None,indexed_pixel_sha256=None,png_sha256=None,geometry="NONPOSITIVE_GEOMETRY",runtime_verified=False)
        assert 0<w*h<=1000000 and w>0 and h>0
        if r["grade"]==BOUNDED:
            d=prior.diagnose(block,w,h);assert d["grade"]==BOUNDED
            b=d["boundary"];assert all(b[k]==v for k,v in r["boundary"].items())
            aa,bb,px,length,strict=rd_indices(block)
            assert (aa,bb,length,strict,r4.sha(px))==(w,h,w*h+1,False,b["canvas_prefix_sha256"])
            row.update(boundary=b,strict=d["strict"])
        else:
            hd,px=decode_rd_block(block,authoritative_block_size=size)
            assert (hd["width_s"],hd["height_s"],px)==independent_rd(block) and (w,h)==(hd["width_s"],hd["height_s"])
        path=f"motion-{i}.png";png=gray_png(px,w,h);(folder/path).write_bytes(png)
        return dict(**row,path=path,indexed_pixel_sha256=r4.sha(px),png_sha256=r4.sha(png))
    with (source/"real_158.bin").open("rb") as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as real:
        for batch in range(BATCH_COUNT):
            selected=ids[batch*BATCH_SIZE:(batch+1)*BATCH_SIZE]
            assert selected
            folder=private/f"batch-{batch+1}";folder.mkdir()
            numbers={f[0] for i in selected for a in seq[i].values() for f in a["frames"] if f[0] is not None}
            bitmaps={str(n):one(refs[n],real,folder) for n in sorted(numbers)}
            motions={}
            for i in selected:
                g=dict(graphic=groups[i]["graphic"],spr_sha256=good[i]["spr_sha256"],all_source_sequences=len(seq[i]),prior_partial=i in already,source_grade=good[i]["status"],**{k:[] for k in CATEGORIES})
                for k,a in seq[i].items():g[classification(a,refs)].append(dict(index=k,**a))
                assert sorted(a["index"] for k in CATEGORIES for a in g[k])==list(range(g["all_source_sequences"]))
                motions[str(i)]=g
            receipt=dict(schema="stoneage.pet.atlas_r10.private_motion_receipt.r1",batch=batch+1,groups=selected,motion_bitmaps=bitmaps,motion_groups=motions,source_files={n:dict(bytes=s,sha256=h) for n,(s,h) in SOURCE_FILES.items()},official_identity_verified=False,original_palette_runtime_verified=False,original_assets_published=False,summary=summary(selected,seq,refs))
            (folder/"receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,sort_keys=True,separators=(",",":")),encoding="utf-8")
            e=r4.seal(folder,public,out/f"batch-{batch+1}")
            print("R10_BATCH="+json.dumps(dict(batch=batch+1,groups=selected,summary=receipt["summary"],cipher_sha256=e["cipher_sha256"]),sort_keys=True),flush=True)
            shutil.rmtree(folder)
def main():
    p=argparse.ArgumentParser();p.add_argument("--plan-only",action="store_true");p.add_argument("--source",type=Path);p.add_argument("--acquisition",type=Path);p.add_argument("--private",type=Path);p.add_argument("--public-key",type=Path);p.add_argument("--output",type=Path);a=p.parse_args()
    if a.plan_only:
        prior.selftest()
        ids,g,s,r,_,already=plan()
        print("R10_PLAN="+json.dumps(dict(groups=ids,prior_partial=already,summary=summary(ids,s,r)),sort_keys=True),flush=True);return
    assert all((a.source,a.acquisition,a.private,a.public_key,a.output))
    export(a.source,a.acquisition,a.private,a.public_key,a.output)
if __name__=="__main__":main()
