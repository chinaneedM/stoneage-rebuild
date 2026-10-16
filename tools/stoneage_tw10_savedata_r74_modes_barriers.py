"""R74: bounded full instruction census, mode predicates and opaque-call barriers.

No original code/API/save data executes. Definitions below are syntax sources,
not values. All calls kill register knowledge regardless of decoder write lists.
"""
import argparse
import hashlib
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_r73_guard import validate as validate_r73
from tools.stoneage_tw10_savedata_r73_modes_static import retained_rows
from tools.stoneage_tw10_savedata_r70_conditional_returns import reg,frame

BASE=Path(__file__).resolve().parents[1]/'research/recovered'
PINS={
 'r73':('STONEAGE-TW10-SAVEDATA-NATIVE-MODES-R73-ORIGINAL.json','2a90bf654a723da53f7d6a26008ca660cb89b290'),
 'r71':('STONEAGE-TW10-SAVEDATA-NATIVE-ADJUSTMENT-R71-ORIGINAL.json','f2a946ffc93c6a32210f2ebaa9dc9191833aac37'),
 'r69':('STONEAGE-TW10-SAVEDATA-NATIVE-EARLY-R69-ORIGINAL.json','d5d4924803dc28de8be00f712eecd11cf9003c66'),
 'r67':('STONEAGE-TW10-SAVEDATA-NATIVE-TAIL-R67-ORIGINAL.json','04162081d346b8c53424295de9fdc6b8f385b011'),
 'r63':('STONEAGE-TW10-SAVEDATA-POSTCALL-R63-DERIVED.json','3b7c9cea63ed4e2a360ddb6934e7dcd44b9833e7'),
 'r44':('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R44-ORIGINAL.json','39c1c0f673747fb560cc285d627490e5cd38047a'),
 'r45':('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R45-ORIGINAL.json','1e7fb71cec336c1b4fc531d4f4a6933c9f66d415')}
ALIASES={'eax':{'eax','ax','al','ah'},'ebp':{'ebp','bp'},'ebx':{'ebx','bx','bl','bh'},'esi':{'esi','si'},'edi':{'edi','di'}}
NEGATIVE=('actual_original_program_or_payload_executed','actual_native_bool_count_or_success_proven',
 'actual_path_predicates_or_return_values_proven','actual_abi_frame_register_memory_preservation_proven',
 'same_table_byte_or_address_across_optional_call_proven','historical_flag_or_error_names_proven',
 'actual_flush_close_disk_persistence_proven','original_savedata_schema_or_server_authority_proven','stage_b_started')

def need(ok,why):
 if not ok:raise ValueError('R74 mode/barrier audit: '+why)

def barrier(row,n,register):
 if row is None:return ('unknown_instruction',n)
 if row['mnemonic']=='call':return ('opaque_call',n)
 w=set(row['decoder_written_registers'])
 if w&ALIASES[register]:return ('full_register_definition'if register in w else'partial_register_unknown',n)
 return None

def forward(nodes,edges,rows,root,at,register):
 need(register in ALIASES and root in nodes and at in nodes,'forward query')
 successors={n:[]for n in nodes}
 for a,b in edges:successors[a].append(b)
 before={n:set()for n in nodes};before[root].add(('unknown_entry',root));pending=[root]
 while pending:
  n=pending.pop();kill=barrier(rows.get(n),n,register);out={kill}if kill else before[n]
  for b in successors[n]:
   if not out<=before[b]:before[b]|=out;pending.append(b)
 return before[at]

def reverse(nodes,edges,rows,root,at,register):
 need(register in ALIASES and root in nodes and at in nodes,'reverse query')
 predecessors={n:[]for n in nodes}
 for a,b in edges:predecessors[b].append(a)
 reachable={root};frontier=[root]
 while frontier:
  source=frontier.pop(0)
  for a,b in edges:
   if a==source and b not in reachable:reachable.add(b);frontier.append(b)
 stack=list(predecessors[at]);seen=set();found={('unknown_entry',root)}if at==root else set()
 while stack:
  n=stack.pop()
  if n in seen or n not in reachable:continue
  seen.add(n)
  if n not in rows:found.add(('unknown_instruction',n));continue
  row=rows[n]
  if row['mnemonic']=='call':found.add(('opaque_call',n));continue
  # Separately authored predecessor-side classification; don't call barrier().
  writes=row['decoder_written_registers']
  if register in writes:found.add(('full_register_definition',n));continue
  if any(w in ALIASES[register]for w in writes):found.add(('partial_register_unknown',n));continue
  if n==root:found.add(('unknown_entry',root))
  stack.extend(predecessors[n])
 return found

