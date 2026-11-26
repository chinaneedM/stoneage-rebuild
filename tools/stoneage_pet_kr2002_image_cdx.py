"""Targeted CDX metadata query for previously verified 2002 page image references."""
import argparse, concurrent.futures, hashlib, json, re, urllib.parse
from pathlib import Path
from stoneage_korean_distribution_cdx_prefix_probe import CDX, get, parse_response

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"research/pets/PET-KR2002-STATIC-CI-OBSERVED-R1.json"
HOST="stoneage.enium.co.kr"
PREFIX="/images/game_introduce/pet_caractor/"
def inputs():
    raw=SOURCE.read_bytes(); d=json.loads(raw)
    assert d["exact_replays"]==15 and d["new_official_identities"]==0 and d["original_payloads_published"] is False
    rows=[x for x in d["results"] if x.get("image_occurrences")]
    bypage={x["original"]:sorted({y["path"] for y in x["image_occurrences"]}) for x in rows}
    allpaths=sorted(set().union(*map(set,bypage.values())))
    assert len(allpaths)==159 and all(p.startswith(PREFIX) and re.fullmatch(r"[A-Za-z0-9_.-]+\.gif",p.rsplit("/",1)[-1],re.I) for p in allpaths)
    numbered=[x for x in allpaths if re.fullmatch(r"4_\d+\.gif",x.rsplit("/",1)[-1],re.I)]
    assert len(numbered)==96 and sum(len(x["image_occurrences"]) for x in rows)==204
    samples=sorted({p for paths in bypage.values() for p in (paths[0],paths[-1])})
    assert len(samples)<=18
    return raw,allpaths,numbered,samples
def query(path,mode,targets):
    params={"url":"http://"+HOST+path,"matchType":mode,"from":"2000","to":"2004","output":"json","fl":"timestamp,original,mimetype,statuscode,digest,length","filter":"statuscode:200","limit":"5000"}
    url=CDX+"?"+urllib.parse.urlencode(params)
    out={"path":path,"mode":mode,"status":"UNKNOWN","rows":[]}
    try:
        raw=get(url,timeout=20,attempts=1)
        rows=parse_response(raw)
        # An empty or malformed successful body is not proof of no archive.
        parsed=json.loads(raw)
        if not isinstance(parsed,list):raise ValueError("CDX shape")
        if parsed and parsed[0]!=["timestamp","original","mimetype","statuscode","digest","length"]:raise ValueError("CDX columns")
        matched=[]
        for r in rows:
            u=urllib.parse.urlsplit(r["original"])
            if u.hostname==HOST and not u.query and u.path in targets and r["statuscode"]=="200" and re.fullmatch(r"[A-Z2-7]{32}",r["digest"]):
                if mode=="prefix" or u.path==path:matched.append(r)
        out.update(status="CDX_RESPONSE",raw_sha256=hashlib.sha256(raw).hexdigest(),raw_rows=len(rows),limit_reached=len(rows)>=5000,rows=matched)
    except Exception as e:out.update(status="QUERY_ERROR",error_type=type(e).__name__)
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument("--verify",action="store_true");a=p.parse_args()
    raw,paths,numbered,samples=inputs()
    print("PET_KR2002_IMAGE_SOURCE_PASS",len(paths),len(numbered),hashlib.sha256(raw).hexdigest(),file=__import__("sys").stderr)
    if a.verify:return
    pref=query(PREFIX,"prefix",set(paths))
    found={urllib.parse.urlsplit(r["original"]).path for r in pref["rows"]}
    remaining=[p for p in samples if p not in found]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results=[pref]+list(pool.map(lambda p:query(p,"exact",{p}),remaining))
    matched=sorted({urllib.parse.urlsplit(r["original"]).path for x in results for r in x["rows"]})
    report={"schema":"stoneage.pet.kr2002_image_cdx.r1","source_sha256":hashlib.sha256(raw).hexdigest(),"target_count":len(paths),"numbered_count":len(numbered),"queries":results,"matched_paths":matched,"numbered_matched_count":len(set(matched)&set(numbered)),"unmatched_paths":sorted(set(paths)-set(matched)),"original_image_pixels_acquired":False,"new_official_identities":0,"official_species_count":None,"scope":"2000-2004 prefix and up to 18 exact representative queries; unmatched paths are not absence evidence."}
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
