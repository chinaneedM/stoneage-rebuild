"""Independent acceptance of archived P3 reports; never launches the client."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECOVERED = ROOT / 'research/recovered'
MANIFEST = RECOVERED / 'STONEAGE-TW10-ORIGINAL-BOOT-P3-CUSTODY-R1.json'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def boundaries(report):
    need(report['schema'] == 'stoneage.p3.isolated_boot_observation.v1', 'schema')
    need(report['sample'] == 'TW_WAEI_JSS_1_0_ACCEPTED_RETAIL_REDUMP_104630', 'sample')
    n = report['network']
    need(n['host_net_namespace'] != n['child_net_namespace'], 'namespace identity')
    need(n['interfaces'] == ['lo'] and n['ipv4_routes'] == [] and n['ipv6_default_routes'] == [], 'network routes')
    need(n['external_documentation_address_connect_errno'] in (101, 113) and n['outbound_namespace_isolation_verified'] is True, 'negative connect')
    for key in ('game_world_entered', 'authentic_game_display_visually_verified',
                'assistant_viewed_original', 'original_assets_published', 'audio_heard_or_recorded'):
        need(report[key] is False, 'automated report overclaim: ' + key)
    need(report['environment']['winearch'] == 'win32', '32-bit compatibility')
    need(report['environment']['old_kernel_drivers_installed'] is False, 'driver boundary')


def synthetic(report, depth=None):
    boundaries(report)
    need(report['preflight_passed'] is True, 'preflight failed')
    need(report['original_client_execution_attempted'] is False and report['original_client_execution_proven'] is False, 'synthetic is not original')
    s = report['synthetic_control']
    need(s['pointer_bytes'] == 4 and s['windows_acp'] == 950 and s['window_created'] is True, 'Win32/CP950')
    for k in ('directdraw_create', 'cooperative', 'surface_8bit_create', 'palette_create', 'palette_attach'):
        need(s[k] == 0, 'DirectDraw failure: ' + k)
    if depth is not None:
        need(s['get_display_mode'] == 0 and s['current_display_bpp'] == depth, 'actual display depth')
    need(report['capture']['nonuniform_pixels'] is True, 'capture')


def native(report, *, modal):
    boundaries(report)
    exe = report['source_executable']
    need(exe == {'path': 'StoneAge/sa_3.exe', 'bytes': 425984,
                 'sha256': 'cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a'}, 'original executable identity')
    expected = ['updated', 'realbin:1', 'adrnbin:1', 'sprbin:1', 'spradrnbin:1',
                'soundbin:1', 'battlebin:1', 'windowmode', 'IP:0:127.0.0.1:9']
    need(report['original_launch_args'] == expected, 'source-backed flags and isolated endpoint')
    need(report['endpoint_is_synthetic_isolated_loopback_not_historical_server'] is True, 'endpoint provenance')
    need(report['original_client_execution_attempted'] is True and report['original_client_execution_proven'] is True, 'original execution')
    need(report['original_input_baseline_unchanged'] is True and report['runtime_copy_changed_paths'] == [], 'input custody')
    observations = report['observations']
    need(len(observations) == 3, 'three observations, not three clients')
    for obs in observations:
        windows = obs['windows']['windows']
        owned = [w for w in windows if w.get('image_path', '').replace('\\', '/').lower().endswith('/sa_3.exe')]
        need(owned and any(w['class'] == 'ＳｔｏｎｅＡｇｅ' for w in owned), 'original-owned main window')
        dialogs = [w for w in owned if w['class'] == '#32770']
        texts = [c.get('text', c.get('title', '')) for w in dialogs for c in w.get('children', [])]
        if modal:
            need(dialogs and any('２５６' in t for t in texts), 'retain actual 256-color error')
        else:
            need(not dialogs, '8-bit attempt still has startup dialog')
        c = obs['capture']
        need(c and (c['width'], c['height']) == (800, 600) and c['nonuniform_pixels'] is True, 'native capture metadata')
        need(c['assistant_viewed_original'] is False and c['image_published'] is False, 'capture overclaim')


def check():
    manifest = json.loads(MANIFEST.read_text())
    reports = {}
    for entry in manifest['derived_files']:
        raw = (RECOVERED / entry['file']).read_bytes()
        need(len(raw) == entry['bytes'] and hashlib.sha256(raw).hexdigest() == entry['sha256'], 'raw custody: ' + entry['file'])
        need(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == entry['git_blob'], 'Git blob custody')
        if entry['file'].endswith('.json'):
            reports[entry['role']] = json.loads(raw)
    synthetic(reports['depth24_preflight'])
    native(reports['depth24_original'], modal=True)
    synthetic(reports['depth8_preflight'], 32)
    synthetic(reports['depth8_display'], 8)
    native(reports['depth8_original'], modal=False)
    synthetic(reports['private_preflight'], 32)
    synthetic(reports['private_display'], 8)
    native(reports['private_original'], modal=False)
    sealed = reports['private_original']['sealed_private_frame']
    need(sealed['plaintext_sha256'] == manifest['private_visual_observation']['png_sha256'], 'private frame identity')
    need(sealed['plaintext_sha256'] == reports['private_original']['observations'][1]['capture']['png_sha256'], 'frame position')
    need(manifest['game_world_entered'] is False and manifest['overall_restoration_percent'] is None, 'overall boundary')
    print('P3_ARCHIVED_SOURCE_CUSTODY_AND_EXECUTION_BOUNDARIES=PASS; NOT_WORLD_ACCEPTANCE')


if __name__ == '__main__':
    check()
