"""R77: bounded original-static source of the seek helper's handle-shaped EAX.

No original executable/API or savedata payload is run or published.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]/'research/recovered'
ROOT=0x4E8FB
RUNTIME_SHA='cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a'
PINS={
 'r75':('STONEAGE-TW10-SAVEDATA-NATIVE-SEEK-HELPER-R75-ORIGINAL.json','757c22945d7e18263b154e88f52376d0ab58d42c'),
 'preflight':('STONEAGE-TW10-SAVEDATA-R77-REFRESH-PREFLIGHT.json','79d6afabc9477f945de449b2265a62a76ff1733b')}
NEGATIVE=('original_program_executed','original_savedata_payload_read_or_published',
 'actual_handle_value_or_validity_proven','actual_seek_position_or_success_proven',
 'actual_abi_frame_register_memory_preservation_proven','actual_flush_close_or_persistence_proven',
 'original_schema_or_server_authority_proven','stage_b_started')

def need(ok,why):
 if not ok:raise ValueError('R77 handle static: '+why)

def priors():
 out={}
 for k,(name,pin)in PINS.items():
  raw=(BASE/name).read_bytes();need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin,'prior '+k);out[k]=json.loads(raw)
 p=out['preflight'];need(p['report_count']==156 and p['targets'][0]['rva']==ROOT and p['targets'][0]['decoded_entry_hits']==[],'retained-first gap')
 return out

def inventory(nodes,edges,front,cap,row):
 nodes=set(nodes);edges=set(edges)
 need(ROOT in nodes and 0<len(nodes)<=256 and all(a in nodes and b in nodes for a,b in edges),'bounded graph')
 need(not front and not cap,'incomplete material handle-source graph')
 rows=[row(n)for n in sorted(nodes)]
 need([r.get('site_rva')for r in rows]==sorted(nodes),'exact inventory')
 need(all(r.get('mnemonic')and isinstance(r.get('operands'),list)and r.get('actual_instruction_effect_or_value_known')is False for r in rows),'static rows')
 return {'bounded_graph_node_rvas':sorted(nodes),'bounded_graph_edges':[list(e)for e in sorted(edges)],'bounded_graph_frontier':[], 'bounded_graph_node_cap_hit':False,'decoded_instruction_rows':rows}

def inspect_verified(runtime):
 need(hashlib.sha256(runtime).hexdigest()==RUNTIME_SHA,'original runtime SHA256');old=priors()
 from tools.stoneage_tw10_savedata_r75_seek_helper_static import inspect_verified as inspect_r75
 from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph
 from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row
 from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
 from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
 from tools.stoneage_tw10_mapcache_binary_probe import image_layout
 parent=inspect_r75(runtime);raw=(json.dumps(parent,sort_keys=True)+'\n').encode()
 need(parent==old['r75']and hashlib.sha256(raw).hexdigest()=='bcec13f8eb8d0b6182a38aa8b0ba67a7f20ca1d9b33ca1c9a76a1448f62b7d85','exact R75 and inherited source replay')
 with tempfile.TemporaryDirectory()as td:
  p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
 for meta,s in zip(sections,pe.sections):meta['characteristics']=int(s.Characteristics)
 t=next(s for s in sections if s['name']=='.text');dec=Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base)
 caller=call_identity(dec,0x4c78e,imports,sections);need(caller['kind']=='direct'and caller['direct_target_rva']==ROOT,'retained direct caller')
 nodes,edges,front,cap=candidate_graph(dec,ROOT)
 result=inventory(nodes,edges,front,cap,lambda n:instruction_row(dec,sections,nodes,n))
 calls=[call_identity(dec,n,imports,sections)for n in sorted(nodes)if nodes[n].mnemonic=='call']
 return {'schema':'tw10-r77-original-static-bounded-handle-source','runtime_sha256':RUNTIME_SHA,'image_base':base,'root_rva':ROOT,
  'source_git_blobs':{k:v[1]for k,v in PINS.items()},'r75_exact_original_rederived_sha256':hashlib.sha256(raw).hexdigest(),
  'caller_identity':caller,'call_candidates':calls,
  'selection_reason':'Only the direct0x4e8fb callee of retained0x4c78e is decoded to qualify the handle-shaped return and caller-visible local effects. Descendant callees and0x4c953 remain unexpanded.',
  **result,**{k:False for k in NEGATIVE},'next':'Independently qualify local return sources, table geometry, guard/control effects and stack/register syntax under explicit memory/ABI premises; actual handle/IO remains OPEN.'}

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
