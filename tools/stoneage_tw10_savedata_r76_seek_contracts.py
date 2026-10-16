"""R76: conditional symbolic stack/bit contracts; original APIs never execute.

Stack words are invented labels. Four call-cleanup assumptions and nonaliasing
saved stack storage are explicit premises, not recovered runtime guarantees.
"""
import argparse
import hashlib
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_r75_guard import validate as validate_r75
from tools.stoneage_tw10_savedata_r74_modes_barriers import forward,reverse,reg,mem,imm
BASE=Path(__file__).resolve().parents[1]/'research/recovered'
PINS={
 'r75':('STONEAGE-TW10-SAVEDATA-NATIVE-SEEK-HELPER-R75-ORIGINAL.json','757c22945d7e18263b154e88f52376d0ab58d42c'),
 'r46':('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R46-ORIGINAL.json','19d730daf617313508ccf81e940c0a51f3be8395'),
 'r73':('STONEAGE-TW10-SAVEDATA-NATIVE-MODES-R73-ORIGINAL.json','2a90bf654a723da53f7d6a26008ca660cb89b290'),
 'r69':('STONEAGE-TW10-SAVEDATA-NATIVE-EARLY-R69-ORIGINAL.json','d5d4924803dc28de8be00f712eecd11cf9003c66')}
CLEANUPS={0x4C78E:0,0x4C7B0:16,0x4C7BD:0,0x4C7CC:0}
NEGATIVE=('actual_original_program_or_payload_executed','actual_native_seek_position_return_or_success_proven',
 'actual_abi_stack_cleanup_or_nonaliasing_proven','actual_callee_frame_register_memory_preservation_proven',
 'same_caller_helper_table_address_or_byte_proven','historical_mask2_flag_name_proven',
 'actual_flush_close_disk_persistence_proven','original_savedata_schema_or_server_authority_proven','stage_b_started')
OFFICIAL={
 'set_file_pointer':{'url':'https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfilepointer','accessed':'2026-10-16','scope':'Modern Microsoft API contract used only as an explicit conditional interpretation: arguments handle/low-distance/high-pointer/method; FILE_END=2, zero distance requests current EOF; no original execution claim.'},
 'x86_stdcall':{'url':'https://learn.microsoft.com/en-us/cpp/cpp/stdcall?view=msvc-170','accessed':'2026-10-16','scope':'Modern Microsoft x86 convention reference: right-to-left stack arguments and callee argument cleanup. Original ABI compatibility remains an assumption.'}}

def need(ok,why):
 if not ok:raise ValueError('R76 conditional seek contracts: '+why)

