"""PET74: compact query projection of accepted, source-separated PET69–73 evidence."""
import argparse
from collections import Counter, defaultdict
import gzip
import json
from tools import stoneage_pet_high_first_69_full_native_routes as routes
from tools import stoneage_pet_high_first_71_bulk_named_pixels as motion
from tools import stoneage_pet_high_first_73_portrait_residual as portrait
from tools import stoneage_pet_high_first_67_bulk_pixels as bulk
from tools import stoneage_pet_high_first_68_rd_boundary as boundary
from tools.stoneage_pet_high_first_57_coverage import ROOT, PINS, blob
from tools import stoneage_pet_source_lookup as lookup

P=ROOT/"research/pets"
OUT=P/"PET-HIGH-FIRST-74-UNIFIED-VISUAL-R1.json"
MANIFEST=ROOT/lookup.MANIFEST
PINS74={
 "route":(P/"PET-HIGH-FIRST-69-FULL-NATIVE-ROUTES-SUMMARY-R1.json","21c7b89dda7997bab464de97804e4c8ab3b03175"),
 "motion":(motion.SUMMARY,"c55a2c74e03ca8af7d41b5888b290106ffe260c3"),
 "motion_raw":(motion.RECEIPT,"157cdf72e74ecb328a15e16771cb36e18735ca08"),
 "geometry":(P/"PET-HIGH-FIRST-72-GEOMETRY-RESIDUAL-SUMMARY-R1.json","c329ba84c0b7cc50a6284fdcdd7e858d156e3b5e"),
 "portrait":(portrait.RECEIPT,"cc1548a2292b782e071e7e1109d67cee1fb3209c"),
 "portrait_summary":(portrait.SUMMARY,"5b91790a0c3c2c893929dac70f1a347ba2decb7f"),
 "boundary":(boundary.RECEIPT,"3648e9b85a85cdb95b6c5207c548de8ecf177d5a"),
 "boundary_summary":(boundary.SUMMARY,"bf296c3bcf07b4992e3af34c69f5dc9e7f808127"),
}
def stable(x):
    return (json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()

def group_motion(sequences, grade):
    frame_grades = Counter()
    sequence_status = Counter()
    for sequence in sequences.values():
        counts = Counter(grade(frame[0]) for frame in sequence["frames"] if frame[0] is not None)
        frame_grades.update(counts)
        if not counts:
            state = "SENTINEL_ONLY"
        elif counts.keys() - {motion.STRICT, motion.BOUNDED}:
            state = "INCOMPLETE"
        else:
            state = "BOUNDED_COMPLETE" if counts[motion.BOUNDED] else "STRICT_COMPLETE"
        sequence_status[state] += 1

    complete = sequence_status["STRICT_COMPLETE"] + sequence_status["BOUNDED_COMPLETE"]
    nonempty = sum(sequence_status.values()) - sequence_status["SENTINEL_ONLY"]
    if not nonempty:
        status = "NO_NONEMPTY_SEQUENCES"
    elif complete == nonempty:
        status = "BOUNDED_COMPLETE" if frame_grades[motion.BOUNDED] else "STRICT_COMPLETE"
    else:
        status = "PARTIAL" if complete else "NO_COMPLETE_SEQUENCE"
    return status, frame_grades, sequence_status

def derive():
    for p,h in PINS74.values():assert blob(p.read_bytes())==h,p
    r=routes.derive()
    assert r["summary"]==json.loads(PINS74["route"][0].read_bytes())["summary"]
    old,targets=motion.plan()
    receipt=json.loads(gzip.decompress(motion.RECEIPT.read_bytes()))
    ms=motion.verify(receipt,old,targets)
    assert ms==json.loads(motion.SUMMARY.read_bytes())
    grades={n:x["grade"] for n,x in old["bitmap_evidence"].items()}
    grades.update({x["bitmap"]:x["grade"] for x in receipt["observations"].values()})
    named={g["group_index"]:g for g in old["groups"]}
    del receipt,targets
    seq=motion.prev.sequence_tables(named,motion.prev.EXTRA["tw85_animation"][0],PINS["frames"][0])
    geo=json.loads(PINS74["geometry"][0].read_bytes())
    geoid=defaultdict(list)
    for j,row in enumerate(geo["geometry_records"]):
        for f in row["frame_references"]:geoid[f["group_index"]].append(j)
    assert set(geoid)=={1369,1541}
    groups={};gc=Counter();sc=Counter();fc=Counter()
    for i,g in named.items():
        status, counts, states = group_motion(seq[i], grades.__getitem__)
        assert sum(counts.values())==g["mapped_frames"]+g["missing_frames"]
        gc[status]+=1;sc.update(states);fc.update(counts)
        groups[str(i)]=dict(graphic=g["graphic"],spr_sha256=g["spr_sha256"],scope="PET71_NAMED_FULL_MOTION",
            status=status,frame_grades=dict(counts),sequence_status=dict(states),geometry_indices=geoid[i])
    assert dict(gc)==ms["group_status"] and dict(sc)==ms["sequence_status"] and dict(fc)==ms["frame_status"]
    del seq,grades,old
    all_rows=[g for row in r["graphics"] for g in row["physical_groups"]]+r["outside_scope"]
    assert len(all_rows)==1739
    for g in all_rows:
        i=str(g["group_index"])
        if i in groups:continue
        status="PET68_EXISTING_CANVAS_SCOPE" if g["pet68_canvas_scope"] else "EARLIER_SELECTED_EXACT_SPR_AND_RD" if i=="363" else "NO_POSITIVE_PET_LINK_IN_COMPARED_SOURCES"
        groups[i]=dict(graphic=g["graphic"],spr_sha256=g["spr_sha256"],scope="PET72_RESIDUAL_SCREEN",status=status,
            geometry_indices=[])
    assert Counter(g["status"] for g in groups.values() if g["scope"]=="PET72_RESIDUAL_SCREEN")=={
        "PET68_EXISTING_CANVAS_SCOPE":6,"EARLIER_SELECTED_EXACT_SPR_AND_RD":1,"NO_POSITIVE_PET_LINK_IN_COMPARED_SOURCES":415}

    # Six of the PET68-covered groups have no named TW85 album route. Preserve
    # their verified per-group grades even though PET71 did not assess them.
    covered = {g["group_index"]: g for g in all_rows if g["pet68_canvas_scope"] and g["group_index"] not in named}
    boundary_receipt = json.loads(boundary.RECEIPT.read_bytes())
    boundary_summary = json.loads(boundary.SUMMARY.read_bytes())
    assert bulk.sha(stable(boundary_receipt)) == boundary_summary["source_receipt_sha256"]
    bounded = {
        int(n) for n, row in boundary_receipt["observations"].items()
        if row["status"] == boundary.BOUND
    }
    assert len(bounded) == boundary_summary["qualified_canvas_bitmaps"] == 68
    assert boundary_summary["canvas_unresolved_bitmaps"] == 0
    sequences = motion.prev.sequence_tables(covered, motion.prev.EXTRA["tw85_animation"][0], PINS["frames"][0])

    def grade_boundary(bitmap):
        return motion.BOUNDED if bitmap in bounded else motion.STRICT

    for index, group in covered.items():
        sequence_table = sequences[index]
        status, counts, states = group_motion(sequence_table, grade_boundary)
        bitmap_ids = {frame[0] for sequence in sequence_table.values() for frame in sequence["frames"]}
        assert status in ("STRICT_COMPLETE", "BOUNDED_COMPLETE")
        assert group["missing_frames"] == 0 and sum(counts.values()) == group["mapped_frames"]
        groups[str(index)].update(
            scope="PET68_FULL_MOTION", status=status, frame_grades=dict(counts),
            sequence_status=dict(states), boundary_bitmaps=sorted(bitmap_ids & bounded),
        )

    pr=json.loads(portrait.RECEIPT.read_bytes());ps=json.loads(portrait.SUMMARY.read_bytes())
    assert bulk.sha(bulk.stable(pr))==ps["receipt_sha256"]
    assert ps["alias_status"]=={"ALL_STRICT":508} and ps["position_status"]=={"ALL_STRICT":1889}
    assert len(pr["palette_file_receipts"])==16 and ps["group_exact_tw10_rd"]==344
    assert groups["363"]["graphic"]==100400
    groups["363"].update(sequence_count=ps["group_sequence_count"],frame_positions=ps["group_frame_positions"],
        distinct_bitmaps=len(pr["frame_indices"]),strict_exact_rd_count=ps["group_exact_tw10_rd"])
    selector_groups = {g["group_index"] for row in r["graphics"] for g in row["physical_groups"]}
    graphics=defaultdict(list)
    for g in sorted(all_rows,key=lambda x:x["group_index"]):
        key=str(g["group_index"])
        assert (g["graphic"],g["spr_sha256"])==(groups[key]["graphic"],groups[key]["spr_sha256"])
        groups[key].update(animation_headers=g["animation_headers"],frame_occurrences=g["frame_occurrences"],
            mapped_frames=g["mapped_frames"],sentinel_frames=g["sentinel_frames"],missing_frames=g["missing_frames"],
            selector_scope="WITHIN_STATIC_INPUT_RANGE" if g["group_index"] in selector_groups else "OUTSIDE_STATIC_INPUT_RANGE")
        graphics[str(g["graphic"])].append(key)
    positions={};pc=Counter()
    for a in r["album_positions"]:
        p,s=a["program"],a["slot"];alias=str(a["portrait_alias"])
        candidates=pr["aliases"][alias]
        assert candidates and all(pr["observations"][str(i)]["grade"]==motion.STRICT for i,n in candidates)
        ids=[str(i) for i in a["physical_group_indices"]]
        assert ids and all(groups[i]["scope"]=="PET71_NAMED_FULL_MOTION" for i in ids)
        states=[groups[i]["status"] for i in ids]
        n=sum(s in ("STRICT_COMPLETE","BOUNDED_COMPLETE") for s in states)
        status="ALL_CANVAS_COMPLETE" if n==len(ids) else "SOME_CANVAS_COMPLETE" if n else "NO_COMPLETE_GROUP"
        pc[status]+=1
        positions[f"{p}:{s}"]=dict(program=p,slot=s,name=a["name"],row_sha256=a["row_sha256"],portrait_alias=int(alias),
            portrait_rows=[i for i,n in candidates],portrait_status="ALL_STRICT",group_ids=ids,
            graphics=a["early_graphics"]+a["high_graphics"],motion_status=status)
    assert len(positions)==1889 and dict(pc)==ms["position_status"]
    assert len({i for a in positions.values() for i in a["portrait_rows"]})==512
    assert all(not pr[k] for k in ("official_identity_verified","original_runtime_verified","original_assets_published"))
    master_groups = [groups[str(g["group_index"])] for g in all_rows if g["pet68_canvas_scope"]]
    assert Counter(g["status"] for g in master_groups) == {"STRICT_COMPLETE": 392, "BOUNDED_COMPLETE": 35}
    return dict(schema="stoneage.pet74.unified_visual_projection.r1",
        source_pins={str(p.relative_to(ROOT)):h for p,h in PINS74.values()},
        positions=positions,groups=groups,graphics=dict(graphics),summary=dict(
            named_positions=1889,strict_portrait_aliases=508,physical_portrait_rows=512,
            position_motion_status=dict(pc),named_group_status=dict(gc),physical_groups=1739,
            residual_group_status=geo["summary"]["residual_status"],same_carrier_palette_files=16),
        official_species_count=None,official_identity_verified=False,original_runtime_verified=False,original_assets_published=False)
def manifest_entries():
    return {k:dict(path=str(p.relative_to(ROOT)),git_blob=h,expected_array=None,expected_rows=None)
        for k,(p,h) in {"hf74":(OUT,blob(OUT.read_bytes())),"hf73":PINS74["portrait"],"hf72":PINS74["geometry"],
                        "hf68_tw85_boundary":PINS74["boundary"]}.items()}
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--generate",action="store_true");a=ap.parse_args()
    report=derive()
    if a.generate:
        OUT.write_bytes(stable(report))
        m=json.loads(MANIFEST.read_bytes())
        m["sources"].update(manifest_entries())
        m["supplement_hf74"]=dict(source_head="68f6f7548fc9fcfc57e35c0a4d8a0996d13959a8",source_tree="5d27797b0d74bb56bd56deea496f44fc063a81d9",
            scope="Existing lookup positions only; original visual evidence, not official species or runtime proof.")
        MANIFEST.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    else:
        assert OUT.read_bytes()==stable(report)
        m=json.loads(MANIFEST.read_bytes())
        assert all(m["sources"][k]==v for k,v in manifest_entries().items())
    m,d=lookup.load();entries=lookup.build(d);lookup.verify(m,d,entries)
    print("PET74_SUMMARY="+json.dumps(report["summary"],sort_keys=True,separators=(",",":")),flush=True)
if __name__=="__main__":main()
