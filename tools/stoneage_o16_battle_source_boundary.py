"""O16 source-derived TW1 SAB/SAP manifest audit. No proprietary originals in CI."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-O16-TW10-BATTLE-NATIVE-PALETTE-INTERLEAVE-R1.json'
PRIOR=ROOT/'research/recovered/STONEAGE-BATTLE-SAB-CROSSVERSION-R17-CORRECTED-R24.json'
SCENE=ROOT/'research/recovered/STONEAGE-SCENE29-TW10-BATTLE-PET-ACTUAL-R1.json'
def load():
 return [json.loads(p.read_text(encoding='utf-8')) for p in (REPORT,PRIOR,SCENE)]
def ensure(b,s):
 if not b:raise ValueError(s)
def validate(d,old,scene):
 ensure(d['schema']=='stoneage.o16.tw1_original_battle_mixed_container_source_verified.r1','schema')
 n=d['native_manifest'];o=d['original_source'];b=d['battle_sab_records'];p=d['embedded_palette_records'];c=d['source_bitmap_coverage'];v=d['private_observer']
 ensure((n['entries'],n['battle_entries'],n['palette_entries'])==(233,218,15),'original 233 mixed records')
 ensure(n['all_233_original_slice_bytes_match_individual_source_members'] and n['original_container_exactly_consumed'],'source byte equality missing')
 ensure((n['first_palette_offset'],n['last_palette_offset'],n['palette_total_bytes'])==(161604,171516,10620),'palette interleave proof')
 ensure((n['battle200_offset'],n['battle201_real_offset'],n['battle201_incorrect_naive_offset'])==(160800,172224,161604),'battle200-201 boundary')
 ensure(not n['palet0_in_container'],'invented Palet0')
 ensure((o['archive_bytes'],o['battle_1_bin_bytes'],o['battletxt_bytes'],o['adrn_bytes'],o['real_bytes'])==(372626292,185892,5792,10079680,315842228),'source bytes')
 ensure(o['archive_sha256']=='3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24','wrong original archive')
 ensure(o['battle_1_bin_sha256']=='d99be6475982cf6098b90ff5dfd81ab275ec8c9271fa83daceb95e3fd4bb8859','wrong battle container')
 ensure(o['battletxt_sha256']=='5c4a38cc7c1f039e232611b5eac33514f67c4d8badbaf638ae9b852440237fc4','wrong native table')
 ensure(len(b)==218 and [r['id'] for r in b]==list(range(218)),'all original SAB IDs')
 oldmaps={i['id']:i['sha256'] for i in old['occurrences'] if i['profile']=='tw10'}
 ensure(len(oldmaps)==218,'old R24 expected source')
 for i,row in enumerate(b):
  ensure(row['packed_offset']==804*i+(10620 if i>200 else 0),'bad native offset')
  ensure(row['bytes']==804 and row['sha256']==oldmaps[i],'historical SAB SHA mismatched')
 ensure(len(p)==15 and [i['name'] for i in p]==[f'Palet_{x}.sap' for x in range(1,16)],'SAP member set')
 for i,r in enumerate(p):ensure(r['packed_offset']==161604+i*708 and r['bytes']==708 and len(r['sha256'])==64,'SAP actual offsets')
 ensure(p[0]['sha256']=='32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0','Palet1 original')
 ensure((c['battle_entries_with_400_source_cells'],c['source_cells_total'],c['distinct_original_sab_SHA256'])==(218,87200,217),'SAB cell counts')
 ensure(c['duplicate_index_group']==[[145,146]] and b[145]['sha256']==b[146]['sha256'],'original repeated SAB not to lose')
 ensure(c['distinct_original_bitmap_ids_in_218_sabs']==2296 and c['all_original_bitmap_ids_unique_in_same_build_adrn'] and c['all_original_rd_data_ranges_in_original_real'],'same TW1 image ids')
 ensure((c['source_rd_decoded'],c['source_rd_codec_open_count'],c['full_scene_source_RD_coverage'])==(2295,1,217),'RD source limitations')
 ensure(c['source_rd_codec_open_id']==6729 and c['source_rd_codec_open_scene_id']==181 and c['source_rd_codec_open_unknown_header_byte']==16 and c['source_rd_codec_open_flag']==1,'RD counterexample')
 ensure(c['source_rd_codec_open_sha256']=='6a2e472dfb9d5c08dfdb0176345c7b2935b0fe900f3fffea98f53674b486977e','RD source sha')
 ensure(c['unresolved_RD_not_silently_dropped'] and c['decoded_original_pixel_positions']==10723848,'RD coverage honesty')
 ensure(len(v['source_map_ids'])==12 and v['source_map_ids']==[0,1,18,40,62,82,100,120,145,167,190,217],'private original source sample')
 for r in scene['sab_maps']:
  png=v['source_candidate_pngs'][str(r['index'])]
  ensure(r['sha256']==b[r['index']]['sha256'] and r['candidate_background_png_sha256']==png['png_sha256'] and r['candidate_background_rgba_sha256']==png['rgba_sha256'],'old SCENE29 RGB source regression')
 ensure(v['source_pixels_in_public_git']==False and v['original_image_loads_passed']==12 and v['js_errors']==0 and v['http_requests']==0 and v['user_file_url_launch_verified']==False,'private browser/evidence boundary')
 ensure(v['source_color_mode']=='Palet_1 ORIGINAL_BYTES_AS_MODERN_CANDIDATE_NOT_NATIVE_GAME_SELECTOR','scene palette not certified')
 ensure(all(q is False for key,q in d['evidence_boundaries'].items() if key!='restoration_percent') and d['evidence_boundaries']['restoration_percent'] is None,'false historical claim')
 g=d['project_gates'];ensure((g['stage_A_partial'],g['stage_A_open'],g['stage_B_gated'],g['wiki_gated'],g['R79_paused_nonblocking'],g['new_game_started'])==(7,2,True,True,True,False),'project stage changed')
 return {'sabs':218,'palettes':15,'RD_decoded':2295,'RD_open':1,'source_full_RDs_for_scenes':217,'original_game_played':False}
if __name__=='__main__':print(json.dumps(validate(*load()),sort_keys=True))
