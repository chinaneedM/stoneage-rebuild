"""Bounded JSS FAQ evidence: bug headings are not recovered quest scripts."""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urljoin
from urllib.request import Request, urlopen

ROOT = "http://www.titan.co.jp/stoneage/"
NAV = "research/recovered/STONEAGE-HISTORICAL-SITE-NAVIGATION-R1.json"
NAV_SHA = "7bec788ca9101aa7a06543c0df2fb15b6bc407fd47141b51cc1a99e216cd61cd"
PAGES = {
    "faqmenu": ("20010417155624", 3356, "d5ea757e563d0bf86ad96b72dc0081761b447fa3771e00a463919b89b7017f5f"),
    "faqgame": ("20010424225131", 5155, "1676093fcccaaeacd234df2dcd7fa05f1c0337c365dc787aea83b3f41fafcf91"),
}
FIXED = (
    ("MAIL_PAGE_CRASH", ("メールウィンドウ", "強制終了")),
    ("PET_NAME_STATUS_ALBUM_MISMATCH", ("ステータスウィンドウ", "ペットの名前")),
    ("BOARDED_PET_SKILLS_LOST_ON_RETURN", ("預けたペット", "技が消える")),
    ("STRING_CUTTING_STONE_NOT_CONSUMED", ("ひも切り石", "なくならない")),
    ("DESERT_CANAAN_REQUIRED_PET_NOT_RECOGNIZED", ("砂漠のカナン", "指定のペット")),
    ("DUEL_COMPANION_SKILL_BATTLE_NOT_ENDING", ("DUEL", "旅は道連れ")),
    ("EARTH_TOUR_COUNTER_BATTLE_NOT_ENDING", ("地球一周", "カウンター")),
    ("KUKUROSU_CAPTURE_EVENT_CERTIFICATE_NOT_RECEIVED", ("ククロス捕獲イベント", "証書")),
    ("KNOWLEDGE_MAGIC_DESCRIPTION_MOJIBAKE", ("物知り", "文字化け")),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def compact(value):
    return " ".join(value.split())


def fingerprint(value):
    return {"characters": len(value), "sha256": hashlib.sha256(value.encode()).hexdigest()}


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.blocks, self.links = [], [], []
        self.block = None
        self.hidden = 0

    def append(self, data):
        self.parts.append(data)
        if self.block is not None:
            self.block.append(data)

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.hidden += 1
        if self.hidden:
            return
        attrs = dict(attrs)
        if tag == "blockquote":
            require(self.block is None, "nested FAQ category")
            self.block = []
        if tag in ("br", "p", "div", "td", "tr"):
            self.append("\n")
        if tag == "a" and attrs.get("href"):
            self.links.append(urljoin(ROOT, attrs["href"]))

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.hidden:
            self.hidden -= 1
        elif not self.hidden:
            if tag == "blockquote":
                require(self.block is not None, "unmatched FAQ category")
                self.blocks.append("".join(self.block))
                self.block = None
            elif tag in ("p", "div", "td", "tr"):
                self.append("\n")

    def handle_data(self, data):
        if not self.hidden:
            self.append(data)

    @property
    def text(self):
        return compact("".join(self.parts))


def parse(document):
    parsed = Document()
    parsed.feed(document)
    parsed.close()
    require(parsed.block is None, "unterminated FAQ category")
    return parsed


def menu_contract(document):
    d = parse(document)
    expected = [ROOT + p + ".html" for p in ("faqgame", "faqstart", "faqquest")]
    require(d.links == expected, "FAQ category links changed; never guess from filename")
    require("修正された不具合" in d.text, "missing fixed-issue heading")
    require(len(d.blocks) == 4, "FAQ category count changed")
    groups = [[compact(x) for x in b.split("●")[1:]] for b in d.blocks]
    require([len(x) for x in groups] == [12, 16, 4, 9], "FAQ question coverage changed")
    require("敵やペット" in groups[0][4], "chosen detail lacks explicit pet topic")
    require("スクリーンショット" in groups[2][3], "faqquest is not a quest-guide category")
    fixed = []
    for position, (key, tokens) in enumerate(FIXED):
        require(all(t in groups[3][position] for t in tokens), "fixed issue row identity changed")
        fixed.append({"key": key, "source_order": position, "heading_fingerprint": fingerprint(groups[3][position]),
                      "evidence_kind": "INDEX_LABEL_UNDER_FIXED_ISSUES", "fix_date": None,
                      "fix_build": None, "fix_independently_executed": False, "script_or_formula_recovered": False})
    return {"category_links": expected, "category_question_counts": [12, 16, 4, 9],
            "question_heading_count": 41, "fixed_issue_count": len(fixed), "fixed_issues": fixed,
            "selected_detail_url": expected[0], "selection_basis": "MENU_EXPLICITLY_NAMES_ENEMY_AND_PET_DISPLAY_ISSUE",
            "faqquest_filename_is_quest_guide_proof": False,
            "faqquest_destination_queried": False, "faqstart_destination_queried": False,
            "category_heading_fingerprints": [[fingerprint(x) for x in group] for group in groups]}


def qa_pairs(document):
    text = parse(document).text
    segments = re.split(r"Q:", text)[1:]
    require(len(segments) == 12, "FAQ answer count changed")
    pairs = []
    for segment in segments:
        require(segment.count("A:") == 1, "missing or ambiguous FAQ answer")
        q, a = segment.split("A:")
        pairs.append((compact(q), compact(a)))
    return pairs


def detail_contract(document):
    d = parse(document)
    pairs = qa_pairs(document)
    def assertion(index, qtokens, atokens):
        q, a = pairs[index]
        require(all(t in q for t in qtokens) and all(t in a for t in atokens), "FAQ question/answer attribution changed")
    assertion(1, ("ヤン＝ミト", "クエスト"), ("現在調査中",))
    assertion(4, ("敵やペット", "表示されません"), ("再インストール", "アンインストール", "フォルダ", "削除"))
    assertion(5, ("建物や洞窟", "入れない"), ("現在調査", "報告", "MAPウィンドウ", "ログイン"))
    assertion(7, ("効果音",), ("ハードウェアアクセラレータ", "基本", "なし"))
    assertion(9, ("DP", "強者表"), ("デュエルを行うと更新",))
    assertion(10, ("フルカラー", "ウィンドウモード"), ("時刻に応じた色の変化", "パレット機能", "256色のみ"))
    require(d.links == [ROOT + "sa_se.lzh"], "FAQ download reference changed")
    return {"answer_count": 12,
            "qa_fingerprints": [{"source_order": i, "question": fingerprint(q), "answer": fingerprint(a)} for i, (q, a) in enumerate(pairs)],
            "yan_mito_quest": {"source_order": 1, "label_as_written": "ヤン＝ミト", "operator_status": "UNDER_INVESTIGATION", "npc_id": None, "quest_script": None, "fix_proven": False},
            "invisible_enemies_or_pets": {"source_order": 4, "operator_advice": "REINSTALL_WITH_OLD_GAME_DIRECTORY_REMOVAL", "client_resource_cause_proven": False, "pet_absence_or_invisibility_game_rule_proven": False, "remedy_executed": False},
            "building_or_cave_entry_issue": {"source_order": 5, "operator_status": "UNDER_INVESTIGATION", "workaround_reports": ["REENTER_VIA_OTHER_BUILDING", "CLOSE_MAP_MOVE_OUT_OF_VIEW_REOPEN_MAP", "RELOGIN"], "reported_workarounds_are_guarantees": False, "floor_or_warp_id": None},
            "duel_ranking": {"source_order": 9, "refresh_trigger_described": "PERFORM_DUEL", "dp_gain_alone_immediate_refresh_proven": False, "dp_formula": None},
            "windowed_color": {"source_order": 10, "supported_colors_described": 256, "operator_reason": "TIME_DEPENDENT_COLOR_CHANGE_USES_PALETTE", "original_palette_schedule_or_pixels_recovered": False},
            "sound_issue": {"source_order": 7, "operator_advice": "LOWER_OR_DISABLE_AUDIO_HARDWARE_ACCELERATION", "original_audio_call_or_track_mapping_proven": False},
            "download_reference": {"url": d.links[0], "queried_or_downloaded": False, "role": "REFERENCED_COMPATIBILITY_AUDIO_ARCHIVE_NOT_RECOVERED_ASSET"}}


def qualify(raw, final_url, key):
    capture, size, digest = PAGES[key]
    expected = f"https://web.archive.org/web/{capture}id_/" + ROOT + key + ".html"
    require(final_url == expected, "unexpected original URL or capture; requalify source")
    require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, "source bytes changed")
    text = raw.decode("shift_jis", errors="strict")
    require("<HTML>" in text and "FAQ" in text, "not authenticated FAQ HTML")
    return text, {"original_url": ROOT + key + ".html", "actual_capture": capture, "final_url": final_url,
                  "bytes": size, "sha256": digest, "codec": "shift_jis", "source_role": "OPERATOR_FIRST_PARTY_JSS_APRIL_2001"}


