"""R34 pinned TW1.0 static CMP/TEST operand provenance and CloseHandle pre-call PUSH.

Never executes historical bytes, evaluates API results or promotes conditional ABI.
"""
import argparse, hashlib, json, tempfile
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r33 import (
    inspect_verified as inspect_r33, RUNTIME_SHA256, SAVEDATA_SHA256,
    PARENT, SECONDARY, BRANCHES, FLAGS as R33_FLAGS,
)
from tools.stoneage_tw10_savedata_native_io_r33_guard import validate as validate_r33
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface, ALIASES
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_upstream_r23 import local_push_suffix
from tools.stoneage_tw10_savedata_write_shapes_r17 import operand_shape
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = 'tw10-r34-original-cmp-test-closehandle-input-provenance'
STATUS = 'PINNED_ORIGINAL_CONDITIONAL_PRE_CLOSEHANDLE_INPUTS_NATIVE_SAVE_OPEN'
PRIOR_SHA256 = '1be7d372b0650b9944a12264b612531d46a5326af3628e12363df365ddab98b5'
CMP = 0x4ed09
TEST = 0x4ed14
CALL = SECONDARY
ANCHOR = 0x4ed07
MAX_PUSHES = 24
FLAGS = tuple(R33_FLAGS) + (
    'actual_edi_sentinel_or_valid_handle_proven',
    'actual_closehandle_argument_or_api_result_proven',
    'original_error_branch_taken_or_owner_known',
    'native_filename_to_handle_to_io_schema_proven',
)

def shape(dec, sections, site, mnemonic, expected_regs):
    ins = dec.at(site)
    if ins is None or ins.mnemonic != mnemonic or len(ins.operands)!=len(expected_regs):
        raise ValueError('R34 original mnemonic/operands changed')
    ops = [operand_shape(ins,op,sections,dec.base) for op in ins.operands]
    if any(o.get('kind')!='register' or o.get('width_bytes')!=4 or o.get('register')!=reg
           for o,reg in zip(ops,expected_regs)):
        raise ValueError('R34 pinned register-only source changed')
    return {'site_rva':site,'mnemonic':mnemonic,'operands':ops,
            'actual_inputs_or_predicate_value_proven':False}

def close_suffix(dec,sections,imports):
    identity = call_identity(dec,CALL,imports,sections)
    if identity['import_identity']!={'dll':'KERNEL32.dll','name':'CloseHandle','iat_rva':0x520a8}:
        raise ValueError('R34 original CloseHandle import changed')
    suffix=local_push_suffix(dec,sections,ANCHOR,CALL)
    if not suffix['linear_call_boundary_reached']:
        raise ValueError('R34 caller suffix did not reach CloseHandle')
    pushes=[]
    for p in suffix['pushes']:
        op=p['input']
        regs = ([op['register']] if op['kind']=='register' and op['register'] in ALIASES else
                [r for r in (op.get('geometry',{}).get('base_register'),
                             op.get('geometry',{}).get('index_register')) if r in ALIASES])
        pushes.append({**p,'source_queries':[{'site_rva':p['site_rva'],'register':r}
                                             for r in sorted(set(regs))],
                       'actual_argument_role_or_value_proven':False})
    return identity,suffix,pushes

def derive(dec,sections,imports,prior):
    nodes,edges,front,hit=candidate_graph(dec,PARENT)
    if not {CMP,TEST,CALL} <= set(nodes):
        raise ValueError('R34 sites missing from bounded parent graph')
    old=prior['branch_flag_contexts']
    if len(old)!=2 or old[0]['source_candidates'][0]['site_rva']!=CMP or old[1]['source_candidates'][0]['site_rva']!=TEST:
        raise ValueError('R34 R33 historical predicate shape differs')
    checks=[shape(dec,sections,CMP,'cmp',('esi','edi')),
            shape(dec,sections,TEST,'test',('eax','eax'))]
    ident,suffix,pushes=close_suffix(dec,sections,imports)
    queries={(CMP,'esi'),(CMP,'edi'),(TEST,'eax'),(CALL,'esi'),(CALL,'eax')}
    for p in pushes:
        queries.update((q['site_rva'],q['register']) for q in p['source_queries'])
    inputs=input_surface(dec,sections,nodes,edges,PARENT,queries)
    return {'schema':SCHEMA,'status':STATUS,
            'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r33_exact_original_revalidated':True,'r33_exact_report_sha256':PRIOR_SHA256,
            'static_only':True,'parent_graph':graph_meta(nodes,edges,front,hit),
            'predicate_operands':checks,'closehandle_identity':ident,
            'closehandle_pre_call_suffix':suffix,'closehandle_push_candidates':pushes,
            'register_sources':inputs,'actual_stack_frames_paths_values_or_returns_proven':False,
            **{k:False for k in FLAGS}}

def inspect_verified(runtime,savedata):
    old=inspect_r33(runtime,savedata)
    validate_r33(old)
    digest=hashlib.sha256((json.dumps(old,sort_keys=True)+'\n').encode()).hexdigest()
    if digest!=PRIOR_SHA256:raise ValueError('R33 exact original derivative changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for section,raw in zip(sections,pe.sections):
        section['characteristics']=int(raw.Characteristics)
    text=next(s for s in sections if s['name']=='.text')
    dec=Decoder(data[text['raw']:text['raw']+text['raw_size']],text['rva'],base)
    return derive(dec,sections,imports,old)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bin',type=Path,required=True);args=ap.parse_args()
    image,rows,_,_=find_rows(args.bin)
    try:
        files={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe,save=Path(td)/'sa_3.exe',Path(td)/'savedata.dat'
            extract_row(image,files[RUNTIME_PATH],exe)
            extract_row(image,files[SAVEDATA_PATH],save)
            report=inspect_verified(exe.read_bytes(),save.read_bytes())
    finally:image.close()
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__':main()
