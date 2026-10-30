"""SCENE41: one currently retrievable, 2001-dated player FAQ -> pinned TW1 BGM filenames.

The article supplies player assertions, NOT original executable event->track selectors.
No original copyrighted HTML or WAV is retained or shipped.
"""
from __future__ import annotations
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.request
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
DATASET=ROOT/"research/recovered/STONEAGE-TW10-AUDIO-DATASET-R1.txt"
DATASET_BLOB="094becbc92397ee8abf72a014deffffabc97a316"
EXE_REPORT=ROOT/"research/recovered/STONEAGE-TW10-AUDIO-EVENT-GATE-R1.json"
EXE_REPORT_BLOB="67cc3707d45b6f079432b1db29b043851571b518"
SOURCE_URL="https://news.17173.com/z/stoneage/content/2001-6-14/n775_691475.html"
EXPECTED_NAMES=("sabgm_b0","sabgm_b1","sabgm_d0","sabgm_d1","sabgm_d2","sabgm_f0","sabgm_f1","sabgm_s0","sabgm_s1","sabgm_t0","sabgm_t1")
DESCRIPTORS=("战斗画面音乐","魔王战斗音乐","洞窟内音乐 1","洞窟内音乐 2","洞窟内音乐 3","原野行走音乐 1","原野行走音乐 2","战斗胜利音乐","登入选项音乐","城镇音乐 1","城镇音乐 2")

def gitblob(b:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

class ExtractText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text=[]
    def handle_data(self,data):
        self.text.append(data)
    def handle_entityref(self,name):
        raise ValueError("entity parser inconsistency")

def original_names():
    raw=DATASET.read_bytes()
    assert gitblob(raw)==DATASET_BLOB,"original audio manifest blob drift"
    rows=[line.split("|") for line in raw.decode("utf-8").splitlines() if line.startswith("BGM|")]
    names=[]
    for row in rows:
        d=dict(v.split("=",1) for v in row[1:] if "=" in v)
        assert d["path"]=="StoneAge/data/bgm/"+d["name"]
        assert re.fullmatch(r"sabgm_[bdfst][0-9]+\.wav",d["name"])
        names.append(d["name"].removesuffix(".wav"))
    assert len(names)==11 and len(set(names))==11
    assert set(names)==set(EXPECTED_NAMES)
    obj=EXE_REPORT.read_bytes()
    assert gitblob(obj)==EXE_REPORT_BLOB,"compiled audio gate report drift"
    p=json.loads(obj)
    assert p["compiled_audio_api_callsite_audit"]["exact_playback_call_argument_values_observed"] is False
    assert p["original_audio_event_to_track_binding_certified"] is False
    return names

def parse_page(raw:bytes, final_url:str):
    u=urlsplit(final_url)
    orig=urlsplit(SOURCE_URL)
    assert (u.scheme,u.hostname,u.path)==(orig.scheme,orig.hostname,orig.path),"unqualified destination"
    assert u.query in ("","_platform=PC"),"unverified query variant"
    assert 2000<len(raw)<500000,"source payload bounds"
    start_phrase="我可以更改石器时代的音乐吗"
    end_phrase="在北岛守桥的愿藏很烦"
    candidates=[]
    for charset in ("utf-8","gb18030"):
        decoded=raw.decode(charset,"surrogateescape")
        p=ExtractText();p.feed(decoded)
        text=re.sub(r"\s+"," "," ".join(p.text))
        if (text.count(start_phrase)==1 and text.count(end_phrase)==1
            and "作者：未知" in text and "2001-06-14" in text
            and "石器时代之全问答集" in text):
            candidates.append((charset,decoded,text))
    assert len(candidates)==1,"source encoding/content not unambiguously qualified"
    charset,decoded,t=candidates[0]
    invalid=sum(0xDC80<=ord(c)<=0xDCFF for c in decoded)
    assert invalid<=512,"too many invalid source bytes"
    start=t.index(start_phrase)
    end=t.index(end_phrase,start)
    section=t[start:end]
    assert not any(0xDC80<=ord(c)<=0xDCFF for c in section),"bad byte within music FAQ"
    matches=list(re.finditer(r"(?<![A-Za-z0-9_])sabgm_[bdfst][0-9]+(?![A-Za-z0-9_])",section,re.I))
    keys=[x.group().lower() for x in matches]
    assert tuple(keys)==EXPECTED_NAMES,("wrong ordered set",keys)
    rows=[]
    for i,m in enumerate(matches):
        field=section[m.end():(matches[i+1].start() if i+1<len(matches) else len(section))]
        label=re.sub(r"\s+"," ",field).strip()
        # The labels are prose descriptions, not verified original software event calls.
        want=DESCRIPTORS[i]
        assert label==want,("wrong original player label",keys[i],label,want)
        rows.append({"basename":keys[i],"file_name":keys[i]+".wav","faq_player_label":label,"tw10_audio_file_name_exactly_present":True,
                     "historical_bgm_event_traced":False,"source_grade":"CONTEMPORARY_LABELLED_PLAYER_FAQ"})
    return {"schema":"stoneage.scene41.2001_player_bgm_filename_claims.r1",
        "requested_url":SOURCE_URL,"resolved_url":final_url,"current_http_bytes":len(raw),
        "current_http_sha256":hashlib.sha256(raw).hexdigest(),"original_bytes_invalid_decoding":invalid,"selected_decoding":charset,
        "source_title_as_rendered":"石器时代之全问答集","source_date_label":"2001-06-14","source_author_label":"未知",
        "historical_published_bytes_authentic":False,"original_article_first_publication_time_verified":False,
        "source_scope":"CURRENTLY_RETRIEVED_17173_PLAYER_FAQ_WITH_2001_DATE_LABEL",
        "tw10_audio_manifest_git_blob":DATASET_BLOB,
        "tw10_original_exe_audio_gate_git_blob":EXE_REPORT_BLOB,
        "rows":rows,"row_count":len(rows),"cross_reference_exact_file_name_count":len(rows),
        "new_original_source_client_audio_files":0,"game_sound_event_playback_observed":False,
        "original_taiwan_v1_event_selector_verified":False,"new_original_game_content_count":0,
        "original_html_or_audio_in_public_git":False,
        "next":"COMPARE_OTHER_2004_PLAYER_GUIDE_WITH_SOURCE_BYTES_OR_STOP"}

def acquire():
    req=urllib.request.Request(SOURCE_URL,headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept-Encoding":"identity","Accept":"text/html,*/*"})
    with urllib.request.urlopen(req,timeout=28) as r:
        raw=r.read(500001)
        assert r.status==200
        return raw,r.geturl()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--replay-live",action="store_true")
    p.add_argument("--output",default=None)
    args=p.parse_args()
    original_names()
    if not args.replay_live:
        print("SCENE41_FIXED_TW10_AUDIO_MANIFEST_OK; no source replay")
        return
    raw,url=acquire()
    report=parse_page(raw,url)
    s=json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.output: Path(args.output).write_text(s,encoding="utf-8")
    print("SCENE41_SOURCE "+json.dumps({k:report[k] for k in ("resolved_url","current_http_bytes","current_http_sha256","original_bytes_invalid_decoding","selected_decoding","row_count","cross_reference_exact_file_name_count")},ensure_ascii=False))

if __name__=="__main__":
    main()
