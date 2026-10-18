"""One authenticated official ice-region page; preserve caption-name conflicts."""
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
from tools.stoneage_wayi_official_worldline import ROOT, compact, dump, fingerprint, metadata, parse, require

PREVIOUS = 'research/recovered/STONEAGE-WAYI-OFFICIAL-WORLDLINE-R1.json'
PREVIOUS_SHA = '619c2b931174058b87eb97631beb11a995c41fedb26010a94c42e9cc54aa785b'
REPORT = 'research/recovered/STONEAGE-WAYI-OFFICIAL-ICE-REGION-R1.json'
ARCHIVE = 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json'
ORIGINAL = ROOT + 'game/game01_01.asp'
CAPTURE = '20050614003328'
URL = f'https://web.archive.org/web/{CAPTURE}id_/' + ORIGINAL
SHA = 'f7e10861dd9f8ee3bef19c46863c7bc818d17635ffecab41b0189c63ff2b234c'
MAP_NAMES = ('瑞爾亞斯之都', '瑞爾亞斯莊園', '漩渦通道', '深海通道', '淺海通道', '淺冰通道', '冰顫通道', '冰封通道', '無息之境', '流冰回廊', '沉睡洞窟', '黃泉之境')
CAPTIONS = (
    ('pic3.jpg', '冰顫通道其一：', 'ICE_PASSAGE_SAMPLE'),
    ('pic3-3.jpg', '薩爾亞斯之都-議會廳內部：', 'COUNCIL_HALL_INTERIOR'),
    ('pic3-1.jpg', '薩爾亞斯之都-24小時便利商店：', 'CONVENIENCE_STORE'),
    ('pic3-4.jpg', '瑞爾亞斯之都-莊園專賣店：', 'MANOR_SPECIALTY_SHOP'),
    ('pic3-2.jpg', '薩爾亞斯之都-訓練所：', 'TRAINING_FACILITY'),
    ('pic3-5.jpg', '瑞爾亞斯之都-武器店：', 'WEAPON_SHOP'),
)
IMAGE_PINS = {'pic3-1.jpg': {'bytes': 16212,
                'final_url': 'https://web.archive.org/web/20060105093929id_/http://www.wayi.com.tw/stoneage/images/game/pic3-1.jpg',
                'sha256': '7c63f9926eaa6c386feca2037398dccd6e9956c56ed1b9c5f666420b27c135dc'},
 'pic3-2.jpg': {'bytes': 14613,
                'final_url': 'https://web.archive.org/web/20060105102053id_/http://www.wayi.com.tw/stoneage/images/game/pic3-2.jpg',
                'sha256': '762f937ed38b5ed02ec19bb31a878adf970a30d65060cc0009055575e00d1e99'},
 'pic3-3.jpg': {'bytes': 19109,
                'final_url': 'https://web.archive.org/web/20060105093954id_/http://www.wayi.com.tw/stoneage/images/game/pic3-3.jpg',
                'sha256': 'd934093ae3ea7a1e0e2bbb950f7b79e573d8d617342ea2aa698e7a1ea9854e56'},
 'pic3-4.jpg': {'bytes': 16292,
                'final_url': 'https://web.archive.org/web/20060105093146id_/http://www.wayi.com.tw/stoneage/images/game/pic3-4.jpg',
                'sha256': '97ac98a40f58a2ba64f83ce718e5e787bcbd416bca3a8264bdfa7ac54e48139a'},
 'pic3-5.jpg': {'bytes': 16638,
                'final_url': 'https://web.archive.org/web/20060105091411id_/http://www.wayi.com.tw/stoneage/images/game/pic3-5.jpg',
                'sha256': '872e00e2a1283fa6dc8f447c053775244bad02f3260b70b38cf69665321ee9a6'},
 'pic3.jpg': {'bytes': 14212,
              'final_url': 'https://web.archive.org/web/20060105082058id_/http://www.wayi.com.tw/stoneage/images/game/pic3.jpg',
              'sha256': '803fbccf687afa1bd46db8cdceaad56fe9fb5f994b871bf3f723fe6dc04f7775'}}
