"""PET64: whole active queue coverage; independent source positions, not species."""
import argparse
import gzip
import json
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from stoneage_pet_source_lookup import load, build, resolve, blob, verify as verify_lookup
from stoneage_pet_gap_queue import queue, verify as verify_queue, FORMAL
from tools.stoneage_pet_high_first_tw85_residual import complete

PINS = {
    "early_atlas": ("research/pets/PET-DETAIL-EVIDENCE23-TW10-124-ORIGINAL-PRIVATE-VISUAL-ATLAS-R1.json", "a3e2584aec45262ebc91f98ec40f5e128e490dbe"),
    "early_motion": ("research/recovered/STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json", "e1cac6980353d09353de43fec0948bfcd84d49e6"),
    "cn_pixels": ("research/pets/PET-HIGH-FIRST-11-PC-INDEXED-PIXEL-RECEIPTS-R1.json.gz", "6ba6e7f9772c90dd1bad05f012e330f43ea41158"),
    "tw_pixels": ("research/pets/PET-HIGH-FIRST-12-TW85-INDEXED-PIXELS-R1.json.gz", "1e384d3faf93502e4e91b124fcc1a49761ca7d97"),
    "tw_long": ("research/pets/PET-HIGH-FIRST-13-TW85-LONG-AND-SPECIAL-R1.json.gz", "97fb8ffecda20d139ce0e72b7fb3548ef72d98dc"),
    "residual_pixels": ("research/pets/PET-HIGH-FIRST-59-RESIDUAL-PIXEL-RECEIPTS-R1.json", "f8083ef6db6f6b2ac057a7b4c440fad5c0dde3a4"),
    "chronology": ("research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json", "74cd977b39b8043b9c16ca57322b35542921ffc5"),
}
def pinned():
    out = {}
    for k,(path,sha) in PINS.items():
        raw = (ROOT/path).read_bytes()
        assert blob(raw)==sha, k
        out[k] = json.loads(gzip.decompress(raw) if path.endswith(".gz") else raw)
    return out

def apply_current_visual(row, visual):
    """Keep current visual observations beside independently sourced formal fields."""
    groups = visual["motion_groups"]
    group_status = Counter(group["status"] for group in groups)
    row["current_visual_source"] = {
        "qualification": visual["qualification"],
        "physical_group_indices": [group["group_index"] for group in groups],
        "group_status": dict(group_status),
    }
    if row["source"] == "tw85_grid":
        assert visual["portrait_status"] == "ALL_STRICT"
        row["portrait"] = "PRESERVED_NATIVE_ALIAS_ALL_PHYSICAL_ROWS_STRICT"
        row["motion"] = visual["album_position_motion_status"]
        row["linked_groups"] = len(groups)
        row.pop("groups_with_sample", None)
        row["groups_with_complete_canvas"] = group_status["STRICT_COMPLETE"] + group_status["BOUNDED_COMPLETE"]
        row["current_visual_source"].update(
            portrait_alias=visual["portrait_alias"], portrait_rows=visual["portrait_rows"],
        )
    elif row["source"] == "tw75":
        assert groups and set(group_status) <= {"STRICT_COMPLETE", "BOUNDED_COMPLETE"}
        if row["motion"] != "NOT_ASSESSED_BY_THIS_PASS":
            row["residual_motion_reference"] = row["motion"]
        grade = "BOUNDED" if group_status["BOUNDED_COMPLETE"] else "STRICT"
        row["motion"] = f"TW85_NUMERIC_GRAPHIC_{grade}_COMPLETE"


