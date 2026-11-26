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
    field_cases = by_id(d["hf38"]["rows"], "pet_id")
    field_cases39 = by_id(d["hf39"]["rows"], "pet_id")
    field_cases40 = by_id(d["hf40"]["rows"], "pet_id")
    field_cases41 = by_id(d["hf41"]["rows"], "pet_id")
    reward42_tw10 = {r["tw10_candidate"]["pet_id"]: r for r in d["hf42_cross"]["rows"] if r["tw10_candidate"] is not None}
    reward42_tw75 = {r["tw75_row_index"]: r for r in d["hf42_cross"]["rows"]}
    exchange43 = d["hf43"]["projection"]
    def exchange_links43(r):
        out = []
        for j, s in enumerate(exchange43["scripts"]):
            if any(r["award_instance_id"] in c["numeric_literals"] for c in s["commands"]):
                out.append(link("hf43", ["projection","scripts",j], "SAVED_EXCHANGE_CONTROL_AND_TOKEN_MULTIPLICITY_NOT_OFFICIAL_PROBABILITY"))
                item_ids = {int(v) for c in s["commands"] if r["award_instance_id"] in c["numeric_literals"] for v in c["fields"]["delitem"]}
                out.extend(link("hf43", ["projection","items",k], "CONFIGURED_EXCHANGE_ITEM_NOT_OFFICIAL_DEPLOYMENT") for k, v in enumerate(exchange43["items"]) if v["id"] in item_ids)
        for j, s in enumerate(d["hf44"]["rows"]):
            if r["award_instance_id"] in s["pet_slots"]:
                out.append(link("hf44", ["rows",j], "SAVED_WINDOW_AND_REWARD_SLOTS_NOT_OFFICIAL_EXECUTION"))
        return out
    def reward_links42(r, qualification):
        i = r["reward_row_index"]
        assert d["hf42"]["rows"][i]["award_instance_id"] == d["hf42_raw"]["rows"][i]["award_instance_id"] == r["award_instance_id"]
        return [link("hf42_cross", ["rows", i], qualification),
                link("hf42", ["rows", i], qualification),
                link("hf42_raw", ["rows", i], qualification),
                *[link("hf42_raw", ["scripts", j], "SAME_SAVED_SCRIPT_STATIC_REWARD_NOT_LIVE_ISSUE")
                  for j, s in enumerate(d["hf42_raw"]["scripts"])
                  if any(r["award_instance_id"] in c["numeric_literals"] for c in s["commands"])], *exchange_links43(r)]

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
        if pet_id in field_cases:
            case_index = field_cases[pet_id]
            case = d["hf38"]["rows"][case_index]
            assert (case["tw10_graphic"], case["original_client_name"]) == (graphic, name)
            links.append(link("hf38", ["rows", case_index], "PC_SOURCE_CASE_NOT_SAME_DEPLOYMENT"))
        if pet_id in field_cases39:
            case_index = field_cases39[pet_id]
            case = d["hf39"]["rows"][case_index]
            assert (case["tw10_graphic"], case["original_client_name"]) == (graphic, name)
            links.append(link("hf39", ["rows", case_index], "PC_SOURCE_CASE_NOT_SAME_DEPLOYMENT"))
        if pet_id in field_cases40:
            case_index = field_cases40[pet_id]
            case = d["hf40"]["rows"][case_index]
            assert (case["tw10_graphic"], case["original_client_name"]) == (graphic, name)
            links.append(link("hf40", ["rows", case_index], "PC_SOURCE_ACQUISITION_NOT_SAME_DEPLOYMENT"))
        if pet_id in field_cases41:
            case_index = field_cases41[pet_id]
            case = d["hf41"]["rows"][case_index]
            assert (case["tw10_graphic"], case["original_client_name"]) == (graphic, name)
            links.append(link("hf41", ["rows", case_index], "PC_SOURCE_GRAPHIC_CANDIDATE_NOT_SAME_DEPLOYMENT"))
            for idx in case["archive_template_row_indices"]:
                links.append(link("hf41_archive", ["projection", "capture_candidates", idx], "MIXED25_TEMPLATE_ROUTE_CANDIDATE_NOT_CAPTURE_PROOF"))
            for idx in case["award_row_indices"]:
                links.append(link("hf41_archive", ["projection", "award_commands", idx], "MIXED25_STATIC_AWARD_NOT_LIVE_ISSUE"))
        for j, t in enumerate(exchange43["templates"]):
            if t["graphic"] == graphic:
                links.append(link("hf43", ["projection","templates",j], "EXCHANGE_PREREQUISITE_TEMPLATE_GRAPHIC_CANDIDATE_NOT_IDENTITY"))
        if pet_id in reward42_tw10:
            r = reward42_tw10[pet_id]
            assert r["graphic"] == graphic and r["tw10_candidate"]["client_name"] == name
            links.extend(reward_links42(r, "SAVED_REWARD_NAME_GRAPHIC_CANDIDATE_NOT_SAME_DEPLOYMENT" if r["tw10_name_exact"] else "SAVED_REWARD_GRAPHIC_ONLY_NAME_CONFLICT_NOT_IDENTITY"))
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
    gap46 = by_id(d["hf46"]["rows"], "tw75_row_index")
    acquisition_updates = collections.defaultdict(list)
    for source, collection in (
        ("hf47", "period_links"), ("hf47", "context_only_links"),
        ("hf48", "rows"), ("hf48", "context"),
        ("hf49", "rows"), ("hf49", "context"),
    ):
        for ordinal, row in enumerate(d[source][collection]):
            acquisition_updates[row["tw75_row_index"]].append(
                link(source, [collection, ordinal], row["qualification"])
            )
    # Later acquisition supplements are linked to existing source positions, never new pets.
    for source, collections_to_link in (
        ("hf81", ("rows",)), ("hf82", ("rows", "conflicts")),
        ("hf83", ("rows", "context")), ("hf84", ("rows", "context")),
        ("hf85", ("rows", "starter_variants")), ("hf86", ("rows", "context")),
        ("hf87", ("rows", "residual")),
    ):
        for collection in collections_to_link:
            for ordinal, row in enumerate(d[source][collection]):
                i = row["tw75_row_index"]
                native = d["tw75"]["pet_flag_1_field_projections"][i]
                assert row["template_id"] == native["template_id"] and row["master_name"] == native["name"]
                if "row_sha256" in row:
                    assert row["row_sha256"] == native["row_sha256"]
                assert row["official_acquisition_verified"] is False
                grade = row.get("qualification", row.get("status", row.get("evidence", "CONTEXT_ONLY_NOT_QUALIFIED")))
                acquisition_updates[i].append(link(source, [collection, ordinal], grade))
    original50 = d["hf50"]["projection"]["records"]
    original50_index = by_id(original50, "tw75_row_index")
    trainer50 = by_id(d["hf50"]["projection"]["npc_source_files"], "path")["sa60/newbie/m_tiger"]
    trainer_instances = {
        instance_id
        for row in d["hf50"]["projection"]["npc_source_files"][trainer50]["candidate_lines"]
        if row["key"] == "AddPet" and row["qualification"] == "GETPET_OR_ADDPET_INSTANCE_LITERAL_CANDIDATE"
        for instance_id in row["matching_instance_tokens"]
    }
    variant52_by_position = {v["position"]: j for j, row in enumerate(d["hf52"]["rows"]) for v in row["master_variants"]}
    roles58 = collections.defaultdict(list)
    for j, row in enumerate(d["hf58"]["rows"]):
        roles58[row["position"]].append(link("hf58", ["rows", j], row["role"]))
        if row["related_position"] is not None:
            roles58[row["related_position"]].append(
                link("hf58", ["rows", j], "SHARED_GRAPHIC_WITH_SEPARATE_ROLE_CANDIDATE")
            )
    coverage57_by_position = by_id(d["hf57"]["rows"], "position")
    observations60 = d["hf60"]["observations"]
    sequences60 = observations60["sequences"]
    sequence60_by_group = by_id(sequences60, "physical_group")
    decoded_bitmaps60 = {
        int(bitmap) for bitmap, index in observations60["frame_bitmap_to_adrn_index"].items()
        if observations60["observed_blocks"][str(index)]["status"] == "DUAL_DECODED_INDEX_PIXELS"
    }
    residual62 = by_id(d["hf62"]["rows"], "position")
    variants63 = by_id(d["hf63"]["rows"], "position")
    skills61 = d["hf61"]
    skills61_by_position = by_id(skills61["rows"], "position")
    skill_definitions61 = by_id(skills61["configured_skill_definitions"], "skill_id")
    special56_by_position = by_id(d["hf56"]["rows"], "position")
    egg54_by_position = {row["position"]: j for j,row in enumerate(d["hf54"]["rows"])}
    reward53_by_position = {row["position"]: j for j,row in enumerate(d["hf53"]["rows"])}
    petabi51 = d["hf51_petabi"]["petabi_rows"]
    petabi_by_tw75 = collections.defaultdict(list)
    for ordinal, row in enumerate(petabi51):
        for ref in row["tw75_name_and_graphic_only_references"]:
            petabi_by_tw75[ref["position"]].append(ordinal)
    acquisition45 = d["hf45"]["projection"]
    route45 = by_id(acquisition45["mixed25_template_routes"], "template_id")
    area45 = by_id(acquisition45["area_metadata"], "id")
    instance45 = by_id(acquisition45["instance_metadata"], "id")
    floor45 = by_id(d["hf45_floor"]["rows"], "floor_id")
    master76 = d.get("hf76")
    definitions76 = by_id(master76["configured_skill_definitions"], "skill_id") if master76 else {}
    shop88 = d.get("hf88_skillshop")
    shop88_ids = by_id(shop88["source_skill_id_master_presence_candidates"], "skill_id") if shop88 else {}
    shop88_routes = collections.defaultdict(list)
    if shop88:
        for j, shop in enumerate(shop88["original_skillshop_CREATE_to_parameter_rows"]):
            for skill_id in set(shop["source_pet_skill_ids_ordered"]):
                shop88_routes[skill_id].append(j)
    special89 = d.get("hf89")
    special89_ids = by_id(special89["rows"], "skill_id") if special89 else {}
    joint90 = d.get("hf90")
    joint90_positions = by_id(joint90["rows"], "position") if joint90 else {}
    joint90_fusion = by_id(joint90["rows"], "fusion_index") if joint90 else {}
    excluded90 = {(r["position"], r["slot_index"]): j for j, r in enumerate(joint90["inheritance_rows"])} if joint90 else {}
    endpoint91 = d.get("hf91")
    endpoint91_positions = collections.defaultdict(list)
    if endpoint91:
        for j, row in enumerate(endpoint91["rows"]):
            endpoint91_positions[row["position"]].append(j)
    dated92 = d.get("hf92")
    dated92_positions = {r["position"]: j for j, r in enumerate(dated92["rows"])} if dated92 else {}
    families93 = d.get("hf93")
    families93_positions = collections.defaultdict(list)
    if families93:
        for j, row in enumerate(families93["rows"]):
            for candidate in row["candidates"]:
                families93_positions[candidate["position"]].append((j, candidate))
    witnesses77 = collections.defaultdict(list)
    for index, witness in enumerate(d.get("hf77", {}).get("rows", [])):
        witnesses77[witness["template_id"]].append((index, witness))
    horse78 = d.get("hf78")
    catalogue79 = by_id(d["hf79"]["pages"], "template_id") if "hf79" in d else {}
    birthid=by_id(d["tw75_birth"]["rows"],"template_id");compid=by_id(d["tw75_comparison"]["rows"],"template_id")
    for i,x in enumerate(d["tw75"]["pet_flag_1_field_projections"]):
        k=x["template_id"];b=d["tw75_birth"]["rows"][birthid[k]];e=d["tw75_comparison"]["rows"][compid[k]]
        assert b["source_row_sha256"]==x["row_sha256"]
        ls=[link("tw75_birth",["rows",birthid[k]],"CONDITIONAL_MODEL_NOT_OFFICIAL_STATS"),link("tw75_comparison",["rows",compid[k]],"LATER_COMPARISON_ENCOUNTER_NOT_ORIGINAL_CAPTURE")]
        for j, t in enumerate(exchange43["templates"]):
            if t["template_id"] == k and t["graphic"] == x["graphic"]:
                ls.append(link("hf43", ["projection","templates",j], "SAVED_EXCHANGE_PREREQUISITE_TEMPLATE_ID_GRAPHIC_NOT_DEPLOYMENT"))
        if i in reward42_tw75:
            r = reward42_tw75[i]
            assert (r["template_id"], r["graphic"], r["shared_template_row_sha256"]) == (k, x["graphic"], x["row_sha256"])
            ls.extend(reward_links42(r, "EXACT_SHARED_TEMPLATE_ROW_NOT_OFFICIAL_DEPLOYMENT"))
        ac = acquisition45["claimed_tw75_rows"][i]
        assert (ac["template_id"], ac["graphic"], ac["tw75_row_sha256"]) == (k, x["graphic"], x["row_sha256"])
        ls.append(link("hf45", ["projection","claimed_tw75_rows",i], ac["match_status"]+"_NOT_OFFICIAL_DEPLOYMENT"))
        floor_refs = []
        if ac["positive_route_count"]:
            j = route45[k]
            ls.append(link("hf45", ["projection","mixed25_template_routes",j], "SAVED_POSITIVE_SLOT_ROUTES_NOT_CAPTURE_PROOF"))
            # Direct area/instance links expose original source rows, level and coordinate data with --full.
            rr = acquisition45["mixed25_template_routes"][j]["routes"]
            ls.extend(link("hf45", ["projection","area_metadata",area45[aid]], "SAVED_AREA_COORDINATES_AND_NORMALIZED_FIELDS_NOT_NATIVE_RUNTIME") for aid in sorted({v[0] for v in rr}))
            ls.extend(link("hf45", ["projection","instance_metadata",instance45[eid]], "SAVED_INSTANCE_LEVEL_AND_PET_FLAG_NOT_CAPTURE_PROOF") for eid in sorted({v[4] for v in rr}))
            for fid in ac["double_flag_floor_ids"]:
                fi = floor45[fid]
                fr = d["hf45_floor"]["rows"][fi]
                nm = fr["later_recovered_name"]
                floor_refs.append(dict(floor_id=fid,recovered_name_candidate=nm["display_name_candidate"] if nm else None,same_archive_dat_present=fr["same_archive_dat"] is not None))
                ls.append(link("hf45_floor", ["rows",fi], "SAME_ARCHIVE_DAT_AND_SEPARATE_RECOVERED_NAME_REFERENCE"))
        gap_detail = None
        if i in gap46:
            gi = gap46[i]
            gap = d["hf46"]["rows"][gi]
            assert not ac["double_pet_flag_route_count"] and gap["row_sha256"] == x["row_sha256"]
            ls.append(link("hf46", ["rows",gi], "SOURCE_SCOPED_ACQUISITION_GAP_NOT_OFFICIAL_RELEASE"))
            for ref in gap["period_guide_refs"]:
                ls.append(link("hf19c", ["rows",ref["row_index"]], "PERIOD_GUIDE_CLAIM_NOT_OFFICIAL_ACQUISITION"))
            for ref in gap["capsule_refs"]:
                ls.append(link("hf20", ["rows",ref["row_index"]], "CAPSULE_SOURCE_ASSOCIATION_NOT_ACTUAL_GRANT"))
            for ref in gap["additional_refs"]:
                ls.append(link(ref["source"], ["records" if ref["source"] == "fusion2003" else "rows",ref["row_index"]], ref["qualification"]))
            gap_detail = dict(gap_state=gap["gap_state"],evidence_categories=gap["evidence_categories"],selected_table=gap["selected_table"]["status"],alternate_table=gap["alternate_table"]["status"],official_acquisition_verified=False)
        ls.extend(acquisition_updates[i])
        ls.extend(roles58[i])
        if i in coverage57_by_position:
            j57 = coverage57_by_position[i]
            r57 = d["hf57"]["rows"][j57]
            assert (r57["template_id"], r57["graphic"], r57["master_row_sha256"]) == (k, x["graphic"], x["row_sha256"])
            ls.append(link("hf57", ["rows", j57], "SAME_NUMBER_PHYSICAL_ASSET_AND_INDEPENDENT_NAME_EVIDENCE_NOT_OFFICIAL_IDENTITY"))
            for group in r57["tw85_physical_groups"]:
                j60 = sequence60_by_group.get(group["group_index"])
                if j60 is None:
                    continue
                sample = sequences60[j60]
                assert (sample["spr"], sample["spr_segment_sha256"]) == (group["graphic"], group["segment_sha256"])
                bitmaps = {frame[0] for frame in sample["frames"] if frame[0] is not None}
                qualification = ("SAVED_TW85_COMPLETE_DUAL_DECODED_INDEX_PIXEL_SAMPLE"
                                 if bitmaps and bitmaps <= decoded_bitmaps60
                                 else "SAVED_TW85_INDEX_PIXEL_SAMPLE_HAS_UNSUPPORTED_BLOCKS")
                ls.append(link("hf60", ["observations", "sequences", j60], qualification))
        for source, positions in (("hf62", residual62), ("hf63", variants63)):
            if i in positions:
                j = positions[i]
                row = d[source]["rows"][j]
                assert (row["template_id"], row["graphic"], row["row_sha256"]) == (k, x["graphic"], x["row_sha256"])
                ls.append(link(source, ["rows", j], "SOURCE_BOUNDED_RESIDUAL_REVIEW_NOT_OFFICIAL_ACQUISITION"))
        if i in skills61_by_position:
            j61 = skills61_by_position[i]
            row61 = skills61["rows"][j61]
            assert (row61["template_id"], row61["graphic"], row61["row_sha256"]) == (k, x["graphic"], x["row_sha256"])
            slots61 = row61["scope"]["petskill.txt"]
            ls.append(link("hf61", ["rows", j61], slots61["template_match"] + "_SAVED_MIXED25_SKILL_REFERENCE"))
            for skill_id in sorted({slot["skill_id"] for slot in slots61["source_slots"]}):
                ls.append(link("hf61", ["configured_skill_definitions", skill_definitions61[skill_id]],
                               "SAVED_MIXED25_CONFIGURED_SKILL_DEFINITION_NOT_OFFICIAL_EFFECT"))
        if i in special56_by_position:
            j56 = special56_by_position[i]
            r56 = d["hf56"]["rows"][j56]
            assert (r56["template"], r56["graphic"], r56["name"]) == (k, x["graphic"], x["name"])
            ls.append(link("hf56", ["rows", j56], r56["qualification"]))
            if "preflight_index" in r56:
                ls.append(link("hf56_preflight", ["rows", r56["preflight_index"]], "LATER_COMPARISON_ROLE_NOT_OFFICIAL_DEPLOYMENT"))
            for h56 in r56["source_hit_indices"]:
                ls.append(link("hf56_replay", ["scan", "typed_candidate_lines", h56], "SAVED_TYPED_REFERENCE_CANDIDATE_NOT_OFFICIAL_AWARD"))
        if i in egg54_by_position:
            j54 = egg54_by_position[i]
            ls.append(link("hf54", ["rows", j54], d["hf54"]["rows"][j54]["grade"]))
        if i in reward53_by_position:
            j53 = reward53_by_position[i]
            ls.append(link("hf53", ["rows", j53], d["hf53"]["rows"][j53]["grade"]))
        if i in variant52_by_position:
            ls.append(link("hf52", ["rows", variant52_by_position[i]], "NAMED_VISUAL_AND_ACQUISITION_VARIANT_COMPARISON_NOT_SAME_DEPLOYMENT"))
        ls.extend(link("hf51_petabi", ["petabi_rows", j],
                       "SAVED_VIP_PRESET_NAME_AND_GRAPHIC_ONLY_NOT_SAME_TEMPLATE")
                  for j in petabi_by_tw75[i])
        if i in original50_index:
            j = original50_index[i]
            original = original50[j]
            assert (original["template_id"], original["row_sha256"]) == (k, x["row_sha256"])
            ls.append(link("hf50", ["projection", "records", j],
                           "SAVED_SELECTED_AND_ALTERNATE_TABLES_NOT_OFFICIAL_ACQUISITION"))
            selected = original["source_pairs"][0]
            if selected["match"] == "EXACT_ROW" and any(
                ins["instance_id"] in trainer_instances for ins in selected["instances"]
            ):
                ls.append(link("hf50", ["projection", "npc_source_files", trainer50],
                               "SAVED_LV1_TRAINER_REWARD_CONFIGURATION_NOT_OFFICIAL_AWARD"))
        saved_acquisition = dict(gap_classification=gap_detail,match_status=ac["match_status"],positive_route_count=ac["positive_route_count"],double_pet_flag_route_count=ac["double_pet_flag_route_count"],lv1_double_flag_route_count=ac["lv1_double_flag_route_count"],floor_candidates=floor_refs,official_acquisition_verified=False)
        detail = dict(graphic=x["graphic"], template_id=k, elements=x["elements"], skill_slots=x["skill_slots"],
                      conditional_lv1_panel=b["level1_unmodified_work_panel_marginal_ranges"],
                      conditional_per_level_internal=b["per_level_internal_increment_marginal_ranges"],
                      comparison_floor_ids=e["comparison_floor_ids"], comparison_status=e["comparison_status"],
                      saved_mixed25_acquisition=saved_acquisition)
        if master76:
            row = master76["rows"][i]
            assert (row["position"], row["template_id"], row["graphic"], row["row_sha256"]) == (i, k, x["graphic"], x["row_sha256"])
            grade = row["selected_table_grade"]
            exact = grade == "EXACT_SHARED_TEMPLATE_ROW"
            ls.append(link("hf76", ["rows", i], grade + "_PRESERVED_SELECTED_TABLE"))
            skills = []
            shop_links = set()
            for slot in row["configured_skill_slots"]:
                j = definitions76[slot["skill_id"]]
                definition = master76["configured_skill_definitions"][j]
                skill = dict(slot_index=slot["slot_index"], skill_id=slot["skill_id"], name=definition["name"])
                if shop88:
                    sid = slot["skill_id"]
                    same_definition = sid in shop88_ids and (
                        shop88["source_skill_id_master_presence_candidates"][shop88_ids[sid]]["primary_petskill_txt"]["row_sha256"]
                        == definition["row_sha256"])
                    routes = shop88_routes[sid] if same_definition else []
                    skill["saved_skillshop_reference"] = dict(
                        qualification="EXACT_PRIMARY_SKILL_ROW_AND_SAVED_SHOP_LIST" if routes else "NO_EXACT_REFERENCE_IN_SELECTED_21_SHOPS",
                        shop_indices=routes,
                        species_can_learn_verified=False, official_runtime_verified=False)
                    shop_links.update(routes)
                if slot["skill_id"] in special89_ids:
                    special_index = special89_ids[slot["skill_id"]]
                    ref = special89["rows"][special_index]
                    assert ref["definition_sha256"] == definition["row_sha256"]
                    assert any(p["position"] == i and p["template_sha256"] == x["row_sha256"]
                               and p["slot_index"] == slot["slot_index"] for p in ref["configured_positions"])
                    skill["period_special_skill_reference"] = dict(
                        qualification="DATED_SKILL_LEVEL_REFERENCE" if any(
                            w["kind"] != "ITEM_ROLE_CONTEXT_ONLY" for w in ref["witnesses"])
                            else "ITEM_CONTEXT_ONLY" if ref["witnesses"] else "NO_QUALIFIED_PERIOD_REFERENCE_IN_BATCH",
                        same_deployment_verified=False)
                    ls.append(link("hf89", ["rows", special_index], "SPECIAL_SKILL_REFERENCE_NOT_OFFICIAL_LEARNABILITY"))
                if (i, slot["slot_index"]) in excluded90:
                    ix = excluded90[(i, slot["slot_index"])]
                    exclusion = joint90["inheritance_rows"][ix]
                    assert exclusion["skill_id"] == slot["skill_id"]
                    skill["later_comparison_fusion_exclusion"] = dict(
                        qualification=exclusion["qualification"], same_deployment_verified=False)
                    ls.append(link("hf90", ["inheritance_rows", ix], "NUMERIC_EXCLUSION_LATER_COMPARISON_ONLY"))
                    ls.append(link("hf55_fusion", ["comparison", "flow", "excluded_inheritance_skill_ids"], "LATER_COMPARISON_NOT_OFFICIAL_INHERITANCE"))
                skills.append(skill)
                ls.append(link("hf76", ["configured_skill_definitions", j], "SAVED_CONFIGURED_SKILL_NOT_BIRTH_SKILL_PROOF"))
            for j in sorted(shop_links):
                ls.append(link("hf88_skillshop", ["original_skillshop_CREATE_to_parameter_rows", j],
                               "SAVED_SKILL_SHOP_LIST_NOT_SPECIES_LEARNABILITY_OR_OFFICIAL_RUNTIME"))
            detail["saved_selected_master_fields"] = dict(
                qualification=grade, selected_row_sha256=row["selected_row_sha256"],
                matched_birth_inputs={key: x[key] for key in ("base", "initnum", "lvup_literal")} if exact else None,
                fields_differing_from_claim=row["selected_fields_differing_from_claim"],
                configured_skill_slots=skills, saved_reward_instance_id=row["saved_reward_instance_id"],
                official_deployment_verified=False,
            )
        if i in joint90_positions:
            ix = joint90_positions[i]
            joint = joint90["rows"][ix]
            assert joint["template_row_sha256"] == x["row_sha256"]
            detail["conditional_joint_panel_witness"] = dict(
                observed_panel=joint["observed_panel"], qualification=joint["qualification"],
                official_birth_verified=False, official_fusion_verified=False)
            ls.append(link("hf90", ["rows", ix], "JOINT_MODEL_COMPATIBILITY_ONLY"))
            ls.append(link("fusion2003", ["records", joint["fusion_index"]], "PERIOD_FUSION_PANEL_NOT_NATURAL_BIRTH_PROOF"))
        if i in endpoint91_positions:
            refs = [endpoint91["rows"][j] for j in endpoint91_positions[i]]
            detail["conditional_endpoint_growth_witnesses"] = dict(
                sample_count=len(refs), both_witnesses=sum(r["claimed_witness"] is not None and r["saved_witness"] is not None for r in refs),
                claimed_witnesses=sum(r["claimed_witness"] is not None for r in refs),
                saved_witnesses=sum(r["saved_witness"] is not None for r in refs),
                official_variant_resolved=False, original_rolls_observed=False,
                null_witness_is_exclusion=False)
            for j in endpoint91_positions[i]:
                ls.append(link("hf91", ["rows", j], "CONDITIONAL_ENDPOINT_WITNESS_NOT_OBSERVED_GROWTH"))
        if i in dated92_positions:
            ix = dated92_positions[i]
            dated = dated92["rows"][ix]
            assert dated["template_row_sha256"] == x["row_sha256"]
            detail["dated_catalogue_crosswalk"] = dict(
                grade=dated["grade"], catalogue_date="2003-04-07", official_release_verified=False,
                first_release_date=None)
            ls.append(link("hf92", ["rows", ix], "DATED_CATALOGUE_COMPATIBILITY_NOT_OFFICIAL_RELEASE"))
            for ref in dated["refs"]:
                ls.append(link("sina2003", ["rows", ref["catalogue_index"]], "DATED_CATALOGUE_CANDIDATE_" + dated["grade"]))
        if i in families93_positions:
            refs = families93_positions[i]
            detail["dated_family_references"] = []
            for j, candidate in refs:
                claim = families93["rows"][j]
                assert candidate["template_row_sha256"] == x["row_sha256"]
                detail["dated_family_references"].append(dict(
                    family=claim["family"], source_date=families93["sources"][claim["source"]]["date"],
                    element_status=candidate["element_status"], official_family_verified=False))
                ls.append(link("hf93", ["rows", j], "SOURCE_FAMILY_LABEL_" + candidate["element_status"]))
        for index, witness in witnesses77.get(k, []):
            assert x["name"] == witness["name"]
            ls.append(link("hf77", ["rows", index], "REPOSTED_PLAYER_PANEL_NAME_WITNESS_NOT_SAME_DEPLOYMENT"))
        if horse78 and k == horse78["template_id"]:
            assert x["name"] == horse78["name"]
            ls.extend(link("hf78", ["posts", j], "DATED_PLAYER_PANEL_NAME_WITNESS_NOT_SAME_DEPLOYMENT")
                      for j in range(len(horse78["posts"])))
            ls.append(link("hf78", ["photo"], "PLAYER_SCREENSHOT_FINAL_PANEL_ONLY"))
        if k in catalogue79:
            ls.append(link("hf79", ["pages", catalogue79[k]], "UNDATED_PLAYER_CATALOGUE_PANELS_NOT_SAME_DEPLOYMENT"))
        add("tw75", ["pet_flag_1_field_projections", i], [x["name"]], "CLAIMED_TW75_MASTER_TEMPLATE", [k, x["graphic"]], ls, detail)
    for i, row in enumerate(petabi51):
        add("hf51_petabi", ["petabi_rows", i], [row["template_name"], row["instance_name"]],
            "PRESERVED_VIP_PRESET_PET_CANDIDATE" if row["instance_pet_flag"] == row["template_pet_flag"] == 1
            else "PRESERVED_VIP_PRESET_INSTANCE_FLAG_CONFLICT",
            [row["instance_id"], row["template_id"], row["graphic_no"]],
            [link("tw75", ["pet_flag_1_field_projections", ref["position"]],
                  "SAVED_VIP_PRESET_NAME_AND_GRAPHIC_ONLY_NOT_SAME_TEMPLATE")
             for ref in row["tw75_name_and_graphic_only_references"]],
            dict(instance_id=row["instance_id"], template_id=row["template_id"], graphic=row["graphic_no"],
                 vip_points=row["vip_points"], official_acquisition_verified=False))
    # Historical observations are separate, even when names/identifiers coincide.
    for i,x in enumerate(d["sina2003"]["rows"]):
        o=x["cn50_album_ordinal_by_name_only"]
        labels=[cnrows[cnid[o]]["compiled_name"]] if o in cnid else []
        ls=[link("cn50",["records",cnid[o]],"NAME_ONLY_CATALOGUE_JOIN")] if o in cnid else []
        add("sina2003",["rows",i],labels,"PERIOD_2003_CATALOGUE_NAME_LINK" if labels else "UNRESOLVED_CATALOGUE_ROW",[x["printed_number"]],ls,dict(reported_elements=x["reported_elements"],level_one_acquisition_cell_has_text=x["level_one_acquisition_cell_has_text"],innate_skill_cell_has_text=x["innate_skill_cell_has_text"]))
    for i,x in enumerate(d["fusion2003"]["records"]):
        ls = []
        if i in joint90_fusion:
            ix = joint90_fusion[i]
            ls = [link("hf90", ["rows", ix], "JOINT_MODEL_COMPATIBILITY_ONLY"),
                  link("tw75", ["pet_flag_1_field_projections", joint90["rows"][ix]["position"]], "NAME_ELEMENT_COMPATIBILITY_NOT_SAME_DEPLOYMENT")]
        add("fusion2003",["records",i],[x["displayed_name"]],"PERIOD_FUSION_PANEL_SAMPLE",[x["printed_number"]],ls)
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
    if "hf94" in d:
        for j, row in enumerate(d["hf94"]["rows"]):
            targets = [("tw85_grid", ["programs", c["program"], "source_records", c["index"]]) for c in row["grid_candidates"]]
            if row["older_cn_reference"]:
                ref = row["older_cn_reference"]
                targets.append((ref["source"], ref["pointer"]))
            for e in out:
                if (e["source"], e["pointer"]) in targets:
                    e["linked_records"].append(link("hf94", ["rows", j], "LATE_NAME_CATALOGUE_REFERENCE_NOT_SAME_DEPLOYMENT"))
            ls = [link("hf93", ["rows", row["family_claim_index"]], "DATED_FAMILY_LABEL_NOT_NATIVE_CODE")]
            ls.extend(link(src, pointer, "EXACT_NAME_REFERENCE_NOT_OFFICIAL_IDENTITY") for src, pointer in targets)
            add("hf94", ["rows", j], [row["name"]], "LATE_COMMUNITY_CATALOGUE_REFERENCE", [],
                ls, dict(family=row["family"], catalogue=row["catalogue"], official_identity_verified=False))
    if "hf99" in d:
        positions99 = {e["pointer"][1]: e for e in out if e["source"] == "tw75"}
        for j, row in enumerate(d["hf99"]["rows"]):
            for side in ("left", "right"):
                positions99[row[side]["position"]]["linked_records"].append(
                    link("hf99", ["rows", j], "CONDITIONAL_MARGINAL_VARIANT_NOT_OFFICIAL_IDENTITY"))
    if "hf98" in d:
        positions98 = {e["pointer"][1]: e for e in out if e["source"] == "tw75"}
        for j, row in enumerate(d["hf98"]["rows"]):
            for side in ("left", "right"):
                positions98[row[side]["position"]]["linked_records"].append(
                    link("hf98", ["rows", j], "SAVED_SKILL_VARIANT_NOT_OFFICIAL_BIRTH"))
    if "hf97" in d:
        positions97 = {e["pointer"][1]: e for e in out if e["source"] == "tw75"}
        for j, row in enumerate(d["hf97"]["rows"]):
            for side in ("left", "right"):
                positions97[row[side]["position"]]["linked_records"].append(
                    link("hf97", ["rows", j], row["qualification"]))
    if "hf96" in d:
        by_position = {e["pointer"][1]: e for e in out if e["source"] == "tw75"}
        for j, row in enumerate(d["hf96"]["rows"]):
            for side in ("left", "right"):
                by_position[row[side]["position"]]["linked_records"].append(
                    link("hf96", ["rows", j], "SAME_NAME_OR_GRAPHIC_NOT_IDENTITY"))
    if "hf95" in d:
        for j, row in enumerate(d["hf95"]["rows"]):
            for e in out:
                if e["source"] == "hf94" and e["pointer"] == ["rows", row["hf94_index"]]:
                    e["linked_records"].append(link("hf95", ["rows", j], row["role"]))
    if "hf74" in d:
        attach_visual(d, out)
    if "hf101" in d:
        attach_cn50_motion(d, out)
    if "cn85_original" in d:
        attach_cn85_original(d, out, add, link)
    if "review_tw75_portrait" in d and "review_residual_visual" in d:
        attach_review_visual(d, out, link)
    return out

