"""Finite source-local shell-delivery witnesses; no article text retained."""
from __future__ import annotations
import argparse,hashlib,json,re,urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tools.stoneage_early_content_probe import plain,require
SOURCES={
 'compilation':('https://games.sina.com.cn/handbook/0101/01186091_c2.shtml','gb18030'),
 'december_player':('https://news.17173.com/z/stoneage/content/2001-12-10/n281_197533.html?_platform=PC','utf-8'),
 'later_delivery':('https://games.sina.com.cn/zhqu/sta/rwgl1_1.shtml','gb18030'),
}

def selected(text,start,end):
 a=text.find(start);require(a>=0,'missing source marker '+start);b=text.find(end,a+len(start));require(b>a,'missing section end '+end)
 s=text[a:b];require('\ufffd'not in s,'selected source decoding damage');return s

def derive(docs):
 p={k:plain(v)for k,v in docs.items()}
 base=p['compilation']
 require(all(t in base for t in ['弥生','日美子','仙尼亚的花','扣两点魅力']),'compilation witness')
 news=selected(p['december_player'],'1、北岛送贝壳任务','2、南岛')
 require(all(t in news for t in ['弥生','日美子','不可思议的贝壳']),'player shell witness')
 # Only the original publication date/byline elements qualify this field.
 for ident,token in [('newsriqi','2001-12-10'),('zhuozhe_left','诗雨')]:
  m=re.search(r'<div\s+id=["\x27]'+ident+r'["\x27][^>]*>(.*?)</div>',docs['december_player'],re.I|re.S)
  require(m is not None and token in plain(m[1]),'article header '+ident)
 coords=re.findall(r'[\[［]\s*(\d+)\s*[，,]\s*(\d+)\s*[\]］]',news)
 require(coords==[('114','662'),('637','491')],'published coordinate context')
 later=p['later_delivery'];require(all(t in later for t in ['2003-05-29','友谊（一）','友谊（二）','扣魅力一点']),'later direction/repeat witness')
 return {'profiles':{
  'compilation':{'source_role':'EARLY_COMPILATION_CURRENT_TEXT_NOT_JANUARY_AUTHENTICATED','flow':['YAYOI_GIVES_SHELL','HIMIKO_RECEIVES','FLOWER_REWARD'],'reported_drop_charm_delta':-2,'exact_server_build':None},
  'december_player':{'source_role':'CONTEMPORANEOUS_PLAYER_ARTICLE_DATE_ASSERTED','asserted_publication_date':'2001-12-10','author':'诗雨','reported_npc_location_references':[{'query_role':'YAYOI','place_label':'玛丽娜斯','coordinates':[114,662]},{'query_role':'HIMIKO','place_label':'萨姆吉尔','coordinates':[637,491]}], 'coordinate_namespace':'UNAUTHENTICATED_MAP_REFERENCE_NOT_A_SPAWN_TILE','reported_use':'SHELL_ACQUISITION_PATH','shell_is_final_reward_rather_than_intermediate_verified':False,'reported_reward_item_id':None},
  'later_delivery':{'source_role':'LATER_PUBLISHED_GUIDE_2003','asserted_publication_date':'2003-05-29','both_delivery_directions_reported':True,'repeat_charm_delta':-1,'repeat_penalty_is_discard_penalty':False}},
  'selected_december_section_sha256':hashlib.sha256(re.sub(r'\s+','',news).encode()).hexdigest(),
  'current_html_authenticated_in_2001':False,'independent_rule_origins_authenticated':False,
  'shell_and_flower_relationship':'KEEP_INTERMEDIATE_OBJECT_AND_FINAL_REWARD_SEPARATE; source1 discusses delivery completion, source2 lists acquisition routes',
  'same_names_prove_same_server_objects':False,'original_item_or_npc_ids':None,'original_server_executed':False,'tw10_membership_verified':False}

def fetch(key):
 url,codec=SOURCES[key]
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'StoneAgeHistoricalResearch/1.0'}),timeout=35)as r:
  b=r.read(2_000_001);final=r.url
 require(0<len(b)<=2_000_000,'source size')
 return key,(b,final)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 with ThreadPoolExecutor(max_workers=3)as pool:acq=dict(pool.map(fetch,SOURCES))
 docs={};meta={}
 for k,(b,u)in acq.items():
  docs[k]=b.decode(SOURCES[k][1],errors='replace');meta[k]={'requested_url':SOURCES[k][0],'final_url':u,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'codec':SOURCES[k][1],'replacement_characters':docs[k].count('\ufffd')}
 r={'schema':'stoneage.shell_delivery.witnesses.r1','sources':meta,'observations':derive(docs),'source_articles_or_raw_text_retained':False}
 a.output.write_text(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n');print(json.dumps({'sources':len(meta),'observations':r['observations']},ensure_ascii=False))
if __name__=='__main__':main()
