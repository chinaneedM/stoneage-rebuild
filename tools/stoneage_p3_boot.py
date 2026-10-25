"""Read-only qualification and isolated Win32 boot observations for original TW1.

Execution takes place ONLY in an already-created, route-free network namespace
and a disposable Wine prefix. Captured images stay transient/private; only
derived metadata is emitted. A window does not prove game-world entry.
"""
import argparse
import errno
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import time

ROOT=Path(__file__).resolve().parents[1]
INVENTORY=ROOT/'research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt'
INVENTORY_BLOB='564233902b10c60760d4f93b1ea65d4dd1469206'
SOURCE='TW_WAEI_JSS_1_0_ACCEPTED_RETAIL_REDUMP_104630'
LAUNCH_ARGS=('updated','realbin:1','adrnbin:1','sprbin:1','spradrnbin:1',
             'soundbin:1','battlebin:1','windowmode','IP:0:127.0.0.1:9')


def require(ok,message):
    if not ok:raise ValueError(message)


def digest_file(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def inventory():
    raw=INVENTORY.read_bytes()
    require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==INVENTORY_BLOB,'original inventory changed')
    output=[]
    for line in raw.decode().splitlines():
        if line.startswith('CORE_FILE|'):
            row=dict(p.split('=',1) for p in line.split('|')[1:])
            if row['category']!='installer_support':output.append(row)
    require(len(output)==375,'original runtime input census changed')
    return output


def extract(disc,output):
    output=output.resolve()
    require(output!=ROOT and ROOT not in output.parents,'original extraction must stay outside public Git')
    require(not output.exists(),'source extraction refuses overwrite')
    from tools.stoneage_tw10_technical_probe import find_rows,extract_row
    img,rows,_,_=find_rows(disc)
    try:
        found={r['path']:r for r in rows if not r['is_dir']}
        for row in inventory():
            require(row['path'] in found and found[row['path']]['size']==int(row['size']),'original runtime member missing/length mismatch')
            path=output/Path(row['path']).relative_to('StoneAge')
            extract_row(img,found[row['path']],path)
            require(digest_file(path)==row['sha256'],'original runtime member SHA mismatch: '+row['path'])
    finally:img.close()
    return {'files':375,'bytes':sum(int(r['size']) for r in inventory()),'all_member_sha256_match':True,
            'original_installer_or_driver_executed':False}


def network_gate():
    # A new NET namespace, only loopback and no routes, is a hard prerequisite.
    mine=os.readlink('/proc/self/ns/net');host=os.environ.get('P3_HOST_NET_NAMESPACE','')
    require(host and mine!=host,'original execution requires a distinct network namespace')
    links=json.loads(subprocess.check_output(['ip','-j','link'],text=True))
    require({r['ifname'] for r in links}=={'lo'},'namespace contains an external network interface')
    routes=subprocess.check_output(['ip','route','show'],text=True).strip()
    routes6=subprocess.check_output(['ip','-6','route','show','default'],text=True).strip()
    require(not routes and not routes6,'namespace has routes')
    s=socket.socket();s.settimeout(1)
    try:
        code=s.connect_ex(('192.0.2.1',9))
        require(code in (errno.ENETUNREACH,errno.EHOSTUNREACH),'external-connect negative control did not fail closed')
    finally:s.close()
    return {'host_net_namespace':host,'child_net_namespace':mine,'interfaces':['lo'],
            'ipv4_routes':[],'ipv6_default_routes':[],'external_documentation_address_connect_errno':code,
            'outbound_namespace_isolation_verified':True}


def command(args,*,cwd=None,timeout=30,env=None):
    return subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                          text=True,errors='replace',timeout=timeout)


def frame(path):
    from PIL import Image,ImageStat
    with Image.open(path) as image:
        rgb=image.convert('RGB');stats=ImageStat.Stat(rgb)
        colors=dict((color,count) for count,color in rgb.getcolors(rgb.width*rgb.height))
        return {'width':rgb.width,'height':rgb.height,'rgb_sha256':hashlib.sha256(rgb.tobytes()).hexdigest(),
                'png_sha256':digest_file(path),'channel_extrema':stats.extrema,
                'nonuniform_pixels':any(lo!=hi for lo,hi in stats.extrema),
                'synthetic_control_red_pixels':colors.get((222,0,0),0),
                'synthetic_control_green_pixels':colors.get((0,200,80),0),
                'assistant_viewed_original':False,'image_published':False}


