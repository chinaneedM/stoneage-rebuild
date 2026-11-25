"""PET68: source-bounded terminal RD index investigation; never upgrade strict failures."""
import argparse
from collections import Counter
import gzip
import json
import mmap
from pathlib import Path
import struct
from tools import stoneage_pet_high_first_67_bulk_pixels as bulk
from tools.stoneage_rd_codec import decode_legacy_rle, parse_rd_header, RDDecodeError
from tools.stoneage_pet11_tw10_capture_sprite_source import rd_indices

ROOT=bulk.ROOT
RECEIPT=ROOT/"research/pets/PET-HIGH-FIRST-68-RD-BOUNDARY-R1.json"
SUMMARY=ROOT/"research/pets/PET-HIGH-FIRST-68-RD-BOUNDARY-SUMMARY-R1.json"
PINS={bulk.RECEIPT:"1801e69665de0d67ea7d15dce5396c267bb65374",bulk.SUMMARY:"0cc6e1b49b36efd65219b27a0d96108ad8041c89"}
BOUND="TERMINAL_C2_ZERO_OUTSIDE_CANVAS"
def sha(data):return bulk.sha(data)
def plan():
    for path,digest in PINS.items():assert bulk.blob(path.read_bytes())==digest,path
    old,native=bulk.plan()
    prior=json.loads(gzip.decompress(bulk.RECEIPT.read_bytes()))
    assert bulk.verify(prior,old,native)==bulk.load(bulk.SUMMARY)
    failures={b["bitmap"]:b for b in prior["observations"].values() if b["status"]!="DUAL_DECODED_INDEX_PIXELS"}
    assert len(failures)==68
    for n,b in failures.items():
        assert b["status"]=="STRICT_DECODE_REJECTED" and b["decoder_two_error"]=="pixel overflow"
        expected=b["width"]*b["height"]
        assert b["decoder_one_error"]==f"decoded output exceeds expected length: {expected+1} > {expected}"
    return old,native,failures

def independent_stream(payload,limit):
    """Independent bounded command parser, retaining only derived terminal metadata."""
    out=bytearray();i=0;last=None
    while i<len(payload):
        start=i;control=payload[i];i+=1
        family=control>>4
        if family not in (0,1,2,8,9,10,12,13,14):raise ValueError("unsupported RLE family")
        kind=family//4;extra=family%4;value=None
        if kind==2:
            if i>=len(payload):raise ValueError("missing repeat byte")
            value=payload[i];i+=1
        if i+extra>len(payload):raise ValueError("truncated count")
        count=control&15
        for j in range(extra):count=count*256+payload[i+j]
        i+=extra
        before=len(out)
        if before+count>limit:raise ValueError("bounded stream overflow")
        if kind==0:
            if i+count>len(payload):raise ValueError("truncated literal")
            out.extend(payload[i:i+count]);i+=count
        elif kind==2:out.extend(bytes([value])*count)
        else:out.extend(bytes(count))
        last=dict(control=control,output_start=before,output_end=len(out),count=count,command_offset=start,command_end=i)
    return bytes(out),last

def diagnose(block,w,h):
    header=parse_rd_header(block);expected=w*h
    assert (header["width_s"],header["height_s"],header["stored_size"])==(w,h,len(block))
    result=dict(flag=header["flag"],expected_canvas_pixels=expected,encoded_payload_bytes=len(block)-16,strict_status_retained="STRICT_DECODE_REJECTED",status="UNQUALIFIED_BOUNDARY",full_stream_sha256=None,canvas_prefix_sha256=None,stream_length=None,excess_count=None,excess_all_zero=None,terminal_command=None)
    if header["flag"]!=1 or w<=0 or h<=0 or expected>1000000:return result
    try:
        first=decode_legacy_rle(block[16:],expected+1)
        second,last=independent_stream(block[16:],expected+1)
    except (ValueError,RDDecodeError) as exc:
        result["diagnostic_error"]=str(exc)[:200]
        return result
    if first!=second:
        result["diagnostic_error"]="independent full stream mismatch"
        return result
    result.update(full_stream_sha256=sha(first),stream_length=len(first),excess_count=len(first)-expected,excess_all_zero=(len(first)>expected and all(x==0 for x in first[expected:])),terminal_command=last)
    if (len(first)==expected+1 and result["excess_all_zero"] and last and
        (last["control"],last["count"],last["output_start"],last["output_end"],last["command_end"])==(0xc2,2,expected-1,expected+1,len(block)-16)
        and first[-2:]==bytes(2)):
        # The earlier TW10 bounded decoder must independently accept exactly the same canvas.
        a,b,prefix,length,strict=rd_indices(block)
        assert (a,b,length,strict,prefix)==(w,h,expected+1,False,first[:expected])
        result.update(status=BOUND,canvas_prefix_sha256=sha(prefix))
    return result

