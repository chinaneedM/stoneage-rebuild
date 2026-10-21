"""Speaker-qualified SA2 pet-care interview; a separate product, not an SA patch."""
import argparse
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-SA2-PET-CARE-INTERVIEW'
REPORT = ROOT / ('research/recovered/' + STEM + '-SOURCE-R1.json')
URL = 'https://www.4gamer.net/specials/stoneage2_interview/stoneage2_interview.shtml'
CONTEXT_URL = 'https://www.4gamer.net/news/history/2006.07/20060710162836detail.html'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(s):
    return re.sub(r'\s+', '', s)


class Interview(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = self.root = self.blocked = 0
        self.blocks, self.turns = [], []
        self.label, self.speaker, self.parts = None, None, []

    def flush(self):
        if self.speaker is not None:
            self.turns.append({'speaker': norm(self.speaker), 'text': norm(''.join(self.parts))})
        self.speaker, self.parts = None, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'div':
            self.depth += 1
            if a.get('class') == 'maintxt':
                require(not self.root, 'Nested interview roots')
                self.root = self.depth
                self.turns = []
        if not self.root:
            return
        if tag in ('script', 'style', 'iframe', 'noscript'):
            self.blocked += 1
        if tag == 'p' and a.get('class') in ('bold', 'bold2') and not self.blocked:
            self.flush()
            self.label = []

    def handle_endtag(self, tag):
        if self.root:
            if tag in ('script', 'style', 'iframe', 'noscript') and self.blocked:
                self.blocked -= 1
            if tag == 'p' and self.label is not None:
                self.speaker = ''.join(self.label)
                self.label = None
            if tag == 'div' and self.depth == self.root:
                self.flush()
                self.blocks.append(self.turns)
                self.root = 0
        if tag == 'div':
            self.depth -= 1

    def handle_data(self, data):
        if self.root and not self.blocked:
            if self.label is not None:
                self.label.append(data)
            elif self.speaker is not None:
                self.parts.append(data)


def section(raw):
    text = raw.decode('euc_jp', errors='strict')
    require('charset=EUC-JP' in text and 'Text by TeT' in text, 'Encoding or interview credit changed')
    p = Interview()
    p.feed(text)
    require(len(p.blocks) == 5, 'Bounded maintxt roots changed')
    turns = p.blocks[1]
    require(turns and turns[0]['speaker'] == '4Gamer：', 'Pet interview root changed')
    require('先ほど発表されたSA2' in turns[0]['text'], 'Wrong interview section')
    require('遊佐孝之氏' in text and '石川彰弘氏' in text and '長田妙子氏' in text, 'Named speakers missing')
    require('2006/07/25' in text and '2月14日' in text, 'Release-footer or introduction context changed')
    return turns


CLAIMS = (
    ('遊佐', '完全な新作として開発', ('ゲームシステム，マップ，キャラクター', 'スキルにいたるまで')),
    ('石川', 'ペットにはAIが搭載', ('育て方でペットの性格や隠しパラメータ', '変化していく')),
    ('長田', 'ペットを育てる場所', ('お部屋を大きく', '飼えるペットも増えて')),
    ('石川', 'ペット同士を交配', ('ほかの人に貸したり', '借りてきたり', '二匹のペットを仲良く', '新しい卵', '両親の資質を受け継いだ')),
    ('遊佐', 'スキルを覚えるのはペット', ('基本的にレベル制',)),
    ('石川', '連れて歩けるのは5匹まで', ('DENの大きさにもよる', '10〜15種類', '最多で20匹程度')),
    ('石川', '寿命という要素', ('天寿を全う', '「転生」という形', '復活させることもできる', '扱い方が悪いと', 'すねて家出')),
    ('石川', '通常のEメールで', ('しばらくゲームにログインしていないと', 'ゲームをしていない間も', 'つながってもらおう')),
)


def extract(raw):
    turns = section(raw)
    for speaker, anchor, clauses in CLAIMS:
        matches = [t for t in turns if anchor in t['text']]
        require(len(matches) == 1 and speaker in matches[0]['speaker'], 'Claim speaker missing/changed: ' + anchor)
        require(all(c in matches[0]['text'] for c in clauses), 'Care claim changed: ' + anchor)
    canonical = json.dumps(turns, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    return {
        'speaker_turn_core_sha256': sha(canonical), 'speaker_turn_count': len(turns),
        'product': 'StoneAge2', 'product_relation': 'SEPARATE_NEW_GAME_NOT_STONEAGE_VERSION_2_PATCH',
        'evidence_phase': 'PRE_BETA_DEVELOPER_INTERVIEW_NOT_DEPLOYMENT',
        'publication_date': None, 'presentation_month_day_as_written': '2月14日',
        'current_footer_release_date': '2006/07/25', 'footer_is_interview_publication_date': False,
        'pet_ai': {'speaker': '石川彰弘', 'influence_reported': 'UPBRINGING_CHANGES_PERSONALITY_AND_HIDDEN_PARAMETERS', 'formula_or_hidden_parameter_names': None},
        'den': {'speaker': '長田妙子', 'function': 'PET_REARING_SPACE', 'larger_rooms_allow_more_pets': True, 'room_size_to_capacity_table': None},
        'breeding': {'speaker': '石川彰弘', 'flow': ['LEND_OR_BORROW_PETS_AS_EXAMPLES', 'MAKE_TWO_PETS_GET_ALONG', 'NEW_EGG', 'CHILD_INHERITS_PARENT_QUALITIES'], 'exact_inheritance_compatibility_cost_time': None},
        'skills': {'speaker': '遊佐孝之', 'learner_reported': 'PETS', 'skill_roster_or_player_has_no_actions_proven': None},
        'capacity': {'speaker': '石川彰弘', 'walking_max_reported': 5, 'walking_unit': '匹', 'den_range_reported': [10, 15], 'den_unit_as_written': '種類', 'den_depends_on_size': True, 'combined_approximate_reported': 20, 'combined_unit_as_written': '匹程度', 'exact_species_total': None, 'types_to_individual_slots_equivalence_proven': False},
        'lifespan_rebirth': {'speaker': '石川彰弘', 'lifespan_reported': True, 'revival_through_rebirth_reported_possible': True, 'exact_duration_clock_cost_and_preserved_state': None},
        'runaway': {'speaker': '石川彰弘', 'cause_reported': 'BAD_TREATMENT_MAY_RESULT_IN_SULKING_AND_LEAVING', 'threshold_probability_and_return_rules': None},
        'notification': {'speaker': '石川彰弘', 'trigger_reported': 'PLAYER_NOT_LOGGING_IN_FOR_A_WHILE', 'channel_reported': 'ORDINARY_EMAIL_NOT_GAME_MAIL', 'purpose_stated': 'KEEP_PLAYER_CONNECTED_TO_WORLD_WHILE_NOT_PLAYING', 'delay_content_delivery_guarantee_or_consent_rules': None, 'message_sent_by_project': False},
        'early_stoneage_rules_transferred': False, 'historical_game_executed': False,
    }


class ContextText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.links = [], []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs).get('href'))

    def handle_data(self, data):
        self.parts.append(data)


