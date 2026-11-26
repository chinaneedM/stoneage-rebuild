"""PET102 custody: check actual derived artifact and replay immutable metadata."""
import argparse
import json
from pathlib import Path
import zipfile
from tools import stoneage_pet_high_first_102_tw85_master_screen as src
ROOT=src.ROOT
P=src.P
REPORT=P/"PET-HIGH-FIRST-102-TW85-EMBEDDED-MASTER-SCREEN-R1.json"
CUSTODY=P/"PET-HIGH-FIRST-102-CUSTODY-R1.json"
RAW_SHA="006bdaa445f4286f22c5a73b0473f8f0e850f1fe9150a6c099cc9d70f1e3106e"
ACQ_SHA="1bb0af733b9772c3b809aa8e3aad46ff612b6dbf2e07c3a47d67b8e80e40fa6d"
ZIP_SHA="c2af3bc4ad1dcc566077b4b8dd720842efa4891f241ca3ca8b9240cf088b9122"
HEAD="adec33e089fc5d4f64815b0d3c44a1caffddc27e"
WRAPPER="971780abc65ed29a6a7aeb1a528c7db2ef07b11a188e56deaef90a54986609f5"
MSI="8f99ceb13eb91fa9231bf1b6ee2c7052df97d59425171c03103732f8795a4bdc"
def inventory(d):
    s=d["inspection"]["inventory"]["samples"][0]
    result={x["path"]:(x["size"],x["sha256"]) for x in s["files"]}
    assert len(result)==s["file_count"]==557
    return result
def verify_report(raw):
    assert src.sha(raw)==RAW_SHA
    r=json.loads(raw); d=src.inputs()
    assert r["source_pins"]=={str(p.relative_to(ROOT)):h for p,h in src.PINS.items()}
    assert not r["official_closures"] and not r["original_assets_published"] and not r["original_program_executed"]
    names=set(src.EXPECTED_PROGRAMS)|src.SMALL
    assert set(r["files"])==names and len(names)==18
    inv=inventory(d[src.MANIFEST]); tokens={}
    for name,x in r["files"].items():
        assert (x["original_bytes"],x["original_sha256"])==inv[x["path"]]
        assert Path(x["path"]).name==name
        if name in d[src.GRID]["programs"]:
            g=d[src.GRID]["programs"][name]
            assert (x["scanned_bytes"],x["scanned_sha256"])==(g["unpacked_bytes"],g["unpacked_sha256"])
        if x["representation"]!="STATIC_UPX_UNPACKED":
            assert (x["scanned_bytes"],x["scanned_sha256"])==(x["original_bytes"],x["original_sha256"])
        assert not x["signature_hits"] and not x["three_distinct_template_stride_candidates"]
        if x["token_hits"]:
            tokens[name]={}
        for h in x["token_hits"]:
            assert h["token"] in src.TOKENS and h["encoding"] in ("ascii","utf-16le")
            size=len(h["token"].encode(h["encoding"]))
            assert h["offsets"]==sorted(set(h["offsets"])) and all(0<=i<=x["scanned_bytes"]-size for i in h["offsets"])
            tokens[name].setdefault(h["token"],{})[h["encoding"]]=len(h["offsets"])
    patterns=src.patterns(d[src.CAT]["pet_flag_1_field_projections"])
    summary=dict(bytes_scanned=sum(x["scanned_bytes"] for x in r["files"].values()),distinct_signatures=len(patterns),files=len(names),signature_hit_files=0,signature_layouts=sorted({k[0] for k in patterns}),stride_candidate_files=0,token_hit_files=len(tokens))
    assert r["summary"]==summary
    assert (summary["bytes_scanned"],summary["distinct_signatures"],summary["token_hit_files"])==(4936120,2291,4)
    # Bounded post-screen classification: data-section literal positions only.
    expected_album={"sa.exe":36,"sb.exe":35,"sc.exe":21,"sd.exe":34}
    assert set(tokens)==set(expected_album)
    for name,count in expected_album.items():
        assert tokens[name]=={"album_":{"ascii":count},"album_13":{"ascii":1},"savedata.dat":{"ascii":1},"auto.dat":{"ascii":1},"AISetting.dat":{"ascii":1}}
        x=r["files"][name]
        for h in x["token_hits"]:
            for i in h["offsets"]:
                assert any(sec["name"]==".data" and sec["file_offset"]<=i and i+len(h["token"])<=sec["file_offset"]+sec["raw_size"] for sec in x["pe_sections"])
        hits=next(h["offsets"] for h in x["token_hits"] if h["token"]=="album_")
        gaps=[b-a for a,b in zip(hits,hits[1:])]
        assert sorted(gaps)==[20]*(count-2)+[36]
        assert next(h["offsets"] for h in x["token_hits"] if h["token"]=="album_13")[0] in hits
    assert sum(expected_album.values())==126
    assert not any("album" in p.lower() for p in inv)
    for name in ("Startup.exe","StoneAge2.exe"):
        assert r["files"][name]["known_album_grid_probe"]=={"anchors":[],"status":"ANCHOR_MISSING_OR_NONUNIQUE"}
    return summary,tokens
