"""Bounded original-derived client resource alias probe for late-preserved tutor NPC configs.

Reads the pre-existing Git source-qualified logical alias catalog (not private art).
Separates logical_alias from physical_bitmapno and never labels a source asset
as an official NPC, same-deployment resource, animation or game-rendered image.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from tools.stoneage_logical_alias_catalog import query
ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/"research/recovered/logical-alias-catalog-r1"
ALIASES=(16122,16127)
FIELDS=("profile","logical_alias","source_index","physical_bitmapno","adrn_offset","adrn_size","xoff","yoff","width","height","attr_sha256","record_sha256","content_id","alias_evidence","source_rd_status","catalog_rd_qualification")
CONTENT=("content_id","rd_sha256","bytes","rd_width","rd_height","reference_count","profiles")

def sha(x):return hashlib.sha256(x).hexdigest()
def compact(entries):
    return [
        {"reference":{k:row["reference"].get(k) for k in FIELDS},
         "content":{k:row["content"].get(k) for k in CONTENT},
         "role":row["role_annotation"]["role"]}
        for row in entries
    ]
def build():
    src=(CAT/"REFERENCES-R1.tsv.gz").read_bytes()
    report=(CAT/"REPORT-R1.json").read_bytes()
    proof=json.loads(report)
    pinned=proof["datasets"]["REFERENCES-R1.tsv.gz"]
    assert pinned["rows"]>43000 and len(src)>2000000
    assert pinned["columns"][0:4]==["profile","logical_alias","source_index","physical_bitmapno"]
    output={"schema":"stoneage.original_NPC16122_16127_derived_alias_probe.r1",
            "original_alias_catalog_source":proof["schema"],
            "catalog_report_git_sha256":sha(report),
            "compressed_REFERENCES_SHA256":sha(src),
            "original_derived_reference_count":pinned["rows"],
            "sources":{}}
    for target in ALIASES:
        exact=query(CAT,alias=target,limit=0)
        same_numeric_physical=query(CAT,physical=target,limit=0)
        assert exact["identifier_namespaces_are_distinct"] and same_numeric_physical["identifier_namespaces_are_distinct"]
        output["sources"][str(target)]={
            "logical_alias_occurrences":exact["total_matches"],
            "logical_alias_entries":compact(exact["matches"]),
            "same_integer_physical_occurrences":same_numeric_physical["total_matches"],
            "same_integer_physical_entries":compact(same_numeric_physical["matches"]),
            "logical_alias_is_not_physical_bitmapno":True}
    output["not_proven"]={"later_NPC_config_official_same_build_as_TW10":True,
      "NPC_graphic_is_rendered_by_original_client":True,
      "physical_bitmap_identifier_is_logical_alias":True,
      "original_sprite_or_NPC_identity_from_client_bitmap_alone":True,
      "missing_alias_in_some_catalog_proves_early_asset_never_existed":True}
    return output
def main():
    p=argparse.ArgumentParser();p.add_argument("--print",action="store_true");args=p.parse_args()
    result=build()
    if args.print:
        print("STONEAGE_NPC_16122_16127_SOURCE_BOUND_BEGIN")
        print(json.dumps(result,ensure_ascii=False,separators=(",",":"),sort_keys=True))
        print("STONEAGE_NPC_16122_16127_SOURCE_BOUND_END")
if __name__=="__main__": main()
