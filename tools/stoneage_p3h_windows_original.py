"""Source-pinned TW1 private Windows login experiment; never an original server.

Public output admits derived metadata and CMS ciphertext only. Original runtime
and all frames are retained together privately for reproducible later work.
"""
from concurrent.futures import ThreadPoolExecutor
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import zipfile
from urllib.request import Request,urlopen
from tools.stoneage_p3_boot import ROOT,inventory,extract,LAUNCH_ARGS,frame,digest_file,require
from tools.stoneage_p3g_manifest_environment import manifest,simultaneous
from tools.stoneage_p3f_manifest_probe import collect
from tools.stoneage_p3d_bench import run_case
from tools.stoneage_p3e_windows import powershell,invoke
from tools.stoneage_p3h_native import Native,JobProcess

CERT_SHA='a3ffff68f3a1fd61ee7252f4e63f2aeb8e5fab239eeaed2bae0ae93b6a592e90'
RULE='StoneAgeP3HGuestOutbound';TASK='StoneAgeP3HGuestRestore'

def fingerprint(p):return dict(bytes=p.stat().st_size,sha256=digest_file(p))

def portable_acquire(output):
    from tools.stoneage_tw10_archive_parallel_download import ranges,_allowed_source
    from tools.stoneage_tw10_archive_chunk_download import approved_source,_verify_response,ARCHIVE_SIZE,ARCHIVE_MD5,ARCHIVE_SHA1,USER_AGENT
    url=approved_source();_allowed_source(url);deadline=time.monotonic()+1200
    with output.open('xb') as f:f.truncate(ARCHIVE_SIZE)
    def chunk(span):
        start,end=span
        for attempt in range(2):
            try:
                require(time.monotonic()<deadline,'original acquisition deadline')
                req=Request(url,headers={'User-Agent':USER_AGENT,'Range':f'bytes={start}-{end}'})
                with urlopen(req,timeout=30) as res,output.open('r+b') as f:
                    _verify_response(res,url,start,end,ARCHIVE_SIZE);f.seek(start);remaining=end-start+1
                    while remaining:
                        require(time.monotonic()<deadline,'original acquisition deadline')
                        b=res.read(min(1024*1024,remaining));require(b and len(b)<=remaining,'short/excess archive range')
                        require(f.write(b)==len(b),'short private write');remaining-=len(b)
                return end-start+1
            except Exception:
                if attempt:raise
                time.sleep(.5)
    with ThreadPoolExecutor(max_workers=16) as pool:total=sum(pool.map(chunk,ranges(ARCHIVE_SIZE,8*1024*1024)))
    require(total==ARCHIVE_SIZE,'whole carrier extent')
    hashes={name:hashlib.new(name) for name in ('md5','sha1','sha256')}
    with output.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):
            for h in hashes.values():h.update(b)
    require(hashes['md5'].hexdigest()==ARCHIVE_MD5 and hashes['sha1'].hexdigest()==ARCHIVE_SHA1,'original whole carrier identity')
    return dict(bytes=total,**{k:v.hexdigest() for k,v in hashes.items()},all_ranges_strict_206=True)

