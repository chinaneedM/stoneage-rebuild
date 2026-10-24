#!/usr/bin/env python3
"""Direct 101-record TW1 -> CN5 physical bitmap bridge from real RD indexes.

Reads the complete separately source-qualified compressed ADRN metadata catalogs;
does NOT infer historical NPC identities, world floors, scripts or pet species.
"""
from __future__ import annotations
import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TW_DIRECTORY="research/recovered/tw10-resource-metadata"
CN_DIRECTORY="research/recovered/cn50-resource-metadata"
CANDIDATE="research/recovered/STONEAGE-TW10-CN50-STATIC-VISUAL-LINEAGE-P2B-R1.json"
CN_MANIFEST_SHA256="e24afc513d28c7f25bd26bde9c69ddc0de4000147a2b11f50b5176655d8558fd"
TW_MANIFEST_SHA256="c8669789de1cc6e3575c2412ed86354a49c2b3e90cd2854c1e7b2fc71b0fe9ea"
FIELDS=("bitmapno","index","size","xoff","yoff","width","height","rd_flag",
        "rd_width","rd_height","rd_size_field","attr_sha256","rd_block_sha256")


def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as src:
        while block:=src.read(1024*1024):
            h.update(block)
    return h.hexdigest()


def verify_source(path, checksum, bytes_count):
    if not path.is_file() or path.stat().st_size != bytes_count:
        raise ValueError("missing-or-wrong-metadata-source-size")
    if digest(path) != checksum:
        raise ValueError("derived-metadata-source-sha256-mismatch")


def selected_adrn(path, target_ids, expected_records):
    selection={}
    count=0
    previous=-1
    with gzip.open(path,"rt",encoding="utf-8",newline="") as stream:
        reader=csv.DictReader(stream,delimiter="\t")
        if set(FIELDS)-set(reader.fieldnames or ()):
            raise ValueError("missing-source-adrn-columns")
        for item in reader:
            count+=1
            ident=int(item["bitmapno"])
            if ident in target_ids:
                if ident in selection:
                    raise ValueError("duplicate-resource-id-in-verified-band")
                if int(item["size"])<16 or not item["rd_block_sha256"]:
                    raise ValueError("invalid-source-record")
                selection[ident]={k:item[k] for k in FIELDS}
            if count > expected_records:
                raise ValueError("unexpected-extra-original-records")
    if count != expected_records or set(selection) != target_ids:
        raise ValueError("not-full-original-metadata-or-missing-candidate")
    return selection


def compare_physical_records(candidate, tw_catalog, cn_catalog):
    ids=set(range(5846,5947))
    rows=candidate["records"]
    if len(rows)!=101 or set(r["tw10_bitmap_id"] for r in rows)!=ids:
        raise ValueError("candidate-bridge-not-complete")
    out=[]
    for legacy in rows:
        key=legacy["tw10_bitmap_id"]
        tw=tw_catalog[key]
        cn=cn_catalog[key]
        for field in ("size","xoff","yoff","width","height","rd_flag",
                      "rd_width","rd_height","rd_size_field",
                      "attr_sha256","rd_block_sha256"):
            if tw[field] != cn[field]:
                raise ValueError("original-client-resource-byte-metadata-changed:"+str(key)+":"+field)
        if tw["rd_block_sha256"] != legacy["tw10_rd_sha256"]:
            raise ValueError("static-R99-source-and-native-tw10-differ:"+str(key))
        if int(tw["size"]) != legacy["tw10_rd_bytes"]:
            raise ValueError("static-original-RD-size-disagrees")
        if ([int(tw["width"]),int(tw["height"])] != legacy["tw10_dimensions"] or
            [int(tw["xoff"]),int(tw["yoff"])] != legacy["tw10_draw_offset"]):
            raise ValueError("static-original-physical-geometry-disagrees")
        for key_name in ("verified_npc_name","verified_original_npc_id",
                         "verified_original_map_floor","verified_original_npc_script",
                         "verified_pet_species_id"):
            if legacy[key_name] is not None:
                raise ValueError("source-had-fabricated-npc-identity")
        out.append({
            "bitmap_id":key,
            "tw10_adrn_index":int(tw["index"]),
            "cn50_adrn_index":int(cn["index"]),
            "original_player_category":"NPC_CANDIDATE_UNVERIFIED",
            "original_map_resource_number":legacy["tw10_map_resource_number"],
            "rd_sha256":cn["rd_block_sha256"],
            "rd_flag":int(cn["rd_flag"]),
            "rd_bytes":int(cn["size"]),
            "attribute_sha256":cn["attr_sha256"],
            "dimensions":[int(cn["width"]),int(cn["height"])],
            "draw_offset":[int(cn["xoff"]),int(cn["yoff"])],
            "same_80_byte_descriptor_and_actual_RD_block":True,
            "original_npc_name":None,
            "original_npc_id":None,
            "original_npc_server_spawn":None,
            "original_pet_species_id":None,
        })
    if [x["bitmap_id"] for x in out]!=list(range(5846,5947)):
        raise ValueError("unsorted-legacy-resource-range")
    return out


