import io
import hashlib
import json
from pathlib import Path
import unittest
from PIL import Image
from tools.stoneage_jss_official_event_venue import (
    IMAGE_NAMES, ROOT, event_contract, image_metadata, parse, qualify, venue_contract,
)

ROOT_DIR = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT_DIR / "research/recovered/STONEAGE-JSS2001-OFFICIAL-EVENT-VENUE-R1.json"


def announcements():
    return '''<b>第２回お笑いコンテスト</b><p>
    11月17日(金) 23:30 太陽サーバー マンモスホール 11月15日(月)AM9:00
    23:00まで 事前エントリー 抽選 レアペット（未登場） 持ち時間は5分。
    1人から最大5人 大賞 30000stone アイデア賞 20000stone 最優秀個人賞 10000stone</p>
    <!-- <a href="http://www.titan.co.jp/cgi-bin/mail/saevent6.html">inactive</a> -->
    <b>第２回ねるとん</b><p>12月22日(金) 22:00 月サーバー 12月18日(月)AM9:00
    マンモスホール 控え室 22:45まで 21:45 見学はOK 事前エントリー 抽選 名刺をひとつ 一時的な変更
    24:00 自己紹介 質問コーナー フリートーク 告白タイム ジャンケン 性別が違う キャラクターグラフィック
    参加者は、10名の予定</p>
    <!-- <a href="http://www.titan.co.jp/cgi-bin/mail/saevent5.html">inactive</a> -->'''


def venue():
    text = '''チャットルーム案内所 チケット販売員 チケットをもらって 案内係
    北側 右端 マンモスホール 右から二番目 結婚式場
    マリナス 東51 南72 トーテムポール南東 カルターナ 東81 南49 トーテムポール北東
    サムギル 東111 南38 村長宅北東スグ ジャジャ 東85 南73 村長宅南西スグ'''
    return text + "".join(f'<img src="image/{name}" width="999" height="888">' for name in IMAGE_NAMES)


