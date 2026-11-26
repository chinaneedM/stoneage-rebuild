"""Independent PET124 custody, table and actual RD candidate replay; no new source download."""
import hashlib, json, sys, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REPORT = "research/pets/PET-HIGH-FIRST-124-CN85-NATIVE-ALBUM-R1.json"
PRIOR = "research/pets/PET-HIGH-FIRST-122-CN85-COMPLETE-TRANSFER-R1.json"
def sha(x): return hashlib.sha256(x).hexdigest()
def blob(x): return hashlib.sha1(b"blob "+str(len(x)).encode()+b"\0"+x).hexdigest()
def main(artifact):
    z = Path(artifact).read_bytes()
    assert len(z)==125182 and sha(z)=="14a7e63fa4e282f3c526aad794c49d0fe6bf3685af54ecd7871ad8f4b1e14969"
    raw=(ROOT/REPORT).read_bytes()
    assert sha(raw)=="670b886a6126351e5ca42190c87997065606a21422151accecc44fa34ddfebb3"
    assert blob(raw)=="17a42f4de1d9e508b580c88de70bb012d7e03c9b"
    with zipfile.ZipFile(artifact) as f:
        files=[x for x in f.infolist() if not x.is_dir()]
        assert len(files)==1 and Path(files[0].filename).name==Path(REPORT).name
        assert f.read(files[0])==raw
    oldraw=(ROOT/PRIOR).read_bytes()
    assert sha(oldraw)=="adae8c922e30fcb14e30e6ab2de6a0c4428f1713a87d704f792f525ec61daf67"
    assert blob(oldraw)=="a6ed895e5b6b18ebaa1c02e809da5a17937dd176"
    old=json.loads(oldraw);d=json.loads(raw);a=d["analysis"]
    assert d["original_client_reacquired"] and not d["original_assets_published"] and d["official_closures"]==0 and "blocker" not in d
    assert d["transfer"]["complete"] and d["transfer"]["cdx_digest_matches"]
    assert d["transfer"]["sha256"]==old["transfer"]["sha256"]=="747dfd8d44274d5d128c2784ed32462eb1930861160003445ec6f7cfe827e843"
    assert d["transfer"]["bytes"]==1351371747
    assert {x["name"]:(x["bytes"],x["sha256"]) for x in d["resource_receipts"]}=={x["name"]:(x["bytes"],x["sha256"]) for x in old["selected_resources"]}
    real=d["real_receipt"];assert real["name"]=="real_185.bin" and real["bytes"]==1839180217 and real["sha256"]=="c1a691d5316b5ec454e7e9ba17509e9b1e22692cf56eca96bf80f610e5446680"
    p,q=a["programs"];assert a["table_full_span_equal"] and p["table_sha256"]==q["table_sha256"] and p["entries"]==q["entries"]
    assert not p["native_selector_proven"] and not q["native_selector_proven"]
    e=p["entries"];assert len(e)==627 and [x["ordinal"] for x in e]==list(range(627))
    known=[x for x in e if x["strict_old_parser"] and x["slot"]>=0]
    blank=[x for x in e if x["strict_old_parser"] and x["slot"]<0]
    unresolved=[x for x in e if not x["strict_old_parser"]]
    assert (len(known),len(blank),len(unresolved))==(548,57,22)
    assert all(544<=x["ordinal"]<593 and "compiled_label" not in x for x in unresolved)
    assert sum(544<=x["ordinal"]<593 for x in known)==27
    assert len({x["compiled_label"] for x in known})==540
    for prog,oldprog in zip((p,q),old["analysis"]["compiled_table_candidates"][1:]):
        assert prog["program"]==oldprog["program"] and prog["source_sha256"]==oldprog["sha256"]
        for seg,start in zip(oldprog["candidates"],(0,593)):
            for j,x in enumerate(seg["entries"]):
                y=prog["entries"][start+j]
                assert (x["name"],x["slot"],x["face"])==(y["compiled_label"],y["slot"],y["face"])
    album=a["album"]
    assert sum(album["flag_histogram"].values())==99*570 and album["flag_1_2_positions"]==889 and album["exact_compiled_slot_label_matches"]==833
    assert not album["layout_confirmed"] and not album["private_names_or_headers_published"]
    links=a["resource_links"];rows=links["rows"]
    assert not links["native_selector_proven"] and len(rows)==len(known)
    groups={}
    for g in old["analysis"]["spr"]["group_rows"]:
        groups.setdefault(int(g["spr_no"]),[]).append(int(g["index"]))
    for x,y in zip(known,rows):
        assert all(x[k]==y[k] for k in ("ordinal","slot","face","compiled_label"))
        assert not y["native_selector_proven"]
        assert y["ordinal_spr_group_indices"]==groups.get(100250+x["ordinal"],[])
        assert y["slot_spr_group_indices"]==groups.get(100250+x["slot"],[])
        assert y["face_map_number_candidates"]
    assert links["face_map_number_rows"]==548 and links["unique_face_map_number_rows"]==sum(len(y["face_map_number_candidates"])==1 for y in rows)==544
    assert links["ordinal_spr_rows"]==sum(bool(y["ordinal_spr_group_indices"]) for y in rows)==349
    assert links["slot_spr_rows"]==sum(bool(y["slot_spr_group_indices"]) for y in rows)==322
    blocks=[(y["ordinal"],x) for y in rows for x in y["face_map_number_candidates"]]
    assert len(blocks)==552 and len({x["rd_sha256"] for _,x in blocks})==552
    assert all(x["rd_magic"] and x["rd_dimensions_match"] and 0<=x["offset"]<x["offset"]+x["size"]<=real["bytes"] for _,x in blocks)
    assert [(o,x["adrn_index"],x["rd_size_field"],x["size"]) for o,x in blocks if x["rd_size_field"]!=x["size"]]==[(108,7339,8631844,10000)]
    print("PET124_INDEPENDENT_RECEIPT_PASS 627 positions, 548 strict names, 540 literal labels, 57 blanks, 22 unresolved, 552 RD blocks, 4 multi-candidates, 1 size-field discrepancy; no selector or official fields",flush=True)
if __name__=="__main__":main(sys.argv[1])
