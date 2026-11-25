"""PET73: complete original portrait alias census and exact TW10 selected group 363 comparison."""
import argparse
from collections import Counter,defaultdict
import gzip
import json
import mmap
from pathlib import Path
import tempfile
from tools import stoneage_pet_high_first_65_full_visual as visual
from tools import stoneage_pet_high_first_66_motion_inheritance as prev
from tools import stoneage_pet_high_first_71_bulk_named_pixels as pet71
from tools import stoneage_pet_high_first_67_bulk_pixels as bulk
from tools.stoneage_pet_high_first_57_coverage import ROOT,PINS,blob,gzrows

P=ROOT/"research/pets"
RECEIPT=P/"PET-HIGH-FIRST-73-PORTRAIT-RESIDUAL-R1.json"
SUMMARY=P/"PET-HIGH-FIRST-73-PORTRAIT-RESIDUAL-SUMMARY-R1.json"
PAL=ROOT/"research/recovered/STONEAGE-TW85-PALETTE-SAME-CARRIER-R33.json"
PINS_EXTRA={PAL:"4b36a32fe52e9361e972904590816bf91a7d60fe",
    P/"PET-HIGH-FIRST-72-GEOMETRY-RESIDUAL-SUMMARY-R1.json":"c329ba84c0b7cc50a6284fdcdd7e858d156e3b5e",
    pet71.RECEIPT:"157cdf72e74ecb328a15e16771cb36e18735ca08",
    bulk.RECEIPT:"1801e69665de0d67ea7d15dce5396c267bb65374",
    **{PINS[k][0]:PINS[k][1] for k in ("grid","groups","frames","native","pairs","patch")},
    **{prev.EXTRA[k][0]:prev.EXTRA[k][1] for k in ("tw10_receipt","tw10_groups","tw10_animations","tw10_frames","tw10_adrn","tw85_animation")}}
def read(p):return json.loads(p.read_bytes())
def key(r):return r["rd_sha256"],int(r["size"]),int(r["width"]),int(r["height"])
def plan():
    for p,h in PINS_EXTRA.items():assert blob(p.read_bytes())==h,p
    d=visual.read()
    positions=defaultdict(list)
    for prog,x in d["grid"]["programs"].items():
        for r in x["source_records"]:
            positions[r["source_portrait_alias"]].append(dict(program=prog,slot=r["slot"],name=r["original_name_cp950"],row_sha256=r["original_row_sha256"]))
    assert len(positions)==508 and sum(map(len,positions.values()))==1889
    prior=defaultdict(dict);prior_pixels={}
    for report in (d["tw_pixels"],d["tw_long"]["observations"],d["tw60"]["observations"]):
        for a,rows in report["portraits_by_original_alias"].items():
            for i,n in rows:
                assert prior[int(a)].setdefault(i,n)==n
        for i,r in report["observed_blocks"].items():
            if r["status"]=="DUAL_DECODED_INDEX_PIXELS":
                assert prior_pixels.setdefault(int(i),r)==r
    assert len(prior)==207
    ep=read(prev.EXTRA["tw10_receipt"][0])
    g=next(x for x in ep["groups"] if x["group_index"]==363)
    assert (g["graphic"],g["segment_sha256"],g["source_sequences"],g["frame_positions"],g["distinct_bitmaps"])==(100400,"8bb05bf8e3ef1e557ed0eceac19111bbd2b99c77f8e2ab6b84e477164c558f5c",104,352,344)
    for path in (PINS["groups"][0],prev.EXTRA["tw10_groups"][0]):
        row=next(r for r in gzrows(path) if int(r["index"])==363)
        assert (int(row["spr_no"]),row["segment_sha256"],int(row["anim_count"]))==(100400,g["segment_sha256"],104)
    group={363:dict(graphic=100400,animation_headers=104)}
    seq=prev.sequence_tables(group,prev.EXTRA["tw85_animation"][0],PINS["frames"][0])
    early=prev.sequence_tables(group,prev.EXTRA["tw10_animations"][0],prev.EXTRA["tw10_frames"][0])
    assert seq==early
    frames=[f[0] for a in seq[363].values() for f in a["frames"]]
    assert len(frames)==352 and None not in frames and len(set(frames))==344
    early_rows={}
    for r in gzrows(prev.EXTRA["tw10_adrn"][0]):
        n=int(r["bitmapno"])
        if n in frames:
            assert n not in early_rows
            early_rows[n]=dict(rd_sha256=r["rd_block_sha256"],size=int(r["size"]),width=int(r["width"]),height=int(r["height"]),strict=n not in ep["bounded_bitmaps"])
    assert set(early_rows)==set(frames)
    # Earlier actual same-carrier pixel receipts, usable only with exact row/hash/geometry.
    for path in (bulk.RECEIPT,pet71.RECEIPT):
        report=json.loads(gzip.decompress(path.read_bytes()))
        for b in report["observations"].values():
            status=b.get("strict",b)
            if status["status"]!="DUAL_DECODED_INDEX_PIXELS":continue
            i=b["index"];r={k:b[k] for k in ("bitmap","adrn_sha256","rd_sha256","width","height")}
            r.update(status="DUAL_DECODED_INDEX_PIXELS",index_pixels_sha256=status["index_pixels_sha256"])
            if i in prior_pixels:
                assert all(prior_pixels[i][k]==v for k,v in r.items())
            else:prior_pixels[i]=r
        del report
    return positions,prior,prior_pixels,g,seq[363],early_rows

