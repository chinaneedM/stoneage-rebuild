"""PET112: independent PET111 custody and two source-qualified torrent archive checks."""
import argparse
import json
from pathlib import Path
import urllib.parse
import urllib.request
import zipfile
from tools import stoneage_pet_high_first_104_cn70_archive_index as idx
from tools import stoneage_pet_high_first_107_cn70_torrent_metadata as tor
from tools import stoneage_pet_high_first_109_cn75_custody as prior
from tools import stoneage_pet_high_first_111_cn75_patch_context as p111
P=idx.ROOT/"research/pets"
R111=P/"PET-HIGH-FIRST-111-CN75-PATCH-CONTEXT-R1.json"
R112=P/"PET-HIGH-FIRST-112-CN75-TORRENT-PREFLIGHT-R1.json"
ZSHA="9f3c8b0546cc393e530491c53952d1f87af00183fed7f05d40bde83d37f7b803"
SHA="8cb0bab0d376cd6ceb93e043d11a2ba80cacf5ab0ac05daccd33d70d02632343"
TARGETS=("http://210.51.191.171/StoneAge75.rar.torrent","http://219.238.234.163/StoneAge75.rar.torrent")
CAP=262144
def verify(artifact):
    z=artifact.read_bytes();assert len(z)==11924 and idx.sha(z)==ZSHA
    with zipfile.ZipFile(artifact) as f:
        assert f.namelist()==["pet111.json"]
        raw=f.read("pet111.json")
    assert idx.sha(raw)==SHA
    d=json.loads(raw)
    assert d["prior_report_git_blob"]=="0ffc934e30f783105198db8cff03fad96df74a4a"
    assert len(d["official_context"])==2 and all(x["result"]=="HTML_METADATA_PARSED" for x in d["official_context"])
    for x,u in zip(d["official_context"],TARGETS):
        assert any(v["url"]==u and v["file_extension_candidate"] for v in x["links"])
    assert [x["metadata"]["row_count"] for x in d["portal_indexes"]]==[6,19,2,0,9,4,5,6,5]
    assert len(d["portal_context"])==8 and sum(x["result"]=="HTML_METADATA_PARSED" for x in d["portal_context"])==6
    assert d["official_closures"]==d["full_originals_verified"]==0 and not d["original_assets_published"]
    R111.write_bytes(raw)
    return d
def jobs():
    return [("WAYBACK_CDX",t,"https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode(dict(url=t,output="json",**{"from":"2004","to":"2008"},limit=100,fl="timestamp,original,statuscode,mimetype,digest,length"))) for t in TARGETS]
def select(rows):
    seen=set();out=[]
    for a in rows:
        if a["result"]!="METADATA_PARSED":continue
        for x in a["metadata"]["rows"]:
            if x["statuscode"]!="200" or p111.norm(x["original"])!=p111.norm(a["target_or_query"]):continue
            if not (len(x["timestamp"])==14 and x["timestamp"].isdigit()):continue
            key=x["digest"]
            if key=="-":key=(x["timestamp"],x["original"])
            if key in seen:continue
            seen.add(key);out.append(x)
    return out[:6],len(out)
def capture(x):
    u="https://web.archive.org/web/"+x["timestamp"]+"id_/"+x["original"]
    row=dict(cdx=x,replay_url=u)
    try:
        q=urllib.request.Request(u,headers={"Accept-Encoding":"identity","User-Agent":"stoneage-rebuild-archaeology/1.0"})
        with urllib.request.build_opener(idx.ArchiveRedirect()).open(q,timeout=30) as f:
            raw=f.read(CAP+1)
            row.update(status=f.status,response_bytes=len(raw),response_sha256=idx.sha(raw),final_url=f.geturl(),content_type=f.headers.get("Content-Type"))
        if len(raw)>CAP:row["result"]="LIMIT_EXCEEDED";return row
        d=tor.metadata(raw)
        assert d["name"].casefold()=="stoneage75.rar" and d["mode"]=="SINGLE_FILE" and d["declared_total_bytes"]>0
        row.update(result="TORRENT_METADATA_VALID",metadata=d)
    except (OSError,ValueError,AssertionError,KeyError,IndexError,TypeError) as e:row.update(result="ACCESS_OR_PARSE_ERROR",error_type=type(e).__name__,error=str(e)[:300])
    return row
def main():
    a=argparse.ArgumentParser();a.add_argument("--artifact",type=Path,required=True);args=a.parse_args()
    tor.selftest();verify(args.artifact)
    rows=[idx.request(j) for j in jobs()]
    choices,n=select(rows)
    result=dict(schema="stoneage.pet112.cn75.torrent_preflight.r1",prior_source_head="4728aac0668ebd6dee23287c326049b1194cdb80",prior_run=45816629353,prior_job=139897925211,prior_artifact=15114803857,prior_zip_bytes=11924,prior_zip_sha256=ZSHA,prior_report_sha256=SHA,prior_report_git_blob=idx.blob(R111.read_bytes()),index_results=rows,unique_http_success_candidates=n,replay_cap=6,replays=[capture(x) for x in choices],full_originals_verified=0,official_closures=0,original_assets_published=False,peer_or_tracker_contacted=False)
    R112.write_bytes(prior.dump(result))
    print("PET112_RESULT="+json.dumps(result,ensure_ascii=False,sort_keys=True),flush=True)
    print("PET112_REPORT_SHA256="+idx.sha(R112.read_bytes()),flush=True)
if __name__=="__main__":main()
