"""Synthetic FAQ fixtures exercise attribution, scope and source rejection."""
import json
from pathlib import Path
import unittest

from tools import stoneage_jss_pet_faq as faq


def menu():
    groups = [["synthetic question"] * n for n in (12, 16, 4, 9)]
    groups[0][4] = "敵やペット"
    groups[2][3] = "スクリーンショット"
    groups[3] = [" ".join(tokens) for _, tokens in faq.FIXED]
    links = ''.join(f'<a href="{p}.html">synthetic category</a>' for p in ('faqgame', 'faqstart', 'faqquest'))
    return links + '修正された不具合' + ''.join('<blockquote>' + ''.join('●' + q + '<br>' for q in g) + '</blockquote>' for g in groups)


def detail():
    pairs = [["synthetic question", "synthetic answer"] for _ in range(12)]
    pairs[1] = ["ヤン＝ミト クエスト", "現在調査中"]
    pairs[4] = ["敵やペット 表示されません", "再インストール アンインストール フォルダ 削除"]
    pairs[5] = ["建物や洞窟 入れない", "現在調査 報告 MAPウィンドウ ログイン"]
    pairs[7] = ["効果音", "ハードウェアアクセラレータ 基本 なし"]
    pairs[9] = ["DP 強者表", "デュエルを行うと更新"]
    pairs[10] = ["フルカラー ウィンドウモード", "時刻に応じた色の変化 パレット機能 256色のみ"]
    return ''.join(f'<p>Q:{q}<br>A:{a}</p>' for q, a in pairs) + '<a href="sa_se.lzh">archive</a>'


class FaqBoundaries(unittest.TestCase):
    def test_all_menu_headings_accounted_for(self):
        r = faq.menu_contract(menu())
        self.assertEqual(r['category_question_counts'], [12, 16, 4, 9])
        self.assertEqual(sum(map(len, r['category_heading_fingerprints'])), 41)

    def test_fixed_labels_do_not_prove_fix_execution_or_date(self):
        r = faq.menu_contract(menu())
        self.assertEqual(len(r['fixed_issues']), 9)
        for row in r['fixed_issues']:
            self.assertIsNone(row['fix_date'])
            self.assertFalse(row['fix_independently_executed'])
            self.assertFalse(row['script_or_formula_recovered'])

    def test_quest_filename_not_used_as_game_quest_source(self):
        r = faq.menu_contract(menu())
        self.assertFalse(r['faqquest_filename_is_quest_guide_proof'])
        self.assertFalse(r['faqquest_destination_queried'])
        self.assertEqual(r['selected_detail_url'], faq.ROOT + 'faqgame.html')

    def test_commented_and_script_links_are_not_followed(self):
        r = faq.menu_contract(menu() + '<!-- <a href="trap.html">x</a> --><script><a href="trap.html">x</a></script>')
        self.assertEqual(len(r['category_links']), 3)

    def test_actual_fixed_heading_cannot_be_supplied_by_comment(self):
        with self.assertRaises(ValueError):
            faq.menu_contract(menu().replace('修正された不具合', '<!-- 修正された不具合 -->'))

    def test_fixed_issue_attribution_cannot_move_to_another_row(self):
        with self.assertRaises(ValueError):
            faq.menu_contract(menu().replace('預けたペット', 'unrelated row'))

    def test_missing_heading_fails_coverage(self):
        with self.assertRaises(ValueError):
            faq.menu_contract(menu().replace('●synthetic question<br>', '', 1))

    def test_quest_investigation_remains_unresolved(self):
        r = faq.detail_contract(detail())
        self.assertEqual(r['yan_mito_quest']['operator_status'], 'UNDER_INVESTIGATION')
        self.assertIsNone(r['yan_mito_quest']['npc_id'])
        self.assertFalse(r['yan_mito_quest']['fix_proven'])

    def test_answer_cannot_be_borrowed_from_other_question(self):
        with self.assertRaises(ValueError):
            faq.detail_contract(detail().replace('A:現在調査中', 'A:fixed') + '<p>現在調査中</p>')

    def test_display_issue_is_not_pet_mechanic_or_proven_cause(self):
        r = faq.detail_contract(detail())['invisible_enemies_or_pets']
        self.assertFalse(r['client_resource_cause_proven'])
        self.assertFalse(r['pet_absence_or_invisibility_game_rule_proven'])
        self.assertFalse(r['remedy_executed'])

    def test_numeric_color_limit_and_ranking_trigger(self):
        r = faq.detail_contract(detail())
        self.assertEqual(r['windowed_color']['supported_colors_described'], 256)
        self.assertEqual(r['duel_ranking']['refresh_trigger_described'], 'PERFORM_DUEL')
        with self.assertRaises(ValueError):
            faq.detail_contract(detail().replace('256色のみ', '65536色のみ'))

    def test_download_reference_is_metadata_only(self):
        r = faq.detail_contract(detail())['download_reference']
        self.assertFalse(r['queried_or_downloaded'])
        self.assertTrue(r['url'].endswith('/sa_se.lzh'))

    def test_qualification_rejects_late_capture_wrong_url_and_bad_bytes(self):
        capture, _, _ = faq.PAGES['faqmenu']
        url = f'https://web.archive.org/web/{capture}id_/' + faq.ROOT + 'faqmenu.html'
        for candidate in (url.replace(capture, '20200101000000'), url.replace('faqmenu', 'faqquest'), url):
            with self.subTest(candidate=candidate), self.assertRaises(ValueError):
                faq.qualify(b'<HTML>FAQ</HTML>', candidate, 'faqmenu')

    def test_navigation_dependency_tampering_rejected(self):
        with self.assertRaisesRegex(ValueError, 'navigation changed'):
            faq.build({}, b'{}')

    def test_archived_report_never_promotes_missing_server_data(self):
        r = json.loads(Path('research/recovered/STONEAGE-JSS-FIRST-PARTY-PET-FAQ-R1.json').read_text())
        b = r['boundaries']
        self.assertFalse(b['original_server_executed'])
        self.assertFalse(b['pet_species_master_or_growth_formula_recovered'])
        self.assertFalse(b['jss1999_or_tw10_build_identity_proven'])
        self.assertFalse(b['proprietary_html_images_audio_or_binaries_retained_in_git'])
        self.assertEqual(b['detail_pages_followed'], 1)
        self.assertFalse(r['source_temporality']['snapshot_dates_are_fix_or_release_dates'])


if __name__ == '__main__':
    unittest.main()
