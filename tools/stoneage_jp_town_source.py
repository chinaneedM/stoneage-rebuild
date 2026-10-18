"""Four operator-described settlements; one separately dated illustration, no game map IDs."""
import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
from PIL import Image
from tools.stoneage_jp_pet_catalog import Grid, acquire, archive, require

ORIGINAL = 'http://www.hangame.co.jp/publish/sa/town.asp'
CAPTURE = '20031214052752'
SOURCE_SHA = '5627429482edaad6d24ac5270b53891c227ae394ab10d07f715a336d77c3175a'
IMAGES = 'http://images.hangame.co.jp/_images/game/saj/'
IMAGE_ORIGINAL = IMAGES + 'town1-1.gif'
IMAGE_CAPTURE = '20060618193306'
IMAGE_SHA = '5712fe0554f9daf067970ec102155fa594ee8e14c9e5333d74662180412bc560'
NAMES = ['サムギル村', 'マリナス村', 'ジャジャ村', 'カルターナ村']
REGIONS = ['サイナス島', 'サイナス', 'ジャルガ', 'ジャルガ']
CLAIMS = [
    ['OPERATOR_DESCRIBES_LARGEST_VILLAGE_ON_NAMED_ISLAND', 'PROMOTIONAL_BEST_ORDERED_AMONG_FOUR_COMPARISON'],
    ['SOURCE_WEST_ASSOCIATION_TO_NAMED_REGION', 'FACES_A_BEACH'],
    ['SOURCE_EAST_ASSOCIATION_TO_NAMED_REGION', 'FOREST_SURROUNDINGS_AND_LUSH_GREEN_SETTING'],
    ['SOURCE_WEST_ASSOCIATION_TO_NAMED_REGION', 'SETTLEMENT_SPANS_SEVERAL_SMALL_ISLANDS'],
]
REPORT = Path('research/recovered/STONEAGE-JP-OFFICIAL-TOWN-SOURCE-R1.json')


class TownGrid(Grid):
    def __init__(self):
        super().__init__()
        self.town_images = []
        self.facilities = []
        self.facility_label = None

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        d = dict(attrs)
        if self.hidden:
            return
        if tag == 'img' and re.fullmatch(re.escape(IMAGES) + r'town1-[1-4]\.gif', d.get('src', '')):
            require(self.tables and self.tables[-1]['open'], 'Town image outside table cell')
            self.town_images.append({**self.tables[-1], **d})
        if tag == 'font' and d.get('onclick') == "location.href='town2.asp';":
            self.facility_label = []

    def handle_data(self, value):
        super().handle_data(value)
        if self.facility_label is not None and not self.hidden and value.strip():
            self.facility_label.append(value.strip())

    def handle_endtag(self, tag):
        if tag == 'font' and self.facility_label is not None and not self.hidden:
            self.facilities.append(''.join(self.facility_label))
            self.facility_label = None
        super().handle_endtag(tag)


def classify_page(html):
    p = TownGrid(); p.feed(html)
    require('村の紹介' in p.visible, 'Actual village topic missing')
    require(len(p.town_images) == 4 and len({im['table'] for im in p.town_images}) == 1, 'Wrong actual village references')
    entries = []
    for i, im in enumerate(p.town_images):
        require(im['src'] == IMAGES + f'town1-{i+1}.gif', 'Village image order/identity differs')
        require((im['row'], im['col']) == (i * 2, 0), 'Village same-row DOM relation differs')
        require((im.get('width'), im.get('height')) == ('200', '150'), 'Village declared dimensions differ')
        texts = p.cells.get((im['table'], im['row'], 2), [])
        require(len(texts) >= 2 and texts[0] == NAMES[i], 'Same-row village name/description missing or changed')
        entries.append({'name_as_written': texts[0], 'image_original_url': im['src'],
                        'dom_cells': {'table': im['table'], 'row': im['row'], 'image_column': 0, 'name_description_column': 2},
                        'source_description_sha256': sha256(('\n'.join(texts[1:]) + '\n').encode()).hexdigest()})
    require(p.facilities == ['村の施設の紹介'], 'Actual facilities link label/target differs')
    return entries


def inspect_page(raw, final):
    require(final == archive(ORIGINAL, CAPTURE), 'Town page host/path/capture mismatch')
    require(len(raw) == 14371 and sha256(raw).hexdigest() == SOURCE_SHA, 'Town page byte pin mismatch')
    return classify_page(raw.decode('cp932', errors='strict'))


def inspect_image(raw, final):
    require(final == archive(IMAGE_ORIGINAL, IMAGE_CAPTURE), 'Town illustration host/path/capture mismatch')
    require(len(raw) == 27303 and sha256(raw).hexdigest() == IMAGE_SHA, 'Town illustration byte pin mismatch')
    with Image.open(BytesIO(raw)) as im:
        require(im.format == 'GIF' and im.size == (200, 150) and im.n_frames == 1, 'Unexpected town GIF structure')
        im.load()


