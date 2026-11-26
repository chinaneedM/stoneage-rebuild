"""PET118: verified small ZIP members; InstallShield directory only."""
import argparse,hashlib,json,re,struct,subprocess,tempfile,zipfile,zlib
from pathlib import Path
from tools import stoneage_pet_high_first_117_cn85_zip_directory as p
from tools import stoneage_pet_high_first_109_cn75_custody as prior
REPORT=p.P/"PET-HIGH-FIRST-118-CN85-INSTALLSHIELD-INDEX-R1.json"
SHA="11962df9697f7dacf33374d2c41010ea75bc0f2587dda189b1fc543743abdc71"
ZSHA="a80fd5ae7a5784fb42669e2b1203483a583b60785d67a126aee5fcc18c4d68d3"
CAP=2*1024*1024
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(path):
    z=path.read_bytes()
    assert len(z)==1911 and sha(z)==ZSHA
    with zipfile.ZipFile(path) as f:
        assert len(f.namelist())==1
        raw=f.read(f.namelist()[0])
    assert raw==p.R117.read_bytes() and sha(raw)==SHA
    d=json.loads(raw)
    assert d["official_closures"]==0 and not d["original_client_verified"] and not d["original_assets_published"]
    a,b=d["results"]
    assert a["cdx"]["timestamp"]=="20120508023725" and a["directory_result"]=="CENTRAL_DIRECTORY_PARSED"
    assert a["eocd"]["entries"]==len(a["entries"])==9 and b["tail"]["result"]=="RANGE_LENGTH_MISMATCH"
    return a
def member(raw,e):
    assert len(raw)>=30
    sig,ver,flags,method,mt,md,crc,packed,size,nlen,xlen=struct.unpack_from("<4s5H3I2H",raw)
    assert sig==b"PK\x03\x04" and flags==e["flags"]==0 and method==e["method"]==8
    assert packed==e["compressed_bytes"] and size==e["uncompressed_bytes"]<=CAP
    assert f"{crc:08x}"==e["crc32"] and raw[30:30+nlen]==e["name"].encode("ascii")
    at=30+nlen+xlen
    assert at+packed==len(raw)
    obj=zlib.decompressobj(-15)
    out=obj.decompress(raw[at:],size+1)
    assert len(out)==size and obj.eof and not obj.unused_data and not obj.unconsumed_tail
    assert zlib.crc32(out)==crc
    return out
def selftest():
    import io
    z=io.BytesIO()
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED) as f:f.writestr("data1.hdr",b"test")
    raw=z.getvalue();info=p.eocd(raw,len(raw))
    e=p.directory(raw[info["central_offset"]:info["eocd_offset"]],info)[0]
    sample=raw[:info["central_offset"]]
    assert member(sample,e)==b"test"
    for bad,entry in ((sample[:-1],e),(sample,dict(e,crc32="00000000"))):
        try:member(bad,entry)
        except AssertionError:pass
        else:raise AssertionError("invalid member accepted")
    print("PET118_SELFTEST_OK")
def listing(root):
    try:
        q=subprocess.run(["unshield","l",str(root/"data1.cab")],capture_output=True,timeout=30,check=False)
    except (OSError,subprocess.TimeoutExpired) as e:return dict(result="LIST_UNAVAILABLE",error_type=type(e).__name__)
    out=q.stdout
    row=dict(returncode=q.returncode,stdout_sha256=sha(out),stderr_sha256=sha(q.stderr),stdout_bytes=len(out))
    if q.returncode or len(out)>CAP:return row|dict(result="LIST_FAILED_OR_LIMIT")
    entries=[]
    for line in out.decode("utf-8",errors="replace").splitlines():
        m=re.match(r"^\s*(\d+)\s+(.+?)\s*$",line)
        if m:entries.append(dict(size=int(m[1]),name=m[2]))
    candidates=[x for x in entries if re.search(r"pet|enemy|spr|adrn|real|graphic|anim|skill|\.dat$|\.bin$",x["name"],re.I)]
    return row|dict(result="DIRECTORY_LISTED" if entries else "NO_PARSED_ENTRIES",parsed_entries=len(entries),candidate_entries=candidates,all_entries=entries)
def main():
    a=argparse.ArgumentParser();a.add_argument("--artifact",type=Path,required=True);args=a.parse_args();selftest()
    cap=verify(args.artifact);entries=cap["entries"];rows=[]
    with tempfile.TemporaryDirectory() as t:
        root=Path(t)
        for i,e in enumerate(entries):
            if e["name"] not in ("setup.ini","data1.cab","data1.hdr"):continue
            start=e["local_header_offset"];end=entries[i+1]["local_header_offset"]-1
            assert 0<end-start+1<=CAP
            rec,raw=p.read_range(cap["replay_url"],start,end)
            row=dict(name=e["name"],range=rec,expected_crc32=e["crc32"])
            if raw is not None:
                try:
                    data=member(raw,e)
                    row.update(result="CRC_VERIFIED_MEMBER",uncompressed_bytes=len(data),uncompressed_sha256=sha(data),first_four_hex=data[:4].hex())
                    if e["name"]!="setup.ini":(root/e["name"]).write_bytes(data)
                except (AssertionError,ValueError,struct.error,zlib.error) as exc:row.update(result="MEMBER_VALIDATION_FAILED",error_type=type(exc).__name__)
            else:row["result"]="RANGE_UNAVAILABLE"
            rows.append(row)
        listed=listing(root) if all((root/x).exists() for x in ("data1.cab","data1.hdr")) else dict(result="MISSING_VERIFIED_MEMBERS")
    d=dict(schema="stoneage.pet118.cn85.installshield_index.r1",prior_artifact=15118386642,prior_zip_sha256=ZSHA,prior_report_sha256=SHA,prior_report_git_blob=p.idx.blob(p.R117.read_bytes()),capture=cap["cdx"],members=rows,installshield_directory=listed,original_client_verified=False,original_assets_published=False,pet_payload_extracted=False,official_closures=0)
    REPORT.write_bytes(prior.dump(d))
    print("PET118_REPORT_SHA256="+sha(REPORT.read_bytes()))
    print("PET118_SUMMARY="+json.dumps(dict(members=rows,list_result={k:v for k,v in listed.items() if k not in ("candidate_entries","all_entries")},candidate_count=len(listed.get("candidate_entries",[]))),ensure_ascii=False))
if __name__=="__main__":main()
