"""Synthetic clause tests, plus guards against archival claims becoming runtime facts."""
import json
import unittest

from tools import stoneage_jss_early_quest_origins_r116 as r116


def synthetic_rows():
    values = [
        ("2000-04-24", "宝捜し ログインとの共同イベント 開始 １ヶ月限定イベント・玄黄の洞窟 イベント進行を修正"),
        ("2000-04-17", "SJOT ログインとの共同イベント 終了"),
        ("2000-04-10", "SJOT関連 NPCの設定 修正"),
        ("2000-08-28", "イベント（転生）を追加・エステ体験版キャンペーン 開始"),
        ("1999-11-01", "期間限定 チャットルームを追加・マップを追加"),
        ("1999-10-18", "ウリウリイベント 貝殻を2つとる不具合 修正"),
        ("2000-05-08", "NPCのセリフ クイズ道場 修正"),
        ("2000-05-29", "クイズ道場の奥に進めるようになりました"),
    ]
    values += [("2000-01-01", f"イベントを追加 synthetic_{i}") for i in range(13)]
    return [{"date": d, "date_as_written": d + " (synthetic)", "text": t} for d, t in values]


def synthetic_faq():
    menu = '<a href="faqquest.html">よくいただくご質問</a>'
    detail = '''よくいただくご質問
    <!-- Q:体験版のデータ A:IDが完全に異なります -->
    Q:Windows2000 A:RC2 保証するものではございません
    Q:画面キャプチャ A:[F12] screenshotフォルダ
    Q:ホームページ A:日本システムサプライの著作物 無断転載、再利用を禁止'''
    return menu, detail


