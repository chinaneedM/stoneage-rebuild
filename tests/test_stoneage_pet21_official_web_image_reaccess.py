"""PET21 original-image URL and archival provenance negative controls (offline)."""
import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import stoneage_pet21_official_web_image_reaccess as pet21


class Pet21Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = pet21.CATALOG.read_bytes()
        cls.catalogue = json.loads(cls.raw)
        cls.targets = pet21.targets(cls.catalogue)

    def test_existing_frozen_catalogue_and_23_cross_page_targets(self):
        self.assertEqual(pet21.git_blob(self.raw), pet21.PINNED_CATALOG_GIT_BLOB)
        self.assertEqual(len(self.targets), 23)
        self.assertEqual(set(x["source_namespace"] for x in self.targets),
                         {"jp_official_web", "cn_official_web"})
        self.assertEqual(
            {x["original_page_url"] for x in self.targets
             if x["source_namespace"] == "jp_official_web"},
            {"http://www.hangame.co.jp/publish/sa/chara2.asp",
             "http://www.hangame.co.jp/publish/sa/chara2-2.asp",
             "http://www.hangame.co.jp/publish/sa/chara2-3.asp"})
        self.assertEqual(
            {x["original_page_url"] for x in self.targets
             if x["source_namespace"] == "cn_official_web"},
            {"http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet.asp",
             "http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet1.asp",
             "http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet2.asp"})

    def test_first_original_jp_image_pin_and_cn_unnamed_is_not_fabricated(self):
        jp = self.targets[0]
        self.assertEqual(jp["name_as_written"], "ウーリ")
        self.assertEqual(jp["previously_verified_image_sha256"],
                         "593345c3edf78ebcaa2dff0c27a2d10a92b4eefcc4aef4db14aee2efdc5e013f")
        self.assertIsNone(jp["actual_client_species_id"])
        self.assertFalse(jp["public_use_permission_verified"])
        cn = next(x for x in self.targets
                  if x["source_namespace"] == "cn_official_web" and x["web_ordinal"] == 1)
        self.assertIsNone(cn["name_as_written"])
        self.assertTrue(cn["original_image_url"].endswith("/6.JPG"))
        self.assertNotEqual(cn["web_ordinal"], 6)

    def test_url_whitelist_and_no_internal_or_external_target_injection(self):
        good = self.targets[0]
        self.assertEqual(pet21.verify_reference(good["original_image_url"], "jp_official_web"),
                         good["original_image_url"])
        for url, namespace in (
            ("file:///tmp/source.gif", "jp_official_web"),
            ("http://127.0.0.1/_images/game/saj/petpicgroup1-1.gif", "jp_official_web"),
            ("http://images.hangame.co.jp/_images/game/saj/foo.gif", "jp_official_web"),
            ("http://images.hangame.co.jp@evil.example/x.gif", "jp_official_web"),
            ("http://www.waei.com.cn/ZHUANQU/stoneage2/pet/img/newpet/1.JPG?x=1", "cn_official_web"),
            ("http://images.hangame.co.jp/_images/game/saj/petpicgroup1-1.gif", "cn_official_web"),
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                pet21.verify_reference(url, namespace)

    def test_image_magic_and_archive_raw_capture_guard(self):
        gif = (b"GIF89a" + (60).to_bytes(2, "little") +
               (65).to_bytes(2, "little") + b"faked-gif-test")
        self.assertEqual(pet21.image_magic(gif), ("GIF", [60, 65]))
        response = {"final_url":
            "https://web.archive.org/web/20060604065927id_/http://images.hangame.co.jp/_images/game/saj/petpicgroup1-1.gif",
            "content_type": "image/gif"}
        proved = pet21.image_proof(response, gif, hashlib.sha256(gif).hexdigest())
        self.assertEqual(proved["kind"], "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED")
        self.assertEqual(proved["archive_image_capture"], "20060604065927")
        self.assertTrue(proved["earlier_confirmed_sha_matches"])
        self.assertFalse(proved["same_capture_instant_as_parent_page_proven"])
        self.assertFalse(proved["official_game_client_graphic_id_proven"])
        self.assertFalse(proved["image_publication_rights_proven"])

        html = b"<html>Wayback Machine request unavailable</html>"
        self.assertEqual(pet21.image_proof(response, html, None)["kind"],
                         "NON_IMAGE_RESPONSE_NOT_RECOVERED")
        no_capture = dict(response, final_url="http://images.hangame.co.jp/picture.gif")
        self.assertEqual(pet21.image_proof(no_capture, gif, None)["kind"],
                         "IMAGE_BYTES_WITHOUT_VERIFIED_ARCHIVE_PROVENANCE")
        oversized = b"GIF89a" + b"X" * pet21.MAX_IMAGE_BYTES
        self.assertEqual(pet21.image_proof(response, oversized, None)["kind"],
                         "RESPONSE_TOO_LARGE_NOT_RECOVERED")

    def test_failed_archive_returns_capped_open_not_absent_and_no_disk_images(self):
        with patch.object(pet21, "retrieve",
                          return_value=({"status": "HTTP_ERROR", "http_status": 502}, None, None)):
            data = pet21.run_probe(self.targets[:2], workers=2, timeout=1)
        self.assertEqual(data["sample_target_count"], 2)
        self.assertEqual(data["source_qualified_archived_images_newly_observed"], 0)
        self.assertEqual(data["result_counts"], {"NOT_RETRIEVED_NETWORK_OR_INDEX_BLOCKED": 2})
        self.assertTrue(data["no_response_does_not_prove_no_archived_image_exists"])
        self.assertFalse(data["original_media_written_to_disk_or_published"])
        self.assertTrue(all(x["image_result"]["kind"] == "NOT_RETRIEVED_NETWORK_OR_INDEX_BLOCKED"
                            for x in data["records"]))

    def test_catalogue_original_image_count_stays_unchanged(self):
        actual_jp = [x for x in self.catalogue["datasets"]["jp_official_web"]
                     if x["image_original_bytes_acquired"]]
        self.assertEqual(len(actual_jp), 1)
        self.assertEqual(len(self.catalogue["datasets"]["jp_official_web"]), 124)
        self.assertEqual(len(self.catalogue["datasets"]["cn_official_web"]), 104)
        self.assertTrue(all(x["image_actual_sha256"] is None
                            for x in self.catalogue["datasets"]["cn_official_web"]))


if __name__ == "__main__":
    unittest.main()
