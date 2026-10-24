"""Replay early JSS update clauses without treating every 'event' as a campaign."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

from tools.stoneage_jss_pet_faq import ROOT, compact, fingerprint, parse, require
from tools.stoneage_jss_pet_patch_history import change_rows

PAGES = {
    "verup": ("20010417162544", 11239, "ba71d859f34f31261f4293dc61583c53a8e77133898c4a8148c544a452abc3cb"),
    "faqmenu": ("20010417155624", 3356, "d5ea757e563d0bf86ad96b72dc0081761b447fa3771e00a463919b89b7017f5f"),
    "faqquest": ("20010425044210", 1654, "7b2006a9d9bf6297523b13d650b23c070d1901b5976a3eccda2c9a12374b4be8"),
}
REPORT = Path("research/recovered/STONEAGE-JSS-EARLY-QUEST-ORIGINS-R116.json")
NAV = Path("research/recovered/STONEAGE-HISTORICAL-SITE-NAVIGATION-R1.json")
NAV_SHA = "7bec788ca9101aa7a06543c0df2fb15b6bc407fd47141b51cc1a99e216cd61cd"


def source_url(key):
    return f"https://web.archive.org/web/{PAGES[key][0]}id_/" + ROOT + key + ".html"


def clauses(row):
    return [compact(x) for x in row["text"].split("・") if x.strip()]


def update_contract(rows):
    """Select exact clauses: a neighbouring campaign never classifies a quest."""
    def select(day, *tokens):
        found = [(i, row, part) for i, row in enumerate(rows) if row["date"] == day
                 for part in clauses(row) if all(t in part for t in tokens)]
        require(len(found) == 1, "missing/ambiguous dated clause: " + day)
        i, row, part = found[0]
        return {"source_order": i, "date_as_written": row["date_as_written"],
                "operator_written_date": day, "clause_fingerprint": fingerprint(part)}

    treasure = select("2000-04-24", "宝捜し", "ログインとの共同イベント", "開始", "１ヶ月限定イベント")
    sjot_end = select("2000-04-17", "SJOT", "ログインとの共同イベント", "終了")
    sjot_fix = select("2000-04-10", "SJOT関連", "NPCの設定", "修正")
    rebirth = select("2000-08-28", "イベント（転生）を追加")
    genkou = select("2000-04-24", "玄黄の洞窟", "イベント進行を修正")
    uriuri = select("1999-10-18", "ウリウリイベント", "貝殻を2つとる不具合", "修正")
    quiz_speech = select("2000-05-08", "NPCのセリフ", "クイズ道場", "修正")
    quiz_access = select("2000-05-29", "クイズ道場の奥に進めるようになりました")
    # These distinct clauses demonstrate why update-row-wide classification fails.
    esthe = select("2000-08-28", "エステ体験版キャンペーン", "開始")
    chatroom = select("1999-11-01", "期間限定", "チャットルームを追加")
    maps = select("1999-11-01", "マップを追加")
    unnamed = [{"source_order": i, "operator_written_date": r["date"],
                "date_as_written": r["date_as_written"], "clause_fingerprint": fingerprint(c)}
               for i, r in enumerate(rows) for c in clauses(r)
               if "イベント" in c and "追加" in c and "転生" not in c]
    require(len(unnamed) == 13, "unnamed event-addition source coverage changed")

    def record(key, label, kind, origin, refs, claim):
        return {"archive_id": key, "source_label": label, "record_kind": kind,
                "origin_class": origin, "region": "JP", "operator_source": "JSS_TITAN_OFFICIAL_ARCHIVE",
                "version": "JSS_1999_2000_OPERATOR_HISTORY_CAPTURED_2001_EXACT_BUILD_UNKNOWN",
                "source_clauses": refs, "bounded_claim": claim,
                "native_quest_id": None, "native_npc_id": None, "first_introduced_date": None,
                "document_publication_date": None, "recurrence_or_rerun": None,
                "post_event_retention": None, "native_reward_ids": None,
                "permanence_proven": False, "baseline_core_admission": False,
                "server_execution_verified": False}

    records = [
        record("JSS-TREASURE-20000424", "宝捜し", "EVENT_ACTIVITY_CLAIM", "OPERATOR_EVENT_QUEST", [treasure],
               "OPERATOR_REPORTS_START_OF_ONE_MONTH_JOINT_LOGIN_EVENT_NOT_QUEST_FLOW"),
        record("JSS-SJOT-200004", "SJOT", "EVENT_ACTIVITY_CLAIM", "OPERATOR_EVENT_QUEST", [sjot_fix, sjot_end],
               "JOINT_LOGIN_EVENT_HAS_NPC_SETTING_FIX_THEN_REPORTED_END_NOT_A_COMPLETE_QUEST"),
        record("JSS-REBIRTH-20000828", "転生", "QUEST_OR_SYSTEM_ADDITION_CLAIM", "ORIGIN_UNRESOLVED", [rebirth],
               "NAMED_GAMEPLAY_ADDITION_WITH_NO_DURATION_OR_PERMANENT_QUEST_PROOF"),
        record("JSS-GENKOU-20000424", "玄黄の洞窟", "QUEST_OR_EVENT_BUGFIX_CLAIM", "ORIGIN_UNRESOLVED", [genkou],
               "PROGRESSION_FIX_AT_NAMED_CAVE_NOT_LAUNCH_OR_PERMANENCE_PROOF"),
        record("JSS-URIURI-19991018", "ウリウリイベント", "QUEST_OR_EVENT_BUGFIX_CLAIM", "ORIGIN_UNRESOLVED", [uriuri],
               "SHELL_DUPLICATION_BUG_FIX_NOT_INTENDED_SHELL_COUNT_OR_QUEST_FLOW"),
        record("JSS-QUIZ-DOJO-200005", "クイズ道場", "VENUE_DIALOGUE_AND_ACCESS_CHANGE_CLAIM", "ORIGIN_UNRESOLVED", [quiz_speech, quiz_access],
               "NPC_DIALOGUE_FIX_AT_VENUE_THEN_INTERIOR_ACCESS_NOT_QUEST_COMPLETION_OR_NPC_IDENTITY"),
    ]
    records[0]["reported_window"] = {"start_date_as_written": "2000-04-24", "duration_as_written": "１ヶ月",
                                      "exact_end_date": None, "actual_runtime_window": None}
    records[1]["reported_window"] = {"start_date_as_written": None, "end_date_as_written": "2000-04-17",
                                      "actual_runtime_window": None}
    return {"records": records, "unnamed_addition_clauses": unnamed,
            "unnamed_clauses_are_not_13_distinct_quests": True,
            "context_separations": {
                "rebirth_and_esthe_are_distinct_same_day_clauses": {"gameplay": rebirth, "campaign": esthe,
                    "campaign_duration_transferred_to_rebirth": False},
                "limited_chatroom_and_map_addition_are_distinct_clauses": {"chatroom": chatroom, "map": maps,
                    "limited_duration_transferred_to_maps_or_unnamed_event": False}},
            "material_views": {
                "game_base_quests": [], "version_permanent_quests": [],
                "operator_event_quests_and_activities": [r["archive_id"] for r in records if r["origin_class"] == "OPERATOR_EVENT_QUEST"],
                "unresolved_origin": [r["archive_id"] for r in records if r["origin_class"] == "ORIGIN_UNRESOLVED"]}}


def faq_contract(menu, detail):
    m, d = parse(menu), parse(detail)
    require(ROOT + "faqquest.html" in m.links, "no real menu-to-detail link")
    require("よくいただくご質問" in d.text, "unexpected FAQ category")
    parts = re.split(r"Q:", d.text)[1:]
    require(len(parts) == 3, "commented trial question must not become an active answer")
    pairs = []
    for part in parts:
        require(part.count("A:") == 1, "malformed FAQ question/answer")
        pairs.append(tuple(compact(x) for x in part.split("A:")))
    require("Windows2000" in pairs[0][0] and "RC2" in pairs[0][1] and "保証するものではございません" in pairs[0][1],
            "RC2 observation must retain retail-Windows non-guarantee")
    require("画面キャプチャ" in pairs[1][0] and "[F12]" in pairs[1][1] and "screenshotフォルダ" in pairs[1][1],
            "screenshot key/path changed")
    require("ホームページ" in pairs[2][0] and "日本システムサプライの著作物" in pairs[2][1]
            and "無断転載、再利用を禁止" in pairs[2][1], "screenshot attribution/reuse qualifications changed")
    require(not any(t in d.text for t in ("体験版のデータ", "IDが完全に異なります")), "inactive comment leaked into visible FAQ")
    return {"active_question_count": 3, "commented_question_count": len(re.findall(r"<!--(?:(?!-->).)*Q:", detail, flags=re.S)),
            "question_answer_fingerprints": [{"question": fingerprint(q), "answer": fingerprint(a)} for q, a in pairs],
            "quest_definition_recovered": False, "filename_proves_quest_topic": False,
            "screenshot_description": {"key": "F12", "subdirectory": "stoneage/screenshot",
                "evidence": "OFFICIAL_FAQ_DESCRIPTION_NOT_EXECUTED_CLIENT_TRACE", "image_format": None},
            "copyright_notice_is_blanket_asset_license": False,
            "inactive_trial_data_answer_is_current_operator_policy": False,
            "windows2000_retail_compatibility_guaranteed": False}


def build(acquisitions, navigation_raw):
    require(hashlib.sha256(navigation_raw).hexdigest() == NAV_SHA, "navigation dependency changed")
    nav = json.loads(navigation_raw)["targets"]["jss_top"]
    require(all(any(x["target_url"] == ROOT + k + ".html" for x in nav["links"])
                for k in ("verup", "faqmenu")), "no authenticated top navigation")
    texts, sources = {}, {}
    for key, (capture, size, digest) in PAGES.items():
        raw, final = acquisitions[key]
        require(final == source_url(key), "unexpected actual source URL/capture: " + key)
        require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, "source bytes changed: " + key)
        texts[key] = raw.decode("shift_jis", errors="strict")
        sources[key] = {"original_url": ROOT + key + ".html", "actual_capture": capture,
                        "final_url": final, "bytes": size, "sha256": digest, "codec": "shift_jis",
                        "document_publication_date": None,
                        "newly_acquired_page_this_package": key == "faqquest"}
    rows = change_rows(texts["verup"])
    require(len(rows) == 40 and rows[0]["date"] == "2000-09-11" and rows[-1]["date"] == "1999-10-18", "dated coverage changed")
    return {"schema": "stoneage.jss.early_quest_origins.r116", "date": "2026-10-24",
            "source_pages": sources, "dependency": {"path": str(NAV), "sha256": NAV_SHA},
            "update_evidence": update_contract(rows), "faq_evidence": faq_contract(texts["faqmenu"], texts["faqquest"]),
            "boundaries": {"capture_dates_are_not_deployment_dates": True,
                "operator_written_updates_are_not_independently_observed_deployments": True,
                "japanese_event_word_alone_proves_operator_campaign": False,
                "all_update_rows_semantically_restored": False, "first_party_quest_scripts_recovered": False,
                "native_ids_or_reward_tables_recovered": False, "source_labels_are_new_original_entities": False,
                "cross_region_same_names_or_later_pet_species_equivalence_proven": False,
                "jss1999_launch_or_tw10_same_build_proven": False,
                "proprietary_html_images_or_binaries_retained_in_git": False,
                "stage_a": "7_PARTIAL_2_OPEN", "stage_b_wiki": "GATED", "savedata_r79": "PAUSED_NON_BLOCKING",
                "overall_restoration_percentage": None}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    acquisitions = {}
    for key in PAGES:
        if args.input_dir:
            acquisitions[key] = ((args.input_dir / (key + ".html")).read_bytes(), source_url(key))
        else:
            with urlopen(Request(source_url(key), headers={"User-Agent": "StoneAge-Historical-Research/1.0"}), timeout=45) as response:
                acquisitions[key] = (response.read(), response.url)
    report = build(acquisitions, NAV.read_bytes())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("R116 exact source replay: 2 operator activities, 4 unresolved labels; no base/permanent quest admission")


if __name__ == "__main__":
    main()