class EarlyQuestOrigins(unittest.TestCase):
    def test_explicit_campaigns_and_ambiguous_gameplay_have_separate_views(self):
        r = r116.update_contract(synthetic_rows())
        self.assertEqual(len(r["material_views"]["operator_event_quests_and_activities"]), 2)
        self.assertEqual(len(r["material_views"]["unresolved_origin"]), 4)
        self.assertEqual(r["material_views"]["game_base_quests"], [])
        self.assertEqual(r["material_views"]["version_permanent_quests"], [])

    def test_rebirth_does_not_inherit_adjacent_campaign(self):
        r = r116.update_contract(synthetic_rows())
        rebirth = next(x for x in r["records"] if x["source_label"] == "転生")
        self.assertEqual(rebirth["origin_class"], "ORIGIN_UNRESOLVED")
        self.assertFalse(rebirth["permanence_proven"])
        self.assertNotIn("reported_window", rebirth)

    def test_limited_chatroom_does_not_limit_same_day_map(self):
        r = r116.update_contract(synthetic_rows())
        self.assertFalse(r["context_separations"]["limited_chatroom_and_map_addition_are_distinct_clauses"]
                         ["limited_duration_transferred_to_maps_or_unnamed_event"])

    def test_treasure_does_not_transfer_duration_to_same_day_cave_fix(self):
        r = r116.update_contract(synthetic_rows())
        cave = next(x for x in r["records"] if x["source_label"] == "玄黄の洞窟")
        self.assertEqual(cave["origin_class"], "ORIGIN_UNRESOLVED")
        self.assertNotIn("reported_window", cave)

    def test_one_month_does_not_invent_exact_closing_date(self):
        treasure = r116.update_contract(synthetic_rows())["records"][0]
        self.assertEqual(treasure["reported_window"]["duration_as_written"], "１ヶ月")
        self.assertIsNone(treasure["reported_window"]["exact_end_date"])

    def test_fix_does_not_invent_normal_required_shell_count(self):
        uriuri = r116.update_contract(synthetic_rows())["records"][4]
        self.assertIsNone(uriuri["first_introduced_date"])
        self.assertNotIn("required_shell_count", uriuri)
        self.assertIsNone(uriuri["native_quest_id"])

    def test_missing_or_changed_source_qualification_is_rejected(self):
        changes = [(0, "１ヶ月限定イベント", "限定未記載"),
                   (1, "終了", "開始"), (2, "SJOT関連", "別イベント"),
                   (3, "イベント（転生）を追加", "イベント（転生）を削除"),
                   (4, "期間限定", "常設"), (5, "貝殻を2つ", "貝殻を3つ")]
        for i, old, new in changes:
            with self.subTest(old=old):
                rows = synthetic_rows()
                rows[i]["text"] = rows[i]["text"].replace(old, new)
                with self.assertRaises(ValueError): r116.update_contract(rows)

    def test_duration_moved_to_adjacent_cave_is_rejected(self):
        rows = synthetic_rows()
        rows[0]["text"] = rows[0]["text"].replace("１ヶ月限定イベント・", "・１ヶ月限定イベント ")
        with self.assertRaises(ValueError): r116.update_contract(rows)

    def test_wrong_date_or_ambiguous_named_clause_is_rejected(self):
        for rows in (synthetic_rows(), synthetic_rows() + [synthetic_rows()[0]]):
            if len(rows) == 21: rows[0]["date"] = "2000-04-25"
            with self.assertRaises(ValueError): r116.update_contract(rows)

    def test_unnamed_addition_rows_are_not_a_quest_census(self):
        r = r116.update_contract(synthetic_rows())
        self.assertEqual(len(r["unnamed_addition_clauses"]), 13)
        self.assertTrue(r["unnamed_clauses_are_not_13_distinct_quests"])
        self.assertEqual(len(r["records"]), 6)

    def test_quiz_dojo_progress_is_not_quest_completion_or_native_identity(self):
        dojo = r116.update_contract(synthetic_rows())["records"][5]
        self.assertEqual(dojo["source_label"], "クイズ道場")
        self.assertIsNone(dojo["native_npc_id"])
        self.assertEqual([x["operator_written_date"] for x in dojo["source_clauses"]], ["2000-05-08", "2000-05-29"])
        self.assertEqual(dojo["origin_class"], "ORIGIN_UNRESOLVED")

    def test_three_active_faq_answers_exclude_comment(self):
        r = r116.faq_contract(*synthetic_faq())
        self.assertEqual(r["active_question_count"], 3)
        self.assertEqual(r["commented_question_count"], 1)
        self.assertFalse(r["quest_definition_recovered"])
        self.assertFalse(r["inactive_trial_data_answer_is_current_operator_policy"])

    def test_uncommenting_trial_policy_is_rejected(self):
        menu, detail = synthetic_faq()
        with self.assertRaises(ValueError): r116.faq_contract(menu, detail.replace("<!--", "").replace("-->", ""))

    def test_changed_faq_key_guarantee_or_rights_is_rejected(self):
        menu, detail = synthetic_faq()
        for old, new in (("[F12]", "[F11]"), ("保証するものではございません", "保証します"),
                         ("無断転載、再利用を禁止", "自由利用")):
            with self.subTest(old=old), self.assertRaises(ValueError):
                r116.faq_contract(menu, detail.replace(old, new))

    def test_fake_filename_without_real_menu_link_is_rejected(self):
        _, detail = synthetic_faq()
        with self.assertRaises(ValueError): r116.faq_contract('<a href="other.html">quest</a>', detail)

    def test_wrong_archive_bytes_or_capture_is_rejected(self):
        nav = r116.NAV.read_bytes()
        acquisitions = {k: (b"not original bytes", r116.source_url(k)) for k in r116.PAGES}
        with self.assertRaises(ValueError): r116.build(acquisitions, nav)

    def test_saved_report_keeps_views_exhaustive_and_history_qualified(self):
        d = json.loads(r116.REPORT.read_text())
        views = d["update_evidence"]["material_views"]
        ids = [r["archive_id"] for r in d["update_evidence"]["records"]]
        self.assertEqual(sorted(sum(views.values(), [])), sorted(ids))
        self.assertEqual(len(set(ids)), 6)
        for r in d["update_evidence"]["records"]:
            self.assertFalse(r["server_execution_verified"])
            self.assertFalse(r["baseline_core_admission"])
            self.assertIsNone(r["native_npc_id"])
        self.assertFalse(d["boundaries"]["jss1999_launch_or_tw10_same_build_proven"])
        self.assertIsNone(d["boundaries"]["overall_restoration_percentage"])


if __name__ == "__main__":
    unittest.main()
