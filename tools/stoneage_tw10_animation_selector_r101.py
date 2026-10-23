"""Original TW1.0 animation-table selection and countdown normalization proof.

Consumes authenticated original bytes transiently. Unicorn executes ONLY two
bounded instruction regions with synthetic memory and explicit bitmap-helper
stubs; this is not original-client UI, server, pet identity or live gameplay.
"""
import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path
import struct
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXE_SHA = 'cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a'
DISC_SHA = '905ee6ad89b8ca7f55a5c1132eede99a15ee7cb1b868f9b0b398fb0c76cfd159'
REPORT = ROOT / 'research/recovered/STONEAGE-TW10-ANIMATION-SELECTOR-R101.json'
GROUP_SHA = '4db7809de4197eb90cca6dc04bda8550025e022c8232e2ebb902db0e9faf0175'
ANIM_SHA = '25f8039e6c6ca47d94289b269d5ff74a67fde999c6b6d4dbb08af297ddcaa567'
BASE = 0x400000
OBJ, ANIMS, FRAMES, POINTER = 0x200000, 0x300000, 0x310000, 0x320000
TABLE, STACK, HALT = 0x1156cf0, 0x91ff00, 0x900100
WINDOWS = {'index_loader': (0xe730, 0xeaf3), 'object_selector': (0x3c380, 0x3c5b8), 'bitmap_lookup': (0xe660, 0xe68b), 'loader_call': (0xd5cd, 0xd5ed), 'filename_writers': (0x1c708, 0x1c78f)}
PIVOTS = [0xd5d7, 0xd5dc, 0xd5e1, 0x1c73a, 0x1c73f, 0x1c744, 0x1c77d, 0x1c782, 0x1c787, 0xe80f, 0xe816, 0xe81c, 0xe8cb, 0xe8d3, 0xe8db, 0xe9a5, 0xe9aa, 0xe9be, 0xea60,
          0x3c3fc, 0x3c40e, 0x3c413, 0x3c468, 0x3c46d, 0x3c473, 0x3c47b, 0x3c49b, 0x3c4a4,
          0x3c4ad, 0x3c4b8, 0x3c4c2, 0x3c4d7, 0x3c4dd, 0x3c4ef, 0x3c4fe, 0x3c552, 0x3c558,
          0x3c577, 0x3c58c, 0x3c597, 0x3c5a4]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def ticks(duration, frames):
    """Engine-neutral rule restricted to non-overflowing source header values."""
    require(isinstance(duration, int) and isinstance(frames, int), 'integer source fields required')
    require(0 <= duration <= 0xffffffff and 0 <= frames <= 0x0fffffff, 'outside bounded arithmetic contract')
    return duration if frames == 0 else max(1, duration // (frames * 16))


def first_match(records, direction, action):
    if not records:
        return None
    return next((i for i, r in enumerate(records) if r[:2] == (direction, action)), 0)


def authenticate(raw):
    require(len(raw) == 425984 and hashlib.sha256(raw).hexdigest() == EXE_SHA, 'not authenticated original TW1.0 executable')


def machine(raw):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
    u = Uc(UC_ARCH_X86, UC_MODE_32)
    u.mem_map(BASE, 0x70000)
    u.mem_write(BASE, raw)
    for address, size in [(OBJ, 0x10000), (ANIMS, 0x30000), (0x1156000, 0x50000), (0x900000, 0x20000)]:
        u.mem_map(address, size)
    return u


def native_ticks(raw, duration, frames):
    from unicorn.x86_const import UC_X86_REG_ESI, UC_X86_REG_EDI, UC_X86_REG_EDX, UC_X86_REG_EIP
    u = machine(raw)
    u.mem_write(ANIMS, struct.pack('<HHIII', 0, 0, duration, frames, FRAMES))
    u.mem_write(POINTER, struct.pack('<I', ANIMS))
    for reg, value in [(UC_X86_REG_ESI, POINTER), (UC_X86_REG_EDI, 0), (UC_X86_REG_EDX, ANIMS)]:
        u.reg_write(reg, value)
    u.emu_start(BASE + 0xe995, BASE + 0xe9c4, count=100)
    require(u.reg_read(UC_X86_REG_EIP) == BASE + 0xe9c4, 'normalization instruction bound not reached')
    return struct.unpack('<I', u.mem_read(ANIMS + 4, 4))[0]


CASES = [
    {'name': 'matching_second_record', 'direction': 2, 'action': 6},
    {'name': 'unmatched_pair_falls_back_first', 'direction': 9, 'action': 9},
    {'name': 'duplicate_pair_uses_first', 'direction': 2, 'action': 6, 'duplicate': True},
    {'name': 'positive_countdown_defers_selection', 'direction': 2, 'action': 6, 'countdown': 3},
    {'name': 'changed_pair_resets_frame_and_countdown', 'direction': 2, 'action': 6, 'countdown': 9, 'frame': 1, 'changed': True},
    {'name': 'missing_group_keeps_prior_bitmap', 'direction': 2, 'action': 6, 'missing': True},
    {'name': 'frame_end_wraps_when_once_zero', 'direction': 2, 'action': 6, 'frame': 2},
    {'name': 'frame_end_once_one_returns_one', 'direction': 2, 'action': 6, 'frame': 2, 'once': 1},
    {'name': 'low_key_clears_bitmap', 'direction': 2, 'action': 6, 'graphic': 99},
    {'name': 'above_compiled_upper_guard_keeps_prior', 'direction': 2, 'action': 6, 'graphic': 132769},
]


def native_select(raw, case):
    from unicorn import UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_EIP, UC_X86_REG_EAX
    u = machine(raw)
    graphic = case.get('graphic', 100000)
    d, a = case['direction'], case['action']
    fields = {0x80: 7777, 0x124: graphic, 0x128: graphic, 0x12c: a, 0x130: a,
              0x134: d, 0x138: d + int(case.get('changed', False)),
              0x13c: case.get('frame', 0), 0x140: case.get('countdown', 0)}
    for off, value in fields.items():
        u.mem_write(OBJ + off, struct.pack('<I', value))
    u.mem_write(TABLE, struct.pack('<H2xI', 0 if case.get('missing') else 2, ANIMS))
    first = (2, 6) if case.get('duplicate') else (0, 0)
    u.mem_write(ANIMS, struct.pack('<HHIII', *first, 5, 2, FRAMES))
    u.mem_write(ANIMS + 16, struct.pack('<HHIII', 2, 6, 7, 2, FRAMES + 0x100))
    u.mem_write(FRAMES, struct.pack('<IhhHH', 1111, -3, 4, 0, 0) * 2)
    u.mem_write(FRAMES + 0x100, struct.pack('<IhhHH', 2222, -5, 6, 0, 0) * 2)
    u.mem_write(STACK, struct.pack('<IIII', HALT, OBJ, 0, case.get('once', 0)))
    u.reg_write(UC_X86_REG_ESP, STACK)
    helper_calls = []

    def hook(uc, address, size, data):
        if address == BASE + 0xe4e0:
            sp = uc.reg_read(UC_X86_REG_ESP)
            ret, bitmap, xx, yy = struct.unpack('<IIII', uc.mem_read(sp, 16))
            helper_calls.append({'rva': 0xe4e0, 'bitmap': bitmap, 'stub_offsets': [0, 0]})
            uc.mem_write(xx, b'\0\0')
            uc.mem_write(yy, b'\0\0')
            uc.reg_write(UC_X86_REG_EAX, 1)
            uc.reg_write(UC_X86_REG_ESP, sp + 4)
            uc.reg_write(UC_X86_REG_EIP, ret)

    u.hook_add(UC_HOOK_CODE, hook)
    u.emu_start(BASE + 0x3c380, HALT, count=2000)
    require(u.reg_read(UC_X86_REG_EIP) == HALT, 'selector exceeded bounded instruction budget')
    def word(off):
        return struct.unpack('<I', u.mem_read(OBJ + off, 4))[0]
    def signed(off):
        return struct.unpack('<i', u.mem_read(OBJ + off, 4))[0]
    return {'bitmap': word(0x80), 'frame': word(0x13c), 'countdown': word(0x140),
            'x': signed(0x144), 'y': signed(0x148), 'return': u.reg_read(UC_X86_REG_EAX), 'helper_calls': helper_calls}


def expected_select(c):
    frame, countdown = c.get('frame', 0), c.get('countdown', 0)
    out = {'bitmap': 7777, 'frame': frame, 'countdown': countdown, 'x': 0, 'y': 0, 'return': 0, 'helper_calls': []}
    if c.get('changed'):
        frame = countdown = 0
        out.update(frame=0, countdown=0)
    if countdown:
        out['countdown'] -= 1
        return out
    if c.get('graphic', 100000) <= 99:
        out['bitmap'] = 0
        return out
    if c.get('missing') or c.get('graphic', 100000) > 132768:
        return out
    if frame >= 2:
        if c.get('once') == 1:
            out.update(countdown=255, **{'return': 1})
            return out
        frame = 0
    pairs = [(2, 6) if c.get('duplicate') else (0, 0), (2, 6)]
    selected = first_match(pairs, c['direction'], c['action'])
    bitmap, x, y, tick = [(1111, -3, 4, 5), (2222, -5, 6, 7)][selected]
    out.update(bitmap=bitmap, frame=frame + 1, countdown=tick - 1, x=x, y=y,
               helper_calls=[{'rva': 0xe4e0, 'bitmap': bitmap, 'stub_offsets': [0, 0]}])
    return out


def source_tables():
    output = {}
    tables = {}
    for name, pin in [('SPR-GROUP-R1.tsv.gz', GROUP_SHA), ('SPR-ANIMATION-R1.tsv.gz', ANIM_SHA)]:
        p = ROOT / 'research/recovered/tw10-resource-metadata' / name
        b = p.read_bytes()
        require(hashlib.sha256(b).hexdigest() == pin, 'original source metadata changed')
        with gzip.open(p, 'rt') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        tables[name] = rows
        output[name] = {'bytes': len(b), 'sha256': pin, 'rows': len(rows)}
    require(len(tables['SPR-GROUP-R1.tsv.gz']) == 464 and len(tables['SPR-ANIMATION-R1.tsv.gz']) == 39065, 'source census changed')
    rows = tables['SPR-ANIMATION-R1.tsv.gz']
    output['derived_countdown'] = {'minimum': min(ticks(int(x['duration']), int(x['frame_count'])) for x in rows),
                                  'maximum': max(ticks(int(x['duration']), int(x['frame_count'])) for x in rows),
                                  'zero_frame_headers': sum(int(x['frame_count']) == 0 for x in rows),
                                  'max_frame_count': max(int(x['frame_count']) for x in rows)}
    return output


def inspect(raw):
    authenticate(raw)
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    windows, ins = {}, {}
    for name, (start, end) in WINDOWS.items():
        chunk = raw[start:end]
        decoded = list(md.disasm(chunk, BASE + start))
        require(sum(x.size for x in decoded) == len(chunk), 'instruction window decode incomplete')
        windows[name] = {'start_rva': start, 'end_rva_exclusive': end, 'sha256': hashlib.sha256(chunk).hexdigest(), 'instructions': len(decoded)}
        ins.update({x.address - BASE: x for x in decoded})
    pivots = [{'rva': rva, 'mnemonic': ins[rva].mnemonic, 'operands': ins[rva].op_str} for rva in PIVOTS]
    literals = {}
    for rva, expected in [(0x59e08, 'data\\spr_%d.bin'), (0x59de8, 'data\\spradrn_%d.bin')]:
        value = raw[rva:raw.index(b'\0', rva)].decode('ascii')
        require(value == expected, 'original animation filename changed')
        literals[str(rva)] = value
    timing = []
    for duration, frames in [(1000, 12), (1000, 7), (1, 1), (0, 1), (15, 1), (16, 1), (31, 2), (32, 2), (64, 2), (1000, 0)]:
        actual = native_ticks(raw, duration, frames)
        require(actual == ticks(duration, frames), 'native/reference countdown mismatch')
        timing.append({'duration': duration, 'frames': frames, 'native_result': actual, 'reference_result': actual})
    cases = []
    for case in CASES:
        actual = native_select(raw, case)
        require(actual == expected_select(case), 'native/reference selector mismatch: ' + case['name'])
        cases.append({'input': case, 'native': actual, 'reference': expected_select(case)})
    return {'schema': 'stoneage.tw10.animation-selector.r101', 'task': 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-101',
            'runtime': {'bytes': len(raw), 'sha256': EXE_SHA, 'version': 'AUTHENTICATED_TW1_RETAIL'},
            'source_windows': windows, 'source_filename_literals': literals, 'selected_instruction_pivots': pivots, 'source_tables': source_tables(),
            'native_countdown_replays': timing, 'native_selector_replays': cases,
            'compiled_contract': {'object_graphic_offset': 0x124, 'selected_bitmap_offset': 0x80,
                'low_graphic_clears_at_or_below': 99, 'animation_lower_inclusive': 100000,
                'compiled_upper_inclusive': 132768, 'loader_slot_count': 32768,
                'upper_endpoint_memory_safety_proven': False, 'runtime_slot_bytes': 8,
                'table_base_va': TABLE, 'disk_index_record_bytes': 12, 'expanded_animation_bytes': 16,
                'disk_frame_bytes': 10, 'expanded_frame_bytes': 12,
                'direction_selector_offset': 0x134, 'action_selector_offset': 0x12c,
                'unmatched_pair_fallback_record': 0, 'zero_count_group_keeps_previous_bitmap': True,
                'positive_frame_count_ticks': 'max(1, floor(duration / (16 * frame_count)))',
                'zero_frame_count_duration_unchanged': True, 'tick_milliseconds_proven': False},
            'instrumentation': {'mode': 'BOUNDED_ORIGINAL_X86_WITH_SYNTHETIC_MEMORY',
                'bitmap_helper_0xe4e0': 'STUBBED_ZERO_OFFSETS_RETURN_ONE', 'audio_calls': 'SYNTHETIC_FRAMES_SOUND_ZERO',
                'selector_instruction_limit': 2000, 'normalizer_instruction_limit': 100,
                'whole_client_or_server_executed': False},
            'boundaries': {'same_build_packet_to_object_graphic_path_proven': False,
                'named_pet_to_spr_proven': False, 'named_npc_to_spr_proven': False,
                'actual_screen_draw_or_palette_proven': False, 'original_server_master_recovered': False,
                'original_world_dat_recovered': False, 'original_assets_committed': False,
                'stage_a_closed': False, 'stage_b_started': False, 'wiki_started': False, 'overall_percent': None},
            'next': 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-102',
            'next_scope': 'Finite whole-portfolio material-gap review before expanding this low-level branch; no further rendering helpers without an upstream named identity or screen deliverable.'}


def main():
    p = argparse.ArgumentParser()
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--exe', type=Path)
    group.add_argument('--disc', type=Path)
    p.add_argument('--write', type=Path, required=True)
    args = p.parse_args()
    if args.exe:
        raw = args.exe.read_bytes()
    else:
        require(hashlib.sha256(args.disc.read_bytes()).hexdigest() == DISC_SHA, 'original disc hash mismatch')
        from tools.stoneage_tw10_technical_probe import find_rows, extract_row
        img, rows, _, _ = find_rows(args.disc)
        try:
            row = next(r for r in rows if r['path'] == 'StoneAge/sa_3.exe')
            with tempfile.TemporaryDirectory() as directory:
                out = Path(directory) / 'runtime.exe'
                extract_row(img, row, out)
                raw = out.read_bytes()
        finally:
            img.close()
    report = inspect(raw)
    args.write.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('R101 PASS: original selector and countdown instructions match bounded reference; named pet/NPC and live rendering remain OPEN')


if __name__ == '__main__':
    main()
