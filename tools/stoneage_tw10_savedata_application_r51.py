"""Pure numeric replay of conditional stack coordinates and consumer surfaces."""
from collections import deque
import json

ROOT=0x47160
PROCESS=0x40189

def effect(row):
    m=row['mnemonic'];o=row['operands'];writes=set(row['decoder_written_registers'])
    if m in ('call','lcall'):return None
    if m in ('push','pop') and len(o)==1:
        if o[0]['width_bytes'] not in (2,4) or (m=='pop' and o[0].get('register') in ('esp','sp')):return None
        return o[0]['width_bytes']*(-1 if m=='push' else 1)
    if m in ('add','sub') and len(o)==2 and o[0].get('register')=='esp' and o[0]['width_bytes']==4 and o[1]['kind']=='immediate' and type(o[1]['constant']) is int and 0<=o[1]['constant']<=4096:
        return o[1]['constant']*(1 if m=='add' else -1)
    if writes&{'esp','sp','spl'} or m in ('enter','leave'):return None
    return 0

def stack(rows,edges,root):
    by={r['site_rva']:r for r in rows}
    if root not in by or len(by)!=len(rows) or len(rows)>256:raise ValueError('stack inventory')
    adj={a:[] for a in by}
    for a,b in edges:
        if a not in by or b not in by:raise ValueError('stack edge membership')
        adj[a].append(b)
    # None represents unknown. More than eight offsets becomes unknown monotonically.
    states={root:{0}};todo=deque([root]);updates=0
    while todo and updates<8192:
        a=todo.popleft();delta=effect(by[a]);s=states[a]
        out={None} if delta is None or None in s else {v+delta for v in s}
        if len(out)>8 or any(v is not None and abs(v)>4096 for v in out):out={None}
        for b in adj[a]:
            new=states.get(b,set())|out
            if None in new or len(new)>8:new={None}
            if new!=states.get(b,set()):states[b]=new;todo.append(b)
        updates+=1
    return {a:next(iter(s)) if len(s)==1 and None not in s and not todo else None for a,s in states.items()},bool(todo)

def coordinates(rows,edges,root,pushes):
    states,limited=stack(rows,edges,root);slots={p['conditional_pre_call_esp_offset']:p for p in pushes};refs=[]
    for r in rows:
        for i,o in enumerate(r['operands']):
            g=o.get('geometry') or {}
            if o['kind']!='memory' or g.get('base_register')!='esp' or g.get('index_register') is not None or g.get('segment_register') is not None:continue
            delta=states.get(r['site_rva']);disp=g.get('relative_field_offset');offset=delta+disp if type(delta) is int and type(disp) is int else None
            slot=offset-4 if type(offset) is int else None
            refs.append({'site_rva':r['site_rva'],'operand_index':i,'width_bytes':o['width_bytes'],'decoder_read':o['decoder_read'],'decoder_write':o['decoder_write'],
                         'conditional_entry_esp_offset':offset,'conditional_caller_pre_call_slot_offset':slot,
                         'matching_physical_push':slots.get(slot),'actual_stack_value_abi_or_alias_proven':False})
    return {'references':refs,'state_update_limit_hit':limited,'actual_call_entry_esp_or_stack_values_proven':False}

def analyze(prior,rows,edges):
    c=prior['caller_context'];pushes=c['processing_call_context']['physical_push_suffix']['pushes']
    selected=[r for r in rows if r['mnemonic'] in ('cmp','test') or any(o['kind']=='memory' for o in r['operands'])]
    local=[r for r in c['literal_effect_input_shapes'] if 0x40177<=r['site_rva']<=PROCESS]
    local_sites={r['site_rva'] for r in local};local_edges=[e for e in c['bounded_edges'] if set(e)<=local_sites]
    states,limited=stack(local,local_edges,0x40177);end=states.get(PROCESS);leas=[]
    for r in local:
        if r['mnemonic']!='lea' or len(r['operands'])!=2:continue
        g=r['operands'][1].get('geometry') or {};start=states.get(r['site_rva']);disp=g.get('relative_field_offset')
        if g.get('base_register')=='esp' and g.get('index_register') is None and g.get('segment_register') is None:
            offset=start+disp-end if all(type(v) is int for v in (start,disp,end)) else None
            leas.append({'site_rva':r['site_rva'],'destination_register':r['operands'][0].get('register'),'conditional_address_relative_pre_call_esp':offset,'actual_address_or_post_call_alias_proven':False})
    return {'processor_entry_stack_coordinates':coordinates(rows,edges,ROOT,pushes),'processor_memory_control_total':len(selected),
            'new_memory_control_shapes_after_r50_sample':selected[32:],
            'processor_arithmetic_shapes':[r for r in rows if r['mnemonic'] in ('xor','add','sub','imul','mul','div','idiv','neg','not','and','or','shl','shr','sar','sal','cdq','cwd','xchg')],
            'application_zf_contexts':[b for b in c['post_read_zf_branch_contexts'] if b['branch_site_rva']>=PROCESS+5],
            'caller_local_lea_coordinates':leas,'caller_local_stack_limit_hit':limited,
            'post_call_esp_change_assumed_zero_or_output_binding_proven':False,
            'actual_schema_length_version_migration_or_algorithm_proven':False}

def same(a,b):return json.dumps(a,sort_keys=True,separators=(',',':'))==json.dumps(b,sort_keys=True,separators=(',',':'))
