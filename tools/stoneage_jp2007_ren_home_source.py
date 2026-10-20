"""Source-qualified Japanese 2007 Ren/White story, exchange and charm recovery."""
import argparse
import copy
import datetime
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-JP2007-REN-HOME'
REPORT = ROOT / ('research/recovered/' + STEM + '-SOURCE-R1.json')
URLS = {
    'june': 'https://www.4gamer.net/news/history/2007.06/20070612195557detail.html',
    'january': 'https://www.4gamer.net/news/history/2007.01/20070130162900detail.html',
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Visible(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.block = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'iframe', 'noscript'):
            self.block += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'iframe', 'noscript') and self.block:
            self.block -= 1

    def handle_data(self, data):
        if not self.block:
            self.parts.append(data)


def source_fragment(raw, key):
    text = raw.decode('cp932', errors='strict')
    stamp = {'june': '2007/06/12 19:55', 'january': '2007/01/30 16:29'}[key]
    require(stamp in text, 'Publication changed: ' + key)
    if key == 'june':
        require('release_maker">ガイアックス' in text and 'メーカー発表文' in text, 'June release attribution missing')
        pattern = r'(<div class="release_box">)(.*?)(</div>)'
    else:
        require('以下リリースより' in text and 'ガイアックス' in text, 'January release attribution missing')
        pattern = r'(<SPAN class="blockquote">)(.*?)(</SPAN>)'
    matches = list(re.finditer(pattern, text, re.S | re.I))
    require(len(matches) == 1, 'Ambiguous release container: ' + key)
    return text, matches[0]


def core(raw, key):
    text, match = source_fragment(raw, key)
    parser = Visible()
    parser.feed(match.group(2))
    return re.sub(r'\s+', '', ''.join(parser.parts))


# Short source anchors are used only for semantic rejection; full articles are never archived.
CLAUSES = {
    'january': ('カルターナの村の村長宅', '少女『レン』', '彼女が指定する材料',
                'コンビニで購入するなど', 'イベント限定アイテム『バレンタインチョコ』',
                '気になる相手がいる様子', '1月30日(火)定期メンテナンス後',
                '2月27日(火)定期メンテナンス開始', '味方パーティ全体体力600前後回復する'),
    'june': ('バレンタインデーとホワイトデーのイベント', 'お互いの気持ちを確認しあった',
             '若者「ワイト」と村長の孫娘「レン」', '「レンの父」から、最後の試練',
             'ある特定の恐竜を倒すと', '『建材アイテム』を落とす',
             'カルターナの村のはずれ', 'ＮＰＣの青年「ワイト」に渡す',
             '建材のランクに応じた景品と、ポイント',
             '6月12日(火)定期メンテナンス後～6月27日(火)定期メンテナンスまで',
             '一定量指定された収集品', '新居が大きくなっていきます',
             'プレイヤーキャラクターの「魅力」ステータス', '命令に従いやすく',
             '敗北などにより減少していた「魅力」が回復', '『ディノ・シャルマン』という香水',
             '効果の高さ別に３種類', '専門ショップ『マンモストア』'),
}


