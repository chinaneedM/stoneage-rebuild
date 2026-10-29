"""Private original-TW1 loose-WAV listening archive; public replay uses metadata.

127 existing loose files, not 127 newly discovered sounds or identified events.
Exact files, including metadata chunks and duplicate occurrences, are preserved.
"""
import argparse
import base64
import hashlib
import io
import json
import struct
import wave
import zipfile
from pathlib import Path

from tools.stoneage_original_observation_lab import pinned_wav_inventory
from tools.stoneage_tw10_audio_metadata import parse_wave

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'research/recovered/STONEAGE-SCENE20-TW10-AUDIO-MATERIAL-R1.json'
PACKAGE_SHA = '3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24'
SCOPE = 'TW10_ORIGINAL_LOOSE_WAV_PRIVATE_OFFLINE_OBSERVER_NOT_GAME_EVENT_TRACE'
FALSE = ('original_client_executed', 'original_world_entered',
         'original_game_audio_event_verified', 'assistant_heard_audio',
         'copyrighted_audio_in_public_git', 'historical_loop_selection_verified')


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def loose_inventory():
    # The older inventory helper also retains the BIN container/address TXT.
    # Only authenticated independent WAV paths enter this listening surface.
    return {p:v for p,v in pinned_wav_inventory().items()
            if p.endswith('.wav') and ('/se/' in p or '/bgm/' in p)}


def prior_formats():
    """Read the old full source crosswalk, including same-name PCM variants."""
    raw = (ROOT/'research/recovered/STONEAGE-TW10-AUDIO-DATASET-R1.txt').read_bytes()
    need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() ==
         '094becbc92397ee8abf72a014deffffabc97a316', 'pinned prior audio format crosswalk')
    out = {}
    for line in raw.decode().splitlines():
        kind = line.split('|')[0]
        if kind not in ('INDEXED', 'BGM', 'UNINDEXED_SFX'):
            continue
        v = dict(s.split('=', 1) for s in line.split('|')[1:])
        prefix = 'loose_' if kind == 'INDEXED' else 'wave_'
        path = v['loose_path'] if kind == 'INDEXED' else v['path']
        need(path not in out, 'prior loose occurrence duplicate')
        out[path] = dict(channels=int(v[prefix+'channels']), sample_rate=int(v[prefix+'sample_rate']),
                         sample_width_bytes=int(v[prefix+'bits_per_sample'])//8,
                         data_bytes=int(v[prefix+'data_size']), PCM_sha256=v[prefix+'data_sha256'],
                         chunk_signature=v[prefix+'chunk_signature'])
    need(len(out) == 127, 'all original loose format records')
    return out


def inspect(raw, path, expected):
    need(path in expected and (len(raw), sha(raw)) == expected[path], 'original full WAV SHA/length')
    m = parse_wave(raw)
    need(m['riff'] == m['wave'] == 1 and m['audio_format'] == 1, 'original PCM WAV only')
    with wave.open(io.BytesIO(raw), 'rb') as f:
        channels, rate, width, frames = f.getnchannels(), f.getframerate(), f.getsampwidth(), f.getnframes()
        pcm = f.readframes(frames)
        need(f.getcomptype() == 'NONE' and width in (1, 2) and channels in (1, 2), 'bounded original PCM format')
    need((channels, rate, width*8, len(pcm), sha(pcm)) ==
         (m['channels'], m['sample_rate'], m['bits_per_sample'], m['data_size'], m['data_sha256']), 'independent wave vs RIFF chunk parser')
    # Exact PCM -> float32 reference, preserving original sample rate/channels.
    # Powers-of-two scaling is exact for both original 8- and 16-bit samples.
    floats = []
    for channel in range(channels):
        b = bytearray(frames*4)
        for i in range(frames):
            at = (i*channels + channel)*width
            value = (pcm[at]-128)/128 if width == 1 else struct.unpack_from('<h', pcm, at)[0]/32768
            struct.pack_into('<f', b, i*4, value)
        floats.append(sha(b))
    return dict(original_path=path, filename=Path(path).name,
                category='BGM_DIRECTORY' if '/bgm/' in path else 'SFX_DIRECTORY',
                bytes=len(raw), WAV_sha256=sha(raw), PCM_sha256=sha(pcm),
                channels=channels, sample_rate=rate, sample_width_bytes=width,
                frames=frames, duration_seconds=frames/rate,
                chunk_signature=m['chunk_signature'],
                expected_browser_float32_channel_sha256=floats,
                in_game_event=None, original_loop_points_applied=False)


