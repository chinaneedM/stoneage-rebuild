"""PET104 retained index custody plus bounded archive replay preflight.

Only archive-host requests. At most 65536 binary prefix bytes per request.
No full original archive, software execution or copyrighted page publication.
"""
import argparse
import concurrent.futures
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from tools import stoneage_pet_high_first_104_cn70_archive_index as idx
P=idx.ROOT/"research/pets"
REPORT=P/"PET-HIGH-FIRST-104-CN70-ARCHIVE-INDEX-R1.json"
CUSTODY=P/"PET-HIGH-FIRST-104-CUSTODY-R1.json"
REPLAY=P/"PET-HIGH-FIRST-105-CN70-ARCHIVE-REPLAY-PREFLIGHT-R1.json"
REPORT_SHA="7c48823b46daf7f5c9254ee0806c42802e3eaf7ceeeb1d1d38da6c262d13d7ee"
ZIP_SHA="ba94846ec05eb4c5e7fcae6daa0334025a97bb44ac72b06df1153942df119701"
SOURCE_HEAD="d18c57a53768e14dba8eb003114e02a4c1f7f2d4"
def stable(d):return (json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()
def verify_report(raw):
    idx.verify_inputs()
    assert idx.sha(raw)==REPORT_SHA
    d=json.loads(raw); assert d["prior_git_blob"]==idx.PRIOR_BLOB
    assert d["queries"]==19 and not d["original_payloads"] and not d["official_closures"]
    assert d["summary"]=={"EMPTY_BODY_NOT_CONFIRMED":5,"METADATA_PARSED":14}
    assert [(x["kind"],x["target_or_query"],x["request_url"]) for x in d["results"]]==idx.jobs()
    counts={}
    available={}
    for x in d["results"]:
        assert x["http_status"]==200 and not x["original_payload_downloaded"]
        assert len(x["response_sha256"])==64
        m=x["metadata"]
        if x["kind"]=="WAYBACK_CDX":
            counts[x["target_or_query"]]=m["row_count"]
            assert m["row_count"]==len(m["rows"])
        if x["kind"]=="WAYBACK_AVAILABLE" and m["closest"]:
            available[x["target_or_query"]]=m["closest"]["timestamp"]
    assert list(counts.values())==[0,5,1,3,13]
    assert available=={idx.TARGETS[1]:"20040508172441",idx.TARGETS[4]:"20031218033632"}
    assert [x["metadata"]["num_found"] for x in d["results"] if x["kind"]=="IA_CATALOGUE"]==[2,1,102,0]
    return d
def extract(artifact):
    z=artifact.read_bytes();assert len(z)==5935 and idx.sha(z)==ZIP_SHA
    with zipfile.ZipFile(artifact) as f:
        assert f.namelist()==["pet104.json"]
        raw=f.read("pet104.json")
    verify_report(raw)
    c=dict(schema="stoneage.pet104.custody.r1",source_head=SOURCE_HEAD,run=45813700669,job=139887832894,artifact=15114760222,zip_bytes=len(z),zip_sha256=ZIP_SHA,report_sha256=REPORT_SHA,report_git_blob=idx.blob(raw),original_payloads=0,official_closures=0)
    REPORT.write_bytes(raw);CUSTODY.write_bytes(stable(c))
    return json.loads(raw)
def verify():
    raw=REPORT.read_bytes();d=verify_report(raw);c=json.loads(CUSTODY.read_bytes())
    assert c==dict(schema="stoneage.pet104.custody.r1",source_head=SOURCE_HEAD,run=45813700669,job=139887832894,artifact=15114760222,zip_bytes=5935,zip_sha256=ZIP_SHA,report_sha256=REPORT_SHA,report_git_blob=idx.blob(raw),original_payloads=0,official_closures=0)
    return d
def selected(d):
    out=[]
    for x in d["results"]:
        if x["kind"]!="WAYBACK_CDX":continue
        for r in x["metadata"]["rows"]:
            if r["statuscode"]!="200":continue
            t=r["timestamp"]; orig=r["original"]
            assert re.fullmatch(r"\d{14}",t)
            parsed=urllib.parse.urlsplit(orig)
            expected=urllib.parse.urlsplit(x["target_or_query"])
            if parsed.hostname!=expected.hostname or parsed.path.lower()!=expected.path.lower() or parsed.username or parsed.password:continue
            kind="PAGE" if x["target_or_query"]==idx.TARGETS[-1] else "RAR_PREFIX"
            out.append(dict(kind=kind,target=x["target_or_query"],timestamp=t,original=orig,cdx_mime=r["mimetype"],cdx_digest=r["digest"],cdx_length=r["length"],replay_url="https://web.archive.org/web/"+t+"id_/"+orig))
    # Replay at most two historical HTML page snapshots; archive prefixes all
    # matching HTTP-200 captures (at most nine). Never contact live source.
    pages=sorted((x for x in out if x["kind"]=="PAGE"),key=lambda x:x["timestamp"])
    page_selected=[x for x in pages if x["timestamp"]=="20031218033632"]
    if pages and pages[0] not in page_selected:page_selected.append(pages[0])
    if not page_selected and pages:page_selected=pages[:1]
    return [x for x in out if x["kind"]=="RAR_PREFIX"]+page_selected
class Links(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag not in ("a","area","iframe","frame","form"):return
        for key,value in attrs:
            if key in ("href","src","action") and value and not value.lower().startswith(("javascript:","mailto:","#")):
                self.links.append(value)
def parse_links(raw,original):
    for enc in ("gb18030","utf-8"):
        try:txt=raw.decode(enc);break
        except UnicodeDecodeError:continue
    else:txt=raw.decode("gb18030","replace")
    p=Links();p.feed(txt)
    out=set()
    for s in p.links:
        resolved=urllib.parse.urljoin(original,s)
        u=urllib.parse.urlsplit(resolved)
        if u.scheme not in ("http","https","ftp") or not u.hostname or u.username or u.password:continue
        if re.search(r"\.(rar|zip|exe|iso|7z|cab)(?:$|[?#])|download|downfile|softview",resolved,re.I):
            out.add(resolved[:1000])
    return sorted(out)[:150]
def classify(raw):
    if raw.startswith(b"Rar!\x1a\x07\x00"):return "RAR4_MAGIC"
    if raw.startswith(b"Rar!\x1a\x07\x01\x00"):return "RAR5_MAGIC"
    if raw.startswith(b"PK\x03\x04"):return "ZIP_MAGIC"
    if raw.startswith(b"MZ"):return "MZ_MAGIC"
    if raw.lstrip().lower().startswith((b"<html",b"<!doctype",b"<?xml",b"<head")):return "HTML_OR_XML"
    return "OTHER_OR_EMPTY"
def replay(x):
    row=dict(x);limit=65536 if x["kind"]=="RAR_PREFIX" else 262144
    try:
        op=urllib.request.build_opener(idx.ArchiveRedirect())
        headers={"User-Agent":"stoneage-rebuild-archaeology/1.0","Accept-Encoding":"identity"}
        if x["kind"]=="RAR_PREFIX":headers["Range"]="bytes=0-65535"
        req=urllib.request.Request(x["replay_url"],headers=headers)
        with op.open(req,timeout=30) as r:
            raw=r.read(limit)
            row.update(status=r.status,final_url=r.geturl(),sample_bytes=len(raw),sample_sha256=idx.sha(raw),magic=classify(raw),headers={k:r.headers.get(k) for k in ("Content-Type","Content-Length","Content-Range","X-Archive-Orig-Content-Length","X-Archive-Orig-Content-Type","Memento-Datetime")})
            row["result"]="BOUNDED_RESPONSE"
        if x["kind"]=="PAGE":row["download_link_candidates"]=parse_links(raw,x["original"])
    except urllib.error.HTTPError as e:
        raw=e.read(min(4096,limit));row.update(result="HTTP_ERROR",status=e.code,sample_bytes=len(raw),sample_sha256=idx.sha(raw),magic=classify(raw))
    except (OSError,ValueError,AssertionError) as e:
        row.update(result="ACCESS_ERROR",error_type=type(e).__name__,error=str(e)[:300])
    row["full_original_verified"]=False
    return row
def main():
    p=argparse.ArgumentParser();p.add_argument("--artifact",type=Path);p.add_argument("--replay",action="store_true");a=p.parse_args()
    d=extract(a.artifact) if a.artifact else verify()
    print("PET104_CUSTODY_OK",flush=True)
    for x in d["results"]:
        if x["kind"]=="WAYBACK_CDX":
            print("PET104_CDX="+json.dumps({"target":x["target_or_query"],"rows":x["metadata"]["rows"]},ensure_ascii=False),flush=True)
        if x["kind"]=="IA_CATALOGUE":
            print("PET104_IA="+json.dumps({"query":x["target_or_query"],"count":x["metadata"]["num_found"],"rows":x["metadata"]["rows"][:8]},ensure_ascii=False),flush=True)
    if not a.replay:return
    choices=selected(d);assert len(choices)<=11
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(replay,choices))
    report=dict(schema="stoneage.pet105.cn70.archive_replay_preflight.r1",source_report_sha256=REPORT_SHA,source_report_git_blob=idx.blob(REPORT.read_bytes()),results=rows,full_originals_verified=0,official_closures=0,original_assets_published=False)
    REPLAY.write_bytes(stable(report))
    for r in rows:print("PET105_REPLAY="+json.dumps(r,ensure_ascii=False,sort_keys=True),flush=True)
    print("PET105_REPORT_SHA256="+idx.sha(REPLAY.read_bytes()),flush=True)
if __name__=="__main__":main()
