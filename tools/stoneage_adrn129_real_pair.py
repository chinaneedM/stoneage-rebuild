"""Pair original repair-index records with actual preserved TW8.5 REAL bytes.

All native/patch occurrences survive. Only derived index metadata and RD block
hashes are exported; no pixels, raw containers or new species names.
"""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import json
import mmap
from pathlib import Path
import struct

from tools.stoneage_tw85_map_payload import ROOT, pin, digest
from tools.stoneage_tw10_resource_metadata import parse_adrn_record, DeterministicGzipTsv
from tools.stoneage_wayi_adrn129_payload import HEADER
from tools.stoneage_wayi85_sixpart_acquisition import acquire as acquire_tw85

PATCH = 'research/recovered/wayi-adrn129-patch-metadata/INDEX-1-R1.tsv.gz'
PATCH_SHA = 'd8049cb6ce74a2c048372aa51fc81b6921a995b6fa45b03dd5511a93509958ca'
CARRIER = 'research/recovered/STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json'
BASELINE = 'research/recovered/cn50-resource-metadata/ADRN-R1.tsv.gz'
NATIVE_FIELDS = ('index',*HEADER,'record_sha256','attr_sha256','rd_status','rd_sha256','rd_flag','rd_width','rd_height','rd_size')
PAIR_FIELDS = ('patch_index','bitmapno','patch_record_sha256','native_exact_indices','rd_status','rd_sha256','qualification')


def inspect_rd(real, row, cache):
    address,size = row['adder'],row['size']
    if size < 16 or address < 0 or address+size > len(real):
        return ('OUT_OF_BOUNDS_OR_SHORT','',-1,0,0,0)
    key = (address,size)
    if key not in cache:
        block = real[address:address+size]
        if block[:2] != b'RD':
            cache[key] = ('BAD_RD_MAGIC',digest(block),-1,0,0,0)
        else:
            width,height,length = struct.unpack_from('<iiI',block,4)
            cache[key] = ('RD',digest(block),block[2],width,height,length)
    status,sha,flag,width,height,length = cache[key]
    if status == 'RD':
        status = 'HEADER_MATCH' if (width,height,length)==(row['width'],row['height'],size) else 'HEADER_MISMATCH'
    return status,sha,flag,width,height,length


def pair_qualification(exact, rd_status):
    if rd_status != 'HEADER_MATCH':
        return 'RD_STRUCTURE_NOT_QUALIFIED'
    return 'EXACT_NATIVE_RECORD_AND_RD_STRUCTURE' if exact else 'RD_STRUCTURE_ONLY_NO_EXACT_NATIVE_RECORD'


