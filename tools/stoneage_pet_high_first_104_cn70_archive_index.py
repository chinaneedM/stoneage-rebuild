"""PET104: exact historical CN7.0 archive-index metadata only."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
ROOT=Path(__file__).resolve().parents[1]
PRIOR=ROOT/"research/pets/PET-HIGH-FIRST-103-CN70-DISTRIBUTION-ROUTES-R1.json"
PRIOR_BLOB="351e89951a9e12d49ad4a150537668d3ac59bd84"
TARGETS=tuple(f"http://210.51.17.{n}/StoneAge7.rar" for n in range(235,239))+("http://download.17173.com/Files/10/20031216/494.htm",)
QUERIES=('title:"石器时代" AND mediatype:software','title:"石器時代" AND mediatype:software','"石头就业所" AND mediatype:software','"StoneAge7.rar" AND mediatype:software')
HOSTS={"web.archive.org","archive.org","arquivo.pt"}
CAP=2*1024*1024
def blob(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def jobs():
    out=[]
    for target in TARGETS:
        out += [
            ("WAYBACK_CDX",target,"https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode({"url":target,"output":"json","from":"2003","to":"2008","limit":100,"fl":"timestamp,original,statuscode,mimetype,digest,length"})),
            ("WAYBACK_AVAILABLE",target,"https://archive.org/wayback/available?"+urllib.parse.urlencode({"url":target,"timestamp":"20031219"})),
            ("ARQUIVO_CDX",target,"https://arquivo.pt/wayback/cdx?"+urllib.parse.urlencode({"url":target,"output":"json","limit":100,"from":"2003","to":"2008"}))]
    for q in QUERIES:
        out.append(("IA_CATALOGUE",q,"https://archive.org/advancedsearch.php?"+urllib.parse.urlencode([("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),("rows",100),("page",1),("output","json")])))
    return out
class ArchiveRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        u=urllib.parse.urlsplit(newurl)
        if u.scheme!="https" or u.hostname not in HOSTS or u.username or u.password:
            raise ValueError("redirect outside allowed public archive index hosts")
        return super().redirect_request(req,fp,code,msg,headers,newurl)
def parse(kind,raw):
    if kind=="ARQUIVO_CDX" and not raw.strip():return {"rows":[],"row_count":0,"format":"EMPTY_BODY_NOT_CONFIRMED"}
    if kind=="ARQUIVO_CDX":
        try:d=json.loads(raw)
        except json.JSONDecodeError:d=[json.loads(s) for s in raw.splitlines() if s.strip()]
    else:d=json.loads(raw)
    if kind=="WAYBACK_CDX":
        if not isinstance(d,list):raise ValueError("expected CDX array")
        if d:
            assert d[0]==["timestamp","original","statuscode","mimetype","digest","length"]
            assert all(isinstance(row,list) and len(row)==6 for row in d[1:])
        rows=[dict(zip(d[0],r)) for r in d[1:]]
        return {"rows":rows,"row_count":len(rows),"limit_reached":len(rows)>=100}
    if kind=="ARQUIVO_CDX":
        if isinstance(d,dict):d=[d]
        if not isinstance(d,list) or not all(isinstance(x,dict) for x in d):raise ValueError("expected CDX JSON objects")
        if not all(("url" in x or "original" in x) and "timestamp" in x for x in d):raise ValueError("invalid CDX result")
        rows=[{k:x[k] for k in ("url","original","timestamp","status","statuscode","mime","mimetype","digest","length") if k in x} for x in d]
        return {"rows":rows,"row_count":len(rows),"limit_reached":len(rows)>=100}
    if kind=="WAYBACK_AVAILABLE":
        assert isinstance(d,dict) and isinstance(d.get("archived_snapshots"),dict)
        snap=d["archived_snapshots"].get("closest")
        if snap is not None:
            assert isinstance(snap,dict) and "available" in snap
        return {"closest":{k:snap[k] for k in ("available","timestamp","status","url") if k in snap} if snap else None}
    assert isinstance(d,dict) and isinstance(d.get("response"),dict)
    response=d["response"];n=response["numFound"];rows=response["docs"]
    assert isinstance(n,int) and n>=0 and isinstance(rows,list) and len(rows)<=100
    assert all(isinstance(x,dict) and "identifier" in x for x in rows)
    return {"num_found":n,"rows":[{k:x[k] for k in ("identifier","title","date") if k in x} for x in rows],"limit_reached":n>len(rows)}
def request(job):
    kind,target,url=job
    row={"kind":kind,"target_or_query":target,"request_url":url,"original_payload_downloaded":False}
    try:
        op=urllib.request.build_opener(ArchiveRedirect())
        req=urllib.request.Request(url,headers={"User-Agent":"stoneage-rebuild-archaeology/1.0","Accept":"application/json,text/plain;q=0.9"})
        with op.open(req,timeout=25) as r:
            raw=r.read(CAP+1);row.update(http_status=r.status,final_url=r.geturl(),response_bytes=len(raw),response_sha256=sha(raw))
            if len(raw)>CAP:row["result"]="RESPONSE_LIMIT_EXCEEDED";return row
        row["metadata"]=parse(kind,raw)
        row["result"]="METADATA_PARSED" if row["metadata"].get("format")!="EMPTY_BODY_NOT_CONFIRMED" else "EMPTY_BODY_NOT_CONFIRMED"
    except urllib.error.HTTPError as e:
        raw=e.read(CAP+1);row.update(result="HTTP_ERROR",http_status=e.code,response_bytes=len(raw),response_sha256=sha(raw))
    except (OSError,ValueError,AssertionError,TypeError,KeyError) as e:
        row.update(result="ACCESS_OR_PARSE_ERROR",error_type=type(e).__name__,error=str(e)[:300])
    return row
def verify_inputs():
    raw=PRIOR.read_bytes();assert blob(raw)==PRIOR_BLOB
    d=json.loads(raw)
    assert tuple(x["url"] for x in d["operator_attributed_notice"]["direct_urls"])==TARGETS[:4]
    assert len(jobs())==19
def selftest():
    verify_inputs()
    assert parse("WAYBACK_CDX",b"[]")["row_count"]==0
    assert parse("WAYBACK_AVAILABLE",b'{"archived_snapshots":{}}')["closest"] is None
    assert parse("ARQUIVO_CDX",b"")["format"]=="EMPTY_BODY_NOT_CONFIRMED"
    assert parse("IA_CATALOGUE",b'{"response":{"numFound":0,"docs":[]}}')["num_found"]==0
    assert all(urllib.parse.urlsplit(x[2]).hostname in HOSTS for x in jobs())
    print("PET104_SELFTEST_OK")
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path);p.add_argument("--self-test",action="store_true");a=p.parse_args();selftest()
    if a.self_test:return
    if not a.output:p.error("--output required")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        rows=list(ex.map(request,jobs()))
    from collections import Counter
    summary=dict(Counter(x["result"] for x in rows))
    report=dict(schema="stoneage.pet104.cn70.archive_index.r1",prior_git_blob=PRIOR_BLOB,queries=len(rows),results=rows,summary=summary,scope="Bounded metadata queries only, no original game payload, no direct historical IP requests, no official field closures.",original_payloads=0,official_closures=0)
    a.output.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("PET104_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    for x in rows:
        m=x.get("metadata",{})
        print("PET104_RESULT="+json.dumps({"kind":x["kind"],"target":x["target_or_query"],"result":x["result"],"status":x.get("http_status"),"rows":m.get("row_count"),"num_found":m.get("num_found"),"closest":m.get("closest")},ensure_ascii=False),flush=True)
    print("PET104_REPORT_SHA256="+sha(a.output.read_bytes()),flush=True)
if __name__=="__main__":main()
