"""Acceptance of the exact original TW1.0 create-character numeric metadata.

Independent semantic replay over archived source-derived bytes and unchanged
original SPR group metadata; never asserts table extent or original player IDs.
"""
from __future__ import annotations
import hashlib
import json
import struct
from pathlib import Path
from tools.stoneage_tw10_character_creation_body_window_r16 import source_groups, classify_window
from tools.stoneage_tw10_character_creation_r16_join import load, qualify, LOGIN, ANIM

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'research/recovered/STONEAGE-TW10-CREATION-BODY-WINDOW-R16.json'
EXPECTED_SHA256 = '03be7a2c14f71c96c8114156c7189d836d99b805895510edf453ae9f706d7a59'
EXPECTED_BLOB = '4e0d8bddf6ee9e9de372b0b484d3489796007726'
WINDOW_SHA256 = '0e9687f40dae13f8b700426b44b8fcd1b5b462396541b0123464034fbb755d65'
EXE_SHA256 = 'cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a'
EXPECTED_VALUES = [100000,100020,100040,100060,100080,100100,100120,100140,100160,100180,100200,100220,198,301,113,258,248,396,130,370,137,160,343,379,479,371,420,310,376,231,297,198]

def need(x, message):
    if not x:
        raise ValueError(message)

def git_blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def accept_record(r, groups):
    need(r['schema'] == 'stoneage.tw10.character_creation_body_static_window.r16', 'wrong source-derived schema')
    need(r['task'] == 'ORIGINAL-CHARACTER-CREATION-CONTENT-16', 'task substituted')
    source = r['primary_source']
    need(source['identity'] == 'TW10_ACCEPTED_RETAIL_SA_3_EXE', 'original lineage replaced')
    need(source['bytes'] == 425984 and source['sha256'] == EXE_SHA256, 'original program mismatch')
    need(source['source_spr_group_gzip_sha256'] == '4db7809de4197eb90cca6dc04bda8550025e022c8232e2ebb902db0e9faf0175', 'SPR origin mismatch')
    need(source['source_spr_group_count'] == len(groups) == 464, 'SPR catalog count mismatch')
    anchors = r['byte_anchors']
    need(anchors['table_operand_virtual_address'] == 4558376 and anchors['table_base_rva'] == 364072, 'physical indexed address mismatch')
    need(anchors['indexed_read_rva'] == 71013 and anchors['body_global_store_rva'] == 71038, 'instruction locus mismatch')
    need(anchors['indexed_read_instruction_sha256'] == '3235ecee8f3c7a3c791fb8152b1548907ceda72b2a557fff314a2b2764b0089c', 'source read instruction changed')
    need(anchors['body_store_instruction_sha256'] == '1dc7450b9ba867f2cca420feb52f7c958ab2c76591625ffd17db07310eaa7c70', 'source write instruction changed')
    need(anchors['create_message_body_global_rva'] == 20934812 and anchors['create_message_face_global_rva'] == 20936876, 'creation-field join mismatch')
    window = r['bounded_window']
    need(window['sampled_dwords'] == 32 and window['starting_at_referenced_address'] is True, 'not the bounded raw window')
    need(all(window[x] is False for x in ('actual_table_extent_verified','index_upper_bound_verified','actual_index_value_verified')), 'unverified native bounds promoted')
    rows = window['values']
    need(len(rows) == 32 and [x['relative_index'] for x in rows] == list(range(32)), 'missing/order-shifted source positions')
    values = [x['dword'] for x in rows]
    need(values == EXPECTED_VALUES, 'original numeric dwords modified')
    need(hashlib.sha256(struct.pack('<32I', *values)).hexdigest() == WINDOW_SHA256 == window['window_sha256'], 'raw 128-byte numeric window hash mismatch')
    independent = classify_window(values, groups)
    need(rows == independent, 'original SPR group joins differ from independent replay')
    need(values[:12] == list(range(100000,100240,20)), 'twelve source keys drift')
    need(all(v in groups for v in values[:12]) and values[12] not in groups, 'source key boundary drift')
    need(all(not x['same_build_role_or_portrait_verified'] and not x['runtime_selected_index_verified'] for x in rows), 'sourced values falsely named as character')
    facts = r['findings']
    need(facts['sampled_group_key_matches'] == sum(x['matches_original_spr_group_key'] for x in rows) == 12, 'group hit count incorrect')
    need(facts['sampled_animation_interval_members'] == sum(x['within_compiled_animation_key_interval'] for x in rows) == 12, 'animation span count incorrect')
    for name in ('original_character_count','selected_bitmap','selected_body_number','selected_face_number','selected_spr_group'):
        need(facts[name] is None, 'unproven actual value: ' + name)
    for name in ('original_character_roster_verified','original_client_executed','server_create_accepted','table_covers_every_character'):
        need(facts[name] is False, 'unproven historical assertion: ' + name)
    return {'original_source_exe_sha256': EXE_SHA256, 'source_window_sha256': WINDOW_SHA256,
            'verified_sampled_dwords': 32, 'matching_consecutive_spr_group_keys': 12,
            'matched_spr_key_range': [100000,100220], 'next_raw_dword':198,
            'actual_table_length':None, 'runtime_selectable_character_total':None,
            'original_character_roster_verified':False, 'native_code_executed':False}

def verify():
    b = PATH.read_bytes()
    need(hashlib.sha256(b).hexdigest() == EXPECTED_SHA256 and git_blob(b) == EXPECTED_BLOB, 'permanent original-derived JSON differs from actual source artifact')
    raw = json.loads(b)
    output = accept_record(raw, source_groups())
    sources = load()
    join = qualify(sources[LOGIN], sources[ANIM])
    need(join['body_writer_bounded_source']['indexed_table_va'] == raw['byte_anchors']['table_operand_virtual_address'], 'source/consumer indexed address mismatch')
    need(join['body_writer_bounded_source']['source_read_rva'] == raw['byte_anchors']['indexed_read_rva'], 'source/consumer read mismatch')
    need(join['body_writer_bounded_source']['source_store_rva'] == raw['byte_anchors']['body_global_store_rva'], 'source/consumer store mismatch')
    need(join['create_message']['body_global_rva'] == raw['byte_anchors']['create_message_body_global_rva'], 'source/consumer destination mismatch')
    output['permanent_derived_sha256'] = EXPECTED_SHA256
    output['permanent_derived_git_blob'] = EXPECTED_BLOB
    output['old_login_and_animation_crosswalk_verified'] = True
    return output

if __name__ == '__main__':
    print(json.dumps(verify(),ensure_ascii=False,sort_keys=True,indent=2))
