"""Read only PET100's remaining exact CN50 resource blocks from qualified CAB.
No native executable is run; derived SHA/metadata only.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
import mmap
from pathlib import Path
import struct
import subprocess
import tempfile
from tools import stoneage_cn50_original_resource_catalog as cat
from tools import stoneage_pet_high_first_100_cn50_full_motion as pre
from tools.stoneage_pet_high_first_67_bulk_pixels import decode
from tools.stoneage_pet_high_first_57_coverage import ROOT, gzrows
from tools.stoneage_stoneage5_msi_probe import load_root, find_entry
from tools.stoneage_stoneage5_cab_probe import iso_file_slice
from tools.stoneage_stoneage5_full_cab_acquisition import (
    EXPECTED_SIZE, checked_layout, download_cab, extracted_inventory)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def plan():
    p = pre.derive()
    observed = json.loads((ROOT / "research/pets/PET-HIGH-FIRST-100-CI-OBSERVED-R1.json").read_text())
    assert p["summary"] == observed["summary"]
    rows = p["read_targets"]
    assert len(rows) == 90
    assert len({pre.key(x) for x in rows.values()}) == 76
    wanted = {}
    for r in gzrows(pre.path("adrn")):
        i = int(r["index"])
        if i not in rows:
            continue
        v = rows[i]
        assert (int(r["bitmapno"]), int(r["adder"]), int(r["size"]), int(r["width"]), int(r["height"]), r["rd_block_sha256"], r["attr_sha256"]) == (v["bitmap"], v["offset"], v["size"], v["width"], v["height"], v["rd_sha256"], v["attr_sha256"])
        assert i not in wanted
        wanted[i] = r
    assert set(wanted) == set(rows)
    return p, wanted

def observe(directory, p, rows, files, cab_sha):
    results = {}
    cache = {}
    with (directory / cat.NAMES["adrn"]).open("rb") as a, (directory / cat.NAMES["real"]).open("rb") as b, mmap.mmap(a.fileno(),0,access=mmap.ACCESS_READ) as adrn, mmap.mmap(b.fileno(),0,access=mmap.ACCESS_READ) as real:
        for i,r in sorted(rows.items()):
            v = p["read_targets"][i]
            raw = adrn[i*80:(i+1)*80]
            expected = (v["bitmap"],v["offset"],v["size"],int(r["xoff"]),int(r["yoff"]),v["width"],v["height"])
            assert len(raw)==80 and struct.unpack_from("<IIIiiii",raw)==expected and sha(raw[28:])==v["attr_sha256"],i
            offset,size=v["offset"],v["size"]
            assert 16<=size and 0<=offset<=offset+size<=len(real),i
            rd=real[offset:offset+size]
            assert sha(rd)==v["rd_sha256"],i
            k=pre.key(v)
            if k not in cache:
                cache[k]=decode(rd,v["width"],v["height"])
            results[str(i)]={**v,"adrn_sha256":sha(raw),**cache[k]}
    assert len(results)==90 and len(cache)==76
    strict={v["bitmap"] for v in results.values() if v["status"]=="DUAL_DECODED_INDEX_PIXELS"}
    assert len({v["bitmap"] for v in results.values()})==90
    remaining={v["bitmap"] for v in results.values()}-strict
    sequences=Counter(); groups=Counter(); positions=Counter()
    grades={}
    for i,g in p["groups"].items():
        states=[]
        for s in g["sequences"]:
            state=s["grade"]
            if state=="INCOMPLETE" and not (set(s["unresolved_bitmaps"]) & remaining):
                assert set(s["unresolved_bitmaps"])<=strict
                state="BOUNDED_COMPLETE" if s["frame_grades"].get(pre.BOUNDED,0) else "STRICT_COMPLETE"
            sequences[state]+=1
            if state!="SENTINEL_ONLY": states.append(state)
        state="NO_NONEMPTY_SEQUENCES" if not states else "INCOMPLETE" if "INCOMPLETE" in states else "BOUNDED_COMPLETE" if "BOUNDED_COMPLETE" in states else "STRICT_COMPLETE"
        groups[state]+=1; grades[i]=state
    for pos in p["positions"]:
        states=[grades[i] for i in pos["group_indices"]]
        state="NO_LINKED_SOURCE_GROUP" if not states else "ALL_STRICT" if all(s=="STRICT_COMPLETE" for s in states) else "ALL_CANVAS_COMPLETE" if all(s in ("STRICT_COMPLETE","BOUNDED_COMPLETE") for s in states) else "SOURCE_GAPS_REMAIN"
        positions[state]+=1
    summary={"native_rows":len(results),"distinct_decode_keys":len(cache),"statuses":dict(Counter(v["status"] for v in results.values())),"strict_new_bitmaps":len(strict),"remaining_bitmaps":sorted(remaining),"sequence_grade":dict(sequences),"group_grade":dict(groups),"position_grade":dict(positions),"official_closures":0,"original_runtime_verified":False}
    return {"schema":"stoneage.pet101.cn50.remaining_original_rd.r1","source_cab_sha256":cab_sha,"source_members":files,"source_pins":p["source_pins"],"summary":summary,"observations":results,"original_assets_published":False,"official_clean_pressing_verified":False}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--plan-only",action="store_true")
    args=ap.parse_args()
    p,rows=plan()
    print("PET101_PLAN="+json.dumps({"rows":len(rows),"keys":p["summary"]["read_target_distinct_rd_keys"]}),flush=True)
    if args.plan_only: return
    source,_,lookup=cat.qualify_sources(ROOT)
    _,_,_,track,carrier,url,_,entries=load_root()
    cab=find_entry(entries,"DATA1.CAB")
    assert cab and int(cab["size"])==EXPECTED_SIZE
    prefix,status,_=iso_file_slice(url,cab,track,0,65536)
    assert status==206
    _,expected=checked_layout(prefix)
    with tempfile.TemporaryDirectory(prefix="stoneage-pet101-") as temp:
        temp=Path(temp); cabfile=temp/"DATA1.CAB"; directory=temp/"contents"; directory.mkdir()
        digest=download_cab(url,cab,track,int(carrier["size"]),cabfile)
        assert digest==source["source"]["cab_sha256"]==p["source_manifest"]["cab_sha256"]
        with cabfile.open("rb") as f: assert f.read(len(prefix))==prefix
        subprocess.run(["cabextract","-q","-d",str(directory),str(cabfile)],check=True,timeout=1500)
        inventory=extracted_inventory(directory,expected)
        assert len(inventory)==413 and all(lookup.get(x["name"])==(x["size"],x["sha256"]) for x in inventory)
        files=cat.verify_four(directory,lookup)
        assert files==p["source_manifest"]["input_containers"]
        report=observe(directory,p,rows,files,digest)
    args.output.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("PET101_SUMMARY="+json.dumps(report["summary"],sort_keys=True,separators=(",",":")),flush=True)

if __name__=="__main__":
    main()
