"""Source-dated pet changes, without inventing builds or exact bug matches."""
import argparse
from datetime import date
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

from tools.stoneage_jss_pet_faq import ROOT, NAV, NAV_SHA, compact, fingerprint, parse, require

CAPTURE = "20010417162544"
URL = f"https://web.archive.org/web/{CAPTURE}id_/" + ROOT + "verup.html"
SHA = "ba71d859f34f31261f4293dc61583c53a8e77133898c4a8148c544a452abc3cb"
FAQ = "research/recovered/STONEAGE-JSS-FIRST-PARTY-PET-FAQ-R1.json"
FAQ_SHA = "38ebbeca6b04d4a3a229da8ac117e76bc083fcd6e03b7ece6db660b58cf153b0"


class Changes(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows, self.header, self.body = [], None, None
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        if self.hidden:
            return
        if tag == 'li':
            require(self.body is None, 'overlapping update entries')
            self.header = []
        elif tag == 'blockquote' and self.header is not None:
            require(self.body is None, 'nested update body')
            self.body = []
        elif tag in ('br', 'dd'):
            self.handle_data(' ')

    def handle_data(self, data):
        if not self.hidden:
            if self.body is not None:
                self.body.append(data)
            elif self.header is not None:
                self.header.append(data)

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.hidden:
            self.hidden -= 1
        elif not self.hidden and tag == 'blockquote' and self.body is not None:
            label, text = compact(''.join(self.header)), compact(''.join(self.body))
            match = re.fullmatch(r'(\d{4})/(\d{1,2})/(\d{1,2})（([月火水木金土日])）', label)
            require(match is not None, 'unrecognized original update date')
            year, month, day = map(int, match.group(1, 2, 3))
            actual = date(year, month, day)
            weekday = match.group(4)
            self.rows.append({'date_as_written': label, 'date': actual.isoformat(), 'weekday_as_written': weekday,
                              'calendar_weekday': '月火水木金土日'[actual.weekday()],
                              'weekday_matches_calendar': weekday == '月火水木金土日'[actual.weekday()], 'text': text})
            self.header, self.body = None, None


def change_rows(document):
    parser = Changes()
    parser.feed(document)
    parser.close()
    require(parser.body is None, 'unterminated update entry')
    return parser.rows


def pet_changes(rows):
    def entry(day, *tokens):
        found = [(i, r) for i, r in enumerate(rows) if r['date'] == day and all(t in r['text'] for t in tokens)]
        require(len(found) == 1, 'missing or ambiguous dated pet assertion')
        return {'source_order': found[0][0], 'source_date': day, 'build_number': None}
    boarding = entry('2000-01-31', '始まりの村', 'ペットショップ', '預けれる')
    arena = entry('2000-02-07', '闘技場', 'ペット預かり屋', '預けたペットの技', '修正')
    duel = entry('2000-01-25', 'DUEL', '旅は道連れとペット入れ替え', '修正')
    earth = entry('1999-10-25', '地球一周', '不具合を修正')
    mail_hold = entry('1999-10-25', '戻ってくる前にログアウト', '12時間', '他の人に拾われなく', '以内にログイン', 'プレイヤーの元に帰って')
    mail_return = entry('1999-10-26', 'ペットメールで戻ってきたペット', '5分で野良ペット')
    skills = entry('1999-11-08', 'ペットの技を追加', 'アイテム合成、調理')
    return {'starting_village_pet_shop_boarding_added': boarding,
            'arena_boarding_added_and_boarded_pet_skill_bug_fix': {**arena, 'faq_join': 'MATCH_FEATURE_AND_DEFECT_FAMILY_NOT_EXACT_SYMPTOM', 'faq_skill_loss_exact_fix_identity_proven': False},
            'duel_companion_and_pet_swap_bug_fix': {**duel, 'faq_join': 'NAMED_SKILL_AND_DUEL_FAMILY_NOT_EXACT_HANG_SYMPTOM'},
            'earth_tour_skill_bug_fix': {**earth, 'faq_join': 'NAMED_SKILL_ONLY_NOT_EXACT_COUNTER_HANG_SYMPTOM'},
            'pet_mail_logout_before_return': {**mail_hold, 'not_pickable_by_others_hours': 12, 'login_within_hours_returns_to_player': 12, 'all_ground_pets_share_this_timer_proven': False},
            'returned_pet_mail_pet_becomes_stray': {**mail_return, 'minutes_as_described': 5, 'all_dropped_pets_share_this_timer_proven': False, 'same_context_as_previous_day_logout_rule_assumed': False},
            'pet_skills_added': {**skills, 'skill_categories': ['ITEM_SYNTHESIS', 'COOKING'], 'recipe_or_skill_id_table_recovered': False}}


def build(raw, final_url, navigation_raw, faq_raw):
    require(final_url == URL, 'unexpected update source URL or actual capture')
    require(len(raw) == 11239 and hashlib.sha256(raw).hexdigest() == SHA, 'update source bytes changed')
    require(hashlib.sha256(navigation_raw).hexdigest() == NAV_SHA, 'navigation source changed')
    require(hashlib.sha256(faq_raw).hexdigest() == FAQ_SHA, 'FAQ comparison source changed')
    nav = json.loads(navigation_raw)['targets']['jss_top']
    require(any(x['target_url'] == ROOT + 'verup.html' for x in nav['links']), 'no authenticated update edge')
    text = raw.decode('shift_jis', errors='strict')
    doc, rows = parse(text), change_rows(text)
    require('STONEAGE' in doc.text and len(rows) == 40, 'update identity or dated coverage changed')
    require([r['date'] for r in rows] == sorted([r['date'] for r in rows], reverse=True), 'chronological order changed')
    require(rows[0]['date'] == '2000-09-11' and rows[-1]['date'] == '1999-10-18', 'date range changed')
    require(sum(r['date'] == '1999-12-20' for r in rows) == 2, 'same-day distinct records were collapsed')
    require(doc.links == [ROOT + 'updater.html', ROOT + 'manual.html'], 'actual update links changed')
    unlocated = {name: {'label_present_in_this_page': name in doc.text, 'fix_date': None, 'global_absence_established': False} for name in ('カナン', 'ククロス', 'ヤン＝ミト')}
    require(not any(x['label_present_in_this_page'] for x in unlocated.values()), 'named quest now present; requalify match')
    changes = pet_changes(rows)
    index = [{k: v for k, v in row.items() if k != 'text'} | {'source_order': i, 'body_fingerprint': fingerprint(row['text'])} for i, row in enumerate(rows)]
    return {'schema': 'stoneage.jss.pet_patch_history.r1', 'source': {'original_url': ROOT + 'verup.html', 'actual_capture': CAPTURE, 'final_url': URL, 'bytes': len(raw), 'sha256': SHA, 'codec': 'shift_jis'},
            'dependencies': [{'path': NAV, 'sha256': NAV_SHA}, {'path': FAQ, 'sha256': FAQ_SHA}],
            'dated_entry_count': 40, 'dated_index': index, 'pet_changes': changes, 'unlocated_specific_quest_labels': unlocated,
            'weekday_conflicts': [x for x in index if not x['weekday_matches_calendar']],
            'unfollowed_links': doc.links, 'additional_detail_or_binary_downloaded': False,
            'boundaries': {'dates_are_operator_written_history_not_independently_observed_deployment': True, 'capture_is_2001_not_1999': True,
                           'version_numbers_recovered': False, 'all40_entries_semantically_restored': False, 'original_server_or_timer_executed': False,
                           'faq_exact_bug_fix_join_proven': False, 'jss_launch_or_tw10_same_build_proven': False,
                           'quest_scripts_species_ids_or_growth_formulas_recovered': False, 'proprietary_originals_retained_in_git': False,
                           'stage_b_production': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    final = URL
    if args.input:
        raw = args.input.read_bytes()
    else:
        with urlopen(Request(URL, headers={'User-Agent': 'StoneAge-Historical-Research/1.0'}), timeout=60) as response:
            raw, final = response.read(), response.url
    result = build(raw, final, Path(NAV).read_bytes(), Path(FAQ).read_bytes())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'dated_entries': 40, 'selected_pet_change_contracts': 7, 'exact_faq_fix_join_proven': False}))


if __name__ == '__main__':
    main()
