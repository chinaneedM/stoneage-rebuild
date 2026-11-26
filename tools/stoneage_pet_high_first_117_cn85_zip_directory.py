"""PET117: archive-only bounded ZIP end record and central directory inspection."""
import argparse,hashlib,json,struct,urllib.request,urllib.error,zipfile
from pathlib import Path
from tools import stoneage_pet_high_first_104_cn70_archive_index as idx
from tools import stoneage_pet_high_first_109_cn75_custody as prior
P=idx.ROOT/"research/pets"
R116=P/"PET-HIGH-FIRST-116-CN85-EXACT-FILE-ARCHIVE-R1.json"
R117=P/"PET-HIGH-FIRST-117-CN85-ZIP-DIRECTORY-R1.json"
SHA="38780cd8ceae3ab990bc25f9de94a87ba34c2c5e50af5aefe38468ae011dcd22"
ZSHA="5e1c54c9b5f1733b564b16044664b8f6c5e172c277a4a3ae312bff457e296435"
TOTAL=1351371747
TAIL=65557
CDCAP=4*1024*1024
def verify(path):
    z=path.read_bytes();assert len(z)==2470 and idx.sha(z)==ZSHA
    with zipfile.ZipFile(path) as f:
        assert f.namelist()==["pet116.json"];raw=f.read("pet116.json")
    assert idx.sha(raw)==SHA
    d=json.loads(raw);assert d["prior_report_git_blob"]=="d0b5c972155e2755ec01aaa20fdde838572fd115"
    assert len(d["indexes"])==14 and d["unique_http_success_candidates"]==4
    assert len(d["prefix_results"])==4
    good=[x for x in d["prefix_results"] if x.get("magic")=="ZIP_MAGIC"]
    assert len(good)==2 and all(x["status"]==206 and x["headers"]["Content-Range"]=="bytes 0-65535/1351371747" and x["sample_sha256"]=="a4ec87915590cc58cf3d63066a9012ae5a186c82614e87aaa996bc32f86b30ac" for x in good)
    assert d["full_originals_verified"]==d["official_closures"]==0 and not d["original_assets_published"]
    R116.write_bytes(raw)
    return good
class NoFollow(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):return None
def read_range(url,start,end):
    assert 0<=start<=end<TOTAL and end-start+1<=CDCAP
    expected=end-start+1
    q=urllib.request.Request(url,headers={"Range":f"bytes={start}-{end}","Accept-Encoding":"identity","User-Agent":"stoneage-rebuild-archaeology/1.0"})
    row=dict(start=start,end=end,requested_bytes=expected)
    try:
        with urllib.request.build_opener(NoFollow()).open(q,timeout=45) as f:
            row.update(status=f.status,content_range=f.headers.get("Content-Range"),content_length=f.headers.get("Content-Length"))
            if f.status!=206 or row["content_range"]!=f"bytes {start}-{end}/{TOTAL}":
                row["result"]="RANGE_NOT_HONORED";return row,None
            raw=f.read(expected+1)
        row.update(response_bytes=len(raw),response_sha256=idx.sha(raw))
        if len(raw)!=expected:row["result"]="RANGE_LENGTH_MISMATCH";return row,None
        row["result"]="EXACT_RANGE";return row,raw
    except (OSError,ValueError,AssertionError) as e:
        row.update(result="ACCESS_OR_PARSE_ERROR",error_type=type(e).__name__,error=str(e)[:200]);return row,None
def eocd(raw,total):
    pos=len(raw)
    while True:
        pos=raw.rfind(b"PK\x05\x06",0,pos)
        if pos<0:raise ValueError("EOCD not found")
        if len(raw)-pos<22:continue
        sig,disk,cd_disk,n_disk,n,size,offset,comment=struct.unpack_from("<4s4H2IH",raw,pos)
        if pos+22+comment!=len(raw):continue
        if disk or cd_disk or n_disk!=n:raise ValueError("multi-disk unsupported")
        if n==65535 or size==0xffffffff or offset==0xffffffff:raise ValueError("ZIP64 unsupported")
        absolute=total-len(raw)+pos
        if offset+size!=absolute:raise ValueError("central directory boundary mismatch")
        return dict(entries=n,central_bytes=size,central_offset=offset,eocd_offset=absolute,comment_bytes=comment)
