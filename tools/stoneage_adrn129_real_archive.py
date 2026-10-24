"""Offline occurrence-preserving acceptance of the actual REAL source export.

R1 source diagnostics remain immutable. This overlay distinguishes a redundant
RD size-field mismatch from ADRN-authoritative raw-block structural validity.
It does not decode pixels or authenticate an official clean client build.
"""
from collections import Counter, defaultdict
import csv
import gzip
import itertools
import json
import re
import subprocess

from tools.stoneage_adrn129_real_pair import PATCH, CARRIER, BASELINE, HEADER, NATIVE_FIELDS, PAIR_FIELDS, pair_qualification
from tools.stoneage_tw85_map_payload import ROOT, pin
from tools.stoneage_wayi_adrn129_archive import require

DIR = ROOT/'research/recovered/adrn129-tw85-real-pair'
OVERLAY = ROOT/'research/recovered/STONEAGE-ADRN129-REAL-ACCEPTANCE-R1.json'
RECEIPT = ROOT/'research/recovered/STONEAGE-ADRN129-REAL-CUSTODY-R1.json'
CODEC = 'tools/stoneage_rd_codec.py'
BOUNDARIES = {'official_2005_same_build_proven','source_pixel_semantics_or_species_proven',
    'all_images_decoded_or_drawn','original_game_executed','duplicate_id_winner_chosen',
    'proprietary_pixels_or_bins_published','official_clean_tw85_pressing_authenticated','server_npc_pet_quest_tables_recovered'}


def structural_status(row, real_size):
    """A bounded RD header and matching dimensions; flag-0 has an exact payload.

    Source read/hash/magic attestation is mandatory. This narrower compatibility
    exception follows decode_rd_block's ADRN-authoritative slice; the R1 raw
    length field is retained, never repaired. Compressed payload is not decoded.
    """
    if row['size'] < 16 or row['adder'] < 0 or row['adder']+row['size'] > real_size:
        return 'NOT_QUALIFIED'
    if row['rd_status'] not in ('HEADER_MATCH','HEADER_MISMATCH') or not re.fullmatch('[0-9a-f]{64}',row['rd_sha256']):
        return 'NOT_QUALIFIED'
    if (row['width'],row['height']) != (row['rd_width'],row['rd_height']):
        return 'NOT_QUALIFIED'
    if row['rd_size'] == row['size']:
        return 'MATCHING_RD_HEADER'
    if row['rd_flag'] == 0 and row['width'] > 0 and row['height'] > 0 and row['size'] == 16+row['width']*row['height']:
        return 'RAW_FLAG0_ADRN_SIZE_AUTHORITATIVE'
    return 'NOT_QUALIFIED'


def contract(report):
    require(report['schema']=='stoneage.adrn129_tw85_real_pair.r1' and report['task']=='TW-WAYI-ADRN129-REAL-COMPANION-QUALIFICATION-06','scope drift')
    require(set(report['boundaries'])==BOUNDARIES and all(v is False for v in report['boundaries'].values()),'evidence promotion')
    require(report['source_pins']=={p:pin(ROOT/p) for p in (PATCH,CARRIER,BASELINE)},'source parent drift')
    carrier=json.loads((ROOT/CARRIER).read_bytes())['inspection']['inventory']['samples'][0]['files']
    require(set(report['containers'])=={'adrn','real'},'container coverage drift')
    for kind,name in [('adrn','adrn_158.bin'),('real','real_158.bin')]:
        actual=report['containers'][kind]
        old=next(x for x in carrier if x['path'].endswith('/data/'+name))
        require(actual['name']==name and actual['bytes']==old['size'] and actual['sha256']==old['sha256'],'actual source container identity drift')
    require(set(report['tables'])=={'NATIVE-R1.tsv.gz','PAIRS-R1.tsv.gz'},'table coverage drift')
    for name,expected in report['tables'].items():
        require(pin(DIR/name)==expected,'derived table bytes drift')


def rows(path,fields=None):
    with gzip.open(path,'rt',encoding='utf-8',newline='') as stream:
        reader=csv.DictReader(stream,delimiter='\t')
        if fields is not None:require(tuple(reader.fieldnames)==fields,'table column drift')
        yield from reader


