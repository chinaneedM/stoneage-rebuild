"""Bounded native CN5 animation material join for exactly three extra groups.

Consume permanent source-derived tables, retain every raw frame/cue occurrence,
and re-encode complete SPR segments against their historical byte digests.
Do not infer names, action labels, audio identities or runtime time units.
"""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import io
import json
import lzma
from pathlib import Path

from tools.stoneage_original_animation_lab import reconstruct_group

ROOT=Path(__file__).resolve().parents[1]
BASE='research/recovered/'
CN=BASE+'cn50-resource-metadata/'
TW=BASE+'tw10-resource-metadata/'
KEYS=[100700,100701,100702]
REPORT=ROOT/BASE/'STONEAGE-CN5-ANIMATION-MATERIAL-R26.json.xz'
SUMMARY=ROOT/BASE/'STONEAGE-CN5-ANIMATION-MATERIAL-R26-SUMMARY.json'
PINS={
  "research/recovered/cn50-resource-metadata/SPR-GROUP-R1.tsv.gz": "67660d3d8ba5e05293f61f60ab3e1bfe736d7b6bdc4159ed96fcb59f5acfa228",
  "research/recovered/cn50-resource-metadata/SPR-ANIMATION-R1.tsv.gz": "63f444ac202a7a9d1d7afafbd068a78d8724a843ea8174bb4d36b83a13cfa8b7",
  "research/recovered/cn50-resource-metadata/SPR-FRAME-R1.tsv.gz": "0b5a326ddd70a5d6957b7e8c6faa2f8e0b7bed2dd70ab02bef9bb86f39f9b3ab",
  "research/recovered/cn50-resource-metadata/ADRN-R1.tsv.gz": "e24afc513d28c7f25bd26bde9c69ddc0de4000147a2b11f50b5176655d8558fd",
  "research/recovered/cn50-resource-metadata/MANIFEST-R1.json": "73181d1de1efadc971eaea254891103bd69fd7d3121fc450ec3b148ca8d06fa8",
  "research/recovered/tw10-resource-metadata/SPR-GROUP-R1.tsv.gz": "4db7809de4197eb90cca6dc04bda8550025e022c8232e2ebb902db0e9faf0175",
  "research/recovered/tw10-resource-metadata/ADRN-R1.tsv.gz": "c8669789de1cc6e3575c2412ed86354a49c2b3e90cd2854c1e7b2fc71b0fe9ea",
  "research/recovered/tw10-resource-metadata/MANIFEST-R1.txt": "fb9b2dbe52a305f5ff2934cc1dcdf275be1215e2a89b326dd76fd7f80b6d9743",
  "research/recovered/STONEAGE-TW10-CN50-REAL-RESOURCE-CUSTODY-R1.json": "9eeab87743c4ee65e7fcafb605eb7f12cafd2fb68c1afee962128ade7318c8de"
}


def need(ok,message):
    if not ok:raise ValueError(message)


def fingerprint(raw):
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
            'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}


def check_source(path,raw):
    need(path in PINS and hashlib.sha256(raw).hexdigest()==PINS[path],'source byte drift: '+path)


def rows(raw):
    with gzip.open(io.BytesIO(raw),'rt',encoding='utf-8',newline='') as handle:
        for row in csv.DictReader(handle,delimiter='\t'):
            yield {k:(v if k.endswith('sha256') else int(v)) for k,v in row.items()}


def select_groups(cn_groups,tw_groups):
    old={x['spr_no'] for x in tw_groups}
    extra=[x for x in cn_groups if x['spr_no'] not in old]
    selected=extra[:3]
    need(len(cn_groups)==1185 and len(tw_groups)==464 and len(extra)==721,'source inventory changed')
    need([x['spr_no'] for x in selected]==KEYS,'not the first three source-order extra groups')
    need(len({x['index'] for x in selected})==3,'group index collision')
    return selected


def rd_identity(row):
    return row['size'],row['rd_block_sha256']


