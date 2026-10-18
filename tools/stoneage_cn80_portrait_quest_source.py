"""Finite, source-bound retrieval of a 17173 8.0 quest guide.

Copyright boundary: keep only factual derived metadata and source SHA digests,
never preserve downloaded HTML, images or proprietary client artifacts in Git.
Neither a fan guide nor tests prove the original commercial server's scripts.
"""
from __future__ import annotations
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

INDEX = "https://news.17173.com/z/stoneage/renwu/renwu.htm"
DETAIL = "https://news.17173.com/z/stoneage/renwu/sa80_05.shtml"
PETS = (
    ("贝洛宝利", "红色", "北岛迷幻洞窟", 3, 4),
    ("加比奥", "黄色", "南岛拉多拉洞窟3F", 5, 6),
    ("朵洛将恩", "黑色", "吉鲁岛漆黑洞窟5F", 7, 8),
    ("格尔希洛", "白色", "吉鲁岛没落的矿坑三楼", 9, 10),
    ("布林帖斯", "蓝色", "吉鲁岛漆黑洞窟18F", 11, 12),
)
STEP_RE = re.compile(r"(?:^|\s)([1-9]|1[0-4])\.\s*(.*?)(?=\s(?:[1-9]|1[0-4])\.\s*|\Z)", re.S)


def validate_url(url: str, expected: str) -> None:
    parsed, want = urlsplit(url), urlsplit(expected)
    if (parsed.scheme != "https" or parsed.netloc.lower() != want.netloc
            or parsed.path != want.path or parsed.query or parsed.fragment):
        raise ValueError("Source response not the exact authenticated 17173 path")


class TextAndLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.text = []
        self.anchor_url = None
        self.anchor_parts = []
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.hidden += 1
        if tag == "a" and not self.hidden:
            self.anchor_url = dict(attrs).get("href")
            self.anchor_parts = []

    def handle_data(self, data):
        if not self.hidden:
            t = " ".join(data.split())
            if t:
                self.text.append(t)
                if self.anchor_url is not None:
                    self.anchor_parts.append(t)

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.hidden:
            self.hidden -= 1
        if tag == "a" and self.anchor_url is not None:
            self.anchors.append((self.anchor_url, "".join(self.anchor_parts)))
            self.anchor_url = None
            self.anchor_parts = []


def decode_and_parse(data: bytes):
    if not 500 <= len(data) <= 350000:
        raise ValueError("source empty, truncated, or abnormally oversized")
    for enc in ("utf-8", "gb18030"):
        try:
            s = data.decode(enc, errors="strict")
            p = TextAndLinks()
            p.feed(s)
            p.close()
            if "爱作画的少女" in " ".join(p.text):
                return enc, p
        except UnicodeDecodeError:
            pass
    raise ValueError("Neither qualified Chinese source text nor strict text encoding")


def split_steps(text: str):
    # Start from the first explicitly identified actual step after the guide label.
    match = re.search(r"(?<!\d)1\.\s*瑞而亚斯", text)
    if not match:
        raise ValueError("guide step 1 not found (do not infer another quest)")
    sections = [(int(n), val.strip()) for n, val in STEP_RE.findall(text[match.start():])]
    if [n for n, _ in sections] != list(range(1, 15)):
        raise ValueError("quest steps not precisely ordered 1..14")
    return {n: val for n, val in sections}


