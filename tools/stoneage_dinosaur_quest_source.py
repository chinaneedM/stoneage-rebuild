"""Bounded documentary source replay, not a quest engine or original server test."""
import argparse
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'STONEAGE-EARLY-DINOSAUR-QUEST'
REPORT = ROOT / f'research/recovered/{PREFIX}-SOURCE-R1.json'
URLS = (
    'https://games.sina.com.cn/handbook/0101/01186091.shtml',
    'https://games.sina.com.cn/handbook/0101/01186091_c2.shtml',
    'https://games.sina.com.cn/zhqu/sta/rwgl1_2.shtml',
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(b):
    return hashlib.sha256(b).hexdigest()


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts, self.links, self.anchors = [], [], []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript', 'iframe'):
            self.hidden += 1
        if tag == 'a' and not self.hidden:
            a = dict(attrs)
            if 'href' in a:
                self.links.append(a['href'])
            if 'name' in a:
                self.anchors.append((a['name'], len(self.parts)))

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript', 'iframe') and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def norm(t):
    return re.sub(r'\s+', '', t)


def decode(raw):
    # Known invalid bytes occur in unrelated navigation/other quest names.
    # The selected business section must separately contain no replacement.
    s = raw.decode('gb18030', errors='replace')
    p = Page()
    p.feed(s)
    return s, p


def section(p, start, end):
    points = dict(p.anchors)
    require(sum(a == start for a, _ in p.anchors) == 1, 'Missing/duplicate source section')
    require(sum(a == end for a, _ in p.anchors) == 1, 'Missing/duplicate next section')
    require(points[start] < points[end], 'Reversed source anchors')
    return norm(''.join(p.parts[points[start]:points[end]]))


def between(t, a, b):
    require(t.count(a) == t.count(b) == 1, 'Missing/duplicate source headings')
    require(t.index(a) < t.index(b), 'Reversed source headings')
    return t.split(a)[1].split(b)[0]


def match(pattern, text):
    m = re.search(pattern, text)
    require(m is not None, 'Source assertion changed: ' + pattern)
    return m.groups()


def extract(raws):
    require(len(raws) == 3, 'Exactly three HTML inputs required')
    decoded = [decode(b) for b in raws]
    index = decoded[0][1]
    require(index.links.count('/handbook/0101/01186091_c2.shtml#17') == 1,
            'Actual dinosaur detail link absent/ambiguous')
    for _, p in decoded[:2]:
        require('游民部落网友松鼠1206提供' in norm(''.join(p.parts)), 'Compiler credit changed')
    early = section(decoded[1][1], '17', '18')
    later_text = norm(''.join(decoded[2][1].parts))
    require('2003-05-2911:37' in later_text and '网友投稿' in later_text, 'Later date/byline changed')
    one = between(later_text, '恐龙博士（一）1.等级要求：', '恐龙博士（二）1.等级要求：')
    two = between(later_text, '恐龙博士（二）1.等级要求：', '7.柯奥山的小洞窟')
    require(all('\ufffd' not in t for t in (early, one, two)), 'Damaged selected source section')
    require('恐龙博士' in early, 'Wrong early section')
    early_pet, early_level = match(r'过桥后的(.+?)，等级(十五)以上', early)
    early_bonus = match(r'练到(十八)级以上就可换到(.+?)（光之精灵）或同等的装备', early)
    early_second = match(r'第二个是南岛的(.+?)（绿毛老虎）', early)[0]
    require('等级三十' in early and '养到三十级' in early, 'Early second target level changed')
    early_reward, early_reward_level = match(r'叫(.+?)的银色小龙LV(\d+)', early)
    npc, x, y = match(r'恐龙博士"([^"<>]+)"（东(\d+)，南(\d+)）', one)
    assistant = match(r'"助手(.+?)"详细询问', one)[0]
    later_pet, later_level = match(r'等级(\d+)级以上的(.+?)，如果', one)[::-1]
    later_reward = match(r'最好的东西为"(.+?)"（魅\+(\d+)光的精灵）', one)
    recommended = [int(match(r'建议等级(\d+)级', t)[0]) for t in (one, two)]
    require('特殊要求：解过恐龙博士（一）' in two, 'Second quest predecessor changed')
    second_level, second_pet = match(r'确定博士要的恐龙是等级(\d+)的(.+?)（绿虎）', two)
    reward = match(r'获得宠物："(.+?)"', two)[0]
    require('并没有等级30以上的贝鲁卡' in two, 'Wild versus raised distinction changed')
    require('超过1只以上的鲁尼帖斯' in one and '超过1只以上的贝鲁卡' in two,
            'Multiple-owned-pet selection warning absent')
    require('连身上骑的贝鲁卡也要小心' in two, 'Mounted-pet warning absent')
    entrance = [int(n) for n in match(r'小洞窟"（东(\d+)，南(\d+)）', one)]
    require('六楼' in one and '最上层' in early, 'Floor wording changed')
    return {
        'compiler': {
            'quest_1': {'target_label': early_pet, 'target_level_min_as_written': early_level,
                        'special_reward_level_min_as_written': early_bonus[0],
                        'special_reward_label': early_bonus[1], 'equivalent_equipment_alternative': True},
            'quest_2': {'target_label': early_second, 'requested_level': 30,
                        'reward_label': early_reward, 'reward_level': int(early_reward_level)},
            'npc_personal_name': None, 'floor_wording': '最上层',
        },
        'dated_2003': {
            'npc': {'name': npc, 'role': '恐龙博士', 'local_xy': [int(x), int(y)],
                    'floor_as_written': 6, 'entrance_xy': entrance},
            'assistant': {'name': assistant, 'role': '助手', 'xy': None},
            'quest_1': {'target_label': later_pet, 'target_level_min': int(later_level),
                        'recommended_player_level': recommended[0], 'required_player_level': None,
                        'reward_kind': 'RANDOM_ITEM', 'best_reward_label': later_reward[0],
                        'best_reward_charm': int(later_reward[1]), 'reward_probability': None},
            'quest_2': {'target_label': second_pet, 'requested_level': int(second_level),
                        'recommended_player_level': recommended[1], 'required_player_level': None,
                        'predecessor': 'quest_1', 'reward_label': reward, 'reward_level': None,
                        'must_raise_captured_pet_to_requested_level': True,
                        'multiple_pet_selection_unspecified': True, 'mounted_pet_warning': True},
        },
        'selected_semantic_sha256': [digest(t.encode()) for t in (early, one, two)],
        'decoding_replacements': [s.count('\ufffd') for s, _ in decoded],
    }


def audit(raws, expected):
    mutations = [
        (0, '/handbook/0101/01186091_c2.shtml#17', '/handbook/0101/01186091_c2.shtml#18'),
        (1, '等级十五以上', '等级十六以上'),
        (1, '练到十八级以上', '练到十九级以上'),
        (1, '阿西美加护符', '阿西美拉护符'),
        (1, '银色小龙LV1', '银色小龙LV2'),
        (2, '2003-05-29', '2004-05-29'),
        (2, '建议等级15级', '建议等级16级'),
        (2, '等级15级以上的鲁尼帖斯', '等级16级以上的鲁尼帖斯'),
        (2, '（东11，南12）', '（东12，南11）'),
        (2, '解过恐龙博士（一）', '解过恐龙博士（二）'),
        (2, '并没有等级30以上的贝鲁卡', '也有等级30以上的贝鲁卡'),
        (2, '连身上骑的贝鲁卡也要小心', '只有未骑乘的贝鲁卡需要小心'),
    ]
    for i, old, new in mutations:
        changed = list(raws)
        a, b = old.encode('gb18030'), new.encode('gb18030')
        require(a in changed[i], 'Counterfactual anchor not exercised')
        changed[i] = changed[i].replace(a, b)
        try:
            require(extract(changed) == expected, 'Changed source semantics')
        except ValueError:
            continue
        raise ValueError('Source mutation was accepted: ' + old)
    peripheral = list(raws)
    peripheral[2] += b'<script>unused_tracking_update=1;</script>'
    require(extract(peripheral) == expected, 'Peripheral script changed selected semantics')
    return {'real_input_mutations_rejected': len(mutations), 'peripheral_script_positive': True,
            'original_game_runtime_verified': False}


def check_archive(report):
    require(report['scope']['runtime_verified'] is False, 'Documentary source promoted to runtime')
    require(report['scope']['historical_bytes_authenticated'] is False, 'Current HTML promoted to historical bytes')
    require(report['scope']['exact_build'] is None, 'Unverified build assigned')
    require(report['scope']['independent_source_authors_established'] is False, 'Unverified source independence')
    records = report['archive_records']
    require(len(records) == 6 and len({r['record_id'] for r in records}) == 6, 'Wrong documentary archive set')
    require({(tuple(r['source_refs']), r['source_key']) for r in records} ==
            {(('S1',), 'quest_1'), (('S1',), 'quest_2'), (('S2',), 'npc'),
             (('S2',), 'assistant'), (('S2',), 'quest_1'), (('S2',), 'quest_2')},
            'Incomplete or duplicated documentary attribution')
    for r in records:
        require(all(k in r for k in ('record_id', 'collection', 'version_profile', 'source_refs',
                                    'verification_status', 'rights_status', 'record_revision')), 'Archive provenance missing')
        require(r['game_ids'] is None and r['rights_status'] == 'RESEARCH_METADATA_NOT_RELEASE_APPROVED',
                'Original IDs or production rights invented')
        require(r['verification_status'] == 'SOURCE_DESCRIPTION_NOT_RUNTIME', 'Archive status promoted')
        require(r['collection'] == ('npcs' if r['source_key'] in ('npc', 'assistant') else 'quests'),
                'Wrong archive collection')
        require(r['source_refs'] in (['S1'], ['S2']), 'Source attribution missing/mixed')
        branch = 'compiler' if r['source_refs'] == ['S1'] else 'dated_2003'
        require(r['source_relation'] == report['extraction'][branch][r['source_key']], 'Archive detached from extraction')
        require(r['version_profile'] == report['profiles'][branch]['id'], 'Cross-version record identity')
    for p in report['parent_pins']:
        b = (ROOT / p['path']).read_bytes()
        require(len(b) == p['bytes'] and digest(b) == p['sha256'], 'Parent evidence changed')
        require(hashlib.sha1(b'blob ' + str(len(b)).encode() + bytes([0]) + b).hexdigest() == p['git_blob'],
                'Parent Git identity changed')


def check_custody(root=ROOT):
    receipt_path = root / f'research/recovered/{PREFIX}-CUSTODY-R1.json'
    require(receipt_path.is_file(), 'Permanent custody receipt missing')
    receipt = json.loads(receipt_path.read_text())
    require(receipt['original_game_runtime_verified'] is False, 'Custody promoted to original runtime')
    required = {f'research/recovered/{PREFIX}-{suffix}-R1.json'
                for suffix in ('SOURCE', 'CI-CANDIDATE', 'CI-MAIN')}
    require(required <= {p['path'] for p in receipt['permanent_pins']}, 'Incomplete permanent evidence set')
    for p in receipt['permanent_pins']:
        path = root / p['path']
        require(path.is_file(), 'Permanent derived evidence missing')
        b = path.read_bytes()
        require(len(b) == p['bytes'] and digest(b) == p['sha256'], 'Permanent evidence bytes changed')
        require(hashlib.sha1(b'blob ' + str(len(b)).encode() + bytes([0]) + b).hexdigest() == p['git_blob'],
                'Permanent evidence Git identity changed')
    source = json.loads((root / f'research/recovered/{PREFIX}-SOURCE-R1.json').read_text())
    for suffix in ('CANDIDATE', 'MAIN'):
        raw = json.loads((root / f'research/recovered/{PREFIX}-CI-{suffix}-R1.json').read_text())
        require(raw['extraction'] == source['extraction'], 'Archived CI semantic replay differs')
        require(raw['audit']['real_input_mutations_rejected'] == 12 and
                raw['audit']['original_game_runtime_verified'] is False, 'Archived source audit boundary changed')
    return receipt


def main():
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--fetch', action='store_true')
    group.add_argument('--inputs', nargs=3)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    raws, inputs = [], []
    for i, url in enumerate(URLS):
        if args.fetch:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'StoneAge-research/1.0'}), timeout=45) as r:
                require(r.status == 200 and r.url == url, 'Unexpected HTTP identity')
                b = r.read(2_000_001)
        else:
            b = Path(args.inputs[i]).read_bytes()
        require(len(b) <= 2_000_000, 'Source response exceeds limit')
        raws.append(b)
        inputs.append({'source_id': ['I1', 'S1', 'S2'][i], 'url': url, 'bytes': len(b), 'sha256': digest(b)})
    actual = extract(raws)
    report = json.loads(REPORT.read_text())
    check_archive(report)
    check_custody()
    require(actual == report['extraction'], 'Source replay differs from qualified extraction')
    out = {'schema': 'stoneage.dinosaur_quest.replay.r1', 'inputs': inputs,
           'extraction': actual, 'audit': audit(raws, actual),
           'scope': 'CURRENT_HTML_REPLAY_NOT_HISTORICAL_BYTES_OR_GAME_EXECUTION'}
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'inputs': inputs, 'audit': out['audit']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
