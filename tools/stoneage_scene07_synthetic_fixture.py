"""Write a synthetic-only test page; no original assets, source data or claims."""
import base64,hashlib,io,json
from pathlib import Path
import sys
from PIL import Image

def png(size,color):
    b=io.BytesIO();Image.new('RGBA',size,color).save(b,format='PNG');return b.getvalue()

def write(target):
    # Opaque synthetic rectangles exercise browser layering/animation, never
    # pretend to be original client resources or a source-qualified export.
    originals={5000:png((64,47),(52,70,57,255)),5001:png((32,64),(92,78,103,255))}
    actors={123:png((16,20),(220,50,30,255)),124:png((16,20),(60,220,30,255)),125:png((16,20),(40,60,220,255)),126:png((16,20),(220,200,30,255))}
    placements=[{'layer':'tile','map_id':5000,'draw_x':(x+y)*32-32,'draw_y':(y-x)*24-24} for y in range(5) for x in range(5)]
    placements += [{'layer':'parts','map_id':5001,'draw_x':64+i*20,'draw_y':-90} for i in range(5)]
    room={'floor':1001,'sprites':{str(n):base64.b64encode(b).decode() for n,b in originals.items()},'sprite_sha256':{str(n):hashlib.sha256(b).hexdigest() for n,b in originals.items()},'placements':placements,'R6_native_sorted_queue_numbers':list(reversed(range(25)))+list(reversed(range(25,30)))}
    groups=[{'spr_no':no,'animations':[{'direction':d,'action':a,'duration_word':1000,'frames':[[first,0,0,0],[first+1,0,0,0]]} for d in range(8) for a in [2,6]]} for no,first in [(100000,123),(100700,125)]]
    report={'source_scope':'SYNTHETIC_TEST_ONLY_NOT_ORIGINAL_SOURCE','groups':groups,'bitmaps':[{'bitmapno':n,'xoff':-8,'yoff':-20,'PNG_sha256':hashlib.sha256(b).hexdigest()} for n,b in actors.items()]}
    pack={'room':room,'actors':report,'actor_images':{str(n):base64.b64encode(b).decode() for n,b in actors.items()}}
    source=Path(__file__).with_name('scene-room-actor-viewer-r7.html').read_text()
    target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(source.replace('"PRIVATE_PACK_PLACEHOLDER"',json.dumps(pack)))

if __name__=='__main__':write(sys.argv[1])
