"""R70: source-qualified special-pet eligibility and temporary battle states."""
import argparse
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-CN30-SPECIAL-PET-SKILLS'
REPORT = ROOT / f'research/recovered/{STEM}-SOURCE-R1.json'
URLS = ('https://games.sina.com.cn/zhuanqu/stoneage3/yaosu.shtml',
        'https://games.sina.com.cn/zhqu/sta/article/2003-05-01/3953.shtml',
        'https://web.archive.org/web/20030324221124id_/http://games.sina.com.cn:80/zhuanqu/stoneage3/yaosu.shtml')
PROFILES = {'S1': 'CN30_SINA_PORTAL_TOPIC_DATE_AND_AUTHOR_UNKNOWN',
            'S2': 'CN2003_HUANG_JIANZHI_ESSAY_QUOTES_UNIDENTIFIED_MAGAZINE_ABOUT_CN30'}
BOUNDARIES = {k: False for k in ('operator_authorship_verified', 'current_http_pages_are_authenticated_historical_bytes',
    'independent_rule_witnesses_established', 'tw10_jss1999_rules_backfilled', 'same_build_ids_proven',
    'eighty_is_fixed_payout', 'ally_target_is_tested_fact', 'dismount_is_permanent',
    'unlimited_uses_means_no_cost_or_guaranteed_hit', 'original_game_runtime_verified',
    'old_r56_t_prefix_unknown_overwritten', 'original_html_or_assets_committed', 'stage_b_started')}


def require(ok, message):
    if not ok: raise ValueError(message)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def compact(s): return re.sub(r'\s+', '', s)


def one(pattern, text):
    rows = re.findall(pattern, text)
    require(len(rows) == 1, 'Missing/duplicated evidence: ' + pattern)
    return rows[0]


class SourceScope(HTMLParser):
    """Visible anchored sections for S1; actual article paragraphs for S2."""
    def __init__(self):
        super().__init__()
        self.hidden = 0; self.visible = []; self.sections = {}; self.section = None; self.anchors = []
        self.td_depth = 0; self.root = None; self.roots = 0; self.paragraph = None; self.paragraphs = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'iframe', 'noscript'): self.hidden += 1
        if self.hidden: return
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('name') in ('3', '4', '5', '6'):
            key = attrs['name']; self.anchors.append(key)
            require(key not in self.sections, 'Duplicate selected section anchor')
            self.section = key; self.sections[key] = []
        if tag == 'td':
            self.td_depth += 1
            if 'l15z' in attrs.get('class', '').split():
                require(self.root is None, 'Nested article root')
                self.root = self.td_depth; self.roots += 1
        if tag == 'p' and self.root is not None:
            if self.paragraph is not None: self.paragraphs.append(compact(''.join(self.paragraph)))
            self.paragraph = []

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'iframe', 'noscript'):
            if self.hidden: self.hidden -= 1
            return
        if self.hidden: return
        if tag == 'p' and self.paragraph is not None:
            self.paragraphs.append(compact(''.join(self.paragraph))); self.paragraph = None
        if tag == 'td':
            if self.root == self.td_depth:
                require(self.paragraph is None, 'Article ended before paragraph')
                self.root = None
            self.td_depth -= 1

    def handle_data(self, text):
        if self.hidden: return
        self.visible.append(text)
        if self.section is not None: self.sections[self.section].append(text)
        if self.paragraph is not None: self.paragraph.append(text)


def source(raw):
    text = raw.decode('gb18030', errors='strict')
    require(re.search(r'charset=gb2312', text, re.I), 'Charset changed')
    p = SourceScope(); p.feed(text)
    return text, p


