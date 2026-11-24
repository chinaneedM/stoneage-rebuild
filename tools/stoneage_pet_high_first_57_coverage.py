"""PET57: source-pinned residual template material coverage, independent of acquisition."""
from collections import defaultdict,Counter
from pathlib import Path
import argparse,csv,gzip,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research/pets"; R=ROOT/"research/recovered"
TARGET=P/"PET-HIGH-FIRST-57-RESIDUAL-VISUAL-COVERAGE-R1.json"
PINS={
"gaps":(P/"PET-HIGH-FIRST-49-DATED-PC-ACQUISITION-GAP-R1.json","3ae127ef6bee449a472b7b4323b09f930e1c8684"),
"original":(P/"PET-HIGH-FIRST-50-ORIGINAL-ACQUISITION-R1.json","4d0b31a7fa196cf8f227a7b0b1aea7183d9598f0"),
"master":(P/"PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json","fec03646d7c7e4e287f9347c306119cc626d6abf"),
"encounter":(P/"PET-HIGH-FIRST-17-COMPARISON-SKILL-ENCOUNTER-R1.json","63af501ab483770c5c58cb2d62152ab8923dcc2b"),
"grid":(P/"PET-HIGH-FIRST-TW85-ORIGINAL-PE-ALBUM-GRID-R1.json","7fb8eceba23dea6dc90ebb18e404d6e837210eaf"),
"cn50":(P/"PET-HIGH-FIRST-CN50-NATIVE-SPR-ALBUM-R1.json","98fea71c051dfa887b91154a8a72d17c67b57744"),
"retention":(P/"PET-HIGH-FIRST-CN50-TW85-ART-RETENTION-R1.json","afb666ecb451aa1cd43fb8a903403419f6b31cff"),
"roles56":(P/"PET-HIGH-FIRST-56-SOURCE-CUSTODY-R1.json","142976ab261a145eae33a51707701fd041514b3f"),
"roles54":(P/"PET-HIGH-FIRST-54-EGG-ROLE-AND-FUNCTION-ACCEPTED-R1.json","2a45004916ed0f41c37d2c49f48db79127bba289"),
"bridge":(P/"PET-HIGH-FIRST-TW85-NATIVE-SPR-ALBUM-R1.json","e7cff0d53585964c9d755ef1fbd2bc5531d883d6"),
"visual":(P/"PET-HIGH-FIRST-TW85-VISUAL-ACTION-REFERENCES-R1.json","3bcfbba98cfb915b14679ba472dbc554db297018"),
"groups":(R/"tw85-spr137-r28/SPR-GROUP-R28.tsv.gz","f201f85ced4a55d59d38ef774711406c59cddbd4"),
"frames":(R/"tw85-spr137-r28/SPR-FRAME-R28.tsv.gz","831fa633adc5bb1f401ee17fca186d476d146196"),
"material":(R/"tw85-frame-bitmap-r29/GROUP-MATERIAL-R29.tsv.gz","273e0c00ab1e1f7aee40815679b00631cd302231"),
"patch":(R/"wayi-adrn129-patch-metadata/INDEX-1-R1.tsv.gz","065ecc874adc637098dc7c8f177e478bc7b6f054"),
"pairs":(R/"adrn129-tw85-real-pair/PAIRS-R1.tsv.gz","7f41ca49ff576914764b77f22684fbc113e1d90e"),
"native":(R/"adrn129-tw85-real-pair/NATIVE-R1.tsv.gz","ffb7b3340116ecaf57daa08242c1ce271e3ad86f")}
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def gzrows(p):
    with gzip.open(p,"rt",encoding="utf-8",newline="") as f:yield from csv.DictReader(f,delimiter="\t")