def sidecar_preflight(work,checker,control):
    result={'original_executed':False}
    plain=work/'plain';side=work/'sidecar';plain.mkdir();side.mkdir()
    a=plain/'sa_3.exe';b=side/'sa_3.exe';shutil.copyfile(checker,a);shutil.copyfile(checker,b)
    (side/'sa_3.exe.manifest').write_text(manifest('zh-TW'),encoding='utf-8')
    h=digest_file(a);require(h==digest_file(b),'unchanged synthetic EXE pair')
    result['plain']=collect(a,'256COLOR');result['external_manifest']=collect(b,'256COLOR')
    require(result['plain']['acp_before']==1252 and result['external_manifest']['acp_before']==950 and
            result['external_manifest']['display_bpp']==8 and result['external_manifest']['ddraw_current'][2]==8,
            'external manifest does not qualify unchanged x86 image')
    receiver=side/'control.exe';shutil.copyfile(control,receiver)
    (side/'control.exe.manifest').write_text(manifest('zh-TW'),encoding='utf-8')
    env=os.environ.copy();env['__COMPAT_LAYER']='256COLOR'
    result['receiver']=run_case(work/'sidecar-ddraw',receiver,env,'ddraw',None,True)
    require(simultaneous(result['receiver']),'same-process sidecar RGB and received input gate')
    smoke=JobProcess(b,[],side,env)
    try:result['job_smoke']=smoke.job_state;require(smoke.wait(20)==0,'suspended-assigned-resumed own process must exit normally')
    finally:smoke.close()
    require(digest_file(a)==digest_file(b)==h,'sidecar must not modify either EXE')
    result.update(binary_sha256=h,unchanged_PE_pair=True,synthetic_sidecar_candidate=True)
    return result

def state_rule():
    return powershell(f"""$r=Get-NetFirewallRule -Name {RULE};$p=$r|Get-NetFirewallPortFilter;$a=$r|Get-NetFirewallApplicationFilter;
    [pscustomobject]@{{direction=$r.Direction.ToString();action=$r.Action.ToString();enabled=$r.Enabled.ToString();
    profile=$r.Profile.ToString();protocol=$p.Protocol.ToString();program=$a.Program}}""")

def arm():
    watchdog=powershell(f"""
    if(Get-NetFirewallRule -Name {RULE} -ErrorAction SilentlyContinue){{throw 'unexpected rule exists'}};
    $cmd='Remove-NetFirewallRule -Name {RULE} -ErrorAction SilentlyContinue';
    $a=New-ScheduledTaskAction -Execute powershell.exe -Argument ('-NoProfile -NonInteractive -Command "'+$cmd+'"');
    Register-ScheduledTask -TaskName {TASK} -Action $a -Trigger (New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2)) -User SYSTEM -RunLevel Highest | Out-Null;
    $t=Get-ScheduledTask -TaskName {TASK};[pscustomobject]@{{registered=($t.State -eq 'Ready');user=$t.Principal.UserId}}
    """)
    require(watchdog['registered'] and watchdog['user']=='SYSTEM','independent restore watchdog required')
    profiles=powershell('Get-NetFirewallProfile | Select-Object Name,Enabled')
    require(len(profiles)==3 and all(p['Enabled'] for p in profiles),'all profiles required')
    powershell(f"New-NetFirewallRule -Name {RULE} -DisplayName {RULE} -Direction Outbound -Action Block -Profile Any -Protocol Any -RemoteAddress Any -LocalAddress Any -Enabled True | Out-Null; [pscustomobject]@{{created=$true}}")
    return dict(watchdog=watchdog,profiles=profiles,rule=state_rule())

def disarm():
    r=powershell(f"Remove-NetFirewallRule -Name {RULE} -ErrorAction SilentlyContinue; [pscustomobject]@{{remaining=@(Get-NetFirewallRule -Name {RULE} -ErrorAction SilentlyContinue).Count}}")
    require(r['remaining']==0,'temporary rule remains; leave independent watchdog armed')
    powershell(f"Unregister-ScheduledTask -TaskName {TASK} -Confirm:$false -ErrorAction SilentlyContinue; [pscustomobject]@{{done=$true}}")
    return r

def surface(windows,exe):
    require(len(windows)==1,'input blocked by missing/extra owned window or dialog')
    w=windows[0]
    require(w['klass']=='ＳｔｏｎｅＡｇｅ' and w['client_size']==[640,480] and
            Path(w['image']).resolve()==exe.resolve(),'input surface is not exact original main image')
    return w

