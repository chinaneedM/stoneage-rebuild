"""PET116: independently verify PET115 and inspect exact historical CN85 file archive indices."""
import argparse,json,urllib.parse,urllib.request,urllib.error,zipfile
from pathlib import Path
from tools import stoneage_pet_high_first_104_cn70_archive_index as idx
from tools import stoneage_pet_high_first_104_accept as pre
from tools import stoneage_pet_high_first_109_cn75_custody as prior
P=idx.ROOT/"research/pets"
R=P/"PET-HIGH-FIRST-115-CN85-OPERATOR-ARCHIVE-R1.json"
R114=P/"PET-HIGH-FIRST-114-CN85-ZOL-ARCHIVE-R1.json"
SHA="4b628dd0364231d6a5d301e299b84ba79869da5b1cd1c98a23fe251c18f886ce"
ZSHA="33fa9e15d50b0b453fda4462cf27aff3b2602ce63d5bbc1b6f2bb959c8778193"
ORDER=("http://download1.cinsgame.com/StoneAge.rar","http://update5.cinsgame.com/saupdate/StoneAge.exe","http://download1.cinsgame.com/StoneAge.zip","http://download1.cinsgame.com/patch_1.00.003.exe","http://download1.cinsgame.com/patch_1.00.002.exe","http://download1.cinsgame.com/patch_1.00.001.exe","http://download1.cinsgame.com/patch_8.5.00.001.exe","http://download1.cinsgame.com/StoneAge_20110713.exe","http://download1.cinsgame.com/StoneAge_20110622_03.exe","http://download1.cinsgame.com/patch20101113_01.exe","http://download.cins.cn/sa_cb1.exe","http://download1.cins.cn/sa_cb1.exe","http://download2.cins.cn/sa_cb1.exe","http://cdn2.download.17173.com/45aa8e12ce3be66c144176a55dbb7647/other/17173_sa_cb11111.exe")
CAP=65536
def verify(path):
    z=path.read_bytes();assert len(z)==8053 and idx.sha(z)==ZSHA
    with zipfile.ZipFile(path) as f:
        assert f.namelist()==[R.name];raw=f.read(R.name)
    assert raw==R.read_bytes() and idx.sha(raw)==SHA and idx.blob(raw)=="d0b5c972155e2755ec01aaa20fdde838572fd115"
    d=json.loads(raw);assert idx.blob(R114.read_bytes())==d["prior_report_git_blob"]=="ebd8f32786c0fa1d1d399a6967102055e0fbe0cd"
    assert [x["metadata"]["row_count"] for x in d["indexes"]]==[21,100,20,26,0,0]
    assert len(d["captures"])==9 and sum(x["result"]=="HTML_METADATA_PARSED" for x in d["captures"])==5
    rows=d["captures"][:3]
    assert [x["cdx"]["timestamp"] for x in rows]==["20101113224132","20111014082949","20121030005014"]
    assert all(x["result"]=="HTML_METADATA_PARSED" and x["status"]==200 for x in rows)
    links={v["url"]:dict(source_capture=x["cdx"]["timestamp"],source_page_sha256=x["response_sha256"],row_version_tokens=v["row_version_tokens"],row_keywords=v["row_keywords"]) for x in rows for v in x["links"] if v["file_extension_candidate"]}
    assert len(links)==len(ORDER)==14 and set(links)==set(ORDER)
    assert links[ORDER[0]]["row_version_tokens"]==["8.5"] and links[ORDER[2]]["row_version_tokens"]==["8.5"]
    assert d["original_payloads"]==d["official_closures"]==0 and not d["original_assets_published"]
    return links
