"""One archived operator-page image reference, with capture dates kept apart.

Public replay uses derived metadata and synthetic HTML/JPEG headers only.
Original page/images and the offline reader stay private. No game is executed.
"""
import argparse
import base64
from datetime import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
import zipfile

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-SCENE36-RIDING-IMAGE-REFERENCE-R1.json'
AUDIT=ROOT/'research/recovered/STONEAGE-SCENE36-PRIVATE-IMAGE-AUDIT-R1.json'
PAGE_ORIGINAL='http://www.wayi.com.tw/stoneage/producer/producer02.asp?idno=66'
PAGE_URL='https://web.archive.org/web/20051117143741id_/'+PAGE_ORIGINAL
PAGE_PIN=(19964,'b1f2163b80137e2140c36a6675a42e4ac1f2e3cc367e08b2a850cd15a6261790')
ORIGINALS=['http://www.wayi.com.tw/images02/sa1210-1.jpg','http://www.wayi.com.tw/images02/sa1210-2.jpg']
IMAGE_PINS=[
 (91133,'f96377883b93a5b12f10a78167b97f2e1a98c4651ad8aa3754161fa05a7ad9f7','20061022095340',[640,480],'3f243591b9ed0755a20c15521b8b74313c8cdc4105bc40cec4db80f71b7aca05'),
 (44719,'ad370b462462769dcfc8bc9430b648f6faf990101cdfec3c71e94871be7ac06f','20040611050307',[300,225],'006eb1e5f74a4f8cc9bdf6c039803b98762bae4db115a36266d28986759a3b07'),
]
PARENTS={
 'STONEAGE-CN20-RIDING-TRAINER-COMBAT-SOURCE-R1.json':(14868,'e41de8bc186771906554775e885cf66ab995a06f01618f7f2d3724a888e69c81'),
 'STONEAGE-CN40-RIDING-CERTIFICATE-MANOR-SOURCE-R1.json':(29266,'3c0f771e0547ed753b38359ccf61023f54c82b4ba4ba2dc1684a1ac8b6f7aae8'),
 'STONEAGE-WAYI2003-NEWBIE-RIDING-PLAN-R1.json':(11911,'b23c0220c58840ddb14ee9eea835687924cc16b42afe091af127f67472580fcd'),
 'STONEAGE-WAYI2003-RIDING-SUCCESSOR-ORE-WORK-R1.json':(7384,'d2c18a33dd56c5aa5ba886ec591b619b3e6b32fcb67385db1e09db8b900b9125'),
 'STONEAGE-TW80-MOUNT-CERTIFICATE-EQUIPMENT-SOURCE-R1.json':(14349,'265a3a9cc19d5a349bf15e381875b20ea2899562ff950d2fc513be8a77fec2e4'),
}
FALSE=('original_client_executed','original_server_executed','original_world_entered',
 'new_riding_eligibility_rule_recovered','newbie_tiger_delivery_implemented_proven',
 'image_is_verified_riding_eligibility_UI','same_build_as_article_authenticated',
 'original_2003_pixels_authenticated','full_and_inline_pixel_identity_authenticated',
 'images_are_independent_runtime_witnesses','exact_NPC_or_quest_identity_authenticated',
 'original_dialogue_transaction_verified','quest_rewards_or_flags_authenticated',
 'raw_original_page_or_images_published','private_original_browser_executed')
FROZEN='f4f23ef7d5217057221cb629150f9fdbedfd1a256fd920c528eb8a914eb014dd'
AUDIT_FROZEN='cc3c284e3cc5dfb6c7468b6aa0cd220cbf492b02a178bfc7ef0a9b9c925c8239'

def need(ok,message):
    if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(r):return json.dumps(r,sort_keys=True,separators=(',',':')).encode()
def pin(b,p):need((len(b),sha(b))==p,'exact source byte identity')

def capture(url,original):
    m=re.fullmatch(r'https://web\.archive\.org/web/(\d{14})id_/'+re.escape(original),url)
    need(m is not None,'archive host/original path identity')
    datetime.strptime(m[1],'%Y%m%d%H%M%S');return m[1]

class LinkPair(HTMLParser):
    def __init__(self):super().__init__();self.anchor=None;self.found=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='a':self.anchor=a.get('href')
        if tag=='img' and (a.get('src')in ORIGINALS or self.anchor in ORIGINALS):
            self.found.append(dict(anchor_href=self.anchor,img_src=a.get('src')))
    def handle_endtag(self,tag):
        if tag=='a':self.anchor=None

