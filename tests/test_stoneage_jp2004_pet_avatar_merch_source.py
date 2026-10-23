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

    def test_published_r94_git_receipt_and_no_fabricated_source_zip(self):
        import hashlib
        from pathlib import Path
        base=P.parents[2]
        path=base/"research/recovered/STONEAGE-JP2004-PET-AVATAR-MERCH-ACCEPTANCE-R94.json"
        raw=path.read_bytes()
        sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
        self.assertEqual(sha,"dfd313501649a308dc33b0d025e2b5cd6b6dfb5c")
        r=json.loads(raw.decode("utf-8"))
        self.assertEqual(r["task"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-94")
        self.assertEqual(r["source_file"]["git_blob_sha1"],"766ef71c55fd9bc0d7a68e255032ed790163805d")
        self.assertEqual(r["source_file"]["bytes"],P.stat().st_size)
        self.assertEqual(r["source_validation"]["original_test_methods"],10)
        self.assertEqual(r["source_validation"]["conclusion"],"success")
        self.assertTrue(r["candidate_continuity_validation"]["all_completed_success"])
        self.assertTrue(r["main_publication_validation"]["all_completed_success"])
        self.assertEqual(len(set(r["candidate_continuity_validation"]["run_ids"])),9)
        self.assertEqual(len(set(r["main_publication_validation"]["run_ids"])),11)
        self.assertTrue(set(r["candidate_continuity_validation"]["run_ids"]).isdisjoint(set(r["main_publication_validation"]["run_ids"])))
        self.assertEqual(r["main_publication_validation"]["dedicated_run_id"],39955548531)
        self.assertEqual(r["source_validation"]["job_id"],120418840764)
        self.assertFalse(r["actions_artifacts"]["raw_original_html_zip_present"])
        self.assertFalse(r["actions_artifacts"]["raw_original_image_zip_present"])
        self.assertEqual(r["actions_artifacts"]["main_dedicated_artifact_count"],0)
        self.assertIsNone(r["source_file"]["original_news_html_sha256"])
        self.assertIsNone(r["source_file"]["original_image_sha256"])
        self.assertTrue(r["preservation"]["old_full_file_preserved_as_prefix"])
        self.assertEqual(r["scope"]["named_2004_avatars"],3)
        self.assertEqual(r["scope"]["total_announced_avatars"],7)
        self.assertFalse(r["scope"]["original_sprite_animation_binding_recovered"])
        self.assertFalse(r["scope"]["stage_a_accepted"])
        self.assertIsNone(r["scope"]["overall_restoration_percentage"])
        self.assertEqual(r["next"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-95")

if __name__ == "__main__":
    unittest.main()
