"""Independent original item fields, ADRN namespaces, RD and modern card pixels."""
import argparse,base64,hashlib,io,json,struct,zipfile
from pathlib import Path
from PIL import Image
from tools.stoneage_scene14_independent_replay import decode

def sha(b):return hashlib.sha256(b).hexdigest()
def replay(folder,server,mixed_file,tw_file):
 root=Path(__file__).resolve().parents[1];folder=folder.resolve();assert folder!=root and root not in folder.parents
 r=json.loads((folder/'source-derived-report.json').read_bytes());model=json.loads((folder/'StoneAge-SCENE24-item-observer.html').read_bytes().split(b'<script id="evidence" type="application/json">')[1].split(b'</script>')[0]);assert model['report']==r
 # Separate selected-row scan, explicit original numeric columns (0-based17 etc).
 positions={};offset=0
 for line_no,line in enumerate((server/'itemset.txt').read_bytes().splitlines(keepends=True),1):
  row=line.rstrip(b'\r\n');cols=[x.strip()for x in row.split(b',')]
  if len(cols)==94 and cols[16]in[b'0',b'4',b'10']:
   key=int(cols[16]);assert key not in positions;positions[key]=(line_no,offset,row,cols)
  offset+=len(line)
 assert set(positions)=={0,4,10}
 mixed=mixed_file.read_bytes();tw=tw_file.read_bytes();assert mixed[:len(tw)]==tw and sha(mixed)==r['mixed_ADRN']['sha256']and sha(tw)==r['client_source_files']['adrn_1.bin']['sha256']
 for item in r['items']:
  ln,off,raw,c=positions[item['id']];old=item['source_row'];assert ln==old['physical_line']and off==old['byte_offset']and sha(raw)==old['row_sha256'];assert [int(c[k])for k in[17,18,19,22]]==[item['imagenumber'],old['numeric_fields']['cost'],old['numeric_fields']['type'],old['numeric_fields']['level']]
  key=item['imagenumber'];am=[];bm=[]
  for p in range(0,len(mixed),80):
   if int.from_bytes(mixed[p+76:p+80],'little')==key:am.append(p//80)
   if int.from_bytes(mixed[p:p+4],'little')==key:bm.append(p//80)
  assert am==[item['alias_candidate']['index']]and bm==[item['literal_bitmap_control']['index']]
  for row in [item['alias_candidate'],item['literal_bitmap_control']]:
   record=mixed[row['index']*80:row['index']*80+80];assert sha(record)==row['record_sha256']and record==tw[row['index']*80:row['index']*80+80]
 ims={};frames=[]
 with zipfile.ZipFile(folder/'private-source-image-subset.zip')as z:
  for palette in ('0','1'):
   sap=z.read('Palet_'+palette+'.sap');rgb={n+16:tuple(sap[n*3:n*3+3][::-1])for n in range(224)};rgb[0]=(0,0,0);rgb[168]=(0,0,0)
   for item in r['items']:
    for row in[item['alias_candidate'],item['literal_bitmap_control']]:
     n=row['bitmapno'];rd=z.read(str(n)+'.rd');assert sha(rd)==row['RD_sha256'];w,h,indices=decode(rd);assert (w,h)==(row['width'],row['height'])and sha(indices)==row['indices_sha256'];assert all(n in rgb for n in indices)
     rgba=bytes(c for y in range(h-1,-1,-1)for n in indices[y*w:(y+1)*w]for c in(*rgb[n],0 if n==0 else 255));expected=row['palette_candidates'][palette];assert sha(rgba)==expected['RGBA_sha256'];png=base64.b64decode(model['images'][palette][str(n)]);assert sha(png)==expected['PNG_sha256'];im=Image.open(io.BytesIO(png)).convert('RGBA');assert im.tobytes()==rgba;ims[(palette,n)]=im
  for mode in ('alias','literal'):
   for palette in ('0','1'):
    for scale in(2,4):
     for item in r['items']:
      row=item['alias_candidate'if mode=='alias'else'literal_bitmap_control'];im=ims[(palette,row['bitmapno'])];c=Image.new('RGBA',(320,360),(20,33,41,255));im=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST);c.alpha_composite(im,((320-im.width)//2,(360-im.height)//2));digest=sha(c.tobytes());old=next(x for x in model['canvas_hashes']if(x['item'],x['mode'],x['palette'],x['scale'])==(item['id'],mode,palette,scale));assert digest==old['RGBA_sha256'];frames.append(old)
 out=dict(schema='stoneage.scene24.independent_original_source_and_pixels.r1',source_report_sha256=sha((folder/'source-derived-report.json').read_bytes()),selected_original_rows_independently_reparsed=3,full_mixed_ADRN_namespaces_checked=True,independent_RD_index_images=6,independent_RGBA_PNG_comparisons=12,complete_card_canvases=24,all_source_pixels_and_canvas_hashes_equal=True,original_source_browser_verified=False,original_world_entered=False,frames=frames)
 (folder/'independent-replay.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');return out
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--private-dir',type=Path,required=True);p.add_argument('--server',type=Path,required=True);p.add_argument('--mixed-adrn',type=Path,required=True);p.add_argument('--tw-adrn',type=Path,required=True);a=p.parse_args();r=replay(a.private_dir,a.server,a.mixed_adrn,a.tw_adrn);print(json.dumps({k:v for k,v in r.items()if k!='frames'}))
