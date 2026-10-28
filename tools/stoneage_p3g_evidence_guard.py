"""Source-safe offline acceptance of actual P3G reports and immutable custody."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
FILES=('STONEAGE-P3G-WINDOWS2022-ACTUAL-R1.json','STONEAGE-P3G-WINDOWS2025-ACTUAL-R1.json')

def require(ok,message):
    if not ok:raise ValueError(message)

def verify_report(r):
    require(r['schema']=='stoneage.p3g.manifest_namespace_environment.v1','report schema')
    for k in ('original_client_downloaded','original_client_executed','original_world_entered',
              'original_process_isolation_qualified','original_server_contacted','usable_original_environment',
              'original_ANSI_GDI_text_qualified'):
        require(r[k] is False,'unsupported original claim '+k)
    expected={'wrong_namespace_zh_tw':('http://schemas.microsoft.com/SMI/2019/WindowsSettings','zh-TW',False),
              'correct_zh_tw':('urn:schemas-microsoft-com:asm.v3','zh-TW',True),
              'correct_utf8':('urn:schemas-microsoft-com:asm.v3','UTF-8',True)}
    require(set(r['embedded_manifest_readback'])==set(expected),'three embedded manifest readbacks')
    for k,values in expected.items():
        d=r['embedded_manifest_readback'][k]
        require((d['settings_namespace'],d['active_codepage'],d['correct_settings_namespace'])==values,'actual embedded namespace')
        require(len(d['sha256'])==64 and int(d['sha256'],16)>0,'embedded manifest digest')
    require([p['layer'] for p in r['cases']]==['DEFAULT','256COLOR'],'finite platform experiment')
    effect=True
    for pair in r['cases']:
        for k in ('plain','wrong_namespace_zh_tw','correct_zh_tw','correct_utf8'):
            d=pair[k]
            require(d['pointer_bytes']==4 and d['original_executed'] is False and
                    d['acp_before']==d['acp_after_console950'],'same receiving process ACP')
            require(d['display_bpp']==d['ddraw_current'][2] and d['ddraw_create']==0 and
                    d['ddraw_current_result']==0,'GDI/DDraw probe')
            require(d['cp950_installed'] is True and d['cp950_sample_fallback'] is False and
                    d['cp950_sample_bytes']==[165,219,190,185],'explicit CP950 converter test')
        effect=effect and pair['wrong_namespace_zh_tw']['acp_before']==pair['plain']['acp_before'] and pair['correct_zh_tw']['acp_before']==950 and pair['correct_utf8']['acp_before']==65001
    require(r['namespace_effect_observed'] is bool(effect),'namespace effect is measured, not inferred')
    candidates=[]
    for c in r['controls']:
        require(c['original_client_executed'] is False and c['process_exit_before_cleanup']==0 and c['final_state']['done'] is True,'actual clean synthetic receiver')
        p=c['palette_state'];known=p['getpixel_valid'] and p['red_getpixel']==[222,0,0] and p['green_getpixel']==[0,200,80]
        capture=any(f['synthetic_control_red_pixels']>=19000 and f['synthetic_control_green_pixels']>=19000 for f in c['palette_capture']['frames'])
        sent=c['sendinput_command']['returncode']==0 and c['sendinput_command']['report']['sendinput_down']==c['sendinput_command']['report']['sendinput_up']==1
        received=all(c['after_sendinput'][k]>c['before_sendinput'][k] for k in ('downs','ups','async_down_polls'))
        foreground=all(p[k] for k in ('foreground_matches','active_matches','focus_matches'))
        if c['mode']=='ddraw':
            render=p['phase']==1 and all(p['ddraw'][k]==0 for k in ('create','cooperative','primary','offscreen_8bit','palette','offscreen_attach','blt'))
            if p['display_bpp']==8:render=render and p['ddraw']['primary_attach']==0
        else:render=p['phase']==1 and p['palette_created']
        candidates.append(c['mode']=='ddraw' and p['windows_acp']==950 and p['display_bpp']==8 and known and capture and sent and received and foreground and render)
    possible=any(candidates)
    require(r['same_process_display_encoding_input_candidate'] is possible,'same-process candidate')
    require(r['status']==('SYNTHETIC_CANDIDATE_ORIGINAL_ISOLATION_OPEN' if possible else 'BLOCKED_NO_SAME_PROCESS_CANDIDATE'),'bounded status')
    for p,h in r['source_sha256'].items():
        b=(ROOT/p).read_bytes().replace(b'\r\n',b'\n')
        require(h in (hashlib.sha256(b).hexdigest(),hashlib.sha256(b.replace(b'\n',b'\r\n')).hexdigest()),'source exact LF/CRLF identity '+p)
    return possible

def main():
    custody=json.loads((ROOT/'research/recovered/STONEAGE-P3G-CUSTODY-R1.json').read_bytes())
    require([s['run'] for s in custody['source_runs']]==[40633664224,40633836213,40634200624], 'actual three source runs')
    for source in custody['source_runs']:
        b=(ROOT/source['path']).read_bytes();p=source['raw']
        require(source['run_status']=='completed' and source['conclusion']=='success' and
                len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256'] and
                hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==p['git_blob'],
                'immutable raw source/custody match')
    for name in FILES:
        p=ROOT/'research/recovered'/name;r=json.loads(p.read_bytes());print(name,verify_report(r),r['status'])
    verify_isolation(json.loads((ROOT/'research/recovered/STONEAGE-P3G-ISOLATION-ACTUAL-R1.json').read_bytes()))
    print('P3G_ACTUAL_SOURCE_OFFLINE_ACCEPTANCE=PASS; ORIGINAL_WORLD_ENTERED=FALSE')

def verify_isolation(r):
    from tools.stoneage_p3g_isolation import qualifies
    require(r['schema']=='stoneage.p3g.disposable_host_egress.v1','isolation source schema')
    for k in ('original_client_downloaded','original_client_executed','original_world_entered',
              'original_process_isolation_qualified','original_ANSI_GDI_text_qualified',
              'usable_original_environment','loopback_server_qualified','IPv6_and_UDP_empirically_tested'):
        require(r[k] is False,'unsupported original/network promotion '+k)
    require(r['source_sha256']=='26d17aa91561228d7bf48758b81eaa2079bfd9624154e82de88a8be080a3a426',
            'exact executed source Windows CRLF; later profile guard is additive')
    require(r['bounded_synthetic_egress_display_input_candidate'] is True and qualifies(r),'actual denial/RGB/input conditions')
    require(0<r['measured_block_window_seconds']<r['watchdog']['restore_delay_seconds']==120,'denial remained before watchdog deadline')
    require(r['empirical_network_scope']=='two_self_authored_program_paths_one_external_TCP_IPv4_destination', 'bounded empirical network scope')
    require(r['policy_scope']=='temporary_all_programs_all_protocols_all_remote_addresses_guest_rule','policy scope')
    return True

if __name__=='__main__':main()
