"""127 small SYNTHETIC audio fixtures for public browser QA, no original WAVs."""
import argparse
import base64
import hashlib
import io
import json
import struct
import wave
from pathlib import Path


def fixtures():
    rows=[]
    for i in range(127):
        channels, width = [(1,1),(2,1),(1,2),(2,2)][i%4];rate=11025 if i%2 else 22050;frames=rate//2
        values=[(n*13+i*17)%256 if width==1 else ((n*389+i*313)%65536)-32768 for n in range(frames*channels)]
        pcm=bytes(values) if width==1 else struct.pack('<'+'h'*len(values),*values)
        b=io.BytesIO()
        with wave.open(b,'wb') as w:w.setnchannels(channels);w.setsampwidth(width);w.setframerate(rate);w.writeframes(pcm)
        raw=b.getvalue();hashes=[]
        for c in range(channels):
            floats=struct.pack('<'+'f'*frames,*[((values[n*channels+c]-128)/128 if width==1 else values[n*channels+c]/32768) for n in range(frames)])
            hashes.append(hashlib.sha256(floats).hexdigest())
        name=f'fixture_{i:03}.wav';cat='BGM_DIRECTORY' if i<11 else 'SFX_DIRECTORY'
        rows.append(dict(original_path='SYNTHETIC_NOT_ORIGINAL/'+('bgm/' if i<11 else 'se/')+name,filename=name,
                         category=cat,bytes=len(raw),WAV_sha256=hashlib.sha256(raw).hexdigest(),PCM_sha256=hashlib.sha256(pcm).hexdigest(),
                         frames=frames,channels=channels,sample_width_bytes=width,sample_rate=rate,duration_seconds=frames/rate,
                         chunk_signature='SYNTHETIC_PCM',reference_float32_channel_sha256=hashes,
                         dataURI='data:audio/wav;base64,'+base64.b64encode(raw).decode()))
    return rows


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    template=(Path(__file__).with_name('stoneage_scene20_audio_observer.html')).read_text(encoding='utf-8')
    html=template.replace('__PRIVATE_AUDIO_JSON__',json.dumps(fixtures(),separators=(',',':')))
    html=html.replace('<h1>','<h1>合成CI测试｜',1).replace('<p class="notice">','<p class="notice">本页全部声音为程序生成的合成测试，不含历史原WAV。',1)
    a.output.write_text(html, encoding='utf-8')
