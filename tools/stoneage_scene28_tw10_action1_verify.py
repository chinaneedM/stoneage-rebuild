#!/usr/bin/env python3
"""SCENE28: exact original TW1 pet action-1 source audit; no pixels leave private source.

Offline --check checks published source receipts and R40/SCENE26 lineage.
--source-dir opt-in additionally verifies original full files, raw action sequences,
and all 48 original RD pixel-index SHA256s. This second path is NOT run in CI.
"""
from __future__ import annotations
import argparse, hashlib, json, re, struct
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PUBLISHED = ROOT / 'research/recovered/STONEAGE-SCENE28-TW10-ACTION1-PIXELS-R1.json'
PREVIOUS = ROOT / 'research/recovered/STONEAGE-SCENE26-PET-ACTION1-DERIVED-R1.json'
PARENT_SCENE26_BLOB = '5e63345a74271ada339b37032e665349d52ec40c'
EXPECTED_SPR_SEGMENTS = {
 100250:'eb1a87cd4cc8e3b409990783c7bcc3bc463acab4cac7d2d961127d899da047ef',
 100251:'073278ba6ae1e623eea969deef11f99fd9be8b995af332506e830bd046c86764',
 100252:'eeb2ec4546277c2acdf1b43fff7967c4c0fe5ac5c019bb7d68a901e134691b0a'}
EXPECTED_FILES = {
 'spr_1.bin':(2889630,'53d5b2d40453a30fd1569637ebf0db7b3010542b00970ec83af0295a3b3ae31a'),
 'spradrn_1.bin':(5568,'275b64ff55667aec633a7e82e09d65c84141380521f0f2e64c9a28e0d3aa6c25'),
 'adrn_1.bin':(10079680,'47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8'),
 'real_1.bin':(315842228,'408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13'),
 'Palet_0.sap':(708,'89709d906bbd9cd9f5c2b8e0bd993e2897a1c9136ada2e211109983bb3b06cbf'),
 'Palet_1.sap':(708,'32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0')}
ZIP_SHA='3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24'


def need(ok, message):
 if not ok: raise ValueError(message)
def sha(b): return hashlib.sha256(b).hexdigest()
def git_blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def full_sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def load_prior(root=ROOT):
 raw=(root/'research/recovered/STONEAGE-SCENE26-PET-ACTION1-DERIVED-R1.json').read_bytes()
 need(git_blob(raw)==PARENT_SCENE26_BLOB,'SCENE26 archived Git blob changed')
 return json.loads(raw)

