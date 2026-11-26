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

def run(args):
    if args.variants: raise SystemExit("--variants is not supported for exact source strings in PET16")
    if args.source and args.source not in COUNTS: raise SystemExit("unknown PET16 namespace")
    data=load_legacy(); rows=index(data); report=verify(data,rows)
    if args.verify:
        print("PET16_LEGACY_ACCESS_PASS "+json.dumps(report,ensure_ascii=False,sort_keys=True))
        return
    if args.summary or not args.query:
        print(json.dumps(report,ensure_ascii=False,indent=2))
        return
    hits=search(rows,args.query,args.source,args.exact)
    if not args.full: hits=[{k:v for k,v in r.items() if k!="record"} for r in hits]
    print(json.dumps(dict(query=args.query,source_occurrences=len(hits),official_species_count=None,source_blob=SHA,results=hits),ensure_ascii=False,indent=2))
