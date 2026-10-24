"""Static, bounded extraction of the pinned Wayi InstallShield 10.5 stream.

Format/decode reference: lifenjoiner ISx, mirrored at Coldblackice/
InstallShield-installer-extractor-ISx, commit 3c4177ddd0519244490ff8e78d380110c8dacdc8.
This Python implementation reads only that hash-qualified wrapper, extracts
MSI/INI data, and invokes msitools as a data parser; no installer is executed.

MIT License
Copyright (c) 2017 lifenjoiner
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import hashlib
from pathlib import Path
import struct
import subprocess

from tools.stoneage_cross_version_file_inventory import scan, normalize_name

WRAPPER_SHA256 = '971780abc65ed29a6a7aeb1a528c7db2ef07b11a188e56deaef90a54986609f5'
MSI_SHA256 = '8f99ceb13eb91fa9231bf1b6ee2c7052df97d59425171c03103732f8795a4bdc'
NIBBLES = bytes(((x & 15) << 4) | (x >> 4) for x in range(256))
XOR = [bytes(x ^ k ^ 255 for x in range(256)) for k in range(256)]


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        while block := f.read(1024*1024):
            h.update(block)
    return h.hexdigest()


def decode_blocks(raw, filename):
    """Nibble swap + filename-derived XOR, with key phase reset every 1024B."""
    magic = bytes.fromhex('13358607')
    name = filename.encode('ascii')
    if not name:
        raise ValueError('empty decode filename')
    key = bytes(x ^ magic[i % 4] for i, x in enumerate(name))
    result = bytearray(raw.translate(NIBBLES))
    for pos in range(min(1024, len(raw))):
        result[pos::1024] = result[pos::1024].translate(XOR[key[pos % len(key)]])
    return bytes(result)


def extract_stream(wrapper, destination):
    if wrapper.stat().st_size != 1145465184 or sha(wrapper) != WRAPPER_SHA256:
        raise ValueError('unqualified InstallShield wrapper')
    destination.mkdir(parents=True, exist_ok=True)
    entries = []
    seen = set()
    with wrapper.open('rb') as f:
        f.seek(0x3e000)
        header = f.read(46)
        if header[:14] != b'InstallShield\x00' or struct.unpack_from('<H', header, 14)[0] != 8:
            raise ValueError('unexpected stream header')
        for _ in range(8):
            attr = f.read(312)
            if len(attr) != 312:
                raise ValueError('truncated file attributes')
            name = normalize_name(attr[:260].split(b'\0', 1)[0].decode('ascii'))
            flags = struct.unpack_from('<I', attr, 260)[0]
            length = struct.unpack_from('<I', attr, 268)[0]
            unicode = struct.unpack_from('<H', attr, 280)[0]
            if name.casefold() in seen or unicode or flags not in (0, 6):
                raise ValueError('unsupported flags/name in pinned stream')
            seen.add(name.casefold())
            start = f.tell()
            if start+length > wrapper.stat().st_size:
                raise ValueError('file extent outside wrapper')
            entry = {'path': name, 'encoded_bytes': length, 'wrapper_offset': start, 'flags': flags}
            if name in ('StoneAge85.msi', 'Setup.ini'):
                target = destination / name
                left = length
                with target.open('wb') as out:
                    while left:
                        raw = f.read(min(left, 1024*1024))
                        if not raw:
                            raise ValueError('truncated encoded stream')
                        out.write(decode_blocks(raw, name) if flags == 6 else raw)
                        left -= len(raw)
                entry['decoded_sha256'] = sha(target)
            else:
                f.seek(length, 1)
            entries.append(entry)
    msi = destination / 'StoneAge85.msi'
    if not msi.is_file() or sha(msi) != MSI_SHA256:
        raise ValueError('decoded MSI does not match independently archived Windows ISx result')
    return entries


def extract_client(wrapper, work):
    parts = extract_stream(wrapper, work/'installshield-data')
    msi = work/'installshield-data/StoneAge85.msi'
    tables = {}
    for table in ('Property', 'File', 'Directory', 'Component', 'Media'):
        r = subprocess.run(['msiinfo', 'export', str(msi), table], capture_output=True, text=True, check=True, timeout=120)
        tables[table] = r.stdout
    dest = work/'msi-client'
    dest.mkdir(exist_ok=True)
    subprocess.run(['msiextract', '-C', str(dest), str(msi)], check=True, stdout=subprocess.DEVNULL, timeout=900)
    inventory = scan({'schema': 'stoneage.cross_version_input_r1', 'samples': [{
        'sample_id': 'TW85-INSTALLER-MSI-CLIENT', 'kind': 'directory', 'local_path': str(dest),
        'source_class': 'PROVENANCE_SUPPORTED_CANDIDATE', 'region': 'TW',
        'claimed_version': '8.50.0000_MSI_PRODUCT',
        'evidence_ref': 'research/recovered/STONEAGE-WAEI85-ISX-WINDOWS-R1.txt'}]})
    files = inventory['samples'][0]['files']
    return {'extraction_status': 'CLIENT_MSI_PAYLOAD_EXTRACTED_AND_HASHED',
            'installed_or_executed': False, 'publisher_authenticity_proven': False,
            'wrapper_sha256': WRAPPER_SHA256, 'msi_sha256': MSI_SHA256,
            'static_extractor_reference': 'ISx 3c4177ddd0519244490ff8e78d380110c8dacdc8 format; independent Python decoder + msitools',
            'stream_entries': parts, 'msi_tables': tables, 'inventory': inventory,
            'map_dat_files': [x for x in files if '/map/' in '/'+x['path'].lower() and x['path'].lower().endswith('.dat')],
            'graphics_animation_files': [x for x in files if x['family_hint'] == 'GRAPHICS_OR_ANIMATION_CONTAINER'],
            'package_date_not_filename_token': True,
            'original_server_quest_pet_master_data_proven': False}
