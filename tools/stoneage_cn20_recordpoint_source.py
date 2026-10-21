"""Replay operator-hosted CN2.0 record-point guide; no bank or persistence implementation."""
import argparse
import hashlib
import json
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from tools.stoneage_cn2003_group2_manor_report import Visible

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-CN20-RECORDPOINT'
REPORT = ROOT / ('research/recovered/' + STEM + '-SOURCE-R1.json')
PROFILE = 'EARLY_LINEAGE:CN_WAEI_SITE_2.0_GUIDE_CAPTURED_2001'
URLS = (
    'https://web.archive.org/web/20011204194619id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet.asp',
    'https://web.archive.org/web/20011204000349id_/http://www.waei.com.cn/ZHUANQU/stoneage2/tyro/operation.asp',
    'https://web.archive.org/web/20011204220248id_/http://www.waei.com.cn/ZHUANQU/stoneage2/sw/meat.asp',
    'https://web.archive.org/web/20011204213609id_/http://www.waei.com.cn/ZHUANQU/stoneage2/sw/facility.asp',
)
ROUTES = [('基本操作', '/ZHUANQU/stoneage2/tyro/operation.asp'),
          ('存储肉位置', '/ZHUANQU/stoneage2/sw/meat.asp'),
          ('公共设施', '/ZHUANQU/stoneage2/sw/facility.asp')]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def visible(s, compact=True):
    p = Visible()
    p.feed(s)
    text = ''.join(p.parts)
    return re.sub(r'\s+', '' if compact else ' ', text).strip()


