"""Replay bounded native-original login evidence without commercial source bytes."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
EXE_SHA="cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"

def require(ok,message):
    if not ok:raise ValueError(message)

def receiver(c):
    p=c['palette_state']
    require(c['mode']=='ddraw' and p['windows_acp']==950 and p['display_bpp']==8,'same receiver ACP950/8bpp')
    require(p['phase']==1 and p['getpixel_valid'] and p['red_getpixel']==[222,0,0] and p['green_getpixel']==[0,200,80],'actual receiver GetPixel')
    require(all(p['ddraw'][k]==0 for k in ('create','cooperative','primary','offscreen_8bit','palette','offscreen_attach','primary_attach','blt')),'native receiver DDraw path')
    require(any(f['synthetic_control_red_pixels']>=19000 and f['synthetic_control_green_pixels']>=19000 for f in c['palette_capture']['frames']),'independent screen RGB capture')
    require(all(p[k] for k in ('foreground_matches','active_matches','focus_matches')),'actual receiver foreground')
    sent=c['sendinput_command']
    require(sent['returncode']==0 and sent['report']['sendinput_down']==sent['report']['sendinput_up']==1,'successful synthetic dispatch')
    require(all(c['after_sendinput'][k]>c['before_sendinput'][k] for k in ('downs','ups','async_down_polls')),'received synthetic input')
    require(c['process_exit_before_cleanup']==0 and c['final_state']['done'] is True,'receiver natural exit')
    return True

def job(j):
    require(j['limit_flags']==0x2008 and j['active_process_limit']==1 and j['created_suspended'] is True and j['assigned_before_resume'] is True,'one-process kill-on-close job before resume')

def rule(r):
    require(r['action']=='Block' and r['direction']=='Outbound' and r['enabled']=='True' and r['profile']=='Any' and r['protocol']=='Any' and r['program']=='Any','whole guest temporary outbound policy')

def verify_report(r):
    require(r['schema']=='stoneage.p3h.original_windows_login.v1','actual report schema')
    for k in ('original_world_entered','original_server_contacted','private_original_data_published'):
        require(r[k] is False,'unsupported capability '+k)
    require(r['original_downloaded'] is True and r['original_client_executed'] is True,'original execution required, not synthetic only')
    require(r['runtime_inventory']==dict(files=375,bytes=372529095),'inventory qualified before transfer')
    c=r['carrier']
    require(c['bytes']==842125501 and c['md5']=='b37a4a47f4eb608cac67e4ddf7a1621a' and c['sha1']=='b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded' and c['all_ranges_strict_206'] is True,'authenticated whole carrier')
    e=r['extraction']
    require(e['files']==375 and e['bytes']==372529095 and e['all_member_sha256_match'] is True and e['original_installer_or_driver_executed'] is False,'full immutable runtime')
    p=r['preflight'];require(p['original_executed'] is False and p['unchanged_PE_pair'] is True,'unchanged synthetic sidecar pair')
    for key,cp in (('plain',1252),('external_manifest',950)):
        q=p[key]
        require(q['pointer_bytes']==4 and q['original_executed'] is False and q['acp_before']==q['acp_after_console950']==cp and q['display_bpp']==q['ddraw_current'][2]==8,'external manifest unchanged-image control')
    receiver(p['receiver']);job(p['job_smoke'])
    t=r['runtime'];job(t['job'])
    require(t['original_executable']==dict(bytes=425984,sha256=EXE_SHA) and t['original_executable_modified'] is False,'actual original EXE identity')
    for key in ('original_world_entered','account_or_password_entered','historical_server_contacted','original_GetACP_directly_measured'):
        require(t[key] is False,'original observation promotion '+key)
    require(t['original_client_execution_attempted'] is True,'actual native original attempt')
    require(t['original_launch_args']==['updated','realbin:1','adrnbin:1','sprbin:1','spradrnbin:1','soundbin:1','battlebin:1','windowmode','IP:0:127.0.0.1:9'],'no real server target')
    require(t['network_before']['connected'] is True and t['network_after_restore']['connected'] is True,'live canary on both sides')
    for key in ('network_blocked_before','network_blocked_after'):
        require(t[key]['connected'] is False and t[key]['wsa_error']==10013,'actual denial during original period')
    i=t['isolation'];require(i['watchdog']==dict(registered=True,user='SYSTEM'),'independent restore task')
    enabled=lambda p:p['Enabled'] is True or (type(p['Enabled']) is int and p['Enabled']==1)
    require({p['Name'] for p in i['profiles']}=={'Domain','Private','Public'} and len(i['profiles'])==3 and all(enabled(p) for p in i['profiles']),'all firewall profiles enabled (PowerShell serializes enum On as 1)')
    rule(i['rule']);rule(t['rule_after_original']);receiver(t['same_blocked_guest_synthetic_receiver'])
    require(t['job_closed_before_network_restore'] is True and t['isolation_cleanup']['remaining']==0,'end original tree before restored network')
    require(len(t['observations'])==3 and all(0<e['seconds_since_isolation']<110 for e in t['observations']),'bounded actual observations')
    original=[]
    for o in t['observations']:
        for w in o['windows']:
            require(w['pid']==t['pid'] and w['image']==t['actual_process_image'],'owned-window process identity')
            if w['klass']=='ＳｔｏｎｅＡｇｅ' and w['client_size']==[640,480]:original.append(o)
    require(t['original_visible_main_observed'] is bool(original),'window presence measured separately from pixels')
    require(any(o.get('frame',{}).get('nonuniform_pixels') is True for o in original),'nonuniform original owned-window capture')
    # Dispatch alone is not received QUIT; process must exit naturally before cleanup.
    q=t.get('quit_input',{})
    quit_observed=(q.get('client_point')==[350,380] and q.get('sendinput_down')==q.get('sendinput_up')==1 and t.get('exit_after_quit')==t['exit_before_cleanup']==0 and t.get('owned_windows_after_quit')==[])
    require(t['quit_exit_before_cleanup'] is bool(quit_observed),'QUIT cannot be credited to forced cleanup')
    require('runtime_error' not in r and 'error' not in r,'source-level runtime error remains explicit')
    return 'ORIGINAL_WINDOW_KNOWN_EXIT_POINT_RESPONSE' if quit_observed else 'ORIGINAL_WINDOW_EXIT_RESPONSE_OPEN'

def verify_visual(r,v):
    require(v['schema']=='stoneage.p3h.independent_visual_review.v1','independent visual review')
    for k in ('visible_game_picture_verified','original_palette_correct_verified','original_ANSI_GDI_text_qualified',
              'original_GetACP_directly_measured','original_input_event_counters_measured','credentials_entered',
              'authenticated_login','original_world_entered'):
        require(v[k] is False,'black/IME capture cannot be promoted: '+k)
    require(v['assistant_directly_viewed_frame_indices']==[0,1] and v['third_frame_identical_to_directly_viewed_first'] is True,'actual visual coverage')
    require(v['status']=='ORIGINAL_PROCESS_EXIT_COORDINATE_OBSERVED_VISUAL_DISPLAY_OPEN','bounded visual outcome')
    require(len(v['frames'])==3,'three independent frame counts')
    for i,(f,o,n) in enumerate(zip(v['frames'],r['runtime']['observations'],(97,104,97))):
        require(f['index']==i and f['png_sha256']==o['frame']['png_sha256'] and f['rgb_sha256']==o['frame']['rgb_sha256'],'source frame identity')
        require(f['nonblack_pixels']==n and f['black_pixels']+n==640*480 and f['colors']==2,'tiny IME/caret is not game artwork')
    require(v['frames'][0]['rgb_sha256']==v['frames'][2]['rgb_sha256'],'third frame duplicate coverage')
    return v['status']

def main():
    c=json.loads((ROOT/'research/recovered/STONEAGE-P3H-CUSTODY-R1.json').read_bytes())
    s=c['source'];b=(ROOT/s['path']).read_bytes();p=s['raw']
    require(s['run']==40636932361 and s['job']==122645935038 and s['artifact']==12793698659 and s['run_status']=='completed' and s['conclusion']=='success','actual finite native source run')
    require(len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==p['git_blob'],'byte-exact archived source/custody')
    for failed in c['failed_runs']:
        if 'path' not in failed:continue
        raw=(ROOT/failed['path']).read_bytes();f=failed['raw'];q=json.loads(raw)
        require(len(raw)==f['bytes'] and hashlib.sha256(raw).hexdigest()==f['sha256'] and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==f['git_blob'],'failed source must remain byte-exact')
        require(q['error']==failed['error'] and q['original_client_executed'] is False and q['original_downloaded'] is failed['original_downloaded'],'prior failure is not successful original execution')
    r=json.loads(b);v=json.loads((ROOT/'research/recovered/STONEAGE-P3H-VISUAL-REVIEW-R1.json').read_bytes())
    require(v['source_report_sha256']==hashlib.sha256(b).hexdigest(),'visual review pinned source')
    keep=c['private_retention']
    require(keep['bytes']==r['private_runtime_zip']['bytes'] and keep['sha256']==keep['full_persistent_readback_sha256']==r['private_runtime_zip']['sha256'],'private archive full readback receipt')
    require(keep['original_files']==375 and keep['immutable_original_runtime_bytes']==372529095 and keep['captured_frames']==3 and keep['all_375_original_members_independently_rehashed'] is True and keep['private_upload_succeeded'] is True,'private immutable runtime retention')
    require(keep['commercial_bytes_or_frames_committed_to_public_git'] is False and keep['private_key_published'] is False,'source-safe public metadata only')
    require(c['result']==verify_visual(r,v) and c['overall_completion_percent'] is None,'no project-wide completion promotion')
    print('P3H_ACTUAL_SOURCE_OFFLINE_ACCEPTANCE',verify_report(r),verify_visual(r,v),'ORIGINAL_WORLD_ENTERED=FALSE')

if __name__=='__main__':main()
