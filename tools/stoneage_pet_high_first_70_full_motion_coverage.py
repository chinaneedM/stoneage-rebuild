"""PET70: complete named-route motion coverage, exact RD inheritance before new source reads."""
import argparse
from collections import Counter, defaultdict
import gzip
import json
from pathlib import Path
from tools import stoneage_pet_high_first_69_full_native_routes as routes
from tools import stoneage_pet_high_first_68_rd_boundary as boundary
from tools import stoneage_pet_high_first_67_bulk_pixels as bulk
from tools import stoneage_pet_high_first_66_motion_inheritance as prev
from tools.stoneage_pet_high_first_65_full_visual import read as read65
from tools.stoneage_pet_high_first_57_coverage import ROOT,PINS,blob,gzrows

P=ROOT/"research/pets"
ROUTES=P/"PET-HIGH-FIRST-69-FULL-NATIVE-ROUTES-SUMMARY-R1.json"
PINS_EXTRA={ROUTES:"21c7b89dda7997bab464de97804e4c8ab3b03175",
    bulk.RECEIPT:"1801e69665de0d67ea7d15dce5396c267bb65374",
    bulk.SUMMARY:"0cc6e1b49b36efd65219b27a0d96108ad8041c89",
    boundary.RECEIPT:"3648e9b85a85cdb95b6c5207c548de8ecf177d5a",
    boundary.SUMMARY:"bf296c3bcf07b4992e3af34c69f5dc9e7f808127",
    **{PINS[k][0]:PINS[k][1] for k in ("frames","native","groups","material")},
    **{prev.EXTRA[k][0]:prev.EXTRA[k][1] for k in ("tw85_animation","tw85_bindings")}}
STRICT="STRICT_PIXEL_RECEIPT"
BOUNDED="BOUNDED_CANVAS_RECEIPT"
NEED="SOURCE_READ_REQUIRED"
MISSING="NO_ADRN_RECORD"
AMBIGUOUS="MULTIPLE_DIFFERENT_RD"
def key(row,size_key="size"):
    return row["rd_sha256"],int(row[size_key]),int(row["width"]),int(row["height"])
def digest(s):
    assert isinstance(s,str) and len(bytes.fromhex(s))==32
    return s

