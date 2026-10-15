"""R59 bounded *existing-source* bridge from R58 shared helper to R28 WriteFile root.

No new original download, executable execution, API simulation, savedata decode,
Windows ABI projection, persistence or ownership claims.
"""
import argparse
import hashlib
import json
from pathlib import Path

R28_SHA = '296e5754a3eebafc6360cc45000ba73b6bcf1cc0a5d0ee439aa291eb45e0d645'
R57_SHA = '3e562ab02a80e0f6516f8a91c93b897eef05f606be62f1df5cb48686d64114e6'
R58_SHA = '04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8'
SCHEMA = 'tw10-r59-prior-metadata-shared-writefile-root-bridge-preflight'
SITES = (0x4c68c, 0x4c6f1)

def read_exact(path, digest):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError('R59 original-derived immutable source digest changed')
    return json.loads(raw)

def derive(r28, r57, r58):
    if r28.get('schema') != 'tw10-r28-original-call-supported-native-api-input-candidates':
        raise ValueError('R59 invalid R28 schema')
    if r57.get('schema') != 'tw10-r57-original-complete-write-close-wrapper-return-syntax':
        raise ValueError('R59 invalid R57 schema')
    if r58.get('schema') != 'tw10-r58-original-rooted-shared-close-helper-static-inventory':
        raise ValueError('R59 invalid R58 schema')
    native = next(x for x in r28['contexts'] if x['api'] == 'WriteFile')
    wrapper = next(x for x in r57['contexts'] if x['root_candidate_rva'] == 0x48bbc)
    shared = next(x for x in r58['contexts'] if x['root_candidate_rva'] == 0x4a657)
    old = next(x for x in wrapper['call_contexts'] if x['site_rva'] == 0x48c5e)
    new = next(x for x in shared['call_contexts'] if x['site_rva'] == 0x4a683)
    if not (native['root_candidate_rva'] == 0x4c5b4
            and native['caller_rva'] == 0x48c5e
            and native['caller_identity']['direct_target_rva'] == 0x4c5b4
            and old['identity']['direct_target_rva'] == 0x4c5b4
            and new['identity']['direct_target_rva'] == 0x4c5b4):
        raise ValueError('R59 direct shared root identity mismatch')
    graph = native['graph']
    if not (graph['nodes'] == 139 and graph['edges'] == 156
            and graph['frontier'] == [] and graph['node_limit_hit'] is False
            and graph['call_fallthrough_structural_only'] is True):
        raise ValueError('R59 original R28 bounded root scope changed')
    sites = []
    for at in SITES:
        row = next(x for x in native['api_sites'] if x['site_rva'] == at)
        if not (row['site_in_candidate_graph'] is True and
                row['identity']['import_identity']['name'] == 'WriteFile' and
                row['actual_external_return_proven'] is False):
            raise ValueError('R59 WriteFile static import-site contract mismatch')
        sites.append({'api_site_rva':at, 'import_name':'WriteFile',
                      'site_in_bounded_root_graph':True,
                      'actual_writefile_executed_or_return_proven':False})
    shared_rows = {x['site_rva']:x for x in shared['instruction_shapes']}
    cmp_row = shared_rows[0x4a68b]
    if (cmp_row['mnemonic'] != 'cmp' or
        [(x.get('kind'),x.get('register')) for x in cmp_row['operands']]
            != [('register','eax'),('register','edi')]):
        raise ValueError('R59 missing post-helper compare')
    return {
        'schema':SCHEMA,
        'r28_original_derived_sha256':R28_SHA,
        'r57_original_derived_sha256':R57_SHA,
        'r58_original_derived_sha256':R58_SHA,
        'reused_function_root_candidate_rva':0x4c5b4,
        'shared_root_call_rva':0x4a683,
        'original_wrapper_call_rva':0x48c5e,
        'shared_root_post_call_eax_edi_comparison_rva':0x4a68b,
        'conditional_r28_bounded_root_nodes':139,
        'conditional_r28_bounded_root_edges':156,
        'writefile_import_syntax_sites':sites,
        'actual_shared_call_path_reaches_writefile_proven':False,
        'actual_call_preservation_argument_values_handle_or_buffer_link_proven':False,
        'actual_bytes_written_error_convention_flush_close_or_persistence_proven':False,
        'original_program_or_native_api_executed':False,
        'next':'Qualify scoped structural path to each API site and conditional arguments/returns across 0x4a683 and 0x48c5e; do not promote native success or storage.',
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--r28',type=Path,required=True)
    ap.add_argument('--r57',type=Path,required=True)
    ap.add_argument('--r58',type=Path,required=True)
    ap.add_argument('--verify',type=Path)
    a=ap.parse_args()
    d=derive(read_exact(a.r28,R28_SHA),read_exact(a.r57,R57_SHA),read_exact(a.r58,R58_SHA))
    if a.verify:
        old=json.loads(a.verify.read_text())
        if json.dumps(d,sort_keys=True,separators=(',',':')) != json.dumps(old,sort_keys=True,separators=(',',':')):
            raise ValueError('R59 preflight spec changed')
        print('TW10_R59_PRIOR_ROOT_BRIDGE=PASS; ACTUAL_NATIVE_PERSISTENCE=OPEN')
    else:
        print(json.dumps(d,sort_keys=True))

if __name__=='__main__':
    main()
