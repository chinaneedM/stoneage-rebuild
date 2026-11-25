"""PET71: original TW85 named-motion residuals; strict and bounded evidence stay separate."""
import argparse
from collections import Counter
import gzip
import json
import mmap
from pathlib import Path
import struct
import tempfile
from tools import stoneage_pet_high_first_70_full_motion_coverage as base
from tools import stoneage_pet_high_first_67_bulk_pixels as bulk
from tools import stoneage_pet_high_first_68_rd_boundary as boundary
from tools import stoneage_pet_high_first_66_motion_inheritance as prev
from tools.stoneage_pet_high_first_57_coverage import ROOT,PINS,blob
from tools.stoneage_rd_codec import parse_rd_header

P=ROOT/"research/pets"
PLAN=P/"PET-HIGH-FIRST-70-FULL-MOTION-COVERAGE-SUMMARY-R1.json"
PLAN_SHA="9691f21d589620595fb76611c3f810ee45b4dbc9"
RECEIPT=P/"PET-HIGH-FIRST-71-BULK-NAMED-PIXELS-R1.json.gz"
SUMMARY=P/"PET-HIGH-FIRST-71-BULK-NAMED-PIXELS-SUMMARY-R1.json"
STRICT="STRICT_PIXEL_RECEIPT"
BOUNDED="BOUNDED_CANVAS_RECEIPT"
UNRESOLVED="SOURCE_READ_UNRESOLVED"
SCHEMA="stoneage.pet71.bulk_named_original_pixels.r1"
def files():return {n:dict(bytes=s,sha256=h) for n,(s,h) in bulk.pix.SOURCE_FILES.items()}
def plan():
    assert blob(PLAN.read_bytes())==PLAN_SHA
    old=base.derive()
    assert old["summary"]==bulk.load(PLAN)["summary"]
    rows=old["source_read_targets"]
    assert len(rows)==164781
    assert len({base.key(x) for x in rows.values()})==163376
    assert len({x["bitmap"] for x in rows.values()})==164781
    assert all(i==r["index"] for i,r in rows.items())
    return old,rows
def diagnose(block,w,h):
    strict=bulk.decode(block,w,h)
    bounded=None
    if (strict["status"]=="STRICT_DECODE_REJECTED" and strict.get("decoder_two_error")=="pixel overflow"
        and strict.get("decoder_one_error")==f"decoded output exceeds expected length: {w*h+1} > {w*h}"):
        header=parse_rd_header(block)
        if (header["flag"],header["width_s"],header["height_s"],header["stored_size"])==(1,w,h,len(block)):
            bounded=boundary.diagnose(block,w,h)
    grade=STRICT if strict["status"]=="DUAL_DECODED_INDEX_PIXELS" else BOUNDED if bounded and bounded["status"]==boundary.BOUND else UNRESOLVED
    return dict(grade=grade,strict=strict,boundary=bounded)
def selftest():
    def block(payload):return b"RD"+bytes([1,0])+struct.pack("<iiI",2,2,16+len(payload))+payload
    assert diagnose(block(bytes([4,1,2,3,4])),2,2)["grade"]==STRICT
    assert diagnose(block(bytes([3,1,2,3,0xc2])),2,2)["grade"]==BOUNDED
    assert diagnose(block(bytes([5,1,2,3,4,5])),2,2)["grade"]==UNRESOLVED
    assert diagnose(block(bytes([3,1,2,3,0xc3])),2,2)["grade"]==UNRESOLVED
    assert diagnose(b"not an RD block",2,2)["grade"]==UNRESOLVED
    print("PET71_SELFTEST_PASS",flush=True)
