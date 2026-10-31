"""O14: validate public, source-separated SOT C/D reader-guide evidence only."""
import json
from pathlib import Path

REPORT = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-O14-SOT-CD-2003-PLAYER-SOURCE-R1.json"

def validate(data):
    if data["schema"] != "stoneage.o14.sot_cd_2003_reader_submission_route_material.r1":
        raise ValueError("wrong schema")
    if data["evidence_class"] != "PLAYER_GUIDE_VISIBLE_2003_NOT_ORIGINAL_GAME_RUNTIME":
        raise ValueError("source scope promoted")
    if data["remote_baseline"]["preserved_current_state_bytes"] != 2708031:
        raise ValueError("historical source prefix not retained")
    src = data["sources"]
    for letter, filename in (("C", "rwgl1_12.shtml"), ("D", "rwgl1_13.shtml")):
        s = src[letter]
        if not s["url"].endswith("/" + filename) or s["byline"] != "网友投稿":
            raise ValueError("source misattribution")
        if s["raw_http_bytes_acquired"] or s["raw_source_sha256"] is not None:
            raise ValueError("unverified raw source claim")
    if src["index"]["original_server_build_verified"]:
        raise ValueError("catalog label is not client build")
    b = data["route_choice"]
    if (b["C"], b["D"], b["required_level_from_code"], b["recommended_level"]) != ("completed", "not_completed", None, 60):
        raise ValueError("C/D route prerequisite mismatch")
    cls = data["source_task_classification"]
    if (not cls["source_uses_word_activity"] or not cls["reader_submission_claims_repeatable"] or cls["limited_time_event_verified"] or cls["repeatability_is_native_verified"] or cls["actual_item_id"] is not None):
        raise ValueError("activity/event/classification claim promoted")
    expected_answers = {
       "C":["贝洛洛克","喝酒","42","特级柯尔克石","为了健康而推荐的温青菜","半年前","ＢＡＲ　Ｓｉｌｋｙ　ＣＬＵＢ","头盔","携带方便的三明治","鲍尔","哥亚山","83岁"],
       "D":["千穗","ＢＡＲ　Ｓｉｌｋｙ　ＣＬＵＢ","岩石炖肉","西扎卡","妮尔","17","强恩一族","达克尔","查罕吉鲁兄弟","邦洛洛克斯","携带方便的三明治","83岁"]
    }
    rows = data["checkpoints"]
    if set(rows) != {"C", "D"}:
        raise ValueError("missing route")
    for letter in ("C","D"):
        rr = rows[letter]
        if len(rr) != 12:
            raise ValueError("not twelve checkpoints")
        if [r["sequence"] for r in rr] != list(range(1,13)):
            raise ValueError("source order lost")
        if [r["checkpoint"] for r in rr] != [f"{letter}-{i}" for i in range(1,13)]:
            raise ValueError("checkpoint ids")
        if [r["player_guide_answer"] for r in rr] != expected_answers[letter]:
            raise ValueError("guide question-answer changed")
        for row in rr:
            point = row["local_coordinate"]
            if (not isinstance(point["east"],int) or not isinstance(point["south"],int)
                or not 0 <= point["east"] <= 1000 or not 0 <= point["south"] <= 1100
                or row["historical_map_floor_id"] is not None
                or row["original_npc_script_id"] is not None
                or row["source_line_range"][0] > row["source_line_range"][1]):
                raise ValueError("unsupported original map or event")
    if rows["C"][2]["floor_or_scope"] == rows["D"][7]["floor_or_scope"]:
        raise ValueError("identical local coordinates cannot imply same floor")
    reward = data["completion"]
    if len(reward["pet_rewards_guide_C"]) != 4 or len(reward["pet_rewards_guide_D"]) != 4:
        raise ValueError("lost route-specific candidate rewards")
    if reward["reward_probability"] is not None or reward["gameplay_transaction_verified"]:
        raise ValueError("reward transaction fabricated")
    if not all(data["unknowns"].values()):
        raise ValueError("unresolved historical source fabricated")
    g = data["status_gates"]
    if (g["stage_A_partial"],g["stage_A_open"],g["stage_B_gated"],g["wiki_gated"],g["R79_paused_nonblocking"],g["overall_percent"],g["new_game_development_started"]) != (7,2,True,True,True,None,False):
        raise ValueError("gates changed without evidence")
    return {"routes":2,"checkpoints":24,"unique_checkpoint_ids":24,"source_grade":"2003_reader_submission_not_original_server","historical_game_runtime_observed":False}

def main():
    result=validate(json.loads(REPORT.read_text(encoding="utf-8")))
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))

if __name__ == "__main__":
    main()
