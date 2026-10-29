"""Accept SCENE18 derived metadata, preserving the unread REAL/pixel boundary.

No original images or programs are consumed. Cross-version equal ADRN records
identify an extraction candidate, never establish equality of unread pixels.
"""
import csv
import gzip
import hashlib
import json
import re
import struct
from pathlib import Path

from tools.stoneage_scene17_derived_acceptance import validate as validate_npc, REPORT as NPC
from tools.stoneage_logical_alias_catalog import SIGNED_ATTR, PINS, PATCH, NATIVE, EARLY

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-SCENE18-ORIGINAL-ADRN-SOURCE-R1.json'
RAW_SHA = 'f53d3630ed49dd06c3822972a2620001d1781bf232b1c9e8db21c3ab1b7c4213'
RECORD_SHA = '2273a098fa5e5f701c44ead12757cbb159570c43ceb5cf0120d32b1a71e5f524'
RD_SHA = 'ce21e49856dde81b79afa5854f400df31393b1d87a08e6357b0eb8fd2e5ad252'
TARGET = dict(index=5894, numeric_graphic_key=16048, bitmapno=5894,
              original_real_offset=25018537, original_real_size=1668,
              width=36, height=79, xoff=-18, yoff=-70,
              adrn_record_sha256=RECORD_SHA)
FALSE = ('actual_native_game_render_verified', 'original_archive_whole_sha_reverified',
         'original_copyrighted_bytes_uploaded', 'original_official_TW10_identity_verified',
         'original_sprite_pixels_decoded')


def need(ok, label):
    if not ok:
        raise ValueError(label)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def validate(r):
    need(r['schema'] == 'stoneage.scene18.original_NPC16048_ADRN_source.r1' and
         r['source_scope'] == 'PRESERVED_MIXED25_SAME_CARRIER_NOT_TW10_OR_NATIVE_RUNTIME', 'source scope')
    need(r['status'] == 'ADRN15_ONE_DECODER_WHOLE_SHA_CRC_SOURCE_RECORD', 'one-decoder status')
    need(all(r[k] is False for k in FALSE) and r['overall_completion_percent'] is None and
         type(r['original_real_bytes_read']) is int and r['original_real_bytes_read'] == 0, 'unread pixels and historical boundaries')
    need(validate_npc(json.loads(NPC.read_bytes()))['source_graphicname'] == r['source_graphic_key'] == 16048, 'original NPC key linkage')
    need(r['matched_count'] == 1 and r['source_record_matches'] == [TARGET], 'unique original ADRN record')
    a = r['archived_original_ADRN']
    need(a['name'].endswith('/stoneage2.5/data/adrn_15.bin') and a['size'] == 18765120 and
         a['whole_sha256'] == '92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74' and
         a['crc32'] == 823378952 and a['full_RAR_CRC32_verified'] is True and a['unar_result'] == 0, 'whole ADRN identity SHA CRC')
    need((a['header_offset'], a['data_offset'], a['packed_size'], a['flags'], a['method']) ==
         (2448577, 2448760, 2282198, 33472, 53), 'original ADRN header extent')
    need(a['original_header_sha256'] == '09bb0815b0893915bef64f457e35771559cf509e8670ede80a063211122558bb' and
         a['packed_payload_sha256'] == 'ab5ac38e6081b38f9f3831fd736f961a02ab5f2d38f99fff6d3d25a6950d68c7', 'compressed source evidence')
    need(a['independent_decompressors_equal'] is False and a['libarchive_version'] == 3007002 and
         a['secondary_decoder_failure']['type'] == 'ArchiveError' and
         a['secondary_decoder_failure']['message'].startswith('Parsing filters is unsupported.'), 'secondary decoder limitation preserved')
    real = r['archived_REAL_header_unfetched_payload']
    need(real['name'].endswith('/stoneage2.5/data/real_15.bin') and
         (real['size'], real['packed_size'], real['header_offset'], real['data_offset']) ==
         (763908374, 338458942, 5107864, 5108046), 'REAL header only')
    need(r['original_header_scan_count'] == 7954 and r['source_requests'] == 218 and
         r['http206_downloaded_bytes'] == 14242060, 'bounded source counts')
    spans = r['range_receipts']; seen = set(); total = 0
    need(len(spans) == 218, 'complete range receipts')
    for s in spans:
        key = (s['part'], s['start'])
        need(s['part'] in (1, 2) and s['start'] >= 0 and s['start'] % 65536 == 0 and
             0 < s['bytes'] <= 65536 and s['bytes'] == s['end'] - s['start'] + 1 and
             re.fullmatch('[0-9a-f]{64}', s['sha256']) and key not in seen, 'source range integrity')
        seen.add(key); total += s['bytes']
    need(total == r['http206_downloaded_bytes'], 'conserved source bytes')
    return dict(source_graphic_key=16048, physical_bitmapno=5894,
                dimensions=[36, 79], original_RD_bytes_read=0, original_world_entered=False)


