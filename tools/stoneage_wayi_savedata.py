"""Hash-pinned settings archaeology and independent bounded synthetic model.

No original program execution or actual settings files. Safe model bounds do
not imply native guards; arbitrary key, aliasing and malformed native IO excluded.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM, X86_OP_MEM
from tools.stoneage_jss_launcher_deep_probe import parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import parse_imports
from tools.stoneage_wayi_pet_sender_probe import EXPECTED_BYTES, EXPECTED_SHA256
from tools.stoneage_wayi_saupdate_route_probe import decode_window, raw_window, operand_metadata
from tools.stoneage_wayi_pet_transport_probe import summarize_window
from tools.stoneage_wayi_codec_profile import read_literal
from tools.stoneage_enemy_creation_audit import definition
from tools.stoneage_wayi_input_editor import settings_factory, demand

SOURCE_REF = '2f736808ff4361f5429ee919b718c88fabb60346'
PINS = {
    'client/stoneage/system/savedata.cpp': '6809dd415e89e87ad00f7813cb35209db034aa53',
    'client/stoneage/system/tool.cpp': '824c1d008322405c9c120f431a62886027032df1',
}
BACKING_RVA = 0x4319d28
WINDOWS = {
    'save-settings-dispatch': (0x805a0, 0x805c4),
    'load-settings-dispatch': (0x805d0, 0x805f1),
    'write-settings-body': (0x806ba, 0x80752),
    'load-settings': (0x80760, 0x808b4),
    'create-settings': (0x808c0, 0x809bb),
    'set-pet-selection': (0x809c0, 0x80a7f),
    'get-pet-selection': (0x80a80, 0x80acf),
    'clear-pet-selection': (0x80ad0, 0x80af5),
    'set-sound': (0x80b00, 0x80b4f),
    'get-sound': (0x80b50, 0x80ba8),
    'set-chat': (0x80bb0, 0x80bd3),
    'get-chat': (0x80be0, 0x80c08),
    'set-interface': (0x80c10, 0x80c1b),
    'get-interface': (0x80c20, 0x80c2d),
    'encode': (0x8e050, 0x8e197),
    'decode': (0x8e1a0, 0x8e2a9),
}
# Exact instructions for independent evidence mutations; no raw assembly dump.
ANCHORS = {0x80766, 0x80791, 0x807b9, 0x807c9, 0x807dc, 0x807e2, 0x807e7,
           0x80810, 0x80815, 0x80819, 0x80825, 0x8082f, 0x80838, 0x8083f,
           0x80846, 0x8084c, 0x80859, 0x80864, 0x8086a, 0x80871, 0x80878,
           0x8088c, 0x8089c, 0x808a3, 0x809cd, 0x809e7, 0x809ea, 0x80a44,
           0x80a64, 0x80ad8, 0x80aef, 0x80af1, 0x80b27, 0x80b63,
           0x8e071, 0x8e0c9, 0x8e0d0, 0x8e0d6, 0x8e0d7, 0x8e0db,
           0x8e0fc, 0x8e102, 0x8e160, 0x8e171, 0x8e175, 0x8e185,
           0x8e1b0, 0x8e1bc, 0x8e1c7, 0x8e22a, 0x8e22e, 0x8e23b,
           0x8e26a, 0x8e26e, 0x8e28f, 0x8e298}


def encode_key_zero(plain):
    """Independent projection of the named settings key=0, sufficient capacity."""
    demand(isinstance(plain, bytes) and 1 <= len(plain) <= 127, 'Bounded nonempty synthetic payload')
    total = sum(plain) & 255
    out = bytearray([total])
    for pos, byte in enumerate(plain):
        if pos % 2 == 0 or pos % 5 == 0:
            byte ^= 255
        n = pos + 1
        out.append((byte + (n*n % 7)*total) & 255)
    return bytes(out)


def decode_key_zero(encoded):
    """No checksum validation added. Native short/oversize behavior is excluded."""
    demand(isinstance(encoded, bytes) and 2 <= len(encoded) <= 128, 'Bounded complete synthetic encoding')
    total = encoded[0]
    out = bytearray()
    for pos, byte in enumerate(encoded[1:]):
        n = pos + 1
        byte = (byte - (n*n % 7)*total) & 255
        if pos % 2 == 0 or pos % 5 == 0:
            byte ^= 255
        out.append(byte)
    return bytes(out)


def migration(decoded, prior):
    """Overlay on explicit prior backing; return outcome and optional save request.

    Success on migration is independent of save return, as in the native path.
    No file deletion, native recreation, or zeroing of untouched tail invented.
    """
    demand(isinstance(decoded, bytes) and 1 <= len(decoded) <= 127, 'Bounded decoded payload')
    demand(isinstance(prior, bytes) and len(prior) == 127, 'Explicit synthetic prior backing')
    out = bytearray(prior)
    out[:len(decoded)] = decoded
    version = int.from_bytes(out[:2], 'little')
    if len(decoded) == 57 and version == 4:
        out[0], out[57] = 6, 3
        return bytes(out), {'success': True, 'error': 0, 'save_requested': True, 'route': 'v4-to-v6'}
    if len(decoded) == 127 and version == 5:
        out[0], out[58] = 6, 0
        return bytes(out), {'success': True, 'error': 0, 'save_requested': True, 'route': 'v5-to-v6'}
    error = 4 if len(decoded) != 127 else 5 if version != 6 else 0
    return bytes(out), {'success': error == 0, 'error': error, 'save_requested': False, 'route': 'reject' if error else 'v6'}


def write_pet_selection(backing, character, selected, mail_pet):
    demand(isinstance(backing, bytes) and len(backing) == 127, 'Explicit settings backing')
    demand(type(character) is int and len(selected) == 5 and all(type(x) is bool for x in selected) and type(mail_pet) is int, 'Synthetic pet state')
    if not 0 <= character < 2:
        return backing
    out = bytearray(backing)
    for pet, active in enumerate(selected):
        out[26 + character*5 + pet] = int(active) | (4 if pet == mail_pet else 0)
    return bytes(out)


def clear_pet_selection(backing, character):
    demand(isinstance(backing, bytes) and len(backing) == 127 and type(character) is int, 'Synthetic clear')
    if not 0 <= character < 2:
        return backing
    out = bytearray(backing)
    out[26 + character*5:31 + character*5] = b'\0'*5
    return bytes(out)


def read_pet_selection(backing, character, prior_mail):
    demand(isinstance(backing, bytes) and len(backing) == 127 and type(character) is int and type(prior_mail) is int, 'Synthetic read')
    demand(0 <= character < 2, 'Valid synthetic character; native invalid call leaves state unchanged')
    row = backing[26 + character*5:31 + character*5]
    mail = prior_mail
    for pet, byte in enumerate(row):
        if byte & 4:
            mail = pet
    return tuple(bool(x & 1) for x in row), mail, -1


def write_options(backing, stereo, se, bgm, pitch, color, lines, area, cursor):
    demand(isinstance(backing, bytes) and len(backing) == 127 and isinstance(pitch, bytes) and len(pitch) == 16, 'Synthetic options backing')
    values = (stereo, se, bgm, color, lines, area, cursor)
    demand(all(type(x) is int and 0 <= x <= 255 for x in values), 'Byte-domain synthetic options')
    out = bytearray(backing)
    out[36:55] = bytes((stereo, se, bgm)) + pitch
    out[55:59] = bytes((color, lines, area, cursor))
    return bytes(out)


def read_options(backing):
    demand(isinstance(backing, bytes) and len(backing) == 127, 'Synthetic options backing')
    return {'stereo': backing[36], 'se': backing[37], 'bgm': backing[38],
            'pitch': backing[39:55], 'color': backing[55], 'lines': backing[56],
            'area': backing[57], 'cursor': backing[58]}


def source_profile(root):
    raw = {}
    for path, pin in PINS.items():
        data = (Path(root)/path).read_bytes()
        actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        demand(actual == pin, 'Source drift: '+path)
        raw[path] = data.decode('utf-8-sig')
    saved = raw['client/stoneage/system/savedata.cpp']
    load = definition(saved, 'loadNowState')
    enc = definition(raw['client/stoneage/system/tool.cpp'], 'jEncode')
    dec = definition(raw['client/stoneage/system/tool.cpp'], 'jDecode')
    get_sound = definition(saved, 'getUserSoundOption')
    set_sound = definition(saved, 'setUserSoundOption')
    r = {'source_ref': SOURCE_REF, 'source_blobs': PINS,
         'load_remove_calls': load.count('remove(SAVEFILE_NAME)'),
         'load_recursive_calls': load.count('loadNowState()'),
         'v4_length': 57, 'v5_length': 127, 'current_version': 6,
         'encoder_mutates_source': 'src[i] = ~src[i]' in enc,
         'encoder_plain_sum_precedes_complement': enc.index('sum = sum + src[i]') < enc.index('src[i] = ~src[i]'),
         'encoder_squared_moduli': [3, 7],
         'decoder_has_no_sum_recompute': 'sum =' in dec and 'sum = sum +' not in dec,
         'source_bgm_has_mute_bit': 'MuteFlag' in set_sound and '0x80' in set_sound and '0x7f' in get_sound,
         'reserved_names_only_enum_tokens': len(re.findall(r'\bCDKEY\b', saved)) == 2 and len(re.findall(r'\bPASSWORD\b', saved)) == 2,
         'source_program_executed': False, 'binary_build_identity_verified': False}
    demand(r['load_remove_calls'] == 2 and r['load_recursive_calls'] == 2, 'Source recovery branch profile')
    demand(all(s in enc and s in dec for s in ('(i * i) % 3', '(i * i) % 7', 'key % 7', 'i % 5', 'key % 2', 'i % 2')), 'Source arithmetic profile')
    demand('tmpsavedatalen == 57' in load and 'tmpsavedatalen == 127' in load and r['source_bgm_has_mute_bit'], 'Source version/sound profile')
    return r


def probe(payload):
    demand(len(payload) == EXPECTED_BYTES and hashlib.sha256(payload).hexdigest() == EXPECTED_SHA256, 'Exact accepted specimen')
    layout = parse_pe_layout(payload)
    base = struct.unpack_from('<I', payload, layout['pe_off']+52)[0]
    imports = parse_imports(payload, layout, base)
    windows, anchors = [], {}
    for label, (a, b) in WINDOWS.items():
        blob = raw_window(payload, layout, a, b)
        ins = decode_window(blob, base+a)
        summary = summarize_window(ins, base, imports)
        windows.append({'label': label, 'start_rva': a, 'end_rva_exclusive': b,
                        'code_sha256': hashlib.sha256(blob).hexdigest(),
                        **{k: summary[k] for k in ('instruction_count', 'calls', 'branches', 'absolute_writes')}})
        for i in ins:
            if i.address-base in ANCHORS:
                anchors[hex(i.address-base)] = {'operation': i.mnemonic, 'operands': operand_metadata(i, base)}
    # Derived direct-reference surface only. Indirect aliases are not closed.
    sec = next(s for s in layout['sections'] if s['name'] == '.text')
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True
    md.skipdata = True
    refs = []
    for i in md.disasm(payload[sec['raw_ptr']:sec['raw_ptr']+sec['raw_size']], base+sec['vaddr']):
        if not i.id:
            continue
        for op in i.operands:
            v = (op.imm & 0xffffffff) if op.type == X86_OP_IMM else (op.mem.disp & 0xffffffff) if op.type == X86_OP_MEM else 0
            if base+BACKING_RVA <= v < base+BACKING_RVA+127:
                refs.append({'instruction_rva': i.address-base, 'backing_offset': v-base-BACKING_RVA, 'operation': i.mnemonic})
                break
    return {'schema': 'STONEAGE-WAYI-SAVEDATA-R1', 'input_bytes': len(payload), 'decompressed_input_sha256': EXPECTED_SHA256,
            'windows': windows, 'anchors': anchors, 'direct_backing_references': refs,
            'backing_rva': BACKING_RVA, 'error_byte_rva': 0x4319dac,
            'literals': {'path': read_literal(payload, layout, 0xd6058), 'read_mode': read_literal(payload, layout, 0xbf944), 'write_mode': read_literal(payload, layout, 0xd606c)},
            'file_executed': False, 'real_savedata_opened': False, 'native_server_pair_verified': False}


EXPECTED_PROBE_PROFILE_SHA256 = '17137fadd6da1fafae63f2054b4acc063ae76ad45cf6de1701d6f043b7dec7b2'


EXPECTED_SOURCE_PROFILE_SHA256 = '2274ec5fc42698fa2d48ac2b4c0dfcecf0d50554eb179a951f667868831419de'


def validate(report):
    p = report['probe']
    demand(p['schema'] == 'STONEAGE-WAYI-SAVEDATA-R1' and p['input_bytes'] == EXPECTED_BYTES and p['decompressed_input_sha256'] == EXPECTED_SHA256, 'Identity')
    demand([(x['label'], x['start_rva'], x['end_rva_exclusive']) for x in p['windows']] == [(n, a, b) for n, (a, b) in WINDOWS.items()], 'Windows')
    demand(set(p['anchors']) == {hex(x) for x in ANCHORS}, 'Complete anchors')
    demand(p['literals'] == {'path': 'data\\savedata.dat', 'read_mode': 'rb+', 'write_mode': 'wb+'}, 'Literal paths/modes')
    demand(p['backing_rva'] == BACKING_RVA and p['error_byte_rva'] == 0x4319dac, 'Settings backing')
    values = {0x80791: 1, 0x807b9: 2, 0x807c9: 4000, 0x807e7: 3, 0x80815: 0,
              0x80819: 0x48e1a0, 0x80825: 57, 0x80838: 6, 0x8083f: 3,
              0x80846: 0x480600, 0x8084c: 1, 0x80859: 127, 0x80864: 5,
              0x8086a: 6, 0x80871: 0, 0x80878: 0x480600, 0x8089c: 6,
              0x808a3: 5, 0x809cd: 2, 0x80a44: 4, 0x80ad8: 2}
    for address, value in values.items():
        demand(p['anchors'][hex(address)]['operands'][-1].get('value') == value, 'Version/length/IO constant drift')
    demand(p['anchors']['0x8088c']['operands'][1] == {'width_bytes': 1, 'kind': 'register', 'name': 'cl'}, 'Native error4 path')
    load = next(w for w in p['windows'] if w['label'] == 'load-settings')
    demand([x['direct_target_rva'] for x in load['calls'] if 'direct_target_rva' in x] == [0x95bf4, 0x808c0, 0x95bf4, 0x9598c, 0x95a74, 0x95a74, 0x8e1a0, 0x80600, 0x80600], 'Bounded load calls: no deletion/recursion')
    demand(len(p['direct_backing_references']) == 44 and all(0x806ba <= x['instruction_rva'] < 0x80c2d for x in p['direct_backing_references']), 'Bounded direct surface; not indirect closure')
    demand(all(p[k] is False for k in ('file_executed', 'real_savedata_opened', 'native_server_pair_verified')), 'Native promotion')
    s = report['source_profile']
    demand(s['source_ref'] == SOURCE_REF and s['source_blobs'] == PINS and s['load_remove_calls'] == 2 and s['load_recursive_calls'] == 2 and s['source_bgm_has_mute_bit'], 'Source/binary distinction')
    demand(s['source_program_executed'] is False and s['binary_build_identity_verified'] is False, 'Source promotion')
    for row in report['synthetic_vectors']:
        plain, encoded = bytes.fromhex(row['plain_hex']), bytes.fromhex(row['encoded_hex'])
        demand(encode_key_zero(plain) == encoded and decode_key_zero(encoded) == plain, 'Synthetic codec vector')
    for key, expected in (('probe', EXPECTED_PROBE_PROFILE_SHA256), ('source_profile', EXPECTED_SOURCE_PROFILE_SHA256)):
        actual = hashlib.sha256(json.dumps(report[key], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        demand(actual == expected, 'Complete derived profile drift: '+key)
    demand(all(x['origin'] == 'GENERATED_SYNTHETIC_NOT_CAPTURED' for x in report['synthetic_vectors']), 'Synthetic provenance')
    return p


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--client', type=Path)
    parser.add_argument('--source-root', type=Path)
    args = parser.parse_args()
    if args.client:
        print(json.dumps(probe(args.client.read_bytes()), indent=2))
    if args.source_root:
        print(json.dumps(source_profile(args.source_root), indent=2))
