"""Finite original-program album table; no original executable in public Git.

Both raw programs must match the pre-existing full hashes before inspection.
The permanent report replays factual table values and semantic instruction
metadata, not game execution or an authenticated official release.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

from tools.stoneage_native_album_source_r36 import TARGETS, pe_summary
from tools.stoneage_album_material_r35 import REPORT as OLD_REPORT, REPORT_SHA as OLD_SHA

ROOT=Path(__file__).resolve().parents[1]
SOURCE='research/recovered/STONEAGE-NATIVE-ALBUM-PROGRAM-SOURCE-R36.json'
REPORT='research/recovered/STONEAGE-NATIVE-ALBUM-MATERIAL-R36.json'
SOURCE_SHA='e10d966b4d45d691dd59020f88d87ebc553e303d20f8044bb9e9cc83d76c9237'
REPORT_SHA='1a79802705c88d94fb755903ddee3a3da5985e302f822e9ba0064af8034595e0'
TABLE_OFFSET=490136
TABLE_VA=0x477a98
COUNT=281
STRIDE=28
TABLE_SHA='fedb572b938ddb63cf6f574831290ed80201dd8e13ab8f91aacba4750b3aeb90'
WINDOWS={
 'compiled_table_bound':(0x42df13,0x42df1d),
 'local_slot_initialization_bound':(0x42dff3,0x42e005),
 'local_224_by_80_reader':(0x42e1ad,0x42e1c8),
 'seen_name_and_flag_only':(0x42e3a2,0x42e40e),
 'photograph_name_and_table_face':(0x4318db,0x43199e),
}

def sha(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def pin(raw):return {'bytes':len(raw),'sha256':sha(raw),'git_blob':blob(raw)}
def need(ok,msg):
 if not ok:raise ValueError(msg)

def at_va(raw,pe,va,size):
 rva=va-pe['image_base']
 for section in pe['sections']:
  delta=rva-section['rva']
  if 0<=delta and delta+size<=section['raw_bytes']:
   offset=section['raw_offset']+delta;return offset,raw[offset:offset+size]
 raise ValueError('VA is not wholly backed by original file bytes')

def parse_table(raw,start,count):
 need(count==COUNT and start>=0 and start+count*STRIDE<=len(raw),'compiled finite table extent')
 rows=[]
 for i in range(count):
  offset=start+i*STRIDE;record=raw[offset:offset+STRIDE]
  slot=struct.unpack_from('<i',record)[0];face=struct.unpack_from('<i',record,24)[0]
  field=record[4:21];need(b'\0' in field,'terminated native table name')
  token=field.split(b'\0')[0];name=token.decode('gbk','strict')
  need(field==token+b'\0'*(17-len(token)) and record[21:24]==b'\0'*3,'actual zero-filled table name/padding')
  need(slot in range(224) or slot==-1,'native album slot namespace')
  need((slot==-1 and name=='无' and face==0) or (slot>=0 and face>0),'native placeholder or populated row')
  rows.append({'table_index':i,'album_slot':slot,'name_gbk':name,'table_face_value':face,
   'source_file_offset':offset,'source_va':TABLE_VA+i*STRIDE,
   'record_sha256':sha(record),'name_field_sha256':sha(field)})
 return rows

def join_observed(rows,old):
 byslot={r['album_slot']:r for r in rows if r['album_slot']>=0};result=[]
 for r in old['album_material']['observed_name_rows']:
  native=byslot[r['album_slot']]
  need(r['observed_name_gbk']==native['name_gbk'],'original saved name conflicts with native program table')
  result.append({'local_block_ordinal':r['local_block_ordinal'],'album_slot':r['album_slot'],
   'source_record_offset':r['source_record_offset'],'native_table_index':native['table_index'],
   'name_gbk':native['name_gbk'],'native_table_face_value':native['table_face_value'],
   'saved_face_or_stat_fields_used':False})
 return result

def build(directory):
 import capstone
 need(capstone.__version__=='5.0.3','pinned static instruction decoder')
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
 programs=[];table_raws=[];reference=None;rowset=None
 for name,identity in TARGETS.items():
  raw=(directory/name).read_bytes();need((len(raw),sha(raw))==identity,'complete original program identity')
  pe=pe_summary(raw);offset,table=at_va(raw,pe,TABLE_VA,COUNT*STRIDE)
  need(offset==TABLE_OFFSET and sha(table)==TABLE_SHA,'original native table anchor')
  rows=parse_table(raw,offset,COUNT);windows={}
  for label,(start,end) in WINDOWS.items():
   pos,data=at_va(raw,pe,start,end-start);instructions=list(cs.disasm(data,start))
   need(sum(i.size for i in instructions)==len(data),'complete bounded instruction decode')
   windows[label]={'start_va':start,'end_va_exclusive':end,'file_offset':pos,
    'bytes':len(data),'sha256':sha(data),
    'instructions':[{'va':i.address,'size':i.size,'mnemonic':i.mnemonic,'operands':i.op_str} for i in instructions]}
  if reference is not None:need(rows==rowset and windows==reference,'two native variant table/code equality')
  else:rowset=rows;reference=windows
  table_raws.append(table);programs.append({'name':name,**pin(raw),'pe':pe,'table_sha256':sha(table)})
 old_raw=(ROOT/OLD_REPORT).read_bytes();need(sha(old_raw)==OLD_SHA,'prior observed name report identity');old=json.loads(old_raw)
 a=(directory/'sa_2903.exe').read_bytes();b=(directory/'sa_2903网通.exe').read_bytes()
 differences=[i for i in range(len(a)) if a[i]!=b[i]]
 return {'schema':'stoneage.native_album_table_material.r36',
  'source_scope':'EXISTING_MIXED25_PRESERVED_CLIENT_SUBTREE_NOT_AUTHENTICATED_OFFICIAL_BUILD',
  'source_report':pin((ROOT/SOURCE).read_bytes()),'programs':programs,
  'table':{'file_offset':TABLE_OFFSET,'va':TABLE_VA,'row_bytes':STRIDE,'compiled_rows':COUNT,
   'table_bytes':COUNT*STRIDE,'sha256':TABLE_SHA,'populated_rows':224,'placeholder_rows':57,
   'unique_populated_slots':224,'slot_min':0,'slot_max':223,'rows':rowset},
  'static_code_windows':reference,'instruction_decoder':'capstone5.0.3/i386',
  'variant_comparison':{'both_full_program_hashes_preserved':True,'table_and_selected_code_windows_equal':True,
   'differing_program_byte_offsets':differences,'different_bytes_interpreted':False},
  'prior_saved_name_report':pin(old_raw),'saved_names_to_native_table':join_observed(rowset,old),
  'boundaries':{'original_program_executed':False,'original_binary_or_ciphertext_published':False,
   'local_account_keys_decoded':False,'saved_free_names_or_random_face_stats_used':False,
   'saved_file_created_by_these_programs_proven':False,'official_build_authenticated':False,
   'physical_bitmap_or_spr_binding_proven':False,'server_species_master_recovered':False,
   'new_official_clients':0,'official_tw10_entities_added':0,'overall_restoration_percent':None,
   'stage_a':'7_PARTIAL_2_OPEN','stage_b_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'},
  'next':'PRESERVED_CLIENT_ALBUM_LOGICAL_RESOURCE_BINDING_37'}

def replay(d):
 need(d['schema']=='stoneage.native_album_table_material.r36','native material schema')
 need(d['source_scope']=='EXISTING_MIXED25_PRESERVED_CLIENT_SUBTREE_NOT_AUTHENTICATED_OFFICIAL_BUILD','source version promotion')
 source_raw=(ROOT/SOURCE).read_bytes();need(sha(source_raw)==SOURCE_SHA and d['source_report']==pin(source_raw),'exact source report')
 source=json.loads(source_raw);need(source['status']=='TWO_ORIGINAL_COMPLETE_PROGRAM_HASHES_MATCH','actual source acquisition status')
 need({r['name']:(r['bytes'],r['sha256']) for r in source['receipt']['two_original_members']}==TARGETS,'both original identities')
 need(source['receipt']['actual_range_bytes']==7995392 and source['receipt']['range_requests']==122,'actual finite source budget')
 receipts=source['receipt']['range_receipts'];need(len(receipts)==122 and sum(r['bytes'] for r in receipts)==7995392,'range accounting')
 need(source['original_program_executed'] is False and source['whole_bundle_reacquired'] is False and source['new_official_clients']==0,'source overclaim')
 need({r['name']:(r['bytes'],r['sha256']) for r in d['programs']}==TARGETS,'native full program identities')
 table=d['table'];need((table['file_offset'],table['va'],table['row_bytes'],table['compiled_rows'],table['table_bytes'])==(TABLE_OFFSET,TABLE_VA,28,281,7868),'table boundary namespace')
 rows=table['rows'];need(len(rows)==281,'all rows including holes required');rebuilt=[]
 for i,r in enumerate(rows):
  need((r['table_index'],r['source_file_offset'],r['source_va'])==(i,TABLE_OFFSET+i*28,TABLE_VA+i*28),'native row location')
  token=r['name_gbk'].encode('gbk');need(0<len(token)<17,'native name length')
  field=token+b'\0'*(17-len(token));record=struct.pack('<i',r['album_slot'])+field+b'\0'*3+struct.pack('<i',r['table_face_value'])
  need(r['name_field_sha256']==sha(field) and r['record_sha256']==sha(record),'native named-value metadata integrity')
  need((r['album_slot']==-1 and r['name_gbk']=='无' and r['table_face_value']==0) or (0<=r['album_slot']<224 and r['table_face_value']>0),'placeholder is not table terminator')
  rebuilt.append(record)
 need(sha(b''.join(rebuilt))==table['sha256']==TABLE_SHA,'all native table row SHA')
 populated=[r for r in rows if r['album_slot']>=0]
 need(len(populated)==224 and {r['album_slot'] for r in populated}==set(range(224)),'224 named slot coverage distinct from281 rows')
 need(len({r['name_gbk'] for r in populated})==224 and len({r['table_face_value'] for r in populated})==224,'native name/number uniqueness')
 need((table['populated_rows'],table['placeholder_rows'],table['unique_populated_slots'],table['slot_min'],table['slot_max'])==(224,57,224,0,223),'native table counts')
 windows=d['static_code_windows'];need(set(windows)==set(WINDOWS),'finite selected code windows')
 for label,(start,end) in WINDOWS.items():
  w=windows[label];need((w['start_va'],w['end_va_exclusive'],w['bytes'])==(start,end,end-start),'code window boundary')
  cursor=start
  for i in w['instructions']:need(i['va']==cursor and i['size']>0,'instruction location');cursor+=i['size']
  need(cursor==end,'instruction window extent')
 def has(label,mnemonic,operands):return any(i['mnemonic']==mnemonic and i['operands']==operands for i in windows[label]['instructions'])
 need(has('compiled_table_bound','mov','dword ptr [0x2aff9bc], 0x119'),'compiled281 bound')
 need(has('seen_name_and_flag_only','imul','ecx, ecx, 0x1c') and has('seen_name_and_flag_only','cmp','esi, -1'),'28B stride and internal holes')
 need(has('seen_name_and_flag_only','mov','dword ptr [edx], 1'),'original seen flag1')
 need(has('photograph_name_and_table_face','mov','dword ptr [edi + 0x2ad3bd4], 2') and has('photograph_name_and_table_face','mov','eax, dword ptr [eax + 0x477ab0]') and has('photograph_name_and_table_face','mov','dword ptr [edi + 0x2ad3bac], eax'),'original photo flag2/table face transfer')
 need(has('local_224_by_80_reader','mov','esi, 0xe0') and has('local_224_by_80_reader','push','0x50'),'original saved-slot count and stride')
 old_raw=(ROOT/OLD_REPORT).read_bytes();need(sha(old_raw)==OLD_SHA and d['prior_saved_name_report']==pin(old_raw),'prior report preservation')
 joined=join_observed(rows,json.loads(old_raw));need(d['saved_names_to_native_table']==joined and len(joined)==148 and len({r['album_slot'] for r in joined})==76,'148 actual names to76 native slots')
 v=d['variant_comparison'];need(v=={'both_full_program_hashes_preserved':True,'table_and_selected_code_windows_equal':True,'differing_program_byte_offsets':[544588,544589],'different_bytes_interpreted':False},'do not flatten variant identities')
 b=d['boundaries'];need(all(b[k] is False for k in ['original_program_executed','original_binary_or_ciphertext_published','local_account_keys_decoded','saved_free_names_or_random_face_stats_used','saved_file_created_by_these_programs_proven','official_build_authenticated','physical_bitmap_or_spr_binding_proven','server_species_master_recovered']),'historical/runtime boundary')
 need(b['new_official_clients']==b['official_tw10_entities_added']==0 and b['overall_restoration_percent'] is None,'no invented roster/progress')
 need((b['stage_a'],b['stage_b_wiki'],b['r79'])==('7_PARTIAL_2_OPEN','GATED','PAUSED_NON_BLOCKING'),'project gate preservation')

def independent_original(directory,d):
 import ctypes as c
 class Native(c.LittleEndianStructure):
  _fields_=[('slot',c.c_int32),('name',c.c_ubyte*17),('face',c.c_int32)]
 need(c.sizeof(Native)==28 and Native.face.offset==24,'independent C ABI')
 for name,identity in TARGETS.items():
  raw=(directory/name).read_bytes();need((len(raw),sha(raw))==identity,'independent original identity')
  anchor=struct.pack('<i',0)+'乌力'.encode('gbk')+b'\0'*16+struct.pack('<i',28001)
  need(raw.count(anchor)==1,'independent unique full row anchor');start=raw.index(anchor)
  observed=[]
  for i in range(281):
   item=Native.from_buffer_copy(raw,start+i*c.sizeof(Native));observed.append((item.slot,bytes(item.name).split(b'\0')[0].decode('gbk'),item.face))
  need(observed==[(r['album_slot'],r['name_gbk'],r['table_face_value']) for r in d['table']['rows']],'independent all281 rows and holes')
 print('R36_INDEPENDENT_CTYPES_BOTH_PROGRAMS_ALL281_ROWS=PASS')

def main():
 p=argparse.ArgumentParser();p.add_argument('--members',type=Path);p.add_argument('--write',action='store_true');p.add_argument('--independent-original',type=Path);a=p.parse_args()
 if a.write:
  d=build(a.members);replay(d);(ROOT/REPORT).write_text(json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 else:
  raw=(ROOT/REPORT).read_bytes();need(sha(raw)==REPORT_SHA,'exact permanent native metadata report');d=json.loads(raw);replay(d)
 if a.independent_original:independent_original(a.independent_original,d)
 print('R36_NATIVE281_ROWS_224_SLOTS_148_SAVED_NAME_JOINS=PASS')

if __name__=='__main__':main()
