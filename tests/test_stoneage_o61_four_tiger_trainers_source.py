"""O61 original four tiger trainers and 12 later-source pet-grant options; derived-only."""
import json,copy,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"research/recovered/STONEAGE-O61-FOUR-TIGER-TRAINERS-SOURCE-R1.json"
R18=ROOT/"research/recovered/STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json"
def validate(d,r18):
    def req(ok): 
        if not ok:raise ValueError("O61 source qualification / disjoint BBI / negative guard")
    req(d["schema"]=="stoneage.o61.later_sa60_four_tiger_trainer_source_conditioned_addpet.r1")
    req(d["source_era"].endswith("NOT_JSS1999_OR_TW1_OFFICIAL_RUNTIME"))
    b=d["baseline"];req((b["current_sha"],b["current_bytes"],b["current_unchanged"])==("20050acf279a01555ab06a381dfcdc936bd381a6",2708031,True))
    a=d["archive"];req((a["bytes"],a["sha256"],a["read_sha_verified"])==(361255180,"d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5",True))
    old={x["path"]:x for x in r18["all_server_occurrences"]}
    for p,expected in {
      "npc/sa60/newbie/tiger.create":(714,"048c55f59a10c5b9d6ea3a0bdc6ff0c79aacfd69abeb2c18477ca6586c5a887b",6579,"aa2131b7"),
      "npc/sa60/newbie/m_tiger":(15073,"0a075f092b3b1e3f3b7c45e5ef18e4eb707392873cd67df1ebd500518f62674e",6574,"22405aaa")
    }.items():
        f=d["source_files"][p];req((f["bytes"],f["sha256"],f["rar_index"],f["crc32"],f["sha_crc_and_r18_match"])==(*expected,True))
        req((old[p]["size"],old[p]["sha256"])==(f["bytes"],f["sha256"]))
    expected_creations=[(1040,[61,43],"1c128f3c3b462dd7c838227d2667986a08700b47747446ea31c033468d078736"),
       (2030,[58,16],"385af720dc8c56bb7e88f9bff81dfc94ba5a17ad703316bd6824b00f18230894"),
       (3030,[52,22],"973394336aa7db7b60c93789b2475fa673f6b8686456d3928863bd8a51c94071"),
       (4030,[16,32],"3357e2f61bf6c97c815ff7de3b5c2b5a905caaba6f600d161d6a20b9dd3eba1b")]
    rows=d["creator_records"];req(len(rows)==4)
    for c,(floor,xy,h) in zip(rows,expected_creations):
        req((c["floor"],c["xy"],c["creator_block_sha256"])==(floor,xy,h))
        req(c["graphicname"]==16354 and c["dir"]==6 and c["source_name"]=="虎的訓練師")
        req(c["script_pointer"]=="npcgen_warpman|file:sa60/newbie/m_tiger")
    s=d["script_observation"]
    req(s["source_directive"]=="NEWWARPMAN" and s["exact_talkevent_count"]==16)
    req(s["grant_talkevent_ids"]==list(range(1,13)) and s["non_grant_talkevent_ids"]==[13,14,15,16])
    req(s["conditions_common_to_all_12_grant_options"]==["LV>29","ENDEV=4","NOWEV!=166","TRANS=0"])
    req(s["grant_command"]=="AddPet" and s["source_event_assignment"]=="Event_Now:166")
    req((s["source_bbi_count_with_duplicates"],s["source_bbi_count_distinct"],s["source_bbi_min"],s["source_bbi_max"],s["source_bbi_exact_contiguous_range"],s["different_reward_ids_have_overlapping_bbi"])==(240,240,100000,100239,True,False))
    groups=s["conditional_pet_reward_groups"];req(len(groups)==4)
    for got,expected in zip(groups,[("紅虎",2483,[1,2,3]),("綠虎",2481,[4,5,6]),("金虎",2484,[7,8,9]),("黃虎",2482,[10,11,12])]):
        req((got["source_label"],got["source_grant_pet_id"],got["talkevent_ids"])==expected)
        req(got["bbi_clause_counts"]==[23,23,14] and got["bbi_union_distinct_count"]==60)
    req(s["non_grant_condition_rows"]==[
      {"talkevent":13,"free":"LV>29&ENDEV=4&NOWEV=166&TRANS=0"},
      {"talkevent":14,"free":"LV>0&ENDEV!=4&TRANS=0&BBI<101000"},
      {"talkevent":15,"free":"LV>0&TRANS!=0"},
      {"talkevent":16,"free":"LV>0&BBI>100999"}])
    q=d["reward_id_qualification"];req(q["source_ids"]==[2481,2482,2483,2484])
    req(q["none_of_four_ids_in_either_checked_TEMPNO"] is True and q["original_248x_absent_as_direct_TEMPNO_but_present_as_ENEMY_ID"] is True)
    req(q["addon_pet_id_namespace_to_template_link_proven"] is True and q["all_four_enemy_ids_unique_and_templates_resolve"] is True and q["source_script_actual_ability_to_grant_pet_proven"] is False)
    e=q["same_preservation_enemy_instance"];req((e["path"],e["size"],e["sha256"],e["original_rar_crc32"],e["fully_sha_crc_and_r18_verified"])==("enemy.txt",222463,"cc7418d3b6726f1c458fef9e44a24696d05f076b67c62a56ed2293e26ae63bb6","0d60e57d",True))
    req((old["enemy.txt"]["size"],old["enemy.txt"]["sha256"])==(e["size"],e["sha256"]))
    links=q["same_preservation_explicit_instance_template_links"];req(len(links)==4)
    expected=[
      (2481,"綠虎",1936,"給新手的貝魯卡",161,161,"新手貝魯卡",100327,"51fb86c7d8145ec270ec115e5fa0d1b6c6bb10f80c7153b0bad51762a50fa595","26bf74dbb3eae136c6875fb1704a4c8231abc8e0eb9e7b6fc7c9e506147b874c"),
      (2482,"黃虎",1937,"給新手的貝魯伊卡",162,162,"新手貝魯伊卡",100328,"ee116d3ac9a3de5b99f4b8630db96cb2ae04b8133fcfd6166b593ac454531729","a1c01650eaf1d15f97764f6e54e93bde3bf3df67e71e96e987b591916407eade"),
      (2483,"紅虎",1938,"給新手的格魯西斯",163,163,"新手格魯西斯",100329,"94497747ad5a7b3de1ac90f425a9cd32dc689e919880636edb4675713b2c04ca","23eccb993bab5bd8f9179addf5cf9ad6ae1d92049e2b624f39cec600f0046f36"),
      (2484,"金虎",1939,"給新手的金格薩貝魯",164,164,"新手金格薩貝魯",100330,"ee26ffebdcbb12d47fbd6166e9c50cf0f1a4762e5863b66fc7873dea8c68435e","a37db0aabd1a185e4eb637702b6e2a4730a44a2b29014c44b710b24bcde8b1db")]
    for v,row in zip(links,expected):
        got=(v["addpet_id"],v["color"],v["enemy_row_line"],v["enemy_name"],v["template_no"],v["template_line"],v["template_name"],v["graphic_id"],v["enemy_record_sha256"],v["template_sha256"])
        req(got==row and v["instance_level_range"]==[1,1] and v["instance_petflag"]==1 and v["template_petflag"]==1 and v["template_default_capture_get"]==5)
        req(len(v["enemy_record_sha256"])==len(v["template_sha256"])==64)
    later=q["later_code_qualified_example"];req(later["fixed_commit"]=="2f736808ff4361f5429ee919b718c88fabb60346" and later["git_blob_sha"]=="019a9578b122773df90442719ece50ad79fbe1b4" and later["function"]=="NPC_EventAddPet")
    req(later["same_rar_server_binary_or_build_proven"] is False and later["script_talkevent_uses_this_exact_handler_proven"] is False)
    for p,(size,sha,n,maxn) in {
       "enemybase.txt":(147750,"1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7",988,1240),
       "enemybase2.txt":(94248,"8ecb23231ae1aeb21fe943c7b459f0c0d10ef3599aedfeaeccca783b077f5fd4",640,1051)}.items():
        x=q["template_files"][p];req((x["bytes"],x["sha256"],x["distinct_TEMPNO_count"],x["maximum_TEMPNO"])==(size,sha,n,maxn))
        req((old[p]["size"],old[p]["sha256"])==(x["bytes"],x["sha256"]))
    lim=d["source_limits"];req(all(lim[k] is False for k in (
      "actual_grant_and_owned_pet_state_observed","event_166_server_persistence_proven","original_mount_unlock_or_riding_executed",
      "original_jss1999_or_tw10_rules_proven","source_240_BBI_labels_official_meaning_proven","user_world_entered","private_source_or_dialogue_published")))
    req(lim["overall_completion_percent"] is None)
    req(d["phase"]=={"stage_a":"7_PARTIAL_2_OPEN","stage_b":"GATED","wiki":"GATED","r79":"PAUSED_NON_BLOCKING"})
