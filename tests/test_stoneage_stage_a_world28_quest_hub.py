"""WORLD28 public custody and cross-module historical-source limits."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research" / "recovered"
D = json.loads((R / "STONEAGE-STAGE-A-WORLD28-UNIFIED-QUEST-HUB-R1.json").read_text(encoding="utf-8"))

def load(filename):
    return json.loads((R / filename).read_text(encoding="utf-8"))

def blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

class World28OriginalQuestHub(unittest.TestCase):
    def test_seven_existing_public_sources_are_byte_qualified(self):
        rows = D["original_source_readers"]
        self.assertEqual([x["id"] for x in rows], ["QUEST01","QUEST02","WORLD14","WORLD21","WORLD22","WORLD23","WORLD27"])
        for row in rows:
            with self.subTest(source=row["id"]):
                p = ROOT / row["public_path"]
                self.assertTrue(p.is_file())
                self.assertEqual(blob_sha(p.read_bytes()), row["public_git_blob"])
                self.assertEqual(len(row["private_source_zip_sha256"]), 64)
                self.assertEqual(len(row["private_reader_html_sha256"]), 64)
                self.assertTrue(row["private_reader_relative_path"].startswith("readers/"))
                self.assertEqual(row["origin_class"], "ORIGIN_UNRESOLVED")
                self.assertFalse(row["original_game_execution_verified"])

    def test_actual_prior_batch_counts_and_unnormalized_source_are_preserved(self):
        f = load("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-14-ORIGINAL-FISHING-QUEST-SOURCE-REPLAY-R1.json")["counts"]
        self.assertEqual((f["maker_branch_count"], f["fisherman_accept_branch_count"], f["fisherman_message_branch_count"]), (9,3,1))
        x = load("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-21-GETPET-QUEST-BRANCHES-R1.json")["counts"]
        self.assertEqual((x["original_GetPet_directive_lines"],x["distinct_GetPet_enemy_master_ids"], x["GetPet_enemy_IDs_also_in_selected_WORLD20_wild_subgraph"]), (29,36,0))
        z = load("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-22-QUEST-CURRENCY-SOURCE-R1.json")["counts"]
        self.assertEqual(z["directive_counts"], {"DelStone":16,"GetStone":99})
        y = load("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-23-NPC-ITEM-TRANSFERS-R1.json")["counts"]
        self.assertEqual((y["source_files"],y["operations"],y["operations_by_field"]), (410,1246,{"DelItem":659,"GetItem":532,"GetRandItem":55}))
        w = load("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-27-PET-HANDOVER-QUEST-BRANCHES-R1.json")["counts"]
        self.assertEqual((w["source_files"],w["DelPet_physical_fields"],w["source_CREATE_refs"],w["DelPet_comma_lexeme_classes"]["UNEXPANDED_EVDEL_MARKER"]), (17,97,15,7))
        self.assertTrue(D["counts_not_quest_population"])

    def test_four_source_origin_classes_do_not_promote_later_mixed_archive(self):
        self.assertEqual(D["policy_classes"], ["BASE_GAME_QUEST","PERMANENT_VERSION_QUEST","OPERATOR_EVENT_QUEST","ORIGIN_UNRESOLVED"])
        self.assertEqual(len(D["independent_operator_event_archive"]),5)
        self.assertTrue(D["operator_event_is_distinct_from_same_deployment_script"])
        origin = load("STONEAGE-QUEST-ORIGIN-SEPARATION-R1.json")
        indexed = {x["id"] for x in origin["records"] if x["origin"]=="OPERATOR_EVENT_QUEST"}
        self.assertEqual(indexed & {x["id"] for x in D["independent_operator_event_archive"]}, {"R110","R111","R112","R115"})
        for event in D["independent_operator_event_archive"]:
            self.assertEqual(event["origin_class"],"OPERATOR_EVENT_QUEST")
            self.assertFalse(event["original_server_execution_verified"])
            self.assertTrue((ROOT / event["source"]).is_file())
        self.assertEqual(D["original_script_origin_classification"],"ORIGIN_UNRESOLVED_NOT_OFFICIAL_BASE")

    def test_links_are_bounded_and_origin_file_stays_intact(self):
        links = {x["id"]:x for x in D["cross_module_links"]}
        self.assertEqual(links["FISHING_ROD_TO_PET_GRANT_CONDITION"]["item_id"],2432)
        self.assertIn("GetPet=333",links["FISHING_ROD_TO_PET_GRANT_CONDITION"]["to"])
        self.assertIn("PET=33-721*1",links["PET_HANDOVER_REWARD_NAMESPACE"]["from"])
        self.assertTrue(all(x["game_execution_verified"] is False for x in links.values()))
        self.assertEqual(blob_sha((ROOT/"docs/CURRENT-STATE.md").read_bytes()), D["baseline"]["current_state_git_blob"])
        self.assertTrue(D["unchanged_old_reports"])
        self.assertIsNone(D["stage_a"]["overall_percent"])

    def test_delivery_is_private_not_claimed_as_native_play_or_library_durable(self):
        p = D["private_delivery"]
        self.assertEqual((p["readers_count"],p["event_archive_cards"],p["index_cards"],p["member_count"]), (7,5,12,10))
        self.assertFalse(p["private_original_text_in_public_repo"])
        self.assertFalse(p["library_uploaded_and_reread_verified"])
        self.assertFalse(D["browser_verification"]["file_url_direct_navigation_tested"])
        self.assertFalse(D["browser_verification"]["native_game_executed"])
        self.assertEqual(D["stage_a"]["savedata_R79"],"PAUSED_NON_BLOCKING")

if __name__ == "__main__":
    unittest.main()
