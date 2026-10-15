"""R58 bounded, authenticated, nonexecuting TW1.0 shared/close helper root inventory.

Original media are transient inputs only; output is static syntax and numeric provenance.
No original game code, APIs, savedata contents or original program are executed.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from tools.stoneage_tw10_savedata_native_io_r57 import inspect_verified as inspect_r57
from tools.stoneage_tw10_savedata_native_io_r57_guard import validate as validate_r57
from tools.stoneage_tw10_savedata_native_io_r54 import inventory, RUNTIME_SHA256, SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_return_r57 import analyze
from tools.stoneage_tw10_savedata_entrygraph_r4 import explore
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = 'tw10-r58-original-rooted-shared-close-helper-static-inventory'
R57_SHA256 = '3e562ab02a80e0f6516f8a91c93b897eef05f606be62f1df5cb48686d64114e6'
# (label, root RVA, (wrapper root RVA, verified CALL RVA) pairs)
TARGETS = (
    ('shared_write_close', 0x4a657, ((0x48bbc, 0x48c38), (0x4856c, 0x48586))),
    ('close_path', 0x4a53e, ((0x4856c, 0x48596),)),
)
FLAGS = (
    'actual_native_flush_close_or_persistence_proven',
    'actual_helper_result_or_error_convention_proven',
    'actual_frame_register_memory_alias_or_abi_proven',
    'original_payload_schema_or_cross_version_proven',
    'native_code_executed', 'original_bytes_published',
)

def canonical_sha(report):
    return hashlib.sha256((json.dumps(report, sort_keys=True) + '\n').encode()).hexdigest()

def find_bridges(r57):
    contexts = {c['root_candidate_rva']: c for c in r57['contexts']}
    found = []
    for label, target, parents in TARGETS:
        edges = []
        for wrapper, call in parents:
            cs = contexts[wrapper]['call_contexts']
            matches = [c for c in cs if c['site_rva'] == call]
            if len(matches) != 1 or matches[0]['identity']['direct_target_rva'] != target:
                raise ValueError('R58 wrapper CALL root bridge mismatch')
            edges.append({'wrapper_root_rva': wrapper, 'call_site_rva': call,
                          'target_rva': target, 'r57_direct_identity': matches[0]['identity']})
        found.append({'label': label, 'root_candidate_rva': target, 'r57_caller_bridges': edges})
    return found

def inspect_verified(runtime, savedata):
    r57 = inspect_r57(runtime, savedata)
    validate_r57(r57)
    if canonical_sha(r57) != R57_SHA256:
        raise ValueError('R58 exact accepted R57 original syntax requalification')
    bridges = find_bridges(r57)
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / 'sa_3.exe'
        path.write_bytes(runtime)
        data, pe, base, sections, imports = image_layout(path)
    for section, pe_section in zip(sections, pe.sections):
        section['characteristics'] = int(pe_section.Characteristics)
    code = next(s for s in sections if s['name'] == '.text')
    raw = data[code['raw']:code['raw'] + code['raw_size']]
    decoder = Decoder(raw, code['rva'], base)
    entry = explore(raw, code['rva'], base, int(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
    results = []
    for bridge in bridges:
        root = bridge['root_candidate_rva']
        inv = inventory(decoder, sections, imports, entry, root)
        result = {**bridge, **inv}
        result['r57_wrapper_edges_seen_in_entrygraph'] = [
            (x['call_site_rva'], root) in entry['edges']
            for x in bridge['r57_caller_bridges']
        ]
        result['return_analysis'] = analyze(inv)
        result['bounded_graph_complete'] = (
            not inv['graph']['node_limit_hit']
            and not inv['graph']['frontier']
            and bool(result['return_analysis']['return_contexts'])
        )
        result['actual_path_or_callee_effects_proven'] = False
        results.append(result)
    return {
        'schema': SCHEMA, 'static_only': True, 'runtime_sha256': RUNTIME_SHA256,
        'savedata_sha256': SAVEDATA_SHA256, 'exact_r57_report_sha256': R57_SHA256,
        'exact_r57_requalified': True, 'entrygraph_node_limit_hit': entry['limit_hit'],
        'contexts': results, **{key: False for key in FLAGS},
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bin', type=Path, required=True)
    args = parser.parse_args()
    image, rows, _, _ = find_rows(args.bin)
    try:
        files = {r['path']: r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            runtime_path = Path(td) / 'sa_3.exe'
            savedata_path = Path(td) / 'savedata.dat'
            extract_row(image, files[RUNTIME_PATH], runtime_path)
            extract_row(image, files[SAVEDATA_PATH], savedata_path)
            result = inspect_verified(runtime_path.read_bytes(), savedata_path.read_bytes())
    finally:
        image.close()
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