def select(root, path):
    raw = (root / path).read_bytes()
    need(sha(raw) == PINS[path], 'pinned prior metadata ' + path)
    with gzip.open(root / path, 'rt', newline='') as f:
        rows = [r for r in csv.DictReader(f, delimiter='\t') if r['index'] == '5894']
    need(len(rows) == 1, 'one physical source position, no last-wins')
    return rows[0], dict(path=path, bytes=len(raw), sha256=sha(raw))


def crossversion(root=ROOT):
    patch, pin = select(root, PATCH)
    header = struct.pack('<IIIiiii', *[int(patch[k]) for k in ['bitmapno', 'adder', 'size', 'xoff', 'yoff', 'width', 'height']])
    attr = struct.pack('<BBH18h3H2xI', int(patch['atari_x']), int(patch['atari_y']), int(patch['hit_raw']),
                       *[int(patch[k]) for k in SIGNED_ATTR],
                       *[int(patch[k]) for k in ['damy_a', 'damy_b', 'damy_c', 'map_number']])
    need(len(header + attr) == 80 and sha(header + attr) == patch['record_sha256'] == RECORD_SHA and
         sha(attr) == patch['attr_sha256'] and int(patch['map_number']) == 16048, 'independent numeric 80B reconstruction')
    result = []
    for profile, path, field in [('TW10', EARLY['TW10']+'ADRN-R1.tsv.gz', 'rd_block_sha256'),
                                 ('CN50', EARLY['CN50']+'ADRN-R1.tsv.gz', 'rd_block_sha256'),
                                 ('TW85_NATIVE', NATIVE, 'rd_sha256')]:
        row, source = select(root, path)
        need(all(row[k] == patch[k] for k in ['bitmapno', 'adder', 'size', 'xoff', 'yoff', 'width', 'height', 'attr_sha256']) and
             row[field] == RD_SHA, 'prior numeric/header/content metadata agreement')
        if 'record_sha256' in row:
            need(row['record_sha256'] == RECORD_SHA, 'native exact original record')
        result.append(dict(profile=profile, source=source, physical_bitmapno=5894,
                           prior_RD_sha256=row[field], original_RD_bytes_read_this_turn=0))
    return dict(schema='stoneage.scene18.crossversion_extraction_candidate.r1',
                reconstructed_ADRN_record_sha256=RECORD_SHA, patch_source=pin,
                prior_samples=result, mixed25_REAL_RD_sha256=None,
                mixed25_RD_equality_verified=False, same_deployed_build_authenticated=False,
                original_NPC_name_or_dialogue_authenticated=False,
                original_sprite_pixels_decoded_this_turn=False, overall_completion_percent=None)


def main():
    raw = REPORT.read_bytes(); need(sha(raw) == RAW_SHA, 'exact original source artifact JSON')
    print(json.dumps({'source': validate(json.loads(raw)), 'crossversion': crossversion()}, sort_keys=True))


if __name__ == '__main__':
    main()
