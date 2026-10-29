"""Independent private RD/color/placement replay, no original process/browser."""
import argparse,base64,hashlib,io,json,struct,zipfile
from pathlib import Path
from PIL import Image
from tools.stoneage_scene14_independent_replay import decode

def sha(b):return hashlib.sha256(b).hexdigest()
def replay(folder):
 root=Path(__file__).resolve().parents[1];folder=folder.resolve();assert folder!=root and root not in folder.parents
 r=json.loads((folder/'source-derived-report.json').read_bytes());model=json.loads((folder/'StoneAge-SCENE23-body-observer.html').read_bytes().split(b'<script id="evidence" type="application/json">')[1].split(b'</script>')[0]);assert model['report']==r
 ims={};result=[];count=0
 with zipfile.ZipFile(folder/'private-first-frame-RD.zip')as z:
  assert len(z.namelist())==96
  for palette in ('0','1'):
   sap=(folder/('Palet_'+palette+'.sap')).read_bytes();assert sha(sap)==r['source_files']['Palet_'+palette+'.sap']['sha256'];rgb={n+16:tuple(sap[n*3:n*3+3][::-1])for n in range(224)};rgb[0]=(0,0,0);rgb[168]=(0,0,0)
   for b in r['bitmaps']:
    rd=z.read(str(b['bitmapno'])+'.rd');assert sha(rd)==b['RD_sha256'];w,h,indices=decode(rd);assert (w,h)==(b['width'],b['height']) and sha(indices)==b['indices_sha256'];assert all(n in rgb for n in indices),'reserved nonzero palette index needs separate source rule'
    rgba=bytes(c for y in range(h-1,-1,-1)for n in indices[y*w:(y+1)*w]for c in (*rgb[n],0 if n==0 else 255));expected=b['palette_candidates'][palette];assert sha(rgba)==expected['RGBA_sha256'];png=base64.b64decode(model['images'][palette][str(b['bitmapno'])]);assert sha(png)==expected['PNG_sha256'];im=Image.open(io.BytesIO(png)).convert('RGBA');assert im.tobytes()==rgba;ims[(palette,b['bitmapno'])]=im;count+=1
  rows={b['bitmapno']:b for b in r['bitmaps']}
  for palette in ('0','1'):
   for g in r['groups']:
    for a in g['directions']:
     n,x,y,sound=a['first_frame'];b=rows[n];im=ims[(palette,n)];c=Image.new('RGBA',(240,260),(20,33,41,255));c.alpha_composite(im.resize((b['width']*2,b['height']*2),Image.Resampling.NEAREST),(120+2*(x+b['xoff']),200+2*(y+b['yoff'])));digest=sha(c.tobytes());old=next(v for v in model['canvas_hashes'] if v['group']==g['spr_no']and v['direction']==a['direction']and v['palette']==palette);assert digest==old['RGBA_sha256'];result.append(old)
 out=dict(schema='stoneage.scene23.independent_actual_pixel_replay.r1',original_RD_bitmaps=96,RGBA_PNG_comparisons=count,complete_modern_card_canvases=len(result),all_indices_RGBA_PNG_and_canvas_hashes_equal=True,actual_source_browser_verified=False,original_world_entered=False,source_report_sha256=sha((folder/'source-derived-report.json').read_bytes()),frames=result)
 (folder/'independent-replay.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');return out
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--private-dir',type=Path,required=True);r=replay(p.parse_args().private_dir);print(json.dumps({k:v for k,v in r.items()if k!='frames'}))
