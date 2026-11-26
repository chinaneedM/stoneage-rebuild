"""PET122: one bounded original-archive read, in-job derived resource analysis."""
import argparse,csv,gzip,hashlib,json,shutil,subprocess,tempfile,time,zipfile
from pathlib import Path
from tools import stoneage_pet_high_first_120_cn85_original_resource_preflight as old
from tools import stoneage_pet_high_first_121_cn85_final_receipt as receipt
from tools.stoneage_cn50_spr_metadata import export_cn50_spr
from tools.stoneage_tw10_resource_metadata import parse_adrn_record
from tools.stoneage_pet126k_cn50_original_exe_probe import table_candidates,parse_row
REPORT=old.p.P/"PET-HIGH-FIRST-122-CN85-COMPLETE-TRANSFER-R1.json"
LIMIT=2400
PROGRAMS=("sa_85_free.exe","sa_25_payment.exe")
def sha(b):return hashlib.sha256(b).hexdigest()
def source(artifact):
    z=artifact.read_bytes();assert len(z)==1029 and sha(z)==receipt.ZIP
    with zipfile.ZipFile(artifact) as f:
        assert len(f.namelist())==1
        raw=f.read(f.namelist()[0])
    assert raw==old.REPORT.read_bytes() and sha(raw)==receipt.SHA and old.p.idx.blob(raw)==receipt.BLOB
    d=json.loads(raw);assert d["transfer"]["attempts"][0]["bytes"]==504365056 and not d["original_client_verified"]
    a=json.loads(old.prev.REPORT.read_bytes())["results"][0]
    cap=json.loads(old.p.R117.read_bytes())["results"][0]
    assert a["cdx"]==cap["cdx"]==d["capture"] and len(a["directory"]["all_entries"])==759
    return cap,a
def transfer(cap,dst):
    dst.touch()
    start=time.monotonic()
    attempt=old.fetch_range(cap["replay_url"],dst,0,old.p.TOTAL-1,start+LIMIT)
    info=old.hash_file(dst)
    return dict(attempts=[attempt],elapsed_seconds=round(time.monotonic()-start,1),**info,complete=info["bytes"]==old.p.TOTAL and attempt["result"]=="EXACT_BYTES",cdx_digest_matches=info["sha1_base32"]==cap["cdx"]["digest"])
def select(root,a,name):
    expected=[x for x in a["directory"]["all_entries"] if x["name"]=="DefaultComponent\\"+name]
    assert len(expected)==1
    out=root/("program-"+name);out.mkdir()
    q=subprocess.run(["unshield","-g","DefaultComponent","-j","-d",str(out),"x",str(root/"data1.cab"),name],capture_output=True,timeout=60,check=False)
    matches=[x for x in out.rglob("*") if x.is_file() and x.name.casefold()==name.casefold()]
    row=dict(name=name,source_path=expected[0]["name"],expected_bytes=expected[0]["size"],returncode=q.returncode,stdout_sha256=sha(q.stdout),stderr_sha256=sha(q.stderr))
    if q.returncode==0 and len(matches)==1 and matches[0].stat().st_size==expected[0]["size"]:
        return row|dict(result="EXTRACTED_SIZE_VERIFIED",**old.hash_file(matches[0])),matches[0]
    return row|dict(result="EXTRACTION_UNVERIFIED",actual_sizes=[x.stat().st_size for x in matches]),None
def scan_program(path):
    raw=path.read_bytes();candidates=table_candidates(raw,"gb18030")
    for c in candidates:
        start=c["file_offset"]
        c["entries"]=[parse_row(raw,start+28*i,"gb18030") for i in range(c["rows"])]
    return dict(program=path.name,sha256=sha(raw),format="28_BYTE_HEURISTIC_CANDIDATES_NOT_NATIVE_SELECTOR_PROOF",candidates=candidates)
