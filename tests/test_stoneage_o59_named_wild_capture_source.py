"""O59 derived-only source and anti-promotion checks; no private original payload."""
import copy, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research/recovered/STONEAGE-O59-NAMED-WILD-CAPTURE-SOURCE-R1.json"
P=ROOT/"research/recovered/STONEAGE-O21-ENCOUNTER-TWO-NAMED-PET-SOURCE-R1.json"
def validate(d,o):
    def req(x):
        if not x: raise ValueError("original pet capture source or boundary changed")
    req(d["schema"]=="stoneage.o59.original_named_wild_capture_gate_and_template_modifier.r1")
    req(d["evidence_scope"].endswith("NOT_TW10_JSS1999_LIVE_EXECUTION"))
    req(d["remote_base"]["current_file_original_blob_sha"]=="20050acf279a01555ab06a381dfcdc936bd381a6" and d["remote_base"]["current_modified"] is False)
    req(d["preserved_original_rar"]["sha256"]=="d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5" and d["preserved_original_rar"]["whole_source_reverified_this_work_unit"] is True)
    pins={"encount.txt":(43420,"d58f5903"),"group1.txt":(70176,"b7a6ed50"),"enemy.txt":(222463,"0d60e57d"),"enemybase.txt":(147750,"29258170")}
    for k,(size,crc) in pins.items():
        x=d["exact_original_file_receipts"][k]
        req((x["bytes"],x["rar_crc32"])==(size,crc) and len(x["sha256"])==64 and x["all_original_bytes_read_and_SHA_CRC_verified"] is True)
        req(x["sha256"]==o["original_sources"][k]["sha256"])
    e=d["source_encounter"]
    req((e["row_id"],e["floor"],e["rectangle_xyxy"],e["selected_group_ids"],e["selected_raw_weight_values"])==(21,100,[582,399,783,560],[88,91],[50,50]) and e["selected_only_not_whole_area"] is True)
    req(e["row_sha256"]==o["bounded_original_encounter"]["source_row_sha256"])
    idx=d["raw_csv_column_zero_based"]
    req(idx["enemy_instance"]["ENEMY_PETFLG"]==13 and idx["enemy_template"]["E_T_GET"]==14 and idx["enemy_template"]["E_T_PETFLG"]==37)
    rows=d["selected_named_wild_enemy_gates"];prev=o["source_named_pet_links"]
    req(len(rows)==len(prev)==2)
    for i,(a,b) in enumerate(zip(rows,prev)):
        target=[(88,119,113,100297,11,"昆依","昆伊",False),(91,122,114,100298,9,"凱比特","凱比特",True)][i]
        req((a["source_encounter_group_id"],a["source_group_enemy_id"],a["source_enemy_template_no"],a["original_template_IMGNUMBER"],a["source_template_E_T_GET"],a["source_enemy_instance_display_suffix_CP950"],a["name_cp950_source"],a["source_template_name_equals_instance_display_suffix"])==target)
        req(a["source_instance_ENEMY_PETFLG"]==1 and a["source_template_E_T_PETFLG"]==1 and a["enemy_record_level_range"]==[1,1])
        req((a["source_encounter_group_id"],a["source_group_enemy_id"],a["source_enemy_template_no"],a["original_template_IMGNUMBER"])==(b["group_id"],b["enemy_id"],b["template_no"],b["enemybase_IMGNUMBER"]))
        for key in ("group1","enemy","enemybase"):
            req(a["record_sha256"][key]==b["original_"+key+"_row_sha256"])
    n=d["negative_contrast_other_enemy_not_in_selected_area"]
    req((n["enemy_id"],n["template_no"],n["instance_ENEMY_PETFLG"],n["template_E_T_GET"],n["template_E_T_PETFLG"])==(2250,29,0,-5,0) and n["outside_selected_encounter_pair"] is True)
    req(n["enemy_row_sha256"]=="741027edfd96ac03f4962ee55c3a973295b73f8878336c735ffb073c4fd46ecc")
    req(n["enemybase_row_sha256"]=="59d67b84311d5a51d2a84aba40d3368671bfc612ec421875fe137d71373c489f")
    s=d["source_interpretation"]
    req(s["two_template_modifiers"]==[11,9] and s["difference_in_score_before_charm_scaling"]==2 and s["template_modifier_NOT_direct_percent_or_outcome"] is True and s["no_captured_pet_or_runtime_encounter_observed"] is True)
    limits=d["strict_nonclaims"]
    req(all(v is False for k,v in limits.items() if k!="overall_completion_percent") and limits["overall_completion_percent"] is None)
    req(d["phase"]=={"stage_a":"7_PARTIAL_2_OPEN","stage_b":"GATED","wiki":"GATED","r79":"PAUSED_NON_BLOCKING"})
class TestO59(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(R.read_text());cls.o=json.loads(P.read_text())
    def test_source_and_prior_o21_join(self):validate(self.d,self.o)
    def test_invalid_capture_and_name_promotions_rejected(self):
        edits=[
        ("strict_nonclaims","original_game_world_entered",True),
        ("strict_nonclaims","specific_capture_probability_or_success_proven",True),
        ("strict_nonclaims","original_1999_JSS_or_TW10_species_capture_gates_proven",True),
        ("source_interpretation","two_template_modifiers",[11,11]),
        ("source_interpretation","template_modifier_NOT_direct_percent_or_outcome",False)]
        for part,key,value in edits:
            d=copy.deepcopy(self.d);d[part][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):validate(d,self.o)
        for i,key,value in [(0,"source_instance_ENEMY_PETFLG",0),(0,"source_enemy_instance_display_suffix_CP950","昆伊"),(1,"source_template_E_T_GET",11),(1,"source_template_E_T_PETFLG",0)]:
            d=copy.deepcopy(self.d);d["selected_named_wild_enemy_gates"][i][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):validate(d,self.o)
        d=copy.deepcopy(self.d);d["negative_contrast_other_enemy_not_in_selected_area"]["instance_ENEMY_PETFLG"]=1
        with self.assertRaises(ValueError):validate(d,self.o)
if __name__=="__main__":unittest.main()
