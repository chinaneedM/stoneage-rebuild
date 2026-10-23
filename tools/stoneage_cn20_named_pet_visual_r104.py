"""Three literal official web-cell image supplements, never native species IDs."""
import argparse
import hashlib
import io
import json
from pathlib import Path
from urllib.request import Request,urlopen
from .stoneage_waei_cn20_new_pet_pagination import parse_page
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'research/recovered/STONEAGE-CN20-NAMED-PET-VISUAL-SOURCE-R104.json'
SOURCE_SHA='9a771b202d5a0bb980de801bb96d8df02da9c2134336679ff09158695f1b5073'
POSITIONS=(84,88,89)
PARENT='research/recovered/STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-R1.json'

def require(ok,message):
    if not ok:raise ValueError(message)

def sha(raw):return hashlib.sha256(raw).hexdigest()

def pin(raw):
    return {'bytes':len(raw),'sha256':sha(raw),'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}

def extract(raw,d,verify_page_bytes=True):
    if verify_page_bytes:require(pin(raw)==d['page']['identity'],'Exact archived page bytes changed')
    grid=parse_page(raw.decode('gb18030',errors='strict'),1)
    rows=[]
    old=json.loads((ROOT/PARENT).read_text())
    for n in POSITIONS:
        r=old['records'][n-1];pos=r['source_position'];cell=grid[pos['row']-1][pos['column']-1]
        require(cell==[r['name_as_written'],r['image_reference']['relative_src_as_written'],r['image_reference']['html_declared_dimensions']], 'Named cell association changed')
        require(r['image_reference']['pixels_requested'] is False and r['original_game_pet_id'] is None,'Old historical unacquired state changed')
        rows.append({'ordinal':n,'existing_catalog_record_id':r['record_id'],'name_as_written':cell[0],
                     'row':pos['row'],'column':pos['column'],'relative_src_as_written':cell[1],
                     'html_declared_dimensions':cell[2],'original_image_url':r['image_reference']['original_url']})
    require(rows==d['selected_cells'],'Selected three literal cells changed')
    return rows

def image_metadata(raw,expected):
    from PIL import Image
    require(len(raw)==expected['bytes'] and sha(raw)==expected['sha256'],'Image bytes changed')
    with Image.open(io.BytesIO(raw)) as im:
        im.load();facts={'format':im.format,'mode':im.mode,'size':list(im.size),'frames':getattr(im,'n_frames',1)}
    require(facts==expected['decoded'],'Full image decoding differs')
    return facts

def validate(d):
    raw=SOURCE.read_bytes();require(sha(raw)==SOURCE_SHA and d==json.loads(raw),'Immutable source contract changed')
    for path,expected in d['parents'].items():require(pin((ROOT/path).read_bytes())==expected,'Parent identity changed')
    require(len(d['records'])==3 and len({r['record_id'] for r in d['records']})==3,'Three visual supplements required')
    for r in d['records']:
        require({'record_id','entity_type','version_profile','source_refs','verification_status','rights_status','record_revision'}<=r.keys(),'Research record schema incomplete')
        require(r['game_ids'] is None and r['original_sprite_or_animation_verified'] is False and
                r['same_instant_as_page_proven'] is False and r['collection']=='pets','Visual supplement boundary promoted')
    return d

def replay(page,images,d):
    validate(d);require(len(images)==3,'Exactly three acquired images required')
    cells=extract(page,d)
    decoded=[]
    for raw,expected in zip(images,d['images']):
        facts=image_metadata(raw,expected)
        decoded.append({'ordinal':expected['ordinal'],'actual_url':expected['actual_url'],
                        'capture':expected['capture'],'bytes':len(raw),'sha256':sha(raw),'decoded':facts})
    return {'schema':'stoneage.cn20.named_pet_visual_replay.r104','source_sha256':SOURCE_SHA,
            'actual_page':pin(page),'selected_cells':cells,'actual_images':decoded,
            'records':d['records'],'boundaries':d['boundaries'],
            'manual_review_repeated_by_ci':False,'new_species_count':None}

def download(requested,expected_final):
    with urlopen(Request(requested,headers={'User-Agent':'StoneAgeResearch/1.0'}),timeout=40) as r:
        require(r.status==200 and r.url==expected_final,'HTTP status/final archived capture changed')
        return r.read()

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--page',type=Path)
    p.add_argument('--images',type=Path,nargs=3);p.add_argument('--write',type=Path,required=True);a=p.parse_args()
    d=validate(json.loads(SOURCE.read_text()));require(bool(a.page)==bool(a.images),'Both page/images or neither required')
    page=a.page.read_bytes() if a.page else download(d['page']['url'],d['page']['url'])
    images=[p.read_bytes() for p in a.images] if a.images else [download(i['requested_url'],i['actual_url']) for i in d['images']]
    result=replay(page,images,d);a.write.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'page':result['actual_page'],'images':result['actual_images'],'visual_supplements':3,
                      'same_instant_or_game_ids_proven':False},sort_keys=True))
if __name__=='__main__':main()
