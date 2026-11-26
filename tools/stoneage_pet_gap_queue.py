"""PET-HIGH-FIRST-33: source-scoped field gap queue; no historical identity promotion."""
import argparse
from collections import Counter, defaultdict
import json
from stoneage_pet_source_lookup import load, build, resolve, search

FORMAL = ("official_native_id", "same_deployment_release", "birth_stats",
          "initial_ranges", "elements", "growth", "innate_skills",
          "capture", "award", "first_release_date", "encyclopedia_text")
CORE = {"tw10", "cn50", "tw85_grid", "tw75"}
LATE = {"hf25", "hf26_27", "hf28_29", "hf30_31"}

def present_arrays(obj):
    return isinstance(obj, dict) and any(isinstance(v, list) and v for v in obj.values())

def queue(d, entries, current=False):
    route_index = defaultdict(list)
    for x in entries:
        if x["source"] == "tw85_spr":
            r = resolve(d, x["source"], x["pointer"])
            p = x["detail"]["program"]
            route_index[(p, r["local_album_slot"], r["original_album_row_sha256"])].append(x)
    aliases = d["tw85_visual"]["portrait_alias_to_saved_tw85_native_rd_candidates"]
    result = []
    for e in entries:
        s, ptr = e["source"], e["pointer"]
        x = resolve(d, s, ptr)
        if s not in CORE | LATE | {"hf21", "hf22", "hf23", "hf34", "hf35"} and not (current and s=="cn85_original"):
            continue
        # Only independently named acquisition dossiers for Japan/Korea.
        # Appearance-only, generic rewards, and re-attestation rows stay in R32.
        if s == "hf23" and ptr[0] != "records":
            continue
        if s in {"hf28_29", "hf30_31"} and x["role"] != "PET_NAME_CANDIDATE":
            continue
        fields = {k: "NOT_CERTIFIED_SAME_DEPLOYMENT" for k in FORMAL}
        evidence = {}
        links = list(e["linked_records"])
        if s == "tw10":
            evidence = {"name": "ORIGINAL_CLIENT", "portrait": "ORIGINAL_RD" if x["original_portrait_rd"] is not None else "ORIGINAL_POSE_FALLBACK_ONLY", "motion": "ORIGINAL_SPR_INDEX"}
            evidence["field_reference"] = e["detail"]["field_reference"]
            fields["official_native_id"] = "CLIENT_GRAPHIC_AND_RESEARCH_ID_ONLY"
            priority = "P2_AUTHENTICATED_EARLY_CLIENT_SERVER_FIELDS"
        elif s == "cn50":
            evidence = {"name": "PRESERVED_COMPILED_ALBUM", "portrait": "PRESERVED_RD_HASH" if x["portrait_lookup_rd_sha256"] else "NOT_INDEXED_HERE", "motion": "PRESERVED_SPR_INDEX" if x["spr_groups"] else "NOT_INDEXED_HERE", "early_relation": x["earlier_tw10_relation"]}
            fields["official_native_id"] = "ALBUM_ORDINAL_AND_GRAPHIC_ONLY"
            for l in links:
                r = resolve(d,l["source"],l["pointer"])
                if l["source"] == "sina2003":
                    if r.get("level_one_acquisition_cell_has_text"): fields["capture"] = "PERIOD_ACQUISITION_CELL_NAME_LINK_ONLY"
                    if r.get("innate_skill_cell_has_text"): fields["innate_skills"] = "PERIOD_SKILL_CELL_NAME_LINK_ONLY"
                    if r.get("reported_elements"): fields["elements"] = "PERIOD_CATALOGUE_NAME_LINK_ONLY"
                if l["source"] == "fusion2003":
                    fields["birth_stats"] = "PERIOD_INDIVIDUAL_LV1_PANEL_NAME_LINK_ONLY"
            priority = "P2_PRESERVED_CN50_SERVER_AND_RELEASE_FIELDS"
        elif s == "cn85_original":
            detail=e["detail"]
            evidence={"name":"AUTHENTICATED_ORIGINAL_COMPILED_TABLE","portrait":detail["portrait_candidate_grade"],"motion":"ARITHMETIC_CANDIDATES_NOT_NATIVE_SELECTOR" if detail["ordinal_spr_candidates"] or detail["slot_spr_candidates"] else "NO_ARITHMETIC_CANDIDATE_NOT_ABSENT"}
            fields["official_native_id"]="COMPILED_SLOT_AND_FACE_ONLY"
            priority="P1_AUTHENTICATED_CN2012_SERVER_AND_NATIVE_SELECTOR_FIELDS"
        elif s == "tw85_grid":
            p = ptr[1]
            matches = route_index[(p,x["slot"],x["original_row_sha256"])]
            for r in matches:
                links.append({"source":r["source"],"pointer":r["pointer"],"qualification":"EXACT_PROGRAM_SLOT_AND_ORIGINAL_ROW_HASH"})
            a = aliases.get(str(x["source_portrait_alias"]), [])
            has_rd = any(z.get("native_exact_candidates") for z in a)
            evidence = {"name":"PRESERVED_PROGRAM_LOCAL_ALBUM",
                        "portrait":"EXTRA_SUBSET_EXACT_PATCH_RD_CANDIDATE" if has_rd else "NOT_ASSESSED_IN_EXTRA_SUBSET",
                        "motion":"EXTRA_SUBSET_NATIVE_ROUTE" if matches else "NOT_ASSESSED_IN_EXTRA_SUBSET",
                        "extra_subset_route_count":len(matches),
                        "program":p}
            if has_rd:
                links.append({"source":"tw85_visual","pointer":["portrait_alias_to_saved_tw85_native_rd_candidates",str(x["source_portrait_alias"])],"qualification":"PRESERVED_NATIVE_PATCH_RD_CANDIDATES_NOT_RENDERER_CHOICE"})
            fields["official_native_id"] = "PROGRAM_SLOT_AND_ALIAS_ONLY"
            priority = "P1_LATER_PC_NATIVE_SERVER_FIELDS"
        elif s == "tw75":
            detail = e["detail"]
            evidence = {"name":"CLAIMED_MASTER_ROW", "client_join_status":x["client_join_status"], "comparison_status":x["comparison_status"]}
            fields.update(official_native_id="CLAIMED_TEMPLATE_ID_ONLY", birth_stats="CONDITIONAL_MODEL_RANGE", initial_ranges="CONDITIONAL_MODEL_RANGE", elements="CLAIMED_MASTER_VALUES", growth="CONDITIONAL_MODEL_INCREMENT", innate_skills="CLAIMED_MASTER_SKILL_SLOTS", capture="LATER_COMPARISON_FLOOR_REFERENCE" if detail["comparison_floor_ids"] else "NOT_INDEXED_IN_COMPARISON")
            priority = "P1_AUTHENTICATE_CLAIMED_MASTER_DEPLOYMENT"
        elif s == "hf35":
            if x["acquisition"]["kind"] == "DIALOGUE_ONLY_NO_REWARD_ATTRIBUTION":
                continue
            evidence = {"name":"PERIOD_NAMED_FIELD_WITNESS", "source_ids":x["source_ids"],
                        "family":x["family"], "element_bar_observation":x["element_label"],
                        "period_skill":x["skill"], "period_acquisition":x["acquisition"]}
            if x["element_label"] is not None:
                fields["elements"] = "PERIOD_VISIBLE_BAR_NOT_NUMERIC_NATIVE_MASTER"
            if x["skill"]["label"] is not None:
                fields["innate_skills"] = "PERIOD_SKILL_CLAIM_NOT_INNATE_VERIFIED"
            if x["acquisition"]["kind"] not in {"PREVIEW_ACQUISITION_UNSPECIFIED"}:
                fields["award"] = "PERIOD_ACQUISITION_CLAIM_NOT_ACTUAL_GRANT"
            if x.get("panel"):
                evidence["status_sample"] = x["panel"]
                if x["panel"]["level"] == 1:
                    fields["birth_stats"] = "PERIOD_INDIVIDUAL_LV1_PANEL_NOT_RANGE"
            if x.get("growth_seal"):
                evidence["growth_seal"] = x["growth_seal"]
                fields["growth"] = "PERIOD_LEVEL_SEAL_CLAIM_NOT_FORMULA"
            priority = "P1_FREE_LATER_ORIGINAL_CLIENT"
        elif s == "hf34":
            evidence = {"name":"PERIOD_NAMED_FIELD_WITNESS",
                        "source_ids":x["source_ids"], "family":x["family"],
                        "reported_element_ratio":x["element_ratio"],
                        "reported_element_label":x["element_label"],
                        "period_skill":x["skill"], "period_acquisition":x["acquisition"]}
            if x["element_ratio"] is not None or x["element_label"] is not None:
                fields["elements"] = "PERIOD_REPORTED_ELEMENT_NOT_NATIVE_MASTER"
            if x["skill"]["label"] is not None:
                fields["innate_skills"] = "PERIOD_SKILL_CLAIM_NOT_INNATE_VERIFIED"
            fields["award"] = "PERIOD_EXCHANGE_OR_AUCTION_CLAIM"
            if x.get("panel"):
                fields["birth_stats"] = "PERIOD_INDIVIDUAL_LV1_PANEL_NOT_RANGE"
                evidence["status_sample"] = x["panel"]
            priority = "P1_FREE_LATER_ORIGINAL_CLIENT"
        elif s == "hf21":
            evidence = {"name":"LATE_RECOLLECTION_AND_CATALOGUE", "element_conflict":x["element_conflict"]}
            fields.update(initial_ranges="LATER_CATALOGUE_ONLY", elements="CONFLICTING_RECOLLECTION_CATALOGUE", growth="LATER_CATALOGUE_ONLY", innate_skills="LATER_CATALOGUE_ONLY", award="LATER_CATALOGUE_CLAIM_ONLY")
            priority = "P1_FREE_LATER_ORIGINAL_CLIENT"
        elif s in {"hf22","hf23"}:
            evidence = {"name":"REGIONAL_PERIOD_WITNESS", "region":x["region"], "visual_refs":len(x.get("images",x.get("visual_refs",[])))}
            fields["award"] = "REGIONAL_PERIOD_ACQUISITION_ATTESTATION_ONLY"
            priority = "P1_JP_KR_ORIGINAL_CLIENT_AND_MASTER"
        else:
            direct = present_arrays(x.get("direct"))
            related = present_arrays(x.get("stem_candidates")) or present_arrays(x.get("related_candidates"))
            evidence = {"name":"HISTORICAL_SOURCE_LABEL", "relation":"DIRECT_NAME_CANDIDATE" if direct else "RELATED_LABEL_CANDIDATE" if related else "NO_QUALIFIED_RESOURCE_MATCH_IN_R32", "role":x.get("role",x.get("source_class")), "year":x.get("year",2011 if s=="hf25" else None), "receipt":x.get("receipt")}
            priority = "P1_FREE_LATER_ORIGINAL_CLIENT" if not (direct or related) else "P2_VERIFY_HISTORICAL_NAME_LINK"
            if x.get("advertised_skill"): fields["innate_skills"] = "ADVERTISED_SKILL_NOT_INNATE"
            if x.get("reported_location"): fields["capture"] = "PERIOD_LOCATION_CLAIM_ONLY"
            if x.get("reported_element"): fields["elements"] = "PERIOD_ELEMENT_CLAIM_ONLY"
        result.append(dict(source=s,pointer=ptr,labels=e["labels"],source_keys=e["source_keys"],priority=priority,source_evidence=evidence,formal_fields=fields,linked_records=links,official_same_deployment_certified=False))
    return result

