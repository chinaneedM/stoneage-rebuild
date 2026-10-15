"""Strict bounded inventory, physical source and independent conditional stack replay."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r54 import *
from tools.stoneage_tw10_savedata_native_io_r45_guard import graph_nodes
from tools.stoneage_tw10_savedata_native_io_r40_guard import rows_guard,suffix_guard
from tools.stoneage_tw10_savedata_native_io_r42_guard import inputs_guard
from tools.stoneage_tw10_savedata_native_io_r41_guard import identity_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN
from tools.stoneage_tw10_savedata_application_r51 import same

def require(ok,why):
    if not ok:raise ValueError('R54 '+why)

def validate(d):
    require(d.get('schema')==SCHEMA and d.get('static_only') is True and d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256 and d.get('r51_exact_original_report_sha256')==PRIOR_SHA and all(d.get(k) is False for k in FLAGS),'source/non-promotion')
    cs=d.get('prefix_direct_callee_contexts');require(isinstance(cs,list) and 1<=len(cs)<=8,'callee bound')
    caller=d['writer_context'];require(caller.get('root_candidate_rva')==ROOT,'writer root')
    for c in [caller]+cs:
        root=c['root_candidate_rva'];ats=graph_nodes(c,root,True);rows=c['instruction_shapes']
        keys={(r['site_rva'],reg) for r in rows for reg in r['input_query_registers']}
        rows_guard(rows,256,root,root+768,keys,False,ats)
        require([r['site_rva'] for r in rows]==ats and c.get('instruction_shapes_truncated') is False and type(c.get('entrygraph_boundary_seen')) is bool,'inventory')
        calls=c['call_contexts'];require(len(calls)<=16 and [x['site_rva'] for x in calls]==[r['site_rva'] for r in rows if r['mnemonic']=='call'],'calls')
        for call in calls:
            at=call['site_rva'];identity_guard(call['identity'],at);ks,cap=inputs_guard(call['input_sources'],root,ats)
            suffix_guard(call['physical_push_suffix'],root,at,set(ks),cap)
            rows_guard(call['direct_input_definition_shapes'],24,root,root+768,set(ks),cap,ats)
            require(call.get('actual_argument_values_roles_return_or_callee_effects_proven') is False,'call non-promotion')
    require(same(d.get('conditional_writer_analysis'),analyze(caller,cs)),'writer replay')
    prior=json.loads((Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R51-ORIGINAL.json').read_text())
    old=prior['r50_snapshot']['caller_context']['literal_effect_input_shapes'];normal=[r for r in old if 0x40195<=r['site_rva']<=0x401b6]
    require(same(d.get('normalization_shapes'),normal) and type(d.get('normalization_call_edge_seen')) is bool and type(d.get('entrygraph_node_limit_hit')) is bool,'normalization chain')
    prefix=[c for c in caller['call_contexts'] if c['site_rva']<0x40064 and c['identity']['direct_target_rva'] is not None]
    require([c['caller_site_rva'] for c in cs]==[c['site_rva'] for c in prefix],'complete direct prefix')
    def ban(o):
        if isinstance(o,dict):
            require(not(set(o)&FORBIDDEN),'payload')
            for v in o.values():ban(v)
        elif isinstance(o,list):
            for v in o:ban(v)
    ban(d);return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);path=p.parse_args().report
    require(path.stat().st_size<=1000000,'report bound');validate(json.loads(path.read_text()));print('TW10_R54_STATIC_WRITER=PASS; ACTUAL_INVERSE_SCHEMA_PERSISTENCE=OPEN')
if __name__=='__main__':main()
