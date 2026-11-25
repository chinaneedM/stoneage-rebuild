"""Full source-qualified TW85 alias census and TW75 graphic crosswalk."""
import argparse
from collections import Counter, defaultdict
import gzip
import json
from pathlib import Path
from tools.stoneage_pet_high_first_57_coverage import PINS, blob, gzrows, ROOT
from tools.stoneage_pet_high_first_tw85_residual import complete
P = ROOT/"research/pets"
EXTRA = {
    "cn_pixels": (P/"PET-HIGH-FIRST-11-PC-INDEXED-PIXEL-RECEIPTS-R1.json.gz", "6ba6e7f9772c90dd1bad05f012e330f43ea41158"),
    "tw_pixels": (P/"PET-HIGH-FIRST-12-TW85-INDEXED-PIXELS-R1.json.gz", "1e384d3faf93502e4e91b124fcc1a49761ca7d97"),
    "tw_long": (P/"PET-HIGH-FIRST-13-TW85-LONG-AND-SPECIAL-R1.json.gz", "97fb8ffecda20d139ce0e72b7fb3548ef72d98dc"),
    "tw60": (P/"PET-HIGH-FIRST-60-TW85-REMAINING-PIXELS-R1.json", "8791199ccbf374495a50b9bc479ababe22c77edf"),
    "baseline": (P/"PET-HIGH-FIRST-64-MODULE-COVERAGE-SUMMARY-R1.json", "177d51d3e27b0e7d2cec4143f35f1955acefb939"),
}
USED={k:PINS[k] for k in ("grid","master","cn50","retention","visual","groups","material","patch","pairs","native")}
USED.update(EXTRA)
def read():
    d={}
    for k,(path,sha) in USED.items():
        raw=path.read_bytes()
        assert blob(raw)==sha,k
        if path.name.endswith(".json.gz"):d[k]=json.loads(gzip.decompress(raw))
        elif path.suffix==".json":d[k]=json.loads(raw)
    return d
