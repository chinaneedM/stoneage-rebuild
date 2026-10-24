"""Qualify real mixed-community DAT bytes and compare to pinned TW8.5 layers.

No TW8.5 package download, map grid export, original server claim or runtime
execution. Layer names remain ordinals across the two different specimens.
"""
import argparse
from collections import Counter
import hashlib
import http.cookiejar
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.parse
import urllib.request

from tools.stoneage_tw85_map_payload import ROOT, digest, parse, pin
from tools.stoneage_tw85_map_archive import REPORT, validate as validate_tw85
from tools.stoneage_tw10_preserved25_file_intersection import BRIDGE, BRIDGE_HASH, BRIDGE_ROOT, GIT_BLOBS, git_blob
from tools.stoneage_wayi85_sixpart_acquisition import direct_link, rehash

BUNDLE_SHA = 'd71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'
PARTS = [
    ('ev7l29fw77891go', 209715200, '7cb7acdecd56617132e6f284c468158917c91d542cad5b2e7b3c7774fb5630d5'),
    ('ytaa168o5jih0lx', 151539980, '567e1ec0aeff9ea6a9ada791a339aa8f8bb8ffba83cf762e4b445fc0f1cb16bb')]
TW85_SHA = 'aacac89c451305c59adf38cfc6c14ba8a2efb88705607206aee7f63a8e14ead5'


def expected_files():
    raw = (ROOT/BRIDGE).read_bytes()
    if git_blob(raw) != GIT_BLOBS[BRIDGE]:
        raise ValueError('mixed25 original inventory drift')
    found = {}
    for line in raw.decode().split('ALL-FILE SHA256\n', 1)[1].splitlines():
        m = BRIDGE_HASH.fullmatch(line)
        if m and BRIDGE_ROOT in m[2]:
            path = m[2].split(BRIDGE_ROOT, 1)[1].casefold()
            if path in found:
                raise ValueError('duplicate qualified mixed25 path')
            found[path] = m[1]
    if len(found) != 2302:
        raise ValueError('incomplete qualified mixed25 namespace')
    return found


def compare_one(reference, raw, expected_sha):
    if digest(raw) != expected_sha:
        raise ValueError('actual mixed25 map bytes differ from original qualified inventory')
    row = {'path': reference['path'], 'tw85_sha256': reference['sha256'],
           'mixed25_bytes': len(raw), 'mixed25_sha256': expected_sha,
           'whole_file_equal': reference['sha256'] == expected_sha,
           'original_place_name': None}
    try:
        observed = parse(raw)
    except ValueError as exc:
        return {**row, 'status': 'MIXED25_LAYOUT_UNRESOLVED', 'reason': str(exc),
                'dimensions_equal': None, 'plane_equal': None}
    dims_equal = (observed['width'], observed['height']) == (reference['width'], reference['height'])
    return {**row, 'status': 'ORDINAL_LAYERS_COMPARED' if dims_equal else 'DIMENSIONS_DIFFER',
            'dimensions_equal': dims_equal,
            'tw85_dimensions': [reference['width'], reference['height']],
            'mixed25_structure': observed,
            'plane_equal': [a['sha256'] == b['sha256'] for a, b in zip(reference['planes'], observed['planes'])]
                           if dims_equal else None}


def compare_directory(client, reference, expected):
    paths = {}
    for path in client.rglob('*'):
        if path.is_symlink():
            raise ValueError('symlink in source client refused')
        if path.is_file():
            rel = path.relative_to(client).as_posix().casefold()
            if rel in paths:
                raise ValueError('case-insensitive duplicate in actual mixed25 namespace')
            paths[rel] = path
    rows = []
    missing = []
    for source in reference['files']:
        key = source['path'].casefold()
        if key not in expected:
            if key in paths:
                raise ValueError('previously absent map appeared in qualified namespace')
            missing.append(source['path'])
            continue
        if key not in paths:
            raise ValueError('expected mixed25 map absent from actual client: '+key)
        rows.append(compare_one(source, paths[key].read_bytes(), expected[key]))
    counts = Counter(x['status'] for x in rows)
    masks = Counter(''.join('1' if v else '0' for v in x['plane_equal'])
                    for x in rows if x['plane_equal'] is not None)
    return {'compared_files': rows, 'tw85_paths_absent_from_mixed25': missing,
            'counts': {'tw85_reference_files': len(reference['files']), 'mixed25_present_paths': len(rows),
                       'mixed25_absent_paths': len(missing),
                       'whole_file_equal': sum(x['whole_file_equal'] for x in rows),
                       'status_counts': dict(sorted(counts.items())), 'plane_equality_masks': dict(sorted(masks.items()))}}


