"""Finite private preserved-program display-order replay; never launches the client.

Original instructions are supplied privately and whole-SHA pinned. No proprietary
instruction bytes, assets, original maps or executables are emitted to public Git.
Only a 5x5 material observation with no actors is admitted.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct

EXE_SHA = 'ec678517f76564ebc9ab00cf3f66853ed9975ef6290eb48168b78909a68a5d16'
HTML_SHA = 'ff9c99fa3df6ccbc162ea87e87f5cd8e4a980e3b0f9877309f99d30776dae298'
SPANS = {'sort_dispatch': (0x44c4a3,0x44c4c0), 'comparator': (0x44cc14,0x44cc47),
         'queue_writer': (0x44c8c6,0x44c974), 'physical_queue_writer': (0x44c974,0x44ca11),
         'parts_list': (0x42a936,0x42aa2a), 'list_append': (0x42abdc,0x42ac03),
         'parts_queue': (0x42ac03,0x42ac48), 'map_scan': (0x427c37,0x427e44),
         'forward_consumer': (0x44c729,0x44c895)}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def compare(a, b):
    """Exact bounded native comparator, including its nonzero equal-record result."""
    if a[1] != b[1]:
        return 1 if a[1] > b[1] else -1
    return -1 if a[0] > b[0] else 1

def display_order(rows):
    require(len(rows) <= 4096, 'native display queue bound')
    require(len({r['queue_no'] for r in rows}) == len(rows), 'duplicate queue identity')
    require(all(type(r['queue_no']) is int and 0 <= r['queue_no'] < 4096 and
                type(r['priority']) is int and 0 <= r['priority'] <= 255 for r in rows),
            'native field range')
    return sorted(rows, key=lambda r:(r['priority'], -r['queue_no']))

class Native:
    def __init__(self, raw):
        require(len(raw) == 561152 and sha(raw) == EXE_SHA, 'private program identity')
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
        from unicorn.x86_const import UC_X86_REG_ESP
        self.u = Uc(UC_ARCH_X86, UC_MODE_32)
        self.u.mem_map(0x400000, 0x3000000)
        self.u.mem_write(0x400000, raw[:0x88000])
        self.u.mem_map(0x4000000,0x20000)
        self.stack = 0x4010000
        self.u.reg_write(UC_X86_REG_ESP,self.stack)
    def put(self, addr, value, fmt='<I'):
        self.u.mem_write(addr,struct.pack(fmt,value))
    def get(self, addr, fmt='<I'):
        return struct.unpack(fmt,self.u.mem_read(addr,struct.calcsize(fmt)))[0]
    def call(self, addr, args=()):
        from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_EIP
        sentinel=0x401f000
        self.u.reg_write(UC_X86_REG_ESP,self.stack)
        self.u.mem_write(self.stack,struct.pack('<'+'I'*(len(args)+1),sentinel,*(x & 0xffffffff for x in args)))
        self.u.emu_start(addr,sentinel,count=200000)
        require(self.u.reg_read(UC_X86_REG_EIP)==sentinel,'bounded original function did not return')
        x=self.u.reg_read(UC_X86_REG_EAX)
        return x if x < 0x80000000 else x-0x100000000

def replay(exe, adrn, html, mapraw):
    require(sha(html)==HTML_SHA,'R5 immutable HTML identity')
    require(len(adrn)==18765120,'private ADRN extent')
    # The full digest is checked against the earlier source receipt, not guessed.
    root=Path(__file__).resolve().parents[1]
    prior=json.loads((root/'research/recovered/STONEAGE-SCENE02-SOURCE-REAL-PIXELS-R2.json').read_text())
    require(sha(adrn)==prior['observation']['source_adrn_sha256'],'private full ADRN identity')
    s=html.decode('utf-8')
    model=json.loads(s.split('<script id="evidence" type="application/json">',1)[1].split('</script>',1)[0])
    rows=model['placements']
    require(len(rows)==30 and sum(r['layer']=='tile' for r in rows)==25 and
            all(r['qualified'] for r in rows),'fixed complete R5 region')
    require(len(mapraw)==5408 and sha(mapraw)==model['source_dat_sha256'] and
            struct.unpack_from('<II',mapraw)==(30,30),'private original DAT identity')
    native=Native(exe)
    # Native getters read these source ADRN records at their original stride.
    native.u.mem_write(0xb14900,adrn)
    tests=[]
    for pa in (0,1,10,127,128,255):
        for pb in (0,1,10,127,128,255):
            for na,nb in ((0,1),(29,0),(32767,0),(0,32767),(3,3)):
                native.u.mem_write(0x4000000,struct.pack('<hBx',na,pa)+struct.pack('<hBx',nb,pb))
                result=native.call(0x44cc14,(0x4000000,0x4000004))
                require(result==compare((na,pa),(nb,pb)),'original comparator mismatch')
                tests.append([na,pa,nb,pb,result])
    # Execute the native map sweep with an explicitly injected 5x5 original
    # DAT crop and translated viewport. Native camera/map/alias loaders are NOT run.
    native.put(0x2b40f50,0,'<h')
    native.put(0x2abba94,0)
    native.put(0x2ab1370,0)
    tile=[r for r in rows if r['layer']=='tile']
    parts=[r for r in rows if r['layer']=='parts']
    ids={r['map_id'] for r in rows}
    aliases={i:[] for i in ids}
    for off in range(0,len(adrn),80):
        key=struct.unpack_from('<I',adrn,off+76)[0]
        if key in aliases:aliases[key].append(struct.unpack_from('<I',adrn,off)[0])
    require(all(len(v)==1 for v in aliases.values()),'ambiguous native crop alias')
    for key,values in aliases.items():native.put(0x7af6b8+key*4,values[0])
    for plane,addr in ((0,0x2ad2660),(1,0x2abaf64)):
        crop=[struct.unpack_from('<H',mapraw,8+2*(plane*900+y*30+x))[0]
              for y in range(13,18) for x in range(13,18)]
        native.u.mem_write(addr,struct.pack('<25H',*crop))
    for addr,value in ((0x2ab1398,5),(0x2aba480,5),(0x2ab1f24,13),(0x2ab1f2c,13)):
        native.put(addr,value)
    from unicorn.x86_const import UC_X86_REG_EBP,UC_X86_REG_ESP,UC_X86_REG_ESI,UC_X86_REG_EDI,UC_X86_REG_EIP
    frame=0x400f000
    native.u.reg_write(UC_X86_REG_EBP,frame)
    native.u.reg_write(UC_X86_REG_ESP,frame-0x100)
    native.u.reg_write(UC_X86_REG_ESI,192)
    native.u.reg_write(UC_X86_REG_EDI,200)
    native.put(frame-12,228)
    native.u.emu_start(0x427c37,0x427e44,count=200000)
    require(native.u.reg_read(UC_X86_REG_EIP)==0x427e44,'bounded original scan did not finish')
    queue=[dict(r,queue_no=no,priority=0 if r['layer']=='tile' else 10)
           for no,r in enumerate(tile+parts)]
    require(native.get(0x2b40f50,'<h')==30,'native 30-entry queue required')
    for r in queue:
        no=r['queue_no'];p=0x2b28f50+20*no
        require((native.get(p,'<i'),native.get(p+4,'<i'),native.get(p+8,'<i'))==
                (r['draw_x']+100,r['draw_y']+200,r['bitmapno']),'original scan/ADRN offset/queue divergence')
        require(native.get(0x2b3cf50+4*no,'<h')==no and
                native.get(0x2b3cf52+4*no,'<B')==r['priority'],'original queue identity/priority divergence')
    native.call(0x44c4a3)  # actual original CRT sorter and callback, no Python sort stub
    order=[native.get(0x2b3cf50+4*i,'<h') for i in range(30)]
    expected=[r['queue_no'] for r in display_order(queue)]
    require(order==expected,'actual original sorter/reference mismatch')
    # Follow the actual consumer traversal, replacing only LoadBmp with failure.
    # This observes requested order without claiming DirectDraw or asset IO success.
    from unicorn import UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EBX
    consumed=[]
    def load_failure(u, address, size, data):
        if address!=0x44cf7f:return
        esp=u.reg_read(UC_X86_REG_ESP)
        consumed.append(native.get(esp+4))
        ret=native.get(esp)
        u.reg_write(UC_X86_REG_EAX,0)
        u.reg_write(UC_X86_REG_ESP,esp+4)
        u.reg_write(UC_X86_REG_EIP,ret)
    hook=native.u.hook_add(UC_HOOK_CODE,load_failure)
    native.put(0x2b40f58,0x2b3cf50)
    native.u.reg_write(UC_X86_REG_ESP,native.stack)
    native.u.reg_write(UC_X86_REG_ESI,0)
    native.u.reg_write(UC_X86_REG_EBX,0)
    native.u.emu_start(0x44c729,0x44c895,count=200000)
    native.u.hook_del(hook)
    require(native.u.reg_read(UC_X86_REG_EIP)==0x44c895 and
            consumed==[queue[i]['bitmapno'] for i in order],'native consumer traversal mismatch')
    return {'schema':'stoneage.scene06.native_display_order.r6','program_bytes':len(exe),
            'program_sha256':sha(exe),'adrn_sha256':sha(adrn),'source_r5_html_sha256':sha(html),
            'source_map_sha256':sha(mapraw),'native_scan_crop':[13,13,17,17],
            'injected_viewport_translation':[100,200],
            'native_map_sweep_executed':True,'native_getters_and_alias_lookup_not_stubbed':True,
            'runtime_alias_table_injected_from_unique_original_adrn':True,
            'source_spans':{k:{'va_start':a,'va_end_exclusive':b,'sha256':sha(exe[a-0x400000:b-0x400000])} for k,(a,b) in SPANS.items()},
            'comparator_cases':tests,'comparator_case_count':len(tests),
            'original_sorter_executed_in_unicorn':True,'sorter_not_stubbed':True,
            'controlled_queue':queue,'original_sorted_queue_numbers':order,
            'native_consumer_requested_bitmap_order':consumed,
            'consumer_LoadBmp_stubbed_to_failure':True,'directdraw_executed':False,
            'no_actor_parts_append_then_reverse_verified':True,
            'native_tile_priority':0,'descendant_header_tile_priority':1,
            'scope':'PRESERVED_MIXED25_NO_ACTORS_CONTROLLED_QUEUE_NOT_ORIGINAL_GAME',
            'unverified':['native_map_and_alias_loader','live_original_palette','native_camera',
                          'characters_parts_occlusion','same_deployed_official_build','playable_world_entry'],
            'original_client_launched':False,'original_world_entered':False,
            'stage_a':'7_PARTIAL_2_OPEN','stage_b':'GATED','r79':'PAUSED_NON_BLOCKING',
            'overall_completion_percent':None}

def export_observer(html, report, target):
    """Private derivative retains original R5 bytes as a separate comparison mode."""
    import base64
    import io
    from PIL import Image
    root=Path(__file__).resolve().parents[1]
    require(root not in target.resolve().parents and not target.exists(),'new private output outside Git required')
    text=html.decode('utf-8')
    first,tail=text.split('<script id="evidence" type="application/json">',1)
    data,last=tail.split('</script>',1)
    model=json.loads(data)
    images={int(k):Image.open(io.BytesIO(base64.b64decode(v))).convert('RGBA')
            for k,v in model['sprites'].items()}
    require(all(sha(base64.b64decode(model['sprites'][str(k)]))==model['sprite_sha256'][str(k)]
                for k in images),'immutable source PNG drift')
    def pixels(rows):
        im=Image.new('RGBA',(400,350))
        for p in rows:im.alpha_composite(images[p['map_id']],(p['draw_x']+70,p['draw_y']+170))
        return im.tobytes()
    rows=model['placements'];ordered=[rows[i] for i in report['original_sorted_queue_numbers']]
    old,new=pixels(rows),pixels(ordered)
    report['pixel_impact']={'canvas':[400,350],'translation':[70,170],
        'old_rgba_sha256':sha(old),'native_queue_order_rgba_sha256':sha(new),
        'changed_pixels':sum(old[i:i+4]!=new[i:i+4] for i in range(0,len(old),4)),
        'actual_native_screenshot':False}
    model['R6_native_sorted_queue_numbers']=report['original_sorted_queue_numbers']
    model['R6_scope']='同保存原程序有限指令重放；无人物、无原生绘图或原游戏进入'
    text=first+'<script id="evidence" type="application/json">'+json.dumps(model,ensure_ascii=False,separators=(',',':'))+'</script>'+last
    needle='for(const p of model.placements){if('
    require(text.count(needle)==1,'R5 draw loop anchor')
    text=text.replace(needle,"for(const p of (by('nativeOrder').checked?model.R6_native_sorted_queue_numbers.map(i=>model.placements[i]):model.placements)){if(")
    needle="for(const id of ['tiles','parts','gaps'])"
    require(text.count(needle)==1,'R5 controls anchor')
    text=text.replace(needle,"for(const id of ['tiles','parts','gaps','nativeOrder'])")
    needle='<canvas'
    require(text.count(needle)==1,'R5 canvas anchor')
    text=text.replace(needle,'<label><input type="checkbox" id="nativeOrder" checked> 原程序顺序候选（无人物；取消可对比旧候选）</label><p>R6：同保存原程序扫描、构件入队、排序与请求顺序已有限重放。调色板、镜头和实际绘图仍未运行认证。</p><canvas',1)
    text=text.replace('观察 R5','观察 R6').replace('window.__stoneageR5','window.__stoneageR6')
    target.write_text(text,encoding='utf-8')
    report['private_observer']={'bytes':target.stat().st_size,'sha256':sha(target.read_bytes()),
                                'new_source_images':0,'contains_source_images':True}

def independent_source_compare(path, cases):
    import subprocess
    import tempfile
    raw=path.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    require(blob=='666eb344f5a5c07265f7bfd4f8c8058bac66c157','fixed independent source blob')
    start=raw.rindex(b'int SortComp(');brace=raw.index(b'{',start);depth=1;end=brace+1
    while depth:
        depth+=(raw[end:end+1]==b'{')-(raw[end:end+1]==b'}');end+=1
    fragment=raw[start:end]
    with tempfile.TemporaryDirectory() as d:
        source=Path(d)/'compare.cpp';binary=Path(d)/'compare'
        source.write_bytes(b'#include <iostream>\nstruct DISP_SORT {short no; unsigned char dispPrio;};\n'+fragment+
            b'\nint main(){int a,p,b,q;while(std::cin>>a>>p>>b>>q){DISP_SORT x{(short)a,(unsigned char)p},y{(short)b,(unsigned char)q};std::cout<<SortComp(&x,&y)<<"\\n";}}\n')
        subprocess.run(['g++','-O2',str(source),'-o',str(binary)],check=True,capture_output=True)
        result=subprocess.run([str(binary)],input=''.join(' '.join(map(str,r[:4]))+'\n' for r in cases),
                              text=True,check=True,capture_output=True)
        require(list(map(int,result.stdout.split()))==[r[4] for r in cases],
                'compiled independent source/native comparator mismatch')
    return {'repository':'BismarckDD/stoneage','commit':'999ffdf1d220ec6666eb65339180689c9caf1876',
            'path':'client/stoneage/system/sprdisp.cpp','git_blob':blob,
            'fragment_sha256':sha(fragment),'compiled_cases_equal_native':len(cases),
            'same_build_source_authenticated':False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('exe','adrn','html','map','report'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--observer',type=Path)
    p.add_argument('--lineage-sprdisp',type=Path)
    a=p.parse_args();report=replay(a.exe.read_bytes(),a.adrn.read_bytes(),a.html.read_bytes(),a.map.read_bytes())
    if a.observer:export_observer(a.html.read_bytes(),report,a.observer)
    if a.lineage_sprdisp:report['independent_source_comparator']=independent_source_compare(a.lineage_sprdisp,report['comparator_cases'])
    a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('BOUNDED_ORIGINAL_INSTRUCTION_ORDER_REPLAY=PASS; ORIGINAL_WORLD_ENTERED=FALSE')

if __name__=='__main__':main()
