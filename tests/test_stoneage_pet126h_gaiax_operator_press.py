"""PET126H: operator press original publication date and no pet release promotion."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    return json.loads((ROOT / "research/recovered" / name).read_text(encoding="utf-8"))

class PET126HOperatorPress(unittest.TestCase):
    def test_2005_gai_ax_original_one_day_before_media_and_same_existing_pet(self):
        r = load("STONEAGE-PET126H-JP2005-GAIAX-DIRECT-OPERATOR-PET-PRESS-R1.json")
        p = load("STONEAGE-PET72-YEAR2005-CN-TW-JP-KR-SOURCE-R1.json")
        g = load("STONEAGE-PET126G-JP-OPERATOR-PLAYER-ALBUM-2003-2010-CROSSWALK-R1.json")
        original = r["operator_source"]
        previous = next(x for x in p["source_records"] if x["id"] == r["baseline"]["prior_pet72_release_record_id"])
        self.assertEqual(original["originally_displayed_publication_time_jst"], "2005-09-29T16:00:00+09:00")
        self.assertEqual(r["press_republication"]["published_jst"], "2005-09-30T17:49:00+09:00")
        self.assertEqual(r["graded_result"]["earlier_than_existing_media_article_calendar_days"], 1)
        self.assertEqual(original["pet_name_as_written"], previous["names"][0])
        self.assertEqual(original["item_as_written"], "不思議な袋(中)")
        self.assertEqual(original["pet_level_advertised"], previous["advertised_pet_level"])
        self.assertEqual(original["official_site_sale_planned"], "2005-10-04_AFTER_REGULAR_MAINTENANCE")
        self.assertEqual(original["hangame_sale_planned"], "2005-10_MIDDLE")
        self.assertEqual(r["baseline"]["prior_pet126g_album_ordinal"], 143)
        self.assertEqual(g["release_document_crosswalk"]["examples"][1]["name"], original["pet_name_as_written"])
        self.assertFalse(original["original_2005_http_bytes_preserved"])
        self.assertIsNone(original["original_html_sha256"])
        self.assertFalse(original["customer_received_pet_verified"])
        self.assertFalse(r["press_republication"]["independent_pet_issuance_event"])
        for key in ("new_original_pc_installers_or_patch_bytes","new_original_server_pet_id_pairs","new_verified_original_account_grants","new_independent_published_release_events","new_verified_official_species"):
            self.assertEqual(r["graded_result"][key], 0)
        self.assertTrue(r["graded_result"]["earlier_2005_promotion_date_is_not_first_live_release"])
        self.assertTrue(r["graded_result"]["no_mobile_or_dual_end_or_new_pc_remake_inclusion"])
        self.assertEqual(r["gate"]["year2026"], "NOT_YEAR_AUDITED")
        self.assertFalse(r["gate"]["source_bounded_closed"])
        self.assertIsNone(r["gate"]["completion_percent"])
        current = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(current), 2709173)
        blob = hashlib.sha1(b"blob " + str(len(current)).encode() + b"\0" + current).hexdigest()
        self.assertEqual(blob, r["gate"]["original_current_state_git_blob"])

if __name__ == "__main__":
    unittest.main()
