"""Three explicitly linked operator catalog pages and one separately dated GIF.

Only research metadata is retained. Listing numbers are not game species IDs;
per-record provenance survives extraction from the mixed-capture catalog.
"""
from __future__ import annotations
import argparse
import hashlib
from html.parser import HTMLParser
from io import BytesIO
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from PIL import Image

BASE = "http://www.hangame.co.jp/publish/sa/"
IMAGES = "http://images.hangame.co.jp/_images/game/saj/"
PAGES = (
    {"file": "chara2.asp", "capture": "20031214055443", "bytes": 36332,
     "sha256": "a01a2c93d410511b9e08f7a066569d8cec8db883f50047baf0ca3160d50ed0fc", "start": 1, "count": 45},
    {"file": "chara2-2.asp", "capture": "20031214051259", "bytes": 36343,
     "sha256": "09faee5a55cb09ea8527090fb09fc00166abce94c83ef34322f4cacd4ad65249", "start": 46, "count": 45},
    {"file": "chara2-3.asp", "capture": "20040220221717", "bytes": 34310,
     "sha256": "b9284c6185fc5a999dd3bf0da3ac9d341e31312dcdf5859ee5a5786eb0cbc9ad", "start": 91, "count": 34},
)
IMAGE_URL = IMAGES + "petpicgroup1-1.gif"
IMAGE_CAPTURE = "20060604065927"
IMAGE_SHA = "593345c3edf78ebcaa2dff0c27a2d10a92b4eefcc4aef4db14aee2efdc5e013f"
REPORT = "research/recovered/STONEAGE-JP-OFFICIAL-PET-CATALOG-R1.json"
PICTURE = re.compile(re.escape(IMAGES) + r"petpicgroup([123])-([1-9][0-9]*)\.gif$")
PAGE_LINK = re.compile(r"location\.href='(chara2(?:-[23])?\.asp)';$")


def require(value, message):
    if not value:
        raise ValueError(message)


def archive(original, capture):
    return "https://web.archive.org/web/" + capture + "id_/" + original


