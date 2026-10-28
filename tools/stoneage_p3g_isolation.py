"""Finite disposable-runner outbound-denial test; no original program permitted.

One exact temporary global rule is removed in finally and by a pre-registered
SYSTEM watchdog. This does not claim an adversarial malware security boundary.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import time
from tools.stoneage_p3e_windows import powershell,invoke
from tools.stoneage_p3f_manifest_probe import collect
from tools.stoneage_p3d_bench import run_case
from tools.stoneage_p3g_manifest_environment import simultaneous,require

RULE='StoneAgeP3GDisposableGuestOutbound'
TASK='StoneAgeP3GDisposableGuestRestore'

def qualifies(r):
    rule=r['rule'];after=r['after_controls_rule']
    return bool(r['before']['connected'] and r['alternate_before']['connected'] and
        all(not r[k]['connected'] and r[k]['wsa_error']==10013 for k in
            ('blocked','alternate_blocked','after_controls_blocked')) and
        r['after_restore']['connected'] and r['cleanup']['remaining']==0 and
        len(r['profiles'])==3 and {p['Name'] for p in r['profiles']}=={'Domain','Private','Public'} and
        all(p['Enabled'] for p in r['profiles']) and
        all(v['action']=='Block' and v['direction']=='Outbound' and v['profile']=='Any' and
            v['enabled']=='True' and v['protocol']=='Any' and v['program']=='Any' and
            v['remote_address']==['Any'] and v['local_address']==['Any'] for v in (rule,after)) and
        r['watchdog']['registered'] and r['watchdog']['user']=='SYSTEM' and
        r['probe_during_block']['acp_before']==950 and r['probe_during_block']['display_bpp']==8 and
        any(simultaneous(c) for c in r['controls_during_block']))

def rule_state():
    return powershell(f"""
    $r=Get-NetFirewallRule -Name {RULE};$p=$r|Get-NetFirewallPortFilter;
    $a=$r|Get-NetFirewallApplicationFilter;$n=$r|Get-NetFirewallAddressFilter;
    [pscustomobject]@{{action=$r.Action.ToString();direction=$r.Direction.ToString();
      enabled=$r.Enabled.ToString();profile=$r.Profile.ToString();protocol=$p.Protocol.ToString();
      program=$a.Program;remote_address=@($n.RemoteAddress);local_address=@($n.LocalAddress)}}
    """)

def run(directory,output):
    require(os.name=='nt','disposable native Windows runner only')
    require(os.environ.get('GITHUB_ACTIONS')=='true' and os.environ.get('RUNNER_ENVIRONMENT')=='github-hosted',
            'never alter personal, persistent or self-hosted firewall')
    exe=directory/'correct_zh_tw.exe';alternate=directory/'network-copy.exe'
    require(exe.read_bytes()==alternate.read_bytes(),'exact synthetic executable copies required')
    address=socket.gethostbyname('api.github.com')
    def connect(path):return invoke([str(path),'connect',address,'443'])
    r={'schema':'stoneage.p3g.disposable_host_egress.v1','original_client_downloaded':False,
       'original_client_executed':False,'original_world_entered':False,
       'original_process_isolation_qualified':False,'original_ANSI_GDI_text_qualified':False,
       'usable_original_environment':False,'target_host':'api.github.com','target_ipv4':address,'target_port':443,
       'policy_scope':'temporary_all_programs_all_protocols_all_remote_addresses_guest_rule',
       'empirical_network_scope':'two_self_authored_program_paths_one_external_TCP_IPv4_destination',
       'loopback_server_qualified':False,'IPv6_and_UDP_empirically_tested':False,
       'host_image_os':os.environ.get('ImageOS'),'host_image_version':os.environ.get('ImageVersion'),
       'controls_during_block':[],
       'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    try:
        r['before']=connect(exe);r['alternate_before']=connect(alternate)
        require(r['before']['connected'] and r['alternate_before']['connected'],'live destination required before blocking')
        r['watchdog']=powershell(f"""
        if(Get-NetFirewallRule -Name {RULE} -ErrorAction SilentlyContinue){{throw 'Rule name already exists'}};
        if(Get-ScheduledTask -TaskName {TASK} -ErrorAction SilentlyContinue){{throw 'Watchdog name already exists'}};
        $cmd='Remove-NetFirewallRule -Name {RULE} -ErrorAction SilentlyContinue';
        $action=New-ScheduledTaskAction -Execute 'powershell.exe' -Argument ('-NoProfile -NonInteractive -Command "'+$cmd+'"');
        $trigger=New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2);
        Register-ScheduledTask -TaskName {TASK} -Action $action -Trigger $trigger -User SYSTEM -RunLevel Highest | Out-Null;
        $t=Get-ScheduledTask -TaskName {TASK};
        [pscustomobject]@{{registered=($t.State -eq 'Ready');user=$t.Principal.UserId;restore_delay_seconds=120}}
        """)
        require(r['watchdog']['registered'],'independent restore watchdog must exist before blocking')
        r['profiles']=powershell('Get-NetFirewallProfile | Select-Object Name,Enabled')
        require(all(p['Enabled'] for p in r['profiles']),'all host firewall profiles enabled')
        powershell(f"New-NetFirewallRule -Name {RULE} -DisplayName {RULE} -Direction Outbound -Action Block -Profile Any -Protocol Any -RemoteAddress Any -LocalAddress Any -Enabled True | Out-Null; [pscustomobject]@{{created=$true}}")
        r['rule']=rule_state();started=time.monotonic()
        r['blocked']=connect(exe);r['alternate_blocked']=connect(alternate)
        require(not r['blocked']['connected'] and r['blocked']['wsa_error']==10013 and
                not r['alternate_blocked']['connected'] and r['alternate_blocked']['wsa_error']==10013,
                'actual WSAEACCES on both program paths required')
        r['probe_during_block']=collect(exe,'256COLOR')
        env=os.environ.copy();env['__COMPAT_LAYER']='256COLOR'
        r['controls_during_block'].append(run_case(directory/'isolated-ddraw',directory/'control-zh-tw.exe',env,'ddraw',None,True))
        r['after_controls_rule']=rule_state();r['after_controls_blocked']=connect(exe)
        r['measured_block_window_seconds']=time.monotonic()-started
    finally:
        r['cleanup']=powershell(f"Remove-NetFirewallRule -Name {RULE} -ErrorAction SilentlyContinue; [pscustomobject]@{{remaining=@(Get-NetFirewallRule -Name {RULE} -ErrorAction SilentlyContinue).Count}}")
        require(r['cleanup']['remaining']==0,'leave watchdog registered if primary cleanup fails')
        r['after_restore']=connect(exe)
        powershell(f"Unregister-ScheduledTask -TaskName {TASK} -Confirm:$false -ErrorAction SilentlyContinue; [pscustomobject]@{{remaining=@(Get-ScheduledTask -TaskName {TASK} -ErrorAction SilentlyContinue).Count}}")
        r['bounded_synthetic_egress_display_input_candidate']=qualifies(r) if 'after_controls_blocked' in r else False
        output.write_text(json.dumps(r,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
    require(r['bounded_synthetic_egress_display_input_candidate'],'finite synthetic isolation candidate did not qualify')
    print('P3G_BOUNDED_SYNTHETIC_HOST_DENIAL=PASS; ORIGINAL_WORLD_ENTERED=FALSE')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.directory,a.output)
