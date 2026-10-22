"""R71: documentary riddles, conditional passage and chosen reward pairs, not server execution."""
import argparse
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-CN2003-FIVE-BROTHERS'
REPORT = ROOT / f'research/recovered/{STEM}-SOURCE-R1.json'
PROFILE = 'CN2003_SINA_FIVE_BROTHERS_EXACT_BUILD_UNKNOWN'
URLS = {
    'S1': 'https://games.sina.com.cn/zhqu/sta/article/2003-06-02/10423.shtml',
    'S2': 'https://web.archive.org/web/20031204051508id_/http://games.sina.com.cn:80/zhqu/sta/article/2003-06-02/10423.shtml',
}
BOUNDARIES = {k: False for k in ('official_authorship_verified', 'current_http_bytes_are_historical_bytes',
    'same_build_tw10_membership_verified', 'original_server_runtime_verified', 'original_ids_recovered',
    'reward_choice_is_random', 'npc_spelling_variants_joined_as_one_id', 'monster_labels_are_complete_species_master',
    'map_coordinates_bound_to_original_floor_ids', 'disconnect_equated_with_leaving_world',
    'original_html_or_assets_committed', 'stage_b_started')}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def compact(text):
    return re.sub(r'\s+', '', text)


class Article(HTMLParser):
    """The current wrapper uses td.l15z, the captured wrapper span.l15z."""
    def __init__(self):
        super().__init__()
        self.counts = {'td': 0, 'span': 0}
        self.active = None
        self.roots = 0
        self.hidden = 0
        self.parts = []
        self.visible = []

    def handle_starttag(self, tag, attrs):
        if tag in ('head', 'script', 'style', 'iframe', 'noscript'):
            self.hidden += 1
        if self.hidden:
            return
        if tag in self.counts:
            self.counts[tag] += 1
            if 'l15z' in dict(attrs).get('class', '').split():
                require(self.active is None, 'Nested article root')
                self.active = (tag, self.counts[tag])
                self.roots += 1

    def handle_endtag(self, tag):
        if tag in ('head', 'script', 'style', 'iframe', 'noscript'):
            if self.hidden:
                self.hidden -= 1
            return
        if self.hidden:
            return
        if tag in self.counts:
            if self.active == (tag, self.counts[tag]):
                self.active = None
            self.counts[tag] -= 1

    def handle_data(self, text):
        if not self.hidden:
            self.visible.append(text)
            if self.active is not None:
                self.parts.append(text)


def one(pattern, text):
    matches = re.findall(pattern, text)
    require(len(matches) == 1, 'Missing/duplicate scoped evidence: ' + pattern)
    return matches[0]


def article(raw):
    text = raw.decode('gb18030', errors='strict')
    require(re.search(r'charset=["\x27]?gb2312', text, re.I), 'Declared charset changed')
    date = one(r'<!-- include 发布时间 begin -->(.*?)<!-- include 发布时间 end -->', text)
    require(compact(date) == '2003-06-0214:22', 'Publication changed')
    parser = Article(); parser.feed(text)
    require(parser.roots == 1 and parser.active is None, 'Article absent/duplicate/unclosed')
    require(compact(''.join(parser.visible)).count('《石器时代》任务功略-五兄弟之谜') == 1,
            'Visible article title absent or ambiguous')
    return compact(''.join(parser.parts))


