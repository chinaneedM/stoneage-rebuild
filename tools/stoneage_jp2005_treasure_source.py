"""R69: release quotation vs editorial claims, phase-specific collectible exchange."""
import argparse
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-JP2005-TREASURE-EVENT'
REPORT = ROOT / f'research/recovered/{STEM}-SOURCE-R1.json'
URL = 'https://www.4gamer.net/news/history/2005.09/20050906172318detail.html'
PROFILE = 'LATER_OFFICIAL_JP_GAIAX_2005_RELEASE_QUOTED_BY_4GAMER_EXACT_BUILD_UNKNOWN'
BOUNDARIES = {k: False for k in ('direct_official_page_acquired', 'historical_2005_bytes_authenticated',
    'original_server_runtime_verified', 'tw10_or_jss1999_rules_backfilled',
    'weekday_conflict_silently_corrected', 'five_types_are_five_units',
    'drop_rate_or_prize_pool_recovered', 'all_dungeons_are_event_areas',
    'transferable_collectibles_means_transferable_prizes', 'quest_acceptance_required_for_drops_proven',
    'repeatable_means_daily_reset', 'original_html_or_assets_committed', 'stage_b_started')}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def compact(s):
    return re.sub(r'\s+', '', s)


class Visible(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'iframe', 'noscript'):
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'iframe', 'noscript') and self.hidden:
            self.hidden -= 1

    def handle_data(self, text):
        if not self.hidden:
            self.parts.append(text)



class VisibleMarkup(HTMLParser):
    """Discard hidden elements before any structural boundary search."""
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'iframe', 'noscript'):
            self.hidden += 1
        elif not self.hidden:
            self.parts.append(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        if not self.hidden:
            self.parts.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'iframe', 'noscript'):
            if self.hidden: self.hidden -= 1
        elif not self.hidden:
            self.parts.append('</' + tag + '>')

    def handle_data(self, data):
        if not self.hidden: self.parts.append(data)

    def handle_comment(self, data):
        if not self.hidden: self.parts.append('<!--' + data + '-->')

    def handle_entityref(self, name):
        if not self.hidden: self.parts.append('&' + name + ';')

    def handle_charref(self, name):
        if not self.hidden: self.parts.append('&#' + name + ';')


def plain(s):
    p = Visible(); p.feed(s)
    return compact(''.join(p.parts))


def one(pattern, text, flags=0):
    found = re.findall(pattern, text, flags)
    require(len(found) == 1, 'Missing/duplicated source evidence: ' + pattern)
    return found[0]


