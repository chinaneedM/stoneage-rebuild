"""R97: strict website-catalog identity boundary and original TW1.0 isolation."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research/recovered/STONEAGE-CN-EARLY-PIG-CATALOG-IMAGE-IDENTITY-SOURCE-R97.json"
SHA="d182d35eaf3d803c488fbf697e757deb75ccd193"
PARENT={
"research/recovered/STONEAGE-EARLY-VISUAL-ID-RANGES-INPUT-R1.json":"11bb14ef00c2ed354c5f00f510da8783376f1f28",
"research/recovered/STONEAGE-TW10-VISUAL-CATEGORY-SPR-JOIN-R1.json":"20a82e4d35661785c4e50b44855cf8e8a4e98f3e",
}
NAMES_INDEX=["乌力","乌力乌力","乌力斯坦","乌力布鲁","黑乌力","扑满乌力","乌力 德","乌力固力"]
NAMES_DETAIL=["乌力","乌力乌力","乌力斯坦","乌力布鲁","黑乌力","扑满乌力","乌力莱德","乌力布鲁"]
ELEMENTS=["地8水2","水4火6","地10","火7风3","地5风5","风10","水8火2","地6风4"]
HP=["12-20","29-36","23-27","18-19","33-38","61","46","39"]
THUMBS=[1,2,3,4,5,6,8,7]
ROOT_IMG="https://images.17173cdn.com/stoneage/images/chongwu"

def blob_sha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()

def verify(data):
    raw=P.read_bytes()
    assert blob_sha(raw)==SHA, "R97 source content changed"
    assert data==json.loads(raw.decode("utf-8")), "unattributed changes"
    for name,sha in PARENT.items():
        assert blob_sha((ROOT/name).read_bytes())==sha, "source parent changed: "+name
    assert data["schema"]=="stoneage.cn_17173_undated_pig_catalog_image_links.r97"
    assert data["task"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-97"
    s=data["sources"]
    assert len(s)==4
    assert s[0]["original_publication_date"] is None and s[1]["original_publication_date"] is None
    assert s[0]["exact_client_build"] is None and s[1]["exact_client_build"] is None
    assert all(s[i]["original_html_bytes_sha256"] is None for i in (0,1))
    assert all(s[i]["historical_original_html_authenticated"] is False for i in (2,3))
    assert [x["catalog_no"] for x in data["rows"]]==[f"{i:03}" for i in range(1,9)]
    for n,r in enumerate(data["rows"]):
        assert r["index_name"]==NAMES_INDEX[n]
        assert r["detail_name"]==NAMES_DETAIL[n]
        assert r["reported_elements"]==ELEMENTS[n] and r["reported_birth_hp"]==HP[n]
        assert r["thumbnail_link"]==f"{ROOT_IMG}/images3/a-{THUMBS[n]:03}.gif"
        assert r["image_link"]==f"{ROOT_IMG}/images2/b{n+1:03}.gif"
        assert r["original_tw10_bitmap_id"] is None
        assert r["original_spr_group_id"] is None and r["game_pet_master_id"] is None
    q=data["finite_reconciliation"]
    assert q["unique_detail_names"]==7 and q["collision_detail_name"]=="乌力布鲁"
    assert q["collision_catalog_nos"]==["004","008"]
    assert q["index_detail_name_mismatches"]==["007","008"]
    assert [(x["catalog_no"],x["linked_thumbnail_stem"]) for x in q["thumbnail_filename_reversals"]]==[("007","a-008"),("008","a-007")]
    assert all(q[k] is False for k in ("gallery_row_number_equals_gif_stem_is_reliable","catalog_no_equals_original_bitmap_id","same_catalog_row_proves_two_detail_variants_same_species","early_player_2001_claims_authenticate_catalog_build","early_player_name_resolves_no008_collision"))
    assert q["early_player_2001_jss_prize_claims_for_nos"]==["004","005"]
    p=data["existing_original_tw10_physical_intersection"]
    assert p["old_player_id_ranges_input_blob"]==PARENT["research/recovered/STONEAGE-EARLY-VISUAL-ID-RANGES-INPUT-R1.json"]
    assert p["original_spr_intersection_report_blob"]==PARENT["research/recovered/STONEAGE-TW10-VISUAL-CATEGORY-SPR-JOIN-R1.json"]
    assert p["player_label_pet_portrait_span"]==[7246,7366]
    assert p["number_of_tw10_bitmap_ids_in_span"]==121
    assert p["tw10_spr_frame_references_for_span"]==0
    assert all(p[k] is False for k in ("numeric_overlap_certifies_species_identity","catalog_gif_to_original_ADRN_id_bound","catalog_gif_to_original_SPR_group_bound"))
    ic=data["image_custody"]
    assert ic["eight_thumbnail_urls_resolved_from_html_links"] is True
    assert ic["eight_portrait_urls_resolved_from_html_links"] is True
    assert ic["full_original_gif_bytes_hashed"] is False and ic["original_asset_authenticity_verified"] is False
    assert ic["original_images_committed"] is False
    assert all(data["publication"][k] is False for k in ("source_html_committed","original_game_assets_committed","stage_a_closed","stage_b_started"))
    assert data["publication"]["overall_restoration_percent"] is None
    assert data["publication"]["next"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-98"
    return True

if __name__=="__main__":
    assert verify(json.loads(P.read_text(encoding="utf-8")))
    print("R97 PASS: eight catalog rows, 007/008 cross-page conflict, GIF link reversal; no TW10 species-ID promotion")
