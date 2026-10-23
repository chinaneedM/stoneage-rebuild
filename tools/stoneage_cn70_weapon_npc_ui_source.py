"""R93 bounded 17173 CN7.0 weapon collection + dialogue screenshot contract."""
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-CN70-WEAPON-COLLECTION-NPC-UI-SOURCE-R93.json"
GIT_BLOB_SHA1 = "932547f5258b6ff5aa78cf722c815d29834585ef"

def _git_blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

def verify(data):
    raw = P.read_bytes()
    assert _git_blob_sha(raw) == GIT_BLOB_SHA1, "source JSON changed relative to independently pinned Git blob"
    original = json.loads(raw.decode("utf-8"))
    assert data == original, "modified/missing/surplus source claims"
    assert set(data) == {"schema","task","source","scene","routes","source_text_conflicts","screenshot","evidence_grade","known_unknowns","execution","acceptance"}
    assert data["schema"] == "stoneage.cn70_weapon_collection_npc_ui_guide.r93"
    assert data["task"] == "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-93"
    source = data["source"]
    assert source["url"] == "https://news.17173.com/z/stoneage/renwu/sa70_05.htm"
    assert source["page_version_label"] == "7.0"
    assert source["official_guide"] is False
    assert source["client_build"] is None and source["displayed_publication_date"] is None
    assert source["original_publish_date_authenticated"] is False
    assert source["original_html_bytes"] is None and source["original_html_sha256"] is None
    scene = data["scene"]
    assert scene["guide_reported_npc"] == "史比"
    assert scene["guide_reported_village"] == "玛丽娜丝渔村"
    assert scene["reported_local_coord"] == [66,93]
    assert scene["original_npc_id"] is None and scene["original_map_id"] is None
    assert scene["hidden_conditions_excluded_by_source"] is False
    assert scene["dialogue_verbatim_authenticated"] is False
    near, far = data["routes"]
    assert [a["id"] for a in data["routes"]] == ["near","far"]
    assert len(near["items"]) == len(far["items"]) == 5
    assert near["items"] == ["合成斧8","合成枪8","合成棍棒8","合成爪8","愿藏的斧头"]
    assert far["items"] == ["合成弓箭8","合成投掷斧8","合成回旋标8","合成石8","近藏的棍棒"]
    assert near["reward_name"] == "双尖枪" and near["reward_stats"] == {"attack":53,"agility":-12,"charm":6}
    assert near["reward_magic_text"] == "混迷的精灵" and near["reward_magic_level"] == 4
    assert far["reward_name"] == "乱射弓" and far["reward_stats"] == {"attack":23,"defense":-24,"target_count":10}
    assert far["reward_magic_text"] == "毒雾的精灵" and far["reward_magic_level"] == 4
    for route in data["routes"]:
        assert route["guide_reports_five_items"] is True
        assert route["server_item_consumption_verified"] is False
    assert data["source_text_conflicts"][1]["main_list_name"] == "近藏的棍棒"
    assert data["source_text_conflicts"][1]["footnote_name"] == "进藏的棍棒"
    assert data["source_text_conflicts"][1]["which_is_original_item_name"] is None
    img = data["screenshot"]
    assert img["url"] == "https://images.17173cdn.com/stoneage/images/mission/sa70/sa70_05/sa031027_002.jpg"
    assert img["linked_article_html_img_tag_verified"] is False
    assert img["original_image_bytes_sha256"] is None and img["original_screenshot_capture_date"] is None
    assert img["npc_name_legible_in_screenshot"] is False and img["button_function_executed"] is False
    assert img["image_binary_in_git"] is False and img["filename_is_release_date"] is False
    assert img["screen_layout_native_resolution_verified"] is False
    assert "绿色“下一页”按钮" in img["visually_observed"]
    assert data["evidence_grade"] == "FACT_OF_CURRENT_PORTAL_GUIDE_AND_VISIBLE_IMAGE_NOT_OFFICIAL_CONFIG"
    assert len(data["known_unknowns"]) >= 7
    assert data["execution"] == {
        "original_client_executed": False,
        "original_server_executed": False,
        "network_capture_verified": False,
        "original_item_ids_recovered": False,
        "original_ui_runtime_recovered": False,
        "derived_source_only": True,
    }
    assert data["acceptance"] == {
        "stage_a_closed": False, "stage_b_started": False,
        "wiki_unlocked": False, "original_mainline_npc_ui_recovered": False,
        "overall_restoration_percentage": None,
        "next": "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-94",
    }
    return True

def main():
    data = json.loads(P.read_text(encoding="utf-8"))
    verify(data)
    print("R93 PASS: 2 bounded weapon paths and 1 static dialogue panel; no original game runtime")

if __name__ == "__main__":
    main()
