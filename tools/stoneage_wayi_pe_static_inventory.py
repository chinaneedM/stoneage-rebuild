"""Bounded offline PE32 inventory; records static observations, never executes.

Works on packed archive responses and separately labelled decompressed outputs.
Header dates and resource strings are mutable; neither authenticates a release.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import struct

MAX_BYTES = 8 * 1024 * 1024
VERSION_KEYS = ('FileVersion', 'ProductVersion', 'ProductName', 'FileDescription',
                'OriginalFilename', 'InternalName', 'CompanyName')
MARKERS = ('ClientLogin', 'CharLogin', 'SaUpdate', 'StoneAge2.exe',
           'stoneage.wayi.com.tw', '/saupdate/sa70a/newest7x.txt',
           '/saupdate/newest6.txt', 'data\\adrn_%d.bin', 'data\\savedata.dat')


def version_candidates(data: bytes) -> list[dict]:
    rows = []
    for key in VERSION_KEYS:
        encoded = (key + '\0').encode('utf-16le')
        for match in re.finditer(re.escape(encoded), data):
            start = match.start() - 6
            if start < 0 or start % 4:
                continue
            length, value_units, kind = struct.unpack_from('<HHH', data, start)
            value_start = (match.end() + 3) & ~3
            end = value_start + value_units * 2
            if kind != 1 or not value_units or length > len(data) - start:
                continue
            if end > start + length or value_start < start + 6:
                continue
            raw = data[value_start:end]
            if not raw.endswith(b'\0\0'):
                continue
            try:
                value = raw[:-2].decode('utf-16le', errors='strict')
            except UnicodeError:
                continue
            if '\0' in value:
                continue
            rows.append({'key': key, 'value': value, 'block_file_offset': start})
    return rows


def inventory_pe(payload: bytes) -> dict:
    if not 64 <= len(payload) <= MAX_BYTES or payload[:2] != b'MZ':
        raise ValueError('Expected bounded DOS/PE file')
    offset = struct.unpack_from('<I', payload, 0x3c)[0]
    if offset < 64 or offset + 24 > len(payload) or payload[offset:offset+4] != b'PE\0\0':
        raise ValueError('Invalid PE header')
    machine, count, stamp = struct.unpack_from('<HHI', payload, offset+4)
    optional_size = struct.unpack_from('<H', payload, offset+20)[0]
    optional = offset+24
    table = optional+optional_size
    if machine != 0x14c or not 1 <= count <= 96 or optional_size < 96:
        raise ValueError('Expected i386 PE32 and bounded section count')
    if table + count*40 > len(payload) or struct.unpack_from('<H', payload, optional)[0] != 0x10b:
        raise ValueError('Truncated section table or non-PE32')
    sections = []
    for index in range(count):
        entry = table+index*40
        name = payload[entry:entry+8].rstrip(b'\0').decode('ascii', errors='strict')
        virtual_size, rva, raw_size, raw_offset = struct.unpack_from('<IIII', payload, entry+8)
        if raw_size and (raw_offset < table+count*40 or raw_size > len(payload)-raw_offset):
            raise ValueError('Section raw range outside file')
        sections.append({'name': name, 'rva': rva, 'virtual_size': virtual_size,
                         'raw_offset': raw_offset, 'raw_size': raw_size})
    markers = []
    for marker in MARKERS:
        for encoding in ('ascii', 'utf-16le'):
            encoded = marker.encode(encoding)
            positions = [m.start() for m in re.finditer(re.escape(encoded), payload)]
            if positions:
                markers.append({'text': marker, 'encoding': encoding, 'file_offsets': positions})
    return {'response_bytes': len(payload), 'response_sha256': hashlib.sha256(payload).hexdigest(),
            'machine': 'i386', 'format': 'PE32', 'coff_timestamp': stamp,
            'coff_timestamp_utc_untrusted': datetime.fromtimestamp(stamp, timezone.utc).isoformat(),
            'sections': sections, 'upx_section_names_present': any(s['name'].startswith('UPX') for s in sections),
            'version_string_candidates_untrusted': version_candidates(payload), 'static_markers': markers,
            'file_executed': False, 'publisher_original_hash_verified': False,
            'release_version_proven': False, 'native_pet_runtime_verified': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('local_pe', type=Path)
    args = parser.parse_args()
    with args.local_pe.open('rb') as stream:
        payload = stream.read(MAX_BYTES+1)
    print(json.dumps(inventory_pe(payload), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
