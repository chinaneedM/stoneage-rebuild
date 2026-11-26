"""One bounded retry for the 12 Korean archived GIF transport failures."""
import argparse, concurrent.futures, hashlib, json
from stoneage_pet_kr2003_gif_payload import ROOT,inputs,inspect
RECEIPT=ROOT/"research/pets/PET-KR2003-GIF-PAYLOAD-CI-OBSERVED-R1.json"
def selection():
    raw=RECEIPT.read_bytes()
    prior=json.loads(raw)
    _,rows=inputs()
    byurl={r["original"]:r for r in rows}
    assert len(prior["results"])==32 and prior["verified_decoded_gifs"]==20
    assert prior["new_official_identities"]==0 and prior["original_image_pixels_published"] is False
    failed=[r for r in prior["results"] if r.get("error_type")=="URLError" and not r["verified"]]
    assert len(failed)==12 and len({r["original"] for r in failed})==12
    for r in prior["results"]:
        src=byurl[r["original"]]
        assert r["timestamp"]==src["timestamp"] and r["cdx_digest"]==src["digest"]
    assert len([r for r in prior["results"] if r["verified"] and "gif" in r])==20
    return raw,[byurl[r["original"]] for r in failed]
def main():
    p=argparse.ArgumentParser();p.add_argument("--verify",action="store_true");a=p.parse_args()
    raw,rows=selection();digest=hashlib.sha256(raw).hexdigest()
    if a.verify:print("PET_KR2003_GIF_RETRY_SELECTION_PASS",len(rows),digest);return
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(inspect,rows))
    valid=[r for r in results if r["verified"] and "gif" in r]
    print(json.dumps({"schema":"stoneage.pet.kr2003_gif_retry.r1","prior_receipt_sha256":digest,"retried":len(rows),"results":results,"new_verified_gifs":len(valid),"cumulative_verified_gifs":20+len(valid),"remaining_unverified":12-len(valid),"new_official_identities":0,"official_species_count":None,"original_pixels_published":False,"private_original_images_retained":False,"scope":"One bounded retry of 12 previous transport failures only; no inferred absence or native identity."},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
