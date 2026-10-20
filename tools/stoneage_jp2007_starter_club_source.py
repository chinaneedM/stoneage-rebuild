"""Read one dated source; separate operator quotation from editorial guidance."""
import argparse
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-JP2007-STARTER-CLUB-SOURCE-R1.json'
URL = 'https://www.4gamer.net/news/history/2007.02/20070202173939detail.html'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def normalize(text):
    return re.sub(r'\s+', '', text)


class Sections(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.quote_depth = None
        self.blocked = 0
        self.visible = []
        self.quotes = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.blocked += 1
        if tag == 'span':
            self.depth += 1
            if 'blockquote' in dict(attrs).get('class', '').split():
                require(self.quote_depth is None, 'Nested quotation ambiguous')
                self.quote_depth = self.depth
                self.quotes.append([])

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.blocked:
            self.blocked -= 1
        if tag == 'span':
            if self.depth == self.quote_depth:
                self.quote_depth = None
            self.depth -= 1

    def handle_data(self, data):
        if not self.blocked:
            self.visible.append(data)
            if self.quote_depth is not None:
                self.quotes[-1].append(data)


def sections(raw):
    # The page declares Shift-JIS. CP932 is its compatible Windows decoder.
    text = raw.decode('cp932', errors='strict')
    require('charset=shift_jis' in text.lower(), 'Source encoding declaration changed')
    start = '<!-- tDialy:TITLE='
    end = '<!-- tDialy:END -->'
    require(text.count(start) == text.count(end) == 1, 'Article boundary missing/ambiguous')
    article = text.split(start, 1)[1].split(end, 1)[0]
    parser = Sections()
    parser.feed(article)
    require(len(parser.quotes) == 2, 'Expected two release quotation spans')
    visible = normalize(''.join(parser.visible))
    marker = '以下，リリースより'
    require(visible.count(marker) == 1, 'Release attribution boundary changed')
    editorial = visible.split(marker)[0]
    quoted = normalize(''.join(''.join(x) for x in parser.quotes))
    require('2007/02/0217:39' in editorial, 'Publication timestamp changed')
    return quoted, editorial


def one(pattern, text, message):
    matches = re.findall(pattern, text)
    require(len(matches) == 1, message)
    return matches[0]


def extract(raw):
    q, e = sections(raw)
    require('アイテム名：『始まりのこん棒』' in q, 'Named item missing')
    stats = one(r'装備効果：攻撃力\+([0-9]+)俊敏力\+([0-9]+)？\+([0-9]+)(?![0-9])', q, 'Exact three stats required')
    skill = one(r'(猛毒の精霊)Lv([0-9]+)を使うことができる（消費気力：([0-9]+)）', q, 'Skill level/cost required')
    require('装備カテゴリー：武器' in q, 'Weapon category missing')
    require('2月2日(金)17:00～※恒久的に設置' in q, 'Distribution schedule/status changed')
    require('戦闘中に相手を毒の状態異常にする呪術' in q, 'Poison effect missing')
    require('気力を消費しないため、何度でも使用することができる' in q, 'Repeated use description missing')
    require('ある「隠しステータス」の数値が１上がる' in q, 'Hidden statistic uncertainty missing')
    require('Gストーンと呼ばれる仮想貨幣を購入' in q, 'Purchased virtual currency missing')
    require('ランダムに中身のペットが変わる『恐竜の袋』『恐竜王の袋』' in q, 'Random pet-bag scope changed')
    require('ハンゲームサイト内「便利商店」が同機能のアイテムモール' in q, 'Portal variant missing')
    require('無料配布を開始する' in e, 'Editorial free claim missing')
    route = ('マンモストア', '発行されたアイテムコードを入力', 'ゲーム内で「便利商店スタッフ」に話しかけ')
    positions = [e.find(x) for x in route]
    require(all(p >= 0 for p in positions) and positions == sorted(positions), 'Editorial route changed')
    return {
        'operator': {
            'item': '始まりのこん棒', 'category': 'WEAPON',
            'attack_bonus': int(stats[0]), 'agility_bonus': int(stats[1]),
            'unnamed_stat_bonus': int(stats[2]), 'hidden_stat_name': None,
            'spell': skill[0], 'spell_level': int(skill[1]), 'spell_vigor_cost': int(skill[2]),
            'spell_effect': 'POISON_OPPONENT_DURING_BATTLE',
            'repeat_use_claim': 'REPEATED_USE_BECAUSE_NO_VIGOR_COST',
            'distribution_start_as_announced': '2007-02-02 17:00',
            'permanent_distribution_claim': True,
            'mall': 'マンモストア', 'hangame_mall': '便利商店',
            'currency_as_written': 'Gストーン', 'currency_acquired_by_purchase': True,
            'random_pet_bags': ['恐竜の袋', '恐竜王の袋']},
        'editorial': {
            'free_item_reported': True,
            'reported_sequence': ['WEB_MALL', 'ISSUED_ITEM_CODE_INPUT', 'IN_GAME_NPC_TALK'],
            'npc_name_as_written': '便利商店スタッフ',
            'code_input_location': None, 'original_npc_id': None,
            'is_operator_quote': False},
        'quote_sha256': digest(q.encode()), 'editorial_sha256': digest(e.encode())}


def validate(report):
    require(report['schema'] == 'stoneage.jp2007_starter_club.source_contract.r1', 'Schema changed')
    require(report['source']['url'] == URL, 'Source changed')
    require(report['source']['historical_2007_bytes_authenticated'] is False, 'Current HTML promoted to historical bytes')
    x = report['extracted']['operator']
    require((x['attack_bonus'], x['agility_bonus'], x['unnamed_stat_bonus']) == (9, 1, 1), 'Documented bonuses changed')
    require(x['hidden_stat_name'] is None, 'Unknown hidden statistic invented')
    require((x['spell_level'], x['spell_vigor_cost']) == (1, 0), 'Skill level/cost changed')
    require(report['extracted']['editorial']['is_operator_quote'] is False, 'Editorial promoted to primary quotation')
    require(report['extracted']['editorial']['code_input_location'] is None, 'Code-entry UI invented')
    for record in report['records']:
        require(record['version_profile'] == 'LATER_OFFICIAL:JP_GAIAX_2007', 'Wrong region/version')
        require(record['game_ids'] is None, 'Original ID invented')
    require(len(report['records']) == 6, 'Finite archive scope changed')
    require(all(v is False for v in report['unproven'].values()), 'Unproven boundary upgraded')
    require(report['status'] == {'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'}, 'Stage status changed')


def replay(report, raw):
    validate(report)
    extracted = extract(raw)
    require(extracted == report['extracted'], 'Source semantics or scoped source digest changed')
    return {'schema': 'stoneage.jp2007_starter_club.derived_replay.r1',
            'source_url': URL, 'http_bytes': len(raw), 'http_sha256': digest(raw),
            'extracted': extracted, 'server_execution_verified': False, 'raw_html_in_output': False}


MUTATIONS = (
    ('attack-90-not-9', '攻撃力+9', '攻撃力+90'),
    ('agility-10-not-1', '俊敏力+1', '俊敏力+10'),
    ('hidden-bonus-10-not-1', '？+1', '？+10'),
    ('vigor-1-not-0', '消費気力：0', '消費気力：1'),
    ('spell-level-10-not-1', '猛毒の精霊 Lv1', '猛毒の精霊 Lv10'),
    ('hidden-stat-remains-unnamed', '隠しステータス', '幸運ステータス'),
    ('poison-not-sleep', '毒の状態異常', '睡眠の状態異常'),
    ('permanent-not-limited', '恒久的に設置', '期間限定設置'),
    ('start-time-not-18', '17:00～', '18:00～'),
    ('gstone-not-stone', 'Gストーン', 'ストーン'),
    ('bag-not-fixed-pet', 'ランダムに中身のペットが変わる', '固定の中身のペットが出る'),
    ('editorial-npc-not-renamed', 'ゲーム内で「便利商店スタッフ」', 'ゲーム内で「別の係員」'),
    ('editorial-free-not-paid', '無料配布を開始する', '有料配布を開始する'),
)


def adversarial(report, raw):
    """Mutate real source bytes and compare semantics with the digest gates bypassed."""
    source = raw.decode('cp932', errors='strict')
    expected = {k: report['extracted'][k] for k in ('operator', 'editorial')}
    checks = []
    for name, old, new in MUTATIONS:
        require(source.count(old) == 1, 'Mutation anchor is not unique: ' + name)
        changed = source.replace(old, new, 1).encode('cp932')
        try:
            x = extract(changed)
            rejected = {k: x[k] for k in expected} != expected
        except ValueError:
            rejected = True
        require(rejected, 'Semantic mutation was accepted: ' + name)
        checks.append({'case': name, 'mutated_input_sha256': digest(changed), 'rejected_without_digest_gate': True})
    # A script outside the article must neither supply missing evidence nor change the source core.
    positive = raw + b'<script>unrelated outer layout change</script>'
    require(extract(positive) == report['extracted'], 'Outer-only positive changed source core')
    return {'real_source_mutations': checks, 'outer_script_positive': True,
            'outer_positive_http_sha256': digest(positive), 'raw_source_in_output': False}


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--fetch', action='store_true')
    g.add_argument('--html', type=Path)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.fetch:
        with urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
            require(response.status == 200, 'HTTP source unavailable')
            raw = response.read(500001)
            require(len(raw) <= 500000, 'Oversized source')
    else:
        raw = args.html.read_bytes()
    report = json.loads(REPORT.read_text())
    result = replay(report, raw)
    result['adversarial'] = adversarial(report, raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'success': True, 'http_bytes': len(raw), 'quote_sha256': result['extracted']['quote_sha256']}))


if __name__ == '__main__':
    main()
