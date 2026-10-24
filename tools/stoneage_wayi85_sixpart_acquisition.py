"""Acquire a community-preserved claimed Wayi installer; never execute it.

MediaFire hashes qualify carrier integrity, not publisher authenticity. Original
parts remain in the requested work directory; only derived reports belong in Git.
"""
import argparse
import hashlib
import html
import http.cookiejar
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.parse
import urllib.request

from tools.stoneage_cross_version_file_inventory import scan, normalize_name
from tools.stoneage_tw10_preserved25_file_intersection import replay, GIT_BLOBS, ROOT

KEYS = ['l5i274801ov19w7', 'g9b3g3hjmwwttg3', 'e859n1nm1tk12j8',
        '69vrzm3nox8f0v9', 'clbwjkcqqhxq6k9', '42uy5b9abbcu4qr']
STEM = 'STONEAGE20060616.exe'
UA = 'Mozilla/5.0'
MAX_PART = 300 * 1024 * 1024


def check_metadata(info, number):
    name = info.get('filename', '')
    if name != f'{STEM}.{number:03d}':
        raise ValueError('carrier filename drift: ' + name)
    size = int(info.get('size', 0))
    digest = str(info.get('hash', '')).lower()
    if not 0 < size <= MAX_PART or not re.fullmatch('[0-9a-f]{64}', digest):
        raise ValueError('missing exact carrier size or SHA256')
    normal = info.get('links', {}).get('normal_download', '')
    if urllib.parse.urlparse(normal).hostname not in ('www.mediafire.com', 'mediafire.com'):
        raise ValueError('unexpected public carrier host')
    return {'part': number, 'key': KEYS[number-1], 'filename': name,
            'service_bytes': size, 'service_sha256': digest,
            'created_label': info.get('created'), 'normal_download': normal}


def direct_link(page):
    m = re.search(r'id="downloadButton"[^>]*href="([^"]+)"', page, re.I | re.S)
    if not m:
        m = re.search(r'(https://download\d+\.mediafire\.com/[^"\'<> ]+)', page, re.I)
    if not m:
        raise ValueError('public carrier download link unavailable')
    link = html.unescape(m.group(1))
    host = urllib.parse.urlparse(link).hostname or ''
    if not re.fullmatch(r'download\d+\.mediafire\.com', host):
        raise ValueError('unexpected payload host')
    return link


def rehash(path):
    h = hashlib.sha256()
    size = 0
    with path.open('rb') as f:
        while block := f.read(1024*1024):
            h.update(block)
            size += len(block)
    return {'bytes': size, 'sha256': h.hexdigest()}


def download_part(opener, meta, work):
    path = work / meta['filename']
    expected = {'bytes': meta['service_bytes'], 'sha256': meta['service_sha256']}
    if path.exists() and rehash(path) == expected:
        return {**meta, **expected, 'reused_verified_local_part': True}
    req = urllib.request.Request(meta['normal_download'], headers={'User-Agent': UA})
    with opener.open(req, timeout=60) as r:
        page = r.read(4*1024*1024).decode('utf-8', 'replace')
        referer = r.geturl()
    req = urllib.request.Request(direct_link(page), headers={'User-Agent': UA, 'Referer': referer})
    temporary = path.with_suffix(path.suffix+'.partial')
    with opener.open(req, timeout=180) as r, temporary.open('wb') as f:
        total = 0
        while block := r.read(1024*1024):
            total += len(block)
            if total > meta['service_bytes']:
                raise ValueError('download longer than exact service metadata')
            f.write(block)
    actual = rehash(temporary)
    if actual != expected:
        raise ValueError('downloaded part differs from carrier SHA256/length')
    temporary.replace(path)
    return {**meta, **actual, 'reused_verified_local_part': False}


def assemble(parts, work):
    if [p['part'] for p in parts] != list(range(1, 7)):
        raise ValueError('six ordered parts required')
    path = work / STEM
    with path.open('wb') as out:
        for p in parts:
            source = work / p['filename']
            if rehash(source) != {'bytes': p['bytes'], 'sha256': p['sha256']}:
                raise ValueError('part changed before concatenation')
            with source.open('rb') as f:
                while block := f.read(1024*1024):
                    out.write(block)
    return path


def safe_7z_members(text):
    if '----------\n' not in text:
        raise ValueError('7zip member section unavailable')
    members = []
    seen = set()
    for section in text.split('----------\n', 1)[1].strip().split('\n\n'):
        values = dict(line.split(' = ', 1) for line in section.splitlines() if ' = ' in line)
        if 'Path' not in values:
            continue
        name = normalize_name(values['Path'])
        if any('link' in k.lower() for k in values):
            raise ValueError('archive links refused')
        if name.casefold() in seen:
            raise ValueError('archive case-insensitive path collision')
        seen.add(name.casefold())
        size = int(values.get('Size', 0))
        if not 0 <= size <= 4*1024**3:
            raise ValueError('archive member length invalid')
        members.append({'path': name, 'bytes': size, 'attributes': values.get('Attributes')})
    if not members or sum(p['bytes'] for p in members) > 16*1024**3:
        raise ValueError('empty or excessive extracted tree')
    return members


