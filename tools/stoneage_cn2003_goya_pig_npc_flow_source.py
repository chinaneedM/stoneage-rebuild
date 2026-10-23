"""Check R91 bounded contemporary quest-guide claims; not a runtime reconstruction."""
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-CN2003-GOYA-PIG-LETTER-NPC-FLOW-SOURCE-R1.json"

def verify(d):
    assert d["task"] == "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-91"
    s = d["source"]
    assert s["url"] == "https://games.sina.com.cn/zhqu/sta/article/2003-05-29/9803.shtml"
    assert (s["displayed_publication"], s["submit_marker"]) == ("2003-05-29 16:24", "网友投稿")
    assert s["named_author"] is None and s["game_build"] is None
    assert s["raw_html_bytes"] is None and s["raw_html_sha256"] is None
    assert s["original_page_bytes_authenticated"] is False
    assert d["evidence_type"] == "FACT_OF_GUIDE_TEXT_NOT_EXECUTED_GAME_SCRIPT"
    assert d["scope"] == "CN_GUIDE_2003_VERSION_UNRESOLVED_NOT_JSS1999_NOT_TW10"
    cf = d["coordinate_frames"]
    assert cf["cave_world_entry_intro"] == [99,425]
    assert cf["cave_world_entry_footer"] == [98,426]
    assert cf["village_world_entrances"] == [[303,599],[301,640]]
    assert cf["village_local_trader"] == [70,97]
    assert cf["entry_coordinates_equivalent_proven"] is False
    assert cf["all_local_coords_are_game_entity_ids"] is False
    assert d["suggested_level_not_gate"] == 20
    f = d["interaction_flow"]
    assert [v["id"] for v in f] == ["N1","N2","N3","N4","N5","N6","N7"]
    assert [v["actor"] for v in f] == ["年轻人","玛丽娜丝商人","年轻人","乌力斯凯","乌力花店","乌力美","乌力斯凯"]
    assert [v["coord"] for v in f] == [[12,14],[70,97],[12,14],[14,11],[44,14],[35,34],[14,11]]
    assert [v["next"] for v in f] == [["N2"],["N3"],["N4"],["N5"],["N6"],["N7"],[]]
    assert all(v["dialogue_verbatim"] is False for v in f)
    assert f[1]["out"] == ["不可思议的贝壳×2（指南叙述）"]
    assert f[2]["out"] == ["宠物：特洛昆 或 呼拔拔（非保证两只）"]
    assert f[4]["out"] == ["月光花"]
    assert f[5]["talk_count_in_guide"] == 2
    assert f[6]["out"] == ["红玉的手环"]
    r = d["guide_rewards"]
    assert r["pet_alternatives"] == ["特洛昆","呼拔拔"]
    assert r["pet_draw_probability"] is None
    assert r["bracelet"] == {"name":"红玉的手环","attack":2,"defense":2,"agility":-2,"charm":1}
    assert r["gifted_shell_count_in_narrative"] == 2
    assert r["shell_final_inventory_count_verified"] is False
    assert r["original_item_ids"] is None and r["original_pet_ids"] is None
    a = d["prior_corroboration"]
    assert a["document"] == "docs/specs/STONEAGE-CN2001-2003-SHELL-QUEST-SOURCE-R1.md"
    assert a["same_game_runtime_verified"] is False and a["independent_source_exact_dialogue_verified"] is False
    ex = d["execution"]
    assert ex["guide_derived_only"] is True
    assert all(ex[k] is False for k in ("original_client_executed","original_server_executed","actual_network_capture","dialogue_ui_screenshot_verified","external_http_raw_replayed"))
    acc = d["acceptance"]
    assert acc["historical_status_promoted"] is False
    assert acc["stage_a_closed"] is False and acc["stage_b_started"] is False
    assert acc["overall_restoration_percentage"] is None
    assert acc["next"] == "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-92"
    assert len(d["unknowns"]) >= 6
    return True

if __name__ == "__main__":
    verify(json.loads(P.read_text(encoding="utf-8")))
    print("R91 bounded NPC guide record PASS; no original runtime inferred")