def derive(raw):
    body = article(raw)
    recommended = int(one(r'等级要求：建议等级(\d+)级', body))
    require('2.交通工具：步行或骑宠。3.精灵的羽毛：福尔德村、达那村。' in body, 'Travel scope changed')
    require('由红、蓝、黄、绿、灰人龙所聚集的地盘' in body, 'Narrative colors changed')
    entrance = [int(x) for x in one(r'前往"五兄弟的山寨"（东(\d+)，南(\d+)）', body)]
    intro = one(r'地下1楼入口的红人龙"([^"]+)"（东(\d+)，南(\d+)）', body)
    board_coords = [[int(x), int(y)] for x, y in re.findall(r'作答区的看板（东(\d+)，南(\d+)）', body)]
    questions = re.findall(r'问题([一二三四五])：([^？]+)？([^。]+)。正确解答为"([^"]+)"。', body)
    require(len(board_coords) == 5 and [q[0] for q in questions] == list('一二三四五'), 'Five ordered questions required')
    papers = re.findall(r'一张"问题([1-5])的答案用纸"', body)
    require(papers == list('12345') and '道具栏预留五个空位' in body and '留一个宠物栏的空格' in body,
            'Paper/slot scope changed')
    quizzes = [{'floor_as_reported': i, 'board_coord': xy, 'question': q[1],
                'options_as_written': q[2].split('，'), 'answer_as_written': q[3],
                'paper_label': f'问题{i}的答案用纸', 'paper_id': None}
               for i, (xy, q) in enumerate(zip(board_coords, questions), 1)]
    require(all(q['answer_as_written'] in q['options_as_written'] for q in quizzes), 'Answer outside option list')
    blue = one(r'带着五张正确的答案纸，和五兄弟的山寨地下5楼的蓝人龙"([^"]+)"（东(\d+)，南(\d+)）', body)
    require('玩家一定要和奇洛斯说话两次才能顺利往下一层楼走' in body and
            '假若智能的水晶掉落或是离开这个世界时，就会瞬间消失' in body,
            'Two conversations or crystal lifecycle changed')
    passage = one(r'和黄人龙"([^"]+)"（东(\d+)，南(\d+)）说话，黄人龙见勇者身上带有五兄弟的秘宝，即会传送勇者至最后的地下6楼', body)
    last_board = [int(x) for x in one(r'找到问题看板（东(\d+)，南(\d+)）', body)]
    return_npc = one(r'地下6楼入口右边的"([^"]+)"说话，将会被传送回地下5楼', body)
    boss = one(r'和黄人龙"([^"]+)"（东(\d+)，南(\d+)）对话，确定黄人龙就是强者即会展开激战', body)
    require('击败它之后勇者便会被传送至后方的传送点' in body and
            '虽然无法与朋友组队战斗，但玩家可以在战斗时利用HELP按键' in body and
            '以让其它人在后来加入战斗行列' in body, 'Battle/HELP distinction changed')
    reward_warp = [int(x) for x in one(r'灰色传送点（东(\d+)，南(\d+)）传送至五兄弟兑奖处', body)]
    require('将智能的水晶交出' in body and '饰品及一级人龙一只' in body and
            '按下"确定"' in body and '按"取消"，就可以重新选择' in body, 'Choice/return scope changed')
    reward_section = one(r'5.获得物品：(.*?)6.获得宠物：', body)
    item_rows = re.findall(r'([^（）或：]+)（([^（）]+)）', reward_section)
    require(len(item_rows) == 5, 'Five accessory descriptions required')
    pairs = re.findall(r'与([红蓝黄绿灰])人龙对话可获得"([^"]+)"和一级"([^"]+)"', body)
    pet_summary = one(r'6.获得宠物：([^。]+)。', body).split('或')
    require([p[0] for p in pairs] == list('红蓝黄绿灰') and
            [p[1] for p in pairs] == [r[0] for r in item_rows] and
            [p[2] for p in pairs] == pet_summary, 'Reward summary/choice pairs disagree')
    rewards = []
    for (color, item, pet), (_, detail) in zip(pairs, item_rows):
        stats = re.findall(r'([攻防敏魅])([+-]\d+)', detail)
        require(stats and len({k for k, v in stats}) == len(stats), 'Malformed/duplicate accessory stats')
        spirit = re.sub(r'[攻防敏魅][+-]\d+', '', detail)
        skill = one(r'(.+精灵)(?:Lv(\d+))?$', spirit)
        rewards.append({'speaker_color': color, 'item_name': item, 'stats': {k: int(v) for k, v in stats},
                        'spirit_name': skill[0], 'spirit_level_as_written': int(skill[1]) if skill[1] else None,
                        'pet_name': pet, 'pet_level_as_reported': 1, 'item_id': None, 'pet_id': None,
                        'pet_growth_stats': None})
    require('每一次的转生过后，再解一次任务' in body and '五次的转生' in body, 'Repeat attribution changed')
    ecologies = []
    for number, name in [('7', '五兄弟的山寨'), ('8', '东吉鲁山岭')]:
        section = one(number + r'\.' + name + r'坐标：(.*?)怪物种类：([^<]+?)(?=' + name + r'(?:地下|1楼))', body)
        coords = [[int(x), int(y)] for x, y in re.findall(r'（东(\d+)，南(\d+)）', section[0])]
        levels = [int(x) for x in one(r'怪物等级：(\d+)~(\d+)', section[0])]
        labels = section[1].split('、')
        require(coords and len(labels) == 4, 'Ecology coordinate or label scope changed')
        ecologies.append({'map_label': name, 'coordinate_literals_as_reported': coords,
            'coordinate_frames': None, 'monster_levels_as_reported': levels, 'monster_labels_as_reported': labels,
            'map_id': None, 'encounter_weights': None, 'capture_eligibility': None})
    require(ecologies[0]['coordinate_literals_as_reported'] == [entrance], 'Entrance summary disagrees')
    def npc(row, color, floor, role):
        return {'name_as_written': row[0], 'color_as_written': color, 'floor_as_reported': floor,
                'coord_as_reported': [int(x) for x in row[1:]], 'role': role, 'npc_id': None}
    return {'recommended_level': recommended, 'hard_entry_level': None,
        'region_label': '吉鲁岛', 'entrance_coord_as_reported': entrance,
        'transport_as_reported': ['步行', '骑宠'], 'feather_locations_as_reported': ['福尔德村', '达那村'],
        'quizzes': quizzes, 'inventory_empty_slots_advised': 5, 'pet_empty_slots_advised': 1,
        'npc_occurrences': [npc(intro, '红', 1, 'introduction'), npc(blue, '蓝', 5, 'two_conversations_and_crystal'),
                            npc(passage, '黄', 5, 'crystal_condition_passage'), npc(boss, '黄', 6, 'final_battle')],
        'crystal': {'name': '智能水晶', 'variant_in_body': '智能的水晶', 'five_correct_papers_required': True,
            'paper_consumption': None, 'two_conversations_required_as_reported': True,
            'drop_disappears_as_reported': True, 'leaving_world_disappears_as_reported': True,
            'leaving_world_equates_to_logout_in_this_page': None, 'disconnect_behavior': None, 'item_id': None},
        'last_question_board_coord': last_board, 'return_npc_label': return_npc, 'return_floor_as_reported': 5,
        'battle': {'preformed_friend_party_not_available_as_reported': True, 'later_HELP_join_as_reported': True,
            'HELP_distance_limit': None, 'boss_stats': None, 'reward_warp_after_victory': reward_warp,
            'battle_id': None, 'party_admission_restriction_in_this_page': None},
        'reward_options': rewards, 'choice_confirm_grants_pair_as_reported': True,
        'cancel_allows_reselection_before_grant_as_reported': True, 'reward_roll_probability': None,
        'crystal_return_for_reward_as_reported': True,
        'repeat': {'after_each_rebirth_as_reported': True, 'five_rebirths_collection_advice': True,
            'universal_lifetime_attempt_cap': None, 'server_flag_reset_verified': False},
        'ecology': ecologies, 'npc_alias_join': None, 'quest_id': None, 'exact_game_build': None,
        'original_server_runtime_verified': False}


