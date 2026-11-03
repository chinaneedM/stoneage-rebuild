"""QUEST03 public source-index contracts: never execute proprietary server, images or dialogue."""
import json, re, unittest
from pathlib import Path
from collections import Counter
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[1]/"research"/"recovered"
QUEST=ROOT/"STONEAGE-QUEST-STORY-MODULE-03-QUIZ-TIMEMAN-ORIGINAL-SOURCE-R1.json"
CHAR=ROOT/"STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json"
HEX=re.compile(r"^[0-9a-f]{64}$")

def verify(d,c):
    assert d["schema"]=="stoneage.quest_story_module03_original_quiz_timeman_control_sources.r1"
    refs=d["source_creation_references"];files=d["source_parameter_files"]
    assert len(refs)==56 and len(files)==55
    m={x[0]:x for x in c["source_files"]}
    cr={(r[0],r[1]):r for r in c["create_rows"]}
    known={}
    for f in files:
        assert f["source_parameter_path"] not in known
        known[f["source_parameter_path"]]=f
        r=m[f["source_parameter_path"]]
        assert (f["original_bytes"],f["original_sha256"],f["original_crc32"])==tuple(r[1:4])
        assert HEX.fullmatch(f["original_sha256"])
        assert f["origin_class"]=="ORIGIN_UNRESOLVED"
    counts=Counter();families=Counter()
    for x in refs:
        assert x["origin_class"]=="ORIGIN_UNRESOLVED"
        r=cr[(x["source_create_path"],x["create_block_ordinal"])]
        assert r[11]==x["family"]
        assert r[4]==x["original_create_block_sha256"]
        assert r[5]==x["original_floorid_numeric"] and r[6]==x["original_graphic_alias_numeric"]
        assert r[15]==[[x["source_parameter_path"],"EXACT_SAME_NPC_SUBTREE_PATH",x["original_parameter_sha256"]]]
        assert x["original_parameter_sha256"]==known[x["source_parameter_path"]]["original_sha256"]
        counts[x["source_parameter_path"]]+=1
        families[x["family"]]+=1
    assert dict(families)=={"npcgen_quiz":22,"npcgen_timeman":34}
    assert all(f["original_create_ref_count"]==counts[f["source_parameter_path"]] for f in files)
    quiz=[f for f in files if f["family"]=="npcgen_quiz"]
    times=[f for f in files if f["family"]=="npcgen_timeman"]
    assert len(quiz)==22 and len(times)==33
    assert sum(f["original_bytes"] for f in quiz)==9975
    assert sum(f["original_bytes"] for f in times)==3811
    assert len(set(x["source_parameter_path"] for x in refs if x["family"]=="npcgen_quiz"))==22
    assert sum(f["source_has_warp_literal"] for f in quiz)==21
    assert [f["source_parameter_path"] for f in quiz if not f["source_has_warp_literal"]]==["genout/quz_812_28_14"]
    assert all(f["original_warp_literal_digit_sequence"]==[] for f in quiz if not f["source_has_warp_literal"])
    assert Counter(f["original_time_literal"] for f in times)=={"ALLNOON":17,"ALLNIGHT":9,"AFTER":7}
    assert sum(f["source_HAS_CHANGE_MSG"] for f in times)==4
    assert sum(f["source_HAS_CHANGE_NO"] for f in times)==4
    assert Counter(tuple(f["original_entryitem_literal_digit_sequence"]) for f in quiz)=={(2752,1):21,(2753,1):1}
    assert Counter(f["original_answer"] for f in quiz)=={7:21,0:1}
    assert Counter(f["original_quiznum"] for f in quiz)=={5:6,1:3,2:3,3:3,7:3,10:3,100:1}
    b=d["bounds"]; assert b["all_56_source_creates_origin_class"]=="ORIGIN_UNRESOLVED"
    assert b["not_proven_permanent_quest_or_operated_event"] is True
    assert b["original_QUIZ_answer_numbers_not_played_or_validated"] is True
    assert b["npcgen_timeman_not_assumed_quest"] is True
    assert b["private_commercial_dialogue_or_images_published"] is False
    assert b["original_game_client_or_server_executed"] is False
    assert b["stage_A"]=="7_PARTIAL_2_OPEN" and b["overall_percent"] is None
    assert d["next"].startswith("QUEST_STORY_MODULE_04")
    return True

class TestQuest03(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(QUEST.read_text("utf-8"))
        cls.c=json.loads(CHAR.read_text("utf-8"))
    def test_full_source_join_and_numeric_contracts(self):self.assertTrue(verify(self.d,self.c))
    def test_unqualified_quest_promotion_rejected(self):
        d=deepcopy(self.d);d["source_creation_references"][0]["origin_class"]="BASE_GAME_QUEST"
        with self.assertRaises(AssertionError):verify(d,self.c)
    def test_fabricated_missing_quiz_warp_rejected(self):
        d=deepcopy(self.d)
        f=next(x for x in d["source_parameter_files"] if x["source_parameter_path"]=="genout/quz_812_28_14")
        f["source_has_warp_literal"]=True;f["original_warp_literal_digit_sequence"]=[812,1,1]
        with self.assertRaises(AssertionError):verify(d,self.c)
    def test_missing_original_source_file_rejected(self):
        d=deepcopy(self.d);d["source_parameter_files"].pop()
        with self.assertRaises(AssertionError):verify(d,self.c)
    def test_altered_original_sha_rejected(self):
        d=deepcopy(self.d);d["source_creation_references"][0]["original_parameter_sha256"]="0"*64
        with self.assertRaises(AssertionError):verify(d,self.c)
    def test_false_quest_runtime_claim_rejected(self):
        d=deepcopy(self.d);d["bounds"]["original_game_client_or_server_executed"]=True
        with self.assertRaises(AssertionError):verify(d,self.c)
    def test_proprietary_content_flag_rejected(self):
        d=deepcopy(self.d);d["bounds"]["private_commercial_dialogue_or_images_published"]=True
        with self.assertRaises(AssertionError):verify(d,self.c)
    def test_clock_semantics_not_inferred(self):
        d=deepcopy(self.d);d["source_parameter_files"][-1]["original_time_literal"]="OFFICIAL_HOLIDAY"
        with self.assertRaises(AssertionError):verify(d,self.c)

if __name__=="__main__":unittest.main()