class Grid(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.table_id = 0
        self.cells = {}
        self.images = []
        self.visible = []
        self.hidden = 0
        self.link = None
        self.links = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ("script", "style"):
            self.hidden += 1
        if self.hidden:
            return
        if tag == "table":
            self.tables.append({"table": self.table_id, "row": -1, "col": -1, "open": False})
            self.table_id += 1
        if tag == "tr" and self.tables:
            self.tables[-1].update(row=self.tables[-1]["row"] + 1, col=-1)
        if tag in ("td", "th") and self.tables:
            t = self.tables[-1]
            t.update(col=t["col"] + 1, open=True)
            self.cells[(t["table"], t["row"], t["col"])] = []
        if tag == "img" and PICTURE.fullmatch(d.get("src", "")):
            require(bool(self.tables), "Pet image outside source table")
            t = self.tables[-1]
            require(t["open"], "Pet image outside source cell")
            self.images.append({**t, **d})
        if tag == "font" and PAGE_LINK.fullmatch(d.get("onclick", "")):
            self.link = {"file": PAGE_LINK.fullmatch(d["onclick"])[1], "label": []}

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.hidden:
            self.hidden -= 1
        if self.hidden:
            return
        if tag in ("td", "th") and self.tables:
            self.tables[-1]["open"] = False
        if tag == "table" and self.tables:
            self.tables.pop()
        if tag == "font" and self.link:
            self.links.append({"file": self.link["file"], "label": "".join(self.link["label"])})
            self.link = None

    def handle_data(self, value):
        value = " ".join(value.split())
        if not value or self.hidden:
            return
        self.visible.append(value)
        if self.link:
            self.link["label"].append(value)
        if self.tables and self.tables[-1]["open"]:
            t = self.tables[-1]
            self.cells[(t["table"], t["row"], t["col"])].append(value)


def classify_page(html, page_number):
    require(page_number in (1, 2, 3), "Page outside qualified manifest")
    pin = PAGES[page_number - 1]
    p = Grid()
    p.feed(html)
    require(any("１００種類を超えるペット" in value for value in p.visible), "Operator pet-catalog topic missing")
    require(len(p.images) == pin["count"], "Wrong number of actual pet image references")
    require(len({im["table"] for im in p.images}) == 1, "Pet references span different tables")
    entries, seen = [], set()
    for im in p.images:
        match = PICTURE.fullmatch(im["src"])
        family, local = int(match[1]), int(match[2])
        require(family == page_number and 1 <= local <= pin["count"], "Wrong image family/local ordinal")
        require(local not in seen, "Duplicate local image reference")
        seen.add(local)
        require((im["row"], im["col"]) == (3 * ((local - 1) // 9) + 2, (local - 1) % 9),
                "Filename order is not the qualified number/name/image DOM relation")
        require((im.get("width"), im.get("height")) == ("60", "65"), "Declared source dimensions changed")
        def cell(row):
            return "".join(p.cells.get((im["table"], row, im["col"]), []))
        ordinal = pin["start"] + local - 1
        require(cell(im["row"] - 2) == str(ordinal), "Displayed number differs from same-column picture")
        name = cell(im["row"] - 1)
        require(bool(name) and not name.isdigit(), "Name cell missing or replaced with ordinal")
        entries.append({"web_ordinal": ordinal, "name_as_written": name, "image_original_url": im["src"],
                        "local_image_number": local, "cells": [im["row"] - 2, im["row"] - 1, im["row"], im["col"]]})
    require([e["web_ordinal"] for e in entries] == list(range(pin["start"], pin["start"] + pin["count"])), "Source entry order changed")
    expected = [
        {"file": "chara2.asp", "label": "【１～４５】"},
        {"file": "chara2-2.asp", "label": "【４６～９０】"},
        {"file": "chara2-3.asp", "label": "【９１～１２４】"},
    ]
    require(p.links == [v for i, v in enumerate(expected, 1) if i != page_number], "Actual pagination labels/targets differ")
    return entries, p.links


def inspect_image(raw, final):
    require(final == archive(IMAGE_URL, IMAGE_CAPTURE), "Wrong pet image host/path/capture")
    require(len(raw) == 4460 and hashlib.sha256(raw).hexdigest() == IMAGE_SHA, "Pet image byte pin mismatch")
    with Image.open(BytesIO(raw)) as im:
        require(im.format == "GIF" and im.size == (60, 65) and im.n_frames == 1, "Unexpected pet GIF structure")
        im.load()


def inspect_page(raw, final, page_number):
    require(page_number in (1, 2, 3), "Page outside qualified manifest")
    pin = PAGES[page_number - 1]
    require(final == archive(BASE + pin["file"], pin["capture"]), "Page host/path/capture mismatch")
    require(len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"], "Page byte pin mismatch")
    return classify_page(raw.decode("cp932", errors="strict"), page_number)


def build(page_inputs, image_raw, image_final):
    require(len(page_inputs) == 3, "Exactly the three qualified linked pages are required")
    inspect_image(image_raw, image_final)
    sources, records = [], []
    for page_number, ((raw, final), pin) in enumerate(zip(page_inputs, PAGES), 1):
        original = BASE + pin["file"]
        entries, links = inspect_page(raw, final, page_number)
        source = {**pin, "original_url": original, "strict_replay_url": final, "encoding": "CP932_STRICT",
                  "name_list_sha256": hashlib.sha256(("\n".join(e["name_as_written"] for e in entries) + "\n").encode()).hexdigest(),
                  "actual_pagination": [{"label": link["label"], "original_url": BASE + link["file"],
                                         "kind": "STATIC_ONCLICK_LITERAL_NOT_EXECUTED"} for link in links]}
        sources.append(source)
        for entry in entries:
            n = entry["web_ordinal"]
            records.append({
                "record_id": f"jp-hangame-pet-web:position:{n:03d}", "collection": "pets",
                "entity_type": "OFFICIAL_NAMED_PET_WEB_ENTRY", "record_revision": 1,
                "version_profile": "JAPAN_HANGAME_WEB_" + pin["capture"][:8],
                "source_refs": [{"source": original, "sha256": pin["sha256"], "actual_capture": pin["capture"],
                                 "evidence_role": "SAME_COLUMN_NUMBER_NAME_IMAGE_REFERENCE", "dom_cells": entry["cells"]}],
                "verification_status": "OPERATOR_NAME_AND_IMAGE_REFERENCE_NOT_GAME_SPECIES_ID",
                "rights_status": "RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED",
                "web_ordinal": n, "name_as_written": entry["name_as_written"], "client_species_graphic_ids": None,
                "cross_region_aliases": None, "stats_growth_habitat_skills": None,
                "image": {"original_url": entry["image_original_url"], "local_image_number": entry["local_image_number"],
                          "declared_size": [60, 65], "pixels_acquired": n == 1,
                          "actual_capture": IMAGE_CAPTURE if n == 1 else None,
                          "sha256": IMAGE_SHA if n == 1 else None, "bytes": 4460 if n == 1 else None,
                          "actual_size": [60, 65] if n == 1 else None, "frames": 1 if n == 1 else None,
                          "same_instant_as_page_proven": False},
            })
    require(len(records) == 124 and len({r["record_id"] for r in records}) == 124, "Catalog range/identity lost")
    return {
        "schema": "stoneage.jp.official_pet_catalog.r1", "date": "2026-10-19",
        "initial_task": "JP2003-OFFICIAL-PET-NAMED-VISUAL-SOURCE-01",
        "adjacent_bounded_task": "JP-OFFICIAL-PET-CATALOG-PAGINATION-CLOSURE-01",
        "parent_source": "research/recovered/STONEAGE-JP2003-CHARACTER-VISUAL-SOURCE-R1.json",
        "scope": "THREE_ACTUALLY_LINKED_PET_PAGINATION_PAGES_AND_ONE_IMAGE_NO_OTHER_TABS",
        "sources": sources, "record_count": len(records), "records": records,
        "reviewed_image": {"original_url": IMAGE_URL, "strict_replay_url": image_final, "actual_capture": IMAGE_CAPTURE,
                           "sha256": IMAGE_SHA, "bytes": 4460, "format": "GIF", "actual_size": [60, 65], "frames": 1,
                           "linked_web_ordinal": 1, "name_as_written": records[0]["name_as_written"],
                           "human_visual_review": "EXACT_HASH_IMAGE_VIEWED_WITH_VIEW_IMAGE",
                           "observations": ["ROUNDED_CREATURE_ILLUSTRATION", "ORANGE_YELLOW_BODY", "PALE_FACE_AND_UPPER_BODY"],
                           "proves_original_client_sprite_or_animation": False},
        "coverage": {"source_describes_more_than_100_pets": True, "pagination_entries_observed": 124,
                     "page_counts": [45, 45, 34], "actual_page_capture_years": [2003, 2003, 2004],
                     "single_contemporaneous_2003_roster_proven": False,
                     "complete_original_server_species_census_proven": False, "unacquired_image_references": 123,
                     "web_ordinal_equals_local_image_suffix_or_game_id": False},
        "boundaries": {"source_html_or_pixels_in_git": False, "javascript_forms_activex_or_binaries_executed": False,
                       "jss1999_tw10_or_174a_build_identity_proven": False,
                       "copyright_1999_footer_proves_client_build_year": False,
                       "translated_aliases_or_same_species_across_regions_assumed": False,
                       "actual_stats_captures_or_server_rules_recovered": False,
                       "stage_a_families": "7_PARTIAL_2_OPEN_UNCHANGED", "stage_b_and_wiki": "GATED", "r79": "PAUSED_NON_BLOCKING"},
        "next": "OFFICIAL-PET-VISUAL-COVERAGE-AND-VERSION-REVIEW-01",
    }


def acquire(url):
    for attempt in range(2):
        try:
            with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0 StoneAgeHistoricalEvidence"}), timeout=40) as r:
                return r.read(350001), r.url
        except HTTPError as exc:
            if attempt or exc.code not in (502, 503, 504):
                raise
            print("BOUNDED_RETRY_HTTP=" + str(exc.code) + " URL=" + url)
        except (URLError, TimeoutError) as exc:
            if attempt:
                raise
            print("BOUNDED_RETRY_NETWORK=" + type(exc).__name__ + " URL=" + url)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--local-input-dir")
    p.add_argument("--output", required=True)
    args = p.parse_args()
    page_inputs = []
    for n, pin in enumerate(PAGES, 1):
        final = archive(BASE + pin["file"], pin["capture"])
        if args.local_input_dir:
            name = "jp-pets.html" if n == 1 else f"jp-pets-{n}.html"
            page_inputs.append(((Path(args.local_input_dir) / name).read_bytes(), final))
        else:
            page_inputs.append(acquire(final))
    final = archive(IMAGE_URL, IMAGE_CAPTURE)
    image, image_final = ((Path(args.local_input_dir) / "jp-pet-first.gif").read_bytes(), final) if args.local_input_dir else acquire(final)
    obj = build(page_inputs, image, image_final)
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(payload, encoding="utf-8")
    print("CATALOG_RECORDS=" + str(len(obj["records"])))
    print("DERIVED_SHA256=" + hashlib.sha256(payload.encode()).hexdigest())
    for source in obj["sources"]:
        print("SOURCE=" + source["file"] + " CAPTURE=" + source["capture"] + " SHA256=" + source["sha256"])


if __name__ == "__main__":
    main()