class Rows(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows, self.row, self.cell = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.row = []
        elif tag == 'td' and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag == 'td' and self.cell is not None:
            self.row.append(re.sub(r'\s+', ' ', ''.join(self.cell)).strip())
            self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.rows.append(self.row)
            self.row = None


def body(raw):
    t = raw.decode('gb18030', errors='strict')
    require('<title>石器时代2.0</title>' in t, 'CN2.0 page title missing')
    marker = '(稿务必注明所在服务器、作者及作品名称)'
    require(t.count(marker) == 1, 'Main content boundary changed')
    t = t.split(marker, 1)[1]
    require(t.count('<span class="p12b">') == 1, 'Main content end changed')
    return t.split('<span class="p12b">', 1)[0]


def extract(raws):
    require(len(raws) == 4, 'Navigation and three source pages required')
    nav = raws[0].decode('gb18030', errors='strict')
    for label, href in ROUTES:
        matches = re.findall(r'<a\b[^>]*href=["\']' + re.escape(href) + r'["\'][^>]*>(.*?)</a>', nav, re.I | re.S)
        require(len(matches) == 1 and visible(matches[0]) == label, 'Real navigation route changed')
    op, meat, fac = [body(b) for b in raws[1:]]
    optext = visible(op)
    logout = re.search(r'登出：结束游戏。原地登出：选择原地登出，在下次登入时会出现在登出地点而不是记录点。', optext)
    trade = re.search(r'd\.交易键接受交易要求的玩家必须将交易设定为(YES)。e\.家族键', optext)
    require(logout and trade, 'Logout destination or receiving trade permission changed')
    require('存储肉位置' in visible(meat) and '储存是以每个村要不同的肉来做储存条件' in visible(meat), 'Meat tribute context changed')
    tables = re.findall(r'<table\s+bordercolor=#74BB3B\b.*?</table>', meat, re.I | re.S)
    require(len(tables) == 3, 'Three island tables required')
    rows = []
    for table, island in zip(tables, ('北岛', '南岛', '吉鲁岛')):
        p = Rows(); p.feed(table)
        require(p.rows[0] == [island] and p.rows[1] == ['储存点名称（村庄名）', '座标', '所需要的肉'], 'Island/header context changed')
        for cells in p.rows[2:]:
            require(len(cells) == 3 and all(cells), 'Malformed source row')
            name, coords, tribute = cells
            rows.append({'island_label': island, 'place_as_written': name,
                         'coordinate_cell_as_written': coords, 'meat_cell_as_written': tribute,
                         'original_map_npc_item_ids': None, 'coordinates_are_verified_npc_positions': False,
                         'multiple_coordinate_meaning': None, 'multi_meat_operator': None})
    require([sum(x['island_label'] == k for x in rows) for k in ('北岛', '南岛', '吉鲁岛')] == [7, 8, 2], 'Finite table row count changed')
    point_rows = [r for r in re.findall(r'<tr\b[^>]*>(.*?)</tr>', fac, re.S | re.I) if '<b>纪录点</b>' in r]
    require(len(point_rows) == 1, 'Record point row changed')
    point = point_rows[0]; text = visible(point)
    checks = ['早先的游戏设定，并没有「原地注销」的系统指令', '一定是出现在最后一次的纪录点前',
              '玩家被敌人打飞后，会飞回到纪录点前', '玩家使用「注销」指令，下次再进入游戏时便会在纪录点',
              '只要对纪录点说话，就可以知道目前的在线人数有多少', '纪录点的使用需要付出贡品，不同的纪录点需要不同的肉']
    require(all(s in text for s in checks), 'Re-entry, knockback, population or tribute semantics changed')
    images = re.findall(r'<img\b[^>]*src=["\']([^"\']+)', point, re.I)
    require(len(images) == 1, 'Record point image declaration changed')
    return {'routes': [{'label': a, 'href': b} for a, b in ROUTES],
            'selected_core_sha256': {'operation': sha((logout[0] + trade[0]).encode()), 'meat': sha(visible(meat).encode()), 'recordpoint': sha(text.encode())},
            'logout': {'normal_label_as_written': '登出', 'in_place_label_as_written': '原地登出',
                       'in_place_reentry': 'LOGOUT_LOCATION_INSTEAD_OF_RECORD_POINT', 'first_introduction_date': None,
                       'exact_save_format_or_local_savedata_relation': None},
            'trade': {'recipient_permission_as_written': trade[1], 'full_exchange_confirmation_or_atomicity': None},
            'recordpoint': {'facility_label_as_written': '纪录点', 'ordinary_logout_reentry': 'LAST_RECORD_POINT',
                            'knocked_away_destination': 'RECORD_POINT', 'in_place_label_as_written': '原地注销',
                            'talk_service_as_reported': 'ONLINE_POPULATION_UNSPECIFIED_SCOPE',
                            'requires_place_specific_meat_tribute': True, 'consume_or_check_only': None,
                            'count_scope_refresh_or_protocol': None, 'original_save_storage': None},
            'rows': rows, 'recordpoint_image_path_declared': images[0],
            'version': PROFILE, 'authorship': 'OPERATOR_HOSTED_GUIDE_AUTHOR_UNVERIFIED',
            'original_server_executed': False}


# Mutate real downloaded source; compare semantics with all digest fields removed.
MUTATIONS = (
    (0, 'route', '/sw/meat.asp', '/sw/missing.asp'),
    (1, 'reentry', '登出地点而不是记录点', '记录点而不是登出地点'),
    (1, 'trade-permission', '设定为YES', '设定为NO'),
    (2, 'island', '<b>北岛</b>', '<b>西岛</b>'),
    (2, 'place-name', '萨姆吉尔村', '萨姆吉尔城'),
    (2, 'coordinate-value', '637，491', '638，491'),
    (2, 'coordinate-second-pair', '708 ，489', '708 ，490'),
    (2, 'duplicate-coordinate', '克洛尔X1', '克洛尔X2'),
    (2, 'meat-name', '凯比特X1', '凯比特斯X1'),
    (2, 'meat-quantity', '乌力斯坦X2', '乌力斯坦X1'),
    (2, 'unknown-meat', '不详', '乌力X1'),
    (2, 'space-coordinate', '191 365', '191 366'),
    (2, 'multiple-meat', '布依X1、火鸡X1', '布依X1'),
    (2, 'case-sensitive-source', '乌力坦斯x1', '乌力坦斯X2'),
    (3, 'knockback', '会飞回到纪录点前', '会停留在原地点'),
    (3, 'ordinary-logout', '下次再进入游戏时便会在纪录点', '下次再进入游戏时便会在原地点'),
    (3, 'population', '目前的在线人数', '目前的注册人数'),
    (3, 'tribute', '需要付出贡品', '不需要付出贡品'),
    (3, 'original-command', '并没有「原地注销」', '已有「原地注销」'),
    (3, 'declared-image', 'img/image011.jpg', 'img/image099.jpg'),
)


def semantic(x):
    return {k: v for k, v in x.items() if k != 'selected_core_sha256'}


def audit(raws, expected):
    out = []
    for i, label, old, new in MUTATIONS:
        text = raws[i].decode('gb18030'); require(old in text, 'Missing mutation anchor: ' + label)
        changed = list(raws); changed[i] = text.replace(old, new).encode('gb18030')
        try:
            rejected = semantic(extract(changed)) != semantic(expected)
        except ValueError:
            rejected = True
        require(rejected, 'Real semantic mutation accepted: ' + label)
        out.append({'case': label, 'source_index': i, 'input_sha256': sha(changed[i]), 'rejected_without_digest_gate': True})
    changed = [b + b'<script>outside content</script>' for b in raws]
    require(extract(changed) == expected, 'Outer script positive failed')
    return {'real_source_mutations': out, 'outer_script_positive': True}


def validate(r):
    require(r['schema'] == 'stoneage.cn20_recordpoint.source.r1', 'Contract schema changed')
    local = json.loads((ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_text())
    require(r['extracted'] == local['extracted'], 'Source semantics changed')
    require([x['url'] for x in r['sources']] == list(URLS), 'Exact captures changed')
    require([x['bytes'] for x in r['sources']] == [x['bytes'] for x in local['http']], 'Source lengths changed')
    require([x['sha256'] for x in r['sources']] == [x['sha256'] for x in local['http']], 'Source digests changed')
    for i, row in enumerate(r['sources']):
        require(row['capture_timestamp'] == URLS[i].split('/web/')[1][:14] and row['publication_date'] is None and row['exact_client_build'] is None, 'Capture promoted to publication/build')
        require(row['encoding'] == 'GB18030_STRICT' and row['author_verified'] is False, 'Encoding or authorship promoted')
        require(row['role'] == ('NAVIGATION_ONLY' if i == 0 else 'OPERATOR_HOSTED_GUIDE_NOT_RUNTIME'), 'Source role promoted')
    require(len(r['records']) == 20 and len({x['record_id'] for x in r['records']}) == 20, '17 table rows plus 3 behavior records required')
    evidence = [r['extracted'][k] for k in ('logout', 'trade', 'recordpoint')] + r['extracted']['rows']
    for i, (row, ev) in enumerate(zip(r['records'], evidence)):
        require(row['evidence'] == ev and row['version_profile'] == PROFILE and row['game_ids'] is None and row['runtime_verified'] is False, 'Record attribution promoted')
        require(row['source_refs'] == ([['S1'], ['S1'], ['S3']][i] if i < 3 else ['S2']), 'Record source changed')
    im = r['image_reference']
    require(im['path_as_written'] == r['extracted']['recordpoint_image_path_declared'] and im['observed_http_status'] == 404, 'Unavailable image observation changed')
    require(im['image_bytes_obtained'] is False and im['capture_timestamp_verified'] is None and im['all_archives_missing_proven'] is False, 'Missing image promoted')
    require(im['requested_url'] == URLS[3].rsplit('/', 1)[0] + '/' + im['path_as_written'] and im['image_authenticates_coordinates_or_save_state'] is False, 'Image provenance promoted')
    require(all(x is False for x in r['unproven'].values()), 'Unproven conclusion promoted')
    require(r['status'] == {'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'}, 'Stage changed')
    require(r['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-52', 'Queue changed')


def replay(r, raws):
    validate(r); x = extract(raws)
    require(x == r['extracted'], 'Selected source content changed')
    http = [{'bytes': len(b), 'sha256': sha(b)} for b in raws]
    require(http == [{'bytes': s['bytes'], 'sha256': s['sha256']} for s in r['sources']], 'Actual HTML pins changed')
    return {'schema': 'stoneage.cn20_recordpoint.derived_replay.r1', 'http': http, 'extracted': x,
            'audit': audit(raws, x), 'raw_html_or_assets_in_output': False, 'original_server_executed': False}


def fetch(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=40) as response:
                require(response.status == 200 and response.url == url, 'Exact capture response mismatch')
                b = response.read(1000001); require(len(b) <= 1000000, 'Source oversized'); return b
        except (OSError, ValueError):
            if attempt == 2:
                raise
            time.sleep(1)


def main():
    p = argparse.ArgumentParser(); p.add_argument('--fetch', action='store_true', required=True); p.add_argument('--output', type=Path, required=True)
    args = p.parse_args(); r = json.loads(REPORT.read_text())
    with ThreadPoolExecutor(max_workers=4) as pool:
        raws = list(pool.map(fetch, URLS))
    out = replay(r, raws); args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'success': True, 'source_bytes': [len(b) for b in raws], 'table_rows': len(out['extracted']['rows']), 'semantic_mutations': len(out['audit']['real_source_mutations'])}))


if __name__ == '__main__':
    main()
