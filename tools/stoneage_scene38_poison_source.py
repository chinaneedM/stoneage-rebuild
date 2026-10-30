"""One existing CN2.0 page row receives a dated documentary source contract."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'research/recovered/STONEAGE-SCENE38-POISON-SKILL-SOURCE-R1.json'
ENTRY = 'https://web.archive.org/web/20011204213609id_/http://www.waei.com.cn/ZHUANQU/stoneage2/sw/facility.asp'
URL = 'https://web.archive.org/web/20011204201517id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/skill.asp'
HREF = '/ZHUANQU/stoneage2/pet/skill.asp'
PINS = {'facility':(73356,'e18f0bced4935358e3be28e328d50a49a6dfbb8c26476a98c211892974e7ba16'),
        'skill':(78022,'3056d727903c56000cdfcd877924efa244967eb8b6407db08c08e60ec7a9b0ee')}
REPORT_SHA = 'c7f1cb772cb72e24140788a0531d088a3afc6673b7939158df02d8f9162c3193'


def need(test, message):
    if not test: raise ValueError(message)


def sha(raw): return hashlib.sha256(raw).hexdigest()
def canon(value): return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def clean(text): return ''.join(text.split())


class Tables(HTMLParser):
    """Track table identity so a navigation row cannot donate a price or heading."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[];self.tables=[];self.hidden=0

    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.hidden+=1
        if self.hidden:return
        if tag=='table':self.stack.append({'rows':[],'row':None,'cell':None})
        if not self.stack:return
        t=self.stack[-1]
        if tag=='tr':
            need(t['row'] is None,'nested unclosed row');t['row']=[]
        if tag in ('td','th'):
            need(t['row'] is not None and t['cell'] is None,'nested or orphan cell');t['cell']=[]

    def handle_endtag(self, tag):
        if tag in ('script','style'):
            self.hidden-=1;need(self.hidden>=0,'hidden element mismatch');return
        if self.hidden or not self.stack:return
        t=self.stack[-1]
        if tag in ('td','th'):
            need(t['cell'] is not None,'orphan cell end')
            t['row'].append(clean(''.join(t['cell'])));t['cell']=None
        if tag=='tr':
            need(t['row'] is not None and t['cell'] is None,'unclosed source cell')
            t['rows'].append(t['row']);t['row']=None
        if tag=='table':
            need(t['row'] is None and t['cell'] is None,'unclosed source row')
            self.tables.append(self.stack.pop()['rows'])

    def handle_data(self, text):
        if not self.hidden and self.stack and self.stack[-1]['cell'] is not None:
            self.stack[-1]['cell'].append(text)


class Links(HTMLParser):
    def __init__(self):super().__init__();self.href=None;self.parts=[];self.links=[]
    def handle_starttag(self,t,a):
        if t=='a':self.href=dict(a).get('href');self.parts=[]
    def handle_data(self,s):
        if self.href:self.parts.append(s)
    def handle_endtag(self,t):
        if t=='a' and self.href:self.links.append((clean(''.join(self.parts)),self.href));self.href=None


def extract_entry(raw):
    h=raw.decode('gb18030',errors='strict');need('\ufffd' not in h,'replacement character')
    p=Links();p.feed(h)
    matches=[u for label,u in p.links if label=='宠物技能']
    need(matches==[HREF],'one real skill route')
    return {'label':'宠物技能','href':matches[0]}


