"""Finite first-party manual / published-guide content acquisition.

Retain derived facts, hashes and exact retrieval URLs only. Never run the game,
infer missing commercial server IDs, or retain downloaded HTML in the report.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html
import json
from pathlib import Path
import re
import urllib.request

JSS_CAPTURE = "20010418083149"
SOURCES = {
    "jss_manual": (f"https://web.archive.org/web/{JSS_CAPTURE}id_/http://www.titan.co.jp/stoneage/manual02.html", "shift_jis"),
    "catalog": ("https://games.sina.com.cn/downgames/other/0118654.shtml", "gb18030"),
    "logging": ("https://games.sina.com.cn/handbook/0101/01186091.shtml", "gb18030"),
    "adult": ("https://games.sina.com.cn/handbook/0101/01186091_c1.shtml", "gb18030"),
    "delivery": ("https://games.sina.com.cn/handbook/0101/01186091_c2.shtml", "gb18030"),
    "brothers": ("https://games.sina.com.cn/handbook/0101/01186092.shtml", "gb18030"),
    "later_delivery": ("https://games.sina.com.cn/zhqu/sta/rwgl1_1.shtml", "gb18030"),
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def plain(text):
    text = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", text, flags=re.I | re.S)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", text)).split())


def section(document, anchor):
    matches = list(re.finditer(r'<a\b[^>]*(?:name|id)=["\x27]?(\d+)["\x27]?[^>]*>', document, re.I))
    index = next((i for i, m in enumerate(matches) if m.group(1) == anchor), None)
    require(index is not None, f"missing original manual anchor {anchor}")
    end = matches[index + 1].start() if index + 1 < len(matches) else len(document)
    return plain(document[matches[index].end():end])


def integer(text, pattern, label):
    match = re.search(pattern, text)
    require(match is not None, f"missing numeric observation: {label}")
    return int(match.group(1).translate(str.maketrans("０１２３４５６７８９", "0123456789")))


def derive(documents):
    manual = documents["jss_manual"]
    selected = {a: section(manual, a) for a in ("7030", "8010", "8025", "8050", "8070", "8100")}
    bus = selected["8100"]
    require(all(name in bus for name in ("サムギル", "マリナス", "クオ", "ジャジャ", "カルターナ", "タムタム")), "bus village set")
    require(re.search(r"サムギル.*?マリナス.*?クオ.*?間", bus) is not None and
            re.search(r"ジャジャ.*?カルターナ.*?タムタム.*?間", bus) is not None, "bus route grouping")
    minutes = integer(bus, r"([0-9０-９]+)分間停車", "bus stop minutes")
    seats = integer(bus, r"乗車は([0-9０-９]+)人まで", "bus passengers")
    require(minutes == 3 and seats == 4 and "エンカウント" in bus and "しません" in bus, "manual bus contract changed")
    require("お供え物" in selected["8010"] and "初めて" in selected["8010"], "first save-point offering")
    require("一定時間" in selected["7030"] and "消滅" in selected["7030"], "ordinary ground-item lifetime")
    require("マンモス急便" in selected["8050"] and "鉱石掘り" in selected["8050"], "manual work examples")
    require("有料" in selected["8070"] and "技" in selected["8070"] and "買取" in selected["8070"], "village services")
    catalog = plain(documents["catalog"])
    require("2001-01-18" in catalog and "36K" in catalog and "sqsd-rw3.zip" in documents["catalog"], "dated download-catalog identity")
    require("24721" in documents["catalog"], "download action identity")
    require("松鼠1206" in catalog and "0118654.shtml" in documents["logging"], "guide-to-dated-catalog link")
    for key in ("logging", "adult", "delivery", "brothers"):
        require("松鼠1206" in plain(documents[key]) and "所有任务完全攻略" in plain(documents[key]), "guide attribution")
    adult = plain(documents["adult"])
    minimum = integer(adult, r"LV\s*到达\s*(\d+)\s*级", "adult level")
    require(minimum == 30 and "十五个仪之玉" in adult and "通行证(200元)" in adult, "adult ceremony guide observations")
    delivery = plain(documents["delivery"])
    require(all(x in delivery for x in ("弥生", "日美子", "仙尼亚的花", "扣两点魅力")), "delivery branch")
    later = plain(documents["later_delivery"])
    require("2003-05-29" in later and "友谊（一）" in later and "友谊（二）" in later and "扣魅力一点" in later, "later two-branch comparison")
    logging = plain(documents["logging"])
    require(all(x in logging for x in ("伐木许可证", "最后攻击", "宠物", "14根木", "约有5000")), "logging reward limits")
    brothers = plain(documents["brothers"])
    require("5张答案纸" in brothers and "水晶" in brothers and "注销" in brothers and "HELP" in brothers, "brothers guide observations")
    return {
        "manual_contracts": {
            "save_point": {"next_login_uses_recorded_point": True, "first_use_offering_required": True, "offering_id": None, "offering_quantity": None, "durable_server_write_proven": False},
            "bus": {"route_village_sets": [["サムギル", "マリナス", "クオ"], ["ジャジャ", "カルターナ", "タムタム"]], "direct_edge_topology_proven": False, "stop_minutes": minutes, "passenger_limit": seats, "encounters_while_riding": False, "boarding_and_exit_control": "GROUP_BUTTON_WHILE_FACING_BUS_FOR_BOARDING", "fare": None},
            "services": {"work_examples": ["VILLAGE_PARCEL_DELIVERY", "KURUKU_MINE_ORE_WORK"], "paid_pet_skill_training": True, "pet_buyback": True, "every_village_has_every_facility": False, "prices_or_job_payouts": None},
            "ground_item": {"ordinary_ground_item_expires_after_unspecified_time": True, "duration": None, "quest_specific_immediate_drop_or_logout_flag_proven": False},
        },
        "guide_profiles": [
            {"id": "FRIENDSHIP_SHELL_DELIVERY", "source": "delivery", "reported_flow": ["YAYOI_MARINAS_GIVES_SHELL", "HIMIKO_SAMGIL_RECEIVES", "FLOWER_REWARD"], "reported_drop_consequence": {"item_vanishes": True, "charm_delta": -2}, "item_id": None, "early_version_membership": "OPEN"},
            {"id": "ADULT_CEREMONY", "source": "adult", "reported_min_level": minimum, "recommended_level_is_gate": False, "reported_jade_quantity": 15, "reported_south_approach_pass_cost": 200, "pass_cost_required_for_all_approaches": False, "reward_type": "CEREMONY_HELMET", "item_id": None, "early_version_membership": "OPEN"},
            {"id": "LOGGING_LICENCE", "source": "logging", "reported_flow": ["AXE_ERRAND", "INTRODUCTION", "LICENCE", "PLAYER_LAST_HIT_WOOD", "WOOD_BUYBACK_AND_LICENCE_RETURN"], "guide_example": {"wood_count": 14, "approximate_total_stone": 5000, "exact_unit_price": None}, "pet_last_hit_qualifies_in_guide": False, "item_id": None, "early_version_membership": "OPEN"},
            {"id": "FIVE_BROTHERS", "source": "brothers", "reported_answer_papers": 5, "reported_crystal_lost_on_logout": True, "party_entry_restricted_in_guide": True, "in_battle_help_reported": True, "server_logout_flag": None, "early_version_membership": "OPEN"},
        ],
        "comparison": {"source": "later_delivery", "dated_page": "2003-05-29", "contains_both_delivery_directions": True, "earlier_shell_to_flower_branch_is_not_disproved_by_reverse_branch": True, "later_repeat_charm_delta": -1, "repeat_penalty_and_earlier_discard_penalty_are_different_operations": True, "all_named_shells_share_one_item_id": None},
        "manual_section_hashes": {a: hashlib.sha256(t.encode()).hexdigest() for a, t in selected.items()},
    }


def report(acquisitions):
    docs, sources = {}, {}
    for key, (body, final_url) in acquisitions.items():
        url, encoding = SOURCES[key]
        require(body and len(body) <= 2_000_000, f"source size {key}")
        if key == "jss_manual":
            require(f"/web/{JSS_CAPTURE}id_/" in final_url and final_url.endswith("/stoneage/manual02.html"), "manual capture redirect changed; requalify date")
        docs[key] = body.decode(encoding, errors="replace")
        sources[key] = {"replay_url": url, "final_url": final_url, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "decoding": encoding, "replacement_characters": docs[key].count("\ufffd")}
    require(set(docs) == set(SOURCES), "incomplete seven-source acquisition")
    return {"schema": "stoneage.early_content.guide_manual_acquisition.r1", "sources": sources,
            "observations": derive(docs), "manual_capture": JSS_CAPTURE,
            "manual_is_1999_or_tw10_exact_build": False,
            "catalog_published_date": "2001-01-18", "catalog_date_authenticates_current_html_bytes_in_2001": False,
            "guide_zip_obtained": False, "original_server_executed": False,
            "early_quest_scripts_recovered": False, "stage_a_accepted": False, "stage_b_gate": "GATED"}


def fetch(key):
    url, _ = SOURCES[key]
    request = urllib.request.Request(url, headers={"User-Agent": "StoneAge historical evidence research"})
    with urllib.request.urlopen(request, timeout=40) as response:
        require(response.status == 200, f"HTTP {key}")
        return key, (response.read(2_000_001), response.url)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--offline-dir", type=Path, help="Temporary source directory, never committed")
    args = parser.parse_args()
    if args.offline_dir:
        acquisitions = {k: ((args.offline_dir / (k + ".raw")).read_bytes(), SOURCES[k][0]) for k in SOURCES}
    else:
        with ThreadPoolExecutor(max_workers=4) as pool:
            acquisitions = dict(pool.map(fetch, SOURCES))
    result = report(acquisitions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"sources": len(result["sources"]), "manual_contracts": 4, "guide_profiles": 4,
                      "original_server_executed": False, "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