def summarize(rows):
    return dict(source_positions=len(rows),by_source=dict(Counter(r["source"] for r in rows)),
                priorities=dict(Counter(r["priority"] for r in rows)),
                official_species_count=None, official_full_fields_certified=0,
                scope="Source positions, not species; unassessed subset is not missing art.")

def verify(d, entries, rows):
    assert len({(r["source"],tuple(r["pointer"])) for r in rows})==len(rows)
    n=Counter(r["source"] for r in rows)
    assert {k:n[k] for k in CORE}=={"tw10":124,"cn50":305,"tw85_grid":1889,"tw75":467}
    assert n["hf21"]==8 and n["hf22"]==29 and n["hf23"]==8
    assert n["hf25"]==41 and n["hf26_27"]==43 and n["hf28_29"]==18 and n["hf30_31"]==54
    assert sum(r["source"]=="tw10" and r["source_evidence"]["portrait"]=="ORIGINAL_RD" for r in rows)==120
    tw10 = [r for r in rows if r["source"] == "tw10"]
    assert sum(len(r["source_evidence"]["field_reference"]["acquisition_witnesses"]) for r in tw10) == 8
    assert all(r["formal_fields"]["elements"] == "NOT_CERTIFIED_SAME_DEPLOYMENT" for r in tw10)
    assert all(r["source_evidence"]["portrait"]=="PRESERVED_RD_HASH" and r["source_evidence"]["motion"]=="PRESERVED_SPR_INDEX" for r in rows if r["source"]=="cn50")
    for p, expected in {"sa.exe":(207,182),"sb.exe":(190,182),"sc.exe":(106,106),"sd.exe":(182,182)}.items():
        subset=[r for r in rows if r["source"]=="tw85_grid" and r["pointer"][1]==p]
        assert sum(r["source_evidence"]["extra_subset_route_count"]>0 for r in subset)==expected[0]
        assert sum(r["source_evidence"]["portrait"]=="EXTRA_SUBSET_EXACT_PATCH_RD_CANDIDATE" for r in subset)==expected[1]
        assert sum(r["source_evidence"]["motion"]=="NOT_ASSESSED_IN_EXTRA_SUBSET" for r in subset)==301
    assert sum(r["source_evidence"].get("extra_subset_route_count",0) for r in rows)==1696
    assert all(r["official_same_deployment_certified"] is False and set(r["formal_fields"])==set(FORMAL) for r in rows)
    assert all(resolve(d,r["source"],r["pointer"]) is not None for r in rows)
    for r in rows:
        for l in r["linked_records"]: resolve(d,l["source"],l["pointer"])
    assert not any(r["source"] in {"hf28_29","hf30_31"} and resolve(d,r["source"],r["pointer"])["role"]!="PET_NAME_CANDIDATE" for r in rows)
    assert not any(r["source"]=="hf30_31" and resolve(d,r["source"],r["pointer"])["year"]==2026 for r in rows)
    assert n["hf34"]==16
    assert sum(x["element_ratio"] is not None for x in d["hf34"]["rows"])==6
    assert sum(bool(x.get("panel")) for x in d["hf34"]["rows"])==1
    assert all(x["official_same_deployment_verified"] is False and x["official_birth_range"] is None and x["first_release_date"] is None for x in d["hf34"]["rows"])
    panel = next(x["panel"] for x in d["hf34"]["rows"] if x["name"]=="蜜雪莉雅")
    assert [panel[k] for k in ("max_hp","attack","defense","agility")]==[69,15,7,14]
    assert n["hf35"]==13
    hf35=d["hf35"]["rows"]
    assert len(hf35)==14 and sum(x["acquisition"]["kind"]=="DIALOGUE_ONLY_NO_REWARD_ATTRIBUTION" for x in hf35)==1
    assert all(x["element_ratio"] is None and x["official_birth_range"] is None and x["official_same_deployment_verified"] is False for x in hf35)
    assert sum(x.get("panel",{}).get("level")==1 for x in hf35)==3
    assert sum(x.get("panel",{}).get("level")==140 for x in hf35)==1
    assert all(x["acquisition"]["individual_reward_mapping"] is None for x in hf35 if x["family"]=="蛇年兽公告具名组")
    assert len(rows)==3015, len(rows)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source");p.add_argument("--priority");p.add_argument("--query")
    p.add_argument("--all",action="store_true");p.add_argument("--verify",action="store_true")
    p.add_argument("--current",action="store_true",help="include PET124 authenticated original CN2012 positions")
    args=p.parse_args()
    m,d=load(); entries=build(d); rows=queue(d,entries,current=args.current)
    if args.verify:
        verify(d,entries,[r for r in rows if r["source"]!="cn85_original"])
        if args.current:
            cn=[r for r in rows if r["source"]=="cn85_original"]
            assert len(rows)==3563 and len(cn)==548
            assert Counter(r["source_evidence"]["portrait"] for r in cn)=={"ORIGINAL_RD_SINGLE_CANDIDATE":543,"ORIGINAL_RD_MULTIPLE_CANDIDATES":4,"ORIGINAL_RD_LENGTH_DISCREPANCY":1}
            assert all(not r["official_same_deployment_certified"] and set(r["formal_fields"])==set(FORMAL) for r in cn)
            for r in cn:
                for l in r["linked_records"]:resolve(d,l["source"],l["pointer"])
            print("PET124_CURRENT_GAP_QUEUE_PASS 3563 source positions; historical 3015 retained")
    if args.source: rows=[r for r in rows if r["source"]==args.source]
    if args.priority: rows=[r for r in rows if r["priority"]==args.priority]
    if args.query:
        hits={(r["source"],tuple(r["pointer"])) for r in search(entries,args.query,True,True,d["hf30_31"]["character_map"])}
        rows=[r for r in rows if (r["source"],tuple(r["pointer"])) in hits]
    out=summarize(rows)
    if args.all or args.query or args.priority or args.source: out["rows"]=rows
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