def derive(index_bytes: bytes, detail_bytes: bytes) -> dict:
    index_encoding, index = decode_and_parse(index_bytes)
    detail_encoding, detail = decode_and_parse(detail_bytes)
    actual_links = [
        {"href": urljoin(INDEX, href), "label": label}
        for href, label in index.anchors if label.strip() == "爱作画的少女"
    ]
    if len(actual_links) != 1 or actual_links[0]["href"] != DETAIL:
        raise ValueError("index link to the exact named guide not demonstrated")
    full = " ".join(detail.text)
    if "石器8.0版本任务全攻略" not in full:
        raise ValueError("source did not identify 8.0 guide context")
    steps = split_steps(full)
    if "纱美加" not in steps[1] or "迪伊恩" not in steps[2]:
        raise ValueError("two character roles missing")
    coords_step1 = steps[1].replace("（", "(").replace("）", ")")
    coords_step2 = steps[2].replace("（", "(").replace("）", ")")
    if "(67.75)" not in coords_step1 or "(59.17)" not in coords_step2 or "(26.47)" not in coords_step2:
        raise ValueError("quest origin and shop coordinates not supported")
    pairs = []
    for name, color, place, get_step, deliver_step in PETS:
        capture = steps[get_step]
        delivery = steps[deliver_step]
        if name not in capture or name not in delivery or color not in delivery:
            raise ValueError(f"pet-to-pigment pairing changed: {name}")
        if "1级" not in capture:
            raise ValueError(f"claimed level-1 constraint absent: {name}")
        pairs.append({
            "pet_name_as_written": name, "reported_capture_level": 1,
            "pigment_color": color, "location_reference": place,
            "source_step_capture": get_step, "source_step_turn_in": deliver_step,
            "pet_master_id": None, "location_floor_id": None,
            "actual_encounter_and_drop_verified": False
        })
    if "5种颜色" not in steps[13] or "纱美加" not in steps[13] or "不能骑宠" not in steps[13]:
        raise ValueError("portrait completion and no-riding remark altered")
    if "5幅自画像" not in steps[14]:
        raise ValueError("reported five-portrait completion not evidenced")
    if "瑞而亚斯" not in steps[1] or "瑞而亚斯" not in steps[2]:
        raise ValueError("do not silently correct source spelling")
    return {
        "schema": "stoneage.cn80.named_quest_portrait.source_r1",
        "package": "CN80_NAMED_QUEST_ORIGINAL_SOURCE_TRACE-01",
        "source_type": "THIRD_PARTY_PLAYER_WALKTHROUGH_NOT_OFFICIAL_RUNTIME",
        "site_scope": "17173_STONEAGE_80_MAINLAND_JINSHAN_LABELED_PORTAL",
        "original_publication_date": None, "archival_snapshot_date": None,
        "source_chain": {
            "index": {"url": INDEX, "sha256": hashlib.sha256(index_bytes).hexdigest(),
                      "bytes": len(index_bytes), "codec": index_encoding,
                      "actual_named_href": actual_links[0]["href"]},
            "detail": {"url": DETAIL, "sha256": hashlib.sha256(detail_bytes).hexdigest(),
                       "bytes": len(detail_bytes), "codec": detail_encoding,
                       "heading": "爱作画的少女", "claimed_version": "8.0"},
            "official_operator_patch_verified": False,
            "page_bytes_retained_in_git": False,
            "downloaded_original_images": False,
        },
        "character_roles": [
            {"name_as_written": "纱美加", "role": "QUEST_GIVER_AND_PORTRAIT_REWARD",
             "reported_urban_xy": [67, 75], "npc_id": None},
            {"name_as_written": "迪伊恩", "role": "PET_TURNIN_AND_PIGMENT_ISSUER",
             "reported_shop_urban_xy": [59, 17], "reported_shop_internal_xy": [26, 47],
             "npc_id": None}
        ],
        "pet_to_pigment": pairs,
        "step_count": 14, "capture_turnin_pair_count": 5,
        "completion": {"requires_five_reported_pigment_colors": True,
                       "reported_portrait_reward_count": 5,
                       "cannot_ride_pet_during_portrait_scene_reported": True,
                       "server_script_or_actual_reward_state_proven": False},
        "name_variants": {"walkthrough_city": "瑞而亚斯", "official_2005_ice_region": "瑞爾亞斯",
                          "identity_equivalence_confirmed": False},
        "prerequisites": {"stated_in_this_guide": None, "none_proven": False,
                          "later_2012_8_5_claim_to_verify_separately": "无法逃离的审判"},
        "unknowns": {"npc_ids": None, "pet_ids": None, "map_floor_ids": None,
                     "quest_flags": None, "actual_first_release_build": None,
                     "exact_reward_item_ids": None, "scripted_event_sequence": None},
        "game_production_started": False, "history_family_status_changed": False,
        "r79_unpaused": False,
        "next": "CN80_PORTRAIT_PREREQUISITE_VERSION_BOUNDARY-01"
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    fetched = {}
    for uri in (INDEX, DETAIL):
        req = Request(uri, headers={"User-Agent": "Mozilla/5.0 (compatible; StoneAgeSourceResearch/1.0)"})
        with urlopen(req, timeout=45) as response:
            validate_url(response.url, uri)
            fetched[uri] = response.read(350001)
    result = derive(fetched[INDEX], fetched[DETAIL])
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)+"\n", encoding="utf-8")
    print("SOURCE_DERIVED_REPORT=" + str(path))
    print("SOURCE_DERIVED_SUMMARY=" + json.dumps({
        "index_bytes": result["source_chain"]["index"]["bytes"],
        "index_sha256": result["source_chain"]["index"]["sha256"],
        "detail_bytes": result["source_chain"]["detail"]["bytes"],
        "detail_sha256": result["source_chain"]["detail"]["sha256"],
        "step_count": result["step_count"],
        "pet_names": [p["pet_name_as_written"] for p in result["pet_to_pigment"]],
        "npc_roles": [p["name_as_written"] for p in result["character_roles"]],
        "reward_count": result["completion"]["reported_portrait_reward_count"]
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