def build():
    raw={path:(ROOT/path).read_bytes() for path in PINS}
    for path,data in raw.items():check_source(path,data)
    selected=select_groups(list(rows(raw[CN+'SPR-GROUP-R1.tsv.gz'])),
                           list(rows(raw[TW+'SPR-GROUP-R1.tsv.gz'])))
    animations=defaultdict(list);frames=defaultdict(lambda:defaultdict(list))
    for row in rows(raw[CN+'SPR-ANIMATION-R1.tsv.gz']):
        if row['spr_no'] in KEYS:animations[row['spr_no']].append(row)
    for row in rows(raw[CN+'SPR-FRAME-R1.tsv.gz']):
        if row['spr_no'] in KEYS:frames[row['spr_no']][row['anim_index']].append(row)
    groups=[];bitmap_refs=defaultdict(list);cues=[];shapes=[]
    for group in selected:
        key=group['spr_no'];aa=animations[key];ff=frames[key]
        binary=reconstruct_group(group,aa,ff)
        need(len(binary)==group['end_offset']-group['offset'],'segment extent changed')
        animation_rows=[];shape=[]
        for animation in aa:
            sequence=ff[animation['anim_index']]
            shape.append([animation['direction'],animation['anim_no'],animation['duration'],
                          animation['frame_count'],[[f['pos_x'],f['pos_y']] for f in sequence]])
            for frame in sequence:
                if frame['sentinel']==0:
                    bitmap_refs[frame['bmp_no']].append({'spr_no':key,'anim_index':animation['anim_index'],
                        'direction':animation['direction'],'anim_no':animation['anim_no'],
                        'frame_index':frame['frame_index']})
                if frame['sound_no']!=0:
                    cues.append({'spr_no':key,'anim_index':animation['anim_index'],
                        'direction':animation['direction'],'anim_no':animation['anim_no'],
                        'frame_index':frame['frame_index'],'raw_sound_word':frame['sound_no'],
                        'event_name':None,'audio_file':None,'heard_or_played':False})
            animation_rows.append({'source':animation,'frames':sequence})
        shapes.append(shape)
        groups.append({'source':group,'complete_segment_reencoding':{
            'bytes':len(binary),'sha256':hashlib.sha256(binary).hexdigest(),
            'matches_prior_complete_segment_digest':True,'binary_bytes_published':False},
            'animations':animation_rows})
        del binary  # Reconstructed proprietary segment exists in memory only.
    cn_bitmaps={}
    for row in rows(raw[CN+'ADRN-R1.tsv.gz']):
        if row['bitmapno'] in bitmap_refs:
            need(row['bitmapno'] not in cn_bitmaps,'ambiguous CN5 physical bitmap number')
            cn_bitmaps[row['bitmapno']]=row
    need(cn_bitmaps.keys()==bitmap_refs.keys(),'selected frame has no physical bitmap source')
    wanted={rd_identity(x) for x in cn_bitmaps.values()}
    old_matches=defaultdict(list);old_ids=set();tw_count=0
    for row in rows(raw[TW+'ADRN-R1.tsv.gz']):
        tw_count+=1
        if row['bitmapno'] in bitmap_refs:old_ids.add(row['bitmapno'])
        if rd_identity(row) in wanted:old_matches[rd_identity(row)].append(row['bitmapno'])
    need(tw_count==125996,'TW1 full bitmap corpus incomplete')
    manifest=json.loads(raw[CN+'MANIFEST-R1.json'])
    need(manifest['source']['official_clean_pressing_verified'] is False,'source grade promoted')
    real_bytes=manifest['source']['input_containers']['real']['bytes']
    bitmaps=[];contents=defaultdict(list)
    for bitmapno,row in sorted(cn_bitmaps.items()):
        need(0<=row['adder'] and row['size']>0 and row['adder']+row['size']<=real_bytes,
             'selected RD block outside authenticated REAL extent')
        members=sorted({x['spr_no'] for x in bitmap_refs[bitmapno]})
        matches=old_matches[rd_identity(row)]
        bitmaps.append({'source':row,'used_by_groups':members,
            'frame_reference_count':len(bitmap_refs[bitmapno]),
            'tw10_same_physical_id_present':bitmapno in old_ids,
            'tw10_exact_complete_rd_matches':matches,
            'interpretation':'NO_MATCH_IN_THIS_TW10_COMPLETE_RD_CORPUS' if not matches else 'EXACT_RD_CONTENT_PRESENT'})
        contents[rd_identity(row)].append(bitmapno)
    membership=Counter('+'.join(map(str,x['used_by_groups'])) for x in bitmaps)
    per_group={}
    for group in groups:
        key=group['source']['spr_no'];aa=group['animations'];all_frames=[f for a in aa for f in a['frames']]
        per_group[str(key)]={'animations':len(aa),'frame_occurrences':len(all_frames),
            'unique_bitmap_numbers':len({f['bmp_no'] for f in all_frames if not f['sentinel']}),
            'directions':sorted({a['source']['direction'] for a in aa}),
            'raw_action_codes':sorted({a['source']['anim_no'] for a in aa}),
            'raw_duration_histogram':dict(sorted(Counter(str(a['source']['duration']) for a in aa).items())),
            'raw_sound_word_histogram':dict(sorted(Counter(str(f['sound_no']) for f in all_frames).items())),
            'sentinel_frame_occurrences':sum(f['sentinel'] for f in all_frames)}
    shared=[x['source']['bitmapno'] for x in bitmaps if len(x['used_by_groups'])==3]
    shared_uses=[{'bitmapno':bitmapno,**ref} for bitmapno in shared for ref in bitmap_refs[bitmapno]]
    summary={'schema':'stoneage.cn5_three_animation_material_summary.r26',
        'task':'CN5-ADDITIONAL-ANIMATION-MATERIAL-26',
        'source_head':'0db5d096a567f62e88ac36796766c3e37cc3b060',
        'selection':KEYS,'source_pins':{p:fingerprint(data) for p,data in raw.items()},
        'source_profile':'PRESERVED_CN5_CAB_MSI_5_00_0000_NOT_INDEPENDENTLY_AUTHENTICATED_CLEAN_PRESSING',
        'source_containers':manifest['source']['input_containers'],
        'per_group':per_group,'animation_occurrences':sum(x['animations'] for x in per_group.values()),
        'frame_occurrences':sum(x['frame_occurrences'] for x in per_group.values()),
        'physical_bitmaps':len(bitmaps),'unique_complete_rd_contents':len(contents),
        'bitmap_group_membership':dict(sorted(membership.items())),
        'tw10_full_bitmap_records_searched':tw_count,
        'selected_physical_ids_present_in_tw10':len(old_ids),
        'selected_rd_contents_found_in_tw10':len(old_matches)-sum(not v for v in old_matches.values()),
        'three_numeric_sequence_shapes_equal_excluding_bitmap_and_sound_words':shapes[0]==shapes[1]==shapes[2],
        'common_three_group_bitmaps':shared,'common_bitmap_frame_occurrences':len(shared_uses),
        'common_bitmap_raw_action_codes':sorted({x['anim_no'] for x in shared_uses}),
        'nonzero_raw_sound_word_occurrences':len(cues),
        'nonzero_raw_sound_words':sorted({x['raw_sound_word'] for x in cues}),
        'complete_spr_segments_reencoded':len(groups),
        'boundaries':{'new_original_bytes_downloaded':False,'original_program_executed':False,
            'original_asset_bytes_published':0,'original_file_bytes_deleted':0,
            'actual_pixels_viewed_or_rendered':False,'sound_words_linked_to_audio_files':False,
            'sound_heard_or_played':False,'named_character_pet_or_npc_identity_proven':False,
            'raw_direction_codes_named_as_compass_directions':False,
            'raw_action_codes_named_as_gameplay_actions':False,'cn5_duration_unit_or_game_fps_proven':False,
            'tw10_loader_timing_formula_promoted_to_cn5':False,'all_versions_contain_or_lack_these_assets_proven':False,
            'stage_a':'7_PARTIAL_2_OPEN','stage_b_wiki':'GATED','r79':'PAUSED_NON_BLOCKING',
            'overall_completion_percent':None},
        'next':'KR-NETMARBLE120-CLIENT-SOURCE-27'}
    return {'schema':'stoneage.cn5_three_animation_material.r26','summary':summary,'groups':groups,
            'bitmaps':bitmaps,'complete_rd_contents':[{'bytes':size,'sha256':sha,'bitmapnos':ids}
                 for (size,sha),ids in sorted(contents.items())],
            'shared_bitmap_frame_references':shared_uses,'nonzero_raw_sound_word_references':cues}


