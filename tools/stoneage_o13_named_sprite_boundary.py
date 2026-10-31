"""O13 public evidence-only validator; never reads proprietary original assets.

Input: previously archived Git source-derived R39, R40, O11, O12 reports.
Verifies one bounded cross-version numerical research reference, not the name of
an original TW1.0 species, a sound trigger, or any executed historical runtime.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RECOVERED = BASE / 'research' / 'recovered'
FILENAMES = {
    'r39': 'STONEAGE-PRESERVED-PET-TEMPLATE-SOURCE-R39.json',
    'r40': 'STONEAGE-PRESERVED-PET-SPR-MATERIAL-R40.json',
    'o11': 'STONEAGE-O11-NATIVE-FRAME-SOUND-SOURCE-R1.json',
    'o12': 'STONEAGE-O12-NATIVE-SOUND-NAMESPACE-R1.json',
    'o13': 'STONEAGE-O13-SOURCE-SEPARATED-NAMED-SPRITE-R1.json',
}
PINS = {
    'r39': 'e32b4dcb2fade31eafee4787ccdae0645dc6ac83',
    'r40': 'cdcfc9fb9a07c60a3320528fdddcdfecdeb6b14d',
    'o11': 'bf8d55ed2805641a0b1357abf914de2da6eadbb3',
    'o12': '1d0df7df7fa9d3527407b5282f9304fe507e7f5d',
}

def blob_sha(raw:bytes)->str:
    return hashlib.sha1(f'blob {len(raw)}\0'.encode('ascii')+raw).hexdigest()

def get_sources(root=RECOVERED):
    values={}
    for k,name in FILENAMES.items():
        b=(root/name).read_bytes()
        if k in PINS and blob_sha(b)!=PINS[k]:
            raise ValueError(f'{k}: archived Git blob identity changed')
        values[k]=json.loads(b.decode('utf-8'))
    return values

def validate(r39:dict,r40:dict,o11:dict,o12:dict,o13:dict)->dict:
    if o13.get('schema')!='stoneage.o13.cross_source_original_sprite_named_observer.r1':
        raise ValueError('wrong O13 report schema')
    expected_pins={
      'R39_mixed25_server_template':PINS['r39'],
      'R40_mixed25_client_spr_and_tw1_segment_comparison':PINS['r40'],
      'O11_original_TW1_SPR_and_pixel_material':PINS['o11'],
      'O12_original_TW1_sound_namespace':PINS['o12'],
    }
    if o13['source_git_blob_pins']!=expected_pins:
        raise ValueError('source Git blob pins changed')
    if o13['remote_baseline_head']!='c21782e9b4f248ec9f71297e4c7f8399619c01ef':
        raise ValueError('wrong O13 historical starting main')
    if o13['remote_baseline_tree']!='99277c814899019cda141a26dd2af9e6c5a9ae26':
        raise ValueError('wrong starting Git tree')
    src_rows=r39['material']['selected_rows']
    src_links=r40['server_occurrence_links']
    out=o13['server_occurrences']
    if len(src_rows)!=7 or len(src_links)!=7 or len(out)!=7:
        raise ValueError('all seven original server row occurrences required')
    fields={'original_server_line':'line','name_zh_Hant':'name','template_column_7':'template_number_column_7',
            'graphic_column_37':'graphic_field_column_37','flag_column_38':'pet_flag_column_38','original_row_sha256':'row_sha256'}
    for i,(source,row,link) in enumerate(zip(src_rows,out,src_links)):
        for dst,key in fields.items():
            if row[dst]!=source[key]:
                raise ValueError(f'server row {i}: changed original {key}')
        if link['server_original_line']!=row['original_server_line'] or link['server_row_sha256']!=row['original_row_sha256']:
            raise ValueError('server linkage source changed')
        if link['server_graphic_column_37']!=row['graphic_column_37'] or link['server_template_column_7']!=row['template_column_7']:
            raise ValueError('server numeric namespace mismatch')
        if link['server_flag_column_38']!=row['flag_column_38'] or link['server_name']!=row['name_zh_Hant']:
            raise ValueError('server name/flag mismatch')
        if link['join_kind']!='SAME_CARRIER_EQUAL_NUMERIC_KEY_ONLY_NOT_DEPLOYMENT_PROOF':
            raise ValueError('historical claim improperly promoted')
    if [r['original_server_line'] for r in out]!=[1,2,3,6,407,479,858]:
        raise ValueError('unverified row ordering')
    if [(r['original_server_line'],r['flag_column_38']) for r in out if r['graphic_column_37']==100252]!=[(3,1),(6,1),(407,1),(479,0)]:
        raise ValueError('original duplicate/conflicting flags lost')
    groups=[100250,100251,100252]
    comparisons=r40['full_segment_comparisons']
    if [g['spr_no'] for g in comparisons]!=groups:
        raise ValueError('wrong SPR groups')
    for j,g in enumerate(comparisons):
        group=groups[j]
        h=g['segment_sha256']
        if str(group) not in o13['same_numeric_group_original_spr_full_segment_sha'] or o13['same_numeric_group_original_spr_full_segment_sha'][str(group)]!=h:
            raise ValueError('wrong whole animation segment SHA')
        if not g['reference_occurrences']['TW10'][0]['exact_full_segment_equal']:
            raise ValueError('TW1 actual SPR content not same')
        if not g['reference_occurrences']['CN50'][0]['exact_full_segment_equal']:
            raise ValueError('CN50 actual SPR content not same')
        x=o13['source_separated_crosswalk'][j]
        if x['community_graphic_column_37']!=group or x['tw1_original_spr_no']!=group or x['full_spr_segment_sha256']!=h:
            raise ValueError('cross-version sprite key not supported')
        if x['community_potential_name']!=next(row['name_zh_Hant'] for row in out if row['graphic_column_37']==group):
            raise ValueError('cross-version source name mismatch')
        if x['qualified_relation']!='ORIGINAL_ANIMATION_NUMERIC_CONTENT_IDENTITY__NOT_ORIGINAL_OFFICIAL_SPECIES':
            raise ValueError('official species false-promotion')
        if x['directions']!=8 or x['original_source_animation_action']!=0:
            raise ValueError('wrong animation observation scope')
    o11_scope=o11['bounded_original_sprite_sample']
    if (o11_scope['numeric_spr_groups']!=groups or o11_scope['sequences']!=24 or
        o11_scope['ordered_frame_positions']!=352 or o11_scope['original_distinct_png']!=208 or
        o11_scope['independent_source_spans_sha_equal']!=24):
        raise ValueError('original TW1 O11 animation bounds changed')
    if (o13['prior_O11_original_animation_sequences'],o13['prior_O11_ordered_frame_positions'],o13['prior_O11_original_distinct_bitmaps'])!=(24,352,208):
        raise ValueError('O13 animation/pixel coverage falsely promoted')
    if o13['tw1_original_archive_sha256']!=o11['source_pins']['tw1_p3h_archive_sha256']:
        raise ValueError('original TW1 archive source invalid')
    if o13['o11_private_archive_sha256']!=o11['private_observation']['private_zip_sha256']:
        raise ValueError('O11 private observer source invalid')
    k73=o12['key_number_73']
    assert k73['native_compiled_number_namespace_differs_from_address_table_ordinal']
    sound_names=(k73['compiled_native_sound_number_filepath'].replace('data\\se\\',''),k73['address_table_zero_based_73'],k73['address_table_one_based_73'])
    if sound_names!=(o13['o12_compiled_sound_number_73'],o13['o12_soundaddr_zero_based_73'],o13['o12_soundaddr_one_based_73']):
        raise ValueError('three sound number namespaces conflated')
    if not o13['source_word_73_meaning_open'] or not o13['source_word_10000_meaning_open']:
        raise ValueError('unknown SPR word semantic misrepresented')
    forbidden=['official_tw1_species_join_proven','original_pet_master_restored','actual_original_palette_choice_confirmed','historical_game_runtime_executed','actual_sound_event_selected','commercial_art_publicly_embedded']
    if any(o13[x] is not False for x in forbidden):
        raise ValueError('historical source/runtime/asset promotion forbidden')
    inv=o13['tw1_private_archive_inventory_actual']
    if inv['scope']!='P3H_PRIVATE_SOURCE_BUNDLE_NOT_ALL_ORIGINAL_DEPLOYMENTS' or not inv['presence_not_proven_absent_embedded_resources']:
        raise ValueError('missing embedded-source boundary')
    if inv['zip_members']!=379 or inv['pet_entity_master_named_file_present'] or inv['original_server_npc_quest_script_named_file_present']:
        raise ValueError('wrong original package inventory projection')
    if o13['overall_restoration_percent'] is not None or o13['stage_a']!='7_PARTIAL_2_OPEN' or o13['stage_b']!='GATED' or o13['savedata_R79']!='PAUSED_NONBLOCKING':
        raise ValueError('overall project completion false-promotion')
    return {'status':'O13_PUBLIC_SOURCE_ONLY_PASS','server_rows':7,'named_candidate_groups':3,'original_source_sequences':24,'original_source_frame_occurrences':352,'original_unique_png':208,'original_runtime_runs':0}

def main():
    print(json.dumps(validate(**get_sources()),ensure_ascii=False,sort_keys=True))

if __name__=='__main__':
    main()
