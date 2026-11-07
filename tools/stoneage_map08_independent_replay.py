"""Independent private DAT parsing and NumPy binary-alpha canvas verification."""
import hashlib,io,json,struct,zipfile
from pathlib import Path
from PIL import Image
import numpy as np
sha=lambda b:hashlib.sha256(b).hexdigest()
import argparse
p=argparse.ArgumentParser();p.add_argument('private_zip',type=Path);a=p.parse_args();root=Path(__file__).resolve().parents[1]
z=zipfile.ZipFile(a.private_zip)
r=json.loads(z.read('scene-source-receipt.json'))
private=json.loads(z.read('private-source-placements.json'));verified=0
images={}
for key,item in r['resources'].items():
 b=z.read('tiles/'+key+'.png');assert sha(b)==item['candidate_PNG_sha256']
 im=Image.open(io.BytesIO(b)).convert('RGBA');assert sha(im.tobytes())==item['candidate_RGBA_sha256']
 ar=np.array(im);assert set(np.unique(ar[:,:,3]))<={0,255};images[int(key)]=ar
for floor,info in r['maps'].items():
 print('verifying '+floor,flush=True)
 dat=z.read('source/'+floor+'.dat');assert sha(dat)==info['source_sha256']
 w,h=struct.unpack('<II',dat[:8]);n=w*h;selected=[]
 for plane,label in [(0,'tile'),(1,'parts')]:
  for diagonal in range(1-h,w):
   for x in range(w-1,-1,-1):
    y=x-diagonal
    if not 0<=y<h:continue
    number=int.from_bytes(dat[8+2*(plane*n+y*w+x):10+2*(plane*n+y*w+x)],'little')
    if number>99:selected.append({'layer':label,'xy':[x,y],'image_key':number,'anchor':[(x+y)*32,(y-x)*24]})
 assert selected==private[floor]['placements']
 width,height=info['canvas_size'];ox,oy=info['origin']
 for mode,expected in info['frames'].items():
  canvas=np.zeros((height,width,4),dtype=np.uint8);canvas[:]=[17,35,42,255]
  for p in selected:
   if mode=='plane0' and p['layer']=='parts':continue
   if mode=='plane1' and p['layer']=='tile':continue
   no=p['image_key'];record=r['resources'][str(no)];im=images[no];hh,ww=im.shape[:2]
   x=ox+p['anchor'][0]+record['xoff'];y=oy+p['anchor'][1]+record['yoff']
   assert 0<=x<=width-ww and 0<=y<=height-hh
   dest=canvas[y:y+hh,x:x+ww];mask=im[:,:,3]==255;dest[mask]=im[mask]
  png=z.read(floor+'-'+mode+'.png');assert sha(png)==expected['candidate_PNG_sha256']
  assert sha(canvas.tobytes())==expected['candidate_RGBA_sha256']
  with Image.open(io.BytesIO(png)) as image:
   assert sha(image.convert('RGBA').tobytes())==sha(canvas.tobytes())
  verified+=1
  del canvas
assert z.testzip() is None
result={'private_members':len(z.namelist()),'original_DAT_reparsed':len(r['maps']),'original_tiles_RGBA_and_PNG':len(images),'independent_complete_canvas_states':verified,'all_equal':True}
print(json.dumps(result))
