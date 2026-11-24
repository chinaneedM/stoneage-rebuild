"""Unified classic-PC pet evidence lookup. Source records remain independent; never infer species identity."""
import argparse, collections, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "research/pets/PET-HIGH-FIRST-32-UNIFIED-SOURCE-LOOKUP-MANIFEST-R1.json"
def read(path):
    return json.loads((ROOT / path).read_bytes())
def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
def load(verify=True):
    m=read(MANIFEST); d={}
    for k,s in m["sources"].items():
        raw=(ROOT/s["path"]).read_bytes()
        if verify:
            assert blob(raw)==s["git_blob"], (k,"source blob changed")
        d[k]=json.loads(raw)
        if s["expected_array"] is not None:
            assert len(d[k][s["expected_array"]])==s["expected_rows"], (k,"source count")
    return m,d
def resolve(d,source,pointer):
    x=d[source]
    for k in pointer:x=x[k]
    return x

def tw10_field_reference(witness, later, starter):
    """Compare attributed values without assigning server fields to the retail client."""
    observed = set()
    missing_web_elements = []
    invalid_web_elements = []
    acquisition = []
    for row in witness["exact_original_printed_name_web_witnesses"]:
        claim = row["player_submitted_four_element_claim_unverified"]
        ordinal = row["web_ordinal"]
        if not claim:
            missing_web_elements.append(ordinal)
        elif (
            set(claim) - set("地水火風")
            or any(type(v) is not int or not 0 <= v <= 10 for v in claim.values())
            or sum(claim.values()) != 10
        ):
            invalid_web_elements.append(ordinal)
        else:
            observed.add(tuple(claim.get(k, 0) * 10 for k in "地水火風"))
        if row["selected_player_claim"]:
            acquisition.append(dict(web_ordinal=ordinal, **row["selected_player_claim"]))

    candidates = []
    for row in later["server2016_candidates"]:
        # Exact numeric comparison includes both later tables' pet flag,
        # graphic, numeric template fields and seven skill slots.
        if row["crossarchive_mixed25_exact_numeric_matches"]:
            elements = tuple(row["source_elements"][k] for k in ("earth", "water", "fire", "wind"))
            candidates.append(dict(template_id=row["source_template_id"], elements=elements))
    later_ratios = {c["elements"] for c in candidates}
    if not observed:
        status = "INVALID_WEB_RATIO" if invalid_web_elements else "NO_WEB_RATIO"
    elif not later_ratios:
        status = "NO_STRICT_LATER_COMPARISON"
    elif observed == later_ratios and len(observed) == 1:
        status = "SINGLE_RATIO_AGREEMENT"
    elif observed & later_ratios:
        status = "AGREEMENT_WITH_VARIANTS"
    else:
        status = "DISJOINT_RATIOS"

    starter_reference = None
    if starter is not None:
        ratio = starter["historical_elements"]
        starter_reference = dict(
            village=starter["village"], reported_ratio=ratio,
            differs_from_all_valid_museum_ratios=tuple(ratio) not in observed if observed else None,
        )
    return dict(
        element_status=status, waei_2001_ratios=sorted(observed),
        missing_web_elements=missing_web_elements, invalid_web_elements=invalid_web_elements,
        later_candidates=candidates, acquisition_witnesses=acquisition,
        period_starter_witness=starter_reference,
    )