def export_pairing(adrn_path, real_path, patch_path, output, baseline_path=None):
    raw = adrn_path.read_bytes()
    if not raw or len(raw)%80:
        raise ValueError('native ADRN record remainder')
    output.mkdir(parents=True,exist_ok=True)
    native_by_key = defaultdict(list)
    native_ids = Counter()
    native_status = Counter()
    cache = {}
    native_exact_hashes = set()
    baseline = {}
    with gzip.open(baseline_path or ROOT/BASELINE,'rt') as f:
        for row in csv.DictReader(f,delimiter='\t'):
            baseline[int(row['bitmapno'])] = row['rd_block_sha256']
    baseline_counts = Counter()
    with real_path.open('rb') as source:
        real = mmap.mmap(source.fileno(),0,access=mmap.ACCESS_READ)
        try:
            with DeterministicGzipTsv(output/'NATIVE-R1.tsv.gz') as stream:
                stream.write('\t'.join(NATIVE_FIELDS)+'\n')
                for index,offset in enumerate(range(0,len(raw),80)):
                    record = raw[offset:offset+80]
                    row = parse_adrn_record(record)
                    sha = digest(record)
                    native_by_key[(row['bitmapno'],sha)].append(index)
                    native_ids[row['bitmapno']] += 1
                    native_exact_hashes.add(sha)
                    status,rd_sha,flag,width,height,length = inspect_rd(real,row,cache)
                    native_status[status] += 1
                    row.update(index=index,record_sha256=sha,rd_status=status,rd_sha256=rd_sha,
                               rd_flag=flag,rd_width=width,rd_height=height,rd_size=length)
                    stream.write('\t'.join(str(row[k]) for k in NATIVE_FIELDS)+'\n')
                    old = baseline.get(row['bitmapno'])
                    baseline_counts['ABSENT_ID' if old is None else 'SAME_RD_BLOCK_BYTES' if old==rd_sha else 'CHANGED_RD_BLOCK_BYTES'] += 1
            patch_ids = Counter()
            patch_keys = set()
            statuses = Counter()
            rd_counts = Counter()
            multiplicity = Counter()
            patch_count = 0
            qualified_samples = []
            with gzip.open(patch_path,'rt',encoding='utf-8') as source, DeterministicGzipTsv(output/'PAIRS-R1.tsv.gz') as stream:
                stream.write('\t'.join(PAIR_FIELDS)+'\n')
                for patch in csv.DictReader(source,delimiter='\t'):
                    row = {k:int(patch[k]) for k in HEADER}
                    key = (row['bitmapno'],patch['record_sha256'])
                    exact = native_by_key.get(key,[])
                    status,sha,*unused = inspect_rd(real,row,cache)
                    qualification = pair_qualification(exact,status)
                    values = (patch['index'],row['bitmapno'],patch['record_sha256'],','.join(map(str,exact)),status,sha,qualification)
                    stream.write('\t'.join(map(str,values))+'\n')
                    patch_ids[row['bitmapno']] += 1
                    patch_keys.add(key)
                    patch_count += 1
                    statuses[qualification] += 1
                    rd_counts[status] += 1
                    multiplicity[len(exact)] += 1
                    if len(qualified_samples)<5:
                        qualified_samples.append(dict(zip(PAIR_FIELDS,values)))
        finally:
            real.close()
    return {'native_records':len(raw)//80,'native_distinct_bitmap_ids':len(native_ids),
      'native_duplicate_number_occurrences':sum(v-1 for v in native_ids.values()),
      'native_rd_status_counts':dict(sorted(native_status.items())),
      'native_rd_hash_comparison_with_cn50':dict(sorted(baseline_counts.items())),
      'patch_records':patch_count,'patch_distinct_bitmap_ids':len(patch_ids),
      'patch_duplicate_number_occurrences':sum(v-1 for v in patch_ids.values()),
      'patch_qualification_counts':dict(sorted(statuses.items())),'patch_rd_status_counts':dict(sorted(rd_counts.items())),
      'exact_native_match_multiplicity':{str(k):v for k,v in sorted(multiplicity.items())},
      'native_records_not_exactly_present_in_patch':sum(len(v) for key,v in native_by_key.items() if key not in patch_keys),
      'first_pair_samples':qualified_samples,'unique_real_extents_hashed':len(cache)}


def acquire(work,derived):
    if pin(ROOT/PATCH)['sha256'] != PATCH_SHA:
        raise ValueError('qualified repair metadata drift')
    acquire_tw85(work,work/'acquisition.json')
    carrier = json.loads((ROOT/CARRIER).read_bytes())
    root = work/'msi-client/Program Files/WAYI/石器時代 魔域大冒險'
    containers = {}
    for kind,name in [('adrn','adrn_158.bin'),('real','real_158.bin')]:
        path = root/'data'/name
        expected = next(x for x in carrier['inspection']['inventory']['samples'][0]['files'] if x['path'].endswith('/data/'+name))
        actual = pin(path)
        if actual['bytes'] != expected['size'] or actual['sha256'] != expected['sha256']:
            raise ValueError('actual MSI source container differs from qualified file inventory')
        containers[kind] = {'name':name,**actual}
    metrics = export_pairing(root/'data/adrn_158.bin',root/'data/real_158.bin',ROOT/PATCH,derived)
    report={'schema':'stoneage.adrn129_tw85_real_pair.r1','task':'TW-WAYI-ADRN129-REAL-COMPANION-QUALIFICATION-06',
      'source_pins':{p:pin(ROOT/p) for p in (PATCH,CARRIER,BASELINE)},'containers':containers,'metrics':metrics,
      'tables':{name:pin(derived/name) for name in ('NATIVE-R1.tsv.gz','PAIRS-R1.tsv.gz')},
      'boundaries':{k:False for k in ('official_2005_same_build_proven','source_pixel_semantics_or_species_proven',
        'all_images_decoded_or_drawn','original_game_executed','duplicate_id_winner_chosen',
        'proprietary_pixels_or_bins_published','official_clean_tw85_pressing_authenticated','server_npc_pet_quest_tables_recovered')}}
    (derived/'REPORT-R1.json').write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print(json.dumps(metrics,ensure_ascii=False,sort_keys=True),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);parser.add_argument('--derived',type=Path,required=True)
    args=parser.parse_args();args.work.mkdir(parents=True,exist_ok=True);args.derived.mkdir(parents=True,exist_ok=True)
    try:acquire(args.work.resolve(),args.derived.resolve())
    except Exception as exc:
        (args.derived/'ATTEMPT-R1.json').write_text(json.dumps({'status':'FAILURE','error_type':type(exc).__name__,'error':str(exc)[:500]},indent=2)+'\n')
        raise