def receipt(archive):
    z=archive.read_bytes();assert len(z)==71105 and src.sha(z)==ZIP_SHA
    with zipfile.ZipFile(archive) as f:
        assert sorted(f.namelist())==["pet102-custody.json","pet102-report.json"]
        raw=f.read("pet102-report.json"); a=f.read("pet102-custody.json")
    assert src.sha(a)==ACQ_SHA
    acq=json.loads(a); expected=src.inputs()[src.MANIFEST]
    assert acq["github_head_sha"]==HEAD and str(acq["github_run_id"])=="45812005473"
    assert acq["status"]=="MSI_CLIENT_PAYLOAD_ACQUISITION_AND_INVENTORY_COMPLETE"
    assert not any(acq[k] for k in ("official_clean_client_authenticated","original_payload_published","server_quest_pet_data_inferred"))
    assert acq["assembled_installer"]==expected["assembled_installer"] and acq["assembled_installer"]["sha256"]==WRAPPER
    ins=acq["inspection"]
    assert ins["msi_sha256"]==MSI and ins["wrapper_sha256"]==WRAPPER
    assert not any(ins[k] for k in ("installed_or_executed","publisher_authenticity_proven","original_server_quest_pet_master_data_proven"))
    assert inventory(acq)==inventory(expected)
    assert len(acq["parts"])==len(expected["parts"])==6
    for p,q in zip(acq["parts"],expected["parts"]):
        assert (p["part"],p["bytes"],p["sha256"])==(q["part"],q["bytes"],q["sha256"])
    s,t=verify_report(raw)
    c=dict(schema="stoneage.pet102.custody.r1",source_head=HEAD,run=45812005473,job=139881951001,artifact=15113441720,zip_bytes=len(z),zip_sha256=ZIP_SHA,report_sha256=RAW_SHA,report_git_blob=src.blob(raw),acquisition_json_sha256=ACQ_SHA,wrapper_sha256=WRAPPER,msi_sha256=MSI,authenticated_parts=6,authenticated_inventory_members=557,summary=s,token_occurrences=t,official_closures=0,original_assets_published=False)
    return raw,c
def verify():
    raw=REPORT.read_bytes();s,t=verify_report(raw);c=json.loads(CUSTODY.read_bytes())
    assert c==dict(schema="stoneage.pet102.custody.r1",source_head=HEAD,run=45812005473,job=139881951001,artifact=15113441720,zip_bytes=71105,zip_sha256=ZIP_SHA,report_sha256=RAW_SHA,report_git_blob=src.blob(raw),acquisition_json_sha256=ACQ_SHA,wrapper_sha256=WRAPPER,msi_sha256=MSI,authenticated_parts=6,authenticated_inventory_members=557,summary=s,token_occurrences=t,official_closures=0,original_assets_published=False)
    print("PET102_VERIFIED="+json.dumps(c,ensure_ascii=False,sort_keys=True),flush=True)
def main():
    p=argparse.ArgumentParser();p.add_argument("--artifact",type=Path);a=p.parse_args()
    if a.artifact:
        raw,c=receipt(a.artifact)
        REPORT.write_bytes(raw); CUSTODY.write_bytes(src.stable(c))
    verify()
if __name__=="__main__":main()