def mem(o,base,offset,width=4):
 g=o.get('geometry',{})
 return o.get('kind')=='memory' and o.get('width_bytes')==width and g=={'base_register':base,'displacement_region':None,'index_register':None,'index_scale':1,'relative_field_offset':offset,'segment_register':None,'width_bytes':width}

def global_slot(o,rva):
 g=o.get('geometry',{});d=g.get('displacement_region')or{}
 return o.get('kind')=='memory'and o.get('width_bytes')==4 and g.get('width_bytes')==4 and g.get('base_register')is None and g.get('index_register')is None and g.get('index_scale')==1 and g.get('relative_field_offset')is None and g.get('segment_register')is None and d.get('displacement_rva')==rva and d.get('writable')is True

def imm(o,n,width=4):return o.get('kind')=='immediate' and o.get('constant')==n and o.get('width_bytes')==width

def qualify(rows,edges):
 def op(n,m):need(n in rows and rows[n]['mnemonic']==m,'instruction '+hex(n));return rows[n]['operands']
 def one(n,m,f):a=op(n,m);need(len(a)==1 and f(a[0]),'single operand '+hex(n))
 def pair(n,m,f,g):a=op(n,m);need(len(a)==2 and f(a[0])and g(a[1]),'operand pair '+hex(n))
 def r(n):return lambda o:reg(o,n)
 pair(0x4C5E3,'mov',r('eax'),lambda o:mem(o,'ebx',0))
 first=op(0x4C5E5,'mov');need(len(first)==2 and first[0].get('kind')=='register'and first[0].get('register')=='al'and first[0].get('width_bytes')==1 and first[1].get('kind')=='memory'and first[1].get('width_bytes')==1 and first[1].get('geometry')=={'base_register':'eax','displacement_region':None,'index_register':'esi','index_scale':1,'relative_field_offset':4,'segment_register':None,'width_bytes':1},'first table-byte load')
 pair(0x4C605,'test',lambda o:o.get('kind')=='register'and o.get('register')=='al'and o.get('width_bytes')==1,lambda o:imm(o,32,1))
 one(0x4C607,'je',lambda o:imm(o,0x44C615))
 one(0x4C609,'push',lambda o:imm(o,2));one(0x4C60B,'push',r('edi'));one(0x4C60C,'push',r('ecx'))
 one(0x4C60D,'call',lambda o:imm(o,0x44C761));pair(0x4C612,'add',r('esp'),lambda o:imm(o,12))
 pair(0x4C615,'mov',r('eax'),lambda o:mem(o,'ebx',0));pair(0x4C617,'add',r('eax'),r('esi'))
 pair(0x4C619,'test',lambda o:mem(o,'eax',4,1),lambda o:imm(o,128,1));one(0x4C61D,'je',lambda o:imm(o,0x44C6E4))
 for test,jump in ((0x4C605,0x4C607),(0x4C619,0x4C61D),(0x4C6C0,0x4C6C3)):
  need(rows[test]['decoder_written_registers']==['eflags']and rows[jump]['decoder_read_registers']==['eflags'],'direct flags')
 one(0x4C6BD,'push',lambda o:imm(o,5));one(0x4C6BF,'pop',r('eax'))
 pair(0x4C6C0,'cmp',lambda o:frame(o,8),r('eax'));one(0x4C6C3,'jne',lambda o:imm(o,0x44C711))
 pair(0x4C6C5,'mov',lambda o:global_slot(o,24252936),lambda o:imm(o,9))
 pair(0x4C6CF,'mov',lambda o:global_slot(o,24252940),r('eax'))
 one(0x4C6D4,'jmp',lambda o:imm(o,0x44C759));one(0x4C711,'push',lambda o:frame(o,8));one(0x4C714,'call',lambda o:imm(o,0x44C953))
 paths=[[0x4C605,0x4C607,0x4C615],[0x4C605,0x4C607,0x4C609,0x4C60B,0x4C60C,0x4C60D,0x4C612,0x4C615],
        [0x4C615,0x4C617,0x4C619,0x4C61D,0x4C623],[0x4C619,0x4C61D,0x4C6E4],
        [0x4C6BD,0x4C6BF,0x4C6C0,0x4C6C3,0x4C6C5,0x4C6CF,0x4C6D4,0x4C759],
        [0x4C6C0,0x4C6C3,0x4C711,0x4C714,0x4C719,0x4C71A,0x4C759]]
 need(all((a,b)in edges for p in paths for a,b in zip(p,p[1:])),'all structural witnesses')
 need(sorted(a for a,b in edges if b==0x4C615)==[0x4C607,0x4C612],'both optional-call rejoins')
 return paths

