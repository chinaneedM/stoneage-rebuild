"""QUEST06-R2 source-only directed courier hints. Public CI never opens private scripts."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/recovered/STONEAGE-QUEST06-R2-ORIGINAL-COURIER-ITEM-HINT-GRAPH-R1.json"
PRIOR = ROOT / "research/recovered/STONEAGE-QUEST06-FOUR-VILLAGE-MAMMOTH-COURIER-SOURCE-R1.json"

def verify(r, prior):
    assert r["schema"] == "stoneage.quest06.r2.original_courier_dialogue_hints_to_matching_item_conditions.source_bounded.r1"
    assert r["baseline_main_head"] == "29c652e0a6704eb65f627431ae6f4dfed0ec74a2"
    assert r["original_historical_CURRENT_blob_unchanged"] == prior["original_historical_CURRENT_blob_preserved"]
    archive = r["private_recheck"]
    assert archive["private_archive_sha256"] == prior["private_delivery"]["ZIP_sha256"]
    assert archive["private_archive_bytes"] == prior["private_delivery"]["ZIP_bytes"] == 40204
    assert archive["original_ZIP_members_crc_passed"] == prior["private_delivery"]["ZIP_entries"] == 13
    assert archive["private_original_message_text_published"] is False
    script_by_floor = {int(s["original_source_script_file"].split("worksell_")[1].split(".")[0]):s for s in prior["source_village_scripts"]}
    meta = prior["carrier"]["private_reopened_source_files"]
    for item in archive["private_CP950_source_files"]:
        f = int(item["path"].split("worksell_")[1].split(".")[0])
        assert item["sha256"] == meta["worksell_"+str(f)+".conf"]["sha256"] == script_by_floor[f]["original_source_script_sha256"]
        assert item["bytes"] == meta["worksell_"+str(f)+".conf"]["bytes"]
        assert item["zip_member_crc32"] == meta["worksell_"+str(f)+".conf"]["zip_crc32"]
    rows = r["original_source_hint_rows"]
    assert len(rows) == 8
    assert sorted((h["origin_script_floor_id"], h["source_TALKEVENT"]) for h in rows) == [(f,e) for f in sorted(script_by_floor) for e in (2,3)]
    expected_names = {(1014,2):"瑪麗娜絲村",(1014,3):"瑪麗娜絲村",(2014,2):"薩姆吉爾村",(2014,3):"薩姆吉爾村",(3014,2):"卡魯他那村",(3014,3):"卡魯他那村",(4014,2):"瑪麗娜絲村",(4014,3):"瑪麗娜絲村"}
    source_pairs = set()
    for h in rows:
        orig = h["origin_script_floor_id"]
        ev = h["source_TALKEVENT"]
        src = script_by_floor[orig]
        assert h["source_FREE_LV_literal"] == "LV<30"
        assert h["source_FREE_TRANS_literal"] == "TRANS=0"
        assert h["source_FREE_ITEM_equal"] == src["source_initial_hint_ITEM_equal_literals"][ev-2]
        assert h["source_dialogue_named_destination"] == expected_names[orig,ev]
        assert h["original_source_script_sha256"] == src["original_source_script_sha256"]
        assert h["origin_SOURCE_CREATE_floor_ids"] == src["linked_CREATE_floor_ids"]
        assert h["original_text_reopened_privately"] is True
        assert h["original_runtime_NPC_delivery_observed"] is False
        target_floor = h["candidate_recipient_script_floor_by_exact_item"]
        dest = script_by_floor[target_floor]
        assert h["candidate_recipient_SOURCE_CREATE_floor_ids"] == dest["linked_CREATE_floor_ids"]
        matches = [s for s in dest["source_quest_stages"] if s.get("source_required_ITEM") == h["source_FREE_ITEM_equal"]]
        assert len(matches) == 1
        assert matches[0]["talkevent"] == h["candidate_recipient_TALKEVENT"] in (4,5)
        assert str(h["source_FREE_ITEM_equal"]) in matches[0]["source_DelItem_literal"]
        source_pairs.add((orig,target_floor))
    assert source_pairs == {(1014,2014),(2014,1014),(3014,4014),(4014,2014)}
    graph = r["derived_candidate_script_pairs"]
    assert {(p["origin_script_floor_id"],p["candidate_recipient_script_floor_id"]) for p in graph} == source_pairs
    for p in graph:
        assert p["distinct_source_ITEM_equal"] == [h["source_FREE_ITEM_equal"] for h in rows if (h["origin_script_floor_id"],h["candidate_recipient_script_floor_by_exact_item"]) == (p["origin_script_floor_id"],p["candidate_recipient_script_floor_id"])]
    destinations = {d["candidate_recipient_script_floor_id"]:d for d in r["destination_source_dialogue_names_only"]}
    assert set(destinations) == {1014,2014,3014,4014}
    assert {f:d["incoming_hint_source_script_floors"] for f,d in destinations.items()} == {1014:[2014],2014:[1014,4014],3014:[],4014:[3014]}
    assert {f:d["source_dialogue_named_place_when_present"] for f,d in destinations.items()} == {1014:"薩姆吉爾村",2014:"瑪麗娜絲村",3014:None,4014:"卡魯他那村"}
    for f,d in destinations.items():
        assert d["source_receivable_ITEM_ids"] == [s["source_required_ITEM"] for s in script_by_floor[f]["source_quest_stages"][:2]]
    s = r["summary"]
    assert (s["original_SOURCE_TALKEVENT2_3_hint_rows"],s["origin_script_count"],s["distinct_candidate_origin_to_recipient_pairs"],s["recipient_script_count_with_inbound_hint"]) == (8,4,4,3)
    assert s["recipient_script_floor_without_inbound_hint_in_this_subset"] == [3014]
    assert s["original_item_receipt_conditions_unchanged"] is True
    assert s["stage_A"] == "7_PARTIAL_2_OPEN" and s["stage_B_wiki"] == "GATED" and s["R79"] == "PAUSED_NON_BLOCKING"
    assert s["overall_percent"] is None
    for key in ["original_item_or_pet_given_at_hint_event_proven","original_NPC_trigger_and_action_executed","original_map_route_verified","official_JSS1999_TW10_or_mainland_182_deployment_proven","official_village_geography_or_island_classification_proven","public_CI_replays_private_original_CP950_bytes"]:
        assert s[key] is False, key

class Quest06R2Hints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads(REPORT.read_text(encoding="utf-8"))
        cls.prior=json.loads(PRIOR.read_text(encoding="utf-8"))

    def test_source_graph(self):
        verify(self.report,self.prior)

    def reject(self, fn):
        r=deepcopy(self.report)
        fn(r)
        with self.assertRaises((AssertionError,KeyError,ValueError)):
            verify(r,self.prior)

    def test_reject_wrong_destination(self):
        self.reject(lambda r:r["original_source_hint_rows"][0].__setitem__("candidate_recipient_script_floor_by_exact_item",3014))

    def test_reject_wrong_item(self):
        self.reject(lambda r:r["original_source_hint_rows"][3].__setitem__("source_FREE_ITEM_equal",2622))

    def test_reject_wrong_event(self):
        self.reject(lambda r:r["original_source_hint_rows"][2].__setitem__("source_TALKEVENT",6))

    def test_reject_invented_script_name(self):
        self.reject(lambda r:r["original_source_hint_rows"][0].__setitem__("source_dialogue_named_destination","加加村"))

    def test_reject_invented_inbound_edge(self):
        self.reject(lambda r:r["destination_source_dialogue_names_only"][2].__setitem__("incoming_hint_source_script_floors",[1014]))

    def test_reject_original_runtime_claim(self):
        self.reject(lambda r:r["summary"].__setitem__("original_NPC_trigger_and_action_executed",True))

    def test_reject_old_official_build_promotion(self):
        self.reject(lambda r:r["summary"].__setitem__("official_JSS1999_TW10_or_mainland_182_deployment_proven",True))

if __name__ == "__main__":
    unittest.main()
