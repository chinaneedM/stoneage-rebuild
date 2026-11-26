"""Exact 2003 archived GIF payload metadata, no public original pixels."""
import argparse,base64,concurrent.futures,hashlib,io,json,re,urllib.parse,urllib.request
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"research/pets/PET-KR2002-IMAGE-CDX-CI-OBSERVED-R1.json"
def inputs():
    raw=SOURCE.read_bytes(); d=json.loads(raw)
    rows={r["original"]:r for q in d["queries"] for r in q["rows"]}
    assert len(rows)==32 and len(d["matched_paths"])==32 and d["numbered_matched_count"]==18
    assert d["new_official_identities"]==0 and d["original_image_pixels_acquired"] is False
    assert set(urllib.parse.urlsplit(u).path for u in rows)==set(d["matched_paths"])
    assert all(urllib.parse.urlsplit(u).hostname=="stoneage.enium.co.kr" and r["timestamp"].startswith("2003") and r["mimetype"]=="image/gif" and re.fullmatch(r"[A-Z2-7]{32}",r["digest"]) for u,r in rows.items())
    return raw,sorted(rows.values(),key=lambda r:r["original"])
def describe(data):
    if data[:6] not in (b"GIF87a",b"GIF89a"):raise ValueError("GIF magic")
    with Image.open(io.BytesIO(data)) as img:
        if img.format!="GIF" or img.width*img.height>1000000 or img.n_frames>300:raise ValueError("GIF bounds")
        frames=[]
        for n in range(img.n_frames):
            img.seek(n);rgba=img.convert("RGBA")
            frames.append({"rgba_sha256":hashlib.sha256(rgba.tobytes()).hexdigest(),"duration_ms":img.info.get("duration"),"nontransparent_bbox":rgba.getbbox()})
        return {"format":img.format,"width":img.width,"height":img.height,"frame_count":len(frames),"frames":frames,"distinct_rgba_frames":len({f["rgba_sha256"] for f in frames})}
def inspect(r):
    out={"original":r["original"],"timestamp":r["timestamp"],"cdx_digest":r["digest"],"verified":False}
    try:
        u="https://web.archive.org/web/"+r["timestamp"]+"id_/"+r["original"]
        req=urllib.request.Request(u,headers={"User-Agent":"stoneage-rebuild-source-review/1.0","Accept-Encoding":"identity"})
        with urllib.request.urlopen(req,timeout=18) as f:
            final=urllib.parse.unquote(f.geturl()); status=f.status; data=f.read(1024*1024+1)
        out.update(bytes_read=len(data),sha256=hashlib.sha256(data).hexdigest(),actual_cdx_digest=base64.b32encode(hashlib.sha1(data).digest()).decode())
        out["verified"]=bool(status==200 and len(data)<=1024*1024 and final.startswith("https://web.archive.org/web/"+r["timestamp"]+"id_/") and final.split("id_/",1)[1].replace(":80/","/")==r["original"].replace(":80/","/") and out["actual_cdx_digest"]==r["digest"])
        if out["verified"]:out["gif"]=describe(data)
    except Exception as e:out["error_type"]=type(e).__name__
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument("--verify",action="store_true");a=p.parse_args();raw,rows=inputs()
    b=io.BytesIO();Image.new("RGBA",(2,3),(255,0,0,255)).save(b,format="GIF")
    assert describe(b.getvalue())["frame_count"]==1
    if a.verify:print("PET_KR2003_GIF_TARGETS_PASS",len(rows),hashlib.sha256(raw).hexdigest());return
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: results=list(pool.map(inspect,rows))
    valid=[x for x in results if x["verified"] and "gif" in x]
    report={"schema":"stoneage.pet.kr2003_gif_payload.r1","source_sha256":hashlib.sha256(raw).hexdigest(),"results":results,"verified_decoded_gifs":len(valid),"numbered_verified_gifs":sum(bool(re.search(r"/4_\d+\.gif$",x["original"])) for x in valid),"animated_gifs":sum(x["gif"]["frame_count"]>1 for x in valid),"new_official_identities":0,"official_species_count":None,"original_image_pixels_published":False,"private_original_images_retained":False,"native_pet_action_verified":False,"scope":"2003 image captures referenced by 2002 pages, not proof of identical 2002 pixels or native action identity"}
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