def link_pair(doc):
    p=LinkPair();p.feed(doc)
    need(p.found==[dict(anchor_href=ORIGINALS[0],img_src=ORIGINALS[1])],'one actual anchor/inline image pair')
    return p.found[0]

def jpeg_shape(raw):
    """Read just the bounded SOF metadata; not an independent pixel decoder."""
    need(raw[:2]==b'\xff\xd8' and raw[-2:]==b'\xff\xd9','JPEG SOI/EOI')
    pos=2
    while pos<len(raw)-1:
        need(raw[pos]==255,'JPEG marker');pos+=1
        while pos<len(raw) and raw[pos]==255:pos+=1
        need(pos<len(raw),'JPEG marker bounds');marker=raw[pos];pos+=1
        need(marker not in (0xda,0xd9),'SOF required before scan')
        need(pos+2<=len(raw),'JPEG segment length');size=struct.unpack_from('>H',raw,pos)[0]
        need(size>=2 and pos+size<=len(raw),'JPEG segment bounds')
        if marker in (0xc0,0xc1,0xc2):
            need(size>=8,'JPEG SOF size');bits,h,w,n=struct.unpack_from('>BHHB',raw,pos+2)
            need(w>0 and h>0 and size==8+3*n,'JPEG SOF dimensions/components')
            return dict(marker=marker,precision=bits,size=[w,h],components=n)
        pos+=size
    raise ValueError('JPEG SOF absent')

def parents():
    for p,v in PARENTS.items():pin((ROOT/'research/recovered'/p).read_bytes(),v)
    old=json.loads((ROOT/'research/recovered/STONEAGE-WAYI2003-NEWBIE-RIDING-PLAN-R1.json').read_bytes())
    need(old['unacquired_image_refs']==ORIGINALS and old['coverage']['images_programs_or_new_game_entities']==0,'old capture-time no-image report retained')
    return [dict(path='research/recovered/'+p,bytes=v[0],sha256=v[1])for p,v in PARENTS.items()]

def viewer(images):
    figures=[]
    for i,(raw,p)in enumerate(zip(images,IMAGE_PINS)):
        role='页面链接目标'if i==0 else'页面内嵌图'
        figures.append('<figure><h2>'+role+' · '+p[2][:4]+'-'+p[2][4:6]+'-'+p[2][6:8]+'捕获</h2><img alt="'+role+'" src="data:image/jpeg;base64,'+base64.b64encode(raw).decode()+'"><figcaption>'+str(p[3][0])+'×'+str(p[3][1])+'；原JPEG字节保留，未重绘或补字。</figcaption></figure>')
    return '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>新手骑宠计划页面的一处图像引用</title><style>
