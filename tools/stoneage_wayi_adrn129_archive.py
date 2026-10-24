"""Replay every derived index row into its original record hash and aggregate.

Only numerical metadata and hashes are consumed. Original index bytes are
reconstructed transiently for hashing, never saved as a proprietary BIN.
"""
from collections import Counter
import csv
import gzip
import hashlib
import json
import struct
import subprocess

from tools.stoneage_wayi_adrn129_payload import ROOT, PARENT, BASES, HEADER, FIELDS, ARCHIVE_SHA, ARCHIVE_BYTES, URL, load_baseline
from tools.stoneage_tw85_map_payload import pin

DIR = ROOT/'research/recovered/wayi-adrn129-patch-metadata'
RECEIPT = ROOT/'research/recovered/STONEAGE-WAYI-ADRN129-PAYLOAD-CUSTODY-R1.json'
SIGNED = ('height_flag','broken','indamage','outdamage','inpoison','innumb','inquiet','instone',
          'indark','inconfuse','outpoison','outnumb','outquiet','outstone','outdark','outconfuse','effect1','effect2')


def require(value, message):
    if not value:
        raise ValueError(message)


def contract(report):
    require(report['schema'] == 'stoneage.wayi_adrn129_official_patch_payload.r1' and
            report['task'] == 'TW-WAYI-ADRN129-OFFICIAL-RESOURCE-PATCH-PAYLOAD-05', 'scope drift')
    require(report['archive_bytes'] == ARCHIVE_BYTES and report['archive_sha256'] == ARCHIVE_SHA and
            report['requested_url'] == report['final_url'] == URL, 'archive identity drift')
    require(report['source_capture'] == '2006-09-11T18:01:32Z' and report['listing_display_date'] == '2005-05-18' and
            report['source_role'] == 'OFFICIAL_LIST_DESCRIBED_75_BLACK_SCREEN_INDEX_REPAIR_2006_CAPTURE_BYTES', 'date/version promotion')
    keys = {'all_official_clients_collected','exact_2005_build_proven','game_or_installer_executed',
            'named_pet_npc_identity_proven','original_real_pixel_blocks_verified','original_server_master_recovered',
            'proprietary_payload_published','version_80_exclusivity_proven'}
    require(set(report['boundaries']) == keys and all(v is False for v in report['boundaries'].values()), 'evidence promotion')
    require(report['source_pins'] == {p: pin(ROOT/p) for p in (PARENT,*BASES.values())}, 'source parent drift')
    require(len(report['members']) == len(report['indexes']) == 1, 'member coverage drift')
    member = report['members'][0]
    require(member == {'path':'adrn_129.bin','bytes':31175840,
        'sha256':'4fb45027f87d44d70675827870a74110fb6c07f65a529bd89e6dc52c0a2b388f',
        'git_blob':'727aae965a62409b5bc8200d282a648a672e7bb1'}, 'member identity drift')
    info = report['indexes'][0]
    require(info['derived_table'] == 'INDEX-1-R1.tsv.gz' and info['member_path'] == member['path'] and
            info['format'] == '80_BYTE_HEADER28_ATTR52_LAYOUT', 'derived table path/format drift')
    require(info['records']*80 == member['bytes'] and info['distinct_bitmap_ids']+info['duplicate_bitmap_occurrences'] == info['records'],
            'record conservation drift')
    for comparison in info['comparisons_by_bitmap_id'].values():
        require(sum(comparison['counts'].values()) == info['records'], 'comparison count drift')
    return info


