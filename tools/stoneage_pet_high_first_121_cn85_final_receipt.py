"""PET121: independent immutable PET120 receipt and bounded transfer outcome."""
import argparse,hashlib,json,zipfile
from pathlib import Path
from tools import stoneage_pet_high_first_120_cn85_original_resource_preflight as prev
from tools import stoneage_pet_high_first_117_cn85_zip_directory as p
SHA="bcd1edc4294d890d2e15db6fb3d5dc78543798501b05452e742f07c2484abe11"
ZIP="ba38510967a70d08e3c1a894cd4eba1d141e982e006c2c09d33ce9b0c762bd04"
BLOB="99cf97ab2be0759da2a8a599818551d7dc28e3e9"
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--artifact",type=Path,required=True);a=ap.parse_args()
    z=a.artifact.read_bytes();assert len(z)==1029 and hashlib.sha256(z).hexdigest()==ZIP
    with zipfile.ZipFile(a.artifact) as f:
        assert len(f.namelist())==1
        raw=f.read(f.namelist()[0])
    assert raw==prev.REPORT.read_bytes() and hashlib.sha256(raw).hexdigest()==SHA and p.idx.blob(raw)==BLOB
    d=json.loads(raw);assert d["blocker"]=="BOUNDED_FULL_TRANSFER_INCOMPLETE"
    assert d["official_closures"]==0 and not d["original_client_verified"] and not d["pet_payload_extracted"] and not d["original_assets_published"]
    assert not d["zip_members"] and not d["selected_resources"]
    t=d["transfer"];assert t["bytes"]==0 and not t["complete"] and not t["cdx_digest_matches"]
    assert len(t["attempts"])==1
    x=t["attempts"][0];assert x["bytes"]==504365056 and x["status"]==206 and x["content_range"]=="bytes 0-1351371746/1351371747"
    assert x["error_type"]=="TimeoutError" and x["error"]=="overall transfer deadline"
    old=json.loads(prev.prev.REPORT.read_bytes())
    assert len(old["results"])==1 and len(old["results"][0]["directory"]["all_entries"])==759
    assert old["results"][0]["directory"]["parsed_entries"]==759
    print("PET121_FINAL_RECEIPT_OK",BLOB,"TRANSFER_DEADLINE_NOT_SOURCE_ABSENCE",x["bytes"],flush=True)
if __name__=="__main__":main()
