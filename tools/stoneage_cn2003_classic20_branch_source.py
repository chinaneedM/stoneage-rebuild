"""A dated official server-branch notice is not a recovered early client build."""
import argparse
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-CN2003-CLASSIC20-BRANCH-SOURCE-R1.json'
URL = 'https://games.sina.com.cn/newgames/2003/11/11188486.shtml'
COMPARISON = 'research/recovered/STONEAGE-CN40-RIDING-CERTIFICATE-MANOR-SOURCE-R1.json'
BEGIN, END = '<!-- 内容 begin -->', '<!-- 内容 end -->'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Visible(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.links, self.block = [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'iframe', 'noscript'):
            self.block += 1
        if tag == 'a' and not self.block:
            self.links.append(dict(attrs).get('href'))

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'iframe', 'noscript') and self.block:
            self.block -= 1

    def handle_data(self, data):
        if not self.block:
            self.parts.append(data)


def section(raw):
    text = raw.decode('gb18030', errors='strict')
    require('2003-11-18 15:33' in text, 'Publication timestamp missing')
    require(text.count(BEGIN) == text.count(END) == 1, 'Article boundaries ambiguous')
    body = text.split(BEGIN, 1)[1].split(END, 1)[0]
    p = Visible()
    p.feed(body)
    core = re.sub(r'\s+', '', ''.join(p.parts))
    require(core.startswith('以下是来自华义的最新官方消息：'), 'Official issuer attribution missing')
    return core, p.links


def extract(raw):
    t, links = section(raw)
    clauses = ('石器时代2.0版本', '划时代的骑宠系统', '更安全的交易系统',
               '新系统加快了游戏的速度', '新添了加美航空，各大村庄的羽毛', '更多更新的宠物和道具',
               '萨姆吉尔、加加……四大庄园', '家族频道、家族管理制度、家族战争',
               '自9月4日北京华义开放2.0服务器组以来',
               '11月19日上午9点停机维护后增开石器时代2.0(2)服务器组',
               '原石器时代2.0服务器组将更名为石器时代2.0(1)',
               '石器时代2.0服务器(2)开放后将开始收费', '关于WGS系统的详细收费方式')
    require(all(c in t for c in clauses), 'Material branch/capability/schedule/billing claim changed')
    fee = 'http://www.wayi.com.cn/pop/server.asp'
    require(links.count(fee) == 1, 'Actual billing reference link missing/ambiguous')
    return {
        'core_sha256': sha(t.encode()),
        'issuer': '华义', 'operator_named': '北京华义',
        'branch_label': '石器时代2.0', 'label_kind': '2003_OPERATOR_SERVER_BRANCH_NOT_CLIENT_BINARY_BUILD',
        'earlier_opening_month_day_as_written': '9月4日', 'earlier_launch_year_in_body': None,
        'announced_maintenance_month_day': '11月19日', 'announced_maintenance_start_time': '09:00',
        'announced_opening_relation': 'AFTER_MAINTENANCE_NOT_PROVEN_EXACT_09_OPEN', 'time_zone': None,
        'new_server_group_label': '石器时代2.0(2)', 'existing_group_renamed_to': '石器时代2.0(1)',
        'billing': {'announced_scope': 'NEW_GROUP_2_AFTER_OPENING', 'policy_system_name': 'WGS',
                    'policy_link_as_written': fee, 'linked_policy_retrieved': False,
                    'price_or_unit': None, 'existing_group_1_billing_rule': None},
        'capabilities': ['RIDING_ADVERTISED', 'SAFER_TRADE_CLAIM', 'FASTER_GAME_CLAIM',
                         'JIAMEI_AIRLINE_AND_VILLAGE_FEATHERS', 'MORE_PETS_AND_ITEMS_NOT_A_ROSTER'],
        'family': {'manor_total_reported': 4, 'named_manors': ['萨姆吉尔', '加加'],
                   'remaining_manor_names': None, 'functions_reported': ['家族频道', '家族管理制度', '家族战争']},
        'actual_server_opening_or_billing_witnessed': False,
        'client_binary_build_authenticated': False, 'security_or_performance_benchmarked': False}


def comparison(pin):
    b = (ROOT / COMPARISON).read_bytes()
    require(pin['path'] == COMPARISON and pin['bytes'] == len(b) and pin['sha256'] == sha(b), 'Comparison source changed')
    require(pin['git_blob'] == hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), 'Comparison Git blob changed')
    rows = [x['source_row'] for x in json.loads(b)['records'] if 'source_row' in x]
    require(len(rows) == 9, 'Expected nine-row CN4.0 source table')
    require({'萨姆吉尔', '加加'} <= {x['manor'] for x in rows}, 'Literal comparison names changed')
    return {'new_notice_reported_count': 4, 'cn40_table_row_count': 9,
            'relation': 'DISTINCT_SOURCE_CONTEXTS_NOT_A_PROVEN_PATCH_DIFF',
            'fills_unwritten_two_names': False, 'proves_five_manors_removed': False,
            'proves_same_server_or_client_build': False, 'transfers_riding_rules': False}