body{background:#eeeadd;color:#273e43;font:17px/1.8 system-ui;margin:0}
main{max-width:960px;margin:40px auto;padding:0 24px}h1{font-size:31px;line-height:1.35}
.note{background:#e0e7dd;border-left:4px solid #71897a;padding:14px 22px}
figure{margin:28px 0;padding:22px;background:#fffdf7;border:1px solid #d6d1c3;border-radius:12px}
img{max-width:100%;height:auto;display:block}figcaption,small{font-size:14px;color:#596c6e}
</style><main><small>SCENE36 · 官方原网页图像引用 · 现代离线查阅</small>
<h1>这处截图实际展示了什么</h1><p class="note">原页面的一处链接，把300×225页内图指向640×480目标图。
两份JPEG来自不同归档捕获，不能当成同日、同构建或2003年原始像素。</p>
<p>目前可辨的是覆盖室内场景的半透明NPC对话窗，以及“確定／取消”按钮。
这不是我们运行游戏取得的画面；它没有为我们认证新手赠虎已经发放、骑宠资格、岛名、具体NPC或任务身份。</p>'''+''.join(figures)+'''
<h2>文字日期与图片日期分开看</h2><p>官方栏目索引把文章标为2003-12-10；
本次核同的正文实际捕获为2005-11-17。页内JPEG捕获于2004-06-11，链接目标JPEG捕获于2006-10-22。
文件名sa1210不等于经过认证的图片创作日期，图像相似也不等于两份像素相同。</p>
<p>新手骑宠、课程、证明书和计划实施等旧文字结论仍按各自版本保存。本次新增的是这一处图像引用的实际字节与目视分类，不新增骑乘规则或任务奖励。</p>
<small>本包只保存原JPEG与来源摘要，不附整页原HTML，也不执行原页面脚本。原游戏世界仍未进入。</small></main></html>'''

class ViewerAudit(HTMLParser):
    def __init__(self):super().__init__();self.images=[];self.scripts=0;self.bad=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='script':self.scripts+=1
        if any(k.startswith('on')for k in a):self.bad.append('event attribute')
        if tag=='img':
            prefix='data:image/jpeg;base64,';need(a.get('src','').startswith(prefix),'inline-only JPEG resource')
            self.images.append(base64.b64decode(a['src'][len(prefix):],validate=True))
        elif any(k in a for k in ('src','href','action')):self.bad.append('external resource')

def audit_viewer(page,images):
    p=ViewerAudit();p.feed(page)
    need(p.images==images and len(images)==2,'exact ordered original JPEG bytes in viewer')
    need(p.scripts==0 and not p.bad,'no active or external source content')
    return dict(embedded_JPEG_bytes_equal_originals=True,original_resource_occurrences=2,scripts=0,external_requests_required=0,browser_executed=False)

def source_probe(source,out):
    from PIL import Image
    need(not out.exists() and ROOT not in out.resolve().parents,'new private output outside Git')
    page=(source/'plan-original.html').read_bytes();pin(page,PAGE_PIN);pair=link_pair(page.decode('big5'))
    http=json.loads((source/'page-receipt.json').read_bytes())
    need(http['requested']==http['resolved']==PAGE_URL and http['status']==200,'exact original page capture')
    receipts=json.loads((source/'image-receipts.json').read_bytes());need(len(receipts)==2,'two observed image responses')
    images=[];derived=[]
    for i,p in enumerate(IMAGE_PINS):
        path=source/ORIGINALS[i].rsplit('/',1)[1];raw=path.read_bytes();pin(raw,p[:2]);h=receipts[i]
        need(h['status']==200 and h['requested']=='https://web.archive.org/web/20051117143741id_/'+ORIGINALS[i] and h['content_type']=='image/jpeg','actual image HTTP response')
        stamp=capture(h['resolved'],ORIGINALS[i]);need(stamp==p[2],'actual image capture')
        sof=jpeg_shape(raw)
        with Image.open(path)as image:
            image.load();need(image.format=='JPEG' and list(image.size)==p[3] and image.mode=='RGB' and getattr(image,'n_frames',1)==1,'actual JPEG decoding')
            need(sof['size']==p[3] and sof['components']==3 and sof['precision']==8,'independent SOF/Pillow metadata')
            rgb=sha(image.tobytes());need(rgb==p[4],'actual decoded RGB')
        derived.append(dict(role='ANCHOR_TARGET'if i==0 else'INLINE_IMAGE',original_url=ORIGINALS[i],HTTP=h,capture_timestamp=stamp,
            bytes=len(raw),sha256=sha(raw),JPEG_SOF=sof,Pillow_RGB_sha256=rgb,frames=1,original_visually_reviewed=True))
        images.append(raw)
    r=dict(schema='stoneage.scene36.riding_image_reference.r1',
        scope='ARCHIVED_WAYI_OPERATOR_WEB_STATIC_DIALOGUE_IMAGE_NOT_RIDING_RUNTIME',
        existing_materials=parents(),original_page=dict(original_url=PAGE_ORIGINAL,HTTP=http,bytes=len(page),sha256=sha(page),
            index_date_as_written='2003-12-10',actual_page_capture='20051117143741'),
        linked_image_pair=pair,images=derived,
        visual_review=dict(kind='INDOOR_NPC_DIALOGUE_WINDOW_REFERENCE',
            visible_labels=['確定','取消'],full_dialogue_transcribed=False,indoor_scene_covered_by_translucent_dialogue=True,
            mount_presence_behind_dialogue='UNRESOLVED',exact_dialogue_or_button_pixel_coordinates_not_measured=True),
        source_delta=dict(new_riding_rules=0,previous_rules_or_plans_recounted_as_new=False,
            new_image_reference_pairs=1,new_image_resources=2,original_resources_are_two_independent_figures=False,
            old_unacquired_flags_preserved_as_capture_time_history=True),
        private_viewer_audit=audit_viewer(viewer(images),images),
        source_action_run_id=None,overall_percent=None,**{k:False for k in FALSE})
    out.mkdir(mode=0o700,parents=True);(out/'source').mkdir()
    (out/'reader.html').write_text(viewer(images),encoding='utf-8')
    for original,raw in zip(ORIGINALS,images):(out/'source'/original.rsplit('/',1)[1]).write_bytes(raw)
    (out/'source/acquisition.json').write_text(json.dumps(dict(page=http,images=receipts),indent=2)+'\n')
    (out/'source-report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    (out/'README.txt').write_text('解压后打开reader.html。本包保留两份原JPEG与来源摘要；整页原HTML不附在交付中，读者页不运行原页面脚本。此包不是原游戏执行。\n',encoding='utf-8')
    z=out/'SCENE36-private-Wayi-dialogue-image-reference.zip'
    with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED)as pack:
        for p in sorted(out.rglob('*')):
            if p.is_file() and p!=z:pack.write(p,p.relative_to(out).as_posix())
    return r,z

def validate(r):
    need(r['scope']=='ARCHIVED_WAYI_OPERATOR_WEB_STATIC_DIALOGUE_IMAGE_NOT_RIDING_RUNTIME','source scope')
    need(all(r[k]is False for k in FALSE),'static image cannot authenticate riding/deployment/runtime')
    need(r['existing_materials']==parents(),'five exact existing source reports')
    need((r['original_page']['bytes'],r['original_page']['sha256'])==PAGE_PIN and r['original_page']['actual_page_capture']=='20051117143741','known page identity')
    need(r['linked_image_pair']==dict(anchor_href=ORIGINALS[0],img_src=ORIGINALS[1]),'one anchor/inline pair')
    need(len(r['images'])==2,'two distinct original resources')
    for i,(im,p)in enumerate(zip(r['images'],IMAGE_PINS)):
        need(im['original_url']==ORIGINALS[i] and (im['bytes'],im['sha256'])==p[:2],'actual JPEG identity/order')
        need(capture(im['HTTP']['resolved'],im['original_url'])==im['capture_timestamp']==p[2],'resolved capture dates retained')
        need(im['JPEG_SOF']['size']==p[3] and im['Pillow_RGB_sha256']==p[4],'actual image dimensions/pixels')
    d=r['source_delta'];need((d['new_riding_rules'],d['new_image_reference_pairs'],d['new_image_resources'])==(0,1,2) and d['original_resources_are_two_independent_figures']is False,'one source reference, no duplicate rule discovery')
    need(d['old_unacquired_flags_preserved_as_capture_time_history']is True,'do not rewrite old capture-time flags')
    need(r['source_action_run_id']is None and r['overall_percent']is None,'no invented source Action/progress')
    need(sha(canonical(r))==FROZEN,'frozen actual image source result')
    return dict(image_reference_pairs=1,actual_image_resources=2,new_riding_rules=0,original_world_entered=False)

def validate_audit(a,r):
    need(a['source_report_sha256']==sha(REPORT.read_bytes()) and a['canonical_source_report_sha256']==sha(canonical(r)),'actual audit/report binding')
    need(a['private_original_bytes']==135852 and a['private_original_objects']==2 and a['ZIP_CRC_and_original_SHA_verified']is True,'actual private source membership')
    need(a['full_original_article_HTML_in_deliverable']is False,'image and source summary only in deliverable')
    need(a['private_package_saved']is True and a['local_identity_applied']is True and a['save_readback_performed']is False,'save acknowledgement boundary')
    need(a['browser_or_game_execution_performed']is False and a['raw_originals_in_Git']is False,'actual static audit scope')
    need(sha(canonical(a))==AUDIT_FROZEN,'frozen private image audit')

def main():
    p=argparse.ArgumentParser();p.add_argument('--private-source',type=Path);p.add_argument('--private-output',type=Path);a=p.parse_args()
    if a.private_source:
        need(a.private_output is not None,'private output required');r,z=source_probe(a.private_source,a.private_output)
        print(json.dumps(dict(canonical_report_sha256=sha(canonical(r)),private_package=str(z),bytes=z.stat().st_size,sha256=sha(z.read_bytes()))))
    else:
        r=json.loads(REPORT.read_bytes());result=validate(r);validate_audit(json.loads(AUDIT.read_bytes()),r);print(json.dumps(result))

if __name__=='__main__':main()
