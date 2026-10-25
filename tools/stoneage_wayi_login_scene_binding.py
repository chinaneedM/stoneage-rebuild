"""Join real login draw operands to original patch aliases, never to same-ID rows.

Original program/graphics are read as evidence only. No game execution or art
export; the static cross-specimen join does not authenticate a deployed build.
"""
import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = '4193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63'
WINDOWS = {'panel': (0x20c80,0x20ebf), 'queue': (0x822b0,0x823e7),
           'alias_lookup': (0x1fcd0,0x1fd0e), 'loader': (0x1f9d0,0x1fa8c),
           'offset_lookup': (0x1fb03,0x1fb2b)}
PATCH = 'research/recovered/wayi-adrn129-patch-metadata/INDEX-1-R1.tsv.gz'
NATIVE = 'research/recovered/adrn129-tw85-real-pair/NATIVE-R1.tsv.gz'
PAIRS = 'research/recovered/adrn129-tw85-real-pair/PAIRS-R1.tsv.gz'
EARLY = {'TW10':'research/recovered/tw10-resource-metadata/COLLISION-ATTR-R1.tsv.gz',
         'CN50':'research/recovered/cn50-resource-metadata/COLLISION-ATTR-R1.tsv.gz'}
PINS = {PATCH:'d8049cb6ce74a2c048372aa51fc81b6921a995b6fa45b03dd5511a93509958ca',
        NATIVE:'495928a0a44d7c81bf1d6ef7b06d26decfc5096803fbd60b9e8e0aa9752a45ce',
        PAIRS:'ee41e4266b3bbab162d9271c1b86cceaa85354e60ff3e389fffccd68010b1314',
        EARLY['TW10']:'d26b318ea73833bd7cc68abc8b5798a81b76ef9309cc91b137f7a55c6c8275dc',
        EARLY['CN50']:'4417afac7caffee86bf64ca36d9bfdff06fef61b9e3af200bf59b153280dc8df'}