def inspect_installer(installer, work):
    output = {'installed_or_executed': False, 'publisher_authenticity_proven': False}
    with installer.open('rb') as f:
        header = f.read(4096)
    output['mz_header_present'] = header.startswith(b'MZ')
    listing = subprocess.run(['7z', 'l', '-slt', str(installer)], capture_output=True, text=True, timeout=120)
    dest = work / 'extracted'
    dest.mkdir(exist_ok=True)
    if listing.returncode == 0:
        output['archive_members'] = safe_7z_members(listing.stdout)
        subprocess.run(['7z', 'x', '-y', '-o'+str(dest), str(installer)], check=True, stdout=subprocess.DEVNULL, timeout=600)
        output['extractor'] = '7zip archive parser; executable not run'
    else:
        trial = subprocess.run(['innoextract', '--test', str(installer)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
        if trial.returncode:
            output['extraction_status'] = 'UNSUPPORTED_INSTALLER_CONTAINER'
            output['sevenzip_return_code'] = listing.returncode
            output['innoextract_return_code'] = trial.returncode
            return output
        subprocess.run(['innoextract', '--silent', '-e', '-d', str(dest), str(installer)], check=True, timeout=600)
        output['extractor'] = 'innoextract archive parser; executable not run'
    inventory = scan({'schema': 'stoneage.cross_version_input_r1', 'samples': [{
        'sample_id': 'TW85-SIXPART-CANDIDATE', 'local_path': str(dest), 'kind': 'directory',
        'source_class': 'UNVERIFIED_CANDIDATE', 'region': 'TW_CLAIMED', 'claimed_version': '8.5_COMMUNITY_CLAIM',
        'evidence_ref': 'research/recovered/STONEAGE-WAYI-85-SIXPART-METADATA-R1.json'}]})
    output['extraction_status'] = 'EXTRACTED_AND_HASHED'
    output['inventory'] = inventory
    baseline = replay()
    old = baseline['matched'] + baseline['unmatched']
    by_hash = {}
    for file in inventory['samples'][0]['files']:
        by_hash.setdefault(file['sha256'], []).append(file['path'])
    output['tw10_exact_file_matches'] = [{**p, 'candidate_paths': by_hash[p['sha256']]} for p in old if p['sha256'] in by_hash]
    output['tw10_source_manifest_git_blobs'] = GIT_BLOBS
    return output


def acquire(work, output):
    work.mkdir(parents=True, exist_ok=True)
    report = {'schema': 'stoneage.wayi85_sixpart_acquisition_r1',
              'classification': 'UNVERIFIED_COMMUNITY_PRESERVED_CLAIMED_WAYI85_INSTALLER',
              'historical_metadata_path': 'research/recovered/STONEAGE-WAYI-85-SIXPART-METADATA-R1.json',
              'github_run_id': os.environ.get('GITHUB_RUN_ID'), 'github_head_sha': os.environ.get('GITHUB_SHA'),
              'parts': [], 'status': 'STARTED', 'original_payload_published': False,
              'official_clean_client_authenticated': False, 'server_quest_pet_data_inferred': False}
    output.parent.mkdir(parents=True, exist_ok=True)
    def checkpoint():
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)+'\n')
    checkpoint()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    try:
        for number, key in enumerate(KEYS, 1):
            data = urllib.parse.urlencode({'quick_key': key, 'response_format': 'json'}).encode()
            req = urllib.request.Request('https://www.mediafire.com/api/1.5/file/get_info.php', data=data, headers={'User-Agent': UA})
            with opener.open(req, timeout=60) as r:
                info = json.load(r)['response']['file_info']
            meta = check_metadata(info, number)
            report['parts'].append(download_part(opener, meta, work))
            checkpoint()
            print(f'part {number}/6 verified: {meta["service_bytes"]} bytes', flush=True)
        installer = assemble(report['parts'], work)
        report['assembled_installer'] = {'filename': STEM, **rehash(installer)}
        report['status'] = 'ALL_SIX_PARTS_DOWNLOADED_AND_ASSEMBLED'
        checkpoint()
        report['inspection'] = inspect_installer(installer, work)
        report['status'] = 'BYTE_ACQUISITION_AND_STATIC_INSPECTION_COMPLETE'
    except Exception as exc:
        report['status'] = 'BOUNDED_ACQUISITION_OR_INSPECTION_FAILURE'
        # Avoid temporary signed payload URLs in permanent derived reports.
        report['error'] = {'type': type(exc).__name__, 'message': re.sub(r'https?://\S+', '[URL omitted]', str(exc))[:500]}
        checkpoint()
        raise
    checkpoint()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    acquire(args.work.resolve(), args.output.resolve())