def attach_review_visual(d, entries, link):
    portraits=d["review_tw75_portrait"]
    residual=d["review_residual_visual"]
    assert not any(portraits["limits"].values()) and not any(residual["limits"].values())
    tw75_residual={r["index"]:(i,r) for i,r in enumerate(residual["tw75_rows"])}
    cn85_residual={r["ordinal"]:(i,r) for i,r in enumerate(residual["cn85_rows"])}
    for e in entries:
        if e["source"]=="tw75":
            i=e["pointer"][1]; r=portraits["rows"][i]
            original=resolve(d,"tw75",e["pointer"])
            assert r["index"]==i and r["row_sha256"]==original["row_sha256"]
            e["detail"]["review_portrait_reference"]={k:r[k] for k in ("grade","portrait_aliases","portrait_rows","exact_positions")}
            e["detail"]["review_portrait_reference"]["same_build_verified"]=False
            e["linked_records"].append(link("review_tw75_portrait",["rows",i],"CROSS_CARRIER_REFERENCE_NOT_SAME_BUILD_PORTRAIT"))
            if i in tw75_residual:
                j,z=tw75_residual[i]
                e["detail"]["review_portrait_conflict"]={k:z[k] for k in ("grade","tw85_aliases","tw85_graphics","cn85_exact_name_face_rd_ordinals")}
                e["linked_records"].append(link("review_residual_visual",["tw75_rows",j],"GRAPHIC_CONFLICT_OR_NO_QUALIFIED_NAME_NOT_IDENTITY"))
        elif e["source"]=="cn85_original":
            o=e["detail"]["physical_ordinal"]
            if o in cn85_residual:
                j,r=cn85_residual[o]
                assert not e["detail"]["ordinal_spr_candidates"] and not e["detail"]["slot_spr_candidates"]
                assert r["name"]==e["labels"][0] and r["face"]==e["detail"]["compiled_face"]
                e["detail"]["review_motion_reference"]={"grade":r["grade"],"cn50_positions":[x["ordinal"] for x in r["cn50"]],"tw85_positions":[x["position"] for x in r["tw85"]],"native_selector_verified":False}
                e["linked_records"].append(link("review_residual_visual",["cn85_rows",j],"EXACT_CROSS_CARRIER_RD_SPR_REFERENCE_NOT_NATIVE_SELECTOR"))

