"""PET120: one bounded full archive attempt; verify every ZIP member, privately extract selected pet resources."""
import argparse,base64,hashlib,json,shutil,subprocess,tempfile,time,urllib.request,zipfile
from pathlib import Path
from tools import stoneage_pet_high_first_119_cn85_cab_hdr_pair as prev
from tools import stoneage_pet_high_first_117_cn85_zip_directory as p
from tools import stoneage_pet_high_first_109_cn75_custody as prior
REPORT=p.P/"PET-HIGH-FIRST-120-CN85-ORIGINAL-RESOURCE-PREFLIGHT-R1.json"
SHA="d31a242ab213e1118341d045040e2b1a6c604b39b85c432416db19b77f5c0800"
ZIP="fde43bbfb777e563612467f99e34f2984144a5b8d6d0aa1b8aa78f0083ada3b4"
TARGETS=("album_47.dat","adrn_185.bin","spr_155.bin","spradrn_155.bin","petlifetype.bin","StoneageNg.dll")
CHUNK=16*1024*1024
def verify(path):
    rawzip=path.read_bytes()
    assert len(rawzip)==6936 and prev.prev.sha(rawzip)==ZIP
    with zipfile.ZipFile(path) as z:
        assert len(z.namelist())==1
        raw=z.read(z.namelist()[0])
    assert raw==prev.REPORT.read_bytes() and prev.prev.sha(raw)==SHA
    d=json.loads(raw);assert d["official_closures"]==0 and not d["original_client_verified"] and not d["pet_payload_extracted"] and not d["original_assets_published"]
    a=d["results"][0];assert len(d["results"])==1 and a["cab_matches_pet118"] is True
    assert a["directory"]["result"]=="DIRECTORY_LISTED" and len(a["directory"]["all_entries"])==759
    assert len(a["directory"]["candidate_entries"])==208
    assert len(a["members"])==2 and all(x["result"]=="CRC_VERIFIED_MEMBER" for x in a["members"])
    assert a["members"][1]["uncompressed_sha256"]=="5b6bbfc648ae86c15314bae2b0529094c8278d5bd1842ee27b54bf11e295fb32"
    return a
def fetch_range(url,dst,start,end,deadline):
    q=urllib.request.Request(url,headers={"Range":f"bytes={start}-{end}","Accept-Encoding":"identity","User-Agent":"stoneage-rebuild-archaeology/1.0"})
    row=dict(start=start,end=end,bytes=0)
    expected=end-start+1
    try:
        with urllib.request.build_opener(p.NoFollow()).open(q,timeout=45) as f:
            row.update(status=f.status,content_range=f.headers.get("Content-Range"),content_length=f.headers.get("Content-Length"))
            if not (f.status==206 and row["content_range"]==f"bytes {start}-{end}/{p.TOTAL}" or f.status==200 and start==0 and end==p.TOTAL-1 and row["content_length"]==str(p.TOTAL)):
                return row|dict(result="RANGE_NOT_HONORED")
            with dst.open("ab") as out:
                while row["bytes"]<expected:
                    if time.monotonic()>deadline:raise TimeoutError("overall transfer deadline")
                    part=f.read(min(1024*1024,expected-row["bytes"]))
                    if not part:break
                    out.write(part);row["bytes"]+=len(part)
                if row["bytes"]!=expected or f.read(1):return row|dict(result="LENGTH_MISMATCH")
        return row|dict(result="EXACT_BYTES")
    except (OSError,ValueError) as e:return row|dict(result="ACCESS_ERROR",error_type=type(e).__name__,error=str(e)[:160])
def hash_file(path):
    s1=hashlib.sha1();s2=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):s1.update(block);s2.update(block)
    return dict(bytes=path.stat().st_size,sha256=s2.hexdigest(),sha1_base32=base64.b32encode(s1.digest()).decode())
def download(cap,path):
    deadline=time.monotonic()+540;url=cap["replay_url"];path.touch()
    attempts=[fetch_range(url,path,0,p.TOTAL-1,deadline)]
    if attempts[0]["result"]!="EXACT_BYTES":
        # No splice after an unverified partial full response; one bounded
        # segmented alternative from the same immutable archive capture.
        path.unlink();path.touch()
        for start in range(0,p.TOTAL,CHUNK):
            if time.monotonic()>deadline:break
            end=min(start+CHUNK,p.TOTAL)-1
            assert path.stat().st_size==start
            a=fetch_range(url,path,start,end,deadline);attempts.append(a)
            if a["result"]!="EXACT_BYTES":break
    info=hash_file(path)
    return dict(attempts=attempts,**info,complete=info["bytes"]==p.TOTAL and attempts[-1]["result"]=="EXACT_BYTES",cdx_digest_matches=info["sha1_base32"]==cap["cdx"]["digest"])
