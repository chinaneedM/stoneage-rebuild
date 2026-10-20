"""One 2005 Japanese map notice; descriptions, editorial claims and later names stay distinct."""
import argparse
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-JP2005-SPECIAL-MAPS-SOURCE-R1.json'
URL = 'https://www.4gamer.net/games/013/G001377/20051129193618/'
LATER = 'research/recovered/STONEAGE-JP2009-GUILD-HAKUEN-SOURCE-R1.json'
NAMES = ['巨獣の島', '閉ざされた氷窟', 'バルツ山の洞窟']


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def compact(s):
    return re.sub(r'\s+', '', s)


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.visible, self.quotes = [], []
        self.span_depth, self.quote_depth, self.blocked = 0, None, 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.blocked += 1
        if tag == 'span':
            self.span_depth += 1
            if 'blockquote' in dict(attrs).get('class', '').split():
                require(self.quote_depth is None, 'Nested quotation')
                self.quote_depth = self.span_depth
                self.quotes.append([])

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.blocked:
            self.blocked -= 1
        if tag == 'span':
            if self.quote_depth == self.span_depth:
                self.quote_depth = None
            self.span_depth -= 1

    def handle_data(self, data):
        if not self.blocked:
            self.visible.append(data)
            if self.quote_depth is not None:
                self.quotes[-1].append(data)


def extract(raw):
    p = Text()
    p.feed(raw.decode('utf-8-sig', errors='strict'))
    t = compact(''.join(p.visible))
    require('2005/11/2919:36' in t, 'Publication timestamp missing')
    require(t.count('以下，リリースより') == 1 and len(p.quotes) == 1, 'Quote boundary/attribution ambiguous')
    q = compact(''.join(p.quotes[0]))
    headings = re.findall(r'ダンジョン([１２３])：(.+?)向けマップ【(.+?)】', q)
    require(headings == [('１', '初級者', NAMES[0]), ('２', '中級者', NAMES[1]), ('３', '上級者', NAMES[2])], 'Three named map tiers/order changed')
    clauses = (
        '最近漁師によって発見された小さな島', '素早さが低い竜脚類系', 'パーティーでの戦闘が比較的楽',
        '氷に閉ざされた洞窟', 'ここでしか入手できない犬型恐竜（親犬）',
        '親犬を複数集めると', '子犬型恐竜がもらえるクエスト',
        '遥か昔に存在していた“バルツ山”の跡地', '生き残りが多数生息',
        '現時点では最強レベル', '高レベルプレイヤー向け', 'ここにしか出現しない強力なボス',
        'アイテムが手に入る可能性')
    require(all(c in q for c in clauses), 'Material map/quest/narrative or uncertainty changed')
    intro_start = 'ガイアックスは，同社が運営している'
    require(t.count(intro_start) == 1 and t.count('（aueki）') == 1, 'Editorial boundaries changed')
    intro = t.split(intro_start, 1)[1].split('以下，リリースより', 1)[0].strip('＃')
    conclusion = t.split(q, 1)[1].split('（aueki）', 1)[0].lstrip('＃')
    require('12月2日から基本プレイ無料化' in intro, 'Editorial date changed')
    require('「便利商店」で購入できるチケットがないと入れない' in intro, 'Editorial admission changed')
    require('特殊マップには3種類' in intro, 'Editorial map count changed')
    require('マップを買っていないプレイヤーがパーティを組みにくい' in conclusion and '問題も懸念される' in conclusion, 'Editorial concern changed')
    return {'map_names': NAMES, 'tier_labels_as_written': ['初級者', '中級者', '上級者'],
            'operator_quote_sha256': sha(q.encode()), 'editorial_intro_sha256': sha(intro.encode()),
            'editorial_comment_sha256': sha(conclusion.encode()),
            'map1': {'discovery': 'RECENT_FISHER_DISCOVERY_NO_ABSOLUTE_IN_WORLD_DATE', 'ecology': 'LOW_AGILITY_SAUROPOD_TYPE', 'party_hunting': 'RELATIVELY_EASY_AS_DESCRIBED'},
            'map2': {'ecology': 'ICE_CAVE_AND_PARENT_DOG_TYPE', 'parent_dog_local_exclusivity_claim': True,
                     'quest': 'COLLECT_MULTIPLE_PARENT_DOGS_FOR_PUPPY_TYPE', 'required_parent_quantity': None, 'pet_species_ids': None},
            'map3': {'history': 'CAVE_AT_ANCIENT_MOUNTAIN_REMAINS_WITH_SURVIVING_DINOSAURS',
                     'strength': 'STRONGEST_LEVEL_AT_TIME_OF_NOTICE_NOT_NUMERIC_LEVEL',
                     'boss': 'LOCAL_EXCLUSIVE_UNNAMED_BOSS', 'reward': 'POSSIBLE_RARE_ITEM', 'drop_rate': None},
            'editorial': {'reported_basic_free_start': '2005-12-02', 'reported_mall_ticket_required': True,
                          'mall_name': '便利商店', 'ticket_price': None, 'ticket_consumption_or_duration': None,
                          'party_access_concern': 'EDITORIAL_SPECULATION_NOT_MEASURED_OUTCOME', 'is_operator_quote': False}}


def comparison(pin):
    b = (ROOT / LATER).read_bytes()
    require(pin['path'] == LATER and len(b) == pin['bytes'] and sha(b) == pin['sha256'], 'Later source pin changed')
    require(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == pin['git_blob'], 'Later source native Git identity changed')
    places = json.loads(b)['limited_events']['mentioned_spawns']
    require('閉ざされた氷窟' in places and 'バルツ山' in places and 'バルツ山の洞窟' not in places, 'Later literal place scope changed')
    return [{'earlier': NAMES[1], 'later': '閉ざされた氷窟', 'relation': 'LITERAL_NAME_RECURRENCE_IDENTITY_UNPROVEN'},
            {'earlier': NAMES[2], 'later': 'バルツ山', 'relation': 'DISTINCT_LABELS_NOT_AUTOMATIC_ALIASES'}]


