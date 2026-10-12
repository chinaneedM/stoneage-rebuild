"""Original-byte-only R8 helper probe. No execution or disassembly emission."""
import argparse,json,tempfile
from pathlib import Path
from tools.stoneage_tw10_savedata_argtrace_r7 import inspect_verified as inspect_r7
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_instruction_probe import RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row
SCHEMA='tw10-r8-original-bounded-helper-effects'
STATUS='PINNED_ORIGINAL_STATIC_HELPER_EFFECTS_NOT_NATIVE_IO'
ROOT=0x4b8a4

def inspect_verified(runtime,savedata):
    r7=inspect_r7(runtime,savedata)
    if (r7['trace']['visited_states']!=136 or len(r7['trace']['calls'])!=8
        or r7['trace']['state_limit_hit'] or not any(c['rva']==0x4879a and c['target_rva']==ROOT for c in r7['trace']['calls'])):
        raise ValueError('accepted original R7 caller/root changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,_=image_layout(p)
    t=next(s for s in sections if s['name']=='.text');raw=data[t['raw']:t['raw']+t['raw_size']]
    if len(raw)!=t['raw_size']:raise ValueError('raw text truncated')
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r7_caller_rva':0x4879a,'r7_verified_trace_states':136,
            'helper':summarize(Decoder(raw,t['rva'],base),ROOT),
            'historical_helper_effect_summary_accepted':False,'caller_resumption_admitted':False,
            'filename_api_link_proven':False,'handle_buffer_size_link_proven':False,
            'native_io_executed':False,'fixed_128_byte_schema_proven':False,'original_bytes_published':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--bin',type=Path,required=True);args=p.parse_args()
    img,rows,_,_=find_rows(args.bin)
    try:
        paths={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe=Path(td)/'sa_3.exe';save=Path(td)/'savedata.dat'
            extract_row(img,paths[RUNTIME_PATH],exe);extract_row(img,paths[SAVEDATA_PATH],save)
            report=inspect_verified(exe.read_bytes(),save.read_bytes())
    finally:img.close()
    print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
