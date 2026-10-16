"""Independent fixed numeric/graph/retained-overlap guard for R71 metadata."""
import argparse
import hashlib
import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/'research/recovered'
PINS={
 'r69':('STONEAGE-TW10-SAVEDATA-NATIVE-EARLY-R69-ORIGINAL.json','d5d4924803dc28de8be00f712eecd11cf9003c66'),
 'r44':('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R44-ORIGINAL.json','39c1c0f673747fb560cc285d627490e5cd38047a'),
 'r45':('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R45-ORIGINAL.json','1e7fb71cec336c1b4fc531d4f4a6933c9f66d415'),
 'r63':('STONEAGE-TW10-SAVEDATA-POSTCALL-R63-DERIVED.json','3b7c9cea63ed4e2a360ddb6934e7dcd44b9833e7'),
 'preflight':('STONEAGE-TW10-SAVEDATA-R71-PREFLIGHT.json','d016b5e3356d3064b1b30a79a2899ec96352e097')}
NEGATIVE=('original_program_executed','original_savedata_payload_read_or_published',
 'actual_native_return_count_or_success_proven','actual_path_predicates_or_values_proven',
 'actual_abi_frame_register_memory_preservation_proven','actual_flush_close_or_persistence_proven',
 'original_schema_or_server_authority_proven','stage_b_started')

def need(ok,why):
 if not ok:raise ValueError('R71 independent guard: '+why)

def validate(d):
 old={}
 for k,(name,pin) in PINS.items():
  raw=(BASE/name).read_bytes();need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin,'immutable prior '+k);old[k]=json.loads(raw)
 need(d.get('schema')=='tw10-r71-original-static-adjustment-loop-neighborhood','schema')
 need(d.get('source_git_blobs')=={k:v[1]for k,v in PINS.items()},'source pins')
 need(d.get('runtime_sha256')==old['r69']['runtime_sha256'] and d.get('image_base')==4194304 and d.get('root_rva')==312756,'runtime/base/root')
 need(d.get('r69_exact_original_rederived_sha256')=='26ff9f92d14a4ef385a279501e456b4bf58156209ad4471aef84109f6e16bfbe','exact inherited report')
 need(all(d.get(k)is False for k in NEGATIVE),'nonpromotion')
 nodes=d.get('bounded_graph_node_rvas');edges=d.get('bounded_graph_edges')
 need(nodes==old['r69']['bounded_graph_node_rvas'] and edges==old['r69']['bounded_graph_edges'],'fixed graph')
 need(d.get('bounded_graph_frontier')==[] and d.get('bounded_graph_node_cap_hit')is False,'graph bounds')
 focus=[n for n in nodes if 312867<=n<=312941];need(len(focus)==25 and d.get('focus_node_rvas')==focus,'fixed focus')
 selected=set(focus)
 for a,b in edges:
  if a in focus or b in focus:selected|={a,b}
 need(len(selected)==29 and d.get('selected_node_rvas')==sorted(selected),'exact one-hop incidence')
 rows=d.get('decoded_instruction_rows',[]);need([r.get('site_rva')for r in rows]==sorted(selected),'exact decoded inventory')
 by={r['site_rva']:r for r in rows}
 for r in rows:
  need(isinstance(r.get('mnemonic'),str) and bool(r['mnemonic']) and isinstance(r.get('operands'),list),'decoded row shape')
  need(r.get('actual_instruction_effect_or_value_known')is False and all(isinstance(r.get(k),list)for k in ('decoder_read_registers','decoder_written_registers','input_query_registers')),'static register inventories')
 need(d.get('selected_internal_edges')==[e for e in edges if e[0]in selected and e[1]in selected],'internal incidence')
 for n in focus:
  need(d.get('focus_predecessors',{}).get(str(n))==sorted(a for a,b in edges if b==n),'predecessors')
  need(d.get('focus_successors',{}).get(str(n))==sorted(b for a,b in edges if a==n),'successors')
 need(d.get('previously_missing_selected_sites')==old['preflight']['selected_missing_decoded_sites'] and len(d['previously_missing_selected_sites'])==11,'precise prior gap')
 core=('site_rva','mnemonic','operands','decoder_read_registers','decoder_written_registers')
 def compare(x):
  if isinstance(x,dict):
   n=x.get('site_rva')
   if type(n)is int and n in by and x.get('mnemonic') and isinstance(x.get('operands'),list):
    need(all(x.get(k)==by[n].get(k)for k in core),'retained overlap')
   for v in x.values():
    if isinstance(v,(dict,list)):compare(v)
  elif isinstance(x,list):
   for v in x:
    if isinstance(v,(dict,list)):compare(v)
 for k in ('r44','r45','r63','r69'):compare(old[k])
 def no_raw(x):
  if isinstance(x,dict):
   need(not set(x)&{'bytes','raw_binary','source_code','original_payload','original_savedata_bytes'},'no raw disclosure')
   for v in x.values():no_raw(v)
  elif isinstance(x,list):
   for v in x:no_raw(v)
 no_raw(d)
 return {'status':'STRUCTURAL_DERIVED_METADATA_ONLY','decoded_rows':len(rows),'native_persistence':'OPEN'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(json.loads(a.report.read_bytes())),sort_keys=True))
if __name__=='__main__':main()
