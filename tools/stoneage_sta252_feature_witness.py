"""Versioned STA2.52 user-review facts; requests and hearsay are not shipped features."""
import argparse,hashlib,json,re,urllib.request
from pathlib import Path
from tools.stoneage_early_content_probe import plain,require
URL='https://news.17173.com/z/stoneage/content/2002-3-10/n974_891060.html'
FEATURES=[
 ('reduced_window_cooking','REPORTED_AVAILABLE_UNSTABLE','缩屏料理','Cooking scripts reportedly stall on slower machines.'),
 ('reduced_window_leveling','REPORTED_AVAILABLE_UNSTABLE','缩屏练功','Reviewer reports disconnections with small encounters.'),
 ('automatic_script_resume','REQUESTED_NOT_VERIFIED_AVAILABLE','自动恢复脚本','Requested improvement; do not count as implemented.'),
 ('automatic_window_mode_switch','REQUESTED_NOT_VERIFIED_AVAILABLE','增加这个功能自动缩屏','Requested improvement; manual switching is only a workaround.'),
 ('special_character_action_conditions','MENU_PRESENT_BEHAVIOR_UNVERIFIED','人物动作特殊条件设定','Reviewer could not verify a behavioral change.'),
 ('two_step_movement','REPORTED_AVAILABLE_LIMITED','二步顺移','Historical movement modification, limited utility as reported.'),
 ('map_deletion_movement','MENTIONED_COMPARATOR_NOT_252_ADDITION','删图顺移','Comparison only; first introduction and validity remain unknown.'),
 ('delay_pacing','REPORTED_WORKAROUND','开延时','Pacing suggestion, not proof of a newly introduced feature.'),
 ('speed_ratio','HEARSAY_NOT_MEASURED','不知道是不是真的','Unverified numerical speed claim; no measured multiplier retained.'),
]

def derive(doc):
 for ident,token in [('newsriqi','2002-03-10'),('zhuozhe_left','☆阿仇☆')]:
  m=re.search(r'<div\s+id=["\x27]'+ident+r'["\x27][^>]*>(.*?)</div>',doc,re.I|re.S)
  require(m is not None and token in plain(m[1]),'publication header '+ident)
 s=plain(doc);a=s.find('天使的外挂');b=s.find('本文言论',a);require(0<=a<b,'review body');body=s[a:b]
 require('sta2.52'in body.lower(),'exact software version')
 rows=[]
 for ident,status,marker,summary in FEATURES:
  require(marker in body,'missing claim '+ident)
  rows.append({'feature_id':ident,'evidence_status':status,'summary':summary,'implemented_in_rebuild':False,'adoption_decided':False})
 return {'schema':'stoneage.legacy_tool.version_features.r1','family':'STA','claimed_version':'2.52',
  'source_role':'CONTEMPORANEOUS_USER_REVIEW_NOT_DEVELOPER_CHANGELOG','asserted_publication_date':'2002-03-10','author':'☆阿仇☆',
  'version_release_date_verified':None,'first_introduction_of_each_feature_verified':False,
  'official_client_compatibility_verified':False,'current_html_authenticated_in_2002':False,
  'review_body_normalized_sha256':hashlib.sha256(re.sub(r'\s+','',body).encode()).hexdigest(),
  'features':rows,'all_STA252_features_recovered':False,'software_executed':False,
  'new_game_assistant_started':False}

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 with urllib.request.urlopen(urllib.request.Request(URL,headers={'User-Agent':'StoneAgeHistoricalResearch/1.0'}),timeout=35)as r:
  raw=r.read(2_000_001);final=r.url
 require(0<len(raw)<=2_000_000 and final==URL,'source size/origin')
 doc=raw.decode('utf-8',errors='replace');out=derive(doc);out['source']={'url':URL,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'codec':'utf-8','replacement_characters':doc.count('\ufffd')};a.output.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True)+'\n')
 print(json.dumps({'version':out['claimed_version'],'features':len(out['features'])}))
if __name__=='__main__':main()
