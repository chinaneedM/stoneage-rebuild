"""Private accepted-parent byte comparison and independent integer Pillow replay."""
import argparse,base64,hashlib,io,json,zipfile
from pathlib import Path
from PIL import Image,ImageDraw

def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def model(b):return json.loads(b.split(b'<script id="evidence" type="application/json">',1)[1].split(b'</script>',1)[0])
def png(b64):return Image.open(io.BytesIO(base64.b64decode(b64,validate=True))).convert('RGBA')
def room_frame(pack,show_npc=True,show_anchor=True):
 c=Image.new('RGBA',(960,720),'#11232a');room=pack['room'];maps={int(n):png(b)for n,b in room['sprites'].items()}
 def paste(im,x,y):c.alpha_composite(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(480+2*(x-128),360+2*(y+80)))
 for no in room['R6_native_sorted_queue_numbers']:
  p=room['placements'][no];paste(maps[p['map_id']],p['draw_x'],p['draw_y'])
 if show_anchor:
  d=ImageDraw.Draw(c);d.rectangle((472,328,489,329),fill='#f0c979');d.rectangle((480,320,481,337),fill='#f0c979')
 if show_npc:
  r=pack['source']['candidate_graphic'];paste(png(pack['npc_image']),128+r['xoff'],-96+r['yoff'])
 return c
def card_frame(b64):
 im=png(b64);c=Image.new('RGBA',(320,240),'#142129');im=im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST);c.alpha_composite(im,((320-im.width)//2,(240-im.height)//2));return c
def references(pack):
 return dict(room=[dict(label=label,RGBA_sha256=sha(room_frame(pack,n,a).tobytes()))for label,n,a in [('default',True,True),('npc_hidden',False,True),('anchor_hidden',True,False),('map_only',False,False)]],cards=[dict(id=int(n),RGBA_sha256=sha(card_frame(b).tobytes()))for n,b in pack['item_observation']['images'].items()])
def replay(folder):
 root=Path(__file__).resolve().parents[1];folder=folder.resolve();assert folder!=root and root not in folder.parents
 html=(folder/'StoneAge-SCENE25-room-shop-observer.html').read_bytes();pack=model(html);report=json.loads((folder/'integration-report.json').read_bytes());assert pack['item_observation']['report']==report and pack['item_observation']['synthetic_fixture'] is False
 for filename,key in [('parent-room-observation.zip','room_archive'),('parent-item-observation.zip','items_archive')]:
  raw=(folder/filename).read_bytes();assert (len(raw),sha(raw))==(report['parents'][key]['bytes'],report['parents'][key]['sha256'])
 with zipfile.ZipFile(folder/'parent-room-observation.zip')as rz,zipfile.ZipFile(folder/'parent-item-observation.zip')as iz:
  old_html=rz.read('stoneage-room-r14-shop-observer.html');old=model(old_html);items=model(iz.read('StoneAge-SCENE24-item-observer.html'))
  assert pack['room']==old['room'] and pack['source']==old['source'] and pack['npc_image']==old['npc_image'] and pack['welcome_original_parameter']==old['welcome_original_parameter']
  assert sha(canon(pack['room']))==report['room_model_sha256']
  assert old_html.split(b'function draw(){',1)[1].split(b'function inspect(){',1)[0]==html.split(b'function draw(){',1)[1].split(b'function inspect(){',1)[0]
  assets=[]
  for name,b64 in list(pack['room']['sprites'].items())+[('npc5863',pack['npc_image'])]:
   raw=base64.b64decode(b64);assets.append(dict(label=name,PNG_sha256=sha(raw),RGBA_sha256=sha(png(b64).tobytes())))
  for row in report['items']:
   key=str(row['id']);b64=pack['item_observation']['images'][key];assert b64==items['images']['1'][str(row['candidate_bitmap'])]
   image=png(b64);assert sha(base64.b64decode(b64))==row['PNG_sha256'] and sha(image.tobytes())==row['RGBA_sha256'];assets.append(dict(label='item'+key,PNG_sha256=row['PNG_sha256'],RGBA_sha256=row['RGBA_sha256']))
  ref=references(pack);prior=json.loads(rz.read('browser-replay.json'))
  for f in ref['room']:assert f['RGBA_sha256']==next(v['canvas_sha256']for v in prior['frames']if v['label']==f['label'])
  # Reparse the three original table rows independently, with their old byte spans.
  original=rz.read('originals/itemset.txt');offset=0;found={}
  for i,line in enumerate(original.splitlines(keepends=True),1):
   row=line.rstrip(b'\r\n');cols=[c.strip()for c in row.split(b',')]
   if len(cols)==94 and cols[16] in [b'0',b'4',b'10']:
    key=int(cols[16]);assert key not in found;found[key]=(i,offset,row,cols)
   offset+=len(line)
  assert set(found)=={0,4,10}
  for row in pack['source']['selected_items']:
   i,offset,raw,c=found[row['id']];assert (i,offset,sha(raw))==(row['physical_line'],row['byte_offset'],row['row_sha256']);assert c[0].decode('cp950')==row['name_original'];assert [int(c[k])for k in [17,18,19,22]]==[row['numeric_fields'][k]for k in ['imagenumber','cost','type','level']]
 result=dict(schema='stoneage.scene25.independent_parent_and_pixels.r1',integration_report_sha256=sha((folder/'integration-report.json').read_bytes()),room_model_and_11_original_PNG_bytes_identical=True,draw_function_byte_identical=True,three_item_PNG_bytes_identical=True,original_item_rows_reparsed=3,original_PNGs=14,integer_room_frames_equal_prior_browser=4,new_integer_card_frames=3,original_source_browser_verified=False,original_world_entered=False,original_transaction_verified=False,references=ref,assets=assets)
 (folder/'independent-replay.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 contact=Image.new('RGBA',(1280,720),'#142129');contact.alpha_composite(room_frame(pack),(0,0))
 for n,b in enumerate(pack['item_observation']['images'].values()):contact.alpha_composite(card_frame(b),(960,n*240))
 contact.save(folder/'StoneAge-SCENE25-independent-room-and-cards.png');return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--private-dir',type=Path,required=True);a=p.parse_args();r=replay(a.private_dir);print(json.dumps({k:v for k,v in r.items()if k not in ['references','assets']}))