def extract(raws):
    cores = {k: core(raws[k], k) for k in URLS}
    for key, clauses in CLAUSES.items():
        require(all(s in cores[key] for s in clauses), 'Material claim changed: ' + key)
    return {
        'core_sha256': {k: sha(v.encode()) for k, v in cores.items()},
        'january': {
            'npc': 'レン', 'location': 'カルターナの村の村長宅',
            'flow': ['OBTAIN_UNNAMED_REQUESTED_MATERIALS_INCLUDING_SHOP_PURCHASE', 'HAND_MATERIALS_TO_REN', 'RECEIVE_EVENT_CHOCOLATE'],
            'item': 'バレンタインチョコ', 'effect': {'stat_label': '体力', 'amount_approximate': 600, 'target': 'ALL_ALLIED_PARTY'},
            'period_as_written': ['1月30日(火)定期メンテナンス後', '2月27日(火)定期メンテナンス開始'],
            'crush_named_in_january': None, 'ingredients_and_quantities': None, 'original_ids': None},
        'june': {
            'event_title': 'ワイトとレンの スウィートホーム大作戦！！',
            'named_roles': {'ワイト': 'YOUNG_MAN_AND_EXCHANGE_NPC', 'レン': 'VILLAGE_CHIEFS_GRANDDAUGHTER', 'レンの父': 'ISSUER_OF_LAST_TRIAL'},
            'retrospective': 'VALENTINE_AND_WHITE_DAY_MUTUAL_FEELINGS_CONFIRMED_AS_REPORTED_IN_JUNE',
            'flow': ['DEFEAT_UNNAMED_SPECIFIC_DINOSAURS', 'COLLECT_BUILDING_MATERIAL_DROPS', 'HAND_TO_WHITE_AT_KARTANA_OUTSKIRTS', 'RECEIVE_RANK_DEPENDENT_PRIZES_AND_POINTS'],
            'world_change_claim': 'HOUSE_GROWS_WHEN_SPECIFIED_COLLECTION_AMOUNTS_REACHED',
            'period_as_written': ['6月12日(火)定期メンテナンス後', '6月27日(火)定期メンテナンスまで'],
            'end_weekday_conflict': {'body_weekday': '火', 'calendar_weekday_if_publication_year': '水', 'publication_year_used_for_check': 2007, 'actual_intended_end_date': None},
            'body_year_explicit': None, 'time_of_day_or_timezone': None,
            'dinosaurs_materials_ranks_prizes_thresholds': None, 'counter_scope': None,
            'final_house_or_marriage_observed': False, 'house_persistence': None, 'original_ids': None},
        'perfume': {
            'name': 'ディノ・シャルマン', 'shop': 'マンモストア', 'types_by_effect_strength': 3,
            'announcement_month_day': '6月12日', 'target': 'PLAYER_CHARACTER_CHARM',
            'effect': 'RESTORE_CHARM_LOST_FOR_EXAMPLE_AFTER_DEFEAT',
            'obedience_claim': 'HIGHER_PLAYER_CHARM_MAKES_PETS_MORE_LIKELY_TO_OBEY',
            'exact_recovery_prices_type_names_cap_formula': None,
            'changes_pet_loyalty_directly': None, 'guarantees_obedience': False},
        'narrative_links': [
            {'from': 'JANUARY_REN_ROMANCE', 'to': 'JUNE_HOME_EVENT', 'relation': 'NAMED_STORY_CONTINUATION_STATED_IN_JUNE_NOT_SAME_BUILD_ID'},
            {'from': 'WHITE_DAY_EVENT_NOT_INDEPENDENTLY_FETCHED', 'to': 'JUNE_HOME_EVENT', 'relation': 'JUNE_RETROSPECTIVE_ONLY'},
        ],
        'server_execution_witnessed': False, 'early_build_membership_proven': False,
    }


