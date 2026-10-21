"""Three new web-image supplements and one known control; no game species or sprite IDs."""
import argparse
import hashlib
import io
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin
from PIL import Image
from tools.stoneage_cn2003_group2_manor_report import Visible
from tools.stoneage_cn20_recordpoint_source import fetch

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-CN20-PET-VISUAL-BATCH'
REPORT = ROOT / ('research/recovered/' + STEM + '-SOURCE-R1.json')
PAGE_ORIGINAL = 'http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet.asp'
PAGE_URL = 'https://web.archive.org/web/20011204194619id_/' + PAGE_ORIGINAL
PARENT_PATHS = [
    'research/recovered/STONEAGE-WAEI-CN20-NEW-PET-CATALOG-FIRST-PAGE-R1.json',
    'research/recovered/STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-R1.json',
    'research/recovered/STONEAGE-WAEI-CN20-AMIDUO-VISUAL-REFERENCE-R1.json',
]
POSITIONS = (1, 4, 7, 40)
PROFILE = 'CN_WAEI_PAGE_2_0_2001_SEPARATE_WEB_IMAGE_CAPTURES_NOT_EXACT_BUILD'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git_blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def visible(s):
    p = Visible(); p.feed(s)
    return re.sub(r'\s+', '', ''.join(p.parts))


def cells(raw):
    t = raw.decode('gb18030', errors='strict')
    require('<title>石器时代2.0</title>' in t and t.count('新 增 宠 物') == 1, 'Page identity changed')
    section = t.split('新 增 宠 物', 1)[1].split('<span class="p12b">', 1)[0]
    tables = re.findall(r'<table\b[^>]*>(.*?)</table>', section, re.I | re.S)
    require(len(tables) == 2 and visible(tables[0]) == '1-4041-8081-104', 'Catalog range changed')
    nav = re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', tables[0], re.I | re.S)
    require([(a, visible(b)) for a, b in nav] == [('new_pet1.asp', '41-80'), ('new_pet2.asp', '81-104')], 'Qualified pagination links changed')
    rows = re.findall(r'<tr\b[^>]*>(.*?)</tr>', tables[1], re.I | re.S)
    leaf = [re.findall(r'<td\b[^>]*>(.*?)</td>', r, re.I | re.S) for r in rows]
    require([len(r) for r in leaf] == [5] * 8, '8 by 5 source grid changed')
    return [c for row in leaf for c in row]


def extract(raw):
    leaf = cells(raw); selected = []
    for ordinal in POSITIONS:
        cell = leaf[ordinal - 1]
        imgs = re.findall(r'<img\b([^>]+)>', cell, re.I)
        require(len(imgs) == 1, 'One source image per selected cell required')
        attrs = dict(re.findall(r'(\w+)\s*=\s*"([^"]*)"', imgs[0]))
        require('src' in attrs and ('width' in attrs) == ('height' in attrs), 'Actual src and paired declared dimensions required')
        label = visible(cell); placeholder = re.fullmatch(r'\?+\d*', label) is not None
        selected.append({'ordinal': ordinal, 'row': (ordinal - 1) // 5 + 1, 'column': (ordinal - 1) % 5 + 1,
                         'display_label_as_written': label, 'name_as_written': None if placeholder else label,
                         'label_status': 'UNRESOLVED_PLACEHOLDER' if placeholder else 'NAMED_ON_WEB_PAGE',
                         'relative_src_as_written': attrs['src'], 'original_url_from_cell': urljoin(PAGE_ORIGINAL, attrs['src']),
                         'html_declared_dimensions': [int(attrs['width']), int(attrs['height'])] if 'width' in attrs else None})
    return {'selected_cells': selected, 'page_grid_positions': 40, 'selected_count': 4,
            'selected_core_sha256': sha(json.dumps(selected, ensure_ascii=False, separators=(',', ':')).encode()),
            'operator_hosted_guide_named_author_verified': False, 'publication_date': None, 'exact_client_build': None}