def source(directory,acquisition,plan_data):
    positions,prior,prior_pixels,g,seq,early=plan_data
    assert bulk.summarize_carrier(acquisition)==bulk.summarize_carrier(bulk.load(bulk.CARRIER))
    bulk.pix.qualify_pair(directory)
    for name in ("adrn_158.bin","real_158.bin"):
        bulk.pix.original_check(directory/name,bulk.pix.SOURCE_FILES[name])
    with tempfile.TemporaryDirectory() as tmp:
        ps=[Path(tmp)/k for k in ("group","animation","frame")]
        bulk.pix.export_cn50_spr(directory/"spradrn_137.bin",directory/"spr_137.bin",*ps)
        for p,r in zip(ps,(PINS["groups"][0],prev.EXTRA["tw85_animation"][0],PINS["frames"][0]),strict=True):
            assert p.read_bytes()==r.read_bytes()
    adrn=(directory/"adrn_158.bin").read_bytes()
    aliases={a:[] for a in positions}
    for i,(n,*_,a) in enumerate(bulk.pix.COLS.iter_unpack(adrn)):
        if a in aliases:aliases[a].append([i,n])
    for a,rows in prior.items():assert aliases[a]==[[i,n] for i,n in sorted(rows.items())]
    want={i for rows in aliases.values() for i,n in rows}
    native={};frame_indices=defaultdict(list)
    for r in gzrows(PINS["native"][0]):
        i,n=int(r["index"]),int(r["bitmapno"])
        if i not in want and n not in early:continue
        native[i]=dict(index=i,bitmap=n,offset=int(r["adder"]),size=int(r["size"]),width=int(r["width"]),height=int(r["height"]),adrn_sha256=r["record_sha256"],rd_sha256=r["rd_sha256"])
        if n in early:frame_indices[n].append(i)
    assert set(frame_indices)==set(early) and all(len(v)==1 for v in frame_indices.values())
    assert set(native)==want|{v[0] for v in frame_indices.values()}
    alias_set={i for rows in aliases.values() for i,n in rows}
    obs={};cache={}
    with (directory/"real_158.bin").open("rb") as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as real:
        for i,r in sorted(native.items(),key=lambda p:p[1]["offset"]):
            raw=adrn[i*80:(i+1)*80];n,off,size,_,_,w,h,a=bulk.pix.COLS.unpack(raw)
            assert (n,off,size,w,h,bulk.sha(raw))==(r["bitmap"],r["offset"],r["size"],r["width"],r["height"],r["adrn_sha256"])
            assert 0<=off and 16<=size<=len(real)-off
            block=real[off:off+size];assert bulk.sha(block)==r["rd_sha256"]
            p=prior_pixels.get(i)
            if p is not None:
                assert all(r[k]==p[k] for k in ("bitmap","adrn_sha256","rd_sha256","width","height"))
                result=dict(grade=pet71.STRICT,method="PRIOR_DIRECT_EXACT_ROW",pixel_sha256=p["index_pixels_sha256"],diagnostic=None)
            elif i not in alias_set and n in early and early[n]["strict"] and key(r)==key(early[n]):
                result=dict(grade=pet71.STRICT,method="TW10_EXACT_STRICT_SCOPE",pixel_sha256=None,diagnostic=None)
            else:
                k=key(r)
                if k not in cache:cache[k]=pet71.diagnose(block,w,h)
                q=cache[k];pixel=q["strict"]["index_pixels_sha256"] if q["grade"]==pet71.STRICT else q["boundary"]["canvas_prefix_sha256"] if q["grade"]==pet71.BOUNDED else None
                result=dict(grade=q["grade"],method="ACTUAL_ORIGINAL_DUAL_DECODE",pixel_sha256=pixel,diagnostic=q)
            obs[str(i)]=dict(**r,alias=a,**result)
    palettes=[]
    for q in read(PAL)["original_palette_pairs_exact"]:
        p=directory/"pal"/Path(q["tw85_path"]).name
        raw=p.read_bytes()
        assert len(raw)==q["size"] and bulk.sha(raw)==q["sha256"]
        palettes.append(q)
    assert len(palettes)==16
    return dict(schema="stoneage.pet73.original_portrait_residual.r1",carrier=bulk.summarize_carrier(acquisition),source_files=pet71.files(),aliases=aliases,frame_indices=frame_indices,
        observations=obs,palette_file_receipts=palettes,original_runtime_verified=False,official_identity_verified=False,original_assets_published=False)
