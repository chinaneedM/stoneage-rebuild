"""PET119: bounded same-capture CAB/HDR paired range; independent PET118 custody."""
import argparse,json,struct,tempfile,zipfile,zlib
from pathlib import Path
from tools import stoneage_pet_high_first_118_cn85_installshield_index as prev
from tools import stoneage_pet_high_first_117_cn85_zip_directory as p
from tools import stoneage_pet_high_first_109_cn75_custody as prior
REPORT=p.P/"PET-HIGH-FIRST-119-CN85-CAB-HDR-PAIR-R1.json"
SHA="a54f441b2a9547067209cf6c683ec463ef406a9bc2b975a9f87a80e43b1c6a5e"
ZIP="d8062558fc44d47682bff5a94eeb983858d5b5d26dc34c116cd6358929c31f4b"
CAB_SHA="af4900c3a7829093a267c2c216a917ae951143d06ca401a7650075695029dec5"
def verify(path):
    z=path.read_bytes();assert len(z)==1206 and prev.sha(z)==ZIP
    with zipfile.ZipFile(path) as f:
        assert len(f.namelist())==1
        raw=f.read(f.namelist()[0])
    assert raw==prev.REPORT.read_bytes() and prev.sha(raw)==SHA
    d=json.loads(raw);assert d["official_closures"]==0 and not d["pet_payload_extracted"] and not d["original_client_verified"] and not d["original_assets_published"]
    m={x["name"]:x for x in d["members"]}
    assert m["data1.cab"]["result"]=="CRC_VERIFIED_MEMBER" and m["data1.cab"]["uncompressed_sha256"]==CAB_SHA
    assert m["data1.hdr"]["result"]=="RANGE_UNAVAILABLE"
    assert d["installshield_directory"]["result"]=="MISSING_VERIFIED_MEMBERS"
    return d
def decode_pair(raw,entries,start):
    out={}
    for i,e in enumerate(entries):
        off=e["local_header_offset"]-start
        end=entries[i+1]["local_header_offset"]-start if i+1<len(entries) else len(raw)
        assert 0<=off<end<=len(raw)
        out[e["name"]]=prev.member(raw[off:end],e)
    return out
def selftest():
    import io
    z=io.BytesIO()
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED) as f:
        f.writestr("data1.cab",b"cab")
        f.writestr("data1.hdr",b"hdr")
    raw=z.getvalue();i=p.eocd(raw,len(raw));entries=p.directory(raw[i["central_offset"]:i["eocd_offset"]],i)
    assert decode_pair(raw[:i["central_offset"]],entries,0)=={"data1.cab":b"cab","data1.hdr":b"hdr"}
    try:decode_pair(raw[:i["central_offset"]-1],entries,0)
    except AssertionError:pass
    else:raise AssertionError("truncated pair accepted")
    print("PET119_SELFTEST_OK")
def record(name,data):
    return dict(name=name,result="CRC_VERIFIED_MEMBER",uncompressed_bytes=len(data),uncompressed_sha256=prev.sha(data),first_four_hex=data[:4].hex())
def probe(cap,allow_split):
    e={x["name"]:x for x in cap["entries"]};pair=[e["data1.cab"],e["data1.hdr"]]
    start=pair[0]["local_header_offset"];end=e["data2.cab"]["local_header_offset"]-1
    row=dict(cdx=cap["cdx"],attempts=[],members=[])
    data={}
    rec,raw=p.read_range(cap["replay_url"],start,end);row["attempts"].append(dict(kind="PAIR",range=rec))
    if raw is not None:
        try:data=decode_pair(raw,pair,start)
        except (AssertionError,ValueError,struct.error,zlib.error) as exc:row["pair_error"]=type(exc).__name__
    if not data and allow_split:
        for i,item in enumerate(pair):
            lo=item["local_header_offset"];hi=pair[i+1]["local_header_offset"]-1 if i==0 else end
            rec,raw=p.read_range(cap["replay_url"],lo,hi)
            row["attempts"].append(dict(kind=item["name"],range=rec))
            if raw is not None:
                try:data[item["name"]]=prev.member(raw,item)
                except (AssertionError,ValueError,struct.error,zlib.error) as exc:row[item["name"]+"_error"]=type(exc).__name__
    row["members"]=[record(k,v) for k,v in data.items()]
    row["cab_matches_pet118"]=prev.sha(data["data1.cab"])==CAB_SHA if "data1.cab" in data else None
    with tempfile.TemporaryDirectory() as t:
        root=Path(t)
        for k,v in data.items():(root/k).write_bytes(v)
        row["directory"]=prev.listing(root) if "data1.cab" in data else dict(result="MISSING_CAB")
    return row
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--artifact",type=Path,required=True);a=ap.parse_args();selftest();verify(a.artifact)
    d=json.loads(p.R117.read_bytes());later,earlier=d["results"]
    assert later["cdx"]["timestamp"]=="20120508023725" and earlier["cdx"]["timestamp"]=="20120113130058"
    rows=[probe(later,True)]
    # Earlier capture has no verified tail. Reuse only the later directory as a
    # candidate layout and validate local headers, CRCs and CAB hash independently.
    # Never merge raw members from distinct captures.
    if len(rows[0]["members"])<2:
        alternate=dict(earlier,entries=later["entries"])
        row=probe(alternate,False);row["layout_source"]="LATER_CAPTURE_CANDIDATE_ONLY";rows.append(row)
    out=dict(schema="stoneage.pet119.cn85.cab_hdr_pair.r1",prior_artifact=15119015145,prior_zip_sha256=ZIP,prior_report_sha256=SHA,prior_report_git_blob=p.idx.blob(prev.REPORT.read_bytes()),results=rows,original_client_verified=False,original_assets_published=False,pet_payload_extracted=False,official_closures=0)
    REPORT.write_bytes(prior.dump(out))
    print("PET119_REPORT_SHA256="+prev.sha(REPORT.read_bytes()))
    for row in rows:
        print("PET119_RESULT="+json.dumps(dict(cdx=row["cdx"],attempts=row["attempts"],members=row["members"],cab_matches_pet118=row["cab_matches_pet118"],directory={k:v for k,v in row["directory"].items() if k not in ("all_entries","candidate_entries")},candidate_count=len(row["directory"].get("candidate_entries",[]))),ensure_ascii=False))
if __name__=="__main__":main()