IDS = (26301,26302,26303)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def observe(payload):
    """Semantic checks independent of the source's whole-file digest gate."""
    from capstone.x86 import X86_OP_IMM, X86_OP_REG
    from tools.stoneage_jss_launcher_deep_probe import parse_pe_layout
    from tools.stoneage_wayi_saupdate_route_probe import decode_window, raw_window
    layout = parse_pe_layout(payload)
    windows, decoded = {}, {}
    for label,(start,end) in WINDOWS.items():
        raw = raw_window(payload,layout,start,end)
        ins = decode_window(raw,0x400000+start)
        decoded[label] = ins
        windows[label] = {'start_rva':start,'end_rva_exclusive':end,
                         'sha256':hashlib.sha256(raw).hexdigest(),'instruction_count':len(ins)}
    by_rva = {i.address-0x400000:i for ins in decoded.values() for i in ins}

    def shape(rva, mnemonic, operands):
        i=by_rva.get(rva)
        need(i is not None and i.mnemonic==mnemonic and i.op_str==operands,
             'compiled semantic anchor changed: '+hex(rva))

    # No memory dereference or assumed actual UI state: this checks compiled
    # register setup and explicit argument encodings, not observed execution.
    shape(0x20c84,'xor','ebx, ebx')
    shape(0x20c91,'call','0x421200')
    shape(0x20ce0,'mov','dword ptr [esp + 0xc], 2')
    shape(0x20cbb,'mov','dword ptr [esp + 0xc], 1')
    shape(0x20e43,'mov','dword ptr [0x4bc054], eax')
    shape(0x20e90,'mov','dword ptr [0x4bc058], eax')
    shape(0x20e25,'cmp','esi, ebx')
    shape(0x20e72,'cmp','esi, ebx')
    shape(0x20e23,'je','0x420e4a')
    shape(0x20e27,'je','0x420e4a')
    shape(0x20e70,'je','0x420e97')
    shape(0x20e74,'je','0x420e97')
    shape(0x82302,'call','0x41fcd0')
    shape(0x82316,'call','0x41fab0')
    shape(0x1fcfb,'mov','edx, dword ptr [eax*4 + 0xa0b4dc]')
    shape(0x1f9db,'push','0x50')
    shape(0x1f9e7,'mov','ecx, 0x14')
    shape(0x1f9f3,'lea','ebp, [ebx + ebx*4]')
    shape(0x1f9f6,'shl','ebp, 4')
    shape(0x1fa01,'mov','ecx, dword ptr [esp + 0x5c]')
    shape(0x1fa54,'mov','dword ptr [ecx*4 + 0xa0b4dc], ebx')
    shape(0x1fb0d,'mov','cx, word ptr [eax + 0xe95aac]')
    shape(0x1fb1b,'mov','ax, word ptr [eax + 0xe95ab0]')

    def arguments(site,target):
        ins=decoded['panel'];index=next(j for j,i in enumerate(ins) if i.address==0x400000+site)
        shape(site,'call',hex(0x400000+target))
        prior=ins[index-5:index]
        need(len(prior)==5 and all(i.mnemonic=='push' for i in prior),'non-contiguous argument group')
        args=[]
        for i in reversed(prior):
            op=i.operands[0]
            if op.type==X86_OP_IMM:args.append(op.imm)
            elif op.type==X86_OP_REG and i.reg_name(op.reg)=='ebx':args.append({'entry_zero_register':'ebx','runtime_value_observed':False})
            else:raise ValueError('unsupported call argument')
        return args

    draws=[]
    for site,logical,flag,role in [(0x20e3b,26302,1,'SUBMIT_OVERLAY'),
                                   (0x20e88,26303,1,'EXIT_OVERLAY'),
                                   (0x20eae,26301,None,'PANEL_BACKGROUND')]:
        args=arguments(site,0x822b0)
        zero={'entry_zero_register':'ebx','runtime_value_observed':False}
        need(args==[320,240,zero,logical,zero if flag is None else flag], 'draw coordinates, logical alias or flags changed')
        draws.append({'role':role,'call_rva':site,'renderer_rva':0x822b0,'x':320,'y':240,
                      'logical_alias':logical,'priority_operand':zero,'hit_flag_operand':args[4],
                      'conditional_call_in_panel':flag is not None,'native_execution_observed':False})
    actual_calls=[i.address-0x400000 for i in decoded['panel'] if i.mnemonic=='call' and i.op_str=='0x4822b0']
    need(actual_calls==[x['call_rva'] for x in draws],'unexpected extra/missing graphics queue call')
    rects=[]
    for site,role,expected in [(0x20e14,'SUBMIT_OVERLAY',[320,225,410,350,-1]),
                               (0x20e66,'EXIT_OVERLAY',[412,232,494,372,-1])]:
        args=arguments(site,0x4ac50);need(args==expected,'hit rectangle changed')
        rects.append({'role':role,'call_rva':site,'arguments':args,'edge_inclusion':'NOT_DETERMINED'})
    return {'windows':windows,'draw_calls':draws,'button_hit_calls':rects,
            'alias_lookup_table_rva':0x60b4dc,'physical_record_stride':80,
            'alias_field_offset':76,'physical_offset_fields':[12,16]}


def negative_source_checks(payload):
    from tools.stoneage_jss_launcher_deep_probe import parse_pe_layout
    layout=parse_pe_layout(payload)
    cases={0x20e2c:'submit alias',0x20e79:'exit alias',0x20e9f:'background alias',
           0x20e37:'draw x',0x20e06:'submit hit edge',0x20e3c:'renderer call target',
           0x1fcfe:'alias table address',0x1f9dc:'record size',0x1fa04:'alias field offset',
           0x1fa57:'alias writer table',0x1fb10:'physical x-offset field',
           0x20e24:'submit hit branch',0x20e75:'exit enable branch'}
    for rva,label in cases.items():
        source=next(s for s in layout['sections'] if s['vaddr']<=rva<s['vaddr']+s['raw_size'])
        offset=source['raw_ptr']+rva-source['vaddr'];changed=bytearray(payload);changed[offset]^=1
        try:observe(bytes(changed))
        except ValueError:continue
        raise ValueError('semantic mutation survived: '+label)
    return len(cases)


def select_aliases(records):
    selected={n:[] for n in IDS}
    for r in records:
        n=int(r['map_number'])
        if n in selected:selected[n].append({k:int(r[k]) if k in ('index','bitmapno','adder','size','xoff','yoff','width','height','map_number') else r[k]
            for k in ('index','bitmapno','adder','size','xoff','yoff','width','height','map_number','record_sha256','attr_sha256')})
    return selected