def validate(r):
    require(r['schema'] == 'stoneage.jp2005_special_maps.source_contract.r1', 'Schema')
    require(r['source']['url'] == URL and r['source']['original_2005_bytes_authenticated'] is False, 'Source scope')
    require(r['extracted']['map_names'] == NAMES, 'Names')
    require(r['extracted']['tier_labels_as_written'] == ['初級者', '中級者', '上級者'], 'Source tiers altered')
    require(r['extracted']['map2']['required_parent_quantity'] is None and r['extracted']['map2']['pet_species_ids'] is None, 'Quest quantity/species invented')
    require(r['extracted']['map3']['reward'] == 'POSSIBLE_RARE_ITEM' and r['extracted']['map3']['drop_rate'] is None, 'Drop certainty/rate invented')
    require(r['extracted']['editorial']['is_operator_quote'] is False, 'Editorial promoted to operator quote')
    require(r['extracted']['editorial']['ticket_price'] is None and r['extracted']['editorial']['ticket_consumption_or_duration'] is None, 'Ticket entitlement invented')
    require(r['comparisons'] == comparison(r['later_derived_input']), 'Cross-version aliases invented')
    require(len(r['records']) == 6, 'Bounded six records')
    for i, x in enumerate(r['records']):
        require(x['version_profile'] == 'LATER_OFFICIAL:JP_GAIAX_2005' and x['game_ids'] is None, 'Original version/ID promotion')
        require(x['source_refs'] == ['S1Q' if i < 4 else 'S1E'], 'Record source layer changed')
        require(x['verification_status'] == ('OPERATOR_QUOTATION_NOT_RUNTIME' if i < 4 else 'CONTEMPORANEOUS_EDITORIAL_NOT_OPERATOR_QUOTATION'), 'Source authority upgraded')
    require(all(v is False for v in r['unproven'].values()), 'Unproven boundary promoted')
    require(r['status'] == {'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'}, 'Stage changed')


MUTATIONS = (
    ('tier-swapped', '初級者向け', '上級者向け'),
    ('species-group', '竜脚類系', '鳥類系'),
    ('agility-direction', '素早さが低い', '素早さが高い'),
    ('discovery-agent', '最近漁師によって', '最近商人によって'),
    ('quest-quantity', '親犬を複数集めると', '親犬を1匹集めると'),
    ('quest-reward', '子犬型恐竜がもらえる', '武器がもらえる'),
    ('ancient-remains', '“バルツ山”の跡地', '“バルツ山”の山頂'),
    ('survivor-history', '生き残りが多数', '新種が多数'),
    ('time-relative-strength', '現時点では最強レベル', '永遠に最強レベル'),
    ('possible-not-guaranteed-drop', '手に入る可能性があります', '必ず手に入ります'),
    ('admission-ticket', 'チケットがないと入れない', 'チケットがなくても入れる'),
    ('free-start-date', '12月2日から基本プレイ無料化', '12月3日から基本プレイ無料化'),
    ('editorial-not-observation', '問題も懸念される', '問題が実証された'),
)


def audit(r, raw):
    s = raw.decode('utf-8-sig')
    require(s.count('</head>') == 1, 'HTML head boundary ambiguous')
    head, body = s.split('</head>', 1)
    cases = []
    for label, before, after in MUTATIONS:
        # Meta descriptions repeat the opening sentence; mutate the actual body only.
        require(body.count(before) == 1, 'Nonunique body mutation anchor: ' + label)
        modified = (head + '</head>' + body.replace(before, after, 1)).encode()
        try:
            # Ignore all digest fields: only semantic guards are considered here.
            x = extract(modified)
            semantics = {k: v for k, v in x.items() if not k.endswith('sha256')}
            expected = {k: v for k, v in r['extracted'].items() if not k.endswith('sha256')}
            rejected = semantics != expected
        except ValueError:
            rejected = True
        require(rejected, 'Semantic mutation accepted: ' + label)
        cases.append({'case': label, 'input_sha256': sha(modified), 'rejected_without_digest_gate': True})
    positive = raw + b'<script>irrelevant outer page change</script>'
    require(extract(positive) == r['extracted'], 'Outer-only positive changed scoped source')
    return {'real_source_mutations': cases, 'outer_script_positive': True}


def replay(r, raw):
    validate(r)
    require(extract(raw) == r['extracted'], 'Source semantics/scoped quote digest changed')
    return {'schema': 'stoneage.jp2005_special_maps.derived_replay.r1', 'http_bytes': len(raw), 'http_sha256': sha(raw),
            'extracted': extract(raw), 'comparisons': comparison(r['later_derived_input']), 'audit': audit(r, raw),
            'historical_2005_bytes_authenticated': False, 'server_execution_verified': False, 'raw_html_in_output': False}


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--fetch', action='store_true')
    g.add_argument('--html', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if a.fetch:
        with urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as f:
            require(f.status == 200, 'HTTP failed')
            raw = f.read(1000001)
            require(len(raw) <= 1000000, 'Oversized source')
    else:
        raw = a.html.read_bytes()
    result = replay(json.loads(REPORT.read_text()), raw)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'success': True, 'http_bytes': len(raw), 'semantic_mutations': len(result['audit']['real_source_mutations'])}))


if __name__ == '__main__':
    main()
