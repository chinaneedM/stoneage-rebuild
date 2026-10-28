"""Replay accepted SCENE17 source-derived report; negative evidence remains hard.
This public verifier uses only permanently archived metadata, not copyright bytes.
"""
import copy
import json
import re
from pathlib import Path
from tools.stoneage_scene16_nearby_npc import public_index, SOURCE_PATH, SOURCE_SIZE, SOURCE_SHA256, TEMPLATE_SIZE, TEMPLATE_SHA256

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-SCENE17-ORIGINAL-NPC-SOURCE-R1.json"
EXPECTED={
 "headers":7954, "requests":184, "http_bytes":12013836,
 "range_source_member_sha":"c9b000a836b0aae3d88358097039f1beea020d92ba84f6ccc338bb54bc478240",
 "template_sha":"0c5a58d5e31cafd3b58ccc1fa88fee7d1f95d12c0b87b04db9f06fea3b2a4df3",
 "source_block_sha":"bbc86e2ab64fa20e8f6702ee11e97c9ff659041c62fcf257bb8d16b2f06a4ce7",
 "template_block_sha":"5f24ae6f815471af9439ed4b824ae494006a8ba6fb7e4bac43b44b8ae5a89b29",
}
FALSE=("original_server_executed","original_client_world_entered",
"official_tw10_NPC_identity_authenticated","original_dialogue_published",
"raw_original_scripts_published","original_npc_rendered",
"original_archive_complete_sha256_reverified")


def need(ok,label):
 if not ok:raise ValueError(label)


def validate(r):
 need(r["schema"]=="stoneage.scene17.original_town1000_npc_source_r1" and
      r["source_scope"]=="COMMUNITY_MIXED25_ORIGINAL_MEMBER_BYTES_NOT_AUTHENTICATED_OFFICIAL_TW10","scope")
 need(r["source_status"]=="PINNED_MEMBER_ONE_TARGET_CANDIDATE" and
      r["original_member_hashes_verified"] is True and r["original_bytes_downloaded_for_analysis_only"] is True,"actual originals extracted")
 need(all(r[k] is False for k in FALSE) and r["overall_completion_percent"] is None,"historical boundaries")
 src=r["source_qualification"];public=public_index()
 need(src["source_status"]=="PINNED_MEMBER_ONE_TARGET_CANDIDATE" and
      src["matched_count"]==1 and len(src["matched_candidates"])==1,"one authentic source candidate")
 need(src["authenticated_create_blocks"]==25 and src["authenticated_template_blocks"]==41,"full original file records")
 need(src["catalog_anchor"]=={**public,"target_is_npc_source_verified":True},"actual manifest and exact doorway anchor")
 need(src["original_world_entered"] is False and
      src["original_npc_interaction_verified"] is False and
      src["official_tw10_npc_authenticated"] is False and
      src["original_dialogue_published"] is False and
      src["overall_completion_percent"] is None,"source projection no promotion")
 c=src["matched_candidates"][0]
 need(c["ordinal"]==1 and c["source_byte_range"]==[287,450] and
      c["source_block_sha256"]==EXPECTED["source_block_sha"],"authored byte-range identity")
 need(c["borncorner"]==[63,103,63,103] and
      c["numeric_source_fields"]=={
       "createnum":1,"dir":4,"floorid":1000,"graphicname":16048,"time":0},
      "actual target position and candidate image key")
 need(c["template_lookup_token"]=="npcgen_man" and
      c["template_binding"]=="EXACT_TEMPLATE_NAME_IN_PINNED_MEMBER" and
      c["template_source_block_sha256"]==EXPECTED["template_block_sha"] and
      c["functionset_token"]=="TownPeople","unique original template binding")
 need(c["name_original_raw_bytes"]==8 and
      c["name_original_sha256"]=="b66523220d17805c9e6b91cff10209eef1b1a4161fa2c3c17c09c6efa7a89959" and
      c["original_dialogue"] is None,"source name hash only, no fabricated dialogue")
 receipt=r["receipt"]
 need(receipt["headers_visited"]==EXPECTED["headers"] and
      receipt["range_requests"]==EXPECTED["requests"] and
      receipt["http206_bytes"]==EXPECTED["http_bytes"],"actual bounded HTTP source counts")
 need(receipt["whole_archive_or_part_redownloaded"] is False and
      receipt["original_NPC_scripts_uploaded"] is False and
      receipt["copyrighted_source_archive_uploaded"] is False,"no proprietary Git/artifact bytes")
 need(receipt["source_range_calls"]==184 and
      receipt["source_http206_bytes"]==12013836 and
      receipt["sparse_source_budget_bytes"]==33554432 and
      receipt["sparse_source_budget_requests"]==512,"bounded ranges")
 spans=receipt["range_receipts"];need(len(spans)==184,"actual 184 requested range records")
 seen=set();total=0
 for v in spans:
  need(v["part"] in (1,2) and v["start"]>=0 and
       v["end"]>=v["start"] and v["bytes"]==v["end"]-v["start"]+1 and
       v["bytes"]<=65536 and v["start"]%65536==0 and
       re.fullmatch("[0-9a-f]{64}",v["sha256"]) is not None,"actual source range row")
  key=(v["part"],v["start"]);need(key not in seen,"duplicate range receipt");seen.add(key);total+=v["bytes"]
 need(total==12013836,"conserved acquired HTTP bytes")
 members=receipt["two_original_members"]
 need(len(members)==2,"two selected original files")
 for m, path, size, sha, crc in zip(members,[
     "npc/genout/1000npc_m.create","npc/genout/npcgen.template"],
     [4413,4950],[SOURCE_SHA256,TEMPLATE_SHA256],[2981039746,1448375672]):
  need(m["name"].endswith("/gmsv/data/"+path) and m["bytes"]==size and
       m["sha256"]==sha and m["crc32"]==crc and m["unar_result"]==0 and
       m["dual_decompressor_byte_equal"] is True and
       all(re.fullmatch("[0-9a-f]{64}",m[k]) is not None
       for k in ("original_header_sha256","compressed_payload_sha256",
                 "isolated_member_sha256")), "two original member SHA CRC dual decoder proofs")
 need(r["template_source_member"]=={
      "bytes":4950,"sha256":TEMPLATE_SHA256,"source_creation_blocks":41},"template extracted")
 return {
 "original_members_verified":2,"authored_NPC_at_63_103":1,
 "source_graphicname":16048,"functionset":"TownPeople",
 "source_http206_bytes":12013836,"original_client_world_entered":False,
 "official_TW10_NPC_authenticated":False,
 }


def main():
 print(json.dumps(validate(json.loads(REPORT.read_bytes())),sort_keys=True))

if __name__=="__main__":main()
