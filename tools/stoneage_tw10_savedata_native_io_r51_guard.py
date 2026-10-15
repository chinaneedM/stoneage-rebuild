"""R51 graph-complete numeric inventory and conditional consumer replay guard."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r51 import *
from tools.stoneage_tw10_savedata_native_io_r40_guard import rows_guard
from tools.stoneage_tw10_savedata_native_io_r42_guard import inputs_guard
from tools.stoneage_tw10_savedata_application_r51 import same
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def require(ok,why):
    if not ok:raise ValueError('R51 '+why)

def validate(d):
    require(d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema/status')
    require(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256 and d.get('static_only') is True and d.get('r50_exact_original_revalidated') is True and d.get('r50_exact_report_sha256')==PRIOR_SHA256 and all(d.get(k) is False for k in FLAGS),'source/non-promotion')
    prior=d.get('r50_snapshot',{});validate_r50(prior);p=prior['processing_entry_context'];ats=p['bounded_node_rvas'];rows=d.get('processor_instruction_shapes')
    require(isinstance(rows,list) and [r['site_rva'] for r in rows]==ats and type(d.get('processor_instruction_count')) is int and d['processor_instruction_count']==len(rows) and d.get('processor_instruction_shapes_truncated') is False,'complete inventory')
    keys={(r['site_rva'],reg) for r in rows for reg in r['input_query_registers']};rows_guard(rows,256,ROOT,ROOT+768,keys,False,ats)
    by={r['site_rva']:r for r in rows}
    for r in p['early_frame_shapes']+p['memory_control_shapes']:require(same(by[r['site_rva']],r),'prior row equality')
    selected=[r for r in rows if r['mnemonic'] in ('cmp','test') or any(o['kind']=='memory' for o in r['operands'])]
    require(len(selected)==p['memory_control_shape_count'] and same(selected[:32],p['memory_control_shapes']),'prior sample/total agreement')
    s=d.get('processor_division_source_surface',{});keys,cap=inputs_guard(s.get('input_sources',{}),ROOT,ats)
    divs=[r for r in rows if r['mnemonic'] in ('div','idiv')];require(len(divs)<=8 and (queries_for(divs)<=set(keys) or cap),'division source queries')
    sites=sorted({t['rva'] for q in s['input_sources']['queries'] for t in q['reaching_candidates'] if t['origin']=='definition'})
    shapes=s.get('source_definition_shapes');rows_guard(shapes,24,ROOT,ROOT+768,keys,cap,ats)
    require(s.get('source_definition_count')==len(sites) and s.get('source_definitions_truncated') is (len(sites)>24) and s.get('source_expansion_rounds')==2,'source bounds')
    require(all(same(by[r['site_rva']],r) for r in shapes) and [r['site_rva'] for r in shapes]==[a for a in sites[:24] if a in {r['site_rva'] for r in shapes}],'definition agreement')
    require(s.get('source_expansion_pending_definition_rvas')==[a for a in sites if a not in {r['site_rva'] for r in shapes}],'source pending replay')
    require(same(d.get('conditional_consumer_analysis'),analyze(prior,rows,p['bounded_edges'])),'consumer replay')
    def ban(o):
        if isinstance(o,dict):
            require(not(set(o)&FORBIDDEN),'original payload')
            for v in o.values():ban(v)
        elif isinstance(o,list):
            for v in o:ban(v)
    ban(d);return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);path=p.parse_args().report
    require(path.stat().st_size<=1000000,'report bound');validate(json.loads(path.read_text()));print('TW10_R51_STRICT_STATIC=PASS; ACTUAL_SAVE_SCHEMA=OPEN')
if __name__=='__main__':main()
