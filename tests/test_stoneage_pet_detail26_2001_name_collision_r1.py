"""PET-DETAIL26: separate two original TW1 thunder records from conflicting 2001 player labels."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E="research/pets/PET-DETAIL-EVIDENCE26-2001-LV1-DINO-THUNDER-ALIAS-CONFLICT-R1.json"
def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def gitblob(path):
    data=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode("ascii")+b"\0"+data).hexdigest()
class EarlyPCLevelOneNames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=read(E)
        cls.tw=read("research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
        cls.o92=read("research/recovered/STONEAGE-O92-EARLY-PET-ACQUISITION-CENSUS-R1.json")
        cls.old=read("research/pets/PET-DETAIL-EVIDENCE07-CN2001-LEVEL1-20-NUMERIC-SOURCE-CLAIMS-R1.json")
        cls.profiles={no:read(f"research/pets/profiles/TW10-G{no}.json") for no in (100351,100353,100371)}
    def test_source_pins_and_web_release_not_original_game_packet(self):
        r=self.e["player_sources"]
        self.assertEqual(r["tw10"]["git_blob"],gitblob(r["tw10"]["path"]))
        self.assertEqual(r["yibobo"]["previous_git_blob"],gitblob(r["yibobo"]["previously_reviewed_in"]))
        self.assertEqual(r["earlier_milk"]["previous_git_blob"],gitblob(r["earlier_milk"]["previously_archived_path"]))
        self.assertEqual(r["yibobo"]["url"],self.o92["source"]["url"])
        self.assertTrue(r["kuaiji"]["page_text_reused_from_pet25"])
        self.assertFalse(r["kuaiji"]["original_2001_html_bytes_verified"])
        self.assertFalse(r["yibobo"]["official_operator_misprint_document_verified"])
        self.assertEqual(self.e["history_baseline"]["current_state_blob_sha"],"c89e0e33537990aa2132b47c40fef49a985a935c")
    def test_three_distinct_original_retail_name_rows_and_spr_segments(self):
        rows=self.e["original_tw10_three_distinct_client_entries"]
        self.assertEqual({x["graphic_number"] for x in rows},{100351,100353,100371})
        self.assertEqual({x["spr_group"] for x in rows},{321,323,337})
        for x in rows:
            rec=next(y for y in self.tw["records"] if y["graphic_number"]==x["graphic_number"])
            p=self.profiles[x["graphic_number"]]
            self.assertEqual(rec["name_as_written"],x["original"])
            self.assertEqual(rec["source_row_sha256"],x["source_row_sha256"])
            self.assertEqual(rec["source_file_offset"],x["source_row_offset"])
            self.assertEqual(rec["spr_original_segment_sha256"],x["spr_segment_sha256"])
            self.assertEqual(rec["spr_group_index"],x["spr_group"])
            self.assertEqual(p["profile_id"],x["profile_id"])
            self.assertEqual(p["historical_player_guide_evidence"]["source_evidence_git_blob"],gitblob(E))
            self.assertEqual(sum(s["path"]==E for s in p["provenance"]["sources"]),1)
    def test_two_player_ranges_are_bounded_player_only(self):
        a,b=self.e["kuaiji_claimed_level_one_records"]
        self.assertEqual((a["matched_dossier"],b["matched_dossier"]),("PET-000098","PET-000082"))
        for record,lo,hi in ((a,[47,8,8,5],[53,10,10,6]),(b,[53,9,8,0],[58,11,10,2])):
            self.assertEqual([record[k]["min"] for k in ("hp","attack","defense","agility")],lo)
            self.assertEqual([record[k]["max"] for k in ("hp","attack","defense","agility")],hi)
            self.assertFalse(record["claimed_location"]["server_spawn_table_verified"])
            self.assertFalse(record["capture_rule_verified"])
            self.assertFalse(record["earlier_milk_nickname_crosscheck"]["same_original_species_id_or_server_proven"])
        self.assertEqual(a["claimed_elements"],{"earth":6,"water":4})
        self.assertEqual(b["claimed_elements"],{"fire":8,"water":2})
        ids={x["obs_id"] for x in self.old["records"]}
        self.assertIn("OBS-CN2001-MILK-LV1-0003",ids)
        self.assertIn("OBS-CN2001-MILK-LV1-0004",ids)
    def test_conflicting_red_thunder_alias_not_a_single_pet(self):
        d=self.e["yibobo_thunder_source_specific_contradiction"]
        self.assertEqual(d["list_row_90"]["literal"],"布洛多斯")
        self.assertEqual(d["list_row_92"]["literal"],"布拉奇多斯")
        self.assertEqual(d["original_client_two_graphic_numbers"],[100351,100353])
        self.assertEqual(d["original_client_two_spr_groups"],[321,323])
        self.assertFalse(d["operator_typo_claim_independently_officially_verified"])
        self.assertFalse(d["same_pet_identity_or_original_race_equivalence_proven"])
        self.assertTrue(d["source_list_ordinals_not_official_pet_ids"])
        self.assertEqual(d["resolution"],"CONFLICT_UNRESOLVED_NO_AUTOMATIC_MERGE_OR_STAT_TRANSFER")
        self.assertEqual(self.profiles[100351]["historical_player_guide_evidence"]["source_claim_kind"],"DIRECT_LITERAL_WITH_RIVAL_CLIENT_PET_IDENTITY_CLAIM")
        self.assertEqual(self.profiles[100353]["historical_player_guide_evidence"]["source_claim_kind"],"ALTERNATE_AUTHENTIC_TW10_NAME_RAISED_BY_SECOND_PLAYER_GUIDE_NOT_IDENTITY_PROOF")
    def test_true_official_stats_growth_skills_encounters_stay_null(self):
        self.assertTrue(all(x is None for x in self.e["field_safety"].values()))
        for p in self.profiles.values():
            self.assertEqual(p["profile_stage"],"PARTIAL_EVIDENCE_PROFILE")
            self.assertEqual(p["combat_stats"]["status"],"OPEN_NOT_PROVEN")
            self.assertTrue(all(x is None for x in p["combat_stats"]["level_1"]["values"].values()))
            for kind in ("minimum","maximum"):
                self.assertTrue(all(x is None for x in p["combat_stats"]["initial_stat_ranges"][kind].values()))
            self.assertTrue(all(x is None for x in p["combat_stats"]["elements"].values()))
            for key in ("growth","skills","acquisition"):
                self.assertEqual(p[key]["status"],"OPEN_NOT_PROVEN")
            self.assertFalse(p["actual_official_pet_identity"]["official_living_pet_release_proven"])
        guard=self.e["scope_guard"]
        self.assertEqual([guard[k] for k in ("tw10_named_client_candidates","tw10_pet_dossiers_partial","tw10_all_fields_historically_complete","new_official_live_species_this_unit")],[124,124,0,0])
        self.assertEqual(guard["only_module"],"PET")
        self.assertIsNone(guard["overall_completion_percent"])
        for path in ("README.md","docs/pets/INDEX.md","docs/pets/TW10-G100351.md","docs/pets/TW10-G100353.md","docs/pets/TW10-G100371.md"):
            self.assertIn("PET-DETAIL26",(ROOT/path).read_text(encoding="utf-8"))
if __name__=="__main__":
    unittest.main()
