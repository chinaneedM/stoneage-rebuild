"""PET72: preserve two original geometry exceptions and source-screen residual groups."""
import argparse
from collections import Counter,defaultdict
import gzip
import json
from pathlib import Path
from tools import stoneage_pet_high_first_69_full_native_routes as routes
from tools import stoneage_pet_high_first_71_bulk_named_pixels as pet71
from tools import stoneage_pet_high_first_66_motion_inheritance as prev
from tools.stoneage_pet_high_first_57_coverage import ROOT,PINS,blob,gzrows

CN=ROOT/"research/recovered/cn50-resource-metadata/ADRN-R1.tsv.gz"
EXTRA={pet71.RECEIPT:"157cdf72e74ecb328a15e16771cb36e18735ca08",pet71.SUMMARY:"c55a2c74e03ca8af7d41b5888b290106ffe260c3",
    CN:"127670eaf2bc19ba9d15776d090a8307058f729d",
    **{PINS[k][0]:PINS[k][1] for k in ("native","frames","groups","material","master","retention","cn50")},
    **{prev.EXTRA[k][0]:prev.EXTRA[k][1] for k in ("tw85_animation","tw10_adrn","tw10_groups","tw10_receipt")}}
def read(p):return json.loads(p.read_bytes())
def derive():
    for p,h in EXTRA.items():assert blob(p.read_bytes())==h,p
    summary=read(pet71.SUMMARY)
    failures={x["index"]:x for x in summary["unresolved_rows"]}
    assert set(failures)=={322863,344133}
    report=json.loads(gzip.decompress(pet71.RECEIPT.read_bytes()))
    assert pet71.bulk.sha(pet71.bulk.stable(report))==summary["source_receipt_sha256"]
    obs={i:report["observations"][str(i)] for i in failures}
    del report
    native={}
    for r in gzrows(PINS["native"][0]):
        i=int(r["index"])
        if i not in failures:continue
        b=obs[i];f=failures[i]
        assert (int(r["bitmapno"]),int(r["size"]),int(r["width"]),int(r["height"]),r["rd_sha256"],r["record_sha256"])==(b["bitmap"],b["size"],b["width"],b["height"],b["rd_sha256"],b["adrn_sha256"])
        assert b["rd_sha256"]==f["rd_sha256"] and b["strict"]==f["strict"] and b["grade"]==pet71.UNRESOLVED
        w,h=b["width"],b["height"]
        geometry="NONPOSITIVE_GEOMETRY" if w<=0 or h<=0 else "POSITIVE_ABOVE_DECODER_BUDGET"
        assert w<=0 or h<=0 or w*h>1000000
        native[i]=dict(bitmap=b["bitmap"],index=i,width=w,height=h,pixel_product=w*h,
            size=b["size"],offset=b["offset"],rd_flag=int(r["rd_flag"]),rd_width=int(r["rd_width"]),rd_height=int(r["rd_height"]),rd_size=int(r["rd_size"]),
            rd_status=r["rd_status"],rd_sha256=b["rd_sha256"],adrn_sha256=b["adrn_sha256"],geometry=geometry,
            xoff=int(r["xoff"]),yoff=int(r["yoff"]),runtime_use="UNVERIFIED",pixel_receipt_promoted=False)
    assert native.keys()==failures.keys()
    by_number={b["bitmap"]:i for i,b in native.items()}
    matches={i:{"CN50":[],"TW10":[]} for i in native}
    for label,path in (("CN50",CN),("TW10",prev.EXTRA["tw10_adrn"][0])):
        for r in gzrows(path):
            n=int(r["bitmapno"]);d=r["rd_block_sha256"]
            for i,b in native.items():
                if n==b["bitmap"] or d==b["rd_sha256"]:
                    matches[i][label].append(dict(bitmap=n,rd_sha256=d,width=int(r["width"]),height=int(r["height"]),size=int(r["size"]),same_number=n==b["bitmap"],same_rd=d==b["rd_sha256"]))
    rr=routes.derive()
    positions=rr["album_positions"];named={i for p in positions for i in p["physical_group_indices"]}
    assert len(named)==1317
    allgroups={g["group_index"]:g for r in rr["graphics"] for g in r["physical_groups"]}
    outside={g["group_index"]:g for g in rr["outside_scope"]}
    assert not (allgroups.keys()&outside.keys())
    allgroups.update(outside)
    assert len(allgroups)==1739
    frame_refs=defaultdict(list)
    for f in gzrows(PINS["frames"][0]):
        if f["sentinel"]=="1":continue
        n=int(f["bmp_no"])
        if n not in by_number:continue
        i=by_number[n];g=int(f["group_index"])
        frame_refs[i].append(dict(group_index=g,graphic=allgroups[g]["graphic"],animation=int(f["anim_index"]),frame=int(f["frame_index"]),x=int(f["pos_x"]),y=int(f["pos_y"]),sound_word=int(f["sound_no"])))
    animation_keys={(f["group_index"],f["animation"]) for fs in frame_refs.values() for f in fs}
    anim={}
    for a in gzrows(prev.EXTRA["tw85_animation"][0]):
        k=(int(a["group_index"]),int(a["anim_index"]))
        if k in animation_keys:
            assert k not in anim
            anim[k]=dict(direction=int(a["direction"]),action=int(a["anim_no"]),duration=int(a["duration"]),frame_count=int(a["frame_count"]))
    assert anim.keys()==animation_keys
    affected=set();records=[]
    for i,b in sorted(native.items()):
        refs=frame_refs[i];ng={f["group_index"] for f in refs if f["group_index"] in named}
        assert len([f for f in refs if f["group_index"] in named])==1
        affected.update(ng)
        pp=[dict(program=p["program"],slot=p["slot"],name=p["name"],row_sha256=p["row_sha256"]) for p in positions if set(p["physical_group_indices"])&ng]
        records.append(dict(**b,frame_references=[dict(**f,**anim[f["group_index"],f["animation"]]) for f in refs],named_positions=pp,earlier_rd_candidates=matches[i]))
    assert len(affected)==2
    impacted=[p for p in positions if set(p["physical_group_indices"])&affected]
    assert len(impacted)==6
    # Residual groups: positive prior pet evidence only. No claim of nonpet
    # from an out-of-range or blank selector.
    master=defaultdict(list)
    for r in read(PINS["master"][0])["pet_flag_1_field_projections"]:
        master[r["graphic"]].append(dict(template_id=r["template_id"],name=r["name"],row_sha256=r["row_sha256"]))
    cn=defaultdict(list)
    for r in read(PINS["retention"][0])["records"]:
        for g in r["routes"]:
            cn[g["tw85_index"]].append(dict(ordinal=r["cn50_album_ordinal"],name=r["cn50_compiled_name"],graphic=g["sprite_group"],spr_sha256=g["same_original_spr_sha256"],cn50_index=g["cn50_index"]))
    early=defaultdict(list)
    for g in read(prev.EXTRA["tw10_receipt"][0])["groups"]:
        early[g["graphic"],g["segment_sha256"]].append(g["group_index"])
    residual=[];grades=Counter()
    for i in sorted(allgroups.keys()-named):
        g=allgroups[i];m=master[g["graphic"]];c=cn[i];e=early[g["graphic"],g["spr_sha256"]]
        assert all((x["graphic"],x["spr_sha256"])==(g["graphic"],g["spr_sha256"]) for x in c)
        assert bool(m)==g["pet68_canvas_scope"]
        status="PET68_ALREADY_COVERED" if m else "EARLIER_NAMED_OR_SELECTED_EXACT_SPR_CANDIDATE" if c or e else "NO_POSITIVE_PET_LINK_IN_COMPARED_SOURCES"
        grades[status]+=1
        residual.append(dict(**g,selector_scope="OUTSIDE" if i in outside else "INSIDE_NOT_NAMED",status=status,
            saved_master_candidates=m,cn50_original_named_exact_spr=c,tw10_selected_exact_spr_indices=e,official_pet_identity_verified=False))
    assert len(residual)==422 and sum(i["selector_scope"]=="OUTSIDE" for i in residual)==240 and grades["PET68_ALREADY_COVERED"]==6
    s=dict(geometry_status=dict(Counter(r["geometry"] for r in records)),named_affected_groups=len(affected),named_affected_positions=len(impacted),
        residual_group_count=422,residual_status=dict(grades),residual_outside_selector=240,residual_inside_not_named=182,
        official_species_count=None,original_runtime_verified=False,geometry_promotions=0)
    return dict(schema="stoneage.pet72.geometry_and_residual_scope.r1",summary=s,geometry_records=records,residual_groups=residual,
        source_pins={str(p.relative_to(ROOT)):h for p,h in EXTRA.items()},original_assets_published=False)
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path);a=p.parse_args()
    r=derive()
    if a.output:a.output.write_bytes(pet71.bulk.stable(r))
    print("PET72_SUMMARY="+json.dumps(r["summary"],ensure_ascii=False,sort_keys=True,separators=(",",":")),flush=True)
    print("PET72_GEOMETRY="+json.dumps(r["geometry_records"],ensure_ascii=False,sort_keys=True,separators=(",",":")),flush=True)
if __name__=="__main__":main()