def derive(raw):
    markup = VisibleMarkup()
    markup.feed(raw.decode('cp932', errors='strict'))
    text = ''.join(markup.parts)
    require(re.search(r'charset=shift_jis', text, re.I), 'Charset declaration changed')
    date = one(r'<div class="news_txt1">(.*?)</div>', text, re.S)
    require(plain(date) == '2005/09/0617:23', 'Visible publication changed')
    title = one(r'<h5>(MMORPG.*?)</h5>', text, re.S)
    require(plain(title) == 'MMORPG「ストーンエイジ」で，限定アイテムが入手できるイベント', 'Visible article title changed')
    container = one(r'<td class="newstext">(.*?)<!-- tDialy:END -->', text, re.S)
    blocks = re.findall(r'<!-- 本文開始 -->(.*?)<!-- 本文終了 -->', container, re.S)
    blocks = [b for b in blocks if plain(b)]
    require(len(blocks) == 1, 'Exactly one nonempty article body required')
    body = blocks[0]
    quote = one(r'<font color=#880000>(.*?)</font>', body, re.S | re.I)
    before, after = body.split(quote)
    intro, release, outro = plain(before), plain(quote), plain(after)
    require('＃＃＃＃＃以下，リリースより＃＃＃＃＃' in intro and outro.startswith('＃＃＃＃＃'),
            'Release/editorial delimiter changed')
    operator = one(r'^(.*?)は，MMORPG「ストーンエイジ」で，', intro)
    require(operator == 'ガイアックス', 'Operator attributed from article, not footer')
    event_name = one(r'"([^"]+)"と題した二部構成のイベント', intro)
    media_weekday = one(r'9月13日（(.)）から', intro)
    phases = []
    pattern = r'第([一二])部9月(\d+)日（(.)）(\d\d:\d\d)（定期メンテナンス明けから）～(\d+)日（(.)）(\d\d:\d\d)（定期メンテナンスに入るまで）'
    for number, start, weekday, time, end, end_weekday, end_time in re.findall(pattern, release):
        phases.append({'phase': 1 if number == '一' else 2,
            'start': {'month': 9, 'day': int(start), 'weekday_as_written': weekday, 'time': time, 'maintenance_relation': 'AFTER'},
            'end': {'month': 9, 'day': int(end), 'weekday_as_written': end_weekday, 'time': end_time, 'maintenance_relation': 'BEFORE'},
            'timezone': None, 'year_context_from_article': 2005, 'actual_operation_verified': False})
    require([p['phase'] for p in phases] == [1, 2], 'Two ordered phase windows required')
    require('●開催場所全サーバーの一部のダンジョン' in release, 'Limited dungeon scope changed')
    require('●参加条件特になし（全ユーザーが参加できます）' in release, 'Participation qualifier changed')
    village, npc = one(r'全サーバーの([^に]+)にNPC『([^』]+)』が登場', release)
    require('精霊の力の結晶を集めてくるよう' in release and 'プレイヤーキャラクターに伝えます（クエストを与えます）' in release,
            'Quest request changed')
    recipient = one(r'全種類集めてイベントの第二部で『([^』]+)』に渡す', release)
    require(recipient == npc, 'Exchange recipient differs from quest NPC')
    require('一部のエリアの恐竜が低確率で特殊なイベントアイテムを落とす' in release,
            'Drop location/probability changed')
    counts = [int(n) for n in one(r'第一部で(\d+)種類、第二部で(\d+)種類の計(\d+)種類', release)]
    require(sum(counts[:2]) == counts[2] and all(n > 0 for n in counts), 'Type totals inconsistent')
    require('第一部と第二部では異なる' in release and '第一部でしか手に入らないアイテム' in release,
            'Phase-limited acquisition changed')
    require('繰り返し行えるクエストであるため、何度でもチャレンジすることが可能' in release,
            'Repeatability changed')
    require('イベントアイテムは他プレイヤーとの受け渡しが可能' in release and
            '他プレイヤーとの売買でアイテムを手に入れるのも一つの方法' in release,
            'Transfer/trade target changed')
    require('イベントアイテムと賞品の交換は第二部から開始' in release and
            '賞品（このイベント限定のアイテム）' in release, 'Exchange gate/reward scope changed')
    link = one(r'<a href="(http://stoneage.to/info/event_020.html)"[^>]*>「こちら」</a>', after)
    require('限定アイテムの詳細は，まだ明かされていない' in outro and '（TeT）' in outro,
            'Editorial prize uncertainty or author changed')
    return {'event_name': event_name, 'operator_as_attributed_by_media': operator,
        'release_scope': 'PUBLISHER_RELEASE_QUOTED_IN_CONTEMPORARY_PRESS_NOT_DIRECT_SITE',
        'phases': phases, 'collectible_type_counts_by_phase': counts[:2], 'total_collectible_types': counts[2],
        'per_type_required_quantity': None, 'collectible_names': None, 'collectible_item_ids': None,
        'locations': {'server_scope': 'ALL_SERVERS', 'drop_area_scope': 'SOME_DUNGEONS_AND_AREAS',
            'dungeon_names': None, 'npc_village_as_written': village, 'coordinates': None, 'map_ids': None},
        'npc': {'name': npc, 'request_theme': 'COLLECT_SCATTERED_SPIRIT_POWER_CRYSTALS',
            'roles': ['GIVE_QUEST', 'RECEIVE_ALL_COLLECTIBLE_TYPES_IN_PHASE_2'], 'npc_id': None},
        'participation': 'NO_SPECIAL_CONDITION_ALL_USERS_AS_REPORTED',
        'drop': {'producer': 'DINOSAURS_IN_SOME_AREAS', 'probability_qualifier': 'LOW',
            'probability': None, 'species_ids': None, 'requires_accepting_quest': None},
        'collection_rules': {'phase_type_sets_differ': True, 'phase1_only_acquisition_reported': True,
            'player_transfer_allowed': True, 'player_trade_suggested': True, 'transferable_target': 'COLLECTIBLE_EVENT_ITEMS',
            'trade_price': None, 'phase1_items_usable_in_phase2_exchange_as_reported': True,
            'post_event_item_persistence': None},
        'exchange': {'starts_phase': 2, 'requires_all_types': True, 'repeatable_as_reported': True,
            'repeat_limit': None, 'daily_reset': None, 'quantity_consumed': None, 'reward_description': 'EVENT_LIMITED_ITEM',
            'reward_names': None, 'reward_ids': None, 'reward_probabilities': None, 'reward_transferability': None},
        'editorial': {'author': 'TeT', 'intro_start_weekday': media_weekday,
            'release_start_weekday': phases[0]['start']['weekday_as_written'],
            'weekday_literals_disagree': media_weekday != phases[0]['start']['weekday_as_written'],
            'conflict_resolved': False, 'prize_details_reported_unannounced': True,
            'official_link_as_cited': link, 'direct_official_page_obtained': False},
        'quest_id': None, 'exact_game_build': None, 'original_server_runtime_verified': False}


