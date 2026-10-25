"""Independent source custody: authenticated Taiwan 1.0 short PE-data labels, not entity IDs."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from tools.stoneage_tw10_original_text_r19 import EXPECTED

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-TW10-ORIGINAL-EXE-TEXT-CANDIDATES-R19.json"
SOURCE_SHA256="66bef73e28bfc8c2cda25d8a1b3a48c62dc1d90a7dc20be452931e03ab7d161c"
WITNESSES={
 "StoneAge/StoneAge.exe":{"下載失敗":205156,"啟動石器時代":205908,"連線發生錯誤":206416},
 "StoneAge/sa_3.exe":{"戰場地圖錯誤":351900,"沒有參戰的寵物":352068,"出其不意的攻擊":352260,"關閉動作視窗":353636}
}

def require(test,msg):
 if not test: raise AssertionError(msg)

def verify(d=None):
 d=json.loads(REPORT.read_text(encoding="utf-8")) if d is None else d
 canonical=(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
 require(hashlib.sha256(canonical).hexdigest()==SOURCE_SHA256,"original source-derived bytes differ")
 require(d["schema"]=="stoneage.tw10.original_executable_text_candidate.r19","schema mismatch")
 require(d["task"]=="EARLY-OFFICIAL-NAMED-CONTENT-SOURCE-19","task mismatch")
 require(d["source_region_version"]=="TW_WAEI_JSS_RETAIL_1_0_REDUMP_104630","version mismatch")
 require(d["original_npc_pet_quest_identity_mappings_proven"]==0,"world entity identity invented")
 require(d["original_executable_executed"] is False and d["actual_runtime_string_selection_proven"] is False,"unobserved runtime")
 require(d["early_official_server_master_acquired"] is False,"unacquired historical server")
 require(d["overall_restoration_percent"] is None and d["stage_b_and_wiki"]=="GATED","stage wrongly promoted")
 require(d["stage_a"]=="7 PARTIAL + 2 OPEN","Stage A changed")
 report=d["executable_observations"]
 require(set(report)==set(EXPECTED),"original executable set changed")
 orig_inventory=(ROOT/"research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt").read_text(encoding="utf-8")
 inventory={}
 for line in orig_inventory.splitlines():
  if line.startswith("CORE_FILE|category=runtime_executable|"):
   fields=dict(item.split("=",1) for item in line.split("|")[1:])
   inventory[fields["path"]]=fields
 require(set(inventory)==set(EXPECTED),"retail disc source inventory drift")
 for path,(size,sha) in EXPECTED.items():
  x=report[path]
  require(x["original_file_length"]==size and x["original_sha256"]==sha,"original executable fingerprint mismatch")
  require(int(inventory[path]["size"])==size and inventory[path]["sha256"]==sha,"disk SHA disagrees with source")
  require(x["sampling_limit"]==24 and len(x["candidates"])==x["sampled_candidate_count"]<=24,"samples not bounded")
  require(x["candidate_decode_occurrences"]>=len(x["candidates"]),"candidate census")
  require(sum(x["candidate_by_codec"].values())==x["candidate_decode_occurrences"],"codec census")
  sections=x["pe_section_scopes"]
  require(len(sections)>0 and all(s["name"] in (".rdata",".data") and s["file_offset"]+s["source_bytes"]<=size for s in sections),"PE code or invalid data")
  by_label={}
  for q in x["candidates"]:
   require(2<=len(q["decoded_short_label"])<=12,"unbounded copyrighted text")
   require(all(0x3400<=ord(ch)<=0x9fff for ch in q["decoded_short_label"]),"not strictly Han")
   require(q["source_candidate_codec"] in ("cp950","cp932","gb18030"),"unknown codec")
   require(len(q["source_bytes_sha256"])==64,"missing byte hash")
   require(q["entity_id"] is None and q["bitmap_id"] is None and q["spr_group_id"] is None,"invented entity")
   require(q["npc_quest_pet_identity_qualified"] is False and q["source_nul_terminated"] is True,"unproved game content")
   require(any(q["source_pe_data_section"]==s["name"] and s["file_offset"]<=q["source_file_offset"] and q["source_file_offset"]+q["byte_count"]+1<=s["file_offset"]+s["source_bytes"] for s in sections),"outside protected PE data section")
   if q["source_candidate_codec"]=="cp950": by_label[q["decoded_short_label"]]=q
  for label,off in WITNESSES[path].items():
   require(label in by_label and by_label[label]["source_file_offset"]==off,"anchored literal missing: "+label)
   raw=label.encode("cp950")
   require(len(raw)==by_label[label]["byte_count"] and hashlib.sha256(raw).hexdigest()==by_label[label]["source_bytes_sha256"],"original CP950 byte witness mismatched")
 return True

if __name__=="__main__":
 verify()
 print("R19_TW10_ORIGINAL_SOURCE_SHORT_UI_LABELS=PASS")
 print("R19_ORIGINAL_NPC_PET_QUEST_ENTITY_RESOURCE_JOINS=OPEN")
