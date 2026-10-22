"""Three finite player documents; speaker-scoped tool claims, never game rules."""
import argparse
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-STA253-SPEAKER'
REPORT = ROOT / f'research/recovered/{STEM}-SOURCE-R1.json'
URLS = (
    'https://news.17173.com/z/stoneage/content/2002-3-27/n352_268196.html?_platform=PC',
    'https://news.17173.com/z/stoneage/content/2002-3-21/n936_852654.html?_platform=PC',
    'https://news.17173.com/z/stoneage/content/2002-3-21/n372_288246.html',
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class Fields(HTMLParser):
    """Read visible text inside unique article fields, excluding site chrome."""
    IDS = ('newsbiaoti', 'newsriqi', 'zhuozhe_left', 'news')

    def __init__(self):
        super().__init__()
        self.depth = 0
        self.hidden = 0
        self.active = None
        self.fields = {}

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'iframe', 'noscript'):
            self.hidden += 1
        if tag == 'div':
            self.depth += 1
            ident = dict(attrs).get('id')
            if ident in self.IDS and not self.hidden:
                require(ident not in self.fields and self.active is None, 'Duplicate/nested article field')
                self.fields[ident] = []
                self.active = (ident, self.depth)

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.active and self.depth == self.active[1]:
                self.active = None
            self.depth -= 1
        if tag in ('script', 'style', 'iframe', 'noscript') and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if self.active and not self.hidden:
            self.fields[self.active[0]].append(data)


def article(raw):
    text = raw.decode('utf-8', errors='strict')
    require(re.search(r'charset=["\x27]?utf-8', text, re.I), 'Changed source charset')
    p = Fields()
    p.feed(text)
    require(p.active is None and set(p.fields) == set(p.IDS), 'Incomplete article fields')
    fields = {k: re.sub(r'\s+', '', ''.join(v)) for k, v in p.fields.items()}
    require(fields['news'].count('本文言论') == 1, 'Article end disclaimer missing/duplicated')
    fields['news'] = fields['news'].split('本文言论')[0]
    return fields


def partition(body):
    boundary = '附录暗夜之狼的原文'
    require(body.count(boundary) == 1, 'Appendix speaker boundary missing/duplicated')
    outer, appendix = body.split(boundary)
    pattern = r'引用([1-4])[:：]?“(.*?)”'
    matches = list(re.finditer(pattern, appendix))
    require([m[1] for m in matches] == list('1234'), 'Four ordered quotations required')
    replies, quoted = [], []
    for i, match in enumerate(matches):
        quoted.append(match[2])
        stop = matches[i + 1].start() if i < 3 else len(appendix)
        replies.append(appendix[match.end():stop])
    return outer, appendix[:matches[0].start()], quoted, replies


def derive(raws):
    a, b, c = [article(raw) for raw in raws]
    require(a['zhuozhe_left'] == '作者：ZHY' and '2002-03-27' in a['newsriqi'], 'Outer attribution changed')
    require(b['zhuozhe_left'] == '作者：地藏乌拉' and '2002-03-21' in b['newsriqi'], 'Earlier attribution changed')
    require(c['zhuozhe_left'] == '作者：加林多斯' and '2002-03-21' in c['newsriqi'], 'Beta attribution changed')
    outer, intro, quotes, replies = partition(a['news'])
    require('2.53' not in outer and 'sta2.53' in intro.lower(), 'Version leaked across speaker boundary')
    require('sta2.53' in a['newsbiaoti'].lower(), 'Named page title changed')
    starts = ['STA与SACH', '练功方面', '脚本方面', '现在混家族', '总体来讲']
    positions = [b['news'].index(s) for s in starts]
    require(positions == sorted(set(positions)), 'Earlier comparison sections changed')
    earlier = [b['news'][positions[i]:positions[i + 1]] for i in range(4)]
    require(quotes == earlier, 'Embedded quotes differ from separately retrieved earlier article')
    require(re.search(r'没有.{0,5}详细', outer) and re.search(r'没有.{0,5}详细', quotes[0]), 'Absent-info claim changed')
    require(re.search(r'Sta是有.{0,8}详细', replies[0]), 'Reply detail claim changed')
    require('快速战斗' in outer and '2.53的快速战斗' in replies[1], 'Fast-battle version context changed')
    require('自动料理' in outer and re.search(r'2.53.{0,8}编辑料理脚本', replies[3]), 'Editable cooking claim changed')
    require('原地遇敌' in replies[3], 'Stationary-encounter reply claim changed')
    beta = c['news']
    require('STA2.53bate7' in beta and 'beta7' in beta and 'WIN2000' in beta, 'Exact beta labels/environment changed')
    require(re.search(r'料理.{0,4}没试用', beta), 'Untested cooking became an availability claim')
    require(re.search(r'设置为(100)', beta) and '等待' in beta, 'Delay observation changed')
    require(all(t in beta for t in ('切换', '信件', '战斗消息', '响应慢', '关掉', '不知道是否')), 'Uncertain stability report changed')
    return {
        'schema': 'stoneage.sta253_speaker.extraction.r1',
        'speaker_sections': {'outer_version': None, 'appendix_version_context': 'Sta2.53',
                             'quote_versions': [None] * 4, 'beta_labels_as_written': ['STA2.53bate7', 'beta7']},
        'quote_crosscheck': {'exact_normalized_matches': [1, 2, 3, 4],
                            'sha256': [digest(q.encode()) for q in quotes],
                            'independent_sources_created_by_requoting': 0},
        'claims': [
            {'feature': 'OPPONENT_DETAIL', 'speaker': 'ZHY', 'tool_version': None, 'status': 'REPORTED_ABSENT'},
            {'feature': 'OPPONENT_DETAIL', 'speaker': '暗夜之狼', 'tool_version': '2.53', 'status': 'REPORTED_PRESENT'},
            {'feature': 'FAST_BATTLE', 'speaker': 'ZHY', 'tool_version': None, 'status': 'PRESENT_SPEED_DISPUTED'},
            {'feature': 'FAST_BATTLE', 'speaker': '暗夜之狼', 'tool_version': '2.53', 'status': 'PRESENT_SPEED_DISPUTED'},
            {'feature': 'AUTO_COOKING', 'speaker': 'ZHY', 'tool_version': None, 'status': 'BOTH_FAMILIES_REPORTED_PRESENT'},
            {'feature': 'EDITABLE_COOKING_SCRIPT', 'speaker': '暗夜之狼', 'tool_version': '2.53', 'status': 'REPORTED_PRESENT'},
            {'feature': 'STATIONARY_ENCOUNTER', 'speaker': '暗夜之狼', 'tool_version': '2.53', 'status': 'REPORTED_PRESENT'},
        ],
        'beta_observations': {'speaker': '加林多斯', 'environment_as_written': 'WIN2000',
                              'setting_as_written': '100', 'setting_unit': None,
                              'post_enemy_death_wait_reported': True,
                              'message_switch_slowness_or_exit_reported': True,
                              'cause_identified': False, 'cooking_tested': False,
                              'trial_duration_independently_verified': False,
                              'same_binary_as_unqualified_253_proven': False},
        'section_digests': {'outer': digest(outer.encode()), 'appendix_intro': digest(intro.encode()),
                            'replies': [digest(x.encode()) for x in replies], 'beta': digest(beta.encode())},
        'historical_bytes_authenticated': False, 'software_executed': False,
        'performance_benchmark_verified': False, 'conflict_resolved': False,
    }


