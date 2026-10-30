"""SCENE43: two CN2.0 original operator-web named pet cells -> bounded archived JPEG evidence.

On a source runner only. Original JPG/HTML bytes must never enter public Git.
A true source HTTP failure is a reported failure, not a fabricated image or game ID.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen
from urllib.parse import urlsplit, unquote
from tools.stoneage_waei_cn20_new_pet_pagination import parse_page

ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/"research/recovered/STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-R1.json"
PARENT_BLOB="f950aa33af0b3ec8693b2867758faf006aee546b"
PRIOR=ROOT/"research/recovered/STONEAGE-CN20-NAMED-PET-VISUAL-SOURCE-R104.json"
PRIOR_BLOB="9001f479efb6abcdf7ac4f28ef7f75c7e6aa344f"
PAGE_ORIGINAL="http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet2.asp"
PAGE_CAPTURE="20011023181629"
PAGE_URL="https://web.archive.org/web/"+PAGE_CAPTURE+"id_/"+PAGE_ORIGINAL
PAGE_BYTES=64382
PAGE_SHA="2c7aea8d0319c2070d5c7590a95bfc892c2463deb76c5b95fca8c281549c76f0"
SELECTION=(85,86)
EXPECTED=(("瑞德宝","img/newpet/84.JPG"),("瑞里西尔","img/newpet/85.JPG"))
FROZEN=ROOT/"research/recovered/STONEAGE-SCENE43-CN20-TWO-NAMED-PET-WEB-IMAGES-R1.json"
MAX_JPEG=80000

def need(ok,msg):
    if not ok:raise ValueError(msg)

def sha(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def originals():
    pr=PARENT.read_bytes();old=PRIOR.read_bytes()
    need(blob(pr)==PARENT_BLOB and blob(old)==PRIOR_BLOB,"upstream source Git blob changed")
    parent=json.loads(pr);old_r=json.loads(old)
    previous={r["ordinal"] for r in old_r["selected_cells"]}
    need(previous=={84,88,89},"R104 source selection changed")
    rows=[]
    for n,(name,relative) in zip(SELECTION,EXPECTED):
        p=parent["records"][n-1]
        need(p["source_position"]["ordinal"]==n and p["name_as_written"]==name,"prior named cell drift")
        need(p["image_reference"]["relative_src_as_written"]==relative,"actual src not ordinal filename")
        need(p["image_reference"]["original_url"]==PAGE_ORIGINAL.rsplit("/",1)[0]+"/"+relative,"original image URL mismatch")
        need(p["image_reference"]["pixels_requested"] is False and p["original_game_pet_id"] is None,"old image already marked obtained")
        need(n not in previous,"overlaps with R104 previously qualified original photo")
        rows.append({"ordinal":n,"name_as_written":name,"src":relative,"original_url":p["image_reference"]["original_url"],
                     "record_id":p["record_id"],"source_position":p["source_position"],
                     "declared_size":p["image_reference"]["html_declared_dimensions"]})
    return rows

def parse_original_page(raw):
    need(len(raw)==PAGE_BYTES and sha(raw)==PAGE_SHA,"actual 2001 archived HTML differs")
    grid=parse_page(raw.decode("gb18030","strict"),1)
    rows=originals()
    for x in rows:
        pos=x["source_position"]
        cell=grid[pos["row"]-1][pos["column"]-1]
        need(cell==[x["name_as_written"],x["src"],x["declared_size"]],"name/image and actual row/column not same")
    return rows

def archived_url(final, original):
    prefix="https://web.archive.org/web/"
    need(final.startswith(prefix),"image not Wayback archive")
    m=re.fullmatch(r"([0-9]{14})id_/(https?://[^?#]+)",final[len(prefix):])
    need(m is not None,"image isn't raw id_ archived original")
    finalpart=urlsplit(m.group(2));origin=urlsplit(original)
    need(finalpart.hostname in {origin.hostname, origin.hostname.removeprefix("www.")},"unqualified archive host")
    need(finalpart.path==origin.path and finalpart.query=="" and finalpart.fragment=="","different pet image")
    need(finalpart.scheme in ("http","https") and (finalpart.port is None or finalpart.port==80),"unknown image URL variant")
    return m.group(1)

def inspect_jpeg(raw,final,original):
    capture=archived_url(final,original)
    need(250<len(raw)<=MAX_JPEG and raw[:2]==b"\xff\xd8","not a qualifying original JPEG payload")
    from PIL import Image
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        need(im.format=="JPEG" and im.mode=="RGB" and im.size==(83,90),"not original 83x90 static JPEG")
        need(getattr(im,"n_frames",1)==1,"unqualified extra frames")
        rgba=im.convert("RGBA")
        facts={"format":im.format,"mode":im.mode,"size":list(im.size),"frames":1,
               "rgba_sha256":sha(rgba.tobytes()),"rgba_bytes":len(rgba.tobytes())}
    return {"actual_capture":capture,"actual_url":final,"bytes":len(raw),"sha256":sha(raw),**facts,
            "visual_review_by_assistant":False,"native_client_bitmap_or_sprite_identity_proven":False}

def acquire(url,maxbytes):
    with urlopen(Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; StoneAgeArchaeology/1.0)","Accept-Encoding":"identity"}),timeout=32) as r:
        raw=r.read(maxbytes+1)
        need(r.status==200 and len(raw)<=maxbytes,"source status/size invalid")
        return raw,r.geturl(),r.status

def build_live():
    page,final,status=acquire(PAGE_URL,100000)
    need(final==PAGE_URL and status==200,"original HTML capture moved")
    rows=parse_original_page(page)
    entries=[]
    for x in rows:
        requested="https://web.archive.org/web/"+PAGE_CAPTURE+"id_/"+x["original_url"]
        common={"web_ordinal":x["ordinal"],"source_parent_record_id":x["record_id"],"name_as_written":x["name_as_written"],
                "original_image_url":x["original_url"],"original_relative_src":x["src"],
                "original_page_position":x["source_position"],"html_declared_size":x["declared_size"],"requested_url":requested,
                "source_page_capture":PAGE_CAPTURE,"same_instant_as_archive_page_proven":False}
        try:
            payload,actual,_=acquire(requested,MAX_JPEG)
            im=inspect_jpeg(payload,actual,x["original_url"])
            entries.append({**common,"status":"JPEG_SOURCE_BYTES_QUALIFIED_NO_VISUAL_REVIEW","image":im,"failure":None})
        except Exception as exc:
            entries.append({**common,"status":"UNAVAILABLE_OR_UNQUALIFIED_THIS_SINGLE_ATTEMPT","image":None,
                            "failure":type(exc).__name__+": "+str(exc)[:450]})
    return {"schema":"stoneage.scene43.cn20.two_original_pet_cells.r1","date":"2026-10-30",
      "original_official_page":PAGE_ORIGINAL,"actual_page_archive_url":PAGE_URL,"page_capture":PAGE_CAPTURE,
      "actual_page_bytes":len(page),"actual_page_sha256":sha(page),"actual_page_decoding":"gb18030",
      "source_prior_catalog_blob":PARENT_BLOB,"source_prior_visual_r104_blob":PRIOR_BLOB,
      "selected_ordinals":list(SELECTION),"entries":entries,
      "qualified_image_count":sum(e["image"] is not None for e in entries),
      "attempted_new_original_image_references":len(entries),"previous_visuals_recounted_as_new":0,
      "official_page_same_build_as_native_tw10_or_jss1999_proven":False,
      "original_game_pet_ids_or_sprites_verified":False,
      "pet_growth_skill_habitat_or_riding_recovered":False,
      "human_visual_review_performed":False,
      "original_html_or_jpegs_committed_to_public_git":False,
      "original_game_world_entered":False,
      "stage_a":"7_PARTIAL_2_OPEN","stage_b":"GATED","wiki":"GATED","r79":"PAUSED_NON_BLOCKING",
      "overall_percent":None,"next":"SCENE44-CROSS-DOMAIN-MATERIAL-ROTATION"}

def validate_frozen(d):
    rows=originals()
    need(d["schema"]=="stoneage.scene43.cn20.two_original_pet_cells.r1","schema changed")
    need(d["selected_ordinals"]==list(SELECTION),"selection changed")
    need(d["actual_page_bytes"]==PAGE_BYTES and d["actual_page_sha256"]==PAGE_SHA,"source page qualification changed")
    need(d["qualified_image_count"]==sum(e["image"] is not None for e in d["entries"]),"fake good count")
    need(len(d["entries"])==len(rows)==2,"missing or extra selected rows")
    for a,r in zip(d["entries"],rows):
        need(a["web_ordinal"]==r["ordinal"] and a["name_as_written"]==r["name_as_written"] and
             a["original_relative_src"]==r["src"] and a["original_image_url"]==r["original_url"],"cell identity drift")
        if a["image"] is not None:
            im=a["image"];need(a["status"]=="JPEG_SOURCE_BYTES_QUALIFIED_NO_VISUAL_REVIEW" and a["failure"] is None,"unqualified photo")
            need(im["size"]==[83,90] and im["format"]=="JPEG" and im["frames"]==1 and im["mode"]=="RGB","image facts changed")
            need(250<im["bytes"]<=MAX_JPEG and re.fullmatch("[a-f0-9]{64}",im["sha256"]) is not None,"digest bounds changed")
            need(archived_url(im["actual_url"],r["original_url"])==im["actual_capture"],"captured bytes URL mismatch")
            need(im["visual_review_by_assistant"] is False and im["native_client_bitmap_or_sprite_identity_proven"] is False,"original visual boundary promoted")
        else:need(a["status"]=="UNAVAILABLE_OR_UNQUALIFIED_THIS_SINGLE_ATTEMPT" and bool(a["failure"]),"missing failure record")
    for k in ("official_page_same_build_as_native_tw10_or_jss1999_proven","original_game_pet_ids_or_sprites_verified",
              "pet_growth_skill_habitat_or_riding_recovered","human_visual_review_performed",
              "original_html_or_jpegs_committed_to_public_git","original_game_world_entered"):
        need(d[k] is False,k+" promoted")
    return d

def main():
    p=argparse.ArgumentParser();p.add_argument("--source-live",action="store_true");p.add_argument("--write")
    a=p.parse_args();originals()
    if a.source_live:
        data=build_live()
        report=json.dumps(data,sort_keys=True,ensure_ascii=False,indent=2)+"\n"
        if FROZEN.exists():need(report==FROZEN.read_text(encoding="utf-8"),"source replay differs from frozen report")
        if a.write:Path(a.write).write_text(report,encoding="utf-8")
        print("SCENE43_SOURCE",json.dumps({"page_bytes":data["actual_page_bytes"],"page_sha":data["actual_page_sha256"],
               "qualified":data["qualified_image_count"],"images":[{"n":r["web_ordinal"],"status":r["status"],"sha":r["image"]["sha256"] if r["image"] else None} for r in data["entries"]]},ensure_ascii=False))
    else:
        if FROZEN.exists():
            d=json.loads(FROZEN.read_text(encoding="utf-8"));validate_frozen(d)
            print("SCENE43_PINNED_PAGE_AND_2_IMAGE_REFERENCES_PASS")
        else:print("SCENE43_SOURCE_PREFLIGHT_2_UNQUALIFIED_PIXELS_UNTIL_LIVE_REPLAY")

if __name__=="__main__":main()
