"""Independent nonpromotion and graph integrity guard for R77 metadata."""
import argparse
import hashlib
import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/'research/recovered'
NEGATIVE=('original_program_executed','original_savedata_payload_read_or_published',
 'actual_handle_value_or_validity_proven','actual_seek_position_or_success_proven',
 'actual_abi_frame_register_memory_preservation_proven','actual_flush_close_or_persistence_proven',
 'original_schema_or_server_authority_proven','stage_b_started')

def need(ok,why):
 if not ok:raise ValueError('R77 independent guard: '+why)

def validate(d):
 pins={'r75':('STONEAGE-TW10-SAVEDATA-NATIVE-SEEK-HELPER-R75-ORIGINAL.json','757c22945d7e18263b154e88f52376d0ab58d42c'),'preflight':('STONEAGE-TW10-SAVEDATA-R77-REFRESH-PREFLIGHT.json','79d6afabc9477f945de449b2265a62a76ff1733b')}
 for name,pin in pins.values():
  raw=(BASE/name).read_bytes();need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin,'prior identity')
 need(d.get('schema')=='tw10-r77-original-static-bounded-handle-source','schema')
 need(d.get('runtime_sha256')=='cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a'and d.get('image_base')==4194304 and d.get('root_rva')==321787,'runtime/root')
 need(d.get('source_git_blobs')=={k:v[1]for k,v in pins.items()},'custody')
 need(d.get('r75_exact_original_rederived_sha256')=='bcec13f8eb8d0b6182a38aa8b0ba67a7f20ca1d9b33ca1c9a76a1448f62b7d85','source replay')
 need(all(d.get(k)is False for k in NEGATIVE),'nonpromotion')
 nodes=d.get('bounded_graph_node_rvas',[]);edges=d.get('bounded_graph_edges',[]);rows=d.get('decoded_instruction_rows',[])
 need(nodes==sorted(set(nodes))and 321787 in nodes and 0<len(nodes)<=256,'nodes')
 need(d.get('bounded_graph_frontier')==[]and d.get('bounded_graph_node_cap_hit')is False,'complete bounded graph')
 need(edges==[list(e)for e in sorted(set(map(tuple,edges)))]and all(a in nodes and b in nodes for a,b in edges),'edges')
 need([r.get('site_rva')for r in rows]==nodes,'complete rows')
 reachable={321787}
 while True:
  nxt=reachable|{b for a,b in edges if a in reachable}
  if nxt==reachable:break
  reachable=nxt
 need(reachable==set(nodes),'root reachability')
 for r in rows:
  need(bool(r.get('mnemonic'))and isinstance(r.get('operands'),list)and r.get('actual_instruction_effect_or_value_known')is False,'unexecuted decoded row')
  need(all(isinstance(r.get(k),list)for k in ('decoder_read_registers','decoder_written_registers','input_query_registers')),'register lists')
  succ={b for a,b in edges if a==r['site_rva']}
  need(bool(succ)or r['mnemonic']=='ret','no unexplained terminal')
 caller=d.get('caller_identity',{});need(caller.get('call_rva')==313230 and caller.get('kind')=='direct'and caller.get('direct_target_rva')==321787 and caller.get('runtime_target_or_effects_proven')is False,'caller')
 calls=d.get('call_candidates',[]);need([c.get('call_rva')for c in calls]==[r['site_rva']for r in rows if r['mnemonic']=='call'],'call census')
 need(all(c.get('runtime_target_or_effects_proven')is False for c in calls),'opaque calls')
 def no_raw(x):
  if isinstance(x,dict):
   need(not set(x)&{'bytes','raw_binary','source_code','original_payload','original_savedata_bytes'},'raw disclosure')
   for v in x.values():no_raw(v)
  elif isinstance(x,list):
   for v in x:no_raw(v)
 no_raw(d)
 return {'status':'STRUCTURAL_DERIVED_METADATA_ONLY','decoded_rows':len(rows),'native_persistence':'OPEN'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(json.loads(a.report.read_bytes())),sort_keys=True))
if __name__=='__main__':main()
