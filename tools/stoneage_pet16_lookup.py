#!/usr/bin/env python3
"""Source-qualified searchable PET16 index; not a list of official game species."""
from pathlib import Path
import argparse
import json
PATH = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json"

def lookup(catalog, query="", dataset=None, limit=20):
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
            result.append({"dataset": group, "id": row["id"], "source": row["source"],
                          "name": row.get("name_as_written"), "template_id": row.get("template_id"),
                          "graphic_number": row.get("graphic_number")})
            if len(result) >= limit:
                return result
    return result

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--query", default="")
    p.add_argument("--dataset", choices=("later2016_templates","later2016_graphics",
        "mixed25_main","mixed25_alternative","tw10_visual","jp_official_web","cn_official_web"))
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--summary", action="store_true")
    p.add_argument("--catalog", type=Path, default=PATH)
    args=p.parse_args()
    if args.limit < 1 or args.limit > 1000:
        p.error("--limit must be 1 to 1000")
    c=json.loads(args.catalog.read_text(encoding="utf-8"))
    print(json.dumps(c["metrics"] if args.summary else lookup(c,args.query,args.dataset,args.limit),ensure_ascii=False,indent=2))
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