def qualify(rows,edges):
 def one(at,m,f):
  need(at in rows and rows[at]['mnemonic']==m,'instruction '+hex(at));o=rows[at]['operands'];need(len(o)==1 and f(o[0]),'operand '+hex(at))
 def pair(at,m,a,b):
  need(at in rows and rows[at]['mnemonic']==m,'instruction '+hex(at));o=rows[at]['operands'];need(len(o)==2 and a(o[0])and b(o[1]),'pair '+hex(at))
 for at,r in[(0x4C765,'ebx'),(0x4C76C,'esi'),(0x4C76D,'edi')]:one(at,'push',lambda o,r=r:reg(o,r))
 for at,r in[(0x4C7F7,'edi'),(0x4C7F8,'esi'),(0x4C7F9,'ebx')]:one(at,'pop',lambda o,r=r:reg(o,r))
 need(rows[0x4C7FA]['mnemonic']=='ret'and rows[0x4C7FA]['operands']==[],'near RET without immediate')
 pair(0x4C761,'mov',lambda o:reg(o,'eax'),lambda o:mem(o,'esp',4))
 one(0x4C7A5,'push',lambda o:mem(o,'esp',24));one(0x4C7A9,'push',lambda o:imm(o,0));one(0x4C7AB,'push',lambda o:mem(o,'esp',28));one(0x4C7AF,'push',lambda o:reg(o,'eax'))
 one(0x4C78D,'push',lambda o:reg(o,'eax'));one(0x4C796,'pop',lambda o:reg(o,'ecx'));one(0x4C7D1,'pop',lambda o:reg(o,'ecx'))
 pair(0x4C7B6,'mov',lambda o:reg(o,'ebx'),lambda o:reg(o,'eax'));pair(0x4C7B8,'cmp',lambda o:reg(o,'ebx'),lambda o:imm(o,-1))
 one(0x4C7BB,'jne',lambda o:imm(o,0x44C7C5));pair(0x4C7C5,'xor',lambda o:reg(o,'eax'),lambda o:reg(o,'eax'))
 pair(0x4C7C7,'test',lambda o:reg(o,'eax'),lambda o:reg(o,'eax'));one(0x4C7C9,'je',lambda o:imm(o,0x44C7D4))
 pair(0x4C7DF,'mov',lambda o:reg(o,'eax'),lambda o:reg(o,'ebx'))
 row=rows[0x4C7D6];o=row['operands'];g=o[0].get('geometry',{})
 need(row['mnemonic']=='and'and len(o)==2 and o[0].get('kind')=='memory'and o[0].get('width_bytes')==1 and g=={'base_register':'eax','displacement_region':None,'index_register':'esi','index_scale':1,'relative_field_offset':4,'segment_register':None,'width_bytes':1}and imm(o[1],253,1)and o[0].get('decoder_read')is True and o[0].get('decoder_write')is True,'exact local table byte read-modify-write')
 for a,b in[(0x4C7B8,0x4C7BB),(0x4C7C7,0x4C7C9)]:need(rows[a]['decoder_written_registers']==['eflags']and rows[b]['decoder_read_registers']==['eflags'],'return/error flags')
 calls=sorted(n for n,r in rows.items()if r['mnemonic']=='call');need(calls==sorted(CLEANUPS),'exact four opaque callees')
 for at,target in[(0x4C78E,0x44E8FB),(0x4C7CC,0x44C953)]:one(at,'call',lambda o,target=target:imm(o,target))
 for at,slot in[(0x4C7B0,0x520CC),(0x4C7BD,0x5208C)]:
  o=rows[at]['operands'][0];g=o.get('geometry',{});region=g.get('displacement_region')or{}
  need(o.get('kind')=='memory'and o.get('width_bytes')==4 and g.get('base_register')is None and g.get('index_register')is None and g.get('segment_register')is None and g.get('index_scale')==1 and region.get('displacement_rva')==slot,'exact API import slot')
 need(all(r['mnemonic']in('push','pop','call','ret')for r in rows.values()if 'esp'in r['decoder_written_registers']),'no unmodeled local ESP adjustment')
 paths=[[0x4C7A5,0x4C7A9,0x4C7AB,0x4C7AF,0x4C7B0],[0x4C7B0,0x4C7B6,0x4C7B8,0x4C7BB,0x4C7BD,0x4C7C3,0x4C7C7],[0x4C7BB,0x4C7C5,0x4C7C7,0x4C7C9,0x4C7D4,0x4C7D6,0x4C7DB,0x4C7DF,0x4C7E1,0x4C7F7,0x4C7F8,0x4C7F9,0x4C7FA]]
 need(all((a,b)in edges for p in paths for a,b in zip(p,p[1:])),'retained local witnesses')
 return paths

def paths_to_return(nodes,edges,rows):
 succ={n:[]for n in nodes}
 for a,b in edges:succ[a].append(b)
 found=[];pending=[(0x4C761,[])]
 while pending:
  n,p=pending.pop();need(n not in p and len(p)<len(nodes),'bounded acyclic helper graph');p=p+[n]
  if rows[n]['mnemonic']=='ret':found.append(p);continue
  need(bool(succ[n]),'no unexplained terminal node')
  for b in sorted(succ[n]):pending.append((b,p))
  need(len(pending)+len(found)<128,'path cap')
 return sorted(found)

