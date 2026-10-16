"""R78: retained-source table-return contracts, not original execution."""
import argparse
import hashlib
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_r77_guard import validate as guard
from tools.stoneage_tw10_savedata_r74_modes_barriers import reg,mem,imm,global_slot,forward,reverse
BASE=Path(__file__).resolve().parents[1]/'research/recovered'
PINS={'r77':('STONEAGE-TW10-SAVEDATA-NATIVE-HANDLE-R77-ORIGINAL.json','870b84cb7968d325b37463ca68de1540960e1f5e'),'r75':('STONEAGE-TW10-SAVEDATA-NATIVE-SEEK-HELPER-R75-ORIGINAL.json','757c22945d7e18263b154e88f52376d0ab58d42c')}
NEGATIVE=('original_program_or_payload_executed','actual_handle_or_table_values_proven','actual_native_seek_success_or_position_proven','actual_abi_stack_nonaliasing_or_memory_validity_proven','stable_table_snapshots_or_no_external_writes_proven','historical_crt_function_or_error_names_proven','actual_flush_close_or_disk_persistence_proven','original_schema_or_server_authority_proven','stage_b_started')

def need(ok,why):
 if not ok:raise ValueError('R78 handle contracts: '+why)

def indexed(o,base,index,scale,offset,width,slot=None):
 g=o.get('geometry',{});region=g.get('displacement_region')
 return o.get('kind')=='memory'and o.get('width_bytes')==width and g.get('width_bytes')==width and g.get('base_register')==base and g.get('index_register')==index and g.get('index_scale')==scale and g.get('relative_field_offset')==offset and g.get('segment_register')is None and ((region is None)if slot is None else isinstance(region,dict)and region.get('displacement_rva')==slot and region.get('writable')is True)

def qualify(rows,edges):
 def pair(at,m,a,b):
  r=rows[at];o=r['operands'];need(r['mnemonic']==m and len(o)==2 and a(o[0])and b(o[1]),'pair '+hex(at))
 def one(at,m,f):
  r=rows[at];o=r['operands'];need(r['mnemonic']==m and len(o)==1 and f(o[0]),'single '+hex(at))
 pair(0x4e8fb,'mov',lambda o:reg(o,'eax'),lambda o:mem(o,'esp',4))
 pair(0x4e8ff,'cmp',lambda o:reg(o,'eax'),lambda o:global_slot(o,24254560))
 one(0x4e905,'jae',lambda o:imm(o,0x44e923))
 pair(0x4e907,'mov',lambda o:reg(o,'ecx'),lambda o:reg(o,'eax'))
 pair(0x4e909,'and',lambda o:reg(o,'eax'),lambda o:imm(o,31))
 pair(0x4e90c,'sar',lambda o:reg(o,'ecx'),lambda o:imm(o,5,1))
 pair(0x4e90f,'mov',lambda o:reg(o,'ecx'),lambda o:indexed(o,None,'ecx',4,None,4,24254304))
 pair(0x4e916,'test',lambda o:indexed(o,'ecx','eax',8,4,1),lambda o:imm(o,1,1))
 pair(0x4e91b,'lea',lambda o:reg(o,'eax'),lambda o:indexed(o,'ecx','eax',8,0,4))
 one(0x4e91e,'je',lambda o:imm(o,0x44e923))
 pair(0x4e920,'mov',lambda o:reg(o,'eax'),lambda o:mem(o,'eax',0))
 pair(0x4e923,'and',lambda o:global_slot(o,24252940),lambda o:imm(o,0))
 pair(0x4e92a,'mov',lambda o:global_slot(o,24252936),lambda o:imm(o,9))
 pair(0x4e934,'or',lambda o:reg(o,'eax'),lambda o:imm(o,0xffffffff))
 for n in(0x4e922,0x4e937):need(rows[n]['mnemonic']=='ret'and rows[n]['operands']==[],'plain near RET')
 expected=[(0x4e8fb,0x4e8ff),(0x4e8ff,0x4e905),(0x4e905,0x4e907),(0x4e905,0x4e923),(0x4e907,0x4e909),(0x4e909,0x4e90c),(0x4e90c,0x4e90f),(0x4e90f,0x4e916),(0x4e916,0x4e91b),(0x4e91b,0x4e91e),(0x4e91e,0x4e920),(0x4e91e,0x4e923),(0x4e920,0x4e922),(0x4e923,0x4e92a),(0x4e92a,0x4e934),(0x4e934,0x4e937)]
 need(edges==set(expected)and set(rows)=={n for e in expected for n in e},'complete16-node16-edge topology')
 need(rows[0x4e8ff]['decoder_written_registers']==['eflags']and rows[0x4e905]['decoder_read_registers']==['eflags'],'unsigned direct flags')
 need(rows[0x4e916]['decoder_written_registers']==['eflags']and rows[0x4e91b]['decoder_written_registers']==['eax']and rows[0x4e91e]['decoder_read_registers']==['eflags'],'TEST through flag-preserving LEA')
 writes=set().union(*(set(r['decoder_written_registers'])for r in rows.values()))
 need(writes=={'eax','ecx','eflags','esp'}and not any(r['mnemonic']=='call'for r in rows.values()),'local register effects/no calls')
 stores=[n for n,r in rows.items()if any(o.get('kind')=='memory'and o.get('decoder_write')is True for o in r['operands'])]
 need(sorted(stores)==[0x4e923,0x4e92a],'only two explicit memory stores')
 return stores

