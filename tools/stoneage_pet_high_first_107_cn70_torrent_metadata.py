"""PET107: verify PET106 artifact, parse complete stored torrent metadata only."""
import argparse
import hashlib
import json
import math
import struct
import urllib.request
import urllib.parse
import zipfile
import zlib
from pathlib import Path
from tools import stoneage_pet_high_first_104_cn70_archive_index as idx
from tools import stoneage_pet_high_first_104_accept as accept
ROOT=idx.ROOT
P=ROOT/"research/pets/PET-HIGH-FIRST-106-CN70-RAR4-CAPTURE-R1.json"
REPORT_SHA="24377de7a7e3682b9401a2f1f96d517836aad86cbf9358a8f0017bb595e73885"
ZIP_SHA="c35d0580a8df68d6a74f3d281a2d46fe209f8d843ce14dfc8e95b3bfc48603bf"
CAP_SHA="d9693c19c66db2109031ee2811732ede3d4d8e0586aa84bce948bc3b04bd1011"
def verify(artifact):
    z=artifact.read_bytes()
    assert len(z)==1370 and idx.sha(z)==ZIP_SHA
    with zipfile.ZipFile(artifact) as f:
        assert f.namelist()==["pet106.json"]
        raw=f.read("pet106.json")
    assert idx.sha(raw)==REPORT_SHA and raw==P.read_bytes()
    return json.loads(raw)
def parse(raw):
    at=0;nodes=0;info_span=None
    def one(depth=0):
        nonlocal at,nodes,info_span
        nodes+=1
        assert nodes<=20000 and depth<=32 and at<len(raw)
        ch=raw[at:at+1]
        if ch==b"i":
            end=raw.index(b"e",at+1);s=raw[at+1:end]
            assert len(s)<=24
            v=int(s);assert str(v).encode()==s
            at=end+1;return v
        if ch in (b"l",b"d"):
            at+=1
            if ch==b"l":
                out=[]
                while raw[at:at+1]!=b"e":out.append(one(depth+1))
            else:
                out={}
                while raw[at:at+1]!=b"e":
                    k=one(depth+1);assert isinstance(k,bytes) and k not in out
                    start=at;v=one(depth+1);out[k]=v
                    if depth==0 and k==b"info":info_span=(start,at)
            at+=1;return out
        assert ch.isdigit()
        colon=raw.index(b":",at);s=raw[at:colon];assert 1<=len(s)<=8
        n=int(s);assert str(n).encode()==s and n>=0 and colon+1+n<=len(raw)
        at=colon+1+n;return raw[colon+1:at]
    top=one();assert at==len(raw) and isinstance(top,dict) and info_span
    info=top[b"info"];assert isinstance(info,dict)
    return top,info,raw[info_span[0]:info_span[1]]
def label(b):
    assert isinstance(b,bytes) and len(b)<=4096
    for e in ("utf-8","gb18030"):
        try:return b.decode(e)
        except UnicodeDecodeError:pass
    return b.decode("ascii","backslashreplace")
def metadata(raw):
    top,info,encoded=parse(raw);name=label(info[b"name"])
    if b"files" in info:
        assert b"length" not in info
        files=[dict(path=[label(p) for p in f[b"path"]],length=f[b"length"]) for f in info[b"files"]]
        mode="MULTI_FILE"
    else:
        files=[dict(path=[name],length=info[b"length"])];mode="SINGLE_FILE"
    assert 0<len(files)<=1000 and all(isinstance(f["length"],int) and f["length"]>=0 for f in files)
    total=sum(f["length"] for f in files);piece=info[b"piece length"];pieces=info[b"pieces"]
    assert isinstance(piece,int) and piece>0 and isinstance(pieces,bytes) and len(pieces)%20==0
    count=len(pieces)//20
    assert count==(total+piece-1)//piece
    return dict(name=name,mode=mode,files=files,declared_total_bytes=total,piece_length=piece,piece_count=count,piece_hashes_sha256=idx.sha(pieces),info_bencode_sha256=idx.sha(encoded),torrent_metadata_sha256=idx.sha(raw),torrent_metadata_bytes=len(raw),creation_date_unverified=top.get(b"creation date") if isinstance(top.get(b"creation date"),int) else None,declared_lengths_not_original_payload_verified=True,peer_or_tracker_contacted=False)
