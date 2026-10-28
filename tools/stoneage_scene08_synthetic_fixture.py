"""Synthetic-only R8 browser fixture. No original imagery or species proof."""
import base64,hashlib,io,json,sys,tempfile
from pathlib import Path
from PIL import Image,ImageDraw
from tools.stoneage_scene07_synthetic_fixture import write as write_room

def write(target):
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'synthetic.html';write_room(p)
        old=json.loads(p.read_text().split('<script id="evidence" type="application/json">')[1].split('</script>')[0])
    human=old['actors']['groups'][0];human['animations']=[a for a in human['animations'] if a['action']==2]
    rows=[r for r in old['actors']['bitmaps'] if r['bitmapno'] in [123,124]]
    images={n:b for n,b in old['actor_images'].items() if n in ['123','124']};groups=[human]
    for gi,no in enumerate([100250,100251,100252]):
        ids=[]
        for i in range(8 if no==100252 else 2):
            n=1000+gi*100+i;ids.append(n);im=Image.new('RGBA',(20,16));draw=ImageDraw.Draw(im)
            draw.ellipse((1,1,18,14),fill=((i*31+gi*45+60)%256,(i*67+gi*80+50)%256,(i*43+gi*17+80)%256,255))
            out=io.BytesIO();im.save(out,format='PNG');b=out.getvalue();images[str(n)]=base64.b64encode(b).decode()
            rows.append({'bitmapno':n,'xoff':-10,'yoff':-16,'PNG_sha256':hashlib.sha256(b).hexdigest()})
        frames=[ids[i%len(ids)] for i in range(20 if no==100252 else 6)]
        groups.append({'spr_no':no,'preserved_template_name':'合成模板'+str(gi+1),
            'available_source_action_codes':[2],'template_links':[{'server_original_line':gi+1,'server_template_column_7':gi+1,'server_flag_column_38':1}],
            'animations':[{'direction':d,'action':2,'duration_word':500,'frames':[[n,0,0,0] for n in frames]} for d in range(8)]})
    pack={'room':old['room'],'actors':{'source_scope':'SYNTHETIC_TEST_ONLY_NOT_ORIGINAL_SOURCE','groups':groups,'bitmaps':rows},'actor_images':images}
    source=Path(__file__).with_name('scene-room-pet-viewer-r8.html').read_text();target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(source.replace('"PRIVATE_PACK_PLACEHOLDER"',json.dumps(pack,ensure_ascii=False)))

if __name__=='__main__':write(sys.argv[1])