class O61SourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(DATA.read_bytes());cls.r18=json.loads(R18.read_bytes())
    def test_source_r18_identity_and_240_disjoint_character_condition_values(self):validate(self.data,self.r18)
    def test_fail_closed_no_invented_pet_identity_and_riding(self):
        edits=[
          (("reward_id_qualification","none_of_four_ids_in_either_checked_TEMPNO"),False),
          (("reward_id_qualification","source_script_actual_ability_to_grant_pet_proven"),True),
          (("reward_id_qualification","all_four_enemy_ids_unique_and_templates_resolve"),False),
          (("source_limits","original_mount_unlock_or_riding_executed"),True),
          (("source_limits","original_jss1999_or_tw10_rules_proven"),True),
          (("source_limits","user_world_entered"),True),
          (("script_observation","source_bbi_count_distinct"),239),
          (("script_observation","different_reward_ids_have_overlapping_bbi"),True),
        ]
        for (scope,key),new in edits:
            x=copy.deepcopy(self.data);x[scope][key]=new
            with self.subTest(scope=scope,key=key),self.assertRaises(ValueError):validate(x,self.r18)
        x=copy.deepcopy(self.data);x["reward_id_qualification"]["same_preservation_explicit_instance_template_links"][0]["template_no"]=164
        with self.assertRaises(ValueError):validate(x,self.r18)
        x=copy.deepcopy(self.data);x["script_observation"]["conditional_pet_reward_groups"][0]["source_grant_pet_id"]=2482
        with self.assertRaises(ValueError):validate(x,self.r18)
if __name__=="__main__":unittest.main()
