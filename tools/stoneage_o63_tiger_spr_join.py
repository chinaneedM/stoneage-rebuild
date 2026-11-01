"""O63: four saved tiger-pet sprite keys, native original TW1 SPR metadata only.

Re-encode the complete selected TW1 SPR animation spans from already accepted
lossless metadata. Never confuse SPR keys with physical REAL bitmap numbers.
No proprietary bytes, palette, imagery, original runtime or server deployment.
"""
from __future__ import annotations
import csv, gzip, hashlib, json, struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
META=ROOT/"research/recovered/tw10-resource-metadata"
O61=ROOT/"research/recovered/STONEAGE-O61-FOUR-TIGER-TRAINERS-SOURCE-R1.json"
R40=ROOT/"research/recovered/STONEAGE-PRESERVED-PET-SPR-SOURCE-R40.json"
PINS={
 "SPR-GROUP-R1.tsv.gz":"4db7809de4197eb90cca6dc04bda8550025e022c8232e2ebb902db0e9faf0175",
 "SPR-ANIMATION-R1.tsv.gz":"25f8039e6c6ca47d94289b269d5ff74a67fde999c6b6d4dbb08af297ddcaa567",
 "SPR-FRAME-R1.tsv.gz":"2bbfb2db4a866445085d98934fd475cbd72e034fe1155b2e17ae802ffdc5fe80",
}
KEYS=(100327,100328,100329,100330)
def need(ok,what):
 if not ok: raise ValueError("O63 source gate: "+what)
def ghblob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def read_json(p,pin):
 b=p.read_bytes();need(ghblob(b)==pin,"immutable source "+p.name);return json.loads(b)
def rows(name):
 raw=(META/name).read_bytes()
 need(hashlib.sha256(raw).hexdigest()==PINS[name],"immutable original TSV "+name)
 with gzip.open(META/name,"rt",newline="") as f:
  return [x for x in csv.DictReader(f,delimiter="\t") if int(x["spr_no"]) in KEYS]
def derive():
 a=read_json(O61,"e1b131962b9a830cabb672ea1d76d1bad817c960")
 b=read_json(R40,"5b49d54d7cff2d79d3610db7ca4a37108f1f9e03")
 need(a["source_era"].startswith("LATER_COMMUNITY_MIXED25"),"version boundary")
 need(a["reward_id_qualification"]["all_four_enemy_ids_unique_and_templates_resolve"],"four qualified template links")
 links=a["reward_id_qualification"]["same_preservation_explicit_instance_template_links"]
 need(sorted(z["graphic_id"] for z in links)==list(KEYS),"source named graphic IDs")
 need(b["source_scope"].startswith("MIXED25_PRESERVED_SAME_ARCHIVE"),"R40 source boundary")
 need(b["material"]["index_rows_count"]==847,"index size")
 br=b["material"]["all_index_rows"]; need(len(br)==847,"full index available")
 gg=rows("SPR-GROUP-R1.tsv.gz")
 aa=rows("SPR-ANIMATION-R1.tsv.gz")
 ff=rows("SPR-FRAME-R1.tsv.gz")
 outputs=[]
 for key in KEYS:
  picks=[(i,row) for i,row in enumerate(br) if row[1]==key]
  need(len(picks)==1,"unique same-archive spr index")
  ix,orig=picks[0]
  next_offsets=[z[2] for z in br if z[2]>orig[2]]
  need(next_offsets,"strict next physical offset")
  boundary=min(next_offsets)
  need(orig[3]==56 and orig[4]==16 and boundary>orig[2],"original group bound")
  g=[x for x in gg if int(x["spr_no"])==key]
  need(len(g)==1,"unique TW10 group")
  g=g[0];anim=sorted((x for x in aa if int(x["spr_no"])==key),key=lambda x:int(x["offset"]))
  need(len(anim)==56,"56 recovered original animations")
  frames=[x for x in ff if int(x["spr_no"])==key]
  seq=[];distinct=set();n=0;first=[]
  for row in anim:
   idx=int(row["anim_index"]);cnt=int(row["frame_count"])
   fs=sorted((x for x in frames if int(x["anim_index"])==idx),key=lambda x:int(x["frame_index"]))
   need(len(fs)==cnt and [int(x["frame_index"]) for x in fs]==list(range(cnt)),"complete source frames")
   binary=struct.pack("<HHII",int(row["direction"]),int(row["anim_no"]),int(row["duration"]),cnt)
   for f in fs:
    bitmap=int(f["bmp_no"])
    binary+=struct.pack("<IhhH",bitmap,int(f["pos_x"]),int(f["pos_y"]),int(f["sound_no"]))
    if bitmap:distinct.add(bitmap)
   need(len(binary)==int(row["end_offset"])-int(row["offset"]),"original animation range")
   seq.append(binary);n+=cnt
   if int(row["direction"])==0:
    first.append({"action_code":int(row["anim_no"]),"first_bitmap_no":int(fs[0]["bmp_no"]),"frames":cnt,"duration_word":int(row["duration"])})
  whole=b"".join(seq)
  sha=hashlib.sha256(whole).hexdigest()
  need(sha==g["segment_sha256"],"complete TW10 original SPR source segment SHA")
  need(int(g["index"])>=0 and int(g["index"])<464,"TW10 original index bound")
  need(len(whole)>0 and n>=56,"actual frames")
  outputs.append({"spr_no":key,"saved_mixed25_index":orig[0],"saved_mixed25_offset":orig[2],
    "saved_mixed25_end_offset":boundary,"saved_mixed25_segment_length":boundary-orig[2],
    "saved_mixed25_original_anim_count":orig[3],"saved_mixed25_index_reserved_word":orig[4],
    "original_tw10_group_index":int(g["index"]),"original_tw10_full_segment_sha256":sha,
    "original_tw10_derived_segment_length":len(whole),
    "original_tw10_animation_count":len(anim),"original_tw10_frame_positions":n,
    "original_tw10_distinct_nonzero_bitmap_keys":len(distinct),
    "original_tw10_first_frame_direction0_by_action":sorted(first,key=lambda x:x["action_code"])})
 total=sum(x["original_tw10_frame_positions"] for x in outputs)
 return {"schema":"stoneage.o63.four_tiger_source_spr_animation_join.r1",
  "source_scope":"MIXED25_SAME_PRESERVATION_SERVER_TO_SPR_INDEX_PLUS_TW10_INDEPENDENT_ORIGINAL_METADATA_REENCODE",
  "four_named_pet_addpet_source_ids":[2481,2482,2483,2484],
  "source_git_blob_sha":{"o61":"e1b131962b9a830cabb672ea1d76d1bad817c960",
                         "r40":"5b49d54d7cff2d79d3610db7ca4a37108f1f9e03"},
  "archived_tw10_tsv_sha256":PINS,"groups":outputs,"sum_original_tw10_frame_positions":total,
  "same_archive_animation_index_membership_proven":True,
  "saved_mixed25_actual_four_spr_segment_content_read":False,
  "tw10_actual_original_spr_raw_files_read_this_run":False,
  "tw10_original_full_animation_bytes_reencoded_from_preserved_metadata":True,
  "tw10_original_bitmap_pixels_read_this_run":False,
  "tw10_and_mixed25_full_segment_byte_equality_proven":False,
  "original_tiger_pet_runtime_or_species_deployment_proven":False,
  "original_game_world_entered":False,"original_sprites_published":False,
  "overall_completion_percent":None}
if __name__=="__main__":
 print(json.dumps(derive(),ensure_ascii=False,sort_keys=True,separators=(",",":")))
