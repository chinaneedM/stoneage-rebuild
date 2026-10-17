"""Acquire six bounded adult-ceremony sources; retain derived metadata only.

Profiles describe what each publication reports, never original server execution.
No source text, invented item IDs, or merged reward defaults enter the report.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import urllib.request

try:
    from tools.stoneage_early_content_probe import plain, require
except ModuleNotFoundError:
    from stoneage_early_content_probe import plain, require

SOURCES = {
    "compilation": ("https://games.sina.com.cn/handbook/0101/01186091_c1.shtml", "gb18030"),
    "duplicate": ("https://news.17173.com/z/stoneage/renwu/n10.htm", "utf-8"),
    "levelguide": ("https://news.17173.com/z/stoneage/content/2001-6-14/n654_570366.html", "utf-8"),
    "caves": ("https://news.17173.com/z/stoneage/content/2001-6-14/n730_646156.html", "utf-8"),
    "later_adult": ("https://games.sina.com.cn/zhqu/sta/rwgl1_5.shtml", "gb18030"),
    "archived_compilation": ("https://web.archive.org/web/20011120063019id_/http://games.sina.com.cn:80/handbook/0101/01186091_c1.shtml", "gb18030"),
}


def between(text, start, end):
    begin = text.find(start)
    require(begin >= 0, f"missing start: {start}")
    finish = text.find(end, begin + len(start))
    require(finish > begin, f"missing ordered end: {end}")
    result = text[begin:finish]
    require("\ufffd" not in result, "selected evidence has decoding damage")
    return result


def contains(text, *tokens):
    require(all(token in text for token in tokens), "missing selected business claim")


def normalize(text):
    return re.sub(r"\s+", "", text)


def same_task_block(first, second, label):
    require(normalize(first) == normalize(second), f"task block changed; requalify {label}")


def news_header(document, author):
    """Read the publication's own date/byline cells, never related stories."""
    for field, token in (("newsriqi", "2001-06-14"), ("zhuozhe_left", "作者：" + author)):
        match = re.search(r'<div\s+id=["\x27]' + field + r'["\x27][^>]*>(.*?)</div>', document, re.I | re.S)
        require(match is not None, f"missing publication header {field}")
        contains(plain(match.group(1)), token)


