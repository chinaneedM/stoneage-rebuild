#!/usr/bin/env python3
"""Source-qualified PET16 catalogue lookup and PET17 numeric-only graphic tracing.

This is a research index, not a verified official pet species registry.
"""
from pathlib import Path
import argparse
import json

PATH = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json"

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
    p.add_argument("--catalog", type=Path, default=PATH)
    args = p.parse_args()
    if args.limit < 1 or args.limit > 1000:
        p.error("--limit must be 1 to 1000")
    if args.trace_graphic is not None and (args.dataset or args.query or args.summary or args.details):
        p.error("--trace-graphic must be used without --dataset/--query/--summary/--details")
    if args.trace_graphic is not None and args.trace_graphic <= 0:
        p.error("--trace-graphic requires a positive original numeric graphic number")
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    if args.summary:
        out = catalog["metrics"]
    elif args.trace_graphic is not None:
        out = graphic_trace(catalog, args.trace_graphic, limit=args.limit)
    else:
        out = lookup(catalog, args.query, args.dataset, args.limit, args.details)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