def build(raw, final, image, image_final):
    entries = inspect_page(raw, final); inspect_image(image, image_final)
    records = []
    for i, e in enumerate(entries):
        im = {'original_url': e['image_original_url'], 'pixels_acquired': i == 0, 'declared_size': [200, 150],
              'actual_capture': IMAGE_CAPTURE if i == 0 else None, 'sha256': IMAGE_SHA if i == 0 else None,
              'bytes': 27303 if i == 0 else None, 'actual_size': [200, 150] if i == 0 else None, 'frames': 1 if i == 0 else None,
              'same_instant_as_page_proven': False, 'building_function_or_original_client_map_proven': False}
        refs = [{'source': ORIGINAL, 'actual_capture': CAPTURE, 'sha256': SOURCE_SHA, 'evidence_role': 'OPERATOR_SAME_ROW_VILLAGE_DESCRIPTION_AND_IMAGE_REFERENCE'}]
        if i == 0: refs.append({'source': IMAGE_ORIGINAL, 'actual_capture': IMAGE_CAPTURE, 'sha256': IMAGE_SHA, 'evidence_role': 'SEPARATE_CAPTURE_WEB_ILLUSTRATION'})
        records.append({'record_id': f'jp-hangame-village:web-position:{i+1:02d}', 'collection': 'maps',
                        'entity_type': 'OPERATOR_DESCRIBED_SETTLEMENT_NOT_CLIENT_MAP_PAYLOAD', 'record_revision': 1,
                        'version_profile': 'JAPAN_HANGAME_WEB_20031214', 'source_refs': refs,
                        'verification_status': 'SOURCE_DESCRIBED_GEOGRAPHY_NOT_RUNTIME_SURVEY',
                        'rights_status': 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED', **e,
                        'region_name_as_written': REGIONS[i], 'region_entity_id': None, 'source_qualified_claims': CLAIMS[i],
                        'client_map_id_coordinates_routes_npcs_encounters': None, 'cross_region_aliases': None,
                        'population_area_or_world_town_census': None, 'image': im})
    return {'schema': 'stoneage.jp.official_town_source.r1', 'date': '2026-10-19',
            'task': 'JP-OFFICIAL-TOWN-NAMED-GEOGRAPHY-SOURCE-01', 'scope': 'ONE_ACTUAL_BODY_FOUR_VILLAGE_REFERENCES_AND_SOLE_FIRST_ILLUSTRATION',
            'source': {'original_url': ORIGINAL, 'strict_replay_url': final, 'actual_capture': CAPTURE, 'bytes': len(raw), 'sha256': SOURCE_SHA, 'encoding': 'CP932_STRICT'},
            'initial_discovery': {'requested_page_url': archive(ORIGINAL, '20031214055553'), 'requested_image_url': archive(IMAGE_ORIGINAL, CAPTURE), 'bounded_failures_observed': []},
            'records': records, 'reviewed_image': {'original_url': IMAGE_ORIGINAL, 'strict_replay_url': image_final, 'actual_capture': IMAGE_CAPTURE,
            'sha256': IMAGE_SHA, 'bytes': 27303, 'format': 'GIF', 'actual_size': [200, 150], 'frames': 1, 'human_visual_review': 'EXACT_HASH_ORIGINAL_FILE_VIEWED',
            'observations': ['GRAY_STONE_BUILDING_WITH_ANIMAL_HEAD_MOTIF', 'SURROUNDING_PAVING_AND_VEGETATION'],
            'building_function_or_map_coordinates_inferred': False},
            'coverage': {'named_village_descriptions': 4, 'qualified_images': 1, 'unacquired_image_references': 3, 'original_world_map_payloads_recovered': 0},
            'boundaries': {'four_entries_are_all_world_villages': False, 'relative_west_east_is_exact_route_or_coordinate': False,
            'promotional_largest_or_best_ordered_is_measured_area_population': False, 'sainas_spellings_silently_merged': False,
            'cross_region_aliases_or_early_build_identity_proven': False, 'original_assets_in_git': False, 'stage_a_families': '7_PARTIAL_2_OPEN',
            'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'},
            'next': {'task': 'JP-OFFICIAL-VILLAGE-FACILITIES-SOURCE-01', 'actual_target': 'http://www.hangame.co.jp/publish/sa/town2.asp',
                     'actual_label': '村の施設の紹介', 'qualification': 'STATIC_LITERAL_NAVIGATION_NOT_YET_READ',
                     'limit': 'ONE_TOPIC_VERIFIED_BODY_AND_AT_MOST_ONE_EXPLICITLY_ASSOCIATED_IMAGE; NO_PROGRAMS_OR_RECURSION'}}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--local-input-dir'); ap.add_argument('--output', required=True); args = ap.parse_args()
    if args.local_input_dir:
        folder = Path(args.local_input_dir); raw = (folder/'jp-town.html').read_bytes(); image = (folder/'jp-town-first.gif').read_bytes()
        final = archive(ORIGINAL, CAPTURE); image_final = archive(IMAGE_ORIGINAL, IMAGE_CAPTURE)
    else:
        raw, final = acquire(archive(ORIGINAL, CAPTURE)); image, image_final = acquire(archive(IMAGE_ORIGINAL, IMAGE_CAPTURE))
    result = build(raw, final, image, image_final)
    payload = json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n'; out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(payload,encoding='utf-8')
    print('VILLAGE_DESCRIPTIONS=4');print('DERIVED_SHA256='+sha256(payload.encode()).hexdigest());print('PAGE_SHA256='+SOURCE_SHA);print('IMAGE_SHA256='+IMAGE_SHA)


if __name__ == '__main__':main()
