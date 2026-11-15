"""PET22 official JP 124 original web source URLs, no inferred client graphic IDs."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import stoneage_pet21_official_web_image_reaccess as p21
import stoneage_pet22_jp_official_124_archive_batch as p22


class PET22ReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = p21.CATALOG.read_bytes()
        cls.catalog = json.loads(cls.raw)
        cls.groups = p22.all_jp_targets(cls.catalog)
        cls.prior = json.loads(p22.PET21_RECEIPT.read_text(encoding="utf-8"))

    def test_all_124_exact_original_web_page_refs_no_guess_and_no_extra(self):
        self.assertEqual(p21.git_blob(self.raw), p21.PINNED_CATALOG_GIT_BLOB)
        self.assertEqual({i: len(g) for i, g in self.groups.items()}, {1: 45, 2: 45, 3: 34})
        ordered = [x for group in self.groups.values() for x in group]
        self.assertEqual([x["web_ordinal"] for x in ordered], list(range(1, 125)))
        self.assertEqual(len({x["record_id"] for x in ordered}), 124)
        self.assertTrue(all(x["source_namespace"] == "jp_official_web" for x in ordered))
        self.assertTrue(all(x["actual_client_species_id"] is None for x in ordered))
        self.assertTrue(all(x["public_use_permission_verified"] is False for x in ordered))
        for group, items in self.groups.items():
            for i, x in enumerate(items, 1):
                self.assertTrue(x["original_image_url"].endswith(
                    f"/petpicgroup{group}-{i}.gif"))
                self.assertEqual(len(x["page_body_sha256"]), 64)

    def test_existing_pet21_positive_observations_remain_independent(self):
        self.assertEqual(self.prior["observed"]["jp_original_archived_image_bytes_observed_transient"], 9)
        self.assertEqual(self.prior["observed"]["jp_original_archived_image_bytes_newly_hashed"], 8)
        self.assertEqual(self.prior["probe_workflow_run_id"], 43693853890)
        observed = {x["web_ordinal"]: x for x in self.prior["records"]
                    if x["source_namespace"] == "jp_official_web"
                    and x["probe_status"] == "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED"}
        self.assertEqual(set(observed), {1, 2, 3, 44, 45, 46, 89, 91, 123})
        mock = {"records": [{
            "web_ordinal": ordinal,
            "image_result": {
                "kind": "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED",
                "sha256": previous["returned_original_media_image_sha256_or_null"],
            },
        } for ordinal, previous in observed.items()]}
        comparison = p22.comparison_to_pet21(mock, self.prior)
        self.assertEqual(len(comparison), 9)
        self.assertTrue(all(c["comparison"] == "SAME_IMAGE_SHA_ACROSS_INDEPENDENT_GITHUB_ACTIONS"
                            for c in comparison))
        mock["records"][0]["image_result"]["sha256"] = "0" * 64
        comparison2 = p22.comparison_to_pet21(mock, self.prior)
        self.assertEqual(comparison2[0]["comparison"],
                         "DIFFERENT_ARCHIVE_CAPTURE_OR_IMAGE_BYTES_MUST_NOT_OVERWRITE_HISTORY")

    def test_original_2004_page_and_2003_image_captures_not_coincident(self):
        latest_page = self.groups[3][0]
        self.assertEqual(latest_page["web_ordinal"], 91)
        self.assertEqual(latest_page["page_archive_capture"], "20040220221717")
        old_jp91 = next(x for x in self.prior["records"]
                        if x["source_namespace"] == "jp_official_web" and x["web_ordinal"] == 91)
        self.assertEqual(old_jp91["observed_image_archive_capture_or_null"], "20031214163657")
        self.assertFalse(old_jp91["contemporaneous_image_with_operator_page_archive_proven"])

    def test_no_cn_web_entries_or_duplicate_jp_game_id(self):
        self.assertEqual(len(self.catalog["datasets"]["cn_official_web"]), 104)
        self.assertEqual(len(self.catalog["datasets"]["jp_official_web"]), 124)
        self.assertTrue(all(x["actual_client_species_id"] is None
                            for x in self.catalog["datasets"]["jp_official_web"]))
        self.assertTrue(all(x["image_reference_url"].startswith(
            "http://images.hangame.co.jp/_images/game/saj/")
                            for x in self.catalog["datasets"]["jp_official_web"]))


if __name__ == "__main__":
    unittest.main()
