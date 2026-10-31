"""O15: refuse silent promotion of 2021 SOT repost to earlier original game."""
import json
from pathlib import Path

REPORT = Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-O15-SOT-CD-SOURCE-VARIANTS-R1.json"

def validate(d):
    if d["schema"]!="stoneage.o15.sot_cd_web_source_variant_comparison.r1":
        raise ValueError("schema")
    if d["status"]!="VERSION_UNVERIFIED_SOURCE_DISAGREEMENT_DO_NOT_OVERWRITE_EARLIER":
        raise ValueError("source precedence")
    old=d["earlier_source"]; new=d["later_source"]
    if not old["o14_git_blob"] or old["original_html_or_game_script_acquired"] or new["html_bytes_or_raw_sha_acquired"]:
        raise ValueError("source qualification")
    for part in ("C","D"):
        if not old["sina_"+part].endswith("rwgl1_"+("12" if part=="C" else "13")+".shtml"):
            raise ValueError("earlier source mismatch")
        if not new[part]["url"].endswith("shiqi"+("3444" if part=="C" else "3445")+".html"):
            raise ValueError("later source mismatch")
    rows=d["all_checkpoints"]
    if len(rows)!=24 or {(q["route"],q["step"]) for q in rows}!={(r,i) for r in ("C","D") for i in range(1,13)}:
        raise ValueError("not a full ordered two-route diff")
    got=sum(q["coordinate_differs"] for q in rows)
    got_ans=sum(q["answer_text_differs"] for q in rows)
    if (got,got_ans)!=(d["survey"]["coordinate_disagreements"],d["survey"]["answer_text_disagreements"]):
        raise ValueError("reported discrepancy totals drift")
    for route in ("C","D"):
        subset=[q for q in rows if q["route"]==route]
        if sum(q["coordinate_differs"] for q in subset)!=d["survey"]["by_route"][route]["coordinate_disagreements"]:
            raise ValueError("route coordinate total drift")
        if sum(q["answer_text_differs"] for q in subset)!=d["survey"]["by_route"][route]["answer_text_disagreements"]:
            raise ValueError("route answer total drift")
        for q in subset:
            if (q["earlier_coordinate"]!=q["later_coordinate"])!=q["coordinate_differs"]:
                raise ValueError("coordinate mismatch")
            if (q["earlier_guide_answer"]!=q["later_repost_answer"])!=q["answer_text_differs"]:
                raise ValueError("answer mutation mismatch")
    if rows[2]["later_coordinate"]!=[33,57] or rows[2]["earlier_coordinate"]!=[27,42]:
        raise ValueError("material C-3 discrepancy lost")
    entry=d["entry_and_exit_variants"]
    if (entry["earlier_C_completion"],entry["later_C_completion"])!=("萨姆吉尔村","卡鲁它那村"):
        raise ValueError("C terminal location conflict erased")
    if entry["earlier_C_gate"]==entry["later_C_gate"] or entry["earlier_D_gate"]==entry["later_D_gate"]:
        raise ValueError("eligibility conflict erased")
    g=d["historical_limits"]
    if not all(v is True for k,v in g.items() if k!="overall_percent") or g["overall_percent"] is not None:
        raise ValueError("unsupported official/production promotion")
    return {"source_variant_count":2,"matched_checkpoints":len(rows),"coordinate_disagreements":got,"answer_text_disagreements":got_ans,"original_build_proven":False}

def main():
    print(json.dumps(validate(json.loads(REPORT.read_text(encoding="utf-8"))),ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
