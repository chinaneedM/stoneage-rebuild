"""Synthetic Win32 capability measurements. NEVER loads an original client."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import time

from tools.stoneage_p3_boot import ROOT, command, frame, network_gate, require


def read_live(path, predicate=lambda x:True, timeout=15):
    end=time.monotonic()+timeout
    while time.monotonic()<end:
        try:
            d=json.loads(path.read_text())
            if predicate(d):return d
        except (OSError,ValueError):pass
        time.sleep(.05)
    raise ValueError('synthetic program did not publish the required live observation')


def input_delta(before,after):
    delta={k:after[k]-before[k] for k in ('downs','ups','async_down_polls')}
    delta['program_received_down_up_and_async']=all(delta[k]>0 for k in ('downs','ups','async_down_polls'))
    return delta


def evaluate_case(case):
    p=case['palette_state']
    readback=p['getpixel_valid'] and p['red_getpixel']==[222,0,0] and p['green_getpixel']==[0,200,80]
    captures=case['palette_capture'].get('frames',[])
    captured=any(f['synthetic_control_red_pixels']>=19000 and f['synthetic_control_green_pixels']>=19000 for f in captures)
    if case['mode']=='gdi':
        render=p['phase']==1 and p['palette_created']
    else:
        render=p['phase']==1 and all(p['ddraw'][k]==0 for k in
            ('create','cooperative','primary','offscreen_8bit','palette','offscreen_attach','blt'))
        if p['display_bpp']==8:render=render and p['ddraw']['primary_attach']==0
    sent=case['sendinput_command'].get('report',{})
    received=input_delta(case['before_sendinput'],case['after_sendinput'])['program_received_down_up_and_async']
    dispatched=case['sendinput_command']['returncode']==0 and sent.get('sendinput_down')==1 and sent.get('sendinput_up')==1
    return {'known_rgb_getpixel':bool(readback),'known_rgb_external_capture':captured,
        'render_path_passed':bool(render),'color_gate_passed':bool(readback and captured and render),
        'sendinput_dispatch_only':bool(dispatched),'sendinput_received':received,
        'sendinput_gate_passed':bool(dispatched and received),
        'foreground_gate_passed':p['foreground_matches'] and p['active_matches'] and p['focus_matches'],
        'original_client_executed':False,'original_game_input_or_color_proven':False}


def shot(directory,name,env,helper,native):
    if native:
        try:
            from PIL import ImageGrab
            live=read_live(directory/'live.json');x,y=live['client_origin']
            path=directory/(name+'.png');ImageGrab.grab(bbox=(x,y,x+320,y+200)).save(path)
            return {'method':'native_ImageGrab_own_synthetic_client_rectangle','frames':[frame(path)]}
        except Exception as e:return {'method':'native_ImageGrab','capture_error_type':type(e).__name__,'frames':[]}
    if helper:
        from tools.stoneage_p3c_capture import capture
        result=capture(helper,directory/name,env)
        return {'method':'X11_each_window_colormap','frames':[w['map'] for w in result['windows']], 'x11':result}
    path=directory/(name+'.png')
    c=command(['import','-window','root',str(path)],env=env)
    return {'method':'ImageMagick_24bit_root','frames':[frame(path)] if c.returncode==0 else [],'returncode':c.returncode}


def run_case(directory,exe,env,mode,helper,native):
    directory.mkdir();prefix=[] if native else ['wine']
    def control(action):
        r=command([*prefix,str(exe),action],cwd=directory,env=env,timeout=20)
        lines=[x for x in r.stdout.splitlines() if x.startswith('{')]
        return {'returncode':r.returncode,'report':json.loads(lines[-1]) if lines else {}}
    with (directory/'process.log').open('w') as log:
        process=subprocess.Popen([*prefix,str(exe),mode],cwd=directory,env=env,stdout=log,stderr=log)
        case={'mode':mode,'original_client_executed':False}
        try:
            case['baseline_state']=read_live(directory/'live.json',lambda x:x['phase']==0)
            case['baseline_capture']=shot(directory,'baseline-capture',env,helper,native)
            case['activation_command']=control('activate')
            case['palette_command']=control('palette')
            time.sleep(.5)
            case['palette_state']=read_live(directory/'live.json',lambda x:x['phase']==1)
            case['palette_capture']=shot(directory,'palette-capture',env,helper,native)
            if not native:
                before=read_live(directory/'live.json');x,y=before['client_origin']
                commands=[]
                for args in (['mousemove','--sync',str(x+160),str(y+170)],['mousedown','1']):
                    commands.append(command(['xdotool',*args],env=env).returncode)
                time.sleep(.2);commands.append(command(['xdotool','mouseup','1'],env=env).returncode);time.sleep(.3)
                after=read_live(directory/'live.json')
                case['x11_input']={'dispatch_returncodes':commands,'before':before,'after':after,'delta':input_delta(before,after)}
            case['before_sendinput']=read_live(directory/'live.json')
            case['sendinput_command']=control('click');time.sleep(.3)
            case['after_sendinput']=read_live(directory/'live.json')
            case['after_input_capture']=shot(directory,'after-input-capture',env,helper,native)
            case['finish_command']=control('finish')
            case['final_state']=read_live(directory/'live.json',lambda x:x['done'])
            case['process_exit_before_cleanup']=process.wait(timeout=15)
            case['assessment']=evaluate_case(case)
        finally:
            if process.poll() is None:process.terminate();process.wait(timeout=10)
    return case


def main():
    a=argparse.ArgumentParser();a.add_argument('--directory',type=Path,required=True)
    a.add_argument('--exe',type=Path,required=True);a.add_argument('--output',type=Path,required=True)
    a.add_argument('--depth',type=int,choices=[8,24],default=24);a.add_argument('--helper',type=Path)
    a.add_argument('--native',action='store_true');args=a.parse_args()
    base=args.directory.resolve();exe=args.exe.resolve()
    require(base!=ROOT and ROOT not in base.parents and not base.exists(),'new synthetic work directory outside Git required')
    base.mkdir();env=os.environ.copy();display=None
    report={'schema':'stoneage.p3d.synthetic_environment_gate.v1','original_client_downloaded':False,
        'original_client_executed':False,'original_game_world_entered':False,'cases':[],
        'host_platform':platform.platform(),'bench_binary_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),
        'control_source_sha256':hashlib.sha256((ROOT/'tools/stoneage_p3d_control.c').read_bytes()).hexdigest()}
    try:
        if args.native:
            require(os.name=='nt','native controller requires Windows')
            report['environment']='native_windows_wow64_x86_control_only'
            report['network_scope']='CI host not network-isolated; synthetic program contains no network calls; no original permitted'
        else:
            report['network']=network_gate();report['environment']=f'wine32_xvfb_800x600x{args.depth}'
            env.update(WINEARCH='win32',WINEPREFIX=str(base/'wine-prefix'),WINEDLLOVERRIDES='mscoree,mshtml=',
                WINEDEBUG='-all',DISPLAY=':94',LANG='zh_TW.UTF-8',LC_ALL='zh_TW.UTF-8',LIBGL_ALWAYS_SOFTWARE='1')
            display=subprocess.Popen(['Xvfb',':94','-screen','0',f'800x600x{args.depth}','-nolisten','tcp','-ac'],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            for _ in range(50):
                if command(['xdpyinfo'],env=env).returncode==0:break
                time.sleep(.1)
            boot=command(['wineboot','-u'],env=env,cwd=base,timeout=120);require(boot.returncode==0,'synthetic Wine prefix failed')
            command(['wine','reg','add','HKCU\\Software\\Wine','/v','Version','/d','winxp','/f'],env=env,cwd=base)
            report['wine_version']=command(['wine','--version']).stdout.strip()
        for mode in ('gdi','ddraw'):
            case=run_case(base/mode,exe,env,mode,args.helper if args.depth==8 else None,args.native)
            report['cases'].append(case)
        # A synthetic pass never authorizes claiming original runtime success.
        report['original_rerun_prerequisite_synthetic_8bit_passed']=any(
            c['mode']=='ddraw' and c['palette_state']['display_bpp']==8 and c['palette_state']['windows_acp']==950 and
            c['assessment']['color_gate_passed'] and c['assessment']['sendinput_gate_passed'] and
            c['assessment']['foreground_gate_passed'] for c in report['cases'])
    except Exception as e:
        report.update(probe_error_type=type(e).__name__,probe_error=str(e));raise
    finally:
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        if not args.native:
            command(['wineserver','-k'],env=env)
            if display:display.terminate();display.wait(timeout=10)
    print('P3D_SYNTHETIC_MEASUREMENT='+json.dumps({'environment':report['environment'],
        'assessments':[c['assessment'] for c in report['cases']],
        'original_rerun_prerequisite_synthetic_8bit_passed':report['original_rerun_prerequisite_synthetic_8bit_passed']}))


if __name__=='__main__':main()