def replay_rows(rows, baselines):
    seen = Counter()
    ids_by_index = []
    duplicate_positions = []
    records = set()
    maps = set()
    counts = {k: Counter() for k in baselines}
    samples = {k: [] for k in baselines}
    changed_fields = {k: Counter() for k in baselines}
    body_hash = hashlib.sha256()
    min_b = None
    max_b = None
    max_end = 0
    special = 0
    number = 0
    for number, raw in enumerate(rows, 1):
        row = {k: (v if k in ('record_sha256','attr_sha256') else int(v)) for k,v in raw.items()}
        require(row['index'] == number-1, 'physical row order lost')
        head = struct.pack('<IIIiiii',*[row[k] for k in HEADER])
        attr = struct.pack('<BBH18h3H2xI',row['atari_x'],row['atari_y'],row['hit_raw'],
                    *[row[k] for k in SIGNED],*[row[k] for k in ('damy_a','damy_b','damy_c','map_number')])
        require(hashlib.sha256(attr).hexdigest() == row['attr_sha256'], 'attribute replay mismatch')
        require(hashlib.sha256(head+attr).hexdigest() == row['record_sha256'], 'whole record replay mismatch')
        require(row['hit_flag'] == row['hit_raw']%100 and row['priority_type'] == row['hit_raw']//100, 'hit interpretation arithmetic drift')
        body_hash.update(head+attr)
        bno = row['bitmapno']
        seen[bno] += 1
        ids_by_index.append(bno)
        if seen[bno] > 1:
            duplicate_positions.append({'index': row['index'], 'bitmapno': bno})
        records.add(row['record_sha256'])
        maps.add(row['map_number'])
        min_b = bno if min_b is None else min(min_b,bno)
        max_b = bno if max_b is None else max(max_b,bno)
        max_end = max(max_end,row['adder']+row['size'])
        special += int(not (0<row['width']<=16384 and 0<row['height']<=16384))
        key = (*[row[k] for k in HEADER],row['attr_sha256'])
        for name, table in baselines.items():
            old = table.get(bno)
            status = 'ABSENT_ID' if old is None else 'EXACT_HEADER_AND_ATTR_HASH' if key == old else 'CHANGED_INDEX_METADATA'
            counts[name][status] += 1
            if status != 'EXACT_HEADER_AND_ATTR_HASH' and len(samples[name]) < 8:
                samples[name].append({'index':row['index'],'bitmapno':bno,'status':status})
            if old is not None and old != key:
                changed_fields[name].update(k for k,a,b in zip((*HEADER,'attr_sha256'),key,old) if a!=b)
    metrics = {'records':number,'distinct_bitmap_ids':len(seen),'duplicate_bitmap_occurrences':sum(v-1 for v in seen.values()),
      'unique_record_hashes':len(records),'bitmap_min':min_b,'bitmap_max':max_b,'nonzero_distinct_map_numbers':len(maps-{0}),
      'max_declared_real_span_end':max_end,'special_dimensions_preserved':special,
      'comparisons_by_bitmap_id':{k:{'counts':dict(sorted(v.items())),'nonexact_samples':samples[k],
        'baseline_ids_absent_from_patch':len(set(baselines[k])-set(seen))} for k,v in counts.items()}}
    return metrics, {'reconstructed_member_sha256':body_hash.hexdigest(),'duplicate_positions':duplicate_positions,
        'changed_metadata_fields':{k:dict(sorted(v.items())) for k,v in changed_fields.items()},
        'distinct_patch_ids_absent_from_baselines':{k:len(set(seen)-set(v)) for k,v in baselines.items()}}


def validate():
    report = json.loads((DIR/'REPORT-R1.json').read_bytes())
    info = contract(report)
    require(pin(DIR/info['derived_table']) == info['derived_pin'], 'derived table byte drift')
    baselines = {name:load_baseline(ROOT/path) for name,path in BASES.items()}
    require(report['baseline_records'] == {k:len(v) for k,v in baselines.items()}, 'baseline coverage drift')
    with gzip.open(DIR/info['derived_table'],'rt',encoding='utf-8',newline='') as stream:
        reader = csv.DictReader(stream,delimiter='\t')
        require(tuple(reader.fieldnames) == FIELDS, 'metadata columns changed')
        metrics, replay = replay_rows(reader,baselines)
    expected = {k:v for k,v in info.items() if k not in ('member_path','format','derived_table','derived_pin')}
    require(metrics == expected, 'independent index metrics do not replay')
    require(replay['reconstructed_member_sha256'] == report['members'][0]['sha256'], 'original member whole SHA does not replay')
    receipt = json.loads(RECEIPT.read_bytes())
    require(receipt['report_pin'] == pin(DIR/'REPORT-R1.json'), 'report custody drift')
    require(receipt['artifact']['independent_zip_sha256'] == receipt['artifact']['api_zip_sha256'], 'artifact custody drift')
    for path, entry in receipt['historical_prefixes'].items():
        old = subprocess.check_output(['git','show',receipt['base_main']+':'+path],cwd=ROOT)
        require(len(old)==entry['bytes'] and hashlib.sha256(old).hexdigest()==entry['sha256'] and
                (ROOT/path).read_bytes().startswith(old), 'historical prefix loss: '+path)
    result = {'status':'PASS',**metrics,**replay}
    saved = ROOT/'research/recovered/STONEAGE-WAYI-ADRN129-INDEPENDENT-REPLAY-R1.json'
    require(pin(saved) == receipt['independent_replay_pin'] and json.loads(saved.read_bytes()) == result,
            'permanent independent replay differs from actual reconstruction')
    return result


if __name__ == '__main__':
    print(json.dumps(validate(),sort_keys=True))
