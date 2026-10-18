"""One exact Japanese operator page, its DOM image pairs and one reviewed GIF.

Web positions are research identifiers. They are never client body/face IDs.
Source HTML and image bytes are transient, including during CI replay.
"""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
from io import BytesIO
import json
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from PIL import Image

PAGE_ORIGINAL = "http://www.hangame.co.jp/publish/sa/chara.asp"
PAGE_REQUESTED = "https://web.archive.org/web/20031214055553id_/" + PAGE_ORIGINAL
PAGE_FINAL = "https://web.archive.org/web/20031214051427id_/" + PAGE_ORIGINAL
PAGE_SHA = "36e1600d1a6192d2613b64750676235fe42010c78b1ca24b43bc38121c9f9e50"
IMAGE_ROOT = "http://images.hangame.co.jp/_images/game/saj/"
IMAGE_ORIGINAL = IMAGE_ROOT + "charapicillust1.gif"
IMAGE_REQUESTED = "https://web.archive.org/web/20031214051427id_/" + IMAGE_ORIGINAL
IMAGE_FINAL = "https://web.archive.org/web/20060619160353id_/" + IMAGE_ORIGINAL
IMAGE_SHA = "9a3d42aca28d67a57d328d33fce57f22adfd0037f064885785c82f6482b1bb39"
UNNAMED_CLAUSE = "特に名前はありません。お好きな名前をつけてプレイしてね！"
RECORD_PATH = "research/recovered/STONEAGE-JP2003-CHARACTER-VISUAL-SOURCE-R1.json"
PHOTO = re.compile(re.escape(IMAGE_ROOT) + r"charapic(illust|com)([1-9][0-9]*)\.gif$")
LINK = re.compile(r"location\.href='(chara[234]\.asp)';$")


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.next_table = 0
        self.pictures = []
        self.visible = []
        self.content_links = []
        self.active_link = None
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ("script", "style"):
            self.hidden += 1
        if self.hidden:
            return
        if tag == "table":
            self.stack.append({"id": self.next_table, "row": -1, "col": -1})
            self.next_table += 1
        if tag == "tr" and self.stack:
            self.stack[-1].update(row=self.stack[-1]["row"] + 1, col=-1)
        if tag in ("td", "th") and self.stack:
            self.stack[-1]["col"] += 1
        if tag == "img" and PHOTO.fullmatch(d.get("src", "")):
            require(bool(self.stack), "Character image is outside a table")
            self.pictures.append({**self.stack[-1], **d})
        if tag == "font" and LINK.fullmatch(d.get("onclick", "")):
            self.active_link = {"target": LINK.fullmatch(d["onclick"])[1], "label": []}

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.hidden:
            self.hidden -= 1
        if self.hidden:
            return
        if tag == "table" and self.stack:
            self.stack.pop()
        if tag == "font" and self.active_link:
            self.content_links.append({"relative_target": self.active_link["target"],
                                       "label": "".join(self.active_link["label"])})
            self.active_link = None

    def handle_data(self, value):
        value = " ".join(value.split())
        if not self.hidden and value:
            self.visible.append(value)
            if self.active_link:
                self.active_link["label"].append(value)


