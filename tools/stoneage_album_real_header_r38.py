"""Read only RAR4 original file headers: possible same-carrier REAL for R37 album images.

No original pixel/compressed REAL payload is read or published.
Preserved community mixed 2.5 bundle is not authenticated official client.
"""
import argparse
import json
from pathlib import Path
import rarfile
from tools.stoneage_native_album_source_r36 import SparseParts, fetcher_factory, PREFIX, need
from tools.stoneage_album_adrn_material_r37 import read_all, check

TARGET=PREFIX+'data/real_15.bin'
KEYS=('28001','28002','28003')
MAX_HEADERS=10000

def selected_expected(report):
 need(report['schema']=='stoneage.preserved_album_adrn_material.r37','source report schema')
 rows=[]
 for k in KEYS:
  need(len(report['album_joins'][k]['adrn_alias_rows'])==1,'one original alias')
  row=report['album_joins'][k]['adrn_alias_rows'][0]
  need(row['logical_alias']==int(k),'original logical alias')
  need(row['size']>0 and row['adder']>=0,'positive real byte range')
  rows.append({'logical_alias':int(k),'physical_bitmapno':row['bitmapno'],'offset':row['adder'],
   'size':row['size'],'end_exclusive':row['adder']+row['size'],'adrn_record_sha256':row['record_sha256']})
 return rows

def classify_header(info):
 name=info.filename.replace('\\','/')
 return {'name':name,'bytes':info.file_size,'compressed_bytes':info.compress_size,
  'flags':info.flags,'compression_method':info.compress_type,'header_offset':info.header_offset,
  'compressed_data_offset':info.data_offset,'original_crc32':info.CRC,
  'exact_expected_member_name':name==TARGET,'is_independent_member':info.flags&(1|2|4|16)==0}

def scan(reader,required,context):
 candidates=[];headers=0;finished=False
 def visitor(info):
  nonlocal headers
  headers+=1
  need(headers<=MAX_HEADERS,'finite10k original archive header limit')
  if info.type!=rarfile.RAR_BLOCK_FILE:return
  name=info.filename.replace('\\','/')
  if name==TARGET:
   candidates.append(classify_header(info))
 # Fully walk the RAR4 header directory; SparseParts skips payloads.
 rarfile.RarFile(reader,info_callback=visitor,errors='strict')
 finished=True
 context['headers_visited']=headers
 context['candidates']=candidates
 context['header_walk_completed']=finished
 context['actual_range_bytes']=reader.fetched
 context['range_requests']=len(reader.receipts)
 context['range_receipts']=reader.receipts
 for entry in candidates:
  entry['all_selected_offsets_fit_file_size']=all(row['end_exclusive']<=entry['bytes'] for row in required)
  entry['bitmap_ranges_covered_if_same_resource_layout']=entry['all_selected_offsets_fit_file_size']
 return candidates

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 material,positive,failed,old=read_all();check(material,positive,failed,old)
 wanted=selected_expected(material)
 result={'schema':'stoneage.album_real_header_qualification.r38','status':'NOT_QUALIFIED',
  'source_scope':'COMMUNITY_MIXED25_PRESERVED_CLIENT_SUBTREE_NOT_OFFICIAL_BUILD',
  'source_branch_r37':'76c605493cb2505c64f8e01a1b63caf49dfbabd7',
  'expected_original_RAR_member':TARGET,'required_adrn_ranges':wanted,
  'original_REAL_payload_read':False,'raw_REAL_or_pixels_published':False,
  'original_executable_executed':False,'official_build_authenticated':False,'new_official_clients':0,
  'full_legacy_bundle_reacquired':False}
 context={}
 try:
  fetch,pages=fetcher_factory();reader=SparseParts(fetch)
  entries=scan(reader,wanted,context);context['public_pages']=pages
  if len(entries)==0:result['status']='REAL_MEMBER_NOT_FOUND_IN_SCANNED_SOURCE'
  elif len(entries)==1:result['status']='SINGLE_REAL_HEADER_PRESENT_PIXELS_NOT_ACQUIRED'
  else:result['status']='MULTIPLE_REAL_HEADERS_AMBIGUOUS'
 except Exception as e:
  result['error']={'type':type(e).__name__,'message':str(e)[:400]}
  if 'reader' in locals():
   context['actual_range_bytes']=reader.fetched
   context['range_requests']=len(reader.receipts)
   context['range_receipts']=reader.receipts
  result['status']='HEADER_SCAN_INCOMPLETE'
 if context:result['receipt']=context
 raw=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(raw,encoding='utf-8')
 print('R38_REAL_HEADER_REPORT_BEGIN');print(raw,end='');print('R38_REAL_HEADER_REPORT_END')
if __name__=='__main__':main()
