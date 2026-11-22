"""Source-only 2001–2003 classic PC thunder naming and attributed player growth."""
import hashlib
import json
import unittest
from collections import Counter
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = "research/pets/PET-DETAIL-EVIDENCE27-2001-2003-THUNDER-DUAL-NAMES-PLAYER-GROWTH-R1.json"


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def git_blob(path):
    content = (ROOT / path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()


class PCThunderNamedPlayerEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e = load(E)
        cls.tw = load("research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
        cls.previous = load("research/pets/PET-DETAIL-EVIDENCE26-2001-LV1-DINO-THUNDER-ALIAS-CONFLICT-R1.json")
        cls.p = {
            100351: load("research/pets/profiles/TW10-G100351.json"),
            100353: load("research/pets/profiles/TW10-G100353.json"),
        }

    def test_source_pins_dates_and_editorial_grade(self):
        e = self.e
        self.assertEqual(e["client_provenance"]["git_blob"], git_blob(e["client_provenance"]["path"]))
        self.assertEqual(e["previous_detail26"]["git_blob"], git_blob(e["previous_detail26"]["path"]))
        self.assertEqual(e["previous_o92"]["git_blob"], git_blob(e["previous_o92"]["path"]))
        self.assertEqual(e["historical_current_blob"], "c89e0e33537990aa2132b47c40fef49a985a935c")
        s = e["sources"]
        self.assertEqual([x["id"] for x in s], ["kuaiji01", "yibobo01", "pk01", "xue02", "zhang02", "sina03", "xiaofeng03"])
        self.assertEqual([x["page_date"][:4] for x in s], ["2001"]*3 + ["2002"]*2 + ["2003"]*2)
        self.assertTrue(all(not x["original_published_html_bytes_sha_authenticated"] for x in s))
        self.assertTrue(all(x["url"].startswith("https://") for x in s))
        self.assertTrue(e["specific_sources"]["kuaiji2001"]["same_article_internal_contradiction"])
        self.assertFalse(e["specific_sources"]["pk2001"]["can_count_independent_numeric_sample"])
        self.assertFalse(e["specific_sources"]["sina2003"]["site_numbers_are_original_server_pet_id"])

    def test_two_client_entries_never_merged(self):
        records = self.e["original_tw10_distinct_compiled_records"]
        self.assertEqual([(x["pet_id"], x["graphic"], x["group"]) for x in records],
                         [("PET-000082", 100351, 321), ("PET-000084", 100353, 323)])
        self.assertEqual([x["sina_site_number"] for x in records], [161, 163])
        for x in records:
            q = next(row for row in self.tw["records"] if row["graphic_number"] == x["graphic"])
            self.assertEqual(q["name_as_written"], x["local"])
            self.assertEqual(q["spr_group_index"], x["group"])
            self.assertEqual(q["source_row_sha256"], x["row_sha"])
            self.assertEqual(q["spr_original_segment_sha256"], x["segment_sha"])
            p = self.p[x["graphic"]]
            self.assertEqual(p["profile_id"], x["pet_id"])
            self.assertEqual(p["names"]["original_client"], x["local"])
            h = p["historical_player_nickname_and_growth_evidence"]
            self.assertEqual(h["detail_evidence_blob"], git_blob(E))
            self.assertEqual(h["player_color_nickname"], x["nickname"])
            self.assertFalse(h["identity_same_deployment_as_tw10_official_source_proven"])
            self.assertTrue(h["earlier_2001_kuaiji_body_name_conflict_still_recorded"])
            self.assertEqual(sum(s["path"] == E for s in p["provenance"]["sources"]), 1)
        mapping = self.e["player_nickname_crosswalk"]
        self.assertFalse(mapping["official_species_identity_proven"])
        self.assertFalse(mapping["primary_operator_typo_notice_verified"])
        self.assertTrue(mapping["do_not_merge_tw10_clients"])

    def test_2002_ranges_are_player_estimates_not_2001_official_bounds(self):
        rows = self.e["zhang_2002_player_lv1_ranges"]
        self.assertEqual([x["pet_id"] for x in rows], ["PET-000082", "PET-000084"])
        self.assertEqual(rows[0]["stats"], {"hp": [53,63], "attack": [8,12], "defense": [9,12], "agility": [1,3]})
        self.assertEqual(rows[1]["stats"], {"hp": [49,60], "attack": [8,13], "defense": [8,12], "agility": [1,4]})
        self.assertEqual(rows[0]["player_reported_upper_growth"]["defense"], "2.17")
        self.assertEqual(rows[1]["player_reported_upper_growth"]["attack"], "2.3")
        self.assertFalse(self.e["specific_sources"]["zhang2002"]["native_riding_in_2001_proven"])
        for row in rows:
            self.assertTrue(all(x[0] <= x[1] for x in row["stats"].values()))
            profile = next(p for p in self.p.values() if p["profile_id"] == row["pet_id"])
            self.assertEqual(profile["historical_player_nickname_and_growth_evidence"]["player_2002_level_one_estimates"], row["stats"])

    def test_2003_genuine_five_attributed_text_records_keep_rebirth_separate(self):
        rows = self.e["xiaofeng_2003_reported_samples"]
        self.assertEqual(len(rows), 5)
        self.assertEqual(Counter(x["source_section"] for x in rows), {"未转宠": 2, "转宠": 3})
        self.assertEqual(Counter(x["pet_id"] for x in rows), {"PET-000082":3, "PET-000084":2})
        self.assertEqual(
            [(x["pet_id"], x["source_section"], x["three_stat_growth_literal"], x["hp_growth_literal"], x["credited_player"]) for x in rows],
            [
                ("PET-000082", "未转宠", "4.556", "11.548", "fjyoo3"),
                ("PET-000084", "未转宠", "4.6652", "11.1596", "wewe"),
                ("PET-000084", "转宠", "5.7265", "13.0431", "流泪の手心"),
                ("PET-000082", "转宠", "5.6451", "12.9113", "÷灵☆光÷"),
                ("PET-000082", "转宠", "5.3739", "13.4676", "fjyoo3"),
            ],
        )
        for x in rows:
            self.assertTrue(Decimal(x["three_stat_growth_literal"]) > 0)
            self.assertTrue(Decimal(x["hp_growth_literal"]) > 0)
            self.assertFalse(x["raw_same_pet_level_records_verified"])
            self.assertFalse(x["original_growth_formula_qualified"])
        for n, p in self.p.items():
            self.assertEqual(p["historical_player_nickname_and_growth_evidence"]["player_2003_reported_growth_sample_count"], 3 if n == 100351 else 2)

    def test_official_stats_skills_spawns_and_early_release_not_promoted(self):
        self.assertTrue(all(self.e["evidence_limits"].values()))
        self.assertTrue(all(val is None for val in self.e["explicitly_unresolved_official"].values()) if "explicitly_unresolved_official" in self.e else True)
        for p in self.p.values():
            self.assertEqual(p["profile_stage"], "PARTIAL_EVIDENCE_PROFILE")
            self.assertFalse(p["actual_official_pet_identity"]["official_living_pet_release_proven"])
            self.assertEqual(p["combat_stats"]["status"], "OPEN_NOT_PROVEN")
            self.assertTrue(all(v is None for v in p["combat_stats"]["level_1"]["values"].values()))
            for bound in ("minimum","maximum"):
                self.assertTrue(all(v is None for v in p["combat_stats"]["initial_stat_ranges"][bound].values()))
            self.assertTrue(all(v is None for v in p["combat_stats"]["elements"].values()))
            for field in ("growth","skills","acquisition"):
                self.assertEqual(p[field]["status"], "OPEN_NOT_PROVEN")
            self.assertTrue(p["historical_player_guide_evidence"]["exact_official_pet_identity_resolution"] == "UNRESOLVED")
        state = self.e["overall"]
        self.assertTrue(state["pc_only"] and state["pet_only"] and state["mobile_content_excluded"])
        self.assertEqual((state["tw10_named_candidates"],state["tw10_partial_dossiers"],state["tw10_historically_complete"],state["new_official_live_species_this_unit"]),(124,124,0,0))
        self.assertIsNone(state["percent"])
        for path in ("docs/pets/INDEX.md", "README.md", "docs/pets/TW10-G100351.md", "docs/pets/TW10-G100353.md"):
            self.assertIn("PET-DETAIL27",(ROOT/path).read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