def attach_cn85_original(d, entries, add, link):
    full=d["cn85_original"]["analysis"]
    a,b=full["programs"]
    assert full["table_full_span_equal"] and a["entries"]==b["entries"]
    old=d["cn50_cn85_crosswalk"]["rows"]
    visual={x["ordinal"]:(i,x) for i,x in enumerate(full["resource_links"]["rows"])}
    inherited={x["cn50_ordinal"]:(i,x) for i,x in enumerate(d["cn50_cn85_spr_inheritance"]["rows"])}
    names=collections.defaultdict(list)
    for i,x in enumerate(old):
        if x["cn50"]["slot"]>=0:
            names[x["cn50"]["name"]].append(i)
    for e in entries:
        if e["source"]!="cn50":continue
        x=resolve(d,"cn50",e["pointer"])
        o=x["ordinal"]
        i,v=visual[o]
        j,z=inherited[o]
        assert old[o]["cn50"]["name"]==x["compiled_name"]==z["cn50_name"]
        e["detail"]["cn85_compiled_crosswalk"]=old[o]
        e["detail"]["cn85_exact_spr_reference"]=z["groups"]
        e["detail"]["cn85_same_ordinal_rd_reference"]=dict(same_label=x["compiled_name"]==v["compiled_label"],exact_rd_hash=any(y["rd_sha256"]==x["portrait_lookup_rd_sha256"] for y in v["face_map_number_candidates"]),identity_verified=False)
        e["linked_records"].extend([link("cn50_cn85_crosswalk",["rows",o],"COMPILED_FIELDS_ONLY_NOT_SERVER_IDENTITY"),link("cn50_cn85_spr_inheritance",["rows",j],"EXACT_OLD_SPR_SEGMENTS_NOT_NATIVE_SELECTOR"),link("cn85_original",["analysis","resource_links","rows",i],"SAME_ORDINAL_RD_COMPARISON_NOT_IDENTITY")])
    for o,x in enumerate(a["entries"]):
        if not x["strict_old_parser"] or x["slot"]<0:continue
        i,v=visual[o]
        assert all(x[k]==v[k] for k in ("ordinal","slot","face","compiled_label"))
        links=[link("cn85_original",["analysis","programs",1,"entries",o],"EXACT_SECOND_PROGRAM_COMPILED_TABLE_NOT_RUNTIME"),link("cn85_original",["analysis","resource_links","rows",i],"ORIGINAL_RD_MAP_NUMBER_CANDIDATES_NOT_RENDERED")]
        for j in names[x["compiled_label"]]:
            links.append(link("cn50_cn85_crosswalk",["rows",j],"SAME_COMPILED_NAME_NOT_SERVER_IDENTITY"))
        if o<len(old) and old[o]["cn50"]["name"]!=x["compiled_label"]:
            links.append(link("cn50_cn85_crosswalk",["rows",o],"SAME_PHYSICAL_POSITION_DIFFERENT_COMPILED_LABEL"))
        if o in inherited:
            links.append(link("cn50_cn85_spr_inheritance",["rows",inherited[o][0]],"EXACT_OLD_SPR_SEGMENTS_AT_OLD_POSITION_NOT_NATIVE_SELECTOR"))
        rd=v["face_map_number_candidates"]
        grade="ORIGINAL_RD_LENGTH_DISCREPANCY" if any(y["rd_size_field"]!=y["size"] for y in rd) else ("ORIGINAL_RD_MULTIPLE_CANDIDATES" if len(rd)>1 else "ORIGINAL_RD_SINGLE_CANDIDATE")
        add("cn85_original",["analysis","programs",0,"entries",o],[x["compiled_label"]],"AUTHENTICATED_CN2012_COMPILED_NAME_POSITION",["ordinal:"+str(o),"slot:"+str(x["slot"]),"face:"+str(x["face"])],links,dict(physical_ordinal=o,compiled_slot=x["slot"],compiled_face=x["face"],programs=[a["program"],b["program"]],source_record_sha256=x["source_record_sha256"],portrait_candidate_grade=grade,original_rd_candidates=rd,ordinal_spr_candidates=v["ordinal_spr_group_indices"],slot_spr_candidates=v["slot_spr_group_indices"],native_selector_verified=False,original_portrait_verified=False,official_release_verified=False,same_deployment_server_fields_verified=False))


