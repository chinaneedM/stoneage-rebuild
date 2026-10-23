"""R94: Japanese 2004 pet-identity cross-media source contract; not original game runtime."""
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-JP2004-PET-AVATAR-MERCH-SOURCE-R94.json"
SOURCE_BLOB_SHA1 = "766ef71c55fd9bc0d7a68e255032ed790163805d"

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()

def verify(data):
    content = P.read_bytes()
    assert git_blob_sha(content) == SOURCE_BLOB_SHA1, "R94 derived source bytes changed"
    assert data == json.loads(content.decode("utf-8")), "R94 source contract changed"
    assert data["schema"] == "stoneage.jp2004_pet_avatar_merch_visual_crosswalk.r94"
    assert data["task"] == "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-94"
    assert len(data["sources"]) == 2
    assert data["sources"][0]["published"] == "2004-03-18 19:22"
    assert data["sources"][1]["published"] == "2004-05-20 19:45"
    assert all(not s["original_html_authenticated"] and s["original_http_sha256"] is None
               and s["exact_game_build"] is None for s in data["sources"])
    s = data["source_claims"]
    assert s["s1_named_pet_avatar_text"] == ["ゴルシス","ウポポ","ミドリガメ"]
    assert (s["s1_pet_avatar_total"],s["s1_background_total"]) == (7,2)
    assert s["s1_per_item_pricing_jpy_range"] == [200,350]
    assert s["s1_available_in_other_hangame_games"] is True
    assert s["s1_availability_is_game_playable_build_evidence"] is False
    assert s["s2_packaged_release_reported_date"] == "2004-05-20"
    assert s["s2_jp_formal_service_announced_date"] == "2004-06-03"
    assert (s["s2_client_cd_rom_count"],s["s2_30_day_pass_count"]) == (2,2)
    assert (s["s2_named_physical_premium"],s["s2_physical_premium_type"],s["s2_physical_premium_count"]) == ("ウポポ","ぬいぐるみストラップ",1)
    assert s["s2_product_may_20_announcement_is_execution_log"] is False
    assert len(data["observations"]) == 4
    assert [x["reported_name"] for x in data["observations"]] == ["ゴルシス","ウポポ","ミドリガメ","ウポポ"]
    for row in data["observations"]:
        assert row["avatar_art_specific_asset_id"] is None
        assert row["in_game_pet_numeric_id"] is None
        assert row["original_sprite_id"] is None
        assert row["species_stat_table_known"] is False
    im = data["illustration"]
    assert im["source_page"] == "R94-S1"
    assert im["url"] == "https://www.itmedia.co.jp/news/article/image/0403/18/1040318075/15463/728"
    assert im["individual_animal_to_reported_name_mapping_verified"] is False
    assert im["original_image_bytes_authenticated"] is False
    assert im["original_image_sha256"] is None
    assert im["original_pet_animation_sprite_verified"] is False
    assert im["native_game_resolution_verified"] is False
    assert im["production_asset_license_granted"] is False and im["artwork_embedded_in_repository"] is False
    rel = data["relation"]
    assert rel["named_entity"] == "ウポポ"
    assert rel["relationship_type"] == "documentary_cross_product_name_match_not_same_build_identity"
    assert rel["same_visual_asset_identical"] is False and rel["same_pet_numeric_id_verified"] is False
    assert all(v is False for v in data["attribution_boundaries"].values())
    assert len(data["unknowns"]) >= 6
    assert data["acceptance"] == {
        "content_ledger_only":True, "new_game_implementation":False, "stage_a_closed":False,
        "stage_b_open":False,"wiki_unlocked":False,
        "overall_restoration_percentage":None,
        "next":"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-95"
    }
    return True

def main():
    data=json.loads(P.read_text(encoding="utf-8"))
    verify(data)
    print("R94 PASS: 3 Japanese pet avatar names + one named 2004 physical premium; original sprites unknown")

if __name__ == "__main__":
    main()
