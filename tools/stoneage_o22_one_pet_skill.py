"""O22 source-only original one-pet-skill provenance: no original bytes in Git."""
import json
from pathlib import Path
REPORT=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-O22-ONE-PET-SKILL-SOURCE-R1.json"
PINS={
"encount.txt":(43420,"70bbd997d98508a0587df183b5bdd48222ff42db91bf21bea632e0ed6f2fea87"),
"group1.txt":(70176,"4a02f2a3fa3d2dcf5589d8a2a560313c35d5a0a7e5e0589cc8df5f7df159ea8f"),
"enemy.txt":(222463,"cc7418d3b6726f1c458fef9e44a24696d05f076b67c62a56ed2293e26ae63bb6"),
"enemybase.txt":(147750,"1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7"),
"petskill.txt":(15112,"f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4")}
ROWS={
"encounter":(1,77,"78dd537235bee8d0f74fdf610a7cb46915c1d949b39de6f9dfeebba1ee8f9358"),
"group":(1048,68,"dbbea4fe40c4010d2ace1d0c280862a080443410b9546df119a3bccd6e4bbdfe"),
"enemy":(1721,96,"741027edfd96ac03f4962ee55c3a973295b73f8878336c735ffb073c4fd46ecc"),
"template":(29,153,"59d67b84311d5a51d2a84aba40d3368671bfc612ec421875fe137d71373c489f"),
"skill":(18,120,"0f1d7758ce8dfb5a31fd83875f5707b8414e1601e55d3415d8418297886b1952")}
def need(a,msg):
    if not a:raise ValueError(msg)
def validate(d):
    need(d["schema"]=="stoneage.o22.one_original_later_pet_skill_documentary_link.r1","schema")
    need(d["source_head"]=="f0b080e54e9afd50905c77285f935bfe1fa0af0d" and d["source_tree"]=="0e53f7bee71f88c10b6493c6c9c8b7ac466c628f","parent")
    need(d["source_version"]=="PRESERVED_MIXED25_NOT_OFFICIAL_TW10_OR_JSS1999","source version")
    need(d["original_current_blob_preserved"]=="20050acf279a01555ab06a381dfcdc936bd381a6","original complete CURRENT")
    need(d["source_carrier_sha256"]=="d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5","carrier")
    need(set(d["source_files"])==set(PINS),"exact five originals")
    for k,v in PINS.items():need((d["source_files"][k]["bytes"],d["source_files"][k]["sha256"])==v,"source identity "+k)
    need(set(d["source_rows"])==set(ROWS),"exact original source rows")
    for k,v in ROWS.items():
        r=d["source_rows"][k]
        need((r["source_line"],r["bytes"],r["sha256"])==v,"source row "+k)
    c=d["bounded_original_source_chain"]
    expected={"encount_id":21,"floor":100,"source_rectangle_inclusive":[582,399,783,560],"group_id":1230,"encount_group_source_raw_weight":100,"enemy_id":2250,"enemybase_TEMPNO":29,"enemybase_name_CP950":"白唬","PETSKILL_slot":3,"PETSKILL_id":61,"petskill_table_numeric_id":61,"petskill_table_CP950_name":"猛毒攻擊","petskill_function_name_original_ascii":"PETSKILL_StatusChange","source_pet_skill_slot_to_table_id_unique":True}
    for k,v in expected.items():need(c[k]==v,"static original content "+k)
    for k in ("actual_encounter_in_original_game_executed","actual_petskill_callback_executed","poison_chance_verified","poison_turn_duration_verified","TW10_same_named_skill_verified"):
        need(c[k] is False,"no original gameplay inference "+k)
    p=d["private_custody"]
    need((p["zip_bytes"],p["zip_sha256"],p["entries"])==(2376,"58998c669dac5eba4cee825ae8b1af3b3e1f318464b1899494f2c97a5d434fb9",6),"zip original proof")
    need(p["original_row_zip_readback_sha_verified"] is True and p["original_text_published_in_public_Git"] is False,"originals are private")
    v=d["limits"]
    for k in ("original_world_entered","original_TW10_or_JSS1999_skill_runtime_verified","late_server_native_callback_executed","historical_skill_success_rate_verified"):
        need(v[k] is False,"unproved skill behavior "+k)
    need(v["overall_percent"] is None,"not completion percentage")
    return {"source_chain":"21 -> 1230 -> 2250 -> 29 -> 61","original_world_entered":False}
if __name__=="__main__":print(json.dumps(validate(json.loads(REPORT.read_bytes())),ensure_ascii=False))