def derive():
    for p,h in PINS_EXTRA.items():assert blob(p.read_bytes())==h,p
    route=routes.derive()
    assert route["summary"]==bulk.load(ROUTES)["summary"]
    assert route["summary"]["position_status"]=={"NEW_EARLY_ROUTE":1204,"PRIOR_HIGH_ROUTE":685}
    old,old_native=bulk.plan()
    prior=json.loads(gzip.decompress(bulk.RECEIPT.read_bytes()))
    assert bulk.verify(prior,old,old_native)==bulk.load(bulk.SUMMARY)
    failures={b["bitmap"]:b for b in prior["observations"].values() if b["status"]!="DUAL_DECODED_INDEX_PIXELS"}
    assert len(failures)==68
    border=bulk.load(boundary.RECEIPT)
    assert boundary.verify(border,old,old_native,failures)==bulk.load(boundary.SUMMARY)
    assert all(x["status"]==boundary.BOUND for x in border["observations"].values())
    strict={};bounded={}
    # Keep one exact receipt per content key, with collision checks for actual pixel hashes.
    def add(k,source,ref,pixel=None):
        digest(k[0])
        if pixel is not None:digest(pixel)
        if k in bounded:raise AssertionError("strict/bounded key conflict")
        if k in strict:
            before=strict[k]
            if before["pixel_sha256"] is not None and pixel is not None:
                assert before["pixel_sha256"]==pixel
            if before["pixel_sha256"] is not None or pixel is None:return
        strict[k]=dict(source=source,ref=ref,pixel_sha256=pixel)
    # First restore direct bulk evidence, then older qualified receipts.
    for n,b in prior["observations"].items():
        k=key(b)
        if b["status"]=="DUAL_DECODED_INDEX_PIXELS":add(k,"PET67_TW85",int(n),b["index_pixels_sha256"])
    for n,b in border["observations"].items():
        k=key(b)
        assert k not in strict
        pixel=digest(b["canvas_prefix_sha256"])
        if k in bounded:assert bounded[k]["pixel_sha256"]==pixel
        else:bounded[k]=dict(source="PET68_TW85_BOUNDARY",ref=int(n),pixel_sha256=pixel)
    for n,b in old["bitmap_evidence"].items():
        if b["grade"]!="NO_STRICT_PIXEL_RECEIPT":
            add(key(b),"PET66_"+b["grade"],n)
    # Include the entire source-qualified earlier pool, not just PET66 intersections.
    d=read65();e=prev.read_extra()
    for n,b in d["cn_pixels"]["cn50_observed_blocks"].items():
        add(key(b,"rd_bytes"),"CN50_FULL_RD",int(n),b["index_pixels_sha256"])
    ep=e["tw10_receipt"];em=e["tw10_manifest"]
    assert ep["source_bitmap_statuses"]=={"strict":32150,"terminal_zero_outside_canvas":5} and not ep["unrendered_bitmaps"]
    for name,(size,h) in ep["source_members"].items():
        if name!="Palet_1.sap":assert f"SOURCE|name={name}|bytes={size}|sha256={h}" in em
    for k in ("tw10_groups","tw10_animations","tw10_frames","tw10_adrn"):
        p=prev.EXTRA[k][0];raw=p.read_bytes()
        assert f"DATASET|name={p.name}|bytes={len(raw)}|sha256={prev.sha(raw)}" in em
    eg={g["group_index"]:g for g in ep["groups"]}
    es=prev.sequence_tables({i:dict(graphic=g["graphic"],animation_headers=g["source_sequences"]) for i,g in eg.items()},prev.EXTRA["tw10_animations"][0],prev.EXTRA["tw10_frames"][0])
    en=set()
    for i,g in eg.items():
        fs=[f[0] for a in es[i].values() for f in a["frames"]]
        assert None not in fs and len(fs)==g["frame_positions"] and len(set(fs))==g["distinct_bitmaps"]
        en.update(fs)
    assert len(en)==32155
    eb=set(ep["bounded_bitmaps"]);assert len(eb)==5 and eb<=en
    early=en-eb;seen=set()
    for r in gzrows(prev.EXTRA["tw10_adrn"][0]):
        n=int(r["bitmapno"])
        if n in early:
            assert n not in seen;seen.add(n)
            k=(r["rd_block_sha256"],int(r["size"]),int(r["width"]),int(r["height"]))
            add(k,"TW10_FULL_STRICT_SCOPE",n)
    assert seen==early
    del es,en,early,seen
    # Older TW85 per-index receipts do not include size; bind the original native row.
    receipts=[d["tw_pixels"],d["tw_long"]["observations"],d["tw60"]["observations"]]
    assert all(r["source_files"]==receipts[0]["source_files"] for r in receipts)
    observed={}
    for report in receipts:
        for i,b in report["observed_blocks"].items():
            if b["status"]!="DUAL_DECODED_INDEX_PIXELS":continue
            i=int(i)
            if i in observed:assert observed[i]==b
            observed[i]=b
    # Exact physical groups selected by the full native album census.
    wanted={i for a in route["album_positions"] for i in a["physical_group_indices"]}
    groups={g["group_index"]:g for r in route["graphics"] for g in r["physical_groups"] if g["group_index"] in wanted}
    assert groups.keys()==wanted
    oldgroups={g["group_index"] for g in old["groups"]}
    assert len(oldgroups)==427
    seq=prev.sequence_tables(groups,prev.EXTRA["tw85_animation"][0],PINS["frames"][0])
    target={f[0] for ss in seq.values() for a in ss.values() for f in a["frames"] if f[0] is not None}
    bindings={}
    for r in gzrows(prev.EXTRA["tw85_bindings"][0]):
        n=int(r["bitmapno"])
        if n not in target:continue
        assert n not in bindings
        ids=[int(v) for v in r["native_indices"].split(",") if v]
        ks=[]
        for item,w,h,s in zip((v for v in r["complete_rd_content_keys"].split(",") if v),(v for v in r["widths"].split(",") if v),(v for v in r["heights"].split(",") if v),(v for v in r["sizes"].split(",") if v),strict=True):
            size,d=item.split(":");assert int(size)==int(s);digest(d)
            ks.append((d,int(size),int(w),int(h)))
        assert len(ids)==len(ks)==int(r["native_candidates"])
        assert len(ids)==len(set(ids))
        bindings[n]=dict(indices=ids,keys=ks,qualification=r["qualification"])
    assert bindings.keys()==target
    # Join selected original native records and preserve every ambiguous alternative.
    native_needed={i for b in bindings.values() for i in b["indices"]}
    all_needed=native_needed|set(observed)
    native={}
    for r in gzrows(PINS["native"][0]):
        i=int(r["index"])
        if i not in all_needed:continue
        assert i not in native
        row=dict(index=i,bitmap=int(r["bitmapno"]),offset=int(r["adder"]),size=int(r["size"]),width=int(r["width"]),height=int(r["height"]),adrn_sha256=r["record_sha256"],rd_sha256=r["rd_sha256"])
        native[i]=row
        if i in observed:
            b=observed[i]
            assert (row["bitmap"],row["adrn_sha256"],row["rd_sha256"],row["width"],row["height"])==(b["bitmap"],b["adrn_sha256"],b["rd_sha256"],b["width"],b["height"])
            add(key(row),"TW85_PRIOR_DIRECT",i,b["index_pixels_sha256"])
    assert native.keys()==all_needed
    evidence={};read_targets={}
    for n,b in bindings.items():
        rr=[native[i] for i in b["indices"]]
        ks=b["keys"]
        assert all(row["bitmap"]==n and key(row)==k for row,k in zip(rr,ks,strict=True))
        distinct=set(ks)
        if not ks:grade=MISSING;receipt=None
        elif len(distinct)!=1:grade=AMBIGUOUS;receipt=None
        else:
            k=ks[0]
            if k in strict:grade=STRICT;receipt=strict[k]
            elif k in bounded:grade=BOUNDED;receipt=bounded[k]
            else:
                grade=NEED;receipt=None
                # Only exact same-content multiple candidates may be grouped.
                for row in rr:read_targets[row["index"]]=row
        evidence[n]=dict(grade=grade,qualification=b["qualification"],native_indices=b["indices"],content_keys=ks,receipt=receipt)
    # Existing master coverage cannot regress within the enlarged scope.
    for n,b in old["bitmap_evidence"].items():
        if n in evidence:
            assert evidence[n]["grade"] in (STRICT,BOUNDED),n
    sc=Counter();gc=Counter();fc=Counter();group_results={};group_rows=[]
    for i,g in sorted(groups.items()):
        entries=[];counts=Counter()
        for j,a in seq[i].items():
            numbers=[f[0] for f in a["frames"] if f[0] is not None]
            c=Counter(evidence[n]["grade"] for n in numbers);counts.update(c);fc.update(c)
            if not numbers:s="SENTINEL_ONLY"
            elif c[NEED] or c[MISSING] or c[AMBIGUOUS]:s="INCOMPLETE"
            elif c[BOUNDED]:s="BOUNDED_COMPLETE"
            else:s="STRICT_COMPLETE"
            sc[s]+=1
            entries.append(dict(animation=j,direction=a["direction"],action=a["action"],duration=a["duration"],status=s,frame_grades=dict(c),
                unresolved_bitmaps=sorted({n for n in numbers if evidence[n]["grade"] not in (STRICT,BOUNDED)})))
        assert sum(counts.values())==g["mapped_frames"]+g["missing_frames"]
        assert sum(a["count"] for a in seq[i].values())==g["frame_occurrences"]
        assert len(entries)==g["animation_headers"]
        nonempty=[r for r in entries if r["status"]!="SENTINEL_ONLY"]
        complete=[r for r in nonempty if r["status"]!="INCOMPLETE"]
        if not nonempty:status="NO_NONEMPTY_SEQUENCES"
        elif len(complete)==len(nonempty):status="STRICT_COMPLETE" if not counts[BOUNDED] else "BOUNDED_COMPLETE"
        elif complete:status="PARTIAL"
        else:status="NO_COMPLETE_SEQUENCE"
        if i in oldgroups:assert status in ("STRICT_COMPLETE","BOUNDED_COMPLETE")
        gc[status]+=1;group_results[i]=status
        group_rows.append(dict(**g,status=status,frame_grades=dict(counts),sequences=entries))
    pc=Counter();pos=[]
    for a in route["album_positions"]:
        ss=[group_results[i] for i in a["physical_group_indices"]]
        assert ss
        status="ALL_CANVAS_COMPLETE" if all(s in ("STRICT_COMPLETE","BOUNDED_COMPLETE") for s in ss) else "SOME_CANVAS_COMPLETE" if any(s in ("STRICT_COMPLETE","BOUNDED_COMPLETE") for s in ss) else "NO_COMPLETE_GROUP"
        pc[status]+=1
        pos.append(dict(program=a["program"],slot=a["slot"],name=a["name"],group_indices=a["physical_group_indices"],status=status))
    bc=Counter(b["grade"] for b in evidence.values())
    assert sum(bc.values())==len(target) and sum(pc.values())==1889
    assert sum(gc.values())==len(wanted)
    assert sum(sc.values())==sum(g["animation_headers"] for g in groups.values())
    assert sum(fc.values())==sum(g["mapped_frames"]+g["missing_frames"] for g in groups.values())
    summary=dict(named_positions=1889,named_route_physical_groups=len(wanted),prior_pet68_groups_in_scope=len(wanted&oldgroups),
        expanded_groups=len(wanted-oldgroups),distinct_bitmaps=len(target),bitmap_status=dict(bc),frame_status=dict(fc),
        sequence_status=dict(sc),group_status=dict(gc),position_status=dict(pc),
        source_read_native_rows=len(read_targets),source_read_content_keys=len({key(x) for x in read_targets.values()}),
        reused_strict_keys=len(strict),reused_bounded_keys=len(bounded),
        official_species_count=None,official_acquisition_closures=0,original_runtime_verified=False)
    return dict(schema="stoneage.pet70.full_motion_coverage.r1",summary=summary,
        source_pins={str(p.relative_to(ROOT)):h for p,h in PINS_EXTRA.items()},
        groups=group_rows,album_positions=pos,bitmap_evidence=evidence,source_read_targets=read_targets,
        original_assets_published=False,original_runtime_verified=False)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--output",type=Path);a=p.parse_args()
    report=derive()
    if a.output:a.output.write_bytes(gzip.compress(bulk.stable(report),compresslevel=6,mtime=0))
    snapshot=json.loads((P/"PET-HIGH-FIRST-70-FULL-MOTION-COVERAGE-SUMMARY-R1.json").read_bytes())
    assert snapshot["summary"]==report["summary"], "fixed replay summary mismatch"
    print("PET70_SUMMARY="+json.dumps(report["summary"],sort_keys=True,separators=(",",":")),flush=True)
if __name__=="__main__":main()
