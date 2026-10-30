"""One own-program Windows prerequisite observation; never launches game code.

Private original-input injection is unavailable in the current connector. Even a
passing finite network observation does not authorize or claim a server boot.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import time

RULES=('StoneAgeSCENE34Outbound','StoneAgeSCENE34Inbound')
TASK='StoneAgeSCENE34Restore'
FALSE=('historical_programs_executed','original_inputs_received_in_Windows',
 'original_server_boot_attempted','SAAC_GMSV_handshake_observed','original_world_entered',
 'client_executed','account_entered','private_source_transport_available',
 'original_execution_admitted','all_network_paths_experimentally_tested')

def need(ok,message):
    if not ok:raise ValueError(message)

def ps(script):
    r=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command',
        "$ErrorActionPreference='Stop'; "+script+' | ConvertTo-Json -Depth 10 -Compress'],capture_output=True,timeout=20,check=True)
    return json.loads(r.stdout.decode('utf-8-sig'))

def state():
    return ps("$rs=@(Get-NetFirewallRule -Name StoneAgeSCENE34Outbound,StoneAgeSCENE34Inbound); @($rs | ForEach-Object { $r=$_;$a=$r|Get-NetFirewallApplicationFilter;$p=$r|Get-NetFirewallPortFilter; [pscustomobject]@{name=$r.Name;direction=$r.Direction.ToString();action=$r.Action.ToString();enabled=$r.Enabled.ToString();profile=$r.Profile.ToString();program=$a.Program;protocol=$p.Protocol.ToString()} })")

def arm():
    watchdog=ps("""
    if(@(Get-NetFirewallRule -Name StoneAgeSCENE34Outbound,StoneAgeSCENE34Inbound -ErrorAction SilentlyContinue).Count){throw 'unexpected rule'};
    $cmd='Remove-NetFirewallRule -Name StoneAgeSCENE34Outbound,StoneAgeSCENE34Inbound -ErrorAction SilentlyContinue';
    $a=New-ScheduledTaskAction -Execute powershell.exe -Argument ('-NoProfile -NonInteractive -Command "'+$cmd+'"');
    Register-ScheduledTask -TaskName StoneAgeSCENE34Restore -Action $a -Trigger (New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2)) -User SYSTEM -RunLevel Highest | Out-Null;
    $t=Get-ScheduledTask -TaskName StoneAgeSCENE34Restore;[pscustomobject]@{registered=($t.State -eq 'Ready');user=$t.Principal.UserId}
    """)
    need(watchdog['registered'] and watchdog['user']=='SYSTEM','independent restore task')
    profiles=ps('Get-NetFirewallProfile | Select-Object Name,Enabled')
    need(len(profiles)==3 and all(x['Enabled']for x in profiles),'three enabled firewall profiles')
    for rule,direction in zip(RULES,('Outbound','Inbound')):
        ps(f"New-NetFirewallRule -Name {rule} -DisplayName {rule} -Direction {direction} -Action Block -Profile Any -Protocol Any -LocalAddress Any -RemoteAddress Any -Enabled True | Out-Null; [pscustomobject]@{{created=$true}}")
    return dict(watchdog=watchdog,profiles=profiles,rules=state())

def disarm():
    r=ps("Remove-NetFirewallRule -Name StoneAgeSCENE34Outbound,StoneAgeSCENE34Inbound -ErrorAction SilentlyContinue; [pscustomobject]@{remaining=@(Get-NetFirewallRule -Name StoneAgeSCENE34Outbound,StoneAgeSCENE34Inbound -ErrorAction SilentlyContinue).Count}")
    need(r['remaining']==0,'retain watchdog until rules removed')
    ps("Unregister-ScheduledTask -TaskName StoneAgeSCENE34Restore -Confirm:$false -ErrorAction SilentlyContinue;[pscustomobject]@{done=$true}")
    return r

def rules_ok(rules):
    return len(rules)==2 and {r['direction']for r in rules}=={'Inbound','Outbound'} and {r['name']for r in rules}==set(RULES) and all(
        r['action']=='Block' and r['enabled']=='True' and r['profile']=='Any' and r['program']=='Any' and r['protocol']=='Any'for r in rules)

def pair_ok(p):
    return bool(p['server_exit']==p['client_exit']==0 and p['ready']['bind_address']=='127.0.0.1' and p['ready']['ready'] and p['ready']['port']==19200 and p['ready']['pointer_bytes']==4 and
        p['server_pid']!=p['client_pid'] and p['server']['pid']==p['server_pid'] and p['client']['pid']==p['client_pid'] and
        p['ready']['pid']==p['server_pid'] and all(p[role]['connected'] and p[role]['echo_exact'] and p[role]['wsa_error']==0 for role in ('server','client')) and
        p['image_identity_verified'] and all(j['created_suspended'] and j['assigned_before_resume'] and j['limit_flags']==0x2008 and j['active_process_limit']==1 for j in p['jobs']))

def evaluate(r):
    need(all(r[k]is False for k in FALSE),'own prerequisites are not original server/world execution')
    need(r['scope']=='OWN_X86_TWO_PROCESS_TCP_IPV4_LOOPBACK_AND_ONE_EXTERNAL_CANARY','bounded experiment scope')
    return bool(r.get('error')is None and rules_ok(r['isolation']['rules']) and rules_ok(r['rules_before_restore']) and
        len(r['isolation']['profiles'])==3 and all(p['Enabled']for p in r['isolation']['profiles']) and
        r['isolation']['watchdog']['registered'] and r['isolation']['watchdog']['user']=='SYSTEM' and
        all(pair_ok(r[x])for x in ('loopback_before','loopback_during','loopback_after')) and
        r['canary_before']['connected'] and r['canary_after']['connected'] and
        all(not r[x]['connected'] and r[x]['wsa_error']==10013 for x in ('canary_blocked_before','canary_blocked_after')) and
        r['cleanup']['remaining']==0 and r['jobs_closed_before_network_restore'] and r['hold_cleanup_observed'] and
        0<r['seconds_under_rules']<100)

def main():
    a=argparse.ArgumentParser();a.add_argument('--probe',type=Path,required=True);a.add_argument('--work',type=Path,required=True);a.add_argument('--output',type=Path,required=True);args=a.parse_args()
    need(os.name=='nt' and os.environ.get('GITHUB_ACTIONS')=='true' and os.environ.get('RUNNER_ENVIRONMENT')=='github-hosted','only disposable github-hosted Windows')
    from tools.stoneage_p3h_native import JobProcess,Native
    work=args.work.resolve();need(not work.exists(),'new own-program directory');work.mkdir(parents=True)
    probe=args.probe.resolve();need(probe.is_file(),'own probe exists');native=Native();jobs=[];start=time.monotonic()
    raw=probe.read_bytes();pe=struct.unpack_from('<I',raw,60)[0]
    need(raw[:2]==b'MZ' and raw[pe:pe+4]==b'PE\0\0' and struct.unpack_from('<H',raw,pe+4)[0]==0x14c,'actual own probe x86 PE')
    r=dict(schema='stoneage.scene34.own_windows_prerequisite.r1',scope='OWN_X86_TWO_PROCESS_TCP_IPV4_LOOPBACK_AND_ONE_EXTERNAL_CANARY',
        input_probe_sha256=hashlib.sha256(probe.read_bytes()).hexdigest(),pointer_bytes=4,own_probe_compiled_x86=True,
        source_sha256={p:hashlib.sha256((Path(__file__).resolve().parents[1]/p).read_bytes()).hexdigest() for p in
            ('tools/stoneage_scene34_loopback.c','tools/stoneage_scene34_windows_gate.py','tools/stoneage_p3h_native.py')},
        runner_image=os.environ.get('ImageVersion'),source_action_run_id=os.environ.get('GITHUB_RUN_ID'),
        execution_HEAD=os.environ.get('GITHUB_SHA'),error=None,**{k:False for k in FALSE})
    def own(args_):
        need(time.monotonic()-start<95,'finite gate deadline')
        p=JobProcess(probe,args_,work,os.environ.copy());jobs.append(p);return p
    def canary(tag):
        p=work/(tag+'.json');call=subprocess.run([str(probe),'canary',address,'443',str(p),'unused'],capture_output=True,timeout=7,check=True)
        return json.loads(p.read_text())
    def loopback(tag):
        ready=work/(tag+'-ready.json');server=work/(tag+'-server.json');client=work/(tag+'-client.json')
        s=own(['listen','127.0.0.1','19200',str(ready),str(server)]);until=time.monotonic()+3
        ready_value=None
        while ready_value is None and s.poll()is None and time.monotonic()<until:
            try:ready_value=json.loads(ready.read_text())
            except (FileNotFoundError,json.JSONDecodeError):time.sleep(.03)
        need(ready_value is not None,'own listener ready')
        c=own(['echo','127.0.0.1','19200',str(client),'unused'])
        ce=c.wait(6);se=s.wait(3)
        result=dict(server_pid=s.pid,client_pid=c.pid,ready=ready_value,server_exit=se,client_exit=ce,
            server=json.loads(server.read_text()),client=json.loads(client.read_text()),jobs=[s.job_state,c.job_state],
            image_identity_verified=identities[s.pid] and identities[c.pid])
        s.close();c.close();jobs.remove(s);jobs.remove(c);return result
    identities={}
    original_own=own
    def own(args_):
        import ctypes as C
        from ctypes import wintypes as W
        p=original_own(args_);path=C.create_unicode_buffer(2048);length=W.DWORD(len(path))
        identities[p.pid]=bool(native.k.QueryFullProcessImageNameW(p.handle,0,path,C.byref(length))) and Path(path.value).resolve()==probe
        return p
    address=socket.gethostbyname('api.github.com');r['external_canary']=dict(host='api.github.com',IPv4=address,port=443)
    armed=False
    try:
        r['canary_before']=canary('before');need(r['canary_before']['connected'],'external live canary before rules')
        r['loopback_before']=loopback('before');need(pair_ok(r['loopback_before']),'loopback before rules')
        h=own(['hold']);need(h.poll()is None,'own hold alive');pid=h.pid;h.close();jobs.remove(h)
        until=time.monotonic()+1
        while native.image(pid) and time.monotonic()<until:time.sleep(.03)
        r['hold_cleanup_observed']=not native.image(pid);need(r['hold_cleanup_observed'],'own Job cleanup')
        collision=ps("[pscustomobject]@{rules=@(Get-NetFirewallRule -Name StoneAgeSCENE34Outbound,StoneAgeSCENE34Inbound -ErrorAction SilentlyContinue).Count;tasks=@(Get-ScheduledTask -TaskName StoneAgeSCENE34Restore -ErrorAction SilentlyContinue).Count}")
        need(collision['rules']==collision['tasks']==0,'no preexisting task-owned names')
        armed=True;r['isolation']=arm();under=time.monotonic();need(rules_ok(r['isolation']['rules']),'two complete block rules')
        r['canary_blocked_before']=canary('blocked-before');need(not r['canary_blocked_before']['connected'] and r['canary_blocked_before']['wsa_error']==10013,'blocked external canary')
        r['loopback_during']=loopback('during');need(pair_ok(r['loopback_during']),'loopback during both block rules')
        r['canary_blocked_after']=canary('blocked-after');r['rules_before_restore']=state();r['seconds_under_rules']=time.monotonic()-under
    except Exception as e:r['error']=type(e).__name__+': '+str(e)[:240]
    finally:
        for p in jobs:p.close()
        r['jobs_closed_before_network_restore']=True
        if armed:r['cleanup']=disarm()
    try:
        r['canary_after']=canary('after');r['loopback_after']=loopback('after')
        r['finite_tcp_ipv4_gate_passed']=evaluate(r)
    except Exception as e:
        r['finite_tcp_ipv4_gate_passed']=False
        if r['error']is None:r['error']=type(e).__name__+': '+str(e)[:240]
    r['stop']='PRIVATE_SOURCE_TO_WINDOWS_CHANNEL_UNAVAILABLE'if r['finite_tcp_ipv4_gate_passed']else'ISOLATION_QUALIFICATION_FAILED'
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(r,ensure_ascii=False));return 0

if __name__=='__main__':main()
