"""Bounded CINS-era stall documentation and current linked JPEG custody."""
import argparse
import hashlib
import json
import re
import struct
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-CN2011-2012-STALL'
REPORT = ROOT / ('research/recovered/' + STEM + '-SOURCE-R1.json')
URLS = {'2011': 'https://games.sina.com.cn/o/n/2011-01-12/1038467817.shtml',
        '2012': 'https://games.sina.com.cn/o/n/2012-12-04/1430674461.shtml'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Article(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = self.article_depth = self.p_depth = self.block = 0
        self.roots, self.paragraphs, self.images, self.current = 0, [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.depth += 1
        if tag == 'div' and a.get('id') == 'artibody':
            self.article_depth = self.depth
            self.roots += 1
        if not self.article_depth:
            return
        if tag in ('script', 'style', 'iframe', 'noscript'):
            self.block += 1
        if tag == 'p' and not self.block:
            self.p_depth, self.current = self.depth, []
        if tag == 'img' and not self.block and re.match(r'http://i[0-3]\.sinaimg\.cn/gm/201[12]/', a.get('src', '')):
            self.images.append({k: a.get(k) for k in ('src', 'alt', 'title')})

    def handle_endtag(self, tag):
        if self.article_depth:
            if tag in ('script', 'style', 'iframe', 'noscript') and self.block:
                self.block -= 1
            if tag == 'p' and self.p_depth:
                self.paragraphs.append(re.sub(r'\s+', '', ''.join(self.current)))
                self.p_depth = 0
            if tag == 'div' and self.depth == self.article_depth:
                self.article_depth = 0
        if tag not in VOID:
            self.depth -= 1

    def handle_data(self, data):
        if self.article_depth and self.p_depth and not self.block:
            self.current.append(data)


def parse(raw, key):
    text = raw.decode('gb18030', errors='strict')
    stamp = {'2011': '2011年01月12日 10:38', '2012': '2012年12月04日 14:30'}[key]
    require(stamp in text, 'Publication changed: ' + key)
    p = Article()
    p.feed(text)
    require(p.roots == 1, 'Article root missing/ambiguous')
    start = next((i for i, s in enumerate(p.paragraphs) if s.startswith('想日进斗金吗')), None)
    end = next((i for i, s in enumerate(p.paragraphs) if s.startswith('声明：')), None)
    require(start is not None and end is not None and start < end, 'Article boundaries missing')
    paragraphs = p.paragraphs[start:end]
    require(any('胜思网络' in s for s in paragraphs), 'Operator promotional attribution missing')
    require('http://sa.cins.cn/?sqsd' in text, 'Official site reference changed')
    require(len(p.images) == (3 if key == '2011' else 1), 'Bounded image reference count changed')
    return paragraphs, p.images


CLAUSES = ('游戏界面左上方的“摆摊”专用按钮', '即可进入店铺设置栏',
           '选择好自己要出售的物品或宠物', '并设置相应的价钱', '加上一个广告说明', '最后，再“确认”',
           '上架到摊位准备出售的商品', '红色的“SELL”标识',
           '普通聊天还是家族、职业或者是密语频道', '无须缴纳任务费用', '想在哪摆就可摆在哪')


def extract(raws):
    parsed = {k: parse(raws[k], k) for k in URLS}
    cores = {k: ''.join(v[0]) for k, v in parsed.items()}
    for key, text in cores.items():
        require(all(c in text for c in CLAUSES), 'Material stall claim changed: ' + key)
    require('石灰封测(不删档)' in cores['2011'] and '2011年1月15日' in cores['2011'], '2011 future test context changed')
    require('更多精彩，敬请继续锁定胜思网络' in cores['2012'], '2012 operator context changed')
    sections = {}
    for key, (paragraphs, _) in parsed.items():
        a, b = paragraphs.index('【如何摆摊】'), paragraphs.index('【价钱商讨】')
        sections[key] = ''.join(paragraphs[a:b])
    require(sections['2011'] == sections['2012'], 'Shared instruction block differs')
    return {
        'core_sha256': {k: sha(t.encode()) for k, t in cores.items()},
        'image_references': {k: v[1] for k, v in parsed.items()},
        'issuer_evidence': 'SINA_HOSTED_CINS_NAMED_PROMOTIONAL_COPY_WITHOUT_AUTHENTICATED_ORIGINAL_ISSUER_FILE',
        'numeric_version_or_build': None,
        'entry': {'position_reported': 'UPPER_LEFT', 'button': '摆摊', 'destination': '店铺设置栏', 'exact_original_coordinates': None},
        'listing_steps': ['SELECT_ITEMS_OR_PETS', 'SET_PRICE', 'ADD_ADVERTISEMENT', 'CONFIRM'],
        'sale_marker': {'text': 'SELL', 'color_reported': 'RED', 'meaning_reported': 'LISTED_FOR_SALE_NOT_SOLD'},
        'bargaining_channels': ['普通', '家族', '职业', '密语'],
        'fee_and_location_claim': {'fee_wording_as_written': '无须缴纳任务费用', 'location': 'PROMOTIONAL_ANYWHERE_CLAIM',
                                   'all_taxes_zero_proven': False, 'verified_map_permission_table': None},
        'test_context_2011': {'announced_date': '2011-01-15', 'label': '石灰封测', 'no_deletion_promised': True, 'launch_or_retention_observed': False},
        'cross_date_relation': {'shared_instruction_block_sha256': sha(sections['2011'].encode()),
                                'relation': 'LITERAL_INSTRUCTION_REUSE_NOT_AUTHENTICATED_SAME_BUILD', 'same_build_proven': False,
                                '2012_includes_literal_weibo_token': 'weibo' in cores['2012']},
        'currency_price_limits_slots_offline_buyer_settlement_rules': None,
        'automatic_bargaining_or_auction_rules_proven': False,
        'historical_server_executed': False, 'early_build_membership_proven': False,
    }


def jpeg_dimensions(b):
    require(b.startswith(b'\xff\xd8'), 'Not JPEG')
    i = 2
    while i < len(b):
        require(b[i] == 255, 'Invalid JPEG marker')
        while i < len(b) and b[i] == 255:
            i += 1
        require(i < len(b), 'Truncated JPEG marker')
        marker = b[i]
        i += 1
        if marker in (0xd8, 0xd9, 0x01) or 0xd0 <= marker <= 0xd7:
            continue
        require(i + 2 <= len(b), 'Truncated JPEG length')
        length = int.from_bytes(b[i:i+2], 'big')
        require(length >= 2 and i + length <= len(b), 'Invalid JPEG segment length')
        if marker in (0xc0, 0xc1, 0xc2):
            require(length >= 8, 'Invalid SOF')
            height, width = struct.unpack('>HH', b[i+3:i+7])
            return width, height
        i += length
    raise ValueError('No supported JPEG SOF')


def inspect_images(r, images):
    out = []
    for pin in r['images']:
        b = images[pin['requested_url']]
        width, height = jpeg_dimensions(b)
        require((len(b), sha(b), width, height) == (pin['bytes'], pin['sha256'], pin['width'], pin['height']), 'Linked JPEG changed')
        out.append({k: pin[k] for k in ('source', 'url_as_written', 'requested_url', 'bytes', 'sha256', 'width', 'height')})
    return out


def validate(r):
    require(r['schema'] == 'stoneage.cn2011_2012_stall.source_contract.r1', 'Schema')
    require({k: x['url'] for k, x in r['sources'].items()} == URLS, 'Source URLs')
    require(all(x['authority'] == 'CINS_NAMED_PROMOTIONAL_ARTICLE_PUBLISHED_BY_SINA' and x['authenticated_historical_original_bytes'] is False for x in r['sources'].values()), 'Source authority promoted')
    local = json.loads((ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_text())
    require(r['extracted'] == local['extracted'], 'Semantics/unknown changed')
    require(all(r['sources'][k]['core_sha256'] == r['extracted']['core_sha256'][k] for k in URLS), 'Source-core pins disagree')
    require(len(r['images']) == 4 and len({x['sha256'] for x in r['images']}) == 4, 'Image count or byte identity')
    refs = r['extracted']['image_references']
    require([x['url_as_written'] for x in r['images']] == [x['src'] for key in URLS for x in refs[key]], 'Images not actually linked by the articles')
    for x in r['images']:
        require(x['requested_url'] == x['url_as_written'].replace('http://', 'https://'), 'Undeclared image URL rewrite')
        require(x['authenticated_capture_date'] is None and x['native_client_resolution_proven'] is False, 'Current image promoted to historical capture/build')
    require(r['visual_observations'] == local['visual_observations'], 'Visual evidence boundary changed')
    require(len(r['records']) == 7 and len({x['record_id'] for x in r['records']}) == 7, 'Bounded records')
    for row in r['records']:
        require(row['version_profile'] == 'LATER_OFFICIAL:CN_CINS_2011_2012_BUILD_UNKNOWN' and row['game_ids'] is None, 'Version or game ID invented')
    require(all(x is False for x in r['unproven'].values()), 'Unproven claim promoted')
    require(r['status'] == {'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'}, 'Stage')
    require(r['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-46', 'Queue')


MUTATIONS = (
    ('entry-location', '游戏界面左上方', '游戏界面右下方'),
    ('entry-button', '“摆摊”专用按钮', '“交易”专用按钮'),
    ('listing-kind', '出售的物品或宠物', '出售的物品'),
    ('price-step', '并设置相应的价钱', '并接受系统固定价钱'),
    ('advertisement-step', '加上一个广告说明', '加上一个密码说明'),
    ('confirm-step', '最后，再“确认”', '最后，再“取消”'),
    ('sale-marker-color', '红色的“SELL”', '绿色的“SELL”'),
    ('sale-marker-state', '“SELL”标识', '“SOLD”标识'),
    ('channel-kind', '家族、职业或者是密语频道', '家族、世界或者是密语频道'),
    ('fee-claim', '无须缴纳任务费用', '需要缴纳任务费用'),
    ('location-claim', '想在哪摆就可摆在哪', '仅在指定地图摆摊'),
)


def audit(raws, expected):
    checks = []
    for key in URLS:
        text = raws[key].decode('gb18030')
        for label, old, new in MUTATIONS:
            # Mutation anchors must be actual visible paragraphs, not repeated metadata.
            paragraphs, _ = parse(raws[key], key)
            require(sum(p.count(old) for p in paragraphs) == 1 and text.count(old) == 1, 'Ambiguous mutation: ' + key + ':' + label)
            modified = text.replace(old, new, 1).encode('gb18030')
            changed = dict(raws, **{key: modified})
            try:
                x = extract(changed)
                x.pop('core_sha256')
                target = dict(expected)
                target.pop('core_sha256')
                rejected = x != target
            except ValueError:
                rejected = True
            require(rejected, 'Semantic change accepted: ' + label)
            checks.append({'source': key, 'case': label, 'input_sha256': sha(modified), 'rejected_without_digest_gate': True})
    positives = {}
    for key in URLS:
        require(extract(dict(raws, **{key: raws[key] + b'<script>outer change</script>'})) == expected, 'Outer-only change affected source')
        positives[key] = True
    return {'real_body_mutations': checks, 'outer_script_positives': positives}


def replay(r, raws, images):
    validate(r)
    require(extract(raws) == r['extracted'], 'Source core or semantics changed')
    return {'schema': 'stoneage.cn2011_2012_stall.derived_replay.r1',
            'http': {k: {'bytes': len(b), 'sha256': sha(b)} for k, b in raws.items()},
            'extracted': extract(raws), 'images': inspect_images(r, images),
            'visual_observations': r['visual_observations'], 'audit': audit(raws, r['extracted']),
            'raw_html_or_assets_in_output': False, 'historical_server_executed': False}


def fetch(url, limit):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
        require(response.status == 200, 'HTTP failed')
        raw = response.read(limit + 1)
        require(len(raw) <= limit, 'Response oversized')
        return raw


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--fetch', action='store_true')
    g.add_argument('--input-dir', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    r = json.loads(REPORT.read_text())
    raws = {k: fetch(u, 1000000) if a.fetch else (a.input_dir / (k + '.html')).read_bytes() for k, u in URLS.items()}
    images = {x['requested_url']: fetch(x['requested_url'], 2000000) if a.fetch else (a.input_dir / x['url_as_written'].rsplit('/', 1)[1]).read_bytes() for x in r['images']}
    out = replay(r, raws, images)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'success': True, 'http_bytes': {k: len(b) for k, b in raws.items()}, 'images': len(images), 'semantic_mutations': len(out['audit']['real_body_mutations'])}))


if __name__ == '__main__':
    main()