def attach_cn50_motion(d, entries):
    """Keep native CN50 full-motion evidence separate from prior cross-carrier comparisons."""
    p = d["hf101"]
    assert p["official_identity_verified"] is False and p["original_runtime_verified"] is False
    for e in entries:
        if e["source"] != "cn50":
            continue
        raw = resolve(d, e["source"], e["pointer"])
        key = str(raw["ordinal"])
        row = p["positions"][key]
        assert (row["name"], row["row_sha256"]) == (raw["compiled_name"], raw["exe_row_sha256"])
        groups = [dict(group_index=int(i), **p["groups"][i]) for i in row["group_ids"]]
        assert {(g["graphic"], g["spr_sha256"]) for g in groups} == {(g["spr_group"], g["sha256"]) for g in raw["spr_groups"]}
        grade = "CN50_NATIVE_ALBUM_EXACT_RD_NOT_OFFICIAL_IDENTITY"
        e["detail"]["cn50_motion_reference"] = dict(qualification=grade, motion_status=row["status"], motion_groups=groups, original_runtime_verified=False, official_identity_verified=False)
        e["linked_records"].append(dict(source="hf101", pointer=["positions", key], qualification=grade))
        for i in row["group_ids"]:
            e["linked_records"].append(dict(source="hf101", pointer=["groups", i], qualification=grade))
        for i in sorted({i for g in groups for i in g["new_original_rows"]}, key=int):
            e["linked_records"].append(dict(source="hf101_raw", pointer=["observations", i], qualification="ORIGINAL_CN50_DUAL_DECODED_INDEX_PIXELS"))
        e["linked_records"].append(dict(source="hf101_custody", pointer=[], qualification="DERIVED_ARTIFACT_CUSTODY"))


def visual_group_links(group_id, group, qualification):
    yield dict(source="hf74", pointer=["groups", group_id], qualification=qualification)
    for index in group["geometry_indices"]:
        yield dict(source="hf72", pointer=["geometry_records", index],
                   qualification="ORIGINAL_NONPOSITIVE_GEOMETRY_RUNTIME_UNRESOLVED")
    for bitmap in group.get("boundary_bitmaps", []):
        yield dict(source="hf68_tw85_boundary", pointer=["observations", str(bitmap)],
                   qualification="BOUNDED_CANVAS_STRICT_DECODE_REJECTED")
    if group["status"] == "EARLIER_SELECTED_EXACT_SPR_AND_RD":
        yield dict(source="hf73", pointer=["frame_indices"],
                   qualification="EXACT_EARLIER_SELECTED_MOTION_RD_NOT_LIVE_IDENTITY")

def attach_visual(d, entries):
    """Attach PET74 projections to existing identities without adding pet records."""
    v=d["hf74"]; p=d["hf73"]
    assert not any(v[k] for k in ("official_identity_verified","original_runtime_verified","original_assets_published"))
    for e in entries:
        source=e["source"];detail=e["detail"];raw=resolve(d,source,e["pointer"])
        position=None;group_ids=[];grade=None
        if source=="tw85_grid":
            position=f"{detail['program']}:{detail['slot']}"
            row=v["positions"][position]
            assert (row["name"],row["row_sha256"],row["portrait_alias"])==(raw["original_name_cp950"],raw["original_row_sha256"],raw["source_portrait_alias"])
            group_ids=row["group_ids"];grade="SAME_PROGRAM_ORIGINAL_ALBUM_ROW_AND_STATIC_ROUTES"
        elif source=="tw85_spr":
            position=f"{detail['program']}:{detail['local_slot']}"
            row=v["positions"][position]
            assert (row["name"],row["row_sha256"],row["portrait_alias"])==(raw["original_name_cp950"],raw["original_album_row_sha256"],raw["original_portrait_alias_u32"])
            group_ids=[i for i in row["group_ids"] if v["groups"][i]["graphic"]==detail["graphic"]]
            assert group_ids
            grade="SAME_PROGRAM_ORIGINAL_NAMED_SPR_ROUTE"
        elif source=="tw75":
            group_ids=v["graphics"][str(detail["graphic"])]
            grade="CROSS_SOURCE_NUMERIC_GRAPHIC_ONLY_NOT_IDENTITY"
        elif source=="cn50":
            wanted={(g["spr_group"],g["sha256"]) for g in raw["spr_groups"]}
            group_ids=[i for g,h in sorted(wanted) for i in v["graphics"].get(str(g),[]) if v["groups"][i]["spr_sha256"]==h]
            grade="EXACT_CROSS_CARRIER_SPR_NOT_IDENTITY"
        elif source=="tw10":
            album=next(resolve(d,l["source"],l["pointer"]) for l in e["linked_records"] if l["source"]=="tw10_album")
            group_ids=[i for i in v["graphics"].get(str(detail["graphic"]),[]) if v["groups"][i]["spr_sha256"]==album["spr_original_segment_sha256"]]
            grade="EXACT_CROSS_CARRIER_SPR_NOT_IDENTITY"
        else:continue
        if position is None and not group_ids:continue
        def attach(src,pointer,q):
            e["linked_records"].append(dict(source=src,pointer=pointer,qualification=q))
        visual=dict(qualification=grade,motion_groups=[dict(group_index=int(i),**v["groups"][i]) for i in group_ids],
                    original_runtime_verified=False,official_identity_verified=False)
        if position is not None:
            row=v["positions"][position];alias=str(row["portrait_alias"])
            assert row["portrait_rows"]==[i for i,n in p["aliases"][alias]]
            visual.update(portrait_alias=int(alias),portrait_status=row["portrait_status"],portrait_rows=row["portrait_rows"],
                          album_position_motion_status=row["motion_status"])
            attach("hf74",["positions",position],grade)
            attach("hf73",["aliases",alias],"SAME_CARRIER_ALL_PHYSICAL_PORTRAIT_ALIAS_CANDIDATES")
            for i in row["portrait_rows"]:
                attach("hf73",["observations",str(i)],"STRICT_ORIGINAL_INDEXED_PIXEL_RECEIPT_NOT_RENDERED_COLOR")
        for i in group_ids:
            e["linked_records"].extend(visual_group_links(i, v["groups"][i], grade))
        attach("hf73",["palette_file_receipts"],"PRESERVED_TW10_TW85_PALETTE_BYTES_NOT_RUNTIME_SELECTION")
        detail["visual_reference"]=visual