def derive():
    d=read()
    grid=defaultdict(list); names=defaultdict(list)
    for program, info in d["grid"]["programs"].items():
        for row in info["source_records"]:
            x=dict(program=program,slot=row["slot"],first_i32=row["original_first_i32"],name=row["original_name_cp950"],row_sha256=row["original_row_sha256"],alias=row["source_portrait_alias"])
            grid[x["alias"]].append(x);names[x["name"]].append(x)
    assert len(grid)==508 and sum(map(len,grid.values()))==1889
    assert sum(len({r["name"] for r in rows})>1 for rows in grid.values())==6
    patch=defaultdict(list)
    for row in gzrows(USED["patch"][0]):
        a=int(row["map_number"])
        if a in grid:
            patch[a].append(dict(patch_index=int(row["index"]),record_sha256=row["record_sha256"]))
    patch_ids={x["patch_index"] for v in patch.values() for x in v}
    pairs={}; indices=set()
    for row in gzrows(USED["pairs"][0]):
        i=int(row["patch_index"])
        if i in patch_ids:
            assert i not in pairs
            ids=[int(n) for n in row["native_exact_indices"].split(",") if n]
            pairs[i]=dict(bitmap=int(row["bitmapno"]),record_sha256=row["patch_record_sha256"],rd_sha256=row["rd_sha256"],qualification=row["qualification"],indices=ids)
            indices.update(ids)
    assert pairs.keys()==patch_ids
    receipts=[d["tw_pixels"],d["tw_long"]["observations"],d["tw60"]["observations"]]
    assert all(r["source_files"]==receipts[0]["source_files"] for r in receipts)
    direct=defaultdict(dict); observed={}
    sample_groups=set()
    for report in receipts:
        for key, b in report["observed_blocks"].items():
            i=int(key)
            if i in observed:
                assert (observed[i]["adrn_sha256"],observed[i]["rd_sha256"])==(b["adrn_sha256"],b["rd_sha256"])
            if i not in observed or b["status"]=="DUAL_DECODED_INDEX_PIXELS":observed[i]=b
        for a,candidates in report["portraits_by_original_alias"].items():
            for i,bitmap in candidates:
                if i in direct[int(a)]:assert direct[int(a)][i]==bitmap
                direct[int(a)][i]=bitmap;indices.add(i)
        for seq in report["sequences"]:
            if complete(seq,report):
                sample_groups.add((seq["physical_group"],seq["spr"],seq["spr_segment_sha256"]))
    native={}
    for row in gzrows(USED["native"][0]):
        i=int(row["index"])
        if i in indices:
            native[i]=dict(index=i,bitmap=int(row["bitmapno"]),adrn_sha256=row["record_sha256"],rd_sha256=row["rd_sha256"],width=int(row["width"]),height=int(row["height"]),rd_status=row["rd_status"])
    assert native.keys()==indices
    cn_by_alias=defaultdict(list)
    cn_by_graphic=defaultdict(list)
    ret={r["cn50_album_ordinal"]:r for r in d["retention"]["records"]}
    cn_pixels={r["ordinal"]:r for r in d["cn_pixels"]["cn50_album"]}
    blocks=d["cn_pixels"]["cn50_observed_blocks"]
    for row in d["cn50"]["records"]:
        cn_by_alias[row["portrait_alias"]].append(row)
        for group in row["spr_groups"]:
            cn_by_graphic[group["spr_group"]].append((row,group))
    aliases=[]
    for a,rows in sorted(grid.items()):
        candidates={}
        for p in patch[a]:
            pair=pairs[p["patch_index"]]
            assert p["record_sha256"]==pair["record_sha256"]
            for i in pair["indices"]:
                n=native[i]
                assert (n["bitmap"],n["adrn_sha256"],n["rd_sha256"])==(pair["bitmap"],pair["record_sha256"],pair["rd_sha256"])
                candidates[i]=n
        for i,b in direct[a].items():
            assert native[i]["bitmap"]==b
            candidates[i]=native[i]
        direct_decoded=[]; cross=[]
        for i,n in sorted(candidates.items()):
            b=observed.get(i)
            if b and b["status"]=="DUAL_DECODED_INDEX_PIXELS":
                assert (b["adrn_sha256"],b["rd_sha256"],b["bitmap"])==(n["adrn_sha256"],n["rd_sha256"],n["bitmap"])
                direct_decoded.append(i)
            for cn in cn_by_alias.get(a, []):
                p=cn_pixels[cn["ordinal"]];b=blocks[str(p["portrait_selected_bitmap"])]
                if b["index_pixels_sha256"] and b["rd_sha256"]==n["rd_sha256"] and (b["width"],b["height"])==(n["width"],n["height"]):
                    cross.append(dict(native_index=i,cn50_ordinal=cn["ordinal"],rd_sha256=n["rd_sha256"]))
        if direct_decoded:status="SAME_CARRIER_DECODED"
        elif cross:status="EXACT_CN50_RD_DECODED_REFERENCE"
        elif candidates:status="NATIVE_INDEX_CANDIDATE_NO_PIXEL_RECEIPT"
        elif patch[a]:status="PATCH_ALIAS_NO_EXACT_NATIVE_ROW_IN_COMPARED_TABLE"
        else:status="NO_PATCH_OR_DIRECT_ALIAS_RECEIPT_NOT_ABSENCE"
        aliases.append(dict(alias=a,program_positions=rows,distinct_names=sorted({r["name"] for r in rows}),
            patch_refs=[dict(**x,pair=pairs[x["patch_index"]]) for x in patch[a]],
            native_candidates=[candidates[i] for i in sorted(candidates)],direct_decoded_indices=direct_decoded,
            exact_cn50_pixel_refs=cross,status=status,official_identity_verified=False))
    alias_by={r["alias"]:r for r in aliases}
    by_graphic=defaultdict(list);group_by={}
    for i,(g,m) in enumerate(zip(gzrows(USED["groups"][0]),gzrows(USED["material"][0]),strict=True)):
        assert int(g["index"])==int(m["group_index"])==i and g["spr_no"]==m["spr_no"]
        spr=int(g["spr_no"]);sha=g["segment_sha256"]
        n=dict(group_index=i,graphic=spr,segment_sha256=sha,animation_headers=int(g["anim_count"]),frame_occurrences=int(m["frame_occurrences"]),mapped_frames=int(m["mapped_frames"]),sentinel_frames=int(m["sentinel_frames"]),missing_frames=int(m["missing_frames"]),has_bounded_direct_sample=(i,spr,sha) in sample_groups)
        assert n["frame_occurrences"]==sum(n[k] for k in ("mapped_frames","sentinel_frames","missing_frames"))
        by_graphic[spr].append(n);group_by[i]=n
    assert len(group_by)==1739
    native_routes=defaultdict(list);route_slots=defaultdict(set)
    for r in d["visual"]["records"]:
        spr=r["tw85_original_spr_no_not_official_pet_id"]
        for g in r["original_physical_sprite_occurrences"]:
            n=group_by[g["original_source_group_index"]]
            assert (n["graphic"],n["segment_sha256"])==(spr,g["original_full_spr_segment_sha256"])
        for p,x in r["original_native_program_routes"].items():
            if x["status"]=="SOURCE_LOCAL_NAMED_ROUTE":
                row=next(y for y in grid[x["source_portrait_alias"]] if y["program"]==p and y["slot"]==x["local_album_slot"] and y["row_sha256"]==x["original_28b_record_sha256"])
                native_routes[spr].append(row)
                route_slots[(p,row["slot"],row["row_sha256"])].add(spr)
    # Additional CN50 relationships remain cross-carrier, not TW85 selector proof.
    master=[]
    for position,x in enumerate(d["master"]["pet_flag_1_field_projections"]):
        spr=x["graphic"];groups=by_graphic[spr]
        candidates=names[x["name"]]
        assert sorted([r["program"],r["slot"]] for r in candidates)==sorted(x["tw85_exact_name_album_slots"])
        nr=native_routes[spr]
        cn=[]
        for row,g in cn_by_graphic[spr]:
            rr=ret[row["ordinal"]]
            exact=[q for q in rr["routes"] if q["sprite_group"]==spr and q["same_original_spr_sha256"]==g["sha256"]]
            assert exact and all((group_by[q["tw85_index"]]["graphic"],group_by[q["tw85_index"]]["segment_sha256"])==(spr,g["sha256"]) for q in exact)
            cn.append(dict(ordinal=row["ordinal"],name=row["compiled_name"],alias=row["portrait_alias"],sprite_sha256=g["sha256"],tw85_group_indices=[q["tw85_index"] for q in exact]))
        master.append(dict(position=position,template_id=x["template_id"],name=x["name"],graphic=spr,row_sha256=x["row_sha256"],
            physical_groups=groups,exact_name_grid_candidates=[dict(**r,portrait_status=alias_by[r["alias"]]["status"]) for r in candidates],
            native_named_routes=nr,cn50_exact_spr_cross_carrier=cn,
            same_deployment_identity_verified=False,official_acquisition_verified=False))
    assert len(master)==467 and len({r["graphic"] for r in master})==425
    status_counts=Counter(r["status"] for r in aliases)
    position_counts=Counter()
    for a in aliases:position_counts[a["status"]]+=len(a["program_positions"])
    assert sum(status_counts.values())==508 and sum(position_counts.values())==1889
    # Cross-carrier CN relationship counts not same-build name claims.
    cn_grid_positions=sum(len(grid[a]) for a,rows in cn_by_alias.items() if rows and a in grid)
    assert cn_grid_positions==1220
    summary=dict(alias_count=508,program_positions=1889,alias_name_conflicts=6,alias_status=dict(status_counts),position_status=dict(position_counts),
        cn50_same_numeric_alias_positions=cn_grid_positions,extra_native_route_positions=len(route_slots),
        master_positions=467,master_distinct_graphics=425,master_with_physical_graphic=sum(bool(r["physical_groups"]) for r in master),
        master_with_all_physical_groups_mapped=sum(bool(r["physical_groups"]) and all(not g["missing_frames"] for g in r["physical_groups"]) for r in master),
        master_with_direct_bounded_sample=sum(any(g["has_bounded_direct_sample"] for g in r["physical_groups"]) for r in master),
        master_with_exact_name_grid=sum(bool(r["exact_name_grid_candidates"]) for r in master),
        master_with_exact_name_native_route=sum(any(x["name"]==r["name"] for x in r["native_named_routes"]) for r in master),
        master_with_cn50_exact_spr=sum(bool(r["cn50_exact_spr_cross_carrier"]) for r in master),
        master_with_cn50_exact_name_and_spr=sum(any(x["name"]==r["name"] for x in r["cn50_exact_spr_cross_carrier"]) for r in master),
        master_unique_group_count=len({g["group_index"] for r in master for g in r["physical_groups"]}),
        aliases_need_original_census=sum(a["status"]=="NO_PATCH_OR_DIRECT_ALIAS_RECEIPT_NOT_ABSENCE" for a in aliases),
        aliases_need_direct_source_read=sum(not a["direct_decoded_indices"] for a in aliases),
        official_species_count=None,new_official_acquisition_closures=0)
    assert summary["extra_native_route_positions"]==685
    assert summary["master_with_exact_name_grid"]==439 and summary["master_with_exact_name_native_route"]==104
    assert summary["master_with_cn50_exact_spr"]==343 and summary["master_with_cn50_exact_name_and_spr"]==142
    return dict(schema="stoneage.pet65.full_visual_index.r1",source_pins={k:dict(path=str(p.relative_to(ROOT)),git_blob=h) for k,(p,h) in USED.items()},summary=summary,aliases=aliases,master=master,original_assets_published=False,runtime_executed=False,official_identity_verified=False)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    report=derive()
    if a.output:a.output.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8")
    print("PET65_SUMMARY="+json.dumps(report["summary"],ensure_ascii=False,sort_keys=True,separators=(",",":")))
if __name__=="__main__":main()