def catalog(ex):
    entries = [('QUEST', 'quests', 'documentary_event_quest', ex),
               ('NPC', 'npcs', 'documentary_event_npc', ex['npc'])]
    return [{'record_id': 'JP2005-GAIAX-R69-' + ident, 'entity_type': kind, 'collection': collection,
        'version_profile': PROFILE, 'source_refs': ['S1-RELEASE'], 'verification_status': 'SOURCE_DESCRIPTION_NOT_RUNTIME',
        'rights_status': 'RESEARCH_METADATA_NOT_RELEASE_APPROVED', 'record_revision': 1, 'game_ids': None,
        'content': content} for ident, collection, kind, content in entries]



def compare_event_shapes(ex):
    """A bounded cross-version relation, not a claim of a common event script."""
    path = 'research/recovered/STONEAGE-JP2008-COOPERATION-SOURCE-R1.json'
    old = json.loads((ROOT / path).read_text())
    tree = next(r for r in old['records'] if r['record_id'] == 'JP2008-COOP-07')
    rewards = [r['source_reported'] for r in old['records'] if r['entity_type'] == 'CONDITIONAL_PUBLIC_REWARD']
    return {'relation': 'DOCUMENTED_MECHANIC_COMPARISON_NOT_LINEAGE_OR_ENTITY_IDENTITY',
        'jp2005': {'profile': PROFILE, 'collectible_types': ex['total_collectible_types'],
            'exchange_starts_phase': ex['exchange']['starts_phase'],
            'specified_per_type_quantities': ex['per_type_required_quantity'],
            'repeatable_as_reported': ex['exchange']['repeatable_as_reported']},
        'jp2008': {'source_report': path, 'profile': tree['version_profile'],
            'tree_flow': tree['source_reported']['flow'],
            'reported_delivery_thresholds': [{k: r[k] for k in ('branch', 'delivery_total', 'delivered_item',
                'reward_label', 'reported_availability', 'individual_cost', 'actual_unlock_verified')} for r in rewards],
            'counter_scope': tree['source_reported']['counter_scope']},
        'types_are_not_delivery_units': True, 'thresholds_are_not_per_player_costs': True,
        'shared_item_or_npc_identity_established': False, 'historical_evolution_proven': False,
        'modern_game_adoption_decided': False}


def pin(path):
    raw = (ROOT / path).read_bytes()
    return {'path': path, 'bytes': len(raw), 'sha256': sha(raw),
            'git_blob': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}