def extract_skill(raw):
    h=raw.decode('gb18030',errors='strict');need('\ufffd' not in h,'replacement character')
    need(re.search(r'<title>\s*石器时代2\.0\s*</title>',h,re.I),'edition label')
    need(h.count('技能名称')==1,'one literal header location')
    begin=h.lower().rfind('<table',0,h.index('技能名称'))
    end=h.lower().find('</table>',begin)
    need(begin>=0 and end>begin,'bounded skill table')
    table=h[begin:end+8]
    need(table.lower().count('<table')==1,'no nested skill table')
    # Legacy nonselected rows have unclosed cells. Do not repair or validate them.
    raw_rows=re.findall(r'<tr\b[^>]*>.*?</tr>',table,re.I|re.S)
    headings=[row for row in raw_rows if '技能名称' in row]
    targets=[row for row in raw_rows if '猛毒攻击' in row]
    need(len(headings)==len(targets)==1 and table.index(headings[0])<table.index(targets[0]),'one in-table header and target')
    p=Tables();p.feed('<table>'+headings[0]+targets[0]+'</table>')
    need(not p.stack and p.hidden==0,'complete selected header and target rows')
    header=['技能名称','技能说明','技能价格']
    tables=[t for t in p.tables if header in t]
    need(len(tables)==1 and tables[0].count(header)==1,'one ordered skill header')
    rows=[r for r in tables[0] if r and r[0]=='猛毒攻击']
    need(len(rows)==1 and len(rows[0])==3,'one full target row')
    row=rows[0]
    m=re.fullmatch(r'攻击力降低([0-9]+)%[，,]造成敌方([0-9]+)回合中毒状态',row[1])
    need(m is not None and row[2].isascii() and row[2].isdigit(),'literal numeric wording and price cell')
    reduction,turns=int(m[1]),int(m[2]);need(0<=reduction<=100 and turns>0,'bounded documentary percentages and turns')
    return {'name_as_written':row[0],'attack_reduction_percent_as_text':reduction,
            'poison_turns_as_text':turns,'listed_price':int(row[2]),
            'header_verified':header,'normalized_row_sha256':sha(canon(row)),
            'original_selected_header_and_row_sha256':sha((headings[0]+targets[0]).encode('utf-8')),
            'price_currency':None,'trainer_location':None,'native_skill_id':None,
            'price_is_actual_training_debit_proven':False,'damage_tick_formula':None}


def source_projection(raws):
    for key,(size,digest) in PINS.items():
        need(len(raws[key])==size and sha(raws[key])==digest,'exact preserved source bytes: '+key)
    return {'entry':extract_entry(raws['facility']),'skill':extract_skill(raws['skill'])}


def validate(r):
    need(r['schema']=='stoneage.scene38.poison_skill_source.r1','schema')
    need(len(r['prior_materials'])==6,'all prior qualification inputs')
    for pin in r['prior_materials']:
        b=(ROOT/pin['path']).read_bytes()
        need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'prior source byte identity')
    need(r['source_projection']['entry']=={'label':'宠物技能','href':HREF},'real route')
    x=r['source_projection']['skill']
    need((x['attack_reduction_percent_as_text'],x['poison_turns_as_text'],x['listed_price'])==(50,5,4000),'dated row facts')
    need(x['price_currency'] is None and x['trainer_location'] is None and x['native_skill_id'] is None,'unknown price unit/location/ID')
    need(x['price_is_actual_training_debit_proven'] is False and x['damage_tick_formula'] is None,'no runtime formula')
    need(r['novelty']=={'new_webpages_discovered':0,'new_skill_names':0,'new_dated_row_attribution_contracts':1,'new_training_predicates':0,'previous_page_recounted_as_new_source':False},'novelty boundary')
    need(all(v is False for v in r['unproven'].values()),'historical promotion')
    need(r['overall_percent'] is None,'no completion percentage')
    need(sha(canon(r))==REPORT_SHA,'immutable dated attribution and unresolved comparisons')
    return {'dated_row_contracts':1,'new_webpages':0,'original_world_entered':False}


def fetch(url):
    with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0 StoneAgeHistoricalEvidence'}),timeout=40) as h:
        b=h.read(200001);need(h.status==200 and h.url==url and len(b)<=200000,'HTTP status/redirect/size')
        return b,{'requested':url,'resolved':h.url,'status':h.status,'bytes':len(b),'sha256':sha(b)}


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-dir');p.add_argument('--replay-live',action='store_true');p.add_argument('--output');a=p.parse_args()
    r=json.loads(REPORT.read_bytes());result=validate(r)
    if a.source_dir or a.replay_live:
        need(not(a.source_dir and a.replay_live),'one source mode')
        if a.source_dir:
            raws={k:(Path(a.source_dir)/(k+'.html')).read_bytes() for k in PINS};receipts=None
        else:
            pairs=[fetch(u) for u in (ENTRY,URL)];raws=dict(zip(PINS,[x[0] for x in pairs]));receipts=dict(zip(PINS,[x[1] for x in pairs]))
        projection=source_projection(raws);need(projection==r['source_projection'],'source semantics changed')
        result={'source_projection':projection,'HTTP':receipts,'original_HTML_or_assets_in_artifact':False,'original_server_executed':False,'original_world_entered':False}
    if a.output:Path(a.output).write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result if not a.output else {'derived_replay_written':True,'original_world_entered':False}))


if __name__=='__main__':main()
