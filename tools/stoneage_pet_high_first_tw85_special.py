"""PET14: source-bounded special RD diagnosis, static decoder anchors and master file census."""
from __future__ import annotations
import argparse
from collections import Counter
import gzip
import json
import mmap
from pathlib import Path
import re
import subprocess

from tools import stoneage_pet_high_first_tw85_pixels as pix
from tools import stoneage_pet_high_first_tw85_residual as residual
from tools.stoneage_pet_high_first_tw85_native import MANIFEST, parse_pe
from tools.stoneage_rd_codec import decode_legacy_rle, parse_rd_header

ROOT = pix.ROOT
TARGET = ROOT / 'research/pets/PET-HIGH-FIRST-14-TW85-SPECIAL-RD-AND-MASTER-CENSUS-R1.json'
ALBUM = ROOT / 'research/pets/PET-HIGH-FIRST-TW85-ORIGINAL-PE-ALBUM-GRID-R1.json'
SCOPE = 'PRESERVED_TW85_CLASSIC_PC_ONLY'
REFERENCE = {'repo': 'BismarckDD/stoneage', 'commit': '2f736808ff4361f5429ee919b718c88fabb60346',
             'path': 'client/stoneage/system/unpack.cpp', 'blob': '11d3438699891a03c940b0a8d76d658293a4e04b',
             'qualification': 'LATER_COMMUNITY_SOURCE_NOT_SAME_BUILD'}


def prior_inputs():
    plan, prior, reasons = residual.build_plan()
    report = json.loads(gzip.decompress(residual.TARGET.read_bytes()))
    summary = residual.verify(report, plan, prior, reasons)
    bad = {}
    for receipt in (prior, report['observations']):
        for key, row in receipt['observed_blocks'].items():
            if row['status'] != 'DUAL_DECODED_INDEX_PIXELS':
                if key in bad and bad[key] != row:
                    raise ValueError('prior observation drift')
                bad[key] = row
    unresolved = []
    for seq in report['observations']['sequences']:
        if residual.complete(seq, report['observations']):
            continue
        unresolved.append({'group': seq['physical_group'], 'spr': seq['spr'],
                           'animation': seq['animation_index'],
                           'bad_bitmapnos': sorted({f[0] for f in seq['frames'] if f[0] is not None
                              and report['observations']['observed_blocks'][str(report['observations']['frame_bitmap_to_adrn_index'][str(f[0])])]['status']
                              != 'DUAL_DECODED_INDEX_PIXELS'})})
    if (len(unresolved), len(bad), summary['cumulative_named_physical_groups_with_complete_sample']) != (8, 10, 510):
        raise ValueError('unexpected prior scope')
    return bad, unresolved


def source_style_runs(data, limit):
    """Independent bit-mask parser for the reference's bounded legacy domain.
    No unbounded writes; do not assume this is the native TW85 decoder."""
    out = bytearray()
    commands = []
    pos = 0
    while pos < len(data):
        start = pos
        cmd = data[pos]; pos += 1
        repeat = bool(cmd & 0x80)
        count = cmd & 15
        if repeat:
            if cmd & 0x40:
                value = 0
            else:
                if pos >= len(data):
                    raise ValueError('missing repeat byte')
                value = data[pos]; pos += 1
            extra = 2 if cmd & 0x20 else int(bool(cmd & 0x10))
        else:
            extra = int(bool(cmd & 0x10))
        if pos + extra > len(data):
            raise ValueError('missing count')
        for x in data[pos:pos+extra]:
            count = count * 256 + x
        pos += extra
        if len(out) + count > limit:
            raise ValueError('diagnostic output budget')
        before = len(out)
        if repeat:
            out.extend(bytes([value]) * count)
        else:
            if pos + count > len(data):
                raise ValueError('missing literal')
            out.extend(data[pos:pos+count]); pos += count
        commands.append({'payload_offset': start, 'output_start': before,
                         'count': count, 'family': 'repeat' if repeat else 'literal',
                         'end': len(out)})
    return bytes(out), commands


