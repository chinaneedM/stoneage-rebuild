"""Check sourced legacy-assistant genealogy and pet/quest content honesty."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"research/recovered/STONEAGE-LEGACY-ASSISTANT-AND-CONTENT-GAP-R1.json"
BLOBS={
  "docs/STAGE-A-CONSOLIDATED-REVIEW-R1.md": "07c9950a40d110d4dabb80b11412db8b4ea64ba9",
  "docs/specs/STONEAGE-TW10-UI-RESOURCE-BIND-R1.md": "600ea59798153f2ab85887b5207f3323b1a19959",
  "research/recovered/STONEAGE-TW10-UI-RESOURCE-BIND-SCOPE-R1.json": "8db0381f876aea901fbdaf55aaa031157d035800",
  "research/recovered/STONEAGE-TW10-VS-25-RESOURCE-DIFF-R1.txt": "b86de21a9c1dc28af1b533f20ebd4b37428517a6",
  "research/mechanics/STONEAGE-PET-GROWTH-CORE-R1.md": "87cdd063f05f6d6f334007cf3db7a31a8d1654a8",
  "research/recovered/STONEAGE-25-PET-GROWTH-R1.txt": "5c528fb382ad13484572bd49905480a6b5775e18",
  "research/clients/STONEAGE-TW10-CLIENT-DATA-BOUNDARY-R1.md": "11e2b77bce2febfef37c3a0c87dec878a6f289ee"
}
def sha(raw):
 return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def req(v,m):
 if not v: raise ValueError(m)
def validate(p):
 req(p["schema"]=="stoneage.legacy_assistant_and_content_gap_registry.r1","schema")
 req(p["baseline_head"]=="d393b135b4fb2e62d5b5162eb3878981cb3e02a8" and p["baseline_tree"]=="5f55795d1b0ad3e63e99abb3be374c8cd4a8ace7","remote baseline")
 for path,blob in BLOBS.items(): req(sha((ROOT/path).read_bytes())==blob,"source pin "+path)
 req(p["source_count"]==len(p["external_sources"])>=10,"sources")
 req(p["tool_family_count"]==len(p["assistant_tools"])>=14,"families")
 req(p["feature_count"]==len(p["game_integrated_functions"])>=10,"features")
 req(p["pet_content_domains"]==len(p["content_gaps"])==10,"domains")
 src={x["id"]:x for x in p["external_sources"]}
 req(len(src)==len(p["external_sources"]),"duplicate source")
 for s in src.values():
  req(s["url"].startswith("https://") and s["facts"] and s["caution"],"source custody")
 names=set()
 for t in p["assistant_tools"]:
  req(t["id"] not in names,"duplicate family")
  names.add(t["id"])
  req(t["source"] and all(v in src for v in t["source"]),"unsupported historical tool")
 req({x["id"] for x in p["content_gaps"]}=={"pet_species_roster","pet_graphic_identity","pet_2d_frames","pet_base_stats","pet_growth","pet_skills","pet_capture","pet_riding","original_quests","world_npc"},"content dimensions")
 req(p["source_layers"]==["V1_DIRECT","EARLY_LINEAGE","LATER_RECOVERED","MODERN_SYNTHETIC","NEW_DESIGN"],"source layers")
 for k in ("original_1999_tool_comprehensive_listing","all_original_pets_identified","all_original_pet_images_mapped","original_pet_growth_table_complete","original_quests_complete","new_game_assistant_production_started","raw_proprietary_binaries_added","stage_a_bounded_review_reversed"):
  req(p[k] is False,"overclaim "+k)
 r=p["pet_resource_claim"]
 req(r["tw10_bitmap_records"]==125996 and r["tw10_sprite_groups"]==464 and r["animations"]==39065 and r["frames"]==242085,"resource counts")
 req(r["pet_species_count"] is None and r["all_pets_shown"] is False,"resource count conflated with species")
 d=p["later_enemybase_derived_count"]
 req(d=={"recovered25_active_rows":988,"other_rows":640,"all_are_unique_1999_pet_species":False},"descendant pet conflation")
 req(p["conditional_stage_a_reopen"]=="ONLY_NAMED_MATERIAL_SAME_BUILD_EVIDENCE_OR_CROSSWALK_GAP","stage A reopening")
 req(p["production_design_gate"]=="DISCUSSION_ONLY" and p["next_priority"]=="PET-ASSET-GROWTH-CATALOG-MATRIX-02","production gate")
 features={x["id"]:x for x in p["game_integrated_functions"]}
 req(features["F12"]["decision"]=="REJECT_EXPLOIT","unsafe product-design advice")
 req(features["F09"]["decision"]=="GATED_FUTURE_DISCUSSION","script production overclaim")
 req(features["F11"]["decision"]=="REPLACE_OR_DROP","multibox suggestion")
 for s in p["game_integrated_functions"]:req(all(z in src for z in s["early"]),"unattributed feature")
 for f in ("docs/STONEAGE-LEGACY-ASSISTANT-TOOLS-CATALOG-R1.md","docs/STONEAGE-PET-QUEST-CONTENT-COVERAGE-RECHECK-R1.md"):
  req((ROOT/f).exists(),"missing review document")
 return {"status":"PASS","historical_tool_families":len(names),"dated_and_later_sources":len(src),"possible_built_in_features":len(features),"pet_and_quest_content_domains":10,"all_original_pets_restored":False}
if __name__=="__main__":
 print(json.dumps(validate(json.loads(MANIFEST.read_text(encoding="utf-8"))),sort_keys=True))
