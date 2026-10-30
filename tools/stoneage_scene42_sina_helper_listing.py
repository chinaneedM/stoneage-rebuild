"""SCENE42: source-bound four download-list labels from an already registered Sina page.

Only a bounded HTML fetch; no executable download, program compatibility claim,
new game logic, or first-publication chronology inferred from page date.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request,urlopen

from tools.stoneage_cn2003_katan_visual_r100 import Tables, compact

ROOT=Path(__file__).resolve().parents[1]
URL="https://games.sina.com.cn/zhqu/sta/ltxs/sqxz.shtml"
PAGE_TITLE="石器时代ONLINE宠物进化史相关下载"
DATE_LABEL="2003-04-03 15:38"
NAMES=("SACHXP++5042","SACHMX5.00B8","SACHMX5.00FREEB1","小明蓝暴自动猜谜器")
OLD_R103=ROOT/"research/recovered/STONEAGE-SACHMX-VERSION-VISUAL-SOURCE-R103.json"
OLD_R103_BLOB="57fe1ede0f8ca421ac2c07b64f99fb79dc52b686"
FROZEN=ROOT/"research/recovered/STONEAGE-SCENE42-SINA-HELPER-DOWNLOAD-LIST-R1.json"

def must(ok, message):
    if not ok: raise ValueError(message)

def gitblob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def old_version_check():
    raw=OLD_R103.read_bytes()
    must(gitblob(raw)==OLD_R103_BLOB,"old SACHMX source drift")
    r=json.loads(raw)
    labels={x["edition"]:x["index_label"] for x in r["articles"]}
    must(labels["member"]=="SACH-MX5.00B9","old actual B9 label missing")
    must(labels["free"].replace("-","").lower().startswith("sachmx"),"old free label missing")
    return labels

def parse(raw, final_url=URL):
    must(final_url==URL,"source redirect or origin drift")
    must(3000<len(raw)<250000,"unexpected HTML extent")
    candidates=[]
    for encoding in ("gb18030","utf-8"):
        try: decoded=raw.decode(encoding,"strict")
        except UnicodeDecodeError: continue
        p=Tables();p.feed(decoded)
        visible=compact("".join(p.text))
        if PAGE_TITLE in visible and "2003-04-0315:38" in visible and "新浪游戏" in visible:
            candidates.append((encoding,p,visible))
    must(len(candidates)==1,"wrong or ambiguous encoding/title/byline")
    encoding,p,visible=candidates[0]
    must(visible.count("石器时代外挂下载")==1,"missing or doubled helper section")
    must(visible.count("2003-04-0315:38")==1,"ambiguous date label")
    found=[]
    for rows in p.tables:
        matching=[]
        for row in rows:
            cells=[compact(c["text"]) for c in row]
            for name in NAMES:
                if name in cells:
                    must(cells.count(name)==1,"duplicate tool label in one row")
                    matching.append((name,row))
        if len(matching)==len(NAMES) and tuple(x[0] for x in matching)==NAMES:
            found.append(matching)
    must(len(found)==1,"four exact labels not in one ordered real HTML table")
    result=[]
    for name,row in found[0]:
        cells=[compact(c["text"]) for c in row]
        must(cells.count(name)==1,"item label missing")
        images=[v for c in row for v in c["images"]]
        links=[img["href"] for img in images if img.get("href")]
        # Preserve actual HREF, but do not dereference or deliver an executable.
        must(len(links)<=2,"unreviewed multiple download links")
        result.append({"archive_listing_label":name,
                       "download_links_in_same_table_row":links,
                       "listed_program_files_downloaded":False,
                       "downloaded_program_build_identity_verified":False,
                       "first_release_or_first_seen_date_verified":False,
                       "original_helper_capabilities_verified":False})
    must("4月6日" in visible,"later-dated tournament listing absent")
    old=old_version_check()
    return {"schema":"stoneage.scene42.sina.helper_listing_source.r1",
      "source_url":URL,"resolved_url":final_url,
      "page_bytes":len(raw),"page_sha256":hashlib.sha256(raw).hexdigest(),
      "page_encoding":encoding,
      "page_byline":"新浪游戏","page_display_date":DATE_LABEL,
      "page_later_tournament_date_label":"4月6日",
      "date_label_does_not_establish_exact_contemporary_page_snapshot":True,
      "source_url_previously_in_repo":True,
      "preexisting_source_register_name":"SRC-CN-2003-SINA-SA-DOWNLOAD-HUB-01",
      "new_material_is_bounded_tool_download_table_attribution":True,
      "entries":result,"entry_count":len(result),
      "same_article_does_not_prove_any_program_binary_or_release":True,
      "previously_verified_june2003_member_listing":old["member"],
      "sachmx_b8_and_june_b9_are_same_binary_verified":False,
      "sachxp_name_and_sachmx_name_same_family_verified":False,
      "blue_pet_quiz_tool_task_answers_verified":False,
      "source_html_or_program_files_committed":False,
      "original_game_started":False,
      "stage_a":"7_PARTIAL_2_OPEN","stage_b":"GATED",
      "r79":"PAUSED_NON_BLOCKING","overall_percent":None,
      "next":"SCENE43-OFFICIAL-PET-NAMED-IMAGE-SOURCE-REVIEW"}

def live():
    req=Request(URL,headers={"User-Agent":"Mozilla/5.0","Accept-Encoding":"identity"})
    with urlopen(req,timeout=30) as response:
        raw=response.read(250001)
        must(response.status==200,"current page HTTP not 200")
        return raw,response.url

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source-live",action="store_true")
    parser.add_argument("--write")
    args=parser.parse_args()
    old_version_check()
    if not args.source_live:
        must(FROZEN.exists()==True,"frozen result not present")
        d=json.loads(FROZEN.read_text(encoding="utf-8"))
        must(d["entry_count"]==4 and [e["archive_listing_label"] for e in d["entries"]]==list(NAMES),"frozen names altered")
        must(d["source_url_previously_in_repo"] and d["date_label_does_not_establish_exact_contemporary_page_snapshot"],"evidence boundary altered")
        must(d["sachmx_b8_and_june_b9_are_same_binary_verified"] is False and d["original_game_started"] is False,"unsupported upgrade")
        print("SCENE42 preserved names/source/boundary PASS; no network fetch")
        return
    body,u=live()
    x=parse(body,u)
    s=json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if FROZEN.exists():
        must(s==FROZEN.read_text(encoding="utf-8"),"live page semantic report has changed")
    if args.write:Path(args.write).write_text(s,encoding="utf-8")
    print("SCENE42_SOURCE",json.dumps({"bytes":x["page_bytes"],"sha256":x["page_sha256"],"encoding":x["page_encoding"],"names":[z["archive_listing_label"] for z in x["entries"]]},ensure_ascii=False))

if __name__=="__main__":main()
