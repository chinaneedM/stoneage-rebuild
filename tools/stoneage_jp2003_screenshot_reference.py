"""One official screenshot index and one exact later-capture GIF, metadata only."""
import argparse
from hashlib import sha256
import io
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen
from PIL import Image
from tools.stoneage_early_content_probe import require

ORIGINAL = 'http://www.hangame.co.jp/publish/sa/game3.asp'
CAPTURE = '20031215093733'
URL = 'https://web.archive.org/web/' + CAPTURE + 'id_/' + ORIGINAL
SOURCE_SHA = 'e2f08e8cb7d5f9469acd158783d343349f31ef1fb4b46a493d00e5441df63a18'
IMAGE_ROOT = 'http://images.hangame.co.jp/_images/game/saj/'
IMAGE_ORIGINAL = IMAGE_ROOT + 'screeshot1.gif'  # Original misspelling retained.
IMAGE_CAPTURE = '20080819022212'
IMAGE_URL = 'https://web.archive.org/web/' + IMAGE_CAPTURE + 'id_/' + IMAGE_ORIGINAL
IMAGE_SHA = '0565913532b59e930958bbb04bb347a349e6667e02304426a6aa2197f48340b6'
REPORT = Path('research/recovered/STONEAGE-JP-OFFICIAL-SCREENSHOT-REFERENCE-R1.json')


def extract_refs(doc):
    doc = re.sub(r'<!--.*?-->', '', doc, flags=re.S)
    doc = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', doc, flags=re.I | re.S)
    refs = []
    for tag in re.findall(r'<img\b[^>]*>', doc, re.I):
        attrs = dict(re.findall(r'([a-z]+)=["\x27]([^"\x27]*)["\x27]', tag, re.I))
        if not attrs.get('src', '').startswith(IMAGE_ROOT + 'screeshot'):
            continue
        require(attrs['src'] == IMAGE_ROOT + 'screeshot' + str(len(refs)+1) + '.gif',
                'Eight original screenshot references must retain order and spelling')
        require((attrs.get('width'), attrs.get('height')) == ('275', '200'), 'Declared screenshot dimensions changed')
        require(not attrs.get('alt') and not attrs.get('title'), 'Uncaptioned reference gained a caption')
        refs.append(attrs['src'])
    require(len(refs) == 8, 'Exactly eight screenshot refs required')
    return refs


def validate_report(o):
    require(len(o['records']) == 8, 'Eight screenshot reference records required')
    r = o['records'][0]; im = r['actual_image']
    require(im['actual_capture'] == IMAGE_CAPTURE and im['sha256'] == IMAGE_SHA
            and im['actual_dimensions'] == [275, 200] and im['frames'] == 1,
            'Exact later image provenance or metadata changed')
    require(im['same_instant_or_same_bytes_as_2003_page_proven'] is False
            and im['native_client_resolution_or_uncropped_frame'] is None,
            'Later web image promoted to same-time source or native resolution')
    require(r['visual_review']['method'] == 'EXACT_HASH_IMAGE_VIEWED_WITH_VIEW_IMAGE'
            and r['visual_review']['reviewed_sha256'] == IMAGE_SHA,
            'Human visual review unbound from exact image bytes')
    require(r['visual_review']['original_map_character_species_ids_or_stat_values'] is None
            and r['visual_review']['login_or_character_creation_screen_proven'] is False,
            'Status screenshot promoted to entity IDs numeric rules or other UI state')
    for r in o['records'][1:]:
        require(r['actual_image'] is None and r['visual_review'] is None,
                'Unacquired screenshot reference promoted to viewed pixels')
    for r in o['records']:
        require(r['caption_as_written'] is None and r['original_client_build_or_runtime_verified'] is False,
                'Uncaptioned reference promoted to named source state or runtime')
    require(o['coverage'] == {'original_index_pages': 1, 'screenshot_references': 8,
                             'actual_images_reacquired_and_reviewed': 1, 'unacquired_references': 7,
                             'new_original_maps_characters_or_game_state_transactions': 0},
            'Screenshot references counted as acquired images or game entities')