def analyze(root,a,resources):
    verified={x["name"] for x in resources if x["result"]=="EXTRACTED_SIZE_VERIFIED"}
    paths={x.name:x for x in (root/"selected").rglob("*") if x.is_file() and x.name in verified}
    d={}
    if "adrn_185.bin" in paths:
        raw=paths["adrn_185.bin"].read_bytes()
        real_size=next(x["size"] for x in a["directory"]["all_entries"] if x["name"]=="Files\\real_185.bin")
        try:
            assert len(raw)%80==0
            count=bad=max_end=0;unique=set()
            for i in range(0,len(raw),80):
                x=parse_adrn_record(raw[i:i+80]);count+=1;unique.add(x["bitmapno"])
                end=x["adder"]+x["size"];max_end=max(max_end,end);bad+=int(end>real_size)
            d["adrn"]=dict(records=count,unique_bitmap_ids=len(unique),declared_real_bytes=real_size,max_end=max_end,out_of_declared_real_bounds=bad,actual_real_bytes_verified=False)
        except (ValueError,AssertionError) as e:d["adrn"]=dict(blocker=type(e).__name__+":"+str(e)[:160])
    if {"spr_155.bin","spradrn_155.bin"}<=paths.keys():
        try:
            g,an,fr=[root/(n+".tsv.gz") for n in ("group","animation","frame")]
            s=export_cn50_spr(paths["spradrn_155.bin"],paths["spr_155.bin"],g,an,fr)
            with gzip.open(g,"rt") as f:s["group_rows"]=list(csv.DictReader(f,delimiter="\t"))
            assert len(s["group_rows"])==s["groups"]
            d["spr"]=s
        except (ValueError,AssertionError) as e:d["spr"]=dict(blocker=type(e).__name__+":"+str(e)[:160])
    if "album_47.dat" in paths:
        n=paths["album_47.dat"].stat().st_size
        d["album"]=dict(bytes=n,sha256=old.hash_file(paths["album_47.dat"])["sha256"],semantics="UNRESOLVED_LOCAL_ALBUM_FORMAT",old_80_byte_block_candidates=[dict(slots=i,blocks=n//(16+80*i)) for i in range(1,4001) if n%(16+80*i)==0])
    programs=[]
    if "StoneageNg.dll" in paths:programs.append(scan_program(paths["StoneageNg.dll"]))
    for name in PROGRAMS:
        try:
            row,path=select(root,a,name);resources.append(row)
            if path:programs.append(scan_program(path))
        except (OSError,ValueError,AssertionError,subprocess.TimeoutExpired) as e:resources.append(dict(name=name,result="EXTRACTION_UNVERIFIED",blocker=str(e)[:160]))
    d["compiled_table_candidates"]=programs
    return d
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--artifact",type=Path,required=True);args=ap.parse_args()
    cap,a=source(args.artifact)
    d=dict(schema="stoneage.pet122.cn85.complete_transfer.r1",prior_artifact=15120460742,prior_report_git_blob=receipt.BLOB,prior_report_sha256=receipt.SHA,prior_zip_sha256=receipt.ZIP,capture=cap["cdx"],original_client_verified=False,original_assets_published=False,pet_payload_extracted=False,official_closures=0,zip_members=[],selected_resources=[],analysis={})
    with tempfile.TemporaryDirectory() as t:
        root=Path(t);path=root/"StoneAge.zip"
        try:
            assert shutil.disk_usage(root).free>4*1024**3
            d["transfer"]=transfer(cap,path)
            print("PET122_TRANSFER="+json.dumps(d["transfer"]),flush=True)
            if d["transfer"]["complete"]:
                d["zip_members"]=old.inspect_zip(path,root,cap,a)
                d["original_client_verified"]=len(d["zip_members"])==9 and d["transfer"]["cdx_digest_matches"]
                if not d["original_client_verified"]:d["authentication_limit"]="ZIP_CRC_AND_CAPTURE_BOUNDARIES_VERIFIED_CDX_DIGEST_UNMATCHED"
                d["selected_resources"]=old.extract(root,a)
                d["pet_payload_extracted"]=any(x["result"]=="EXTRACTED_SIZE_VERIFIED" and x["name"]!="StoneageNg.dll" for x in d["selected_resources"])
                d["analysis"]=analyze(root,a,d["selected_resources"])
            else:d["blocker"]="FINAL_BOUNDED_TRANSFER_INCOMPLETE"
        except (OSError,AssertionError,ValueError,zipfile.BadZipFile,subprocess.TimeoutExpired) as e:d["blocker"]=type(e).__name__+": "+str(e)[:200]
    REPORT.write_bytes(old.prior.dump(d))
    print("PET122_REPORT_SHA256="+sha(REPORT.read_bytes()),flush=True)
    print("PET122_SUMMARY="+json.dumps({k:v for k,v in d.items() if k!="analysis"},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