def geometry(value):
 """Invented 32-bit word arithmetic only; SAR is deliberately signed."""
 x=value&0xffffffff;signed=x if x<0x80000000 else x-0x100000000
 return signed>>5,(x&31)*8

def reference_geometry(value):
 x=value%(2**32)
 bucket=x//32 if x<2**31 else -((2**32-x+31)//32)
 return bucket,(x%32)*8

def analyze(raws):
 d={}
 for k,(_,pin)in PINS.items():
  raw=raws[k];need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin,'immutable source '+k);d[k]=json.loads(raw)
 guard(d['r77']);g=d['r77'];rows={r['site_rva']:r for r in g['decoded_instruction_rows']};edges=set(map(tuple,g['bounded_graph_edges']));stores=qualify(rows,edges)
 queries=[]
 for at in(0x4e922,0x4e937):
  for register in('ebp','ebx','esi','edi','eax'):
   f=forward(set(rows),edges,rows,0x4e8fb,at,register);r=reverse(set(rows),edges,rows,0x4e8fb,at,register);need(f==r,'independent register sources')
   queries.append({'before_rva':at,'register':register,'syntax_sources':sorted(f)})
 caller={r['site_rva']:r for r in d['r75']['decoded_instruction_rows']}
 need(caller[0x4c78d]['mnemonic']=='push'and reg(caller[0x4c78d]['operands'][0],'eax'),'caller input PUSH EAX')
 need(caller[0x4c793]['mnemonic']=='cmp'and reg(caller[0x4c793]['operands'][0],'eax')and imm(caller[0x4c793]['operands'][1],-1),'caller sentinel comparison')
 need(caller[0x4c797]['mnemonic']=='jne'and imm(caller[0x4c797]['operands'][0],0x44c7a5),'caller skips API on allones')
 values=list(range(4096))+[0x7fffffff,0x80000000,0x80000001,0xffffffe0,0xffffffff,-1,2**32,2**32+31]
 for x in values:need(geometry(x)==reference_geometry(x),'independent invented geometry')
 # Full invented byte domain: local bit1 predicate, not original flag values.
 for x in range(256):need(bool(x&1)==bool(x%2),'invented bit predicate')
 return {'schema':'tw10-r78-conditional-handle-table-return-contracts','source_git_blobs':{k:v[1]for k,v in PINS.items()},'graph_nodes':16,'graph_edges':16,'call_count':0,'explicit_store_rvas':sorted(stores),'register_source_queries':queries,'local_untouched_registers':['ebp','ebx','esi','edi','edx'],'plain_ret_rvas':[0x4e922,0x4e937],'conditional_return_sources':{'guard_pass':'dword read at table_pointer[(signed32(input)>>5)] +8*(input&31)','guard_failure':'0xffffffff after global AND0 and MOV9 spellings'},'guard_shape':'unsigned input<global24254560, then byte[slot+4]&1 nonzero; memory validity/stability required','table_base_displacement_rva':24254304,'bucket_index_is_arithmetic_signed_shift':True,'invented_geometry_comparisons':len(values),'invented_flag_byte_comparisons':256,'caller_relation':'Under normal dword near-call/ret, valid nonaliasing stack and stable valid table memory, PUSH EAX supplies helper[ESP+4]; non-allones result reaches SetFilePointer hFile PUSH. This does not prove a valid OS handle or actual I/O.','premises':['normal32-bit near-call/ret','valid nonaliasing stack and global/table reads/writes','stable corresponding input/table snapshots where equated','actual path reaches caller/API only conditionally'],'stage_a_families':'PARTIAL/OPEN',**{k:False for k in NEGATIVE},'next':'R79: qualify retained caller/table relation and error-helper0x4c953 only where material to nonzero-error return; keep original IO/persistence/schema and ABI/alias boundaries OPEN.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args();raw=json.dumps(analyze({k:(BASE/n).read_bytes()for k,(n,_)in PINS.items()}),sort_keys=True,indent=2)+'\n'
 if a.output:a.output.write_text(raw)
 else:print(raw,end='')
if __name__=='__main__':main()