def jobs():
    return [("WAYBACK_CDX",t,"https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode(dict(url=t,output="json",**{"from":"2010","to":"2016"},limit=100,fl="timestamp,original,statuscode,mimetype,digest,length"))) for t in ORDER]
def key(url):
    u=urllib.parse.urlsplit(url)
    return (u.hostname,u.path.lower(),u.query)
def select(rows):
    chosen=[];seen=set()
    for a in rows:
        if a["result"]!="METADATA_PARSED":continue
        for x in a["metadata"]["rows"]:
            if x["statuscode"] not in ("200","206") or key(x["original"])!=key(a["target_or_query"]):continue
            if not (len(x["timestamp"])==14 and x["timestamp"].isdigit()):continue
            digest=x["digest"]
            k=digest if digest!="-" else (x["original"],x["timestamp"])
            if k in seen:continue
            seen.add(k);chosen.append(dict(target=a["target_or_query"],cdx=x))
    return chosen[:10],len(chosen)
class NoFollow(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):return None
def capture(x):
    row=dict(x);c=x["cdx"];url="https://web.archive.org/web/"+c["timestamp"]+"id_/"+c["original"]
    row["replay_url"]=url
    try:
        q=urllib.request.Request(url,headers={"Range":"bytes=0-65535","Accept-Encoding":"identity","User-Agent":"stoneage-rebuild-archaeology/1.0"})
        try:f=urllib.request.build_opener(NoFollow()).open(q,timeout=25)
        except urllib.error.HTTPError as e:f=e
        with f:
            raw=f.read(CAP);row.update(status=f.status,sample_bytes=len(raw),sample_sha256=idx.sha(raw),magic=pre.classify(raw),headers={k:f.headers.get(k) for k in ("Content-Type","Content-Length","Content-Range","X-Archive-Orig-Content-Length","X-Archive-Orig-Location","Location")})
        row["result"]="BOUNDED_RESPONSE" if row["status"] in (200,206) else "HTTP_RESPONSE_NOT_FILE"
    except (OSError,ValueError,AssertionError) as e:row.update(result="ACCESS_OR_PARSE_ERROR",error_type=type(e).__name__,error=str(e)[:250])
    row["full_original_verified"]=False
    return row
def selftest():
    assert len(ORDER)==len(set(ORDER))==14
    assert len(jobs())==14
    assert all(urllib.parse.urlsplit(j[2]).hostname=="web.archive.org" for j in jobs())
    t=ORDER[0];x=dict(timestamp="20121031000000",original=t,statuscode="200",mimetype="application/octet-stream",digest="TEST",length="123")
    a=dict(result="METADATA_PARSED",target_or_query=t,metadata=dict(rows=[x,x]))
    assert select([a])==([dict(target=t,cdx=x)],1)
    assert select([dict(a,metadata=dict(rows=[dict(x,original=ORDER[1])]))])==([],0)
    print("PET116_SELFTEST_OK")
def main():
    p=argparse.ArgumentParser();p.add_argument("--self-test",action="store_true");p.add_argument("--artifact",type=Path);p.add_argument("--output",type=Path);a=p.parse_args();selftest()
    if a.self_test:return
    assert a.artifact and a.output
    links=verify(a.artifact)
    rows=[idx.request(j) for j in jobs()];chosen,n=select(rows)
    out=dict(schema="stoneage.pet116.cn85.exact_file_archive.r1",prior_report_git_blob=idx.blob(R.read_bytes()),prior_report_sha256=SHA,prior_artifact=15116469533,prior_zip_sha256=ZSHA,source_qualified_targets=[dict(url=t,**links[t]) for t in ORDER],indexes=rows,unique_http_success_candidates=n,prefix_cap=10,prefix_results=[capture(x) for x in chosen],full_originals_verified=0,official_closures=0,original_assets_published=False,redirects_followed=False)
    a.output.write_bytes(prior.dump(out))
    print("PET116_REPORT_SHA256="+idx.sha(a.output.read_bytes()),flush=True)
    for x in rows:print("PET116_INDEX="+json.dumps(dict(target=x["target_or_query"],result=x["result"],count=x.get("metadata",{}).get("row_count")),ensure_ascii=False),flush=True)
    for x in out["prefix_results"]:print("PET116_PREFIX="+json.dumps(x,ensure_ascii=False,sort_keys=True),flush=True)
if __name__=="__main__":main()
