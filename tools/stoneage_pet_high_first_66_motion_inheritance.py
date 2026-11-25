"""PET66: target SPR sequences and exact complete RD pixel-evidence inheritance."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
from tools.stoneage_pet_high_first_57_coverage import PINS, ROOT, blob, gzrows
from tools.stoneage_pet_high_first_65_full_visual import read as read65
R=ROOT/"research/recovered"
P=ROOT/"research/pets"
EXTRA={
 "tw10_receipt":(R/"STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json","e1cac6980353d09353de43fec0948bfcd84d49e6"),
 "tw10_manifest":(R/"tw10-resource-metadata/MANIFEST-R1.txt","6154dcf806163b82cb96af344e6a644143d15f56"),
 "tw10_groups":(R/"tw10-resource-metadata/SPR-GROUP-R1.tsv.gz","5ec65f043848fb3260bc04c94847b45fb1706d36"),
 "tw10_animations":(R/"tw10-resource-metadata/SPR-ANIMATION-R1.tsv.gz","90b19256f465effa6a8b6964a3777f7b31e3004c"),
 "tw10_frames":(R/"tw10-resource-metadata/SPR-FRAME-R1.tsv.gz","ec374e9ab30c54d29de453c51f30fa1fb0df1fd1"),
 "tw10_adrn":(R/"tw10-resource-metadata/ADRN-R1.tsv.gz","e389540f9962d1868c42b1edfe2acc7c83387ff1"),
 "tw85_animation":(R/"tw85-spr137-r28/SPR-ANIMATION-R28.tsv.gz","240a4d034842f7732261d88109e8534cae018822"),
 "tw85_bindings":(R/"tw85-frame-bitmap-r29/BITMAP-BINDINGS-R29.tsv.gz","fd024d9b30ed478ece7810a0207b157fd627a629"),
 "pet65_summary":(P/"PET-HIGH-FIRST-65-FULL-VISUAL-SUMMARY-R1.json","22e6932d280b6ac2d6ea7610b04ddafd066c7cd3"),
}
def sha(b):return hashlib.sha256(b).hexdigest()
def read_extra():
    d={}
    for k,(p,h) in EXTRA.items():
        b=p.read_bytes()
        assert blob(b)==h,k
        if p.suffix==".json":d[k]=json.loads(b)
        elif p.suffix==".txt":d[k]=b.decode()
    return d
def sequence_tables(groups, animation_path, frame_path):
    seq=defaultdict(dict)
    for a in gzrows(animation_path):
        i=int(a["group_index"])
        if i not in groups:continue
        assert int(a["spr_no"])==groups[i]["graphic"]
        j=int(a["anim_index"])
        assert j==len(seq[i])
        seq[i][j]=dict(direction=int(a["direction"]),action=int(a["anim_no"]),duration=int(a["duration"]),count=int(a["frame_count"]),frames=[])
    for f in gzrows(frame_path):
        i=int(f["group_index"])
        if i not in groups:continue
        a=seq[i][int(f["anim_index"])]
        assert int(f["frame_index"])==len(a["frames"])
        a["frames"].append([None if f["sentinel"]=="1" else int(f["bmp_no"]),int(f["pos_x"]),int(f["pos_y"]),int(f["sound_no"])])
    for i,g in groups.items():
        assert len(seq[i])==g["animation_headers"]
        assert all(len(a["frames"])==a["count"] for a in seq[i].values())
    return seq
def derive():
    x=read_extra();d=read65()
    prior=x["pet65_summary"]["summary"]
    wanted={r["graphic"] for r in d["master"]["pet_flag_1_field_projections"]}
    groups={}
    for i,(g,m) in enumerate(zip(gzrows(PINS["groups"][0]),gzrows(PINS["material"][0]),strict=True)):
        assert int(g["index"])==int(m["group_index"])==i and g["spr_no"]==m["spr_no"]
        spr=int(g["spr_no"])
        if spr in wanted:
            groups[i]=dict(graphic=spr,sha256=g["segment_sha256"],animation_headers=int(g["anim_count"]),mapped_frames=int(m["mapped_frames"]),sentinel_frames=int(m["sentinel_frames"]),missing_frames=int(m["missing_frames"]))
    assert len(groups)==prior["master_unique_group_count"]==427
    assert {g["graphic"] for g in groups.values()}==wanted and all(not g["missing_frames"] for g in groups.values())
    seq=sequence_tables(groups,EXTRA["tw85_animation"][0],PINS["frames"][0])
    target_numbers={f[0] for ss in seq.values() for a in ss.values() for f in a["frames"] if f[0] is not None}
    bindings={}
    for b in gzrows(EXTRA["tw85_bindings"][0]):
        n=int(b["bitmapno"])
        if n not in target_numbers:continue
        assert n not in bindings and int(b["native_candidates"])==1,b
        index=int(b["native_indices"]);size,digest=b["complete_rd_content_keys"].split(":")
        assert int(size)==int(b["sizes"]) and len(digest)==64
        bindings[n]=dict(index=index,rd_sha256=digest,size=int(size),width=int(b["widths"]),height=int(b["heights"]))
    assert bindings.keys()==target_numbers
    def key(b):return (b["rd_sha256"],b["size"],b["width"],b["height"])
    # Earlier source receipt covers all selected strict TW10 bitmaps except the
    # explicitly bounded list. Rebuild exact group membership from pinned tables,
    # tie their source members to manifest, and retain aggregate evidence grade.
    p=x["tw10_receipt"];m=x["tw10_manifest"]
    assert not p["unrendered_bitmaps"] and p["source_bitmap_statuses"]=={"strict":32150,"terminal_zero_outside_canvas":5}
    for name,(size,digest) in p["source_members"].items():
        if name!="Palet_1.sap":
            assert f"SOURCE|name={name}|bytes={size}|sha256={digest}" in m
    for k in ("tw10_groups","tw10_animations","tw10_frames","tw10_adrn"):
        path=EXTRA[k][0];raw=path.read_bytes()
        assert f"DATASET|name={path.name}|bytes={len(raw)}|sha256={sha(raw)}" in m
    early={g["group_index"]:g for g in p["groups"]}
    assert len(early)==131
    for row in gzrows(EXTRA["tw10_groups"][0]):
        i=int(row["index"])
        if i in early:
            g=early[i]
            assert (int(row["spr_no"]),row["segment_sha256"],int(row["anim_count"]))==(g["graphic"],g["segment_sha256"],g["source_sequences"])
    early_seq=sequence_tables({i:dict(graphic=g["graphic"],animation_headers=g["source_sequences"]) for i,g in early.items()},EXTRA["tw10_animations"][0],EXTRA["tw10_frames"][0])
    early_numbers=set()
    for i,g in early.items():
        frames=[f[0] for a in early_seq[i].values() for f in a["frames"]]
        assert None not in frames and len(frames)==g["frame_positions"] and len(set(frames))==g["distinct_bitmaps"]
        early_numbers.update(frames)
    assert len(early_numbers)==32155 and sum(g["frame_positions"] for g in early.values())==73500
    bounded=set(p["bounded_bitmaps"]);assert bounded<=early_numbers and len(bounded)==5
    early_strict=early_numbers-bounded
    early_keys=defaultdict(list);early_seen=set()
    for r in gzrows(EXTRA["tw10_adrn"][0]):
        n=int(r["bitmapno"])
        if n in early_numbers:
            assert n not in early_seen
            early_seen.add(n)
            if n in early_strict:
                early_keys[(r["rd_block_sha256"],int(r["size"]),int(r["width"]),int(r["height"]))].append(n)
    assert early_seen==early_numbers
    # Independently retained per-block indexed-pixel receipts for CN50 and TW85.
    cn_keys=defaultdict(list)
    for n,b in d["cn_pixels"]["cn50_observed_blocks"].items():
        assert len(b["index_pixels_sha256"])==64
        cn_keys[(b["rd_sha256"],b["rd_bytes"],b["width"],b["height"])].append(int(n))
    assert len(d["cn_pixels"]["cn50_observed_blocks"])==1536
    tw_observed={}
    receipts=[d["tw_pixels"],d["tw_long"]["observations"],d["tw60"]["observations"]]
    assert all(r["source_files"]==receipts[0]["source_files"] for r in receipts)
    for report in receipts:
        for i,b in report["observed_blocks"].items():
            if b["status"]!="DUAL_DECODED_INDEX_PIXELS":continue
            i=int(i)
            if i in tw_observed:assert tw_observed[i]==b
            tw_observed[i]=b
    # For each target frame, exact size/hash/geometry required. TW85 direct
    # grade requires exact native index/bitmap and original RD hash.
    evidence={}
    for n,b in bindings.items():
        t=tw_observed.get(b["index"])
        direct=bool(t and (t["bitmap"],t["rd_sha256"],t["width"],t["height"])==(n,b["rd_sha256"],b["width"],b["height"]))
        c=cn_keys.get(key(b),[])
        e=early_keys.get(key(b),[])
        grade="TW85_DIRECT" if direct else "CN50_EXACT_RD" if c else "TW10_STRICT_SCOPE_EXACT_RD" if e else "NO_STRICT_PIXEL_RECEIPT"
        evidence[n]=dict(grade=grade,tw85_direct=direct,cn50_bitmaps=c,tw10_strict_bitmaps=e,**b)
    out=[];sequence_counts=Counter();frame_counts=Counter();group_counts=Counter()
    early_ident={(g["graphic"],g["segment_sha256"]):i for i,g in early.items()}
    for i,g in sorted(groups.items()):
        entries=[];gc=Counter()
        old=early_ident.get((g["graphic"],g["sha256"]))
        if old is not None:assert seq[i]==early_seq[old]
        for j,a in seq[i].items():
            numbers=[f[0] for f in a["frames"] if f[0] is not None]
            count=Counter(evidence[n]["grade"] for n in numbers)
            gc.update(count);frame_counts.update(count)
            if not numbers:status="SENTINEL_ONLY"
            elif count["NO_STRICT_PIXEL_RECEIPT"]:status="INCOMPLETE"
            elif count["TW85_DIRECT"]==len(numbers):status="COMPLETE_TW85_DIRECT"
            else:status="COMPLETE_EXACT_RD_INHERITANCE"
            sequence_counts[status]+=1
            entries.append(dict(animation=j,direction=a["direction"],action=a["action"],duration=a["duration"],status=status,non_sentinel_frames=len(numbers),grades=dict(count),missing_bitmaps=sorted({n for n in numbers if evidence[n]["grade"]=="NO_STRICT_PIXEL_RECEIPT"})))
        assert sum(gc.values())==g["mapped_frames"]
        nonempty=[a for a in entries if a["status"]!="SENTINEL_ONLY"]
        complete=[a for a in nonempty if a["status"].startswith("COMPLETE_")]
        if nonempty and len(complete)==len(nonempty):status="ALL_NONEMPTY_SEQUENCES_COMPLETE"
        elif complete:status="SOME_SEQUENCES_COMPLETE"
        else:status="NO_COMPLETE_NONEMPTY_SEQUENCE"
        group_counts[status]+=1
        out.append(dict(group_index=i,**g,exact_tw10_spr_group_index=old,status=status,complete_sequences=len(complete),sequence_count=len(entries),grades=dict(gc),sequences=entries))
    assert sum(frame_counts.values())==sum(g["mapped_frames"] for g in groups.values())
    assert sum(sequence_counts.values())==sum(g["animation_headers"] for g in groups.values())
    per_graphic=defaultdict(list)
    for row in out:per_graphic[row["graphic"]].append(row)
    templates=[]
    for pos,m in enumerate(d["master"]["pet_flag_1_field_projections"]):
        gg=per_graphic[m["graphic"]]
        templates.append(dict(position=pos,template_id=m["template_id"],name=m["name"],row_sha256=m["row_sha256"],graphic=m["graphic"],groups=[g["group_index"] for g in gg],all_groups_complete=all(g["status"]=="ALL_NONEMPTY_SEQUENCES_COMPLETE" for g in gg),any_complete_sequence=any(g["complete_sequences"] for g in gg)))
    assert len(templates)==467
    # Every absent pixel is a source-read task, not a missing source bitmap.
    missing={n for n,b in evidence.items() if b["grade"]=="NO_STRICT_PIXEL_RECEIPT"}
    summary=dict(physical_groups=len(out),template_positions=len(templates),distinct_graphics=len(wanted),
        group_status=dict(group_counts),sequence_status=dict(sequence_counts),frame_evidence=dict(frame_counts),
        distinct_frame_bitmaps=len(evidence),distinct_bitmap_grades=dict(Counter(b["grade"] for b in evidence.values())),
        groups_with_exact_tw10_spr=sum(g["exact_tw10_spr_group_index"] is not None for g in out),
        positions_with_any_complete_sequence=sum(t["any_complete_sequence"] for t in templates),
        positions_with_all_groups_complete=sum(t["all_groups_complete"] for t in templates),
        groups_without_complete_sequence=[g["group_index"] for g in out if g["status"]=="NO_COMPLETE_NONEMPTY_SEQUENCE"],
        groups_with_missing_strict_pixels=sum(bool(g["grades"].get("NO_STRICT_PIXEL_RECEIPT")) for g in out),
        missing_strict_pixel_bitmaps=len(missing),official_species_count=None,official_acquisition_closures=0)
    return dict(schema="stoneage.pet66.motion_inheritance.r1",summary=summary,groups=out,templates=templates,bitmap_evidence=evidence,
        pins={k:dict(path=str(p.relative_to(ROOT)),git_blob=h) for k,(p,h) in EXTRA.items()},
        boundaries=["TW10 strict scope reconstructed from pinned aggregate receipt and original metadata, not re-read individual pixel hashes","CN50 individual per-block exact RD and pixel digest","TW85 source-local exact native bitmap reference","Complete source index sequences not native palette, timing, renderer, or live pet identity"],
        original_assets_published=False,new_original_bytes_reacquired=False,runtime_executed=False)
def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument("--output",type=Path);args=a.parse_args()
    report=derive()
    if args.output:args.output.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8")
    snapshot=json.loads((ROOT/"research/pets/PET-HIGH-FIRST-66-MOTION-INHERITANCE-SUMMARY-R1.json").read_bytes())
    assert snapshot["summary"]==report["summary"], "coverage summary differs from fixed replay"
    print("PET66_SUMMARY="+json.dumps(report["summary"],sort_keys=True,separators=(",",":")))
if __name__=="__main__":main()
