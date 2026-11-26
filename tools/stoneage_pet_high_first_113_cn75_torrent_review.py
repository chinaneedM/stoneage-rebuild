"""PET113: verify archived torrent receipts and diagnose second 7.5 metadata without relaxing validation."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import urllib.request
import zipfile
from tools import stoneage_pet_high_first_104_cn70_archive_index as idx
from tools import stoneage_pet_high_first_107_cn70_torrent_metadata as tor
from tools import stoneage_pet_high_first_109_cn75_custody as prior
R=idx.ROOT/"research/pets/PET-HIGH-FIRST-112-CN75-TORRENT-PREFLIGHT-R1.json"
SHA="cd92ad584fa70bf41113ab0587807fa966f3775d4ff45edc8ca2d4f8f2639bdf"
ZSHA="67f22d7de1ff497b65f9dd28127c12d936657efeb5200fefa5a003afa70935fe"
def verify(path):
    raw=path.read_bytes();assert len(raw)==1954 and idx.sha(raw)==ZSHA
    with zipfile.ZipFile(path) as f:
        assert f.namelist()==[R.name]
        data=f.read(R.name)
    assert data==R.read_bytes() and idx.sha(data)==SHA and idx.blob(data)=="a5dc9d2bdae37f36b3c4900d701f9cbe9c8bae1c"
    d=json.loads(data)
    assert [x["metadata"]["row_count"] for x in d["index_results"]]==[3,4]
    assert len(d["replays"])==2 and d["unique_http_success_candidates"]==2
    a,b=d["replays"]
    assert a["result"]=="TORRENT_METADATA_VALID" and a["metadata"]["declared_total_bytes"]==770632364 and a["metadata"]["piece_count"]==1470
    assert b["result"]=="ACCESS_OR_PARSE_ERROR" and b["error_type"]=="AssertionError" and b["response_bytes"]==29885
    assert not d["peer_or_tracker_contacted"] and d["full_originals_verified"]==d["official_closures"]==0 and not d["original_assets_published"]
    return d
def examine(raw):
    d={"bencode_valid":False,"metadata_consistent":False,"expected_single_rar":False}
    try:
        top,info,encoded=tor.parse(raw)
        d.update(bencode_valid=True,info_bencode_sha256=idx.sha(encoded))
    except (AssertionError,ValueError,KeyError,IndexError,TypeError) as e:
        d.update(failure_stage="BENCODE_STRICT",error_type=type(e).__name__)
        return d
    try:
        name=tor.label(info[b"name"])
        d.update(name_candidate=name[:300],name_matches_expected=name.casefold()=="stoneage75.rar",has_files=b"files" in info,has_length=b"length" in info)
        if isinstance(info.get(b"length"),int):d["declared_length_candidate"]=info[b"length"]
        if isinstance(info.get(b"piece length"),int):d["piece_length_candidate"]=info[b"piece length"]
        if isinstance(info.get(b"pieces"),bytes):d["piece_hash_bytes"]=len(info[b"pieces"])
        meta=tor.metadata(raw)
        d.update(metadata_consistent=True,expected_single_rar=meta["name"].casefold()=="stoneage75.rar" and meta["mode"]=="SINGLE_FILE" and meta["declared_total_bytes"]>0,metadata=meta)
        if not d["expected_single_rar"]:d["failure_stage"]="EXPECTED_SINGLE_RAR_IDENTITY"
    except (AssertionError,ValueError,KeyError,IndexError,TypeError) as e:
        d.update(failure_stage="METADATA_CONSISTENCY",error_type=type(e).__name__)
    return d
def capture(x):
    row=dict(cdx=x["cdx"],replay_url=x["replay_url"],prior_response_sha256=x["response_sha256"])
    try:
        q=urllib.request.Request(x["replay_url"],headers={"Accept-Encoding":"identity","User-Agent":"stoneage-rebuild-archaeology/1.0"})
        with urllib.request.build_opener(idx.ArchiveRedirect()).open(q,timeout=30) as f:
            raw=f.read(262145);row.update(status=f.status,response_bytes=len(raw),response_sha256=idx.sha(raw))
        assert len(raw)<=262144 and len(raw)==x["response_bytes"] and idx.sha(raw)==x["response_sha256"]
        digest=base64.b32encode(hashlib.sha1(raw).digest()).decode("ascii")
        row.update(result="EXACT_REPLAY_VERIFIED",cdx_sha1_base32_recomputed=digest,cdx_digest_matches=digest==x["cdx"]["digest"],**examine(raw))
    except (OSError,AssertionError,ValueError) as e:
        row.update(result="ACCESS_OR_IDENTITY_ERROR",error_type=type(e).__name__,error=str(e)[:200])
    return row
def selftest():
    tor.selftest()
    t=b"d4:infod6:lengthi3e4:name1:x12:piece lengthi4e6:pieces20:"+b"a"*20+b"ee"
    d=examine(t);assert d["metadata_consistent"] and not d["expected_single_rar"] and d["failure_stage"]=="EXPECTED_SINGLE_RAR_IDENTITY"
    assert not examine(t+b"x")["bencode_valid"]
    print("PET113_SELFTEST_OK")
def main():
    p=argparse.ArgumentParser();p.add_argument("--artifact",type=Path,required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args()
    selftest();d=verify(a.artifact)
    rows=[capture(x) for x in d["replays"]]
    report=dict(schema="stoneage.pet113.cn75.torrent_identity_review.r1",prior_report_git_blob=idx.blob(R.read_bytes()),prior_report_sha256=SHA,prior_artifact=15116282300,prior_zip_sha256=ZSHA,results=rows,original_client_verified=False,original_assets_published=False,peer_or_tracker_contacted=False,official_closures=0)
    a.output.write_bytes(prior.dump(report))
    print("PET113_RESULT="+json.dumps(report,ensure_ascii=False,sort_keys=True),flush=True)
    print("PET113_REPORT_SHA256="+idx.sha(a.output.read_bytes()),flush=True)
if __name__=="__main__":main()