def validate(r):
    require(r['schema'] == 'stoneage.cn2003_classic20_branch.source_contract.r1', 'Schema')
    require(r['source']['url'] == URL and r['source']['current_bytes_are_authenticated_2003_original'] is False, 'Historical/current source boundary')
    require(r['source']['authority'] == 'CONTEMPORANEOUS_WAYI_OFFICIAL_MESSAGE_REPUBLISHED_BY_SINA', 'Source attribution changed')
    x = r['extracted']
    require(x['branch_label'] == '石器时代2.0' and (x['new_server_group_label'], x['existing_group_renamed_to']) == ('石器时代2.0(2)', '石器时代2.0(1)'), 'Server labels renamed')
    require(x['label_kind'] == '2003_OPERATOR_SERVER_BRANCH_NOT_CLIENT_BINARY_BUILD', 'Label promoted to binary build')
    require(x['announced_opening_relation'] == 'AFTER_MAINTENANCE_NOT_PROVEN_EXACT_09_OPEN', 'Maintenance start promoted to opening time')
    require(x['earlier_launch_year_in_body'] is None and x['time_zone'] is None, 'Unwritten year/timezone invented')
    require(x['billing']['announced_scope'] == 'NEW_GROUP_2_AFTER_OPENING', 'Billing scope expanded')
    require(x['billing']['price_or_unit'] is None and x['billing']['existing_group_1_billing_rule'] is None, 'Unseen policy or old-group fee invented')
    require(x['billing']['linked_policy_retrieved'] is False, 'Unfetched policy promoted')
    require(x['family']['manor_total_reported'] == 4 and x['family']['named_manors'] == ['萨姆吉尔', '加加'] and x['family']['remaining_manor_names'] is None, 'Partial names/count changed')
    require(x['client_binary_build_authenticated'] is False and x['security_or_performance_benchmarked'] is False and x['actual_server_opening_or_billing_witnessed'] is False, 'Promotional or scheduled claim promoted to runtime')
    require(r['comparison'] == comparison(r['comparison_input']), 'Cross-version rules transferred')
    require(len(r['records']) == 6, 'Bounded record count')
    for row in r['records']:
        require(row['version_profile'] == 'LATER_OFFICIAL:CN_WAYI_2003_CLASSIC20_SERVER_BRANCH' and row['game_ids'] is None, 'Original build or game ID invented')
    require(all(v is False for v in r['unproven'].values()), 'Unproven claim promoted')
    require(r['status'] == {'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'}, 'Stage changed')
    require(r['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-44', 'Portfolio queue')


MUTATIONS = (
    ('reported-earlier-month-day', '自9月4日北京华义', '自9月5日北京华义'),
    ('maintenance-month-day', '11月19日上午9点', '11月20日上午9点'),
    ('maintenance-start-hour', '11月19日上午9点', '11月19日上午10点'),
    ('after-not-before-maintenance', '停机维护后增开', '停机维护前增开'),
    ('new-group-label', '增开石器时代2.0(2)', '增开石器时代2.0(3)'),
    ('rename-existing-group', '更名为石器时代2.0(1)', '更名为石器时代2.0(9)'),
    ('billing-scope', '2.0服务器(2)开放后将开始收费', '2.0服务器(1)开放后将开始收费'),
    ('manor-count', '四大庄园', '九大庄园'),
    ('named-manor', '萨姆吉尔、加加', '萨姆吉尔、伊甸'),
    ('family-channel', '家族频道、家族管理制度', '家族私聊、家族管理制度'),
    ('airline-name', '新添了加美航空', '新添了其他航空'),
    ('security-claim-not-guarantee', '更安全的交易系统', '绝对安全的交易系统'),
    ('fee-link', 'http://www.wayi.com.cn/pop/server.asp', 'http://www.wayi.com.cn/pop/unknown.asp'),
)


def audit(r, raw):
    text = raw.decode('gb18030')
    head, tail = text.split(BEGIN, 1)
    body, suffix = tail.split(END, 1)
    checks = []
    for label, old, new in MUTATIONS:
        require(body.count(old) == 1, 'Nonunique body mutation: ' + label)
        modified = (head + BEGIN + body.replace(old, new, 1) + END + suffix).encode('gb18030')
        try:
            x = extract(modified)
            rejected = {k: v for k, v in x.items() if k != 'core_sha256'} != {k: v for k, v in r['extracted'].items() if k != 'core_sha256'}
        except ValueError:
            rejected = True
        require(rejected, 'Semantic mutation accepted: ' + label)
        checks.append({'case': label, 'input_sha256': sha(modified), 'rejected_without_digest_gate': True})
    positive = raw + b'<script>outer layout change</script>'
    require(extract(positive) == r['extracted'], 'Outer-only positive changed core')
    return {'real_body_mutations': checks, 'outer_script_positive': True}


def replay(r, raw):
    validate(r)
    require(extract(raw) == r['extracted'], 'Source core/semantics changed')
    return {'schema': 'stoneage.cn2003_classic20_branch.derived_replay.r1', 'http_bytes': len(raw), 'http_sha256': sha(raw),
            'extracted': extract(raw), 'comparison': comparison(r['comparison_input']), 'audit': audit(r, raw),
            'raw_html_or_assets_in_output': False, 'historical_server_or_client_executed': False}


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--fetch', action='store_true')
    g.add_argument('--html', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if a.fetch:
        with urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
            require(response.status == 200, 'HTTP failed')
            raw = response.read(1000001)
            require(len(raw) <= 1000000, 'Source oversized')
    else:
        raw = a.html.read_bytes()
    result = replay(json.loads(REPORT.read_text()), raw)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'success': True, 'http_bytes': len(raw), 'semantic_mutations': len(result['audit']['real_body_mutations'])}))


if __name__ == '__main__':
    main()
