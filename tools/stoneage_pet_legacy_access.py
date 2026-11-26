"""Expose retained PET16 source namespaces without merging them into official species."""
import json
from collections import Counter
from pathlib import Path
from stoneage_pet_source_lookup import blob

ROOT=Path(__file__).resolve().parents[1]
PATH="research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json"
SHA="fdb7d9aade2df62d1a1e06b2d2f9e383693ed980"
COUNTS={"later2016_templates":1024,"later2016_graphics":598,"mixed25_main":495,"mixed25_alternative":316,"tw10_visual":131,"jp_official_web":124,"cn_official_web":104}
GRADES={"later2016_templates":"COMMUNITY_CONFIGURATION_TECHNICAL_ONLY","later2016_graphics":"CROSS_CARRIER_NUMERIC_INDEX_ONLY","mixed25_main":"PRESERVED_COMMUNITY_MAIN_TABLE","mixed25_alternative":"PRESERVED_COMMUNITY_ALTERNATIVE_NOT_COACTIVE","tw10_visual":"AUTHENTICATED_RETAIL_GRAPHICS_NOT_SPECIES","jp_official_web":"OPERATOR_WEB_CATALOGUE_NOT_LIVE_ISSUANCE","cn_official_web":"OPERATOR_WEB_CATALOGUE_NOT_LIVE_ISSUANCE"}

def load_legacy():
    raw=(ROOT/PATH).read_bytes()
    assert blob(raw)==SHA
    data=json.loads(raw)
    assert data["metrics"]["source_namespace_row_counts_NOT_species"]==COUNTS
    for evidence in data["source_evidence"].values():
        assert blob((ROOT/evidence["path"]).read_bytes())==evidence["git_blob"],evidence["path"]
    assert set(data["datasets"])==set(COUNTS)
    return data

def index(data):
    return [dict(namespace=k,id=r["id"],grade=GRADES[k],pointer=["datasets",k,i],name=r.get("name_as_written"),graphic=r.get("graphic_number"),template=r.get("template_id"),web_ordinal=r.get("web_ordinal"),official_release_certified=False,record=r) for k,rows in data["datasets"].items() for i,r in enumerate(rows)]

def labels(row):
    out=[row["id"]]
    if row["name"] is not None: out.append(row["name"])
    for k in ("graphic","template","web_ordinal"):
        if row[k] is not None: out.append(k+":"+str(row[k]))
    return out

def search(rows,query,source=None,exact=False):
    q=query.casefold()
    return [r for r in rows if (source is None or r["namespace"]==source) and any((q==s.casefold() if exact else q in s.casefold()) for s in labels(r))]

def verify(data,rows):
    assert len(rows)==2792==len({r["id"] for r in rows})
    assert dict(Counter(r["namespace"] for r in rows))==COUNTS
    assert all(not r["official_release_certified"] for r in rows)
    assert all(not r["record"].get(k,False) for r in rows for k in ("official_species_identity","official_tw10_species_identity","native_runtime_verified"))
    assert all(r["record"]["actual_client_species_id"] is None for r in rows if r["namespace"] in ("jp_official_web","cn_official_web"))
    named=Counter(r["namespace"] for r in rows if r["name"])
    assert dict(named)=={"mixed25_main":10,"jp_official_web":124,"cn_official_web":98}
    assert len(search(rows,"ウーリ","jp_official_web",True))>=1
    assert len(search(rows,"web_ordinal:1","cn_official_web",True))==1
    assert search(rows,"web_ordinal:1","cn_official_web",True)[0]["name"] is None
    assert len(search(rows,"COMMUNITY2016:1","later2016_templates",True))==1
    assert len(search(rows,"graphic:100015","tw10_visual",True))==1
    assert not search(rows,"graphic:-999",None,True)
    assert all(data["datasets"][r["pointer"][1]][r["pointer"][2]]==r["record"] for r in rows)
    return dict(schema="stoneage.pet16.legacy_access.r1",source_blob=SHA,namespace_counts=COUNTS,named_counts=dict(named),total_source_rows=2792,unknown_cn_web_names=6,source_evidence_pins=len(data["source_evidence"]),official_species_count=None,official_release_promotions=0,overlap_with_current_lookup="NOT_ADDITIVE_NOT_DEDUPLICATED",module_closed=False)