def validate(doc):
    need(doc==build(),'permanent group/frame/RD material differs from exact pinned sources')
    s=doc['summary']
    need((s['animation_occurrences'],s['frame_occurrences'],s['physical_bitmaps'],s['unique_complete_rd_contents'])
         ==(312,1464,936,936),'selected material occurrence/content coverage changed')
    need(s['bitmap_group_membership']=={'100700':296,'100700+100701+100702':48,'100701':296,'100702':296},
         'shared frame assets silently duplicated or deleted')
    need(s['selected_rd_contents_found_in_tw10']==0 and s['selected_physical_ids_present_in_tw10']==0,
         'unsupported TW1 inheritance claim')
    need(s['nonzero_raw_sound_word_occurrences']==64 and s['common_bitmap_raw_action_codes']==[12],
         'raw cue/action location changed')
    return s


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    if args.write:
        doc=build()
        REPORT.write_bytes(lzma.compress((json.dumps(doc,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()))
        SUMMARY.write_text(json.dumps(doc['summary'],ensure_ascii=False,indent=2)+'\n')
    doc=json.loads(lzma.decompress(REPORT.read_bytes()));summary=validate(doc)
    need(json.loads(SUMMARY.read_bytes())==summary,'summary mismatch')
    print(json.dumps({'status':'PASS','animations':summary['animation_occurrences'],
          'frames':summary['frame_occurrences'],'complete_rd_contents':summary['unique_complete_rd_contents'],
          'complete_spr_segment_sha_replays':summary['complete_spr_segments_reencoded']}))


if __name__=='__main__':main()
