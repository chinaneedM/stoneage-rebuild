"""Pinned numeric writer/read correspondence, conditional hardware geometry only."""
import argparse,hashlib,json
from pathlib import Path
from tools.stoneage_tw10_savedata_application_r51 import effect,stack,coordinates,same
PIN='635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387'
SIZE=132329

def physical_pushes(rows,call):
    by={r['site_rva']:r for r in rows};before=[r for r in rows if r['site_rva']<call];out=[]
    # This local straight-line window is separately checked by exact graph edges.
    for r in reversed(before):
        m=r['mnemonic'];ops=r['operands']
        if m in ('call','ret','jmp','ljmp') or m.startswith('j'):break
        if m=='push':
            if len(ops)!=1 or ops[0]['width_bytes']!=4:raise ValueError('physical push width')
            out.append({'site_rva':r['site_rva'],'conditional_pre_call_esp_offset':4*len(out),'input':ops[0]})
            if len(out)>24:raise ValueError('push bound')
        elif effect(r)!=0:break
    return out

def derive(raw):
    if len(raw)!=SIZE or hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('R54 source custody')
    d=json.loads(raw);c=d['writer_context'];rs=c['instruction_shapes'];es=c['bounded_edges'];by={r['site_rva']:r for r in rs}
    p=next(x for x in d['prefix_direct_callee_contexts'] if x['caller_site_rva']==0x4005a)
    if p['root_candidate_rva']!=0x47010:raise ValueError('historical transform target')
    local=[r for r in rs if 0x4002a<=r['site_rva']<=0x4005a];sites={r['site_rva'] for r in local};edges=[e for e in es if set(e)<=sites]
    if edges!=[[a['site_rva'],b['site_rva']] for a,b in zip(local,local[1:])]:raise ValueError('straight-line prefix')
    pushes=physical_pushes([r for r in local if r['site_rva']>=0x40040],0x4005a)
    if [x['site_rva'] for x in pushes]!=[0x40058,0x40056,0x40050,0x4004f,0x4004e,0x40040]:raise ValueError('six physical pushes')
    states,cap=stack(local,edges,0x4002a);end=states[0x4005a];leas=[]
    for r in local:
        if r['mnemonic']!='lea':continue
        o=r['operands'];g=o[1].get('geometry',{})
        if g.get('base_register')=='esp' and g.get('index_register') is None:
            leas.append({'site_rva':r['site_rva'],'register':o[0]['register'],'conditional_pre_call_esp_relative_address':states[r['site_rva']]+g['relative_field_offset']-end})
    coord=coordinates(p['instruction_shapes'],p['bounded_edges'],0x47010,pushes)
    return {'schema':'tw10-r54-pinned-conditional-writer-read-correspondence','source_sha256':PIN,
      'local_straight_line_verified':True,'physical_push_window_start_rva':0x40040,'physical_pushes':pushes,'conditional_caller_lea_coordinates':leas,
      'processor_entry_coordinates':coord,
      'copy_syntax':{'dword_repeat_count_literal':31,'word_copy_width':2,'byte_copy_width':1,'conditional_total_if_rep_count_direction_segments_and_addresses_valid':127,'original_bytes_or_direction_flag_proven':False},
      'conditional_slot_roles':{'entry_plus4':'input pointer shaped','entry_plus8':'input count shaped literal127','entry_plus12':'seed shaped literal0','entry_plus16':'output pointer shaped','entry_plus20':'output count pointer shaped','entry_plus24':'capacity shaped literal4000'},
      'comparison_to_r53':{'writer_count_plus_one_site_rva':0x4701c,'writer_output_count_store_site_rva':0x47068,'writer_byte_accumulator_add_site_rva':0x47090,'writer_not_site_rva':0x470c2,'writer_key_insert_site_rva':0x47124,'writer_suffix_add_site_rva':0x47140,'reader_count_minus_one_site_rva':0x4716a,'reader_suffix_sub_site_rva':0x471fb,'candidate_only':True},
      'local_stack_cap_hit':cap,'actual_bytes_copy_size_inverse_schema_migration_or_persistence_proven':False,
      'historical_writer_equals_invented_inverse_for_arbitrary_key_proven':False,
      'open':['REP direction/segment/register values','stack helper0x49160 actual frame effect','opaque open/write/close effects','writer mutates its input before output','key is input dependent, not arbitrary invented inverse key','signed division and capacity/error paths','full numerical inverse verification on invented fixtures pending']}

def validate(contract,raw):
    if not same(contract,derive(raw)):raise ValueError('R54 contract mismatch')
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--verify',type=Path);a=p.parse_args();raw=a.source.read_bytes();d=derive(raw)
    if a.verify:validate(json.loads(a.verify.read_text()),raw);print('TW10_R54_CONTRACT=PASS; ACTUAL_INVERSE=OPEN')
    else:print(json.dumps(d,sort_keys=True))
if __name__=='__main__':main()
