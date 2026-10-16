"""Independent fixed numeric/graph/retained-overlap guard for R73 metadata."""
import argparse
import hashlib
import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/'research/recovered'
PINS={
 'r71':('STONEAGE-TW10-SAVEDATA-NATIVE-ADJUSTMENT-R71-ORIGINAL.json','f2a946ffc93c6a32210f2ebaa9dc9191833aac37'),
 'r67':('STONEAGE-TW10-SAVEDATA-NATIVE-TAIL-R67-ORIGINAL.json','04162081d346b8c53424295de9fdc6b8f385b011'),
 'r69':('STONEAGE-TW10-SAVEDATA-NATIVE-EARLY-R69-ORIGINAL.json','d5d4924803dc28de8be00f712eecd11cf9003c66'),
 'r44':('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R44-ORIGINAL.json','39c1c0f673747fb560cc285d627490e5cd38047a'),
 'r45':('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R45-ORIGINAL.json','1e7fb71cec336c1b4fc531d4f4a6933c9f66d415'),
 'r63':('STONEAGE-TW10-SAVEDATA-POSTCALL-R63-DERIVED.json','3b7c9cea63ed4e2a360ddb6934e7dcd44b9833e7'),
 'preflight':('STONEAGE-TW10-SAVEDATA-R73-REFRESH-PREFLIGHT.json','2e93328203526d465cfa0af22a0defcc0f3b9b21')}
NEGATIVE=('original_program_executed','original_savedata_payload_read_or_published',
 'actual_native_return_count_or_success_proven','actual_path_predicates_or_values_proven',
 'actual_abi_frame_register_memory_preservation_proven','actual_flush_close_or_persistence_proven',
 'original_schema_or_server_authority_proven','stage_b_started')

def need(ok,why):
 if not ok:raise ValueError('R73 independent guard: '+why)

def validate(d):
 old={}
 for k,(name,pin) in PINS.items():
  raw=(BASE/name).read_bytes();need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin,'immutable prior '+k);old[k]=json.loads(raw)
 need(d.get('schema')=='tw10-r73-original-static-mode-direct-count-neighborhood','schema')
 need(d.get('source_git_blobs')=={k:v[1]for k,v in PINS.items()},'source pins')
 need(d.get('runtime_sha256')==old['r71']['runtime_sha256'] and d.get('image_base')==4194304 and d.get('root_rva')==312756,'runtime/base/root')
 need(d.get('r71_exact_original_rederived_sha256')=='746c7e64a973b52ca5cf3412342eb68725fcf15dcb5ad4a1e71a8e638ae90af5','exact inherited report')
 need(all(d.get(k)is False for k in NEGATIVE),'nonpromotion')
 nodes=d.get('bounded_graph_node_rvas');edges=d.get('bounded_graph_edges')
 need(nodes==old['r71']['bounded_graph_node_rvas'] and edges==old['r71']['bounded_graph_edges'],'fixed graph')
 need(d.get('bounded_graph_frontier')==[] and d.get('bounded_graph_node_cap_hit')is False,'graph bounds')
 focus=[312839, 312841, 312843, 312844, 312845, 312853, 312855, 312857, 313027, 313029, 313039];need(set(focus)<=set(nodes) and len(focus)==11 and d.get('focus_node_rvas')==focus,'fixed focus')
 selected=set(focus)
 for a,b in edges:
  if a in focus or b in focus:selected|={a,b}
 need(len(selected)==17 and d.get('selected_node_rvas')==sorted(selected),'exact one-hop incidence')
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
 for k in ('r44','r45','r63','r69','r71','r67'):compare(old[k])
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
