"""PET111: preserve PET110 and recover patch-role labels from source-qualified HTML."""
import argparse
from datetime import datetime
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request
import zipfile
from tools import stoneage_pet_high_first_104_cn70_archive_index as idx
from tools import stoneage_pet_high_first_109_cn75_custody as prior
from tools import stoneage_pet_high_first_110_cn75_rar_preflight as last
P=idx.ROOT/"research/pets"
R110=P/"PET-HIGH-FIRST-110-CN75-RAR-PREFLIGHT-R1.json"
R109=P/"PET-HIGH-FIRST-109-CN75-BOUNDED-REPLAY-R1.json"
SHA110="b2ee784de3e16d9ec7c1bb346f7676ea588d8753e71175414c3adfeb1e7bb56f"
ZIP110="8d4255a906cf3afa9349464975aefb897d6301283007caf0c1b0c4255b175bf3"
NEW=(
"http://download.17173.com/Files/11/20041104/2450.shtml",
"http://download.17173.com/Files/12/20041105/2457.shtml",
"http://games.enet.com.cn/download/D0120041109001.html",
"http://games.enet.com.cn/download/gmdown.php?downid=D0220041110001",
"http://download.cgame.cn/view.asp?letmesee=5086",
"http://download.cgame.cn/view.asp?letmesee=5087",
"http://www.gameking.com.cn/gk/download/04/11/9/134931278.htm",
"http://www.play119.com/down/softview.aspx?ID=259",
"http://www.play119.com/down/softview.aspx?ID=260",
)
FILE_RE=re.compile(r"\.(?:rar|zip|exe|cab|7z|iso|torrent)(?:$|[?#])",re.I)
VERSION_RE=re.compile(r"(?<!\d)(?:1\.82|2\.0|3\.0|3\.6|5\.0|6\.0|7\.0|7\.5|8\.0|8\.5)(?!\d)")
WORDS=("补丁","升级","测试","正式","客户端","完整版","完整","专用","安装","下载","精灵的召唤","精灵召唤","BT","种子","patch","update","beta")
def verify(artifact):
    z=artifact.read_bytes()
    assert len(z)==938 and idx.sha(z)==ZIP110
    with zipfile.ZipFile(artifact) as f:
        assert f.namelist()==["pet110.json"]
        raw=f.read("pet110.json")
    assert raw==R110.read_bytes() and idx.sha(raw)==SHA110
    d=json.loads(raw)
    assert d["targets"]==list(last.TARGETS) and len(d["index_results"])==4
    assert all(x["http_status"]==200 and x["result"]=="METADATA_PARSED" and x["metadata"]["rows"]==[] and x["metadata"]["row_count"]==0 for x in d["index_results"])
    assert not d["prefix_results"] and d["unique_http_success_digest_candidates"]==d["full_originals_verified"]==d["official_closures"]==0
    assert not d["original_assets_published"]
    raw109=R109.read_bytes();assert idx.blob(raw109)==d["prior_git_blob"]
    p=json.loads(raw109)
    assert all(u in p["attempts"][1]["download_link_candidates"] for u in NEW)
    return p
