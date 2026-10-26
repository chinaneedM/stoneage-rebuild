"""One bounded acquisition of twelve missing named operator-web GIF references.

Only derived metadata and encrypted decoded PNG leave the source runner.
Names belong to pinned web positions, never inferred client/species identities.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from PIL import Image
from tools.stoneage_p3_private_frame import seal

PARENT = Path('research/recovered/STONEAGE-JP-OFFICIAL-PET-CATALOG-R1.json')
PRIOR = Path('research/recovered/STONEAGE-JP-OFFICIAL-PET-VISUAL-SAMPLE-R1.json')
PARENT_SHA = 'edf50ec2fe9915db1904992ee2871def9b719fa05e40619019229be21dca413f'
PRIOR_SHA = 'fce2492fc51abfae360d189eb6a86319bcabec482cb5f151c5a68250dbd8640e'
PUBLIC = Path('research/recovered/STONEAGE-JP-PET-VISUAL-R25-PUBLIC.pem')
SELECTION = [3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15]
MAX_GIF_BYTES = 100000


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def selected(parent_raw, prior_raw):
    need(sha(parent_raw) == PARENT_SHA and sha(prior_raw) == PRIOR_SHA, 'parent/prior bytes changed')
    parent, prior = json.loads(parent_raw), json.loads(prior_raw)
    need(len(parent['records']) == 124 and prior['coverage']['qualified_new_images'] == 12,
         'prior coverage changed')
    seen = {x['image']['original_url'] for x in prior['records'] if x['image']['pixels_acquired']}
    seen.update(x['image']['original_url'] for x in parent['records'] if x['image']['pixels_acquired'])
    need(len(seen) == 13, 'prior qualified URL coverage changed')
    rows = [x for x in parent['records'] if x['image']['original_url'] not in seen][:12]
    need([x['web_ordinal'] for x in rows] == SELECTION, 'next12 are not first unacquired positions')
    need(len({x['image']['original_url'] for x in rows}) == 12, 'duplicate selected URL')
    return rows


def inspect(raw, final_url, original_url):
    match = re.fullmatch(r'https://web\.archive\.org/web/([0-9]{14})id_/(.+)', final_url)
    need(match is not None and match[2] == original_url, 'unqualified capture/host/path redirect')
    need(0 < len(raw) <= MAX_GIF_BYTES and raw[:6] in (b'GIF87a', b'GIF89a'), 'not bounded original GIF')
    with Image.open(BytesIO(raw)) as image:
        need(image.format == 'GIF' and image.size == (60, 65), 'unqualified GIF dimensions')
        need(image.n_frames == 1, 'this static-image package cannot qualify animated source')
        image.load()
        rgba = image.convert('RGBA')
        png = BytesIO(); rgba.save(png, format='PNG')
        return {'actual_capture': match[1], 'strict_replay_url': final_url,
                'sha256': sha(raw), 'bytes': len(raw), 'format': 'GIF',
                'actual_size': list(image.size), 'frames': image.n_frames,
                'rgba_sha256': sha(rgba.tobytes()), 'decoded_png_sha256': sha(png.getvalue()),
                'decoded_png_bytes': len(png.getvalue())}, png.getvalue()


def acquire_one(parent, public_pem, fetch):
    original = parent['image']['original_url']
    requested = 'https://web.archive.org/web/'+parent['source_refs'][0]['actual_capture']+'id_/'+original
    base = {'web_ordinal': parent['web_ordinal'], 'parent_record_id': parent['record_id'],
            'name_as_written': parent['name_as_written'], 'version_profile': parent['version_profile'],
            'page_source': parent['source_refs'][0], 'original_url': original,
            'requested_url': requested, 'attempt_count': 1,
            'visual_review_performed_at_source': False}
    try:
        raw, final, status, content_type = fetch(requested)
        base['http'] = {'status': status, 'final_url': final, 'content_type': content_type,
                        'response_bytes': len(raw), 'response_sha256': sha(raw)}
        need(status == 200, 'HTTP response is not successful')
        metadata, png = inspect(raw, final, original)
        return {**base, 'status': 'SOURCE_GIF_BYTES_QUALIFIED_PENDING_PRIVATE_VISUAL_REVIEW',
                'image': metadata}, seal(png, public_pem)
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as error:
        # A bounded failed fetch is not a new image or a no-image historical claim.
        if isinstance(error, HTTPError):
            base['http'] = {'status': error.code, 'final_url': error.url}
        return {**base, 'status': 'UNAVAILABLE_OR_UNQUALIFIED_THIS_SINGLE_ATTEMPT',
                'failure': type(error).__name__+': '+str(error)[:500], 'image': None}, None


def fetch(url):
    with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 StoneAgeHistoricalEvidence'}), timeout=45) as response:
        return response.read(MAX_GIF_BYTES+1), response.url, response.status, response.headers.get('Content-Type')


def run(public_pem, fetcher=fetch):
    rows = selected(PARENT.read_bytes(), PRIOR.read_bytes())
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda p: acquire_one(p, public_pem, fetcher), rows))
    entries = [x[0] for x in results]
    envelopes = {str(x['web_ordinal']): e for x, e in results if e is not None}
    qualified = sum(x['image'] is not None for x in entries)
    return {
        'schema': 'stoneage.jp_named_pet_visual_r25.actual_source.v1',
        'task': 'JP-OFFICIAL-NAMED-PET-VISUAL-BATCH-25', 'date': '2026-10-26',
        'source_pins': {str(PARENT): {'sha256': PARENT_SHA}, str(PRIOR): {'sha256': PRIOR_SHA}},
        'selection': SELECTION, 'entries': entries,
        'counts': {'attempted_references': 12, 'qualified_gifs': qualified,
                   'unavailable_or_unqualified': 12-qualified, 'previously_qualified_references': 13,
                   'qualified_reference_total': 13+qualified, 'unacquired_references': 111-qualified},
        'transport': {'public_key_sha256': sha(public_pem), 'encrypted_png_count': len(envelopes),
                      'method': 'EXISTING_P3_X25519_AESGCM_PNG_TRANSPORT'},
        'boundaries': {'original_gifs_or_plain_png_uploaded': False, 'original_assets_in_git': False,
                       'assistant_visual_review_done': False, 'original_game_executed': False,
                       'tw10_or_same_build_species_identity_proven': False,
                       'same_instant_as_parent_page_proven': False, 'all_species_census_complete': False},
    }, envelopes


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args(); args.output_dir.mkdir(parents=True, exist_ok=False)
    report, envelopes = run(PUBLIC.read_bytes())
    (args.output_dir/'source-derived.json').write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)+'\n')
    (args.output_dir/'private-png-envelopes.json').write_text(json.dumps(envelopes, sort_keys=True)+'\n')
    print('R25_ATTEMPTED_REFERENCES=12')
    print('R25_SOURCE_QUALIFIED_GIFS='+str(report['counts']['qualified_gifs']))
    print('R25_ORIGINAL_ASSET_PLAINTEXT_UPLOAD=0')


if __name__ == '__main__': main()