def diagnostic(block, row):
    h = parse_rd_header(block)
    if h['stored_size'] != len(block) or (h['width_s'], h['height_s']) != (row['width'], row['height']):
        raise ValueError('original RD header identity')
    item = {'header': h, 'block_bytes': len(block), 'rd_sha256': pix.sha(block)}
    w, height = h['width_s'], h['height_s']
    if w <= 0 or height <= 0:
        item.update(status='HEADER_ONLY_NONPOSITIVE_DIMENSION' if len(block) == 16 else 'NONPOSITIVE_DIMENSION_OPEN',
                    payload_bytes=len(block)-16, candidate_prefix_sha256=None)
        return item
    if h['flag'] != 1:
        raise ValueError('unexpected special flag')
    expected = w * height
    first = decode_legacy_rle(block[16:])
    second, commands = source_style_runs(block[16:], expected + 4096)
    if first != second:
        raise ValueError('reference parser disagreement')
    item.update(status='EXACT_RLE_STREAM_LENGTH_MISMATCH' if len(first) != expected else 'EXACT_LENGTH_REVIEW',
                expected_pixels=expected, decoded_stream_bytes=len(first),
                excess_bytes=len(first)-expected, final_command=commands[-1],
                full_stream_sha256=pix.sha(first),
                candidate_prefix_sha256=pix.sha(first[:expected]) if len(first) >= expected else None,
                excess_all_zero=all(x == 0 for x in first[expected:]) if len(first) > expected else None)
    return item


def master_census():
    raw = MANIFEST.read_bytes()
    report = json.loads(raw)
    files = report['inspection']['inventory']['samples'][0]['files']
    if len(files) != 557:
        raise ValueError('MSI file count drift')
    pattern = re.compile(r'enemy|pet|skill|master|charbase|npc|server|gmsv|saac', re.I)
    candidates = [{'path': x['path'], 'bytes': x['size'], 'sha256': x['sha256']}
                  for x in files if pattern.search(x['path'])]
    misc = [{'path': x['path'], 'bytes': x['size'], 'sha256': x['sha256']}
            for x in files if re.search(r'\.(dat|txt|bin)$', x['path'], re.I) and '/map/' not in x['path'].lower()]
    return {'manifest_sha256': pix.sha(raw), 'file_count': len(files),
            'extensions': dict(Counter(Path(x['path']).suffix.lower() for x in files)),
            'named_master_candidates': candidates, 'non_map_data_files': misc,
            'same_deployment_server_pet_master_verified': False,
            'filename_scan_cannot_exclude_embedded_tables': True}


def static_anchors(source_root, temporary):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    from capstone.x86_const import X86_OP_IMM, X86_OP_MEM
    grid = json.loads(ALBUM.read_bytes())['programs']['sa.exe']
    entry = next(x for x in json.loads(MANIFEST.read_bytes())['inspection']['inventory']['samples'][0]['files']
                 if Path(x['path']).name == 'sa.exe')
    packed = source_root / entry['path']
    if pix.sha(packed.read_bytes()) != grid['packed_sha256']:
        raise ValueError('sa.exe packed identity')
    plain = temporary / 'unpacked-sa.exe'
    subprocess.run(['upx','-d','-q','-o',str(plain),str(packed)], check=True, timeout=120)
    raw = plain.read_bytes()
    if pix.sha(raw) != grid['unpacked_sha256']:
        raise ValueError('sa.exe unpacked identity')
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True
    sections = parse_pe(raw)['sections']
    anchors = []
    for sec in sections:
        if not sec['name'].lower().startswith('.text'):
            continue
        off = sec['file_offset']; body = raw[off:off+sec['raw_size']]
        # Scan likely byte/word comparisons at exact file offsets, not arbitrary whole-file strings.
        for hit in re.finditer(rb'\x80[\x38-\x7f](?:[\x00-\xff]{0,4}?)\x52|\x66\x81[\x38-\x7f](?:[\x00-\xff]{0,4}?)\x52\x44', body):
            pos = hit.start()
            ins = list(md.disasm(body[pos:pos+380],sec['virtual_address']+pos, count=100))
            if not ins or ins[0].mnemonic != 'cmp' or len(ins[0].operands) != 2:
                continue
            a,b = ins[0].operands
            if a.type != X86_OP_MEM or b.type != X86_OP_IMM or b.imm not in (0x52,0x4452):
                continue
            second = next((i for i in ins[1:16] if i.mnemonic == 'cmp' and len(i.operands)==2
                           and i.operands[0].type==X86_OP_MEM and i.operands[1].type==X86_OP_IMM
                           and i.operands[1].imm==0x44 and i.operands[0].mem.base==a.mem.base
                           and i.operands[0].mem.disp==a.mem.disp+1), None)
            if b.imm == 0x52 and second is None:
                continue
            anchors.append({'rva': ins[0].address, 'source_window_sha256': pix.sha(body[pos:pos+380]),
                            'magic_comparison': 'BYTE_PAIR' if second else 'WORD',
                            'multiply_instruction_rvas': [i.address for i in ins if i.mnemonic in ('mul','imul')],
                            'direct_call_count': sum(i.mnemonic=='call' for i in ins)})
    return {'packed_sha256': grid['packed_sha256'], 'unpacked_sha256': grid['unpacked_sha256'],
            'candidate_anchors': anchors, 'native_decode_function_proven': False,
            'original_executable_run': False}


