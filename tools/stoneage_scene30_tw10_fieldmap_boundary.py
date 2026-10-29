"""Bound the retail/installer field-map search; never execute original programs.

Public mode rederives a report from immutable historical derived evidence.
Optional private mode hashes ALL 375 retained original members and proves the
eight omitted retail members are installer support, not missing world maps.
No proprietary content or local source paths are emitted.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'research/recovered/STONEAGE-SCENE30-TW10-FIELDMAP-BOUNDARY-R1.json'
PREFIX = 'research/recovered/'
PINS = {
 'STONEAGE-TW10-CLIENT-INVENTORY-R1.txt': '413d197d19ea405490bfffc2bdbf021089177671445ca567533b2eb2576dae7b',
 'STONEAGE-TW10-INSTALLSHIELD-R1.txt': 'f54136b5ddd67c01e7ce93f6bfc67169e1eb3b05b7bee8e289f9f854b7fc697b',
 'STONEAGE-TW10-RECEIVE-MAP-JOIN-R1.txt': 'f9989640efa9ee50379d294e284bc96a1f5223d92e688d27464b4a6a0d12d65e',
}
ZIP_SHA = '3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24'
AUDIT_PATH = PREFIX + 'STONEAGE-SCENE30-PRIVATE-SOURCE-AUDIT-R1.json'
AUDIT_SHA = 'd84ebae2680e544d7bfb3611e2e3d1add95136795b55488580f44385a076755e'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def records(text, kind):
    return [dict(s.split('=', 1) for s in line.split('|')[1:])
            for line in text.splitlines() if line.startswith(kind + '|')]

def inputs():
    result = {}
    for name, expected in PINS.items():
        data = (ROOT / PREFIX / name).read_bytes()
        require(digest(data) == expected, 'historical source changed: ' + name)
        result[name] = data.decode('utf-8')
    return result

def core_records(source):
    rows = records(source, 'CORE_FILE')
    require(len(rows) == 383 and len({r['path'] for r in rows}) == 383,
            'complete unique retail core required')
    require(sum(int(r['size']) for r in rows) == 373564663, 'retail byte accounting')
    return rows

def derive():
    source = inputs()
    rows = core_records(source[next(iter(PINS))])
    installer = source['STONEAGE-TW10-INSTALLSHIELD-R1.txt']
    installed = records(installer, 'INSTALLED_FILE')
    support = [r for r in rows if r['category'] == 'installer_support']
    dats = [r['path'] for r in rows if r['path'].lower().endswith('.dat')]
    require(dats == ['StoneAge/data/savedata.dat'], 'unexpected retail DAT: reopen search')
    require(not any('map' == p.lower() for r in rows for p in PurePosixPath(r['path']).parts),
            'retail field-map directory: reopen search')
    require(len(installed) == 13 and len({r['path'] for r in installed}) == 13,
            'installer extraction completeness')
    require(sum(int(r['size']) for r in installed) == 1374113, 'installer byte accounting')
    require(all(r['map_like'] == '0' for r in installed), 'installer map: reopen search')
    require(records(installer, 'UNSHIELD') == [{'list_rc': '0', 'extract_rc': '0'}],
            'historical extraction must have succeeded')
    targets = records(installer, 'TARGET')
    bypath = {r['path']: r for r in rows}
    require(len(targets) == 7 and len({r['path'] for r in targets}) == 7,
            'installer target coverage')
    for r in targets:
        require(all(bypath[r['path']][k] == r[k] for k in ('size', 'sha256')),
                'installer and retail provenance differ')
    join = source['STONEAGE-TW10-RECEIVE-MAP-JOIN-R1.txt']
    signatures = records(join, 'MAP_XREF_SIGNATURE')
    require(len(signatures) == 6, 'six static map paths required')
    modes = {r['name']: [] for r in records(join, 'MAP_CALLBACK_XREF_JOIN')}
    for r in records(join, 'MAP_SEMANTIC_MODE'):
        modes[r['name']].append(r['mode'])
    require(modes == {'MC': ['rb', 'wb', 'rb'], 'M': ['rb+', 'wb', 'rb+']},
            'receive-side map update/read distinction lost')
    audit_bytes = (ROOT / AUDIT_PATH).read_bytes()
    require(digest(audit_bytes) == AUDIT_SHA, 'archived local source receipt changed')
    return {
      'schema': 'stoneage.scene30.tw10_fieldmap_boundary.r1',
      'scope': 'REVIEW_OF_EXISTING_PINNED_EVIDENCE_NOT_NEW_DISC_EXTRACTION',
      'sources': [{'path': PREFIX + n, 'sha256': h} for n, h in PINS.items()],
      'archived_local_original_audit': {'path': AUDIT_PATH, 'sha256': AUDIT_SHA,
        'public_ci_reexecutes_private_source': False},
      'retail': {'namespace': 'Joliet', 'disc_files': 411, 'core_files': len(rows),
        'core_bytes': sum(int(r['size']) for r in rows), 'only_core_dat': dats,
        'field_map_files': 0, 'battle_sab_files': sum(r['path'].lower().endswith('.sab') for r in rows)},
      'installer': {'core_support_files': support, 'source_targets_crosschecked': len(targets),
        'historical_extracted_files': len(installed), 'historical_extracted_bytes': 1374113,
        'historical_map_like_files': 0, 'new_installer_execution': False,
        'script_dynamic_behavior_fully_proven': False},
      'map_delivery': {'evidence': 'ORIGINAL_BINARY_STATIC_PATH_NOT_LIVE_SERVER_CAPTURE',
        'joins': records(join, 'MAP_CALLBACK_XREF_JOIN'), 'file_mode_sequences': modes,
        'six_file_path_signatures': signatures, 'live_server_payload_obtained': False},
      'decision': 'STOP_REDOWNLOADING_IDENTICAL_RETAIL_DISC_FOR_PREINSTALLED_FIELD_DAT',
      'reopen_only_with': ['source-qualified same-build installed map cache or captured M payload',
        'authenticated same-build server map data', 'different explicitly qualified carrier with actual map bytes'],
      'original_world_entered': False, 'new_historical_map_payloads': 0,
      'later_mixed25_map_is_tw10_official_world': False, 'overall_percent': None,
    }

def audit_private(path):
    with path.open('rb') as f:
        require(hashlib.file_digest(f, 'sha256').hexdigest() == ZIP_SHA, 'private parent SHA')
    rows = core_records(inputs()['STONEAGE-TW10-CLIENT-INVENTORY-R1.txt'])
    expected = {'source/' + r['path'].split('/', 1)[1]: r for r in rows
                if r['category'] != 'installer_support'}
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), 'duplicate ZIP members')
        source_names = {n for n in names if n.startswith('source/') and not n.endswith('/')}
        require(source_names == set(expected), 'private source member coverage')
        total = 0
        for name, r in expected.items():
            with z.open(name) as f:
                actual = hashlib.file_digest(f, 'sha256').hexdigest()
            require(z.getinfo(name).file_size == int(r['size']) and actual == r['sha256'],
                    'original member identity: ' + name)
            total += int(r['size'])
        exe = z.read('source/sa_3.exe')
        require(exe.count(b'map\\%d.dat\0') == 1, 'original runtime map-cache literal')
        # Finite original-byte corroboration, not a new generic disassembler.
        pe = struct.unpack_from('<I', exe, 60)[0]
        require(exe[pe:pe + 4] == b'PE\0\0', 'original PE header')
        optional = pe + 24
        image_base = struct.unpack_from('<I', exe, optional + 28)[0]
        section_start = optional + struct.unpack_from('<H', exe, pe + 20)[0]
        sections = []
        for i in range(struct.unpack_from('<H', exe, pe + 6)[0]):
            start = section_start + i * 40
            name = exe[start:start + 8].rstrip(b'\0')
            _, rva, size, offset = struct.unpack_from('<IIII', exe, start + 8)
            sections.append((name, rva, size, offset))
        literal_offset = exe.index(b'map\\%d.dat\0')
        _, rva, _, offset = next(s for s in sections if s[3] <= literal_offset < s[3] + s[2])
        literal_va = image_base + rva + literal_offset - offset
        needle = b'\x68' + struct.pack('<I', literal_va)  # x86 PUSH imm32
        _, text_rva, text_size, text_offset = next(s for s in sections if s[0] == b'.text')
        text = exe[text_offset:text_offset + text_size]
        sites = [text_rva + i for i in range(len(text)) if text.startswith(needle, i)]
        expected_sites = [int(r['rva'], 16) for r in records(
            inputs()['STONEAGE-TW10-RECEIVE-MAP-JOIN-R1.txt'], 'MAP_FILE_XREF')]
        require(sites == expected_sites, 'original six static map-pointer sites differ')
    return {'schema': 'stoneage.scene30.private_source_audit.r1', 'parent_zip_sha256': ZIP_SHA,
      'parent_zip_bytes': path.stat().st_size, 'original_members_fully_hashed': len(expected),
      'original_member_bytes_hashed': total, 'all_match_complete_retail_inventory': True,
      'omitted_retail_members': [r['path'] for r in rows if r['category'] == 'installer_support'],
      'ordinary_world_map_members': 0, 'runtime_map_cache_literal_occurrences': 1,
      'original_static_push_map_pointer_rvas': [hex(s) for s in sites],
      'pointer_scan_is_not_control_flow_or_runtime_replay': True,
      'source_action_run_id': None, 'original_executable_executed': False,
      'new_cd_or_installer_extraction': False, 'original_world_entered': False}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--original-zip', type=Path)
    args = ap.parse_args()
    report = derive()
    if args.write:
        OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    else:
        require(json.loads(OUT.read_text()) == report, 'published report semantic mismatch')
    if args.original_zip:
        print(json.dumps(audit_private(args.original_zip), ensure_ascii=False, indent=2))
    else:
        print('SCENE30 pinned retail + installer + static map delivery review: PASS; no raw-source CI')

if __name__ == '__main__':
    main()
