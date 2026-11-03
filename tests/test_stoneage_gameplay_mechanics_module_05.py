"""Public GAMEPLAY05 source-bound metadata checks; no proprietary source data in CI."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / "research" / "recovered"
EVIDENCE = ROOT / "STONEAGE-GAMEPLAY05-ORIGINAL-PETSHOP-SAVEPOINT-HEAL-SOURCE-R1.json"
CHAR = ROOT / "STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json"
ITEMS = [ROOT / "item-module-01" / f"STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{i:02d}-R1.json" for i in range(1, 8)]
FAMILIES = {"npcgen_petshop":16,"npcgen_savepoint":22,"npcgen_winhealer":27,
            "npcgen_healer":4,"npcgen_fmhealer":4,"npcgen_charm":4}

def verify(d,c,shards):
    assert d["schema"] == "stoneage.gameplay_mechanics_module05_preserved_pet_storage_savepoint_heal_source.r1"
    s = d["source"]; summary = d["summary"]
    assert s["scope"] == "MIXED25_COMMUNITY_PRESERVED_NPC_SOURCE_NOT_AUTHENTICATED_OFFICIAL_DEPLOYMENT"
    assert s["original_private_NPC_ZIP_sha256"] == "c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f"
    assert (s["original_NPC_ZIP_bytes"],s["private_NPC_subtree_file_count"],s["private_original_NPC_subtree_bytes"]) == (995176,2205,1930332)
    assert s["source_CHAR01_manifest_blob"] == "a088b61a3212f7049e7793f587123ffb29bebad7"
    assert s["original_parent_RAR_reopened_this_unit"] is False
    assert c["npc_subtree_source_files"] == 2205 and c["npc_subtree_source_bytes"] == 1930332
    sourcefiles = {r[0]:r for r in c["source_files"]}
    origrows = {(r[0],r[1]):r for r in c["create_rows"] if r[11] in FAMILIES}
    assert len(origrows) == 77
    receipts = {r["path"]:r for r in d["source_parameter_members"]}
    assert len(receipts) == summary["original_parameter_file_count"] == 38
    assert sum(r["source_bytes"] for r in receipts.values()) == summary["original_parameter_bytes_sum"] == 12707
    for path,receipt in receipts.items():
        f=sourcefiles[path]
        assert (receipt["source_bytes"],receipt["source_SHA256"],receipt["source_CRC32"]) == tuple(f[1:4])
        assert receipt["source_kind"] in ("npcgen_petshop","npcgen_savepoint")
    rows=d["original_CREATE_refs_and_derived_numeric_fields"]
    assert len(rows) == summary["create_refs_total"] == 77
    counter=Counter(); joined=Counter(); seen=set(); ids=set(); saveids=set(); tokens=0
    rates=Counter(); fees=Counter(); pool=0; special=0; missing=0; malformed=[]; bare=0
    healerparams=set()
    for row in rows:
        key=(row["create_path"],row["create_ordinal"])
        assert key in origrows and key not in seen
        seen.add(key);orig=origrows[key];fam=row["source_function"]
        assert fam == orig[11] and fam in FAMILIES
        assert (row["create_block_sha256"],row["floorid"],row["graphicname"]) == (orig[4],orig[5],orig[6])
        assert row["origin_class"] == "ORIGIN_UNRESOLVED"
        counter[fam] += 1
        p=row["source_parameter_path"]
        if fam in ("npcgen_petshop","npcgen_savepoint"):
            assert p is not None and p in receipts
            assert row["source_parameter_sha256"] == receipts[p]["source_SHA256"]
            assert orig[15] == [[p,"EXACT_SAME_NPC_SUBTREE_PATH",row["source_parameter_sha256"]]]
            assert receipts[p]["source_kind"] == fam
            joined[p] += 1
            f=row["source_fields"]
            if fam=="npcgen_petshop":
                assert f["original_key_is_nomal_rate_not_normal_rate"] in ("1.0","0.6","0.7")
                rates[f["original_key_is_nomal_rate_not_normal_rate"]] += 1
                if f["pool_cost_raw"] is None:
                    fees["MISSING"] += 1
                else:
                    assert f["pool_cost_raw"] in ("200","2000")
                    fees[f["pool_cost_raw"]] += 1
                if f["pool_flg_raw"] is not None:
                    assert f["pool_flg_raw"] == "1"
                    pool += 1
                if f["special_rate_raw"] is not None:
                    assert f["special_rate_raw"] == "1.5"
                    special += 1
                    assert f["special_pet_field_exists"] is True and f["special_pet_source_is_empty"] is True
                else:
                    assert f["special_pet_field_exists"] is False
            else:
                assert isinstance(f["source_save_ID_number"],int)
                saveids.add(f["source_save_ID_number"])
                assert len(f["source_Born_triplet"]) == 3
                assert all(isinstance(v,int) for v in f["source_Born_triplet"])
                assert isinstance(f["source_GetItem_field_present"],bool)
                assert f["source_GetItem_option_tokens"] >= 0
                if not f["source_GetItem_field_present"]:
                    assert f["source_GetItem_option_tokens"] == 0
                    missing += 1
                tokens += f["source_GetItem_option_tokens"]
                assert all(isinstance(i,int) and i>=0 for i in f["source_GetItem_distinct_numeric_IDs"])
                ids.update(f["source_GetItem_distinct_numeric_IDs"])
                if f["source_GetItem_malformed_component"] is not None:
                    malformed.append((p,f["source_GetItem_malformed_component"]))
                bare += bool(f["source_GetItem_bare_ID_form_without_quantities"])
        else:
            assert p is None and not orig[15]
            args=row["source_enemy_argument_tokens"]
            if fam == "npcgen_winhealer":
                assert len(args)==4
                healerparams.add(tuple(args))
            elif fam == "npcgen_charm":
                assert args == []
            else:
                assert args == ["1"]
    assert seen == set(origrows) and counter == Counter(FAMILIES)
    assert summary["family_create_counts"] == dict(sorted(counter.items()))
    assert len(joined)==38 and all(n==1 for n in joined.values())
    assert dict(rates) == summary["source_petshop_nomal_rate_literal_counts"] == {"1.0":13,"0.6":2,"0.7":1}
    assert dict(fees) == summary["source_petshop_pool_cost_literal_counts"] == {"200":5,"2000":1,"MISSING":10}
    assert pool == summary["source_petshop_pool_flag_present_count"] == 6
    assert special == summary["source_petshop_special_rate_1_5_count"] == 14
    assert len(saveids) == summary["savepoint_distinct_source_ID_count"] == 22
    assert tokens == summary["savepoint_GetItem_option_tokens"] == 209
    assert len(ids) == summary["savepoint_GetItem_distinct_numeric_item_ids"] == 116
    assert missing == summary["savepoint_GetItem_source_missing_field_count"] == 1
    assert malformed == [("genout/sp_200_449_982","1991*")]
    assert len(malformed) == summary["savepoint_GetItem_incomplete_quantity_token_count"] == 1
    assert bare == summary["savepoint_GetItem_bare_id_source_count"] == 1
    assert len(healerparams) == summary["source_winhealer_distinct_four_argument_literal_sets"] == 14
    assert summary["source_winhealer_inline_create_count"] == 27
    assert summary["source_nonwinhealer_inline_create_count"] == 12
    lookup={}
    for shard in shards:
        for row in shard["rows"]:
            assert row[0] not in lookup
            lookup[row[0]] = row
    assert len(lookup)==13915 and ids <= set(lookup)
    only_b = sorted(i for i in ids if lookup[i][1] is None and lookup[i][2] is not None)
    both = sorted(i for i in ids if lookup[i][1] is not None and lookup[i][2] is not None)
    missing_both = [i for i in ids if lookup[i][1] is None and lookup[i][2] is None]
    assert only_b == summary["only_itemset_B_source_ids"] == [1732,1733,1734,1735,1736,1737]
    assert len(only_b)==summary["savepoint_item_IDs_only_present_in_itemset_B"]==6
    assert len(both)==summary["savepoint_item_IDs_present_in_both_candidate_itemsets"]==110
    assert len(missing_both)==summary["savepoint_item_IDs_missing_both"]==0
    b=d["source_limits"]
    for name in ["native_pet_shop_pool_or_sale_transaction_executed",
        "native_savepoint_offering_consumption_or_relogin_executed",
        "native_healer_price_or_HP_MP_effect_executed",
        "official_TW10_JSS1999_CN182_source_equivalence_proven",
        "original_commercial_dialogue_or_art_in_public_git"]:
        assert b[name] is False
    for name in ["all_families_are_STATIC_CREATE_or_PARAMETER_TEXT_not_actual_native_server_callback",
        "same_archive_item_ID_presence_is_not_active_database_or_payable_item_proof",
        "original_savepoint_malformed_token_must_not_be_silently_corrected",
        "original_pet_shop_missing_fields_are_not_automatic_zero"]:
        assert b[name] is True
    assert b["stage_A"]=="7_PARTIAL_2_OPEN" and b["stage_B_and_wiki"]=="GATED"
    assert b["R79"]=="PAUSED_NON_BLOCKING" and b["overall_percent"] is None
    assert d["next"].startswith("GAMEPLAY-MECHANICS-MODULE-06")
    return True

class TestOriginalGameplay05(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(EVIDENCE.read_text("utf-8"))
        cls.char=json.loads(CHAR.read_text("utf-8"))
        cls.items=[json.loads(p.read_text("utf-8")) for p in ITEMS]
    def test_entire_original_service_source_graph(self):
        self.assertTrue(verify(self.d,self.char,self.items))
    def reject(self,edit):
        x=deepcopy(self.d);edit(x)
        with self.assertRaises((AssertionError,KeyError,TypeError)):
            verify(x,self.char,self.items)
    def test_source_create_sha_mutation_rejected(self):
        self.reject(lambda x:x["original_CREATE_refs_and_derived_numeric_fields"][0].__setitem__("create_block_sha256","0"*64))
    def test_original_parameter_sha_mutation_rejected(self):
        self.reject(lambda x:x["source_parameter_members"][0].__setitem__("source_SHA256","0"*64))
    def test_pet_shop_false_fee_rejected(self):
        self.reject(lambda x:next(r for r in x["original_CREATE_refs_and_derived_numeric_fields"] if r["source_function"]=="npcgen_petshop")["source_fields"].__setitem__("pool_cost_raw","999"))
    def test_fake_savepoint_item_rejected(self):
        self.reject(lambda x:next(r for r in x["original_CREATE_refs_and_derived_numeric_fields"] if r["source_function"]=="npcgen_savepoint")["source_fields"]["source_GetItem_distinct_numeric_IDs"].append(999999))
    def test_malformed_quantity_silently_fixed_rejected(self):
        self.reject(lambda x:next(r for r in x["original_CREATE_refs_and_derived_numeric_fields"] if r["source_parameter_path"]=="genout/sp_200_449_982")["source_fields"].__setitem__("source_GetItem_malformed_component",None))
    def test_false_pet_shop_transaction_rejected(self):
        self.reject(lambda x:x["source_limits"].__setitem__("native_pet_shop_pool_or_sale_transaction_executed",True))
    def test_false_relogin_verified_rejected(self):
        self.reject(lambda x:x["source_limits"].__setitem__("native_savepoint_offering_consumption_or_relogin_executed",True))
    def test_false_official_same_build_rejected(self):
        self.reject(lambda x:x["source_limits"].__setitem__("official_TW10_JSS1999_CN182_source_equivalence_proven",True))
if __name__=="__main__":unittest.main()
