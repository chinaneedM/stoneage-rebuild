"""Replay a bounded Sina SACH-MX edition comparison and two linked UI images."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen
from .stoneage_cn2003_katan_visual_r100 import Tables, compact

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'research/recovered/STONEAGE-SACHMX-VERSION-VISUAL-SOURCE-R103.json'
SOURCE_SHA = '5ea71a0338fb4bfb0a6b3c2d6d47313d4c9238c91a52d913413e81b0f744f2f2'
LABELS = ['外挂名称','目前版本','制作者（组）','服务器端','使用费用','付费方式','更新速度','作弊功能','辅助功能','测试评价']
COMMON_ABUSE = [('game_speed','游戏加速'),('movement_speed','快速走路'),
                ('wall_bypass','穿墙行走'),('encounter_speed','快速遇敌')]
COMMON_HELP = [('automatic_login','自动登入'),('task_scripts','任务脚本'),
               ('task_secret_text','任务秘语'),('information_display','情报显示(各类石器资料均有)')]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',',':')).encode()

def pin(raw):
    return {'bytes':len(raw),'sha256':digest(raw),
            'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}

class Links(Tables):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.active=None
    def handle_starttag(self,tag,attrs):
        super().handle_starttag(tag,attrs)
        if tag=='a' and not self.hidden_tags:
            self.active={'href':dict(attrs).get('href'),'text':''}
            self.links.append(self.active)
    def handle_endtag(self,tag):
        hidden=bool(self.hidden_tags)
        super().handle_endtag(tag)
        if tag=='a' and not hidden:
            self.active=None
    def handle_data(self,data):
        super().handle_data(data)
        if not self.hidden_tags and self.active is not None:
            self.active['text']+=data

def extract(raw):
    parser=Links()
    parser.feed(raw.decode('gb18030',errors='strict'))
    return parser

def table_rows(parser):
    candidates=[]
    for rows in parser.tables:
        if rows and any(compact(c['text'])=='【外挂名称】' for c in rows[0]):
            candidates.append(rows)
    require(len(candidates)==1, 'Missing or ambiguous product table')
    rows=candidates[0]
    require(len(rows)==10, 'Product table row count changed')
    fields={}
    for i,(label,row) in enumerate(zip(LABELS,rows)):
        texts=[compact(c['text']) for c in row]
        marker='【'+label+'】'
        if i==0:
            require(len(row)==3 and texts[0]=='' and texts[1]==marker, 'Image/product row changed')
            value=texts[2]
        elif i<7:
            require(len(row)==2 and texts[0]==marker, 'Metadata row changed')
            value=texts[1]
        else:
            require(len(row)==1 and texts[0].startswith(marker), 'Feature/review cell changed')
            value=texts[0][len(marker):]
        require(label not in fields, 'Duplicate table label')
        fields[label]=value
    return fields,rows

def numbered(value, expected, suffix=''):
    parts=re.split(r'(\d+)\.',value)
    require(parts[0]=='' and len(parts)==1+2*len(expected), 'Feature list shape changed')
    actual=[]
    for i,((code,text),num,body) in enumerate(zip(expected,parts[1::2],parts[2::2])):
        require(num==str(i+1) and body==text+(suffix if i==len(expected)-1 else ''),
                'Explicit feature meaning/order changed')
        actual.append(code)
    return actual

def parse_article(raw, source, enforce_fingerprint=True):
    p=extract(raw)
    values,rows=table_rows(p)
    expected=source['metadata']
    require(all(values[k]==compact(v) for k,v in expected.items()), 'Edition metadata changed')
    header=[]
    for table in p.tables:
        for row in table:
            if len(row)==3 and compact(row[0]['text']).startswith('作者：'):
                header.append([compact(row[0]['text']),compact(row[1]['text'])])
    require(header==[[compact('作者：'+source['author']),compact(source['display_date'])]],
            'Author/date attribution changed')
    visible=compact(''.join(p.text))
    require(source['title'] in visible, 'Title changed')
    abuse=COMMON_ABUSE
    help_features=COMMON_HELP
    if source['edition']=='member':
        abuse=[('unrestricted_level_claim','不限等')]+abuse
        help_features=help_features+[('delivery_currency_script','自动送货赚石币脚本')]
    suffix='' if source['edition']=='member' else '等等的辅助功能与收费的SACH-MX会员版里的功能大致相同'
    result={'explicit_abuse_categories':numbered(values['作弊功能'],abuse),
            'explicit_assistance_categories':numbered(values['辅助功能'],help_features,suffix)}
    # This is a review claim. Hash it without copying its prose into a public catalog.
    require(digest(values['测试评价'].encode())==source['review_sha256'], 'Review claim changed')
    image=source['image']
    require(rows[0][0]['images']==[{'href':image['original_href'],'src':image['thumbnail']}],
            'Linked full image/thumbnail association changed')
    fingerprint=digest(canonical(values))
    if enforce_fingerprint:
        require(fingerprint==source['table_sha256'], 'Table fingerprint changed')
    result.update(table_sha256=fingerprint,full_image_url=image['url'],
                  review_is_benchmark=False,edition_feature_list_complete=False)
    return result

def parse_index(raw, contract):
    p=extract(raw)
    visible=compact(''.join(p.text))
    require('不提供外挂下载并且在截图资料中隐去了外挂网址' in visible,
            'Missing editorial URL-redaction/no-download policy')
    for source in contract['articles']:
        matches=[l for l in p.links if l['href']==source['original_url']]
        require(len(matches)==1 and compact(matches[0]['text'])==source['index_label'],
                'Index edition link/label changed')
    return {'both_edition_links_verified':True,'editorial_helper_urls_redacted':True,
            'developer_homepage_obtained':False,'binary_download_performed':False}

def decode_image(raw, expected):
    from PIL import Image
    require(len(raw)==expected['bytes'] and digest(raw)==expected['sha256'], 'Image bytes changed')
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        facts={'format':im.format,'mode':im.mode,'size':list(im.size),'frames':getattr(im,'n_frames',1)}
    require(all(facts[k]==expected[k] for k in facts), 'Image decode changed')
    return facts

def validate_source(contract):
    raw=SOURCE.read_bytes()
    require(digest(raw)==SOURCE_SHA and contract==json.loads(raw), 'Source contract changed')
    for path,expected in contract['parents'].items():
        require(pin((ROOT/path).read_bytes())==expected, 'Parent provenance changed')
    return contract

def replay(inputs, contract):
    validate_source(contract)
    require(set(inputs)=={'index','member_html','free_html','member_image','free_image'}, 'Five bounded inputs required')
    parsed_index=parse_index(inputs['index'],contract)
    articles=[]
    actual={}
    initial={'index':contract['index']}
    for source in contract['articles']:
        key=source['edition']
        article=parse_article(inputs[key+'_html'],source)
        image=decode_image(inputs[key+'_image'],source['image'])
        articles.append({'edition':key,**article,'decoded_image':image})
        initial[key+'_html']=source
        initial[key+'_image']=source['image']
    for key,raw in sorted(inputs.items()):
        initial_pin=initial[key]
        actual[key]={'bytes':len(raw),'sha256':digest(raw),
                     'equals_initial':len(raw)==initial_pin['bytes'] and digest(raw)==initial_pin['sha256']}
    return {'schema':'stoneage.sachmx.version_visual_replay.r103','contract_sha256':SOURCE_SHA,
            'actual_inputs':actual,'index':parsed_index,'articles':articles,
            'comparison':contract['comparison'],'records':contract['records'],
            'visual_observations':contract['visual_observations'],'boundaries':contract['boundaries']}

def download(url):
    with urlopen(Request(url,headers={'User-Agent':'StoneAgeResearch/1.0'}),timeout=35) as r:
        require(r.status==200 and r.url==url, 'Unexpected HTTP status/redirect')
        return r.read()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input-dir',type=Path)
    p.add_argument('--write',type=Path,required=True)
    args=p.parse_args()
    contract=validate_source(json.loads(SOURCE.read_text()))
    urls={'index':contract['index']['url']}
    for s in contract['articles']:
        urls[s['edition']+'_html']=s['url'];urls[s['edition']+'_image']=s['image']['url']
    inputs={k:(args.input_dir/(k+'.bin')).read_bytes() if args.input_dir else download(u) for k,u in urls.items()}
    report=replay(inputs,contract)
    args.write.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'inputs':report['actual_inputs'],'records':len(report['records']),
                      'semantics':'EDITION_LISTINGS_AND_STATIC_UI_NOT_EXECUTION'},sort_keys=True))

if __name__=='__main__':
    main()
