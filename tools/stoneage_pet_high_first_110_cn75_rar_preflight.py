"""PET110: archive-only CN7.5 exact original distribution RAR preflight."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import urllib.parse
import urllib.request
import zipfile
from tools import stoneage_pet_high_first_104_cn70_archive_index as idx
from tools import stoneage_pet_high_first_104_accept as pre
from tools import stoneage_pet_high_first_106_cn70_rar4_capture as rar
from tools import stoneage_pet_high_first_109_cn75_custody as prior
P=idx.ROOT/"research/pets"
CUST=P/"PET-HIGH-FIRST-108-CUSTODY-R1.json"
REPORT=P/"PET-HIGH-FIRST-109-CN75-BOUNDED-REPLAY-R1.json"
TARGETS=tuple("http://219.238.234."+str(i)+"/StoneAge75.rar" for i in range(161,165))
ZIP_SHA="e505227cf10c28b410063783b6d8e99c750118ff6997a0825edf11f3b032f909"
REPORT_SHA="f5051c3279caded7f3b0766d6fee917365aae82e047ecaf3fd76aae77bb147a4"
def verify(path):
    z=path.read_bytes();assert len(z)==3076 and idx.sha(z)==ZIP_SHA
    with zipfile.ZipFile(path) as f:
        assert sorted(f.namelist())==sorted([CUST.name,REPORT.name])
        assert f.read(CUST.name)==CUST.read_bytes()
        raw=f.read(REPORT.name);assert raw==REPORT.read_bytes() and idx.sha(raw)==REPORT_SHA
    d=json.loads(raw);assert len(d["attempts"])==3 and all(x["status"]==200 and x["result"]=="BOUNDED_RESPONSE" for x in d["attempts"])
    assert all(t in d["attempts"][0]["download_link_candidates"] and t in d["attempts"][1]["download_link_candidates"] for t in TARGETS)
    assert TARGETS[0] in d["attempts"][2]["download_link_candidates"]
    assert not d["original_assets_published"] and d["official_closures"]==d["original_payloads"]==0
    assert len(d["archive_catalogue_candidates"])==32
    return d
def jobs():
    return [("WAYBACK_CDX",t,"https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode(dict(url=t,output="json",**{"from":"2004","to":"2008"},limit=100,fl="timestamp,original,statuscode,mimetype,digest,length"))) for t in TARGETS]
def select(rows):
    out=[];seen=set()
    for a in rows:
        if a["result"]!="METADATA_PARSED":continue
        t=a["target_or_query"];u=urllib.parse.urlsplit(t)
        for r in a["metadata"]["rows"]:
            o=urllib.parse.urlsplit(r["original"])
            if r["statuscode"] not in ("200","206") or o.hostname!=u.hostname or o.path.lower()!=u.path.lower() or o.query or o.username or o.password:continue
            if not (len(r["timestamp"])==14 and r["timestamp"].isdigit()):continue
            key=r["digest"]
            if key=="-":key=(r["original"],r["timestamp"])
            if key in seen:continue
            seen.add(key)
            out.append(dict(kind="RAR_PREFIX",target=t,timestamp=r["timestamp"],original=r["original"],cdx_mime=r["mimetype"],cdx_digest=r["digest"],cdx_length=r["length"],replay_url="https://web.archive.org/web/"+r["timestamp"]+"id_/"+r["original"]))
    return out[:8],len(out)
def prefix(x):
    row=dict(x)
    try:
        q=urllib.request.Request(x["replay_url"],headers={"Range":"bytes=0-65535","Accept-Encoding":"identity","User-Agent":"stoneage-rebuild-archaeology/1.0"})
        with urllib.request.build_opener(idx.ArchiveRedirect()).open(q,timeout=30) as f:
            raw=f.read(65536)
            row.update(result="BOUNDED_RESPONSE",status=f.status,final_url=f.geturl(),sample_bytes=len(raw),sample_sha256=idx.sha(raw),magic=pre.classify(raw),headers={k:f.headers.get(k) for k in ("Content-Length","Content-Range","Content-Type","X-Archive-Orig-Content-Length","Memento-Datetime")})
        if row["magic"]=="RAR4_MAGIC":row["rar4_structure"]=rar.scan(raw)
    except (OSError,ValueError,AssertionError) as e:row.update(result="ACCESS_OR_PARSE_ERROR",error_type=type(e).__name__,error=str(e)[:300])
    row["full_original_verified"]=False
    return row
def main():
    p=argparse.ArgumentParser();p.add_argument("--artifact",type=Path,required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args();verify(a.artifact)
    rows=[idx.request(j) for j in jobs()]
    choices,n=select(rows)
    out=dict(schema="stoneage.pet110.cn75.archive_rar_preflight.r1",prior_git_blob=idx.blob(REPORT.read_bytes()),prior_report_sha256=REPORT_SHA,prior_artifact=15116635005,prior_zip_sha256=ZIP_SHA,targets=list(TARGETS),index_results=rows,unique_http_success_digest_candidates=n,prefix_limit=8,prefix_results=[prefix(x) for x in choices],official_closures=0,full_originals_verified=0,original_assets_published=False)
    a.output.write_bytes(prior.dump(out))
    print("PET110_RESULT="+json.dumps(out,ensure_ascii=False,sort_keys=True),flush=True)
    print("PET110_REPORT_SHA256="+idx.sha(a.output.read_bytes()),flush=True)
if __name__=="__main__":main()
