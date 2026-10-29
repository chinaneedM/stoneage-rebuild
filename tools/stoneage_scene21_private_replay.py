"""Independent DAT bytes, RD runs, BGR palette and full source-image composites."""
import argparse,hashlib,io,json,struct,zipfile
from pathlib import Path
from PIL import Image
from tools.stoneage_scene14_independent_replay import decode

def sha(b):return hashlib.sha256(b).hexdigest()
def replay(folder):
 import numpy as np
 folder=folder.resolve();root=Path(__file__).resolve().parents[1];assert folder!=root and root not in folder.parents
 r=json.loads((folder/'source-derived-report.json').read_bytes());images={}
 with zipfile.ZipFile(folder/'private-original-subset.zip') as z:
  dat=z.read('1000.DAT');pal=z.read('Palet_1.sap');assert sha(dat)==r['source_map_sha256'] and sha(pal)==r['source_palette_sha256']
  w,h=struct.unpack('<II',dat[:8]);assert (w,h)==(160,160)
  cells=[]
  for y in range(96,107):
   for x in range(60,67):cells.append({'xy':[x,y],'tile':int.from_bytes(dat[8+2*(y*w+x):10+2*(y*w+x)],'little'),'parts':int.from_bytes(dat[8+2*(w*h+y*w+x):10+2*(w*h+y*w+x)],'little')})
  assert cells==r['cells']
  rgb=np.zeros((256,3),dtype=np.uint8);rgb[16:240]=np.frombuffer(pal[:672],dtype=np.uint8).reshape(224,3)[:,::-1];rgb[168]=0
  for key,row in r['resources'].items():
   rd=z.read(key+'.rd');assert sha(rd)==row['RD_sha256'];ww,hh,px=decode(rd);assert sha(px)==row['index_sha256'] and (ww,hh)==(row['width'],row['height'])
   indices=np.frombuffer(px,dtype=np.uint8).reshape(hh,ww)[::-1];rgba=np.empty((hh,ww,4),dtype=np.uint8);rgba[:,:,:3]=rgb[indices];rgba[:,:,3]=np.where(indices==0,0,255)
   assert sha(rgba.tobytes())==row['RGBA_candidate_sha256'];images[int(key)]=rgba
  # Separate diagonal enumeration rather than reuse the primary source sweep.
  grid=sorted([(x,y)for y in range(11)for x in range(7)],key=lambda q:(-(q[1]-q[0]),-q[0]));placements=[]
  for plane,layer in [(0,'tile'),(1,'parts')]:
   for rx,ry in grid:
    x,y=60+rx,96+ry;offset=8+2*(plane*w*h+y*w+x);key=int.from_bytes(dat[offset:offset+2],'little')
    if key>99:placements.append({'layer':layer,'xy':[x,y],'image_key':key,'anchor':[(x+y-166)*32,(y-x-40)*24]})
  assert placements==r['placements'];frames={}
  for name,expected in r['frames'].items():
   old=name.startswith('old_');parts='_parts1_' in name;npc=name.endswith('_npc1');width,height=r['canvas_size'];canvas=np.empty((height,width,4),dtype=np.uint8);canvas[:]=[17,35,42,255]
   def paste(key,x,y):
    im=images[key];rr=r['resources'][str(key)];xx=r['origin'][0]+x+rr['xoff'];yy=r['origin'][1]+y+rr['yoff'];hh,ww=im.shape[:2];assert 0<=xx<=width-ww and 0<=yy<=height-hh
    target=canvas[yy:yy+hh,xx:xx+ww];mask=im[:,:,3]==255;target[mask]=im[mask]
   for p in placements:
    if old and p['xy'][1]>102:continue
    if not parts and p['layer']=='parts':continue
    paste(p['image_key'],*p['anchor'])
   if npc and not old:paste(16048,0,0)
   assert sha(canvas.tobytes())==expected['RGBA_sha256'],name
   image=Image.open(folder/(name+'.png')).convert('RGBA');assert image.tobytes()==canvas.tobytes() and sha((folder/(name+'.png')).read_bytes())==expected['PNG_sha256'];frames[name]=sha(canvas.tobytes())
 model=json.loads((folder/'stoneage-town1000-scene21-observer.html').read_bytes().split(b'<script id="evidence" type="application/json">')[1].split(b'</script>')[0]);assert model['report']==r
 for name in frames:
  import base64
  assert sha(base64.b64decode(model['frames'][name]))==r['frames'][name]['PNG_sha256']
 out={'schema':'stoneage.scene21.independent_actual_source_pixel_replay.r1','source_report_sha256':sha((folder/'source-derived-report.json').read_bytes()),'actual_original_RD_images_verified':56,'full_canvas_states_verified':8,'canvas_size':r['canvas_size'],'frames':frames,'independent_DAT_cells':77,'assistant_actual_composite_viewed':False,'actual_source_browser_verified':False,'original_world_entered':False}
 (folder/'independent-replay.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');return out

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--private-dir',type=Path,required=True);a=p.parse_args();print(json.dumps(replay(a.private_dir),sort_keys=True))
