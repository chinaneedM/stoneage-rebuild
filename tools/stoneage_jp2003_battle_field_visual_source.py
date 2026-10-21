"""A finite current-web screenshot witness, explicitly labelled development material."""
import argparse
import hashlib
import io
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-JP2003-BATTLE-FIELD-VISUAL-SOURCE-R1.json'
CUSTODY = ROOT / 'research/recovered/STONEAGE-JP2003-BATTLE-FIELD-VISUAL-CUSTODY-R1.json'
BASE = 'https://www.4gamer.net/store/shots/stoneage/'
URLS = ['https://www.4gamer.net/DataContents/game/1377.html', BASE + 'index.html',
        BASE + 'pages/image0000.html', BASE + 'pages/image0001.html',
        BASE + 'images/image0000.jpg', BASE + 'images/image0001.jpg']


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text, self.links, self.images, self.pairs = [], [], [], []
        self.href, self.hidden = None, 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style', 'iframe', 'noscript'):
            self.hidden += 1
        if self.hidden:
            return
        if tag == 'a':
            self.href = attrs.get('href')
            self.links.append(self.href)
        if tag == 'img':
            self.images.append(attrs)
            if self.href:
                self.pairs.append({'href': self.href, 'src': attrs.get('src'), 'alt': attrs.get('alt')})

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'iframe', 'noscript') and self.hidden:
            self.hidden -= 1
        if tag == 'a':
            self.href = None

    def handle_data(self, data):
        if not self.hidden:
            self.text.append(data)


def page(raw, encoding='cp932'):
    p = Page()
    p.feed(raw.decode(encoding, errors='strict'))
    return p, re.sub(r'\s+', '', ''.join(p.text))


def publisher(raw):
    p, text = page(raw, 'euc_jp')
    require('ストーンエイジのScreenshots集をUp' in text and '2003/12/1220:20' in text,
            'Dated gallery announcement missing')
    require('合計40点近く' in text, 'Approximate count wording changed')
    links = [u for u in p.links if u and 'store/shots/stoneage/index.html' in u]
    require(bool(links), 'Real gallery link absent')
    return {'announcement_label': '2003/12/12 20:20', 'time_zone': None,
            'gallery_links_as_written': links, 'claimed_image_count': 'NEAR_40_NOT_EXACT',
            'same_day_client_download_claim_not_execution': True}


def gallery(raw):
    p, text = page(raw)
    for token in ('ストーンエイジ', '1/3ページ', '12thDec.2003', '画面は開発中のものです', 'ProducedbyBOTHTEC'):
        require(token in text, 'Gallery date/development/pagination context changed: ' + token)
    rows = [r for r in p.pairs if (r['href'] or '').startswith('pages/image')]
    require(len(rows) == 15, 'First-page reference coverage changed')
    for i, row in enumerate(rows):
        stem = 'image' + str(i).zfill(4)
        require(row == {'href': 'pages/' + stem + '.html', 'src': 'thumbnails/' + stem + '.jpg', 'alt': stem},
                'Thumbnail-wrapper binding changed')
    require(p.links.count('index_2.html') == 1, 'Next gallery page reference changed')
    return {'gallery_date_label': '12th Dec. 2003', 'page_index': 1, 'declared_pages': 3,
            'development_notice': True, 'actual_image_capture_date': None,
            'reference_rows': rows, 'later_gallery_pages_retrieved': False,
            'copyright_label': '(C)1999 DigiPark Inc. All Rights Reserved. Produced by BOTHTEC'}


def wrapper(raw, ordinal):
    p, text = page(raw)
    require('ストーンエイジ' in text, 'Wrapper title context changed')
    images = [r for r in p.images if (r.get('src') or '').startswith('../images/image')]
    stem = 'image' + str(ordinal).zfill(4)
    require(len(images) == 1 and images[0].get('src') == '../images/' + stem + '.jpg'
            and images[0].get('alt') == stem, 'Actual full image reference changed')
    return {'ordinal': ordinal, 'image_src_as_written': images[0]['src'],
            'html_width_declaration': images[0].get('width'), 'html_height_declaration': images[0].get('height'),
            'javascript_executed': False}


def image_metadata(raw):
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        return {'bytes': len(raw), 'sha256': sha(raw), 'format': im.format,
                'width': im.width, 'height': im.height, 'mode': im.mode,
                'frames': getattr(im, 'n_frames', 1), 'fully_decoded': True}


def extract(raws):
    require(len(raws) == 6, 'Exactly four HTML objects and two images required')
    return {'publisher': publisher(raws[0]), 'gallery': gallery(raws[1]),
            'wrappers': [wrapper(raws[2], 0), wrapper(raws[3], 1)],
            'images': [image_metadata(raws[4]), image_metadata(raws[5])]}


def verify(expected, raws):
    require(extract(raws) == expected, 'Source bindings or reviewed image bytes changed')


