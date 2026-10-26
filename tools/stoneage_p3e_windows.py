"""One finite native-Windows prerequisite package, synthetic programs only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
from tools.stoneage_p3d_bench import run_case, evaluate_case

ROOT=Path(__file__).resolve().parents[1]
LAYERS=('', '256COLOR', 'WINXPSP3 256COLOR')

def invoke(args,env=None):
    r=subprocess.run(args,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90)
    if r.returncode:raise ValueError(f'command failed {r.returncode}: {r.stderr.decode(errors="replace")[:500]}')
    return json.loads(r.stdout.decode('utf-8-sig'))

def powershell(script,env=None):
    return invoke(['pwsh','-NoProfile','-NonInteractive','-Command',
        "$ErrorActionPreference='Stop'; "+script+' | ConvertTo-Json -Depth 8 -Compress'],env)

def network_probe(exe,directory):
    """Exact program-path firewall canary, not a claim about original process trees."""
    alternate=directory/'unblocked-canary.exe';shutil.copyfile(exe,alternate)
    ip=socket.gethostbyname('api.github.com')
    def connect(program):return invoke([str(program),'connect',ip,'443'])
    env=os.environ.copy();env['P3E_PROGRAM']=str(exe)
    result={'scope':'synthetic_exact_program_path_tcp_ipv4_one_destination_only',
        'destination_host':'api.github.com','destination_ip':ip,'destination_port':443,
        'before':connect(exe),'original_process_isolation_qualified':False}
    try:
        result['rule']=powershell("""
        New-NetFirewallRule -Name StoneAgeP3ESyntheticOnly -DisplayName StoneAgeP3ESyntheticOnly -Program $env:P3E_PROGRAM -Direction Outbound -Action Block -Profile Any -Enabled True | Out-Null;
        $r=Get-NetFirewallRule -Name StoneAgeP3ESyntheticOnly;
        $p=$r | Get-NetFirewallApplicationFilter;
        [pscustomobject]@{direction=$r.Direction.ToString();action=$r.Action.ToString();enabled=$r.Enabled.ToString();profile=$r.Profile.ToString();program=$p.Program}
        """,env)
        result['profiles']=powershell('Get-NetFirewallProfile | Select-Object Name,Enabled')
        result['blocked_attempt']=connect(exe)
        result['unblocked_copy_during_rule']=connect(alternate)
    finally:
        result['cleanup']=powershell("Remove-NetFirewallRule -Name StoneAgeP3ESyntheticOnly -ErrorAction SilentlyContinue; [pscustomobject]@{remaining=@(Get-NetFirewallRule -Name StoneAgeP3ESyntheticOnly -ErrorAction SilentlyContinue).Count}")
    result['after_removal']=connect(exe)
    result['assessment']=evaluate_network(result)
    return result

def evaluate_network(n):
    r=n['rule']
    return bool(n['before']['connected'] and not n['blocked_attempt']['connected'] and
        n['blocked_attempt']['wsa_error']==10013 and n['unblocked_copy_during_rule']['connected'] and
        n['after_removal']['connected'] and n['cleanup']['remaining']==0 and
        r['direction']=='Outbound' and r['action']=='Block' and r['enabled']=='True' and r['profile']=='Any' and
        n['profiles'] and all(p['Enabled'] for p in n['profiles']))

def qualify(cases):
    # One actual receiving process must satisfy all prerequisites simultaneously.
    return any(c['mode']=='ddraw' and c['palette_state']['display_bpp']==8 and
        c['palette_state']['windows_acp']==950 and all(evaluate_case(c)[k] for k in
        ('color_gate_passed','sendinput_gate_passed','foreground_gate_passed')) for c in cases)

def main():
    a=argparse.ArgumentParser();a.add_argument('--environment-exe',type=Path,required=True)
    a.add_argument('--control-exe',type=Path,required=True);a.add_argument('--directory',type=Path,required=True)
    a.add_argument('--output',type=Path,required=True);args=a.parse_args()
    if os.name!='nt':raise ValueError('native Windows only')
    directory=args.directory.resolve()
    if directory.exists() or directory==ROOT or ROOT in directory.parents:raise ValueError('new external scratch directory required')
    directory.mkdir();report={'schema':'stoneage.p3e.available_windows.v1','original_downloaded':False,
        'original_executed':False,'world_entered':False,'original_process_isolation_qualified':False,'cases':[]}
    report['source_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in
        ('tools/stoneage_p3e_environment.c','tools/stoneage_p3e_windows.py','tools/stoneage_p3d_control.c','tools/stoneage_p3d_bench.py')}
    try:
        report['system_locale']=powershell("[pscustomobject]@{locale=(Get-WinSystemLocale).Name; registry_acp=(Get-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Nls\\CodePage').ACP; restart_performed=$false; locale_changed=$false}")
        for i,layer in enumerate(LAYERS):
            env=os.environ.copy()
            if layer:env['__COMPAT_LAYER']=layer
            else:env.pop('__COMPAT_LAYER',None)
            entry={'requested_layer':layer,'environment':invoke([str(args.environment_exe)],env),'controls':[]}
            report['cases'].append(entry)
            for mode in ('gdi','ddraw'):
                entry['controls'].append(run_case(directory/f'case-{i}-{mode}',args.control_exe,env,mode,None,True))
            entry['simultaneous_synthetic_prerequisites']=qualify(entry['controls'])
        report['network']=network_probe(args.environment_exe,directory)
        report['usable_original_environment']=False  # Original process isolation never qualified here.
        report['display_encoding_input_candidate_found']=any(c['simultaneous_synthetic_prerequisites'] for c in report['cases'])
        report['status']='SYNTHETIC_CANDIDATE_REQUIRES_ORIGINAL_PATH_ISOLATION' if report['display_encoding_input_candidate_found'] else 'BLOCKED_AVAILABLE_WINDOWS_ENVIRONMENT'
    except Exception as e:
        report.update(probe_error_type=type(e).__name__,probe_error=str(e));raise
    finally:
        args.output.write_bytes((json.dumps(report,ensure_ascii=True,indent=2)+'\n').encode())
    print(report['status'])

if __name__=='__main__':main()
