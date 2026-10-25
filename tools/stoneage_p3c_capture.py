"""Finite X11 colormap comparison; all image bytes remain private."""
import hashlib
import json
from pathlib import Path
import subprocess

from tools.stoneage_p3_boot import ROOT, frame, require
from tools.stoneage_p3_private_frame import seal


def capture(helper, directory, env, *, selftest=False, seal_dir=None):
    directory=directory.resolve()
    require(directory!=ROOT and ROOT not in directory.parents and not directory.exists(), 'new private capture directory required')
    directory.mkdir()
    args=[str(helper),str(directory)]+(['--selftest'] if selftest else [])
    p=subprocess.run(args,env=env,text=True,capture_output=True,timeout=20,check=True)
    result=json.loads(p.stdout)
    require(result['x_errors']==0 and result['windows'], 'no valid indexed windows')
    for w in result['windows']:
        stem=directory/('window-'+str(w['window']))
        for mode in ('map','rootmap'):
            from PIL import Image
            png=Path(str(stem)+'-'+mode+'.png')
            with Image.open(str(stem)+'-'+mode+'.ppm') as im: im.save(png)
            w[mode]=frame(png)
        for suffix in ('indices','palette'):
            raw=Path(str(stem)+'-'+suffix+'.bin').read_bytes()
            w[suffix+'_sha256']=hashlib.sha256(raw).hexdigest()
        w['same_indices_different_colormap_rgb']=w['map']['rgb_sha256']!=w['rootmap']['rgb_sha256']
        if seal_dir is not None:
            public=ROOT/'research/recovered/STONEAGE-P3C-SESSION-TRANSPORT-PUBLIC.pem'
            raw=Path(str(stem)+'-map.png').read_bytes();envelope=seal(raw,public.read_bytes())
            dest=seal_dir/('frame-'+directory.name+'-'+str(w['window'])+'-sealed.json')
            require(not dest.exists(), 'sealed frame refuses overwrite')
            dest.write_text(json.dumps(envelope,sort_keys=True))
            w['sealed_private_frame']={k:envelope[k] for k in ('schema','plaintext_sha256','plaintext_bytes','recipient_key_sha256')}
            w['sealed_private_frame']['ciphertext_envelope_sha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
            w['sealed_private_frame']['file']=dest.name
    if selftest:
        require(len(result['windows'])==1, 'synthetic capture census')
        w=result['windows'][0]
        require(w['map']['synthetic_control_red_pixels']==25600 and w['map']['synthetic_control_green_pixels']==25600,
                'own-colormap capture did not preserve known RGB')
        require(w['same_indices_different_colormap_rgb'], 'root-colormap negative control did not differ')
        result['synthetic_known_rgb_passed']=True
        result['original_client_executed']=False
    return result
