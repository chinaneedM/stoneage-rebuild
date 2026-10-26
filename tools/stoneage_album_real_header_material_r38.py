"""R38 original REAL header-only acceptance; rejects invented pixel data."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'research/recovered/STONEAGE-ALBUM-REAL-HEADER-SOURCE-R38.json'
MAT=ROOT/'research/recovered/STONEAGE-ALBUM-REAL-HEADER-MATERIAL-R38.json'
R37=ROOT/'research/recovered/STONEAGE-PRESERVED-ALBUM-ALIAS-R37.json'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def validate(m,s,old):
 def need(ok,message):
  if not ok:raise ValueError(message)
 need(m['schema']=='stoneage.album_real_header_material.r38','schema')
 need(s['status']=='SINGLE_REAL_HEADER_PRESENT_PIXELS_NOT_ACQUIRED','source status')
 need(m['source']['run']==40422947999 and m['source']['job']==121921573780,'source job')
 need(m['source']['head']=='1c58edffe3a299466373f1c5d4e3713a4ac751ac','source commit')
 need(s['original_REAL_payload_read'] is False and s['raw_REAL_or_pixels_published'] is False,'source no pixels')
 need(s['official_build_authenticated'] is False,'not authenticated official')
 need(m['archive_header_survey']['source_member_candidates']==s['receipt']['candidates'],'original header rows')
 need(s['receipt']['headers_visited']==m['archive_header_survey']['headers_visited']==7954,'full header count')
 need(s['receipt']['header_walk_completed'] is True,'full directory scan')
 need(s['receipt']['range_requests']==m['archive_header_survey']['range_requests']==184,'range requests')
 need(s['receipt']['actual_range_bytes']==m['archive_header_survey']['actual_range_bytes']==12013836,'range budget actual')
 need(m['archive_header_survey']['actual_range_bytes']<m['archive_header_survey']['reader_budget_bytes']==16777216,'range budget')
 entries=s['receipt']['candidates']
 need(len(entries)==1,'one real member header')
 x=entries[0]
 need(x['name'].endswith('/stoneage2.5/data/real_15.bin') and x['exact_expected_member_name'] is True,'same preserved source')
 need(x['bytes']==763908374 and x['compressed_bytes']==338458942 and x['compression_method']==53,'bounded original REAL header')
 need(x['flags']==33472 and x['original_crc32']==3180047245,'original CRC/flags')
 need(x['compressed_bytes']>m['archive_header_survey']['reader_budget_bytes'],'not seekable within total compressed source budget')
 need(x['all_selected_offsets_fit_file_size'] is True,'all original offsets within declared REAL')
 need(len(s['required_adrn_ranges'])==len(m['three_adrn_byte_ranges'])==3,'three expected ranges')
 need(m['three_adrn_byte_ranges']==s['required_adrn_ranges'],'real offsets verbatim')
 for alias,p in zip(('28001','28002','28003'),m['three_adrn_byte_ranges']):
  need(alias in old['album_joins'] and len(old['album_joins'][alias]['adrn_alias_rows'])==1,'old alias')
  r=old['album_joins'][alias]['adrn_alias_rows'][0]
  need(p['logical_alias']==int(alias) and p['physical_bitmapno']==r['bitmapno'],'same R37 face')
  need(p['offset']==r['adder'] and p['size']==r['size'] and p['end_exclusive']==r['adder']+r['size'],'exact original offsets')
  need(p['adrn_record_sha256']==r['record_sha256'],'original source record SHA')
  need(p['end_exclusive']<=x['bytes'],'offset bound')
 need(m['qualification']['real_payload_read'] is False and m['qualification']['actual_RD_headers_verified'] is False,'no REAL source content')
 need(m['qualification']['official_same_build_authentication'] is False and m['qualification']['overall_percent'] is None,'no certification')
 return {'original_header_count':7954,'same_carrier_real_member_found':True,'three_offsets_within_declared_length':True,'pixels_verified':False}
if __name__=='__main__':print(json.dumps(validate(load(MAT),load(SRC),load(R37)),sort_keys=True))
