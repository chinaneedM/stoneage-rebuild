"""Independent reverse-source audit of complete R57 return inventories."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_return_r57 import analyze
from tools.stoneage_tw10_savedata_native_io_r52_guard import reverse_sources

def audit(c):
    analysis=c['return_analysis']
    if json.dumps(analysis,sort_keys=True,separators=(',',':'))!=json.dumps(analyze(c),sort_keys=True,separators=(',',':')):raise ValueError('R57 analysis replay')
    rows=c['instruction_shapes'];edges=c['bounded_edges'];root=c['root_candidate_rva'];checked=set()
    for ret in analysis['return_contexts']:
        for q in ret['eax_source_graph']['queries']:
            expected=reverse_sources(rows,edges,root,q['site_rva'],q['register'],False);actual={(s['origin'],s['site_rva']) for s in q['source_candidates']}
            if expected!=actual:raise ValueError('R57 independent reverse return-source mismatch')
            checked.add((q['site_rva'],q['register']))
    return len(checked)

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    if a.report.stat().st_size>1000000:raise ValueError('R57 report bound')
    d=json.loads(a.report.read_text())
    from tools.stoneage_tw10_savedata_native_io_r57_guard import validate
    validate(d);count=sum(audit(c) for c in d['contexts']);print('TW10_R57_INDEPENDENT_REVERSE_RETURNS=PASS; QUERIES='+str(count)+'; ACTUAL_NATIVE_PERSISTENCE=OPEN')
if __name__=='__main__':main()