def verify_report(report):
    require(report['scope'] == {'official_game_rules': False, 'developer_changelog': False,
                                'all_tool_features_complete': False, 'adoption_decided': False,
                                'new_game_production_started': False}, 'Scope promoted')
    for pin in report['parent_pins']:
        raw = (ROOT / pin['path']).read_bytes()
        require(len(raw) == pin['bytes'] and digest(raw) == pin['sha256'], 'Parent bytes changed')
        require(hashlib.sha1(b'blob ' + str(len(raw)).encode() + bytes([0]) + raw).hexdigest() == pin['git_blob'],
                'Parent Git identity changed')


MUTATIONS = (
    (0, '附录', '附注'), (0, 'STA还是没有', 'STA仍然含有'),
    (0, 'Sta是有', 'Sta没有'), (0, '2.53的快速战斗', '2.52的快速战斗'),
    (0, '编辑料理脚本', '删除料理脚本'), (0, '原地遇敌', '禁止遇敌'),
    (1, '作者：地藏乌拉', '作者：其他'), (1, '没有详细资料', '具有详细资料'),
    (2, 'STA2.53bate7', 'STA2.53bate8'), (2, '没试用', '已试用'),
    (2, '设置为100', '设置为200'), (2, 'WIN2000', 'WIN98'),
    (2, '不知道是否', '已经确认'), (2, '等待', '立刻'),
)


def audit(raws, expected):
    semantic = lambda d: {k: v for k, v in d.items() if k not in ('section_digests', 'quote_crosscheck')}
    for index, old, new in MUTATIONS:
        text = raws[index].decode('utf-8')
        require(old in text, 'Unexercised real-source counterexample')
        changed = list(raws)
        changed[index] = text.replace(old, new).encode()
        try:
            actual = derive(changed)
        except ValueError:
            continue
        require(semantic(actual) != semantic(expected), 'Semantic mutation passed without digest gate')
    for index in range(3):
        changed = list(raws)
        changed[index] += b'<script>site_chrome_only=1;</script>'
        require(derive(changed) == expected, 'Peripheral script changed selected evidence')
    return {'real_source_mutations_rejected_without_digest_gate': len(MUTATIONS),
            'three_peripheral_script_positives': True, 'original_game_runtime_verified': False}


def main():
    p = argparse.ArgumentParser()
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--fetch', action='store_true')
    group.add_argument('--inputs', nargs=3)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    report = json.loads(REPORT.read_text())
    verify_report(report)
    raws, inputs = [], []
    for i, url in enumerate(URLS):
        if args.fetch:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'StoneAge-research/1.0'}), timeout=45) as r:
                require(r.status == 200 and r.url == url, 'Source HTTP identity changed')
                raw = r.read(2_000_001)
        else:
            raw = Path(args.inputs[i]).read_bytes()
        require(len(raw) <= 2_000_000, 'Source exceeds bound')
        raws.append(raw)
        inputs.append({'id': f'S{i + 1}', 'url': url, 'bytes': len(raw), 'sha256': digest(raw)})
    actual = derive(raws)
    require(actual == report['extraction'], 'Source semantics changed')
    out = {'schema': 'stoneage.sta253_speaker.replay.r1', 'inputs': inputs, 'extraction': actual,
           'audit': audit(raws, actual),
           'original_html_or_assets_in_output': False, 'original_game_runtime_verified': False}
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'inputs': inputs, 'quote_matches': actual['quote_crosscheck']['exact_normalized_matches']}))


if __name__ == '__main__':
    main()