# Supplemental retained source observations, exact parents only. No native identity upgrade.
R="research/recovered/"
SUPPLEMENTS={
 "jp_sample":("STONEAGE-JP-OFFICIAL-PET-VISUAL-SAMPLE-R1.json","069280bf3fa61be0e08e979672af6864f2b7c616"),
 "jp_r25":("STONEAGE-JP-PET-VISUAL-R25-ACTUAL-SOURCE-R1.json","04b042c63ed2f03982a0c0f1d3b5c829738fa4d1"),
 "jp_observed":("STONEAGE-JP-PET-VISUAL-R25-OBSERVATIONS-R1.json","6fcdb9dd53a7a895882e6facbd0876ce74ff36e7"),
 "jp_custody":("STONEAGE-JP-PET-VISUAL-R25-CUSTODY-R1.json","a2851606a2210e41eafd7f4c467c523ae2bb9de4"),
 "cn_batch":("STONEAGE-CN20-PET-VISUAL-BATCH-SOURCE-R1.json","52fde4b4f0a2dd71b3751258b3d84d989074bbdc"),
 "cn_batch_custody":("STONEAGE-CN20-PET-VISUAL-BATCH-CUSTODY-R1.json","14e8246e56b0074d5ebc54b53c4ba700e8c476b6"),
 "cn_r104":("STONEAGE-CN20-NAMED-PET-VISUAL-SOURCE-R104.json","9001f479efb6abcdf7ac4f28ef7f75c7e6aa344f"),
 "cn_r104_custody":("STONEAGE-CN20-NAMED-PET-VISUAL-CUSTODY-R104.json","8a6d4fe628744694547b9a21ef4b78c8b83d573b"),
 "skill_gaps":("STONEAGE-PET-MODULE-19-MISSING-SKILL-SOURCE-GAP-AUDIT-R1.json","0b014a5d4ccf8da81f7df4c96ba9d8392d3a6231"),
}
def attach_supplements(rows):
    data={}
    for k,(path,sha) in SUPPLEMENTS.items():
        raw=(ROOT/(R+path)).read_bytes()
        assert blob(raw)==sha,path
        data[k]=json.loads(raw)
    by={r["id"]:r for r in rows}
    def link(row,key,pointer,grade,evidence):
        path,sha=SUPPLEMENTS[key]
        row.setdefault("supplemental_evidence",[]).append(dict(source=R+path,git_blob=sha,pointer=pointer,grade=grade,evidence=evidence,official_identity_certified=False,native_runtime_verified=False))
    for i,x in enumerate(data["jp_sample"]["records"]):
        row=by[x["parent_record_id"]]; r=row["record"]
        assert r["name_as_written"]==x["name_as_written"] and r["web_ordinal"]==x["web_ordinal"] and r["image_reference_url"]==x["image"]["original_url"]
        assert x["image"]["pixels_acquired"]
        link(row,"jp_sample",["records",i],"ARCHIVED_WEB_IMAGE_NOT_NATIVE_SPR",x["image"])
    observations=data["jp_observed"]["entries"]
    for i,x in enumerate(data["jp_r25"]["entries"]):
        row=by[x["parent_record_id"]];r=row["record"];o=str(x["web_ordinal"])
        assert r["name_as_written"]==x["name_as_written"] and r["web_ordinal"]==x["web_ordinal"] and r["image_reference_url"]==x["original_url"]
        if x.get("image"):
            seen=observations[o]
            assert seen["decoded_png_sha256"]==x["image"]["decoded_png_sha256"] and seen["rgba_sha256"]==x["image"]["rgba_sha256"] and seen["authenticated_decryption"] and seen["assistant_viewed"]
            link(row,"jp_r25",["entries",i],"ARCHIVED_WEB_IMAGE_NOT_NATIVE_SPR",x["image"])
            link(row,"jp_observed",["entries",o],"PRIOR_PRIVATE_PIXEL_OBSERVATION_NOT_IDENTITY",seen)
        else:
            assert x["status"]=="UNAVAILABLE_OR_UNQUALIFIED_THIS_SINGLE_ATTEMPT" and o not in observations
            link(row,"jp_r25",["entries",i],"UNAVAILABLE_THIS_ATTEMPT_NOT_ABSENCE",{"status":x["status"]})
    for k,cells in (("cn_batch",data["cn_batch"]["extracted"]["selected_cells"]),("cn_r104",data["cn_r104"]["selected_cells"])):
        images={x["ordinal"]:(i,x) for i,x in enumerate(data[k]["images"])}
        assert len(cells)==len(images)
        for cell in cells:
            ordinal=cell["ordinal"];row=by["waei-cn20:new-pet-web-position:"+str(ordinal).zfill(3)]
            r=row["record"]; assert r["name_as_written"]==cell["name_as_written"] and r["web_ordinal"]==ordinal and r["image_reference_url"]==(cell.get("original_url_from_cell") or cell["original_image_url"])
            i,x=images[ordinal]
            link(row,k,["images",i],"ARCHIVED_WEB_IMAGE_NOT_NATIVE_SPR",x)
    for namespace,group in (("later2016_templates","later2016_configured_selected_active"),("mixed25_alternative","mixed25_alternative_paired_not_proven_active")):
        for i,skill in enumerate(data["skill_gaps"]["missing_by_source"][group]):
            for j,x in enumerate(skill["original_references"]):
                row=by[x["source_record_id"]];r=row["record"];n=x["slot_1based"]-1
                assert row["namespace"]==namespace and r["original_row"]==x["original_row"] and r["template_id"]==x["template_id"] and r["graphic_number"]==x["graphic_number"]
                assert skill["skill_id"]==x["skill_id"]
                if namespace=="later2016_templates":
                    assert r["skill_source_slots"][n]==[x["skill_id"],None,None]
                else:
                    assert r["original_skill_slot_ids"][n]==x["skill_id"] and r["original_fields_sha256"]==x["original_fields_sha256"]
                link(row,"skill_gaps",["missing_by_source",group,i,"original_references",j],"MISSING_IN_OWN_SKILL_TABLE_NO_SUBSTITUTION",x)
    counts=Counter((r["namespace"],l["grade"]) for r in rows for l in r.get("supplemental_evidence",[]))
    assert counts=={("jp_official_web","ARCHIVED_WEB_IMAGE_NOT_NATIVE_SPR"):22,("jp_official_web","PRIOR_PRIVATE_PIXEL_OBSERVATION_NOT_IDENTITY"):10,("jp_official_web","UNAVAILABLE_THIS_ATTEMPT_NOT_ABSENCE"):2,("cn_official_web","ARCHIVED_WEB_IMAGE_NOT_NATIVE_SPR"):7,("later2016_templates","MISSING_IN_OWN_SKILL_TABLE_NO_SUBSTITUTION"):102,("mixed25_alternative","MISSING_IN_OWN_SKILL_TABLE_NO_SUBSTITUTION"):12}
    # The original parent contains one already-qualified JP image; the 22 supplements are disjoint.
    jp=[r for r in rows if r["namespace"]=="jp_official_web"]
    assert sum(bool(r["record"]["image_original_bytes_acquired"]) for r in jp)==1
    assert all(not r["record"]["image_original_bytes_acquired"] for r in jp if r.get("supplemental_evidence"))
    assert data["jp_custody"]["encrypted_private_png_count"]==10 and data["jp_custody"]["all_png_decryptions_and_source_rgba_hashes_independently_verified"]
    assert data["cn_batch_custody"]["candidate"]["fully_decoded_images"]==4 and data["cn_r104_custody"]["candidate_main_local_raw_equal"]
    return dict(verified_supplement_files=len(SUPPLEMENTS),jp_web_images_including_parent=23,jp_single_attempt_unavailable=2,cn_web_image_references=7,missing_2016_skill_slots=102,missing_mixed25_alternative_skill_slots=12,official_promotions=0)

def run(args):
    if args.variants: raise SystemExit("--variants is not supported for exact source strings in PET16")
    if args.source and args.source not in COUNTS: raise SystemExit("unknown PET16 namespace")
    data=load_legacy(); rows=index(data); report=verify(data,rows); report["supplements"]=attach_supplements(rows)
    if args.verify:
        print("PET16_LEGACY_ACCESS_PASS "+json.dumps(report,ensure_ascii=False,sort_keys=True))
        return
    if args.summary or not args.query:
        print(json.dumps(report,ensure_ascii=False,indent=2))
        return
    hits=search(rows,args.query,args.source,args.exact)
    if not args.full: hits=[{k:v for k,v in r.items() if k!="record"} for r in hits]
    print(json.dumps(dict(query=args.query,source_occurrences=len(hits),official_species_count=None,source_blob=SHA,results=hits),ensure_ascii=False,indent=2))
