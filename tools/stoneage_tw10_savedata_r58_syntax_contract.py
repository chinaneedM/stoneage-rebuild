"""Pinned R58 static-only register-return spelling; no native I/O semantics.

This deliberately checks literal operand shapes, not actual branch feasibility,
ABI preservation, persisted bytes, success statuses or original game execution.
"""
import argparse
import hashlib
import json
from pathlib import Path

SHA = '04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8'
SCHEMA = 'tw10-r58-pinned-shared-close-conditional-return-syntax'

def expect_row(rows, site, mnemonic, operands):
    row = rows.get(site)
    if not row or row.get('mnemonic') != mnemonic:
        raise ValueError('R58 expected static instruction absent at ' + hex(site))
    actual = [(x.get('kind'), x.get('register'), x.get('constant')) for x in row['operands']]
    if actual != operands:
        raise ValueError('R58 exact operand spelling mismatch at ' + hex(site))
    return row

def derive(raw):
    if len(raw) != 124989 or hashlib.sha256(raw).hexdigest() != SHA:
        raise ValueError('R58 immutable original-derived source mismatch')
    report = json.loads(raw)
    if report.get('schema') != 'tw10-r58-original-rooted-shared-close-helper-static-inventory' or len(report.get('contexts', [])) != 2:
        raise ValueError('R58 root/schema mismatch')
    shared, close = report['contexts']
    if (shared['root_candidate_rva'],close['root_candidate_rva']) != (0x4a657,0x4a53e) or not all(c['bounded_graph_complete'] for c in (shared,close)):
        raise ValueError('R58 graph/source scope mismatch')
    w = {r['site_rva']:r for r in shared['instruction_shapes']}
    c = {r['site_rva']:r for r in close['instruction_shapes']}
    R=lambda name:('register',name,None)
    I=lambda value:('immediate',None,value)
    expect_row(w,0x4a65d,'xor',[R('ebx'),R('ebx')])
    expect_row(w,0x4a6a1,'or',[R('ebx'),I(0xffffffff)])
    expect_row(w,0x4a6ae,'mov',[R('eax'),R('ebx')])
    expect_row(w,0x4a6b2,'ret',[])
    expect_row(w,0x4a68b,'cmp',[R('eax'),R('edi')])
    expect_row(c,0x4a5d4,'xor',[R('eax'),R('eax')])
    expect_row(c,0x4a5e9,'or',[R('eax'),I(0xffffffff)])
    expect_row(c,0x4a5f0,'ret',[])
    calls = {x['site_rva']:x['identity'].get('direct_target_rva') for x in shared['call_contexts']}
    if calls.get(0x4a683) != 0x4c5b4:
        raise ValueError('R58 helper original subcall changed')
    indirect = [x['site_rva'] for x in close['call_contexts']
                if x['identity'].get('kind') == 'memory_indirect']
    if indirect != [0x4a5a3,0x4a5ad]:
        raise ValueError('R58 unknown indirect helper set changed')
    result = {
        'schema':SCHEMA,'source_sha256':SHA,
        'shared_helper':{
            'root_rva':0x4a657,'zero_ebx_source_rva':0x4a65d,
            'all_ones_ebx_source_rva':0x4a6a1,'eax_from_ebx_rva':0x4a6ae,
            'return_rva':0x4a6b2,
            'native_context_subcall_rva':0x4a683,
            'native_context_subcall_target_rva':0x4c5b4,
            'postcall_eax_edi_compare_rva':0x4a68b,
            'syntactic_conditional_register_result':'EAX gets EBX; EBX has zero/all-one direct writes but opaque call and alias preservation remain unknown',
            'original_ebx_value_or_proven_call_preservation':False,
        },
        'close_path_helper':{
            'root_rva':0x4a53e,'zero_eax_source_rva':0x4a5d4,
            'all_ones_eax_source_rva':0x4a5e9,'return_rva':0x4a5f0,
            'indirect_opaque_call_rvas':indirect,
            'conditional_return_bitpatterns':['0x00000000','0xffffffff'],
            'native_error_or_success_conventions_proven':False,
        },
        'actual_native_write_flush_close_descriptor_ownership_or_persistence_proven':False,
        'original_code_executed':False,
    }
    return result

def validate(contract,raw):
    if json.dumps(contract,sort_keys=True,separators=(',',':')) != json.dumps(derive(raw),sort_keys=True,separators=(',',':')):
        raise ValueError('R58 conditional return contract changed')
    return True

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--verify',type=Path);args=ap.parse_args()
    raw=args.source.read_bytes()
    if args.verify:
        validate(json.loads(args.verify.read_text()),raw)
        print('TW10_R58_CONDITIONAL_RETURN_SPELLING=PASS; NATIVE_PERSISTENCE=OPEN')
    else:
        print(json.dumps(derive(raw),sort_keys=True))

if __name__=='__main__':
    main()