def visual_graphic(d, graphic, full=False):
    """Return physical TW85 groups for one exact graphic number, including residuals."""
    projection = d["hf74"]
    results = []
    for group_id in projection["graphics"].get(str(graphic), []):
        group = projection["groups"][group_id]
        result = dict(group_index=int(group_id), **group)
        if full:
            links = visual_group_links(group_id, group, "TW85_PHYSICAL_GROUP_NOT_PET_ID")
            result["linked_original_records"] = [
                dict(link, record=resolve(d, link["source"], link["pointer"]))
                for link in links if link["source"] != "hf74"
            ]
        results.append(result)
    return dict(graphic=graphic, carrier="PRESERVED_TW85", physical_group_occurrences=len(results),
                official_species_count=None, official_identity_verified=False,
                original_runtime_verified=False, results=results)

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
    assert [r["printed_number"] for r in tw10_refs["PET-000004"]["mainland_2003_catalogue_rows"]] == [4, 8]
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
    cases = d["hf38"]["rows"]
    assert {x["pet_id"] for x in cases} == {"PET-000004", "PET-000017", "PET-000021"}
    assert sum(
        1 for entry in entries if entry["source"] == "tw10"
        for link in entry["linked_records"] if link["source"] == "hf38"
    ) == 3
    assert all(
        row["official_tw10_native_stats"] is None and row["official_tw10_skillset"] is None
        and row["official_tw10_acquisition_verified"] is False
        and row["official_first_release_date"] is None for row in cases
    )
    cases39 = d["hf39"]["rows"]
    assert {r["pet_id"] for r in cases39} == {"PET-000014", "PET-000116", "PET-000117", "PET-000118", "PET-000124"}
    assert sum(l["source"] == "hf39" for e in entries if e["source"] == "tw10" for l in e["linked_records"]) == 5
    assert sum(len(r["community_fixed_table"]) for r in cases39) == 10
    assert sum(t["pet_flag"] == 0 for r in cases39 for t in r["community_fixed_table"]) == 4
    assert sum(len(r["mixed25_archived_projection"]) for r in cases39) == 10
    assert sum(t["pet_flag"] == 0 for r in cases39 for t in r["mixed25_archived_projection"]) == 4
    assert len({x["git_blob"] for x in d["hf39"]["community_sources"]}) == 1
    assert all(r["official_tw10_native_stats"] is None and r["official_tw10_skillset"] is None and not r["official_tw10_acquisition_verified"] and r["official_first_release_date"] is None and not r["japan_album"]["actual_image_bytes_read"] for r in cases39)
    assert sum(r["japan_album"]["exact_ordinal_name_match"] for r in cases39) == 2
    panels39 = {r["pet_id"]: r["japan_album"]["panel"] for r in cases39 if r["japan_album"]["panel"] is not None}
    assert len(panels39) == 4
    assert all(p["level"] == 19 and p["original_jpeg_sha256"] is None and p["server"] is None and p["build"] is None and not p["official_tw10_identity_verified"] for p in panels39.values())
    assert panels39["PET-000116"]["visually_estimated_elements_earth_water_fire_wind"] == [5, 5, 0, 0]
    assert [panels39["PET-000124"][k] for k in ("hp_max", "attack", "defense", "speed")] == [199, 41, 30, 35]
    assert all(r["period_growth_20030924"] is None or r["period_growth_20030924"]["section"] == "转宠" for r in cases39)
    cases40 = d["hf40"]["rows"]
    assert {r["pet_id"] for r in cases40} == {"PET-000014", "PET-000116", "PET-000117", "PET-000118", "PET-000124"}
    assert sum(l["source"] == "hf40" for e in entries if e["source"] == "tw10" for l in e["linked_records"]) == 5
    assert sum(r["archive_positive_reference_count"] for r in cases40) == 70
    assert sum(r["archive_lv1_reference_count"] for r in cases40) == 6
    assert [r["period_floor_lv1_static_match"] for r in cases40] == [None, False, True, True, None]
    assert cases40[-1]["quest_reward"]["instance_id"] == 484 and cases40[-1]["quest_reward"]["template_id"] == 315
    assert all(r["official_tw10_native_stats"] is None and r["official_tw10_skillset"] is None and not r["official_tw10_acquisition_verified"] and r["official_first_release_date"] is None for r in cases40)
    high45 = [e for e in entries if e["source"] == "tw75"]
    assert len(high45) == 467
    g46 = [e["detail"]["saved_mixed25_acquisition"]["gap_classification"] for e in high45 if e["detail"]["saved_mixed25_acquisition"]["gap_classification"] is not None]
    assert len(g46) == 349
    assert collections.Counter(g["gap_state"] for g in g46) == d["hf46"]["summary"]["gap_state_counts"]
    source_counts = collections.Counter(l["source"] for e in high45 for l in e["linked_records"])
    strict = d["hf49"]["remaining_gap_row_indices"]
    remaining = list(strict)
    matched = set()
    for source in ("hf81", "hf82", "hf83", "hf84", "hf85", "hf86", "hf87"):
        supplement = d[source]
        assert supplement["official_same_deployment_verified"] is False and supplement["original_assets_published"] is False
        for j, row in enumerate(supplement["rows"]):
            i = row["tw75_row_index"]
            native = d["tw75"]["pet_flag_1_field_projections"][i]
            assert i in remaining and i not in matched
            assert row["row_sha256"] == native["row_sha256"] and row["master_elements"] == native["elements"]
            assert row["official_acquisition_verified"] is False and row["official_first_release"] is None
            assert sum(l["source"] == source and l["pointer"] == ["rows", j] for l in high45[i]["linked_records"]) == 1
            matched.add(i)
        remaining = [i for i in remaining if i not in matched]
        assert remaining == supplement["remaining_without_new_later_reference"]
    assert len(strict) == 67 and len(matched) == 34 and len(remaining) == 33
    residual87 = d["hf87"]["residual"]
    assert [r["tw75_row_index"] for r in residual87] == remaining
    assert all(r["retain_strict_gap"] and not r["official_acquisition_verified"] and r["selected_positive_routes"] == 0 for r in residual87)
    assert collections.Counter(r["category"] for r in residual87) == d["hf87"]["summary"]["category_counts"]
    assert {r["tw75_row_index"] for r in residual87 if r["prior_documentary_references"] is not None} == {31, 32, 208, 344, 345}
    for j, row in enumerate(residual87):
        assert sum(l["source"] == "hf87" and l["pointer"] == ["residual", j] for l in high45[row["tw75_row_index"]]["linked_records"]) == 1

    assert {key: source_counts[key] for key in ("hf46", "hf47", "hf48", "hf49", "hf50")} == {
        "hf46": 349, "hf47": 29, "hf48": 19, "hf49": 22, "hf50": 71,
    }
    assert source_counts["hf51_petabi"] == 33
    assert source_counts["hf57"] == 67
    assert {i for i,e in enumerate(high45) if any(l["source"]=="hf57" for l in e["linked_records"])} == set(d["hf49"]["remaining_gap_row_indices"])
    assert all(r["retain_strict_gap"] and not r["official_acquisition_verified"] for r in d["hf57"]["rows"])
    source60 = d["hf60"]
    assert all(source60[key] is False for key in
               ("official_release_verified", "native_runtime_verified", "original_assets_published"))
    groups60 = {s["physical_group"] for s in source60["observations"]["sequences"]}
    assert len(groups60) == 20
    expected60 = {r["position"]: {g["group_index"] for g in r["tw85_physical_groups"]} & groups60
                  for r in d["hf57"]["rows"]}
    for i, item in enumerate(high45):
        links60 = [l for l in item["linked_records"] if l["source"] == "hf60"]
        actual60 = {resolve(d, l["source"], l["pointer"])["physical_group"] for l in links60}
        assert actual60 == expected60.get(i, set()) and len(links60) == len(actual60)
    assert set(d["hf61"]["qualification"].values()) == {False}
    assert [r["position"] for r in d["hf61"]["rows"]] == d["hf49"]["remaining_gap_row_indices"]
    assert source_counts["hf62"] == 67 and source_counts["hf63"] == 13
    assert {i for i,e in enumerate(high45) if any(l["source"]=="hf63" for l in e["linked_records"])} == {r["position"] for r in d["hf63"]["rows"]}
    assert source_counts["hf61"] == 67 + 135
    if "hf77" in d:
        assert source_counts["hf77"] == 12
        assert d["hf77"]["official_same_deployment_verified"] is False
    if "hf78" in d:
        assert source_counts["hf78"] == 6
        assert d["hf78"]["same_deployment_birth_and_growth_proven"] is False
    if "hf79" in d:
        assert source_counts["hf79"] == 6
        assert d["hf79"]["submitted_measurement_date_or_build_verified"] is False
    for row61 in d["hf61"]["rows"]:
        links61 = [l for l in high45[row61["position"]]["linked_records"] if l["source"] == "hf61"]
        assert {resolve(d, l["source"], l["pointer"])["skill_id"] for l in links61
                if l["pointer"][0] == "configured_skill_definitions"} == {
                    slot["skill_id"] for slot in row61["scope"]["petskill.txt"]["source_slots"]}
    if "hf76" in d:
        assert source_counts["hf76"] == 467 + 941
        assert set(d["hf76"]["qualification"].values()) == {False}
        verified76 = [entry["detail"]["saved_selected_master_fields"] for entry in high45]
        assert sum(row["matched_birth_inputs"] is not None for row in verified76) == 440
        assert sum(bool(row["fields_differing_from_claim"]) for row in verified76) == 6
        assert sum(row["saved_reward_instance_id"] is not None for row in verified76) == 36
        assert all(row["matched_birth_inputs"] is not None or not row["configured_skill_slots"] for row in verified76)
    if "hf88_skillshop" in d:
        shop = d["hf88_skillshop"]
        assert len(shop["original_skillshop_CREATE_to_parameter_rows"]) == 21
        assert shop["summary"]["distinct_skill_IDs"] == 23
        all_slots = [slot for row in verified76 for slot in row["configured_skill_slots"]]
        linked = [slot for slot in all_slots if slot["saved_skillshop_reference"]["shop_indices"]]
        assert len(all_slots) == 941 and len(linked) == 904
        assert len({slot["skill_id"] for slot in linked}) == 19
        assert sum(any(slot["saved_skillshop_reference"]["shop_indices"] for slot in row["configured_skill_slots"])
                   for row in verified76) == 440
        assert source_counts["hf88_skillshop"] == 6636
        definitions = {row["skill_id"]: row for row in d["hf76"]["configured_skill_definitions"]}
        master_rows = {row["skill_id"]: row for row in shop["source_skill_id_master_presence_candidates"]}
        for entry, row in zip(high45, verified76):
            expected_shops = set()
            for slot in row["configured_skill_slots"]:
                ref = slot["saved_skillshop_reference"]
                sid = slot["skill_id"]
                exact = sid in master_rows and master_rows[sid]["primary_petskill_txt"]["row_sha256"] == definitions[sid]["row_sha256"]
                expected = [j for j, p in enumerate(shop["original_skillshop_CREATE_to_parameter_rows"])
                            if exact and sid in p["source_pet_skill_ids_ordered"]]
                assert ref["shop_indices"] == expected
                assert not ref["species_can_learn_verified"] and not ref["official_runtime_verified"]
                expected_shops.update(expected)
            assert {l["pointer"][1] for l in entry["linked_records"] if l["source"] == "hf88_skillshop"} == expected_shops
    if "hf89" in d:
        special = d["hf89"]["rows"]
        assert len(special) == 19 and len({r["skill_id"] for r in special}) == 19
        expected = {(r["skill_id"], p["position"], p["slot_index"], p["template_sha256"])
                    for r in special for p in r["configured_positions"]}
        actual = {(slot["skill_id"], i, slot["slot_index"], d["tw75"]["pet_flag_1_field_projections"][i]["row_sha256"])
                  for i, row in enumerate(verified76) for slot in row["configured_skill_slots"]
                  if not slot["saved_skillshop_reference"]["shop_indices"]}
        assert actual == expected and len(actual) == 37
        assert source_counts["hf89"] == 37
        refs = [slot["period_special_skill_reference"] for row in verified76 for slot in row["configured_skill_slots"]
                if "period_special_skill_reference" in slot]
        assert collections.Counter(ref["qualification"] for ref in refs) == {
            "DATED_SKILL_LEVEL_REFERENCE": 21, "ITEM_CONTEXT_ONLY": 4, "NO_QUALIFIED_PERIOD_REFERENCE_IN_BATCH": 12}
        assert all(not ref["same_deployment_verified"] for ref in refs)
        assert all(not r["same_deployment_learnability_verified"] and not r["official_birth_skill_verified"]
                   and not r["official_runtime_verified"] for r in special)
    # A resolved pointer is insufficient: verify each definition ID and hash.
    if "hf76" in d:
        for entry, row in zip(high45, d["hf76"]["rows"]):
            actual = [resolve(d, l["source"], l["pointer"])
                      for l in entry["linked_records"]
                      if l["source"] == "hf76" and l["pointer"][0] == "configured_skill_definitions"]
            assert [(z["skill_id"], z["row_sha256"]) for z in actual] == [
                (z["skill_id"], z["definition_row_sha256"]) for z in row["configured_skill_slots"]]
    if "hf90" in d:
        # The growth model imports its dependencies via the tools package.
        # Support both direct script invocation and python -m tools.... .
        if not __package__:
            import sys
            sys.path.insert(0, str(ROOT))
        from tools.stoneage_pet_growth_model import project_pet_birth
        from tools.stoneage_pet_detail30_base_panel import project_pet_source_base_panel
        joint = d["hf90"]
        assert len(joint["rows"]) == 41
        assert {row["fusion_index"] for row in joint["rows"]} == set(range(41))
        assert len({row["position"] for row in joint["rows"]}) == 41
        assert sum(row["selected_archive_grade"] == "EXACT_SHARED_TEMPLATE_ROW" for row in joint["rows"]) == 40
        for row in joint["rows"]:
            i = row["position"]
            pet = d["tw75"]["pet_flag_1_field_projections"][i]
            sample = d["fusion2003"]["records"][row["fusion_index"]]
            assert (pet["name"], pet["elements"], pet["row_sha256"]) == (row["name"], row["elements"], row["template_row_sha256"])
            assert sample["displayed_name"] == pet["name"]
            assert [sample["image"]["observed_elements"][e] * 10 for e in ("earth","water","fire","wind")] == pet["elements"]
            assert sample["image"]["sha256"] == row["panel_image_sha256"]
            assert d["hf76"]["rows"][i]["selected_table_grade"] == row["selected_archive_grade"]
            assert not row["official_birth_verified"] and not row["official_fusion_verified"]
            witness = row["witness"]
            rolls = [j for j, n in enumerate(witness["allocation_counts"]) for _ in range(n)]
            birth = project_pet_birth(template_base=pet["base"], init_num=pet["initnum"], lvup_point=0,
                                      level=1, offsets=witness["offsets"], birth_rolls=rolls)
            assert list(birth.internal_stats) == witness["internal_stats"]
            panel = project_pet_source_base_panel(birth.internal_stats)
            stats = sample["image"]["observed_stats"]
            assert [panel.max_hp, panel.attack, panel.defense, panel.quick] == row["observed_panel"] == [
                stats["max_hp"], stats["attack"], stats["defense"], stats["agility"]]
            assert all(lo <= value <= hi for value, (lo, hi) in zip(row["observed_panel"], row["marginal_ranges"]))
        excluded = set(d["hf55_fusion"]["comparison"]["flow"]["excluded_inheritance_skill_ids"])
        expected = {(i, slot["slot_index"], slot["skill_id"], slot["definition_row_sha256"])
                    for i, row in enumerate(d["hf76"]["rows"]) for slot in row["configured_skill_slots"]
                    if slot["skill_id"] in excluded}
        actual = {(r["position"], r["slot_index"], r["skill_id"], r["skill_definition_sha256"]) for r in joint["inheritance_rows"]}
        assert expected == actual and len(actual) == 8
        assert all(not r["same_deployment_verified"] for r in joint["inheritance_rows"])
        assert source_counts["hf90"] == 49 and source_counts["hf55_fusion"] == 8
        assert not joint["probability_inferred"] and joint["summary"]["official_fields_closed"] == 0
    if "hf91" in d:
        if not __package__:
            import sys
            if str(ROOT) not in sys.path:
                sys.path.insert(0, str(ROOT))
        from tools.stoneage_pet_growth_model import project_pet_birth, advance_pet_growth, PetLevelGrowthRolls
        from tools.stoneage_pet_detail30_base_panel import project_pet_source_base_panel
        endpoint = d["hf91"]
        for path, sha in endpoint["input_git_blobs"].items():
            assert blob((ROOT / path).read_bytes()) == sha
        assert not endpoint["official_variant_resolved"] and not endpoint["original_rolls_observed"] and not endpoint["probability_inferred"]
        expected_sources = {("hf77", ("rows", j)) for j in range(len(d["hf77"]["rows"]))}
        expected_sources |= {("hf78", ("posts", i, "rows", j)) for i, post in enumerate(d["hf78"]["posts"])
                             for j in range(len(post["rows"]))}
        assert len(expected_sources) == len(endpoint["rows"]) == 29
        assert {(row["source"], tuple(row["pointer"])) for row in endpoint["rows"]} == expected_sources
        counts = collections.Counter()
        paths_replayed = 0
        for j, row in enumerate(endpoint["rows"]):
            i = row["position"]
            pet = d["tw75"]["pet_flag_1_field_projections"][i]
            variant = d["hf76"]["rows"][i]
            sample = resolve(d, row["source"], row["pointer"])
            assert row["template_id"] == pet["template_id"] == variant["template_id"]
            assert row["template_id"] == (sample["template_id"] if row["source"] == "hf77" else d["hf78"]["template_id"])
            assert row["claimed_row_sha256"] == pet["row_sha256"] and row["saved_row_sha256"] == variant["selected_row_sha256"]
            assert (row["initial"], row["final"], row["final_level"]) == (sample["initial"], sample["final"], sample["final_level"])
            assert row["reported_arithmetic_conflicts"] == sample.get("published_arithmetic_conflicts")
            assert row["assumed_initial_level"] == 1 and row["final_level"] > 1
            assert sum(l["source"] == "hf91" and l["pointer"] == ["rows", j] for l in high45[i]["linked_records"]) == 1
            counts[(row["claimed_witness"] is not None, row["saved_witness"] is not None)] += 1
            for label, base in (("claimed", pet["base"]), ("saved", variant["selected_fields_differing_from_claim"]["base"])):
                witness = row[label + "_witness"]
                if witness is None:
                    continue
                assert len(witness["birth_allocation_counts"]) == len(witness["level_allocation_mode_counts"]) == 4
                assert all(type(n) is int and n >= 0 for n in witness["birth_allocation_counts"] + witness["level_allocation_mode_counts"])
                assert sum(witness["birth_allocation_counts"]) == 10
                rolls = [k for k, n in enumerate(witness["birth_allocation_counts"]) for _ in range(n)]
                birth = project_pet_birth(template_base=base, init_num=pet["initnum"], lvup_point=0,
                                          level=1, offsets=witness["offsets"], birth_rolls=rolls)
                assert birth.rank == witness["rank"] and list(birth.internal_stats) == witness["start_internal"]
                assert sum(witness["level_allocation_mode_counts"]) == row["final_level"] - 1
                level_rolls = [PetLevelGrowthRolls((k,) * 10, witness["rank_roll"])
                               for k, n in enumerate(witness["level_allocation_mode_counts"]) for _ in range(n)]
                result = advance_pet_growth(birth.individualized_growth_base, birth.rank, birth.internal_stats, 0, level_rolls)
                assert result.levels_gained == row["final_level"] - 1
                assert list(result.end_internal_stats) == witness["end_internal"]
                for raw, observed in ((birth.internal_stats, row["initial"]), (result.end_internal_stats, row["final"])):
                    panel = project_pet_source_base_panel(raw)
                    assert [panel.max_hp, panel.attack, panel.defense, panel.quick] == observed
                paths_replayed += 1
        assert counts == {(True, True): 26, (True, False): 1, (False, False): 2}
        assert paths_replayed == 53 and source_counts["hf91"] == 29
        assert sum(bool(row["reported_arithmetic_conflicts"]) for row in endpoint["rows"]) == 2
        assert endpoint["summary"]["official_closures"] == 0
    if "hf92" in d:
        dated = d["hf92"]
        for path, sha in dated["input_git_blobs"].items():
            assert blob((ROOT / path).read_bytes()) == sha
        equivalences = dated["character_equivalences"]
        def norm92(name):
            return "".join(equivalences.get(ch, ch) for ch in name if not ch.isspace())
        by_graphic = collections.defaultdict(list)
        by_ordinal = collections.defaultdict(list)
        for j, cn in enumerate(d["cn50"]["records"]):
            for graphic in {g["spr_group"] for g in cn["spr_groups"]}:
                by_graphic[graphic].append((j, cn))
        for k, row in enumerate(d["sina2003"]["rows"]):
            by_ordinal[row["cn50_album_ordinal_by_name_only"]].append((k, row))
        expected = []
        for i, pet in enumerate(d["tw75"]["pet_flag_1_field_projections"]):
            refs = []
            for j, cn in by_graphic[pet["graphic"]]:
                for k, row in by_ordinal[cn["ordinal"]]:
                    refs.append(dict(cn50_index=j, cn50_ordinal=cn["ordinal"], cn50_name=cn["compiled_name"],
                        cn50_row_sha256=cn["exe_row_sha256"], graphic=pet["graphic"], catalogue_index=k,
                        catalogue_row_sha256=row["normalized_row_sha256"], printed_number=row["printed_number"],
                        rebirth_label=row["rebirth_variant_label"], name_match=norm92(pet["name"]) == norm92(cn["compiled_name"]),
                        element_match=[row["reported_elements"].get(e, 0)*10 for e in ("earth","water","fire","wind")] == pet["elements"]))
            if not refs:
                continue
            strict = [r for r in refs if r["name_match"] and r["element_match"]]
            if len(strict) == 1:
                grade = "REBIRTH_LABEL_COMPATIBLE" if strict[0]["rebirth_label"] else "UNIQUE_NAME_GRAPHIC_ELEMENT_COMPATIBLE"
            elif strict:
                grade = "AMBIGUOUS_COMPATIBLE"
            else:
                grade = "ELEMENT_CONFLICT" if any(r["name_match"] for r in refs) else "GRAPHIC_ONLY_DIFFERENT_NAME"
            expected.append(dict(position=i, template_id=pet["template_id"], template_row_sha256=pet["row_sha256"],
                name=pet["name"], grade=grade, refs=refs, official_release_verified=False, first_release_date=None))
        assert expected == dated["rows"]
        assert collections.Counter(r["grade"] for r in expected) == {"UNIQUE_NAME_GRAPHIC_ELEMENT_COMPATIBLE":223,"REBIRTH_LABEL_COMPATIBLE":1,"GRAPHIC_ONLY_DIFFERENT_NAME":19,"ELEMENT_CONFLICT":12}
        assert len(expected) == 255 and sum(len(r["refs"]) for r in expected) == 260
        assert source_counts["hf92"] == 255 and dated["summary"]["official_closures"] == 0
        for j, row in enumerate(expected):
            assert sum(l["source"] == "hf92" and l["pointer"] == ["rows", j] for l in high45[row["position"]]["linked_records"]) == 1
    if "hf93" in d:
        family_report = d["hf93"]
        for path, sha in family_report["input_git_blobs"].items():
            assert blob((ROOT / path).read_bytes()) == sha
        def norm93(name):
            return "".join(family_report["character_equivalences"].get(ch, ch) for ch in name)
        claims = family_report["rows"]
        assert len(claims) == 38 and len(family_report["sources"]) == 3
        assert collections.Counter(r["source"] for r in claims) == {0: 24, 1: 1, 2: 13}
        counts = collections.Counter()
        linked = set()
        for j, claim in enumerate(claims):
            expected = []
            for i, pet in enumerate(d["tw75"]["pet_flag_1_field_projections"]):
                if norm93(pet["name"]) != norm93(claim["name"]):
                    continue
                elements = claim["reported_elements"]
                status = "NOT_REPORTED" if elements is None else "COMPATIBLE" if elements == pet["elements"] else "CONFLICT"
                expected.append(dict(position=i, template_id=pet["template_id"],
                    template_row_sha256=pet["row_sha256"], name=pet["name"], element_status=status))
                counts[status] += 1
                linked.add(i)
                assert sum(l["source"] == "hf93" and l["pointer"] == ["rows", j] for l in high45[i]["linked_records"]) == 1
            assert expected == claim["candidates"]
            assert not claim["official_family_verified"] and not claim["official_release_verified"]
        assert counts == {"COMPATIBLE": 26, "CONFLICT": 1, "NOT_REPORTED": 5}
        assert len(linked) == 31 and source_counts["hf93"] == 32
        assert sum(not row["candidates"] for row in claims) == 8
        assert family_report["summary"]["official_family_closures"] == 0
    if "hf94" in d:
        late = d["hf94"]
        for path, sha in late["input_git_blobs"].items():
            assert blob((ROOT / path).read_bytes()) == sha
        expected = [i for i, row in enumerate(d["hf93"]["rows"]) if not row["candidates"]]
        assert [r["family_claim_index"] for r in late["rows"]] == expected
        grid_count = 0
        for j, row in enumerate(late["rows"]):
            claim = d["hf93"]["rows"][row["family_claim_index"]]
            assert (row["name"], row["family"]) == (claim["name"], claim["family"])
            refs = []
            for program, branch in d["tw85_grid"]["programs"].items():
                for i, raw in enumerate(branch["source_records"]):
                    if raw["original_name_cp950"] != row["name"]:
                        continue
                    refs.append(dict(program=program, index=i, slot=raw["slot"], portrait_alias=raw["source_portrait_alias"],
                        row_sha256=raw["original_row_sha256"], visual_pointer=["positions", f"{program}:{raw['slot']}"]))
            assert refs == row["grid_candidates"]
            for ref in refs:
                visual = resolve(d, "hf74", ref["visual_pointer"])
                assert visual["row_sha256"] == ref["row_sha256"]
                assert visual["portrait_alias"] == ref["portrait_alias"]
                assert visual["name"] == row["name"]
            grid_count += len(refs)
            cat = row["catalogue"]
            assert sum(cat["elements"]) == 10 and cat["skill_slots"] == 7 and cat["raw_html_sha256"] is None
            if row["older_cn_reference"]:
                ref = row["older_cn_reference"]
                source = resolve(d, ref["source"], ref["pointer"])
                assert source["name"] == row["name"] and source["element_ratio"] == cat["elements"]
                assert ref["element_compatible"]
            if row["year_beast_recollection"]:
                ref = row["year_beast_recollection"]
                assert sum(ref["reported_elements"]) == 10 and ref["reported_elements"] != cat["elements"]
                assert ref["element_conflict"] and ref["name_variant"] == (ref["reported_name"] != row["name"])
            assert not row["official_identity_verified"] and not row["official_birth_growth_verified"] and not row["official_release_verified"]
            assert len([e for e in entries if e["source"] == "hf94" and e["pointer"] == ["rows", j]]) == 1
        assert grid_count == 5 and sum(bool(r["year_beast_recollection"]) for r in late["rows"]) == 4
        assert sum(r["year_beast_recollection"]["name_variant"] for r in late["rows"] if r["year_beast_recollection"]) == 1
        assert late["summary"]["official_closures"] == 0
    if "hf99" in d:
        numeric99 = d["hf99"]
        for path, sha in numeric99["input_git_blobs"].items():
            assert blob((ROOT / path).read_bytes()) == sha
        master99 = d["tw75"]["pet_flag_1_field_projections"]
        birth99 = d["tw75_birth"]
        assert numeric99["panel_order"] == birth99["panel_order"] and numeric99["internal_order"] == birth99["internal_order"]
        def numeric_side99(z):
            i = z["position"]
            a, r = master99[i], birth99["rows"][i]
            assert a["template_id"] == z["template_id"] == r["template_id"]
            assert a["row_sha256"] == z["row_sha256"] == r["source_row_sha256"]
            return dict(position=i,template_id=z["template_id"],row_sha256=z["row_sha256"],selected_grade=z["selected_table_grade"],
                selected_route_counts=z["route_counts"],selected_reward_instance_id=z["reward_instance_id"],conditional_rank=r["rank"])
        keys99 = ["level1_internal_marginal_ranges","level1_unmodified_work_panel_marginal_ranges","per_level_internal_increment_marginal_ranges"]
        expected99 = []
        for i,p in enumerate(d["hf96"]["rows"]):
            if p["relation"] == "SAME_NAME_GRAPHIC" and p["differing_projected_fields"] in ([],["skill_slots"]):
                continue
            lft,rgt = numeric_side99(p["left"]),numeric_side99(p["right"])
            l,r = [birth99["rows"][z["position"]] for z in (lft,rgt)]
            comparisons = {k:dict(equal=l[k] == r[k],disjoint_components=[j for j,(a,b) in enumerate(zip(l[k],r[k])) if max(a[0],b[0]) > min(a[1],b[1])]) for k in keys99}
            expected99.append(dict(collision_index=i,relation=p["relation"],left=lft,right=rgt,differing_projected_fields=p["differing_projected_fields"],
                comparisons=comparisons,both_selected_exact=p["both_selected_exact"],selected_route_or_reward_reference_differs=p["selected_route_or_reward_reference_differs"],official_identity_verified=False))
        assert numeric99["rows"] == expected99
        panel99,growth99 = keys99[1:]
        stat99 = dict(pairs=len(expected99),distinct_positions=len({r[s]["position"] for r in expected99 for s in ("left","right")}),
            relation_counts=dict(collections.Counter(r["relation"] for r in expected99)),
            panel_range_different_pairs=sum(not r["comparisons"][panel99]["equal"] for r in expected99),
            growth_range_different_pairs=sum(not r["comparisons"][growth99]["equal"] for r in expected99),
            panel_any_disjoint_pairs=sum(bool(r["comparisons"][panel99]["disjoint_components"]) for r in expected99),
            panel_all_disjoint_pairs=sum(len(r["comparisons"][panel99]["disjoint_components"]) == 4 for r in expected99),
            growth_any_disjoint_pairs=sum(bool(r["comparisons"][growth99]["disjoint_components"]) for r in expected99),
            both_selected_exact=sum(r["both_selected_exact"] for r in expected99),
            selected_route_or_reward_reference_differs=sum(r["selected_route_or_reward_reference_differs"] is True for r in expected99),official_closures=0)
        assert numeric99["summary"] == stat99 == m["supplement_hf99"]
        assert len(expected99) == 36
        partition99 = [[r["collision_index"] for r in d[k]["rows"]] for k in ("hf97","hf98","hf99")]
        assert sorted(i for part in partition99 for i in part) == list(range(len(d["hf96"]["rows"])))
        assert {(e["pointer"][1],l["pointer"][1]) for e in high45 for l in e["linked_records"] if l["source"] == "hf99"} == {(r[s]["position"],j) for j,r in enumerate(expected99) for s in ("left","right")}
        assert sum(l["source"] == "hf99" for e in entries for l in e["linked_records"]) == 72
    if "hf98" in d:
        variants98 = d["hf98"]
        for path, sha in variants98["input_git_blobs"].items():
            assert blob((ROOT / path).read_bytes()) == sha
        master98 = d["tw75"]["pet_flag_1_field_projections"]
        selected98 = d["hf76"]
        cross98 = d["hf42_cross"]["rows"]
        reward98 = d["hf42"]["rows"]
        later98 = d["tw75_comparison"]
        def side98(z):
            i = z["position"]
            a, s, c = master98[i], selected98["rows"][i], later98["rows"][i]
            assert a["template_id"] == z["template_id"] == c["template_id"]
            assert a["row_sha256"] == z["row_sha256"] == s["row_sha256"]
            wi = next((j for j,q in enumerate(cross98) if q["tw75_row_index"] == i and q["shared_template_row_sha256"] == a["row_sha256"]), None)
            ri = None if wi is None else cross98[wi]["reward_row_index"]
            if ri is not None:
                rr = reward98[ri]
                assert rr["template_id"] == a["template_id"] and rr["award_instance_id"] == z["reward_instance_id"]
                assert rr["skill_slots"] == a["skill_slots"]
            return dict(position=i,template_id=z["template_id"],row_sha256=z["row_sha256"],selected_grade=z["selected_table_grade"],
                selected_route_counts=z["route_counts"],selected_reward_crosswalk_index=wi,selected_reward_row_index=ri,
                later_comparison_row_index=i,later_comparison_status=c["comparison_status"],later_comparison_instance_count=c["comparison_instance_count"],
                later_comparison_positive_reference_count=c["positive_reference_count"],official_birth_skills_verified=False)
        def slot98(z,j,skill):
            if skill is None or skill <= 0:
                return None
            s = selected98["rows"][z["position"]]
            record = next((q for q in s["configured_skill_slots"] if q["slot_index"] == j and q["skill_id"] == skill), None)
            di = next((i for i,q in enumerate(selected98["configured_skill_definitions"]) if q["skill_id"] == skill), None)
            ci = next((i for i,q in enumerate(later98["skill_ids"]) if q["id"] == skill), None)
            if record is not None:
                assert di is not None and record["definition_row_sha256"] == selected98["configured_skill_definitions"][di]["row_sha256"]
            return dict(skill_id=skill,selected_definition_index=di if record is not None else None,later_comparison_definition_index=ci,
                qualification="SAVED_CONFIGURED_SLOT_DEFINITION_NOT_BIRTH_PROOF" if record is not None else "NO_EXACT_SELECTED_SLOT_COMPARISON_ONLY")
        expected98 = []
        for i,p in enumerate(d["hf96"]["rows"]):
            if p["relation"] != "SAME_NAME_GRAPHIC" or p["differing_projected_fields"] != ["skill_slots"]:
                continue
            lft,rgt = p["left"],p["right"]
            lslots,rslots = [master98[z["position"]]["skill_slots"] for z in (lft,rgt)]
            changed = [dict(slot_index=j,left=a,right=b,left_evidence=slot98(lft,j,a),right_evidence=slot98(rgt,j,b))
                for j,(a,b) in enumerate(zip(lslots,rslots)) if a != b]
            expected98.append(dict(collision_index=i,left=side98(lft),right=side98(rgt),changed_slots=changed,official_identity_verified=False))
        assert variants98["rows"] == expected98
        ev98 = [d[k] for r in expected98 for d in r["changed_slots"] for k in ("left_evidence","right_evidence") if d[k] is not None]
        stat98 = dict(pairs=len(expected98),positions=len({r[s]["position"] for r in expected98 for s in ("left","right")}),
            both_selected_exact=sum(all(r[s]["selected_grade"] == "EXACT_SHARED_TEMPLATE_ROW" for s in ("left","right")) for r in expected98),
            changed_positive_slot_occurrences=len(ev98),distinct_changed_skill_ids=len({e["skill_id"] for e in ev98}),
            selected_definition_occurrences=sum(e["selected_definition_index"] is not None for e in ev98),
            comparison_only_occurrences=sum(e["selected_definition_index"] is None and e["later_comparison_definition_index"] is not None for e in ev98),
            reward_pair_count=sum(any(r[s]["selected_reward_row_index"] is not None for s in ("left","right")) for r in expected98),official_closures=0)
        assert variants98["summary"] == stat98 == m["supplement_hf98"]
        assert len(expected98) == 9
        assert {(e["pointer"][1],l["pointer"][1]) for e in high45 for l in e["linked_records"] if l["source"] == "hf98"} == {(r[s]["position"],j) for j,r in enumerate(expected98) for s in ("left","right")}
        assert sum(l["source"] == "hf98" for e in entries for l in e["linked_records"]) == 18
    if "hf97" in d:
        roles97 = d["hf97"]
        for path, sha in roles97["input_git_blobs"].items():
            assert blob((ROOT / path).read_bytes()) == sha
        proj97 = d["hf45"]["projection"]
        floor97 = d["hf45_floor"]["rows"]
        areas97 = {a["id"]: i for i,a in enumerate(proj97["area_metadata"])}
        instances97 = {a["id"]: i for i,a in enumerate(proj97["instance_metadata"])}
        routes97 = {a["template_id"]: i for i,a in enumerate(proj97["mixed25_template_routes"])}
        floor_indices97 = {a["floor_id"]: i for i,a in enumerate(floor97)}
        def role_side97(s):
            row = proj97["claimed_tw75_rows"][s["position"]]
            assert row["template_id"] == s["template_id"] and row["tw75_row_sha256"] == s["row_sha256"]
            base = dict(position=s["position"], template_id=s["template_id"], official_acquisition_verified=False)
            if s["selected_table_grade"] != "EXACT_SHARED_TEMPLATE_ROW":
                return dict(base, grade="NO_EXACT_SELECTED_ROW_NOT_ASSESSED", **{k: None for k in ("route_index","positive_route_count","double_flag_route_count","lv1_double_flag_route_count","instance_indices","area_indices","group_ids","floor_ids","floor_reference_indices","pet_flag_1_instance_levels")})
            ri = routes97.get(s["template_id"])
            rr = [] if ri is None else proj97["mixed25_template_routes"][ri]["routes"]
            if ri is not None:
                assert proj97["mixed25_template_routes"][ri]["source_template_row_sha256"] == s["row_sha256"]
            def inst(r):
                return proj97["instance_metadata"][instances97[r[4]]]
            pet = [r for r in rr if inst(r)["pet_flag"] == 1]
            lv1 = [r for r in pet if inst(r)["level"][0] <= 1 <= inst(r)["level"][1]]
            assert [len(rr),len(pet),len(lv1)] == s["route_counts"]
            fl = sorted({proj97["area_metadata"][areas97[r[0]]]["floor"] for r in pet})
            pet_idx = sorted({instances97[r[4]] for r in pet})
            levels = [dict(instance_index=i,id=proj97["instance_metadata"][i]["id"],level=proj97["instance_metadata"][i]["level"]) for i in pet_idx]
            return dict(base, grade="SAVED_POSITIVE_DOUBLE_FLAG_ROUTES" if pet else "SAVED_POSITIVE_NON_DOUBLE_FLAG_ONLY" if rr else "NO_POSITIVE_ROUTE_IN_RETAINED_PROJECTION",
                route_index=ri,positive_route_count=len(rr),double_flag_route_count=len(pet),lv1_double_flag_route_count=len(lv1),
                instance_indices=sorted({instances97[r[4]] for r in rr}),area_indices=sorted({areas97[r[0]] for r in rr}),
                group_ids=sorted({r[2] for r in pet}),floor_ids=fl,floor_reference_indices=[floor_indices97.get(x) for x in fl],pet_flag_1_instance_levels=levels)
        expected97 = [dict(collision_index=i,left=role_side97(r["left"]),right=role_side97(r["right"]),
            qualification="BOTH_EXACT_PROJECTED_FIELDS_EQUAL_NOT_FULL_ROW_OR_IDENTITY" if r["both_selected_exact"] else "NO_EXACT_SELECTED_ROW_DO_NOT_INFER_ZERO_ROUTES",official_identity_verified=False)
            for i,r in enumerate(d["hf96"]["rows"]) if r["relation"] == "SAME_NAME_GRAPHIC" and not r["differing_projected_fields"]]
        assert roles97["rows"] == expected97
        exact97 = [r for r in expected97 if r["qualification"].startswith("BOTH")]
        summary97 = dict(pairs=len(expected97),both_exact_pairs=len(exact97),unassessed_pairs=len(expected97)-len(exact97),
            distinct_positions=len({r[s]["position"] for r in expected97 for s in ("left","right")}),
            exact_pairs_with_lv1_left=sum(r["left"]["lv1_double_flag_route_count"] > 0 for r in exact97),
            exact_pairs_with_lv1_right=sum(r["right"]["lv1_double_flag_route_count"] > 0 for r in exact97),
            exact_pairs_right_positive=sum(r["right"]["double_flag_route_count"] > 0 for r in exact97),
            exact_pairs_right_no_positive=sum(r["right"]["positive_route_count"] == 0 for r in exact97),
            right_floor_125_pairs=sum(r["right"]["floor_ids"] == [125] for r in exact97),
            right_floor_20901_20902_pairs=sum(r["right"]["floor_ids"] in ([20901],[20902]) for r in exact97),official_closures=0)
        assert roles97["summary"] == summary97 == m["supplement_hf97"]
        assert len(expected97) == 10 and len(exact97) == 6
        assert {(e["pointer"][1], l["pointer"][1]) for e in high45 for l in e["linked_records"] if l["source"] == "hf97"} == {(r[s]["position"],j) for j,r in enumerate(expected97) for s in ("left","right")}
        assert sum(l["source"] == "hf97" for e in entries for l in e["linked_records"]) == 20
    if "hf96" in d:
        collision = d["hf96"]
        for path, sha in collision["input_git_blobs"].items():
            assert blob((ROOT / path).read_bytes()) == sha
        source = d["tw75"]["pet_flag_1_field_projections"]
        selected = d["hf76"]["rows"]
        ranges = d["tw75_birth"]["rows"]
        fields = ["name","graphic","elements","base","initnum","lvup_literal","skill_slot_capacity","skill_slots"]
        assert collision["fields_compared"] == fields
        assert len(source) == len(selected) == len(ranges) == 467
        def collision_position(i):
            a, b, c = source[i], selected[i], ranges[i]
            assert a["template_id"] == b["template_id"] == c["template_id"]
            assert a["row_sha256"] == b["row_sha256"] == c["source_row_sha256"]
            exact = b["selected_table_grade"] == "EXACT_SHARED_TEMPLATE_ROW"
            return dict(position=i, template_id=a["template_id"], row_sha256=a["row_sha256"],
                        selected_table_grade=b["selected_table_grade"], selected_row_sha256=b["selected_row_sha256"],
                        rank=c["rank"], route_counts=[b["positive_route_count"], b["double_pet_flag_route_count"],
                        b["lv1_double_pet_flag_route_count"]] if exact else None,
                        reward_instance_id=b["saved_reward_instance_id"] if exact else None)
        expected = []
        for i, a in enumerate(source):
            for j in range(i+1, len(source)):
                b = source[j]
                if a["name"] != b["name"] and a["graphic"] != b["graphic"]:
                    continue
                relation = ("SAME_NAME_GRAPHIC" if a["graphic"] == b["graphic"] else "SAME_NAME_DIFFERENT_GRAPHIC") if a["name"] == b["name"] else "SAME_GRAPHIC_DIFFERENT_NAME"
                left, right = collision_position(i), collision_position(j)
                both = left["route_counts"] is not None and right["route_counts"] is not None
                differs = (left["route_counts"], left["reward_instance_id"]) != (right["route_counts"], right["reward_instance_id"])
                expected.append(dict(left=left,right=right,relation=relation,
                    differing_projected_fields=[key for key in fields if a[key] != b[key]],
                    both_selected_exact=both, selected_route_or_reward_reference_differs=differs if both else None,
                    official_identity_verified=False))
        assert collision["rows"] == expected
        count = collections.Counter
        linked = {r[s]["position"] for r in expected for s in ("left","right")}
        collision_summary = dict(positions=len(source), pairs=len(expected), linked_positions=len(linked),
            relation_counts=dict(count(r["relation"] for r in expected)),
            field_difference_counts=dict(count(f for r in expected for f in r["differing_projected_fields"])),
            both_selected_exact=sum(r["both_selected_exact"] for r in expected),
            selected_route_or_reward_reference_differs=sum(r["selected_route_or_reward_reference_differs"] is True for r in expected),
            conditional_rank_differs=sum(r["left"]["rank"] != r["right"]["rank"] for r in expected),
            same_name_graphic_no_projected_difference=sum(r["relation"] == "SAME_NAME_GRAPHIC" and not r["differing_projected_fields"] for r in expected),
            same_name_graphic_skill_slots_only=sum(r["relation"] == "SAME_NAME_GRAPHIC" and r["differing_projected_fields"] == ["skill_slots"] for r in expected),
            official_closures=0)
        assert collision["summary"] == collision_summary == m["supplement_hf96"]
        assert len(expected) == 55 and len(linked) == 89
        assert {(e["pointer"][1], l["pointer"][1]) for e in high45 for l in e["linked_records"] if l["source"] == "hf96"} == {(r[s]["position"], j) for j,r in enumerate(expected) for s in ("left","right")}
        assert sum(l["source"] == "hf96" for e in entries for l in e["linked_records"]) == 110
    if "hf95" in d:
        late_skill = d["hf95"]
        for path, sha in late_skill["input_git_blobs"].items():
            assert blob((ROOT / path).read_bytes()) == sha
        assert late_skill["source"]["qualification"] == "LATER_EDITED_COMMUNITY_REPOST_NOT_INDEPENDENT_PERIOD_OR_OPERATOR_EVIDENCE"
        assert [r["hf94_index"] for r in late_skill["rows"]] == [2,3,4,5,6,7,1]
        for j, row in enumerate(late_skill["rows"]):
            old = d["hf94"]["rows"][row["hf94_index"]]
            assert old["name"] == row["name"]
            if row["role"] != "FUSION_FORM_ONLY_IDENTITY_UNRESOLVED":
                assert old["additional_skill_reference"] == row["skill"]
            else:
                assert old["additional_skill_reference"] is None
            assert not any(row[k] for k in ("official_skill_verified", "official_birth_skill_verified", "runtime_verified"))
            matched = [e for e in entries if e["source"] == "hf94" and e["pointer"] == ["rows", row["hf94_index"]]]
            assert len(matched) == 1
            assert [l["pointer"] for l in matched[0]["linked_records"] if l["source"] == "hf95"] == [["rows", j]]
        assert sum(l["source"] == "hf95" for e in entries for l in e["linked_records"]) == 7
        assert sum(r["effect_conflict"] for r in late_skill["rows"]) == 2
        assert len({r["skill"] for r in late_skill["rows"]}) == 3
        assert late_skill["summary"]["official_closures"] == 0
    roles58 = d["hf58"]["rows"]
    master58 = d["tw75"]["pet_flag_1_field_projections"]
    originals58 = {r["tw75_row_index"]: r for r in d["hf50"]["projection"]["records"]}
    assert [r["position"] for r in roles58] == d["hf57"]["summary"]["positions_without_exact_name_grid"]
    assert source_counts["hf58"] == 18
    assert d["hf58"]["strict_residual_positions"] == len(d["hf49"]["remaining_gap_row_indices"])
    assert d["hf58"]["new_official_acquisition_closures"] == 0 and d["hf58"]["official_species_count"] is None
    for j, role in enumerate(roles58):
        i = role["position"]
        master = master58[i]
        assert (role["template_id"], role["name"], role["graphic"], role["master_row_sha256"]) == (
            master["template_id"], master["name"], master["graphic"], master["row_sha256"])
        selected = originals58[i]["source_pairs"][0]
        assert selected["match"] == "EXACT_ROW" and selected["base_row_sha256"] == master["row_sha256"]
        instance, = selected["instances"]
        assert (role["selected_instance_id"], role["selected_level"], role["selected_instance_pet_flag"]) == (
            instance["instance_id"], instance["level"], instance["pet_flag"])
        assert role["retain_strict_gap"] and not role["official_acquisition_verified"]
        assert set(role["documentary_sources"]) <= d["hf58"]["documentary_sources"].keys()
        same_graphic = [n for n, candidate in enumerate(master58)
                        if n != i and candidate["graphic"] == master["graphic"]]
        assert role["other_same_graphic_positions"] == same_graphic
        assert any(l["source"] == "hf58" and l["pointer"] == ["rows", j] and l["qualification"] == role["role"]
                   for l in high45[i]["linked_records"])
        other = role["related_position"]
        if other is not None:
            assert other in same_graphic and master58[other]["row_sha256"] != master["row_sha256"]
            assert role["compared_fields_differ"] == [
                k for k in d["hf58"]["field_comparison_order"] if master[k] != master58[other][k]]
            assert any(l["source"] == "hf58" and l["pointer"] == ["rows", j]
                       and l["qualification"] == "SHARED_GRAPHIC_WITH_SEPARATE_ROLE_CANDIDATE"
                       for l in high45[other]["linked_records"])
    assert source_counts["hf56"] == 10 and source_counts["hf56_replay"] == 14 and source_counts["hf56_preflight"] == 5
    assert {i for i,e in enumerate(high45) if any(l["source"]=="hf56" for l in e["linked_records"])} == {108,109,110,111,144,187,309,317,318,401}
    assert all(r["retain_strict_gap"] and not r["official_acquisition_verified"] for r in d["hf56"]["rows"])
    assert source_counts["hf54"] == 3
    assert {i for i,e in enumerate(high45) if any(l["source"]=="hf54" for l in e["linked_records"])} == {387,453,454}
    assert source_counts["hf53"] == 4
    assert {i for i,e in enumerate(high45) if any(l["source"]=="hf53" for l in e["linked_records"])} == {68,75,144,208}
    assert source_counts["hf52"] == 4
    assert {i for i,e in enumerate(high45) if any(l["source"]=="hf52" for l in e["linked_records"])} == {67,144,171,208}
    preset_lookup = [e for e in entries if e["source"] == "hf51_petabi"]
    assert len(preset_lookup) == 28
    assert sum(e["role"] == "PRESERVED_VIP_PRESET_PET_CANDIDATE" for e in preset_lookup) == 27
    for i, e in enumerate(high45):
        for evidence in e["linked_records"]:
            if evidence["qualification"] == "SAVED_LV1_TRAINER_REWARD_CONFIGURATION_NOT_OFFICIAL_AWARD":
                assert e["detail"]["template_id"] in (161, 162, 163, 164)
                assert resolve(d, evidence["source"], evidence["pointer"])["path"] == "sa60/newbie/m_tiger"
            elif evidence["source"] in ("hf47", "hf48", "hf49", "hf50"):
                row = resolve(d, evidence["source"], evidence["pointer"])
                assert (row["tw75_row_index"], row["template_id"]) == (i, e["detail"]["template_id"])
    assert all(not g["official_acquisition_verified"] for g in g46)
    assert sum(e["detail"]["saved_mixed25_acquisition"]["match_status"] == "EXACT_SHARED_TEMPLATE_ROW" for e in high45) == 440
    assert sum(e["detail"]["saved_mixed25_acquisition"]["positive_route_count"] > 0 for e in high45) == 123
    assert sum(e["detail"]["saved_mixed25_acquisition"]["double_pet_flag_route_count"] > 0 for e in high45) == 118
    assert sum(e["detail"]["saved_mixed25_acquisition"]["lv1_double_flag_route_count"] > 0 for e in high45) == 94
    assert sum(l["source"] == "hf45" and l["pointer"][:2] == ["projection","claimed_tw75_rows"] for e in high45 for l in e["linked_records"]) == 467
    assert sum(l["source"] == "hf45" and l["pointer"][:2] == ["projection","mixed25_template_routes"] for e in high45 for l in e["linked_records"]) == 123
    assert all(not e["detail"]["saved_mixed25_acquisition"]["official_acquisition_verified"] for e in high45)
    assert len(d["hf45_floor"]["rows"]) == 281
    assert len(d["hf44"]["rows"]) == 4
    assert len({n for s in d["hf44"]["rows"] for n in s["pet_slots"]}) == 15
    for source in ("tw10","tw75"):
        assert sum(any(l["source"] == "hf44" for l in e["linked_records"]) for e in entries if e["source"] == source) == 15
        assert sum(l["source"] == "hf44" for e in entries if e["source"] == source for l in e["linked_records"]) == 18
    assert len(d["hf43"]["projection"]["templates"]) == 5
    assert sum(l["source"] == "hf43" and l["pointer"][:2] == ["projection","templates"] for e in entries if e["source"] == "tw10" for l in e["linked_records"]) == 5
    assert sum(l["source"] == "hf43" and l["pointer"][:2] == ["projection","templates"] for e in entries if e["source"] == "tw75" for l in e["linked_records"]) == 5
    for source in ("tw10","tw75"):
        assert sum(any(l["source"] == "hf43" and l["pointer"][:2] == ["projection","scripts"] for l in e["linked_records"]) for e in entries if e["source"] == source) == 17
    assert len(d["hf42"]["rows"]) == len(d["hf42_raw"]["rows"]) == len(d["hf42_cross"]["rows"]) == 36
    assert sum(l["source"] == "hf42_cross" for e in entries if e["source"] == "tw10" for l in e["linked_records"]) == 33
    assert sum(l["source"] == "hf42_cross" for e in entries if e["source"] == "tw75" for l in e["linked_records"]) == 36
    assert sum(l["qualification"] == "SAVED_REWARD_GRAPHIC_ONLY_NAME_CONFLICT_NOT_IDENTITY" and l["source"] == "hf42_cross" for e in entries for l in e["linked_records"]) == 2
    assert len(d["hf41"]["rows"]) == 57
    assert sum(l["source"] == "hf41" for e in entries if e["source"] == "tw10" for l in e["linked_records"]) == 57
    assert sum(l["source"] == "hf41_archive" for e in entries if e["source"] == "tw10" for l in e["linked_records"]) == 148
    assert all(not r["official_tw10_acquisition_verified"] and r["official_tw10_native_stats"] is None and r["official_first_release_date"] is None for r in d["hf41"]["rows"])
    wulibulu, weibo, beiluobaoli = cases
    panel = wulibulu["japan_album_panel"]
    assert panel["level"] == 19 and panel["visible_element_bar_center_widths_px"] == [0, 0, 56, 24]
    assert panel["deployment_build"] is None and not panel["panel_is_birth_or_growth_series"]
    assert weibo["japan_album_panel"]["album_name"] != weibo["japan_album_panel"]["archived_jp_operator_name_at_ordinal"]
    (configured_2079,) = (
        ins for template in weibo["mixed25_template_refs"] for ins in template["selected_instances"]
        if template["file"] == "enemybase.txt" and ins["id"] == 2079
    )
    assert configured_2079["pet_flag"] == 0 and weibo["later_2079_instance_comparison"]["instance_pet_flag"] == 1
    location = beiluobaoli["specific_capture_location_reference"]
    assert location["period_printed_coordinate"] == [44, 15] and not location["encounter_or_capture_executed"]
    assert {tuple(route["level"]) for route in location["selected_mixed25_positive_routes"]} == {(1, 1), (34, 35)}
    assert all(
        route["floor"] == 10406 and route["rect"][0] <= 44 <= route["rect"][2]
        and route["rect"][1] <= 15 <= route["rect"][3]
        for route in location["selected_mixed25_positive_routes"]
    )
    assert {x["claim"]["lane"] for x in hf36 if x["name"]=="格鲁西斯"}=={"精灵觉醒2.5","特色8.5"}
    assert any(x["claim"].get("prior_source_for_2025") for x in hf36 if x["name"]=="奇格拉" and x["year"]==2016)
    assert any(x["claim"].get("prior_source_for_2025") for x in hf36 if x["name"]=="多格斯" and x["year"]==2016)
    if "hf74" in d:
        visual_entries=[e for e in entries if e.get("detail") and "visual_reference" in e["detail"]]
        vc=collections.Counter(e["source"] for e in visual_entries)
        assert vc["tw85_grid"]==1889 and vc["tw85_spr"]==1696 and vc["tw75"]==467
        assert all(not e["detail"]["visual_reference"]["original_runtime_verified"] and not e["detail"]["visual_reference"]["official_identity_verified"] for e in visual_entries)
        grid=[e for e in visual_entries if e["source"]=="tw85_grid"]
        assert all(e["detail"]["visual_reference"]["portrait_status"]=="ALL_STRICT" for e in grid)
        assert collections.Counter(e["detail"]["visual_reference"]["album_position_motion_status"] for e in grid)=={"ALL_CANVAS_COMPLETE":1883,"SOME_CANVAS_COMPLETE":6}
        assert sum(any(l["source"]=="hf72" for l in e["linked_records"]) for e in grid)==6
        assert all(e["detail"]["visual_reference"]["qualification"]=="CROSS_SOURCE_NUMERIC_GRAPHIC_ONLY_NOT_IDENTITY" for e in visual_entries if e["source"]=="tw75")
        master = [e["detail"]["visual_reference"]["motion_groups"] for e in visual_entries if e["source"] == "tw75"]
        assert len(master) == 467 and all(groups for groups in master)
        assert all(g["status"] in ("STRICT_COMPLETE", "BOUNDED_COMPLETE") for groups in master for g in groups)
        assert sum(all(g["status"] == "STRICT_COMPLETE" for g in groups) for groups in master) == 430
        residual = visual_graphic(d, 100400, full=True)["results"]
        assert [g["group_index"] for g in residual] == [363]
        assert residual[0]["status"] == "EARLIER_SELECTED_EXACT_SPR_AND_RD"
        assert len(residual[0]["linked_original_records"][0]["record"]) == 344
        assert visual_graphic(d, -1)["results"] == []
        print("PET74_LOOKUP="+json.dumps(dict(vc),sort_keys=True),flush=True)
    if "hf101" in d:
        cn = [e for e in entries if e["source"] == "cn50"]
        refs = [e["detail"]["cn50_motion_reference"] for e in cn]
        assert len(cn)==305 and collections.Counter(r["motion_status"] for r in refs)=={"ALL_STRICT":284,"ALL_CANVAS_COMPLETE":21}
        assert all(not r["original_runtime_verified"] and not r["official_identity_verified"] for r in refs)
        assert {l["pointer"][1] for e in cn for l in e["linked_records"] if l["source"]=="hf101_raw"}==set(d["hf101_raw"]["observations"])
        assert all(e["source"]=="cn50" for e in entries if e.get("detail") and "cn50_motion_reference" in e["detail"])
    if "cn85_original" in d:
        cn85 = [e for e in entries if e["source"] == "cn85_original"]
        cn50 = [e for e in entries if e["source"] == "cn50"]
        assert len(cn85) == 548 and len({e["labels"][0] for e in cn85}) == 540
        assert len({e["detail"]["compiled_slot"] for e in cn85}) == len({e["detail"]["compiled_face"] for e in cn85}) == 548
        assert len(cn50) == 305 and all("cn85_compiled_crosswalk" in e["detail"] for e in cn50)
        assert sum(e["detail"]["cn85_compiled_crosswalk"]["exact_same_ordinal"] for e in cn50) == 304
        assert all(not e["detail"][k] for e in cn85 for k in ("native_selector_verified","original_portrait_verified","official_release_verified","same_deployment_server_fields_verified"))
        assert sum(544 <= e["detail"]["physical_ordinal"] < 593 for e in cn85)==27
        assert collections.Counter(e["detail"]["portrait_candidate_grade"] for e in cn85)=={"ORIGINAL_RD_SINGLE_CANDIDATE":543,"ORIGINAL_RD_MULTIPLE_CANDIDATES":4,"ORIGINAL_RD_LENGTH_DISCREPANCY":1}
        assert sum(len(e["detail"]["original_rd_candidates"]) for e in cn85)==552
        assert sum(e["detail"]["cn85_same_ordinal_rd_reference"]["same_label"] and e["detail"]["cn85_same_ordinal_rd_reference"]["exact_rd_hash"] for e in cn50)==304
        assert sum(len(e["detail"]["cn85_exact_spr_reference"]) for e in cn50)==594
        assert len(list(search(entries,"ordinal:547",exact=True,source="cn85_original")))==1
        assert not list(search(entries,"ordinal:544",exact=True,source="cn85_original"))
        assert len(list(search(entries,"艾柏瑞",exact=True,source="cn85_original"))) == 1
        assert list(search(entries,"艾柏瑞",exact=True,source="cn85_original"))[0]["detail"]["physical_ordinal"] == 439
        assert list(search(entries,"ordinal:314",exact=True,source="cn85_original"))[0]["labels"] == ["艾比斯"]
        print("PET124_FULL_LOOKUP_PASS 548 named positions, 540 labels, 552 RD candidates, 304 same-label exact RD, 594 exact SPR links",flush=True)
    if "review_tw75_portrait" in d:
        tw=[e for e in entries if e["source"]=="tw75"]
        cn=[e for e in entries if e["source"]=="cn85_original"]
        assert len(tw)==467 and len(cn)==548
        assert collections.Counter(e["detail"]["review_portrait_reference"]["grade"] for e in tw)=={"EXACT_NAME_GRAPHIC_UNIQUE_ALIAS":424,"NAME_ONLY":15,"NO_EXACT_NAME":28}
        assert sum("review_portrait_conflict" in e["detail"] for e in tw)==43
        assert collections.Counter(e["detail"]["review_motion_reference"]["grade"] for e in cn if "review_motion_reference" in e["detail"])=={"CN50_EXACT_NAME_FACE_RD_SPR":61,"TW85_NAME_VARIANT_EXACT_FACE_RD_SPR":70}
        assert all(not e["detail"]["review_portrait_reference"]["same_build_verified"] for e in tw)
        assert all(not e["detail"]["review_motion_reference"]["native_selector_verified"] for e in cn if "review_motion_reference" in e["detail"])
        assert len(entries)==5924
        print("PET_REVIEW_LOOKUP_PASS 467 portrait projections, 43 conflicts, 131 motion references; unchanged query occurrences",flush=True)
    assert m["expected"]["official_species_count"] is None and not m["original_assets_published"]
    print(json.dumps(summary(entries),ensure_ascii=False,indent=2))
