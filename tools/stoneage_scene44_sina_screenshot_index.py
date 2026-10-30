"""SCENE44 one-page screenshot link census: provenance, not observed game footage.

One fetch of preexisting public 2003-labelled Sina player screenshot index.
No screenshot files or proprietary images are downloaded at this step.
"""
from __future__ import annotations
import argparse
import hashlib
from html.parser import HTMLParser
import json
import re
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urljoin,urlsplit

ROOT=Path(__file__).resolve().parents[1]
URL="https://games.sina.com.cn/zhqu/sta/ltxs/ltxs_1.shtml"
TARGETS=("6.0新手村","6.0登陆画面","1.82时的机暴")
FROZEN=ROOT/"research/recovered/STONEAGE-SCENE44-SINA-GAMEPLAY-SCREENSHOT-INDEX-R1.json"
MAX_HTML=200000

def must(condition,message):
    if not condition:raise ValueError(message)
def squish(s):return "".join(s.split())

class AnchorReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.anchors=[];self.current=None;self.visible=[];self.hidden=0
    def handle_starttag(self,t,attrs):
        d=dict(attrs)
        if t in ("script","style"):self.hidden+=1
        if self.hidden:return
        if t=="a" and self.current is None:
            self.current={"href":d.get("href"),"text":"","images":[]}
            self.anchors.append(self.current)
        elif t=="img" and self.current is not None:
            self.current["images"].append(d.get("src"))
    def handle_endtag(self,t):
        if t in ("script","style"):
            self.hidden=max(0,self.hidden-1);return
        if t=="a":self.current=None
    def handle_data(self,d):
        if self.hidden:return
        self.visible.append(d)
        if self.current is not None:self.current["text"]+=d

def decode_source(raw):
    candidates=[]
    for enc in ("gb18030","utf-8"):
        try:source=raw.decode(enc,"strict")
        except UnicodeError:continue
        p=AnchorReader();p.feed(source)
        v=squish(" ".join(p.visible))
        if "石器截图" in v and "新浪游戏" in v and "2003-04-0519:35" in v and all(z in v for z in TARGETS):
            candidates.append((enc,p,v))
    must(len(candidates)==1,"source bytes/encoding/byline/title qualification ambiguous")
    return candidates[0]

def inspect(raw,url=URL):
    must(url==URL,"redirected away from specified historical index")
    must(5000<len(raw)<=MAX_HTML,"unqualified page payload")
    enc,p,v=decode_source(raw)
    matches=[]
    for label in TARGETS:
        hits=[a for a in p.anchors if squish(a["text"])==label]
        matches.append({"label":label,"exact_anchor_match_count":len(hits),
                        "anchors":[{"href_literal":h["href"],"resolved_url":urljoin(URL,h["href"] or ""),
                                    "inline_image_src":h["images"]} for h in hits]})
    archive_date_not_image_date=True
    return {"schema":"stoneage.scene44.sina_gameplay_screenshot_index.discovery.r1",
       "page_url":URL,"requested_url":URL,"final_url":url,"source_bytes":len(raw),
       "source_sha256":hashlib.sha256(raw).hexdigest(),"source_charset":enc,
       "display_date_label":"2003-04-05 19:35","publisher_label":"新浪游戏",
       "original_2003_publication_bytes_authenticated":False,"individual_screenshot_capture_date_authenticated":False,
       "same_version_as_original_tw1_or_jss1999_proven":False,
       "source_grade":"CURRENT_PUBLIC_SINA_PLAYER_SUBMITTED_SCREENSHOT_INDEX",
       "selected_labels":matches,
       "all_target_labels_in_visible_original_html":True,
       "original_screenshot_image_bytes_downloaded":False,
       "original_client_executed_this_round":False,
       "original_game_world_entered":False,
       "no_original_html_or_images_in_public_git":True,
       "next":"QUALIFY_EXACT_SELECTED_SCREENSHOT_DETAIL_LINKS_AND_ONE_ACTUAL_IMAGE_OR_STOP"}

def fetch():
    req=Request(URL,headers={"User-Agent":"Mozilla/5.0","Accept-Encoding":"identity"})
    with urlopen(req,timeout=30) as r:
        raw=r.read(MAX_HTML+1)
        must(r.status==200,"HTTP status not 200")
        return raw,r.url

def main():
    p=argparse.ArgumentParser();p.add_argument("--source-live",action="store_true");p.add_argument("--write")
    a=p.parse_args()
    if not a.source_live:
        if FROZEN.exists():
            d=json.loads(FROZEN.read_text(encoding="utf-8"))
            must(d["source_bytes"]>5000 and len(d["selected_labels"])==3,"frozen source qualification changed")
            must(not d["original_screenshot_image_bytes_downloaded"] and not d["original_game_world_entered"],"evidence promotion")
        print("SCENE44_SCREENSHOT_SOURCE_OFFLINE_BOUNDARY_PASS")
        return
    raw,url=fetch();d=inspect(raw,url)
    data=json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if FROZEN.exists():must(data==FROZEN.read_text(encoding="utf-8"),"current page differs from archived report")
    if a.write:Path(a.write).write_text(data,encoding="utf-8")
    print("SCENE44_SOURCE",json.dumps({"bytes":d["source_bytes"],"sha256":d["source_sha256"],
       "encoding":d["source_charset"],"match_counts":{r["label"]:r["exact_anchor_match_count"] for r in d["selected_labels"]},
       "anchors":{r["label"]:[a["resolved_url"] for a in r["anchors"]] for r in d["selected_labels"]}},ensure_ascii=False))
if __name__=="__main__":main()