def invented_decisions(first,second):
 need(type(first)is int and type(second)is int and 0<=first<=255 and 0<=second<=255,'two invented independent byte snapshots')
 return bool(first&32),bool(second&128)

def analyze(raws):
 need(set(raws)==set(PINS),'source inventory');d={}
 for k,(_,pin)in PINS.items():
  raw=raws[k];need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin,'immutable source '+k);d[k]=json.loads(raw)
 validate_r73(d['r73']);rows=retained_rows(d.values());nodes=set(d['r73']['bounded_graph_node_rvas']);edges={tuple(e)for e in d['r73']['bounded_graph_edges']};root=0x4C5B4
 need(nodes<=rows.keys()and len(nodes)==139 and len(edges)==156,'complete bounded139/156 operand inventory')
 paths=qualify(rows,edges);queries=[]
 for register,at in [('ebp',0x4C615),('ebx',0x4C615),('esi',0x4C615),('ebp',0x4C696),('ebp',0x4C6FB),('ebp',0x4C743),('edi',0x4C6B0),('eax',0x4C760)]:
  f=forward(nodes,edges,rows,root,at,register);r=reverse(nodes,edges,rows,root,at,register);need(f==r and bool(f),'independent register source agreement')
  queries.append({'register':register,'before_rva':at,'syntax_sources':[{'origin':k,'site_rva':n}for k,n in sorted(f)],'actual_value_or_preservation_proven':False})
 need(all(any(s['origin']=='opaque_call'and s['site_rva']==0x4C60D for s in q['syntax_sources'])for q in queries[:3]),'optional call prevents frame/table register carry')
 counts={(a,b):0 for a in (False,True)for b in(False,True)}
 for first in range(256):
  for second in range(256):
   got=invented_decisions(first,second);ref=((first//32)%2==1,second>=128);need(got==ref,'independent invented predicate arithmetic');counts[got]+=1
 need(set(counts.values())=={16384},'four independent snapshot predicate combinations')
 calls=[]
 for n in sorted(nodes):
  row=rows[n]
  if row['mnemonic']!='call':continue
  o=row['operands'][0]
  calls.append({'site_rva':n,'target_rva':o['constant']-4194304 if o['kind']=='immediate'else None,'indirect_slot_rva':o.get('geometry',{}).get('displacement_region',{}).get('displacement_rva'),'all_register_and_memory_effects_opaque':True})
 need(len(calls)==6,'six retained calls')
 return {'schema':'tw10-r74-full-bounded-mode-predicates-and-call-barriers','source_git_blobs':{k:v[1]for k,v in PINS.items()},'root_rva':root,'bounded_graph_nodes':len(nodes),'bounded_graph_edges':len(edges),'decoded_graph_nodes':len(nodes&rows.keys()),'missing_bounded_operand_nodes':sorted(nodes-rows.keys()),'complete_original_execution_or_callee_graph_claimed':False,'qualified_structural_paths':paths,'mode_snapshot_masks':[32,128],'first_nonzero_mask_route':'three PUSH shapes then opaque direct call0x4c761; first-mask zero bypasses call','second_nonzero_mask_route':'fallthrough0x4c623 to qualified byte-expansion loop; zero jumps0x4c6e4 direct native-prefix shapes','mode_bytes_are_separate_temporal_snapshots':True,'register_queries':queries,'opaque_calls':calls,'invented_two_snapshot_predicate_comparisons':65536,'invented_combination_counts':[{'optional_call':a,'expansion_route':b,'count':n}for(a,b),n in sorted(counts.items())],'literal_five_route':'PUSH5/POP EAX; CMP frame[+8],EAX/JNE; equality writes literals9 and5-shaped EAX to two globals before all-ones return; historical meaning unproven','literal_five_inequality_route':'PUSH frame[+8]; opaque direct call0x4c953; POP ECX; JMP all-ones definition','every_call_still_kills_register_and_memory_knowledge':True,'all_model_snapshots_are_invented':True,**{k:False for k in NEGATIVE},'stage_a_families':'PARTIAL/OPEN','next':'R75 retained-first original helper0x4c761/0x4c953 entry/call effects and ABI/frame/table preservation gap inventory; prioritize effects material to native count/position/persistence; no indiscriminate helper exhaustion.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--verify',type=Path);a=p.parse_args();d=analyze({k:(BASE/n).read_bytes()for k,(n,_)in PINS.items()})
 if a.verify:need(d==json.loads(a.verify.read_bytes()),'exact permanent replay');print('TW10_R74_FULL_BOUNDED_OPERANDS_AND_OPAQUE_CALLS=PASS; ACTUAL_NATIVE_IO=OPEN')
 else:print(json.dumps(d,sort_keys=True,indent=2))
if __name__=='__main__':main()
