"""Independent P3C color/QUIT evidence acceptance, without game execution."""
import hashlib
import json
from pathlib import Path
from tools.stoneage_p3_evidence_guard import boundaries, need, synthetic

ROOT=Path(__file__).resolve().parents[1]
RECOVERED=ROOT/'research/recovered'


def calibration(report):
    synthetic(report,8)
    control=report['x11_known_rgb_control']
    need(control['synthetic_known_rgb_passed'] is True and control['original_client_executed'] is False,'synthetic provenance')
    need(control['x_errors']==0 and len(control['windows'])==1,'X11 known window')
    w=control['windows'][0]
    need(w['depth']==8 and w['visual_class']==3 and w['colormap']!=w['default_colormap'],'private indexed visual')
    need(w['map']['synthetic_control_red_pixels']==25600 and w['map']['synthetic_control_green_pixels']==25600,'known RGB calibration')
    need(w['same_indices_different_colormap_rgb'] is True and w['map']['rgb_sha256']!=w['rootmap']['rgb_sha256'],'wrong-colormap negative control')
    actual=any(w['map']['synthetic_control_red_pixels']>1000 and w['map']['synthetic_control_green_pixels']>1000
               for w in report['wine_window_colormaps']['windows'])
    need(report['wine_known_rgb_preserved']==actual,'Wine color claim differs from pixels')


def fullscreen_failure(report):
    boundaries(report)
    need(report['original_client_execution_proven'] is True and report['original_input_baseline_unchanged'] is True,'original custody/execution')
    need(report['source_executable']=={'path':'StoneAge/sa_3.exe','bytes':425984,
        'sha256':'cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a'},'original executable')
    need(report['original_launch_args']==['updated','realbin:1','adrnbin:1','sprbin:1','spradrnbin:1','soundbin:1','battlebin:1','IP:0:127.0.0.1:9'],'original fullscreen flags and isolated endpoint')
    before=report['original_window_colormaps']
    need(before['x_errors']==0 and before['windows'],'original X11 captures')
    for w in before['windows']:
        need(w['depth']==8 and w['visual_class']==3,'indexed visual')
        need(w['sealed_private_frame']['plaintext_sha256']==w['map']['png_sha256'],'sealed native frame identity')
        need(w['map']['image_published'] is False and w['map']['assistant_viewed_original'] is False,'automated screenshot boundary')
    i=report['input_observation']
    need(i['operation']=='one_held_left_click_at_previous_authenticated_QUIT_label' and i['screen_xy']==[350,380],'finite input scope')
    need(i['fullscreen_original_path'] is True and 'windowmode' not in report['original_launch_args'],'original default fullscreen branch')
    need(report['environment']['display']=='640x480x8_XVFB','fullscreen geometry')
    need(i['hold_milliseconds']==200 and i['mousedown_returncode']==0 and i['mouseup_returncode']==0,'held input dispatch')
    need(report['focus_observation']['returncode']==0,'focus dispatch')
    need(i['account_or_password_entered'] is False and i['server_started_or_login_attempted'] is False,'no account/server experiment')
    need(i['mousemove_returncode']==0 and i['click_returncode']==0,'actual input dispatch')
    owned=[w for w in i['windows_after']['windows'] if w.get('image_path','').replace('\\','/').lower().endswith('/sa_3.exe')]
    need(len(owned)==i['original_owned_windows_remaining'],'post-input ownership')
    exit_observed=i['launcher_returncode_after']==0 and not owned
    need(i['exit_observed_before_cleanup']==exit_observed,'cleanup is not user exit')
    need(i['exit_observed_before_cleanup'] is False,'fullscreen crash is not QUIT success')
    for o in report['observations']:
        need(any(w.get('image_path','').replace('\\','/').lower().endswith('/winedbg.exe')
                 for w in o['windows']['windows']),'retain pre-input crash debugger')
    need(any('Unhandled page fault' in line for line in report['wine_diagnostic_lines']),'retain original Wine fault')


def check():
    m=json.loads((RECOVERED/'STONEAGE-TW10-ORIGINAL-LOGIN-P3C-CUSTODY-R1.json').read_text())
    reports={}
    for f in m['derived_files']:
        raw=(RECOVERED/f['file']).read_bytes()
        need(len(raw)==f['bytes'] and hashlib.sha256(raw).hexdigest()==f['sha256'],'raw report custody')
        need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==f['git_blob'],'Git blob identity')
        if f['file'].endswith('.json'):reports[f['role']]=json.loads(raw)
    synthetic(reports['preflight'])
    calibration(reports['display'])
    fullscreen_failure(reports['original'])
    for prefix in ('initial_','focused_'):
        calibration(reports[prefix+'display'])
        r=reports[prefix+'original'];boundaries(r)
        need(r['input_observation']['exit_observed_before_cleanup'] is False and
             r['input_observation']['original_owned_windows_remaining']==1,'retain unsuccessful windowed QUIT history')
        need(r['original_window_colormaps']['windows'][0]['map_installed'] is False,'retain uninstalled windowed colormap evidence')
    seen=m['private_visual_observation']
    need(any(w['sealed_private_frame']['plaintext_sha256']==seen['png_sha256'] for w in reports['focused_original']['original_window_colormaps']['windows']),'manual view source bridge')
    need(seen['correct_color_rendering_verified'] is False and m['quit_click_accepted'] is False,'retain unresolved color and click')
    need(m['game_world_entered'] is False and m['overall_restoration_percent'] is None,'overall boundary')
    print('P3C_ARCHIVED_SOURCE_AND_NEGATIVE_BOUNDARIES=PASS; COLOR_AND_QUIT_REMAIN_OPEN')


if __name__=='__main__':check()
