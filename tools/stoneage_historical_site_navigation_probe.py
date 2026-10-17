"""Finite historical-site link metadata, never a reconstructed historical layout."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

LIMIT = 2_000_000
TARGETS = {
    'jss_manual_index': ('http://www.titan.co.jp/stoneage/manual.html', '20010418083149', 'shift_jis', 'OPERATOR_FIRST_PARTY', 'DIRECT_REPLAY_REQUEST'),
    'jss_home': ('http://www.titan.co.jp/stoneage/', '20010418', 'shift_jis', 'OPERATOR_FIRST_PARTY', 'AVAILABILITY'),
    'jss_home_index': ('http://www.titan.co.jp/stoneage/index.html', '20010418', 'shift_jis', 'OPERATOR_FIRST_PARTY', 'AVAILABILITY'),
    'jss_manual01': ('http://www.titan.co.jp/stoneage/manual01.html', '20010418082314', 'shift_jis', 'OPERATOR_FIRST_PARTY', 'DIRECT_REPLAY_REQUEST'),
    'jss_manual02': ('http://www.titan.co.jp/stoneage/manual02.html', '20010418083149', 'shift_jis', 'OPERATOR_FIRST_PARTY', 'DIRECT_REPLAY_REQUEST'),
    '17173_home': ('http://stoneage.17173.com/', '20010630', 'gb18030', 'CONTEMPORANEOUS_MEDIA', 'AVAILABILITY'),
    '17173_exchange': ('http://stoneage.17173.com/jiaoliu/jiaoliu.shtml', '20020321', 'gb18030', 'CONTEMPORANEOUS_MEDIA', 'AVAILABILITY'),
}
TOPICS = {
    'login_splash': r'ログイン|登入|登录', 'character_creation': r'キャラクター|人物|角色',
    'pet_species': r'ペット|宠物|寵物', 'quest_content': r'クエスト|任务|任務',
    'world_map': r'マップ|地図|地图|地圖', 'battle_ui_rules': r'戦闘|战斗|戰鬥',
    'item_equipment_economy': r'アイテム|道具|物品|合成|料理|购物|購物',
    'reference_web': r'マニュアル|manual|攻略|指南|手册|手冊',
    'helper_versions': r'外挂|外掛|辅助|輔助',
}


def require(ok, message):
    if not ok: raise ValueError(message)


def archive_parts(url):
    m = re.fullmatch(r'https?://web\.archive\.org/web/(\d{14})(?:id_)?/(https?://.+)', url)
    require(m is not None, 'not an exact archive replay URL')
    return m[1], m[2]


def identity(url):
    p = urllib.parse.urlsplit(url)
    require(p.scheme in ('http', 'https') and p.hostname and not p.username and not p.password, 'URL identity')
    require(p.port in (None, 80, 443), 'unexpected port')
    return p.hostname.lower(), p.path or '/', p.query


class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []; self.active = None; self.base = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'base' and attrs.get('href') and self.base is None: self.base = attrs['href']
        if tag == 'a':
            if self.active is not None: self.links.append(self.active)
            self.active = {'kind': 'ANCHOR', 'href': attrs.get('href', ''), 'text': ''}
        elif tag in ('frame', 'iframe') and attrs.get('src'):
            self.links.append({'kind': tag.upper(), 'href': attrs['src'], 'text': ''})
        elif tag == 'area' and attrs.get('href'):
            self.links.append({'kind': 'AREA', 'href': attrs['href'], 'text': attrs.get('alt', '')})
        elif tag == 'img' and self.active is not None:
            self.active['text'] += attrs.get('alt', '')

    def handle_endtag(self, tag):
        if tag == 'a' and self.active is not None:
            self.links.append(self.active); self.active = None

    def handle_data(self, data):
        if self.active is not None: self.active['text'] += data

    def finish(self):
        if self.active is not None: self.links.append(self.active); self.active = None


def derived_links(doc, original):
    parser = Links(); parser.feed(doc); parser.close(); parser.finish()
    base = urllib.parse.urljoin(original, parser.base) if parser.base else original
    # A base may itself have been rewritten by a replay service.
    if re.match(r'https?://web\.archive\.org/web/', base): _, base = archive_parts(base)
    identity(base)
    rows = []
    for entry in parser.links:
        href = entry['href'].strip()
        if not href or re.match(r'(?i)(javascript|mailto|data|tel):', href): continue
        target = urllib.parse.urljoin(base, href)
        if re.match(r'https?://web\.archive\.org/web/', target): _, target = archive_parts(target)
        p = urllib.parse.urlsplit(target)
        if p.scheme not in ('http', 'https') or p.username or p.password: continue
        label = ' '.join(entry['text'].split())
        topics = sorted(k for k, regex in TOPICS.items() if re.search(regex, label, re.I))
        kind = 'PAGE_OR_FRAGMENT'
        if re.search(r'\.(gif|jpe?g|png|bmp|wav|mid|mp3)$', p.path, re.I): kind = 'ASSET_REFERENCE_NOT_FETCHED'
        if re.search(r'\.(exe|zip|lzh|rar|cab|dll)$', p.path, re.I): kind = 'DOWNLOAD_REFERENCE_NOT_FETCHED'
        rows.append({'source_order': len(rows), 'link_kind': entry['kind'], 'target_url': target,
                     'target_kind': kind, 'same_host': p.hostname == urllib.parse.urlsplit(original).hostname,
                     'label_sha256': hashlib.sha256(label.encode()).hexdigest(), 'label_characters': len(label),
                     'topic_candidates': topics, 'topic_match_basis': 'ANCHOR_LABEL_HEURISTIC_NOT_DESTINATION_VERIFICATION'})
    require(len(rows) <= 1000, 'bounded navigation link count')
    return rows


def qualify(key, raw, final_url):
    original, requested, codec, role, method = TARGETS[key]
    timestamp, actual_original = archive_parts(final_url)
    require('19990101000000' <= timestamp <= '20021231235959', 'capture outside historical window')
    require(identity(actual_original) == identity(original), 'replay changed original target')
    require(0 < len(raw) <= LIMIT, 'bounded HTML bytes')
    doc = raw.decode(codec, errors='replace')
    require(re.search(r'<(?:html|frameset|body)\b', doc, re.I) is not None, 'not HTML')
    # Identity guards supplement origin/date; they do not certify all content.
    require(re.search(r'stoneage|stone\s+age|ストーンエイジ|石器', doc, re.I) is not None, 'site identity absent')
    links = derived_links(doc, actual_original)
    return {'status': 'ARCHIVED_HTML_LINK_METADATA_QUALIFIED', 'requested_original': original,
            'requested_timestamp': requested, 'actual_capture': timestamp, 'actual_original': actual_original,
            'final_url': final_url, 'source_role': role, 'discovery_method': method,
            'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'codec': codec,
            'replacement_characters': doc.count('\ufffd'), 'links': links,
            'link_count': len(links), 'visual_layout_verified': False,
            'linked_destination_contents_verified': False, 'full_historical_site_recovered': False}


def get(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'StoneAgeHistoricalNavigationResearch/1.0', 'Accept-Encoding': 'identity'})
    with urllib.request.urlopen(request, timeout=25) as response:
        require(response.status == 200, 'HTTP status')
        raw = response.read(LIMIT + 1)
        require(len(raw) <= LIMIT, 'response too large')
        return raw, response.url


def acquire(key):
    original, timestamp, _, role, method = TARGETS[key]
    row = {'requested_original': original, 'requested_timestamp': timestamp, 'source_role': role, 'discovery_method': method}
    try:
        if method == 'AVAILABILITY':
            url = 'https://archive.org/wayback/available?' + urllib.parse.urlencode({'url': original, 'timestamp': timestamp})
            raw, final = get(url)
            row['availability_query'] = {'url': url, 'final_url': final, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
            cap = json.loads(raw).get('archived_snapshots', {}).get('closest')
            if not cap:
                return key, dict(row, status='NO_CLOSEST_FOR_THIS_QUERY_NOT_GLOBAL_ABSENCE')
            require(cap.get('available') is True and str(cap.get('status')) == '200', 'unqualified closest response')
            replay = str(cap['url'])
            ts, target = archive_parts(replay)
            require(identity(target) == identity(original), 'availability changed target')
            require('19990101000000' <= ts <= '20021231235959', 'closest outside early window')
        else:
            replay = f'https://web.archive.org/web/{timestamp}id_/{original}'
        # id_ avoids present-day replay navigation contaminating link extraction.
        ts, target = archive_parts(replay)
        replay = f'https://web.archive.org/web/{ts}id_/{target}'
        raw, final = get(replay)
        out = qualify(key, raw, final)
        if 'availability_query' in row: out['availability_query'] = row['availability_query']
        out['replay_request'] = replay
        return key, out
    except Exception as exc:
        if isinstance(exc, urllib.error.HTTPError): error = {'kind': 'HTTPError', 'status_code': exc.code}
        else: error = {'kind': type(exc).__name__, 'message': str(exc)[:180]}
        return key, dict(row, status='QUERY_OR_REPLAY_UNQUALIFIED_NOT_GLOBAL_ABSENCE', error=error)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with ThreadPoolExecutor(max_workers=4) as pool: pages = dict(pool.map(acquire, TARGETS))
    out = {'schema': 'stoneage.historical_site_navigation.r1', 'targets': pages,
           'historical_window': ['1999-01-01', '2002-12-31'],
           'qualified_pages': sum(p['status'] == 'ARCHIVED_HTML_LINK_METADATA_QUALIFIED' for p in pages.values()),
           'historical_site_structure_fully_recovered': False, 'website_implemented': False,
           'original_html_images_or_binaries_retained': False, 'source_absence_established': False}
    args.output.write_text(json.dumps(out, ensure_ascii=False, sort_keys=True) + '\n')
    print(json.dumps({'qualified_pages': out['qualified_pages'], 'statuses': {k: p['status'] for k, p in pages.items()}}))


if __name__ == '__main__': main()
