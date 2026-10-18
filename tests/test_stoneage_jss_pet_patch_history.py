import json
from pathlib import Path
import unittest
from tools import stoneage_jss_pet_patch_history as patch


def pet_rows():
    values = [
        ('2000-01-31', '始まりの村 ペットショップ 預けれる'),
        ('2000-02-07', '闘技場 ペット預かり屋 預けたペットの技 修正'),
        ('2000-01-25', 'DUEL 旅は道連れとペット入れ替え 修正'),
        ('1999-10-25', '地球一周 不具合を修正 戻ってくる前にログアウト 12時間 他の人に拾われなく 以内にログイン プレイヤーの元に帰って'),
        ('1999-10-26', 'ペットメールで戻ってきたペット 5分で野良ペット'),
        ('1999-11-08', 'ペットの技を追加 アイテム合成、調理'),
    ]
    return [{'date': d, 'text': t} for d, t in values]


class PatchEvidence(unittest.TestCase):
    def test_same_day_blocks_not_collapsed(self):
        rows = patch.change_rows('<li>1999/12/20（月）<blockquote>one</blockquote><li>1999/12/20（月）<blockquote>two</blockquote>')
        self.assertEqual(len(rows), 2)
        self.assertEqual([x['text'] for x in rows], ['one', 'two'])

    def test_weekday_conflict_is_preserved_not_corrected(self):
        row = patch.change_rows('<li>1999/11/9（金）<blockquote>synthetic</blockquote>')[0]
        self.assertEqual(row['weekday_as_written'], '金')
        self.assertEqual(row['calendar_weekday'], '火')
        self.assertFalse(row['weekday_matches_calendar'])
        self.assertEqual(row['date_as_written'], '1999/11/9（金）')

    def test_commented_dates_and_script_claims_ignored(self):
        rows = patch.change_rows('<!-- <li>1999/1/1（金）<blockquote>fake</blockquote> --><li>2000/2/7（月）<blockquote>real<script>fake claim</script></blockquote>')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['text'], 'real')

    def test_unterminated_body_rejected(self):
        with self.assertRaises(ValueError):
            patch.change_rows('<li>2000/2/7（月）<blockquote>incomplete')

    def test_pet_mail_timers_have_different_qualifying_contexts(self):
        changes = patch.pet_changes(pet_rows())
        hold = changes['pet_mail_logout_before_return']
        returned = changes['returned_pet_mail_pet_becomes_stray']
        self.assertEqual(hold['not_pickable_by_others_hours'], 12)
        self.assertEqual(returned['minutes_as_described'], 5)
        self.assertFalse(hold['all_ground_pets_share_this_timer_proven'])
        self.assertFalse(returned['all_dropped_pets_share_this_timer_proven'])
        self.assertFalse(returned['same_context_as_previous_day_logout_rule_assumed'])

    def test_numeric_timer_change_requires_new_source_contract(self):
        rows = pet_rows()
        rows[4]['text'] = rows[4]['text'].replace('5分', '6分')
        with self.assertRaises(ValueError):
            patch.pet_changes(rows)

    def test_source_date_not_borrowed_from_adjacent_entry(self):
        rows = pet_rows()
        rows[1]['date'] = '2000-02-08'
        with self.assertRaises(ValueError):
            patch.pet_changes(rows)

    def test_generic_skill_bug_not_exact_faq_loss_fix(self):
        r = patch.pet_changes(pet_rows())['arena_boarding_added_and_boarded_pet_skill_bug_fix']
        self.assertFalse(r['faq_skill_loss_exact_fix_identity_proven'])
        self.assertIsNone(r['build_number'])

    def test_duplicate_matching_date_is_ambiguous(self):
        rows = pet_rows()
        with self.assertRaises(ValueError):
            patch.pet_changes(rows + [rows[0]])

    def test_wrong_source_url_and_bytes_rejected(self):
        for url in (patch.URL.replace('verup', 'updater'), patch.URL):
            with self.subTest(url=url), self.assertRaises(ValueError):
                patch.build(b'fake source', url, b'{}', b'{}')

    def test_report_keeps_specific_quest_and_runtime_unknowns(self):
        r = json.loads(Path('research/recovered/STONEAGE-JSS-PET-PATCH-HISTORY-R1.json').read_text())
        self.assertEqual(r['dated_entry_count'], 40)
        self.assertEqual(len(r['weekday_conflicts']), 1)
        self.assertFalse(r['additional_detail_or_binary_downloaded'])
        for value in r['unlocated_specific_quest_labels'].values():
            self.assertFalse(value['label_present_in_this_page'])
            self.assertFalse(value['global_absence_established'])
            self.assertIsNone(value['fix_date'])
        for key in ('version_numbers_recovered', 'all40_entries_semantically_restored', 'original_server_or_timer_executed', 'faq_exact_bug_fix_join_proven', 'jss_launch_or_tw10_same_build_proven'):
            self.assertFalse(r['boundaries'][key])


if __name__ == '__main__':
    unittest.main()
