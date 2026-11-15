#!/usr/bin/env python3
"""Source-qualified PET16 catalogue lookup and PET17 numeric-only graphic tracing.

This is a research index, not a verified official pet species registry.
"""
from pathlib import Path
import argparse
import json

PATH = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json"
PET13_PATH = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-PET-MODULE-13-ORIGINAL-CAPTURE-TEMPLATE-ATTRIBUTES-SKILLS-R1.json"

# Only datasets carrying an original numeric graphic field participate.
# Official JP/CN page ordinals/image filenames are NOT client graphic numbers.
GRAPHIC_DATASETS = (
    "later2016_templates", "later2016_graphics",
    "mixed25_main", "mixed25_alternative", "tw10_visual",
)


def lookup(catalog, query="", dataset=None, limit=20, details=False):
    """Return original source-separated records; never merge sources into species."""
    q = str(query).strip().casefold()
    result = []
    for group, records in catalog["datasets"].items():
        if dataset and group != dataset:
            continue
        for row in records:
            fields = (row.get("id"), row.get("name_as_written"), row.get("label_as_written"),
                      row.get("template_id"), row.get("graphic_number"), row.get("web_ordinal"))
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
    return {
        "graphic_number": graphic_number,
        "relation": "LITERAL_GRAPHIC_NUMBER_COINCIDENCE_ONLY",
        "official_pet_species_identity_verified": False,
        "same_historical_build_or_server_deployment_verified": False,
        "tw10_original_species_name": None,
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


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--query", default="")
    p.add_argument("--dataset", choices=(
        "later2016_templates", "later2016_graphics",
        "mixed25_main", "mixed25_alternative", "tw10_visual",
        "jp_official_web", "cn_official_web"))
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--summary", action="store_true")
    p.add_argument("--details", action="store_true",
                   help="Include the full original-derived row within its named source")
    p.add_argument("--trace-graphic", type=int, metavar="NUMBER",
                   help="Trace equal numeric graphic references without identity merging")
    p.add_argument("--capture-template", type=int, metavar="TEMPLATE_ID",
                   help="PET13 original same-archive capture item/skill source links (not runtime)")
    p.add_argument("--catalog", type=Path, default=PATH)
    args = p.parse_args()
    if args.limit < 1 or args.limit > 1000:
        p.error("--limit must be 1 to 1000")
    if args.trace_graphic is not None and (args.dataset or args.query or args.summary or args.details):
        p.error("--trace-graphic must be used without --dataset/--query/--summary/--details")
    if args.trace_graphic is not None and args.trace_graphic <= 0:
        p.error("--trace-graphic requires a positive original numeric graphic number")
    if args.capture_template is not None:
        if args.capture_template <= 0:
            p.error("--capture-template requires a positive original template ID")
        if args.trace_graphic is not None or args.dataset or args.query or args.summary or args.details:
            p.error("--capture-template must be used by itself (and optional --catalog)")
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
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
