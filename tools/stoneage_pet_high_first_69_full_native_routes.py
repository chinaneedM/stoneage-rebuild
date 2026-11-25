"""PET69: full bounded static selector route census, not live pet identity."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
from tools.stoneage_pet_high_first_57_coverage import ROOT, PINS, blob, gzrows
from tools.stoneage_pet_high_first_tw85_native_bridge import validate, route_slot

# Derived by finite control-flow replay of the four source-exact selector
# windows retained in source job 137698380853, not by guessing ordinal IDs.
EARLY = [(100250,100430,-100250),(100431,101150,-100639),
 (101151,101176,-100871),(101177,101177,-100884),
 (101178,101179,-100893),(101180,101180,-100894),
 (101181,101411,-100995),(101412,101422,-101118),
 (101423,101436,-101127),(101437,101463,-101136),
 (101464,101464,-101133),(101465,101466,-101136),
 (101467,101467,-101139),(101468,101489,-101136),
 (101490,101500,-101139)]
# Independent ordered branch semantics from the same four original windows.
# Explicit comparison order matters at special equalities and boundaries.
RULES = [("eq",0x4be,0x14b),("eq",0x4c1,0x148),
 ("gt",0x4d7,0x379),("gt",0x4a2,0x376),
 ("gt",0x495,0x36d),("gt",0x494,0x36d),
 ("gt",0x489,0x364),("gt",0x3a2,0x2e9),
 ("eq",0x39f,0x125),("gt",0x3a1,0x284),
 ("gt",0x39f,0x283),("gt",0x384,0x26d),("gt",0xb4,0x185)]
SOURCE = dict(run_id=45176319806,job_id=137698380853,
 source_report_sha256="c7cdbfb3fdf420e14847a33c4c5982e493a8affc84436874ec86cc2f95361f74",
 evidence="PREVIOUS_SUCCESSFUL_ORIGINAL_STATIC_SOURCE_JOB_LOG_REPLAY",
 early_inputs_per_program=1251,prior_high_inputs_per_program=550,
 early_negative_inputs_per_program=208,original_runtime_verified=False)
REQUIRED = {k:PINS[k] for k in ("grid","bridge","groups","material","master")}
REQUIRED["pet68"]=(ROOT/"research/pets/PET-HIGH-FIRST-68-RD-BOUNDARY-SUMMARY-R1.json","bf296c3bcf07b4992e3af34c69f5dc9e7f808127")
def early_slot(g):
    assert 100250<=g<=101500
    matches=[g+d for a,b,d in EARLY if a<=g<=b]
    assert len(matches)==1
    x=g-100250
    for condition,c,value in RULES:
        if condition=="eq" and x==c:
            x=value;break
        if condition=="gt" and x>c:
            x-=value;break
    assert x==matches[0]
    return x

def derive():
    d={}
    for k,(p,h) in REQUIRED.items():
        raw=p.read_bytes();assert blob(raw)==h,k
        if p.suffix==".json":d[k]=json.loads(raw)
    assert sum(early_slot(g)<0 for g in range(100250,101501))==208
    old=d["bridge"];validate(old)
    assert d["pet68"]["canvas_unresolved_bitmaps"]==0
    assert d["pet68"]["canvas_covered_bitmaps"]==113311
    assert d["pet68"]["strict_exceptions"]==68
    programs=d["grid"]["programs"]
    assert set(programs)==set(old["programs"])
    named={p:{r["slot"]:r for r in x["source_records"]} for p,x in programs.items()}
    blanks={p:{r["slot"]:r for r in x["blank_or_unqualified"]} for p,x in programs.items()}
    for p,x in programs.items():
        assert not (named[p].keys()&blanks[p].keys())
        assert named[p].keys()|blanks[p].keys()==set(range(x["total_grid_slots"]))
        assert old["programs"][p]["original_executable_sha256"]==x["packed_sha256"]
        assert old["programs"][p]["original_unpacked_sha256"]==x["unpacked_sha256"]
    assert sum(map(len,named.values()))==1889
    master={r["graphic"] for r in d["master"]["pet_flag_1_field_projections"]}
    assert len(master)==425
    by_graphic=defaultdict(list);outside=[]
    for i,(g,m) in enumerate(zip(gzrows(REQUIRED["groups"][0]),gzrows(REQUIRED["material"][0]),strict=True)):
        assert int(g["index"])==int(m["group_index"])==i and g["spr_no"]==m["spr_no"]
        n=int(g["spr_no"])
        record=dict(group_index=i,graphic=n,spr_sha256=g["segment_sha256"],animation_headers=int(g["anim_count"]),frame_occurrences=int(m["frame_occurrences"]),mapped_frames=int(m["mapped_frames"]),sentinel_frames=int(m["sentinel_frames"]),missing_frames=int(m["missing_frames"]),
            pet68_canvas_scope=n in master)
        assert record["frame_occurrences"]==sum(record[k] for k in ("mapped_frames","sentinel_frames","missing_frames"))
        if 100250<=n<=102050:by_graphic[n].append(record)
        else:outside.append(record)
    assert sum(map(len,by_graphic.values()))+len(outside)==1739
    assert master<=by_graphic.keys()
    assert sum(len(by_graphic[n]) for n in master)==427
    prior={r["tw85_original_spr_number"]:r for r in old["records"]}
    assert set(prior)=={g for g in by_graphic if g>=101501}
    positions=defaultdict(list);rows=[];counts={p:Counter() for p in programs}
    conflicts=0
    for g,groups in sorted(by_graphic.items()):
        routes={};names=set()
        for p in sorted(programs):
            slot=early_slot(g) if g<=101500 else route_slot(old["programs"][p]["source_rule_segments_for_550_graphic_numbers"],g)
            if slot in named[p]:
                r=named[p][slot];status="SOURCE_LOCAL_NAMED_ROUTE"
                result=dict(name=r["original_name_cp950"],row_sha256=r["original_row_sha256"],portrait_alias=r["source_portrait_alias"])
                names.add(result["name"]);positions[p,slot].append(g)
            elif slot in blanks[p]:
                status="SOURCE_BLANK_OR_UNQUALIFIED";result=dict(row_sha256=blanks[p][slot]["original_row_sha256"])
            else:
                status="OUTSIDE_QUALIFIED_LOCAL_GRID";result={}
                assert slot<0 or slot>=programs[p]["total_grid_slots"]
            routes[p]=dict(slot=slot,status=status,**result);counts[p][status]+=1
            if g in prior:
                q=prior[g]["program_routes"][p]
                assert (slot,status)==(q["local_album_slot"],q["record_source_status"])
                if status=="SOURCE_LOCAL_NAMED_ROUTE":
                    assert (result["name"],result["row_sha256"],result["portrait_alias"])==(q["original_name_cp950"],q["original_album_row_sha256"],q["original_portrait_alias_u32"])
        if g in prior:
            assert [(x["group_index"],x["spr_sha256"],x["animation_headers"]) for x in groups]==[(x["source_occurrence_index"],x["original_spr_segment_sha256"],x["original_animation_header_count"]) for x in prior[g]["source_spr_occurrences"]]
        conflict=len(names)>1;conflicts+=conflict
        rows.append(dict(graphic=g,physical_groups=groups,program_routes=routes,name_conflict=conflict))
    pos=[];pc=Counter()
    for p in sorted(programs):
        for slot,r in sorted(named[p].items()):
            gs=positions.get((p,slot),[])
            high=[g for g in gs if g>=101501];early=[g for g in gs if g<=101500]
            if high:status="PRIOR_HIGH_ROUTE"
            elif early:status="NEW_EARLY_ROUTE"
            else:status="NO_ROUTE_IN_COMPARED_PHYSICAL_GRAPHICS"
            pc[status]+=1
            pos.append(dict(program=p,slot=slot,name=r["original_name_cp950"],row_sha256=r["original_row_sha256"],portrait_alias=r["source_portrait_alias"],
                early_graphics=early,high_graphics=high,route_status=status,
                any_pet68_canvas_route=any(g in master for g in gs),
                all_route_groups_pet68_canvas=bool(gs) and all(g in master for g in gs),
                physical_group_indices=[q["group_index"] for g in gs for q in by_graphic[g]]))
    assert pc["PRIOR_HIGH_ROUTE"]==685
    assert pc["NEW_EARLY_ROUTE"]+pc["NO_ROUTE_IN_COMPARED_PHYSICAL_GRAPHICS"]==1204
    assert len(pos)==1889
    new=[x for x in pos if x["route_status"]=="NEW_EARLY_ROUTE"]
    summary=dict(total_source_groups=1739,compared_graphic_numbers=len(rows),compared_physical_groups=sum(map(len,by_graphic.values())),
        outside_scope_physical_groups=len(outside),early_graphic_numbers=sum(g<=101500 for g in by_graphic),
        high_graphic_numbers=len(prior),program_positions=len(pos),position_status=dict(pc),
        new_early_positions_with_any_pet68_canvas=sum(x["any_pet68_canvas_route"] for x in new),
        new_early_positions_with_all_routes_pet68_canvas=sum(x["all_route_groups_pet68_canvas"] for x in new),
        new_early_physical_groups=len({i for x in new for i in x["physical_group_indices"]}),
        cross_program_graphic_name_conflicts=conflicts,program_route_counts={p:dict(c) for p,c in counts.items()},
        official_species_count=None,official_acquisition_closures=0,original_runtime_verified=False)
    return dict(schema="stoneage.pet69.full_native_routes.r1",source=SOURCE,source_pins={k:dict(path=str(p.relative_to(ROOT)),git_blob=h) for k,(p,h) in REQUIRED.items()},
        early_segments=EARLY,summary=summary,graphics=rows,album_positions=pos,outside_scope=outside,
        original_programs_or_pixels_published=False,official_identity_verified=False)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--output",type=Path);a=p.parse_args()
    report=derive()
    if a.output:a.output.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8")
    print("PET69_SUMMARY="+json.dumps(report["summary"],sort_keys=True,separators=(",",":")),flush=True)
if __name__=="__main__":main()
