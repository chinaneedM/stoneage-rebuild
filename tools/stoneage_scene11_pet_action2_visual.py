"""SCENE11 source-safe recheck of original-source PET action2 pixels.
Offline mode validates derived report vs R40 historical material. --private-html
authenticates the full private R10 page, all 208 source PNG hashes and compares
real RGBA pixels, without ever serializing or publishing original PNG bytes.
"""
import argparse,base64,copy,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'research/recovered/STONEAGE-SCENE11-PET-ACTION2-VISUAL-R1.json'
R40=ROOT/'research/recovered/STONEAGE-PRESERVED-PET-SPR-MATERIAL-R40.json'
EXPECTED={100250:(240,'eb1a87cd4cc8e3b409990783c7bcc3bc463acab4cac7d2d961127d899da047ef',48,48,0,500),100251:(241,'073278ba6ae1e623eea969deef11f99fd9be8b995af332506e830bd046c86764',48,48,0,500),100252:(242,'eeb2ec4546277c2acdf1b43fff7967c4c0fe5ac5c019bb7d68a901e134691b0a',160,64,96,1200)}
PATTERN=[0,1,0,1,0,1,0,1,0,1,1,1,1,1,2,3,4,5,6,7]
def need(v,msg):
 if not v:raise ValueError(msg)
def sha(data):return hashlib.sha256(data).hexdigest()
def validate(report,source):
 need(report['schema']=='stoneage.scene11.pet_action2_visible_source_facts.r1','schema')
 need(report['source_scope']=='PRESERVED_COMMUNITY_MIXED25_NOT_AUTHENTICATED_OFFICIAL_TW10','scope')
 need(report['private_viewer_bytes']==1150992 and report['private_viewer_sha256']=='00e7565587e009c3e44bcffa1523ab4018886d637aaef1e04749dc01637628d4','private source identity')
 need(report['png_original_sha256_checked']==208 and report['selected_pet_pngs']==160 and report['character_pngs_control']==48,'source bitmap conservation')
 need(report['action_code']==2 and report['source_group_segment_verified_to_R40'] is True,'source-bounded action')
 need(len(report['groups'])==3,'3 finite source graphics')
 groups={z['graphic_no']:z for z in report['groups']}
 need(set(groups)==set(EXPECTED),'graphics')
 mat={z['spr_no']:z for z in source['full_segment_comparisons']}
 need(set(EXPECTED)<=set(mat),'R40 source groups')
 for number,(idx,digest,frames,unique,repeats,duration) in EXPECTED.items():
  g=groups[number]
  need((g['original_spr_index'],g['full_group_SHA256'],g['original_action2_frame_positions'],g['different_source_images'],g['repeated_frame_positions'],g['original_duration_word'])==(idx,digest,frames,unique,repeats,duration),'source action2 material diverged')
  need(mat[number]['segment_sha256']==digest and mat[number]['client_group_index']==idx,'R40 full group segment mismatch')
  need(g['direction_count']==8,'eight directions')
  need(len(g['direction_visible_pixel_totals'])==len(g['direction_union_bbox_xyxy'])==len(g['direction_unique_source_images'])==8,'direction records')
  need(all(type(n)==int and n>0 for n in g['direction_visible_pixel_totals']),'alpha count')
  need(all(len(b)==4 and b[0]==b[1]==0 and 0<b[2]<=256 and 0<b[3]<=256 for b in g['direction_union_bbox_xyxy']),'visible bounds')
  need(g['direction_unique_source_images']==[6 if frames==48 else 8]*8,'direction distinct counts')
  need(frames==sum(g['direction_unique_source_images'])+repeats,'original sequence multiplicity')
 a,b=groups[100250],groups[100251]
 need(a['direction_union_bbox_xyxy']==b['direction_union_bbox_xyxy'],'paired silhouette bounds')
 p=report['pair_100250_100251']
 need(p['aligned_source_frames']==48 and p['exact_alpha_masks']==38 and p['total_alpha_mask_pixel_differences']==12 and p['total_rgba_pixel_differences']==43069 and p['rgba_identical_frames']==0,'pixel pair totals')
 need(p['per_direction_exact_alpha_masks']==[5,3,5,4,5,6,5,5] and sum(p['per_direction_visible_pixel_differences'])==43069,'paired direction totals')
 need(report['graphic_100252_direction_frame_pattern']==PATTERN,'20-position source repetition pattern')
 for flag in ['original_game_world_entered','original_native_client_render_verified','official_species_identity_proven','same_deployed_build_proven','original_frame_rate_authenticated','private_proprietary_png_published']:
  need(report[flag] is False,'unsafe historical status: '+flag)
 need(report['percent_restored'] is None,'no invented restoration percent')
 return {'pet_graphics':3,'direction_sequences':24,'source_frames':256,'distinct_pet_source_pngs':160,'paired_frames':48,'original_world_entered':False}
