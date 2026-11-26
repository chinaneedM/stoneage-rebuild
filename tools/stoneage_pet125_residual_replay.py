"""Independent exact-blob replay of PET125 and bounded residual classification."""
import hashlib,json,struct,subprocess
from pathlib import Path
P=Path("research/pets")
sources={
"pet124":("PET-HIGH-FIRST-124-CN85-NATIVE-ALBUM-R1.json","17a42f4de1d9e508b580c88de70bb012d7e03c9b"),
"pet122":("PET-HIGH-FIRST-122-CN85-COMPLETE-TRANSFER-R1.json","a6ed895e5b6b18ebaa1c02e809da5a17937dd176"),
"tw85":("PET-HIGH-FIRST-TW85-ORIGINAL-PE-ALBUM-GRID-R1.json","7fb8eceba23dea6dc90ebb18e404d6e837210eaf"),
"cn50":("PET-HIGH-FIRST-CN50-NATIVE-SPR-ALBUM-R1.json","98fea71c051dfa887b91154a8a72d17c67b57744"),
}
def load(name,expected):
    raw=(P/name).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==expected,name
    return json.loads(raw)
a,c,t,n=(load(*v) for v in sources.values())
d=load("PET-HIGH-FIRST-125-CN85-RESIDUAL-CROSSCHECK-R1.json","49ec91be55b8466db9b6d05a1f55ee4ebc71f853")
assert d["input_git_blobs"]=={k:v[1] for k,v in sources.items()}
assert not any(d["limits"].values())
assert subprocess.check_output(["git","rev-parse","HEAD:docs/CURRENT-STATE.md"],text=True).strip()=="c89e0e33537990aa2132b47c40fef49a985a935c"
p,q=a["analysis"]["programs"]
assert p["table_sha256"]==q["table_sha256"]
u=[x for x in p["entries"] if not x["strict_old_parser"]]
assert len(u)==22
rows=[]
for x in u:
    i,s,f=x["ordinal"],x["slot"],x["face"]
    assert x==q["entries"][i] and not x.get("compiled_label") and x["nul_terminated"] and not x["nonzero_padding_bytes"]
    # Test exactly one structural hypothesis: all 20 name bytes are zero.
    assert hashlib.sha256(struct.pack("<i20sI",s,b"",f)).hexdigest()==x["source_record_sha256"]
    matches=[]
    for program,v in t["programs"].items():
        for y in v["source_records"]:
            if (y["original_first_i32"],y["source_portrait_alias"])==(s,f):
                matches.append(dict(program=program,name=y["original_name_cp950"],exact_row=y["original_row_sha256"]==x["source_record_sha256"]))
        for y in v["blank_or_unqualified"]:
            if (y["original_first_i32_or_minus_one"],y["source_trailing_u32"])==(s,f):
                matches.append(dict(program=program,name=None,exact_row=y["original_row_sha256"]==x["source_record_sha256"]))
    groups=[]
    for y in c["analysis"]["spr"]["group_rows"]:
        number=int(y["spr_no"])
        if number not in (100250+i,100250+s):continue
        sha=y["segment_sha256"]
        matches50=[z["ordinal"] for z in n["records"] for g in z["spr_groups"] if (g["spr_group"],g["sha256"])==(number,sha)]
        groups.append(dict(number=number,index=int(y["index"]),sha=sha,cn50_exact=matches50))
    rows.append(dict(ordinal=i,slot=s,face=f,row_sha256=x["source_record_sha256"],tw85_matches=matches,spr_candidates=groups))
assert rows==d["rows"]
assert sum(any(m["exact_row"] for m in x["tw85_matches"]) for x in rows)==9
assert not any(m["name"] for x in rows for m in x["tw85_matches"])
assert sum(len(x["spr_candidates"]) for x in rows)==44
assert sum(bool(g["cn50_exact"]) for x in rows for g in x["spr_candidates"])==35
rd=[]
for x in a["analysis"]["resource_links"]["rows"]:
    candidates=x["face_map_number_candidates"]
    if len(candidates)==1 and all(y["rd_size_field"]==y["size"] for y in candidates):continue
    old=[z for z in n["records"] if (z["ordinal"],z["compiled_name"],z["portrait_alias"])==(x["ordinal"],x["compiled_label"],x["face"])]
    assert len(old)==1
    old=old[0]
    exact=[y for y in candidates if y["rd_sha256"]==old["portrait_lookup_rd_sha256"] and y["bitmapno"]==old["portrait_lookup_after_ordered_load"]]
    assert len(exact)==1
    y=exact[0]
    rd.append(dict(ordinal=x["ordinal"],label=x["compiled_label"],face=x["face"],cn85_candidate_count=len(candidates),cn50_ordered_lookup_bitmap=y["bitmapno"],cn50_exact_rd_sha256=y["rd_sha256"],adrn_size=y["size"],rd_header_size=y["rd_size_field"],cn85_native_selector_proven=False))
assert [x["ordinal"] for x in rd]==[108,139,140,141,142]
assert [x["cn85_candidate_count"] for x in rd]==[1,2,2,2,2]
assert rd[0]["adrn_size"]==10000 and rd[0]["rd_header_size"]==8631844
assert all(x["adrn_size"]==x["rd_header_size"] for x in rd[1:])
print("PET125 independent replay PASS: 22/22 all-zero name fields; 9 TW85 exact unqualified; 44 SPR candidates, 35 CN50 exact; 5/5 exact CN50 RD references; native selector and official closures 0.")
print(json.dumps(rd,ensure_ascii=False,sort_keys=True))