def original_runtime(work,checker,receiver,result):
    import socket
    from PIL import ImageGrab
    run=work/'run';shutil.copytree(work/'source',run);exe=run/'sa_3.exe'
    expected=next(r for r in inventory() if r['path']=='StoneAge/sa_3.exe')
    require(digest_file(exe)==expected['sha256'],'actual original EXE pin')
    (run/'sa_3.exe.manifest').write_text(manifest('zh-TW'),encoding='utf-8')
    address=socket.gethostbyname('api.github.com')
    connect=lambda:invoke([str(checker),'connect',address,'443'])
    result.update({'original_executable':fingerprint(exe),'original_executable_modified':False,
            'original_world_entered':False,'account_or_password_entered':False,
            'historical_server_contacted':False,'original_GetACP_directly_measured':False,
            'original_launch_args':list(LAUNCH_ARGS),'observations':[],
            'original_client_execution_attempted':False,'original_visible_main_observed':False,'quit_exit_before_cleanup':False})
    result['network_before']=connect();require(result['network_before']['connected'],'live external canary before isolation')
    process=None;native=Native();frames=work/'frames';frames.mkdir()
    env=os.environ.copy();env['__COMPAT_LAYER']='256COLOR'
    try:
        result['isolation']=arm();start=time.monotonic()
        blocked=connect();result['network_blocked_before']=blocked
        require(not blocked['connected'] and blocked['wsa_error']==10013,'fail closed before original execution')
        gate=run_case(work/'blocked-own-receiver',receiver,env,'ddraw',None,True)
        result['same_blocked_guest_synthetic_receiver']=gate
        require(simultaneous(gate),'source environment changed before original launch')
        process=JobProcess(exe,LAUNCH_ARGS,run,env)
        result.update(original_client_execution_attempted=True,pid=process.pid,job=process.job_state,
                      actual_process_image=native.image(process.pid))
        require(Path(result['actual_process_image']).resolve()==exe.resolve(),'actual process image identity')
        for delay in (2,3,3):
            time.sleep(delay);windows=native.windows(process.pid)
            entry=dict(seconds_since_isolation=time.monotonic()-start,windows=windows,process_exit=process.poll())
            if windows:
                # Capture only the owned client rectangle, never the whole desktop.
                w=windows[0];x,y=w['client_origin'];ww,hh=w['client_size']
                if 0<ww<=1024 and 0<hh<=768:
                    p=frames/f'original-frame-{len(result["observations"])}.png'
                    ImageGrab.grab(bbox=(x,y,x+ww,y+hh)).save(p);entry['frame']=frame(p)
            result['observations'].append(entry)
        result['original_visible_main_observed']=any(w['klass']=='ＳｔｏｎｅＡｇｅ' for e in result['observations'] for w in e['windows'])
        try:
            w=surface(native.windows(process.pid),exe)
            require(process.poll() is None,'original must still be alive before input')
            require(native.activate(w),'actual foreground activation failed')
            result['quit_input']=native.click(w,350,380)
            result['exit_after_quit']=process.wait(5)
            result['owned_windows_after_quit']=native.windows(process.pid)
            result['quit_exit_before_cleanup']=result['exit_after_quit']==0 and not result['owned_windows_after_quit'] and all(result['quit_input'][k]==1 for k in ('sendinput_down','sendinput_up'))
        except Exception as e:result['input_gate_error']=type(e).__name__+': '+str(e)
        result['rule_after_original']=state_rule();result['network_blocked_after']=connect()
        require(not result['network_blocked_after']['connected'] and result['network_blocked_after']['wsa_error']==10013,'isolation expired during original observation')
        require(time.monotonic()-start<110,'observation exceeded bounded isolation window')
    finally:
        if process:
            result['exit_before_cleanup']=process.poll();process.close();result['job_closed_before_network_restore']=True
        result['isolation_cleanup']=disarm();result['network_after_restore']=connect()
    require(digest_file(exe)==expected['sha256'],'original EXE changed on disk')
    return result

