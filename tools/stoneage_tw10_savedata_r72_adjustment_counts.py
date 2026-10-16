"""R72: pinned adjustment/byte-store syntax and invented count-unit models.

This is an independently authored specification model, never an emulator of
original client code and never an evaluation of original save/memory bytes.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_r71_guard import validate as validate_r71
from tools.stoneage_tw10_savedata_r71_adjustment_static import retained_rows
from tools.stoneage_tw10_savedata_r70_conditional_returns import reg, frame
from tools.stoneage_tw10_savedata_r66_count_consumers import consumer_contract

BASE=Path(__file__).resolve().parents[1]/'research/recovered'
U32=2**32-1
PINS={
 'r71':('STONEAGE-TW10-SAVEDATA-NATIVE-ADJUSTMENT-R71-ORIGINAL.json','f2a946ffc93c6a32210f2ebaa9dc9191833aac37'),
 'r69':('STONEAGE-TW10-SAVEDATA-NATIVE-EARLY-R69-ORIGINAL.json','d5d4924803dc28de8be00f712eecd11cf9003c66'),
 'r67':('STONEAGE-TW10-SAVEDATA-NATIVE-TAIL-R67-ORIGINAL.json','04162081d346b8c53424295de9fdc6b8f385b011'),
 'r63':('STONEAGE-TW10-SAVEDATA-POSTCALL-R63-DERIVED.json','3b7c9cea63ed4e2a360ddb6934e7dcd44b9833e7'),
 'r44':('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R44-ORIGINAL.json','39c1c0f673747fb560cc285d627490e5cd38047a'),
 'r45':('STONEAGE-TW10-SAVEDATA-NATIVE-IO-R45-ORIGINAL.json','1e7fb71cec336c1b4fc531d4f4a6933c9f66d415')}
NEGATIVE=('actual_original_execution_or_payload_evaluated','actual_native_bool_count_or_success_proven',
 'actual_path_predicates_or_return_values_proven','actual_temporal_frame_memory_alias_or_abi_proven',
 'partial_write_return_is_general_logical_prefix_count','actual_flush_close_disk_persistence_proven',
 'original_savedata_schema_checksum_migration_server_authority_proven','stage_b_started')

def need(ok,why):
 if not ok:raise ValueError('R72 adjustment counts: '+why)

def byte_reg(o,name):return o.get('kind')=='register' and o.get('register')==name and o.get('width_bytes')==1

def byte_mem(o,base):
 g=o.get('geometry',{})
 return o.get('kind')=='memory' and o.get('width_bytes')==1 and g=={'base_register':base,'displacement_region':None,'index_register':None,'index_scale':1,'relative_field_offset':0,'segment_register':None,'width_bytes':1}

def literal(o,n,width):return o.get('kind')=='immediate' and o.get('constant')==n and o.get('width_bytes')==width

def qualify(rows,edges):
 def op(at,m):
  need(at in rows and rows[at]['mnemonic']==m,'mnemonic '+hex(at));return rows[at]['operands']
 def pair(at,m,a,b):
  o=op(at,m);need(len(o)==2 and a(o[0]) and b(o[1]),'geometry '+hex(at))
 def unary(at,m,a):
  o=op(at,m);need(len(o)==1 and a(o[0]),'unary '+hex(at))
 def r(n):return lambda o:reg(o,n)
 def f(n):return lambda o:frame(o,n) and o.get('geometry',{}).get('index_scale')==1
 pair(0x4C623,'mov',r('eax'),f(12));pair(0x4C629,'mov',f(-4),r('eax'))
 pair(0x4C635,'lea',r('eax'),f(-1044))
 pair(0x4C63B,'mov',r('ecx'),f(-4));pair(0x4C63E,'sub',r('ecx'),f(12))
 pair(0x4C641,'cmp',r('ecx'),f(16));unary(0x4C644,'jae',lambda o:literal(o,0x44C66F,4))
 pair(0x4C646,'mov',r('ecx'),f(-4));unary(0x4C649,'inc',f(-4))
 pair(0x4C64C,'mov',lambda o:byte_reg(o,'cl'),lambda o:byte_mem(o,'ecx'))
 pair(0x4C64E,'cmp',lambda o:byte_reg(o,'cl'),lambda o:literal(o,10,1))
 unary(0x4C651,'jne',lambda o:literal(o,0x44C65A,4))
 unary(0x4C653,'inc',f(-16))
 pair(0x4C656,'mov',lambda o:byte_mem(o,'eax'),lambda o:literal(o,13,1))
 unary(0x4C659,'inc',r('eax'))
 pair(0x4C65A,'mov',lambda o:byte_mem(o,'eax'),lambda o:byte_reg(o,'cl'))
 unary(0x4C65C,'inc',r('eax'));pair(0x4C65D,'mov',r('ecx'),r('eax'))
 pair(0x4C65F,'lea',r('edx'),f(-1044));pair(0x4C665,'sub',r('ecx'),r('edx'))
 pair(0x4C667,'cmp',r('ecx'),lambda o:literal(o,1024,4))
 unary(0x4C66D,'jl',lambda o:literal(o,0x44C63B,4))
 pair(0x4C6AD,'mov',r('eax'),f(-8));pair(0x4C743,'sub',r('eax'),f(-16))
 pair(0x4C5F1,'xor',r('edi'),r('edi'))
 for at,off in ((0x4C5F6,-8),(0x4C5F9,-16)):pair(at,'mov',f(off),r('edi'))
 inc=rows[0x4C653]['operands'][0]
 need(inc.get('decoder_read')is True and inc.get('decoder_write')is True,'adjustment read-modify-write')
 for cmp,jcc in ((0x4C641,0x4C644),(0x4C64E,0x4C651),(0x4C667,0x4C66D)):
  need(rows[cmp]['decoder_written_registers']==['eflags'] and rows[jcc]['decoder_read_registers']==['eflags'],'direct flag provenance')
 paths=[
  [0x4C646,0x4C649,0x4C64C,0x4C64E,0x4C651,0x4C653,0x4C656,0x4C659,0x4C65A,0x4C65C,0x4C65D,0x4C65F,0x4C665,0x4C667,0x4C66D],
  [0x4C64E,0x4C651,0x4C65A,0x4C65C],
  [0x4C63B,0x4C63E,0x4C641,0x4C644,0x4C66F],
  [0x4C667,0x4C66D,0x4C63B],
  [0x4C6AD,0x4C6B0,0x4C6B2,0x4C743]]
 need(all((a,b)in edges for p in paths for a,b in zip(p,p[1:])),'bounded structural witnesses')
 need(sorted(a for a,b in edges if b==0x4C653)==[0x4C651] and sorted(b for a,b in edges if a==0x4C651)==[0x4C653,0x4C65A],'both adjustment predicate edges')
 return paths

def model(tokens,threshold=1024):
 """Invented octets only, with ordinary nonwrapping indices and valid memory."""
 need(type(threshold)is int and 1<=threshold<=1024,'invented threshold')
 need(isinstance(tokens,(list,tuple)) and all(type(x)is int and 0<=x<=255 for x in tokens),'invented octet domain')
 chunks=[];out=[];adjustment=0;consumed=0
 for token in tokens:
  consumed+=1
  if token==10:adjustment+=1;out.append(13)
  out.append(token)
  # The source compares after both stores, so a threshold may be exceeded by1.
  if len(out)>=threshold:
   chunks.append({'output':out,'adjustment':adjustment,'consumed':consumed});out=[];adjustment=0;consumed=0
 if out:chunks.append({'output':out,'adjustment':adjustment,'consumed':consumed})
 return chunks

def independent_reference(tokens):
 return [v for token in tokens for v in ((13,token)if token==10 else(token,))]

def full_write_relation(tokens,threshold=1024):
 chunks=model(tokens,threshold);output=[v for c in chunks for v in c['output']]
 need(output==independent_reference(tokens),'independent invented byte-sequence reference')
 writes=sum(len(c['output'])for c in chunks);adjustment=sum(c['adjustment']for c in chunks)
 need(writes-adjustment==len(tokens),'invented complete-write count identity')
 return writes,adjustment,[len(c['output'])for c in chunks]

def analyze(raws):
 need(set(raws)==set(PINS),'source inventory');sources={}
 for k,(_,pin)in PINS.items():
  raw=raws[k];need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin,'immutable source '+k);sources[k]=json.loads(raw)
 validate_r71(sources['r71']);rows=retained_rows(sources.values());g=sources['r71'];edges={tuple(e)for e in g['bounded_graph_edges']};nodes=set(g['bounded_graph_node_rvas'])
 paths=qualify(rows,edges);consumers=consumer_contract(sources['r63'])
 traces=0
 for size in range(5):
  for seq in itertools.product((0,10,13,65,255),repeat=size):
   for threshold in (1,2,3,1024):full_write_relation(seq,threshold);traces+=1
 edge_cases=[[65]*1023+[10],[10]*513,[65]*1024+[10],[10,13,10]]
 boundary=[{'invented_input_units':len(s),'output_units':full_write_relation(s)[0],'insertions':full_write_relation(s)[1],'chunk_lengths':full_write_relation(s)[2]}for s in edge_cases]
 need(boundary[0]['chunk_lengths']==[1025] and boundary[1]['chunk_lengths']==[1024,2],'post-store threshold behavior')
 # Generated for one invented token10: output13,10 and adjustment1. Prefix0
 # underflows uint32 subtraction; prefix1 (only inserted13) gives0; prefix2 gives1.
 partial=[{'invented_native_count':n,'invented_total_adjustment':1,'uint32_subtraction':(n-1)&U32,'completed_input_tokens_in_output_prefix':int(n==2)}for n in range(3)]
 # A planned insertion later in the buffer invalidates a general prefix-count
 # reading even without unsigned underflow: A, LF -> A, CR, LF; prefix1 ->0,
 # while one original token is fully present in the output prefix.
 counterexample={'invented_tokens':[65,10],'invented_output':[65,13,10],'invented_native_count':1,'invented_total_adjustment':1,'uint32_subtraction':0,'completed_input_tokens_in_output_prefix':1}
 return {'schema':'tw10-r72-conditional-adjustment-byte-expansion-and-count-units','source_git_blobs':{k:v[1]for k,v in PINS.items()},'available_decoded_graph_nodes':len(nodes&rows.keys()),'undecoded_graph_nodes':sorted(nodes-rows.keys()),'graph_nodes':len(nodes),'graph_edges':len(edges),'qualified_structural_paths':paths,'adjustment_increment_rva':0x4C653,'conditional_compared_octet':10,'conditional_inserted_octet':13,'post_store_threshold':1024,'post_store_conditional_max_chunk_units':1025,'threshold_is_signed_jl_and_input_bound_is_unsigned_jae':True,'conditional_initialization':'XOR EDI,EDI then frame[-8]/[-16]<-EDI; later calls/frame/aliases remain opaque','conditional_adjustment_unit':'one increment for each selected byte10 expansion; frame[-16] counts these increments only under valid stable frame/memory and realized path premises','conditional_return_count_expression':'(frame[-8]-frame[-16]) modulo2^32; full transfer and all counted insertions assumptions needed for source-unit identity','count_consumer_contract':consumers,'invented_trace_threshold_comparisons':traces,'invented_boundary_cases':boundary,'invented_partial_write_prefixes':partial,'invented_partial_write_counterexample':counterexample,'all_numerical_tokens_and_counts_are_invented':True,'unknown_calls_and_frame_alias_barriers_preserved':True,**{k:False for k in NEGATIVE},'stage_a_families':'PARTIAL/OPEN','next':'R73 retained-first mode/direct-count path predicate gaps and exact remaining11 graph-node operand census; keep actual native IO, frame aliases and disk persistence OPEN.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--verify',type=Path);a=p.parse_args();d=analyze({k:(BASE/n).read_bytes()for k,(n,_)in PINS.items()})
 if a.verify:need(d==json.loads(a.verify.read_bytes()),'exact canonical replay');print('TW10_R72_ADJUSTMENT_AND_CONDITIONAL_COUNT_UNITS=PASS; NATIVE_IO=OPEN')
 else:print(json.dumps(d,sort_keys=True,indent=2))
if __name__=='__main__':main()
