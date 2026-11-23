#!/usr/bin/env python3
"""Source-qualified PET16 catalogue lookup and PET17 numeric-only graphic tracing.

This is a research index, not a verified official pet species registry.
"""
from pathlib import Path
import argparse
import json

PATH = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json"
PET13_PATH = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-PET-MODULE-13-ORIGINAL-CAPTURE-TEMPLATE-ATTRIBUTES-SKILLS-R1.json"
PET19_PATH = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-PET-MODULE-19-MISSING-SKILL-SOURCE-GAP-AUDIT-R1.json"
PET21_PATH = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-PET-MODULE-21-OFFICIAL-WEB-ARCHIVED-IMAGE-REACCESS-R1.json"
PET22_PATH = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-PET-MODULE-22-JP-124-ARCHIVED-IMAGE-RECOVERY-R1.json"
PET23_PATH = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-PET-MODULE-23-JP-LOW-RATE-IMAGE-REACCESS-R1.json"
PET39_PATH = PATH.with_name("STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
PET126R_PATH = PATH.with_name("STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json")
CN50_NATIVE_PATH = PATH.parent.parent / "pets/PET-HIGH-FIRST-CN50-NATIVE-SPR-ALBUM-R1.json"
CN50_RETENTION_PATH = PATH.parent.parent / "pets/PET-HIGH-FIRST-CN50-TW85-ART-RETENTION-R1.json"
CN50_FUSION_PATH = PATH.parent.parent / "pets/PET-HIGH-FIRST-CN50-FUSION-PANELS-R1.json"
CN50_SINA_PATH = PATH.parent.parent / "pets/PET-HIGH-FIRST-CN50-SINA2003-CATALOG-R1.json"
PET41_PATH = PATH.with_name("STONEAGE-PET41-TW-EARLY-WGS-MUSEUM-R1.json")
PET25_OFFICIAL_PATH = PATH.with_name("STONEAGE-PET25-OFFICIAL-RELEASE-ROSTER-R1.json")
PET26_OFFICIAL_PATH = PATH.with_name("STONEAGE-PET26-JP-TW-CLASSIC-OFFICIAL-RELEASE-R1.json")
JP_OFFICIAL_PAGE_PATH = PATH.with_name("STONEAGE-JP-OFFICIAL-PET-CATALOG-R1.json")
CN_OFFICIAL_PAGE_PATH = PATH.with_name("STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-R1.json")

CLIENT_ALBUM = "tw10_client_album"
CN50_COMPILED_ALBUM = "cn50_compiled_album"
TW_MUSEUM = "tw_early_wgs_museum"

# Only datasets carrying an original numeric graphic field participate.
# Official JP/CN page ordinals/image filenames are NOT client graphic numbers.
GRAPHIC_DATASETS = (
    "later2016_templates", "later2016_graphics",
    "mixed25_main", "mixed25_alternative", "tw10_visual",
)


def load_catalog(path=PATH):
    """Load the frozen PET16 catalogue and the Taiwan client and museum indexes."""
    catalog = json.loads(path.read_text(encoding="utf-8"))
    if path.resolve() == PATH:
        album = json.loads(PET39_PATH.read_text(encoding="utf-8"))["records"]
        catalog["datasets"][CLIENT_ALBUM] = album
        cn50 = json.loads(PET126R_PATH.read_text(encoding="utf-8"))
        if (cn50.get("scope") != "ORIGINAL_CLASSIC_PC_ONLY" or
            cn50["metrics"]["compiled_source_named_rows"] != 305 or
            len(cn50["records"]) != 362 or
            cn50["negative_boundaries"]["CN50_same_build_name_to_SPR_selector_proven"]):
            raise ValueError("CN50-album-source-grade-or-count-mismatch")
        native = json.loads(CN50_NATIVE_PATH.read_text(encoding="utf-8"))
        by_ordinal = {row["ordinal"]: row for row in native["records"]}
        if (native["schema"] != "stoneage.pet_high_first.cn50_native_spr_to_album.r1"
            or len(native["records"]) != len(by_ordinal) or len(by_ordinal) != 305):
            raise ValueError("CN50 native source routes missing or duplicated")
        sina = json.loads(CN50_SINA_PATH.read_text(encoding="utf-8"))
        if (sina["schema"] != "stoneage.pet.cn50_sina_2003_source_crosswalk.r1"
            or sina["published_number_is_server_species_id"]
            or sina["serving_version_and_official_release_established_by_web_join"]):
            raise ValueError("CN50 editorial catalogue is not a bounded source crosswalk")
        sina_by_ordinal = {}
        for row in sina["rows"]:
            ordinal = row["cn50_album_ordinal_by_name_only"]
            if ordinal is None:
                continue
            page = sina["pages"][row["page"]]
            sina_by_ordinal.setdefault(ordinal, []).append({
                "source_url": page["url"],
                "displayed_date": page["displayed_date"],
                "row_in_pet_table": row["row_in_pet_table"],
                "printed_catalogue_number": row["printed_number"],
                "rebirth_variant_label": row["rebirth_variant_label"],
                "reported_elements": row["reported_elements"],
                "innate_skill_cell_has_text": row["innate_skill_cell_has_text"],
                "level_one_acquisition_cell_has_text": row["level_one_acquisition_cell_has_text"],
            })
        year_card = sina["cn30_year_card_announcement"]
        year_card_by_ordinal = {
            row["cn50_album_ordinal_by_name_only"]: {
                "source_url": year_card["archive_url"],
                "displayed_date": year_card["displayed_article_date"],
                "main_element": row["main_element"],
            }
            for row in year_card["named_variants"]
        }
        fusion = json.loads(CN50_FUSION_PATH.read_text(encoding="utf-8"))
        if (fusion["schema"] != "stoneage.pet.cn50_sina_2003_fusion_panels.r1"
            or fusion["image_serving_build_or_operator_verified"]
            or fusion["printed_number_is_official_pet_id"]
            or fusion["observations_are_official_template_or_growth_parameters"]):
            raise ValueError("CN50 fusion sources are not bounded panel observations")
        fusion_by_ordinal = {
            row["cn50_album_ordinal"]: {
                "source_url": fusion["pages"][str(row["page"])]["url"],
                **{key: row[key] for key in ("image_url", "displayed_name", "printed_number", "image")},
            }
            for row in fusion["records"]
        }
        may_fusion = fusion["may_editorial_catalogue"]
        may_fusion_by_ordinal = {
            row["cn50_album_ordinal_by_exact_name"]: {
                "source_url": may_fusion["url"],
                "article_date": may_fusion["article_date"],
                "reported_elements": row["reported_elements"],
                "formula_cell_has_text": row["formula_cell_has_text"],
            }
            for row in may_fusion["rows"]
            if row["cn50_album_ordinal_by_exact_name"] is not None
        }
        retention = json.loads(CN50_RETENTION_PATH.read_text(encoding="utf-8"))
        if (retention["schema"] != "stoneage.pet.cn50_tw85_art_retention.r1"
            or retention["tw85_runtime_pet_selector_or_name_table_verified"]
            or retention["official_release_or_gameplay_verified"]):
            raise ValueError("TW85 retention is resource evidence")
        retention_by_ordinal = {r["cn50_album_ordinal"]: r for r in retention["records"]}
        if set(retention_by_ordinal) != set(by_ordinal) or len(retention["records"]) != len(retention_by_ordinal):
            raise ValueError("TW85 retention atlas is incomplete")
        cn50_named = []
        for raw in cn50["records"]:
            if raw["label_as_compiled_GB18030"] is None:
                continue
            route = by_ordinal[raw["ordinal"]]
            if (route["compiled_name"] != raw["label_as_compiled_GB18030"]
                or route["exe_row_sha256"] != raw["source_exe_row_sha256"]
                or route["portrait_alias"] != raw["source_raw_trailing_u32"]
                or not route["spr_groups"]):
                raise ValueError("CN50 native SPR route disagrees with compiled source row")
            cn50_named.append({
                "id": raw["record_key"], "source": raw["carrier"],
                "name_as_written": raw["label_as_compiled_GB18030"],
                "source_ordinal": raw["ordinal"],
                "compiled_raw_i32": raw["source_raw_first_i32"],
                "compiled_raw_u32": raw["source_raw_trailing_u32"],
                "graphic_number": None,
                "TW10_ordinal_based_candidate_SPR_only":
                    raw["TW10_ordinal_based_graphic_hypothesis"],
                "same_carrier_candidate_SPR_present":
                    raw["same_CAB_SPR_group_for_hypothesis_present"],
                "TW10_cross_version_exact_SPR_hash":
                    raw["TW10_retail_exact_same_SPR_segment_at_this_ordinal"],
                "cn50_native_spr_group_numbers": [group["spr_group"] for group in route["spr_groups"]],
                "cn50_native_held_pet_spr_group_numbers": [
                    group["spr_group"] for group in route["spr_groups"]
                    if group["held_pet_path_also_maps_to_slot"]
                ],
                "cn50_portrait_bitmap_after_ordered_adrn_load":
                    route["portrait_lookup_after_ordered_load"],
                "sina_2003_editorial_same_name_rows": sina_by_ordinal.get(raw["ordinal"], []),
                "cn30_2002_year_card_same_name_announcement": year_card_by_ordinal.get(raw["ordinal"]),
                "sina_2003_may_fusion_editorial_entry": may_fusion_by_ordinal.get(raw["ordinal"]),
                "sina_2003_fusion_panel": fusion_by_ordinal.get(raw["ordinal"]),
                "tw85_preserved_art_comparison": retention_by_ordinal[raw["ordinal"]],
                "source_evidence": "SAME_CAB_STATIC_NATIVE_SPR_TO_COMPILED_ALBUM_SLOT",
                "official_live_release_confirmed": False,
                # The source code resolves SPR to a slot, which can have several SPR groups.
                "native_same_build_graphic_selector_proven": False,
            })
        if len(cn50_named) != 305:
            raise ValueError("CN50-compiled-source-name-rows-missing")
        catalog["datasets"][CN50_COMPILED_ALBUM] = cn50_named
        museum = json.loads(PET41_PATH.read_text(encoding="utf-8"))
        pages = {page["filename"]: page["replay_url"] for page in museum["pages"]}
        catalog["datasets"][TW_MUSEUM] = [
            {**row, "id": f"TW_WGS_MUSEUM:{row['web_ordinal']:04d}",
             "source": museum["evidence"], "source_page_replay_url": pages[row["source_page"]]}
            for row in museum["rows"]
        ]
        counts = catalog["metrics"]["source_namespace_row_counts_NOT_species"]
        counts[CLIENT_ALBUM] = len(album)
        counts[CN50_COMPILED_ALBUM] = len(cn50_named)
        counts[TW_MUSEUM] = len(museum["rows"])
        catalog["metrics"]["record_total_NOT_species"] = sum(counts.values())
    return catalog


def lookup(catalog, query="", dataset=None, limit=20, details=False):
    """Return original source-separated records; never merge sources into species."""
    q = str(query).strip().casefold()
    result = []
    for group, records in catalog["datasets"].items():
        if dataset and group != dataset:
            continue
        for row in records:
            fields = (row.get("id"), row.get("name_as_written"), row.get("label_as_written"),
                      row.get("template_id"), row.get("graphic_number"), row.get("web_ordinal"),
                      row.get("tw10_same_printed_name_graphic"),
                      *row.get("cn50_native_spr_group_numbers", ()))
            if q and not any(q in str(v).casefold() for v in fields if v is not None):
                continue
            result.append(
                {"dataset": group, **row} if details else
                {"dataset": group, "id": row["id"], "source": row["source"],
                 "name": row.get("name_as_written"), "template_id": row.get("template_id"),
                 "graphic_number": row.get("graphic_number")}
            )
            if len(result) >= limit:
                return result
    return result


def graphic_trace(catalog, graphic_number, limit=20):
    """Trace equal *numeric* graphic references; no same-pet identity inference.

    Record totals are uncapped. Each source's displayed original records is capped.
    """
    if isinstance(graphic_number, bool) or not isinstance(graphic_number, int) or graphic_number <= 0:
        raise ValueError("graphic_number must be a positive integer")
    if limit < 1:
        raise ValueError("limit must be positive")

    groups = {}
    for group in GRAPHIC_DATASETS:
        matched = [
            row for row in catalog["datasets"][group]
            if row.get("graphic_number") == graphic_number
        ]
        groups[group] = {
            "matching_original_rows": len(matched),
            "returned_rows": len(matched[:limit]),
            "truncated": len(matched) > limit,
            "records": matched[:limit],
        }
    album_record = next((row for row in catalog["datasets"].get(CLIENT_ALBUM, [])
                         if row["graphic_number"] == graphic_number), None)
    museum_matches = [row for row in catalog["datasets"].get(TW_MUSEUM, [])
                      if row["tw10_same_printed_name_graphic"] == graphic_number]
    return {
        "graphic_number": graphic_number,
        "relation": "LITERAL_GRAPHIC_NUMBER_COINCIDENCE_ONLY",
        "official_pet_species_identity_verified": False,
        "same_historical_build_or_server_deployment_verified": False,
        "tw10_original_species_name": None,
        "tw10_same_client_album_record": album_record,
        "tw_museum_exact_printed_name_matches": museum_matches[:limit],
        "official_JP_CN_web_ordinal_or_image_URL_not_mappable_to_graphic": True,
        "note": ("The same graphic number may be reused by multiple source templates. "
                 "A named late-community row never names the TW10 retail sprite. "
                 "Alternative server table rows are not proven concurrently active."),
        "source_separated_matches": groups,
    }


def capture_trace(catalog, pet13, template_id):
    """PET13 original-archive source-qualified capture/skill candidates, not runtime.

    Join a PET13 template to PET16 mixed25 MAIN only when physical row,
    original template ID, original graphic number and all-56-fields SHA agree.
    PETFLG=0 remains outside PET16's filtered PETFLG=1 pet catalogue.
    """
    if isinstance(template_id, bool) or not isinstance(template_id, int) or template_id <= 0:
        raise ValueError("template_id must be a positive integer")
    candidates = [x for x in pet13["templates"] if x["original_template_numeric_ID"] == template_id]
    if len(candidates) > 1:
        raise ValueError("PET13 source template ID is not unique; refusing to guess")
    original = candidates[0] if candidates else None
    linked = []
    skills = []
    if original is not None:
        if original["original_PETFLG"] == 1:
            linked = [
                x for x in catalog["datasets"]["mixed25_main"]
                if (x["original_row"] == original["original_server_template_physical_row"]
                    and x["template_id"] == original["original_template_numeric_ID"]
                    and x["graphic_number"] == original["original_graphic_numeric_ID"]
                    and x["original_fields_sha256"] == original["original_56_column_normalized_sha256"]
                    and x["petflag"] == 1)
            ]
        labels = pet13["same_source_original_petskill_short_labels_private_verified"]
        for link in original["same_archive_original_skill_links"]:
            name_match = [
                x for x in labels
                if (x["skill_id"] == link["source_pet_skill_id"]
                    and x["source_original_row_sha256"] == link["original_skill_normalized_full_row_sha256"])
            ]
            skills.append({
                **link,
                "same_archive_short_name_when_sha_matched":
                    name_match[0]["source_short_name"] if len(name_match) == 1 else None,
                "short_name_original_source_sha_verified": len(name_match) == 1,
                "native_skill_effect_verified": False,
            })
    if len(linked) > 1:
        raise ValueError("ambiguous four-field original row match; refusing to merge")
    return {
        "template_id": template_id,
        "source": "MIXED25_COMMUNITY_PRESERVED_PET13",
        "pet13_original_template_found": original is not None,
        "pet13_original_derived_record": original,
        "pet16_exact_same_source_petflag1_row": linked[0] if linked else None,
        "pet16_match_requires_row_template_graphic_full_fields_sha": True,
        "qualified_same_archive_skill_definitions": skills,
        "compiled_capture_required_item_references_only":
            original["capture_required_item_IDs"] if original is not None else [],
        "original_compiled_capture_selector_native_verified": False,
        "original_capture_success_or_server_execution_verified": False,
        "official_TW10_pet_identity_verified": False,
        "other_petflag_0_templates_NOT_petflag_1": True,
    }


def skill_gap_trace(audit, skill_id=None, limit=20):
    """Read PET19 independently source-qualified missing skill definitions.

    Never copy a same numeric ID from a different skill table into a missing
    definition, and never imply original game skill runtime behavior.
    """
    if skill_id is not None and (isinstance(skill_id, bool) or
                                 not isinstance(skill_id, int) or skill_id <= 0):
        raise ValueError("skill_id must be a positive integer")
    if limit < 1:
        raise ValueError("limit must be positive")
    out = {}
    for source, groups in audit["missing_by_source"].items():
        selected = [g for g in groups if skill_id is None or g["skill_id"] == skill_id]
        out[source] = [{
            "skill_id": g["skill_id"],
            "reference_count": g["reference_count"],
            "source_template_rows": g["source_template_rows"],
            "returned_references": min(len(g["original_references"]), limit),
            "truncated": len(g["original_references"]) > limit,
            "original_references": g["original_references"][:limit],
        } for g in selected]
    return {
        "query_skill_id": skill_id,
        "source_scope": audit["source_scope"],
        "totals_all_skills_not_filtered": audit["totals"],
        "exact_source_provenance": audit["source_refs"],
        "missing_by_source": out,
        "evidence_guards": audit["evidence_guards"],
        "no_original_pet_skill_effect_or_early_official_identity_verified": True,
    }


def operator_image_trace(catalog, pet21, region, ordinal, pet22=None, pet23=None):
    """Show archived operator-web image SHA receipt without mapping any game pet ID."""
    if region not in ("jp", "cn"):
        raise ValueError("region must be 'jp' or 'cn'")
    if isinstance(ordinal, bool) or not isinstance(ordinal, int) or ordinal <= 0:
        raise ValueError("web ordinal must be a positive integer")
    source = "jp_official_web" if region == "jp" else "cn_official_web"
    items = [x for x in catalog["datasets"][source] if x["web_ordinal"] == ordinal]
    if len(items) > 1:
        raise ValueError("nonunique original web ordinal in source catalogue")
    original = items[0] if items else None
    checked = [
        x for x in pet21["records"]
        if x["source_namespace"] == source and x["web_ordinal"] == ordinal
    ]
    if len(checked) > 1:
        raise ValueError("duplicate operator-image probe receipt")
    if checked and (original is None or checked[0]["original_record_id"] != original["id"]):
        raise ValueError("PET21 source receipt does not match original catalogue record")
    later = []
    if pet22 is not None and source == "jp_official_web":
        later = [x for x in pet22["records"] if x["web_ordinal"] == ordinal]
        if len(later) > 1:
            raise ValueError("PET22 contains duplicated JP historical web ordinal")
        if later and (original is None or
                      later[0]["original_operator_web_record_id"] != original["id"]):
            raise ValueError("PET22 source receipt does not match original operator record")
    best_sha = (
        later[0]["best_archival_observation_sha256_or_null"] if later else
        checked[0]["returned_original_media_image_sha256_or_null"] if checked else None
    )
    best_capture = (
        later[0]["best_archival_observation_capture_or_null"] if later else
        checked[0]["observed_image_archive_capture_or_null"] if checked else None
    )
    newest = []
    if pet23 is not None and source == "jp_official_web":
        newest = [x for x in pet23["records"] if x["web_ordinal"] == ordinal]
        if len(newest) > 1:
            raise ValueError("duplicate PET23 JP operator webpage position")
        if newest:
            x = newest[0]
            ref = original["source_refs"][0] if original else {}
            if (original is None or x["original_source_record_id"] != original["id"] or
                    x["historical_operator_original_image_url"] != original["image_reference_url"] or
                    x["original_page_archive_capture"] != ref.get("capture") or
                    x["original_page_bytes_sha256"] != ref.get("sha256")):
                raise ValueError("PET23 source mismatches original official operator HTML")
            if later and later[0]["best_archival_observation_sha256_or_null"] is not None:
                raise ValueError("PET23 cannot overwrite earlier proven archived image")
            if x["image_original_sha256_or_null"] is not None:
                if x["actual_probe_status"] != "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED":
                    raise ValueError("PET23 image SHA not qualified by original byte response")
                best_sha = x["image_original_sha256_or_null"]
                best_capture = x["image_observed_archive_capture_or_null"]
    followup = []
    if pet23 is not None and source == "jp_official_web":
        second = pet23.get("independent_followup_after_initial_receipt", {})
        followup = [x for x in second.get("records", []) if x["web_ordinal"] == ordinal]
        if len(followup) > 1:
            raise ValueError("duplicate PET23 independent source replay webpage position")
        if followup:
            s = followup[0]
            ref = original["source_refs"][0] if original else {}
            if (original is None or s["original_source_record_id"] != original["id"] or
                    s["original_image_url"] != original["image_reference_url"] or
                    s["source_original_page_sha256"] != ref.get("sha256")):
                raise ValueError("PET23 independent replay original official page/source mismatch")
            repeated_sha = s["image_original_sha256_or_null"]
            if repeated_sha is not None:
                if s["image_result_kind"] != "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED":
                    raise ValueError("unqualified PET23 followup GIF SHA")
                if best_sha is not None and repeated_sha != best_sha:
                    raise ValueError("different archived image SHA must remain a historical conflict")
                best_sha = repeated_sha
                best_capture = s["image_archive_capture_or_null"]
    return {
        "source_namespace": source,
        "web_ordinal": ordinal,
        "original_catalogue_record_or_null": original,
        "pet21_probe_status": (
            checked[0]["probe_status"] if checked else
            "NOT_IN_PET21_SAMPLE" if original else "NO_SOURCE_POSITION"
        ),
        "pet21_source_receipt_or_null": checked[0] if checked else None,
        "pet22_source_receipt_or_null": later[0] if later else None,
        "pet23_source_receipt_or_null": newest[0] if newest else None,
        "pet23_independent_replay_source_receipt_or_null": followup[0] if followup else None,
        "best_observed_operator_archived_image_sha256_or_null": best_sha,
        "best_observed_operator_archived_image_capture_or_null": best_capture,
        "operator_web_image_is_not_authenticated_game_sprite": True,
        "original_official_client_species_ID_proven": False,
        "jss1999_tw10_early_same_deployment_proven": False,
        "webpage_and_image_same_capture_instant_proven": False,
        "commercial_image_bytes_in_public_repository": False,
        "image_custody_verified_private": False,
        "permission_for_game_or_public_wiki_use_verified": False,
    }


def official_pc_release_view(pet25, pet26, query="", region=None,
                             check_earlier_web_names=False, jp_page=None, cn_page=None):
    """Search only historically documented original-classic-PC release *events*.

    This deliberately excludes community server templates, sprite IDs, mobile
    derivatives, independent PC remakes and prelaunch-only web positions.
    An event is not a unique species, and dated reporting is not first release.
    """
    if region not in (None, "CN", "JP"):
        raise ValueError("release region must be CN or JP")
    if check_earlier_web_names and (jp_page is None or cn_page is None):
        raise ValueError("both early source-qualified operator web catalogues required")
    sources25 = {x["id"]: x for x in pet25["source_register"]}
    sources26 = {x["id"]: x for x in pet26["sources"]}
    if len(sources25) != len(pet25["source_register"]) or len(sources26) != len(pet26["sources"]):
        raise ValueError("original source register has repeated IDs")
    entries = []
    original_web = {
        "CN": cn_page["records"] if check_earlier_web_names else [],
        "JP": jp_page["records"] if check_earlier_web_names else [],
    }
    for src, rows, registry, status in (
        ("PET25", pet25["confirmed_official_release_records"], sources25,
         "OFFICIAL_IN_GAME_RELEASE_DOCUMENTED"),
        ("PET26", pet26["new_japan_classic_official_release_events"], sources26,
         "OFFICIAL_GAME_RELEASE_DOCUMENTED"),
    ):
        for record in rows:
            if record["status"] != status:
                raise ValueError("unqualified original PC release record")
            name = (record["official_name_as_written"] if src == "PET25"
                    else record["official_name_as_written_or_null"])
            kind = (record["record_identity_kind"] if src == "PET25"
                    else record["identity_kind"])
            if name is None and kind != "UNNAMED_PAIR_ONE_RELEASE_EVENT":
                raise ValueError("unexpected anonymous release category")
            original_ids = record["source_ids"]
            if not original_ids or any(i not in registry for i in original_ids):
                raise ValueError("release record has a missing original source reference")
            if not record["product_line"].startswith("STONEAGE_CLASSIC_PC_"):
                raise ValueError("non-original PC product lineage in release events")
            current_region = record["region"]
            if current_region not in ("CN", "JP"):
                raise ValueError("unexpected release event region")
            date_text = (record["release_documented_no_later_than_or_announced_at"]
                         if src == "PET25" else record["first_published_release_date"])
            event = {
                "source_namespace": src,
                "record_id": record["record_id"] if src == "PET25" else record["id"],
                "region": current_region,
                "product_line": record["product_line"],
                "original_name_or_null": name,
                "record_identity_kind": kind,
                "original_documentary_status": status,
                "source_attestation_date_not_first_actual_release": date_text,
                "first_actual_official_release_date_proven": False,
                "native_original_pc_pet_id": None,
                "native_same_deployment_sprite_link_verified": False,
                "native_same_deployment_stats_skills_verified": False,
                "unique_global_species_contribution": None,
                "source_references": [
                    {"id": key, "url": registry[key]["url"],
                     "source_grade": registry[key].get("layer", registry[key].get("tier"))}
                    for key in original_ids
                ],
            }
            if check_earlier_web_names:
                hits = [
                    {"original_web_record_id": x["record_id"],
                     "name_as_written": x["name_as_written"]}
                    for x in original_web[current_region]
                    if name is not None and x["name_as_written"] == name
                ]
                event["earlier_operator_web_exact_literal_matches"] = hits
                event["web_literal_match_is_not_pet_identity"] = True
                event["web_archive_is_not_a_later_live_promotion"] = True
            entries.append(event)
    if len({(x["source_namespace"], x["record_id"]) for x in entries}) != len(entries):
        raise ValueError("duplicate original documentary release event")
    if len(entries) != (pet25["counts"]["release_documentary_records"] +
                        pet26["counts"]["new_japan_release_events"]):
        raise ValueError("published documentary event counters disagree")
    selected = [
        x for x in entries
        if (region is None or x["region"] == region)
        and (not query or str(query).casefold() in
             " ".join(str(v) for v in (x["record_id"], x["original_name_or_null"],
                                       x["product_line"], x["source_namespace"])).casefold())
    ]
    return {
        "scope": "ONLY_OFFICIAL_ORIGINAL_CLASSIC_PC_DOCUMENTARY_RELEASE_EVENTS",
        "counts_all_unfiltered_not_pet_species": {
            "documentary_release_events": len(entries),
            "named_pet_or_form_release_events": sum(x["record_identity_kind"] == "NAMED_PET"
                                                    for x in entries),
            "family_or_card_series_events": sum(x["record_identity_kind"] == "FAMILY_OR_CARD_SERIES"
                                                 for x in entries),
            "unnamed_pair_events_not_two_separate_documentary_events":
                sum(x["record_identity_kind"] == "UNNAMED_PAIR_ONE_RELEASE_EVENT"
                    for x in entries),
            "unique_original_pc_species_population": None,
            "native_original_pc_species_id_verified": 0,
        },
        "query": query,
        "region_filter": region,
        "returned_event_count": len(selected),
        "early_web_literal_check": check_earlier_web_names,
        "records": selected,
        "negative_boundaries": {
            "no_private_server_templates_in_release_view": True,
            "no_independent_pc_remake_or_mobile_products": True,
            "no_web_order_as_species_id": True,
            "no_cross_version_name_as_identity_without_same_build": True,
            "no_documentary_events_added_as_unique_species": True,
            "no_source_attestation_date_as_proven_first_release": True,
        },
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--query", default="")
    p.add_argument("--dataset", choices=(
        "later2016_templates", "later2016_graphics",
        "mixed25_main", "mixed25_alternative", "tw10_visual",
        "jp_official_web", "cn_official_web", CLIENT_ALBUM, CN50_COMPILED_ALBUM, TW_MUSEUM))
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--summary", action="store_true")
    p.add_argument("--details", action="store_true",
                   help="Include the full original-derived row within its named source")
    p.add_argument("--trace-graphic", type=int, metavar="NUMBER",
                   help="Trace equal numeric graphic references without identity merging")
    p.add_argument("--capture-template", type=int, metavar="TEMPLATE_ID",
                   help="PET13 original same-archive capture item/skill source links (not runtime)")
    p.add_argument("--skill-gaps", action="store_true",
                   help="PET19 missing selected skill definitions with source-separated original row provenance")
    p.add_argument("--skill-id", type=int,
                   help="Filter PET19 missing definitions by positive original numeric skill ID")
    p.add_argument("--operator-web", choices=("jp", "cn"),
                   help="Exact historic operator website source namespace; no client pet IDs")
    p.add_argument("--web-ordinal", type=int,
                   help="Historic official website position, NOT client sprite or pet species ID")
    p.add_argument("--official-releases", action="store_true",
                   help="PET25+PET26 verified classic-PC release DOCUMENTARY events only")
    p.add_argument("--release-region", choices=("CN", "JP"),
                   help="Region filter for --official-releases")
    p.add_argument("--release-web-name-check", action="store_true",
                   help="Exact older CN/JP operator web NAME lookup; never identity")
    p.add_argument("--catalog", type=Path, default=PATH)
    args = p.parse_args()
    if args.limit < 1 or args.limit > 1000:
        p.error("--limit must be 1 to 1000")
    if (args.release_region or args.release_web_name_check) and not args.official_releases:
        p.error("--release-region/--release-web-name-check require --official-releases")
    if args.official_releases:
        if (args.dataset or args.details or args.trace_graphic is not None or
                args.capture_template is not None or args.skill_gaps or
                args.skill_id is not None or args.operator_web or
                args.web_ordinal is not None or args.catalog != PATH):
            p.error("--official-releases is independent of raw graphic/skill/web lookup modes")
        original25 = json.loads(PET25_OFFICIAL_PATH.read_text(encoding="utf-8"))
        original26 = json.loads(PET26_OFFICIAL_PATH.read_text(encoding="utf-8"))
        jp_page = (json.loads(JP_OFFICIAL_PAGE_PATH.read_text(encoding="utf-8"))
                   if args.release_web_name_check else None)
        cn_page = (json.loads(CN_OFFICIAL_PAGE_PATH.read_text(encoding="utf-8"))
                   if args.release_web_name_check else None)
        result = official_pc_release_view(
            original25, original26, query=args.query, region=args.release_region,
            check_earlier_web_names=args.release_web_name_check,
            jp_page=jp_page, cn_page=cn_page)
        if args.summary:
            result["records"] = []
        else:
            result["records"] = result["records"][:args.limit]
            result["truncated_by_limit"] = result["returned_event_count"] > args.limit
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if args.trace_graphic is not None and (args.dataset or args.query or args.summary or args.details):
        p.error("--trace-graphic must be used without --dataset/--query/--summary/--details")
    if args.trace_graphic is not None and args.trace_graphic <= 0:
        p.error("--trace-graphic requires a positive original numeric graphic number")
    if args.capture_template is not None:
        if args.capture_template <= 0:
            p.error("--capture-template requires a positive original template ID")
        if args.trace_graphic is not None or args.dataset or args.query or args.summary or args.details:
            p.error("--capture-template must be used by itself (and optional --catalog)")
    if args.skill_id is not None and not args.skill_gaps:
        p.error("--skill-id requires --skill-gaps")
    if args.skill_gaps:
        if (args.dataset or args.query or args.summary or args.details or
                args.trace_graphic is not None or args.capture_template is not None):
            p.error("--skill-gaps is separate from name/graphic/capture lookup modes")
        if args.skill_id is not None and args.skill_id <= 0:
            p.error("--skill-id requires a positive original skill number")
        audit = json.loads(PET19_PATH.read_text(encoding="utf-8"))
        result = skill_gap_trace(audit, skill_id=args.skill_id, limit=args.limit)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if args.operator_web is None and args.web_ordinal is not None:
        p.error("--web-ordinal requires --operator-web")
    if args.operator_web is not None:
        if args.web_ordinal is None or args.web_ordinal <= 0:
            p.error("--operator-web requires a positive --web-ordinal")
        if (args.query or args.dataset or args.summary or args.details or
                args.trace_graphic is not None or args.capture_template is not None
                or args.skill_gaps or args.skill_id is not None):
            p.error("--operator-web is an independent exact-source lookup mode")
        catalog = load_catalog(args.catalog)
        report = json.loads(PET21_PATH.read_text(encoding="utf-8"))
        pet22 = json.loads(PET22_PATH.read_text(encoding="utf-8"))
        pet23 = json.loads(PET23_PATH.read_text(encoding="utf-8"))
        result = operator_image_trace(catalog, report, args.operator_web,
                                      args.web_ordinal, pet22=pet22, pet23=pet23)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    catalog = load_catalog(args.catalog)
    if args.summary:
        out = catalog["metrics"]
    elif args.capture_template is not None:
        pet13 = json.loads(PET13_PATH.read_text(encoding="utf-8"))
        out = capture_trace(catalog, pet13, args.capture_template)
    elif args.trace_graphic is not None:
        out = graphic_trace(catalog, args.trace_graphic, limit=args.limit)
    else:
        out = lookup(catalog, args.query, args.dataset, args.limit, args.details)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
