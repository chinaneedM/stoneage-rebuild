"""Qualify a hosted guide, paired GIF roles and a separately voiced rollout notice."""
import argparse
import hashlib
import json
import re
import struct
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from tools.stoneage_cn2003_group2_manor_report import Visible, fetch

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-CN2003-ONBOARDING'
REPORT = ROOT / ('research/recovered/' + STEM + '-SOURCE-R1.json')
URLS = {'guide': 'https://games.sina.com.cn/zhqu/sta/liucheng.shtml',
        'notice': 'https://games.sina.com.cn/newgames/2003/06/06092201.shtml'}
PROFILE = 'LATER_LINEAGE:CN_WAYI_60_HOSTED_GUIDE_BUILD_UNAUTHENTICATED'
PREFIX = 'http://image2.sina.com.cn/gm/zhuanqu/stoneage3/xslc/image'
IDS = ['032', '033', '035', '036', '038', '039', '041', '042', '044', '045']


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Paragraphs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active = False
        self.parts, self.images, self.rows = [], [], []

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.active, self.parts, self.images = True, [], []
        if self.active and tag == 'img':
            a = dict(attrs)
            self.images.append({k: a.get(k) for k in ('src', 'width', 'height')})

    def handle_endtag(self, tag):
        if tag == 'p' and self.active:
            self.rows.append({'text': re.sub(r'\s+', '', ''.join(self.parts)), 'images': self.images})
            self.active = False

    def handle_data(self, text):
        if self.active:
            self.parts.append(text)


def guide(raw):
    t = raw.decode('gb18030', errors='strict')
    require('<!-- include 发布时间 begin -->2003-05-30 14:14<!-- include 发布时间 end -->' in t, 'Guide displayed stamp changed')
    require('target=_blank>网友投稿</A>' in t, 'Guide submission marker changed')
    require('<title>6.0新手流程_' in t, 'Guide title changed')
    p = Paragraphs()
    p.feed(t)
    rows = p.rows
    start = [i for i, r in enumerate(rows) if r['text'].startswith('双击桌面“Deeplay”')]
    end = [i for i, r in enumerate(rows) if r['text'].startswith('玩家一开始会出现在新手村内')]
    require(len(start) == len(end) == 1 and start[0] < end[0], 'Selected entry/birth boundary changed')
    selected = rows[start[0]:end[0] + 1]
    texts = [r['text'] for r in selected if r['text']]
    images = [im for r in selected for im in r['images']]
    require(len(texts) == 8 and len(images) == 10, 'Finite paragraph/image scope changed')
    transport_start = [i for i, r in enumerate(rows) if r['text'] == '新手传送师：']
    require(len(transport_start) == 1, 'Transport paragraph ambiguous')
    transport = [r['text'] for r in rows[transport_start[0]:transport_start[0] + 4]]
    t = ''.join(texts)
    require('选择石器时代图标双击运行游戏' in texts[0], 'Launcher instruction changed')
    require('输入用户名、密码，点击OK进入游戏' in t, 'Login instruction changed')
    require('哦，这里插一下以后进入游戏直接看到这个画面' in t, 'Editorial returning-character insertion changed')
    roster = re.search(r'选择(\d+)种人物，并且每种人物都有(\d+)种颜色的头发和衣服搭配', t)
    name = re.search(r'最多(\d+)个字符的名字', t)
    allocation = re.search(r'初始的(\d+)点(经验值)分配', t)
    pets = re.search(r'自己选择出生宠了（([^）]+)）', t)
    require(roster and name and allocation and pets, 'Creation values or literal allocation wording changed')
    require('你的面部表情一样可以自己设定' in t and '建议加在速度和体力上' in t, 'Face edit or editorial recommendation changed')
    require('地、水、火、风丝属性相克' in t, 'Literal element wording changed')
    require('从一出生就会特殊技能' in t, 'Unspecified birth-skill description changed')
    require('到新手村外的草地上捕捉' in t, 'Additional starter capture description changed')
    require('就不能再进入' in texts[-1] and '就不能再进入' in transport[-1], 'One-way exit description changed')
    dest = re.search(r'会到达石器时代中的(.+?)村', transport[2])
    require(dest, 'Transport destination changed')
    return {
        'core_sha256': sha(json.dumps({'texts': texts, 'images': images, 'transport': transport}, ensure_ascii=False, separators=(',', ':')).encode()),
        'authority': 'SINA_HOSTED_GUIDE_WITH_USER_SUBMISSION_MARKER_NOT_AUTHENTICATED_WAYI_MANUAL',
        'displayed_publication': '2003-05-30 14:14',
        'displayed_credit': '新浪游戏', 'submission_link_proves_user_authorship': False,
        'entry': {'launcher_label': 'Deeplay', 'credential_fields_reported': ['用户名', '密码'], 'button_as_written': 'OK',
                  'returning_character_view_is_editorial_insertion': True, 'fully_executed_login_state_machine': False},
        'roster': {'character_types_as_reported': int(roster[1]), 'paired_hair_clothes_color_choices_as_reported': int(roster[2]),
                   'independent_hair_times_clothes_choices': None, 'original_character_ids': None},
        'creation': {'name_limit_value': int(name[1]), 'name_limit_unit_as_written': '字符', 'encoding_byte_limit_or_chinese_character_count': None,
                     'face_edit_reported': True, 'initial_allocation_value': int(allocation[1]), 'allocation_term_as_written': allocation[2],
                     'runtime_exp_or_stat_point_semantics': None, 'speed_vitality_advice_is_editorial_not_optimal_build': True,
                     'elements_as_reported': ['地', '水', '火', '风'], 'element_formula_or_budgets': None},
        'starter_pets': {'labels_as_written': pets[1].split('、'), 'initial_special_skill_claim': True,
                         'skills_ids_names_stats_or_first_release_proven': None, 'grass_capture_reported': True},
        'newcomer': {'arrival_as_reported': '新手村', 'exit_via': '新手传送师', 'destination_label_as_written': dest[1] + '村',
                     'reentry_disallowed_as_reported': True, 'actual_warp_id_coordinates_or_execution': None,
                     'wording_about_levels_not_treated_as_global_level_cap': True},
        'image_references_in_source_order': images,
        'historical_client_or_server_executed': False,
    }


