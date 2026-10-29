"""Fourteen synthetic PNGs; no original map cells, dialogue, or image bytes."""
import argparse,base64,io,json
from pathlib import Path
from PIL import Image
from tools.stoneage_scene25_room_shop import R14,R24,REPORT,render
from tools.stoneage_scene25_independent_replay import references

def image(w,h,color):
 im=Image.new('RGBA',(w,h),color);out=io.BytesIO();im.save(out,format='PNG');return base64.b64encode(out.getvalue()).decode()
def build():
 source=json.loads(R14.read_bytes());r24=json.loads(R24.read_bytes());report=json.loads(REPORT.read_bytes())
 sprites={str(5000+i):image(64,48,(30+i*15,70+i*10,90+i*9,255))for i in range(10)}
 room=dict(floor=1001,source_dat_sha256=source['source_members']['client-map/1001.dat']['sha256'],original_game_world_entered=False,sprites=sprites,R6_native_sorted_queue_numbers=[0,1,2],placements=[dict(map_id=5000+i,draw_x=i*32+60,draw_y=i*24-30)for i in range(3)])
 ob=dict(report=report,images={str(item['id']):image(item['alias_candidate']['width'],item['alias_candidate']['height'],(70+i*60,150,70,255))for i,item in enumerate(r24['items'])},synthetic_fixture=True)
 pack=dict(room=room,source=source,npc_image=image(36,79,(220,140,60,255)),welcome_original_parameter='SYNTHETIC TEXT ONLY',item_observation=ob);ob['synthetic_references']=references(pack);return pack
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.write_text(render(build()).replace('<h1>','<h1>全部合成色块｜',1))
