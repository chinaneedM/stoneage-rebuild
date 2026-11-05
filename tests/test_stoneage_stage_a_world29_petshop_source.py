"""WORLD29 source-separated original pet shop configuration vs pinned later C."""
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research" / "recovered"
D = json.loads((R / "STONEAGE-STAGE-A-WORLD29-PETSHOP-STATIC-CODE-BOUNDARY-R1.json").read_text(encoding="utf-8"))
OLD = json.loads((R / "STONEAGE-GAMEPLAY05-ORIGINAL-PETSHOP-SAVEPOINT-HEAL-SOURCE-R1.json").read_text(encoding="utf-8"))

def git_blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

def strip_comments(s):
    return re.sub(r"/\*[\s\S]*?\*/|//[^\n]*", "", s)

def function_text(s, signature, next_signature):
    a = s.index(signature)
    return s[a:s.index(next_signature, a + len(signature))]

class World29PetshopSource(unittest.TestCase):
    def test_prior_original_file_pins_unaltered(self):
        path = ROOT / D["original_configuration"]["prior_GAMEPLAY05_report_path"]
        self.assertEqual(git_blob_sha(path.read_bytes()), D["original_configuration"]["prior_GAMEPLAY05_git_blob"])
        self.assertEqual(D["original_configuration"]["selected_CREATE_refs"], 16)
        self.assertEqual(D["original_configuration"]["private_NPC_member_count"], 2205)
        self.assertFalse(D["original_configuration"]["parent_RAR_reopened"])

    def test_all_sixteen_original_create_and_parameter_joins(self):
        refs = {(x["create_path"], x["create_ordinal"]): x for x in OLD["original_CREATE_refs_and_derived_numeric_fields"] if x["source_function"] == "npcgen_petshop"}
        files = {x["path"]: x for x in OLD["source_parameter_members"] if x["source_kind"] == "npcgen_petshop"}
        rows = D["source_referenced_shop_configs"]
        self.assertEqual((len(rows), len(refs), len(files)), (16, 16, 16))
        for x in rows:
            with self.subTest(x=x["source_parameter_path"]):
                old = refs[(x["create_path"], x["create_ordinal"])]
                p = files[x["source_parameter_path"]]
                self.assertEqual(x["create_block_sha256"], old["create_block_sha256"])
                self.assertEqual(x["source_parameter_sha256"], p["source_SHA256"])
                self.assertEqual(x["source_parameter_sha256"], old["source_parameter_sha256"])
                self.assertEqual(x["floorid"], old["floorid"])
                self.assertEqual(x["nomal_rate_literal"], old["source_fields"]["original_key_is_nomal_rate_not_normal_rate"])
                self.assertEqual(x["special_rate_literal"], old["source_fields"]["special_rate_raw"])
                self.assertEqual(x["pool_cost_literal"], old["source_fields"]["pool_cost_raw"])
                self.assertEqual(x["pool_flg_literal"], old["source_fields"]["pool_flg_raw"])
                self.assertEqual(x["derived_under_pinned_c_only"]["work_normal_rate_milli"], int(float(x["nomal_rate_literal"])*1000))
                special = x["special_rate_literal"]
                self.assertEqual(x["derived_under_pinned_c_only"]["work_special_rate_milli"], int(float(special)*1000) if special is not None else 1200)
                self.assertEqual(x["derived_under_pinned_c_only"]["pool_flg"], int(x["pool_flg_literal"] == "1"))
                self.assertFalse(x["derived_under_pinned_c_only"]["configured_pool_cost_consumed_by_this_source"])

    def test_counts_do_not_promote_evidence_to_actual_transactions(self):
        rows = D["source_referenced_shop_configs"]
        self.assertEqual(Counter(x["nomal_rate_literal"] for x in rows), {"1.0":13,"0.6":2,"0.7":1})
        self.assertEqual(Counter(x["special_rate_literal"] for x in rows), {"1.5":14,None:2})
        self.assertEqual(Counter(x["pool_cost_literal"] for x in rows), {"200":5,"2000":1,None:10})
        self.assertEqual(Counter(x["pool_flg_literal"] for x in rows), {"1":6,None:10})
        self.assertTrue(all(x["special_pet_empty_if_exists"] is True for x in rows if x["special_pet_field_exists"]))
        self.assertEqual(D["summary"]["actual_historical_price_calculated"],0)
        self.assertFalse(D["evidence_boundaries"]["same_build_match_proven"])
        self.assertFalse(D["evidence_boundaries"]["original_game_or_commercial_server_executed"])

    def test_pinned_separate_community_C_actual_source(self):
        path = os.environ.get("STONEAGE_WORLD29_PINNED_C")
        if not path:
            self.skipTest("raw pinned C is checked on GitHub Actions from exact commit")
        raw = Path(path).read_bytes()
        self.assertEqual(git_blob_sha(raw), D["comparison_code"]["git_blob"])
        # The fixed 2000s-era C file is not UTF-8. Preserve each byte
        # exactly while checking the ASCII-only source tokens and branches.
        s = raw.decode("latin-1")
        code = strip_comments(s)
        self.assertIn('"nomal_rate"', code)
        self.assertIn('"special_rate"', code)
        self.assertIn("CHAR_WORK_NOMALRATE ,1000", code)
        self.assertIn("CHAR_WORK_SPECIALRATE ,1200", code)
        self.assertRegex(code, r"if\s*\(\s*tmp\s*!=\s*1\s*\)\s*tmp\s*=\s*0")
        self.assertNotRegex(code, r'GetNumFromStrWithDelim\s*\(\s*npcarg,\s*"pool_cost"')
        self.assertRegex(code, r'NPC_GETPOOLCOST\s*\(\s*talker\s*\).*?50\s*\+\s*CHAR_getInt\s*\(\s*talker\s*,\s*CHAR_LV\s*\)\s*\*\s*4')
        self.assertIn("cost = ((levelcost-getlevel)+(level*PETCOST))*rare", code)
        self.assertIn("CHAR_WORKFIXAI", code)
        self.assertIn("CHAR_WORKFIXCHARM", code)
        self.assertIn("#ifdef _NPC_DEPOTPET", code)
        self.assertIn("CHAR_setDepotPetIndex", code)
        self.assertIn("CHAR_setCharPoolPet", code)
        self.assertIn("CHAR_DelGold( talker, NPC_GETPOOLCOST( talker) )", code)
        self.assertIn("CHAR_PickAllPet", code)
        self.assertIn("CHAR_TRANSMIGRATION) > 0", code)
        self.assertIn("CHAR_LV)+5 >= CHAR_getInt( petindex, CHAR_LV", code)
        self.assertIn("CHAR_RIDEPET", code)
        sell = function_text(code, "void NPC_PetDel(int meindex, int talker,int select,char* token)\n{", "void NPC_PetDel2(")
        self.assertIn("CHAR_PETFAMILY", sell)
        self.assertIn("CHAR_RIDEPET", sell)
        self.assertLess(sell.index("CHAR_endCharOneArray( petindex );"), sell.index("cost=NPC_GetCost(meindex,talker,petindex);"))
        self.assertFalse(D["evidence_boundaries"]["source_code_order_risk_not_claimed_as_observed_crash_or_payout_bug"] is False)

    def test_stage_a_unchanged(self):
        e = D["evidence_boundaries"]
        self.assertEqual((e["stage_A"],e["stage_B"],e["R79"],e["overall_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
        self.assertEqual(git_blob_sha((ROOT/"docs/CURRENT-STATE.md").read_bytes()), D["baseline"]["old_CURRENT_blob"])

if __name__ == "__main__":
    unittest.main()