def real_private_pixel_replay(path,report):
 from PIL import Image,ImageChops
 b=Path(path).read_bytes()
 need(len(b)==report['private_viewer_bytes'] and sha(b)==report['private_viewer_sha256'],'original private observer whole SHA')
 m=re.search(rb'<script id="evidence" type="application/json">(.*?)</script>',b,re.S)
 need(m is not None,'original evidence')
 root=json.loads(m.group(1));imgs=root['actor_images']
 records={x['bitmapno']:x for x in root['actors']['bitmaps']}
 need(len(imgs)==len(records)==208 and set(map(int,imgs))==set(records),'source frame PNG set')
 im={}
 for k,b64 in imgs.items():
  bid=int(k);raw=base64.b64decode(b64,validate=True);rec=records[bid]
  need(sha(raw)==rec['PNG_sha256'],'raw PNG checksum '+k)
  obj=Image.open(io.BytesIO(raw));need(obj.format=='PNG' and obj.mode=='RGBA','original source must be RGBA')
  need(obj.size==(rec['width'],rec['height']),'recorded ADRN PNG dimensions')
  im[bid]=obj
 groups={g['spr_no']:g for g in root['actors']['groups']}
 need(set(groups)=={100000,100250,100251,100252},'bounded graphics set')
 for g in report['groups']:
  src=groups[g['graphic_no']]
  need(src['source_group_index']==g['original_spr_index'] and src['whole_group_segment_sha256']==g['full_group_SHA256'],'source segment mismatch')
  anim={a['direction']:a for a in src['animations']}
  need(set(anim)==set(range(8)),'actual 8 directions')
  all_ids=set();occ=0
  for direction in range(8):
   seq=anim[direction];ids=[f[0] for f in seq['frames']]
   need(seq['action']==2 and seq['duration_word']==g['original_duration_word'],'action/duration mismatch')
   need(all(len(f)==4 and f[1:]==[0,0,0] for f in seq['frames']),'source displacement mismatch')
   need(len(ids)==g['original_action2_frame_positions']//8,'frame count')
   if g['graphic_no']==100252:
    keys=list(dict.fromkeys(ids));need([keys.index(x) for x in ids]==PATTERN,'source frame pattern mismatch')
   all_ids.update(ids);occ+=len(ids)
   tot=0;rect=[]
   for bid in ids:
    alpha=im[bid].getchannel('A')
    tot+=sum(a>0 for a in alpha.getdata())
    r=alpha.point(lambda a:255 if a else 0).getbbox()
    need(r is not None,'unexpected transparent source sprite')
    rect.append(r)
   bbox=[min(r[0] for r in rect),min(r[1] for r in rect),max(r[2] for r in rect),max(r[3] for r in rect)]
   need(tot==g['direction_visible_pixel_totals'][direction] and bbox==g['direction_union_bbox_xyxy'][direction],'real source visible pixels')
  need(len(all_ids)==g['different_source_images'] and occ==g['original_action2_frame_positions'],'frame references')
 mask_equal=changed_mask=changed_rgba=0;per_equal=[];per_rgba=[]
 a={s['direction']:s for s in groups[100250]['animations']}
 c={s['direction']:s for s in groups[100251]['animations']}
 for direction in range(8):
  eq=0;rgba_count=0
  for fa,fb in zip(a[direction]['frames'],c[direction]['frames']):
   p,q=im[fa[0]],im[fb[0]]
   need(p.size==q.size,'source pair dimensions')
   opa=p.getchannel('A').point(lambda t:255 if t else 0)
   opb=q.getchannel('A').point(lambda t:255 if t else 0)
   dif_mask=sum(t>0 for t in ImageChops.difference(opa,opb).getdata())
   dif_rgba=sum(any(v!=0 for v in pixel) for pixel in ImageChops.difference(p,q).getdata())
   eq+=int(dif_mask==0);changed_mask+=dif_mask;rgba_count+=dif_rgba
  per_equal.append(eq);per_rgba.append(rgba_count);mask_equal+=eq;changed_rgba+=rgba_count
 p=report['pair_100250_100251']
 need(mask_equal==p['exact_alpha_masks'] and changed_mask==p['total_alpha_mask_pixel_differences'],'source pair alpha delta')
 need(changed_rgba==p['total_rgba_pixel_differences'],'actual RGBA difference')
 need(per_equal==p['per_direction_exact_alpha_masks'] and per_rgba==p['per_direction_visible_pixel_differences'],'pair direction conservation')
 return {'source_pngs_hash_verified':208,'pet_source_pngs':160,'source_frame_positions':256,'matching_alpha_masks':mask_equal,'changed_RGBA_pixel_positions':changed_rgba,'original_game_world_entered':False}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--private-html',type=Path,default=None);a=ap.parse_args()
 report=json.loads(S.read_text(encoding='utf-8'));source=json.loads(R40.read_text(encoding='utf-8'))
 print(json.dumps({'offline':validate(report,source),'private':real_private_pixel_replay(a.private_html,report) if a.private_html else 'NOT_RUN_REQUIRES_PRIVATE_PROPRIETARY_SOURCE'},ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