def context_extract(raw):
    text = raw.decode('cp932', errors='strict')
    require('2006/07/10 16:28' in text, 'Context article publication changed')
    bodies = re.findall(r'<!-- 本文開始 -->(.*?)<!-- 本文終了 -->', text, re.S)
    parser = ContextText()
    parser.feed(''.join(bodies))
    core = norm(''.join(parser.parts))
    require('2006年2月に収録したもの' in core, 'Recording month claim changed')
    require('別のタイトルとして同時に運営される' in core, 'Separate-title context changed')
    link = URL.replace('https://', 'http://')
    require(parser.links.count(link) == 1, 'Actual link does not identify this interview')
    return {'core_sha256': sha(core.encode()), 'recorded_month_reported': '2006-02',
            'context_article_publication': '2006-07-10 16:28',
            'actual_interview_link_as_written': link,
            'authority': 'LATER_CONTEMPORANEOUS_MEDIA_REPORT_BY_TET_NOT_INTERVIEW_SPEAKER',
            'concurrent_separate_titles_reported': True, 'exact_interview_publication_date': None}


CONTEXT_MUTATIONS = (
    ('recorded-month', '2006年2月に収録', '2006年3月に収録'),
    ('product-separation', '別のタイトルとして同時に運営される', '同じタイトルの更新として運営される'),
    ('linked-interview-identity', 'http://www.4gamer.net/specials/stoneage2_interview/stoneage2_interview.shtml', 'http://www.4gamer.net/specials/other_interview/other.shtml'),
)


def context_audit(raw, expected):
    text = raw.decode('cp932')
    checks = []
    for label, old, new in CONTEXT_MUTATIONS:
        require(text.count(old) == 1, 'Nonunique context mutation')
        modified = text.replace(old, new, 1).encode('cp932')
        try:
            x = context_extract(modified)
            x.pop('core_sha256')
            target = dict(expected)
            target.pop('core_sha256')
            rejected = x != target
        except ValueError:
            rejected = True
        require(rejected, 'Context semantic change accepted')
        checks.append({'case': label, 'input_sha256': sha(modified), 'rejected_without_digest_gate': True})
    require(context_extract(raw + b'<script>outer change</script>') == expected, 'Outer context changed')
    return {'real_source_mutations': checks, 'outer_script_positive': True}


