"""Static settings lifecycle joins and synthetic IO-event projections only.

No file IO, process API, native code or real PID is used by the projections.
Loader zero-fill is a declared PE state, not proof of every pre-load writer.
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
from tools.stoneage_wayi_input_editor import settings_factory, demand
from tools.stoneage_wayi_savedata import (BACKING_RVA, encode_key_zero, decode_key_zero,
                                         migration, source_profile as prior_source_profile)

SOURCE_REF = '2f736808ff4361f5429ee919b718c88fabb60346'
PINS = {'client/stoneage/game/main.cpp': '65b5d8501f6770aefe35d38c5d4c1c4c902259bd',
        'client/stoneage/system/savedata.cpp': '6809dd415e89e87ad00f7813cb35209db034aa53',
        'client/stoneage/system/tool.cpp': '824c1d008322405c9c120f431a62886027032df1'}
PE_SPEC = 'https://learn.microsoft.com/en-us/windows/win32/debug/pe-format#section-table-section-headers'
WINDOWS = {
    'save-full': (0x80600, 0x80752),
    'create-full': (0x808c0, 0x809bb),
    'load-full': (0x80760, 0x808b4),
    'startup-load-result': (0x1e5df, 0x1e629),
    'startup-current-parent-process': (0x3f457, 0x3f4cf),
    'snapshot-import-thunks': (0x93e50, 0x93e62),
    'snapshot-close': (0x3f69d, 0x3f6aa),
    'save-wrapper': (0x805a0, 0x805c4),
    'load-wrapper': (0x805d0, 0x805f1),
}
ROOTS = (0x805a0, 0x805d0, 0x80600, 0x80760, 0x808c0, 0x8e050, 0x8e1a0)
ANCHORS = {0x80611, 0x80622, 0x80642, 0x80668, 0x80686, 0x8068b,
           0x8069d, 0x806aa, 0x806b0, 0x806c1, 0x806e6, 0x80707,
           0x8072e, 0x8073c, 0x80744, 0x80935, 0x80956, 0x80973,
           0x80997, 0x809a5, 0x809ad, 0x80846, 0x8084c, 0x80878,
           0x8087e, 0x1e5e4, 0x1e5eb, 0x1e621, 0x3f457, 0x3f45e,
           0x3f460, 0x3f465, 0x3f46d, 0x3f4c3, 0x3f4c9, 0x3f6a4}


def initial_region(payload, section, rva, length):
    """Bounded PE virtual-region projection, safely split raw bytes/zero-fill."""
    demand(type(rva) is int and type(length) is int and 0 < length <= 127, 'Bounded region')
    relative = rva-section['vaddr']
    demand(0 <= relative and relative+length <= section['vsize'], 'Region within virtual section')
    raw_count = min(length, max(0, section['raw_size']-relative))
    offset = section['raw_ptr']+relative
    if raw_count:
        demand(0 <= offset <= len(payload)-raw_count, 'Raw-backed region within file')
    return payload[offset:offset+raw_count] + b'\0'*(length-raw_count)


def complemented_backing(plain):
    demand(isinstance(plain, bytes) and len(plain) == 127, 'Synthetic fixed factory/backing')
    return bytes(byte ^ (255 if i % 2 == 0 or i % 5 == 0 else 0) for i, byte in enumerate(plain))


def io_outcome(opened, written):
    demand(type(opened) is bool and type(written) is int and 0 <= written <= 128, 'Synthetic IO domain')
    return {'success': opened and written == 128, 'open_attempted': True,
            'write_attempted': opened, 'close_attempted': opened and written == 128}


def create_projection(factory, opened=True, written=128):
    demand(isinstance(factory, bytes) and len(factory) == 127 and factory[:2] == b'\x06\0', 'Explicit synthetic version6 factory')
    result = io_outcome(opened, written)
    # The caller passes global backing, so mutation precedes every IO outcome.
    return complemented_backing(factory), encode_key_zero(factory), result


def save_projection(backing, opened=True, written=128):
    demand(isinstance(backing, bytes) and len(backing) == 127, 'Explicit synthetic saved backing')
    # Native stack-copy encode has no corresponding write to global backing.
    return backing, encode_key_zero(backing), io_outcome(opened, written)


def load_projection(prior, encoded, factory, create_io=(True, 128), reopen=True,
                    read_error=False, migration_io=(True, 128)):
    """Bounded, explicitly supplied hypothetical IO results. No real filesystem.

    encoded=None means missing file. On successful creation this model reads
    its complete generated encoding. Empty/one-byte/oversize native input is OPEN.
    """
    demand(isinstance(prior, bytes) and len(prior) == 127, 'Synthetic prior backing')
    demand(type(reopen) is bool and type(read_error) is bool, 'Synthetic read gates')
    backing, trace = prior, ['error=0', 'open-existing']
    if encoded is None:
        trace.append('create')
        backing, encoded, creation = create_projection(factory, *create_io)
        if not creation['success']:
            return backing, {'success': False, 'error': 1, 'trace': trace, 'creation': creation}
        trace.append('reopen')
        if not reopen:
            return backing, {'success': False, 'error': 2, 'trace': trace, 'creation': creation}
    trace.extend(['read', 'close-read'])
    if read_error:
        return backing, {'success': False, 'error': 3, 'trace': trace}
    decoded = decode_key_zero(encoded)
    backing, decision = migration(decoded, backing)
    trace.append('decode')
    if decision['save_requested']:
        # This names the full native call, including its external preamble.
        trace.append('call-full-save')
        backing, _, write = save_projection(backing, *migration_io)
        decision = {**decision, 'write': write}
    return backing, {**decision, 'trace': trace}


def preamble_projection(pending, enumeration_ok, pid_found, name_equal, process_opened):
    """Control-event names only; NEVER an executor, OS call, PID or command."""
    demand(all(type(x) is bool for x in (pending, enumeration_ok, pid_found, name_equal, process_opened)), 'Synthetic boolean gates')
    events = []
    if pending:
        events.append('enumeration')
        if enumeration_ok and pid_found:
            events.append('name-compare')
            if name_equal:
                events.append('OpenProcess')
                if process_opened:
                    events.extend(['TerminateProcess', 'CloseHandle'])
        events.append('reset-pending-id')
    events.append('settings-body')
    return events


def source_profile(root):
    prior = prior_source_profile(root)
    raw = {}
    for path, pin in PINS.items():
        data = (Path(root)/path).read_bytes()
        demand(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == pin, 'Source drift: '+path)
        raw[path] = data.decode('utf-8-sig')
    main = raw['client/stoneage/game/main.cpp']
    block = re.search(r'#ifdef __NEW_CLIENT\s+dwPID = GetCurrentProcessId\(\);(.*?)#endif', main, re.S)
    demand(block is not None and 'dwPID = pe32.th32ParentProcessID' in block[1], 'Source conditional parent setup')
    return {'source_ref': SOURCE_REF, 'source_blobs': PINS,
            'prior_settings_profile': prior,
            'main_parent_setup_conditional_macro': '__NEW_CLIENT',
            'main_parent_snapshot_size_uses_sizeof': 'sizeof(PROCESSENTRY32)' in block[1],
            'main_and_savedata_terminate_tokens': {p: len(re.findall(r'\bTerminateProcess\b', raw[p])) for p in list(PINS)[:2]},
            'source_program_executed': False, 'whole_source_build_identity_verified': False}


def probe(payload):
    demand(len(payload) == EXPECTED_BYTES and hashlib.sha256(payload).hexdigest() == EXPECTED_SHA256, 'Exact accepted client')
    layout = parse_pe_layout(payload)
    base = struct.unpack_from('<I', payload, layout['pe_off']+52)[0]
    imports = parse_imports(payload, layout, base)
    sec = next(s for s in layout['sections'] if s['vaddr'] <= BACKING_RVA < s['vaddr']+s['vsize'])
    initial = initial_region(payload, sec, BACKING_RVA, 127)
    windows, anchors = [], {}
    for label, (a, b) in WINDOWS.items():
        code = raw_window(payload, layout, a, b)
        ins = decode_window(code, base+a)
        summary = summarize_window(ins, base, imports)
        windows.append({'label': label, 'start_rva': a, 'end_rva_exclusive': b,
                        'code_sha256': hashlib.sha256(code).hexdigest(),
                        **{k: summary[k] for k in ('instruction_count', 'calls', 'branches', 'absolute_writes')}})
        for i in ins:
            if i.address-base in ANCHORS:
                anchors[hex(i.address-base)] = {'operation': i.mnemonic, 'operands': operand_metadata(i, base)}
    text = next(s for s in layout['sections'] if s['name'] == '.text')
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail, md.skipdata = True, True
    edges, process_writes, skipped = [], [], 0
    for i in md.disasm(payload[text['raw_ptr']:text['raw_ptr']+text['raw_size']], base+text['vaddr']):
        if not i.id:
            skipped += i.size
            continue
        if i.mnemonic in ('call', 'jmp') and i.operands[0].type == X86_OP_IMM and i.operands[0].imm-base in ROOTS:
            edges.append({'instruction_rva': i.address-base, 'operation': i.mnemonic, 'target_rva': i.operands[0].imm-base})
        if i.mnemonic == 'mov' and i.operands[0].type == X86_OP_MEM:
            mem = i.operands[0].mem
            if not mem.base and not mem.index and mem.disp-base == 0x41658e0:
                process_writes.append({'instruction_rva': i.address-base, 'source': operand_metadata(i, base)[1]})
    pointer_words = []
    for target in (BACKING_RVA,)+ROOTS[:5]:
        for section in layout['sections']:
            if section['chars'] & 0x20000000:
                continue
            raw = payload[section['raw_ptr']:section['raw_ptr']+section['raw_size']]
            start, needle = 0, struct.pack('<I', base+target)
            while (offset := raw.find(needle, start)) >= 0:
                pointer_words.append({'target_rva': target, 'section': section['name'], 'word_rva': section['vaddr']+offset})
                start = offset+1
    import_rvas = (0xa00a8, 0xa00b8, 0xa0190, 0xa0194, 0xa01b8, 0xa01bc, 0xa0174)
    return {'schema': 'STONEAGE-WAYI-SAVEDATA-LIFECYCLE-R1', 'input_bytes': len(payload), 'decompressed_input_sha256': EXPECTED_SHA256,
            'initial_region': {'backing_rva': BACKING_RVA, 'bytes': 127, 'section': sec,
                               'entirely_beyond_raw': BACKING_RVA-sec['vaddr'] >= sec['raw_size'],
                               'declared_zero_filled': initial == b'\0'*127, 'sha256': hashlib.sha256(initial).hexdigest(), 'spec': PE_SPEC},
            'windows': windows, 'anchors': anchors,
            'literal_name_gate': read_literal(payload, layout, 0xa2080),
            'process_imports': {hex(r): list(imports[base+r]) for r in import_rvas},
            'direct_control_edges': edges, 'non_executable_pointer_words': pointer_words,
            'linear_sweep_skipped_bytes': skipped, 'pending_process_id_writes': process_writes,
            'file_executed': False, 'process_api_called': False, 'real_savedata_opened': False,
            'all_indirect_writers_closed': False, 'authentic_publisher_hash_verified': False}


# Complete fingerprints added after independent original-byte/source derivation.
EXPECTED_PROBE_PROFILE_SHA256 = '3c3a2af3f315def5ade9a7079fd50d93349844b57e7d9ea27f065d129f0473c2'
EXPECTED_SOURCE_PROFILE_SHA256 = '5af2131f5ebfab861e222c0e9bde7bb98bdd7ced630aa1b04c3855a5dd2b7467'


def validate(report):
    p = report['probe']
    demand(p['schema'] == 'STONEAGE-WAYI-SAVEDATA-LIFECYCLE-R1' and p['input_bytes'] == EXPECTED_BYTES and p['decompressed_input_sha256'] == EXPECTED_SHA256, 'Identity')
    demand([(x['label'], x['start_rva'], x['end_rva_exclusive']) for x in p['windows']] == [(n, a, b) for n, (a, b) in WINDOWS.items()], 'Windows')
    demand(set(p['anchors']) == {hex(x) for x in ANCHORS}, 'Anchor coverage')
    initial = p['initial_region']
    demand(initial['backing_rva'] == BACKING_RVA and initial['bytes'] == 127 and initial['entirely_beyond_raw'] and initial['declared_zero_filled'], 'Loader declared state')
    demand(p['literal_name_gate'] == 'explorer.exe', 'Static literal gate')
    demand(p['process_imports']['0xa01bc'] == ['KERNEL32.DLL', 'TerminateProcess'], 'Import identity')
    demand(p['non_executable_pointer_words'] == [], 'Bounded pointer surface')
    demand(len(p['direct_control_edges']) == 31, 'Direct call/transfer surface')
    for address, value in ((0x80686, 0x1f0fff), (0x806e6, 127), (0x80744, 1), (0x809ad, 1), (0x8084c, 1), (0x8087e, 1), (0x1e621, None), (0x3f45e, 2)):
        operands = p['anchors'][hex(address)]['operands']
        if value is not None:
            demand(operands[-1].get('value') == value, 'Critical constant')
    demand(all(p[k] is False for k in ('file_executed', 'process_api_called', 'real_savedata_opened', 'all_indirect_writers_closed', 'authentic_publisher_hash_verified')), 'Native/provenance promotion')
    s = report['source_profile']
    demand(s['source_ref'] == SOURCE_REF and s['source_blobs'] == PINS and s['main_parent_setup_conditional_macro'] == '__NEW_CLIENT', 'Pinned source setup')
    demand(s['source_program_executed'] is False and s['whole_source_build_identity_verified'] is False, 'Source promotion')
    for key, expected in (('probe', EXPECTED_PROBE_PROFILE_SHA256), ('source_profile', EXPECTED_SOURCE_PROFILE_SHA256)):
        actual = hashlib.sha256(json.dumps(report[key], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        demand(actual == expected, 'Complete derived profile drift: '+key)
    return p


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--client', type=Path)
    ap.add_argument('--source-root', type=Path)
    args = ap.parse_args()
    if args.client:
        print(json.dumps(probe(args.client.read_bytes()), indent=2))
    if args.source_root:
        print(json.dumps(source_profile(args.source_root), indent=2))
