"""Independent FFmpeg float32 comparison of all actual private embedded WAVs.

No speaker output, assistant hearing, browser playback or game event asserted.
"""
import argparse
import base64
import hashlib
import json
import subprocess
from pathlib import Path


def replay(folder):
    import numpy as np
    root = Path(__file__).resolve().parents[1]; folder = folder.resolve()
    if folder == root or root in folder.parents:
        raise ValueError('private original audio outside Git only')
    html = (folder/'stoneage-tw10-audio-observer.html').read_bytes()
    r = json.loads((folder/'source-derived-report.json').read_bytes())
    rows = json.loads(html.split(b'<script id="evidence" type="application/json">')[1].split(b'</script>')[0])
    if len(rows) != 127 or [x['original_path'] for x in rows] != [x['original_path'] for x in r['files']]:
        raise ValueError('all original audio occurrences must survive HTML embedding')
    result = []
    for item, expected in zip(rows, r['files']):
        raw = base64.b64decode(item['dataURI'].split(',', 1)[1], validate=True)
        assert hashlib.sha256(raw).hexdigest() == expected['WAV_sha256'] and len(raw) == expected['bytes']
        assert {k:v for k,v in item.items() if k != 'dataURI'} == expected
        run = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'pipe:0', '-f', 'f32le',
                              '-acodec', 'pcm_f32le', 'pipe:1'], input=raw, capture_output=True, timeout=30)
        assert run.returncode == 0, expected['original_path']
        floats = np.frombuffer(run.stdout, dtype='<f4').reshape((-1, expected['channels']))
        assert len(floats) == expected['frames']
        hashes = [hashlib.sha256(floats[:, c].copy().tobytes()).hexdigest() for c in range(expected['channels'])]
        assert hashes == expected['reference_float32_channel_sha256'], expected['original_path']
        result.append(dict(original_path=expected['original_path'], frames=len(floats), float32_channel_sha256=hashes))
    out = dict(schema='stoneage.scene20.actual_private_FFmpeg_audio_replay.r1',
               source_report_sha256=hashlib.sha256((folder/'source-derived-report.json').read_bytes()).hexdigest(),
               private_HTML_sha256=hashlib.sha256(html).hexdigest(), actual_original_WAVs_verified=127,
               original_WAV_bytes=38009578, files=result,
               actual_browser_original_audio_verified=False, assistant_heard_audio=False,
               original_world_entered=False)
    (folder/'independent-ffmpeg-replay.json').write_text(json.dumps(out, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    return out


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--private-dir',type=Path,required=True);a=p.parse_args()
    print(json.dumps({k:v for k,v in replay(a.private_dir).items() if k!='files'},sort_keys=True))