class LinkRows(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.rows=[];self.stack=[];self.active=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=="tr":
            self.stack.append({"text":[],"links":[]})
        if tag=="a":
            d=dict(attrs);href=d.get("href")
            if href:self.active.append({"href":href,"text":[],"row":self.stack[-1] if self.stack else None})
    def handle_data(self,s):
        for row in self.stack:row["text"].append(s)
        if self.active:self.active[-1]["text"].append(s)
    def handle_endtag(self,tag):
        if tag=="a" and self.active:
            a=self.active.pop();self.links.append(a)
        if tag=="tr" and self.stack:self.rows.append(self.stack.pop())
def keywords(s):
    return [w for w in WORDS if w.casefold() in s.casefold()]
def versions(s):return sorted(set(VERSION_RE.findall(s)))
def parse(raw,url):
    for enc in ("gb18030","utf-8"):
        try:s=raw.decode(enc);break
        except UnicodeDecodeError:continue
    else:s=raw.decode("gb18030","replace");enc="gb18030-replacement"
    p=LinkRows();p.feed(s);p.close()
    out=[]
    for a in p.links:
        h=a["href"].strip()
        # Literal anchors only, never run scripts or follow them.
        if h.lower().startswith(("javascript:","mailto:","#")):continue
        resolved=urllib.parse.urljoin(url,h)
        u=urllib.parse.urlsplit(resolved)
        if u.scheme not in ("http","https","ftp") or not u.hostname or u.username or u.password:continue
        label=" ".join("".join(a["text"]).split())
        context=" ".join("".join(a["row"]["text"]).split()) if a["row"] else ""
        f=bool(FILE_RE.search(resolved))
        if not f and resolved not in NEW and not re.search(r"download|downfile|softview|gmdown|show_file|view\.asp",resolved,re.I):continue
        out.append(dict(url=resolved[:1000],file_extension_candidate=f,anchor_keywords=keywords(label),anchor_version_tokens=versions(label),row_keywords=keywords(context),row_version_tokens=versions(context),row_length=len(context),row_sha256=idx.sha(context.encode("utf-8")) if context else None))
    uniq={json.dumps(x,sort_keys=True,ensure_ascii=False):x for x in out}
    # Full retained metadata, no archived HTML or long original text.
    return dict(encoding=enc,link_count=len(uniq),links=list(uniq.values())[:240],limit_reached=len(uniq)>240)
def capture(url,original,expected=None):
    row=dict(replay_url=url,original=original)
    try:
        assert urllib.parse.urlsplit(url).hostname=="web.archive.org"
        req=urllib.request.Request(url,headers={"Accept-Encoding":"identity","User-Agent":"stoneage-rebuild-archaeology/1.0"})
        with urllib.request.build_opener(idx.ArchiveRedirect()).open(req,timeout=30) as f:
            raw=f.read(262145);row.update(status=f.status,response_bytes=len(raw),response_sha256=idx.sha(raw),final_url=f.geturl(),content_type=f.headers.get("Content-Type"))
        if len(raw)>262144:row["result"]="LIMIT_EXCEEDED";return row
        if expected and idx.sha(raw)!=expected:row["result"]="REPLAY_MISMATCH";return row
        row.update(result="HTML_METADATA_PARSED",**parse(raw,original))
    except (OSError,ValueError,AssertionError) as e:row.update(result="ACCESS_OR_PARSE_ERROR",error_type=type(e).__name__,error=str(e)[:300])
    return row
def jobs():
    return [("WAYBACK_CDX",t,"https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode(dict(url=t,output="json",**{"from":"2004","to":"2005"},limit=100,fl="timestamp,original,statuscode,mimetype,digest,length"))) for t in NEW]
def norm(url):
    u=urllib.parse.urlsplit(url)
    return (u.hostname,urllib.parse.unquote(u.path).lower(),sorted(urllib.parse.parse_qsl(u.query,keep_blank_values=True)))
def choose(row):
    if row["result"]!="METADATA_PARSED":return None
    candidates=[r for r in row["metadata"]["rows"] if r["statuscode"]=="200" and r["mimetype"].lower()=="text/html" and norm(r["original"])==norm(row["target_or_query"]) and len(r["timestamp"])==14 and r["timestamp"].isdigit()]
    if not candidates:return None
    def key(x):return(abs((datetime.strptime(x["timestamp"][:8],"%Y%m%d")-datetime(2004,11,10)).days),x["timestamp"])
    x=min(candidates,key=key)
    return x
def selftest():
    raw=b'<table><tr><td>7.5 patch</td><td><a href="test.rar">update</a></td></tr></table>'
    out=parse(raw,"http://example.invalid/page")
    x=out["links"][0];assert x["url"]=="http://example.invalid/test.rar" and x["anchor_keywords"]==["update"] and x["row_version_tokens"]==["7.5"] and "patch" in x["row_keywords"]
    assert len(NEW)==9 and len(set(NEW))==9
    print("PET111_SELFTEST_OK")
def main():
    a=argparse.ArgumentParser();a.add_argument("--artifact",type=Path);a.add_argument("--output",type=Path);a.add_argument("--self-test",action="store_true");args=a.parse_args();selftest()
    if args.self_test:return
    assert args.artifact and args.output
    p=verify(args.artifact)
    official=[capture(x["replay_url"],x["original"],x["sample_sha256"]) for x in p["attempts"][:2]]
    indexes=[idx.request(j) for j in jobs()]
    pages=[]
    for r in indexes:
        x=choose(r)
        if x:pages.append(dict(cdx=x,**capture("https://web.archive.org/web/"+x["timestamp"]+"id_/"+x["original"],x["original"])))
    result=dict(schema="stoneage.pet111.cn75.patch_route_context.r1",prior_report_git_blob=idx.blob(R110.read_bytes()),prior_report_sha256=SHA110,prior_artifact=15115382389,prior_zip_sha256=ZIP110,official_context=official,portal_indexes=indexes,portal_context=pages,official_closures=0,full_originals_verified=0,original_assets_published=False)
    args.output.write_bytes(prior.dump(result))
    print("PET111_REPORT_SHA256="+idx.sha(args.output.read_bytes()),flush=True)
    for x in official+pages:
        print("PET111_CONTEXT="+json.dumps(dict(original=x["original"],result=x["result"],response_bytes=x.get("response_bytes"),response_sha256=x.get("response_sha256"),link_count=x.get("link_count"),file_candidates=[v for v in x.get("links",[]) if v["file_extension_candidate"] or "补丁" in v["anchor_keywords"] or "patch" in v["anchor_keywords"]]),ensure_ascii=False,sort_keys=True),flush=True)
    for x in indexes:print("PET111_INDEX="+json.dumps(dict(target=x["target_or_query"],result=x["result"],count=x.get("metadata",{}).get("row_count")),ensure_ascii=False),flush=True)
if __name__=="__main__":main()