def validate(r):
    expected = loose_inventory(); formats = prior_formats()
    need(r['schema'] == 'stoneage.scene20.original_TW10_audio_material.r1' and r['scope'] == SCOPE, 'scope')
    need(r['source_private_package_sha256'] == PACKAGE_SHA, 'preserved private source package')
    need(all(r[k] is False for k in FALSE) and r['overall_completion_percent'] is None and
         r['source_CI_run_id'] is None, 'historical evidence limits')
    rows = r['files']
    need(len(rows) == r['loose_WAV_count'] == len(expected) == 127 and
         {v['original_path'] for v in rows} == set(expected), 'all 127 exact loose occurrences')
    need(sum(v['bytes'] for v in rows) == r['original_WAV_bytes'] == 38009578, 'conserved original bytes')
    need(sum(v['category'] == 'BGM_DIRECTORY' for v in rows) == 11 and
         sum(v['category'] == 'SFX_DIRECTORY' for v in rows) == 116, 'original directory categories')
    for v in rows:
        need((v['bytes'], v['WAV_sha256']) == expected[v['original_path']], 'original WAV occurrence identity')
        need(v['filename'] == Path(v['original_path']).name and v['in_game_event'] is None and
             v['original_loop_points_applied'] is False, 'no semantic renaming or historical loop adoption')
        need(v['channels'] in (1, 2) and v['sample_width_bytes'] in (1, 2) and v['sample_rate'] > 0 and
             v['frames'] > 0 and v['duration_seconds'] == v['frames']/v['sample_rate'] and
             len(v['expected_browser_float32_channel_sha256']) == v['channels'], 'original format/frame bounds')
        need(all(len(h) == 64 and set(h) <= set('0123456789abcdef') for h in
                 [v['PCM_sha256'], *v['expected_browser_float32_channel_sha256']]), 'derived PCM/channel hashes')
        old = formats[v['original_path']]
        need(all(v[k] == old[k] for k in ('channels', 'sample_rate', 'sample_width_bytes', 'PCM_sha256', 'chunk_signature')) and
             v['frames']*v['channels']*v['sample_width_bytes'] == old['data_bytes'], 'original prior PCM/format crosswalk')
    return dict(loose_files=127, BGM_files=11, SFX_files=116, WAV_bytes=38009578,
                original_event_bindings=0, original_world_entered=False)


def export(package, destination):
    destination = destination.expanduser().resolve()
    need(destination != ROOT and ROOT not in destination.parents and not destination.exists(), 'new private directory outside Git')
    with package.open('rb') as f:
        need(hashlib.file_digest(f, 'sha256').hexdigest() == PACKAGE_SHA, 'whole preserved original package SHA')
    expected = loose_inventory(); rows = []; private = []
    with zipfile.ZipFile(package) as z:
        for path in sorted(expected):
            member = 'source/' + path.removeprefix('StoneAge/')
            need(z.namelist().count(member) == 1, 'one exact original source member')
            raw = z.read(member); row = inspect(raw, path, expected); rows.append(row)
            private.append(dict(**row, dataURI='data:audio/wav;base64,'+base64.b64encode(raw).decode()))
    report = dict(schema='stoneage.scene20.original_TW10_audio_material.r1', scope=SCOPE,
                  source_private_package_sha256=PACKAGE_SHA, loose_WAV_count=len(rows),
                  original_WAV_bytes=sum(v['bytes'] for v in rows), files=rows,
                  source_CI_run_id=None, **{k:False for k in FALSE}, overall_completion_percent=None)
    validate(report)
    template = (ROOT/'tools/stoneage_scene20_audio_observer.html').read_text()
    html = template.replace('__PRIVATE_AUDIO_JSON__', json.dumps(private, separators=(',', ':')))
    need('__PRIVATE_AUDIO_JSON__' not in html, 'private audio embedded once')
    destination.mkdir(mode=0o700)
    (destination/'stoneage-tw10-audio-observer.html').write_text(html)
    (destination/'source-derived-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)+'\n')
    return report


def validate_replay(a, r):
    need(a['schema'] == 'stoneage.scene20.actual_private_FFmpeg_audio_replay.r1' and
         a['source_report_sha256'] == sha(REPORT.read_bytes()), 'actual private replay/source metadata identity')
    need(a['actual_original_WAVs_verified'] == 127 and a['original_WAV_bytes'] == 38009578 and
         a['actual_browser_original_audio_verified'] is False and a['assistant_heard_audio'] is False and
         a['original_world_entered'] is False, 'FFmpeg does not certify browser/speaker/game execution')
    need(len(a['files']) == 127, 'complete independent original replay')
    for x, v in zip(a['files'], r['files']):
        need(x == dict(original_path=v['original_path'], frames=v['frames'],
                       float32_channel_sha256=v['expected_browser_float32_channel_sha256']), 'independent FFmpeg full-channel samples')
    return {'actual_original_WAVs_independently_decoded':127, 'browser_original_audio_verified':False}


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--package', type=Path); p.add_argument('--private-output', type=Path)
    a = p.parse_args()
    if a.package or a.private_output:
        need(a.package and a.private_output, 'both private source and output required'); r = export(a.package, a.private_output)
    else:
        r = json.loads(REPORT.read_bytes())
    result=validate(r)
    if not a.package:
        result.update(validate_replay(json.loads((REPORT.parent/'STONEAGE-SCENE20-LOCAL-FFMPEG-ACCEPTANCE-R1.json').read_bytes()),r))
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