def catalog(ex):
    rows = [('quests', 'documentary_quest_description', ex)]
    rows += [('items', 'documentary_accessory_reward', r) for r in ex['reward_options']]
    rows += [('pets', 'documentary_chosen_pet_reward_not_species_master',
              {k: r[k] for k in ('speaker_color', 'pet_name', 'pet_level_as_reported', 'pet_id', 'pet_growth_stats')})
             for r in ex['reward_options']]
    rows += [('maps', 'documentary_ecology_labels_not_original_geometry', r) for r in ex['ecology']]
    return [{'record_id': f'CN2003-SINA-R71-{i:02d}', 'entity_type': kind, 'collection': collection,
        'version_profile': PROFILE, 'source_refs': ['S1', 'S2'], 'verification_status': 'SOURCE_DESCRIPTION_NOT_RUNTIME',
        'rights_status': 'RESEARCH_METADATA_NOT_RELEASE_APPROVED', 'record_revision': 1, 'game_ids': None, 'content': content}
        for i, (collection, kind, content) in enumerate(rows, 1)]


def pin(path):
    raw = (ROOT / path).read_bytes()
    return {'path': path, 'bytes': len(raw), 'sha256': sha(raw),
            'git_blob': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}


def verify_report(report):
    require(report['version_profile'] == PROFILE and report['negative_boundaries'] == BOUNDARIES,
            'Evidence/version boundaries changed')
    ex = report['extraction']
    require(report['catalog_records'] == catalog(ex), 'Detached/promoted catalogue')
    for key in ('hard_entry_level', 'reward_roll_probability', 'npc_alias_join', 'quest_id', 'exact_game_build'):
        require(ex[key] is None, 'Unknown promoted: ' + key)
    for key in ('paper_consumption', 'leaving_world_equates_to_logout_in_this_page', 'disconnect_behavior', 'item_id'):
        require(ex['crystal'][key] is None, 'Crystal lifecycle/identity promoted')
    for key in ('HELP_distance_limit', 'boss_stats', 'battle_id', 'party_admission_restriction_in_this_page'):
        require(ex['battle'][key] is None, 'Battle scope promoted')
    require(ex['original_server_runtime_verified'] is False and ex['repeat']['server_flag_reset_verified'] is False and
            ex['repeat']['universal_lifetime_attempt_cap'] is None, 'Runtime/repeat promoted')
    require(all(r['item_id'] is r['pet_id'] is r['pet_growth_stats'] is None for r in ex['reward_options']) and
            all(n['npc_id'] is None for n in ex['npc_occurrences']), 'Original identity/stats invented')
    require(all(all(e[k] is None for k in ('coordinate_frames', 'map_id', 'encounter_weights', 'capture_eligibility'))
                for e in ex['ecology']), 'Map identity/encounter execution invented')
    require(len(report['parent_pins']) == 2 and all(pin(p['path']) == p for p in report['parent_pins']),
            'Parent bytes/Git identity changed')
    require(all(q['paper_id'] is None for q in ex['quizzes']), 'Paper identity invented')
    require(report['original_html_or_assets_in_output'] is False and report['original_game_runtime_verified'] is False,
            'Original asset/runtime status promoted')
    for page in report['source_pages']:
        require(page['official_authorship_verified'] is False and page['exact_game_build'] is None and
                page['named_original_author'] is None and page['replacement_characters'] == 0,
                'Source author/build authority promoted')
    parent = json.loads((ROOT / report['parent_pins'][0]['path']).read_text())
    old = next(p for p in parent['observations']['guide_profiles'] if p['id'] == 'FIVE_BROTHERS')
    comparison = report['previous_guide_comparison']
    require(comparison['parent_profile'] == old and comparison['shared_crystal_original_id_verified'] is False and
            comparison['new_page_party_admission_restriction'] is None and
            comparison['textual_similarity_establishes_copy_lineage'] is False,
            'Previous guide evidence promoted or replaced')
    h = report['historical_comparison']
    require(h['reference_capture'] == '20031204051508' and h['selected_full_visible_article_equal'] is True and
            h['independent_witness_count'] == 1 and h['first_publication_authenticated'] is False and
            h['current_raw_equals_archive_raw'] is False, 'Historical authority promoted')
    require([(p['id'], p['url']) for p in report['source_pages']] == list(URLS.items()), 'Source detached')


