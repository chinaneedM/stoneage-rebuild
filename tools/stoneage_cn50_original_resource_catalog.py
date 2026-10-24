#!/usr/bin/env python3
"""Full per-ID physical metadata archive from actual preserved Mainland 5.0 CAB.

Exports deterministic compressed ADRN/RD, collision and SPR animation/frame
tables, never an original bitmap/sprite/sound byte. Must verify all 413 originals.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from tools.stoneage_stoneage5_msi_probe import load_root, find_entry
from tools.stoneage_stoneage5_cab_probe import iso_file_slice
from tools.stoneage_stoneage5_full_cab_acquisition import (
    EXPECTED_SIZE, checked_layout, download_cab, extracted_inventory, hash_file)
from tools.stoneage_tw10_resource_metadata import export_adrn, export_spr, sha256_file

REPORT="research/recovered/STONEAGE-STONEAGE5-REAL-CAB-PAYLOAD-R1.json"
COMPARE="research/recovered/STONEAGE-TW10-CN50-REAL-RECORD-DIFF-R1.json"
NAMES={"adrn":"adrn_31.bin","real":"real_31.bin",
       "spradrn":"spradrn_17.bin","spr":"spr_17.bin"}
DATASETS=("ADRN-R1.tsv.gz","COLLISION-ATTR-R1.tsv.gz","SPR-GROUP-R1.tsv.gz",
          "SPR-ANIMATION-R1.tsv.gz","SPR-FRAME-R1.tsv.gz")


def qualify_sources(repo):
    manifest=json.loads((repo/REPORT).read_text(encoding="utf8"))
    difference=json.loads((repo/COMPARE).read_text(encoding="utf8"))
    if (manifest.get("status")!="REAL_FULL_CAB_EXTRACTED_AND_413_FILES_HASHED"
        or manifest["files"]["count"]!=413
        or difference.get("result")!="DERIVED_RECORD_LEVEL_DIFF_OF_REACQUIRED_ORIGINAL_RESOURCE_BYTES"):
        raise ValueError("unqualified-provenance")
    lookup={x["name"]:(int(x["size"]),x["sha256"])
            for x in manifest["files"]["inventory"]}
    if len(lookup)!=413:
        raise ValueError("ambiguous-installation-file-keys")
    for key,name in NAMES.items():
        if tuple(difference["source_claims"]["CN50"]["files"][key][x]
                 for x in ("bytes","sha256")) != lookup[name]:
            raise ValueError("resource-hash-source-conflict")
    return manifest,difference,lookup


def verify_four(files,lookup):
    result={}
    for family,name in NAMES.items():
        path=files/name
        if not path.is_file():
            raise ValueError("missing-original-container")
        digest,size=hash_file(path)
        if (size,digest)!=lookup[name]:
            raise ValueError("unqualified-original-container:"+name)
        result[family]={"name":name,"bytes":size,"sha256":digest}
    return result


def dataset_manifest(out_dir,source_files,metrics):
    files=[]
    for name in DATASETS:
        path=out_dir/name
        if not path.is_file() or not path.stat().st_size:
            raise ValueError("missing-derived-table:"+name)
        files.append({"name":name,"bytes":path.stat().st_size,"sha256":sha256_file(path)})
    return {
        "schema":"stoneage.cn50.original_resource_catalog_r1",
        "status":"COMPLETE_VERIFIED_5_0_BITMAP_AND_SPR_RESOURCE_METADATA",
        "source":{"archive_item":"Stoneage-5","official_clean_pressing_verified":False,
                  "source_413_files_rehashed":True,"cab_sha256":metrics["cab_sha256"],
                  "input_containers":source_files},
        "tables":files,
        "metrics":{"adrn":metrics["adrn"],"spr":metrics["spr"]},
        "claims":{"bitmap_record_count_not_pet_species_count":True,
                  "sprite_group_count_not_character_species_count":True,
                  "client_visual_selector_or_name_join_proven":False,
                  "original_server_pet_npc_quest_master_recovered":False,
                  "original_proprietary_payload_retained":False},
    }


def build(output_dir):
    root=Path(__file__).resolve().parents[1]
    source,prior,lookup=qualify_sources(root)
    meta,cue_name,cue,track,carrier,url,volume,entries=load_root()
    cab=find_entry(entries,"DATA1.CAB")
    if not cab or int(cab["size"])!=EXPECTED_SIZE:
        raise ValueError("preserved-cab-not-qualified")
    prefix,status,_=iso_file_slice(url,cab,track,0,65536)
    if status!=206:
        raise ValueError("source-range-not-honored")
    head,expected=checked_layout(prefix)
    with tempfile.TemporaryDirectory(prefix="stoneage-cn50-resource-catalog-") as tmp:
        temp=Path(tmp)
        file=temp/"DATA1.CAB"
        sha=download_cab(url,cab,track,int(carrier["size"]),file)
        if sha!=source["source"]["cab_sha256"]:
            raise ValueError("source-cab-SHA-mismatch")
        with file.open("rb") as f:
            if f.read(len(prefix))!=prefix:
                raise ValueError("source-cab-prefix-mismatch")
        expanded=temp/"contents"
        expanded.mkdir()
        run=subprocess.run(["cabextract","-q","-d",str(expanded),str(file)],
                           capture_output=True,text=True,timeout=1500)
        if run.returncode:
            raise ValueError("static-cabextract-failure")
        rows=extracted_inventory(expanded,expected)
        if len(rows)!=413 or any(lookup.get(x["name"])!=(x["size"],x["sha256"]) for x in rows):
            raise ValueError("source-413-files-differ-from-verified-full-cab")
        four=verify_four(expanded,lookup)
        output_dir.mkdir(parents=True,exist_ok=True)
        adrn=export_adrn(expanded/NAMES["adrn"],expanded/NAMES["real"],
                         output_dir/DATASETS[0],output_dir/DATASETS[1])
        spr=export_spr(expanded/NAMES["spradrn"],expanded/NAMES["spr"],
                       output_dir/DATASETS[2],output_dir/DATASETS[3],output_dir/DATASETS[4])
        if adrn["records"]!=303197 or spr["groups"]!=1185:
            raise ValueError("source-r1-record-inheritance-mismatch")
        if (prior["families"]["bitmap_rd"]["comparison"]["exact_payload_or_segment_count"],
            prior["families"]["animation_spr"]["comparison"]["exact_payload_or_segment_count"])!=(125996,464):
            raise ValueError("prior-source-inheritance-check-disagrees")
        complete=dataset_manifest(output_dir,four,{"cab_sha256":sha,"adrn":adrn,"spr":spr})
        (output_dir/"MANIFEST-R1.json").write_text(
            json.dumps(complete,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
            encoding="utf8")
        print("CATALOG|source_original_cab_sha256="+sha+"|ADRN="+str(adrn["records"])+
              "|SPR="+str(spr["groups"])+"|SPR_frames="+str(spr["frames"])+
              "|collision_resource_keys="+str(adrn["collision_map_numbers"]),flush=True)
        for obj in complete["tables"]:
            print("DATASET|name="+obj["name"]+"|bytes="+str(obj["bytes"])+
                  "|sha256="+obj["sha256"],flush=True)
        return complete


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output-dir",type=Path,required=True)
    args=p.parse_args()
    build(args.output_dir)


if __name__=="__main__":
    main()
