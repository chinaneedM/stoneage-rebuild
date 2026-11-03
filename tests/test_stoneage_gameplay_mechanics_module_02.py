"""Metadata-only validation: the original proprietary NPC files are not uploaded to Git."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1] / "research" / "recovered"
NEW = ROOT / "STONEAGE-GAMEPLAY02-ORIGINAL-RIDER-PET-TALK-SOURCE-R1.json"
CHAR = ROOT / "STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json"
PREV = ROOT / "STONEAGE-GAMEPLAY01-ORIGINAL-FAMILY-ARENA-PET-REBIRTH-R1.json"
NAMES = {
    "family/familyman.template", "family/riderman.create", "family/riderman.conf",
    "family/riderman.conf.old", "family/riderman2.conf", "family/rider.create",
    "family/rider.arg", "sa60/rider.create", "sa60/rider.arg",
    "sa60/rider.arg.bak", "sa60/newbie/fighter", "sa60/newbie/petmaster",
    "pettalk/pettalk.menu",
    *(f"pettalk/ptalk{i:02}.arg" for i in range(1, 8)),
}

def verify(d, char, prev):
    assert d["schema"] == "stoneage.gameplay_mechanics_module02_original_rider_pet_talk_source.r1"
    source = d["source"]
    assert source["scope"] == "RETAINED_COMMUNITY_MIXED25_NOT_OFFICIAL_EARLY_DEPLOYMENT"
    assert source["all_2205_zip_NPC_files_sha_crc_verified"] is True
    assert (source["verified_NPC_files"], source["verified_NPC_bytes"]) == (2205, 1930332)
    assert (char["npc_subtree_source_files"], char["npc_subtree_source_bytes"]) == (2205, 1930332)
    assert source["upstream_CHAR01_immutable_blob_sha"] == "a088b61a3212f7049e7793f587123ffb29bebad7"
    assert source["parent_original_RAR_reopened_in_this_unit"] is False
    assert source["private_npc_zip_sha256"] == "c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f"
    actual = {r["path"]: r for r in d["verified_source_file_receipts"]}
    original = {r[0]: r for r in char["source_files"]}
    assert set(actual) == NAMES
    for path, r in actual.items():
        assert (r["bytes"], r["sha256"], r["crc32"]) == tuple(original[path][1:4])
    old = [r for r in prev["source_CREATE_references"] if r["family"] == "riderman"]
    new = d["rider_trainers"]
    blocks = {(r[0], r[1]): r for r in char["create_rows"]}
    assert len(old) == len(new) == 4
    for i, r in enumerate(new):
        c = blocks[("family/riderman.create", i)]
        assert r["create_ordinal"] == old[i]["create_ordinal"] == i
        assert r["create_sha256"] == old[i]["create_block_sha256"] == c[4]
        assert r["floorid"] == old[i]["source_floorid"] == c[5]
        assert r["graphicname"] == old[i]["source_graphicnum"] == c[6]
        assert r["trainer_family_index"] == i + 1
        assert r["conff_path"] == "family/riderman.conf" and r["conff_path"] in actual
        assert r["create_uses_file_keyword"] is False and old[i]["original_source_file"] is None
        assert r["create_uses_conff_keyword"] is True
    conf = d["riding_configurations"]
    live = conf["four_created_trainers_config"]
    assert live["path"] == "family/riderman.conf"
    assert live["source_window_ids"] == [1,2,100,110,120,130,140,1000,1010,1011,2000]
    assert live["source_gotowin_integer_occurrences"] == 17
    assert live["gotowin_targets_not_local_window_ids"] == [5,6,7,8,9]
    assert [(r["window"],r["source_course_max_pet_level_label"],r["takegold_integer"],r["yes_gotowin"]) for r in live["courses"]] == [
        (110,40,5000,6),(120,80,10000,7),(130,120,15000,8),(140,None,20000,9)
    ]
    assert all(r["letter_ids"] == [19005,19006,19007,19008] for r in live["courses"])
    older = conf["old_suffix_file"]
    assert older["path"] == "family/riderman.conf.old"
    assert older["source_window_count"] == 14 and older["course_winno"] == [110,120,130]
    assert older["literal_takegold_numeric_entries"] == 0 and older["proven_deployed"] is False
    special = conf["special_file"]
    assert special["path"] == "family/riderman2.conf"
    assert special["source_course_takegold"] == 20000
    assert special["source_window_count"] == 8
    assert special["configured_fifth_trainer_only_commented_out"] is True
    assert special["active_created_trainers_reference_it"] == 0
    rid = d["rider_item_argument_sources"]
    assert rid["family_current"]["path"] == "family/rider.arg"
    assert rid["sa60_backup"]["path"] == "sa60/rider.arg.bak"
    assert rid["sa60_current"]["path"] == "sa60/rider.arg"
    assert actual[rid["family_current"]["path"]]["sha256"] == actual[rid["sa60_backup"]["path"]]["sha256"]
    assert actual[rid["sa60_current"]["path"]]["sha256"] != actual[rid["family_current"]["path"]]["sha256"]
    assert (rid["family_current"]["npcpoint_triples"],rid["sa60_current"]["npcpoint_triples"]) == (17,9)
    assert all(v["literal_item_id"] == 20296 and v["trans_candidates"] == [5,6] for v in rid.values())
    talk = d["pet_talk_source_menu"]
    assert talk["menu_path"] == "pettalk/pettalk.menu"
    rows = talk["ordered_source_refs"]
    assert [x["source_pettempno"] for x in rows] == [718,2,914,913,170,401,1147]
    assert [x["path"] for x in rows] == [
        "pettalk/ptalk01.arg","pettalk/ptalk02.arg","pettalk/ptalk04.arg",
        "pettalk/ptalk03.arg","pettalk/ptalk05.arg","pettalk/ptalk06.arg",
        "pettalk/ptalk07.arg"
    ]
    counts = Counter()
    for row in rows:
        assert row["path"] in actual and row["source_pettempno_matches_target_file"] is True
        assert sum(row["original_section_counts"].values()) == row["total_original_section_headers"]
        counts.update(row["original_section_counts"])
    assert dict(counts) == {"EVENTRUN":67,"TALKRUN":38,"BOTH":20,"OTHER":7}
    assert sum(counts.values()) == d["summary"]["original_pet_talk_section_headers"] == 132
    assert d["summary"]["new_source_files_examined"] == 20
    assert {r["path"] for r in d["original_newbie_text_guides"]} == {
        "sa60/newbie/fighter","sa60/newbie/petmaster"
    }
    assert all(r["message_slot_headers"] == 9 for r in d["original_newbie_text_guides"])
    b = d["limits"]
    assert b["same_build_early_official_game_rule_proven"] is False
    assert b["original_riding_training_executed"] is False
    assert b["literal_takegold_proves_actual_debit"] is False
    assert b["pet_talk_content_actually_executed"] is False
    assert b["source_text_or_original_art_published"] is False
    assert b["archival_GAMEPLAY01_no_file_token_finding_preserved"] is True
    assert b["stage_A"] == "7_PARTIAL_2_OPEN" and b["overall_percent"] is None
    assert d["next"].startswith("GAMEPLAY-MECHANICS-MODULE-03")
    return True

class TestOriginalGameplay02(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.new=json.loads(NEW.read_text(encoding="utf-8"))
        cls.char=json.loads(CHAR.read_text(encoding="utf-8"))
        cls.prev=json.loads(PREV.read_text(encoding="utf-8"))
    def test_original_sources_and_all_joins(self):
        self.assertTrue(verify(self.new,self.char,self.prev))
    def reject(self,fn):
        d=deepcopy(self.new)
        fn(d)
        with self.assertRaises((AssertionError,KeyError,TypeError)):
            verify(d,self.char,self.prev)
    def test_false_conff_path_rejected(self):
        self.reject(lambda d:d["rider_trainers"][0].__setitem__("conff_path","missing.file"))
    def test_wrong_course_fee_rejected(self):
        self.reject(lambda d:d["riding_configurations"]["four_created_trainers_config"]["courses"][0].__setitem__("takegold_integer",0))
    def test_commented_fifth_trainer_not_deployed(self):
        self.reject(lambda d:d["riding_configurations"]["special_file"].__setitem__("active_created_trainers_reference_it",1))
    def test_wrong_pettempno_rejected(self):
        self.reject(lambda d:d["pet_talk_source_menu"]["ordered_source_refs"][0].__setitem__("source_pettempno",719))
    def test_pet_section_loss_rejected(self):
        self.reject(lambda d:d["pet_talk_source_menu"]["ordered_source_refs"][0]["original_section_counts"].__setitem__("EVENTRUN",1))
    def test_false_game_execution_rejected(self):
        self.reject(lambda d:d["limits"].__setitem__("original_riding_training_executed",True))
    def test_false_early_official_claim_rejected(self):
        self.reject(lambda d:d["limits"].__setitem__("same_build_early_official_game_rule_proven",True))
if __name__ == "__main__":
    unittest.main()
