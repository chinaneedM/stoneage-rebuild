"""Independent final PET113 archive receipt and strict source boundary verification."""
import argparse,json,zipfile
from pathlib import Path
from tools import stoneage_pet_high_first_104_cn70_archive_index as idx
P=idx.ROOT/"research/pets"
R=P/"PET-HIGH-FIRST-113-CN75-TORRENT-IDENTITY-REVIEW-R1.json"
def main():
    p=argparse.ArgumentParser();p.add_argument("--artifact",type=Path,required=True);a=p.parse_args()
    z=a.artifact.read_bytes();assert len(z)==1518 and idx.sha(z)=="55feba776995bb1bfd593c78abb281436a7bba629bd40c8c087fe7dcda99acd3"
    with zipfile.ZipFile(a.artifact) as f:
        assert f.namelist()==["pet113.json"];raw=f.read("pet113.json")
    assert raw==R.read_bytes() and idx.sha(raw)=="7d1692c682dfce1f4d8733705d7aa864a0b87199ff81053117e1026f3906027a"
    d=json.loads(raw)
    assert idx.blob((P/"PET-HIGH-FIRST-112-CN75-TORRENT-PREFLIGHT-R1.json").read_bytes())==d["prior_report_git_blob"]=="a5dc9d2bdae37f36b3c4900d701f9cbe9c8bae1c"
    rows=d["results"];assert len(rows)==2
    assert all(x["result"]=="EXACT_REPLAY_VERIFIED" and x["cdx_digest_matches"] and x["bencode_valid"] and x["metadata_consistent"] for x in rows)
    assert [x["metadata"]["name"] for x in rows]==["StoneAge75.rar","stoneage7.5.rar"]
    assert [x["metadata"]["declared_total_bytes"] for x in rows]==[770632364,779056544]
    assert [x["metadata"]["piece_count"] for x in rows]==[1470,1486]
    assert all(x["metadata"]["piece_length"]==524288 and x["metadata"]["declared_lengths_not_original_payload_verified"] for x in rows)
    assert len({x["metadata"]["piece_hashes_sha256"] for x in rows})==2
    assert len({x["metadata"]["info_bencode_sha256"] for x in rows})==2
    assert rows[0]["expected_single_rar"] and not rows[1]["expected_single_rar"]
    assert rows[1]["failure_stage"]=="EXPECTED_SINGLE_RAR_IDENTITY"
    assert not d["original_client_verified"] and not d["original_assets_published"] and not d["peer_or_tracker_contacted"] and d["official_closures"]==0
    print("PET113_FINAL_RECEIPT_OK "+idx.blob(raw))
if __name__=="__main__":main()
