"""PET45: join PET44 pet-graphic selectors to previously recovered R28/R29."""
import argparse,csv,gzip,hashlib,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"research/recovered"
P44=BASE/"STONEAGE-PET44-LATER-CLIENT-PETFLAG1-GAP-CANDIDATES-R1.json"
R28=BASE/"tw85-spr137-r28/SOURCE-DERIVED-R28.json"
R28G=BASE/"tw85-spr137-r28/SPR-GROUP-R28.tsv.gz"
R29=BASE/"tw85-frame-bitmap-r29/REPORT-R29.json"
R29G=BASE/"tw85-frame-bitmap-r29/GROUP-MATERIAL-R29.tsv.gz"
CARRIER=BASE/"STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json"
OUTPUT=BASE/"STONEAGE-PET45-TW85-SAME-CARRIER-SPR-RD-INDEX-R1.json"
def must(condition,message):
 if not condition:raise ValueError(message)
def digest(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def jl(p):return json.loads(p.read_text(encoding="utf-8"))
def tbl(p):
 with gzip.open(p,"rt",encoding="utf-8",newline="") as f:return list(csv.DictReader(f,delimiter="\t"))
def calculate():
 a,b,c,d=(jl(x) for x in (P44,R28,R29,CARRIER))
 must(a["schema"]=="stoneage.pet44.later_candidate_petflag1_source_cohort.r1","PET44 source changed")
 must(b["source"]=="TW85-INSTALLER-MSI-CLIENT_UNVERIFIED_COMMUNITY_PRESERVED","R28 source promoted")
 must(c["source_grade"]=="UNVERIFIED_COMMUNITY_PRESERVED_CLAIMED_TW85_SAME_INSTALLER_CARRIER","R29 source promoted")
 must(c["source_pins"]["CARRIER"]["sha256"]==digest(CARRIER),"R29 sample provenance mismatched")
 must(d["inspection"]["inventory"]["samples"][0]["file_count"]==557,"TW85 inventory changed")
 must(digest(R28G)==b["outputs"]["GROUP"]["sha256"],"R28 group source SHA mismatch")
 must(digest(R29G)==c["tables"]["GROUP-MATERIAL-R29.tsv.gz"]["sha256"],"R29 group source SHA mismatch")
 must(digest(R28)==c["source_pins"]["R28_SOURCE"]["sha256"],"R29 R28 input mismatch")
 r28=tbl(R28G);r29=tbl(R29G)
 must(len(r28)==len(r29)==1739,"full original group rows missing")
 must(all(int(x["index"])==i for i,x in enumerate(r28)),"R28 physical group order changed")
 must(all(int(x["group_index"])==i for i,x in enumerate(r29)),"R29 physical group order changed")
 cohort=a["later_source_graphics_without_TW1_index"]
 must(len(cohort)==412,"PET44 target set changed")
 sums=Counter();rows=[];dups={}
 metric=("frame_occurrences","sentinel_frames","mapped_frames","missing_frames","single_frames","multiple_same_rd_frames","multiple_different_rd_frames","distinct_bitmap_ids","missing_bitmap_ids","distinct_mapped_rd_contents","raw_sound_word_occurrences")
 for entry in cohort:
  key=entry["graphic_number"];idxs=entry["indexes"]
  must(not idxs["TW1"] and idxs["TW85"],"not later-only graphic")
  must(len(idxs["TW85"])==len(entry["tw85_exact_spr_segment_sha256_by_occurrence"]),"missing physical SPR SHA")
  if len(idxs["TW85"])>1:dups[str(key)]=len(idxs["TW85"])
  positions=[]
  for index,want in zip(idxs["TW85"],entry["tw85_exact_spr_segment_sha256_by_occurrence"]):
   g=r28[index];m=r29[index]
   must(int(g["spr_no"])==int(m["spr_no"])==key,"source graphic number changed")
   must(g["segment_sha256"]==want,"exact source SPR SHA changed")
   scope="EXACT_CN50_SPR_SEGMENT" if idxs["CN50"] else "R28_UNMATCHED_CN50_SPR_SEGMENT"
   must(m["source_scope"]==scope,"cross-carrier source grade changed")
   vals={x:int(m[x]) for x in metric}
   must(vals["frame_occurrences"]==vals["sentinel_frames"]+vals["mapped_frames"]+vals["missing_frames"],"frame conservation failed")
   must(vals["missing_frames"]==vals["missing_bitmap_ids"]==vals["multiple_same_rd_frames"]==vals["multiple_different_rd_frames"]==0,"same carrier RD incomplete")
   must(vals["mapped_frames"]==vals["single_frames"],"ambiguous bitmap join")
   sums["physical_groups"]+=1
   sums[scope+"_physical_groups"]+=1
   for n in metric:sums[n]+=vals[n]
   positions.append({"source_tw85_physical_group_index":index,"exact_full_original_SPR_segment_sha256":want,"source_scope":scope,**vals})
  rows.append({"graphic_number":key,"PET44_community_template_physical_lines":entry["community_2016_petflag1_template_lines"],"source_tw85_index_positions":idxs["TW85"],"source_CN50_index_positions":idxs["CN50"],"source_MIXED25_numeric_positions_only":idxs["MIXED25"],"positions":positions,"same_build_original_pet_name":None,"confirmed_official_live_pet_release":False,"verified_native_gameplay":False,"new_original_pixel_replay":False})
 must(len(rows)==412 and len({x["graphic_number"] for x in rows})==412,"graphics missing or repeated")
 must(sums["physical_groups"]==416,"source physical count changed")
 must(sums["EXACT_CN50_SPR_SEGMENT_physical_groups"]==214,"CN50 exact subset changed")
 must(sums["R28_UNMATCHED_CN50_SPR_SEGMENT_physical_groups"]==202,"TW85-only physical subset changed")
 must(sums["frame_occurrences"]==sums["mapped_frames"]+sums["sentinel_frames"],"RD source conservation failed")
 must(dups=={"101866":3,"101990":2,"101991":2},"duplicate exact source groups missing")
 inv=d["inspection"]["inventory"]["samples"][0]["files"]
 named=[f["path"] for f in inv if any(k in f["path"].casefold() for k in ("pet","enemy","skill","monster","creature","寵物","宠物","圖鑑","图鉴"))]
 return {"schema":"stoneage.pet45.tw85_same_saved_carrier_original_frame_rd_source_index.r1","date":"2026-11-16","active_module":"PET","frontier_year":2000,"frontier_status":"OPEN","source_grade":"UNVERIFIED_COMMUNITY_PRESERVED_CLAIMED_TW85_SAME_INSTALLER_CARRIER","selector_grade":"2016_COMMUNITY_PETFLG1_GRAPHIC_NUMBERS_NOT_OFFICIAL_PET_IDENTITIES",
 "source_pins":{p.name:{"path":str(p.relative_to(ROOT)),"bytes":p.stat().st_size,"sha256":digest(p)} for p in (P44,R28,R28G,R29,R29G,CARRIER)},
 "summary":{"source_graphic_candidates_NOT_species":412,"original_physical_SPR_groups":416,"full_SPR_segment_exact_CN50_physical_groups":214,"unmatched_CN50_original_TW85_physical_groups":202,**dict(sorted(sums.items())),"duplicate_numeric_original_groups":dups,"new_same_build_named_pets":0,"new_official_live_released_pets":0,"new_original_RD_pixels_decoded":0,"historical_official_species_total":None},
 "same_carrier_file_inventory_name_scan":{"files_in_installer":557,"explicit_pet_enemy_skill_like_filenames":named,"does_not_rule_out_embedded_executable_names":True,"executable_content_read_now":False},
 "candidate_groups":rows,"TW1_six_without_qualified_album_names":[x["graphic_number"] for x in a["tw1_sprite_groups_without_same_build_album_name"]],
 "four_carriers_index_absent_community_candidates":[x["graphic_number"] for x in a["community_petflag1_graphics_missing_all_four_indexes"]],
 "guardrails":{"original_RD_index_means_rendered_pixels":False,"graphics_count_means_pet_species_count":False,"community_server_petflag_means_official_release":False,"later_installer_proven_original_official_clean_build":False,"old_2000_year_source_audit_closed":False},
 "next":"PET46_PRIORITIZE_SAME_CARRIER_ORIGINAL_NAMED_PET_ID_TABLE_OR_PRIVATE_RD_PIXEL_REPLAY","current_state_git_blob_preserved":"c89e0e33537990aa2132b47c40fef49a985a935c","stage_a":"7_PARTIAL_2_OPEN","stage_b_wiki":"GATED","r79":"PAUSED_NON_BLOCKING","overall_percent":None}
def main():
 p=argparse.ArgumentParser();p.add_argument("--mode",choices=("generate","verify"),default="verify");arg=p.parse_args()
 report=json.dumps(calculate(),ensure_ascii=False,sort_keys=True,indent=2)+"\n"
 if arg.mode=="generate":OUTPUT.write_text(report,encoding="utf-8")
 else:must(OUTPUT.read_text(encoding="utf-8")==report,"published report not exact replay")
 obj=json.loads(report);print(json.dumps({"mode":arg.mode,**obj["summary"]},ensure_ascii=False,sort_keys=True))
if __name__=="__main__":main()
