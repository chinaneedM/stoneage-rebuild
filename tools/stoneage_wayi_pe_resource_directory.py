"""Bounded original packed PE resource declarations; no executable code runs."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
from tools.stoneage_wayi_pe_static_inventory import inventory_pe

SHA = '4b5a059b45b589b609ca925d210d76838be1e970b805fab3df863b7d563fbb38'
URL = 'https://web.archive.org/web/20060915184620id_/http://www.wayi.com.tw:80/download/file/onlineGame/sa.exe'
UNPACKED_SHA = '4193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63'


def inspect(data, require_source=True):
    meta = inventory_pe(data)
    if require_source and (len(data) != 369152 or meta['response_sha256'] != SHA):
        raise ValueError('unexpected official-path specimen')
    pe = struct.unpack_from('<I', data, 60)[0]
    optional = pe + 24
    optional_size = struct.unpack_from('<H', data, pe + 20)[0]
    if optional_size < 120 or struct.unpack_from('<I', data, optional + 92)[0] < 3:
        raise ValueError('no resource data directory')
    rva, size = struct.unpack_from('<II', data, optional + 112)
    if not rva or not 16 <= size <= len(data):
        raise ValueError('invalid resource directory extent')

    def mapping(address, length):
        hits = [(s, s['raw_offset'] + address - s['rva']) for s in meta['sections']
                if s['rva'] <= address and address + length <= s['rva'] + s['raw_size']]
        if len(hits) != 1:
            raise ValueError('ambiguous or nonresident RVA')
        return hits[0]

    section, base = mapping(rva, size)
    if section['name'].startswith('UPX'):
        raise ValueError('resource directory itself packed')
    seen = set()
    rows = []

    def bounded(offset, length):
        if offset < 0 or length < 0 or offset + length > size:
            raise ValueError('resource directory relative range escaped')
        return base + offset

    def walk(offset, parts):
        if offset in seen or len(parts) > 2:
            raise ValueError('cyclic, aliased or overdeep resource directory')
        seen.add(offset)
        p = bounded(offset, 16)
        named, ids = struct.unpack_from('<HH', data, p + 12)
        count = named + ids
        bounded(offset + 16, 8 * count)
        names = set()
        for i in range(count):
            name, child = struct.unpack_from('<II', data, p + 16 + 8 * i)
            if name & 0x80000000:
                string_offset = name & 0x7fffffff
                units = struct.unpack_from('<H', data, bounded(string_offset, 2))[0]
                start = bounded(string_offset + 2, units * 2)
                name = data[start:start + units * 2].decode('utf-16le', 'strict')
            if name in names:
                raise ValueError('duplicate resource key')
            names.add(name)
            if child & 0x80000000:
                walk(child & 0x7fffffff, parts + [name])
                continue
            if len(parts) != 2:
                raise ValueError('resource leaf at unexpected depth')
            address, length, codepage, reserved = struct.unpack_from('<IIII', data, bounded(child, 16))
            if not length or reserved:
                raise ValueError('invalid leaf declaration')
            target, file_offset = mapping(address, length)
            # A numeric RVA mapping into packed bytes cannot establish resource
            # payload identity, even when its raw file range happens to exist.
            qualified = target['name'] == section['name'] and not target['name'].startswith('UPX')
            rows.append({'path': parts + [name], 'declared_rva': address,
                'declared_bytes': length, 'codepage_field': codepage,
                'mapped_section': target['name'],
                'payload_status': 'DIRECT_RSRC_BYTES' if qualified else 'PACKED_SECTION_UNQUALIFIED',
                'payload_file_offset': file_offset if qualified else None,
                'payload_sha256': hashlib.sha256(data[file_offset:file_offset+length]).hexdigest() if qualified else None})

    walk(0, [])
    return {'schema': 'stoneage.wayi_packed_pe_resource_directory.r1',
        'source_url': URL if require_source else None,
        'source_bytes': len(data), 'source_sha256': meta['response_sha256'],
        'directory_rva': rva, 'directory_bytes': size, 'entries': rows,
        'entry_count': len(rows), 'direct_payload_count': sum(x['payload_status'] == 'DIRECT_RSRC_BYTES' for x in rows),
        'declared_menu_dialog_string_types': sorted(set(x['path'][0] for x in rows) & {4, 5, 6}),
        'absence_proves_no_game_ui': False,
        'program_executed': False, 'input_has_upx_sections': meta['upx_section_names_present'],
        'login_screen_recovered': False, 'same_build_tw10_or_jss1999': False}


def audit_pair(packed, unpacked):
    before = inspect(packed)
    if len(unpacked) != 921600 or hashlib.sha256(unpacked).hexdigest() != UNPACKED_SHA:
        raise ValueError('unpacked original specimen mismatch')
    after = inspect(unpacked, False)
    if after['input_has_upx_sections']:
        raise ValueError('unpacked specimen still packed')
    old = {tuple(e['path']): e for e in before['entries']}
    new = {tuple(e['path']): e for e in after['entries']}
    if set(old) != set(new) or any(old[k]['declared_bytes'] != new[k]['declared_bytes'] for k in old):
        raise ValueError('packed/unpacked resource membership changed')
    if any(e['payload_status'] != 'DIRECT_RSRC_BYTES' for e in new.values()):
        raise ValueError('unpacked resources not directly qualified')
    if any(e['payload_sha256'] != new[k]['payload_sha256'] for k,e in old.items()
           if e['payload_status'] == 'DIRECT_RSRC_BYTES'):
        raise ValueError('resident resources changed on decompression')
    rc = new[(10,156,1028)]
    start = rc['payload_file_offset']
    body = unpacked[start:start + rc['declared_bytes']]
    nested = inventory_pe(body)
    return {'schema': 'stoneage.wayi_saexe_resource_content.r1',
        'task': 'WAYI-OFFICIAL-SAEXE-LOGIN-RESOURCE-CONTENT-11',
        'packed': before, 'unpacked': after,
        'same_resource_paths_and_lengths': True,
        'previously_direct_payloads_unchanged': True,
        'rcdata_observation': {'path': [10,156,1028], 'bytes': len(body),
            'sha256': nested['response_sha256'], 'format': nested['format'],
            'machine': nested['machine'], 'section_count': len(nested['sections']),
            'has_porttalk_pdb_marker': b'porttalk.pdb' in body.lower(),
            'has_nt_kernel_import_name': b'ntoskrnl.exe' in body.lower(),
            'driver_loaded_or_executed': False},
        'new_ui_labels_recovered': 0,
        'login_scene_assets_or_runtime_proven': False,
        'raw_originals_committed': False,
        'next': 'OFFICIAL-CLIENT-LOGIN-SCENE-ASSET-BINDING-12'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--unpacked', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.source.open('rb') as f:
        data = f.read(8 * 1024 * 1024 + 1)
    with args.unpacked.open('rb') as f:
        unpacked = f.read(8 * 1024 * 1024 + 1)
    args.output.write_text(json.dumps(audit_pair(data, unpacked), indent=2, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
