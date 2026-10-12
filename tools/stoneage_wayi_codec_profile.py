"""Offline codec/framing model and hash-pinned static evidence. Never runs client.

The synthetic model accepts a deliberately bounded valid domain; its validation
is not a claim that the historical parser rejects malformed input.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

from tools.stoneage_jss_launcher_deep_probe import parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import parse_imports
from tools.stoneage_wayi_pet_sender_probe import EXPECTED_BYTES, EXPECTED_SHA256
from tools.stoneage_wayi_saupdate_route_probe import decode_window, raw_window, operand_metadata
from tools.stoneage_wayi_pet_transport_probe import summarize_window

ALPHABET = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}'
WINDOWS = {
    'outer-encoder': (0x8fc10, 0x8fccb),
    'outer-decoder': (0x8fcd0, 0x8fd91),
    'unkeyed-six-bit-encoder': (0x8fed0, 0x8ff6d),
    'unkeyed-six-bit-decoder': (0x8ff70, 0x9007f),
    'byte-permutation': (0x90590, 0x905b8),
    'byte-complement': (0x905c0, 0x90611),
    'rotate-right': (0x90620, 0x906b1),
    'rotate-left': (0x906c0, 0x90736),
    'integer-field-decoder': (0x90740, 0x9079e),
    'integer-field-encoder': (0x907a0, 0x90855),
    'string-field-decoder': (0x90860, 0x90894),
    'string-field-encoder': (0x908a0, 0x90949),
    'default-key-copy': (0x5f539, 0x5f54d),
    'post-login-key-branches': (0x5f979, 0x5f9c7),
    'newline-handoff': (0x3e300, 0x3e363),
    'receive-line-intake': (0x5ee80, 0x5ef10),
}


def permute(value, rule):
    if not isinstance(value, bytes) or len(value) != 4 or sorted(rule) != list('1234'):
        raise ValueError('Four bytes and a byte permutation required')
    out = bytearray(4)
    for i, c in enumerate(rule):
        out[int(c) - 1] = value[i]
    return bytes(out)


def sixbit(data):
    """Little-endian groups; omit a zero residual as observed in the helper."""
    if not isinstance(data, bytes):
        raise ValueError('Byte input required')
    out = bytearray()
    for pos in range(0, len(data), 3):
        group = data[pos:pos+3]
        value = int.from_bytes(group, 'little')
        count = 4 if len(group) == 3 else len(group)
        for _ in range(count):
            out.append(ALPHABET[value & 63]); value >>= 6
        if value:
            out.append(ALPHABET[value])
    return bytes(out)


def unsixbit_seed(token):
    # Only the valid fixed-size outer seed is modeled, not invalid-char pointer reuse.
    if not isinstance(token, bytes) or len(token) != 6 or any(c not in ALPHABET for c in token):
        raise ValueError('Six-character valid seed required')
    value = sum(ALPHABET.index(c) << (6*i) for i, c in enumerate(token))
    if value >= 1 << 32:
        raise ValueError('Seed outside uint32')
    return value.to_bytes(4, 'little')


def encode_outer(message, seed):
    if not isinstance(message, bytes) or not 1 <= len(message) <= 4096 or any(c in message for c in (0, 10, 13, 255)):
        raise ValueError('Synthetic message domain')
    if type(seed) is not int or not 0 <= seed <= 98:
        raise ValueError('Synthetic rand remainder domain')
    head = sixbit(bytes(c ^ 255 for c in permute(struct.pack('<I', seed), '2413')))
    shift = seed % len(message)
    return bytes(c ^ 255 for c in head + message[shift:] + message[:shift])


def decode_outer(packet):
    if not isinstance(packet, bytes) or not 7 <= len(packet) <= 4102 or 0 in packet:
        raise ValueError('Synthetic packet domain')
    raw = bytes(c ^ 255 for c in packet)
    seed = int.from_bytes(permute(bytes(c ^ 255 for c in unsixbit_seed(raw[:6])), '3142'), 'little')
    if not 0 <= seed <= 98:
        raise ValueError('Synthetic seed range')
    body = raw[6:]; shift = seed % len(body)
    return body[-shift:] + body[:-shift] if shift else body


def field_key(supplied_base, mode):
    """Hypothetical stack-supplied base; no account/credential handling."""
    if not isinstance(supplied_base, bytes) or not supplied_base or 0 in supplied_base or type(mode) is not int or not 0 <= mode <= 0xffffffff:
        raise ValueError('Synthetic key inputs')
    return supplied_base + (b'07062005' if mode & 0x0f000000 == 0x0f000000 else b'19761101')


def read_literal(payload, layout, rva):
    for s in layout['sections']:
        relative = rva - s['vaddr']
        if 0 <= relative and relative + 80 <= s['raw_size']:
            start = s['raw_ptr'] + relative
            raw = payload[start:start+80]
            if b'\0' not in raw:
                raise ValueError('Unterminated bounded literal')
            return raw.split(b'\0')[0].decode('ascii')
    raise ValueError('Literal outside raw-backed section')


def probe(payload):
    if len(payload) != EXPECTED_BYTES or hashlib.sha256(payload).hexdigest() != EXPECTED_SHA256:
        raise ValueError('Exact accepted unpacked specimen required')
    layout = parse_pe_layout(payload)
    base = struct.unpack_from('<I', payload, layout['pe_off']+52)[0]
    imports = parse_imports(payload, layout, base)
    windows = []
    arithmetic = []
    for name, (a, b) in WINDOWS.items():
        ins = decode_window(raw_window(payload, layout, a, b), base+a)
        for i in ins:
            if i.mnemonic in ('and', 'or', 'xor', 'not', 'shl', 'shr', 'div', 'idiv'):
                arithmetic.append({'rva': i.address-base, 'operation': i.mnemonic, 'operands': operand_metadata(i,base)})
        windows.append({'label': name, 'start_rva': a, 'end_rva_exclusive': b,
                        **summarize_window(ins, base, imports)})
    literals = {hex(r): read_literal(payload, layout, r) for r in
                (0xdb918, 0xdb95c, 0xdb964, 0xdb970, 0xc8548, 0xc8514, 0xc8508)}
    return {'schema': 'STONEAGE-WAYI-CODEC-PROFILE-R1', 'input_bytes': len(payload),
            'decompressed_input_sha256': EXPECTED_SHA256, 'windows': windows,
            'literals': literals, 'arithmetic_evidence': arithmetic, 'key_buffer_rva': 0x4bb4694,
            'key_copy_import': list(imports[base+0xa0180]),
            'key_append_import': list(imports[base+0xa00a4]),
            'file_executed': False, 'packets_captured': False,
            'matching_server_verified': False, 'native_pet_runtime_verified': False}


def validate(report):
    p = report['probe']
    if p['schema'] != 'STONEAGE-WAYI-CODEC-PROFILE-R1' or p['input_bytes'] != EXPECTED_BYTES or p['decompressed_input_sha256'] != EXPECTED_SHA256:
        raise ValueError('Specimen identity')
    rows = p['windows']
    if [(r['label'], r['start_rva'], r['end_rva_exclusive']) for r in rows] != [(n,a,b) for n,(a,b) in WINDOWS.items()]:
        raise ValueError('Window identity')
    if p['literals'] != {'0xdb918': ALPHABET.decode(), '0xdb95c': '2413', '0xdb964': '3142',
                         '0xdb970': '&;%d%s;#;', '0xc8548': 'r7f83t6c3', '0xc8514': '07062005', '0xc8508': '19761101'}:
        raise ValueError('Literal profile')
    if p['key_buffer_rva'] != 0x4bb4694 or p['key_copy_import'] != ['KERNEL32.DLL', 'lstrcpyA'] or p['key_append_import'] != ['KERNEL32.DLL', 'lstrcatA']:
        raise ValueError('Key binding')
    arithmetic = {x['rva']:x for x in p['arithmetic_evidence']}
    for rva, operation, value in ((0x8fc23,'mov',99),):
        # MOV constants are retained in the ordinary window summary below.
        if not any(x['rva']==rva and x['operation']==operation and x['operands'][1].get('value')==value for x in rows[0]['selected_constants']):
            raise ValueError('Seed modulus evidence')
    for rva, operation, value in ((0x8ff13,'and',255),(0x8ff25,'and',63),(0x8ff29,'shr',6),(0x5f982,'and',0x0f000000)):
        x=arithmetic.get(rva)
        if x is None or x['operation']!=operation or x['operands'][1].get('value')!=value:
            raise ValueError('Arithmetic evidence')
    for key in ('file_executed','packets_captured','matching_server_verified','native_pet_runtime_verified'):
        if p[key] is not False:
            raise ValueError('Unproved runtime promotion')
    for v in report['synthetic_vectors']:
        message = bytes.fromhex(v['message_hex'])
        packet = bytes.fromhex(v['packet_hex'])
        if encode_outer(message,v['seed']) != packet or decode_outer(packet) != message:
            raise ValueError('Synthetic vector mismatch')
    return p


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('local_unpacked_client',type=Path)
    args = parser.parse_args()
    print(json.dumps(probe(args.local_unpacked_client.read_bytes()),indent=2))
