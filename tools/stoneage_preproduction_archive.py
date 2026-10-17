"""Validate historical-content coverage and future public-wiki metadata without fake source completeness."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json"
PINS={
  "research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json": "e39a3a6020b578da017ab0bfa9369dc083e0b700",
  "research/recovered/STONEAGE-TW10-UI-SEMANTICS-R1.json": "ee3d230317c47b13e3513f25c3feba2ff9305e1c",
  "docs/STAGE-A-CONSOLIDATED-REVIEW-R1.md": "07c9950a40d110d4dabb80b11412db8b4ea64ba9",
  "research/recovered/STONEAGE-LEGACY-ASSISTANT-AND-CONTENT-GAP-R1.json": "103122ec0358d45fe149b0389b8ac3ecac3b315a",
  "research/recovered/STONEAGE-TW10-VS-25-RESOURCE-DIFF-R1.txt": "b86de21a9c1dc28af1b533f20ebd4b37428517a6",
  "research/mechanics/STONEAGE-PET-GROWTH-CORE-R1.md": "87cdd063f05f6d6f334007cf3db7a31a8d1654a8",
  "research/clients/STONEAGE-TW10-CLIENT-DATA-BOUNDARY-R1.md": "11e2b77bce2febfef37c3a0c87dec878a6f289ee",
  "docs/STAGE-B-COLLABORATIVE-DESIGN-BRIEF-R1.md": "3a791ba28cad340a7603c9ac3ade32d3e63955ee",
  "docs/STONEAGE-PET-QUEST-CONTENT-COVERAGE-RECHECK-R1.md": "9c5f41a9db9bce91528a0d370b25c4083fd760ba"
}
DOMAIN_IDS=["version_lineage","login_splash","character_creation","character_sprite_model","world_map","npc_identity","npc_dialog_ui","quest_content","pet_species","pet_visual","pet_stats","pet_growth","pet_skills","pet_encounter","ride_mount","battle_ui_rules","item_equipment_economy","audio_fx","helper_versions","helper_capabilities","reference_web","future_player_wiki"]
RELATION_IDS=["char_creation_body","char_creation_face","npc_world_record","npc_dialog_event","quest_dialog","pet_graphic","pet_stats","pet_growth","pet_skill","pet_habitat","pet_ride","quest_item","battle_graphics","helpers_history","wiki_exports"]
PROFILES=["JSS1999_ORIGIN","TW10","CN182","RECOVERED25","LATER_OFFICIAL","PRIVATE_SERVER","NEW_GAME"]
COLLECTIONS=["versions","sources","characters","screens","maps","npcs","quests","pets","pet_animations","growth_profiles","skills","items","recipes","encounters","riding","historical_sites","helper_programs","helper_capabilities","tutorials"]
def gitblob(raw):
 return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def req(flag,msg):
 if not flag: raise ValueError(msg)
def validate(p):
 req(p["schema"]=="stoneage.preproduction_content_archive_r1","schema")
 req(p["baseline_main"]=="ba4e12c265c1db7caf5d5afdd4b3e068b3df1d1f" and p["baseline_tree"]=="081c6952f3ae9ee37ec4e99b25f75edd6c0d3b84","baseline")
 req(p["source_pins"]==PINS,"source pin list drift")
 for path,sha in PINS.items():
  req(gitblob((ROOT/path).read_bytes())==sha,"source blob mismatch "+path)
 req([v["id"] for v in p["version_profiles"]]==PROFILES,"version provenance")
 req(all(v["can_backfill"] is False for v in p["version_profiles"]),"unsafe cross-build merging")
 req([d["id"] for d in p["domains"]]==DOMAIN_IDS,"missing content domain")
 req(all(d["complete"] is False and d["original_full_payload_recovered"] is False and d["missing"] and d["verification_target"] for d in p["domains"]),"false domain coverage completion")
 req([r["id"] for r in p["relationship_requirements"]]==RELATION_IDS,"missing crosswalk requirements")
 req(all(r["same_build_runtime_verified"] is False and r["status"]=="OPEN_OR_VERSION_SEPARATED" for r in p["relationship_requirements"]),"unproven matching")
 req(set(x["id"] for x in p["domains"])>=set(r["from"] for r in p["relationship_requirements"]),"bad source foreign keys")
 req(set(x["id"] for x in p["domains"])>=set(r["to"] for r in p["relationship_requirements"]),"bad target foreign keys")
 tw=json.loads((ROOT/"research/recovered/STONEAGE-TW10-UI-SEMANTICS-R1.json").read_text(encoding="utf-8"))
 sc=json.loads((ROOT/"research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json").read_text(encoding="utf-8"))
 req(p["tw10_verified_surface_count"]==len(tw["surfaces"])==5,"UI surface count")
 req(p["tw10_verified_record_shapes"]==len(sc["records"])==16,"record types")
 req([s["id"] for s in p["tw10_ui_structural_sources"]]==[s["id"] for s in tw["surfaces"]],"UI shape ids")
 req(all(s["renderVerified"] is False for s in p["tw10_ui_structural_sources"]),"visual claim")
 a=p["tw10_asset_census"]
 req(a["bitmap_address_records"]==125996 and a["sprite_groups"]==464 and a["animation_records"]==39065 and a["frame_records"]==242085,"graphics record census")
 req(a["species_count"] is None and a["original_species_to_sprite_map_complete"] is False,"graphics not pet census")
 d=p["descendant_pet_probe"]
 req(d["source"]=="RECOVERED25" and d["active_enemybase_rows"]==988 and d["inactive_enemybase_rows"]==640 and d["original_v1_species_count"] is None,"descendant status")
 legacy=json.loads((ROOT/"research/recovered/STONEAGE-LEGACY-ASSISTANT-AND-CONTENT-GAP-R1.json").read_text(encoding="utf-8"))
 h=p["legacy_helper_corpus"]
 req(h["source_manifest"]=="research/recovered/STONEAGE-LEGACY-ASSISTANT-AND-CONTENT-GAP-R1.json","helper source")
 req(h["initial_source_count"]==legacy["source_count"] and h["initial_tool_families"]==legacy["tool_family_count"] and h["initial_feature_families"]==legacy["feature_count"],"helper catalog census")
 req(all(h[k] is False for k in ("all_programs_archived","all_versions_collected","all_features_semantically_reconstructed","all_programs_executed")),"false helper restoration")
 req(h["feature_reconstruction_levels"]==["MENTION_ONLY","SOURCE_ATTESTED","VERSION_SPECIFIC_SEMANTIC_SPEC","SAFE_REFERENCE_BEHAVIOR_VERIFIED","NEW_GAME_ADOPTION_DECIDED"],"helper restoration workflow")
 req(h["prohibited_transition"]=="MENTION_ONLY_TO_HISTORICALLY_VERIFIED_WITHOUT_SOURCE","helper no evidence gate")
 req(p["future_website"]["required_collections"]==COLLECTIONS and len(COLLECTIONS)>=15,"future wiki schema")
 wc=p["future_website"]["record_contract"]
 req(set(["record_id","entity_type","version_profile","source_refs","verification_status","rights_status","record_revision"]).issubset(wc["required"]),"missing website source and rights metadata")
 req("Public release only when rights_status=RELEASE_APPROVED" in wc["export_rules"],"unapproved copying risk")
 for k in ("website_not_built","production_not_started"):req(wc[k] is True,"website claimed")
 req(all(p["future_website"][k] is False for k in ("website_development_started","site_go_live","original_company_site_cloned")),"website production claim")
 req(p["future_website"]["player_publication_requires_separate_approval"] is True,"publication bypass")
 r=p["status"]
 req(r["historical_research_checkpoint_accepted"] is True,"history rewritten")
 for k in ("all_historical_quests_complete","all_historical_pets_complete","all_npc_interactions_complete","all_historical_avatars_complete","all_login_and_ui_frames_complete","all_external_helper_functions_complete","stage_b_production_started","website_implementation_started"): req(r[k] is False,"false completeness or build status "+k)
 req(r["overall_completion_percent"] is None and r["r79"]=="PAUSED_NON_BLOCKING","invented percent or R79")
 req([v["id"] for v in p["milestone_work_order"]]==["P1","P2","P3","P4","P5"],"not enough concrete preparation milestones")
 req(p["next_priority"]=="PET-ASSET-GROWTH-CATALOG-MATRIX-02","wrong priority")
 req(p["raw_copyrighted_original_payload_added"] is False and p["no_unbounded_feature_claim"] is True,"claims/rights")
 for s in p["public_discovery_sources"]:
  req(s["url"].startswith("https://") and s["cannot_certify"] and s["scope"].endswith("ONLY"),"public source mistaken as original")
 for path in ("docs/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.md",):
  content=(ROOT/path).read_text(encoding="utf-8")
  req(all(w in content for w in ["登录","NPC","外挂","宠物","资料网站","UNKNOWN","125,996","PET-ASSET-GROWTH-CATALOG-MATRIX-02"]),"incomplete human-readable plan")
 return {"status":"PASS","domains":len(DOMAIN_IDS),"versions":len(PROFILES),"source_bounded_relation_targets":len(RELATION_IDS),"web_collections":len(COLLECTIONS),"all_original_content_complete":False,"website_built":False}
if __name__=="__main__":
 print(json.dumps(validate(json.loads(PATH.read_text(encoding="utf-8"))),ensure_ascii=False,sort_keys=True))
