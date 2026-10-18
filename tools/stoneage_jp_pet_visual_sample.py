"""Bounded web pet illustration references; never a client species/animation census."""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from PIL import Image

PARENT = Path('research/recovered/STONEAGE-JP-OFFICIAL-PET-CATALOG-R1.json')
PARENT_SHA = 'edf50ec2fe9915db1904992ee2871def9b719fa05e40619019229be21dca413f'
MANIFEST = Path('research/recovered/STONEAGE-JP-OFFICIAL-PET-VISUAL-SAMPLE-SOURCES-R1.json')
REPORT = Path('research/recovered/STONEAGE-JP-OFFICIAL-PET-VISUAL-SAMPLE-R1.json')
SELECTION = [2, 10, 19, 28, 46, 55, 64, 73, 91, 100, 109, 118]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inspect_image(raw, final_url, pin):
    require(final_url == pin['strict_replay_url'], 'Actual image host/path/capture differs')
    require(len(raw) == pin['bytes'] and sha256(raw).hexdigest() == pin['sha256'], 'Image byte pin mismatch')
    with Image.open(BytesIO(raw)) as im:
        require(im.format == 'GIF' and list(im.size) == pin['actual_size'] == [60, 65], 'Unexpected image format/dimensions')
        require(im.n_frames == pin['frames'] and 1 <= im.n_frames <= 100, 'Unexpected image frame count')
        for frame in range(im.n_frames):
            im.seek(frame)
            im.load()


def validate_manifest(parent_raw, manifest):
    require(sha256(parent_raw).hexdigest() == PARENT_SHA, 'Parent catalog pin mismatch')
    parent = json.loads(parent_raw)
    entries = manifest['entries']
    require([e['web_ordinal'] for e in entries] == SELECTION, 'Bounded selection/order changed')
    require(len({e['original_url'] for e in entries}) == 12, 'Duplicate source URL')
    for e in entries:
        p = parent['records'][e['web_ordinal'] - 1]
        require(e['parent_record_id'] == p['record_id'] and e['name_as_written'] == p['name_as_written'], 'Parent identity/name differs')
        require(e['original_url'] == p['image']['original_url'] and e['page_capture'] == p['source_refs'][0]['actual_capture'], 'Source reference/page capture differs')
        require(not p['image']['pixels_acquired'], 'Selected image was already acquired in parent')
        if e['status'] == 'QUALIFIED_LOCAL_BYTES_PENDING_INDEPENDENT_REPLAY':
            expected = 'https://web.archive.org/web/' + e['actual_capture'] + 'id_/' + e['original_url']
            require(bool(re.fullmatch(r'[0-9]{14}', e['actual_capture'])) and e['strict_replay_url'] == expected, 'Unqualified archived image URL')
            require(e['format'] == 'GIF' and e['actual_size'] == [60, 65] and 1 <= e['frames'] <= 100, 'Manifest structure differs')
            require(0 < e['bytes'] <= 100000 and bool(re.fullmatch(r'[a-f0-9]{64}', e['sha256'])), 'Invalid byte fingerprint')
            require(e['visual_review']['status'] == 'EXACT_HASH_FILE_VIEWED' and bool(e['visual_review']['observations']), 'Missing actual visual review')
        else:
            require(e['status'] == 'UNAVAILABLE_THIS_BOUNDED_ATTEMPT' and bool(e['attempts']), 'Unsupported source status')
            require(all(e.get(k) is None for k in ('sha256', 'actual_capture', 'actual_size', 'frames')), 'Failure contains acquired pixel claims')
    return parent


