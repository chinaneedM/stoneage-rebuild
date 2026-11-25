"""PET67: authenticate and dual-decode the exact PET66 remaining target RD blocks."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
import mmap
from pathlib import Path
import tempfile
from tools import stoneage_pet_high_first_66_motion_inheritance as prev
from tools import stoneage_pet_high_first_tw85_pixels as pix
from tools.stoneage_pet_high_first_60_source_pixels import summarize_carrier, CARRIER
from tools.stoneage_pet_high_first_57_coverage import ROOT, PINS, blob, gzrows
from tools.stoneage_rd_codec import decode_rd_block, RDDecodeError

RECEIPT=ROOT/"research/pets/PET-HIGH-FIRST-67-BULK-PIXELS-R1.json.gz"
SUMMARY=ROOT/"research/pets/PET-HIGH-FIRST-67-BULK-PIXELS-SUMMARY-R1.json"
BASE=ROOT/"research/pets/PET-HIGH-FIRST-66-MOTION-INHERITANCE-SUMMARY-R1.json"
BASE_SHA="7348b60bb6ee5fdda8ae1d71689b99a65d12e38f"
CARRIER_SHA="18a68c9d4275763ef0ed7a347cca940cffe0fee2"
SCOPE="EXACT_SAVED_TW85_PET66_REMAINING_RD_BLOCKS"
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load(path):return json.loads(path.read_bytes())
def stable(data):return (json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
def plan():
    assert blob(BASE.read_bytes())==BASE_SHA and blob(CARRIER.read_bytes())==CARRIER_SHA
    old=prev.derive()
    assert old["summary"]==load(BASE)["summary"]
    missing={n:b for n,b in old["bitmap_evidence"].items() if b["grade"]=="NO_STRICT_PIXEL_RECEIPT"}
    assert len(missing)==79056
    by_index={b["index"]:(n,b) for n,b in missing.items()}
    assert len(by_index)==len(missing)
    native={}
    for row in gzrows(PINS["native"][0]):
        i=int(row["index"])
        if i not in by_index:continue
        n,b=by_index[i]
        assert (int(row["bitmapno"]),row["rd_sha256"],*(int(row[k]) for k in ("size","width","height")))==(n,b["rd_sha256"],b["size"],b["width"],b["height"])
        native[n]=dict(index=i,bitmap=n,offset=int(row["adder"]),size=b["size"],width=b["width"],height=b["height"],adrn_sha256=row["record_sha256"],rd_sha256=b["rd_sha256"])
    assert native.keys()==missing.keys()
    return old,native

def decode(block,width,height):
    from tools.stoneage_scene07_independent_pixels import independent_rd
    if width<=0 or height<=0 or width*height>1000000:
        return dict(status="NONPOSITIVE_OR_OVERSIZE_GEOMETRY",index_pixels_sha256=None)
    if len(block)<16 or block[:2]!=b"RD":
        return dict(status="INVALID_RD_HEADER",index_pixels_sha256=None)
    if block[2] not in (0,1):
        return dict(status="UNSUPPORTED_ENCODING",index_pixels_sha256=None)
    first=second=None; e1=e2=None
    try:
        header,pixels=decode_rd_block(block,authoritative_block_size=len(block))
        first=(header["width_s"],header["height_s"],pixels)
    except RDDecodeError as exc:e1=str(exc)[:160]
    try:second=independent_rd(block)
    except ValueError as exc:e2=str(exc)[:160]
    if first is not None and second is not None:
        if first!=second or first[:2]!=(width,height):
            return dict(status="DECODER_DISAGREEMENT",index_pixels_sha256=None)
        return dict(status="DUAL_DECODED_INDEX_PIXELS",index_pixels_sha256=sha(first[2]))
    return dict(status="STRICT_DECODE_REJECTED",index_pixels_sha256=None,decoder_one_error=e1,decoder_two_error=e2)

def read_original(directory,native,acquisition):
    assert summarize_carrier(acquisition)==summarize_carrier(load(CARRIER))
    pix.qualify_pair(directory)
    for filename in ("adrn_158.bin","real_158.bin"):
        pix.original_check(directory/filename,pix.SOURCE_FILES[filename])
    # Re-export complete original SPR tables, checking exact archived bytes.
    with tempfile.TemporaryDirectory() as temp:
        paths=[Path(temp)/k for k in ("group","animation","frame")]
        pix.export_cn50_spr(directory/"spradrn_137.bin",directory/"spr_137.bin",*paths)
        for path,reference in zip(paths,(PINS["groups"][0],prev.EXTRA["tw85_animation"][0],PINS["frames"][0]),strict=True):
            assert path.read_bytes()==reference.read_bytes(),reference.name
    adrn=(directory/"adrn_158.bin").read_bytes()
    observations={};cache={}
    with (directory/"real_158.bin").open("rb") as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as real:
        for n,row in sorted(native.items(),key=lambda x:x[1]["offset"]):
            i=row["index"];raw=adrn[i*80:(i+1)*80]
            number,offset,size,_,_,width,height,_=pix.COLS.unpack(raw)
            assert (number,offset,size,width,height,sha(raw))==(n,row["offset"],row["size"],row["width"],row["height"],row["adrn_sha256"]),n
            assert 16<=size<=len(real)-offset,n
            block=real[offset:offset+size]
            assert sha(block)==row["rd_sha256"],n
            key=(row["rd_sha256"],size,width,height)
            if key not in cache:cache[key]=decode(block,width,height)
            observations[str(n)]=dict(**row,**cache[key])
            if len(observations)%10000==0:print("PET67_PROGRESS",len(observations),"/",len(native),flush=True)
    return dict(schema="stoneage.pet67.bulk_original_pixels.r1",scope=SCOPE,base_git_blob=BASE_SHA,carrier=summarize_carrier(acquisition),
        source_files={name:dict(bytes=size,sha256=digest) for name,(size,digest) in pix.SOURCE_FILES.items()},
        original_assets_published=False,runtime_executed=False,official_identity_verified=False,
        observations=observations,distinct_decode_keys=len(cache))

def verify(report,old,native):
    assert report["schema"]=="stoneage.pet67.bulk_original_pixels.r1" and report["scope"]==SCOPE and report["base_git_blob"]==BASE_SHA
    assert report["carrier"]==summarize_carrier(load(CARRIER))
    assert report["source_files"]=={name:dict(bytes=size,sha256=digest) for name,(size,digest) in pix.SOURCE_FILES.items()}
    assert not any(report[k] for k in ("original_assets_published","runtime_executed","official_identity_verified"))
    observations=report["observations"]
    assert set(observations)=={str(n) for n in native}
    decoded=set();failures=[];statuses=Counter();keys={}
    for n,row in native.items():
        b=observations[str(n)]
        assert all(b[k]==v for k,v in row.items()),n
        status=b["status"];digest=b["index_pixels_sha256"]
        assert status in ("DUAL_DECODED_INDEX_PIXELS","NONPOSITIVE_OR_OVERSIZE_GEOMETRY","INVALID_RD_HEADER","UNSUPPORTED_ENCODING","DECODER_DISAGREEMENT","STRICT_DECODE_REJECTED")
        statuses[status]+=1
        if status=="DUAL_DECODED_INDEX_PIXELS":
            assert isinstance(digest,str) and len(bytes.fromhex(digest))==32
            decoded.add(n)
        else:
            assert digest is None
            failures.append(dict(bitmap=n,status=status,width=b["width"],height=b["height"],rd_sha256=b["rd_sha256"],decoder_one_error=b.get("decoder_one_error"),decoder_two_error=b.get("decoder_two_error")))
        key=(b["rd_sha256"],b["size"],b["width"],b["height"])
        assert keys.setdefault(key,(status,digest))==(status,digest)
    assert len(keys)==report["distinct_decode_keys"]
    remaining=set(native)-decoded
    sc=Counter();gc=Counter();group_status={};affected=[]
    for group in old["groups"]:
        states=[]
        for a in group["sequences"]:
            if a["status"]=="SENTINEL_ONLY":state="SENTINEL_ONLY"
            elif set(a["missing_bitmaps"]) & remaining:state="INCOMPLETE"
            else:state="COMPLETE"
            sc[state]+=1;states.append(state)
        nonempty=[s for s in states if s!="SENTINEL_ONLY"]
        status="ALL_COMPLETE" if nonempty and all(s=="COMPLETE" for s in nonempty) else "PARTIAL" if "COMPLETE" in nonempty else "NONE_COMPLETE"
        gc[status]+=1;group_status[group["group_index"]]=status
        if status!="ALL_COMPLETE":affected.append(dict(group_index=group["group_index"],graphic=group["graphic"],incomplete_sequences=states.count("INCOMPLETE")))
    tc=Counter()
    for r in old["templates"]:
        s=[group_status[g] for g in r["groups"]]
        tc["ALL_COMPLETE" if all(v=="ALL_COMPLETE" for v in s) else "PARTIAL" if any(v!="NONE_COMPLETE" for v in s) else "NONE_COMPLETE"]+=1
    target_groups=set(group_status)
    remaining_frames=0;new_frames=0
    for f in gzrows(PINS["frames"][0]):
        if int(f["group_index"]) not in target_groups or f["sentinel"]=="1":continue
        n=int(f["bmp_no"])
        remaining_frames+=n in remaining
        new_frames+=n in decoded
    assert remaining_frames+new_frames==old["summary"]["frame_evidence"]["NO_STRICT_PIXEL_RECEIPT"]
    assert sum(sc.values())==24144 and sum(gc.values())==427 and sum(tc.values())==467
    return dict(schema="stoneage.pet67.bulk_pixel_summary.r1",source_receipt_sha256=sha(stable(report)),target_bitmaps=len(native),new_strict_decoded=len(decoded),
        remaining_strict_bitmaps=len(remaining),distinct_decode_keys=len(keys),block_status=dict(statuses),
        total_target_bitmaps=old["summary"]["distinct_frame_bitmaps"],total_strict_bitmaps=old["summary"]["distinct_frame_bitmaps"]-len(remaining),
        newly_covered_frame_positions=new_frames,remaining_frame_positions=remaining_frames,
        sequence_status=dict(sc),group_status=dict(gc),template_status=dict(tc),affected_groups=affected,failures=sorted(failures,key=lambda x:x["bitmap"]),
        new_official_acquisition_closures=0,official_species_count=None,original_assets_published=False,native_runtime_verified=False)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--plan-only",action="store_true");p.add_argument("--source-dir",type=Path);p.add_argument("--acquisition",type=Path)
    a=p.parse_args()
    assert bool(a.source_dir)==bool(a.acquisition)
    old,native=plan()
    if a.plan_only:
        print("PET67_PLAN",len(native),len({(b["rd_sha256"],b["size"],b["width"],b["height"]) for b in native.values()}))
        return
    if a.source_dir:
        report=read_original(a.source_dir,native,load(a.acquisition))
        summary=verify(report,old,native)
        RECEIPT.write_bytes(gzip.compress(stable(report),compresslevel=6,mtime=0))
        SUMMARY.write_bytes(stable(summary))
    else:
        report=json.loads(gzip.decompress(RECEIPT.read_bytes()))
        summary=verify(report,old,native)
        assert SUMMARY.read_bytes()==stable(summary),"durable summary differs from replay"
    print("PET67_SUMMARY="+json.dumps({k:v for k,v in summary.items() if k not in ("affected_groups","failures")},sort_keys=True,separators=(",",":")),flush=True)
if __name__=="__main__":main()
