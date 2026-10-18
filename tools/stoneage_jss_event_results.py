"""Source-qualified first comedy result; reject cross-edition pet attribution.

Read two authenticated HTML sources and only their three named image references.
Keep recipient fingerprints, not a player roster; never infer a rare-pet species
from participant names, the template banner, a prize amount or another event.
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
import unicodedata
from urllib.parse import urljoin
import urllib.request
from PIL import Image
from tools.stoneage_jss_official_event_venue import ROOT, parse, require

PAGES = {
    "eventjsk": ("20010418085802", 5041, "8287f0bf401201f6931edd53758129e6bb447293d0c1211efc2413247814a541"),
    "eventj09": ("20010422015200", 2153, "230a804678c4fa21d3df9a574637a921309e25649dbe72e87e895726356724a9"),
}
IMAGES = ("sass0901.jpg", "sass0902.jpg", "sass0903.jpg")
PREVIOUS = "research/recovered/STONEAGE-JSS2001-OFFICIAL-EVENT-VENUE-R1.json"


def normalized(text):
    return " ".join(text.split())


class TableRows(HTMLParser):
    """Retain each row's own cells/links despite nested result tables."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows, self.row_stack, self.cell_stack = [], [], []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self.hidden += 1
        if self.hidden:
            return
        if tag == "tr":
            self.row_stack.append({"cells": [], "links": []})
        if tag in ("td", "th") and self.row_stack:
            cell = []
            self.row_stack[-1]["cells"].append(cell)
            self.cell_stack.append(cell)
        if tag == "br":
            for cell in self.cell_stack:
                cell.append(" ")
        if tag == "a" and attrs.get("href") and self.row_stack:
            self.row_stack[-1]["links"].append(urljoin(ROOT, attrs["href"]))

    def handle_data(self, data):
        if not self.hidden:
            for cell in self.cell_stack:
                cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.hidden:
            self.hidden -= 1
        elif not self.hidden:
            if tag in ("td", "th") and self.cell_stack:
                self.cell_stack.pop()
            if tag == "tr" and self.row_stack:
                row = self.row_stack.pop()
                self.rows.append({"cells": [normalized("".join(c)) for c in row["cells"]], "links": row["links"]})


def rows(document):
    result = TableRows()
    result.feed(document)
    result.close()
    return result.rows


def index_entries(document):
    entries = []
    for row in rows(document):
        links = [u for u in row["links"] if re.fullmatch(re.escape(ROOT) + r"eventj\d{2}\.html", u)]
        if links:
            require(len(links) == 1, "ambiguous event row links")
            title = normalized(" ".join(row["cells"]))
            for suffix in ("結果発表", "講座の様子", "式の様子"):
                if title.endswith(suffix):
                    title = title[:-len(suffix)].strip()
                    break
            entries.append({"title_as_written": title, "detail_url": links[0], "scope": "INDEX_ONLY_NOT_DETAIL_CONTENT"})
        else:
            title = next((c for c in row["cells"] if c), "")
            if title in ("はずれくじキャンペーン", "スクリーンショットコンテスト"):
                entries.append({"title_as_written": title, "detail_url": None, "scope": "INDEX_ONLY_MAGAZINE_EVENT_WITHOUT_DETAIL_LINK"})
    require(len(entries) == 16 and sum(x["detail_url"] is not None for x in entries) == 14, "official index coverage changed")
    require(len({x["detail_url"] for x in entries if x["detail_url"]}) == 14, "duplicate detail target")
    return entries


def select_comedy_result(entries):
    chosen = [x for x in entries if unicodedata.normalize("NFKC", x["title_as_written"]) == "第1回お笑いコンテスト"]
    require(len(chosen) == 1, "missing unique first comedy index title")
    require(chosen[0]["detail_url"] == ROOT + "eventj09.html", "comedy identity/path mismatch; do not substitute eventj07")
    return chosen[0]


def compare_event_profiles(a, b):
    for key, rejection in (("family", "REJECT_FAMILY_MISMATCH"), ("edition", "REJECT_EDITION_MISMATCH"), ("year", "REJECT_CONTEXT_MISMATCH"), ("month_day", "REJECT_CONTEXT_MISMATCH"), ("server", "REJECT_CONTEXT_MISMATCH")):
        if a.get(key) is not None and b.get(key) is not None and a[key] != b[key]:
            return rejection
    if any(a.get(k) is None or b.get(k) is None for k in ("family", "edition", "year", "month_day", "server")):
        return "OPEN_MISSING_IDENTITY_CONTEXT"
    return "MATCHING_METADATA_ONLY_NOT_SERVER_EXECUTION"


