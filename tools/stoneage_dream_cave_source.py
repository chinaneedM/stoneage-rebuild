"""R68 documentary quest branches and unassigned route pairs; never a server replay."""
import argparse
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-CN2003-DREAM-CAVE'
REPORT = ROOT / f'research/recovered/{STEM}-SOURCE-R1.json'
URL = 'https://games.sina.com.cn/zhqu/sta/article/2003-05-30/10033.shtml'
PROFILE = 'CN2003_SINA_DREAM_CAVE_EXACT_BUILD_UNKNOWN'
BOUNDARIES = {k: False for k in ('official_authorship_verified', 'historical_bytes_authenticated',
    'same_build_tw10_membership_verified', 'original_server_runtime_verified',
    'route_pairs_assigned_to_day_night', 'village_three_coordinates_resolved',
    'all_source_monster_labels_are_pet_species', 'original_ids_recovered',
    'disconnect_equated_with_logout', 'original_html_or_assets_committed', 'stage_b_started')}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def compact(text):
    return re.sub(r'\s+', '', text)


class Article(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.active = None
        self.hidden = 0
        self.roots = 0
        self.parts = []
        self.table_stack = []
        self.table_children = []
        self.tables = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'iframe', 'noscript'):
            self.hidden += 1
        if self.hidden:
            return
        if tag == 'td':
            self.depth += 1
            if 'l15z' in dict(attrs).get('class', '').split():
                require(self.active is None, 'Nested article root')
                self.roots += 1
                self.active = self.depth
        if tag == 'table' and self.active is not None:
            if self.table_children:
                self.table_children[-1] = True
            self.table_stack.append([])
            self.table_children.append(False)

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'iframe', 'noscript'):
            if self.hidden:
                self.hidden -= 1
            return
        if self.hidden:
            return
        if tag == 'table' and self.active is not None:
            require(bool(self.table_stack), 'Unexpected table close')
            table = compact(''.join(self.table_stack.pop()))
            if not self.table_children.pop():
                self.tables.append(table)
        if tag == 'td':
            if self.depth == self.active:
                self.active = None
            self.depth -= 1

    def handle_data(self, text):
        if self.active is not None and not self.hidden:
            self.parts.append(text)
            for table in self.table_stack:
                table.append(text)


def one(pattern, text):
    matches = re.findall(pattern, text)
    require(len(matches) == 1, 'Missing/duplicate selected evidence: ' + pattern)
    return matches[0]