def build(page, final, image, image_final):
    require(final == URL and image_final == IMAGE_URL, 'Exact original page/image and captures required')
    require(len(page) == 14113 and sha256(page).hexdigest() == SOURCE_SHA, 'Screenshot index byte pin differs')
    require(len(image) == 46583 and sha256(image).hexdigest() == IMAGE_SHA, 'Screenshot GIF byte pin differs')
    doc = page.decode('cp932', errors='strict')
    require('<title>ストーンエイジ</title>' in doc.lower() and 'スクリーンショット' in doc,
            'Actual title or screenshot section missing')
    refs = extract_refs(doc)
    with Image.open(io.BytesIO(image)) as im:
        require((im.format, im.size, im.n_frames) == ('GIF', (275, 200), 1), 'Exact GIF metadata differs')
    records = []
    for i, ref in enumerate(refs):
        records.append({'record_id': f'jp-official-screenshot-reference:{i+1:02d}', 'collection': 'screens',
                        'entity_type': 'OFFICIAL_WEB_SCREENSHOT_REFERENCE', 'record_revision': 1,
                        'version_profile': 'JAPAN_2003_WEB_INDEX_2008_IMAGE_DISTINCT_CAPTURES',
                        'source_refs': [{'source': ORIGINAL, 'actual_capture': CAPTURE, 'sha256': SOURCE_SHA,
                                         'reference_index': i}],
                        'verification_status': 'WEB_IMAGE_OBSERVED_NOT_EXACT_CLIENT_BUILD' if i == 0 else 'REFERENCE_ONLY_PIXELS_UNACQUIRED',
                        'rights_status': 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
                        'original_image_url': ref, 'html_declared_dimensions': [275, 200],
                        'caption_as_written': None,
                        'actual_image': {'original_url': IMAGE_ORIGINAL, 'strict_replay_url': IMAGE_URL,
                                         'actual_capture': IMAGE_CAPTURE, 'bytes': 46583, 'sha256': IMAGE_SHA,
                                         'format': 'GIF', 'actual_dimensions': [275, 200], 'frames': 1,
                                         'same_instant_or_same_bytes_as_2003_page_proven': False,
                                         'native_client_resolution_or_uncropped_frame': None} if i == 0 else None,
                        'visual_review': {'method': 'EXACT_HASH_IMAGE_VIEWED_WITH_VIEW_IMAGE', 'reviewed_sha256': IMAGE_SHA,
                                          'observed_ui_state': 'FIELD_SCENE_WITH_CHARACTER_STATUS_AND_MAP_WINDOWS',
                                          'observations': ['ISOMETRIC_GRASS_STONE_AND_COAST_FIELD',
                                                           'LEFT_STATUS_PANEL_WITH_PORTRAIT_GAUGES_AND_SMALL_TEXT',
                                                           'UPPER_RIGHT_MAP_PANEL', 'SMALL_FIGURES_IN_FIELD'],
                                          'visible_map_label_as_written': 'サムギルの村',
                                          'original_map_character_species_ids_or_stat_values': None,
                                          'login_or_character_creation_screen_proven': False,
                                          'portrait_equals_static_web_illustration_or_face_editor_asset': None,
                                          'runner_repeats_human_visual_interpretation': False} if i == 0 else None,
                        'original_client_build_or_runtime_verified': False})
    o = {'schema': 'stoneage.jp.official_screenshot_reference.r1', 'date': '2026-10-19',
         'task': 'JP-OFFICIAL-SCREENSHOT-REFERENCE-SOURCE-01',
         'source': {'original_url': ORIGINAL, 'strict_replay_url': URL, 'actual_capture': CAPTURE,
                    'bytes': len(page), 'sha256': SOURCE_SHA, 'encoding': 'CP932_STRICT',
                    'initial_requested_capture': '20031214050618',
                    'actual_title': 'ストーンエイジ', 'actual_visible_section': 'スクリーンショット'},
         'selection': {'portfolio_task': 'OFFICIAL-VERSION-COVERAGE-MATERIAL-REVIEW-10',
                       'authenticated_parent_source_report': 'STONEAGE-JP2003-GAME-FEATURES-R1.json',
                       'edge_evidence': {'original_source': 'http://www.hangame.co.jp/publish/sa/game2.asp',
                                         'actual_capture': '20031214050618',
                                         'original_sha256': '4e92ce95cfb836db9fd78f7b4f64905e60270202d1e2ea0b00cf56b79b6440b0',
                                         'static_literal_target': 'game3.asp',
                                         'label_as_written': 'スクリーンショット',
                                         'javascript_executed': False},
                       'explicit_new_package_not_automatic_gallery_recursion': True,
                       'finite_scope': 'ONE_INDEX_AND_ONLY_FIRST_AUTHENTIC_REFERENCED_IMAGE'},
         'acquisition_history': {'initial_image_requested_capture': CAPTURE,
                                 'image_redirect_actual_capture': IMAGE_CAPTURE,
                                 'remaining_seven_images_not_attempted': True},
         'records': records,
         'coverage': {'original_index_pages': 1, 'screenshot_references': 8,
                      'actual_images_reacquired_and_reviewed': 1, 'unacquired_references': 7,
                      'new_original_maps_characters_or_game_state_transactions': 0},
         'boundaries': {'original_html_or_image_bytes_committed': False,
                        '1999_tw10_cn182_174a_same_build_identity': False,
                        'same_2003_capture_original_ui_layout_recovered': False,
                        'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'},
         'next': 'OFFICIAL-VERSION-REGIONAL-AND-DOMAIN-ROTATION-11'}
    validate_report(o)
    return o


def fetch(url, limit):
    with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 StoneAgeHistoricalEvidence'}), timeout=35) as response:
        return response.read(limit), response.url


def main():
    p = argparse.ArgumentParser(); p.add_argument('--input-page'); p.add_argument('--input-image'); p.add_argument('--output', required=True)
    a = p.parse_args(); require(bool(a.input_page) == bool(a.input_image), 'Both local source objects or neither required')
    page, final = (Path(a.input_page).read_bytes(), URL) if a.input_page else fetch(URL, 150001)
    image, image_final = (Path(a.input_image).read_bytes(), IMAGE_URL) if a.input_image else fetch(IMAGE_URL, 2000001)
    o = build(page, final, image, image_final); payload = json.dumps(o, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    out = Path(a.output); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(payload, encoding='utf-8')
    print('INDEX_SHA256=' + SOURCE_SHA); print('IMAGE_SHA256=' + IMAGE_SHA)
    print('SCREENSHOT_REFS=8 ACTUAL_IMAGES=1 REMAINING_UNACQUIRED=7')
    print('DERIVED_SHA256=' + sha256(payload.encode()).hexdigest())


if __name__ == '__main__': main()