def derive(documents):
    docs = {key: plain(value) for key, value in documents.items()}
    original = between(docs["compilation"], "当你的 LV", "SBC报导")
    copy = between(docs["duplicate"], "当你的 LV", "返回==>")
    same_task_block(original, copy, "duplicate lineage")
    archived = between(docs["archived_compilation"], "当你的 LV", "SBC报导")
    same_task_block(original, archived, "20011120063019 archive")
    contains(docs["archived_compilation"], "松鼠1206")
    contains(original, "LV35后去会比较轻松", "等级30级以上", "十五个仪之玉", "清光身上所有东西", "防+15 敏-2", "通行证(200元)")
    contains(docs["compilation"], "松鼠1206")
    level = between(docs["levelguide"], "lv30有一个很重要的迷", "过愿藏桥前往卡坦村")
    contains(level, "lv30以下进不去", "仪之兜(防+15 抗所有异常状态+3)", "海底隧道2楼", "多找几个lv30未解成人礼的伙伴")
    news_header(documents["levelguide"], "未知")
    caves = between(docs["caves"], "A：需要解成人", "相关新闻")
    contains(caves, "以上是我转生4次得来的经验")
    news_header(documents["caves"], "Atron")
    later = between(docs["later_adult"], "1.等级要求：30级", "7.海底通路")
    contains(docs["later_adult"][:docs["later_adult"].find("1.等级要求：30级")], "2003-05-29 13:49")
    contains(later, "15个勾玉", "道具栏全部清空", "如果此时身上有任何物品", "掉落地面", "瞬间消失", "注销或断线", "敏-3", "无法组队", "利用求救", "将15个勾玉交给仪式的审判")
    return {
        "profiles": {
            "compilation": {"reported_minimum_level": 30, "recommendation_level": 35, "recommendation_is_gate": False,
                            "jade_quantity": 15, "collection_requires_empty_bag": True,
                            "south_approach_pass_cost": 200, "all_approaches_pay": False,
                            "reward": {"name": "仪之盔", "defense_delta": 15, "agility_delta": -2, "resistance_delta": 3, "resistance_scope": "OTHER_SPELL_RESISTANCE_AS_REPORTED"},
                            "drop_destroys_jade": None, "logout_destroys_jade": None},
            "levelguide": {"reported_minimum_level": 30, "approach": "KOAO_UNDERSEA_PASSAGE_FLOOR_2_GUARD",
                           "reward": {"name": "仪之兜", "defense_delta": 15, "agility_delta": None, "resistance_delta": 3, "resistance_scope": "ALL_ABNORMAL_STATUS_AS_REPORTED"},
                           "advises_party_on_approach": True, "party_allowed_inside_trial_proven": False},
            "caves": {"adult_completion_reported_as_later_quest_prerequisite": True, "adult_completion_event_id": None},
            "later_adult": {"reported_minimum_level": 30, "jade_quantity": 15, "collection_requires_empty_bag": True,
                            "reported_flow": ["TALK_TO_GUARD", "JUDGE_REQUEST", "MESSENGER_GIVES_15_JADE", "RETURN_15_TO_JUDGE", "HELMET_REWARD"],
                            "drop_destroys_jade": True, "logout_destroys_jade": True, "disconnect_destroys_jade": True,
                            "party_inside_trial": False, "battle_help_allowed": True,
                            "reward": {"name": "仪之兜", "defense_delta": 15, "agility_delta": -3, "resistance_delta": 3, "resistance_scope": "ALL_ABNORMAL_STATUS_PREVENTION_AS_REPORTED"}},
        },
        "lineage": {"duplicate_of": {"duplicate": "compilation"}, "comparison": "COMPLETE_SELECTED_TASK_BLOCK_EQUAL_AFTER_WHITESPACE_REMOVAL",
                    "distinct_text_candidates": ["levelguide", "caves"], "independent_origins_authenticated": False,
                    "levelguide_author": "UNKNOWN", "caves_author": "Atron", "caves_firsthand_experience_is_author_claim": True},
        "source_asserted_dates": {"compilation": None, "duplicate": None, "levelguide": "2001-06-14", "caves": "2001-06-14", "later_adult": "2003-05-29"},
        "temporal_witness": {"source": "archived_compilation", "actual_capture": "20011120063019",
                             "selected_task_block_matches_current": True, "selected_normalized_characters": len(normalize(archived)),
                             "earliest_capture_exhaustively_established": False, "january_2001_content_proven": False,
                             "archive_is_independent_rule_author": False},
        "conflicts": [{"field": "reward.agility_delta", "compilation": -2, "later_adult": -3, "resolution": "UNRESOLVED_KEEP_SEPARATE_PROFILES"}],
        "scope_distinctions": {"approach_party_advice_does_not_override_trial_party_restriction": True,
                               "empty_bag_at_collection_is_not_empty_bag_at_entry": True,
                               "later_jade_lifetime_not_backdated_into_compilation": True,
                               "jade_names_are_source_local_labels_not_template_identity": True},
        "selected_block_sha256": {k: hashlib.sha256(normalize(v).encode()).hexdigest() for k, v in
                                  {"compilation": original, "duplicate": copy, "levelguide": level, "caves": caves, "later_adult": later, "archived_compilation": archived}.items()},
        "unknown": {"historical_region_and_exact_build": None, "original_item_ids": None, "original_npc_ids": None,
                    "completion_event_id": None, "reward_delivery_transaction": None, "repeatability": None,
                    "original_inventory_slots_or_stack_rules": None, "cross_profile_item_identity": None},
    }


def report(acquisitions):
    require(set(acquisitions) == set(SOURCES), "incomplete six-source acquisition")
    docs, metadata = {}, {}
    for key, (body, final_url) in acquisitions.items():
        url, encoding = SOURCES[key]
        require(body and len(body) <= 2_000_000, f"source size {key}")
        require(final_url == url, f"source redirect requires requalification {key}")
        docs[key] = body.decode(encoding, errors="replace")
        metadata[key] = {"url": url, "final_url": final_url, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                         "decoding": encoding, "replacement_characters": docs[key].count("\ufffd")}
    return {"schema": "stoneage.adult_ceremony.source_contract.r1", "sources": metadata, "observations": derive(docs),
            "current_html_authenticated_in_asserted_publication_year": False,
            "catalog_date_authenticates_compilation_bytes": False,
            "original_server_executed": False, "early_exact_build_membership": "OPEN",
            "original_quest_script_recovered": False, "stage_a_accepted": False, "stage_b_gate": "GATED"}


def fetch(key):
    url, _ = SOURCES[key]
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "StoneAge historical evidence research"}), timeout=40) as response:
        require(response.status == 200, f"HTTP {key}")
        return key, (response.read(2_000_001), response.url)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline-dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.offline_dir:
        acquisitions = {k: ((args.offline_dir / (k + ".raw")).read_bytes(), SOURCES[k][0]) for k in SOURCES}
    else:
        with ThreadPoolExecutor(max_workers=4) as pool:
            acquisitions = dict(pool.map(fetch, SOURCES))
    result = report(acquisitions)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"sources": len(result["sources"]), "profiles": 4, "original_server_executed": False}))


if __name__ == "__main__":
    main()