def derive(raw):
    text = raw.decode('gb18030', errors='strict')
    require(re.search(r'charset=["\x27]?gb2312', text, re.I), 'Charset changed')
    date = one(r'<!-- include 发布时间 begin -->(.*?)<!-- include 发布时间 end -->', text)
    require(compact(date) == '2003-05-3013:51', 'Publication changed')
    title = one(r'<td\b[^>]*height=30[^>]*colspan=4[^>]*>(.*?)</td>', text)
    require(compact(re.sub('<[^>]*>', '', title)) == '《石器时代》任务功略-梦幻洞窟', 'Title changed')
    parser = Article()
    parser.feed(text)
    require(parser.roots == 1 and parser.active is None, 'Article root absent/duplicate/unclosed')
    body = compact(''.join(parser.parts))
    recommended = int(one(r'等级要求：建议等级(\d+)级', body))
    require('虽然没有硬性规定，但若玩家解过成人仪式，之后才能得到空想系列的装备；否则随机物品一个。' in body,
            'Adult completion is reward eligibility, not admission')
    village = one(r'奇努伊村((?:（东\d+，南\d+）){3})，和', body)
    elder = [int(x) for x in one(r'村中的老人（东(\d+)，南(\d+)）谈话', body)]
    day = [int(x) for x in one(r'白天的时候，玩家可以从坐标（东(\d+)，南(\d+)）的洞口进入', body)]
    night = [int(x) for x in one(r'晚上则只能由坐标（东(\d+)，南(\d+)）的洞口进入', body)]
    require('3.交通工具：加美航空。4.精灵的羽毛：无。' in body, 'Travel claim changed')
    require('将先见之光弄掉在地上的话，虽然先见之光会立刻消失不见' in body and
            '勇者可以再跟老人拿一次是没问题的' in body and
            '只要玩家注销，“先见之光”就会如同光束般消失不见' in body, 'Offering lifecycle changed')
    require('每年都会将先见之光贡献给仙人' in body and '传说沙姆岛住着一位仙人' in body,
            'Narrative attribution changed')
    sage = one(r'住在“梦幻洞窟”里的“([^”]+)”', body)
    require(sage == '梦见的仙人' and '将“先见之光”交给仙人' in body, 'Named recipient or delivery changed')
    guards = list(one(r'红蛙“([^”]+)”和金蛙“([^”]+)”率领的宠物大队', body))
    require('红蛙跟金蛙是仙人聊天的对象' in body and '无法跟仙人以外的人类接近' in body,
            'Companion narrative changed')
    rewards = []
    for name, stats, skill, level in re.findall(r'“(空想的[^”]+)”（([^（）]*?)([^（）]+精灵)Lv(\d+)）', body):
        # Split immediately before the named spirit, preserving the source labels.
        stats_match = re.match(r'((?:[攻防敏魅][+-]\d+)+)(.+精灵)$', stats + skill)
        require(stats_match is not None, 'Reward stat/skill structure changed')
        rewards.append({'name': name, 'stats': {k: int(v) for k, v in re.findall(r'([攻防敏魅])([+-]\d+)', stats_match[1])},
                        'spirit_name': stats_match[2], 'spirit_level': int(level), 'item_id': None})
    require([r['name'] for r in rewards] == ['空想的竖琴', '空想的帽子', '空想的衣服'], 'Reward set changed')
    order = re.findall(r'第([一二三])次解此任务可以获得“([^”]+)”', body)
    require(order == list(zip('一二三', [r['name'] for r in rewards])), 'Repeat order changed')
    require('第四次以后解此任务则会获得仙人给的随机物品' in body and '又可以重复解' in body,
            'Repeat/random branch changed')
    levels = [int(x) for x in one(r'怪物等级：(\d+)~(\d+)级', body)]
    labels = one(r'怪物种类：([^上]+)上左', body).split('、')
    route_tables = [t for t in parser.tables if '传送点路径' in t]
    require(len(route_tables) == 2 and all(len(re.findall('传送点路径', t)) == 2 for t in route_tables),
            'Exactly two separate route-pair tables required')
    routes = [{'direction': direction, 'steps': steps.split('→'), 'day_night_assignment': None}
              for direction, steps in re.findall(r'传送点路径（(去程|回程)）：([上下左右→]+)。', body)]
    require(all(''.join(re.findall(r'传送点路径（(去程|回程)）', t)) == '去程回程' for t in route_tables),
            'Route direction order differs inside table')
    require([r['direction'] for r in routes] == ['去程', '回程', '去程', '回程'], 'Route pair scope changed')
    return {'recommended_level': recommended, 'hard_entry_level': None, 'adult_required_for_admission': False,
        'adult_required_for_named_reward_sequence': True, 'region': '沙姆岛', 'village': '奇努伊村',
        'village_coordinate_literals': re.findall(r'（东\d+，南\d+）', village),
        'village_coordinate_frames': None, 'elder_position_as_reported': elder,
        'entrances_as_reported': {'day': day, 'night': night}, 'transport_as_reported': '加美航空',
        'feather_as_reported': '无', 'offering': {'name': '先见之光', 'drop_disappears': True,
            'logout_disappears': True, 'disconnect_behavior': None, 'elder_regrant_reported': True,
            'regrant_limit': None, 'item_id': None},
        'narrative_relations': [
            {'from': '奇努伊村村民', 'relation': 'annual_offering_custom', 'to': '梦见的仙人'},
            {'from': '仙人守护航空安全', 'relation': 'source_legend_and_speculation', 'to': '沙姆岛'},
            {'from': guards, 'relation': 'guard_battle_then_described_as_sages_conversation_companions', 'to': '梦见的仙人'}],
        'named_guards': guards, 'sage': sage,
        'documentary_flow': [
            {'order': 1, 'actor': '村中的老人', 'action': 'accept_annual_offering_request', 'item': '先见之光'},
            {'order': 2, 'actor': '勇者', 'action': 'choose_time_dependent_entrance_then_teleport', 'route_pair_assignment': None},
            {'order': 3, 'actor': guards, 'action': 'defeat_guard_party_before_visiting_sage', 'battle_script_id': None},
            {'order': 4, 'actor': sage, 'action': 'receive_offering_and_give_conditional_reward', 'server_event_id': None}],
        'rewards': rewards,
        'reward_sequence_if_adult': [r['name'] for r in rewards] + ['RANDOM_FROM_FOURTH'],
        'nonadult_reward': 'RANDOM_ITEM', 'random_item_pool': None, 'repeat_counter_storage': None,
        'monster_level_range_as_reported': levels, 'monster_labels_as_reported': labels,
        'route_pairs_in_source_order': [routes[:2], routes[2:]], 'map_geometry': None,
        'quest_id': None, 'npc_ids': None, 'map_ids': None, 'exact_game_build': None,
        'original_server_runtime_verified': False}


