"""R8: one authenticated TW85 acquisition, multiple bounded full motion capsules.
Original commercial assets only in authenticated encrypted private capsules.
"""
import argparse,json,mmap
from pathlib import Path
from collections import Counter
from tools import stoneage_pet_atlas_r4_private_source as r4
from tools.stoneage_pet_atlas_r3_visual_reuse import build as reuse,PINS_R3
from tools.stoneage_pet_high_first_57_coverage import PINS,gzrows,blob
from tools.stoneage_pet_high_first_66_motion_inheritance import EXTRA,sequence_tables
from tools.stoneage_pet_high_first_tw85_pixels import COLS,SOURCE_FILES,qualify_pair,original_check
from tools.stoneage_pet_high_first_60_source_pixels import summarize_carrier,CARRIER
from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_scene07_independent_pixels import independent_rd
from tools.stoneage_original_observation_lab import gray_png
BATCH_SIZE=48
BATCH_COUNT=4
def plan():
    assert blob((PINS_R3["later"][0].parents[1].parent/"tools/stoneage_pet_atlas_r5_motion_batches.py").read_bytes())=="1bea93b1fd6545a4f7dfed592d37b44e5cb505c3"
    assert blob((PINS_R3["later"][0].parents[1].parent/"tools/stoneage_pet_atlas_r6_motion_batches.py").read_bytes())=="586e15d9e9157eb623fe195fe3a84496b96586c0"
    assert blob((PINS_R3["later"][0].parents[1].parent/"tools/stoneage_pet_atlas_r7_motion_batches.py").read_bytes())=="b3f1f6c7674190525b1e2b2800dfe0203e14eebc"
    old=reuse()
    late=r4.load(PINS_R3["later"][0])
    good={int(i):g for i,g in late["groups"].items() if g["status"]=="STRICT_COMPLETE" and i not in old["available_motion"]}
    prior=[1185]+[i for i in sorted(good) if i!=1185][:31]
    assert len(set(prior))==32 and set(prior)<=set(good)
    # The R4 receipt contains exactly these 32 groups, pinned by its accepted
    # deterministic source plan. Prioritize source order for repeatable recovery.
    remaining=[i for i in sorted(good) if i not in prior]
    prior_r5=remaining[:192]
    assert len(prior_r5)==192 and prior_r5[0]==499 and prior_r5[-1]==737
    prior_r6=remaining[192:384]
    assert len(prior_r6)==192 and prior_r6[0]==738 and prior_r6[-1]==936
    prior_r7=remaining[384:576]
    assert len(prior_r7)==192 and prior_r7[0]==937
    from tools.stoneage_pet_atlas_r7_motion_batches import plan as r7_plan
    assert prior_r7==r7_plan()[0], "R7 scope mismatch"
    residual=remaining[576:]
    assert len(residual)==500, "strict residual count differs from R7 acceptance; reconcile before extraction"
    ids=residual[:BATCH_SIZE*BATCH_COUNT]
    assert len(ids)==BATCH_SIZE*BATCH_COUNT and not set(ids)&(set(prior)|set(prior_r5)|set(prior_r6)|set(prior_r7))
    groups={i:dict(graphic=good[i]["graphic"],animation_headers=0) for i in ids}
    for g in gzrows(PINS["groups"][0]):
        i=int(g["index"])
        if i in groups:
            assert (int(g["spr_no"]),g["segment_sha256"])==(groups[i]["graphic"],good[i]["spr_sha256"])
            groups[i]["animation_headers"]=int(g["anim_count"])
    seq=sequence_tables(groups,EXTRA["tw85_animation"][0],PINS["frames"][0])
    numbers={f[0] for x in seq.values() for a in x.values() for f in a["frames"] if f[0] is not None}
    refs={}
    for r in gzrows(PINS["native"][0]):
        n=int(r["bitmapno"])
        if n in numbers:
            assert n not in refs
            refs[n]=dict(index=int(r["index"]),bitmap=n,offset=int(r["adder"]),size=int(r["size"]),width=int(r["width"]),height=int(r["height"]),adrn_sha256=r["record_sha256"],rd_sha256=r["rd_sha256"])
    assert set(refs)==numbers
    return ids,groups,seq,refs,good