def build(root=ROOT):
    source=(root/CANDIDATE)
    candidate=json.loads(source.read_text(encoding="utf-8"))
    if candidate["status"]!="101_STATIC_BITMAP_CANDIDATE_PHYSICAL_LINEAGE_PROVED":
        raise ValueError("no-prior-source-qualified-lineage")
    if candidate["metrics"]["cn50_verified_named_npc_entities"]!=0:
        raise ValueError("invented-npc-identity")
    tw=root/TW_DIRECTORY/"ADRN-R1.tsv.gz"
    cn=root/CN_DIRECTORY/"ADRN-R1.tsv.gz"
    verify_source(tw,TW_MANIFEST_SHA256,8238749)
    verify_source(cn,CN_MANIFEST_SHA256,19745873)
    manifest=json.loads((root/CN_DIRECTORY/"MANIFEST-R1.json").read_text(encoding="utf-8"))
    if (manifest["status"]!="COMPLETE_VERIFIED_5_0_BITMAP_AND_SPR_RESOURCE_METADATA" or
        manifest["metrics"]["adrn"]["records"]!=303197 or
        manifest["source"]["official_clean_pressing_verified"] is not False or
        manifest["source"]["source_413_files_rehashed"] is not True):
        raise ValueError("unqualified-cn5-original-resource-catalog")
    table={row["name"]:row for row in manifest["tables"]}
    if table["ADRN-R1.tsv.gz"]["sha256"]!=CN_MANIFEST_SHA256:
        raise ValueError("cn5-manifest-digest-mismatch")
    target=set(range(5846,5947))
    tw_rows=selected_adrn(tw,target,125996)
    cn_rows=selected_adrn(cn,target,303197)
    aligned=compare_physical_records(candidate,tw_rows,cn_rows)
    return {
        "schema":"stoneage.tw10_cn50.direct_static_visual_source_records_p2b_r1",
        "status":"101_OF_101_ACTUAL_ORIGINAL_BITMAP_RECORDS_IDENTICAL_BOTH_VERSIONS",
        "source":{
            "tw10_adrn_sha256":TW_MANIFEST_SHA256,
            "cn50_adrn_sha256":CN_MANIFEST_SHA256,
            "tw10_metadata_rows":125996,
            "cn50_metadata_rows":303197,
            "tw10_cn50_candidate_parent_blob_sha256":digest(source),
            "cn50_catalog_manifest_sha256":digest(root/CN_DIRECTORY/"MANIFEST-R1.json"),
            "origins":"SEPARATELY_EXPORTED_FROM_ACTUAL_CLIENT_RESOURCE_CONTAINERS",
        },
        "counts":{
            "original_player_labeled_candidate_rows":101,
            "direct_original_id_matches":101,
            "rd_sha_equal":101,
            "map_collision_attr_raw_hash_equal":101,
            "different_or_missing":0,
            "verified_named_npcs":0,
            "verified_pet_species":0,
        },
        "records":aligned,
        "limitations":{
            "original_2001_player_NPC_label_proves_original_game_role":False,
            "original_map_resource_number_is_world_map_id":False,
            "same_physical_bitmap_proves_same_server_npc":False,
            "original_server_npc_name_spawn_quest_data_present":False,
            "new_game_art_asset_license_proven":False,
            "8_5_entity_compatibility_verified_by_this_report":False,
            "proprietary_original_game_bytes_committed":False
        },
        "reopen_when":"A period-authenticated same-build actor/resource selector or original NPC master provides a named ID with a verifiable bitmap mapping",
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    result=build()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"REAL_P2B_DIRECT_JOIN|tw1_ids={result['counts']['direct_original_id_matches']}|"
          f"same_rd={result['counts']['rd_sha_equal']}|same_map_attr={result['counts']['map_collision_attr_raw_hash_equal']}|named_npcs=0")


if __name__=="__main__":
    main()
