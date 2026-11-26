"""Source-separated Korean web image evidence, not native pet species rows."""
import collections,hashlib,json,re,urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="research/pets/"
STATIC=P+"PET-KR2002-STATIC-CI-OBSERVED-R1.json"
CDX=P+"PET-KR2002-IMAGE-CDX-CI-OBSERVED-R1.json"
FIRST=P+"PET-KR2003-GIF-PAYLOAD-CI-OBSERVED-R1.json"
RETRY=P+"PET-KR2003-GIF-RETRY-CI-OBSERVED-R1.json"
PIN={STATIC:"618b0d92f6a75ebe83c006b93a093229cdd69260",CDX:"740aa67da47b7e5aadc8c76426243635417fed05",FIRST:"1c0ab623772c91fb1cf66fa44b99be87aec6d717"}
def read(path):
    b=(ROOT/path).read_bytes()
    sha=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    if path in PIN:assert sha==PIN[path],path
    return json.loads(b),sha,hashlib.sha256(b).hexdigest()
def build():
    st,ss,sd=read(STATIC);cd,cs,ch=read(CDX);fi,fs,fh=read(FIRST);rt,rs,rh=read(RETRY)
    assert cd["source_sha256"]==sd and fi["source_sha256"]==ch and rt["prior_receipt_sha256"]==fh
    assert st["exact_replays"]==15 and st["new_official_identities"]==0
    assert cd["target_count"]==159 and cd["numbered_count"]==96
    assert fi["verified_decoded_gifs"]==20 and rt["new_verified_gifs"]==12
    paths=collections.defaultdict(list)
    for n,page in enumerate(st["results"]):
        for j,img in enumerate(page.get("image_occurrences",[])):
            paths[img["path"]].append({"page":page["original"],"page_capture":page["timestamp"],"image_ordinal":img["image_ordinal"],"source_path":STATIC,"source_pointer":["results",n,"image_occurrences",j]})
    meta={}
    for qn,q in enumerate(cd["queries"]):
        for rn,r in enumerate(q["rows"]):
            k=urllib.parse.urlsplit(r["original"]).path
            assert k in paths and k not in meta
            meta[k]=(r,["queries",qn,"rows",rn])
    assert len(meta)==32 and set(meta)==set(cd["matched_paths"])
    initial={urllib.parse.urlsplit(x["original"]).path:(x,n) for n,x in enumerate(fi["results"])}
    retry={urllib.parse.urlsplit(x["original"]).path:(x,n) for n,x in enumerate(rt["results"])}
    assert set(initial)==set(meta)
    assert set(retry)=={k for k,(v,n) in initial.items() if not v["verified"] and v.get("error_type")=="URLError"}
    rows=[]
    for path,refs in sorted(paths.items()):
        row={"path":path,"filename":path.rsplit("/",1)[-1],"numbered_reference":bool(re.search(r"/4_\d+\.gif$",path)),"page_references":refs,"status":"NO_MATCH_IN_BOUNDED_CDX","official_native_pet_id":None,"pet_name":None,"native_action_verified":False,"original_pixels_published":False,"private_original_image_retained":False}
        if path in meta:
            m,mp=meta[path];first,fn=initial[path]
            r,n=retry.get(path,(first,fn));src=RETRY if path in retry else FIRST
            assert r["original"]==m["original"] and r["timestamp"]==m["timestamp"] and r["cdx_digest"]==m["digest"]==r["actual_cdx_digest"]
            assert r["verified"] and "gif" in r and r["timestamp"].startswith("2003")
            row.update(status="EXACT_ARCHIVE_GIF_DECODED",capture=r["timestamp"],bytes_read=r["bytes_read"],sha256=r["sha256"],cdx_digest=r["cdx_digest"],gif=r["gif"],cdx_source={"path":CDX,"pointer":mp},decoded_source={"path":src,"pointer":["results",n]},first_attempt_transport_error=path in retry)
        rows.append(row)
    valid=[x for x in rows if x["status"]=="EXACT_ARCHIVE_GIF_DECODED"]
    assert len(rows)==159 and sum(len(x["page_references"]) for x in rows)==204
    assert len(valid)==32 and sum(x["numbered_reference"] for x in valid)==18
    assert sum(x["gif"]["frame_count"] for x in valid)==54 and sum(x["bytes_read"] for x in valid)==215866
    assert sum(x["gif"]["frame_count"]>1 for x in valid)==3
    assert len({x["sha256"] for x in valid})==32
    summary={"page_image_occurrences":204,"distinct_reference_paths":159,"numbered_references":96,"exact_decoded_gifs":32,"numbered_decoded_gifs":18,"unmatched_reference_paths":127,"static_gifs":29,"animated_gifs":3,"decoded_frames":54,"original_bytes_transiently_read":215866,"initial_transport_errors_resolved":12,"new_official_identities":0,"official_species_count":None,"original_assets_published":False,"private_originals_retained":False,"historical_scope":"2002 page references; 2003 GIF captures; not a native client or roster","source_bounded_archive_query_finished":True,"pet_module_closed":False}
    return {"schema":"stoneage.pet.kr_archive_access.r1","summary":summary,"source_blobs":{STATIC:ss,CDX:cs,FIRST:fs,RETRY:rs},"rows":rows}
def run(args):
    d=build()
    if args.verify:
        print("PET_KR_ARCHIVE_ACCESS_PASS 159 references 32 exact GIFs 54 frames 127 unmatched")
        return
    if args.summary or not args.query:
        print(json.dumps({k:v for k,v in d.items() if k!="rows"},ensure_ascii=False,indent=2));return
    q=args.query.casefold()
    hits=[r for r in d["rows"] if (q in (r["path"].casefold(),r["filename"].casefold()) if args.exact else q in r["path"].casefold())]
    if not args.full:
        hits=[{k:v for k,v in r.items() if k not in ("page_references","gif","cdx_source","decoded_source")} for r in hits]
    print(json.dumps({"query":args.query,"count":len(hits),"official_species_count":None,"results":hits},ensure_ascii=False,indent=2))
