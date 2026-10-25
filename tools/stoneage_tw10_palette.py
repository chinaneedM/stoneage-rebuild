"""Original TW1 Palet_0 initialization colors, not an actual scene palette.

The original 0x96c0 initializer supplies 32 reserved RGB colors, reads 224 BGR
triplets and forces index 168 black. The source guard must be zero. This model
does not implement the 0x9b20 fade path or infer scene/time/bitmap selection.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct
import zlib

from tools.stoneage_original_observation_lab import check_original,chunk
from tools.stoneage_tw10_palette_source_probe import EXE_SHA,PAL_SHA,authenticate

FIXED_RGB=((0,0,0),(128,0,0),(0,128,0),(128,128,0),(0,0,128),(128,0,128),
           (0,128,128),(192,192,192),(192,220,192),(166,202,240),(222,0,0),
           (255,95,0),(255,255,160),(0,95,210),(80,210,255),(40,225,40),
           (245,195,150),(225,160,95),(195,125,70),(155,85,30),(70,65,55),
           (40,35,30),(255,251,240),(160,160,164),(128,128,128),(255,0,0),
           (0,255,0),(255,255,0),(0,0,255),(255,0,255),(0,255,255),(255,255,255))
MODE='AUTHENTICATED_PAL0_INITIAL_RGB_PREVIEW_NOT_ACTUAL_SCENE_COLOR'
BASE=0x400000
PALETTE=0x49f5d0


def require(ok,message):
    if not ok:raise ValueError(message)


def digest(raw):return hashlib.sha256(raw).hexdigest()


def initial_rgb(palette):
    """Reference arithmetic; caller supplies identity qualification separately."""
    require(len(palette)==708,'SAP must retain all 708 bytes including unused suffix')
    colors=list(FIXED_RGB[:16])
    colors.extend(tuple(palette[p:p+3][::-1]) for p in range(0,672,3))
    colors.extend(FIXED_RGB[16:])
    colors[168]=(0,0,0)
    return bytes(v for c in colors for v in c)


def original_rgb(path):
    check_original(path,(708,PAL_SHA))
    return initial_rgb(path.read_bytes())


def indexed_png(pixels,width,height,rgb):
    require(0<width and 0<height and width*height==len(pixels)<=8_000_000,'invalid indexed image geometry')
    require(len(rgb)==768,'256 RGB entries required; no implicit reserved colors')
    rows=b''.join(b'\0'+pixels[y*width:(y+1)*width] for y in range(height))
    ihdr=struct.pack('>IIBBBBB',width,height,8,3,0,0,0)
    return (b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',ihdr)+chunk(b'PLTE',rgb)+
            chunk(b'IDAT',zlib.compress(rows,9))+chunk(b'IEND',b''))


def emulate_initial(exe,palette,*,cache_guard=0):
    """Bounded original x86 with explicit FILE stubs; no OS, COM or real IO."""
    require(len(exe)==425984 and digest(exe)==EXE_SHA,'not accepted original executable')
    require(len(palette)==708 and cache_guard in (0,1),'outside finite emulator input contract')
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_EIP
    u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(BASE,0x100000);u.mem_write(BASE,exe)
    u.mem_map(0x300000,0x20000);u.reg_write(UC_X86_REG_ESP,0x31ff00)
    u.mem_write(PALETTE,bytes([0xa5])*1024)
    u.mem_write(0x49edc0,struct.pack('<I',cache_guard))
    state={'reads':0,'opens':[],'closes':0,'instructions':0}
    def cstring(address):
        return bytes(u.mem_read(address,64)).split(b'\0')[0].decode('ascii')
    def hook(uc,address,size,data):
        state['instructions']+=1
        if address not in (BASE+0x487ba,BASE+0x485c2,BASE+0x4856c):return
        sp=uc.reg_read(UC_X86_REG_ESP)
        ret,arg=struct.unpack('<II',uc.mem_read(sp,8))
        if address==BASE+0x487ba:
            mode=struct.unpack('<I',uc.mem_read(sp+8,4))[0]
            state['opens'].append({'path':cstring(arg),'mode':cstring(mode)})
            result=0x200001
        elif address==BASE+0x485c2:
            require(arg==0x200001 and state['reads']<672,'unbounded/incorrect native FILE read')
            result=palette[state['reads']];state['reads']+=1
        else:
            require(arg==0x200001,'incorrect close stub input')
            state['closes']+=1;result=0
        uc.reg_write(UC_X86_REG_EAX,result);uc.reg_write(UC_X86_REG_ESP,sp+4)
        uc.reg_write(UC_X86_REG_EIP,ret)
    u.hook_add(UC_HOOK_CODE,hook)
    u.emu_start(BASE+0x96c0,BASE+0x9a3e,count=10000)
    require(u.reg_read(UC_X86_REG_EIP)==BASE+0x9a3e,'native initialization exceeded bounded instruction budget')
    entries=bytes(u.mem_read(PALETTE,1024))
    rgb=b''.join(entries[i:i+3] for i in range(0,1024,4))
    if cache_guard==0:
        require(state['opens']==[{'path':'data\\pal\\Palet_0.sap','mode':'rb'}] and
                state['reads']==672 and state['closes']==1,'native original palette IO stub contract differs')
        require(rgb==initial_rgb(palette),'native/reference RGB mismatch')
    else:
        require(state['reads']==0 and not state['opens'] and state['closes']==0,'cached path unexpectedly read palette')
        colors=[bytes(c) for c in FIXED_RGB[:16]]+[b'\xa5'*3]*224+[bytes(c) for c in FIXED_RGB[16:]]
        colors[168]=b'\0'*3
        require(rgb==b''.join(colors),'cached native path must retain prior middle colors')
    state.update(rgb_sha256=digest(rgb),flags_sha256=digest(entries[3::4]),
                 cache_guard=cache_guard,original_client_executed=False,
                 original_com_palette_creation_executed=False,
                 real_file_io_executed=False)
    return rgb,state


def native_report(exe,palette):
    authenticate(exe,palette)
    actual,state=emulate_initial(exe,palette)
    synthetic=bytes((i*17+3)%256 for i in range(708))
    _,synthetic_state=emulate_initial(exe,synthetic)
    _,cached_state=emulate_initial(exe,palette,cache_guard=1)
    return {'schema':'stoneage.tw10.palette_initial_native.p2b_v1',
            'original_exe_sha256':EXE_SHA,'original_palette_sha256':PAL_SHA,
            'original_actual_palette':state,'synthetic_palette_with_original_code':synthetic_state,
            'synthetic_cached_state_with_original_code':cached_state,
            'fixed_32_rgb_sha256':digest(bytes(v for c in FIXED_RGB for v in c)),
            'read_file_bytes':672,'preserved_unread_suffix_bytes':36,
            'source_palette_rgb_mapping_verified':True,'actual_scene_palette_selection_proven':False,
            'historical_color_screenshot_observed':False,'original_client_executed':False,
            'original_assets_published':False}


def color_preview(t,paths,palette_path):
    from tools.stoneage_original_animation_lab import preview
    rgb=original_rgb(palette_path)
    colored=copy.deepcopy(t)
    colored.update(preview_mode=MODE,original_palette_verified=True,
                   source_palette_rgb_mapping_verified=True,
                   source_palette={'path':'StoneAge/data/pal/Palet_0.sap','sha256':PAL_SHA,
                                   'rgb_sha256':digest(rgb),'initial_cache_guard':0},
                   actual_scene_palette_selection_proven=False)
    html,custody=preview(colored,paths,color_table=rgb)
    return html,custody


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--native-exe',type=Path);p.add_argument('--palette',type=Path,required=True)
    p.add_argument('--native-report',type=Path);p.add_argument('--original-dir',type=Path)
    p.add_argument('--output',type=Path);p.add_argument('--spr-no',type=int,default=100000)
    p.add_argument('--direction',type=int,default=0);p.add_argument('--action',type=int,default=6)
    a=p.parse_args()
    if a.native_exe:
        require(a.native_report is not None and a.output is None,'native report output required')
        d=native_report(a.native_exe.read_bytes(),a.palette.read_bytes())
        a.native_report.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
        print('P2B_NATIVE_PALETTE_SOURCE='+json.dumps(d,separators=(',',':')))
    else:
        require(a.original_dir is not None and a.output is not None,'private original input/output required')
        from tools.stoneage_original_animation_lab import ORIGINALS,timeline,write_private
        t=timeline(a.spr_no,a.direction,a.action)
        html,custody=color_preview(t,{n:a.original_dir/n for n in ORIGINALS},a.palette)
        write_private(a.output,html,custody)
        print('PRIVATE_PAL0_INITIAL_COLOR_PREVIEW=PASS; ACTUAL_SCENE_AND_GAME_RUNTIME=OPEN')


if __name__=='__main__':main()
