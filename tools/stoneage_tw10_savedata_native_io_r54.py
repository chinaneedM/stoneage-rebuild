"""Authenticated nonexecuting original writer prefix and direct callees, bounded metadata only."""
import argparse,hashlib,json,tempfile
from pathlib import Path
from capstone import CS_GRP_CALL
from tools.stoneage_tw10_savedata_native_io_r51 import inspect_verified as inspect_r51
from tools.stoneage_tw10_savedata_native_io_r51_guard import validate as validate_r51
from tools.stoneage_tw10_savedata_native_io_r50 import (RUNTIME_SHA256,SAVEDATA_SHA256,graph_record,call_surface)
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph
from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row
from tools.stoneage_tw10_savedata_native_io_r42 import branch_context
from tools.stoneage_tw10_savedata_entrygraph_r4 import explore
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row
from tools.stoneage_tw10_savedata_writer_r54 import analyze
ROOT=0x40020
PRIOR_SHA='15f54e5de8d1d20128fb7d948b54f13a0e3f6cf372eca203cbc7bb8adc473052'
SCHEMA='tw10-r54-original-writer-prefix-complete-bounded-callees'
FLAGS=('actual_argument_values_or_abi_proven','actual_writer_inverse_proven','actual_schema_migration_or_persistence_proven','native_io_executed','original_bytes_published')

def inventory(dec,sections,imports,entry,root):
    ns,es,fr,cap=candidate_graph(dec,root)
    rows=[instruction_row(dec,sections,ns,a) for a in sorted(ns)]
    sites=[a for a,i in sorted(ns.items()) if i.group(CS_GRP_CALL)]
    if len(sites)>16:raise ValueError('R54 call bound')
    return {'root_candidate_rva':root,**graph_record(ns,es,fr,cap),'instruction_shapes':rows,
      'instruction_shapes_truncated':False,'entrygraph_boundary_seen':root in entry['visited'],
      'call_contexts':[call_surface(dec,sections,imports,ns,es,root,a) for a in sites]}

def inspect_verified(runtime,savedata):
    prior=inspect_r51(runtime,savedata);validate_r51(prior)
    if hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()!=PRIOR_SHA:raise ValueError('R54 exact R51 requalification')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for s,p in zip(sections,pe.sections):s['characteristics']=int(p.Characteristics)
    t=next(s for s in sections if s['name']=='.text');raw=data[t['raw']:t['raw']+t['raw_size']]
    dec=Decoder(raw,t['rva'],base);entry=explore(raw,t['rva'],base,int(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
    caller=inventory(dec,sections,imports,entry,ROOT)
    prefix=[c for c in caller['call_contexts'] if c['site_rva']<0x40064]
    if not prefix or len(prefix)>8:raise ValueError('R54 prefix callee bound')
    processors=[]
    for c in prefix:
        target=c['identity']['direct_target_rva']
        if target is not None:
            processors.append({'caller_site_rva':c['site_rva'],**inventory(dec,sections,imports,entry,target),
              'entrygraph_call_edge_seen':(c['site_rva'],target) in entry['edges']})
    # Exact accepted read caller normalization chain remains separate from writer interpretation.
    old=prior['r50_snapshot']['caller_context'];normal=[r for r in old['literal_effect_input_shapes'] if 0x40195<=r['site_rva']<=0x401b6]
    ns,es,fr,cap=candidate_graph(dec,0x40115)
    if [instruction_row(dec,sections,ns,r['site_rva']) for r in normal]!=normal:raise ValueError('R54 exact normalization syntax')
    return {'schema':SCHEMA,'static_only':True,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
      'r51_exact_original_report_sha256':PRIOR_SHA,'normalization_shapes':normal,
      'normalization_call_edge_seen':(0x401b6,ROOT) in entry['edges'],'entrygraph_node_limit_hit':entry['limit_hit'],
      'writer_context':caller,'prefix_direct_callee_contexts':processors,
      'conditional_writer_analysis':analyze(caller,processors),**{k:False for k in FLAGS}}

def main():
    p=argparse.ArgumentParser();p.add_argument('--bin',type=Path,required=True);image,rows,_,_=find_rows(p.parse_args().bin)
    try:
        files={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe,save=Path(td)/'sa_3.exe',Path(td)/'savedata.dat'
            extract_row(image,files[RUNTIME_PATH],exe);extract_row(image,files[SAVEDATA_PATH],save)
            report=inspect_verified(exe.read_bytes(),save.read_bytes())
    finally:image.close()
    print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
