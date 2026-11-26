"""PET114: archive-only independent CN8.5 ZOL 2011 distribution record."""
import argparse
from datetime import datetime
from html.parser import HTMLParser
import json,re
from pathlib import Path
import urllib.parse,urllib.request,urllib.error
from tools import stoneage_pet_high_first_104_cn70_archive_index as idx
from tools import stoneage_pet_high_first_109_cn75_custody as prior
from tools import stoneage_pet_high_first_111_cn75_patch_context as context
P=idx.ROOT/"research/pets"
R=P/"PET-HIGH-FIRST-113-CN75-TORRENT-IDENTITY-REVIEW-R1.json"
PAGE="youxi.zol.com.cn/ol/13450/download.html"
TARGETS=tuple(s+"://"+x for x in (PAGE,PAGE+"?softId=357206","youxi.zol.com.cn/down.php?site=11&softid=357206&subcatid=62") for s in ("http","https"))
CAP=262144
def jobs():
    return [("WAYBACK_CDX",t,"https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode(dict(url=t,output="json",**{"from":"2010","to":"2015"},limit=100,fl="timestamp,original,statuscode,mimetype,digest,length"))) for t in TARGETS]
def verify():
    raw=R.read_bytes()
    assert idx.blob(raw)=="bec4bf24c737ac0e2510a010ac50e5c65a83f015"
    d=json.loads(raw);assert not d["original_client_verified"] and d["official_closures"]==0
def norm(url):
    u=urllib.parse.urlsplit(url)
    return (u.hostname,u.path.lower(),tuple(sorted((k.lower(),v) for k,v in urllib.parse.parse_qsl(u.query,keep_blank_values=True))))
def select(rows):
    # Separate page and redirect endpoint. At most two distinct digests each.
    groups={norm(t):[] for t in TARGETS}
    for row in rows:
        if row["result"]!="METADATA_PARSED":continue
        for x in row["metadata"]["rows"]:
            if norm(x["original"])!=norm(row["target_or_query"]):continue
            if not (len(x["timestamp"])==14 and x["timestamp"].isdigit()):continue
            if x["statuscode"] not in ("200","301","302","303","307","308"):continue
            groups[norm(row["target_or_query"])].append(x)
    result=[]
    for group in groups.values():
        seen=set()
        for x in sorted(group,key=lambda x:(abs((datetime.strptime(x["timestamp"][:8],"%Y%m%d")-datetime(2011,6,22)).days),x["timestamp"])):
            key=x["digest"] if x["digest"]!="-" else (x["original"],x["timestamp"])
            if key in seen:continue
            seen.add(key);result.append(x)
            if len(seen)==2:break
    return result
class NoFollow(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return None
def extract_redirect(loc):
    if not loc:return None
    # Never follow the redirect. Unwrap only archive wrapper prefix.
    m=re.match(r"^(?:https?://web\.archive\.org)?/web/\d{1,14}(?:[a-z_]+)?/(https?://.+)$",loc,re.I)
    u=m.group(1) if m else loc
    p=urllib.parse.urlsplit(u)
    if p.scheme not in ("http","https","ftp") or not p.hostname or p.username or p.password:return None
    return u[:1200]
class Text(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.text=[];self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ("script","style"):self.skip+=1
    def handle_endtag(self,tag):
        if tag in ("script","style") and self.skip:self.skip-=1
    def handle_data(self,t):
        if not self.skip:self.text.append(t)
def capture(x):
    url="https://web.archive.org/web/"+x["timestamp"]+"id_/"+x["original"]
    row=dict(cdx=x,replay_url=url)
    q=urllib.request.Request(url,headers={"Accept-Encoding":"identity","User-Agent":"stoneage-rebuild-archaeology/1.0"})
    try:
        try:f=urllib.request.build_opener(NoFollow()).open(q,timeout=25)
        except urllib.error.HTTPError as e:f=e
        with f:
            raw=f.read(CAP+1);row.update(status=f.status,response_bytes=len(raw),response_sha256=idx.sha(raw),content_type=f.headers.get("Content-Type"),historical_location_candidate=extract_redirect(f.headers.get("X-Archive-Orig-Location")),replay_location_candidate=extract_redirect(f.headers.get("Location")))
        if len(raw)>CAP:row["result"]="LIMIT_EXCEEDED";return row
        if row["status"] in (301,302,303,307,308):
            row["result"]="REDIRECT_METADATA_ONLY";return row
        if row["status"]!=200:row["result"]="HTTP_ERROR";return row
        if not (row["content_type"] or "").lower().startswith("text/html"):
            row["result"]="NON_HTML_NO_EXTRACTION";return row
        d=context.parse(raw,x["original"])
        for enc in ("utf-8","gb18030"):
            try:s=raw.decode(enc);break
            except UnicodeDecodeError:continue
        else:s=raw.decode("gb18030","replace")
        p=Text();p.feed(s)
        t=" ".join(p.text)
        row.update(result="HTML_METADATA_PARSED",**d,mentions_stoneage="石器时代" in t or "石器時代" in t,mentions_magic_adventure="魔域大冒险" in t or "魔域大冒險" in t,mentions_1_15gb=bool(re.search(r"1\.15\s*G(?:B)?",t,re.I)),mentions_2011_06_22=bool(re.search(r"2011[-/年]0?6[-/月]22",t)),mentions_record_id="357206" in s)
    except (OSError,ValueError,AssertionError) as e:row.update(result="ACCESS_OR_PARSE_ERROR",error_type=type(e).__name__,error=str(e)[:200])
    return row
def selftest():
    verify()
    assert len(TARGETS)==6 and len({norm(x) for x in TARGETS})==3
    assert extract_redirect("https://web.archive.org/web/20110622000000id_/http://example.invalid/a.exe")=="http://example.invalid/a.exe"
    assert extract_redirect("http://a:b@example.invalid/a.exe") is None
    assert not select([{"result":"METADATA_PARSED","target_or_query":TARGETS[0],"metadata":{"rows":[]}}])
    sample=dict(timestamp="20110622000000",original=TARGETS[0],statuscode="200",mimetype="text/html",digest="TEST",length="100")
    sample2=dict(sample,original=TARGETS[1],timestamp="20110623000000")
    sample3=dict(sample,original=TARGETS[2],digest="OTHER")
    rows=[dict(result="METADATA_PARSED",target_or_query=t,metadata=dict(rows=[x])) for t,x in zip(TARGETS[:3],[sample,sample2,sample3])]
    assert select(rows)==[sample,sample3]
    assert norm(TARGETS[-1])==norm("http://youxi.zol.com.cn/down.php?subcatid=62&softid=357206&site=11")
    print("PET114_SELFTEST_OK")
def main():
    p=argparse.ArgumentParser();p.add_argument("--self-test",action="store_true");p.add_argument("--output",type=Path);a=p.parse_args();selftest()
    if a.self_test:return
    assert a.output
    rows=[idx.request(j) for j in jobs()];chosen=select(rows);assert len(chosen)<=6
    result=dict(schema="stoneage.pet114.cn85.zol_2011_archive_r1",prior_git_blob=idx.blob(R.read_bytes()),targets=list(TARGETS),indexes=rows,captures=[capture(x) for x in chosen],original_payloads=0,official_closures=0,original_assets_published=False,redirects_followed=False)
    a.output.write_bytes(prior.dump(result))
    print("PET114_REPORT_SHA256="+idx.sha(a.output.read_bytes()),flush=True)
    for x in rows:print("PET114_INDEX="+json.dumps(dict(target=x["target_or_query"],result=x["result"],count=x.get("metadata",{}).get("row_count")),ensure_ascii=False),flush=True)
    for x in result["captures"]:print("PET114_CAPTURE="+json.dumps({k:v for k,v in x.items() if k!="links"}|{"file_links":[v for v in x.get("links",[]) if v["file_extension_candidate"] or "357206" in v["url"]]},ensure_ascii=False,sort_keys=True),flush=True)
if __name__=="__main__":main()