def notice(raw):
    t = raw.decode('gb18030', errors='strict')
    require('2003年06月09日 12:15' in t, 'Notice stamp changed')
    begin, end = '<!-- 内容 begin -->', '<!-- 内容 end -->'
    require(t.count(begin) == t.count(end) == 1, 'Notice body ambiguous')
    t = t.split(begin)[1].split(end)[0]
    require(t.count('<!--画中画广告开始-->') == t.count('<!--画中画广告结束-->') == 1, 'Notice ad boundary changed')
    t = re.sub(r'<!--画中画广告开始-->.*?<!--画中画广告结束-->', '', t, flags=re.S)
    p = Visible()
    p.feed(t)
    core = re.sub(r'\s+', '', ''.join(p.parts))
    date = re.search(r'自(2003)年(6)月(10)日起。(中国网通9)服务器将率先升级到《海贼王遗迹》\(石器(6\.0)\)', core)
    require(date, 'Planned first-server rollout changed')
    require('及时更新客户端不然可是没办法登录服务器' in core and '所有服务器将陆续更新' in core, 'Client compatibility or phased rollout changed')
    require('我们特意为新手们准备了新手村' in core and '北京华义精心为您制作' in core, 'Operator-voiced context changed')
    require('http://www.waei.com.cn/zhuanqu/sa6/' in p.links, 'Actual first-party context link changed')
    return {'core_sha256': sha(core.encode()), 'authority': 'SINA_HOSTED_WAYI_VOICED_NOTICE_NOT_AUTHENTICATED_ISSUER_OR_RUNTIME',
            'displayed_publication': '2003-06-09 12:15', 'announced_first_date': '-'.join([date[1], date[2].zfill(2), date[3].zfill(2)]),
            'announced_first_group': date[4], 'version_label': date[5], 'other_groups_phased_without_dates': True,
            'client_update_required_as_reported': True, 'newcomer_village_announced': True,
            'official_context_link_as_written': 'http://www.waei.com.cn/zhuanqu/sa6/',
            'actual_rollout_or_all_groups_complete_proven': False, 'authenticates_guide_or_current_image_build': False,
            'guide_may30_date_proves_live_deployment': False}