def stack_ledger(path,rows,cleanups=None,clobber_saved=False):
 """Conditional symbolic slots only. Calls kill registers; stack memory is a premise."""
 cleanups=CLEANUPS if cleanups is None else cleanups
 regs={r:'entry_'+r for r in('eax','ecx','edx','ebx','esi','edi','ebp')};stack={0:'caller_return_address',4:'caller_ecx',8:0,12:2};esp=0;seek_args=None;reads=[]
 def value(o):
  if o['kind']=='register':return regs.get(o['register'],'unknown_partial_register')
  if o['kind']=='immediate':return o['constant']
  if o['kind']=='memory'and o.get('geometry',{}).get('base_register')=='esp':return stack.get(esp+o['geometry']['relative_field_offset'],'unknown_stack_word')
  return 'unknown_memory'
 for n in path:
  r=rows[n];m=r['mnemonic'];op=r['operands'];handled=False
  if m=='push':v=value(op[0]);esp-=4;stack[esp]=v;handled=True
  elif m=='pop':regs[op[0]['register']]=stack.get(esp,'unknown_stack_word');esp+=4;handled=True
  elif m=='call':
   need(n in cleanups and type(cleanups[n])is int and 0<=cleanups[n]<=16 and cleanups[n]%4==0,'explicit returning-call cleanup premise')
   if n==0x4C7B0:seek_args=[stack.get(esp+i,'unknown_stack_word')for i in(0,4,8,12)]
   for register in regs:regs[register]='opaque_'+register+'_after_'+str(n)
   esp+=cleanups[n]
   if clobber_saved:
    for address in(-4,-8,-12):stack[address]='opaque_alias_write'
   handled=True
  elif m=='mov'and op[0].get('kind')=='register':regs[op[0]['register']]=value(op[1]);handled=True
  if not handled:
   for w in r['decoder_written_registers']:
    if w in regs:regs[w]='unmodeled_definition_'+str(n)
  if m=='ret':
   return {'ret_rva':n,'esp_before_ret':esp,'return_address_token':stack.get(esp),'restored_registers':[r for r in('ebx','esi','edi')if regs[r]=='entry_'+r],'ebp_entry_token_preserved':regs['ebp']=='entry_ebp','seek_argument_tokens_if_reached':seek_args}
 raise ValueError('R76 ledger: no RET')

def delta_reference(path,rows,cleanups):
 # Independent scalar accounting; this routine never stores labels or registers.
 pushes=sum(rows[n]['mnemonic']=='push'for n in path)
 pops=sum(rows[n]['mnemonic']=='pop'for n in path)
 return 4*(pops-pushes)+sum(cleanups[n]for n in path if rows[n]['mnemonic']=='call')

