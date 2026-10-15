"""Authenticated nonexecuting write/close wrapper complete bounded inventories."""
import argparse,hashlib,json,tempfile
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r54 import (inspect_verified as inspect_r54,inventory,RUNTIME_SHA256,SAVEDATA_SHA256)
from tools.stoneage_tw10_savedata_native_io_r54_guard import validate as validate_r54
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph
from tools.stoneage_tw10_savedata_native_io_r38 import stack_effect
from tools.stoneage_tw10_savedata_entrygraph_r4 import explore
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row
from tools.stoneage_tw10_savedata_return_r57 import analyze
SCHEMA='tw10-r57-original-complete-write-close-wrapper-return-syntax'
PRIOR_SHA='635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387'
FLAGS=('actual_wrapper_return_values_or_error_convention_proven','actual_native_write_count_close_flush_or_persistence_proven','actual_frame_alias_abi_or_file_owner_proven','actual_payload_schema_checksum_migration_or_cross_version_proven','native_io_executed','original_bytes_published')
SPECS=((0x40090,0x48bbc),(0x400ac,0x4856c))

def inspect_verified(runtime,savedata):
    prior=inspect_r54(runtime,savedata);validate_r54(prior)
    if hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()!=PRIOR_SHA:raise ValueError('R57 exact R54 requalification')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for s,p in zip(sections,pe.sections):s['characteristics']=int(p.Characteristics)
    t=next(s for s in sections if s['name']=='.text');raw=data[t['raw']:t['raw']+t['raw_size']];dec=Decoder(raw,t['rva'],base);entry=explore(raw,t['rva'],base,int(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
    old42=json.loads((Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R42-ORIGINAL.json').read_text());oldwrite=next(c for c in old42['wrappers'] if c['root_candidate_rva']==0x48bbc)
    contexts=[]
    for call,root in SPECS:
        caller=next(c for c in prior['writer_context']['call_contexts'] if c['site_rva']==call)
        if caller['identity']['direct_target_rva']!=root:raise ValueError('R57 prior target')
        c={'caller_site_rva':call,'savedata_caller_identity':caller['identity'],'entrygraph_caller_edge_seen':(call,root) in entry['edges'],**inventory(dec,sections,imports,entry,root)}
        if root==0x48bbc:
            ns,es,fr,cap=candidate_graph(dec,root)
            if c['bounded_edges']!=oldwrite['bounded_edges'] or c['bounded_node_rvas']!=[e['site_rva'] for e in oldwrite['stack_effect_candidates']] or [stack_effect(ns[a],base) for a in sorted(ns)]!=oldwrite['stack_effect_candidates']:raise ValueError('R57 exact R42 write graph/effects')
            by={r['site_rva']:r for r in c['instruction_shapes']}
            if any(by[r['site_rva']]!=r for r in oldwrite['early_stack_read_or_multiply_shapes']+oldwrite['entry_prolog_shapes']+oldwrite['frame_definition_shapes']):raise ValueError('R57 exact R42 write shapes')
        c['return_analysis']=analyze(c);contexts.append(c)
    return {'schema':SCHEMA,'static_only':True,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
      'r54_exact_original_report_sha256':PRIOR_SHA,'r42_write_graph_effects_and_retained_shapes_exact_requalified':True,
      'entrygraph_node_limit_hit':entry['limit_hit'],'contexts':contexts,**{k:False for k in FLAGS}}

def main():
    p=argparse.ArgumentParser();p.add_argument('--bin',type=Path,required=True);image,rows,_,_=find_rows(p.parse_args().bin)
    try:
        files={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe,save=Path(td)/'sa_3.exe',Path(td)/'savedata.dat';extract_row(image,files[RUNTIME_PATH],exe);extract_row(image,files[SAVEDATA_PATH],save);d=inspect_verified(exe.read_bytes(),save.read_bytes())
    finally:image.close()
    print(json.dumps(d,sort_keys=True))
if __name__=='__main__':main()