# Actual selected cell mutations; semantic comparison excludes every digest field.
HTML_MUTATIONS = (
    (1, 'placeholder-remains-literal', '???', '乌力'),
    (4, 'placeholder-suffix', '??2', '??5'),
    (40, 'named-label', '呼波波', '呼波'),
    (1, 'neighbor-image', '6.JPG', '5.JPG'),
    (4, 'path-case', '2.jpg', '2.JPG'),
    (40, 'last-image', '40.JPG', '39.JPG'),
    (1, 'declared-width', 'width="83"', 'width="84"'),
    (1, 'declared-height', 'height="90"', 'height="91"'),
    (7, 'undeclared-dimensions', 'border="0"', 'border="0" width="83" height="90"'),
    (4, 'missing-dimensions', 'width="83" height="90"', ''),
    (7, 'control-label', '阿米朵', '艾尔蛙'),
    (4, 'control-path-swap', '2.jpg', '7.JPG'),
)


def audit(raw, expected):
    t = raw.decode('gb18030'); leaf = cells(raw); out = []
    cases = []
    for ordinal, label, old, new in HTML_MUTATIONS:
        original = leaf[ordinal - 1]; require(old in original, 'Actual mutation anchor missing: ' + label)
        require(t.count(original) == 1, 'Selected cell not unique')
        cases.append((label, t.replace(original, original.replace(old, new), 1).encode('gb18030')))
    cases.extend([('page-heading', t.replace('新 增 宠 物', '宠 物 总 数').encode('gb18030')),
                  ('pagination-link', t.replace('href="new_pet1.asp"', 'href="missing.asp"').encode('gb18030'))])
    for label, changed in cases:
        try:
            x = extract(changed)
            rejected = {k: v for k, v in x.items() if k != 'selected_core_sha256'} != {k: v for k, v in expected.items() if k != 'selected_core_sha256'}
        except ValueError:
            rejected = True
        require(rejected, 'Source semantic mutation accepted: ' + label)
        out.append({'case': label, 'input_sha256': sha(changed), 'rejected_without_digest_gate': True})
    require(extract(raw + b'<script>outer only</script>') == expected, 'Outer script positive failed')
    return {'real_html_mutations': out, 'outer_script_positive': True}


def image_metadata(b):
    with Image.open(io.BytesIO(b)) as im:
        im.load()
        return {'format': im.format, 'dimensions': list(im.size), 'mode': im.mode,
                'frames_in_this_file': getattr(im, 'n_frames', 1), 'full_pixels_decoded': True}