def analyze(raws):
 need(set(raws)==set(PINS),'source inventory');d={}
 for k,(_,pin)in PINS.items():
  raw=raws[k];need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin,'immutable source '+k);d[k]=json.loads(raw)
 validate_r75(d['r75']);g=d['r75'];rows={r['site_rva']:r for r in g['decoded_instruction_rows']};nodes=set(g['bounded_graph_node_rvas']);edges={tuple(e)for e in g['bounded_graph_edges']};witness=qualify(rows,edges);paths=paths_to_return(nodes,edges,rows);ledgers=[stack_ledger(p,rows)for p in paths]
 need(all(delta_reference(p,rows,CLEANUPS)==x['esp_before_ret']for p,x in zip(paths,ledgers)),'independent scalar stack-delta agreement')
 need(all(x['esp_before_ret']==0 and x['return_address_token']=='caller_return_address'and x['restored_registers']==['ebx','esi','edi']for x in ledgers),'conditional local save/restore and return address')
 seeks=[x['seek_argument_tokens_if_reached']for x in ledgers if x['seek_argument_tokens_if_reached']is not None]
 need(seeks and all(s[1:]==[0,0,2]for s in seeks),'conditional low0/high-null/method2 physical binding')
 ebp_writes=[n for n,r in rows.items()if 'ebp'in r['decoder_written_registers']or 'bp'in r['decoder_written_registers']];need(ebp_writes==[],'no local explicit EBP definition')
 queries=[]
 for register,at in [('ebp',0x4C7FA),('edi',0x4C7D4),('esi',0x4C7D6),('ebx',0x4C7DF)]:
  f=forward(nodes,edges,rows,0x4C761,at,register);r=reverse(nodes,edges,rows,0x4C761,at,register);need(f==r and bool(f),'independent strict call barrier query')
  queries.append({'register':register,'before_rva':at,'syntax_sources':[{'origin':k,'site_rva':n}for k,n in sorted(f)],'actual_value_or_preservation_proven':False})
 # Verify caller route's zero-EDI/PUSH2/PUSH EDI/PUSH ECX spelling separately.
 caller={r['site_rva']:r for r in d['r73']['decoded_instruction_rows']};early={r['site_rva']:r for r in d['r69']['decoded_instruction_rows']}
 need(early[0x4C5F1]['mnemonic']=='xor'and all(reg(o,'edi')for o in early[0x4C5F1]['operands']),'caller conditional EDI zero')
 need(imm(caller[0x4C609]['operands'][0],2)and reg(caller[0x4C60B]['operands'][0],'edi')and reg(caller[0x4C60C]['operands'][0],'ecx'),'caller suffix')
 seek_id=d['r46']['write_helper_context']['seek_api_identity'];need(seek_id['call_rva']==0x4C7B0 and seek_id['import_identity']=={'dll':'KERNEL32.dll','iat_rva':0x520CC,'name':'SetFilePointer'},'original import identity')
 for byte in range(256):
  changed=byte&253;ref=byte-2 if (byte//2)%2 else byte;need(changed==ref and changed&32==byte&32 and changed&128==byte&128,'invented local bit2-clear contract')
 return {'schema':'tw10-r76-conditional-seek-helper-stack-register-and-table-contracts','source_git_blobs':{k:v[1]for k,v in PINS.items()},'graph_nodes':len(nodes),'graph_edges':len(edges),'decoded_rows':len(rows),'qualified_witness_paths':witness,'structural_root_to_ret_paths':len(paths),'path_overapproximation_is_not_actual_feasibility':True,'conditional_stack_ledgers':ledgers,'call_cleanup_assumptions_bytes':{str(k):v for k,v in CLEANUPS.items()},'additional_stack_premises':['32-bit near-call/ret and dword stack geometry','all calls return normally with the declared cleanup','entry arguments and saved register slots are valid and not overwritten by aliases or callees','all explicit nonstack stores are disjoint from saved stack slots','caller reaches optional call after zero EDI definition; no historical path asserted'],'conditional_local_ebx_esi_edi_restoration':True,'local_explicit_ebp_write_sites':ebp_writes,'strict_opaque_call_queries':queries,'conditional_seek_request':{'import':'KERNEL32.dll!SetFilePointer','hFile':'opaque EAX result from direct helper0x4e8fb','lDistanceToMove':0,'lpDistanceToMoveHigh':0,'dwMoveMethod':2,'interpretation':'Under the documented API/ABI and stack premises this requests positioning at the current end of a valid seekable file; actual call/position/success and original flag names remain unproven.'},'local_table_byte_and_mask':253,'local_clear_bit_value':2,'invented_byte_mask_comparisons':256,'local_operation_preserves_mask32_and128':True,'does_not_establish_global_snapshot_identity':True,'official_conditional_contract_references':OFFICIAL,**{k:False for k in NEGATIVE},'stage_a_families':'PARTIAL/OPEN','next':'R77 retained-first direct helper0x4e8fb handle-source/caller-visible effects and0x4c953 error/helper impacts only where material; preserve import ABI, saved-slot nonaliasing, table pointer and actual native IO boundaries.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--verify',type=Path);a=p.parse_args();d=analyze({k:(BASE/n).read_bytes()for k,(n,_)in PINS.items()})
 if a.verify:need(d==json.loads(a.verify.read_bytes()),'exact canonical replay');print('TW10_R76_CONDITIONAL_SEEK_STACK_AND_LOCAL_MASK_CONTRACTS=PASS; ACTUAL_NATIVE_IO=OPEN')
 else:print(json.dumps(d,sort_keys=True,indent=2))
if __name__=='__main__':main()
