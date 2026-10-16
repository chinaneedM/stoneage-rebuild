"""Independent exact inventory and retained-row guard for R75 derived metadata."""
import argparse
import hashlib
import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/'research/recovered'
PINS={
 'r73':('STONEAGE-TW10-SAVEDATA-NATIVE-MODES-R73-ORIGINAL.json','2a90bf654a723da53f7d6a26008ca660cb89b290'),
 'r46':('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R46-ORIGINAL.json','19d730daf617313508ccf81e940c0a51f3be8395'),
 'r37':('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R37-ORIGINAL.json','1ed7b1593286b401c866ccd31118bbd235f4269a'),
 'preflight':('STONEAGE-TW10-SAVEDATA-R75-REFRESH-PREFLIGHT.json','2ea2b2ecae600cdff94eaf414526f486f0fa6fa9')}
NEGATIVE=('original_program_executed','original_savedata_payload_read_or_published',
 'actual_native_seek_return_position_or_success_proven','actual_path_predicates_or_values_proven',
 'actual_abi_frame_register_memory_preservation_proven','actual_flush_close_or_persistence_proven',
 'original_schema_or_server_authority_proven','stage_b_started')

def need(ok,why):
 if not ok:raise ValueError('R75 independent guard: '+why)

def validate(d):
 old={}
 for k,(name,pin)in PINS.items():
  raw=(BASE/name).read_bytes();need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin,'prior identity '+k);old[k]=json.loads(raw)
 need(d.get('schema')=='tw10-r75-original-static-bounded-seek-helper-effects','schema')
 need(d.get('runtime_sha256')==old['r73']['runtime_sha256']and d.get('image_base')==4194304 and d.get('root_rva')==313185,'runtime/root')
 need(d.get('source_git_blobs')=={k:v[1]for k,v in PINS.items()},'custody')
 need(d.get('r73_exact_original_rederived_sha256')=='5cf096089f60f8a6afd80fe2923f214f609ac57a92ab3d9d02aeefb04248013d'and d.get('r46_r37_helper_surface_exactly_revalidated')is True,'exact original parent/context replay')
 need(all(d.get(k)is False for k in NEGATIVE),'nonpromotion')
 g=old['r46']['write_helper_context'];nodes=d.get('bounded_graph_node_rvas');edges=d.get('bounded_graph_edges')
 need(nodes==g['bounded_node_rvas']and edges==g['bounded_edges']and len(nodes)==51 and len(edges)==55,'exact fixed graph')
 need(d.get('bounded_graph_frontier')==[]and d.get('bounded_graph_node_cap_hit')is False,'bounds')
 need(d.get('selected_node_rvas')==nodes,'all local effects covered')
 rows=d.get('decoded_instruction_rows',[]);need([r.get('site_rva')for r in rows]==nodes,'complete inventory')
 by={r['site_rva']:r for r in rows}
 for r in rows:
  need(isinstance(r.get('mnemonic'),str)and bool(r['mnemonic'])and isinstance(r.get('operands'),list)and r.get('actual_instruction_effect_or_value_known')is False,'unexecuted row')
  need(all(isinstance(r.get(k),list)for k in ('decoder_read_registers','decoder_written_registers','input_query_registers')),'register inventories')
 need(d.get('previously_missing_selected_sites')==old['preflight']['missing_decoded_node_rvas']and len(d['previously_missing_selected_sites'])==48,'registered row gap')
 def visit(x):
  if isinstance(x,dict):
   at=x.get('site_rva')
   if type(at)is int and at in by and x.get('mnemonic')and isinstance(x.get('operands'),list):need(all(x.get(k)==by[at].get(k)for k in ('site_rva','mnemonic','operands','decoder_read_registers','decoder_written_registers')),'known operand overlap')
   for v in x.values():
    if isinstance(v,(dict,list)):visit(v)
  elif isinstance(x,list):
   for v in x:
    if isinstance(v,(dict,list)):visit(v)
 for k in ('r46','r37'):visit(old[k])
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
