#!/usr/bin/env python3
"""PET-DETAIL36: 305 saved CN5 PC album names -> their compiled +24 alias
-> same preserved CAB's ADRN last-record projection -> physical RD metadata.

The derived collision table overwrites duplicate +76 aliases. This is NOT an
all-candidates enumeration, native renderer selector, official server master,
confirmed active species, or the historical first-release version.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.stoneage_pet_detail32_higher_pc_portrait_probe import verified_gzip, select_rows

ROOT=Path(__file__).resolve().parents[1]
ALBUM="research/recovered/STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json"
METADATA="research/recovered/cn50-resource-metadata/MANIFEST-R1.json"
PET35="research/pets/PET-DETAIL-EVIDENCE35-CN2002-2003-NAME-TO-CN50-ALBUM-BRIDGE-R1.json"
PINS={
 ALBUM:"8b1058a43c267dfeaa298d4c2c472209cebd24d9",
 METADATA:"5063cf2fade4e0739ac35c38a90dfff1a43db960",
 PET35:"deb54b65593014d7b019b93ecf0cefb280bf004e",
}
SEVEN=("葛雷基欧","葛雷洛比","葛雷吉鲁","葛雷马恩","艾迪希洛","蒙奇","菲奇亚")


def git_blob(raw: bytes)->str:
 return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()


def audit(root=ROOT):
 root=Path(root)
 sources={}
 for path,sha in PINS.items():
  raw=(root/path).read_bytes()
  if git_blob(raw)!=sha: raise ValueError("historical derived source blob changed: "+path)
  sources[path]=json.loads(raw)
 album=sources[ALBUM]
 meta=sources[METADATA]
 bridge=sources[PET35]
 assert meta["status"]=="COMPLETE_VERIFIED_5_0_BITMAP_AND_SPR_RESOURCE_METADATA"
 assert meta["source"]["official_clean_pressing_verified"] is False
 assert meta["metrics"]["adrn"]["records"]==303197
 rows=album["records"]
 assert len(rows)==362 and album["metrics"]["compiled_source_named_rows"]==305
 named=[r for r in rows if r["label_as_compiled_GB18030"] is not None]
 assert len(named)==305
 aliases=[int(r["source_raw_trailing_u32"]) for r in named]
 assert len(set(aliases))==len(aliases)
 md={t["name"]:t for t in meta["tables"]}
 directory="research/recovered/cn50-resource-metadata"
 collisions=verified_gzip(root,directory+"/COLLISION-ATTR-R1.tsv.gz",
                          md["COLLISION-ATTR-R1.tsv.gz"])
 projected=select_rows(collisions,"map_number",aliases)
 if any(len(vals)>1 for vals in projected.values()):
  raise ValueError("collision last-record metadata duplicate key")
 physical=sorted({int(x["bitmapno"]) for arr in projected.values() for x in arr})
 adrn=verified_gzip(root,directory+"/ADRN-R1.tsv.gz",md["ADRN-R1.tsv.gz"])
 rd=select_rows(adrn,"bitmapno",physical)
 if any(len(vals)!=1 for vals in rd.values()):
  raise ValueError("physical RD metadata not unique")
 results=[]
 for r in named:
  alias=int(r["source_raw_trailing_u32"])
  selection=projected[alias]
  phys=selection[0] if selection else None
  source_rd=rd[int(phys["bitmapno"])][0] if phys else None
  results.append({
    "record_key":r["record_key"],
    "album_ordinal":r["ordinal"],
    "client_compiled_name":r["label_as_compiled_GB18030"],
    "source_exe_row_sha256":r["source_exe_row_sha256"],
    "album_local_index_not_official_pet_id":r["source_raw_first_i32"],
    "source_compiled_alias_u32":alias,
    "same_CAB_ADRN_last_record_projection_present":bool(phys),
    "last_projected_source_adrn_index":int(phys["adrn_index"]) if phys else None,
    "last_projected_physical_rd_bitmapno":int(phys["bitmapno"]) if phys else None,
    "same_CAB_rd_block_sha256":source_rd["rd_block_sha256"] if source_rd else None,
    "same_CAB_rd_width":int(source_rd["width"]) if source_rd else None,
    "same_CAB_rd_height":int(source_rd["height"]) if source_rd else None,
    "duplicate_original_ADRN_candidates_ruled_out":False,
    "actual_native_renderer_selection_verified":False,
    "same_build_original_server_pet_id_verified":False,
    "historical_official_live_release_verified_by_this_join":False,
  })
 n=sum(int(r["same_CAB_ADRN_last_record_projection_present"]) for r in results)
 seven={r["client_compiled_name"]:r for r in results if r["client_compiled_name"] in SEVEN}
 assert set(seven)==set(SEVEN)
 for x in bridge["records"]:
  r=seven[x["name"]]
  assert r["album_ordinal"]==x["local_album_ordinal"]
  assert r["source_compiled_alias_u32"]==x["local_tail_u32_not_verified_selector"]
 assert next(r for r in results if r["client_compiled_name"]=="宠物蛋")["historical_official_live_release_verified_by_this_join"] is False
 return {
  "schema":"stoneage.pet_detail36.cn50_pc_compiled_name_alias_to_adrn_last_record_rd_reference.r1",
  "date":"2026-11-23",
  "scope":"CLASSIC_PC_ONLY",
  "active_module":"PET",
  "data_origin":"PRESERVED_CN50_5_0_PC_COMPILATION_UNCERTIFIED_OFFICIAL_ORIGINAL_PRESSING",
  "derivation":"EXE_ALBUM_ROW_PLUS24_ALIAS_TO_SAME_CAB_ADRN_PLUS76_COLLISION_LAST_ENTRY_TO_PHYSICAL_RD_METADATA",
  "input_git_pins":PINS,
  "source_cab_sha256":meta["source"]["cab_sha256"],
  "source_exe_sha256":album["source"]["original_exe_sha256"],
  "source_adrn_sha256":meta["source"]["input_containers"]["adrn"]["sha256"],
  "source_real_sha256":meta["source"]["input_containers"]["real"]["sha256"],
  "derived_gz_pins":{
   "ADRN-R1.tsv.gz":md["ADRN-R1.tsv.gz"],
   "COLLISION-ATTR-R1.tsv.gz":md["COLLISION-ATTR-R1.tsv.gz"],
  },
  "counts":{
   "all_album_slots":len(rows),
   "named_album_rows":len(results),
   "distinct_named_aliases":len(aliases),
   "named_aliases_with_last_record_projection":n,
   "named_aliases_without_last_record_projection":len(results)-n,
   "same_build_native_name_to_SPR_selector_newly_verified":0,
   "same_build_official_server_pet_ids_newly_verified":0,
   "live_pet_issuance_newly_verified":0,
  },
  "known_collision_negative_control":{
   "aliases":[28085,28086,28087,28088],
   "original_ADRN_has_two_candidate_rows_each_as_independently_read_in_PET_DETAIL33":True,
   "one_record_projection_is_not_original_full_candidate_list":True,
   "last_in_ADRN_is_not_proven_game_display_choice":True,
  },
  "claims":{
   "saved_CAB_independently_certified_official_distribution":False,
   "same_build_native_selector_verified":False,
   "all_original_ADRN_alias_candidates_enumerated":False,
   "current_browser_or_game_verified":False,
   "original_RD_pixels_recovered_in_this_audit":False,
   "album_name_is_an_actually_issued_live_pet":False,
   "new_species_or_PET_permanent_numbers_created":False,
  },
  "source_safety":{
   "raw_commercial_images_binaries_published":False,
   "original_current_state_git_blob_preserved":"c89e0e33537990aa2132b47c40fef49a985a935c",
   "stage_a":"7_PARTIAL_2_OPEN",
   "stage_b_wiki":"GATED",
   "overall_percent":None,
  },
  "seven_historical_name_source_checks":seven,
  "records":results,
 }


def main():
 report=audit()
 print("PET36_SUMMARY "+json.dumps(report["counts"],ensure_ascii=False,sort_keys=True),flush=True)
 print("PET36_SEVEN "+json.dumps(report["seven_historical_name_source_checks"],ensure_ascii=False,sort_keys=True),flush=True)
 print("PET36_JSON_BEGIN",flush=True)
 print(json.dumps(report,ensure_ascii=False,sort_keys=True,separators=(",",":")),flush=True)
 print("PET36_JSON_END",flush=True)


if __name__=="__main__":
 main()
