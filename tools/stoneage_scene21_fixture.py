"""Synthetic eight-frame UI fixture; never embeds original game pixels."""
import argparse,base64,copy,hashlib,io,json
from pathlib import Path
from PIL import Image
from tools.stoneage_scene21_town1000 import REPORT

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 r=json.loads(REPORT.read_bytes());frames={}
 for i,name in enumerate(r['frames']):
  im=Image.new('RGBA',tuple(r['canvas_size']),((i*37+11)%256,(i*61+20)%256,(i*23+90)%256,255));b=io.BytesIO();im.save(b,format='PNG');raw=b.getvalue();r['frames'][name]['RGBA_sha256']=hashlib.sha256(im.tobytes()).hexdigest();r['frames'][name]['PNG_sha256']=hashlib.sha256(raw).hexdigest();frames[name]=base64.b64encode(raw).decode()
 model={'synthetic_fixture':True,'report':r,'frames':frames}
 template=Path(__file__).with_name('stoneage_scene21_observer.html').read_text(encoding='utf-8')
 html=template.replace('__PRIVATE_SCENE_JSON__',json.dumps(model,separators=(',',':'))).replace('<h1>','<h1>合成UI测试｜',1).replace('<p class="note">','<p class="note"><b>此测试页面全部图像均为程序合成色块，无原游戏像素。</b>',1)
 a.output.write_text(html,encoding='utf-8')