def result_contract(document, chosen):
    require(chosen["detail_url"] == ROOT + "eventj09.html", "wrong result resource")
    doc = parse(document)
    require("第1回お笑いコンテスト" in doc.text, "wrong event body; a generic banner is insufficient")
    require(all(t in doc.text for t in ("多数のご参加ありがとうございました", "無事に終了", "最優秀個人賞の意見が分かれたため急遽賞を追加", "第２回お笑いコンテストも予定")), "missing completion/additional-award/next-edition description")
    banners = re.findall(r'<font\b[^>]*size\s*=\s*["\x27]?5["\x27]?[^>]*>(.*?)</font>', document, re.I | re.S)
    require(len(banners) == 1 and parse(banners[0]).text == "ねるとん", "template banner changed; requalify identity")
    require(not doc.links, "active result links changed; do not submit feedback forms")
    categories = {"大賞": "GRAND_PRIZE", "アイデア賞": "IDEA_PRIZE", "最優秀個人賞": "BEST_INDIVIDUAL", "特別個人賞": "SPECIAL_INDIVIDUAL"}
    awards = []
    for row in rows(document):
        cells = row["cells"]
        if len(cells) == 3 and cells[0] in categories:
            match = re.match(r"^(\d+)stone", cells[1])
            require(match is not None and cells[2], "missing result prize or recipient")
            awards.append({"category": categories[cells[0]], "stone": int(match[1]), "extra_prize_description": "UNIDENTIFIED_UNRELEASED_RARE_PET" if "レアペット（未登場）" in cells[1] else None, "pet_species_or_id": None, "recipient_column_role": "PLAYER_GROUP_OR_CHARACTER_TEXT_NOT_PET_SPECIES", "recipient_normalized_sha256": hashlib.sha256(cells[2].encode()).hexdigest(), "recipient_characters": len(cells[2])})
    require([(a["category"], a["stone"]) for a in awards] == [("GRAND_PRIZE", 30000), ("IDEA_PRIZE", 20000), ("BEST_INDIVIDUAL", 10000), ("SPECIAL_INDIVIDUAL", 10000)], "first-event award table changed")
    require(awards[0]["extra_prize_description"] is not None and all(x["extra_prize_description"] is None for x in awards[1:]), "rare-pet column meaning changed")
    refs = [x for x in doc.images if x["original_url"].rsplit("/", 1)[-1] in IMAGES]
    require([x["original_url"].rsplit("/", 1)[-1] for x in refs] == list(IMAGES), "three result image references changed")
    return {"identity": {"family": "COMEDY_CONTEST", "edition": 1, "year": None, "month_day": None, "server": None}, "body_title": "第1回お笑いコンテスト", "template_banner": "ねるとん", "template_banner_mismatch_preserved": True, "identity_basis": "INDEX_ROW_AND_SPECIFIC_BODY_HEADING_AND_NEXT_EDITION_DESCRIPTION", "operator_reports_event_completed": True, "server_execution_or_reward_transaction_verified": False, "awards": awards, "special_individual_award_added_described": True, "reason_described": "JUDGES_DISAGREED_ON_BEST_INDIVIDUAL", "second_edition_described_as_planned": True, "original_pet_master_or_graphic_mapping_recovered": False, "recipient_names_are_not_pet_names": True}, refs


def qualify(raw, final, key):
    capture, size, digest = PAGES[key]
    require(final == f"https://web.archive.org/web/{capture}id_/" + ROOT + key + ".html", "result original/capture changed")
    require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, "result source bytes changed")
    text = raw.decode("shift_jis", errors="strict")
    return text, {"final_url": final, "actual_capture": capture, "bytes": size, "sha256": digest, "encoding": "shift_jis", "replacement_characters": 0, "normalized_visible_sha256": hashlib.sha256(parse(text).text.encode()).hexdigest()}


