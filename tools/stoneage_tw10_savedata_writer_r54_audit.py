"""Independent legacy stack algorithm against full R54 numeric inventories."""
import argparse,hashlib,json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r54_guard import validate as primary
from tools.stoneage_tw10_savedata_native_io_r50 import inventory_effect
from tools.stoneage_tw10_savedata_native_io_r38 import stack_states,state_summary
from tools.stoneage_tw10_savedata_application_r51 import stack

def validate(d):
    primary(d);checked=0
    for c in [d['writer_context']]+d['prefix_direct_callee_contexts']:
        rows=c['instruction_shapes'];edges=c['bounded_edges'];root=c['root_candidate_rva']
        first,limited=stack(rows,edges,root)
        second,updates,cap=stack_states([inventory_effect(r) for r in rows],edges,root)
        for r in rows:
            at=r['site_rva'];v=state_summary(second,at,cap)['unique_conditional_esp_delta']
            if first.get(at)!=v:raise ValueError('R54 independent stack disagreement')
            checked+=1
        # A complete published arithmetic inventory must not silently hide a frontier.
        if c['graph']['node_limit_hit'] or c['graph']['frontier']:raise ValueError('R54 incomplete bounded inventory requires scoped follow-up')
    for c in d['prefix_direct_callee_contexts']:
        if c.get('entrygraph_call_edge_seen') is not True or c.get('entrygraph_boundary_seen') is not True:raise ValueError('R54 original call support')
    if d.get('normalization_call_edge_seen') is not True or d.get('entrygraph_node_limit_hit') is not False:raise ValueError('R54 normalization support')
    return checked

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    if a.report.stat().st_size>1000000:raise ValueError('R54 report bound')
    print('TW10_R54_INDEPENDENT_STACK=PASS; SITES='+str(validate(json.loads(a.report.read_text())))+'; ACTUAL_INVERSE_SCHEMA=OPEN')
if __name__=='__main__':main()