def validate(r):
    local = json.loads((ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_text())
    require(r['schema'] == 'stoneage.cn20_pet_visual_batch.source.r1' and r['extracted'] == local['extracted'], 'Source semantics changed')
    require(r['source']['url'] == PAGE_URL and r['source']['capture_timestamp'] == '20011204194619', 'Body identity changed')
    require(r['source']['bytes'] == 69317 and r['source']['sha256'] == '561950fd7bba41e7d39f4a781a671e11e175c7fe08dd1b5481fdf1fd23ba351b', 'Known page pin changed')
    require([x['path'] for x in r['parents']] == PARENT_PATHS, 'Immutable parents changed')
    parents = []
    for pin in r['parents']:
        b = (ROOT / pin['path']).read_bytes()
        require(len(b) == pin['bytes'] and sha(b) == pin['sha256'] and git_blob(b) == pin['git_blob'], 'Parent byte identity changed')
        parents.append(json.loads(b))
    require(r['images'] == local['images'] and len(r['images']) == 4, 'Image/inspection semantics changed')
    require(len(r['records']) == 3 and len({x['record_id'] for x in r['records']}) == 3, 'Exactly three new visual supplements required')
    for cell, image in zip(r['extracted']['selected_cells'], r['images']):
        n = cell['ordinal']; old = parents[0]['records'][n - 1]; compiled = parents[1]['records'][n - 1]
        require(old == compiled and old['source_position'] == {k: cell[k] for k in ('ordinal', 'row', 'column')}, 'Parent row/position identity changed')
        require(old['display_label_as_written'] == cell['display_label_as_written'] and old['name_as_written'] == cell['name_as_written'], 'Placeholder/name changed')
        require(old['image_reference']['relative_src_as_written'] == cell['relative_src_as_written'] and old['image_reference']['html_declared_dimensions'] == cell['html_declared_dimensions'], 'Source cell association changed')
        require(old['image_reference']['pixels_requested'] is False, 'Historical unacquired state rewritten')
        require(image['ordinal'] == n and image['requested_from_page_url'] == PAGE_URL.rsplit('/', 1)[0] + '/' + cell['relative_src_as_written'], 'Actual initial image URL changed')
        require(image['metadata'] == {'format': 'JPEG', 'dimensions': [83, 90], 'mode': 'RGB', 'frames_in_this_file': 1, 'full_pixels_decoded': True}, 'Actual pixel metadata changed')
        require(image['manual_inspection']['exact_image_sha256'] == image['sha256'] and image['manual_inspection']['performed_by'] == 'ASSISTANT_VIEW_IMAGE_ORIGINAL_PIXELS' and image['manual_inspection']['ci_repeats_human_inspection'] is False, 'Manual/CI observation conflated')
        if n == 7:
            known = parents[2]['records'][0]['acquired_image']
            require(image['strict_replay_url'] == known['strict_replay_url'] and image['sha256'] == known['sha256'] and image['bytes'] == known['bytes'], 'Existing Amiduo control changed')
        else:
            row = next(x for x in r['records'] if x['ordinal'] == n)
            require(row['source_cell'] == cell and row['image_sha256'] == image['sha256'] and row['version_profile'] == PROFILE, 'New supplement association changed')
            require(row['original_game_pet_id_stats_alias_or_animation'] is None and row['new_original_game_entity'] is False, 'Game entity promoted')
    require(r['coverage'] == {'finite_catalog_positions': 104, 'new_image_references_acquired': 3, 'previously_acquired_replayed_control': 1, 'acquired_disjoint_references_after_supplement': 4, 'remaining_image_references_without_acquired_pixels': 100, 'unresolved_placeholders_still': 6, 'newly_resolved_names': 0, 'new_original_game_entities': 0, 'parent_historical_reports_rewritten': False}, 'Coverage or history promoted')
    require(all(x is False for x in r['unproven'].values()), 'Unsupported conclusion promoted')
    require(r['status'] == {'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'} and r['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-53', 'Stage/queue changed')


def check_image(pin, b):
    require(len(b) == pin['bytes'] and sha(b) == pin['sha256'], 'Exact image bytes changed')
    require(image_metadata(b) == pin['metadata'], 'Actual full image decode differs')


def replay(r, raw, pictures):
    validate(r); x = extract(raw)
    require(x == r['extracted'] and len(raw) == r['source']['bytes'] and sha(raw) == r['source']['sha256'], 'Actual source changed')
    require(len(pictures) == 4, 'Three new images plus one known control required')
    negatives = []
    for pin, b in zip(r['images'], pictures):
        check_image(pin, b)
        changed = b[:-1] + bytes([b[-1] ^ 1])
        try:
            check_image(pin, changed)
        except ValueError:
            pass
        else:
            raise ValueError('Image byte mutation accepted')
        negatives.append({'ordinal': pin['ordinal'], 'input_sha256': sha(changed), 'exact_byte_mutation_rejected': True})
    return {'schema': 'stoneage.cn20_pet_visual_batch.derived_replay.r1', 'http_bytes': len(raw), 'http_sha256': sha(raw),
            'extracted': x, 'images': r['images'], 'audit': {**audit(raw, x), 'real_image_byte_mutations': negatives},
            'coverage': r['coverage'], 'raw_html_or_images_in_output': False, 'original_game_executed': False}


def main():
    p = argparse.ArgumentParser(); p.add_argument('--fetch', action='store_true', required=True); p.add_argument('--output', type=Path, required=True); a = p.parse_args()
    r = json.loads(REPORT.read_text())
    with ThreadPoolExecutor(max_workers=5) as pool:
        bs = list(pool.map(fetch, [PAGE_URL] + [im['strict_replay_url'] for im in r['images']]))
    out = replay(r, bs[0], bs[1:]); a.output.parent.mkdir(parents=True, exist_ok=True); a.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'success': True, 'html_bytes': len(bs[0]), 'image_bytes': [len(b) for b in bs[1:]], 'new_images': 3, 'known_control': 1, 'html_mutations': 14, 'image_mutations': 4}))


if __name__ == '__main__':
    main()