def main():
    p=argparse.ArgumentParser(description=__doc__)
    query=p.add_mutually_exclusive_group()
    query.add_argument("--query")
    modes=p.add_mutually_exclusive_group()
    modes.add_argument("--legacy-pet16",action="store_true",help="search the retained PET16 independent source namespaces")
    modes.add_argument("--documentary",action="store_true",help="search historical commission, skill and release evidence separately")
    modes.add_argument("--history",action="store_true",help="browse pinned annual and regional historical evidence")
    modes.add_argument("--annual-names",action="store_true",help="search literal named evidence in annual source receipts")
    p.add_argument("--year",type=int,choices=range(1999,2027));p.add_argument("--region",choices=("CN","TW","HK_MO","KR","JP","OTHER"));p.add_argument("--version",help="exact explicitly indexed version label, history only")
    query.add_argument("--visual-graphic", type=int, help="exact preserved TW85 graphic number, including residual groups")
    p.add_argument("--exact",action="store_true");p.add_argument("--variants",action="store_true")
    p.add_argument("--source");p.add_argument("--full",action="store_true");p.add_argument("--summary",action="store_true");p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    if args.annual_names:
        if args.visual_graphic is not None: p.error("--annual-names and --visual-graphic are separate lookups")
        from stoneage_pet_annual_names import run
        run(args)
        return
    if args.history:
        if args.visual_graphic is not None: p.error("--history and --visual-graphic are separate lookups")
        from stoneage_pet_history_access import run
        run(args)
        return
    if any((args.year,args.region,args.version)): p.error("--year, --region and --version require --history or --annual-names (version history only)")
    if args.documentary:
        if args.visual_graphic is not None: p.error("--documentary and --visual-graphic are separate lookups")
        from stoneage_pet_documentary_access import run
        run(args)
        return
    if args.legacy_pet16:
        if args.visual_graphic is not None: p.error("--legacy-pet16 and --visual-graphic are separate lookups")
        from stoneage_pet_legacy_access import run
        run(args)
        return
    m,d=load()
    if args.visual_graphic is not None:
        if args.source or args.verify or args.summary:
            p.error("--visual-graphic is a separate physical-group lookup")
        print(json.dumps(visual_graphic(d, args.visual_graphic, args.full), ensure_ascii=False, indent=2))
        return
    entries=build(d)
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