def replay(report):
    native=[];keys=defaultdict(list);ids=Counter();statuses=Counter();corrected=Counter();extents=set()
    baseline={int(r['bitmapno']):r['rd_block_sha256'] for r in rows(ROOT/BASELINE)}
    comparison=Counter();exceptions=[]
    real_size=report['containers']['real']['bytes']
    for i,raw in enumerate(rows(DIR/'NATIVE-R1.tsv.gz',NATIVE_FIELDS)):
        row={k:(v if k in ('record_sha256','attr_sha256','rd_status','rd_sha256') else int(v)) for k,v in raw.items()}
        require(row['index']==i,'native physical order lost')
        diagnostic='HEADER_MATCH' if (row['width'],row['height'],row['size'])==(row['rd_width'],row['rd_height'],row['rd_size']) else 'HEADER_MISMATCH'
        require(row['rd_status']==diagnostic,'strict source header diagnostic drift')
        status=structural_status(row,real_size)
        require(status!='NOT_QUALIFIED','unqualified native structure')
        if status=='RAW_FLAG0_ADRN_SIZE_AUTHORITATIVE':
            exceptions.append({k:row[k] for k in ('index',*HEADER,'rd_flag','rd_size','rd_sha256')})
        corrected[status]+=1;statuses[row['rd_status']]+=1;ids[row['bitmapno']]+=1
        keys[(row['bitmapno'],row['record_sha256'])].append(i)
        extents.add((row['adder'],row['size']))
        old=baseline.get(row['bitmapno'])
        comparison['ABSENT_ID' if old is None else 'SAME_RD_BLOCK_BYTES' if old==row['rd_sha256'] else 'CHANGED_RD_BLOCK_BYTES']+=1
        native.append(row)
    require(len(native)*80==report['containers']['adrn']['bytes'],'native record conservation drift')
    patch_ids=Counter();patch_keys=set();pstatus=Counter();pqual=Counter();multiplicity=Counter();pcorrected=Counter();samples=[];patch_exceptions=[];count=0
    for i,(patch,pair) in enumerate(itertools.zip_longest(rows(ROOT/PATCH),rows(DIR/'PAIRS-R1.tsv.gz',PAIR_FIELDS))):
        require(patch is not None and pair is not None,'patch/pair coverage differs')
        require(int(patch['index'])==int(pair['patch_index'])==i,'patch physical order lost')
        key=(int(patch['bitmapno']),patch['record_sha256']);exact=keys.get(key,[])
        require(pair['bitmapno']==patch['bitmapno'] and pair['patch_record_sha256']==patch['record_sha256'] and
                pair['native_exact_indices']==','.join(map(str,exact)),'exact native candidates overwritten or changed')
        require(exact,'no actual native record match')
        for index in exact:
            target=native[index]
            require(all(int(patch[k])==target[k] for k in HEADER) and patch['attr_sha256']==target['attr_sha256'],'exact hash join disagrees with fields')
            require(pair['rd_status']==target['rd_status'] and pair['rd_sha256']==target['rd_sha256'],'patch REAL read differs from native read')
        expected=pair_qualification(exact,pair['rd_status'])
        require(pair['qualification']==expected,'R1 diagnostic qualification changed')
        corrected_status=structural_status(native[exact[0]],real_size)
        pcorrected[corrected_status]+=1
        if corrected_status=='RAW_FLAG0_ADRN_SIZE_AUTHORITATIVE':
            patch_exceptions.append({'patch_index':i,'bitmapno':key[0],'native_exact_indices':exact})
        patch_ids[key[0]]+=1;patch_keys.add(key);pstatus[pair['rd_status']]+=1;pqual[expected]+=1;multiplicity[str(len(exact))]+=1
        if len(samples)<5:samples.append({**pair,'bitmapno':int(pair['bitmapno'])})
        count+=1
    metrics={'native_records':len(native),'native_distinct_bitmap_ids':len(ids),'native_duplicate_number_occurrences':sum(v-1 for v in ids.values()),
        'native_rd_status_counts':dict(statuses),'native_rd_hash_comparison_with_cn50':dict(comparison),
        'patch_records':count,'patch_distinct_bitmap_ids':len(patch_ids),'patch_duplicate_number_occurrences':sum(v-1 for v in patch_ids.values()),
        'patch_qualification_counts':dict(pqual),'patch_rd_status_counts':dict(pstatus),'exact_native_match_multiplicity':dict(multiplicity),
        'native_records_not_exactly_present_in_patch':sum(len(v) for k,v in keys.items() if k not in patch_keys),
        'first_pair_samples':samples,'unique_real_extents_hashed':len(extents)}
    require(metrics==report['metrics'],'source R1 metrics do not independently replay')
    return {'schema':'stoneage.adrn129_real_acceptance.r1','status':'PASS','source_report_pin':pin(DIR/'REPORT-R1.json'),
        'policy_code_pin':pin(ROOT/CODEC),'policy':'ADRN-authoritative block length; exact raw flag-0 payload exception to redundant RD length field',
        'source_strict_metrics_unchanged':metrics,'native_structure_counts':dict(corrected),'patch_structure_counts':dict(pcorrected),
        'qualified_native_records':sum(corrected.values()),'qualified_patch_records':sum(pcorrected.values()),
        'native_raw_length_exceptions':exceptions,'patch_raw_length_exceptions':patch_exceptions,
        'raw_length_field_minus_adrn_size_counts':dict(Counter(str(r['rd_size']-r['size']) for r in exceptions)),
        'pixel_decoding_or_rendering_verified':False,'named_species_npc_or_quest_binding_proven':False}


def validate():
    report=json.loads((DIR/'REPORT-R1.json').read_bytes());contract(report)
    result=replay(report)
    require(json.loads(OVERLAY.read_bytes())==result,'immutable acceptance overlay differs from replay')
    receipt=json.loads(RECEIPT.read_bytes())
    require(receipt['acceptance_pin']==pin(OVERLAY),'acceptance custody drift')
    require(receipt['derived_pins']=={p.name:pin(p) for p in sorted(DIR.iterdir()) if p.is_file()},'derived custody drift')
    require(receipt['artifact']['independent_zip_sha256']==receipt['artifact']['api_zip_sha256'] and receipt['artifact']['all_members_exactly_equal_git_bytes'] is True,'artifact custody drift')
    for path,expected in receipt['historical_prefixes'].items():
        old=subprocess.check_output(['git','show',receipt['base_main']+':'+path],cwd=ROOT)
        require(len(old)==expected['bytes'] and (ROOT/path).read_bytes().startswith(old),'historical prefix lost: '+path)
    return {'status':'PASS','qualified_patch_records':result['qualified_patch_records'],'qualified_native_records':result['qualified_native_records'],
        'native_raw_length_exceptions':len(result['native_raw_length_exceptions']),'patch_raw_length_exceptions':len(result['patch_raw_length_exceptions'])}


if __name__=='__main__':print(json.dumps(validate(),sort_keys=True))