def build(acquisitions, navigation_raw):
    require(hashlib.sha256(navigation_raw).hexdigest() == NAV_SHA, "previous authenticated navigation changed")
    nav = json.loads(navigation_raw)["targets"]["jss_top"]
    require(nav["actual_capture"] == "20010414014135", "top source identity changed")
    require(any(x["target_url"] == ROOT + "faqmenu.html" for x in nav["links"]), "FAQ not linked from authenticated top")
    texts, sources = {}, {}
    for key in PAGES:
        texts[key], sources[key] = qualify(*acquisitions[key], key)
    menu, detail = menu_contract(texts["faqmenu"]), detail_contract(texts["faqgame"])
    return {"schema": "stoneage.jss.first_party_pet_faq.r1", "source_pages": sources,
            "navigation_dependency": {"path": NAV, "sha256": NAV_SHA, "top_actual_capture": nav["actual_capture"], "top_reacquired_this_round": False},
            "menu": menu, "game_faq": detail,
            "source_temporality": {"same_capture_instant": False, "snapshot_dates_are_fix_or_release_dates": False},
            "boundaries": {"qualified_html_pages": 2, "detail_pages_followed": 1, "original_server_executed": False,
                           "fixes_independently_verified": False, "pet_species_master_or_growth_formula_recovered": False,
                           "named_quest_or_skill_label_is_complete_definition": False, "jss1999_or_tw10_build_identity_proven": False,
                           "proprietary_html_images_audio_or_binaries_retained_in_git": False,
                           "stage_a_family_status_changed": False, "stage_b_production": "GATED", "r79": "PAUSED_NON_BLOCKING"}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    acquisitions = {}
    for key, (capture, _, _) in PAGES.items():
        url = f"https://web.archive.org/web/{capture}id_/" + ROOT + key + ".html"
        if args.input_dir:
            raw = (args.input_dir / ("stoneage-jss-" + key + ".raw")).read_bytes()
        else:
            with urlopen(Request(url, headers={"User-Agent": "StoneAge-Historical-Research/1.0"}), timeout=60) as response:
                raw, url = response.read(), response.url
        acquisitions[key] = raw, url
    report = build(acquisitions, Path(NAV).read_bytes())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"html_sources": 2, "detail_pages": 1, "menu_headings": 41, "fixed_issue_labels": 9, "game_answers": 12, "pet_growth_formula_recovered": False}))


if __name__ == "__main__":
    main()