def selftest():
    t=b"d4:infod6:lengthi3e4:name1:x12:piece lengthi4e6:pieces20:"+b"a"*20+b"ee"
    d=metadata(t);assert d["declared_total_bytes"]==3 and d["piece_count"]==1
    try:parse(t+b"x")
    except AssertionError:pass
    else:raise AssertionError("trailing data accepted")
    print("PET107_SELFTEST_OK",flush=True)
def main():
    p=argparse.ArgumentParser();p.add_argument("--artifact",type=Path);p.add_argument("--output",type=Path);p.add_argument("--self-test",action="store_true");a=p.parse_args();selftest()
    if a.self_test:return
    assert a.artifact and a.output
    prev=verify(a.artifact);rows=prev["structure"]["blocks"];member=rows[1]
    assert member["filename_candidate"]=="STONEAGE7.rar.torrent" and member["method"]=="0x30" and member["packed_bytes"]==member["unpacked_bytes"]==34183
    assert not member["encrypted"] and not member["split_before"] and not member["split_after"]
    out=dict(schema="stoneage.pet107.cn70.torrent_metadata.r1",pet106_source_head="f2a0d9b2385c1833f2b471f96ce2c526c75e48cc",pet106_run=45814573053,pet106_job=139890845259,pet106_artifact=15115016195,pet106_zip_sha256=ZIP_SHA,pet106_report_sha256=REPORT_SHA,pet106_report_git_blob=idx.blob(P.read_bytes()),full_original_client_verified=False,original_assets_published=False,official_closures=0)
    try:
        u="https://web.archive.org/web/20040508172441id_/http://210.51.17.236:80/STONEAGE7.rar"
        q=urllib.request.Request(u,headers={"Range":"bytes=0-34267","Accept-Encoding":"identity","User-Agent":"stoneage-rebuild-archaeology/1.0"})
        with urllib.request.build_opener(idx.ArchiveRedirect()).open(q,timeout=30) as f:raw=f.read(34269)
        assert len(raw)==34268 and idx.sha(raw)==CAP_SHA
        start=member["offset"]+member["header_bytes"];torrent=raw[start:start+member["packed_bytes"]]
        assert len(torrent)==34183 and f"{zlib.crc32(torrent)&0xffffffff:08x}"==member["file_crc32"]
        out.update(torrent_result="EXACT_STORED_MEMBER_CRC_VERIFIED",member_crc32=member["file_crc32"],metadata=metadata(torrent))
    except (OSError,ValueError,AssertionError,KeyError,IndexError,TypeError) as e:out.update(torrent_result="ACCESS_OR_PARSE_ERROR",error_type=type(e).__name__,error=str(e)[:300])
    # Only replay the three independently observed HTML archive captures.
    choices=[]
    for x in prev["new_route_index"]["metadata"]["rows"]:
        assert x["statuscode"]=="200" and x["mimetype"]=="text/html" and urllib.parse.urlsplit(x["original"]).hostname=="down.17173.com"
        choices.append(dict(kind="PAGE",target=prev["new_route_index"]["target_or_query"],timestamp=x["timestamp"],original=x["original"],cdx_mime=x["mimetype"],cdx_digest=x["digest"],cdx_length=x["length"],replay_url="https://web.archive.org/web/"+x["timestamp"]+"id_/"+x["original"]))
    assert len(choices)==3
    out["new_route_page_replays"]=[accept.replay(x) for x in choices]
    a.output.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("PET107_RESULT="+json.dumps(out,ensure_ascii=False,sort_keys=True),flush=True)
    print("PET107_REPORT_SHA256="+idx.sha(a.output.read_bytes()),flush=True)
if __name__=="__main__":main()