VISUALS = {
    'pic3.jpg': ['CYAN_ICE_CAVE_AND_ICICLES', 'TOP_GREEN_ICON_BAR', 'OVERLAPPING_HUMAN_LIKE_AND_YELLOW_CREATURE_SPRITES'],
    'pic3-3.jpg': ['GREY_TILED_INTERIOR_WITH_TABLES_OR_SEATS', 'GOLDEN_ORNAMENTS', 'CHARACTER_SPRITES_AND_TOP_GREEN_ICON_BAR'],
    'pic3-1.jpg': ['SNOWY_STONE_BUILDING', 'RED_24_MARKING', 'POTS_OR_BARRELS_AND_TOP_GREEN_ICON_BAR'],
    'pic3-4.jpg': ['SNOWY_STONE_ENTRANCE', 'WOOD_OR_ROPE_FRAME_AND_CONTAINERS', 'TOP_GREEN_ICON_BAR'],
    'pic3-2.jpg': ['SNOWY_CARVED_STONE_BUILDING', 'BARE_TREE_AND_ENTRANCE', 'TOP_GREEN_ICON_BAR'],
    'pic3-5.jpg': ['SNOWY_CARVED_STONE_BUILDING', 'POINTED_ORNAMENTS_AND_ENTRANCE', 'TOP_GREEN_ICON_BAR'],
}


