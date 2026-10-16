"""R75: complete local effect inventory on the already bounded seek helper.

This source acquisition covers every local return/control/write possibility
inside51 fixed nodes; no descendant calls or original save payload are opened.
"""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile

BASE=Path(__file__).resolve().parents[1]/'research/recovered'
ROOT=0x4C761
RUNTIME_SHA='cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a'
R73_SHA='5cf096089f60f8a6afd80fe2923f214f609ac57a92ab3d9d02aeefb04248013d'
PINS={
 'r73':('STONEAGE-TW10-SAVEDATA-NATIVE-MODES-R73-ORIGINAL.json','2a90bf654a723da53f7d6a26008ca660cb89b290'),
 'r46':('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R46-ORIGINAL.json','19d730daf617313508ccf81e940c0a51f3be8395'),
 'r37':('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R37-ORIGINAL.json','1ed7b1593286b401c866ccd31118bbd235f4269a'),
 'preflight':('STONEAGE-TW10-SAVEDATA-R75-REFRESH-PREFLIGHT.json','2ea2b2ecae600cdff94eaf414526f486f0fa6fa9')}
FALSE=('original_program_executed','original_savedata_payload_read_or_published',
 'actual_native_seek_return_position_or_success_proven','actual_path_predicates_or_values_proven',
 'actual_abi_frame_register_memory_preservation_proven','actual_flush_close_or_persistence_proven',
 'original_schema_or_server_authority_proven','stage_b_started')
CORE=('site_rva','mnemonic','operands','decoder_read_registers','decoder_written_registers')

def need(ok,why):
 if not ok:raise ValueError('R75 seek helper static: '+why)

def priors():
 out={}
 for k,(name,pin)in PINS.items():
  raw=(BASE/name).read_bytes();need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin,'immutable prior '+k);out[k]=json.loads(raw)
 p=out['preflight'];need(p['report_count']==150 and len(p['decoded_node_rvas'])==3 and len(p['missing_decoded_node_rvas'])==48,'retained-first exact gap')
 return out

def selection(nodes,edges,row):
 nodes=set(nodes);edges=set(edges)
 need(ROOT in nodes and len(nodes)==51 and len(edges)==55 and all(a in nodes and b in nodes for a,b in edges),'fixed local effect graph')
 rows=[row(n)for n in sorted(nodes)]
 need([r.get('site_rva')for r in rows]==sorted(nodes),'complete local row inventory')
 for r in rows:need(bool(r.get('mnemonic'))and isinstance(r.get('operands'),list)and r.get('actual_instruction_effect_or_value_known')is False,'decoded unexecuted row')
 return {'selected_node_rvas':sorted(nodes),'decoded_instruction_rows':rows}

def inspect_verified(runtime):
 need(hashlib.sha256(runtime).hexdigest()==RUNTIME_SHA,'original runtime SHA256');old=priors()
 from tools.stoneage_tw10_savedata_r73_modes_static import inspect_verified as original_r73,retained_rows
 from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph
 from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row,memory_surface
 from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
 from tools.stoneage_tw10_mapcache_binary_probe import image_layout
 parent=original_r73(runtime);raw=(json.dumps(parent,sort_keys=True)+'\n').encode()
 need(hashlib.sha256(raw).hexdigest()==R73_SHA and parent==old['r73'],'exact R73 and inherited R71/R69/R67/R63')
 with tempfile.TemporaryDirectory()as td:
  p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
 for meta,s in zip(sections,pe.sections):meta['characteristics']=int(s.Characteristics)
 t=next(s for s in sections if s['name']=='.text');dec=Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base)
 nodes,edges,front,cap=candidate_graph(dec,ROOT);prior=old['r46']['write_helper_context']
 need(base==4194304 and sorted(nodes)==prior['bounded_node_rvas']and [list(e)for e in sorted(edges)]==prior['bounded_edges']and not front and not cap,'exact original R46 helper graph')
 surface=memory_surface(dec,sections,imports,ROOT)
 need(surface==prior['r37_helper_surface_rederived'],'exact original R46/R37 helper call/memory surface')
 known37=next(c['callee_context']for c in old['r37']['helper_candidates']if c['callee_context']['root_candidate_rva']==ROOT)
 need(surface==known37,'immutable R37 helper surface equality')
 result=selection(nodes,edges,lambda n:instruction_row(dec,sections,nodes,n));known=retained_rows([old['r46'],old['r37']])
 for r in result['decoded_instruction_rows']:
  if r['site_rva']in known:need({k:r[k]for k in CORE}==known[r['site_rva']],'retained entry/ESP operand equality')
 return {'schema':'tw10-r75-original-static-bounded-seek-helper-effects','runtime_sha256':RUNTIME_SHA,'image_base':base,'root_rva':ROOT,
  'source_git_blobs':{k:v[1]for k,v in PINS.items()},'r73_exact_original_rederived_sha256':R73_SHA,
  'r46_r37_helper_surface_exactly_revalidated':True,'bounded_graph_node_rvas':sorted(nodes),'bounded_graph_edges':[list(e)for e in sorted(edges)],
  'bounded_graph_frontier':[],'bounded_graph_node_cap_hit':False,
  'selection_reason':'All51 already bounded helper nodes are required to inventory every local register/stack restore, memory store, RET and controlling branch. No descendant-callee graph expansion.',
  'previously_missing_selected_sites':old['preflight']['missing_decoded_node_rvas'],**result,**{k:False for k in FALSE},
  'next':'Independently qualify explicit local save/restore paths, stack argument geometry, SetFilePointer/error continuations and table-byte writes under opaque-call/alias/ABI premises.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--bin',type=Path,required=True);a=p.parse_args()
 from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH
 from tools.stoneage_tw10_technical_probe import find_rows,extract_row
 image,rows,_,_=find_rows(a.bin)
 try:
  files={r['path']:r for r in rows if not r['is_dir']}
  with tempfile.TemporaryDirectory()as td:
   exe=Path(td)/'sa_3.exe';extract_row(image,files[RUNTIME_PATH],exe);result=inspect_verified(exe.read_bytes())
 finally:image.close()
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
