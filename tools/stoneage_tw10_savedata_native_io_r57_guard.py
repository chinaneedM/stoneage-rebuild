"""Strict inventory/source replay; original/artifact custody checked separately."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r57 import *
from tools.stoneage_tw10_savedata_native_io_r45_guard import graph_nodes
from tools.stoneage_tw10_savedata_native_io_r40_guard import rows_guard,suffix_guard
from tools.stoneage_tw10_savedata_native_io_r42_guard import inputs_guard
from tools.stoneage_tw10_savedata_native_io_r41_guard import identity_guard
from tools.stoneage_tw10_savedata_application_r51 import same
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def req(ok,why):
    if not ok:raise ValueError('R57 '+why)

def validate(d):
    req(d.get('schema')==SCHEMA and d.get('static_only') is True and d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256 and d.get('r54_exact_original_report_sha256')==PRIOR_SHA and d.get('r42_write_graph_effects_and_retained_shapes_exact_requalified') is True and d.get('entrygraph_node_limit_hit') is False and all(d.get(k) is False for k in FLAGS),'source/non-promotion')
    cs=d.get('contexts');req(isinstance(cs,list) and len(cs)==2,'contexts')
    for c,(call,root) in zip(cs,SPECS):
        req(c.get('caller_site_rva')==call and c.get('root_candidate_rva')==root and c.get('entrygraph_caller_edge_seen') is True and c.get('entrygraph_boundary_seen') is True,'caller support')
        identity_guard(c['savedata_caller_identity'],call);req(c['savedata_caller_identity']['direct_target_rva']==root,'caller target')
        ats=graph_nodes(c,root,True);rows=c['instruction_shapes'];keys={(r['site_rva'],reg) for r in rows for reg in r['input_query_registers']};rows_guard(rows,256,root,root+768,keys,False,ats)
        req([r['site_rva'] for r in rows]==ats and c.get('instruction_shapes_truncated') is False,'complete rows')
        calls=c['call_contexts'];req(len(calls)<=16 and [x['site_rva'] for x in calls]==[r['site_rva'] for r in rows if r['mnemonic']=='call'],'complete calls')
        for x in calls:
            at=x['site_rva'];identity_guard(x['identity'],at);ks,cap=inputs_guard(x['input_sources'],root,ats);suffix_guard(x['physical_push_suffix'],root,at,set(ks),cap);rows_guard(x['direct_input_definition_shapes'],24,root,root+768,set(ks),cap,ats)
            req(x.get('actual_argument_values_roles_return_or_callee_effects_proven') is False,'call promotion')
        req(same(c.get('return_analysis'),analyze(c)),'return/source replay')
    def ban(o):
        if isinstance(o,dict):
            req(not(set(o)&FORBIDDEN),'payload')
            for v in o.values():ban(v)
        elif isinstance(o,list):
            for v in o:ban(v)
    ban(d);return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);a=p.parse_args();req(a.report.stat().st_size<=1000000,'report bound');validate(json.loads(a.report.read_text()));print('TW10_R57_STATIC_WRITE_CLOSE=PASS; ACTUAL_NATIVE_PERSISTENCE=OPEN')
if __name__=='__main__':main()