def download_bundle(work):
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    parts = []
    ua = {'User-Agent': 'Mozilla/5.0'}
    for number, (key, size, sha) in enumerate(PARTS, 1):
        req = urllib.request.Request('https://www.mediafire.com/api/1.5/file/get_info.php',
                data=urllib.parse.urlencode({'quick_key': key, 'response_format': 'json'}).encode(), headers=ua)
        with opener.open(req, timeout=60) as response:
            info = json.load(response)['response']['file_info']
        if int(info['size']) != size or info['hash'].lower() != sha:
            raise ValueError('preserved part metadata drift')
        normal = info['links']['normal_download']
        if urllib.parse.urlparse(normal).hostname not in ('www.mediafire.com', 'mediafire.com'):
            raise ValueError('unexpected metadata host')
        with opener.open(urllib.request.Request(normal, headers=ua), timeout=60) as response:
            page = response.read(4*1024*1024).decode('utf-8', 'replace')
            referer = response.geturl()
        path = work/f'part.{number:03d}'
        with opener.open(urllib.request.Request(direct_link(page), headers={**ua, 'Referer': referer}), timeout=180) as response, path.open('wb') as output:
            total = 0
            while block := response.read(1024*1024):
                total += len(block)
                if total > size:
                    raise ValueError('download exceeds fixed original part size')
                output.write(block)
        if rehash(path) != {'bytes': size, 'sha256': sha}:
            raise ValueError('downloaded part SHA/size mismatch')
        parts.append({'key': key, 'bytes': size, 'sha256': sha, 'historical_filename': info['filename']})
        print(f'preserved mixed25 part {number}/2 verified', flush=True)
    bundle = work/'bundle.rar'
    with bundle.open('wb') as output:
        for number in (1, 2):
            with (work/f'part.{number:03d}').open('rb') as part:
                while block := part.read(1024*1024):
                    output.write(block)
    if rehash(bundle) != {'bytes': 361255180, 'sha256': BUNDLE_SHA}:
        raise ValueError('assembled preserved bundle mismatch')
    subprocess.run(['unar', '-f', '-o', str(work/'out'), str(bundle)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
    clients = [p for p in (work/'out').rglob('stoneage2.5')
               if p.is_dir() and p.parent.name == 'SA2.5主程式']
    if len(clients) != 1:
        raise ValueError('mixed bundle has no unique original client namespace')
    return clients[0], parts


def acquire(work, output):
    validate_tw85()
    if digest((ROOT/REPORT).read_bytes()) != TW85_SHA:
        raise ValueError('qualified TW85 layer report drift')
    reference = json.loads((ROOT/REPORT).read_bytes())
    expected = expected_files()
    work.mkdir(parents=True, exist_ok=True)
    client, parts = download_bundle(work)
    result = compare_directory(client, reference, expected)
    if (result['counts']['mixed25_present_paths'], result['counts']['mixed25_absent_paths']) != (35, 7):
        raise ValueError('unexpected qualified cross-version coverage')
    result.update(schema='stoneage.tw85_mixed25_map_plane_diff.r1', task='CLIENT-MAP-CROSS-VERSION-PLANE-DIFF-04',
                  source_class='MIXED_COMMUNITY_BRIDGE_NOT_AUTHENTICATED_OFFICIAL_25',
                  source_pins={p: pin(ROOT/p) for p in (REPORT, BRIDGE)},
                  bundle_sha256=BUNDLE_SHA, bundle_bytes=361255180, acquired_parts=parts,
                  tw85_source_bytes_reused_from_qualified_permanent_layer_metadata=True,
                  boundaries={key: False for key in ('tw85_package_redownloaded', 'game_or_installer_executed',
                      'same_named_place_proven', 'official_patch_chronology_proven', 'changed_cells_computed',
                      'plane_runtime_semantics_proven', 'npc_quest_or_spawn_tables_recovered',
                      'original_payload_published', 'full_world_map_completion_proven')})
    output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)+'\n')
    print(json.dumps(result['counts'], sort_keys=True), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    acquire(args.work.resolve(), args.output.resolve())