def gif_structure(b):
    require(b[:6] in (b'GIF87a', b'GIF89a') and len(b) >= 14, 'Not GIF')
    width, height = struct.unpack('<HH', b[6:10])
    pos = 13 + (3 * 2 ** ((b[10] & 7) + 1) if b[10] & 128 else 0)
    frames, transparency = [], []
    def subblocks(i):
        while True:
            require(i < len(b), 'Truncated GIF block')
            n = b[i]
            i += 1
            if not n:
                return i
            require(i + n <= len(b), 'Truncated GIF subblock')
            i += n
    while pos < len(b):
        code = b[pos]
        pos += 1
        if code == 0x3b:
            require(pos == len(b), 'Unexpected GIF trailer payload')
            return {'width': width, 'height': height, 'frames': len(frames), 'frame_rectangles': frames,
                    'transparency_flags': transparency}
        if code == 0x21:
            require(pos < len(b), 'Missing extension label')
            label = b[pos]
            pos += 1
            if label == 0xf9:
                require(pos + 6 <= len(b) and b[pos] == 4, 'Malformed GCE')
                transparency.append(bool(b[pos + 1] & 1))
            pos = subblocks(pos)
        elif code == 0x2c:
            require(pos + 9 <= len(b), 'Truncated descriptor')
            frames.append(list(struct.unpack('<HHHH', b[pos:pos+8])))
            packed = b[pos+8]
            pos += 9
            if packed & 128:
                pos += 3 * 2 ** ((packed & 7) + 1)
            require(pos < len(b), 'Missing LZW size')
            pos = subblocks(pos + 1)
        else:
            raise ValueError('Invalid GIF block marker')
    raise ValueError('Missing GIF trailer')


MUTATIONS = [
    ('guide', 'submission-marker', 'target=_blank>网友投稿</A>', 'target=_blank>官方发布</A>'),
    ('guide', 'displayed-date', '2003-05-30 14:14', '2003-06-30 14:14'),
    ('guide', 'login-fields', '输入用户名、密码', '输入邮箱、密码'),
    ('guide', 'editorial-order', '这里插一下以后进入游戏', '这里证明必须重新进入游戏'),
    ('guide', 'roster-count', '选择12种人物', '选择16种人物'),
    ('guide', 'paired-colors', '每种人物都有4种颜色', '每种人物都有8种颜色'),
    ('guide', 'name-unit', '最多8个字符', '最多8个汉字'),
    ('guide', 'name-limit', '最多8个字符', '最多16个字符'),
    ('guide', 'initial-value', '初始的20点经验值', '初始的30点经验值'),
    ('guide', 'literal-exp-term', '初始的20点经验值', '初始的20点属性点'),
    ('guide', 'starter-spelling', '乌力乌力、凯比、克克尔、威伯', '乌力、凯比、克克尔、威伯'),
    ('guide', 'birth-skill', '从一出生就会特殊技能', '从一出生不会特殊技能'),
    ('guide', 'grass-capture', '到新手村外的草地上捕捉', '到新手村内的医院捕捉'),
    ('guide', 'one-way', '就不能再进入', '就可以再进入'),
    ('guide', 'exit-destination', '会到达石器时代中的萨姆吉尔村', '会到达石器时代中的加加村'),
    ('guide', 'actual-image', 'xslc/image032.gif', 'xslc/image034.gif'),
    ('notice', 'rollout-date', '2003年6月10日', '2003年6月11日'),
    ('notice', 'first-group', '中国网通9服务器', '中国网通1服务器'),
    ('notice', 'phased-not-done', '所有服务器将陆续更新', '所有服务器已全部更新'),
    ('notice', 'actual-context-link', 'http://www.waei.com.cn/zhuanqu/sa6/', 'http://example.invalid/sa6/'),
]


def extract(raws):
    return {'guide': guide(raws['guide']), 'notice': notice(raws['notice'])}


def audit(raws, expected):
    results = []
    for source, label, old, new in MUTATIONS:
        t = raws[source].decode('gb18030')
        require(t.count(old) >= 1, 'Mutation anchor missing: ' + label)
        b = t.replace(old, new).encode('gb18030')
        try:
            x = (guide if source == 'guide' else notice)(b)
            rejected = {k: v for k, v in x.items() if k != 'core_sha256'} != {k: v for k, v in expected[source].items() if k != 'core_sha256'}
        except ValueError:
            rejected = True
        require(rejected, 'Semantic mutation accepted: ' + label)
        results.append({'source': source, 'case': label, 'input_sha256': sha(b), 'rejected_without_digest_gate': True})
    for key in raws:
        require((guide if key == 'guide' else notice)(raws[key] + b'<script>outside</script>') == expected[key], 'Outer positive rejected')
    changed = raws['guide'].replace(b'published at 2006-10-09 22:51:58', b'published at 2007-10-09 22:51:58')
    require(changed != raws['guide'] and guide(changed) == expected['guide'], 'Regeneration comment became publication evidence')
    return {'real_source_mutations': results, 'outer_script_positives': 2, 'regeneration_comment_positive': True}


