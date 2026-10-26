"""Recompute P3E prerequisites without promoting compatibility flags to evidence."""
import hashlib
import json
from pathlib import Path
from tools.stoneage_p3d_evidence_guard import need, verify_report as verify_p3d
from tools.stoneage_p3e_windows import LAYERS, evaluate_network, qualify

ROOT=Path(__file__).resolve().parents[1]
RECOVERED=ROOT/'research/recovered'

def verify_report(r):
    need(r['schema']=='stoneage.p3e.available_windows.v1','P3E schema')
    for k in ('original_downloaded','original_executed','world_entered','original_process_isolation_qualified','usable_original_environment'):
        need(r[k] is False,'original runtime/isolation must remain unqualified: '+k)
    need('probe_error' not in r,'incomplete source measurement')
    need([c['requested_layer'] for c in r['cases']]==list(LAYERS),'finite compatibility matrix')
    for entry in r['cases']:
        e=entry['environment'];need(e['pointer_bytes']==4 and e['original_executed'] is False,'own x86 inspector')
        need(e['desktop_mode_changed'] is False,'CDS_TEST is not a desktop mode change')
        need(e['cp950_installed'] is True and e['cp950_sample_bytes']==list('石器'.encode('cp950')) and
            e['cp950_sample_fallback'] is False,'CP950 converter availability, not ACP qualification')
        eligible=qualify(entry['controls'])
        need(entry['simultaneous_synthetic_prerequisites']==eligible,'all prerequisites must hold in one actual process')
        verify_p3d({'schema':'stoneage.p3d.synthetic_environment_gate.v1',
            'original_client_downloaded':False,'original_client_executed':False,'original_game_world_entered':False,
            'cases':entry['controls'],'original_rerun_prerequisite_synthetic_8bit_passed':eligible,
            'environment':'native_windows_p3e_synthetic_only','network_scope':'CI host not network-isolated; exact-path canary is separately bounded'})
    candidate=any(c['simultaneous_synthetic_prerequisites'] for c in r['cases'])
    need(r['display_encoding_input_candidate_found']==candidate,'candidate status')
    expected='SYNTHETIC_CANDIDATE_REQUIRES_ORIGINAL_PATH_ISOLATION' if candidate else 'BLOCKED_AVAILABLE_WINDOWS_ENVIRONMENT'
    need(r['status']==expected,'bounded environment verdict')
    n=r['network']
    need(n['scope']=='synthetic_exact_program_path_tcp_ipv4_one_destination_only' and
        n['original_process_isolation_qualified'] is False,'do not generalize one path/TCP endpoint to original descendants or UDP/IPv6')
    need(n['assessment']==evaluate_network(n),'firewall status needs before/block/control/after observations')
    need(r['system_locale']['restart_performed'] is False and r['system_locale']['locale_changed'] is False,'no unobserved locale/reboot claim')

def check():
    m=json.loads((RECOVERED/'STONEAGE-P3E-WINDOWS-CUSTODY-R1.json').read_bytes())
    f=m['derived_file'];b=(RECOVERED/f['path']).read_bytes()
    need(len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],'raw report digest')
    need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['git_blob'],'raw Git blob')
    r=json.loads(b);verify_report(r)
    for p,d in r['source_sha256'].items():
        source=(ROOT/p).read_bytes().replace(b'\r\n',b'\n')
        need(hashlib.sha256(source.replace(b'\n',b'\r\n')).hexdigest()==d,'exact native checkout source digest')
    need(m['original_executed'] is False and m['overall_restoration_percent'] is None,'global boundary')
    print('P3E_AVAILABLE_WINDOWS_QUALIFICATION_REPLAY=PASS; ORIGINAL_ENVIRONMENT_NOT_PROMOTED')

if __name__=='__main__':check()
