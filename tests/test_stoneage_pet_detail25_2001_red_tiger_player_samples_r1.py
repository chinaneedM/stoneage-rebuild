"""PET-DETAIL25: two distinct 2001 player red tigers; no official Taiwan 1.0 stat backfill."""
import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
EP = "research/pets/PET-DETAIL-EVIDENCE25-2001-RED-TIGER-TWO-LV1-LV80-PLAYER-WITNESSES-R1.json"
PP = "research/pets/profiles/TW10-G100329.json"
def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))
def gitsha(path):
    raw = (ROOT / path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
class OriginalPC2001RedTigerPlayerSamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e = read(EP); cls.p = read(PP)
        cls.tw = read("research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
        cls.older = read("research/pets/PET-DETAIL-EVIDENCE07-CN2001-LEVEL1-20-NUMERIC-SOURCE-CLAIMS-R1.json")
    def test_exact_source_links_and_pins(self):
        self.assertEqual(gitsha(EP), self.p["historical_player_measurement_evidence"]["source_evidence_git_blob"])
        self.assertEqual(self.e["original_client_identity_crosswalk"]["source_git_blob"], gitsha("research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json"))
        self.assertEqual(self.e["independent_earlier_player_text_relation"]["source_git_blob"], gitsha("research/pets/PET-DETAIL-EVIDENCE07-CN2001-LEVEL1-20-NUMERIC-SOURCE-CLAIMS-R1.json"))
        self.assertEqual([x["path"] for x in self.p["provenance"]["sources"]].count(EP),1)
        self.assertEqual(self.e["coverage_guard"]["original_current_state_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(self.e["baseline_main_sha"],"e9192f4b6eaf40798a4a73884bc0fb89a0d357ba")
    def test_qualified_original_client_name_not_live_pet_id(self):
        r = self.e["original_client_identity_crosswalk"]
        source = next(x for x in self.tw["records"] if x["graphic_number"]==100329)
        self.assertEqual((self.p["profile_id"],r["profile_id"]),("PET-000064","PET-000064"))
        self.assertEqual((source["name_as_written"],r["compiled_original_name"]),("格魯西斯","格魯西斯"))
        self.assertEqual(source["source_row_sha256"],r["compiled_name_row_sha256"])
        self.assertEqual(source["source_file_offset"],r["compiled_name_row_offset"])
        self.assertEqual(source["spr_original_segment_sha256"],r["full_spr_sha256"])
        self.assertFalse(r["same_2001_player_server_as_tw10_retail_verified"])
        self.assertFalse(self.p["actual_official_pet_identity"]["official_living_pet_release_proven"])
    def test_two_individuals_only_and_firsthand_claimed_values(self):
        animals=self.e["fengxin_individual_player_claims"]
        self.assertEqual([x["individual_id"] for x in animals],["FENGXIN_RED_TIGER_A","FENGXIN_RED_TIGER_B"])
        self.assertEqual([len(x["reported_panels"]) for x in animals],[1,2])
        self.assertEqual([x["level"] for x in animals[0]["reported_panels"]],[1])
        self.assertEqual([x["level"] for x in animals[1]["reported_panels"]],[1,80])
        self.assertEqual(animals[0]["reported_panels"][0],dict(level=1,hp=32,attack=8,defense=5,agility=7))
        self.assertEqual(animals[1]["reported_panels"][0],dict(level=1,hp=37,attack=8,defense=5,agility=6))
        self.assertEqual(animals[1]["reported_panels"][1],dict(level=80,hp=771,attack=170,defense=98,agility=139))
        self.assertTrue(self.e["evidence_verification"]["level80_other_tiger_is_not_third_animal"])
        self.assertEqual(self.p["historical_player_measurement_evidence"]["reported_red_tiger_individuals"],2)
    def test_exact_two_endpoint_arithmetic_only(self):
        animals=self.e["fengxin_individual_player_claims"]
        beg,end=animals[1]["reported_panels"]
        avg=self.e["fengxin_second_pet_arithmetic"]
        self.assertEqual(avg["level_gaps"],79)
        for k in ("hp","attack","defense","agility"):
            diff=end[k]-beg[k]
            self.assertEqual(avg["derived_differences"][k],diff)
            f=avg["mean_per_level_exact_rationals"][k]
            self.assertEqual(Fraction(f["numerator"],f["denominator"]),Fraction(diff,79))
        self.assertIn("NOT_SERVER_GROWTH_ALGORITHM",avg["type"])
    def test_player_ranges_separate_from_server_config(self):
        q=self.e["kuaiji_claimed_common_level1_ranges"]
        for a in self.e["fengxin_individual_player_claims"]:
            r=a["reported_panels"][0]
            for k in ("hp","attack","defense","agility"):
                self.assertLessEqual(q[k]["min"],r[k])
                self.assertLessEqual(r[k],q[k]["max"])
        older=next(x for x in self.older["records"] if x["obs_id"]=="OBS-CN2001-MILK-LV1-0018")
        self.assertEqual(self.e["independent_earlier_player_text_relation"]["four_unlabeled_slots"],older["numeric_slots_bounds_without_stat_labels"])
        self.assertFalse(self.e["independent_earlier_player_text_relation"]["stat_slot_names_authenticated"])
        self.assertFalse(q["claim_officially_verified"])
        for rec in self.e["source_records"]:
            self.assertFalse(rec["historical_original_html_sha_authenticated"])
    def test_official_fields_are_unchanged_null_and_modules_locked(self):
        p=self.p; e=self.e
        self.assertEqual(p["profile_stage"],"PARTIAL_EVIDENCE_PROFILE")
        self.assertFalse(p["combat_stats"]["verified_version_specific_server_master"])
        self.assertEqual(p["combat_stats"]["status"],"OPEN_NOT_PROVEN")
        self.assertTrue(all(v is None for v in p["combat_stats"]["level_1"]["values"].values()))
        for side in ("minimum","maximum"):
            self.assertTrue(all(v is None for v in p["combat_stats"]["initial_stat_ranges"][side].values()))
        self.assertTrue(all(v is None for v in p["combat_stats"]["elements"].values()))
        for k in ("growth","skills","acquisition"):
            self.assertEqual(p[k]["status"],"OPEN_NOT_PROVEN")
        self.assertTrue(all(v is None for v in e["official_game_fields_preserved_unknown"].values()))
        g=e["coverage_guard"]
        self.assertEqual((g["original_client_named_profiles"],g["fully_verified_official_profiles"],g["added_official_live_species"]),(124,0,0))
        self.assertEqual(g["only_active_module"],"PET")
        self.assertIsNone(g["overall_completion_percent"])
        self.assertIn("PET-DETAIL25",(ROOT/"docs/pets/TW10-G100329.md").read_text(encoding="utf-8"))
        self.assertIn("PET-DETAIL25",(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8"))
        self.assertIn("PET-DETAIL25",(ROOT/"README.md").read_text(encoding="utf-8"))
if __name__=="__main__":
    unittest.main()
