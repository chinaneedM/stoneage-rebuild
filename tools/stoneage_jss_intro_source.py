"""First-party JSS 2001 introduction and its finite 15 linked screenshot sources.

Keep only derived numeric assertions, URL custody and image metadata. Never
write original HTML or images to Git or infer that Japanese screenshots are TW1.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import urllib.request
from urllib.parse import urljoin
from PIL import Image

from tools.stoneage_early_content_probe import plain

ROOT = "http://www.titan.co.jp/stoneage/"
PAGE_URL = "https://web.archive.org/web/20010417155051id_/" + ROOT + "contents.html"
PAGE_SHA = "a5553d476ed39deadde296d589d0a9eabe1378e11cbd528f8947f37eb74e4a8b"


def require(ok, message):
    if not ok:
        raise ValueError(message)


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img" and re.fullmatch(r"image/sakss\d{2}\.jpg", attrs.get("src", "")):
            self.rows.append({"original_url": urljoin(ROOT, attrs["src"]),
                              "html_width": int(attrs["width"]),
                              "html_height": int(attrs["height"])})


def page_contract(raw, final_url):
    require(final_url == PAGE_URL, "introduction source redirect changed")
    require(len(raw) == 6426 and hashlib.sha256(raw).hexdigest() == PAGE_SHA, "introduction source bytes changed")
    text = raw.decode("shift_jis", errors="strict")
    normalized = plain(text)

    def numeric(pattern):
        m = re.search(pattern, normalized)
        require(m is not None, "missing original numerical assertion")
        return int(m.group(1))

    characters = numeric(r"キャラクターは全部で(\d+)種類")
    colors = numeric(r"カラーのバリエーションを含めれば(\d+)種類")
    pets = numeric(r"ペットは最大(\d+)匹")
    party = numeric(r"最大(\d+)人までパーティー")
    require((characters, colors, pets, party) == (12, 48, 5, 5), "JSS introduction counts changed")
    require(all(t in normalized for t in ("外見は能力に関係しない", "レベルが低いうちはただ", "何かの肉", "相棒となる恐竜", "双方合意")), "JSS introduction gameplay identity")
    parser = Images()
    parser.feed(text)
    expected = [ROOT + f"image/sakss{i:02d}.jpg" for i in range(1, 16)]
    require([r["original_url"] for r in parser.rows] == expected, "finite linked screenshot set changed")
    return {
        "character_body_types_reported": characters,
        "appearance_variants_including_colors_reported": colors,
        "appearance_affects_ability_described": False,
        "maximum_carried_pets_reported": pets,
        "maximum_party_players_reported": party,
        "low_level_free_healing_described": True,
        "free_healing_level_cutoff": None,
        "savepoint_asks_for_some_meat_described": True,
        "savepoint_specific_item_id_or_quantity": None,
        "starting_companion_described": True,
        "starting_companion_species_or_allocation": None,
        "consensual_duel_described": True,
        "exact_tw10_character_census_or_rule_equivalence": False,
    }, parser.rows


def image_metadata(raw, final_url, original_url):
    m = re.fullmatch(r"https://web\.archive\.org/web/(\d{14})id_/(http://www\.titan\.co\.jp/stoneage/image/sakss\d{2}\.jpg)", final_url)
    require(m is not None and m.group(2) == original_url, "image redirected to another original resource")
    require("19990101000000" <= m.group(1) <= "20021231235959", "image capture outside historical window")
    require(0 < len(raw) <= 1_000_000, "image size boundary")
    with Image.open(io.BytesIO(raw)) as im:
        im.verify()
    with Image.open(io.BytesIO(raw)) as im:
        require(im.format == "JPEG", "linked JPEG has another format")
        width, height = im.size
    return {"final_url": final_url, "actual_capture": m.group(1), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "actual_width": width,
            "actual_height": height, "format": "JPEG", "same_moment_as_page_proven": False,
            "tw10_same_build_authenticated": False}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "StoneAge historical evidence research"})
    with urllib.request.urlopen(req, timeout=40) as response:
        require(response.status == 200, "source HTTP status")
        return response.read(1_000_001), response.url


def build(page_raw, page_final, acquire, unavailable=()):
    contracts, references = page_contract(page_raw, page_final)
    unavailable = set(unavailable)

    def one(row):
        raw, final = acquire(row["original_url"])
        return {**row, **image_metadata(raw, final, row["original_url"])}

    with ThreadPoolExecutor(max_workers=4) as pool:
        images = list(pool.map(one, [r for r in references if r["original_url"] not in unavailable]))
    unqualified = [{**r, "status": "NOT_OBTAINED_IN_BOUNDED_ATTEMPTS",
                    "source_absence_established": False}
                   for r in references if r["original_url"] in unavailable]
    return {"schema": "stoneage.jss2001.introduction_screenshot_sources.r1",
            "source_page": {"final_url": page_final, "actual_capture": "20010417155051", "bytes": len(page_raw), "sha256": PAGE_SHA, "encoding": "shift_jis", "replacement_characters": 0, "role": "FIRST_PARTY_INTRODUCTION"},
            "contracts": contracts, "linked_screenshot_count": len(references),
            "qualified_screenshot_count": len(images), "images": images,
            "unqualified_image_references": unqualified,
            "boundaries": {"image_bytes_checked_temporarily": True, "original_html_or_pixels_retained_in_git": False, "entire_game_visuals_recovered": False, "species_or_bitmap_id_mapping_proven": False, "jss1999_or_tw10_same_build_proven": False, "screen_coordinates_recovered": False, "server_runtime_executed": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page", type=Path, help="Temporary original HTML input")
    parser.add_argument("--images", type=Path, help="Temporary source image directory")
    parser.add_argument("--source-index", type=Path, help="Temporary first retrieval URL metadata")
    parser.add_argument("--reference", type=Path, help="Replay exact already qualified image captures")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    page_raw, final = (args.page.read_bytes(), PAGE_URL) if args.page else fetch(PAGE_URL)
    if args.images:
        index = json.loads(args.source_index.read_text())
        lookup = {r["original_url"]: r for r in index}
        unavailable = [r["original_url"] for r in index if "error" in r]
        def acquire(original):
            row = lookup[original]
            require("error" not in row, "first source attempt unavailable; not source absence")
            return (args.images / original.rsplit("/", 1)[-1]).read_bytes(), row["final_url"]
    else:
        reference = json.loads(args.reference.read_text()) if args.reference else None
        unavailable = [r["original_url"] for r in reference.get("unqualified_image_references", [])] if reference else []
        lookup = {r["original_url"]: r["final_url"] for r in reference["images"]} if reference else {}
        def acquire(original):
            return fetch(lookup.get(original, "https://web.archive.org/web/20010417155051id_/" + original))
    result = build(page_raw, final, acquire, unavailable)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"source_page": result["source_page"]["actual_capture"], "qualified_images": len(result["images"]), "tw10_same_build": False}))


if __name__ == "__main__":
    main()
