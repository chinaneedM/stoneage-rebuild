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
        add("tw75",["pet_flag_1_field_projections",i],[x["name"]],"CLAIMED_TW75_MASTER_TEMPLATE",[k,x["graphic"]],ls,dict(graphic=x["graphic"],template_id=k,elements=x["elements"],skill_slots=x["skill_slots"],conditional_lv1_panel=b["level1_unmodified_work_panel_marginal_ranges"],conditional_per_level_internal=b["per_level_internal_increment_marginal_ranges"],comparison_floor_ids=e["comparison_floor_ids"],comparison_status=e["comparison_status"],saved_mixed25_acquisition=saved_acquisition))
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
    assert source_counts["hf61"] == 67 + 135
    for row61 in d["hf61"]["rows"]:
        links61 = [l for l in high45[row61["position"]]["linked_records"] if l["source"] == "hf61"]
        assert {resolve(d, l["source"], l["pointer"])["skill_id"] for l in links61
                if l["pointer"][0] == "configured_skill_definitions"} == {
                    slot["skill_id"] for slot in row61["scope"]["petskill.txt"]["source_slots"]}
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
