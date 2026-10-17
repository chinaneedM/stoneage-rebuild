"""Check 2001 player stonepic ID ranges against EXACT v1.0 ADRN indexes.

Presence/absence of a number is original-client evidence; a player-supplied
category label is still only a 2001 player claim and NOT proven v1 semantics.
"""
from __future__ import annotations
from pathlib import Path
import csv,gzip,hashlib,json
from tools.stoneage_pet_asset_growth_catalog import META,gitblob,require,sha256file
ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/"research/recovered/STONEAGE-EARLY-VISUAL-ID-RANGES-INPUT-R1.json"
ADRN_SHA256="c8669789de1cc6e3575c2412ed86354a49c2b3e90cd2854c1e7b2fc71b0fe9ea"
CREATE_RECORD_BLOB="e39a3a6020b578da017ab0bfa9369dc083e0b700"
def audit():
 p=json.loads(INPUT.read_text(encoding="utf-8"))
 require(p["schema"]=="stoneage.early_ui_visual_resource_claims.r1","schema changed")
 require(p["source_grade"]=="2001_DATED_PLAYER_CLAIM_NOT_DIRECT_JSS_OR_TW10_UI_PROOF","category false promotion")
 require(p["original_tw10_source"]["adrn_compressed_sha256"]==ADRN_SHA256,"source hash")
 require(p["tw10_create_character_shape"]["git_blob"]==CREATE_RECORD_BLOB,"compiled schema source metadata")
 require(gitblob((ROOT/p["tw10_create_character_shape"]["schema_path"]).read_bytes())==CREATE_RECORD_BLOB,"compiled schema changed")
 sc=json.loads((ROOT/p["tw10_create_character_shape"]["schema_path"]).read_text(encoding="utf-8"))
 c=sc["records"]["character_creation"]
 require(p["tw10_create_character_shape"]["field_count"]==len(c["fields"])==13,"creation record")
 fields={x["name"] for x in c["fields"]}
 require("body_image_id" in fields and "face_image_id" in fields,"body and face identity absent")
 require(p["tw10_create_character_shape"]["render_actual_positions_verified"] is False,"historic layout overclaim")
 require(sha256file(META/"ADRN-R1.tsv.gz")==ADRN_SHA256,"original bitmap dataset changed")
 bitmap=set()
 with gzip.open(META/"ADRN-R1.tsv.gz","rt",encoding="utf-8",newline="") as f:
  for row in csv.DictReader(f,delimiter="\t"):
   i=int(row["bitmapno"])
   require(i not in bitmap,"repeated original image ID")
   bitmap.add(i)
 require(len(bitmap)==125996 and min(bitmap)==0 and max(bitmap)==125995,"TW10 numeric ID envelope")
 require(bitmap==set(range(125996)),"TW10 original image numbers not contiguous")
 seen=set();covered=set();ranges=[]
 for r in p["claimed_ranges"]:
  lo=r["from"];hi=r["to"];require(lo>=0 and hi>=lo,"invalid 2001 interval")
  ids=set(range(lo,hi+1))
  require(not (covered&ids),"overlapping 2001 main category ranges")
  covered|=ids
  inside=len(ids&bitmap)
  ranges.append({**r,"claimed_count":len(ids),"present_in_tw10_adrn":inside,"absent_from_tw10_adrn":len(ids)-inside,
                 "id_membership_status":"ALL_ID_MEMBERS_PRESENT_ONLY" if inside==len(ids) else "ID_OUTSIDE_TW10_OR_PARTIAL",
                 "category_tw10_verified":False})
 expected=p["expected_output"]["unsourced_gap_ranges"]
 gaps=bitmap-covered
 require(len(gaps)==5 and gaps==set([0,95879,95880,95881,95882]),"new source gaps")
 require(expected==[[0,0],[95879,95882]],"missing explicit historic mapping gaps")
 for a in p["explicit_extra_claims"]:
  require(a["exact_tw10_presence"] is None and a["actual_tw10_login_visual_verified"] is False if "actual_tw10_login_visual_verified" in a else a["exact_tw10_presence"] is None,"pre-runtime claim wrongly asserted")
 require(126766 not in bitmap and 126766>=125996,"later mainland login should NOT be v1")
 require(all(v["same_version_compiled_binding"] is False for v in p["guide_claims"]),"guide upgraded to original runtime fact")
 require(all(v["actual_tw10_semantic_certified"] is False for v in p["claimed_ranges"]),"2001 player categories promoted to exact TW1 fact")
 for k in ("game_original_login_screen_restored","all_original_avatars_identified","complete_pet_portraits_identified","full_original_ui_layout_verified","stage_b_production_started"):
  require(p[k] is False,"false closure "+k)
 return {"schema":"stoneage.early_ui_visual_range_checked.r1","source_grade":p["source_grade"],"fixed_2001_article":"SA17173-20010614-STONEPIC",
         "tw10_ad rn_bitmap_records".replace(" ",""):len(bitmap),"tw10_bitmap_range":[0,125995],
         "source_version":"TW10_DIRECT_ADRN_IDS_VS_2001_PLAYER_CATEGORY_CLAIMS",
         "ranges":ranges,"unclassified_tw10_ids":sorted(gaps),"external_mainland_login_image_126766_in_tw10":False,
         "tw10_actual_login_render_verified":False,
         "create_new_character_compiled_fields":13,"body_face_image_fields_verified":True,
         "historic_character_appearances_count_from_undated_guide_only":12,
         "historic_pet_species_count":None,"original_pet_portrait_semantic_binding_verified":False,
         "orig_v1_client_ui_rendering_complete":False}
if __name__=="__main__":
 print("EARLY_VISUAL_RANGES_JSON="+json.dumps(audit(),ensure_ascii=False,sort_keys=True,separators=(",",":")))