MUTATIONS = (('建议等级60级', '建议等级61级'), ('2003-06-02 14:22', '2003-06-03 14:22'),
    ('东343，南191', '东343，南192'), ('红人龙"吉诺"', '红人龙"别名甲"'),
    ('东10，南9', '东11，南9'), ('正确解答为"424KG"', '正确解答为"434KG"'),
    ('正确解答为"火风"', '正确解答为"风火"'), ('问题5的答案用纸', '问题4的答案用纸'),
    ('道具栏预留五个空位', '道具栏预留四个空位'), ('宠物栏的空格', '道具栏的空格'),
    ('说话两次', '说话一次'), ('掉落或是离开这个世界', '掉落或是断线'),
    ('黄人龙"浦鲁德"', '黄人龙"布鲁德"'), ('东25，南9', '东24，南9'),
    ('传送回地下5楼', '传送回地下4楼'), ('无法与朋友组队战斗', '可以与朋友组队战斗'),
    ('在战斗时利用HELP', '在战斗前利用HELP'), ('按"取消"，就可以重新选择', '按"取消"，就会领取奖品'),
    ('攻-3魅+4光的精灵', '攻-2魅+4光的精灵'), ('滋润的精灵Lv2', '滋润的精灵Lv3'),
    ('和一级"扬奇洛斯"', '和一级"邦奇诺"'), ('每一次的转生过后', '每一次的登录过后'),
    ('怪物等级：44~46级', '怪物等级：45~46级'), ('东393，南245', '东394，南245'),
    ('怪物种类：布鲁德、布比、布伊比、布伊', '怪物种类：另一怪物、布比、布伊比、布伊'))