class OfficialEventVenueTests(unittest.TestCase):
    def test_commented_form_is_not_an_active_registration_link(self):
        doc = parse('<a href="event.html">active</a><!--<a href="form.html">hidden</a>--><script>fake NPC reward30000</script>')
        self.assertEqual(doc.links, [ROOT + "event.html"])
        self.assertEqual(doc.commented_links, [ROOT + "form.html"])
        self.assertNotIn("hidden", doc.text)
        self.assertNotIn("fake NPC", doc.text)

    def test_planned_event_keeps_unknown_year_and_conflicting_times(self):
        r = event_contract(announcements())
        self.assertEqual(r["comedy"]["prizes_as_announced"]["grand_prize_stone"], 30000)
        self.assertIsNone(r["comedy"]["rare_pet_species_or_id"])
        self.assertIsNone(r["comedy"]["year"])
        self.assertIsNone(r["matchmaking"]["year"])
        self.assertEqual(r["matchmaking"]["gathering_callout"], "22:45")
        self.assertEqual(r["matchmaking"]["gathering_timetable"], "21:45")
        self.assertTrue(r["matchmaking"]["gathering_conflict_preserved"])
        self.assertFalse(r["matchmaking"]["planned_count_is_server_capacity"])
        self.assertFalse(r["events_actually_held_or_prizes_actually_awarded_proven"])

    def test_changed_participation_number_requires_requalification(self):
        with self.assertRaisesRegex(ValueError, "quantities changed"):
            event_contract(announcements().replace("参加者は、10名", "参加者は、20名"))

    def test_active_form_changes_source_semantics(self):
        with self.assertRaisesRegex(ValueError, "active links"):
            event_contract(announcements() + '<a href="form.html">register</a>')

    def test_hidden_false_event_does_not_change_visible_contract(self):
        original = event_contract(announcements())
        self.assertEqual(event_contract(announcements() + '<!--第２回ねるとん NPC999 reward99999-->'), original)

    def test_source_coordinates_are_not_server_floor_or_npc_ids(self):
        r, references = venue_contract(venue())
        self.assertEqual([x["coordinate_labels"] for x in r["village_entrances"]],
                         [{"east": 51, "south": 72}, {"east": 81, "south": 49}, {"east": 111, "south": 38}, {"east": 85, "south": 73}])
        self.assertIsNone(r["ticket_price"])
        self.assertIsNone(r["ticket_item_id"])
        for row in r["village_entrances"]:
            self.assertIsNone(row["server_floor_id"])
            self.assertIsNone(row["npc_id"])
            self.assertFalse(row["tw10_or_recovered25_map_join_proven"])
        self.assertEqual(references[0]["html_width"], "999")

    def test_coordinate_transposition_is_not_silently_accepted(self):
        with self.assertRaisesRegex(ValueError, "coordinates changed"):
            venue_contract(venue().replace("東51 南72", "東72 南51"))

    def test_foreign_or_retimed_html_is_not_same_source(self):
        with self.assertRaisesRegex(ValueError, "original/capture changed"):
            qualify(b"anything", "https://example.com/event.html", "event")
        url = "https://web.archive.org/web/20010417155224id_/" + ROOT + "event.html"
        with self.assertRaisesRegex(ValueError, "bytes changed"):
            qualify(b"new body", url, "event")

    def test_image_dimensions_come_from_actual_jpeg(self):
        stream = io.BytesIO()
        Image.new("RGB", (23, 17), "red").save(stream, "JPEG")
        original = ROOT + "image/chat02.jpg"
        r = image_metadata(stream.getvalue(), "https://web.archive.org/web/20010630210857id_/" + original, original)
        self.assertEqual((r["actual_width"], r["actual_height"]), (23, 17))
        self.assertFalse(r["same_moment_as_html_proven"])
        with self.assertRaisesRegex(ValueError, "historical window"):
            image_metadata(stream.getvalue(), "https://web.archive.org/web/20210630210857id_/" + original, original)

    def test_archive_preserves_three_sources_and_all_six_image_outcomes(self):
        data = json.loads(ARCHIVE.read_text())
        self.assertEqual(set(data["source_pages"]), {"event", "eventjss", "eventmaz"})
        qualified = {x["original_url"] for x in data["images"]}
        unqualified = {x["original_url"] for x in data["unqualified_image_references"]}
        self.assertFalse(qualified & unqualified)
        self.assertEqual(qualified | unqualified, {ROOT + "image/" + name for name in IMAGE_NAMES})
        self.assertFalse(data["boundaries"]["named_npc_quest_script_recovered"])
        self.assertFalse(data["boundaries"]["jss1999_or_tw10_same_build_proven"])

    def test_visual_observations_reference_exact_verified_image_bytes(self):
        report = ARCHIVE.read_bytes()
        catalog = json.loads((ROOT_DIR / "research/recovered/STONEAGE-JSS-OFFICIAL-EVENT-CONTENT-CATALOG-R1.json").read_text())
        self.assertEqual(catalog["report"]["sha256"], hashlib.sha256(report).hexdigest())
        data = json.loads(report)
        self.assertEqual({(x["file"], x["sha256"], x["actual_capture"]) for x in catalog["rows"]},
                         {(x["original_url"].rsplit("/", 1)[-1], x["sha256"], x["actual_capture"]) for x in data["images"]})
        self.assertTrue(catalog["editorial_annotations_are_not_client_ui_proof"])
        self.assertFalse(catalog["runtime_route_or_event_execution_proven"])

    def test_original_continuity_and_source_prefixes_survive_append(self):
        intake = json.loads((ROOT_DIR / "research/recovered/STONEAGE-JSS-OFFICIAL-EVENT-SOURCE-INTAKE-R1.json").read_text())
        for row in intake["baseline_input_files"]:
            raw = (ROOT_DIR / row["path"]).read_bytes()[:row["bytes"]]
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row["sha256"], row["path"])
        self.assertFalse(intake["results_page_or_entry_forms_queried"])


if __name__ == "__main__":
    unittest.main()