def skill_block(text, source_ref):
    # Keep original labels, including full-width numerals and editorial typos.
    skills = one(r'这些宠物技能有[：:]?([^。]+)。其中除了', text).split('、')
    require(len(skills) == 7 and len(set(skills)) == 7 and skills.count('捐献') == 1, 'Seven distinct reported skills required')
    prefix, machine = one(r'有([ＴT])字的宠技只能让特殊的宠物学习，那就是[“‘]([^”’]+)[”’]', text)
    gold = one(r'然而[“‘]捐献[”’]的技能，也只有[“‘]([^”’]+)[”’]', text)
    require(machine == '帖拉所伊朵' and gold == '扑满乌力', 'Special-pet label changed')
    require(('如果你用其他的宠物去学这些技能，是学不来的' in text or
             '如果你用其他的宠物去学这些技能，那就是学不到来的' in text), 'Eligibility exclusion removed')
    return [{'source_ref': source_ref, 'name_as_written': name,
        'prefix_reported_for_category': None if name == '捐献' else prefix,
        'eligible_pet_label_as_reported': gold if name == '捐献' else machine,
        'skill_id': None, 'pet_id': None, 'cost': None, 'effect_formula': None,
        'verification_status': 'PORTAL_DESCRIPTION' if source_ref == 'S1' else 'ESSAY_QUOTING_UNIDENTIFIED_MAGAZINE'}
        for name in skills]


def donation(text, source_ref):
    require(re.search(r'不是攻击用的?，?也不是?合成或料理的技能', text), 'Non-attack/crafting/cooking description changed')
    require(('必需使用在战斗中' in text or '必需使用战斗中' in text), 'Battle context lost')
    require('不管对手是人物还是宠物' in text and '只能得到石币' in text, 'Target/currency scope changed')
    amount = int(one(r'战斗结束后发现可以从克克尔身上取得(\d+)石币', text))
    waiting, battle = one(r'使用[“‘]捐献[”’]技能后，扑满乌力就会变成[“‘]([^”’]+)[”’]状态，你必需再召唤他回到[“‘]([^”’]+)[”’]状态', text)
    require(waiting == '等待' and battle == '战斗' and '才能进行下一回合的' in text, 'Post-skill state sequence changed')
    return {'source_ref': source_ref, 'context': 'BATTLE', 'described_as_not_attack_crafting_or_cooking': True, 'actor_label': '扑满乌力',
        'opponent_categories_as_reported': ['人物', '宠物'], 'obtained_resource_label': '石币',
        'example': {'target_label': '克克尔', 'amount': amount, 'scope': 'ONE_NARRATIVE_EXAMPLE_NOT_FORMULA'},
        'after_use_state_as_written': waiting, 'manual_return_state_as_written': battle,
        'next_use_timing_as_reported': 'NEXT_TURN_AFTER_RETURN_TO_BATTLE_STATE',
        'fixed_payout': None, 'success_probability': None, 'target_actual_balance_delta': None,
        'actual_server_state_enum': None, 'runtime_verified': False}


