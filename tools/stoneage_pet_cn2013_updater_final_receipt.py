"""Final independent receipt for CN2013 updater path witnesses."""
import argparse,hashlib,json,zipfile
from pathlib import Path
from tools import stoneage_pet_cn2013_updater_path_witnesses as prev
SHA="bd547f14d8d93a8008277278e2e7c3a1660ee8571366647422154bcacdd63011"
ZIP="f146e8c1f62f42952e9b7b5cf25da000c562721c984641e020d7e3127d65deaa"
BLOB="58f204e9df34f29457cc12b1552e8de382357514"
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--artifact",type=Path,required=True);a=ap.parse_args()
    assert a.artifact.stat().st_size==1087 and prev.sha(a.artifact.read_bytes())==ZIP
    with zipfile.ZipFile(a.artifact) as z:
        assert len(z.namelist())==1
        raw=z.read(z.namelist()[0])
    assert raw==prev.REPORT.read_bytes() and prev.sha(raw)==SHA and prev.prev.src.idx.blob(raw)==BLOB
    d=json.loads(raw);assert d["reacquisition"]["identity_matches"] and d["reacquisition"]["response_sha256"]==prev.EXE
    assert len(d["path_literals"])==20
    assert {"SaUpdateNew.exe","_SaUpdateNew.exe","sa_85_free.exe","sa_25_payment.exe","http://update5.cinsgame.com"}<={x["token"] for x in d["path_literals"]}
    assert d["official_closures"]==0 and not d["original_client_verified"] and not d["pet_payload_extracted"] and not d["original_assets_published"]
    print("CN2013_UPDATER_RECEIPT_PASS",BLOB,flush=True)
if __name__=="__main__":main()
