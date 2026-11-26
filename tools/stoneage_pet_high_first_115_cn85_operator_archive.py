"""PET115: preserve PET114 negative index; examine dated operator archive routes."""
import argparse,json
from pathlib import Path
import urllib.parse,zipfile
from tools import stoneage_pet_high_first_104_cn70_archive_index as idx
from tools import stoneage_pet_high_first_109_cn75_custody as prior
from tools import stoneage_pet_high_first_114_cn85_zol_archive as p114
P=idx.ROOT/"research/pets"
R114=P/"PET-HIGH-FIRST-114-CN85-ZOL-ARCHIVE-R1.json"
R115=P/"PET-HIGH-FIRST-115-CN85-OPERATOR-ARCHIVE-R1.json"
SHA="0d0b9aa349d43169cf60bc6638f81578cf66b964755019eab174763ba073a28b"
ZSHA="c93f494a2ff2bfce5913867dfc9ab9f874801181a2961e24a8593606256d9571"
TARGETS=("http://sa.cins.cn/indownload.html","http://sa.cins.cn/","http://download.17173.com/10939/","http://download.17173.com/27/","http://news.yzz.cn/internalnews/2010,225312_2.shtml","http://news.yzz.cn/internalnews/2011,261027_5.shtml")
def verify(path):
    z=path.read_bytes();assert len(z)==914 and idx.sha(z)==ZSHA
    with zipfile.ZipFile(path) as f:
        assert f.namelist()==["pet114.json"];raw=f.read("pet114.json")
    assert idx.sha(raw)==SHA
    d=json.loads(raw)
    assert d["targets"]==list(p114.TARGETS) and len(d["indexes"])==6
    assert all(x["result"]=="METADATA_PARSED" and x["metadata"]["row_count"]==0 and not x["metadata"]["rows"] for x in d["indexes"])
    assert d["captures"]==[] and d["original_payloads"]==d["official_closures"]==0 and not d["redirects_followed"]
    R114.write_bytes(raw)
def jobs():
    return [("WAYBACK_CDX",t,"https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode(dict(url=t,output="json",**{"from":"2010","to":"2015"},limit=100,fl="timestamp,original,statuscode,mimetype,digest,length"))) for t in TARGETS]
def select(rows):
    # Fixed windows cover pressure test, January 2011 test, 2011 and 2012 public builds.
    out=[]
    for a in rows:
        if a["result"]!="METADATA_PARSED":continue
        t=a["target_or_query"]
        eligible=[x for x in a["metadata"]["rows"] if p114.norm(x["original"])==p114.norm(t) and x["statuscode"] in ("200","301","302","303","307","308") and len(x["timestamp"])==14 and x["timestamp"].isdigit()]
        seen=set()
        dates=("20101111","20110113","20111002","20121009") if t==TARGETS[0] else ("20101111","20110622")
        for date in dates:
            if not eligible:break
            from datetime import datetime
            def distance(x):return abs((datetime.strptime(x["timestamp"][:8],"%Y%m%d")-datetime.strptime(date,"%Y%m%d")).days)
            x=min(eligible,key=lambda x:(distance(x),x["timestamp"]))
            if x["digest"] in seen:continue
            seen.add(x["digest"]);out.append(x)
    assert len(out)<=14
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument("--artifact",type=Path,required=True);a=p.parse_args()
    verify(a.artifact)
    rows=[idx.request(j) for j in jobs()]
    pages=[p114.capture(x) for x in select(rows)]
    d=dict(schema="stoneage.pet115.cn85.operator_archive.r1",prior_report_git_blob=idx.blob(R114.read_bytes()),prior_report_sha256=SHA,prior_artifact=15117371023,prior_zip_sha256=ZSHA,targets=list(TARGETS),indexes=rows,captures=pages,original_payloads=0,official_closures=0,original_assets_published=False,redirects_followed=False)
    R115.write_bytes(prior.dump(d))
    print("PET115_REPORT_SHA256="+idx.sha(R115.read_bytes()),flush=True)
    for x in rows:print("PET115_INDEX="+json.dumps(dict(target=x["target_or_query"],result=x["result"],count=x.get("metadata",{}).get("row_count")),ensure_ascii=False),flush=True)
    for x in pages:print("PET115_CAPTURE="+json.dumps({k:v for k,v in x.items() if k!="links"}|{"file_links":[v for v in x.get("links",[]) if v["file_extension_candidate"] or "download" in v["url"].lower() and "cins.cn" in v["url"].lower()]},ensure_ascii=False,sort_keys=True),flush=True)
if __name__=="__main__":main()