def validate(r):
    require(r['schema'] == 'stoneage.sa2_pet_care_interview.source_contract.r1', 'Schema')
    require(r['source']['url'] == URL and r['source']['authority'] == 'NAMED_DEVELOPER_AND_PRODUCER_INTERVIEW_PUBLISHED_BY_4GAMER', 'Source authority')
    require(r['source']['authenticated_historical_original_bytes'] is False, 'Current source promoted')
    local = json.loads((ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_text())
    require(r['extracted'] == local['extracted'], 'Product/phase/speaker/unknown boundary changed')
    require(r['source']['core_sha256'] == r['extracted']['speaker_turn_core_sha256'], 'Core pin')
    require(r['recording_context'] == local['recording_context'] and r['source']['context_url'] == CONTEXT_URL, 'Recording context boundary')
    require(len(r['records']) == 8 and len({x['record_id'] for x in r['records']}) == 8, 'Bounded records')
    require([x['speaker'] for x in r['records']] == ['遊佐孝之', '石川彰弘', '長田妙子', '石川彰弘', '遊佐孝之', '石川彰弘', '石川彰弘', '石川彰弘'], 'Record speaker attribution')
    for x in r['records']:
        require(x['version_profile'] == 'SEPARATE_OFFICIAL_PRODUCT:JP_STONEAGE2_PREBETA_INTERVIEW' and x['game_ids'] is None, 'Product or original ID promoted')
    require(all(x is False for x in r['unproven'].values()), 'Unproven claim promoted')
    require(r['status'] == {'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'}, 'Stage')
    require(r['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-47', 'Queue')


MUTATIONS = (
    ('separate-product', '完全な新作として開発', '同じゲームの更新として開発'),
    ('developer-attribution', '石川彰弘氏', '別人彰弘氏'),
    ('personality-upbringing', '育て方でペットの性格', '生まれた時のペットの性格'),
    ('hidden-parameters', '隠しパラメータ', '公開パラメータ'),
    ('room-capacity-direction', '飼えるペットも増えて', '飼えるペットも減って'),
    ('breeding-parent-number', '二匹のペットを仲良く', '三匹のペットを仲良く'),
    ('parent-qualities', '両親の資質を受け継いだ', '両親の資質を受け継がない'),
    ('skill-learner', 'スキルを覚えるのはペット', 'スキルを覚えるのはプレイヤー'),
    ('walking-limit', '連れて歩けるのは5匹まで', '連れて歩けるのは6匹まで'),
    ('den-unit', '10〜15種類', '10〜15匹'),
    ('approximate-not-exact', '最多で20匹程度', '最多で20匹固定'),
    ('lifespan', '寿命という要素', '不死という要素'),
    ('rebirth-possible', '復活させることもできる', '復活させることはできない'),
    ('runaway-care-condition', '扱い方が悪いと', '扱い方が良いと'),
    ('absence-trigger', 'しばらくゲームにログインしていないと', '毎日ゲームにログインしていると'),
    ('email-channel', '通常のEメールで', 'ゲーム内メールで'),
)


def audit(raw, expected):
    text = raw.decode('euc_jp')
    checks = []
    for label, old, new in MUTATIONS:
        require(text.count(old) == 1, 'Nonunique mutation: ' + label)
        modified = text.replace(old, new, 1).encode('euc_jp')
        try:
            x = extract(modified)
            x.pop('speaker_turn_core_sha256')
            target = dict(expected)
            target.pop('speaker_turn_core_sha256')
            rejected = x != target
        except ValueError:
            rejected = True
        require(rejected, 'Semantic change accepted: ' + label)
        checks.append({'case': label, 'input_sha256': sha(modified), 'rejected_without_digest_gate': True})
    require(extract(raw + b'<script>outer change</script>') == expected, 'Outer script changed core')
    return {'real_source_mutations': checks, 'outer_script_positive': True}


def replay(r, raw, context_raw):
    validate(r)
    require(extract(raw) == r['extracted'], 'Core or semantics changed')
    require(context_extract(context_raw) == r['recording_context'], 'Recording-context core changed')
    return {'schema': 'stoneage.sa2_pet_care_interview.derived_replay.r1', 'http_bytes': len(raw), 'http_sha256': sha(raw),
            'extracted': extract(raw), 'audit': audit(raw, r['extracted']),
            'context_http_bytes': len(context_raw), 'context_http_sha256': sha(context_raw),
            'recording_context': context_extract(context_raw), 'context_audit': context_audit(context_raw, r['recording_context']),
            'raw_html_or_assets_in_output': False, 'historical_game_executed': False, 'message_sent': False}


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--fetch', action='store_true')
    g.add_argument('--html', type=Path)
    p.add_argument('--context-html', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if a.fetch:
        with urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
            require(response.status == 200, 'HTTP failed')
            raw = response.read(1000001)
            require(len(raw) <= 1000000, 'Source oversized')
    else:
        raw = a.html.read_bytes()
    if a.fetch:
        with urllib.request.urlopen(urllib.request.Request(CONTEXT_URL, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
            require(response.status == 200, 'Context HTTP failed')
            context_raw = response.read(1000001)
            require(len(context_raw) <= 1000000, 'Context oversized')
    else:
        if a.context_html is None:
            p.error('--context-html is required with --html')
        context_raw = a.context_html.read_bytes()
    out = replay(json.loads(REPORT.read_text()), raw, context_raw)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'success': True, 'http_bytes': len(raw), 'speaker_turns': out['extracted']['speaker_turn_count'], 'context_http_bytes': len(context_raw), 'semantic_mutations': len(out['audit']['real_source_mutations']) + len(out['context_audit']['real_source_mutations'])}))


if __name__ == '__main__':
    main()
