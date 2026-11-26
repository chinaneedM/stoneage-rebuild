"""PET101 immutable source receipt replay and native CN50 full-motion projection."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import zipfile
from tools.stoneage_pet_high_first_57_coverage import ROOT, blob
from tools import stoneage_pet_high_first_100_cn50_full_motion as pre

P=ROOT/"research/pets"
PREFLIGHT=P/"PET-HIGH-FIRST-100-CN50-FULL-MOTION-PREFLIGHT-R1.json.gz"
PC=P/"PET-HIGH-FIRST-100-CUSTODY-R1.json"
RAW=P/"PET-HIGH-FIRST-101-CN50-ORIGINAL-RD-R1.json"
OUT=P/"PET-HIGH-FIRST-101-CN50-MOTION-PROJECTION-R1.json"
CUSTODY=P/"PET-HIGH-FIRST-101-CUSTODY-R1.json"
MANIFEST=P/"PET-HIGH-FIRST-32-UNIFIED-SOURCE-LOOKUP-MANIFEST-R1.json"
PINS={PREFLIGHT:"3b2a0b8fd7a3bf1a750138188b789552d69ce16f",PC:"50d9847d694f9d150f5fe568a4a6a631929a2313",RAW:"f7a50af4bb440008a227d1522d65004dd38a58a6"}
RAW_SHA="f26be92e4a5482c308d82837f97f3378842cf81b0872c4685a7e3cc06a276714"
ZIP_SHA="eb076963bba91eb1bc770908da4b459f612db65c6e02a8bd1e0191a5be855632"
def sha(b): return hashlib.sha256(b).hexdigest()
def stable(d): return (json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
def read(p):
    b=p.read_bytes()
    if p in PINS: assert blob(b)==PINS[p],p
    return b
def hex256(s):
    return isinstance(s,str) and len(s)==64 and len(bytes.fromhex(s))==32

def derive():
    z=read(PREFLIGHT); custody=json.loads(read(PC))
    assert custody["artifact_download_verified"] is True and custody["report_git_blob_sha"]==PINS[PREFLIGHT]
    assert sha(z)==custody["gzip_sha256"] and len(z)==custody["report_bytes"]
    raw=read(RAW); assert sha(raw)==RAW_SHA
    raw_p=gzip.decompress(z); assert sha(raw_p)==custody["raw_json_sha256"]
    p=json.loads(raw_p); del raw_p
    assert p["summary"]==custody["summary"] and p["original_assets_published"] is False
    report=json.loads(raw)
    assert report["source_pins"]==p["source_pins"]
    assert report["source_cab_sha256"]==p["source_manifest"]["cab_sha256"]
    assert report["source_members"]==p["source_manifest"]["input_containers"]
    assert report["original_assets_published"] is False and report["official_clean_pressing_verified"] is False
    targets=p["read_targets"]; obs=report["observations"]
    assert len(targets)==len(obs)==90 and targets.keys()==obs.keys()
    by_bitmap={}; keys={}
    for i,t in targets.items():
        o=obs[i]
        assert all(o[k]==v for k,v in t.items()) and o["status"]=="DUAL_DECODED_INDEX_PIXELS"
        assert hex256(o["index_pixels_sha256"]) and hex256(o["adrn_sha256"])
        key=pre.key(t)
        assert keys.setdefault(key,o["index_pixels_sha256"])==o["index_pixels_sha256"]
        n=str(t["bitmap"]); assert n not in by_bitmap; by_bitmap[n]=i
        b=p["bitmap_refs"][n]
        assert b["grade"]==pre.NEED and t in b["native_candidates"] and b["receipt"] is None
    assert len(keys)==76
    assert Counter(b["grade"] for b in p["bitmap_refs"].values())=={pre.STRICT:142150,pre.BOUNDED:28,pre.NEED:90}
    groups={}; gc=Counter(); sc=Counter(); fc=Counter(); seen=set()
    for i,g in p["groups"].items():
        ss=Counter(); ff=Counter(); new=set()
        for s in g["sequences"]:
            c=Counter(s["frame_grades"]); missing=s["unresolved_bitmaps"]
            assert set(map(str,missing))<=by_bitmap.keys()
            if c.get(pre.NEED,0):
                assert missing
                new.update(by_bitmap[str(n)] for n in missing)
                c[pre.STRICT]+=c.pop(pre.NEED)
            else: assert not missing
            assert set(c)<={pre.STRICT,pre.BOUNDED}
            state="SENTINEL_ONLY" if not c else "BOUNDED_COMPLETE" if c.get(pre.BOUNDED,0) else "STRICT_COMPLETE"
            ss[state]+=1; ff.update(c)
        assert sum(ss.values())>ss["SENTINEL_ONLY"]
        state="BOUNDED_COMPLETE" if ss["BOUNDED_COMPLETE"] else "STRICT_COMPLETE"
        groups[i]=dict(graphic=g["graphic"],spr_sha256=g["sha256"],status=state,frame_grades=dict(ff),sequence_status=dict(ss),new_original_rows=sorted(new,key=int))
        gc[state]+=1; sc.update(ss); fc.update(ff); seen.update(new)
    assert seen==targets.keys()
    positions={}; pc=Counter()
    for a in p["positions"]:
        ids=list(map(str,a["group_indices"])); assert ids and set(ids)<=groups.keys()
        state="ALL_STRICT" if all(groups[i]["status"]=="STRICT_COMPLETE" for i in ids) else "ALL_CANVAS_COMPLETE"
        pc[state]+=1; key=str(a["ordinal"]); assert key not in positions
        positions[key]=dict(name=a["name"],row_sha256=a["row_sha256"],group_ids=ids,status=state)
    summary=dict(native_rows=90,distinct_decode_keys=76,statuses={"DUAL_DECODED_INDEX_PIXELS":90},strict_new_bitmaps=90,remaining_bitmaps=[],sequence_grade=dict(sc),group_grade=dict(gc),position_grade=dict(pc),official_closures=0,original_runtime_verified=False)
    assert summary==report["summary"]
    assert pc=={"ALL_STRICT":284,"ALL_CANVAS_COMPLETE":21}
    assert gc=={"STRICT_COMPLETE":572,"BOUNDED_COMPLETE":22}
    assert sc=={"STRICT_COMPLETE":42415,"BOUNDED_COMPLETE":32,"SENTINEL_ONLY":128}
    assert fc=={pre.STRICT:272892,pre.BOUNDED:40}
    return dict(schema="stoneage.pet101.cn50.native_motion_projection.r1",source_pins={str(k.relative_to(ROOT)):v for k,v in PINS.items()},positions=positions,groups=groups,summary=summary,bitmap_grade={pre.STRICT:142240,pre.BOUNDED:28},frame_grade=dict(fc),official_identity_verified=False,original_runtime_verified=False,original_assets_published=False)

def receipt(archive):
    z=archive.read_bytes(); assert len(z)==13519 and sha(z)==ZIP_SHA
    with zipfile.ZipFile(archive) as f:
        assert f.namelist()==["pet101.json"]; raw=f.read("pet101.json")
    assert raw==read(RAW)
    return dict(schema="stoneage.pet101.cn50.original_rd_custody.r1",source_head="fced346294530606c374dc009777a0e4ac115fd5",run=45809235229,job=139872424658,artifact=15111326113,zip_bytes=len(z),zip_sha256=sha(z),report_bytes=len(raw),report_sha256=sha(raw),report_git_blob=blob(raw),original_assets_published=False,official_identity_verified=False,original_runtime_verified=False)

def entries():
    return {k:dict(path=str(p.relative_to(ROOT)),git_blob=blob(p.read_bytes()),expected_array=None,expected_rows=None) for k,p in {"hf101":OUT,"hf101_raw":RAW,"hf101_custody":CUSTODY}.items()}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--artifact",type=Path); args=ap.parse_args()
    p=derive()
    if args.artifact:
        CUSTODY.write_bytes(stable(receipt(args.artifact))); OUT.write_bytes(stable(p))
        m=json.loads(MANIFEST.read_bytes()); m["sources"].update(entries())
        m["supplement_hf101"]=dict(scope="Native CN50 album exact RD full-motion evidence, not official identity, runtime or palette selection.",source_head="b33783ffa7c05ef3c7f38cf5f7354f692d79d5a4")
        MANIFEST.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    else:
        assert OUT.read_bytes()==stable(p)
        c=json.loads(CUSTODY.read_bytes())
        assert (c["report_git_blob"],c["report_sha256"],c["zip_sha256"],c["report_bytes"])==(PINS[RAW],RAW_SHA,ZIP_SHA,len(read(RAW)))
        assert (c["source_head"],c["run"],c["job"],c["artifact"],c["zip_bytes"])==("fced346294530606c374dc009777a0e4ac115fd5",45809235229,139872424658,15111326113,13519)
        assert not any(c[k] for k in ("original_assets_published","official_identity_verified","original_runtime_verified"))
        m=json.loads(MANIFEST.read_bytes()); assert all(m["sources"][k]==v for k,v in entries().items())
    print("PET101_ACCEPT_SUMMARY="+json.dumps(p["summary"],sort_keys=True,separators=(",",":")),flush=True)
if __name__=="__main__": main()