def inspect_zip(path,root,cap,a):
    expected={x["name"]:x for x in cap["entries"]}
    verified=[]
    with path.open("rb") as f:
        assert prev.prev.sha(f.read(65536))=="a4ec87915590cc58cf3d63066a9012ae5a186c82614e87aaa996bc32f86b30ac"
        f.seek(-65557,2);assert prev.prev.sha(f.read())=="836e5e19e1858d29433a1f534f4db83efaaef448c01a56386f8cd8111c3c089b"
    with zipfile.ZipFile(path) as z:
        assert z.namelist()==list(expected)
        for i in z.infolist():
            e=expected[i.filename]
            assert (i.file_size,i.compress_size,i.header_offset,i.compress_type,i.flag_bits,f"{i.CRC:08x}")== (e["uncompressed_bytes"],e["compressed_bytes"],e["local_header_offset"],e["method"],e["flags"],e["crc32"])
            h=hashlib.sha256();n=0
            target=root/i.filename if i.filename in ("data1.cab","data1.hdr","data2.cab") else None
            with z.open(i) as src:
                if target:
                    with target.open("wb") as out:
                        for block in iter(lambda:src.read(1024*1024),b""):h.update(block);n+=len(block);out.write(block)
                else:
                    for block in iter(lambda:src.read(1024*1024),b""):h.update(block);n+=len(block)
            assert n==i.file_size
            verified.append(dict(name=i.filename,bytes=n,sha256=h.hexdigest(),crc32=f"{i.CRC:08x}"))
    pins={x["name"]:x["uncompressed_sha256"] for x in a["members"]}
    assert all(x["sha256"]==pins[x["name"]] for x in verified if x["name"] in pins)
    return verified
def extract(root,a):
    out=root/"selected";out.mkdir()
    rows=[];inventory=a["directory"]["all_entries"]
    for name in TARGETS:
        candidates=[x for x in inventory if x["name"].split("\\")[-1].casefold()==name.casefold()]
        assert len(candidates)==1
        expected=candidates[0]
        q=subprocess.run(["unshield","-j","-d",str(out),"x",str(root/"data1.cab"),name],capture_output=True,timeout=90,check=False)
        matches=[x for x in out.rglob("*") if x.is_file() and x.name.casefold()==name.casefold()]
        row=dict(name=name,source_path=expected["name"],expected_bytes=expected["size"],returncode=q.returncode,stdout_sha256=prev.prev.sha(q.stdout),stderr_sha256=prev.prev.sha(q.stderr))
        if q.returncode==0 and len(matches)==1 and matches[0].stat().st_size==expected["size"]:
            row.update(result="EXTRACTED_SIZE_VERIFIED",**hash_file(matches[0]))
        else:row.update(result="EXTRACTION_UNVERIFIED",actual_sizes=[x.stat().st_size for x in matches])
        rows.append(row)
    return rows
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--artifact",type=Path,required=True);args=ap.parse_args()
    a=verify(args.artifact);cap=json.loads(p.R117.read_bytes())["results"][0];assert cap["cdx"]==a["cdx"]
    d=dict(schema="stoneage.pet120.cn85.original_resource_preflight.r1",prior_artifact=15119150171,prior_zip_sha256=ZIP,prior_report_sha256=SHA,prior_report_git_blob=p.idx.blob(prev.REPORT.read_bytes()),capture=cap["cdx"],original_client_verified=False,original_assets_published=False,pet_payload_extracted=False,official_closures=0,zip_members=[],selected_resources=[])
    with tempfile.TemporaryDirectory() as t:
        root=Path(t);path=root/"StoneAge.zip"
        try:
            assert shutil.disk_usage(root).free>4*1024**3
            d["transfer"]=download(cap,path)
            if d["transfer"]["complete"]:
                d["zip_members"]=inspect_zip(path,root,cap,a)
                d["original_client_verified"]=len(d["zip_members"])==9 and d["transfer"]["cdx_digest_matches"]
                d["selected_resources"]=extract(root,a)
                d["pet_payload_extracted"]=any(x["result"]=="EXTRACTED_SIZE_VERIFIED" and x["name"]!="StoneageNg.dll" for x in d["selected_resources"])
            else:d["blocker"]="BOUNDED_FULL_TRANSFER_INCOMPLETE"
        except (OSError,AssertionError,ValueError,zipfile.BadZipFile,subprocess.TimeoutExpired) as e:d["blocker"]=type(e).__name__+": "+str(e)[:200]
    REPORT.write_bytes(prior.dump(d))
    print("PET120_REPORT_SHA256="+prev.prev.sha(REPORT.read_bytes()),flush=True)
    print("PET120_SUMMARY="+json.dumps(d,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