def check_catalog(catalog, extracted):
    rows = catalog['records']
    require(len(rows) == 15 and len({r['record_id'] for r in rows}) == 15, 'Catalog coverage/identity changed')
    for i, row in enumerate(rows):
        required = {'record_id', 'entity_type', 'version_profile', 'source_refs',
                    'verification_status', 'rights_status', 'record_revision'}
        require(required <= set(row), 'Archive metadata missing')
        require(row['version_profile'] == 'JP_BOTHTEC_2003_GALLERY_DEVELOPMENT_BUILD_UNVERIFIED',
                'Version/source identity promoted or merged')
        require(row['source_refs'] == (['G1', 'W' + str(i + 1), 'I' + str(i + 1)] if i < 2 else ['G1']),
                'Per-record source custody missing')
        require(row['gallery_reference'] == extracted['gallery']['reference_rows'][i], 'Catalog source reference changed')
        require(row['collection'] == 'screens' and row['game_ids'] is None, 'Research record is not a game master')
        require(row['development_notice'] is True and row['exact_build_verified'] is False,
                'Development material promoted to deployed build')
        require(row['rights_status'] == 'RESEARCH_METADATA_NOT_RELEASE_APPROVED', 'Asset rights silently approved')
        if i < 2:
            require(row['acquired_image'] is not None and row['manual_observation'] is not None,
                    'Reviewed image evidence missing')
            require(row['acquired_image'] == {'url': URLS[4 + i], **extracted['images'][i]},
                    'Reviewed pixels attached to wrong gallery position')
            require(row['manual_observation']['reviewed_image_sha256'] == extracted['images'][i]['sha256'],
                    'Visual judgment detached from reviewed image bytes')
        else:
            require(row['acquired_image'] is None and row['manual_observation'] is None,
                    'Unrequested image silently acquired or interpreted')
        require(row['original_native_resolution'] is None and row['image_capture_date'] is None,
                'Web dimensions or gallery label became native resolution/capture date')


def verify_custody(receipt, root):
    paths = {row['path'] for row in receipt['permanent_derived_files']}
    stem = 'research/recovered/STONEAGE-JP2003-BATTLE-FIELD-VISUAL-'
    require({stem + 'SOURCE-R1.json', stem + 'CI-CANDIDATE-R1.json', stem + 'CI-MAIN-R1.json'} <= paths,
            'Permanent source/dual replay custody incomplete')
    require(receipt['source_scope']['original_runtime_executed'] is False, 'Custody promoted to game execution')
    for row in receipt['permanent_derived_files']:
        raw = (root / row['path']).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()
        require(len(raw) == row['bytes'] and sha(raw) == row['sha256'] and blob == row['git_blob'],
                'Permanent derived evidence changed: ' + row['path'])


def audit(expected, raws):
    mutations = [(0, '2003/12/12 20:20', '2003/12/13 20:20', 'announcement-date'),
                 (0, '合計40点近く', '合計40点ちょうど', 'approximate-count'),
                 (1, '画面は開発中のものです', '画面は正式版のものです', 'development-notice'),
                 (1, '12th Dec. 2003', '12th Dec. 2004', 'gallery-date'),
                 (1, 'pages/image0000.html', 'pages/image0001.html', 'wrapper-binding'),
                 (1, 'thumbnails/image0000.jpg', 'thumbnails/image0001.jpg', 'thumbnail-binding'),
                 (2, '../images/image0000.jpg', '../images/image0001.jpg', 'full-image-binding')]
    cases = []
    for page_no, old, new, label in mutations:
        encoding = 'euc_jp' if page_no == 0 else 'cp932'
        before, after = old.encode(encoding), new.encode(encoding)
        require(before in raws[page_no], 'Real mutation anchor absent: ' + label)
        changed = list(raws)
        changed[page_no] = changed[page_no].replace(before, after, 1)
        try:
            verify(expected, changed)
        except (ValueError, UnicodeError):
            cases.append({'case': label, 'rejected': True, 'input_sha256': sha(changed[page_no])})
        else:
            raise ValueError('Real HTML mutation accepted: ' + label)
    changed = list(raws)
    changed[4], changed[5] = changed[5], changed[4]
    try:
        verify(expected, changed)
    except ValueError:
        cases.append({'case': 'swap-two-valid-jpeg-responses', 'rejected': True})
    else:
        raise ValueError('Wrong reviewed image binding accepted')
    positive = list(raws)
    positive[0] += b'<script>peripheral only</script>'
    verify(expected, positive)
    return {'real_input_mutations': cases, 'peripheral_script_positive': True,
            'html_digest_gate_used': False, 'human_visual_review_reexecuted': False}


def main():
    p = argparse.ArgumentParser()
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument('--fetch', action='store_true')
    source.add_argument('--inputs', nargs=6, type=Path)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    report = json.loads(REPORT.read_text())
    verify_custody(json.loads(CUSTODY.read_text()), ROOT)
    check_catalog(report['catalog'], report['extracted'])
    raws = []
    if args.fetch:
        for url in URLS:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40) as r:
                require(r.status == 200 and r.geturl() == url, 'Source HTTP status or redirect changed')
                raw = r.read(2000001)
                require(len(raw) <= 2000000, 'Source oversized')
                raws.append(raw)
    else:
        raws = [p.read_bytes() for p in args.inputs]
    verify(report['extracted'], raws)
    result = {'schema': 'stoneage.jp2003_battle_field_visual.derived_replay.r1',
              'http_inputs': [{'url': url, 'bytes': len(raw), 'sha256': sha(raw)} for url, raw in zip(URLS, raws)],
              'extracted': extract(raws), 'catalog': report['catalog'], 'audit': audit(report['extracted'], raws),
              'original_assets_in_output': False, 'original_runtime_executed': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'ok': True, 'references': 15, 'images': 2, 'mutations': len(result['audit']['real_input_mutations'])}))


if __name__ == '__main__':
    main()