def inspect_windows(control,env,cwd):
    p=command(['wine',str(control),'inspect'],cwd=cwd,env=env,timeout=20)
    lines=[line for line in p.stdout.splitlines() if line.startswith('{')]
    return json.loads(lines[-1]) if lines else {'windows':[],'inspection_returncode':p.returncode}


def runtime(directory,control,output,original=False,depth_probe=False,colormap_helper=None):
    net=network_gate();directory=directory.resolve();control=control.resolve()
    require(directory.is_dir() and directory!=ROOT and ROOT not in directory.parents,'runtime directory must be private and outside public Git')
    env=os.environ.copy();env.update(WINEARCH='win32',WINEPREFIX=str(directory/'wine-prefix'),
        WINEDLLOVERRIDES='mscoree,mshtml=',WINEDEBUG='-all',DISPLAY=':93',LIBGL_ALWAYS_SOFTWARE='1',
        LANG='zh_TW.UTF-8',LC_ALL='zh_TW.UTF-8')
    xlog=(directory/'xvfb.log').open('w')
    screen_depth=8 if original or depth_probe else 24
    display=subprocess.Popen(['Xvfb',':93','-screen','0',f'800x600x{screen_depth}','-nolisten','tcp','-ac'],stdout=xlog,stderr=xlog)
    processes=[]
    result={'schema':'stoneage.p3.isolated_boot_observation.v1','sample':SOURCE,'network':net,
            'preflight_passed':False,'original_client_execution_attempted':False,
            'original_client_execution_proven':False,'game_world_entered':False,
            'authentic_game_display_visually_verified':False,'assistant_viewed_original':False,
            'original_assets_published':False}
    try:
        for _ in range(50):
            if command(['xdpyinfo'],env=env,timeout=3).returncode==0:break
            time.sleep(.1)
        else:raise ValueError('isolated Xvfb display unavailable')
        boot=command(['wineboot','-u'],env=env,cwd=directory,timeout=120)
        result['wineboot']={'returncode':boot.returncode,'diagnostic_lines':boot.stderr.splitlines()[-12:]}
        require(boot.returncode==0,'Wine 32-bit prefix initialization failed')
        setting=command(['wine','reg','add','HKCU\\Software\\Wine','/v','Version','/d','winxp','/f'],env=env,cwd=directory,timeout=20)
        require(setting.returncode==0,'Wine version setting failed')
        result.update(environment={'wine_version':command(['wine','--version']).stdout.strip(),
                    'winearch':'win32','windows_version_setting':'winxp','display':f'800x600x{screen_depth}_XVFB',
                    'requested_locale':'zh_TW.UTF-8','old_kernel_drivers_installed':False},audio_heard_or_recorded=False)
        if not original:
            log=(directory/'control.log').open('w')
            p=subprocess.Popen(['wine',str(control)],cwd=directory,env=env,stdout=log,stderr=log);processes.append(p)
            for _ in range(100):
                if (directory/'synthetic-control.json').exists():break
                time.sleep(.1)
            else:raise ValueError('32-bit synthetic window/DirectDraw control did not report')
            synthetic=json.loads((directory/'synthetic-control.json').read_text())
            result['synthetic_control']=synthetic
            require(synthetic['pointer_bytes']==4 and synthetic['window_created'],'synthetic Win32 control failed')
            require(all(synthetic[k]==0 for k in ['directdraw_create','cooperative','surface_8bit_create','palette_create','palette_attach']),
                    'synthetic original-era DirectDraw prerequisites failed')
            require(synthetic['windows_acp']==950,'Traditional Chinese original ANSI codepage unavailable')
            result['windows']=inspect_windows(control,env,directory)
            shot=directory/'synthetic-control.png'
            command(['import','-window','root',str(shot)],env=env,timeout=15)
            result['capture']=frame(shot);require(result['capture']['nonuniform_pixels'],'synthetic display capture is blank')
            if depth_probe:
                require(synthetic['get_display_mode']==0 and synthetic['current_display_bpp']==8,
                        'native current display is not 8-bit despite offscreen palette support')
            else:
                require(result['capture']['synthetic_control_red_pixels']>1000 and
                        result['capture']['synthetic_control_green_pixels']>1000,'synthetic Win32 painted pixels absent')
            if depth_probe and colormap_helper:
                from tools.stoneage_p3c_capture import capture as xcapture
                result['x11_known_rgb_control']=xcapture(colormap_helper,directory/'x11-known-rgb',env,selftest=True)
                time.sleep(.5)
                result['wine_window_colormaps']=xcapture(colormap_helper,directory/'wine-window-colormaps',env)
                result['wine_known_rgb_preserved']=any(w['map']['synthetic_control_red_pixels']>1000 and
                    w['map']['synthetic_control_green_pixels']>1000 for w in result['wine_window_colormaps']['windows'])
            result['preflight_passed']=True
        else:
            source=directory/'source';run=directory/'run'
            require(source.is_dir() and not run.exists(),'missing immutable input or existing run copy')
            for row in inventory():
                path=source/Path(row['path']).relative_to('StoneAge')
                require(path.stat().st_size==int(row['size']) and digest_file(path)==row['sha256'],'source changed before launch')
            shutil.copytree(source,run)
            exe=run/'sa_3.exe';result['source_executable']={'path':'StoneAge/sa_3.exe','bytes':exe.stat().st_size,'sha256':digest_file(exe)}
            log=(directory/'original-wine.log').open('w')
            result['original_launch_args']=list(LAUNCH_ARGS)
            result['endpoint_is_synthetic_isolated_loopback_not_historical_server']=True
            p=subprocess.Popen(['wine',str(exe),*LAUNCH_ARGS],cwd=run,env=env,stdout=log,stderr=log);processes.append(p)
            result['original_client_execution_attempted']=True;result['host_launcher_pid']=p.pid
            result['observations']=[]
            for delay in (3,7,10):
                time.sleep(delay)
                shot=directory/('original-frame-'+str(len(result['observations']))+'.png')
                capture=command(['import','-window','root',str(shot)],env=env,timeout=15)
                result['observations'].append({'launcher_returncode':p.poll(),
                    'windows':inspect_windows(control,env,run),
                    'capture':frame(shot) if capture.returncode==0 and shot.exists() else None})
            result['launcher_returncode_before_cleanup']=p.poll()
            native_windows=[w for observation in result['observations'] for w in observation['windows'].get('windows',[])
                            if w.get('image_path','').replace('\\','/').lower().endswith('/sa_3.exe')]
            result['original_client_execution_proven']=bool(native_windows)
            result['original_visible_window_occurrences']=len(native_windows)
            if native_windows and colormap_helper:
                from tools.stoneage_p3c_capture import capture as xcapture
                sealed_dir=Path('/tmp/stoneage-p3c-sealed');sealed_dir.mkdir(exist_ok=False)
                require(any(w['class']=='ＳｔｏｎｅＡｇｅ' for w in native_windows),'original main window unavailable before input')
                result['before_focus_window_colormaps']=xcapture(colormap_helper,directory/'before-focus',env)
                client=[w for w in result['before_focus_window_colormaps']['windows'] if (w['width'],w['height'])==(640,480)]
                require(len(client)==1,'ambiguous native 640x480 client drawable')
                focus=command(['xdotool','windowfocus','--sync',str(client[0]['window'])],env=env)
                require(focus.returncode==0,'X11 input focus dispatch failed')
                time.sleep(2)
                result['focus_observation']={'x11_window':client[0]['window'],'returncode':focus.returncode,
                    'operation':'XSetInputFocus_via_xdotool_no_window_manager_no_game_patch'}
                result['original_window_colormaps']=xcapture(colormap_helper,directory/'focused-before-input',env,seal_dir=sealed_dir)
                # Point selected from the authenticated P3 login frame, not account fields.
                move=command(['xdotool','mousemove','--sync','350','410'],env=env)
                down=command(['xdotool','mousedown','1'],env=env) if move.returncode==0 else move
                time.sleep(.2)
                up=command(['xdotool','mouseup','1'],env=env)
                time.sleep(3)
                after=inspect_windows(control,env,run)
                after_owned=[w for w in after.get('windows',[]) if w.get('image_path','').replace('\\','/').lower().endswith('/sa_3.exe')]
                result['input_observation']={'operation':'one_held_left_click_at_previous_authenticated_QUIT_label',
                    'screen_xy':[350,410],'coordinate_source_png_sha256':'8d7a9594292e262615c187d2fd21504b3b0f71a4d02e8c9a31811af53f460cc0',
                    'account_or_password_entered':False,'mousemove_returncode':move.returncode,'click_returncode':down.returncode or up.returncode,
                    'mousedown_returncode':down.returncode,'mouseup_returncode':up.returncode,'hold_milliseconds':200,
                    'windows_after':after,'launcher_returncode_after':p.poll(),
                    'original_owned_windows_remaining':len(after_owned),
                    'exit_observed_before_cleanup':p.poll()==0 and not after_owned,
                    'server_started_or_login_attempted':False}
                if after_owned:
                    result['after_input_window_colormaps']=xcapture(colormap_helper,directory/'after-input',env,seal_dir=sealed_dir)
            if native_windows:
                from tools.stoneage_p3_private_frame import seal
                public=ROOT/'research/recovered/STONEAGE-P3-SESSION-TRANSPORT-PUBLIC.pem'
                if public.exists():
                    image=directory/'original-frame-1.png'
                    sealed=seal(image.read_bytes(),public.read_bytes())
                    path=Path('/tmp/stoneage-p3-private-frame-sealed.json')
                    path.write_text(json.dumps(sealed,sort_keys=True))
                    result['sealed_private_frame']={k:sealed[k] for k in ('schema','plaintext_sha256','plaintext_bytes','recipient_key_sha256')}
                    result['sealed_private_frame']['ciphertext_envelope_sha256']=digest_file(path)
            log.flush();text=(directory/'original-wine.log').read_text(errors='replace')
            result['wine_log_sha256']=hashlib.sha256(text.encode()).hexdigest()
            result['wine_diagnostic_lines']=[line[:400] for line in text.splitlines() if
                any(k in line.lower() for k in ('err:','exception','failed','could not','unhandled'))][:20]
            changes=[]
            for row in inventory():
                rel=Path(row['path']).relative_to('StoneAge');before=source/rel;after=run/rel
                require(digest_file(before)==row['sha256'],'baseline input was modified')
                if not after.exists() or digest_file(after)!=row['sha256']:changes.append(str(rel))
            result['original_input_baseline_unchanged']=True;result['runtime_copy_changed_paths']=changes
            result['runtime_status']='ORIGINAL_PROCESS_ATTEMPT_RECORDED_NO_WORLD_OR_VISUAL_CLASSIFICATION'
        output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print('P3_OBSERVATION='+json.dumps(result,ensure_ascii=True,separators=(',',':')))
    except Exception as exc:
        result.update(observation_error_type=type(exc).__name__,observation_error=str(exc))
        output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print('P3_OBSERVATION='+json.dumps(result,ensure_ascii=True,separators=(',',':')))
        raise
    finally:
        for p in processes:
            if p.poll() is None:p.terminate()
        command(['wineserver','-k'],env=env,timeout=10)
        display.terminate();display.wait(timeout=10);xlog.close()


def main():
    p=argparse.ArgumentParser();p.add_argument('--extract-disc',type=Path)
    p.add_argument('--directory',type=Path,required=True);p.add_argument('--control',type=Path)
    p.add_argument('--output',type=Path);p.add_argument('--original',action='store_true')
    p.add_argument('--depth-probe',action='store_true');p.add_argument('--colormap-helper',type=Path);a=p.parse_args()
    if a.extract_disc:print(json.dumps(extract(a.extract_disc,a.directory)))
    else:
        require(a.control is not None and a.output is not None,'control/output required')
        runtime(a.directory,a.control,a.output,a.original,a.depth_probe,a.colormap_helper)


if __name__=='__main__':main()