def derive_primary(raws):
    text1, p1 = source(raws[0]); text2, p2 = source(raws[1])
    require('石器时代3.0新增要素' in compact(''.join(p1.visible)), 'Portal topic header changed')
    require(p1.anchors == ['3', '4', '5', '6'], 'Selected anchor scope/order changed')
    s1 = compact(''.join(p1.sections['5'])); gp = compact(''.join(p1.sections['3']))
    require(s1.startswith('开放宠物新技能') and gp.startswith('超级可爱逗趣GP宠物诞生'), 'Section titles changed')
    require(p2.roots == 1 and p2.root is None, 'Essay article scope invalid')
    dates = re.findall(r'<!-- include 发布时间 begin -->(.*?)<!-- include 发布时间 end -->', text2, re.S)
    require(dates == ['2003-05-01 06:52'], 'Essay publication changed')
    require(re.search(r'<td style=padding-left:40px>\s*黄建枝</td>', text2) and
            '黄建枝' in compact(''.join(p2.visible)) and '2003-05-0106:52' in compact(''.join(p2.visible)),
            'Essay visible byline/date changed')
    paras = p2.paragraphs
    eligibility = [p for p in paras if p.startswith('据杂志报道：“开放宠物新技能：')]
    require(len(eligibility) == 1 and '《石器时代3.0版本伊甸新大陆》' in eligibility[0], 'Magazine quote/version scope missing')
    accounts = [p for p in paras if p.startswith('杂志报道：“这是只有扑满乌力')]
    ally = [p for p in paras if p.startswith('也听说：“‘捐献’的技能也可能')]
    require(len(accounts) == len(ally) == 1 and '自己队友身上' in ally[0], 'Magazine account/hearsay not separated')
    require(any('我是从石器时代5.0开始玩的' in p for p in paras), 'Author starting-era qualification missing')
    require(any('我也不够清楚' in p and '新技能“捐献”' in p for p in paras), 'Author uncertainty erased')
    rows1 = skill_block(s1, 'S1'); rows2 = skill_block(eligibility[0], 'S2')
    effect1 = donation(s1, 'S1'); effect2 = donation(accounts[0], 'S2')
    coordinates = one(r'卡鲁它那的庄园（南岛(\d+)，(\d+)）.*?卡鲁它那庄园(\d+)，(\d+)）', s1)
    outer, inner = coordinates[:2], coordinates[2:]
    require('不是该庄园家族族员也是进得去的' in s1, 'Nonmember access description changed')
    essay_coord = [int(n) for n in one(r'卡鲁它那的庄园里的坐标(\d+)，(\d+)\)', eligibility[0])]
    require('听说“捐献”技能也可能会使用在自己队友身上' in s1, 'Portal hearsay qualifier changed')
    require('机暴是五转的转生宠' in s1 and '只有五转后的人物才能驾驭机暴' in s1 and
            '用交易换来的话，也要看你有没有资格（五转）使用' in s1, 'Control/rebirth claim changed')
    require('扑满乌力目前尚无任务或可以补抓到的地方' in s1 and '扑满乌力抽奖活动' in s1 and
            '如果你可以用交易方式取得' in s1 and '等级是否低于交易的扑满乌力' in s1, 'Acquisition/time/level qualifier changed')
    require('便恢复成单人状况' in gp and '原先骑乘的宠物，也不能叫出来战斗' in gp and
            '落马者必需等回合结束后，才能对原先骑乘的宠物做调度' in gp and
            '落马技的使用是不限次数的' in gp, 'Temporary dismount restrictions changed')
    return {'source_skill_rows': rows1 + rows2, 'donation_descriptions': [effect1, effect2],
        'training_locations': [
            {'source_ref': 'S1', 'village_as_written': '卡鲁它那庄园', 'outer_south_island_coordinate': list(map(int, outer)),
             'inside_manor_coordinate': list(map(int, inner)), 'nonmember_entry_reported': True, 'npc_id': None},
            {'source_ref': 'S2', 'village_as_written': '卡鲁它那的庄园', 'outer_south_island_coordinate': None,
             'inside_manor_coordinate': essay_coord, 'nonmember_entry_reported': None, 'npc_id': None}],
        'ally_target_claims': [{'source_ref': ref, 'qualifier': 'HEARSAY_POSSIBLE', 'tested': False} for ref in ('S1', 'S2')],
        'portal_acquisition': {'machine_rebirth_label': '五转', 'control_word_as_written': '驾驭',
            'control_means_riding_or_general_use': None, 'trade_does_not_remove_reported_machine_qualification': True,
            'gold_pig_pack_lottery_reported': True, 'gold_pig_player_trade_reported': True,
            'gold_pig_character_pet_level_inequality': None, 'claim_is_time_qualified_not_all_eras': True},
        'gp_dismount': {'source_ref': 'S1', 'actor_category': 'GP宠物', 'skill_label': '落马技',
            'rider_returns_to_single_state_as_reported': True, 'former_mount_cannot_enter_battle_until_turn_end_as_reported': True,
            'former_mount_dispatch_after_turn_end_as_reported': True, 'use_count_unrestricted_as_reported': True,
            'success_probability': None, 'cost': None, 'remount_next_turn_guaranteed': None, 'species_ids': None},
        'source_relationship': {'shared_example_amount': effect1['example']['amount'] == effect2['example']['amount'],
            'shared_post_skill_state_words': True, 'independent_witnesses_established': False,
            'direct_copy_or_common_ancestor_proven': False, 'same_skill_or_pet_ids_established': False,
            'two_last_skill_literals': [rows1[-1]['name_as_written'], rows2[-1]['name_as_written']],
            'author_reports_started_at_5_0': True, 'magazine_identity': None, 'magazine_original_acquired': False},
        'exact_game_build': None, 'original_game_runtime_verified': False}


