"""PET123: independent PET122 custody and shared compiled name-table audit."""
import argparse,hashlib,json,zipfile,collections
from pathlib import Path
from tools import stoneage_pet_high_first_122_cn85_complete_transfer as prev
SHA="adae8c922e30fcb14e30e6ab2de6a0c4428f1713a87d704f792f525ec61daf67"
ZIP="975abd371ee1aaf3572fc1fd8d9f2f9e557604ee0e576bbe26ebd43b02fcbb7d"
BLOB="a6ed895e5b6b18ebaa1c02e809da5a17937dd176"
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--artifact",type=Path,required=True);a=ap.parse_args()
    z=a.artifact.read_bytes();assert len(z)==124361 and sha(z)==ZIP
    with zipfile.ZipFile(a.artifact) as f:
        assert len(f.namelist())==1
        raw=f.read(f.namelist()[0])
    assert len(raw)==769206 and raw==prev.REPORT.read_bytes() and sha(raw)==SHA and prev.old.p.idx.blob(raw)==BLOB
    d=json.loads(raw);t=d["transfer"]
    assert d["original_client_verified"] and d["pet_payload_extracted"] and not d["original_assets_published"] and d["official_closures"]==0
    assert t["complete"] and t["cdx_digest_matches"] and t["bytes"]==1351371747
    assert t["sha1_base32"]==d["capture"]["digest"]=="HPHIMJS3N6XJWPGDS3LNPYHDAHFPDCZB"
    assert t["sha256"]=="747dfd8d44274d5d128c2784ed32462eb1930861160003445ec6f7cfe827e843"
    assert len(t["attempts"])==1 and t["attempts"][0]["result"]=="EXACT_BYTES"
    directory=json.loads(prev.old.p.R117.read_bytes())["results"][0]["entries"]
    assert [(x["name"],x["bytes"],x["crc32"]) for x in d["zip_members"]]==[(x["name"],x["uncompressed_bytes"],x["crc32"]) for x in directory]
    assert len(directory)==9
    inv={x["name"]:x["size"] for x in json.loads(prev.old.prev.REPORT.read_bytes())["results"][0]["directory"]["all_entries"]}
    resources=d["selected_resources"];assert len(resources)==8 and len({x["name"] for x in resources})==8
    assert all(x["result"]=="EXTRACTED_SIZE_VERIFIED" and x["bytes"]==x["expected_bytes"]==inv[x["source_path"]] and x["returncode"]==0 for x in resources)
    an=d["analysis"];s=an["spr"];g=s["group_rows"]
    assert len(g)==s["groups"]==s["exact_group_spans"]==1837
    assert sum(int(x["anim_count"]) for x in g)==s["animations"]==122073
    assert s["frames"]==784418 and s["sentinel_frames"]==4760
    physical=sorted(g,key=lambda x:int(x["offset"]))
    assert int(physical[0]["offset"])==0 and int(physical[-1]["end_offset"])==s["spr_bytes"]==9309056
    for i,x in enumerate(physical):
        assert int(x["offset"])<int(x["end_offset"])==int(x["next_offset"])
        if i:assert int(physical[i-1]["end_offset"])==int(x["offset"])
    ad=an["adrn"];assert ad["records"]==458990 and ad["unique_bitmap_ids"]==458898 and ad["out_of_declared_real_bounds"]==0
    assert ad["declared_real_bytes"]==ad["max_end"]==1839180217 and not ad["actual_real_bytes_verified"]
    assert an["album"]["bytes"]==99*(16+570*80)==4515984
    programs=an["compiled_table_candidates"];assert [p["program"] for p in programs]==["StoneageNg.dll","sa_85_free.exe","sa_25_payment.exe"]
    assert not programs[0]["candidates"]
    a,b=[p["candidates"] for p in programs[1:]]
    assert [x["rows"] for x in a]==[544,34]
    for i,(x,y) in enumerate(zip(a,b)):
        assert x["table_source_sha256"]==y["table_source_sha256"] and x["entries"]==y["entries"] and x["stride"]==y["stride"]==28
        assert len(x["entries"])==x["rows"] and not x["native_pet_id_or_release_proven"]
    assert a[1]["file_offset"]-(a[0]["file_offset"]+544*28)==b[1]["file_offset"]-(b[0]["file_offset"]+544*28)==49*28
    rows=[r for c in a for r in c["entries"]];filled=[r for r in rows if r["slot"]!=-1]
    assert len(rows)==578 and len(filled)==521 and len({r["slot"] for r in filled})==len({r["face"] for r in filled})==521
    assert {r["slot"] for r in filled}==set(range(487))|set(range(536,570))
    names=collections.Counter(r["name"] for r in filled)
    assert len(names)==513 and sum(n>1 for n in names.values())==8
    spr={int(x["spr_no"]) for x in g}
    assert sum(r["face"] in spr for r in filled)==0 and sum(100250+r["slot"] in spr for r in filled)==295
    print("PET123_RECEIPT_PASS",BLOB,"ARCHIVE_BYTES",t["bytes"],"RESOURCE_COUNT",len(resources),"NAME_POSITIONS",len(filled),"DISTINCT_NAMES",len(names),"UNPARSED_RECORD_LENGTHS",49,flush=True)
if __name__=="__main__":main()
