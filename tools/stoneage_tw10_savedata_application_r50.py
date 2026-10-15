"""Metadata-only application inventory; no original program or decoder needed."""
import argparse
import hashlib
import json
from pathlib import Path

PINNED_SHA256='0badd1423f403a9e8a246a40518a68ee5a1bd67d380ea7ab3460fc3c607c3e94'
SOURCE_SCHEMA='tw10-r50-original-savedata-read-caller-application-consumers-processing-entry'
SCHEMA='tw10-r50-pinned-application-consumer-inventory'

def derive(raw,expected_sha=PINNED_SHA256):
    if len(raw)>500000 or hashlib.sha256(raw).hexdigest()!=expected_sha:
        raise ValueError('source custody')
    d=json.loads(raw)
    if d.get('schema')!=SOURCE_SCHEMA or d.get('static_only') is not True:
        raise ValueError('source schema')
    for k,v in d.items():
        if (k.startswith('actual_') or k in ('native_io_executed','original_bytes_published')) and v is not False:
            raise ValueError('source promotion')
    c=d['caller_context']; rows=c['literal_effect_input_shapes']; sites=[r['site_rva'] for r in rows]
    if sites!=c['bounded_node_rvas'] or sites!=sorted(set(sites)) or len(rows)>256:
        raise ValueError('incomplete or duplicate caller inventory')
    if any(r.get('actual_instruction_effect_or_value_known') is not False for r in rows):
        raise ValueError('instruction promotion')
    after=[r for r in rows if r['site_rva']>0x40189]
    compares=[]; literals=[]; memory=[]
    for r in after:
        ops=r['operands']
        if r['mnemonic'] in ('cmp','test'):
            compares.append(r)
        if r['mnemonic']=='mov' and len(ops)==2 and ops[0]['kind']=='register' and ops[1]['kind']=='immediate':
            literals.append(r)
        for i,o in enumerate(ops):
            if o['kind']=='memory':
                memory.append({'site_rva':r['site_rva'],'operand_index':i,'mnemonic':r['mnemonic'],'operand':o})
    p=d['processing_entry_context']
    return {'schema':SCHEMA,'source_sha256':expected_sha,'static_only':True,
            'actual_schema_length_tag_migration_or_buffer_alias_proven':False,
            'post_processing_comparisons':compares,'post_processing_register_literal_definitions':literals,
            'post_processing_memory_operands':memory,
            'processing_physical_suffix':c['processing_call_context']['physical_push_suffix'],
            'caller_address_stack_unknowns':c['address_stack_state_queries'],
            'caller_graph':c['graph'],'processing_graph':p['graph'],
            'processor_memory_control_sample':{'total':p['memory_control_shape_count'],'retained':len(p['memory_control_shapes']),
                'truncated':p['memory_control_shapes_truncated']}}

def validate(contract,raw,expected_sha=PINNED_SHA256):
    if contract!=derive(raw,expected_sha):raise ValueError('consumer contract differs from pinned source')
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    if a.report.stat().st_size>500000:raise ValueError('report bound')
    print(json.dumps(derive(a.report.read_bytes()),sort_keys=True,indent=2))

if __name__=='__main__':main()