def build():
    d={}
    for k,(p,h) in PINS.items():
        raw=p.read_bytes();assert blob(raw)==h,k
        if p.suffix==".json":d[k]=json.loads(raw)
    residual=d["gaps"]["remaining_gap_row_indices"]
    original=d["original"]["projection"]["records"]
    assert len(residual)==67 and [r["tw75_row_index"] for r in original]==residual
    master=d["master"]["pet_flag_1_field_projections"]
    targets={master[i]["graphic"] for i in residual}
    native_bridge={x["tw85_original_spr_number"]:x for x in d["bridge"]["records"]}
    group_rows=list(gzrows(PINS["groups"][0]));mat=list(gzrows(PINS["material"][0]))
    assert len(group_rows)==len(mat)==1739
    bygraphic=defaultdict(list); wanted={}
    for i,(g,m) in enumerate(zip(group_rows,mat)):
        assert int(g["index"])==int(m["group_index"])==i and g["spr_no"]==m["spr_no"]
        spr=int(g["spr_no"])
        if spr not in targets:continue
        r={"group_index":i,"graphic":spr,"segment_sha256":g["segment_sha256"],"animation_headers":int(g["anim_count"]),"source_scope":m["source_scope"]}
        for k in ("frame_occurrences","sentinel_frames","mapped_frames","missing_frames","distinct_bitmap_ids","distinct_mapped_rd_contents"):r[k]=int(m[k])
        assert r["frame_occurrences"]==sum(r[k] for k in ("sentinel_frames","mapped_frames","missing_frames"))
        bygraphic[spr].append(r);wanted[i]=r
    hashes={i:hashlib.sha256() for i in wanted};counts=Counter()
    for f in gzrows(PINS["frames"][0]):
        i=int(f["group_index"])
        if i in wanted:
            hashes[i].update(("\t".join(f[k] for k in ("anim_index","frame_index","bmp_no","pos_x","pos_y","sound_no","sentinel"))+"\n").encode("ascii"))
            counts[i]+=1
    for i,g in wanted.items():
        assert counts[i]==g["frame_occurrences"]
        g["ordered_frame_reference_sha256"]=hashes[i].hexdigest()
    # All exact-name grid rows, and distinct portrait alias namespaces for those rows.
    named={};aliases=set()
    for i in residual:
        row=master[i];matches=[]
        for program,p in d["grid"]["programs"].items():
            for r in p["source_records"]:
                if r["original_name_cp950"]==row["name"]:
                    matches.append({"program":program,**r});aliases.add(r["source_portrait_alias"])
        assert sorted([x["program"],x["slot"]] for x in matches)==sorted(row["tw85_exact_name_album_slots"])
        named[i]=matches
    patch=defaultdict(list)
    for r in gzrows(PINS["patch"][0]):
        alias=int(r["map_number"])
        if alias in aliases:patch[alias].append({"patch_index":int(r["index"]),"patch_record_sha256":r["record_sha256"]})
    patchids={x["patch_index"] for v in patch.values() for x in v}
    pairs={};indices=set()
    for r in gzrows(PINS["pairs"][0]):
        i=int(r["patch_index"])
        if i in patchids:
            assert i not in pairs
            n=[int(x) for x in r["native_exact_indices"].split(",") if x]
            pairs[i]={"bitmapno":int(r["bitmapno"]),"patch_record_sha256":r["patch_record_sha256"],"rd_sha256":r["rd_sha256"],"qualification":r["qualification"],"native_exact_indices":n}
            indices.update(n)
    assert set(pairs)==patchids
    natives={}
    for r in gzrows(PINS["native"][0]):
        i=int(r["index"])
        if i in indices:
            natives[i]={"native_index":i,"bitmapno":int(r["bitmapno"]),"rd_sha256":r["rd_sha256"],"adrn_sha256":r["record_sha256"],"width":int(r["width"]),"height":int(r["height"]),"status":r["rd_status"]}
    assert set(natives)==indices
    portrait={}
    for a in sorted(aliases):
        v=[]
        for p in patch[a]:
            z=pairs[p["patch_index"]];assert p["patch_record_sha256"]==z["patch_record_sha256"]
            n=[natives[i] for i in z["native_exact_indices"]]
            assert all(x["bitmapno"]==z["bitmapno"] and x["rd_sha256"]==z["rd_sha256"] for x in n)
            v.append({**p,**z,"native_candidates":n})
        portrait[str(a)]=v
    comp={x["template_id"]:x for x in d["encounter"]["rows"]}
    roles={x["position"]:x["qualification"] for x in d["roles56"]["rows"]}
    roles.update({x["position"]:x["grade"] for x in d["roles54"]["rows"]})
    rows=[]
    for o in original:
        i=o["tw75_row_index"];m=master[i];spr=m["graphic"];k=m["template_id"]
        assert (o["template_id"],o["graphic"],o["row_sha256"])==(k,spr,m["row_sha256"])
        b=native_bridge.get(spr);native_routes=[]
        if b:
            for p,r in b["program_routes"].items():
                if r["record_source_status"]=="SOURCE_LOCAL_NAMED_ROUTE":
                    native_routes.append({"program":p,"slot":r["local_album_slot"],"name":r["original_name_cp950"],"portrait_alias":r["original_portrait_alias_u32"],"row_sha256":r["original_album_row_sha256"],"exact_name":r["original_name_cp950"]==m["name"]})
        cr=[]
        for c in d["cn50"]["records"]:
            for g in c["spr_groups"]:
                if g["spr_group"]!=spr:continue
                rr=next(r for r in d["retention"]["records"] if r["cn50_album_ordinal"]==c["ordinal"])
                matching=[r for r in rr["routes"] if r["sprite_group"]==spr and r["same_original_spr_sha256"]==g["sha256"]]
                assert matching and all(any(x["group_index"]==r["tw85_index"] and x["segment_sha256"]==g["sha256"] for x in bygraphic[spr]) for r in matching)
                cr.append({"ordinal":c["ordinal"],"name":c["compiled_name"],"source_spr_sha256":g["sha256"],"tw85_retained_indices":[r["tw85_index"] for r in matching],"portrait_alias":c["portrait_alias"],"cn50_portrait_rd_sha256":c["portrait_lookup_rd_sha256"],"tw85_retained_portrait_rd_sha256":rr["tw85_same_physical_portrait_rd_sha256"]})
        c=comp[k];assert c["positive_reference_count"]==0
        rows.append({"position":i,"name":m["name"],"template_id":k,"graphic":spr,"master_row_sha256":m["row_sha256"],"selected_server_match":o["source_pairs"][0]["match"],"selected_instance_ids":[r["instance_id"] for r in o["source_pairs"][0]["instances"]],"later_encounter_positive_refs":c["positive_reference_count"],"tw85_physical_groups":bygraphic[spr],"tw85_native_named_routes":native_routes,"tw85_exact_name_grid_candidates":named[i],"cn50_graphic_bound_routes":cr,"known_role":roles.get(i),"same_deployment_official_identity_verified":False,"official_acquisition_verified":False,"retain_strict_gap":True})
    summary={"template_positions":len(rows),"distinct_graphics":len(targets),"tw85_physical_graphic_positions":sum(bool(r["tw85_physical_groups"]) for r in rows),"tw85_unique_physical_groups":len(wanted),"tw85_exact_name_and_native_graphic_positions":sum(any(x["exact_name"] for x in r["tw85_native_named_routes"]) for r in rows),"tw85_exact_name_grid_positions":sum(bool(r["tw85_exact_name_grid_candidates"]) for r in rows),"cn50_graphic_bound_positions":sum(bool(r["cn50_graphic_bound_routes"]) for r in rows),"positions_with_any_same_number_tw85_frame_mapping":sum(bool(r["tw85_physical_groups"]) and all(x["missing_frames"]==0 for x in r["tw85_physical_groups"]) for r in rows),"distinct_named_grid_portrait_aliases":len(aliases),"aliases_with_exact_native_candidates":sum(any(x["native_candidates"] for x in v) for v in portrait.values()),"positions_with_name_only_portrait_candidates":sum(any(any(x["native_candidates"] for x in portrait[str(v["source_portrait_alias"])]) for v in r["tw85_exact_name_grid_candidates"]) for r in rows),"positions_without_tw85_physical_graphic":[r["position"] for r in rows if not r["tw85_physical_groups"]],"positions_without_exact_name_grid":[r["position"] for r in rows if not r["tw85_exact_name_grid_candidates"]],"later_positive_encounter_positions":0,"strict_gap_count":67,"official_acquisition_closed":0}
    assert (summary["tw85_exact_name_grid_positions"],summary["tw85_exact_name_and_native_graphic_positions"],summary["cn50_graphic_bound_positions"])==(57,34,26)
    assert sum(r["selected_server_match"]=="EXACT_ROW" for r in rows)==64
    return {"schema":"stoneage.pet57.residual_high_version_visual_coverage.r1","source_pins":{k:{"path":str(p.relative_to(ROOT)),"git_blob":h} for k,(p,h) in PINS.items()},"summary":summary,"rows":rows,"portrait_alias_candidates":portrait,"original_asset_payload_published":False,"new_original_client_bytes":0,"runtime_executed":False,"official_species_count":None,"limitations":["source-scoped physical graphic numbers not species IDs","grid name or portrait alias alone does not bind to target graphic","same number different role or name retained","same-carrier frame binding is not pixel rendering or official acquisition"]}
def main():
    a=argparse.ArgumentParser();a.add_argument("--write",action="store_true");args=a.parse_args()
    d=build();raw=(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()
    if args.write:TARGET.write_bytes(raw)
    else:assert TARGET.read_bytes()==raw
    print("PET57",json.dumps(d["summary"],ensure_ascii=False,sort_keys=True))
if __name__=="__main__":main()
