"""Read-only local reacceptance of O16 originals; never render or publish assets.

Public CI runs synthetic framing tests only. --original-zip authenticates the
existing private P3H package and replays every native manifest slice and source
bitmap through the two previously independent codecs. Only hashes/counts leave
this process. It does not execute a game or establish runtime palette semantics.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import struct
import zipfile

from tools.stoneage_o16_battle_source_boundary import ensure, load, validate
from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_scene29_tw10_battle_pet import alternate_rle


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def manifest(raw, container):
    """Keep on-disk order, reject holes/overlap/tails and ambiguous paths."""
    rows = []
    cursor = 0
    names = set()
    for line in raw.decode('ascii').splitlines():
        match = re.fullmatch(r'(\d+):(\d+):((?:battle\d+\.sab)|(?:Palet_\d+\.sap))', line)
        ensure(match is not None, 'native manifest line')
        offset, length = map(int, match.group(1, 2))
        name = match.group(3)
        ensure(offset == cursor and length > 0 and offset + length <= len(container), 'native extent')
        ensure(name not in names, 'duplicate native name')
        names.add(name)
        rows.append((offset, length, name))
        cursor += length
    ensure(rows and cursor == len(container), 'unaccounted container bytes')
    return rows


def replay(path):
    report, old, scene = load()
    validate(report, old, scene)
    source = report['original_source']
    ensure(path.stat().st_size == source['archive_bytes'], 'private package length')
    with path.open('rb') as stream:
        ensure(hashlib.file_digest(stream, 'sha256').hexdigest() == source['archive_sha256'], 'private package identity')
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        ensure(len(names) == len(set(names)) == 379, 'private original package membership')
        originals = {}
        for name, prefix in [('battle_1.bin', 'battle_1_bin'), ('battletxt_1.txt', 'battletxt'),
                             ('adrn_1.bin', 'adrn'), ('real_1.bin', 'real')]:
            raw = archive.read('source/data/' + name)
            ensure(len(raw) == source[prefix + '_bytes'] and sha(raw) == source[prefix + '_sha256'], 'original member identity: ' + name)
            originals[name] = raw
        container = originals['battle_1.bin']
        rows = manifest(originals['battletxt_1.txt'], container)
        ensure(len(rows) == 233, 'native entry census')
        maps, palettes = {}, []
        for offset, length, name in rows:
            is_map = name.endswith('.sab')
            raw = archive.read('source/data/' + ('battlemap/' if is_map else 'pal/') + name)
            ensure(len(raw) == length and container[offset:offset + length] == raw, 'original standalone/container mismatch')
            if is_map:
                num = int(name[6:-4])
                expected = report['battle_sab_records'][num]
                ensure((offset, length, sha(raw)) == (expected['packed_offset'], expected['bytes'], expected['sha256']), 'map receipt mismatch')
                ensure(raw[:4] == b'SAB ' and length == 804, 'native SAB envelope')
                maps[num] = struct.unpack('>400H', raw[4:])
            else:
                palettes.append(dict(name=name, packed_offset=offset, bytes=length, sha256=sha(raw)))
        ensure(palettes == report['embedded_palette_records'], 'all original palette receipts')
        ensure(sorted(maps) == list(range(218)), 'all native maps')
        wanted = {num for cells in maps.values() for num in cells}
        adrn = originals['adrn_1.bin']
        records = defaultdict(list)
        for offset in range(0, len(adrn), 80):
            fields = struct.unpack_from('<7i', adrn, offset)
            if fields[0] in wanted:
                records[fields[0]].append(fields)
        ensure(len(wanted) == 2296 and all(len(records[num]) == 1 for num in wanted), 'same-build physical bitmap census')
        real = originals['real_1.bin']
        failures, decoded = [], []
        pixels_count = 0
        for num in sorted(wanted):
            _, offset, length, _, _, width, height = records[num][0]
            ensure(0 <= offset <= len(real) - length and length >= 16, 'RD extent')
            raw = real[offset:offset + length]
            ensure(struct.unpack_from('<ii', raw, 4) == (width, height), 'ADRN/RD geometry')
            results = []
            errors = []
            for decoder in (lambda: decode_rd_block(raw, length)[1], lambda: alternate_rle(raw, width, height)):
                try:
                    results.append(decoder())
                except ValueError as error:
                    errors.append(str(error))
            if errors:
                ensure(len(errors) == 2 and num == 6729, 'unexpected decoder failure/disagreement')
                ensure('exceeds expected length' in errors[0] and 'output overflow' in errors[1], 'unexpected unresolved codec reason')
                failures.append(dict(bitmap_id=num, bytes=length, sha256=sha(raw), width=width, height=height,
                                     flag=raw[2], unknown_header_byte=raw[3], decoder_errors=errors,
                                     scene_ids=[i for i, cells in maps.items() if num in cells]))
                continue
            ensure(results[0] == results[1] and len(results[0]) == width * height, 'independent RD pixels')
            pixels_count += len(results[0])
            decoded.append((num, sha(results[0])))
        coverage = report['source_bitmap_coverage']
        ensure(len(decoded) == coverage['source_rd_decoded'] and pixels_count == coverage['decoded_original_pixel_positions'], 'decoded coverage')
        ensure(len(failures) == 1 and failures[0]['sha256'] == coverage['source_rd_codec_open_sha256'] and failures[0]['scene_ids'] == [181], 'unresolved original bitmap')
        ensure((failures[0]['width'], failures[0]['height'], failures[0]['flag'], failures[0]['unknown_header_byte']) == (40, 30, 1, 16), 'unresolved source dimensions')
        full_maps = [i for i, cells in maps.items() if not any(row['bitmap_id'] in cells for row in failures)]
        ensure(len(full_maps) == 217, 'complete source-RD map coverage')
    # Inventory of this *saved research package*, never a claim about the full
    # retail carrier or all possible archived clients/server deployments.
    dat_names = [name for name in names if name.lower().endswith('.dat')]
    ensure(dat_names == ['source/data/savedata.dat'], 'saved package DAT inventory changed')
    digest = sha(''.join(f'{num}:{digest}\n' for num, digest in decoded).encode('ascii'))
    return dict(schema='stoneage.o16.independent_original_reacceptance.r1',
                private_source_sha256=source['archive_sha256'], source_members_rehashed=4,
                original_manifest_entries=len(rows), original_slices_equal_standalones=len(rows),
                original_sabs=len(maps), original_palettes=len(palettes), source_cell_occurrences=sum(map(len, maps.values())),
                distinct_original_bitmap_ids=len(wanted), independently_decoded_bitmaps=len(decoded),
                decoded_index_bytes=pixels_count, decoded_id_and_sha_ascii_lines_sha256=digest,
                codec_open=failures, scenes_with_complete_source_rd_coverage=len(full_maps),
                private_package_dat_member_names=dat_names,
                private_package_scope_only=True, original_world_map_dat_in_saved_package=False,
                original_game_executed=False, original_pixels_exported=False, private_browser_reexecuted=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original-zip', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(replay(args.original_zip), indent=2, ensure_ascii=False))