def read_original(directory,acquisition,native,failures):
    assert bulk.summarize_carrier(acquisition)==bulk.summarize_carrier(bulk.load(bulk.CARRIER))
    bulk.pix.qualify_pair(directory)
    for filename in ("adrn_158.bin","real_158.bin"):
        bulk.pix.original_check(directory/filename,bulk.pix.SOURCE_FILES[filename])
    adrn=(directory/"adrn_158.bin").read_bytes();observations={}
    with (directory/"real_158.bin").open("rb") as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as real:
        for n in sorted(failures):
            row=native[n];i=row["index"];raw=adrn[i*80:(i+1)*80]
            number,offset,size,_,_,width,height,_=bulk.pix.COLS.unpack(raw)
            assert (number,offset,size,width,height,sha(raw))==(n,row["offset"],row["size"],row["width"],row["height"],row["adrn_sha256"])
            assert 16<=size<=len(real)-offset
            block=real[offset:offset+size]
            assert sha(block)==row["rd_sha256"]==failures[n]["rd_sha256"]
            assert bulk.decode(block,width,height)=={k:failures[n][k] for k in ("status","index_pixels_sha256","decoder_one_error","decoder_two_error")}
            observations[str(n)]=dict(**row,**diagnose(block,width,height))
    return dict(schema="stoneage.pet68.rd_boundary.r1",source_grade="SAME_SAVED_TW85_CARRIER",prior_receipt_git_blob=PINS[bulk.RECEIPT],prior_summary_git_blob=PINS[bulk.SUMMARY],
        carrier=bulk.summarize_carrier(acquisition),source_files={name:dict(bytes=size,sha256=digest) for name,(size,digest) in bulk.pix.SOURCE_FILES.items()},
        observations=observations,original_pixels_published=False,original_runtime_executed=False,strict_failure_promotions=0)

