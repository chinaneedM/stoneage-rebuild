import json
import unittest
from pathlib import Path
from tools import stoneage_pet33_jp1999_capture_rearing as pet33


class Pet33Boundary(unittest.TestCase):
    def test_published_source_contract(self):
        p = Path("research/recovered/STONEAGE-PET33-JP1999-0518-PRELAUNCH-PET-SOURCE-R1.json")
        data = json.loads(p.read_text(encoding="utf-8"))
        self.assertEqual(data["source"]["bytes"], pet33.BYTES)
        self.assertEqual(data["source"]["sha256"], pet33.SHA256)
        self.assertEqual(data["bounded_record"]["normalized_entry_sha256"], pet33.ENTRY_SHA256)
        self.assertEqual(data["bounded_record"]["source_attestation_date_not_pet_release_date"], "1999-05-18")
        self.assertEqual(data["bounded_record"]["pet_feature_capture"], "PRE_LAUNCH_ANNOUNCED_ONLY")
        self.assertEqual(data["bounded_record"]["pet_feature_rearing"], "PRE_LAUNCH_ANNOUNCED_ONLY")
        self.assertFalse(data["bounded_record"]["named_pet_released_or_obtainable_proven"])
        self.assertFalse(data["bounded_record"]["official_game_live_feature_execution_proven"])
        self.assertFalse(data["bounded_record"]["original_1999_client_binary_or_server_deployment_proven"])
        self.assertEqual(data["new_official_released_named_pet_species"], [])
        self.assertEqual(data["chronology"]["1999_year_review_status"], "NOT_YEAR_AUDITED")
        self.assertEqual(data["chronology"]["active_module"], "PET")

    def test_wrong_primary_source_rejected(self):
        with self.assertRaises(ValueError):
            pet33.build(b"unqualified", pet33.URL)
        with self.assertRaises(ValueError):
            pet33.build(b"unqualified", "https://other.example/pet.html")
        with self.assertRaises(ValueError):
            pet33.feature_entry("<p>1999年5月18日</p><p>ストーンエイジ ペット もう発売しました</p>")

    def test_1999_promotion_is_not_a_species_row(self):
        data = json.loads(Path(
            "research/recovered/STONEAGE-PET33-JP1999-0518-PRELAUNCH-PET-SOURCE-R1.json"
        ).read_text(encoding="utf-8"))
        self.assertEqual(data["bounded_record"]["1999_official_named_pet_species_in_this_entry"], [])
        self.assertNotEqual(data["bounded_record"]["sale_or_launch_timing"], "LIVE_DEPLOYED")
        self.assertTrue(data["chronology"]["does_not_supersede_live_pet_release_audit"])


if __name__ == "__main__":
    unittest.main()