def build(d):
    out=[]
    def add(source,pointer,labels,role,keys=(),links=(),detail=None):
        labels=list(dict.fromkeys(x for x in labels if isinstance(x,str) and x.strip()))
        keys=list(dict.fromkeys(str(x) for x in keys if x is not None))
        out.append(dict(source=source,pointer=pointer,labels=labels,role=role,source_keys=keys,linked_records=list(links),detail=detail,official_same_deployment_identity_verified=False))
    def by_id(seq,field):
        res={}
        for i,x in enumerate(seq):
            k=x[field];assert k not in res,(field,k)
            res[k]=i
        return res
    def link(source,pointer,qualification):
        return dict(source=source,pointer=pointer,qualification=qualification)
    cnrows=d["cn50"]["records"]; cnid=by_id(cnrows,"ordinal")
    sina_by=collections.defaultdict(list)
    for i,x in enumerate(d["sina2003"]["rows"]):
        if x["cn50_album_ordinal_by_name_only"] in cnid:sina_by[x["cn50_album_ordinal_by_name_only"]].append(i)
    cn50_by_spr = collections.defaultdict(list)
    for i, row in enumerate(cnrows):
        for group in row["spr_groups"]:
            cn50_by_spr[(group["spr_group"], group["sha256"])].append(i)
    # Link by source-bound dossier ID and verify the original name/graphic
    # before comparing values. The later links do not establish species identity.
    album_by_graphic = by_id(d["tw10_album"]["records"], "graphic_number")
    museum_by_pet = by_id(d["tw10_waei2001"]["entries"], "pet_id")
    later_by_pet = by_id(d["tw10_later2016"]["dossiers"], "pet_id")
    starters = by_id(d["hf18"]["starters"], "name")
    for i,x in enumerate(d["tw10"]["records"]):
        pet_id, graphic, name = x["pet_id"], x["client_graphic"], x["client_name_original"]
        album_index = album_by_graphic[graphic]
        museum_index = museum_by_pet[pet_id]
        later_index = later_by_pet[pet_id]
        album = d["tw10_album"]["records"][album_index]
        witness = d["tw10_waei2001"]["entries"][museum_index]
        later = d["tw10_later2016"]["dossiers"][later_index]
        assert album["name_as_written"] == witness["tw10_original_name"] == later["tw10_name"] == name
        assert witness["source_tw10_graphic_number"] == later["tw10_graphic"] == graphic
        assert witness["source_tw10_name_row_sha256"] == album["source_row_sha256"]
        links = [
            link("tw10_album", ["records", album_index], "SAME_RETAIL_CLIENT_ROW"),
            link("tw10_waei2001", ["entries", museum_index], "PERIOD_NAME_ONLY_NOT_SAME_DEPLOYMENT"),
            link("tw10_later2016", ["dossiers", later_index], "LATER_NUMERIC_GRAPHIC_ONLY"),
        ]
        starter_index = starters.get(name)
        starter = None
        if starter_index is not None:
            starter = d["hf18"]["starters"][starter_index]
            links.append(link("hf18", ["starters", starter_index], "PERIOD_STARTER_NAME_ONLY"))
        reference = tw10_field_reference(witness, later, starter)
        reference["mainland_2003_catalogue_rows"] = []
        for cn_index in cn50_by_spr.get((graphic, album["spr_original_segment_sha256"]), ()):
            links.append(link("cn50", ["records", cn_index], "EXACT_SPR_ASSET_NOT_SERVER_IDENTITY"))
            for position in sina_by[cnrows[cn_index]["ordinal"]]:
                row = d["sina2003"]["rows"][position]
                links.append(link("sina2003", ["rows", position], "CN50_NAME_REFERENCE_VIA_SHARED_SPR_ASSET"))
                reference["mainland_2003_catalogue_rows"].append(dict(
                    page=row["page"], printed_number=row["printed_number"],
                    reported_elements=row["reported_elements"], rebirth_variant=row["rebirth_variant_label"],
                ))
        add("tw10", ["records", i], [name], "ORIGINAL_TW10_CLIENT_NAME_ASSET", [pet_id, graphic], links,
            dict(pet_id=pet_id, graphic=graphic, original_portrait_rd=x["original_portrait_rd"],
                 source_motion_sequences=x["source_motion_sequences"], dossier_path=x["dossier_path"],
                 formal_missing_fields=x["formal_missing_fields"], field_reference=reference))
    artid=by_id(d["cn50_art"]["records"],"cn50_album_ordinal")
    fusion_by=collections.defaultdict(list)
    for i,x in enumerate(d["fusion2003"]["records"]):fusion_by[x["cn50_album_ordinal"]].append(i)
    for i,x in enumerate(cnrows):
        o=x["ordinal"];ls=[]
        if o in artid:ls.append(link("cn50_art",["records",artid[o]],"SAME_SOURCE_ORDINAL_ART_REFERENCE"))
        ls.extend(link("sina2003",["rows",k],"PERIOD_NAME_ONLY_NOT_SAME_DEPLOYMENT") for k in sina_by[o])
        ls.extend(link("fusion2003",["records",k],"PERIOD_PANEL_NAME_LINK_NOT_MASTER") for k in fusion_by[o])
        add("cn50",["records",i],[x["compiled_name"]],"PRESERVED_CN50_COMPILED_ALBUM",[o,x["source_record_id"],*[z["spr_group"] for z in x["spr_groups"]]],ls,dict(graphic_groups=[z["spr_group"] for z in x["spr_groups"]],portrait_rd_sha256=x["portrait_lookup_rd_sha256"],source_motion_header_counts=[z["animation_header_count"] for z in x["spr_groups"]]))
    for program,branch in d["tw85_grid"]["programs"].items():
        for i,x in enumerate(branch["source_records"]):
            add("tw85_grid",["programs",program,"source_records",i],[x["original_name_cp950"]],"PRESERVED_TW85_PROGRAM_LOCAL_ALBUM",[x["slot"],x["source_portrait_alias"]],detail=dict(program=program,slot=x["slot"],portrait_alias=x["source_portrait_alias"]))
    visualid=by_id(d["tw85_visual"]["records"],"tw85_original_spr_no_not_official_pet_id")
    for i,x in enumerate(d["tw85_spr"]["records"]):
        g=x["tw85_original_spr_number"]
        for program,v in x["program_routes"].items():
            if v["record_source_status"]!="SOURCE_LOCAL_NAMED_ROUTE":continue
            ls=[link("tw85_visual",["records",visualid[g]],"SAME_PRESERVED_SPR_NUMBER_PROGRAM_ROUTES_AND_FRAME_REFERENCES")]
            add("tw85_spr",["records",i,"program_routes",program],[v["original_name_cp950"]],"PRESERVED_TW85_PROGRAM_NAMED_SPR_ROUTE",[g,v["local_album_slot"]],ls,dict(program=program,graphic=g,local_slot=v["local_album_slot"],cross_program_name_conflict=x["graphic_has_conflicting_names_across_installer_programs"]))
    birthid=by_id(d["tw75_birth"]["rows"],"template_id");compid=by_id(d["tw75_comparison"]["rows"],"template_id")
    for i,x in enumerate(d["tw75"]["pet_flag_1_field_projections"]):
        k=x["template_id"];b=d["tw75_birth"]["rows"][birthid[k]];e=d["tw75_comparison"]["rows"][compid[k]]
        assert b["source_row_sha256"]==x["row_sha256"]
        ls=[link("tw75_birth",["rows",birthid[k]],"CONDITIONAL_MODEL_NOT_OFFICIAL_STATS"),link("tw75_comparison",["rows",compid[k]],"LATER_COMPARISON_ENCOUNTER_NOT_ORIGINAL_CAPTURE")]
        add("tw75",["pet_flag_1_field_projections",i],[x["name"]],"CLAIMED_TW75_MASTER_TEMPLATE",[k,x["graphic"]],ls,dict(graphic=x["graphic"],template_id=k,elements=x["elements"],skill_slots=x["skill_slots"],conditional_lv1_panel=b["level1_unmodified_work_panel_marginal_ranges"],conditional_per_level_internal=b["per_level_internal_increment_marginal_ranges"],comparison_floor_ids=e["comparison_floor_ids"],comparison_status=e["comparison_status"]))
    # Historical observations are separate, even when names/identifiers coincide.
    for i,x in enumerate(d["sina2003"]["rows"]):
        o=x["cn50_album_ordinal_by_name_only"]
        labels=[cnrows[cnid[o]]["compiled_name"]] if o in cnid else []
        ls=[link("cn50",["records",cnid[o]],"NAME_ONLY_CATALOGUE_JOIN")] if o in cnid else []
        add("sina2003",["rows",i],labels,"PERIOD_2003_CATALOGUE_NAME_LINK" if labels else "UNRESOLVED_CATALOGUE_ROW",[x["printed_number"]],ls,dict(reported_elements=x["reported_elements"],level_one_acquisition_cell_has_text=x["level_one_acquisition_cell_has_text"],innate_skill_cell_has_text=x["innate_skill_cell_has_text"]))
    for i,x in enumerate(d["fusion2003"]["records"]):
        add("fusion2003",["records",i],[x["displayed_name"]],"PERIOD_FUSION_PANEL_SAMPLE",[x["printed_number"]])
    specs=[
      ("hf18","starters","name","STARTER_WITNESS"),("hf18","coordinate_cases","name","CAPTURE_WITNESS"),
      ("hf19","rows","name","PERIOD_ACQUISITION_NAME"),("hf19b","coordinate_cases","source_name","CAPTURE_WITNESS"),
      ("hf19c","rows","source_name","QUEST_GIFT_WITNESS"),("hf19d","rows","source_name","DIRECTORY_WITNESS"),
      ("hf20","rows","source_name","CAPSULE_WITNESS"),("hf21","rows","recollection_name","YEAR_BEAST_RECOLLECTION"),
      ("hf22","rows","name","JP_KR_NAMED_WITNESS"),("hf23","records","original_name","JP_KR_ACQUISITION_WITNESS"),
      ("hf23","appearance_only_relations","name","APPEARANCE_ONLY"),("hf23","unresolved_reward_labels","label","UNRESOLVED_REWARD_LABEL"),
      ("hf23","existing_named_dossier_attestations","name","ADDITIONAL_HISTORICAL_WITNESS"),
      ("hf24","rows","name","CN2010_PANEL_OR_REWARD_WITNESS"),("hf25","rows","name","2011_SOURCE_WITNESS"),
      ("hf26_27","rows","name","2012_2013_SOURCE_WITNESS"),("hf28_29","rows","name",None),("hf30_31","rows","name",None),("hf34","rows","name","PERIOD_CN2011_2012_FIELD_WITNESS"),("hf35","rows","name","PERIOD_CN2013_FIELD_WITNESS")]
    for source,arr,key,role in specs:
        for i,x in enumerate(d[source][arr]):
            add(source,[arr,i],[x.get(key)],role or x["role"],detail={k:x[k] for k in ("year","region","lane","version","version_lane","receipt","source_id","official_first_release") if k in x})
    # Supplementary historical field references; later unqualified realm claims
    # stay in the pinned research source, not in the active pet query.
    for i,x in enumerate(d["hf36"]["rows"]):
        if x["role"].startswith("UNQUALIFIED_"):
            continue
        add("hf36",["rows",i],[x["name"]],x["role"],detail={k:x[k] for k in ("year","region","source_id","claim")})
    return out