class PictureTables(HTMLParser):
    """Bind each picture to its smallest nonempty containing table caption."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.tables = [], []
        self.hidden, self.picture_order = 0, []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        if self.hidden:
            return
        attrs = dict(attrs)
        if tag == 'table':
            self.stack.append({'parts': [], 'pictures': []})
        elif tag in ('br', 'td', 'tr'):
            self.handle_data(' ')
        elif tag == 'img' and attrs.get('src'):
            original = urljoin(ORIGINAL, attrs['src'])
            if re.fullmatch(re.escape(ROOT) + r'images/game/pic3(?:-\d)?\.jpg', original):
                row = {'original_url': original, 'html_width': attrs.get('width'), 'html_height': attrs.get('height')}
                self.picture_order.append(original)
                for table in self.stack:
                    table['pictures'].append(row)

    def handle_data(self, data):
        if not self.hidden:
            for table in self.stack:
                table['parts'].append(data)

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.hidden:
            self.hidden -= 1
        elif not self.hidden and tag == 'table':
            require(self.stack, 'unmatched image table')
            table = self.stack.pop()
            self.tables.append({'text': compact(''.join(table['parts'])), 'pictures': table['pictures']})


def caption_pairs(document):
    p = PictureTables()
    p.feed(document)
    p.close()
    require(not p.stack, 'unterminated source table')
    require(len(p.picture_order) == 6 and len(set(p.picture_order)) == 6, 'six distinct scene references required')
    result = []
    for original in p.picture_order:
        choices = [t for t in p.tables if len(t['pictures']) == 1 and t['pictures'][0]['original_url'] == original and t['text']]
        require(choices, 'image has no containing caption')
        selected = min(choices, key=lambda t: len(t['text']))
        result.append({**selected['pictures'][0], 'caption_as_written': selected['text']})
    expected = [(ROOT + 'images/game/' + name, caption) for name, caption, _ in CAPTIONS]
    require([(x['original_url'], x['caption_as_written']) for x in result] == expected, 'caption-to-image or source order changed')
    return result


def region_contract(document):
    d = parse(document, ORIGINAL)
    start, end = '瑞爾亞斯：', '冰顫通道其一：'
    require(d.text.count(start) == 1 and d.text.count(end) == 1, 'region content boundaries changed')
    paragraph = d.text.split(start, 1)[1].split(end, 1)[0]
    for token in ('第十大莊園', '別名又叫作冰世界', '常年都是冰天雪地', '風是寒冷', '草與稻作都很難生長', '桀傲不訓'):
        require(token in paragraph, 'region environmental or cultural assertion changed')
    match = re.search(r'新地圖包括([^。]+)。', paragraph)
    require(match is not None, 'missing named map list')
    names = match.group(1).split('、')
    require(tuple(names) == MAP_NAMES, 'named map coverage or order changed')
    refs = caption_pairs(document)
    for i, ((_, _, kind), row) in enumerate(zip(CAPTIONS, refs)):
        row.update(source_order=i, caption_role=kind, caption_place_prefix=('薩爾亞斯之都' if row['caption_as_written'].startswith('薩爾') else '瑞爾亞斯之都' if row['caption_as_written'].startswith('瑞爾') else None),
                   canonical_npc_or_map_id=None, service_transaction_executed=False)
    return {'primary_label_as_written': '瑞爾亞斯', 'explicit_alias_as_written': '冰世界',
            'estate_ordinal_described': 10, 'ordinal_is_verified_complete_estate_census': False,
            'description_fingerprint': fingerprint(paragraph),
            'environment_and_culture': {'year_round_snow_and_ice_described': True, 'cold_wind_described': True,
                'grass_and_rice_growth_described': 'DIFFICULT_NOT_IMPOSSIBLE', 'resident_characterization': 'OPERATOR_DESCRIBES_HEADSTRONG_ADVENTUROUS_PEOPLE',
                'crop_growth_rate_or_weather_mechanic_recovered': False, 'npc_behavior_program_recovered': False},
            'named_maps': [{'source_order': i, 'label_as_written': name, 'floor_id': None, 'coordinates': None, 'adjacency_proven': False} for i, name in enumerate(names)],
            'named_map_count': 12, 'scenes': refs,
            'name_conflict': {'body_and_map_list_prefix': '瑞爾亞斯', 'other_caption_prefix': '薩爾亞斯', 'caption_orders_with_other_prefix': [1, 2, 4],
                'disposition': 'UNRESOLVED_VARIANT_OR_TYPO_OR_DISTINCT_NAME', 'automatically_merged_or_corrected': False},
            'twenty_four_hour_store': {'source': 'CAPTION_LABEL', 'actual_always_open_service_verified': False},
            'relationship_to_previous_lost_world': 'ACTUAL_LINKED_DETAIL_ONLY_NOT_EXPLICIT_IDENTITY_OR_EXACT_BUILD'}


def jpeg_contract(raw, final, original):
    name = original.rsplit('/', 1)[-1]
    require(name in IMAGE_PINS and original == ROOT + 'images/game/' + name, 'unknown scene reference')
    pin = IMAGE_PINS[name]
    require(final == pin['final_url'], 'scene original URL or actual capture changed')
    require(len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'], 'scene source bytes changed')
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        require(im.format == 'JPEG', 'not original JPEG scene')
        size = list(im.size)
    return {'pixels_acquired': True, 'final_url': final, 'actual_capture': re.search(r'/web/(\d{14})id_/', final).group(1),
            'bytes': len(raw), 'sha256': pin['sha256'], 'format': 'JPEG', 'actual_dimensions': size,
            'individually_viewed': True, 'visual_observations': VISUALS[name], 'named_npc_or_pet_identification': None}


def build(raw, final, images, previous_raw):
    require(final == URL, 'wrong detail original URL or actual capture')
    require(len(raw) == 26346 and hashlib.sha256(raw).hexdigest() == SHA, 'detail source bytes changed')
    require(hashlib.sha256(previous_raw).hexdigest() == PREVIOUS_SHA, 'previous authenticated introduction changed')
    previous = json.loads(previous_raw)
    require(previous['world']['detail_links'][0]['url'] == ORIGINAL, 'first actual source-order detail edge changed')
    document = raw.decode('big5', errors='strict')
    facts = region_contract(document)
    require(set(images) == {x['original_url'] for x in facts['scenes']}, 'six-scene source coverage changed')
    for row in facts['scenes']:
        row.update(jpeg_contract(*images[row['original_url']], row['original_url']))
        require(row['actual_dimensions'] == [int(row['html_width']), int(row['html_height'])] == [220, 163], 'actual scene dimensions changed')
    return {'schema': 'stoneage.wayi.official_ice_region.r1',
            'source': {'original_url': ORIGINAL, 'actual_capture': CAPTURE, 'final_url': final, 'bytes': len(raw), 'sha256': SHA, 'codec': 'big5'},
            'previous_introduction': metadata(PREVIOUS, previous_raw),
            'selection': {'basis': 'FIRST_REAL_HREF_IN_SOURCE_ORDER', 'topic_from_numeric_filename_assumed': False, 'other_three_detail_bodies_queried': False},
            'version_context': {'profile': 'TAIWAN_WAYI_OFFICIAL_WEB_2005_DETAIL', 'exact_client_build': None, 'source_title_is_build_number': False,
                'previous_intro_discusses_1_to_8': True, 'ice_region_equals_all_of_lost_world_proven': False},
            'region': facts, 'qualified_scene_count': 6,
            'temporality': {'html_capture_year': 2005, 'scene_capture_year': 2006, 'same_capture_instant': False, 'actual_first_release_date': None},
            'riding_visual_candidate': {'basis': 'OVERLAPPING_SPRITES_IN_ICE_PASSAGE_IMAGE', 'grade': 'HYPOTHESIS_VISUAL_APPEARANCE_ONLY', 'normal_player_unlock_or_mount_rules_proven': False},
            'boundaries': {'actual_game_server_or_service_transaction_executed': False, 'original_map_payload_floor_ids_or_route_graph_recovered': False,
                'named_npc_dialogue_or_pet_species_recovered': False, 'same_build_jss1999_or_tw10_promoted': False,
                'original_native_client_resolution_proven': False, 'estate_ownership_or_guild_mechanic_proven': False,
                'original_html_jpeg_or_software_retained_in_git': False, 'stage_a_family_status_changed': False,
                'stage_b_production': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'}}


def catalog_contract(report_raw, archive_raw):
    report, archive = json.loads(report_raw), json.loads(archive_raw)
    require(report['schema'] == 'stoneage.wayi.official_ice_region.r1', 'wrong region report schema')
    collections = archive['future_website']['required_collections']
    require(len(collections) == 19 and {'maps', 'screens'} <= set(collections), 'existing archive collections changed')
    source = metadata(REPORT, report_raw)
    records = []
    def record(suffix, collection, entity_type, label, status, pointer, **extra):
        row = {'record_id': 'wayi-tw-web2005-ice:' + suffix, 'collection': collection, 'entity_type': entity_type,
               'version_profile': report['version_context']['profile'], 'source_refs': [{'path': source['path'], 'sha256': source['sha256'], 'json_pointer': pointer}],
               'verification_status': status, 'rights_status': 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED', 'record_revision': 1,
               'display_label_as_written': label, 'game_ids': None, **extra}
        require(set(archive['future_website']['record_contract']['required']) <= set(row), 'missing shared archive field')
        records.append(row)
    region = report['region']
    record('region', 'maps', 'OFFICIAL_REGION_DESCRIPTION', region['primary_label_as_written'], 'OPERATOR_DESCRIPTION_WITH_UNRESOLVED_CAPTION_NAME_VARIANT', '/region',
           explicit_alias=region['explicit_alias_as_written'], exact_client_build=None, estate_ordinal_described=10)
    for row in region['named_maps']:
        i = row['source_order']
        record('map:' + str(i), 'maps', 'OFFICIAL_NAMED_MAP_LABEL', row['label_as_written'], 'NAME_ONLY_NOT_RECOVERED_FLOOR_OR_ROUTE', '/region/named_maps/' + str(i),
               floor_id=None, coordinates=None, outgoing_routes=None)
    for row in region['scenes']:
        i = row['source_order']
        record('scene:' + str(i), 'screens', 'OFFICIAL_SCENE_JPEG_AND_CAPTION', row['caption_as_written'], 'SOURCE_QUALIFIED_IMAGE_CAPTION_WITH_PLACE_VARIANT_PRESERVED', '/region/scenes/' + str(i),
               asset_refs=[{'original_url': row['original_url'], 'actual_capture': row['actual_capture'], 'sha256': row['sha256']}],
               npc_entity_id=None, pet_species_id=None, original_native_resolution=None)
    require(len(records) == 19 and len({x['record_id'] for x in records}) == 19, 'catalog record coverage changed')
    return {'schema': 'stoneage.wayi.official_ice_region.content_catalog.r1', 'derived_source': source,
            'existing_archive_contract': metadata(ARCHIVE, archive_raw), 'record_count': len(records), 'records': records,
            'counts_are_source_records_not_complete_maps_or_entities': True, 'npc_pet_or_quest_entities_created': 0,
            'all_place_name_variants_canonicalized': False, 'public_export_allowed': False, 'website_or_game_implemented': False,
            'original_asset_bytes_included': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path)
    p.add_argument('--image-dir', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--catalog-output', type=Path)
    args = p.parse_args()
    final = URL
    if args.input:
        raw = args.input.read_bytes()
    else:
        with urlopen(Request(URL, headers={'User-Agent': 'StoneAge-Historical-Research/1.0'}), timeout=60) as response:
            raw, final = response.read(262145), response.url
            require(len(raw) <= 262144, 'HTML outside source bound')
    def acquire(name):
        original, final = ROOT + 'images/game/' + name, IMAGE_PINS[name]['final_url']
        if args.image_dir:
            b = (args.image_dir / name).read_bytes()
        else:
            with urlopen(Request(final, headers={'User-Agent': 'StoneAge-Historical-Research/1.0'}), timeout=60) as response:
                b, final = response.read(1048577), response.url
                require(len(b) <= 1048576, 'JPEG outside source bound')
        return original, (b, final)
    with ThreadPoolExecutor(max_workers=3) as pool:
        images = dict(pool.map(acquire, IMAGE_PINS))
    result = build(raw, final, images, Path(PREVIOUS).read_bytes())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    raw_report = dump(result)
    args.output.write_text(raw_report, encoding='utf-8')
    if args.catalog_output:
        args.catalog_output.parent.mkdir(parents=True, exist_ok=True)
        args.catalog_output.write_text(dump(catalog_contract(raw_report.encode(), Path(ARCHIVE).read_bytes())), encoding='utf-8')
    print(json.dumps({'new_detail_page': 1, 'named_maps': 12, 'qualified_original_scenes': 6, 'unresolved_name_conflict': True, 'original_map_ids_recovered': False}))


if __name__ == '__main__':
    main()