def read_original(directory,rows,acquisition):
    assert bulk.summarize_carrier(acquisition)==bulk.summarize_carrier(bulk.load(bulk.CARRIER))
    bulk.pix.qualify_pair(directory)
    for filename in ("adrn_158.bin","real_158.bin"):
        bulk.pix.original_check(directory/filename,bulk.pix.SOURCE_FILES[filename])
    with tempfile.TemporaryDirectory() as tmp:
        paths=[Path(tmp)/k for k in ("group","animation","frame")]
        bulk.pix.export_cn50_spr(directory/"spradrn_137.bin",directory/"spr_137.bin",*paths)
        for p,r in zip(paths,(PINS["groups"][0],prev.EXTRA["tw85_animation"][0],PINS["frames"][0]),strict=True):
            assert p.read_bytes()==r.read_bytes(),r
    adrn=(directory/"adrn_158.bin").read_bytes()
    obs={};cache={}
    with (directory/"real_158.bin").open("rb") as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as real:
        for i,r in sorted(rows.items(),key=lambda x:x[1]["offset"]):
            raw=adrn[i*80:(i+1)*80]
            n,off,size,_,_,w,h,_=bulk.pix.COLS.unpack(raw)
            assert (n,off,size,w,h,bulk.sha(raw))==(r["bitmap"],r["offset"],r["size"],r["width"],r["height"],r["adrn_sha256"]),i
            assert 0<=off and 16<=size<=len(real)-off,i
            block=real[off:off+size]
            assert bulk.sha(block)==r["rd_sha256"],i
            key=base.key(r)
            if key not in cache:cache[key]=diagnose(block,w,h)
            obs[str(i)]=dict(**r,**cache[key])
            if len(obs)%20000==0:print("PET71_PROGRESS",len(obs),"/",len(rows),flush=True)
    return dict(schema=SCHEMA,plan_git_blob=PLAN_SHA,carrier=bulk.summarize_carrier(acquisition),source_files=files(),
        original_assets_published=False,original_runtime_verified=False,official_identity_verified=False,
        distinct_decode_keys=len(cache),observations=obs)
def verify_result(x):
    s=x["strict"];b=x["boundary"];grade=x["grade"]
    assert s["status"] in ("DUAL_DECODED_INDEX_PIXELS","NONPOSITIVE_OR_OVERSIZE_GEOMETRY","INVALID_RD_HEADER","UNSUPPORTED_ENCODING","DECODER_DISAGREEMENT","STRICT_DECODE_REJECTED")
    if s["status"]=="DUAL_DECODED_INDEX_PIXELS":
        assert grade==STRICT and b is None
        base.digest(s["index_pixels_sha256"])
    else:
        assert s["index_pixels_sha256"] is None
        if b is not None:
            expected=x["width"]*x["height"]
            assert s["status"]=="STRICT_DECODE_REJECTED" and s["decoder_two_error"]=="pixel overflow"
            assert s["decoder_one_error"]==f"decoded output exceeds expected length: {expected+1} > {expected}"
            assert b["strict_status_retained"]=="STRICT_DECODE_REJECTED"
            assert b["expected_canvas_pixels"]==expected and b["encoded_payload_bytes"]==x["size"]-16
            if b["status"]==boundary.BOUND:
                q=b["terminal_command"]
                assert grade==BOUNDED and b["flag"]==1 and b["stream_length"]==expected+1 and b["excess_count"]==1 and b["excess_all_zero"] is True
                assert (q["control"],q["count"],q["output_start"],q["output_end"],q["command_end"])==(0xc2,2,expected-1,expected+1,b["encoded_payload_bytes"])
                assert 0<=q["command_offset"]<q["command_end"] and q["command_end"]-q["command_offset"]==1
                base.digest(b["canvas_prefix_sha256"]);base.digest(b["full_stream_sha256"])
            else:assert b["status"]=="UNQUALIFIED_BOUNDARY" and grade==UNRESOLVED and b["canvas_prefix_sha256"] is None
        else:assert grade==UNRESOLVED