def image_metadata(raw, final, original):
    m = re.fullmatch(r"https://web\.archive\.org/web/(\d{14})id_/(http://www\.titan\.co\.jp/stoneage/image/[^/]+\.jpg)", final)
    require(m is not None and m[2] == original and original.rsplit("/", 1)[-1] in IMAGES, "unqualified result image resource")
    require("19990101000000" <= m[1] <= "20021231235959", "result image outside historical window")
    require(0 < len(raw) <= 1_000_000, "result image size limit")
    with Image.open(io.BytesIO(raw)) as im:
        im.verify()
    with Image.open(io.BytesIO(raw)) as im:
        require(im.format == "JPEG", "not a JPEG source")
        width, height = im.size
    return {"final_url": final, "actual_capture": m[1], "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "actual_width": width, "actual_height": height, "format": "JPEG", "pet_identity_proven": False}


def fetch(url):
    class Redirects(urllib.request.HTTPRedirectHandler):
        max_redirections = 4
        max_repeats = 1
    with urllib.request.build_opener(Redirects()).open(urllib.request.Request(url, headers={"User-Agent": "StoneAge historical content research"}), timeout=40) as response:
        require(response.status == 200, "source HTTP status")
        return response.read(1_000_001), response.url


def build(acquisitions, previous_raw, acquire, unavailable=()):
    texts, sources = {}, {}
    for key in PAGES:
        texts[key], sources[key] = qualify(*acquisitions[key], key)
    entries = index_entries(texts["eventjsk"])
    chosen = select_comedy_result(entries)
    facts, references = result_contract(texts["eventj09"], chosen)
    prior = json.loads(previous_raw)
    require(prior["announcements"]["comedy"]["research_key"] == "SECOND_COMEDY_CONTEST", "previous announcement source changed")
    announcement = prior["announcements"]["comedy"]
    title = unicodedata.normalize("NFKC", announcement["source_title"])
    match = re.fullmatch(r"第(\d+)回お笑いコンテスト", title)
    require(match is not None and int(match[1]) == 2, "previous source title/edition changed")
    target = {"family": "COMEDY_CONTEST", "edition": int(match[1]), "year": announcement["year"], "month_day": announcement["month_day"], "server": announcement["server_as_written"]}
    decision = compare_event_profiles(facts["identity"], target)
    require(decision == "REJECT_EDITION_MISMATCH", "cross-edition attribution was not rejected")
    unavailable = set(unavailable)
    require(unavailable <= {r["original_url"] for r in references}, "unknown unavailable image reference")
    def one(row):
        raw, final = acquire(row["original_url"])
        return {**row, **image_metadata(raw, final, row["original_url"])}
    with ThreadPoolExecutor(max_workers=3) as pool:
        images = list(pool.map(one, [r for r in references if r["original_url"] not in unavailable]))
    return {"schema": "stoneage.jss.official_event_results_pet_attribution.r1", "source_pages": sources, "results_index": {"entries": entries, "entry_count": len(entries), "linked_detail_count": 14, "only_followed_qualified_detail": chosen["detail_url"], "feedback_form_queried": False}, "first_comedy_result": facts, "second_comedy_attribution": {"previous_source": PREVIOUS, "previous_sha256": hashlib.sha256(previous_raw).hexdigest(), "target_identity": target, "decision": decision, "second_event_completed_or_pet_identity_proven": False}, "images": images, "qualified_image_count": len(images), "unqualified_image_references": [{**r, "status": "UNOBTAINED_IN_BOUNDED_SOURCE_ATTEMPTS", "source_absence_established": False, "actual_dimensions": None, "visual_contents_unknown": True} for r in references if r["original_url"] in unavailable], "boundaries": {"qualified_html_pages": 2, "other_event_result_bodies_exhaustively_read": False, "all_event_years_or_server_details_recovered": False, "original_server_or_npc_quest_executed": False, "jss1999_or_tw10_same_build_proven": False, "original_html_or_pixels_retained_in_git": False, "stage_a_family_status_changed": False, "stage_b_production": "GATED", "r79": "PAUSED_NON_BLOCKING"}}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input-dir", type=Path)
    p.add_argument("--images", type=Path)
    p.add_argument("--source-index", type=Path)
    p.add_argument("--reference", type=Path)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    acquisitions = {}
    for key, (capture, _, _) in PAGES.items():
        url = f"https://web.archive.org/web/{capture}id_/" + ROOT + key + ".html"
        acquisitions[key] = ((args.input_dir / ("stoneage-jss-" + key + ".raw")).read_bytes(), url) if args.input_dir else fetch(url)
    if args.images:
        lookup = {r["original_url"]: r for r in json.loads(args.source_index.read_text())}
        unavailable = [u for u, r in lookup.items() if "error" in r or not r.get("final_url")]
        def acquire(original):
            return (args.images / original.rsplit("/", 1)[-1]).read_bytes(), lookup[original]["final_url"]
    else:
        reference = json.loads(args.reference.read_text()) if args.reference else {}
        lookup = {r["original_url"]: r["final_url"] for r in reference.get("images", [])}
        unavailable = [r["original_url"] for r in reference.get("unqualified_image_references", [])]
        def acquire(original):
            return fetch(lookup.get(original, "https://web.archive.org/web/20010422015200id_/" + original))
    result = build(acquisitions, Path(PREVIOUS).read_bytes(), acquire, unavailable)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"html_sources": 2, "index_entries": 16, "result_awards": 4, "qualified_images": len(result["images"]), "second_event_pet_join": result["second_comedy_attribution"]["decision"]}))


if __name__ == "__main__":
    main()
