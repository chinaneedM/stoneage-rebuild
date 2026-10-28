"""Independent original doorway spans,51 private RD images and observer canvases.
Original pixels remain outside Git. This is not original game execution.
"""
import argparse,base64,hashlib,io,json,math,struct,zipfile
from pathlib import Path
from PIL import Image,ImageDraw
from tools.stoneage_scene14_independent_replay import decode,source_blocks


def sha(b):return hashlib.sha256(b).hexdigest()

def replay(folder,warp,template):
    folder=folder.resolve();root=Path(__file__).resolve().parents[1];assert folder!=root and root not in folder.parents
    r=json.loads((folder/'source-derived-report.json').read_bytes());html=(folder/'stoneage-r15-doorway-observer.html').read_bytes();pack=json.loads(html.split(b'<script id="evidence" type="application/json">')[1].split(b'</script>')[0]);actual=json.loads((folder/'browser-replay.json').read_bytes())
    raw=warp.read_bytes();gs=source_blocks(raw)
    for d in r['doorway_pair']:
        b=d['source_block'];g=gs[b['ordinal']];assert (g['start'],g['end'],sha(raw[g['start']:g['end']]))==(b['byte_start'],b['byte_end'],b['block_sha256'])
        f=g['fields'];target=f[b'enemy'].decode('ascii').split('|');assert target==['npcgen_warp',str(d['destination_floor']),*map(str,d['destination_xy'])]
    raw=template.read_bytes();b=r['template_block'];g=source_blocks(raw)[b['ordinal']];assert sha(raw[g['start']:g['end']])==b['block_sha256'] and g['fields'][b'functionset']==b'Warp'
    sap=(folder/'private-palette.sap').read_bytes();assert sha(sap)==r['source_art_files']['Palet_1.sap']['sha256'];pal={i+16:tuple(sap[i*3:i*3+3][::-1]) for i in range(224)};pal[0]=(0,0,0);pal[168]=(0,0,0);images={}
    with zipfile.ZipFile(folder/'private-source-rd-subset.zip') as z:
        assert len(z.namelist())==51
        for key,row in r['resources'].items():
            rd=z.read(key+'.rd');assert sha(rd)==row['RD_sha256'];w,h,indices=decode(rd);assert (w,h)==(row['width'],row['height']) and sha(indices)==row['index_pixels_sha256']
            rgba=bytes(v for y in range(h-1,-1,-1) for n in indices[y*w:(y+1)*w] for v in (*pal[n],0 if n==0 else 255));assert sha(rgba)==row['RGBA_candidate_sha256']
            png=base64.b64decode(pack['images'][key]);assert sha(png)==row['PNG_sha256'];im=Image.open(io.BytesIO(png)).convert('RGBA');assert im.tobytes()==rgba;images[int(key)]=im
    png=base64.b64decode(pack['human_image']);assert sha(png)==r['human_reference']['bitmap']['PNG_sha256'];human=Image.open(io.BytesIO(png)).convert('RGBA');frames=[]
    for frame in actual['frames']:
        s=frame['state'];scale=s['scale'];assert scale in (1,2) and s['dx']==s['dy']==0;view=next(v for v in r['views'] if v['floor']==s['floor']);bounds=view['source_art_bounds'];ox=math.floor((960-(bounds[2]-bounds[0])*scale)/2)-bounds[0]*scale;oy=math.floor((720-(bounds[3]-bounds[1])*scale)/2)-bounds[1]*scale
        canvas=Image.new('RGBA',(960,720),'#11232a')
        def paste(im,x,y):canvas.alpha_composite(im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST),(ox+x*scale,oy+y*scale))
        for p in view['placements']:
            if p['layer']=='parts' and not frame['showParts']:continue
            paste(images[p['map_id']],*p['draw_relative'])
        if frame['showMarker']:
            draw=ImageDraw.Draw(canvas);draw.rectangle((ox-5*scale,oy,ox+6*scale-1,oy+scale-1),fill='#edc66f');draw.rectangle((ox,oy-5*scale,ox+scale-1,oy+6*scale-1),fill='#edc66f')
        if frame['showHuman']:
            f=r['human_reference']['source_frame'];row=r['human_reference']['bitmap'];dx=s['x']-view['center_xy'][0];dy=s['y']-view['center_xy'][1];paste(human,(dx+dy)*32+f[1]+row['xoff'],(dy-dx)*24+f[2]+row['yoff'])
        digest=sha(canvas.tobytes());assert digest==frame['canvas_sha256'],frame['label'];frames.append({'label':frame['label'],'canvas_sha256':digest})
    result={'schema':'stoneage.scene15.independent_private_replay.r1','source_config_spans_verified':3,'independent_original_RD_index_RGBA_PNGs':51,'human_reference_PNG_verified':1,'all_integer_scale_full_canvas_matches':len(frames),'canvas_pixels':691200,'frames':frames,'original_world_entered':False}
    (folder/'independent-replay.json').write_text(json.dumps(result,indent=2)+'\n');return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--private-dir',type=Path,required=True);p.add_argument('--warp',type=Path,required=True);p.add_argument('--template',type=Path,required=True);a=p.parse_args();r=replay(a.private_dir,a.warp,a.template);print(json.dumps({k:v for k,v in r.items() if k!='frames'}))
if __name__=='__main__':main()