def build(parent_raw, manifest, acquired):
    parent = validate_manifest(parent_raw, manifest)
    records = []
    for e in manifest['entries']:
        p = parent['records'][e['web_ordinal'] - 1]
        qualified = e['status'] == 'QUALIFIED_LOCAL_BYTES_PENDING_INDEPENDENT_REPLAY'
        if qualified:
            require(e['web_ordinal'] in acquired, 'Qualified image bytes missing')
            raw, final = acquired[e['web_ordinal']]
            inspect_image(raw, final, e)
        else:
            require(e['web_ordinal'] not in acquired, 'Failed source has unqualified image bytes')
        image_fields = ('original_url', 'actual_capture', 'strict_replay_url', 'sha256', 'bytes', 'format', 'actual_size', 'frames')
        image = {k: e.get(k) for k in image_fields}
        image.update(pixels_acquired=qualified, declared_size=p['image']['declared_size'],
                     same_instant_as_page_proven=False, original_client_sprite_or_animation_proven=False)
        refs = [dict(p['source_refs'][0])]
        if qualified:
            refs.append({'source': e['original_url'], 'sha256': e['sha256'], 'actual_capture': e['actual_capture'], 'evidence_role': 'INDEPENDENTLY_HASHED_WEB_ILLUSTRATION_NOT_CLIENT_RESOURCE'})
        records.append({'record_id': f"jp-hangame-pet-web:visual-sample:{e['web_ordinal']:03d}", 'collection': 'pets',
                        'entity_type': 'OFFICIAL_NAMED_PET_WEB_VISUAL_REFERENCE',
                        'record_revision': 1, 'version_profile': p['version_profile'], 'source_refs': refs,
                        'verification_status': 'NAMED_WEB_ILLUSTRATION_BYTES_QUALIFIED' if qualified else 'REFERENCE_ONLY_PIXEL_SOURCE_UNAVAILABLE_THIS_ATTEMPT',
                        'rights_status': 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED', 'parent_record_id': p['record_id'],
                        'web_ordinal': e['web_ordinal'], 'name_as_written': p['name_as_written'],
                        'client_species_graphic_ids': None, 'cross_region_aliases': None, 'stats_growth_habitat_skills': None,
                        'image': image, 'visual_review': e.get('visual_review'), 'initial_bounded_acquisition_attempts': e['attempts']})
    successful = sum(r['image']['pixels_acquired'] for r in records)
    require(set(acquired) == {r['web_ordinal'] for r in records if r['image']['pixels_acquired']}, 'Extra unselected acquisition')
    return {'schema': 'stoneage.jp.official_pet_visual_sample.r1', 'date': '2026-10-19',
            'task': 'OFFICIAL-PET-VISUAL-COVERAGE-AND-VERSION-REVIEW-01',
            'parent_catalog': {'path': str(PARENT), 'sha256': PARENT_SHA, 'records': 124, 'immutable_parent_not_rewritten': True},
            'selection': SELECTION, 'sampling': 'FOUR_EXISTING_REFERENCES_PER_PAGE_FROM_DISTINCT_TABLE_GROUPS_NOT_SPECIES_REPRESENTATIVE',
            'records': records, 'coverage': {'attempted_new_references': 12, 'qualified_new_images': successful,
            'unavailable_this_attempt': 12 - successful, 'qualified_with_parent': 1 + successful,
            'remaining_unacquired_references': 123 - successful, 'complete_species_or_visual_catalog': False,
            'new_image_capture_year_counts': dict(sorted(Counter(r['image']['actual_capture'][:4] for r in records if r['image']['pixels_acquired']).items()))},
            'boundaries': {'original_assets_in_git': False, 'web_position_or_filename_is_game_id': False,
            'same_contemporaneous_roster_or_client_build_proven': False, 'aliases_stats_growth_habitat_skills_recovered': False,
            'all_images_are_original_game_sprite_frames': False, 'visual_similarity_proves_cross_region_identity': False,
            'stage_a_families': '7_PARTIAL_2_OPEN_UNCHANGED', 'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'},
            'material_review': 'research/recovered/STONEAGE-OFFICIAL-VERSION-COVERAGE-MATERIAL-REVIEW-R6.json',
            'next': 'JP-OFFICIAL-TOWN-NAMED-GEOGRAPHY-SOURCE-01'}


def acquire(url):
    for attempt in range(2):
        try:
            with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 StoneAgeHistoricalEvidence'}), timeout=35) as r:
                return r.read(100001), r.url
        except HTTPError as exc:
            if attempt or exc.code not in (502, 503, 504):
                raise
            print('BOUNDED_RETRY_HTTP=' + str(exc.code) + ' URL=' + url, flush=True)
        except (URLError, TimeoutError) as exc:
            if attempt:
                raise
            print('BOUNDED_RETRY_NETWORK=' + type(exc).__name__ + ' URL=' + url, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--local-input-dir')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    parent_raw = PARENT.read_bytes()
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    validate_manifest(parent_raw, manifest)
    acquired = {}
    for e in manifest['entries']:
        if e['status'] != 'QUALIFIED_LOCAL_BYTES_PENDING_INDEPENDENT_REPLAY':
            continue
        if args.local_input_dir:
            raw = (Path(args.local_input_dir) / f"{e['web_ordinal']:03d}.gif").read_bytes()
            acquired[e['web_ordinal']] = raw, e['strict_replay_url']
        else:
            acquired[e['web_ordinal']] = acquire(e['strict_replay_url'])
        print('SOURCE_IMAGE=' + str(e['web_ordinal']) + ' CAPTURE=' + e['actual_capture'] + ' SHA256=' + e['sha256'], flush=True)
    result = build(parent_raw, manifest, acquired)
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(payload, encoding='utf-8')
    print('QUALIFIED_NEW_IMAGES=' + str(result['coverage']['qualified_new_images']))
    print('DERIVED_SHA256=' + sha256(payload.encode()).hexdigest())


if __name__ == '__main__':
    main()