def classify_layout(html):
    p = Page()
    p.feed(html)
    require(UNNAMED_CLAUSE in p.visible, "Explicit unnamed-character clause missing")
    require(len(p.pictures) == 24, "Not the qualified 24-image character grid")
    require(len({im["id"] for im in p.pictures}) == 1, "Mixed source tables")
    indexed = {}
    for picture in p.pictures:
        match = PHOTO.fullmatch(picture["src"])
        family, ordinal = match[1], int(match[2])
        key = family, ordinal
        require(key not in indexed, "Duplicate character picture reference")
        require(1 <= ordinal <= 12, "Unexpected web ordinal")
        expected_row = 2 * ((ordinal - 1) // 4) + (family == "com")
        expected_col = (ordinal - 1) % 4
        require((picture["row"], picture["col"]) == (expected_row, expected_col),
                "Same-number filenames are not in the qualified paired DOM cells")
        size = (65, 75) if family == "illust" else (75, 105)
        require((picture.get("width"), picture.get("height")) == tuple(map(str, size)),
                "Declared web image footprint changed")
        indexed[key] = picture
    require(p.content_links == [
        {"relative_target": "chara2.asp", "label": "ペット"},
        {"relative_target": "chara3.asp", "label": "呪術"},
        {"relative_target": "chara4.asp", "label": "ペット技術"},
    ], "Actual labelled operator navigation differs")
    return indexed, p.content_links


def inspect_image(image_raw, image_final):
    require(image_final == IMAGE_FINAL, "Wrong illustration host/path/capture")
    require(len(image_raw) == 6312 and hashlib.sha256(image_raw).hexdigest() == IMAGE_SHA,
            "Illustration byte pin mismatch")
    with Image.open(BytesIO(image_raw)) as im:
        require(im.format == "GIF" and im.size == (65, 75) and im.n_frames == 1,
                "Unexpected actual GIF structure")
        im.load()


def build(page_raw, page_final, image_raw, image_final):
    require(page_final == PAGE_FINAL, "Wrong official page/capture/host or replay mode")
    require(len(page_raw) == 16437 and hashlib.sha256(page_raw).hexdigest() == PAGE_SHA,
            "Page source byte pin mismatch")
    cells, links = classify_layout(page_raw.decode("cp932", errors="strict"))
    inspect_image(image_raw, image_final)
    characters = []
    for n in range(1, 13):
        illust, companion = cells["illust", n], cells["com", n]
        characters.append({
            "record_id": f"jp-hangame-web2003:character-position:{n:02d}",
            "collection": "characters", "entity_type": "OFFICIAL_UNNAMED_CHARACTER_WEB_POSITION",
            "version_profile": "JAPAN_HANGAME_OFFICIAL_WEB_2003",
            "source_refs": [{"source": PAGE_ORIGINAL, "sha256": PAGE_SHA,
                             "illustration_cell": [illust["row"], illust["col"]],
                             "companion_cell": [companion["row"], companion["col"]]}],
            "verification_status": "OPERATOR_PAGE_POSITION_NOT_GAME_ID",
            "rights_status": "RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED", "record_revision": 1,
            "web_ordinal": n, "canonical_character_name": None, "client_body_face_sprite_ids": None,
            "illustration": {"original_url": illust["src"], "declared_size": [65, 75], "pixels_acquired": n == 1},
            "companion_reference": {"original_url": companion["src"], "declared_size": [75, 105],
                                    "pixels_acquired": False, "contents_or_animation_status": "UNINSPECTED"},
        })
    return {
        "schema": "stoneage.jp2003.character_visual.source_contract.r1",
        "task": "JP2003-OFFICIAL-CHARACTER-VISUAL-SOURCE-01",
        "page": {"original_url": PAGE_ORIGINAL, "requested_url": PAGE_REQUESTED,
                 "final_url": page_final, "actual_capture": "20031214051427", "bytes": 16437,
                 "sha256": PAGE_SHA, "encoding": "CP932_STRICT",
                 "parent_qualified_report": "research/recovered/STONEAGE-OFFICIAL-VERSION-COVERAGE-MATERIAL-REVIEW-R5.json",
                 "first_party_operator": "HANGAME_JAPAN", "capture_is_publication_or_build_date": False},
        "identity": {"operator_explicitly_describes_no_fixed_names": True,
                     "player_naming_described": True,
                     "source_clause_sha256": hashlib.sha256(UNNAMED_CLAUSE.encode()).hexdigest(),
                     "named_identity_gate_adjustment": "USE_QUALIFIED_UNNAMED_WEB_POSITION_WITHOUT_INVENTING_NAMES",
                     "web_ordinal_is_game_identity": False},
        "grid": {"rows": 6, "columns": 4, "paired_web_positions": 12,
                 "illustration_references": 12, "companion_references": 12,
                 "pair_basis": "ADJACENT_TABLE_ROWS_AND_SAME_COLUMN_WITH_MATCHING_SOURCE_FILENAME_ORDINAL",
                 "illustrations_visually_inspected": 1, "other_image_references_unacquired": 23,
                 "complete_playable_character_census_proven": False},
        "characters": characters,
        "reviewed_image": {"original_url": IMAGE_ORIGINAL, "requested_url": IMAGE_REQUESTED,
                           "final_url": image_final, "actual_capture": "20060619160353", "bytes": 6312,
                           "sha256": IMAGE_SHA, "format": "GIF", "actual_size": [65, 75], "frames": 1,
                           "human_visual_review": "EXACT_HASH_IMAGE_VIEWED_WITH_VIEW_IMAGE",
                           "observations": ["HUMAN_FACE_ILLUSTRATION", "LIGHT_ORANGE_HAIR", "TOP_HAIR_TUFT", "SMILING_EXPRESSION"],
                           "named_character_identified": False, "proves_original_client_sprite": False,
                           "same_instant_or_same_bytes_as_2003_html_proven": False},
        "actual_labelled_navigation": [{"label": link["label"],
                                        "original_url": "http://www.hangame.co.jp/publish/sa/" + link["relative_target"],
                                        "kind": "STATIC_ONCLICK_LITERAL_NOT_EXECUTED", "target_read": False} for link in links],
        "boundaries": {"original_html_or_pixels_in_git": False, "forms_javascript_activex_or_executables_run": False,
                       "jss1999_tw10_or_174a_build_identity_proven": False,
                       "twelve_positions_equal_other_version_twelve_characters_proven": False,
                       "all_directions_colors_or_animations_recovered": False,
                       "stage_a_families": "7_PARTIAL_2_OPEN_UNCHANGED", "stage_b_and_wiki": "GATED", "r79": "PAUSED_NON_BLOCKING"},
    }


def acquire(url):
    for attempt in range(2):
        try:
            with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0 StoneAgeHistoricalEvidence"}), timeout=40) as r:
                return r.read(300001), r.url
        except HTTPError as exc:
            if attempt or exc.code not in (502, 503, 504):
                raise


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--page-input")
    p.add_argument("--image-input")
    p.add_argument("--output", required=True)
    args = p.parse_args()
    require(bool(args.page_input) == bool(args.image_input), "Provide both local initial source files or neither")
    page, page_final = (Path(args.page_input).read_bytes(), PAGE_FINAL) if args.page_input else acquire(PAGE_REQUESTED)
    image, image_final = (Path(args.image_input).read_bytes(), IMAGE_FINAL) if args.image_input else acquire(IMAGE_REQUESTED)
    obj = build(page, page_final, image, image_final)
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(payload, encoding="utf-8")
    print("PAGE_SHA256=" + PAGE_SHA)
    print("IMAGE_SHA256=" + IMAGE_SHA)
    print("DERIVED_SHA256=" + hashlib.sha256(payload.encode()).hexdigest())


if __name__ == "__main__":
    main()
