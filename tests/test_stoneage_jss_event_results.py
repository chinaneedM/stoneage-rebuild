import io
import hashlib
import json
from pathlib import Path
import unittest
from PIL import Image
from tools.stoneage_jss_event_results import (
    ROOT, IMAGES, compare_event_profiles, image_metadata, index_entries,
    result_contract, select_comedy_result,
)

BASE = Path(__file__).resolve().parents[1]
REPORT = BASE / "research/recovered/STONEAGE-JSS-EVENT-RESULTS-PET-ATTRIBUTION-R1.json"


def index_fixture():
    parts = []
    for i in range(14, 0, -1):
        title = "第1回お笑いコンテスト" if i == 9 else f"他のイベント{i}"
        parts.append(f'<table><tr><td>{title}</td><td><a href="eventj{i:02d}.html">結果発表</a></td></tr></table>')
    for title in ("はずれくじキャンペーン", "スクリーンショットコンテスト"):
        parts.append(f'<table><tr><td>{title}</td></tr><tr><td>magazine notice</td></tr></table>')
    return "".join(parts)


def result_fixture():
    awards = [("大賞", "30000stone＆ レアペット（未登場）", "PLAYER_NAME_NOT_A_PET_SPECIES"),
              ("アイデア賞", "20000stone", "GROUP_B"), ("最優秀個人賞", "10000stone", "PLAYER_C"),
              ("特別個人賞", "10000stone", "PLAYER_A")]
    cells = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in awards)
    images = "".join(f'<img src="image/{name}" width="999" height="888">' for name in IMAGES)
    return ('<font size="5">ねるとん</font><table><tr><td>第1回お笑いコンテスト</td></tr>'
            '<tr><td>多数のご参加ありがとうございました<table>' + cells + '</table>'
            '最優秀個人賞の意見が分かれたため急遽賞を追加 無事に終了 '
            '第２回お笑いコンテストも予定' + images + '</td></tr></table>')