def validate(r):
    require(r['schema'] == 'stoneage.jp2007_ren_home.source_contract.r1', 'Schema')
    require({k: x['url'] for k, x in r['sources'].items()} == URLS, 'Source URLs')
    require(all(x['current_bytes_are_authenticated_2007_original'] is False for x in r['sources'].values()), 'Current page promoted to historical bytes')
    require(r['sources']['june']['authority'] == 'GAIAX_RELEASE_EXPLICITLY_REPUBLISHED_BY_4GAMER', 'June authority')
    require(r['sources']['january']['authority'] == 'RELEASE_EXCERPT_WITH_GAIAX_ATTRIBUTED_IN_MEDIA_INTRODUCTION', 'January authority')
    x = r['extracted']
    require(datetime.date(2007, 6, 27).weekday() == 2, 'Calendar invariant')
    require(x['june']['end_weekday_conflict'] == {'body_weekday': '火', 'calendar_weekday_if_publication_year': '水', 'publication_year_used_for_check': 2007, 'actual_intended_end_date': None}, 'Calendar conflict silently repaired')
    # Compare all semantic fields to the independently archived local replay; no unknown may be filled.
    local = ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')
    require(x == json.loads(local.read_text())['extracted'], 'Historical semantics or unknown fields changed')
    require(len(r['records']) == 8 and len({a['record_id'] for a in r['records']}) == 8, 'Bounded unique records')
    require([a['source'] for a in r['records']] == ['january'] * 3 + ['june'] * 5, 'Source roles transferred')
    for row in r['records']:
        require(row['version_profile'] == 'LATER_OFFICIAL:JP_GAIAX_2007' and row['game_ids'] is None, 'Original version or ID invented')
    require(all(v is False for v in r['unproven'].values()), 'Unproven claim promoted')
    require(r['status'] == {'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'}, 'Stage changed')
    require(r['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-45', 'Portfolio queue')


MUTATIONS = (
    ('january', 'ren-location', 'カルターナの村の村長宅', 'カルターナの村の病院'),
    ('january', 'chocolate-recipient', '少女『レン』', '少女『リナ』'),
    ('january', 'approximate-not-exact', '600前後', '600ちょうど'),
    ('january', 'party-not-one', '味方パーティ全体', '味方一人'),
    ('january', 'start-after-maintenance', '定期メンテナンス後', '定期メンテナンス前'),
    ('june', 'family-relation', '村長の孫娘', '村長の娘'),
    ('june', 'prior-story-relation', 'お互いの気持ちを確認しあった', 'お互いに会ったことのない'),
    ('june', 'trial-issuer', '「レンの父」から', '「レンの母」から'),
    ('june', 'defeat-not-capture', '恐竜を倒すと', '恐竜を捕まえると'),
    ('june', 'exchange-target', '青年「ワイト」に渡す', '青年「レン」に渡す'),
    ('june', 'rank-not-quantity', '建材のランクに応じた', '建材の数量に応じた'),
    ('june', 'end-date-not-silent-fix', '6月27日(火)', '6月26日(火)'),
    ('june', 'house-growth-direction', '新居が大きくなって', '新居が小さくなって'),
    ('june', 'player-not-pet-stat', 'プレイヤーキャラクターの「魅力」', 'ペットの「忠誠」'),
    ('june', 'restore-not-unbounded-increase', '「魅力」が回復', '「魅力」が無制限に増加'),
    ('june', 'perfume-count', '効果の高さ別に３種類', '効果の高さ別に４種類'),
    ('june', 'shop-name', '専門ショップ『マンモストア』', '専門ショップ『他店』'),
)


def audit(raws, expected):
    checks = []
    for key, label, old, new in MUTATIONS:
        text, match = source_fragment(raws[key], key)
        body = match.group(2)
        require(body.count(old) == 1, 'Nonunique source mutation: ' + label)
        modified = (text[:match.start(2)] + body.replace(old, new, 1) + text[match.end(2):]).encode('cp932')
        changed = dict(raws, **{key: modified})
        try:
            value = extract(changed)
            value.pop('core_sha256')
            target = copy.deepcopy(expected)
            target.pop('core_sha256')
            rejected = value != target
        except ValueError:
            rejected = True
        require(rejected, 'Semantic change accepted without digest: ' + label)
        checks.append({'source': key, 'case': label, 'input_sha256': sha(modified), 'rejected_without_digest_gate': True})
    positives = {}
    for key in URLS:
        modified = dict(raws, **{key: raws[key] + b'<script>outer change</script>'})
        require(extract(modified) == expected, 'Outer-only source change affected core')
        positives[key] = True
    return {'real_body_mutations': checks, 'outer_script_positives': positives}


def replay(r, raws):
    validate(r)
    require(extract(raws) == r['extracted'], 'Source semantics or core SHA changed')
    return {'schema': 'stoneage.jp2007_ren_home.derived_replay.r1',
            'http': {k: {'bytes': len(b), 'sha256': sha(b)} for k, b in raws.items()},
            'extracted': extract(raws), 'audit': audit(raws, r['extracted']),
            'raw_html_or_assets_in_output': False, 'historical_server_executed': False}


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--fetch', action='store_true')
    g.add_argument('--html-dir', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    raws = {}
    for key, url in URLS.items():
        if a.fetch:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
                require(response.status == 200, 'HTTP failed: ' + key)
                raws[key] = response.read(1000001)
                require(len(raws[key]) <= 1000000, 'Source oversized')
        else:
            raws[key] = (a.html_dir / (key + '.html')).read_bytes()
    result = replay(json.loads(REPORT.read_text()), raws)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'success': True, 'http_bytes': {k: len(b) for k, b in raws.items()}, 'semantic_mutations': len(result['audit']['real_body_mutations'])}))


if __name__ == '__main__':
    main()