def export(source,acquisition,private,public,out):
    ids,groups,seq,refs,good=plan()
    assert summarize_carrier(r4.load(acquisition))==summarize_carrier(r4.load(CARRIER))
    qualify_pair(source)
    for n in ("adrn_158.bin","real_158.bin"):original_check(source/n,SOURCE_FILES[n])
    private.mkdir(parents=True,exist_ok=False)
    out.mkdir(parents=True,exist_ok=False)
    adrn=(source/"adrn_158.bin").read_bytes()
    def one(r,real,folder):
        i=r["index"];raw=adrn[i*80:(i+1)*80]
        n,off,size,_,_,w,h,alias=COLS.unpack(raw)
        assert (n,off,size,w,h,r4.sha(raw))==tuple(r[k] for k in ("bitmap","offset","size","width","height","adrn_sha256"))
        assert 0<=off and 16<=size<=len(real)-off and 0<w*h<=1000000 and w>0 and h>0
        block=real[off:off+size];assert r4.sha(block)==r["rd_sha256"]
        header,px=decode_rd_block(block,authoritative_block_size=size)
        assert (header["width_s"],header["height_s"],px)==independent_rd(block) and (w,h)==(header["width_s"],header["height_s"])
        path=f"motion-{i}.png";png=gray_png(px,w,h);(folder/path).write_bytes(png)
        return dict(index=i,bitmap=n,alias=alias,width=w,height=h,size=size,rd_sha256=r4.sha(block),adrn_sha256=r4.sha(raw),indexed_pixel_sha256=r4.sha(px),png_sha256=r4.sha(png),path=path)
    with (source/"real_158.bin").open("rb") as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as real:
        for batch in range(BATCH_COUNT):
            selected=ids[batch*BATCH_SIZE:(batch+1)*BATCH_SIZE]
            folder=private/f"batch-{batch+1}";folder.mkdir()
            numbers={f[0] for i in selected for a in seq[i].values() for f in a["frames"] if f[0] is not None}
            bitmaps={str(n):one(refs[n],real,folder) for n in sorted(numbers)}
            motions={str(i):dict(graphic=groups[i]["graphic"],spr_sha256=good[i]["spr_sha256"],all_source_sequences=len(seq[i]),sentinel_sequences=[dict(index=k,**a) for k,a in seq[i].items() if not a["frames"] or any(f[0] is None for f in a["frames"])],sequences=[dict(index=k,**a) for k,a in seq[i].items() if a["frames"] and all(f[0] is not None for f in a["frames"])]) for i in selected}
            # Never discard a mixed drawable/sentinel sequence silently.
            for g in motions.values():
                assert len(g["sequences"])+len(g["sentinel_sequences"])==g["all_source_sequences"]
                assert all(all(f[0] is None for f in a["frames"]) for a in g["sentinel_sequences"]), "mixed sentinel sequence requires separate handling"
            summary=dict(motion_groups=len(motions),motion_bitmaps=len(bitmaps),playable_sequences=sum(len(g["sequences"]) for g in motions.values()),source_sequences=sum(g["all_source_sequences"] for g in motions.values()),frame_positions=sum(len(a["frames"]) for g in motions.values() for a in g["sequences"]))
            receipt=dict(schema="stoneage.pet.atlas_r8.private_motion_receipt.r1",batch=batch+1,groups=selected,motion_bitmaps=bitmaps,motion_groups=motions,source_files={n:dict(bytes=s,sha256=h) for n,(s,h) in SOURCE_FILES.items()},official_identity_verified=False,original_palette_runtime_verified=False,original_assets_published=False,summary=summary)
            (folder/"receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,sort_keys=True,separators=(",",":")),encoding="utf-8")
            e=r4.seal(folder,public,out/f"batch-{batch+1}")
            print("R8_BATCH="+json.dumps(dict(batch=batch+1,summary=summary,cipher_sha256=e["cipher_sha256"],groups=selected),sort_keys=True),flush=True)
            import shutil
            shutil.rmtree(folder)
def main():
    p=argparse.ArgumentParser();p.add_argument("--plan-only",action="store_true");p.add_argument("--source",type=Path);p.add_argument("--acquisition",type=Path);p.add_argument("--private",type=Path);p.add_argument("--public-key",type=Path);p.add_argument("--output",type=Path);a=p.parse_args()
    if a.plan_only:
        ids,g,s,r,_=plan()
        print("R8_PLAN="+json.dumps(dict(groups=ids,group_count=len(ids),bitmaps=len(r),sequences=sum(len(v) for v in s.values()),frame_positions=sum(len(x["frames"]) for v in s.values() for x in v.values()),strict_remaining_before=500,strict_remaining_after_candidate=500-len(ids),sentinel_only_sequences=sum(not a["frames"] or all(f[0] is None for f in a["frames"]) for v in s.values() for a in v.values()),mixed_sentinel_sequences=sum(bool(a["frames"]) and any(f[0] is None for f in a["frames"]) and any(f[0] is not None for f in a["frames"]) for v in s.values() for a in v.values())),sort_keys=True),flush=True);return
    assert all((a.source,a.acquisition,a.private,a.public_key,a.output))
    export(a.source,a.acquisition,a.private,a.public_key,a.output)
if __name__=="__main__":main()