def derive(raws):
    require(len(raws) == 3, 'Two current pages and exact archived reference required')
    current = derive_primary(raws[:2])
    _, current_scope = source(raws[0]); _, old_scope = source(raws[2])
    core_hashes = {}
    for key in ('3', '5'):
        a = compact(''.join(current_scope.sections[key])); b = compact(''.join(old_scope.sections[key]))
        require(a == b, 'Current/archive selected full text differs')
        core_hashes[key] = {'utf8_bytes': len(a.encode()), 'sha256': sha(a.encode())}
    historical = derive_primary([raws[2], raws[1]])
    require(current == historical, 'Selected current/20030324 documentary semantics differ')
    current['historical_comparison'] = {'source_ref': 'S3', 'capture_timestamp': '20030324221124',
        'selected_s1_semantics_equal': True, 'current_and_archived_raw_bytes_equal': raws[0] == raws[2],
        'original_publication_date_established': False, 'same_game_build_authenticated': False,
        'selected_visible_core_hashes': core_hashes}
    return current


def catalog(ex):
    result = []
    for i, row in enumerate(ex['source_skill_rows']):
        result.append({'record_id': f'CN30-R70-SKILL-{i + 1:02}', 'entity_type': 'documentary_special_pet_skill',
            'collection': 'skills', 'version_profile': PROFILES[row['source_ref']], 'source_refs': (['S1', 'S3'] if row['source_ref'] == 'S1' else ['S2']),
            'verification_status': row['verification_status'], 'rights_status': 'RESEARCH_METADATA_NOT_RELEASE_APPROVED',
            'record_revision': 1, 'game_ids': None, 'content': row})
    result.append({'record_id': 'CN30-R70-DISMOUNT', 'entity_type': 'documentary_mount_state_constraint',
        'collection': 'riding', 'version_profile': PROFILES['S1'], 'source_refs': ['S1', 'S3'],
        'verification_status': 'PORTAL_DESCRIPTION_NOT_RUNTIME', 'rights_status': 'RESEARCH_METADATA_NOT_RELEASE_APPROVED',
        'record_revision': 1, 'game_ids': None, 'content': ex['gp_dismount']})
    return result


def pin(path):
    raw = (ROOT / path).read_bytes()
    return {'path': path, 'bytes': len(raw), 'sha256': sha(raw),
            'git_blob': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}


def verify_report(report):
    require(report['source_profiles'] == PROFILES and report['negative_boundaries'] == BOUNDARIES, 'Source/evidence authority changed')
    ex = report['extraction']; require({k: v for k, v in ex['historical_comparison'].items() if k != 'selected_visible_core_hashes'} == {
        'source_ref': 'S3', 'capture_timestamp': '20030324221124', 'selected_s1_semantics_equal': True,
        'current_and_archived_raw_bytes_equal': False, 'original_publication_date_established': False,
        'same_game_build_authenticated': False}, 'Historical capture qualification changed')
    require(set(ex['historical_comparison']['selected_visible_core_hashes']) == {'3', '5'} and all(
        x['utf8_bytes'] > 0 and re.fullmatch(r'[0-9a-f]{64}', x['sha256'])
        for x in ex['historical_comparison']['selected_visible_core_hashes'].values()), 'Missing selected core hashes')
    require(report['catalog_records'] == catalog(ex), 'Catalog detached or promoted')
    require(ex['exact_game_build'] is None and ex['original_game_runtime_verified'] is False, 'Runtime/build invented')
    for row in ex['source_skill_rows']:
        require(all(row[k] is None for k in ('skill_id', 'pet_id', 'cost', 'effect_formula')), 'Original skill values invented')
    for desc in ex['donation_descriptions']:
        require(all(desc[k] is None for k in ('fixed_payout', 'success_probability', 'target_actual_balance_delta', 'actual_server_state_enum'))
                and desc['runtime_verified'] is False, 'Narrative example became formula/runtime')
    require(all(r['qualifier'] == 'HEARSAY_POSSIBLE' and r['tested'] is False for r in ex['ally_target_claims']), 'Hearsay promoted')
    relation = ex['source_relationship']
    require(all(relation[k] is False for k in ('independent_witnesses_established', 'direct_copy_or_common_ancestor_proven',
            'same_skill_or_pet_ids_established', 'magazine_original_acquired')) and relation['magazine_identity'] is None,
            'Source genealogy/authority invented')
    require(ex['portal_acquisition']['control_means_riding_or_general_use'] is None and
            ex['portal_acquisition']['gold_pig_character_pet_level_inequality'] is None and
            ex['training_locations'][1]['outer_south_island_coordinate'] is None and
            ex['training_locations'][1]['nonmember_entry_reported'] is None and
            all(x['npc_id'] is None for x in ex['training_locations']), 'Unstated qualification or NPC invented')
    require(all(ex['gp_dismount'][k] is None for k in ('success_probability', 'cost', 'remount_next_turn_guaranteed', 'species_ids')),
            'Dismount execution promoted')
    require(len(report['parent_pins']) == 3 and all(pin(p['path']) == p for p in report['parent_pins']), 'Parent evidence changed')


