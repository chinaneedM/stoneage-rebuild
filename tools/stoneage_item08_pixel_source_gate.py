"""Qualify ITEM07 recovery locations against their actual TW85 pixel carrier.

The official patch supplies ADRN metadata only. RD fingerprints come from the
separately preserved TW85 REAL; no pixel payload is acquired by this program.
"""
import argparse
import copy
import json
from pathlib import Path
from tools import stoneage_item07_patch129_item_alias_crosswalk as prior

ROOT = prior.ROOT
NATIVE = ROOT / 'research/recovered/adrn129-tw85-real-pair/NATIVE-R1.tsv.gz'
PAIR_REPORT = ROOT / 'research/recovered/adrn129-tw85-real-pair/REPORT-R1.json'
OUTPUT = ROOT / 'research/recovered/STONEAGE-ITEM08-TW85-PIXEL-CARRIER-QUALIFICATION-R1.json'
PINS = {prior.OUTPUT:'6c0339d1f41e2eb7e67c460b461867817c35c575',
        NATIVE:'ffb7b3340116ecaf57daa08242c1ce271e3ad86f',
        PAIR_REPORT:'8377b3aeb2ea59f5ca23a5f8b9a0a7e8a85fb660'}


def qualify_occurrence(patch, native):
    checks = {
        'record_sha256': patch['source_record_sha256'],
        'bitmapno': str(patch['original_patch_physical_bitmapno']),
        'rd_sha256': patch['source_original_rd_sha256'],
        'size': str(patch['source_original_rd_size']),
        'width': str(patch['source_width']), 'height': str(patch['source_height']),
        'rd_status':'HEADER_MATCH',
    }
    for key, expected in checks.items():
        if native[key] != expected:
            raise ValueError('patch/native source mismatch: '+key)
    if (native['rd_width'], native['rd_height'], native['rd_size']) != (native['width'], native['height'], native['size']):
        raise ValueError('native RD header mismatch')
    if int(native['adder']) < 0 or int(native['size']) < 16:
        raise ValueError('invalid source block extent')
    return {**patch, 'tw85_native_record_index':int(native['index']),
            'tw85_real_byte_offset':int(native['adder']),
            'pixel_carrier':'TW85_PRESERVED_real_158.bin',
            'qualification':'EXACT_NATIVE_RECORD_AND_RD_HEADER_NOT_PIXEL_DECODE'}


def build():
    for path, expected in PINS.items():
        if prior.git_blob_sha(path) != expected:
            raise ValueError('pinned source changed: '+str(path))
    original = json.loads(prior.OUTPUT.read_text())
    wanted = {p['source_record_sha256'] for a in original['aliases'] for p in a['patch_source_occurrences']}
    native = {}
    rows = 0
    for row in prior.read_tsv(NATIVE):
        rows += 1
        if row['record_sha256'] in wanted:
            if row['record_sha256'] in native:
                raise ValueError('ambiguous native record SHA')
            native[row['record_sha256']] = row
    if rows != 416220 or len(native) != len(wanted):
        raise ValueError('incomplete native source identity join')
    missing = []
    qualified = 0
    for alias in original['aliases']:
        locations = [qualify_occurrence(p,native[p['source_record_sha256']]) for p in alias['patch_source_occurrences']]
        qualified += len(locations)
        if alias['mixed25_current_status'] == 'absent':
            entry = copy.deepcopy(alias)
            entry['patch_source_occurrences'] = locations
            missing.append(entry)
    if qualified != 826 or len(missing) != 416:
        raise ValueError('ITEM07 source conservation changed')
    carrier = json.loads(PAIR_REPORT.read_text())['containers']
    for alias in missing:
        for location in alias['patch_source_occurrences']:
            if location['tw85_real_byte_offset'] + location['source_original_rd_size'] > carrier['real']['bytes']:
                raise ValueError('candidate block outside qualified carrier')
    return {
        'schema':'stoneage.item08.tw85_pixel_carrier_qualification.r1',
        'source_pins_git_blobs':{str(p.relative_to(ROOT)):v for p,v in PINS.items()},
        'source_roles':{'official_20060911_patch':'adrn_129.bin index records; no REAL pixel payload',
                        'pixel_fingerprint_carrier':carrier,
                        'pixel_carrier_provenance':'COMMUNITY_PRESERVED_CLAIMED_TW85_NOT_AUTHENTICATED_OFFICIAL_PRESSING'},
        'summary':{'item07_occurrences_requalified':qualified,'native_source_rows_checked':rows,
                   'mixed25_missing_aliases':len(missing),'candidate_aliases':sum(bool(x['patch_source_occurrences']) for x in missing),
                   'candidate_record_locations':sum(len(x['patch_source_occurrences']) for x in missing),
                   'missing_in_patch_scope':7,'new_pixel_payload_bytes_read':0,'new_pixels_decoded':0},
        'recovery_candidates':missing,
        'boundaries':{'official_patch_contains_real_pixels':False,'full_tw85_alias_search_performed':False,
                       'original_ui_selector_verified':False,'official_same_deployment_verified':False,
                       'raw_pixels_in_public_git':False,'overall_percent':None},
    }


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=OUTPUT);args=parser.parse_args()
    report=build();args.output.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print(json.dumps(report['summary'],sort_keys=True))

if __name__=='__main__':main()
