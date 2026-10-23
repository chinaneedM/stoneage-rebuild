"""R94 adversarial evidence tests: 2004 pet avatars not original game sprites."""
import copy
import json
import unittest
from tools.stoneage_jp2004_pet_avatar_merch_source import P,verify

class JP2004PetAvatarCrossMediaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original=json.loads(P.read_text(encoding="utf-8"))
    def reject(self, mut):
        d=copy.deepcopy(self.original)
        mut(d)
        with self.assertRaises(AssertionError):
            verify(d)
    def test_original_source_pinned(self):
        self.assertTrue(verify(self.original))
    def test_no_original_build_or_archived_html(self):
        self.reject(lambda d:d["sources"][0].update(exact_game_build="JSS1999"))
        self.reject(lambda d:d["sources"][1].update(original_html_authenticated=True))
    def test_three_named_not_seven_species(self):
        self.reject(lambda d:d["source_claims"].update(s1_pet_avatar_total=3))
        self.reject(lambda d:d["source_claims"]["s1_named_pet_avatar_text"].append("new species"))
    def test_background_and_price_are_not_game_stats(self):
        self.reject(lambda d:d["source_claims"].update(s1_background_total=7))
        self.reject(lambda d:d["attribution_boundaries"].update(price_is_virtual_pet_in_game_price=True))
    def test_cross_source_names_not_original_ids(self):
        self.reject(lambda d:d["observations"][1].update(in_game_pet_numeric_id=444))
        self.reject(lambda d:d["relation"].update(same_pet_numeric_id_verified=True))
    def test_avatar_image_not_original_sprite(self):
        self.reject(lambda d:d["illustration"].update(individual_animal_to_reported_name_mapping_verified=True))
        self.reject(lambda d:d["illustration"].update(original_pet_animation_sprite_verified=True))
    def test_physical_premium_vs_virtual_avatar(self):
        self.reject(lambda d:d["source_claims"].update(s2_named_physical_premium="ゴルシス"))
        self.reject(lambda d:d["relation"].update(same_visual_asset_identical=True))
    def test_packaged_formal_date_not_1999_launch(self):
        self.reject(lambda d:d["source_claims"].update(s2_jp_formal_service_announced_date="1999-01-01"))
        self.reject(lambda d:d["attribution_boundaries"].update(s2_june_3_is_1999_launch_date=True))
    def test_no_copyright_asset_transfers(self):
        self.reject(lambda d:d["illustration"].update(artwork_embedded_in_repository=True))
        self.reject(lambda d:d["illustration"].update(production_asset_license_granted=True))
    def test_stage_a_and_next_never_promoted(self):
        self.reject(lambda d:d["acceptance"].update(stage_a_closed=True))
        self.reject(lambda d:d["acceptance"].update(overall_restoration_percentage=88))
        self.reject(lambda d:d["acceptance"].update(next="CLOSED"))

if __name__ == "__main__":
    unittest.main()
