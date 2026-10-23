"""Replay two real Katan NPC image links; emit derived metadata only."""
import argparse
import hashlib
import io
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/recovered/STONEAGE-CN2003-KATAN-NPC-VISUAL-SOURCE-R100.json'
SOURCE_SHA = '04494355d31ac97e26f6ce275ca6c10eb05a5b50da0998bece67439a0a7c6cdf'


def require(value, message):
    if not value:
        raise ValueError(message)


class Tables(HTMLParser):
    """Extract visible table cells, retaining actual anchor/image adjacency."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables = []
        self.stack = []
        self.hidden_tags = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        void = tag in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr')
        style = ''.join(a.get('style', '').lower().split())
        hidden = tag in ('script', 'style') or 'hidden' in a or a.get('aria-hidden') == 'true' or 'display:none' in style or 'visibility:hidden' in style
        if self.hidden_tags or hidden:
            if not void:
                self.hidden_tags.append(tag)
            return
        if tag == 'table':
            self.stack.append({'rows': [], 'row': None, 'cell': None, 'anchor': None})
        if not self.stack:
            return
        t = self.stack[-1]
        if tag == 'tr':
            t['row'] = []
            t['rows'].append(t['row'])
        elif tag in ('td', 'th') and t['row'] is not None:
            t['cell'] = {'text': '', 'images': []}
            t['row'].append(t['cell'])
        elif tag == 'a':
            t['anchor'] = a.get('href')
        elif tag == 'img' and t['cell'] is not None:
            t['cell']['images'].append({'href': t['anchor'], 'src': a.get('src')})

    def handle_endtag(self, tag):
        if self.hidden_tags:
            if tag in self.hidden_tags:
                self.hidden_tags = self.hidden_tags[:len(self.hidden_tags) - 1 - self.hidden_tags[::-1].index(tag)]
            return
        if not self.stack:
            return
        t = self.stack[-1]
        if tag == 'table':
            self.tables.append(self.stack.pop()['rows'])
        elif tag in ('td', 'th'):
            t['cell'] = None
        elif tag == 'a':
            t['anchor'] = None

    def handle_data(self, data):
        if self.hidden_tags:
            return
        self.text.append(data)
        if self.stack and self.stack[-1]['cell'] is not None:
            self.stack[-1]['cell']['text'] += data


def compact(s):
    return ''.join(s.split())


def validate_source(d):
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, 'source contract hash mismatch')
    require(d == json.loads(raw), 'mutated source contract')
    for path, pin in d['parents'].items():
        b = (ROOT / path).read_bytes()
        require(len(b) == pin['bytes'] and hashlib.sha256(b).hexdigest() == pin['sha256'], 'parent digest mismatch')
        blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
        require(blob == pin['git_blob'], 'parent blob mismatch')
    return d


def parse_page(raw, d):
    parser = Tables()
    parser.feed(raw.decode(d['source']['encoding'], errors='strict'))
    visible = compact(''.join(parser.text))
    require(d['source']['title'] in visible and d['source']['display_date'].replace(' ', '') in visible, 'wrong article identity')
    require('网友投稿' in visible, 'missing player submission attribution')
    candidates = []
    for rows in parser.tables:
        if len(rows) < 2:
            continue
        images = [c for c in rows[0] if c['images']]
        captions = [c for c in rows[1] if compact(c['text'])]
        if captions and compact(captions[0]['text']) == compact(d['images'][0]['caption']):
            candidates.append((images, captions))
    require(len(candidates) == 1, 'missing or ambiguous first illustration table')
    images, captions = candidates[0]
    require(len(images) == len(captions) == 3, 'illustration table shape changed')
    selected = []
    for index, expected in enumerate(d['images']):
        require(compact(captions[index]['text']) == compact(expected['caption']), 'caption/order changed')
        require(images[index]['images'] == [{'href': expected['original_href'], 'src': expected['thumbnail']}], 'full/thumbnail link changed')
        # The only transport normalization permitted is HTTP to HTTPS at same host/path.
        selected.append(expected['original_href'].replace('http:', 'https:', 1))
    return selected


def decode_image(raw, expected):
    from PIL import Image
    require(len(raw) == expected['bytes'] and hashlib.sha256(raw).hexdigest() == expected['sha256'], 'image byte identity mismatch')
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        facts = {'format': im.format, 'size': list(im.size), 'mode': im.mode, 'frames': getattr(im, 'n_frames', 1)}
    require(all(facts[k] == expected[k] for k in facts), 'image decode metadata mismatch')
    return facts


def download(url):
    with urlopen(url, timeout=30) as response:
        require(response.status == 200 and response.url == url, 'unexpected HTTP response or redirect')
        return response.read()


def replay(html, images, d):
    validate_source(d)
    urls = parse_page(html, d)
    require(len(images) == 2, 'expected exactly two selected image payloads')
    decoded = [decode_image(b, row) for b, row in zip(images, d['images'])]
    digest = hashlib.sha256(html).hexdigest()
    return {'schema': 'stoneage.cn2003.katan.visual-replay.r100',
            'contract_sha256': SOURCE_SHA,
            'html': {'bytes': len(html), 'sha256': digest,
                     'equals_initial': len(html) == d['source']['initial_bytes'] and digest == d['source']['initial_sha256']},
            'selected_links': urls,
            'images': [{'url': u, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), **facts}
                       for u, b, facts in zip(urls, images, decoded)],
            'observations': d['observations'], 'boundaries': d['boundaries'],
            'semantic_replay': 'CURRENT_PAGE_LINK_AND_IMAGE_BYTES_VERIFIED_NOT_LIVE_SERVER_EXECUTION'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--html', type=Path)
    p.add_argument('--images', type=Path, nargs=2)
    p.add_argument('--write', type=Path, required=True)
    args = p.parse_args()
    d = validate_source(json.loads(SOURCE.read_text()))
    html = args.html.read_bytes() if args.html else download(d['source']['url'])
    urls = parse_page(html, d)
    payloads = [x.read_bytes() for x in args.images] if args.images else [download(u) for u in urls]
    result = replay(html, payloads, d)
    args.write.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('R100 PASS: two caption-linked NPC/quest images verified; native TW1.0 IDs and server execution remain OPEN')


if __name__ == '__main__':
    main()