def validate(r):
    local = json.loads((ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_text())
    require(r['extracted'] == local['extracted'] and r['images'] == local['images'], 'Source/visual observation changed')
    require(len(r['sources']) == 2 and [x['url'] for x in r['sources']] == list(URLS.values()), 'Source pair changed')
    for key, source in zip(URLS, r['sources']):
        require(source['authority'] == r['extracted'][key]['authority'] and source['authenticated_original_bytes'] is False, 'Authority promotion')
        require(source['displayed_publication'] == r['extracted'][key]['displayed_publication'] and source['encoding'] == 'GB18030_STRICT', 'Displayed stamp or encoding changed')
        require(source['current_observed_bytes'] == local['http'][key]['bytes'] and source['current_observed_sha256'] == local['http'][key]['sha256'], 'Observed source pins changed')
    require(len(r['records']) == 7, 'Bounded seven records')
    for row, key in zip(r['records'], ['entry', 'roster', 'creation', 'starter_pets', 'newcomer']):
        require(row['evidence'] == r['extracted']['guide'][key] and row['source_refs'] == ['S1'], 'Guide record evidence alignment')
    require(r['records'][5]['evidence'] == r['extracted']['notice'] and r['records'][5]['source_refs'] == ['S2'], 'Notice authority alignment')
    require(r['records'][6]['evidence'] == r['images'] and r['records'][6]['source_refs'] == ['S1'], 'Visual record alignment')
    require(len({x['record_id'] for x in r['records']}) == 7, 'Duplicate record IDs')
    for row in r['records']:
        require(row['version_profile'] == PROFILE and row['game_ids'] is None and row['runtime_verified'] is False, 'Version/ID/runtime promotion')
    require([x['id'] for x in r['images']] == IDS, 'Source image pair/order changed')
    require([x['url_as_written'] for x in r['images']] == [x['src'] for x in r['extracted']['guide']['image_references_in_source_order']], 'Not actual source-linked images')
    for im in r['images']:
        require(im['requested_url'] == im['url_as_written'].replace('http:', 'https:'), 'Image URL rewrite')
        require(im['capture_date'] is None and im['native_client_resolution_proven'] is False and im['exact_build_proven'] is False, 'Image authenticity promotion')
    require(all(v is False for v in r['unproven'].values()), 'Unproven claim promoted')
    require(r['status'] == {'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'}, 'Stage')
    require(r['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-50', 'Queue')


def replay(r, raws, images):
    validate(r)
    x = extract(raws)
    require(x == r['extracted'], 'Source core or semantics changed')
    require(len(images) == len(r['images']), 'Ten linked image objects required')
    for pin, b in zip(r['images'], images):
        require(len(b) == pin['bytes'] and sha(b) == pin['sha256'] and gif_structure(b) == pin['gif_structure'], 'Current GIF bytes/structure changed')
    return {'schema': 'stoneage.cn2003_onboarding.derived_replay.r1',
            'http': {k: {'bytes': len(v), 'sha256': sha(v)} for k, v in raws.items()},
            'extracted': x, 'images': r['images'], 'audit': audit(raws, x),
            'raw_html_or_assets_in_output': False, 'historical_client_or_server_executed': False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--fetch', action='store_true', required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    r = json.loads(REPORT.read_text())
    with ThreadPoolExecutor(max_workers=5) as pool:
        pages = list(pool.map(lambda u: fetch(u, 1000000), URLS.values()))
        raws = dict(zip(URLS, pages))
        images = list(pool.map(lambda im: fetch(im['requested_url'], 2000000), r['images']))
    out = replay(r, raws, images)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'success': True, 'http_bytes': {k: len(v) for k, v in raws.items()}, 'image_objects': len(images),
                      'content_images': sum(x['role'] == 'CONTENT_IMAGE' for x in r['images']), 'semantic_mutations': len(out['audit']['real_source_mutations'])}))


if __name__ == '__main__':
    main()