def verify(report,old,rows):
    assert report["schema"]==SCHEMA and report["plan_git_blob"]==PLAN_SHA
    assert report["carrier"]==bulk.summarize_carrier(bulk.load(bulk.CARRIER)) and report["source_files"]==files()
    assert not any(report[k] for k in ("original_assets_published","original_runtime_verified","official_identity_verified"))
    obs=report["observations"];assert set(obs)=={str(i) for i in rows}
    keys={};new={};failures=[];new_status=Counter();strict_status=Counter()
    for i,row in rows.items():
        x=obs[str(i)]
        assert all(x[k]==v for k,v in row.items()),i
        verify_result(x)
        result={k:x[k] for k in ("grade","strict","boundary")}
        key=base.key(row)
        assert keys.setdefault(key,result)==result
        assert row["bitmap"] not in new
        new[row["bitmap"]]=x["grade"];new_status[x["grade"]]+=1;strict_status[x["strict"]["status"]]+=1
        if x["grade"]==UNRESOLVED:
            failures.append(dict(index=i,bitmap=row["bitmap"],rd_sha256=row["rd_sha256"],strict=x["strict"],boundary=x["boundary"]))
    assert len(keys)==report["distinct_decode_keys"]==163376
    grades={n:x["grade"] for n,x in old["bitmap_evidence"].items()}
    assert set(new)=={n for n,g in grades.items() if g==base.NEED}
    grades.update(new)
    bc=Counter(grades.values());sc=Counter();gc=Counter();fc=Counter();pc=Counter();gs={}
    groups={g["group_index"]:g for g in old["groups"]}
    seq=prev.sequence_tables(groups,prev.EXTRA["tw85_animation"][0],PINS["frames"][0])
    for i,g in groups.items():
        counts=Counter();states=[]
        for j,a in seq[i].items():
            numbers=[f[0] for f in a["frames"] if f[0] is not None]
            c=Counter(grades[n] for n in numbers);counts.update(c);fc.update(c)
            if not numbers:status="SENTINEL_ONLY"
            elif any(k not in (STRICT,BOUNDED) for k in c):status="INCOMPLETE"
            elif c[BOUNDED]:status="BOUNDED_COMPLETE"
            else:status="STRICT_COMPLETE"
            if g["sequences"][j]["status"] in ("STRICT_COMPLETE","BOUNDED_COMPLETE"):assert status==g["sequences"][j]["status"]
            sc[status]+=1;states.append(status)
        assert sum(counts.values())==g["mapped_frames"]+g["missing_frames"]
        nonempty=[s for s in states if s!="SENTINEL_ONLY"]
        complete=[s for s in nonempty if s!="INCOMPLETE"]
        if not nonempty:status="NO_NONEMPTY_SEQUENCES"
        elif len(complete)==len(nonempty):status="BOUNDED_COMPLETE" if counts[BOUNDED] else "STRICT_COMPLETE"
        elif complete:status="PARTIAL"
        else:status="NO_COMPLETE_SEQUENCE"
        if g["status"] in ("STRICT_COMPLETE","BOUNDED_COMPLETE"):assert status==g["status"]
        gs[i]=status;gc[status]+=1
    for p in old["album_positions"]:
        ss=[gs[i] for i in p["group_indices"]]
        complete=[s for s in ss if s in ("STRICT_COMPLETE","BOUNDED_COMPLETE")]
        status="ALL_CANVAS_COMPLETE" if len(complete)==len(ss) else "SOME_CANVAS_COMPLETE" if complete else "NO_COMPLETE_GROUP"
        if p["status"]=="ALL_CANVAS_COMPLETE":assert status==p["status"]
        pc[status]+=1
    assert sum(bc.values())==282279 and sum(sc.values())==74652 and sum(gc.values())==1317 and sum(pc.values())==1889
    assert sum(fc.values())==516608 and sum(new_status.values())==164781
    assert bc[STRICT]==117429+new_status[STRICT] and bc[BOUNDED]==69+new_status[BOUNDED]
    assert bc[UNRESOLVED]==len(failures)==new_status[UNRESOLVED]
    return dict(schema="stoneage.pet71.bulk_named_pixels_summary.r1",source_receipt_sha256=bulk.sha(bulk.stable(report)),
        target_rows=164781,distinct_decode_keys=len(keys),new_status=dict(new_status),strict_decode_status=dict(strict_status),
        bitmap_status=dict(bc),frame_status=dict(fc),sequence_status=dict(sc),group_status=dict(gc),position_status=dict(pc),
        unresolved_rows=sorted(failures,key=lambda x:x["index"]),official_species_count=None,official_acquisition_closures=0,original_runtime_verified=False)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--plan-only",action="store_true");p.add_argument("--selftest",action="store_true")
    p.add_argument("--source-dir",type=Path);p.add_argument("--acquisition",type=Path);a=p.parse_args()
    assert bool(a.source_dir)==bool(a.acquisition)
    selftest()
    if a.selftest:return
    old,rows=plan()
    if a.plan_only:
        print("PET71_PLAN",len(rows),163376,flush=True);return
    if a.source_dir:
        report=read_original(a.source_dir,rows,bulk.load(a.acquisition))
        summary=verify(report,old,rows)
        RECEIPT.write_bytes(gzip.compress(bulk.stable(report),compresslevel=6,mtime=0))
        SUMMARY.write_bytes(bulk.stable(summary))
    else:
        assert blob(RECEIPT.read_bytes())=="157cdf72e74ecb328a15e16771cb36e18735ca08"
        assert blob(SUMMARY.read_bytes())=="c55a2c74e03ca8af7d41b5888b290106ffe260c3"
        report=json.loads(gzip.decompress(RECEIPT.read_bytes()))
        summary=verify(report,old,rows)
        assert SUMMARY.read_bytes()==bulk.stable(summary)
    print("PET71_SUMMARY="+json.dumps({k:v for k,v in summary.items() if k!="unresolved_rows"},sort_keys=True,separators=(",",":")),flush=True)
if __name__=="__main__":main()
