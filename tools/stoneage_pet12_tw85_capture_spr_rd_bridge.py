#!/usr/bin/env python3
"""PET12: verify six capture-key graphic candidates in archived same-carrier TW85 SPR/RD evidence.

Source-limited public metadata only. Rebuilds the six complete SPR segments from
archived ORIGINAL-byte-derived R28 records, then joins the bounded R29 actual-RD
index. No original source pixels, server execution, FPS or species identities.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'research/recovered'
R2B3 = BASE / 'STONEAGE-STAGE-A-WORLD37-R2B3-CAPTURE-ORIGINAL-SPR-BRIDGE-R1.json'
PET01 = BASE / 'STONEAGE-PET-MODULE-01-BATCH-SOURCE-SPR-INDEX-R1.json'
R28 = BASE / 'tw85-spr137-r28'
R29 = BASE / 'tw85-frame-bitmap-r29'
KEYS = (101279,101280,101281,101564,101736,101737)
PINS = {
 'r2b3': (R2B3, '0e80e5a62dd59542c3e1ede18460d92e17927a30', None),
 'pet01': (PET01, '5c4864e87f717711eac3c10cd9cefd27970484e6', None),
 'r28_source': (R28/'SOURCE-DERIVED-R28.json', None, '1726d1220102532d6c4bfa59ea36a6048c0623a2838394338bff5496de504af9'),
 'r28_group': (R28/'SPR-GROUP-R28.tsv.gz', None, 'bba57495fb4df36bd41e967033e799ea021cde3c7d11e982c50a1fdd5f9b1c18'),
 'r28_animation': (R28/'SPR-ANIMATION-R28.tsv.gz', None, '46aeb0628a2d7a66bf52644dfc80b1c063b4b32dcb1894a31bd2268c136eb86e'),
 'r28_frame': (R28/'SPR-FRAME-R28.tsv.gz', None, 'd5e026801e743fed481847fe69da4a235c14d8019d3824d64182bc2821645142'),
 'r29_report': (R29/'REPORT-R29.json', None, None),
 'r29_group': (R29/'GROUP-MATERIAL-R29.tsv.gz', None, 'bbd7588d473143ff2c4918f988e48f4f524907afee7623abfaf1d043f6c025bf'),
 'r29_bitmap': (R29/'BITMAP-BINDINGS-R29.tsv.gz', None, '7afa7d1274cddd4006640f7326056f0e4b96cdb5400048a6a4cd39e944b1013d'),
}


def need(ok, description):
 if not ok: raise ValueError('PET12 original source boundary: '+description)


def sha(data): return hashlib.sha256(data).hexdigest()

def gitblob(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def pin_sources():
 out={}
 for key,(path,git,s256) in PINS.items():
  b=path.read_bytes()
  if git:need(gitblob(b)==git,'immutable Git blob: '+key)
  if s256:need(sha(b)==s256,'immutable original-derived file: '+key)
  out[key]={'git_blob':git or gitblob(b),'sha256':sha(b),'bytes':len(b)}
 return out

def read_rows(name):
 with gzip.open(PINS[name][0],'rt',encoding='utf8',newline='') as f:
  yield from csv.DictReader(f,delimiter='\t')


def derive():
 pins=pin_sources()
 r2=json.loads(R2B3.read_text(encoding='utf8'))
 pet=json.loads(PET01.read_text(encoding='utf8'))
 r28=json.loads((R28/'SOURCE-DERIVED-R28.json').read_text())
 r29=json.loads((R29/'REPORT-R29.json').read_text())
 need(r2['conservation']['source_capture_rows']==11 and r2['conservation']['graph_numbers_absent_within_this_single_spradrn_index']==6,'WORLD37 source counts')
 need(pet['source_scope'].startswith('2016_LATER_COMMUNITY'),'PET01 independent source class')
 need(r28['schema']=='stoneage.tw85_original_spr137_material.r28' and r29['schema']=='stoneage.tw85_frame_to_bitmap_same_saved_carrier.r29','archived original-derived source types')
 need(r29['source_pins']['R28_FRAME']['sha256']==pins['r28_frame']['sha256'] and r29['source_pins']['R28_GROUP']['sha256']==pins['r28_group']['sha256'],'R28/R29 original carrier cross-source pin')
 need(r29['tables']['GROUP-MATERIAL-R29.tsv.gz']['sha256']==pins['r29_group']['sha256'] and r29['tables']['BITMAP-BINDINGS-R29.tsv.gz']['sha256']==pins['r29_bitmap']['sha256'],'R29 native RD source pins')
 need(r29['native_records']==416220 and r29['frame_mapping_classifications']=={'SINGLE_ORIGINAL_RD_RECORD':730907},'R29 complete same-source RD qualification')
 cands={x['configured_enemybase_column37_graphic_number']:x for x in r2['rows'] if x['preserved_original_spradrn_5_match'] is None}
 need(set(cands)==set(KEYS),'all and only six missing-within-mixed25 candidates')
 registry={row[0]:row for row in pet['graphic_registry'] if row[0] in KEYS}
 need(set(registry)==set(KEYS),'PET01 all six indexed')
 for gid,row in registry.items():
  need(not row[2] and not row[5] and len(row[4])==1,'TW1 and mixed25 absence, TW85 unique index '+str(gid))
  need(len(row[3])==int(gid in (101279,101280,101281)),'only three CN5 numeric matches')
 gs={int(x['spr_no']):x for x in read_rows('r28_group') if int(x['spr_no']) in KEYS}
 need(set(gs)==set(KEYS),'six TW85 original R28 groups missing/ambiguous')
 r29_groups={int(x['spr_no']):x for x in read_rows('r29_group') if int(x['spr_no']) in KEYS}
 need(set(r29_groups)==set(KEYS),'six same-carrier R29 groups missing/ambiguous')
 old={int(x['tw85_index']) for x in r28['joins']['reference_relationships']['CN50']}
 need(len(old)==1185,'previous CN5 exact whole SPR compare changed')
 selected_index={int(gs[n]['index']) for n in KEYS}
 by_anim=defaultdict(list); by_frame=defaultdict(list)
 for a in read_rows('r28_animation'):
  gi=int(a['group_index'])
  if gi in selected_index:by_anim[gi].append(a)
 for f in read_rows('r28_frame'):
  gi=int(f['group_index'])
  if gi in selected_index:by_frame[(gi,int(f['anim_index']))].append(f)
 result=[];allbits=set();samples=set();frame_total=0;sentinels=0
 for gid in KEYS:
  g=gs[gid];idx=int(g['index']);p=registry[gid];joined=r29_groups[gid];c=cands[gid]
  need(p[4]==[idx] and p[6]==[g['segment_sha256']],'PET01 source whole segment SHA/index')
  need(joined['source_scope']==('EXACT_CN50_SPR_SEGMENT' if idx in old else 'R28_UNMATCHED_CN50_SPR_SEGMENT'),'CN5 exact-byte vs unmatched status')
  need((idx in old)==bool(p[3]),'CN5 same-number and same-SPR-full-byte relation')
  cursor=int(g['offset']);raw=bytearray();seen=set();sounds=Counter();directions=Counter();actions=Counter();first=[];occ=0;flag=0
  animations=by_anim[idx]
  need(len(animations)==int(g['anim_count']),'complete 56 or non-56 original animations')
  for ai,a in enumerate(animations):
   need((int(a['group_index']),int(a['anim_index']),int(a['offset']))==(idx,ai,cursor),'original source animation offsets')
   cnt=int(a['frame_count']);direction=int(a['direction']);action=int(a['anim_no']);duration=int(a['duration'])
   need(0<cnt<=112,'finite original animation frame bound')
   raw+=struct.pack('<HHII',direction,action,duration,cnt);cursor+=12
   directions[direction]+=1;actions[action]+=1
   fr=by_frame.get((idx,ai),[])
   need(len(fr)==cnt,'missing exact original source frame')
   for i,f in enumerate(fr):
    need((int(f['group_index']),int(f['anim_index']),int(f['frame_index']),int(f['offset']))==(idx,ai,i,cursor),'frame order and physical offsets')
    bitmap=int(f['bmp_no']);sent=int(f['sentinel']);cue=int(f['sound_no'])
    need(sent==int(bitmap==0xffffffff),'original sentinel')
    raw+=struct.pack('<IhhH',bitmap,int(f['pos_x']),int(f['pos_y']),cue);cursor+=10;occ+=1;flag+=sent;sounds[cue]+=1
    if not sent:seen.add(bitmap);allbits.add(bitmap)
   if direction==0 and fr and not (int(fr[0]['sentinel'])):
    first.append({'action':action,'animation_index':ai,'duration_word':duration,'frame_count':cnt,'first_bitmap_no':int(fr[0]['bmp_no'])})
  need(cursor==int(g['end_offset'])==int(g['next_offset']),'complete source segment extent')
  need(sha(raw)==g['segment_sha256'],'full original source segment byte identity')
  need(int(joined['frame_occurrences'])==occ and int(joined['sentinel_frames'])==flag and int(joined['distinct_bitmap_ids'])==len(seen),'full original R29 frame/RD identities')
  need(int(joined['missing_frames'])==0 and int(joined['multiple_different_rd_frames'])==0 and int(joined['mapped_frames'])==occ-flag,'original same-carrier RD mapping is unique')
  need(int(joined['raw_sound_word_occurrences'])==sum(cu for n,cu in sounds.items() if n!=0),'original cue count')
  samples.update(x['first_bitmap_no'] for x in first)
  need(len(first)>0,'at least direction 0 original animation')
  frame_total+=occ;sentinels+=flag
  result.append({'graphic_no':gid,'capture_source_key53_candidate':c['source_char_int_key53'],'mixed25_configured_name_cp950':c['configured_enemybase_name_original_cp950'],'source_petflag':c['configured_enemybase_column38_PETFLG'],'tw85_original_group_index':idx,'tw85_segment_offset':int(g['offset']),'tw85_segment_bytes':len(raw),'tw85_exact_original_segment_sha256':sha(raw),'tw85_original_animation_sequences':len(animations),'tw85_original_frame_positions':occ,'tw85_sentinel_frame_positions':flag,'tw85_distinct_same_carrier_bitmap_numbers':len(seen),'tw85_distinct_complete_rd_contents':int(joined['distinct_mapped_rd_contents']),'tw85_unique_original_rd_bitmap_refs':occ-flag,'direction_sequence_counts':{str(k):v for k,v in sorted(directions.items())},'action_sequence_counts':{str(k):v for k,v in sorted(actions.items())},'raw_sound_nonzero_positions':sum(v for k,v in sounds.items() if k!=0),'direction0_first_qualified_original_frames':first,'cn50_index':p[3][0] if p[3] else None,'cn50_same_id_and_entire_spr_segment_sha_verified_in_R28':idx in old,'tw10_original_spr_index':None,'mixed25_original_spr_index':None,'full_original_RD_pixels_read_now':0,'original_gameplay_action_semantics_proven':False})
 matched={}
 for x in read_rows('r29_bitmap'):
  bmp=int(x['bitmapno'])
  if bmp in allbits:
   need(bmp not in matched,'duplicate same-carrier bitmap binding in R29')
   need(int(x['native_candidates'])==1 and x['qualification']=='SINGLE_ORIGINAL_RD_RECORD','same-carrier missing/ambiguous RD original source')
   need(len(x['complete_rd_content_keys'].split(':'))==2,'complete RD SHA+length source key')
   rd_size,rd_sha=x['complete_rd_content_keys'].split(':')
   need(len(rd_sha)==64 and rd_size==x['sizes'],'original RD complete SHA')
   matched[bmp]={'native_adrn_physical_index':int(x['native_indices']),'RD_original_bytes':int(rd_size),'RD_original_sha256':rd_sha,'width':int(x['widths']),'height':int(x['heights'])}
 need(set(matched)==allbits,'all six original bitmap IDs link same-carrier verified original RD')
 for row in result:
  for f in row['direction0_first_qualified_original_frames']:
   f['same_carrier_original_RD']=matched[f['first_bitmap_no']]
  # Indexed inventory only: no full copyrighted bitmap/palette/sprite payload duplicated.
  row['sample_direction0_first_frame_count']=len(row['direction0_first_qualified_original_frames'])
 need(len(result)==6 and sum(x['tw85_original_frame_positions']for x in result)==frame_total,'six-source group conservation')
 need(sum(x['cn50_same_id_and_entire_spr_segment_sha_verified_in_R28'] for x in result)==3,'three exact CN5 group sources')
 need(len(allbits)>=len(samples)>0,'sample and full bitmap membership')
 return {'schema':'stoneage.pet12.six_capture_candidates_original_tw85_spr_and_same_carrier_rd_sources.r1',
    'source_grade':'TW85_UNVERIFIED_COMMUNITY_PRESERVED_CLAIMED_RELEASE_NOT_OFFICIAL_CLEAN_BUILD',
    'source_pins':pins,'capture_candidate_graphics_six':list(KEYS),
    'origin':'original WORLD37 mixed25 numeric candidate -> independent TW85 recorded SPR group -> same TW85 archived original RD record',
    'original_sources':{'tw85_saved_spr_137_complete_source_sha256':r28['pair']['spr_137.bin']['sha256'],
        'tw85_saved_spradrn_137_complete_source_sha256':r28['pair']['spradrn_137.bin']['sha256'],
        'tw85_original_REAL_complete_source_sha256':'e0f9c0d20fd3d9daae0701d8a872c9842e27d3da1be4d449d558c9c76d1c5f5b',
        'tw85_original_ADRN_complete_source_sha256':'16ba4fa3825b2c4b6645bab8b4fe3152a262a4789c8bb89e3043a7d3f0d53681'},
    'groups':result,
    'summary':{'group_occurrences':6,'groups_with_CN50_exact_full_SPR_bytes':3,'groups_not_in_CN50_source':3,'groups_with_TW1_source_index':0,'groups_with_mixed25_source_index':0,
        'original_animation_sequences':sum(x['tw85_original_animation_sequences'] for x in result),'original_frame_occurrences':frame_total,'original_sentinel_frame_occurrences':sentinels,'original_nonsentinel_frame_occurrences':frame_total-sentinels,
        'distinct_referenced_original_same_carrier_bitmap_ids':len(allbits),'distinct_original_direction0_first_frame_bitmap_ids':len(samples),
        'same_carrier_source_qualified_original_RD_bitmap_ids':len(matched),
        'actually_new_original_pixels_decoded_in_this_work_unit':0,
        'actual_source_replay_type':'COMPLETE_ARCHIVED_SOURCE_METADATA_REENCODE_AND_SAME_CARRIER_RD_SHA_JOIN_NOT_SOURCE_REAL_IO'},
    'negative_boundaries':{'original_tw85_REAL_bytes_reacquired_this_turn':False,'original_tw85_RD_pixels_recovered_now':False,'official_TW85_clean_build_certified':False,'mixed25_and_TW85_same_deployed_build_proven':False,'capture_entity_species_join_native_runtime_proven':False,'original_fps_or_duration_units_authenticated':False,'original_animation_action_meanings_authenticated':False,'CN50_only_matching_ID_implies_same_payload':False,'TW10_source_species_identity_from_other_build':False,'original_client_or_server_executed':False,'proprietary_source_payloads_published':False,'stage_a':'7_PARTIAL_2_OPEN','stage_b_wiki':'GATED','r79':'PAUSED_NON_BLOCKING','overall_percent':None}}


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--emit-json',action='store_true');ap.add_argument('--check',type=Path)
 args=ap.parse_args();result=derive()
 if args.check is not None:need(json.loads(args.check.read_text(encoding='utf8'))==result,'archived public report differs from complete source replay')
 if args.emit_json:print('PET12_SOURCE_JSON_BEGIN\n'+json.dumps(result,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\nPET12_SOURCE_JSON_END')
 print('PET12_SOURCE_PASS groups=6 animations='+str(result['summary']['original_animation_sequences'])+' frames='+str(result['summary']['original_frame_occurrences'])+' original_pixels_now=0')

if __name__=='__main__':main()