def verify(report,old,native,failures):
    assert report["schema"]=="stoneage.pet68.rd_boundary.r1" and report["source_grade"]=="SAME_SAVED_TW85_CARRIER"
    assert report["prior_receipt_git_blob"]==PINS[bulk.RECEIPT] and report["prior_summary_git_blob"]==PINS[bulk.SUMMARY]
    assert report["carrier"]==bulk.summarize_carrier(bulk.load(bulk.CARRIER))
    assert report["source_files"]=={name:dict(bytes=size,sha256=digest) for name,(size,digest) in bulk.pix.SOURCE_FILES.items()}
    assert not report["original_pixels_published"] and not report["original_runtime_executed"] and report["strict_failure_promotions"]==0
    obs=report["observations"];assert set(obs)=={str(n) for n in failures}
    qualified=set();status=Counter()
    for n in failures:
        row=obs[str(n)]
        assert all(row[k]==v for k,v in native[n].items())
        expected=row["width"]*row["height"]
        assert row["strict_status_retained"]=="STRICT_DECODE_REJECTED" and row["expected_canvas_pixels"]==expected
        assert row["encoded_payload_bytes"]==row["size"]-16
        assert row["status"] in (BOUND,"UNQUALIFIED_BOUNDARY")
        status[row["status"]]+=1
        if row["status"]==BOUND:
            q=row["terminal_command"]
            assert row["flag"]==1 and row["stream_length"]==expected+1 and row["excess_count"]==1 and row["excess_all_zero"] is True
            assert (q["control"],q["count"],q["output_start"],q["output_end"],q["command_end"])==(0xc2,2,expected-1,expected+1,row["encoded_payload_bytes"])
            assert 0<=q["command_offset"]<q["command_end"] and q["command_end"]-q["command_offset"]==1
            for k in ("full_stream_sha256","canvas_prefix_sha256"):assert len(bytes.fromhex(row[k]))==32
            qualified.add(n)
        else:assert row["canvas_prefix_sha256"] is None
    remaining=set(failures)-qualified
    sc=Counter();gc=Counter();groups={}
    for group in old["groups"]:
        states=[]
        for a in group["sequences"]:
            miss=set(a["missing_bitmaps"])&set(failures)
            if a["status"]=="SENTINEL_ONLY":s="SENTINEL_ONLY"
            elif miss&remaining:s="INCOMPLETE_CANVAS"
            elif miss:s="BOUNDED_CANVAS_COMPLETE"
            else:s="STRICT_COMPLETE"
            states.append(s);sc[s]+=1
        nonempty=[s for s in states if s!="SENTINEL_ONLY"]
        g="STRICT_COMPLETE" if nonempty and all(s=="STRICT_COMPLETE" for s in nonempty) else "BOUNDED_CANVAS_COMPLETE" if nonempty and all(s!="INCOMPLETE_CANVAS" for s in nonempty) else "PARTIAL"
        groups[group["group_index"]]=g;gc[g]+=1
    tc=Counter()
    for row in old["templates"]:
        ss=[groups[g] for g in row["groups"]]
        tc["STRICT_COMPLETE" if all(s=="STRICT_COMPLETE" for s in ss) else "BOUNDED_CANVAS_COMPLETE" if all(s!="PARTIAL" for s in ss) else "PARTIAL"]+=1
    assert sum(sc.values())==24144 and sum(gc.values())==427 and sum(tc.values())==467
    assert sc["STRICT_COMPLETE"]==24078 and gc["STRICT_COMPLETE"]==392 and tc["STRICT_COMPLETE"]==430
    remaining_frames=bounded_frames=0
    for f in bulk.gzrows(bulk.PINS["frames"][0]):
        if int(f["group_index"]) not in groups or f["sentinel"]=="1":continue
        n=int(f["bmp_no"]);remaining_frames+=n in remaining;bounded_frames+=n in qualified
    assert remaining_frames+bounded_frames==88
    return dict(schema="stoneage.pet68.rd_boundary_summary.r1",source_receipt_sha256=sha(bulk.stable(report)),
        strict_bitmaps=113243,strict_exceptions=68,qualified_canvas_bitmaps=len(qualified),canvas_unresolved_bitmaps=len(remaining),canvas_covered_bitmaps=113243+len(qualified),
        boundary_status=dict(status),bounded_frame_positions=bounded_frames,remaining_canvas_frame_positions=remaining_frames,
        sequence_status=dict(sc),group_status=dict(gc),template_status=dict(tc),unqualified_bitmaps=sorted(remaining),
        strict_failure_promotions=0,original_runtime_verified=False,official_species_count=None,official_acquisition_closures=0)

def selftest():
    def block(payload):
        return b"RD"+bytes([1,0])+struct.pack("<iiI",2,2,16+len(payload))+payload
    a=diagnose(block(bytes([3,1,2,3,0xc2])),2,2)
    assert a["status"]==BOUND and a["canvas_prefix_sha256"]==sha(bytes([1,2,3,0]))
    assert diagnose(block(bytes([5,1,2,3,4,5])),2,2)["status"]=="UNQUALIFIED_BOUNDARY"
    assert diagnose(block(bytes([3,1,2,3,0xc3])),2,2)["status"]=="UNQUALIFIED_BOUNDARY"
    assert diagnose(block(bytes([4,1,2,3,4])),2,2)["status"]=="UNQUALIFIED_BOUNDARY"
    print("PET68_SELFTEST_PASS",flush=True)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--plan-only",action="store_true");p.add_argument("--source-dir",type=Path);p.add_argument("--acquisition",type=Path);p.add_argument("--selftest",action="store_true")
    a=p.parse_args();assert bool(a.source_dir)==bool(a.acquisition)
    selftest()
    if a.selftest:return
    old,native,failures=plan()
    if a.plan_only:print("PET68_PLAN",len(failures));return
    if a.source_dir:
        report=read_original(a.source_dir,bulk.load(a.acquisition),native,failures)
        summary=verify(report,old,native,failures)
        RECEIPT.write_bytes(bulk.stable(report));SUMMARY.write_bytes(bulk.stable(summary))
    else:
        report=bulk.load(RECEIPT);summary=verify(report,old,native,failures)
        assert SUMMARY.read_bytes()==bulk.stable(summary)
    print("PET68_SUMMARY="+json.dumps(summary,sort_keys=True,separators=(",",":")),flush=True)
if __name__=="__main__":main()
