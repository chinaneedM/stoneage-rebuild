"""QUEST06: source-limited four village mammoth courier / original item and DAT joins.

Public tests re-derive relations from pinned prior source receipts, not private
commercial full-text scripts, sprites, native runtime or historical deployment.
"""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "research/recovered/STONEAGE-QUEST06-FOUR-VILLAGE-MAMMOTH-COURIER-SOURCE-R1.json"


def git_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def load_qualified_sources(report):
    loaded = {}
    for name, pin in report["public_qualified_source_blobs"].items():
        raw = (ROOT / pin["path"]).read_bytes()
        assert git_sha(raw) == pin["sha"], "upstream source drift: " + name
        loaded[name] = json.loads(raw)
    return loaded


def verify(report, source):
    assert report["schema"] == "stoneage.quest06.four_village_mammoth_delivery_source_conditioned_item_pet_map.r1"
    assert report["baseline_main_head"] == "4885fb69ea0a2e374e5fd952d596edad725f3816"
    assert report["original_historical_CURRENT_blob_preserved"] == "c89e0e33537990aa2132b47c40fef49a985a935c"
    q = source["quest05"]
    a = source["item_shard02"]
    b = source["item_shard05"]
    original = {(x["source_CREATE_file"], x["source_CREATE_block_ordinal"]):x
       for x in q["source_CREATE_references"] if x["source_CREATE_file"] == "sa60/newbie/newbie2.create"}
    assert len(original) == 8
    assert report["carrier"]["mixed25_preserved_original_RAR_sha256"] == q["source_original_mixed25_RAR_sha256"]
    meta = report["carrier"]["private_reopened_source_files"]
    assert len(meta) == 5
    assert meta["newbie2.create"]["sha256"] == "31ef809c62f2cc208d0e5439796ee3a2e5466cda64e7561b7094248bf8a7455f"
    assert meta["newbie2.create"]["bytes"] == 1548
    assert len(report["source_CREATEs"]) == 8
    assert {x["original_CREATE_block_ordinal"] for x in report["source_CREATEs"]} == set(range(8))
    assert len({x["source_floor_id"] for x in report["source_CREATEs"]}) == 8
    for x in report["source_CREATEs"]:
        qrow = original[(x["original_CREATE_source_file"],x["original_CREATE_block_ordinal"])]
        assert x["original_CREATE_whole_file_sha256"] == qrow["source_CREATE_sha256"] == meta["newbie2.create"]["sha256"]
        assert x["source_floor_id"] == qrow["source_floor_id"]
        assert x["source_original_graphicname"] == qrow["source_graphic_alias"]
        assert x["source_original_script_pointer"] == qrow["source_parameter_file"]
        assert x["source_original_script_sha256"] == qrow["source_parameter_sha256"]
        assert x["source_DAT_sha256"] == qrow["source_DAT_sha256"]
        assert x["source_DAT_bytes"] == qrow["source_DAT_bytes"] == 5408
        assert x["original_DAT_source_grade"] == qrow["map_status"] == "MAP09_GT99_RD_SOURCE_READY_CANDIDATE"
        assert x["native_NPC_appearance_and_dialogue_executed"] is False
    expected = {
        1014:([1014,1011],[2622,4224],2623,12879,"1-13"),
        2014:([2014,2011],[2623,12879],2622,4224,"1-13"),
        3014:([3014,3011],[2624,12874],2625,4212,"1-292"),
        4014:([4014,4011],[2622,4224],2624,12874,"1-292"),
    }
    assert len(report["source_village_scripts"]) == 4
    for site in report["source_village_scripts"]:
        file = site["original_source_script_file"]
        floor = int(file.split("worksell_")[1].split(".")[0])
        pair, hints, item4, item5, pet = expected[floor]
        assert site["original_source_script_sha256"] == meta["worksell_" + str(floor) + ".conf"]["sha256"]
        assert site["original_source_TALKEVENT_count"] == 6
        assert site["original_source_NOFREE_literal_guard"] == "LV>30"
        assert site["original_source_newcomer_literal_guard_head"] == "LV<30"
        assert site["linked_CREATE_floor_ids"] == pair
        assert site["source_initial_hint_ITEM_equal_literals"] == hints
        s4,s5,s6 = site["source_quest_stages"]
        assert [s["talkevent"] for s in [s4,s5,s6]] == [4,5,6]
        assert [s["source_level_literal_range"] for s in [s4,s5,s6]] == [[1,9],[10,19],[20,29]]
        assert [s["source_alternative_conditions_count"] for s in [s4,s5,s6]] == [9,10,10]
        assert (s4["source_required_ITEM"], s4["source_DelItem_literal"]) == (item4,str(item4))
        assert (s5["source_required_ITEM"], s5["source_DelItem_literal"]) == (item5,str(item5)+"*1")
        assert s6["source_required_PET_literal"] == pet
        assert s6["source_DelPet_command_present"] is False
        assert [(s["AddGold_literal"],s["AddExps_literal"]) for s in [s4,s5,s6]] == [(1000,1000),(2000,16000),(5000,81000)]
        assert site["real_original_source_message_reopened_and_SHA_verified_privately"] is True
        assert site["runtime_delivery_completion_observed"] is False
    raw_items = {r[0]:r for r in a["rows"]+b["rows"]}
    assert len(report["source_item_identity_and_image_qualifications"]) == 8
    assert {x["numeric_item_ID"] for x in report["source_item_identity_and_image_qualifications"]} == {2622,2623,2624,2625,4212,4224,12874,12879}
    for it in report["source_item_identity_and_image_qualifications"]:
        src = raw_items[it["numeric_item_ID"]]
        assert src[1] == it["original_itemset_master_A_normalized_row_sha256"]
        assert src[2] == it["original_itemset_master_B_normalized_row_sha256"]
        assert src[3] == it["original_image_alias_in_both_original_itemsets"] == src[4]
        assert src[8] == it["source_TW10_retail_RD_candidate_qualification"]
        assert (src[1] == src[2]) == (it["source_master_A_vs_B_full_row_identity"] == "IDENTICAL")
        assert it["same_official_deployment_with_retail_TW10_verified"] is False
    idx = {x["numeric_item_ID"]:x for x in report["source_item_identity_and_image_qualifications"]}
    assert idx[4212]["original_image_alias_in_both_original_itemsets"] == idx[4224]["original_image_alias_in_both_original_itemsets"] == 20407
    assert idx[4212]["source_master_A_vs_B_full_row_identity"] == idx[4224]["source_master_A_vs_B_full_row_identity"] == "DIFFERENT"
    assert idx[2622]["source_TW10_retail_RD_candidate_qualification"] == "TW1_INDEX_NOT_FOUND"
    assert idx[2622]["cross_version_original_PNG_privately_verified_sha256"] is None
    assert sum(x["cross_version_original_PNG_privately_verified_sha256"] is not None for x in idx.values()) == 7
    assert len({x["cross_version_original_PNG_privately_verified_sha256"] for x in idx.values() if x["cross_version_original_PNG_privately_verified_sha256"]}) == 6
    s = report["summary"]
    assert s["source_original_CREATE_refs"] == 8
    assert s["source_distinct_floor_ids"] == 8
    assert s["source_village_script_count"] == 4
    assert s["source_original_talkevent_count_total"] == 24
    assert s["source_literal_reward_stage_count"] == 12
    assert s["source_distinct_item_ID_refs"] == 8
    assert s["source_first_stage_original_delivery_items"] == [2622,2623,2624,2625]
    assert s["source_second_stage_items"] == [4212,4224,12874,12879]
    assert s["source_LV30_no_explicit_FREE_OR_NOFREE_literal_branch"] is True
    assert s["source_pet_required_stage_without_DelPet_count"] == 4
    assert s["source_absent_TW10_retail_ADRN_item_image_alias_IDs"] == [2622]
    assert s["two_original_source_itemset_rows_differ_item_IDs"] == [4212,4224]
    assert s["the_two_weapon_item_IDs_share_graphic_alias"] == 20407
    floors = {x["source_floor_id"]:x for x in report["source_CREATEs"]}
    assert floors[1014]["source_DAT_sha256"] == floors[1011]["source_DAT_sha256"]
    assert s["source_CREATE_1014_and_1011_DAT_sha_equal"] is True
    assert s["source_genout_newbie2_CREATE_is_different_original_file_not_merged"] is True
    assert report["private_delivery"]["ZIP_bytes"] == 40204
    assert report["private_delivery"]["ZIP_entries"] == 13
    assert report["private_delivery"]["ZIP_sha256"] == "cd26689805ad0c40e23ef934aa7c9509fe461630dd0431f7a43740abd7c91254"
    assert report["private_delivery"]["full_library_retrieval_SHA_and_13_member_CRC_passed"] is True
    assert report["private_delivery"]["added_original_RD_decodes_this_unit"] == 0
    for key,value in report["bounds"].items():
        if key == "stage_A": assert value == "7_PARTIAL_2_OPEN"
        elif key == "stage_B_wiki": assert value == "GATED"
        elif key == "R79": assert value == "PAUSED_NON_BLOCKING"
        elif key == "overall_percent": assert value is None
        else: assert value is False, key


