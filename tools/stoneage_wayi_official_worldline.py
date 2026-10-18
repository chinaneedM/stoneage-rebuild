"""Official2005 world synopsis and bounded22-domain material review."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from PIL import Image

ROOT = 'http://www.wayi.com.tw/stoneage/'
REPORT = 'research/recovered/STONEAGE-WAYI-OFFICIAL-WORLDLINE-R1.json'
REVIEW = 'research/recovered/STONEAGE-CROSS-DOMAIN-MATERIAL-REVIEW-R4.json'
PAGES = {
    'home': ('', '20050615023834', 45669, '4a4a7f0667a8d71b1d37ab0b73712793cf2d7e8a6cd7a7a158a487d060657397'),
    'game01': ('game/game01.asp', '20050614002509', 20444, 'c0a2f96c1d0232eb3f94328481ff512c3efed63daeab912fcc5dd0c397f1ba0d'),
}
PRIOR = 'research/recovered/STONEAGE-CROSS-DOMAIN-MATERIAL-REVIEW-R3.json'
ARCHIVE = 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json'
IMAGE_PINS = {'pic2_1.gif': {'bytes': 9255,
                'final_url': 'https://web.archive.org/web/20060105091436id_/http://www.wayi.com.tw/stoneage/images/game/pic2_1.gif',
                'sha256': '0710dd77a4a6ca362de52da3550bd1b244e31c83b2be4ab00d9de4b64cd92a9f'},
 'pic2_2.gif': {'bytes': 10419,
                'final_url': 'https://web.archive.org/web/20060105095956id_/http://www.wayi.com.tw/stoneage/images/game/pic2_2.gif',
                'sha256': 'e4868c494818ac8bf80f54a0a177a40396b8aff75cf7416603b542813424a196'},
 'pic2_3.gif': {'bytes': 7579,
                'final_url': 'https://web.archive.org/web/20060105093615id_/http://www.wayi.com.tw/stoneage/images/game/pic2_3.gif',
                'sha256': '39c016c22089ad1a6ebdd11a23fd47dcf407f44b940eb926144d16f6cd8f404f'},
 'pic2_4.gif': {'bytes': 11319,
                'final_url': 'https://web.archive.org/web/20060105082234id_/http://www.wayi.com.tw/stoneage/images/game/pic2_4.gif',
                'sha256': '673c751229511e0df2e22f5f268630f29231d594349bfc9fa7ac8732bbc98bc6'},
 'pic2_5.gif': {'bytes': 13571,
                'final_url': 'https://web.archive.org/web/20060105095908id_/http://www.wayi.com.tw/stoneage/images/game/pic2_5.gif',
                'sha256': '08514171ccfd7cc70b38183c8ca2f12e0f99ccd36ff7c31da9fbd4de54a7d6cc'},
 'pic2_6.gif': {'bytes': 8261,
                'final_url': 'https://web.archive.org/web/20060105073350id_/http://www.wayi.com.tw/stoneage/images/game/pic2_6.gif',
                'sha256': 'cc9c950d736460db933e526b0935eb4869e87c8aea5bf079d3d02a48de42eb16'},
 'pic2_7.gif': {'bytes': 8220,
                'final_url': 'https://web.archive.org/web/20060105081854id_/http://www.wayi.com.tw/stoneage/images/game/pic2_7.gif',
                'sha256': 'e1c5ea6587cd2d09e8aff7869aabe2ce39ee2db17b86c900cd63540cc454ca38'},
 'pic2_8.gif': {'bytes': 9984,
                'final_url': 'https://web.archive.org/web/20060105102245id_/http://www.wayi.com.tw/stoneage/images/game/pic2_8.gif',
                'sha256': 'fbf008b46b70bfedf23725eb2dfbd9fe80a271407a17dce5caf6b629a0669399'}}



def require(ok, message):
    if not ok:
        raise ValueError(message)


def compact(s):
    return ' '.join(s.split())


def fingerprint(text):
    return {'characters': len(text), 'sha256': hashlib.sha256(text.encode()).hexdigest()}


def metadata(path, raw=None):
    raw = Path(path).read_bytes() if raw is None else raw
    return {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'git_blob': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}


class Document(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base, self.hidden, self.in_title = base, 0, False
        self.parts, self.links, self.images, self.title = [], [], [], []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        if self.hidden:
            return
        attrs = dict(attrs)
        if tag == 'title':
            self.in_title = True
        if tag in ('br', 'p', 'td', 'tr', 'div'):
            self.parts.append(' ')
        if tag == 'a' and attrs.get('href') and not attrs['href'].startswith(('#', 'javascript:', 'mailto:')):
            self.links.append(urljoin(self.base, attrs['href']))
        if tag == 'img' and attrs.get('src'):
            self.images.append({'original_url': urljoin(self.base, attrs['src']),
                                'html_width': attrs.get('width'), 'html_height': attrs.get('height')})

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.hidden:
            self.hidden -= 1
        elif not self.hidden:
            if tag == 'title':
                self.in_title = False
            if tag in ('p', 'td', 'tr', 'div'):
                self.parts.append(' ')

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)
            if self.in_title:
                self.title.append(data)

    @property
    def text(self):
        return compact(''.join(self.parts))


def parse(text, base):
    d = Document(base)
    d.feed(text)
    d.close()
    return d


def world_contract(document):
    d = parse(document, ROOT + PAGES['game01'][0])
    start, end = '遠古機械文明的消失', '只能等待冒險者前去探訪才能得知'
    require(d.text.count(start) == 1 and d.text.count(end) == 1, 'world synopsis boundaries changed')
    body = d.text.split(start, 1)[1].split(end, 1)[0]
    body = start + body + end
    assertions = ('傳說', '記憶中消失', '精靈王的出現創造了尼斯大陸', '新的文明',
                  '後來發現的伊甸大陸', '自己的文明', '特有的文化', '海底冒險',
                  '越是前往海的深處越是覺得冰冷', '冰壁缺口', '不被外界所知',
                  '機械文明的遺跡還是另一個全新的文明？')
    require(all(x in body for x in assertions), 'missing or altered narrative assertion')
    groups = re.findall(r'\((\d\.\d(?:、\d\.\d)*)\)', body)
    require(groups == ['1.0、2.0、2.5', '3.0、4.0', '5.0、7.0', '6.0', '8.0'], 'publisher version-group order changed')
    require('尼斯大陸(' + groups[0] + ')' in body and '伊甸大陸(' + groups[1] + ')' in body, 'version labels attached to different continent')
    expected = [ROOT + 'game/game01_0' + str(i) + '.asp' for i in range(1, 5)]
    actual = [u for u in d.links if re.fullmatch(re.escape(ROOT) + r'game/game01_\d\d\.asp', u)]
    require(actual == expected, 'intro detail edges changed')
    images = [x for x in d.images if re.fullmatch(re.escape(ROOT) + r'images/game/pic2_\d\.gif', x['original_url'])]
    require([x['original_url'].rsplit('/', 1)[-1] for x in images] == [f'pic2_{i}.gif' for i in range(1, 10)], 'nine image-slice references changed')
    rows = [
        ('NIS_CONTINENT', '尼斯大陸', ['1.0', '2.0', '2.5'], 'SPIRIT_KING_CREATES_CONTINENT_AND_NEW_CIVILIZATION_FOLLOWS'),
        ('EDEN_CONTINENT', '伊甸大陸', ['3.0', '4.0'], 'LATER_DISCOVERY_AND_OWN_CIVILIZATION'),
        ('DISTINCT_CULTURES', None, ['5.0', '7.0'], 'CIVILIZATIONS_AND_DISTINCT_CULTURES_EMERGE'),
        ('UNDERSEA_EXPLORATION', None, ['6.0'], 'PEOPLE_EXPLORE_UNDERSEA_AND_DEEPER_WATER_IS_COLDER'),
        ('LOST_WORLD', '失落的世界', ['8.0'], 'ICE_WALL_GAP_LEADS_TO_A_WORLD_UNKNOWN_OUTSIDE'),
    ]
    return {'evidence_kind': 'TAIWAN_OPERATOR_2005_RETROSPECTIVE_WORLD_SYNOPSIS',
            'synopsis_fingerprint': fingerprint(body),
            'version_groups_in_source_order': [{'source_order': i, 'topic': k, 'name_as_written': name, 'versions_as_written': versions, 'narrative_assertion': claim} for i, (k, name, versions, claim) in enumerate(rows)],
            'named_figure': {'label_as_written': '精靈王', 'role_described': 'CREATOR_OF_NIS_CONTINENT', 'npc_master_id': None},
            'mechanical_civilization': {'past_disappearance_described': True, 'legends_and_fading_memory_described': True, 'date': None, 'spirit_king_destroyed_it_proven': False},
            'journey_links': [{'from': 'UNDERSEA_EXPLORATION', 'to': 'ICE_WALL_GAP', 'basis': 'NARRATIVE_DISCOVERY_SEQUENCE'}, {'from': 'ICE_WALL_GAP', 'to': 'LOST_WORLD', 'basis': 'NARRATIVE_DISCOVERY_SEQUENCE'}],
            'lost_world_identity': {'operator_leaves_question_open': True, 'alternatives_as_paraphrase': ['RUINS_OF_MECHANICAL_CIVILIZATION', 'ANOTHER_NEW_CIVILIZATION'], 'chosen_answer': None},
            'chronology': {'presentation_order_preserved': True, 'group_5_and_7_precedes_6_in_source': True, 'presentation_order_is_numeric_release_order': False, 'fictional_calendar_years_given': False, 'real_release_dates_derived_from_synopsis': False},
            'detail_links': [{'url': x, 'queried': False, 'topic_from_number_assumed': False} for x in actual],
            'image_slice_references': [{**x, 'pixels_acquired': False, 'actual_dimensions': None, 'visual_content_verified': False} for x in images],
            'literal_version_labels_are_same_build_jss1999_or_tw10_identity': False}


def image_contract(raw, final, original):
    name = original.rsplit('/', 1)[-1]
    require(name in IMAGE_PINS and original == ROOT + 'images/game/' + name, 'unqualified image reference')
    pin = IMAGE_PINS[name]
    require(final == pin['final_url'], 'image original URL or actual capture changed')
    require(len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'], 'image source bytes changed')
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        require(im.format == 'GIF', 'not original GIF pixels')
        dimensions = list(im.size)
        frames = im.n_frames
    return {'pixels_acquired': True, 'final_url': final, 'actual_capture': re.search(r'/web/(\d{14})id_/', final).group(1),
            'bytes': len(raw), 'sha256': pin['sha256'], 'format': 'GIF', 'actual_dimensions': dimensions,
            'frames': frames, 'visual_content_verified': True, 'manual_visual_review_basis': 'EXACT_EIGHT_SOURCE_SLICES_INDIVIDUALLY_VIEWED'}


def build(acquisitions, image_acquisitions=None):
    documents, sources = {}, {}
    for key, (path, capture, size, digest) in PAGES.items():
        raw, final = acquisitions[key]
        original = ROOT + path
        expected = f'https://web.archive.org/web/{capture}id_/' + original
        require(final == expected, 'actual capture or original URL changed')
        require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, 'official source bytes changed')
        documents[key] = parse(raw.decode('big5', errors='strict'), original)
        sources[key] = {'original_url': original, 'actual_capture': capture, 'final_url': final, 'bytes': size, 'sha256': digest, 'codec': 'big5'}
    require(ROOT + PAGES['game01'][0] in documents['home'].links, 'intro not linked from authenticated home')
    require('全星系更新為8.0版本' in documents['home'].text, 'official home context changed')
    raw = acquisitions['game01'][0]
    facts = world_contract(raw.decode('big5', errors='strict'))
    image_acquisitions = image_acquisitions or {}
    require(set(image_acquisitions) == {ROOT + 'images/game/' + n for n in IMAGE_PINS}, 'qualified image coverage changed')
    qualified = 0
    for row in facts['image_slice_references']:
        original = row['original_url']
        if original in image_acquisitions:
            row.update(image_contract(*image_acquisitions[original], original))
            require(row['actual_dimensions'] == [int(row['html_width']), int(row['html_height'])], 'actual GIF size differs from HTML; requalify')
            qualified += 1
        else:
            row.update(status='UNOBTAINED_HTTP404_IN_BOUNDED_ATTEMPT', source_absence_established=False)
    require(qualified == 8, 'expected eight qualified slices')
    return {'schema': 'stoneage.wayi.official_worldline.r1', 'source_pages': sources,
            'source_count': {'reacquired_previously_authenticated_pages': 1, 'newly_acquired_world_intro_pages': 1},
            'site_title_as_written': compact(''.join(documents['game01'].title)), 'site_title_is_exact_client_build': False,
            'qualified_edge': {'from': sources['home']['original_url'], 'to': sources['game01']['original_url'], 'kind': 'ACTUAL_HTML_HREF', 'click_or_script_executed': False},
            'world': facts,
            'visual_summary': {'qualified_slices': 8, 'unobtained_slices': 1, 'html_grid_rows': 3, 'html_grid_columns': 3,
                'complete_artwork_acquired_or_reconstructed': False, 'visual_observations': ['ILLUSTRATED_HUMAN_FIGURES', 'PART_OF_YELLOW_HORNED_CREATURE', 'ICY_OR_SNOWY_BACKGROUND'],
                'named_character_or_pet_identification': None, 'actual_gameplay_screenshot_or_playable_map_proven': False,
                'same_instant_as_2005_html_proven': False, 'image_capture_year': 2006},
            'boundaries': {'operator_story_attribution_is_not_real_ancient_history': True, 'original_release_or_deployment_witnessed': False,
                           'jss1999_or_tw10_same_build_promoted': False, 'all_versions_share_one_universal_canon_proven': False,
                           'complete_npc_quest_scripts_or_pet_roster_recovered': False, 'flash_activex_or_binaries_acquired': False,
                           'original_html_or_assets_retained_in_git': False, 'stage_a_family_status_changed': False, 'stage_b_production': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'}}


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir', type=Path)
    parser.add_argument('--image-dir', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    acquisitions = {}
    for key, (path, capture, _, _) in PAGES.items():
        url = f'https://web.archive.org/web/{capture}id_/' + ROOT + path
        if args.input_dir:
            raw = (args.input_dir / ('stoneage-wayi-' + key + '.raw')).read_bytes()
        else:
            with urlopen(Request(url, headers={'User-Agent': 'StoneAge-Historical-Research/1.0'}), timeout=60) as response:
                raw, url = response.read(), response.url
        acquisitions[key] = raw, url
    def acquire_image(name):
        original = ROOT + 'images/game/' + name
        final = IMAGE_PINS[name]['final_url']
        if args.image_dir:
            raw = (args.image_dir / name).read_bytes()
        else:
            with urlopen(Request(final, headers={'User-Agent': 'StoneAge-Historical-Research/1.0'}), timeout=60) as response:
                raw, final = response.read(1024 * 1024 + 1), response.url
                require(len(raw) <= 1024 * 1024, 'image outside byte bound')
        return original, (raw, final)
    with ThreadPoolExecutor(max_workers=3) as pool:
        image_acquisitions = dict(pool.map(acquire_image, IMAGE_PINS))
    result = build(acquisitions, image_acquisitions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(dump(result), encoding='utf-8')
    print(json.dumps({'new_world_page': 1, 'reacquired_home': 1, 'version_groups': 5, 'version_labels': 9, 'image_slices_acquired': 8, 'image_slices_unobtained': 1, 'lost_world_answer_known': False}))


if __name__ == '__main__':
    main()