def derive(current=False):
    manifest,d=load()
    entries=build(d)
    verify_lookup(manifest,d,entries)
    rows=queue(d,entries)
    verify_queue(d,entries,rows)
    current_visual = {
        (entry["source"], tuple(entry["pointer"])): entry["detail"]["visual_reference"]
        for entry in entries if entry["detail"] and "visual_reference" in entry["detail"]
    } if current else {}
    if current:
        assert len(current_visual) == 4481
    z=pinned()
    atlas={x["pet_id"]:x for x in z["early_atlas"]["profiles"]}
    early_groups={x["graphic"]:x for x in z["early_motion"]["groups"]}
    cn={x["ordinal"]:x for x in z["cn_pixels"]["cn50_album"]}
    cn_blocks=z["cn_pixels"]["cn50_observed_blocks"]
    assert len(atlas)==124 and len(cn)==305
    tw_receipts=[z["tw_pixels"],z["tw_long"]["observations"],d["hf60"]["observations"]]
    assert all(a["source_files"] == tw_receipts[0]["source_files"] for a in tw_receipts)
    direct_groups=set()
    for receipt in tw_receipts:
        for seq in receipt["sequences"]:
            if complete(seq,receipt):
                direct_groups.add((seq["physical_group"],seq["spr"],seq["spr_segment_sha256"]))
    direct_aliases=set()
    for receipt in tw_receipts:
        for alias, candidates in receipt["portraits_by_original_alias"].items():
            if any(receipt["observed_blocks"][str(idx)]["status"]=="DUAL_DECODED_INDEX_PIXELS" for idx,_ in candidates):
                direct_aliases.add(str(alias))
    cross_aliases={str(k) for k,v in z["residual_pixels"]["portrait_candidates"].items() if any(a["source"]=="cn50" for a in v)}
    route_groups=defaultdict(set)
    for rec in d["tw85_visual"]["records"]:
        spr=rec["tw85_original_spr_no_not_official_pet_id"]
        for program,route in rec["original_native_program_routes"].items():
            if route["status"]!="SOURCE_LOCAL_NAMED_ROUTE":
                continue
            key=(program,route["local_album_slot"],route["original_28b_record_sha256"])
            route_groups[key].update((g["original_source_group_index"],spr,g["original_full_spr_segment_sha256"]) for g in rec["original_physical_sprite_occurrences"])
    residual={x["position"]:x for x in d["hf62"]["rows"]}
    claimed=d["hf45"]["projection"]["claimed_tw75_rows"]
    gaps={x["tw75_row_index"]:x for x in d["hf46"]["rows"]}
    out=[]
    for r in rows:
        source=r["source"]; ptr=r["pointer"]; x=resolve(d,source,ptr)
        fields=r["formal_fields"]
        v=dict(source=source,pointer=ptr,labels=r["labels"],formal_fields=fields,
            portrait="NOT_ASSESSED_BY_THIS_PASS",motion="NOT_ASSESSED_BY_THIS_PASS",
            acquisition="NOT_ASSESSED_BY_THIS_PASS",family="NO_EXPLICIT_FAMILY_IN_QUEUE_PROJECTION",
            official_full_fields_certified=False)
        if r["source_evidence"].get("family"):
            v["family"]="EXPLICIT_SOURCE_FAMILY_LABEL"
        if source=="tw10":
            a=atlas[x["pet_id"]];g=early_groups[x["client_graphic"]]
            assert a["original_sprite_segment_sha256"]==g["segment_sha256"]
            v["portrait"]="ORIGINAL_RD_DECODED" if a["original_album_RD"] else "ORIGINAL_POSE_FALLBACK_NOT_PORTRAIT"
            v["motion"]="ORIGINAL_ALL_SELECTED_GROUP_SEQUENCES_OBSERVED" if g["fully_observable_sequences"]==g["source_sequences"] else "ORIGINAL_PARTIAL_GROUP_SEQUENCES_OBSERVED"
            ref=r["source_evidence"]["field_reference"]
            v["element_reference"]=ref["element_status"]
            v["acquisition"]="PERIOD_ACQUISITION_OR_STARTER_REFERENCE" if ref["acquisition_witnesses"] or ref["period_starter_witness"] else "NO_PERIOD_ACQUISITION_IN_THIS_REFERENCE_SET"
        elif source=="cn50":
            c=cn[x["ordinal"]]
            assert c["cn50_name_row_sha256"]==x["exe_row_sha256"]
            b=cn_blocks[str(c["portrait_selected_bitmap"])]
            assert b["rd_sha256"]==x["portrait_lookup_rd_sha256"] and b["index_pixels_sha256"]
            v["portrait"]="PRESERVED_RD_DECODED"
            v["motion"]="PRESERVED_ONE_SEQUENCE_DECODED" if c["sample"] else "PRESERVED_SPR_INDEX_NO_R11_SAMPLE"
            v["acquisition"]="PERIOD_CATALOGUE_NAME_LINK" if fields["capture"]!="NOT_CERTIFIED_SAME_DEPLOYMENT" else "NO_PERIOD_ACQUISITION_CELL_IN_THIS_JOIN"
        elif source=="tw85_grid":
            key=(ptr[1],x["slot"],x["original_row_sha256"]);a=str(x["source_portrait_alias"])
            groups=route_groups[key]
            v["portrait"]="PRESERVED_NATIVE_ALIAS_DECODED" if a in direct_aliases else "CROSS_CARRIER_EXACT_RD_RECEIPT" if a in cross_aliases else "EXTRA_SUBSET_PATCH_RD_CANDIDATE" if r["source_evidence"]["portrait"]=="EXTRA_SUBSET_EXACT_PATCH_RD_CANDIDATE" else "NOT_ASSESSED_IN_COMPARED_RECEIPTS"
            if groups:
                n=len(groups & direct_groups)
                v["motion"]="ALL_LINKED_GROUPS_HAVE_BOUNDED_SAMPLE" if n==len(groups) else "SOME_LINKED_GROUPS_HAVE_BOUNDED_SAMPLE" if n else "LINKED_GROUPS_NO_COMPLETE_SAMPLE_IN_COMPARED_RECEIPTS"
                v["linked_groups"]=len(groups);v["groups_with_sample"]=n
            else:
                v["motion"]="NOT_ASSESSED_IN_EXTRA_SUBSET"
            v["acquisition"]="NO_SERVER_ACQUISITION_JOIN_IN_THIS_PASS"
        elif source=="tw75":
            i=ptr[1];ac=claimed[i]
            assert ac["tw75_row_sha256"]==x["row_sha256"]
            if ac["double_pet_flag_route_count"]:
                v["acquisition"]="SAVED_DOUBLE_FLAG_POSITIVE_ROUTE"
            elif gaps[i]["gap_state"]=="SAVED_TASK_REWARD_CONFIGURED_NOT_EXECUTED":
                v["acquisition"]="SAVED_TASK_REWARD_CONFIGURATION"
            elif i in residual:
                v["acquisition"]="STRICT_RESIDUAL_REVIEWED_NOT_CLOSED"
                v["motion"]=residual[i]["sequence_receipt"]
            else:
                v["acquisition"]="OTHER_REFERENCE_NOT_OFFICIAL_ACQUISITION"
            v["master_match"]=ac["match_status"]
            v["element_sum"]=sum(x["elements"])
        else:
            if fields["award"]!="NOT_CERTIFIED_SAME_DEPLOYMENT" or fields["capture"]!="NOT_CERTIFIED_SAME_DEPLOYMENT":
                v["acquisition"]="HISTORICAL_REFERENCE_NOT_OFFICIAL_SAME_DEPLOYMENT"
            else:
                v["acquisition"]="NO_ACQUISITION_FIELD_IN_QUEUE_PROJECTION"
        if current and source in {"tw10", "cn50", "tw85_grid", "tw75"}:
            apply_current_visual(v, current_visual[source, tuple(ptr)])
        out.append(v)
    assert len(out)==3015 and len({(r["source"],tuple(r["pointer"])) for r in out})==3015
    assert all(not r["official_full_fields_certified"] for r in out)
    def counts(rs,k):
        return dict(sorted(Counter(r[k] for r in rs if k in r).items()))
    by_source={}
    for source in sorted({r["source"] for r in out}):
        rs=[r for r in out if r["source"]==source]
        by_source[source]=dict(positions=len(rs),portrait=counts(rs,"portrait"),motion=counts(rs,"motion"),acquisition=counts(rs,"acquisition"),family=counts(rs,"family"),
            formal_fields={k:dict(sorted(Counter(r["formal_fields"][k] for r in rs).items())) for k in FORMAL})
        for k in ("element_reference","master_match","element_sum"):
            if any(k in r for r in rs):by_source[source][k]=counts(rs,k)
    for source, info in by_source.items():
        assert all(sum(info[k].values())==info["positions"] for k in ("portrait","motion","acquisition","family"))
        assert all(sum(v.values())==info["positions"] for v in info["formal_fields"].values())
    assert by_source["tw10"]["portrait"]=={"ORIGINAL_POSE_FALLBACK_NOT_PORTRAIT":4,"ORIGINAL_RD_DECODED":120}
    assert by_source["cn50"]["portrait"]=={"PRESERVED_RD_DECODED":305}
    assert by_source["cn50"]["motion"]["PRESERVED_ONE_SEQUENCE_DECODED"]==181
    assert by_source["tw75"]["acquisition"]["SAVED_DOUBLE_FLAG_POSITIVE_ROUTE"]==118
    assert by_source["tw75"]["acquisition"]["STRICT_RESIDUAL_REVIEWED_NOT_CLOSED"]==67
    if current:
        assert by_source["tw85_grid"]["portrait"] == {"PRESERVED_NATIVE_ALIAS_ALL_PHYSICAL_ROWS_STRICT": 1889}
        assert by_source["tw85_grid"]["motion"] == {"ALL_CANVAS_COMPLETE": 1883, "SOME_CANVAS_COMPLETE": 6}
        assert by_source["tw75"]["motion"] == {"TW85_NUMERIC_GRAPHIC_BOUNDED_COMPLETE": 37, "TW85_NUMERIC_GRAPHIC_STRICT_COMPLETE": 430}
        assert sum("residual_motion_reference" in row for row in out) == 67
    else:
        assert by_source["tw85_grid"]["motion"]["NOT_ASSESSED_IN_EXTRA_SUBSET"]==1204
    history=z["chronology"]
    annual=Counter(x["research_gate"] for x in history["yearly_work_queue"])
    assert annual=={"SOURCE_BOUNDED_REVIEWED":27,"NOT_YEAR_AUDITED":1}
    assert history["current_frontier"]["year"]==2026
    assert history["pc_only_scope_supersession"]["classic_pc_only_source_filter"]
    vip=d["hf51_petabi"]["petabi_rows"]
    summary=dict(source_positions=len(out),query_occurrences=len(entries),distinct_literal_labels=len({n for e in entries for n in e["labels"]}),by_source=by_source,
        additional_vip_positions_outside_queue=len(vip),chronological_year_status=dict(annual),chronology_frontier=2026,
        official_species_count=None,official_full_fields_certified=0,
        scope="Queue positions only. No deduplicated species total. Unassessed is not absent. Actual index pixel receipts are bounded; not proof of palette, timing, official identity or gameplay.")
    if current:
        summary["visual_projection"] = dict(
            newer_evidence="PET74", lookup_positions_with_visual=len(current_visual),
            queue_positions_with_visual=sum("current_visual_source" in row for row in out),
            official_fields_reclassified=0,
        )
    return summary,out
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--all",action="store_true")
    p.add_argument("--source")
    p.add_argument("--current", action="store_true", help="include the unified lookup's current visual evidence")
    a=p.parse_args()
    if a.current:
        with redirect_stdout(sys.stderr):
            s, rows = derive(current=True)
    else:
        s, rows = derive()
    if a.source:rows=[r for r in rows if r["source"]==a.source]
    if a.all or a.source:
        print(json.dumps(dict(summary=s,rows=rows),ensure_ascii=False,indent=2,sort_keys=True))
    elif a.current:
        print(json.dumps(s,ensure_ascii=False,indent=2,sort_keys=True))
    else:
        compact={k:{f:v[f] for f in ("positions","portrait","motion","acquisition","family")} for k,v in s["by_source"].items()}
        actual={**s,"by_source":compact}
        snapshot=json.loads((ROOT/"research/pets/PET-HIGH-FIRST-64-MODULE-COVERAGE-SUMMARY-R1.json").read_bytes())
        assert snapshot["summary"]==actual, "durable coverage summary differs from replay"
        print("PET64_SUMMARY="+json.dumps(actual,ensure_ascii=False,sort_keys=True,separators=(",",":")))
if __name__=="__main__":
    main()