def summary(entries):
    return dict(source_record_occurrences=len(entries),literal_labels=len({n for x in entries for n in x["labels"]}),unlabelled_source_occurrences=sum(not x["labels"] for x in entries),by_source=dict(sorted(collections.Counter(x["source"] for x in entries).items())),by_role=dict(sorted(collections.Counter(x["role"] for x in entries).items())),official_species_count=None,warning="Source occurrences and literal labels are not distinct species, nor official first release.")
def search(entries,query,exact=False,variants=False,char_map=None,source=None):
    inv={v:k for k,v in (char_map or {}).items()};mp=char_map or {}
    qs=[query]
    if variants:qs=list(dict.fromkeys([query,"".join(mp.get(c,c) for c in query),"".join(inv.get(c,c) for c in query)]))
    for x in entries:
        if source and x["source"]!=source:continue
        # Source numbers only match exactly, never substring; labels may use substring.
        for i,q in enumerate(qs):
            if any(q.casefold()==n.casefold() if exact else q.casefold() in n.casefold() for n in x["labels"]) or q in x["source_keys"]:
                yield dict(x,match_type="LITERAL_QUERY" if i==0 else "EXPLICIT_SCRIPT_VARIANT_QUERY",matched_query=q)
                break
def verify(m,d,entries):
    assert {p:len(v["source_records"]) for p,v in d["tw85_grid"]["programs"].items()}==m["expected"]["tw85_grid_program_counts"]
    route=collections.Counter(x["detail"]["program"] for x in entries if x["source"]=="tw85_spr")
    assert dict(route)==m["expected"]["tw85_named_route_counts"]
    assert sum(x["original_portrait_rd"] is not None for x in d["tw10"]["records"])==120
    assert sum(x["original_portrait_rd"] is None for x in d["tw10"]["records"])==4
    assert not any(x["official_same_deployment_identity_verified"] for x in entries)
    for x in entries:
        resolve(d,x["source"],x["pointer"])
        for l in x["linked_records"]:resolve(d,l["source"],l["pointer"])
    assert len({(x["source"],tuple(x["pointer"])) for x in entries})==len(entries)
    assert len(list(search(entries,"蒙奇",exact=True)))>1
    assert len(list(search(entries,"PET-000001",exact=True,source="tw10")))==1
    tw10_refs = {x["detail"]["pet_id"]: x["detail"]["field_reference"] for x in entries if x["source"] == "tw10"}
    assert collections.Counter(r["element_status"] for r in tw10_refs.values()) == m["expected"]["tw10_element_reference_counts"]
    assert sum(len(r["acquisition_witnesses"]) for r in tw10_refs.values()) == 8
    assert tw10_refs["PET-000047"]["invalid_web_elements"] == [2]  # 凱比, total 4/10
    assert tw10_refs["PET-000115"]["missing_web_elements"] == [107]  # 黑烏力, blank
    assert tw10_refs["PET-000017"]["period_starter_witness"]["differs_from_all_valid_museum_ratios"] is True
    assert sum(r["period_starter_witness"] is not None for r in tw10_refs.values()) == 4
    assert {r["printed_number"] for r in tw10_refs["PET-000004"]["mainland_2003_catalogue_rows"]} == {4, 8}
    assert sum(bool(r["mainland_2003_catalogue_rows"]) for r in tw10_refs.values()) == 119
    assert sum(len(r["mainland_2003_catalogue_rows"]) for r in tw10_refs.values()) == 121
    assert all(
        sum(l["source"] == "cn50" for l in entry["linked_records"]) == 1
        for entry in entries if entry["source"] == "tw10"
    )
    for reference in tw10_refs.values():
        if reference["element_status"] == "DISJOINT_RATIOS":
            later_ratios = {c["elements"] for c in reference["later_candidates"]}
            assert any(
                row["reported_elements"] and tuple(
                    row["reported_elements"].get(key, 0) * 10 for key in ("earth", "water", "fire", "wind")
                ) in later_ratios for row in reference["mainland_2003_catalogue_rows"]
            )
    assert all(x["role"]!="PET_NAME_CANDIDATE" for x in search(entries,"馬年獸",exact=True,source="hf30_31"))
    assert len([x for x in entries if x["source"]=="hf30_31" and x["detail"].get("year")==2026 and x["role"]=="ITEM"])==7
    hf36=d["hf36"]["rows"]
    assert len(hf36)==48 and sum(x["role"].startswith("UNQUALIFIED_") for x in hf36)==13
    assert sum(x["source"]=="hf36" for x in entries)==35
    assert all(x["official_same_deployment_verified"] is False and x["official_native_pet_id"] is None and x["first_release_date"] is None for x in hf36)
    assert all(not resolve(d,x["source"],x["pointer"])["role"].startswith("UNQUALIFIED_") for x in entries if x["source"]=="hf36")
    assert {x["claim"]["lane"] for x in hf36 if x["name"]=="格鲁西斯"}=={"精灵觉醒2.5","特色8.5"}
    assert any(x["claim"].get("prior_source_for_2025") for x in hf36 if x["name"]=="奇格拉" and x["year"]==2016)
    assert any(x["claim"].get("prior_source_for_2025") for x in hf36 if x["name"]=="多格斯" and x["year"]==2016)
    assert m["expected"]["official_species_count"] is None and not m["original_assets_published"]
    print(json.dumps(summary(entries),ensure_ascii=False,indent=2))
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--query");p.add_argument("--exact",action="store_true");p.add_argument("--variants",action="store_true")
    p.add_argument("--source");p.add_argument("--full",action="store_true");p.add_argument("--summary",action="store_true");p.add_argument("--verify",action="store_true")
    args=p.parse_args();m,d=load();entries=build(d)
    if args.verify:verify(m,d,entries);return
    if args.source and args.source not in m["sources"]:p.error("unknown source ID")
    if args.summary or not args.query:print(json.dumps(summary(entries),ensure_ascii=False,indent=2));return
    rows=list(search(entries,args.query,args.exact,args.variants,d["hf30_31"]["character_map"],args.source))
    if args.full:
        for x in rows:
            x["original_source_record"]=resolve(d,x["source"],x["pointer"])
            x["linked_original_records"]=[dict(l,record=resolve(d,l["source"],l["pointer"])) for l in x["linked_records"]]
    print(json.dumps(dict(query=args.query,source_occurrences=len(rows),official_species_count=None,results=rows),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
