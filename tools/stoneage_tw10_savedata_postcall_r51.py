"""Pinned numeric metadata: conditional normal-return stack geometry only."""
import argparse,hashlib,json
from pathlib import Path
from tools.stoneage_tw10_savedata_application_r51 import stack,same
PINNED_SHA256='15f54e5de8d1d20128fb7d948b54f13a0e3f6cf372eca203cbc7bb8adc473052'
SCHEMA='tw10-r51-original-complete-processor-caller-conditional-stack-consumers'

def return_candidates(rows,edges,root):
    states,limited=stack(rows,edges,root);outgoing={a for a,b in edges};exits=[r for r in rows if r['site_rva'] not in outgoing];out=[]
    for r in exits:
        ops=r['operands'];cleanup=0 if not ops else ops[0].get('constant') if len(ops)==1 and ops[0].get('kind')=='immediate' else None
        delta=states.get(r['site_rva']);ok=r['mnemonic']=='ret' and type(cleanup) is int and 0<=cleanup<=65535 and type(delta) is int and not limited
        out.append({'exit_rva':r['site_rva'],'mnemonic':r['mnemonic'],'conditional_net_near_call_esp_delta':delta+cleanup if ok else None,'actual_return_or_calling_convention_proven':False})
    return out

def derive(raw,expected_sha=PINNED_SHA256):
    if len(raw)>1000000 or hashlib.sha256(raw).hexdigest()!=expected_sha:raise ValueError('source custody')
    d=json.loads(raw)
    if d.get('schema')!=SCHEMA or d.get('static_only') is not True:raise ValueError('source schema')
    prior=d['r50_snapshot'];p=prior['processing_entry_context'];g=p['graph'];rows=d['processor_instruction_shapes']
    if [r['site_rva'] for r in rows]!=p['bounded_node_rvas']:raise ValueError('inventory membership')
    exits=return_candidates(rows,p['bounded_edges'],0x47160)
    normal=bool(exits) and g['node_limit_hit'] is False and not g['frontier'] and all(e['conditional_net_near_call_esp_delta'] is not None for e in exits)
    deltas=sorted({e['conditional_net_near_call_esp_delta'] for e in exits if e['conditional_net_near_call_esp_delta'] is not None})
    c=prior['caller_context'];load=next(r for r in c['literal_effect_input_shapes'] if r['site_rva']==0x4018e)
    ops=load['operands'];geo=ops[1].get('geometry') if len(ops)==2 else None
    qualified=load['mnemonic']=='mov' and geo and geo['base_register']=='esp' and geo['index_register'] is None and geo['segment_register'] is None and type(geo['relative_field_offset']) is int
    offsets=sorted({geo['relative_field_offset']+n for n in deltas}) if qualified and normal else []
    leas=[x for x in d['conditional_consumer_analysis']['caller_local_lea_coordinates'] if x['conditional_address_relative_pre_call_esp'] in offsets]
    return {'schema':'tw10-r51-conditional-normal-return-caller-coordinate-contract','source_sha256':expected_sha,
            'normal_return_exit_candidates':exits,'all_bounded_graph_exits_qualified_normal_ret_syntax':bool(normal),
            'conditional_normal_return_net_esp_delta_candidates':deltas,'caller_post_call_load_pre_call_offset_candidates':offsets,
            'candidate_matching_caller_lea_coordinates':leas,'near_call_return_address_geometry_only':True,
            'actual_stack_alias_processor_output_length_schema_or_execution_proven':False}

def validate(contract,raw,expected_sha=PINNED_SHA256):
    if not same(contract,derive(raw,expected_sha)):raise ValueError('postcall contract differs')
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    if a.report.stat().st_size>1000000:raise ValueError('report bound')
    print(json.dumps(derive(a.report.read_bytes()),sort_keys=True,indent=2))
if __name__=='__main__':main()
