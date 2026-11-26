"""PET whole-module review: combine current source-scoped queue and verified visual evidence.
No global species counts, no source/runtime promotion, no claim of closure."""
import json
from collections import Counter
from pathlib import Path
from stoneage_pet_source_lookup import load,build,verify,blob
from stoneage_pet_gap_queue import queue,verify as verify_queue,FORMAL
from stoneage_pet_high_first_64_coverage import derive
ROOT=Path(__file__).resolve().parents[1]
def hist(items):
    return dict(sorted(Counter(items).items()))
def review():
    m,d=load(); entries=build(d);verify(m,d,entries)
    rows=queue(d,entries,current=True)
    verify_queue(d,entries,[r for r in rows if r["source"]!="cn85_original"])
    prior,visual=derive(current=True)
    key=lambda r:(r["source"],tuple(r["pointer"]))
    v={key(r):r for r in visual}
    keys={key(x) for x in rows}
    e={key(r):r for r in entries if key(r) in keys}
    assert len(rows)==len({key(r) for r in rows})==len(e)==3563
    assert len(v)==3015 and len(entries)==5924
    out={}
    for source in sorted({r["source"] for r in rows}):
        subset=[r for r in rows if r["source"]==source]
        portraits=[]; motions=[]; acquisitions=[]; families=[]
        links=Counter(); details=Counter()
        for row in subset:
            k=key(row); x=e[k]; detail=x["detail"] or {}
            assert row["official_same_deployment_certified"] is False
            if k in v:
                old=v[k]
                assert row["formal_fields"]==old["formal_fields"]
                portraits.append(old["portrait"]); motions.append(old["motion"])
                acquisitions.append(old["acquisition"]);families.append(old["family"])
            else:
                assert source=="cn85_original"
                portraits.append(detail["portrait_candidate_grade"])
                motions.append(row["source_evidence"]["motion"])
                acquisitions.append("NO_CERTIFIED_SERVER_ACQUISITION_JOIN")
                families.append("NO_EXPLICIT_FAMILY_IN_QUEUE_PROJECTION")
            links.update({l["source"] for l in x["linked_records"]})
            details.update(detail.keys())
        out[source]=dict(positions=len(subset),portrait=hist(portraits),motion=hist(motions),
            acquisition=hist(acquisitions),family=hist(families),
            formal_fields={k:hist(r["formal_fields"][k] for r in subset) for k in FORMAL},
            linked_source_position_counts=dict(sorted(links.items())),
            detail_key_position_counts=dict(sorted(details.items())))
        for k in ("portrait","motion","acquisition","family"):
            assert sum(out[source][k].values())==len(subset)
        assert all(sum(x.values())==len(subset) for x in out[source]["formal_fields"].values())
    cn=out["cn85_original"]
    assert cn["portrait"]=={"ORIGINAL_RD_LENGTH_DISCREPANCY":1,"ORIGINAL_RD_MULTIPLE_CANDIDATES":4,"ORIGINAL_RD_SINGLE_CANDIDATE":543}
    assert out["tw85_grid"]["motion"]=={"ALL_CANVAS_COMPLETE":1883,"SOME_CANVAS_COMPLETE":6}
    assert out["cn50"]["motion"]=={"ALL_CANVAS_COMPLETE":21,"ALL_STRICT":284}
    assert out["tw75"]["acquisition"]["STRICT_RESIDUAL_REVIEWED_NOT_CLOSED"]==67
    chronology=json.loads((ROOT/"research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json").read_bytes())
    years=chronology["yearly_work_queue"]
    assert len(years)==28 and not any(x["historically_complete"] for x in years)
    assert all(x["historical_species_count"] is None for x in years)
    assert hist(x["research_gate"] for x in years)=={"NOT_YEAR_AUDITED":1,"SOURCE_BOUNDED_REVIEWED":27}
    master=d["hf76"]
    master_grades=hist(x["selected_table_grade"] for x in master["rows"])
    assert len(master["rows"])==467 and len(master["configured_skill_definitions"])==38
    residual=json.loads((ROOT/"research/pets/PET-HIGH-FIRST-125-CN85-RESIDUAL-CROSSCHECK-R1.json").read_bytes())
    assert residual["metrics"]["unresolved_positions"]==22
    assert all(not x for x in residual["limits"].values())
    return dict(schema="stoneage.pet.whole_module_review.r1",scope="CLASSIC_PC_SOURCE_POSITIONS_NOT_UNIQUE_SPECIES",
        source_manifest_blob=blob((ROOT/"research/pets/PET-HIGH-FIRST-32-UNIFIED-SOURCE-LOOKUP-MANIFEST-R1.json").read_bytes()),
        manifest_sources=len(m["sources"]),lookup_occurrences=len(entries),queue_positions=len(rows),
        historical_queue_positions=len(v),by_source=out,
        formal_field_totals={k:hist(r["formal_fields"][k] for r in rows) for k in FORMAL},
        selected_master_grades=master_grades,configured_skill_definitions=len(master["configured_skill_definitions"]),
        supplementary_manifest_evidence={k:m[k] for k in ("supplement_hf76","supplement_hf87","supplement_hf91","supplement_hf93","supplement_hf95","supplement_hf96","supplement_hf99","supplement_pet124")},
        chronology=[dict(year=x["year"],research_gate=x["research_gate"],historically_complete=x["historically_complete"],historical_species_count=x["historical_species_count"]) for x in years],
        official_species_count=None,official_full_fields_certified=0,module_source_bounded_closed=False,original_runtime_verified=False,original_assets_published=False,
        limitations=["Queue is a selected audit cohort; additional linked and standalone documentary/skill/reward records exist outside it.",
                     "RD hash/candidate is not decoded pixels; SPR numeric match is not native selector; preserved rows are not authenticated deployments.",
                     "2026 YTD is open; source-bounded reviewed years are not historically complete.",
                     "Source availability/custody and remaining obtainable materials require separate final reconciliation before user acceptance."])
if __name__=="__main__":
    result=review()
    print("PET_WHOLE_REVIEW_PASS "+json.dumps({k:result[k] for k in ("manifest_sources","lookup_occurrences","queue_positions","formal_field_totals","selected_master_grades","configured_skill_definitions")},ensure_ascii=False,sort_keys=True))
    print("PET_WHOLE_VISUAL="+json.dumps({k:{f:v[f] for f in ("positions","portrait","motion","acquisition")} for k,v in result["by_source"].items()},ensure_ascii=False,sort_keys=True))
    Path("pet-whole-module-review.json").write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