def audit(raw, expected):
    text = raw.decode('gb18030')
    for old, new in MUTATIONS:
        require(old in text, 'Real-source mutation absent: ' + old)
        try:
            actual = derive(text.replace(old, new).encode('gb18030'))
        except ValueError:
            continue
        require(actual != expected, 'Semantic mutation accepted: ' + old)
    require(derive(raw + b'<script>chrome=1</script>') == expected, 'Peripheral script altered evidence')
    return {'semantic_mutations_rejected_without_digest_gate': len(MUTATIONS), 'peripheral_script_positive': True}


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--fetch', action='store_true'); g.add_argument('--input-dir')
    p.add_argument('--output', required=True); args = p.parse_args()
    report = json.loads(REPORT.read_text()); verify_report(report)
    inputs, extractions, scopes, audits = [], [], [], []
    for sid, url in URLS.items():
        if args.fetch:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'StoneAge-research/1.0'}), timeout=45) as r:
                require(r.status == 200 and r.url == url, 'HTTP identity changed')
                raw = r.read(2_000_001)
        else:
            raw = (Path(args.input_dir) / ('current.html' if sid == 'S1' else 'archive.html')).read_bytes()
        require(0 < len(raw) <= 2_000_000, 'Source size outside bound')
        actual = derive(raw); require(actual == report['extraction'], 'Documentary semantics changed')
        scopes.append(article(raw)); extractions.append(actual); audits.append({'id': sid, **audit(raw, actual)})
        inputs.append({'id': sid, 'url': url, 'bytes': len(raw), 'sha256': sha(raw)})
    require(scopes[0] == scopes[1], 'Current and historical selected full article differ')
    h = report['historical_comparison']
    require(len(scopes[0]) == h['visible_compact_characters'] and sha(scopes[0].encode()) == h['visible_compact_utf8_sha256'],
            'Selected article changed')
    out = {'schema': 'stoneage.five_brothers.replay.r1', 'inputs': inputs, 'extraction': extractions[0],
        'catalog_records': catalog(extractions[0]), 'historical_comparison': h, 'audit': audits,
        'original_html_or_assets_in_output': False, 'original_game_runtime_verified': False}
    target = Path(args.output); target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'inputs': inputs, 'catalog_records': len(out['catalog_records']), 'audits': audits}))


if __name__ == '__main__':
    main()