def verify(report,plan_data):
    positions,prior,prior_pixels,g,seq,early=plan_data
    assert report["schema"]=="stoneage.pet73.original_portrait_residual.r1"
    assert report["carrier"]==bulk.summarize_carrier(bulk.load(bulk.CARRIER)) and report["source_files"]==pet71.files()
    assert not any(report[k] for k in ("original_runtime_verified","official_identity_verified","original_assets_published"))
    aliases={int(a):v for a,v in report["aliases"].items()};fi={int(a):v for a,v in report["frame_indices"].items()}
    assert aliases.keys()==positions.keys() and fi.keys()==early.keys() and all(len(v)==1 for v in fi.values())
    for a,rows in prior.items():assert aliases[a]==[[i,n] for i,n in sorted(rows.items())]
    want={i for rows in aliases.values() for i,n in rows}
    selected=want|{v[0] for v in fi.values()};obs={int(i):r for i,r in report["observations"].items()}
    assert obs.keys()==selected
    # Replay every selected original metadata row, and independently check all prior patch alias candidates.
    patch={}
    for r in gzrows(PINS["patch"][0]):
        a=int(r["map_number"])
        if a in aliases:patch[int(r["index"])]=(a,r["record_sha256"])
    for r in gzrows(PINS["pairs"][0]):
        i=int(r["patch_index"])
        if i not in patch:continue
        a,h=patch[i];assert r["patch_record_sha256"]==h
        for v in r["native_exact_indices"].split(","):
            if v:assert [int(v),int(r["bitmapno"])] in aliases[a]
    seen=set()
    for r in gzrows(PINS["native"][0]):
        i,n=int(r["index"]),int(r["bitmapno"])
        if n in fi:assert i in fi[n]
        if i not in obs:continue
        seen.add(i);b=obs[i]
        assert (n,int(r["adder"]),int(r["size"]),int(r["width"]),int(r["height"]),r["record_sha256"],r["rd_sha256"])==(b["bitmap"],b["offset"],b["size"],b["width"],b["height"],b["adrn_sha256"],b["rd_sha256"])
        grade=b["grade"];method=b["method"];pixel=b["pixel_sha256"]
        if method=="PRIOR_DIRECT_EXACT_ROW":
            p=prior_pixels[i];assert all(b[k]==p[k] for k in ("bitmap","adrn_sha256","rd_sha256","width","height"))
            assert grade==pet71.STRICT and pixel==p["index_pixels_sha256"] and b["diagnostic"] is None
        elif method=="TW10_EXACT_STRICT_SCOPE":
            assert i not in want and early[n]["strict"] and key(b)==key(early[n])
            assert grade==pet71.STRICT and pixel is None and b["diagnostic"] is None
        else:
            assert method=="ACTUAL_ORIGINAL_DUAL_DECODE"
            q=b["diagnostic"];pet71.verify_result(dict(**{k:b[k] for k in ("width","height","size")},**q))
            assert grade==q["grade"]
            assert pixel==(q["strict"]["index_pixels_sha256"] if grade==pet71.STRICT else q["boundary"]["canvas_prefix_sha256"] if grade==pet71.BOUNDED else None)
    assert seen==selected
    ac=Counter();pc=Counter()
    for a,rows in aliases.items():
        assert rows==sorted(rows) and len({i for i,n in rows})==len(rows)
        for i,n in rows:assert (obs[i]["alias"],obs[i]["bitmap"])==(a,n)
        s="NO_NATIVE_ALIAS" if not rows else "ALL_STRICT" if all(obs[i]["grade"]==pet71.STRICT for i,n in rows) else "ALL_CANVAS" if all(obs[i]["grade"] in (pet71.STRICT,pet71.BOUNDED) for i,n in rows) else "UNRESOLVED_CANDIDATE"
        ac[s]+=1;pc[s]+=len(positions[a])
    for i,b in obs.items():
        if b["alias"] in aliases:assert [i,b["bitmap"]] in aliases[b["alias"]]
    gc=Counter(obs[v[0]]["grade"] for v in fi.values())
    assert sum(gc.values())==344 and sum(ac.values())==508 and sum(pc.values())==1889
    assert report["palette_file_receipts"]==read(PAL)["original_palette_pairs_exact"]
    return dict(schema="stoneage.pet73.portrait_residual_summary.r1",receipt_sha256=bulk.sha(bulk.stable(report)),alias_status=dict(ac),position_status=dict(pc),native_portrait_rows=len(want),prior_direct_aliases=len(prior),
        group_graphic=100400,group_index=363,group_sequence_count=104,group_frame_positions=352,group_bitmap_status=dict(gc),
        group_exact_tw10_rd=sum(key(obs[v[0]])==key(early[n]) for n,v in fi.items()),
        methods=dict(Counter(b["method"] for b in obs.values())),same_carrier_palette_files=16,original_runtime_verified=False,official_species_count=None)
def main():
    p=argparse.ArgumentParser();p.add_argument("--source-dir",type=Path);p.add_argument("--acquisition",type=Path);p.add_argument("--plan-only",action="store_true");a=p.parse_args()
    assert bool(a.source_dir)==bool(a.acquisition)
    data=plan()
    if a.plan_only:print("PET73_PLAN",len(data[0]),len(data[-1]),flush=True);return
    if a.source_dir:
        r=source(a.source_dir,read(a.acquisition),data);s=verify(r,data)
        RECEIPT.write_bytes(bulk.stable(r));SUMMARY.write_bytes(bulk.stable(s))
    else:
        r=read(RECEIPT);s=verify(r,data);assert SUMMARY.read_bytes()==bulk.stable(s)
    print("PET73_SUMMARY="+json.dumps(s,sort_keys=True,separators=(",",":")),flush=True)
if __name__=="__main__":main()
