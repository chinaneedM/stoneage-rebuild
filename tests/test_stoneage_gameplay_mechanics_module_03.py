"""Original GAMEPLAY03 source-derived data checks, without proprietary game assets."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
import unittest

BASE=Path(__file__).resolve().parents[1]/"research"/"recovered"
NEW=BASE/"STONEAGE-GAMEPLAY03-ORIGINAL-21-PET-SKILL-SHOP-SOURCE-R1.json"
CHAR=BASE/"STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json"
PET=BASE/"STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json"

def verify(d,c,p):
    assert d["schema"]=="stoneage.gameplay_mechanics_module03_21_original_petskillshop_source.r1"
    source=d["source"]
    assert source["scope"]=="MIXED25_COMMUNITY_PRESERVED_NPC_SOURCE_NOT_EARLY_OFFICIAL"
    assert source["replayed_all_2205_NPC_source_files_SHA_CRC"] is True
    assert source["replayed_original_NPC_bytes"]==1930332
    assert source["upstream_CHAR01_blob"]=="a088b61a3212f7049e7793f587123ffb29bebad7"
    assert source["PET10_verified_server_table_blob"]=="25a37aeb134fb180e322e7dc335029b7374452d8"
    assert source["original_parent_RAR_reread_this_unit"] is False
    assert source["original_parent_RAR_sha256"]==p["preserved_original_rar"]["sha256"]
    refs=[a for a in c["create_rows"] if a[11]=="npcgen_petskillshop"]
    ref={(a[0],a[1]):a for a in refs}
    files={f[0]:f for f in c["source_files"]}
    rows=d["original_skillshop_CREATE_to_parameter_rows"]
    assert len(refs)==len(rows)==21
    seen=set(); skillcount=Counter();rates=Counter()
    for r in rows:
        k=(r["create_file"],r["create_ordinal"])
        assert k not in seen and k in ref
        seen.add(k);orig=ref[k]
        assert r["source_function_token"]==orig[11]=="npcgen_petskillshop"
        assert r["create_block_sha256"]==orig[4]
        assert r["source_floorid"]==orig[5] and r["source_graphicnum"]==orig[6]
        path=r["parameter_path"]
        assert orig[15]==[[path,"EXACT_SAME_NPC_SUBTREE_PATH",r["source_original_sha256"]]]
        assert (r["source_original_bytes"],r["source_original_sha256"],r["source_original_crc32"])==tuple(files[path][1:4])
        assert r["source_skill_rate_literal"] in ("1.0","1.1","1.2")
        assert all(isinstance(n,int) and n>=0 for n in r["source_pet_skill_ids_ordered"])
        assert len(set(r["source_pet_skill_ids_ordered"]))==len(r["source_pet_skill_ids_ordered"])
        assert r["source_pet_skill_trailing_empty_token"]==(path=="genout/psks_5103_11_10")
        rates[r["source_skill_rate_literal"]]+=1
        skillcount.update(r["source_pet_skill_ids_ordered"])
    assert seen==set(ref)
    s=d["summary"]
    assert s["original_create_references"]==s["exact_source_parameter_members"]==21
    assert s["original_parameter_bytes_total"]==sum(r["source_original_bytes"] for r in rows)==2117
    assert dict(rates)==s["original_skill_rate_literal_counts"]=={"1.2":7,"1.0":11,"1.1":3}
    assert sum(skillcount.values())==s["original_pet_skill_ID_occurrences"]==150
    assert len(skillcount)==s["distinct_skill_IDs"]==23
    assert s["unique_skill_IDs_present_in_both_potential_master_tables"]==23
    assert s["source_current_deployed_active_master_choice_proven"] is False
    a={x[1]:x for x in p["source_rows"]["petskill.txt"]}
    b={x[1]:x for x in p["source_rows"]["petskill1.txt"]}
    joined=d["source_skill_id_master_presence_candidates"]
    assert len(joined)==23 and [j["skill_id"] for j in joined]==sorted(skillcount)
    for j in joined:
        i=j["skill_id"];assert i in a and i in b
        assert j["primary_petskill_txt"]=={"source_line":a[i][0],"row_sha256":a[i][2]}
        assert j["alternative_petskill1_txt"]=={"source_line":b[i][0],"row_sha256":b[i][2]}
    limits=d["source_bounds"]
    assert limits["source_skill_rate_price_multiplier_runtime_proven"] is False
    assert limits["source_pet_skill_field_defines_actual_learnable_skill_runtime_proven"] is False
    assert limits["original_game_shop_operation_executed"] is False
    assert limits["primary_or_alternative_master_actually_deployed_proven"] is False
    assert limits["same_archive_numeric_id_is_not_runtime_foreign_key_confirmation"] is True
    assert limits["official_TW10_CN182_JSS1999_equivalence_proven"] is False
    assert limits["proprietary_original_skill_names_or_text_or_assets_published"] is False
    assert limits["stage_A"]=="7_PARTIAL_2_OPEN" and limits["overall_percent"] is None
    assert d["next"].startswith("GAMEPLAY-MECHANICS-MODULE-04")
    return True

class TestOriginalGameplay03(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(NEW.read_text("utf-8"))
        cls.c=json.loads(CHAR.read_text("utf-8"))
        cls.p=json.loads(PET.read_text("utf-8"))
    def test_21_original_source_links_and_23_skill_ids(self):
        self.assertTrue(verify(self.d,self.c,self.p))
    def reject(self,action):
        x=deepcopy(self.d);action(x)
        with self.assertRaises((AssertionError,KeyError,TypeError)):
            verify(x,self.c,self.p)
    def test_false_skill_id_rejected(self):
        self.reject(lambda x:x["original_skillshop_CREATE_to_parameter_rows"][0]["source_pet_skill_ids_ordered"].append(999999))
    def test_false_source_SHA_rejected(self):
        self.reject(lambda x:x["original_skillshop_CREATE_to_parameter_rows"][0].__setitem__("source_original_sha256","0"*64))
    def test_false_master_line_rejected(self):
        self.reject(lambda x:x["source_skill_id_master_presence_candidates"][0]["primary_petskill_txt"].__setitem__("source_line",999999))
    def test_false_skill_rate_rejected(self):
        self.reject(lambda x:x["original_skillshop_CREATE_to_parameter_rows"][0].__setitem__("source_skill_rate_literal","9.9"))
    def test_false_live_shop_rejected(self):
        self.reject(lambda x:x["source_bounds"].__setitem__("original_game_shop_operation_executed",True))
    def test_false_early_official_source_rejected(self):
        self.reject(lambda x:x["source_bounds"].__setitem__("official_TW10_CN182_JSS1999_equivalence_proven",True))
if __name__=="__main__":
    unittest.main()
