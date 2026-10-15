"""R51 authenticated original complete processor inventory and caller predicates."""
import argparse,hashlib,json,tempfile
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r50 import inspect_verified as inspect_r50,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_native_io_r50_guard import validate as validate_r50
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph
from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row
from tools.stoneage_tw10_savedata_native_io_r49 import sources
from tools.stoneage_tw10_savedata_native_io_r41 import queries_for
from tools.stoneage_tw10_savedata_application_r51 import analyze,ROOT
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row
SCHEMA='tw10-r51-original-complete-processor-caller-conditional-stack-consumers'
STATUS='PINNED_ORIGINAL_CONDITIONAL_PROCESSOR_INVENTORY_SCHEMA_OPEN'
PRIOR_SHA256='0badd1423f403a9e8a246a40518a68ee5a1bd67d380ea7ab3460fc3c607c3e94'
FLAGS=('actual_processor_algorithm_or_decoded_bytes_proven','actual_caller_output_length_buffer_alias_or_abi_proven','actual_savedata_schema_tag_migration_or_persistence_proven','native_io_executed','original_bytes_published')

def derive(dec,sections,prior):
    nodes,edges,front,cap=candidate_graph(dec,ROOT);old=prior['processing_entry_context']
    es=[list(e) for e in sorted(edges)]
    if sorted(nodes)!=old['bounded_node_rvas'] or es!=old['bounded_edges']:raise ValueError('R51 exact processor graph')
    rows=[instruction_row(dec,sections,nodes,a) for a in sorted(nodes)]
    selected=[r for r in rows if r['mnemonic'] in ('cmp','test') or any(o['kind']=='memory' for o in r['operands'])]
    if selected[:32]!=old['memory_control_shapes']:raise ValueError('R51 exact processor prior sample')
    divisions=[r for r in rows if r['mnemonic'] in ('div','idiv')]
    if len(divisions)>8:raise ValueError('R51 division bound')
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,'static_only':True,
            'r50_exact_original_revalidated':True,'r50_exact_report_sha256':PRIOR_SHA256,'r50_snapshot':prior,
            'processor_instruction_shapes':rows,'processor_instruction_count':len(rows),'processor_instruction_shapes_truncated':False,
            'processor_division_source_surface':sources(dec,sections,nodes,edges,ROOT,divisions),
            'conditional_consumer_analysis':analyze(prior,rows,es),**{k:False for k in FLAGS}}

def inspect_verified(runtime,savedata):
    prior=inspect_r50(runtime,savedata);validate_r50(prior)
    if hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()!=PRIOR_SHA256:raise ValueError('R51 exact R50 derivative')
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/'sa_3.exe';path.write_bytes(runtime);data,pe,base,sections,imports=image_layout(path)
    for s,p in zip(sections,pe.sections):s['characteristics']=int(p.Characteristics)
    t=next(s for s in sections if s['name']=='.text');dec=Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base)
    return derive(dec,sections,prior)

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