MUTATIONS = ((0, '不是该庄园家族族员也是进得去的', '只有该庄园家族族员才进得去'),
    (0, '南岛274，532', '南岛275，532'), (0, '卡鲁它那庄园39，17', '卡鲁它那庄园39，18'),
    (0, '不防守战法２', '不防守战法４'), (0, '背水之战之３', '背水一战之３'),
    (1, '2003-05-01 06:52', '2003-05-02 06:52'), (1, '黄建枝</td>', '另一作者</td>'),
    (1, '我是从石器时代5.0开始玩的', '我是从石器时代1.0开始玩的'),
    (1, '据杂志报道：', '亲自测试证实：'), (1, '背水一战战之3', '背水之战之3'),
    (0, '取得80石币', '取得90石币'), (1, '取得80石币', '取得90石币'),
    (0, '变成“等待”状态', '变成“休息”状态'), (1, '回到‘战斗’状态', '回到‘休息’状态'),
    (0, '听说“捐献”技能也可能', '确认“捐献”技能一定'), (1, '也听说：', '已证实：'),
    (0, '等回合结束后', '等战斗结束后'), (0, '使用是不限次数的', '使用是仅限一次的'),
    (0, '只有五转后的人物', '只有四转后的人物'), (0, '如果你可以用交易方式取得', '禁止交易方式取得'),
    (0, '不是攻击用，也不是合成或料理的技能', '是攻击用，也是合成或料理的技能'),
    (2, '卡鲁它那庄园39，17', '卡鲁它那庄园39，18'), (2, '等回合结束后', '等战斗结束后'))


def audit(raws, expected):
    for idx, old, new in MUTATIONS:
        text = raws[idx].decode('gb18030'); require(old in text, 'Real-source mutation absent')
        changed = list(raws); changed[idx] = text.replace(old, new).encode('gb18030')
        try: actual = derive(changed)
        except ValueError: continue
        require(actual != expected, 'Semantic mutation accepted')
    for idx in range(3):
        changed = list(raws); changed[idx] += b'<script>peripheral=1</script>'
        require(derive(changed) == expected, 'Peripheral script affected semantics')
    return {'semantic_mutations_rejected_without_digest_gate': len(MUTATIONS), 'three_peripheral_script_positives': True}


def main():
    p = argparse.ArgumentParser(); g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--fetch', action='store_true'); g.add_argument('--inputs', nargs=3)
    p.add_argument('--output', required=True); args = p.parse_args()
    report = json.loads(REPORT.read_text()); verify_report(report)
    raws, inputs = [], []
    for i, url in enumerate(URLS):
        if args.fetch:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'StoneAge-research/1.0'}), timeout=45) as r:
                require(r.status == 200 and r.url == url, 'HTTP identity changed'); raw = r.read(2_000_001)
        else: raw = Path(args.inputs[i]).read_bytes()
        require(len(raw) <= 2_000_000, 'Source exceeds bound'); raws.append(raw)
        inputs.append({'id': f'S{i+1}', 'url': url, 'bytes': len(raw), 'sha256': sha(raw)})
    ex = derive(raws); require(ex == report['extraction'], 'Source semantics changed')
    out = {'schema': 'stoneage.cn30_special_pet_skills.replay.r1', 'inputs': inputs, 'extraction': ex,
        'catalog_records': catalog(ex), 'audit': audit(raws, ex),
        'original_html_or_assets_in_output': False, 'original_game_runtime_verified': False}
    path = Path(args.output); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'inputs': inputs, 'source_skill_rows': 14, 'catalog_records': 15}))


if __name__ == '__main__': main()
