"""Later operator report qualifies a four-manor snapshot, not server execution."""
import argparse
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from tools.stoneage_cn2011_stall_source import jpeg_dimensions

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-CN2003-GROUP2-MANOR-REPORT'
REPORT = ROOT / ('research/recovered/' + STEM + '-SOURCE-R1.json')
URL = 'https://games.sina.com.cn/newgames/2003/11/11208618.shtml'
PRIOR = 'research/recovered/STONEAGE-CN2003-CLASSIC20-BRANCH-SOURCE-R1.json'
PRIOR_LINK = 'http://games.sina.com.cn/newgames/2003/11/11188486.shtml'
BEGIN, END = '<!-- 内容 begin -->', '<!-- 内容 end -->'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Visible(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.images, self.links, self.block = [], [], [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style', 'iframe', 'noscript'):
            self.block += 1
        if not self.block and tag == 'img':
            self.images.append(a.get('src'))
        if not self.block and tag == 'a':
            self.links.append(a.get('href'))

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'iframe', 'noscript') and self.block:
            self.block -= 1

    def handle_data(self, data):
        if not self.block:
            self.parts.append(data)


def section(raw):
    text = raw.decode('gb18030', errors='strict')
    require('2003-11-20 16:43' in text, 'Publication timestamp missing')
    require(text.count(BEGIN) == text.count(END) == 1, 'Ambiguous article boundaries')
    p = Visible()
    p.feed(text.split(BEGIN, 1)[1].split(END, 1)[0])
    core = re.sub(r'\s+', '', ''.join(p.parts))
    require(core.startswith('以下是来自华义的最新官方消息：'), 'Operator attribution missing')
    all_page = Visible()
    all_page.feed(text)
    require(all_page.links.count(PRIOR_LINK) == 1, 'Editorial related link does not identify prior notice')
    require(len(p.images) == 1, 'Bounded activity-image reference changed')
    return core, p.images[0]


def extract(raw):
    t, picture = section(raw)
    opening = re.search(r'自(\d+月\d+日)(中午)(石器时代2\.0\(\d+\))新服务器组开机以来', t)
    manor = re.search(r'；(.+?)村的四大庄园分别为(.+?)四大家族占领，四家族的人数超过(\d+)，声望分别达到([\d，]+)！', t)
    online = re.search(r'平均同时在线人数达到(\d+)人以上', t)
    families = re.search(r'到现在为止的(\d+)小时内，服务器组内已经建立家族超过(\d+)个', t)
    require(opening and manor and online and families, 'Opening, list, population or scope statement changed')
    villages, owners = manor[1].split('，'), manor[2].split('，')
    reputations = [int(x) for x in manor[4].split('，')]
    require(len(villages) == len(owners) == len(reputations) == 4, 'Four ordered lists required')
    require('四大家族专属骑宠更是家族地位的象征' in t, 'Riding social claim changed')
    require('庄园挑战赛，家族PK赛也将同时拉开' in t, 'Future challenge/PK clause changed')
    require('11月20日早晨曾一度出现服务器繁忙状态' in t, 'Busy-period statement changed')
    require('北京华义对该服务器组进行了临时调整，重新保持了服务器的正常运行' in t, 'Operator recovery claim changed')
    return {
        'core_sha256': sha(t.encode()),
        'server_group_label': opening[3], 'label_is_authenticated_client_build': False,
        'opening_report': {'month_day_as_written': opening[1], 'period_as_written': opening[2],
                           'exact_time': None, 'body_year': None, 'timezone': None, 'authority': 'OPERATOR_RETROSPECTIVE_REPORT_NOT_EXECUTION_TRACE'},
        'manor_snapshot': [{'village_label': v, 'occupying_family_label': f, 'reputation_reported': n} for v, f, n in zip(villages, owners, reputations)],
        'population_report': {'average_concurrent_threshold_as_written': int(online[1]), 'concurrent_qualifier': '人以上',
                              'window_hours_as_written': int(families[1]), 'exact_window_start_end': None,
                              'families_established_strictly_more_than': int(families[2]),
                              'four_family_headcount_threshold_as_written': int(manor[3]), 'headcount_qualifier': '超过',
                              'headcount_scope': 'UNRESOLVED_PER_FAMILY_VS_AGGREGATE', 'per_family_counts': None, 'audited_statistics': False},
        'family_riding': {'source_role': 'EXCLUSIVE_RIDING_AS_STATUS_SYMBOL', 'mount_names_ids_or_eligibility_rules': None},
        'events': {'labels': ['庄园挑战赛', '家族PK赛'], 'status_in_notice': 'FUTURE_TENSE_NOT_COMPLETED_TOURNAMENT', 'schedule_rules_or_results': None},
        'operations_report': {'busy_month_day_as_written': '11月20日', 'busy_period': '早晨',
                              'operator_claim': 'TEMPORARY_ADJUSTMENT_RESTORED_NORMAL_OPERATION', 'independent_uptime_or_compensation': None},
        'activity_image_link_as_written': picture, 'editorial_related_prior_notice_link': PRIOR_LINK,
        'opening_occupancy_or_statistics_independently_witnessed': False,
        'reputations_are_eligibility_thresholds': False, 'current_manor_owners_in_2026_proven': False}


def comparison(pin, x):
    b = (ROOT / PRIOR).read_bytes()
    require(pin['path'] == PRIOR and len(b) == pin['bytes'] and sha(b) == pin['sha256'], 'Prior source pin changed')
    require(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == pin['git_blob'], 'Prior Git blob changed')
    old = json.loads(b)['extracted']
    require(old['family']['remaining_manor_names'] is None, 'Prior unwritten names were retroactively filled')
    require(old['new_server_group_label'] == x['server_group_label'], 'Different literal server-group label')
    later = [row['village_label'] for row in x['manor_snapshot']]
    return {'prior_announced_maintenance_start': old['announced_maintenance_start_time'],
            'prior_opening_relation': old['announced_opening_relation'], 'later_reported_opening_period': x['opening_report']['period_as_written'],
            'newly_named_villages_in_later_source': [v for v in later if v not in old['family']['named_manors']],
            'relation': 'PREANNOUNCEMENT_TO_LATER_OPERATOR_REPORT_SAME_LITERAL_GROUP_LABEL',
            'prior_article_itself_now_contains_all_names': False, 'proves_exact_noon_clock_time_or_binary_build': False,
            'manor_reputations_prove_entry_requirements': False, 'nine_to_four_manor_patch_or_rules_transfer_proven': False,
            'prior_billing_execution_now_verified': False}


def inspect_image(r, b):
    pin = r['image']
    width, height = jpeg_dimensions(b)
    require((len(b), sha(b), width, height) == (pin['bytes'], pin['sha256'], pin['width'], pin['height']), 'Activity JPEG changed')
    return {k: pin[k] for k in ('url_as_written', 'requested_url', 'bytes', 'sha256', 'width', 'height')}


def validate(r):
    require(r['schema'] == 'stoneage.cn2003_group2_manor_report.source_contract.r1', 'Schema')
    require(r['source']['url'] == URL and r['source']['authority'] == 'WAYI_OFFICIAL_MESSAGE_REPUBLISHED_BY_SINA', 'Authority')
    require(r['source']['authenticated_2003_original_bytes'] is False, 'Current page promoted to historical bytes')
    local = json.loads((ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_text())
    require(r['extracted'] == local['extracted'] and r['visual_observation'] == local['visual_observation'], 'Semantics/unknown/visual boundary changed')
    require(r['comparison'] == comparison(r['prior_input'], r['extracted']), 'Prior/later source relation changed')
    require(r['image']['url_as_written'] == r['extracted']['activity_image_link_as_written'], 'Image is not actually linked')
    require(r['image']['requested_url'] == r['image']['url_as_written'].replace('http://', 'https://'), 'Undeclared image URL rewrite')
    require(r['image']['capture_date'] is None and r['image']['native_client_resolution_proven'] is False, 'Image capture/build promotion')
    expected_evidence = [r['extracted']['opening_report'], *r['extracted']['manor_snapshot'],
                         {'population': r['extracted']['population_report'], 'operations': r['extracted']['operations_report']},
                         {'riding': r['extracted']['family_riding'], 'events': r['extracted']['events']}, r['visual_observation']]
    require([row['evidence'] for row in r['records']] == expected_evidence, 'Record order or source evidence changed')
    require(r['source']['published'] == '2003-11-20 16:43' and r['source']['encoding'] == 'GB18030_STRICT', 'Publication/encoding')
    require(r['source']['current_observed_bytes'] == local['http_bytes'] and r['source']['current_observed_sha256'] == local['http_sha256'], 'Current HTML pin')
    require(len(r['records']) == 8 and len({x['record_id'] for x in r['records']}) == 8, 'Bounded records')
    for row in r['records']:
        require(row['version_profile'] == 'LATER_OFFICIAL:CN_WAYI_2003_CLASSIC20_SERVER_BRANCH' and row['game_ids'] is None, 'Version or game IDs invented')
        require(row['record_revision'] == 1 and row['rights_status'] == 'DERIVED_RESEARCH_METADATA_PRODUCTION_ASSET_RIGHTS_UNKNOWN', 'Record/rights boundary')
    require(all(v is False for v in r['unproven'].values()), 'Unproven claim promoted')
    require(r['status'] == {'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'}, 'Stage')
    require(r['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-48', 'Queue')


MUTATIONS = (
    ('noon-period', '11月19日中午', '11月19日下午'),
    ('server-group', '石器时代2.0(2)新服务器组', '石器时代2.0(3)新服务器组'),
    ('online-threshold', '达到2000人以上', '达到3000人以上'),
    ('online-qualifier', '2000人以上', '2000人以下'),
    ('reported-window', '24小时内', '48小时内'),
    ('family-count', '家族超过200个', '家族超过300个'),
    ('literal-village-name', '玛丽娜丝', '玛丽娜斯'),
    ('literal-fourth-village', '卡鲁它那村', '卡鲁他那村'),
    ('family-name', '永远友情', '永恒友情'),
    ('ordered-occupants', '圣战部落光，永远友情', '永远友情，圣战部落光'),
    ('reputation', '4524，2280', '4525，2280'),
    ('headcount-scope', '四家族的人数超过90', '每家族的人数超过90'),
    ('busy-period', '11月20日早晨', '11月20日中午'),
    ('recovery-not-benchmark', '重新保持了服务器的正常运行', '未能恢复服务器的正常运行'),
    ('future-events', '也将同时拉开', '已经全部完成'),
    ('actual-related-link', 'http://games.sina.com.cn/newgames/2003/11/11188486.shtml', 'http://games.sina.com.cn/newgames/2003/11/11180000.shtml'),
    ('actual-image-link', '655_20031120164335.jpg', '655_20031120164336.jpg'),
    ('riding-social-role', '四大家族专属骑宠', '四大家族通用骑宠'),
)


def audit(raw, expected):
    text = raw.decode('gb18030')
    checks = []
    for label, old, new in MUTATIONS:
        require(text.count(old) == 1, 'Nonunique source mutation: ' + label)
        modified = text.replace(old, new, 1).encode('gb18030')
        try:
            x = extract(modified)
            x.pop('core_sha256')
            target = dict(expected)
            target.pop('core_sha256')
            rejected = x != target
        except ValueError:
            rejected = True
        require(rejected, 'Semantic source change accepted: ' + label)
        checks.append({'case': label, 'input_sha256': sha(modified), 'rejected_without_digest_gate': True})
    require(extract(raw + b'<script>outer change</script>') == expected, 'Outer-only positive changed source')
    return {'real_source_mutations': checks, 'outer_script_positive': True}


def replay(r, raw, picture):
    validate(r)
    x = extract(raw)
    require(x == r['extracted'], 'Source core or semantics changed')
    return {'schema': 'stoneage.cn2003_group2_manor_report.derived_replay.r1', 'http_bytes': len(raw), 'http_sha256': sha(raw),
            'extracted': x, 'comparison': comparison(r['prior_input'], x), 'image': inspect_image(r, picture),
            'visual_observation': r['visual_observation'], 'audit': audit(raw, x),
            'raw_html_or_assets_in_output': False, 'historical_server_executed': False}


def fetch(url, limit):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
        require(response.status == 200, 'HTTP failed')
        b = response.read(limit + 1)
        require(len(b) <= limit, 'Response oversized')
        return b


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--fetch', action='store_true')
    g.add_argument('--html', type=Path)
    p.add_argument('--image', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    r = json.loads(REPORT.read_text())
    if a.fetch:
        raw, picture = fetch(URL, 1000000), fetch(r['image']['requested_url'], 2000000)
    else:
        if a.image is None:
            p.error('--image is required with --html')
        raw, picture = a.html.read_bytes(), a.image.read_bytes()
    out = replay(r, raw, picture)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'success': True, 'http_bytes': len(raw), 'image_bytes': len(picture), 'ordered_manors': len(out['extracted']['manor_snapshot']), 'semantic_mutations': len(out['audit']['real_source_mutations'])}))


if __name__ == '__main__':
    main()