def join(selected,native,pairs):
    output=[]
    for logical,rows in selected.items():
        candidates=[]
        for r in rows:
            need(r['map_number']==logical,'alias group/record key mismatch')
            key=r['bitmapno'];matches=[n for n in native if int(n['bitmapno'])==key and n['record_sha256']==r['record_sha256']]
            links=[p for p in pairs if int(p['patch_index'])==r['index'] and p['patch_record_sha256']==r['record_sha256']]
            need(len(matches)==1 and len(links)==1,'ambiguous or absent exact native record/patch link')
            n,p=matches[0],links[0]
            need(int(p['bitmapno'])==key,'pair physical identifier mismatch')
            need(p['qualification']=='EXACT_NATIVE_RECORD_AND_RD_STRUCTURE' and p['native_exact_indices']==n['index'], 'native index qualification drift')
            need(n['rd_status']==p['rd_status']=='HEADER_MATCH' and n['rd_sha256']==p['rd_sha256'],'RD pairing mismatch')
            for field in ('adder','size','xoff','yoff','width','height'):
                need(int(n[field])==r[field],'native header field changed')
            need(n['attr_sha256']==r['attr_sha256'] and [int(n[k]) for k in ('rd_width','rd_height','rd_size')]==[r['width'],r['height'],r['size']], 'native RD/attribute fields changed')
            candidates.append({**r,'native_index':int(n['index']),'rd_sha256':n['rd_sha256'],
                'static_draw_origin':[320+r['xoff'],240+r['yoff']],
                'pixels_decoded_this_turn':False,'same_deployed_executable_build_proven':False})
        output.append({'logical_alias':logical,'candidate_count':len(candidates),'candidates':candidates,
                       'selection':'UNIQUE_IN_THIS_PINNED_PATCH' if len(candidates)==1 else 'UNRESOLVED_PRESERVE_ALL_OCCURRENCES'})
    return output


def build(payload,root=ROOT):
    need(len(payload)==921600 and hashlib.sha256(payload).hexdigest()==SOURCE_SHA,'original executable identity mismatch')
    compiled=observe(payload);negative_count=negative_source_checks(payload)
    pins={}
    for path,sha in PINS.items():
        raw=(root/path).read_bytes();need(hashlib.sha256(raw).hexdigest()==sha,'metadata pin drift: '+path)
        pins[path]={'bytes':len(raw),'sha256':sha,'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
    def rows(path):
        with gzip.open(root/path,'rt',encoding='utf-8',newline='') as f:
            yield from csv.DictReader(f,delimiter='\t')
    selected=select_aliases(rows(PATCH));physical={r['bitmapno'] for rs in selected.values() for r in rs}
    native=[r for r in rows(NATIVE) if int(r['bitmapno']) in physical]
    pairs=[r for r in rows(PAIRS) if int(r['bitmapno']) in physical]
    joined=join(selected,native,pairs)
    need([r['candidate_count'] for r in joined]==[1,1,1], 'pinned patch aliases changed')
    early={name:[int(r['map_number']) for r in rows(path) if int(r['map_number']) in IDS] for name,path in EARLY.items()}
    return {'schema':'stoneage.wayi_login_scene_alias_binding.r1','task':'OFFICIAL-CLIENT-LOGIN-SCENE-ASSET-BINDING-12',
            'original_executable_bytes':len(payload),'original_executable_sha256':SOURCE_SHA,
            'compiled':compiled,'original_patch_alias_bindings':joined,'metadata_pins':pins,
            'early_metadata_alias_hits':early,'semantic_real_source_mutations_rejected':negative_count,
            'join_role':'STATIC_CROSS_SPECIMEN_COMPATIBILITY_NOT_DEPLOYED_BUILD_AUTHENTICATION',
            'logical_alias_is_physical_bitmap_id':False,'map_number_field_is_world_floor_id':False,
            'original_game_executed':False,'original_pixels_rendered':False,'complete_login_ui_restored':False,
            'overall_restoration_percentage':None,'next':'ORIGINAL-RESOURCE-LOGICAL-ALIAS-CROSSVERSION-CATALOG-13'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    with args.source.open('rb') as f:payload=f.read(921601)
    args.output.write_text(json.dumps(build(payload),ensure_ascii=False,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':main()
