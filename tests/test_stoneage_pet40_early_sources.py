"""Protect the source grades of the early Taiwanese and Japanese pet evidence."""

import json
import unittest
from pathlib import Path

from tools.stoneage_pet27_chronology import choose, load

ROOT = Path(__file__).resolve().parents[1]
RECOVERED = ROOT / "research" / "recovered"


def read(name):
    return json.loads((RECOVERED / name).read_text(encoding="utf-8"))


class EarlyPetSourcesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = read("STONEAGE-PET40-TW-JP-EARLY-OFFICIAL-SOURCE-BOUNDARIES-R1.json")

    def test_player_account_links_only_to_the_original_client_label(self):
        account = self.receipt["tw"]["published_player_account"]
        self.assertEqual(account["evidence"], "OPERATOR_HOSTED_PLAYER_RECOLLECTION")
        self.assertEqual(account["editorial_date_as_written"], "2001/1/20")
        self.assertEqual(account["source"]["capture"], "20010128223100")
        self.assertEqual((account["reported_name"], account["reported_acquisition"]),
                         ("布魯頓", "五兄弟之謎獎勵選擇"))
        self.assertIsNone(account["actual_acquisition_date"])
        self.assertIsNone(account["original_running_build"])
        self.assertFalse(account["official_live_release_confirmed"])
        album = read("STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
        reference, = (row for row in album["records"] if row["name_as_written"] == "布魯頓")
        self.assertEqual(account["client_album"],
                         {field: reference[field] for field in account["client_album"]})
        self.assertEqual(account["name_match_client_scope"], "EXACT_PRINTED_NAME_ONLY")

    def test_original_year_2000_updates_and_named_skill_remain_bounded(self):
        observed = self.receipt["jp"]["year_2000_operator_update_index"]
        prior = read("STONEAGE-JSS-PET-PATCH-HISTORY-R1.json")["dated_index"]
        self.assertEqual(observed["all_year_2000_dated_rows"], [
            {field: row[field] for field in ("source_order", "date", "body_fingerprint")}
            for row in prior if row["date"].startswith("2000-")
        ])
        self.assertEqual(observed["explicit_pet_term_source_orders"], [16, 20, 21, 22])
        skill = observed["new_named_skill_observation"]
        self.assertEqual((skill["date"], skill["skill_as_written"]), ("2000-03-06", "背水の陣"))
        self.assertIsNone(skill["pet_name"])
        self.assertIsNone(skill["affected_parameter"])
        launcher = self.receipt["jp"]["launcher"]
        self.assertTrue(all(capture.startswith("2001") for capture in launcher["exact_target_captures"]))
        self.assertFalse(launcher["year_2000_full_client_acquired"])

    def test_neither_cards_nor_unrelated_binaries_enter_release_roster(self):
        card = self.receipt["tw"]["operator_commercial_card_history"]
        self.assertEqual((card["recalled_card_release_month"], card["cards_in_recalled_set"]), ("2000-08", 3))
        self.assertEqual(card["named_pets_from_2000_set"], [])
        self.assertFalse(card["in_game_redemption_proven"])
        self.assertEqual(len(self.receipt["archive_files_excluded"]), 3)
        for patch in self.receipt["archive_files_excluded"]:
            self.assertTrue(patch["static_title"].startswith("三國風雲2 "))
            self.assertFalse(patch["is_stoneage_client_or_patch"])
        self.assertEqual(self.receipt["new_named_pet_release_proofs"], 0)
        self.assertIsNone(self.receipt["historical_pet_population_count"])
        self.assertEqual(choose(load(), year=2000), [])
