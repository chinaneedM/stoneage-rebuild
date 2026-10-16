"""R71: retained-first, authenticated original-static adjustment loop metadata."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile

BASE = Path(__file__).resolve().parents[1] / 'research/recovered'
ROOT = 0x4C5B4
RUNTIME_SHA = 'cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a'
R69_SHA = '26ff9f92d14a4ef385a279501e456b4bf58156209ad4471aef84109f6e16bfbe'
PINS = {
    'r69': ('STONEAGE-TW10-SAVEDATA-NATIVE-EARLY-R69-ORIGINAL.json', 'd5d4924803dc28de8be00f712eecd11cf9003c66'),
    'r44': ('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R44-ORIGINAL.json', '39c1c0f673747fb560cc285d627490e5cd38047a'),
    'r45': ('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R45-ORIGINAL.json', '1e7fb71cec336c1b4fc531d4f4a6933c9f66d415'),
    'r63': ('STONEAGE-TW10-SAVEDATA-POSTCALL-R63-DERIVED.json', '3b7c9cea63ed4e2a360ddb6934e7dcd44b9833e7'),
    'preflight': ('STONEAGE-TW10-SAVEDATA-R71-PREFLIGHT.json', 'd016b5e3356d3064b1b30a79a2899ec96352e097'),
}
FALSE = ('original_program_executed', 'original_savedata_payload_read_or_published',
         'actual_native_return_count_or_success_proven', 'actual_path_predicates_or_values_proven',
         'actual_abi_frame_register_memory_preservation_proven', 'actual_flush_close_or_persistence_proven',
         'original_schema_or_server_authority_proven', 'stage_b_started')
CORE = ('site_rva', 'mnemonic', 'operands', 'decoder_read_registers', 'decoder_written_registers')


def need(ok, why):
    if not ok:
        raise ValueError('R71 adjustment static: ' + why)


def priors():
    out = {}
    for k, (name, pin) in PINS.items():
        raw = (BASE / name).read_bytes()
        need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == pin, 'pinned source '+k)
        out[k] = json.loads(raw)
    p = out['preflight']
    need(p['report_count'] == 138 and len(p['selected_missing_decoded_sites']) == 11 and
         len(p['decoded_sites_in_full_graph']) == 117, 'bounded retained-first gap')
    return out


def retained_rows(reports):
    """Only same-dictionary, numeric site_rva and explicit decoded operand rows."""
    out = {}
    def visit(x):
        if isinstance(x, dict):
            if type(x.get('site_rva')) is int and x.get('mnemonic') and isinstance(x.get('operands'), list):
                at = x['site_rva']; core = {k: x[k] for k in CORE}
                need(at not in out or out[at] == core, 'retained overlapping operand identity')
                out[at] = core
            for v in x.values():
                if isinstance(v, (dict, list)): visit(v)
        elif isinstance(x, list):
            for v in x:
                if isinstance(v, (dict, list)): visit(v)
    for report in reports: visit(report)
    return out


def selection(nodes, edges, row):
    nodes, edges = set(nodes), set(edges)
    focus = {n for n in nodes if 0x4C623 <= n <= 0x4C66D}
    need(len(focus) == 25 and 0x4C653 in focus, 'fixed update/control focus')
    selected = set(focus)
    for a,b in edges:
        need(a in nodes and b in nodes, 'edge endpoints')
        if a in focus or b in focus: selected.update((a,b))
    need(len(selected) == 29, 'exact bounded one-hop size')
    rows = [row(n) for n in sorted(selected)]
    need([r.get('site_rva') for r in rows] == sorted(selected), 'exact rows')
    for r in rows:
        need(bool(r.get('mnemonic')) and isinstance(r.get('operands'),list) and
             r.get('actual_instruction_effect_or_value_known') is False, 'static row')
    return {'focus_node_rvas': sorted(focus), 'selected_node_rvas': sorted(selected),
            'decoded_instruction_rows': rows,
            'selected_internal_edges': [list(e) for e in sorted(edges) if e[0] in selected and e[1] in selected],
            'focus_predecessors': {str(n): sorted(a for a,b in edges if b==n) for n in sorted(focus)},
            'focus_successors': {str(n): sorted(b for a,b in edges if a==n) for n in sorted(focus)}}


def inspect_verified(runtime):
    need(hashlib.sha256(runtime).hexdigest() == RUNTIME_SHA, 'original runtime SHA256')
    old = priors()
    from tools.stoneage_tw10_savedata_r69_early_static import inspect_verified as original_r69
    from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph
    from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row
    from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
    from tools.stoneage_tw10_mapcache_binary_probe import image_layout
    r69 = original_r69(runtime)
    raw = (json.dumps(r69,sort_keys=True)+'\n').encode()
    need(hashlib.sha256(raw).hexdigest() == R69_SHA and r69 == old['r69'], 'exact inherited R69/R67/R63 reproduction')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime)
        data, pe, base, sections, _ = image_layout(p)
    for meta, sec in zip(sections,pe.sections): meta['characteristics']=int(sec.Characteristics)
    t=next(s for s in sections if s['name']=='.text')
    dec=Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base)
    nodes,edges,frontier,cap=candidate_graph(dec,ROOT)
    need(base==0x400000 and sorted(nodes)==r69['bounded_graph_node_rvas'] and
         [list(e) for e in sorted(edges)]==r69['bounded_graph_edges'] and not frontier and not cap, 'exact bounded original graph')
    result=selection(nodes,edges,lambda at: instruction_row(dec,sections,nodes,at))
    known=retained_rows([old[k] for k in ('r44','r45','r63','r69')])
    for r in result['decoded_instruction_rows']:
        if r['site_rva'] in known:
            need({k:r[k] for k in CORE} == known[r['site_rva']], 'requalified retained original operand row')
    return {'schema':'tw10-r71-original-static-adjustment-loop-neighborhood',
            'runtime_sha256':RUNTIME_SHA,'image_base':base,'root_rva':ROOT,
            'source_git_blobs':{k:v[1] for k,v in PINS.items()},
            'r69_exact_original_rederived_sha256':R69_SHA,
            'bounded_graph_node_rvas':sorted(nodes),'bounded_graph_edges':[list(e)for e in sorted(edges)],
            'bounded_graph_frontier':[],'bounded_graph_node_cap_hit':False,
            'selection_rule':'0x4c623..0x4c66d focus25 plus exact one-hop incidence29; no execution',
            'previously_missing_selected_sites':old['preflight']['selected_missing_decoded_sites'],
            **result,**{k:False for k in FALSE},
            'next':'Independently qualify adjustment predicate, byte-store and count-unit syntax; preserve all call/frame/alias/native-value barriers.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--bin',type=Path,required=True);a=p.parse_args()
    from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH
    from tools.stoneage_tw10_technical_probe import find_rows,extract_row
    image,rows,_,_=find_rows(a.bin)
    try:
        files={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe=Path(td)/'sa_3.exe';extract_row(image,files[RUNTIME_PATH],exe);d=inspect_verified(exe.read_bytes())
    finally:image.close()
    print(json.dumps(d,sort_keys=True))


if __name__=='__main__':main()