def build(source_root, temp):
    bad, groups = prior_inputs()
    data = source_root / 'Program Files/WAYI/石器時代 魔域大冒險/data'
    for filename in ('adrn_158.bin','real_158.bin'):
        pix.original_check(data / filename, pix.SOURCE_FILES[filename])
    adrn = (data / 'adrn_158.bin').read_bytes()
    observations = {}
    with (data / 'real_158.bin').open('rb') as f, mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as real:
        for key,row in bad.items():
            i=int(key); rec=adrn[i*80:(i+1)*80]
            bitmap, off, size, _, _, _, _, _=pix.COLS.unpack(rec)
            block=real[off:off+size]
            if (bitmap,pix.sha(rec),pix.sha(block)) != (row['bitmap'],row['adrn_sha256'],row['rd_sha256']):
                raise ValueError('special RD bytes changed')
            observations[key]=diagnostic(block,row)
    return {'scope': SCOPE,'source_reference':REFERENCE,'unresolved_groups':groups,
            'observations':observations,'native_static':static_anchors(source_root,temp),
            'master_census':master_census(),'official_live_pet_release_verified':False,
            'original_assets_published':False,'new_native_complete_groups':0}


def verify(report):
    bad, groups = prior_inputs()
    if (report['scope'],report['source_reference'],report['unresolved_groups'],report['master_census']) != (SCOPE,REFERENCE,groups,master_census()):
        raise ValueError('source or census drift')
    if set(report['observations']) != set(bad):
        raise ValueError('special coverage drift')
    for key,row in report['observations'].items():
        old=bad[key]
        if row['rd_sha256']!=old['rd_sha256'] or (row['header']['width_s'],row['header']['height_s'])!=(old['width'],old['height']):
            raise ValueError('special row drift')
        if row['status']=='HEADER_ONLY_NONPOSITIVE_DIMENSION' and (row['block_bytes']!=16 or row['payload_bytes']!=0 or row['candidate_prefix_sha256'] is not None):
            raise ValueError('invented nonimage pixel')
        if row['status']=='EXACT_RLE_STREAM_LENGTH_MISMATCH' and row['decoded_stream_bytes']-row['expected_pixels']!=row['excess_bytes']:
            raise ValueError('length mismatch arithmetic')
    if any(report[k] is not False for k in ('official_live_pet_release_verified','original_assets_published')) or report['new_native_complete_groups']!=0 or report['native_static']['native_decode_function_proven'] is not False:
        raise ValueError('unsupported promotion')
    return {'special_blocks':len(bad),'unresolved_groups':len(groups),
            'statuses':dict(Counter(x['status'] for x in report['observations'].values())),
            'excess_counts':dict(Counter(x['excess_bytes'] for x in report['observations'].values() if 'excess_bytes' in x)),
            'native_magic_candidates':len(report['native_static']['candidate_anchors']),
            'msi_files':report['master_census']['file_count'],
            'named_master_candidates':len(report['master_census']['named_master_candidates'])}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path)
    p.add_argument('--temp',type=Path)
    a=p.parse_args()
    if a.source_root:
        r=build(a.source_root,a.temp)
    else:
        r=json.loads(TARGET.read_bytes())
    print(json.dumps(verify(r),sort_keys=True))
    if a.source_root:
        TARGET.write_text(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
        print(json.dumps({'observations':r['observations'],'native_static':r['native_static']},sort_keys=True))

if __name__=='__main__':
    main()