def verify_report(report):
    require(report['version_profile'] == PROFILE and report['negative_boundaries'] == BOUNDARIES,
            'Version/evidence boundaries changed')
    ex = report['extraction']
    require(report['catalog_records'] == catalog(ex), 'Catalog detached/promoted')
    require(report['cross_version_comparison'] == compare_event_shapes(ex), 'Cross-version relation changed')
    require(ex['editorial']['conflict_resolved'] is False and ex['editorial']['direct_official_page_obtained'] is False and
            ex['original_server_runtime_verified'] is False, 'Authority or resolved conflict invented')
    for obj, keys in [(ex, ('per_type_required_quantity', 'collectible_names', 'collectible_item_ids', 'quest_id', 'exact_game_build')),
        (ex['drop'], ('probability', 'species_ids', 'requires_accepting_quest')),
        (ex['exchange'], ('repeat_limit', 'daily_reset', 'quantity_consumed', 'reward_names', 'reward_ids', 'reward_probabilities', 'reward_transferability')),
        (ex['locations'], ('dungeon_names', 'coordinates', 'map_ids')), (ex['npc'], ('npc_id',)),
        (ex['collection_rules'], ('trade_price', 'post_event_item_persistence'))]:
        require(all(obj[k] is None for k in keys), 'Unknown values promoted')
    require(all(p['timezone'] is None and p['actual_operation_verified'] is False for p in ex['phases']),
            'Calendar context became deployment proof')
    require(len(report['parent_pins']) == 2 and all(pin(p['path']) == p for p in report['parent_pins']), 'Parent bytes changed')


MUTATIONS = (('2005/09/06 17:23', '2005/09/07 17:23'), ('9月13日（金）', '9月13日（火）'),
    ('ガイアックス</a>は', '別運営</a>は'), ('トレジャーハント大作戦！', '別イベント！'),
    ('9月13日（火）16:00', '9月13日（火）17:00'), ('20日（火）13:00', '20日（火）14:00'),
    ('9月20日（火）16:00', '9月21日（水）16:00'), ('27日（火）13:00', '28日（水）13:00'),
    ('第一部で3種類、第二部で2種類の計5種類', '第一部で2種類、第二部で3種類の計5種類'),
    ('低確率', '必ず'), ('一部のダンジョン', 'すべてのダンジョン'),
    ('特になし（全ユーザーが参加できます）', 'Lv50以上'), ('サムギルの村', '別の村'),
    ('光の精霊の使徒', '別のNPC'), ('受け渡しが可能', '受け渡しは不可能'),
    ('第二部から開始', '第一部から開始'), ('何度でもチャレンジ', '一度だけチャレンジ'),
    ('まだ明かされていない', '既に公開された'))


def audit(raw, expected):
    text = raw.decode('cp932')
    for old, new in MUTATIONS:
        require(old in text, 'Real source mutation did not match')
        try:
            actual = derive(text.replace(old, new).encode('cp932'))
        except ValueError:
            continue
        require(actual != expected, 'Semantic mutation accepted')
    require(derive(raw + b'<script>outside=1</script>') == expected, 'Peripheral script changed source meaning')
    return {'semantic_mutations_rejected_without_digest_gate': len(MUTATIONS), 'peripheral_script_positive': True}


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--fetch', action='store_true'); g.add_argument('--input')
    p.add_argument('--output', required=True); args = p.parse_args()
    report = json.loads(REPORT.read_text()); verify_report(report)
    if args.fetch:
        with urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent': 'StoneAge-research/1.0'}), timeout=45) as response:
            require(response.status == 200 and response.url == URL, 'HTTP source identity changed')
            raw = response.read(2_000_001)
    else: raw = Path(args.input).read_bytes()
    require(len(raw) <= 2_000_000, 'Source exceeds bound')
    ex = derive(raw); require(ex == report['extraction'], 'Source semantics changed')
    out = {'schema': 'stoneage.jp2005_treasure.replay.r1',
        'inputs': [{'id': 'S1', 'url': URL, 'bytes': len(raw), 'sha256': sha(raw)}],
        'extraction': ex, 'catalog_records': catalog(ex), 'cross_version_comparison': compare_event_shapes(ex), 'audit': audit(raw, ex),
        'original_html_or_assets_in_output': False, 'original_game_runtime_verified': False}
    target = Path(args.output); target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'input_bytes': len(raw), 'sha256': sha(raw), 'phases': 2, 'catalog_records': 2}))


if __name__ == '__main__': main()