def published_gate(r, old):
 need(r['schema']=='stoneage.scene28.tw10_actually_decoded_pet_action1.r1','SCENE28 schema')
 need(r['historical_source_scope']=='ACCEPTED_TW_WAEI_JSS_1_0_RETAIL_REDUMP_104630_NOT_A_RUNTIME_GAME_SESSION','source identity')
 zipinfo=r['original_private_zip']
 need(zipinfo['bytes']==372626292 and zipinfo['sha256']==ZIP_SHA,'original private zip identity')
 for name,(size,digest) in EXPECTED_FILES.items():
  item=r['exact_original_source_files'][name]
  need(item=={'bytes':size,'sha256':digest},'original full-file receipt mismatch: '+name)
 groups=r['same_segment_as_R40_preserved_mixed25']
 need(len(groups)==3 and [x['graphic']for x in groups]==list(EXPECTED_SPR_SEGMENTS),'original SPR group ordering')
 for i,g in enumerate(groups):
  need(g['tw10_source_group_index']==240+i and g['whole_spr_segment_sha256']==EXPECTED_SPR_SEGMENTS[g['graphic']],'cross-build source SPR segment digest conflict')
 p=r['reproduces_scene26_released_frame_sequences']
 need(p['source_derived_Git_blob']==PARENT_SCENE26_BLOB and p['action_code']==1,'SCENE26 binding')
 need([p[k] for k in ('source_directions','source_sequences','frame_positions','distinct_bitmap_numbers')]==[8,24,80,48],'action1 counts')
 need(p['per_group_frame_positions']==[32,32,16] and p['every_source_duration_word']==100 and p['every_frame_sound_field_zero'] is True,'action1 duration and sound literal fact')
 need(p['action_semantics_or_duration_units_proven'] is False,'unproven action semantics promoted')
 need(old['summary']=={'group_count':3,'direction_sequences':24,'frame_occurrences':80,'distinct_bitmap_numbers':48,'zero_sound_field_occurrences':80},'SCENE26 public summary no longer exact')
 # Recheck every direction against original SCENE26 immutable source-derived index.
 ids=[]
 for i,g in enumerate(old['groups']):
  need(g['spr_no']==groups[i]['graphic'] and g['group_index']==groups[i]['tw10_source_group_index'] and g['full_segment_sha256']==groups[i]['whole_spr_segment_sha256'],'cross-source group mismatch')
  need(len(g['directions'])==8 and [x['direction']for x in g['directions']]==list(range(8)),'prior original direction missing')
  for a in g['directions']:
   need(a['duration_word']==100 and all(f[3]==0 for f in a['frames']),'frame control field mismatch')
   ids.extend(f[0]for f in a['frames'])
 need(len(ids)==80 and len(set(ids))==48,'prior frames or duplicate positions lost')
 receipt=r['TW10_actual_adrn_real_pixel_receipts']
 need(len(receipt)==48 and [x['bitmapno']for x in receipt]==sorted(set(ids)),'source bitmap set has missing/duplicate ids')
 offsetsize=EXPECTED_FILES['real_1.bin'][0]
 for x in receipt:
  need(all(type(x[k])is int for k in ('bitmapno','source_adrn_index','offset','size','width','height','flag','visible_index_pixels')),'actual RD numeric fields')
  need(x['source_adrn_index']>=0 and 0<=x['offset']<offsetsize and 16<=x['size']<=1000000 and x['offset']+x['size']<=offsetsize,'RD file range invalid')
  need(0<x['width']<=1024 and 0<x['height']<=1024 and 0<x['visible_index_pixels']<=x['width']*x['height'] and x['flag']==1,'source geometry/flag mismatch')
  need(all(re.fullmatch('[0-9a-f]{64}',x[k]) for k in ('record_sha256','RD_sha256','index_pixels_sha256')),'hash format')
 a=r['actual_source_replay_results']
 need(a['original_bitmap_records_unique']==a['actual_original_RD_blocks_read']==a['RD_decode_count']==a['RD_decode_flag1_count']==a['decoded_pixels_independently_compared']==a['distinct_source_bitmap_ids']==48,'actual direct pixel source acceptance')
 need(a['sum_visible_index_pixels_across_unique_bitmaps']==sum(x['visible_index_pixels']for x in receipt)==53932,'pixel occupancy total')
 need(a['source_original_bitmaps_viewed_as_contact_sheet'] is True and a['embedded_candidate_pngs_verified']==96 and a['private_interactive_browser_controls_tested'] is True,'private visual witness scope')
 need(a['private_browser_page_errors']==0 and a['private_web_browser_method'].startswith('Chromium page.set_content'),'actual observer browser status')
 priv=r['private_observation_artifact']
 need(priv['sha256']=='f707d196acb6c449e2b6b11345a02db36ac6726131ce51f9a93587b32c3ad492' and priv['bytes']==347996 and priv['saved_to_private_library'] is True,'private artifact identity/persistence')
 limits=r['evidence_limits']
 for key in ('source_file_original_bytes_published','original_sprite_pixels_or_palettes_in_public_repo','original_game_client_ran_in_this_work_unit','original_game_world_entered','actual_game_frame_rate_verified','historical_action1_semantic_name_verified','official_pet_species_names_authenticated','historical_scene_palette_selection_verified','same_deployed_build_as_R40_mixed25_proven','original_server_state_or_event_verified'):
  need(limits[key] is False,'unproven original game claim: '+key)
 need(limits['overall_restoration_percentage'] is None and limits['stage_a']=='7_PARTIAL_2_OPEN' and limits['stage_b_wiki']=='GATED' and limits['r79']=='PAUSED_NON_BLOCKING','restoration stage not promoted')
 return True

def get_count(data, pos, ctrl, base):
 family=ctrl&0xf0
 if family==base:return ctrl&15,pos
 if family==base+16:
  need(pos<len(data),'short 12bit RLE');return (ctrl&15)*256+data[pos],pos+1
 if family==base+32:
  need(pos+1<len(data),'short 20bit RLE');return ((ctrl&15)<<16)+(data[pos]<<8)+data[pos+1],pos+2
 raise ValueError('invalid legacy RLE instruction')

def rd_index_pixels(rd):
 need(len(rd)>=16 and rd[:2]==b'RD','RD header missing')
 w,h=struct.unpack_from('<ii',rd,4);flag=rd[2]
 need(0<w<=1024 and 0<h<=1024 and flag in (0,1),'unverified source geometry or RLE')
 payload=memoryview(rd)[16:];out=bytearray();pos=0
 if flag==0:
  need(len(payload)>=w*h,'raw RD short');return (w,h,bytes(payload[:w*h]),flag)
 while pos<len(payload):
  ctrl=payload[pos];pos+=1;family=ctrl&0xf0
  if family in (0x00,0x10,0x20):
   n,pos=get_count(payload,pos,ctrl,0x00);need(pos+n<=len(payload),'literal too long');out.extend(payload[pos:pos+n]);pos+=n
  elif family in (0x80,0x90,0xa0):
   need(pos<len(payload),'missing repeat pixel');b=payload[pos];pos+=1;n,pos=get_count(payload,pos,ctrl,0x80);out.extend(bytes([b])*n)
  elif family in (0xc0,0xd0,0xe0):
   n,pos=get_count(payload,pos,ctrl,0xc0);out.extend(b'\0'*n)
  else:raise ValueError('invalid RD control family')
  need(len(out)<=w*h,'pixel decode overflow')
 need(len(out)==w*h,'pixel count short')
 return w,h,bytes(out),flag