def catalog(extraction):
    return [{'record_id': 'CN2003-SINA-R68-QUEST-01', 'entity_type': 'documentary_quest_description',
        'collection': 'quests', 'version_profile': PROFILE, 'source_refs': ['S1'],
        'verification_status': 'SOURCE_DESCRIPTION_NOT_RUNTIME',
        'rights_status': 'RESEARCH_METADATA_NOT_RELEASE_APPROVED', 'record_revision': 1,
        'game_ids': None, 'content': extraction}]


def pin(path):
    raw = (ROOT / path).read_bytes()
    return {'path': path, 'bytes': len(raw), 'sha256': sha(raw),
            'git_blob': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}


def verify_report(report):
    require(report['version_profile'] == PROFILE and report['negative_boundaries'] == BOUNDARIES,
            'Evidence/version boundaries changed')
    require(report['catalog_records'] == catalog(report['extraction']), 'Detached or promoted catalog')
    ex = report['extraction']
    for key in ('hard_entry_level', 'village_coordinate_frames', 'random_item_pool', 'repeat_counter_storage',
                'map_geometry', 'quest_id', 'npc_ids', 'map_ids', 'exact_game_build'):
        require(ex[key] is None, 'Unknown content promoted: ' + key)
    require(ex['original_server_runtime_verified'] is False and ex['adult_required_for_admission'] is False,
            'Runtime or admission promoted')
    require(ex['offering']['item_id'] is None and
            ex['documentary_flow'][1]['route_pair_assignment'] is None and
            ex['documentary_flow'][2]['battle_script_id'] is None and
            ex['documentary_flow'][3]['server_event_id'] is None, 'Nested IDs or route assignment invented')
    require(ex['offering']['disconnect_behavior'] is None and ex['offering']['regrant_limit'] is None,
            'Offering semantics invented')
    require(all(r['day_night_assignment'] is None for pair in ex['route_pairs_in_source_order'] for r in pair),
            'Routes assigned without labels')
    require(all(r['item_id'] is None for r in ex['rewards']), 'Original item identity invented')
    require(len(report['parent_pins']) == 2 and all(pin(p['path']) == p for p in report['parent_pins']),
            'Parent evidence changed')


MUTATIONS = (('建议等级60级', '建议等级61级'), ('2003-05-30 13:51', '2003-05-31 13:51'),
    ('虽然没有硬性规定', '这是硬性规定'), ('东96，南120', '东95，南120'),
    ('东87，南102', '东87，南103'), ('东73，南55', '东73，南56'),
    ('攻+2敏+1魅+5', '攻+3敏+1魅+5'), ('滋润的精灵Lv2', '滋润的精灵Lv3'),
    ('第三次解此任务可以获得', '第二次解此任务可以获得'), ('第四次以后', '第五次以后'),
    ('下→左→左→上', '下→右→左→上'), ('注销', '断线'),
    ('红蛙“卡卡金宝”', '红蛙“另一名称”'), ('怪物等级：37~60级', '怪物等级：38~60级'),
    ('住在“梦幻洞窟”里的“梦见的仙人”', '住在“梦幻洞窟”里的“别的仙人”'),
    ('将“先见之光”交给仙人', '将“另一物品”交给仙人'))


def audit(raw, expected):
    text = raw.decode('gb18030')
    for old, new in MUTATIONS:
        require(old in text, 'Real-source mutation absent')
        try:
            actual = derive(text.replace(old, new).encode('gb18030'))
        except ValueError:
            continue
        require(actual != expected, 'Semantic mutation accepted')
    require(derive(raw + b'<script>peripheral=1</script>') == expected, 'Peripheral script affected extraction')
    return {'semantic_mutations_rejected_without_digest_gate': len(MUTATIONS), 'peripheral_script_positive': True}


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--fetch', action='store_true')
    g.add_argument('--input')
    p.add_argument('--output', required=True)
    args = p.parse_args()
    report = json.loads(REPORT.read_text())
    verify_report(report)
    if args.fetch:
        with urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent': 'StoneAge-research/1.0'}), timeout=45) as r:
            require(r.status == 200 and r.url == URL, 'HTTP identity changed')
            raw = r.read(2_000_001)
    else:
        raw = Path(args.input).read_bytes()
    require(len(raw) <= 2_000_000, 'Source exceeds bound')
    actual = derive(raw)
    require(actual == report['extraction'], 'Documentary semantics changed')
    out = {'schema': 'stoneage.dream_cave.replay.r1', 'inputs': [{'id': 'S1', 'url': URL, 'bytes': len(raw), 'sha256': sha(raw)}],
        'extraction': actual, 'catalog_records': catalog(actual), 'audit': audit(raw, actual),
        'original_html_or_assets_in_output': False, 'original_game_runtime_verified': False}
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'input_bytes': len(raw), 'sha256': sha(raw), 'route_pairs': 2, 'quest_records': 1}))


if __name__ == '__main__':
    main()