def run(a):
    require(os.name=='nt' and os.environ.get('GITHUB_ACTIONS')=='true' and os.environ.get('RUNNER_ENVIRONMENT')=='github-hosted','disposable hosted Windows only')
    work=a.work.resolve();out=a.output.resolve()
    require(ROOT not in work.parents and not work.exists() and ROOT not in out.parents and not out.exists(),'new private external directories')
    require(digest_file(a.certificate)==CERT_SHA,'private transfer recipient pin')
    require(shutil.which('7z') or shutil.which('7z.exe'),'static RAR extractor unavailable')
    work.mkdir();out.mkdir();report={'schema':'stoneage.p3h.original_windows_login.v1','original_downloaded':False,
        'original_client_executed':False,'original_world_entered':False,'original_server_contacted':False,
        'private_original_data_published':False,'host_image_os':os.environ.get('ImageOS'),
        'host_image_version':os.environ.get('ImageVersion'),'runtime':None}
    try:
        report['preflight']=sidecar_preflight(work,a.checker.resolve(),a.control.resolve())
        print('P3H_UNCHANGED_SIDECAR_AND_JOB_PREFLIGHT=PASS',flush=True)
        report['original_carrier_acquisition_attempted']=True
        report['carrier']=portable_acquire(work/'CD_DIC.rar');report['original_downloaded']=True
        print('P3H_PINNED_ORIGINAL_CARRIER=PASS',flush=True)
        subprocess.run(['7z','x','-y','-o'+str(work),str(work/'CD_DIC.rar'),'STONEAGE.bin'],check=True,stdout=subprocess.DEVNULL)
        report['extraction']=extract(work/'STONEAGE.bin',work/'source')
        report['runtime']={}
        try:original_runtime(work,work/'sidecar/sa_3.exe',work/'sidecar/control.exe',report['runtime'])
        except Exception as e:report['runtime_error']=type(e).__name__+': '+str(e)[:240]
        report['original_client_executed']=report['runtime'].get('original_client_execution_attempted',False)
        # Keep only the immutable authenticated original tree plus private captures.
        private=work/'private-runtime-and-observation.zip'
        with zipfile.ZipFile(private,'w',compression=zipfile.ZIP_STORED) as z:
            for row in inventory():
                p=work/'source'/Path(row['path']).relative_to('StoneAge')
                require(p.stat().st_size==int(row['size']) and digest_file(p)==row['sha256'],'immutable private runtime changed')
                z.write(p,'source/'+str(Path(row['path']).relative_to('StoneAge')).replace('\\','/'))
            for p in (work/'frames').glob('*.png'):z.write(p,'frames/'+p.name)
            z.writestr('private-source-report.json',json.dumps(report,ensure_ascii=True,indent=2))
        require(private.stat().st_size<400*1024*1024,'private retention size bound')
        report['private_runtime_zip']=fingerprint(private)
        sealed=out/'private-runtime-and-observation.der'
        subprocess.run([str(a.openssl),'cms','-encrypt','-binary','-aes-256-cbc','-in',str(private),'-out',str(sealed),'-outform','DER',str(a.certificate.resolve())],check=True,capture_output=True)
        report['encrypted_private_runtime']=fingerprint(sealed)
        report['transfer_certificate_sha256']=CERT_SHA
        print('P3H_ORIGINAL_WINDOWS_RESULT',json.dumps(dict(main=report['runtime'].get('original_visible_main_observed'),quit=report['runtime']['quit_exit_before_cleanup'],world_entered=False)),flush=True)
    except Exception as e:
        report.update(error_type=type(e).__name__,error=str(e)[:300]);raise
    finally:
        if report.get('runtime'):
            report['original_client_executed']=report['runtime'].get('original_client_execution_attempted',False)
        (out/'source-report.json').write_text(json.dumps(report,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
        shutil.rmtree(work,ignore_errors=True)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for key in ('work','output','checker','control','certificate','openssl'):p.add_argument('--'+key,type=Path,required=True)
    run(p.parse_args())
