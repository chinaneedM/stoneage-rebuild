"""R97 independent catalog-source assertions and identity/graphic regression guards."""
import copy
import json
import unittest
from tools.stoneage_cn_early_pig_catalog_r97 import P,verify

class R97PigCatalog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(P.read_text(encoding="utf-8"))
    def rejects(self, mutate):
        c=copy.deepcopy(self.d)
        mutate(c)
        with self.assertRaises(AssertionError):
            verify(c)
    def test_original_claim_pinned(self):
        self.assertTrue(verify(self.d))
    def test_original_date_is_unknown(self):
        self.rejects(lambda d:d["sources"][0].update(original_publication_date="2001-06-14"))
    def test_original_build_is_unknown(self):
        self.rejects(lambda d:d["sources"][1].update(exact_client_build="TW1.0"))
    def test_catalog_has_duplicate_name(self):
        self.rejects(lambda d:d["rows"][7].update(detail_name="乌力固力"))
    def test_index_detail_disagreement_retained(self):
        self.rejects(lambda d:d["rows"][6].update(index_name="乌力莱德"))
    def test_thumbnail_number_swap(self):
        self.rejects(lambda d:d["rows"][6].update(thumbnail_link=d["rows"][6]["thumbnail_link"].replace("a-008","a-007")))
        self.rejects(lambda d:d["rows"][7].update(thumbnail_link=d["rows"][7]["thumbnail_link"].replace("a-007","a-008")))
    def test_catalog_number_not_native_bitmap(self):
        self.rejects(lambda d:d["rows"][0].update(original_tw10_bitmap_id=1))
    def test_pet_master_not_guessed(self):
        self.rejects(lambda d:d["rows"][0].update(game_pet_master_id=1))
    def test_numeric_intersection_cannot_name_pet(self):
        self.rejects(lambda d:d["existing_original_tw10_physical_intersection"].update(catalog_gif_to_original_ADRN_id_bound=True))
        self.rejects(lambda d:d["existing_original_tw10_physical_intersection"].update(tw10_spr_frame_references_for_span=121))
    def test_no_pixel_authenticity_claim(self):
        self.rejects(lambda d:d["image_custody"].update(full_original_gif_bytes_hashed=True))
    def test_prize_report_not_game_master(self):
        self.rejects(lambda d:d["finite_reconciliation"].update(early_player_name_resolves_no008_collision=True))
    def test_versions_and_stage_are_open(self):
        self.rejects(lambda d:d["publication"].update(stage_a_closed=True))
        self.rejects(lambda d:d["publication"].update(overall_restoration_percent=100))
        self.rejects(lambda d:d["publication"].update(next="BEGIN_STAGE_B"))
    def test_pig_birth_stats_are_player_catalog_values(self):
        self.rejects(lambda d:d["rows"][3].update(reported_elements="地6风4"))
        self.rejects(lambda d:d["rows"][7].update(reported_birth_hp="18-19"))
    def test_unexpected_authority_fields_rejected(self):
        self.rejects(lambda d:d.update(original_server_pet_master_verified=True))

if __name__=="__main__":
    unittest.main()
