"""PET106: inspect the actually archived 34,268-byte RAR4 response, not a full client."""
import argparse
import json
import struct
import urllib.request
import urllib.parse
import zlib
from pathlib import Path
from tools import stoneage_pet_high_first_104_cn70_archive_index as idx

P=idx.ROOT/"research/pets/PET-HIGH-FIRST-105-CN70-ARCHIVE-REPLAY-PREFLIGHT-R1.json"
PRIOR="802a6200640abb4721c07959118c01fffaf42eb0"
SHA="d9693c19c66db2109031ee2811732ede3d4d8e0586aa84bce948bc3b04bd1011"
LINK="http://down.17173.com/index.php?file=shiqi/StoneAge70.rar"
def scan(raw):
    assert raw.startswith(b"Rar!\x1a\x07\x00")
    pos=7
    rows=[]
    stop="END_OF_CAPTURE_WITHOUT_END_HEADER"
    while pos<len(raw):
        if len(raw)-pos<7:
            stop="PARTIAL_BLOCK_HEADER";break
        crc,typ,flags,head=struct.unpack_from("<HBHH",raw,pos)
        if head<7 or pos+head>len(raw):
            stop="INVALID_OR_PARTIAL_HEADER_SIZE";break
        h=raw[pos:pos+head]
        if zlib.crc32(h[2:])&65535!=crc:
            stop="HEADER_CRC_MISMATCH";break
        if flags&0x8000 and head<11:
            stop="PARTIAL_LONG_BLOCK_HEADER";break
        size=struct.unpack_from("<I",h,7)[0] if flags&0x8000 else 0
        row=dict(offset=pos,type=hex(typ),flags=hex(flags),header_bytes=head,header_crc_valid=True)
        if typ==0x74:
            if head<32:
                stop="PARTIAL_FILE_HEADER";break
            pack,unp,host,fcrc,ftime,version,method,nlen,attr=struct.unpack_from("<IIBIIBBHI",h,7)
            npos=32
            if flags&0x100:
                if head<40:
                    stop="PARTIAL_LARGE_FILE_HEADER";break
                hp,hu=struct.unpack_from("<II",h,32)
                pack|=hp<<32;unp|=hu<<32;npos=40
            if npos+nlen>head:
                stop="PARTIAL_FILENAME";break
            name=h[npos:npos+nlen].split(b"\0",1)[0]
            try: label=name.decode("gb18030")
            except UnicodeDecodeError: label=name.decode("ascii","backslashreplace")
            size=pack
            row.update(filename_candidate=label,filename_hex=name.hex(),packed_bytes=pack,unpacked_bytes=unp,method=hex(method),file_crc32=f"{fcrc:08x}",split_before=bool(flags&1),split_after=bool(flags&2),encrypted=bool(flags&4))
        data_start=pos+head
        row.update(declared_data_bytes=size,available_data_bytes=min(size,len(raw)-data_start),complete_data_extent=data_start+size<=len(raw))
        rows.append(row)
        if typ==0x7b:
            stop="END_HEADER_PRESENT";break
        if data_start+size>len(raw):
            stop="DECLARED_BLOCK_EXTENDS_BEYOND_CAPTURE";break
        pos=data_start+size
    return dict(blocks=rows,stop=stop,capture_bytes=len(raw),full_original_client_verified=False,member_data_crc_verified=False)
def selftest():
    def hdr(t,flags,payload):
        body=struct.pack("<BHH",t,flags,7+len(payload))+payload
        return struct.pack("<H",zlib.crc32(body)&65535)+body
    sig=b"Rar!\x1a\x07\x00"
    name=b"test.dat"
    f=struct.pack("<IIBIIBBHI",100,200,2,0,0,20,0x30,len(name),0)+name
    x=scan(sig+hdr(0x73,0,b"\0"*6)+hdr(0x74,0x8000,f)+b"abc")
    assert x["stop"]=="DECLARED_BLOCK_EXTENDS_BEYOND_CAPTURE"
    assert x["blocks"][1]["packed_bytes"]==100 and x["blocks"][1]["available_data_bytes"]==3
    assert scan(sig+hdr(0x7b,0,b""))["stop"]=="END_HEADER_PRESENT"
    assert scan(sig+b"abcdefg")["stop"]=="INVALID_OR_PARTIAL_HEADER_SIZE"
    print("PET106_SELFTEST_OK")
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--output",type=Path);ap.add_argument("--self-test",action="store_true");a=ap.parse_args();selftest()
    if a.self_test:return
    assert a.output
    raw_report=P.read_bytes();assert idx.blob(raw_report)==PRIOR
    prior=json.loads(raw_report)
    hits=[x for x in prior["results"] if x["kind"]=="RAR_PREFIX" and x["sample_sha256"]==SHA]
    assert len(hits)==3 and all(x["sample_bytes"]==34268 for x in hits)
    assert any(LINK in x.get("download_link_candidates",[]) for x in prior["results"])
    out=dict(schema="stoneage.pet106.cn70.rar4_capture_structure.r1",prior_blob=PRIOR,expected_capture_sha256=SHA,original_assets_published=False,full_original_client_verified=False,official_closures=0)
    try:
        u=hits[0]["replay_url"]
        assert urllib.parse.urlsplit(u).hostname=="web.archive.org"
        req=urllib.request.Request(u,headers={"Range":"bytes=0-34267","Accept-Encoding":"identity","User-Agent":"stoneage-rebuild-archaeology/1.0"})
        with urllib.request.build_opener(idx.ArchiveRedirect()).open(req,timeout=30) as f:
            raw=f.read(34269);out.update(response_status=f.status,response_bytes=len(raw),response_sha256=idx.sha(raw),response_range=f.headers.get("Content-Range"))
        if len(raw)==34268 and idx.sha(raw)==SHA:
            out["structure"]=scan(raw);out["capture_result"]="EXACT_CAPTURE_REPLAYED"
        else:out["capture_result"]="REPLAY_MISMATCH"
    except (OSError,ValueError,AssertionError) as e:out.update(capture_result="ACCESS_OR_PARSE_ERROR",error_type=type(e).__name__,error=str(e)[:300])
    # Only a new, exact archived distribution URL; no live host request.
    q="https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode({"url":LINK,"output":"json","from":"2003","to":"2008","limit":100,"fl":"timestamp,original,statuscode,mimetype,digest,length"})
    out["new_route_index"]=idx.request(("WAYBACK_CDX",LINK,q))
    a.output.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("PET106_RESULT="+json.dumps(out,ensure_ascii=False,sort_keys=True),flush=True)
    print("PET106_REPORT_SHA256="+idx.sha(a.output.read_bytes()),flush=True)
if __name__=="__main__":main()
