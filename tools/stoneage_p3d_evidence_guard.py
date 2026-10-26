"""Replay P3D synthetic measurements, preserving original-client unknowns."""
import hashlib
import json
from pathlib import Path
from tools.stoneage_p3d_bench import evaluate_case,input_delta

ROOT=Path(__file__).resolve().parents[1]
RECOVERED=ROOT/'research/recovered'


def need(ok,message):
    if not ok:raise ValueError(message)


def verify_report(report):
    need(report['schema']=='stoneage.p3d.synthetic_environment_gate.v1','schema')
    for key in ('original_client_downloaded','original_client_executed','original_game_world_entered'):
        need(report[key] is False,'synthetic overclaim: '+key)
    need('probe_error' not in report,'incomplete probe')
    need([c['mode'] for c in report['cases']]==['gdi','ddraw'],'finite render paths')
    for c in report['cases']:
        need(c['original_client_executed'] is False,'case original boundary')
        need(c['assessment']==evaluate_case(c),'assessment differs from real RGB and received input')
        for k in ('baseline_state','palette_state','before_sendinput','after_sendinput','final_state'):
            p=c[k];need(p['pointer_bytes']==4 and p['original_client_executed'] is False,'actual x86 control')
            need(p['mode']==c['mode'] and p['client_size']==[320,200],'window/mode provenance')
        need(c['baseline_state']['phase']==0 and c['palette_state']['phase']==1,'before/after palette state')
        need(c['final_state']['done'] is True and c['process_exit_before_cleanup']==0,'program finished before cleanup')
        if 'x11_input' in c:
            x=c['x11_input'];need(x['delta']==input_delta(x['before'],x['after']),'X11 reception differs from counters')
    eligible=any(c['mode']=='ddraw' and c['palette_state']['display_bpp']==8 and c['palette_state']['windows_acp']==950 and
        c['assessment']['color_gate_passed'] and c['assessment']['sendinput_gate_passed'] and
        c['assessment']['foreground_gate_passed'] for c in report['cases'])
    need(report['original_rerun_prerequisite_synthetic_8bit_passed']==eligible,'do not promote 32bit display or wrong ACP to original preflight')
    if report['environment'].startswith('wine32_'):
        n=report['network'];need(n['host_net_namespace']!=n['child_net_namespace'] and n['interfaces']==['lo'] and
            n['ipv4_routes']==[] and n['ipv6_default_routes']==[] and n['external_documentation_address_connect_errno'] in (101,113),'Wine process tree isolation')
        if 'wine_x11_configuration' in report:
            config=report['wine_x11_configuration'];restart=report['wine_restart_observation']
            need(config['PrivateColorMap']=='Y' and config['registry_write_and_readback_passed'] is True and
                 config['wineserver_restarted_before_control'] is True,'configuration provenance')
            need(restart['living_server_pids_after_wait']==[] and restart['server_absence_verified'] is True,'actual server retirement, not command status')
    else:
        need('CI host not network-isolated' in report['network_scope'],'native host isolation must not be invented')


def check():
    m=json.loads((RECOVERED/'STONEAGE-P3D-SYNTHETIC-CUSTODY-R1.json').read_text())
    for f in m['derived_files']:
        b=(RECOVERED/f['file']).read_bytes()
        need(len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],'raw source custody')
        need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['git_blob'],'raw Git blob')
        if f['file'].endswith('.json'):
            report=json.loads(b)
            if f.get('role')=='failed_private_restart':
                need(report['cases']==[] and report['probe_error']=='old Wine graphics processes not retired','retain initial restart guard failure')
                need(report['original_client_executed'] is False and report['original_client_downloaded'] is False,'failed synthetic scope')
            else:verify_report(report)
            expected=m['control_windows_crlf_source_sha256'] if report['environment'].startswith('native_windows') else m['control_source_sha256']
            need(report['control_source_sha256']==expected,'same source with explicitly preserved platform checkout line endings')
    need(m['original_client_executed'] is False and m['game_world_entered'] is False and m['overall_restoration_percent'] is None,'overall boundary')
    need(m['usable_original_8bit_environment_found'] is False,'no synthetic environment passed the complete prerequisites')
    print('P3D_SYNTHETIC_RGB_AND_RECEIVED_INPUT_REPLAY=PASS; ORIGINAL_RUNTIME_NOT_PROMOTED')


if __name__=='__main__':check()