def directory(raw,info):
    at=0;rows=[]
    while at<len(raw):
        if at+46>len(raw) or raw[at:at+4]!=b"PK\x01\x02":raise ValueError("central entry header mismatch")
        fields=struct.unpack_from("<4s6H3I5H2I",raw,at)
        _,made,need,flags,method,mtime,mdate,crc,packed,unpacked,nlen,xlen,clen,disk,iattr,eattr,offset=fields
        end=at+46+nlen+xlen+clen
        if end>len(raw) or disk or packed==0xffffffff or unpacked==0xffffffff or offset==0xffffffff or offset>=info["central_offset"]:raise ValueError("unsupported entry bounds")
        name_raw=raw[at+46:at+46+nlen]
        if flags&2048:name=name_raw.decode("utf-8","strict")
        else:
            try:name=name_raw.decode("gb18030","strict")
            except UnicodeDecodeError:name=name_raw.decode("cp437")
        # Metadata only; never extract, normalize into a path, or execute.
        rows.append(dict(name=name,name_bytes_sha256=idx.sha(name_raw),flags=flags,method=method,crc32=f"{crc:08x}",compressed_bytes=packed,uncompressed_bytes=unpacked,local_header_offset=offset))
        at=end
    assert len(rows)==info["entries"]
    return rows
def probe(x):
    u=x["replay_url"];row=dict(replay_url=u,cdx=x["cdx"])
    rec,raw=read_range(u,TOTAL-TAIL,TOTAL-1);row["tail"]=rec
    if raw is None:return row
    try:
        info=eocd(raw,TOTAL);row["eocd"]=info
        size=info["central_bytes"];offset=info["central_offset"]
        if not 0<size<=CDCAP:row["directory_result"]="CENTRAL_SIZE_LIMIT";return row
        if offset>=TOTAL-TAIL:
            cd=raw[offset-(TOTAL-TAIL):offset-(TOTAL-TAIL)+size]
            row["central_range"]={"result":"WITHIN_VERIFIED_TAIL","response_bytes":len(cd),"response_sha256":idx.sha(cd)}
        else:
            rec,cd=read_range(u,offset,offset+size-1);row["central_range"]=rec
        if cd is None:return row
        assert len(cd)==size
        row["entries"]=directory(cd,info)
        row["directory_result"]="CENTRAL_DIRECTORY_PARSED"
    except (ValueError,AssertionError,UnicodeError,struct.error) as e:row.update(directory_result="PARSE_ERROR",error_type=type(e).__name__,error=str(e)[:200])
    return row
def selftest():
    import io
    b=io.BytesIO()
    with zipfile.ZipFile(b,"w",compression=zipfile.ZIP_DEFLATED) as f:f.writestr("data/pet.txt",b"test")
    raw=b.getvalue();info=eocd(raw,len(raw));entries=directory(raw[info["central_offset"]:info["eocd_offset"]],info)
    assert len(entries)==1 and entries[0]["name"]=="data/pet.txt" and entries[0]["uncompressed_bytes"]==4
    print("PET117_SELFTEST_OK")
def main():
    p=argparse.ArgumentParser();p.add_argument("--artifact",type=Path,required=True);a=p.parse_args();selftest()
    good=verify(a.artifact)
    # Later capture first, independent earlier tail corroboration second.
    results=[probe(x) for x in reversed(good)]
    d=dict(schema="stoneage.pet117.cn85.zip_directory.r1",prior_git_blob=idx.blob(R116.read_bytes()),prior_report_sha256=SHA,prior_artifact=15118206490,prior_zip_sha256=ZSHA,declared_total_bytes=TOTAL,results=results,original_client_verified=False,original_assets_published=False,official_closures=0)
    R117.write_bytes(prior.dump(d))
    print("PET117_REPORT_SHA256="+idx.sha(R117.read_bytes()),flush=True)
    for x in results:
        print("PET117_CAPTURE="+json.dumps({k:v for k,v in x.items() if k!="entries"}|{"entry_count":len(x.get("entries",[])),"entry_examples":[v for v in x.get("entries",[]) if any(s in v["name"].lower() for s in ("pet","enemy","spr","real","graphic","data/","data\\"))][:35]},ensure_ascii=False,sort_keys=True),flush=True)
if __name__=="__main__":main()