class ResultAttributionTests(unittest.TestCase):
    def chosen(self):
        return select_comedy_result(index_entries(index_fixture()))

    def test_real_row_identity_selects_09_and_wrong_prefetch_07_is_rejected(self):
        row = self.chosen()
        self.assertEqual(row["detail_url"], ROOT + "eventj09.html")
        row["detail_url"] = ROOT + "eventj07.html"
        with self.assertRaisesRegex(ValueError, "identity/path mismatch"):
            select_comedy_result([row])
        with self.assertRaisesRegex(ValueError, "wrong result resource"):
            result_contract(result_fixture(), row)

    def test_comment_only_fake_index_row_cannot_replace_real_event(self):
        fake = '<!--<tr><td>第1回お笑いコンテスト</td><td><a href="eventj07.html">wrong</a></td></tr>-->'
        self.assertEqual(index_entries(index_fixture() + fake), index_entries(index_fixture()))

    def test_missing_unique_title_is_not_replaced_by_the_first_result_link(self):
        entries = index_entries(index_fixture().replace("第1回お笑いコンテスト", "第2回お笑いコンテスト"))
        with self.assertRaisesRegex(ValueError, "unique first comedy"):
            select_comedy_result(entries)

    def test_nested_award_table_preserves_four_awards_and_recipient_roles(self):
        facts, refs = result_contract(result_fixture(), self.chosen())
        self.assertEqual([r["stone"] for r in facts["awards"]], [30000, 20000, 10000, 10000])
        self.assertTrue(facts["special_individual_award_added_described"])
        for award in facts["awards"]:
            self.assertIsNone(award["pet_species_or_id"])
            self.assertEqual(award["recipient_column_role"], "PLAYER_GROUP_OR_CHARACTER_TEXT_NOT_PET_SPECIES")
        self.assertEqual(len(refs), 3)
        self.assertNotIn("PLAYER_NAME_NOT_A_PET_SPECIES", json.dumps(facts))

    def test_template_banner_is_recorded_but_cannot_override_event_body(self):
        facts, _ = result_contract(result_fixture(), self.chosen())
        self.assertEqual(facts["template_banner"], "ねるとん")
        self.assertTrue(facts["template_banner_mismatch_preserved"])
        with self.assertRaisesRegex(ValueError, "wrong event body"):
            result_contract(result_fixture().replace("第1回お笑いコンテスト", "第2回ログイン杯デュエル大会"), self.chosen())

    def test_same_prize_does_not_join_different_editions(self):
        one = {"family": "COMEDY_CONTEST", "edition": 1, "prize": 30000}
        two = {"family": "COMEDY_CONTEST", "edition": 2, "prize": 30000}
        self.assertEqual(compare_event_profiles(one, two), "REJECT_EDITION_MISMATCH")

    def test_same_edition_with_missing_dates_or_server_still_stays_open(self):
        one = {"family": "COMEDY_CONTEST", "edition": 1}
        self.assertEqual(compare_event_profiles(one, dict(one)), "OPEN_MISSING_IDENTITY_CONTEXT")
        complete = dict(one, year=2000, month_day="01-01", server="SUN")
        self.assertEqual(compare_event_profiles(complete, dict(complete)), "MATCHING_METADATA_ONLY_NOT_SERVER_EXECUTION")

    def test_result_comment_does_not_create_a_fifth_award_or_pet(self):
        fake = '<!--<tr><td>大賞</td><td>99999stone PET_SPECIES</td><td>wrong</td></tr>-->'
        self.assertEqual(result_contract(result_fixture() + fake, self.chosen()), result_contract(result_fixture(), self.chosen()))

    def test_changed_special_prize_requires_source_requalification(self):
        with self.assertRaisesRegex(ValueError, "award table changed"):
            result_contract(result_fixture().replace("<td>特別個人賞</td><td>10000stone", "<td>特別個人賞</td><td>20000stone"), self.chosen())

    def test_image_dimensions_require_actual_bytes_and_early_origin(self):
        b = io.BytesIO()
        Image.new("RGB", (23, 17), "blue").save(b, "JPEG")
        original = ROOT + "image/sass0901.jpg"
        r = image_metadata(b.getvalue(), "https://web.archive.org/web/20010422000000id_/" + original, original)
        self.assertEqual((r["actual_width"], r["actual_height"]), (23, 17))
        with self.assertRaisesRegex(ValueError, "historical window"):
            image_metadata(b.getvalue(), "https://web.archive.org/web/20210422000000id_/" + original, original)

    def test_archived_missing_images_have_no_invented_visuals_or_dimensions(self):
        r = json.loads(REPORT.read_text())
        self.assertEqual(r["qualified_image_count"], 0)
        self.assertEqual(len(r["unqualified_image_references"]), 3)
        for image in r["unqualified_image_references"]:
            self.assertFalse(image["source_absence_established"])
            self.assertTrue(image["visual_contents_unknown"])
            self.assertIsNone(image["actual_dimensions"])
        self.assertEqual(r["second_comedy_attribution"]["decision"], "REJECT_EDITION_MISMATCH")

    def test_first_result_has_no_promoted_second_event_or_taiwan_identity(self):
        r = json.loads(REPORT.read_text())
        self.assertTrue(r["first_comedy_result"]["operator_reports_event_completed"])
        self.assertFalse(r["first_comedy_result"]["server_execution_or_reward_transaction_verified"])
        self.assertFalse(r["second_comedy_attribution"]["second_event_completed_or_pet_identity_proven"])
        self.assertFalse(r["boundaries"]["jss1999_or_tw10_same_build_proven"])
        self.assertEqual(r["results_index"]["entry_count"], 16)

    def test_actual_retrieval_error_and_three_unavailable_images_are_preserved(self):
        intake = json.loads((BASE / "research/recovered/STONEAGE-JSS-EVENT-RESULTS-SOURCE-INTAKE-R1.json").read_text())
        correction = intake["retrieval_correction"]
        self.assertEqual(correction["wrong_prefetched_resource"], "eventj07.html")
        self.assertEqual(correction["expected_resource"], "eventj09.html")
        self.assertTrue(correction["excluded_from_current_result_and_pet_facts"])
        self.assertEqual(len(intake["image_first_attempts"]), 3)
        self.assertEqual(len(intake["image_bounded_availability_attempts"]), 3)
        self.assertTrue(intake["availability_rate_limited_no_further_retry"])
        self.assertFalse(intake["forms_or_feedback_endpoints_queried_or_submitted"])

    def test_source_intake_preserves_original_continuity_prefix_and_report(self):
        intake = json.loads((BASE / "research/recovered/STONEAGE-JSS-EVENT-RESULTS-SOURCE-INTAKE-R1.json").read_text())
        for row in intake["baseline_input_files"]:
            data = (BASE / row["path"]).read_bytes()[:row["bytes"]]
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])
        self.assertEqual(hashlib.sha256(REPORT.read_bytes()).hexdigest(), intake["report"]["sha256"])


if __name__ == "__main__":
    unittest.main()