def source_gate(directory, report, old, private_zip=None):
 directory=Path(directory)
 if private_zip is not None:
  p=Path(private_zip);need(p.stat().st_size==372626292 and full_sha(p)==ZIP_SHA,'private original zip mismatch')
 for name,(size,digest)in EXPECTED_FILES.items():
  p=directory/name
  need(p.is_file() and not p.is_symlink() and p.stat().st_size==size and full_sha(p)==digest,'original file identity: '+name)
 index=(directory/'spradrn_1.bin').read_bytes();spr=(directory/'spr_1.bin').read_bytes()
 need(len(index)%12==0,'original SPR index rows')
 rows=[struct.unpack_from('<IIHH',index,i*12)for i in range(len(index)//12)]
 offsets=sorted({x[1]for x in rows});end={n:offsets[i+1]if i+1<len(offsets)else len(spr)for i,n in enumerate(offsets)}
 for g in old['groups']:
  key=g['spr_no'];matches=[(i,x)for i,x in enumerate(rows)if x[0]==key]
  need(len(matches)==1,'SPR group not uniquely identified');i,(n,start,count,unused)=matches[0]
  need(i==g['group_index'] and count==56 and sha(spr[start:end[start]])==EXPECTED_SPR_SEGMENTS[key],'original SPR segment no longer equal')
  cursor=start;actual=[]
  for ai in range(count):
   begin=cursor;direction,action,duration,frames=struct.unpack_from('<HHII',spr,cursor);cursor+=12
   need(0<frames<=112 and cursor+10*frames<=end[start],'original source frame range')
   fr=[list(struct.unpack_from('<IhhH',spr,cursor+j*10))for j in range(frames)];cursor+=frames*10
   if action==1:actual.append((direction,ai,begin,cursor,duration,fr))
  need(cursor==end[start] and len(actual)==8,'whole exact source SPR parse')
  for a,b in zip(sorted(actual),g['directions']):
   direction,ai,begin,e,duration,fr=a
   need((direction,ai,begin,e,duration,fr)==(b['direction'],b['source_animation_index'],b['header_offset'],b['end_offset'],b['duration_word'],b['frames']),'actual TW1 source action1 sequence mismatch')
 needed={x['bitmapno']for x in report['TW10_actual_adrn_real_pixel_receipts']}
 adrn=(directory/'adrn_1.bin').read_bytes(); matches={n:[]for n in needed}
 for i in range(len(adrn)//80):
  a=adrn[i*80:i*80+80];no=struct.unpack_from('<I',a)[0]
  if no in matches:matches[no].append((i,a))
 need(all(len(v)==1 for v in matches.values()),'source ADRN bitmap missing/ambiguous')
 with (directory/'real_1.bin').open('rb')as f:
  for item in report['TW10_actual_adrn_real_pixel_receipts']:
   i,a=matches[item['bitmapno']][0];no,off,sz,x,y,w,h=struct.unpack_from('<7i',a)
   need((i,off,sz,w,h)==tuple(item[k] for k in ('source_adrn_index','offset','size','width','height')),'source ADRN index/body changed')
   need(sha(a)==item['record_sha256'],'actual index source digest changed')
   f.seek(off);rd=f.read(sz)
   need(len(rd)==sz and sha(rd)==item['RD_sha256'],'actual RD source digest changed')
   rw,rh,px,flag=rd_index_pixels(rd)
   need((rw,rh,flag)==(w,h,item['flag']) and sha(px)==item['index_pixels_sha256'] and sum(v!=0 for v in px)==item['visible_index_pixels'],'original indexed pixels differ')
 return 48

def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--private-original-zip',type=Path);args=p.parse_args()
 need(args.check or args.source_dir is not None,'--check or --source-dir required')
 r=json.loads(PUBLISHED.read_text(encoding='utf-8'));old=load_prior();published_gate(r,old)
 count=source_gate(args.source_dir,r,old,args.private_original_zip)if args.source_dir else 0
 print(json.dumps({'schema':'stoneage.scene28.public_source_guard.result.r1','public_metadata_valid':True,'original_source_replayed_now':bool(args.source_dir),'independent_original_RD_blocks_recomputed':count,'original_game_world_entered':False}))
if __name__=='__main__':main()