class Quest06SourceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(TARGET.read_text(encoding="utf-8"))
        cls.sources = load_qualified_sources(cls.report)

    def test_full_sources(self):
        verify(self.report,self.sources)

    def mutate(self,fun):
        c=deepcopy(self.report);fun(c)
        with self.assertRaises((AssertionError,KeyError,ValueError)):
            verify(c,self.sources)

    def test_reject_wrong_original_CREATE_floor(self):
        self.mutate(lambda c:c["source_CREATEs"][0].__setitem__("source_floor_id",4000))

    def test_reject_fake_same_build_image_proof(self):
        self.mutate(lambda c:c["source_item_identity_and_image_qualifications"][0].__setitem__("same_official_deployment_with_retail_TW10_verified",True))

    def test_reject_conflation_of_weapon_ids_and_alias(self):
        self.mutate(lambda c:next(i for i in c["source_item_identity_and_image_qualifications"] if i["numeric_item_ID"] == 4224).__setitem__("original_image_alias_in_both_original_itemsets",4224))

    def test_reject_artificial_pet_consumption(self):
        self.mutate(lambda c:c["source_village_scripts"][0]["source_quest_stages"][2].__setitem__("source_DelPet_command_present",True))

    def test_reject_fabricated_earliest_version(self):
        self.mutate(lambda c:c["bounds"].__setitem__("quest_origins_are_confirmed_original_2001_official_core",True))

    def test_reject_misleading_missing_TW10_image_as_absent_ever(self):
        self.mutate(lambda c:c["bounds"].__setitem__("source_item_2622_absent_from_all_later_sources",True))

    def test_reject_private_material_interpreted_as_playable(self):
        self.mutate(lambda c:c["source_village_scripts"][0].__setitem__("runtime_delivery_completion_observed",True))

    def test_reject_wrong_gold_amount(self):
        self.mutate(lambda c:c["source_village_scripts"][1]["source_quest_stages"][0].__setitem__("AddGold_literal",9000))


if __name__ == "__main__":
    unittest.main()
