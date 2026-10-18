"""Bounded first-party JSS social announcements and four-village venue access.

Three named HTML sources, six directly embedded JPEG references; no form
submission, recursive crawl, original server execution or proprietary assets in Git.
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

ROOT = "http://www.titan.co.jp/stoneage/"
PAGES = {
    "event": ("20010417155224", 1587, "f11aa3a19be0dc307ec4580b0c8efa919c6dcaca3a1cac988656bd32ff376fd1"),
    "eventjss": ("20010418090522", 4166, "51c237c961002d862fcba2a4ea3a10aa67afdf9c87d1e523818cc2db3c7dea93"),
    "eventmaz": ("20010418085855", 2652, "2a52793ecff532885090d3336bea2cc00c6ed5ecc518f285dc41b47a1b9ec4bf"),
}
IMAGE_NAMES = ("mari01.jpg", "karu01.jpg", "samu01.jpg", "chat01.jpg", "jyajya01.jpg", "chat02.jpg")


def require(ok, message):
    if not ok:
        raise ValueError(message)


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.links, self.images, self.commented_links = [], [], [], []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self.hidden += 1
        if self.hidden:
            return
        if tag in ("br", "p", "div", "tr", "td", "dd"):
            self.parts.append(" ")
        if tag == "a" and attrs.get("href"):
            self.links.append(urljoin(ROOT, attrs["href"]))
        if tag == "img" and attrs.get("src"):
            self.images.append({"original_url": urljoin(ROOT, attrs["src"]),
                                "html_width": attrs.get("width"), "html_height": attrs.get("height")})

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.hidden:
            self.hidden -= 1
        elif tag in ("p", "div", "tr", "td", "dd") and not self.hidden:
            self.parts.append(" ")

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)

    def handle_comment(self, data):
        for href in re.findall(r'\bhref\s*=\s*["\x27]([^"\x27]+)', data, re.I):
            self.commented_links.append(urljoin(ROOT, href))

    @property
    def text(self):
        return " ".join("".join(self.parts).split())


def parse(document):
    result = Document()
    result.feed(document)
    result.close()
    return result


def mentions(text, *tokens):
    require(all(t in text for t in tokens), "missing official business assertion")


def number(text, pattern):
    match = re.search(pattern, text)
    require(match is not None, "missing official numeric assertion")
    return int(match.group(1))


def event_contract(document):
    doc = parse(document)
    title1, title2 = "第２回お笑いコンテスト", "第２回ねるとん"
    require(doc.text.count(title1) == 1 and doc.text.count(title2) == 1, "two named announcements changed")
    first, second = doc.text.split(title1, 1)[1].split(title2, 1)
    mentions(first, "11月17日(金)", "23:30", "太陽サーバー", "マンモスホール", "11月15日(月)AM9:00", "23:00まで", "事前エントリー", "抽選", "レアペット（未登場）")
    mentions(second, "12月22日(金)", "22:00", "月サーバー", "マンモスホール", "控え室", "12月18日(月)AM9:00", "22:45まで", "21:45", "見学はOK", "事前エントリー", "抽選", "名刺をひとつ", "一時的な変更", "24:00", "自己紹介", "質問コーナー", "フリートーク", "告白タイム", "ジャンケン", "性別が違う", "キャラクターグラフィック")
    require(re.search(r"(?:19|20)\d{2}[年/-]", doc.text) is None, "event now states an explicit year; requalify chronology")
    minutes = number(first, r"持ち時間は(\d+)分")
    minimum = number(first, r"(\d+)人から最大")
    maximum = number(first, r"人から最大(\d+)人")
    planned = number(second, r"参加者は、(\d+)名の予定")
    awards = [number(first, rf"{label}\s+(\d+)stone") for label in ("大賞", "アイデア賞", "最優秀個人賞")]
    require((minutes, minimum, maximum, planned, awards) == (5, 1, 5, 10, [30000, 20000, 10000]), "official announcement quantities changed")
    require(not doc.links, "announcement acquired active links; requalify registration status")
    expected = ["http://www.titan.co.jp/cgi-bin/mail/saevent6.html", "http://www.titan.co.jp/cgi-bin/mail/saevent5.html"]
    require(doc.commented_links == expected, "commented registration link evidence changed")
    return {
        "kind": "OFFICIAL_SOCIAL_EVENT_ANNOUNCEMENTS_NOT_NPC_QUEST_SCRIPTS",
        "comedy": {"research_key": "SECOND_COMEDY_CONTEST", "source_title": title1, "month_day": "11-17", "year": None, "weekday_as_written": "金", "start": "23:30", "server_as_written": "太陽", "venue_as_written": "マンモスホール", "meeting_room": "VENUE_WAITING_ROOM", "gathering": "23:00", "entry_deadline_month_day": "11-15", "entry_deadline_weekday_as_written": "月", "entry_deadline_time": "AM9:00", "group_size_min": minimum, "group_size_max": maximum, "performance_minutes": minutes, "prizes_as_announced": {"grand_prize_stone": awards[0], "grand_prize_extra": "UNIDENTIFIED_UNRELEASED_RARE_PET", "idea_prize_stone": awards[1], "individual_prize_stone": awards[2]}, "rare_pet_species_or_id": None, "participation_prize_identity": None, "entry_required": True, "oversubscription_lottery_described": True},
        "matchmaking": {"research_key": "SECOND_MATCHMAKING_EVENT", "source_title": title2, "month_day": "12-22", "year": None, "weekday_as_written": "金", "start": "22:00", "planned_end": "24:00", "server_as_written": "月", "venue_as_written": "マンモスホール", "planned_participants": planned, "planned_count_is_server_capacity": False, "spectators_allowed_described": True, "gathering_callout": "22:45", "gathering_timetable": "21:45", "gathering_conflict_preserved": True, "entry_deadline_month_day": "12-18", "entry_deadline_weekday_as_written": "月", "entry_deadline_time": "AM9:00", "stages": ["INTRODUCTIONS", "QUESTIONS", "FREE_TALK", "CONFESSIONS"], "spectator_rock_paper_scissors_during_free_talk": True, "reserve_one_contact_card_slot_described": True, "temporary_character_graphic_change_described_for_gender_mismatch": True, "general_player_graphic_editor_proven": False, "entry_required": True, "oversubscription_lottery_described": True},
        "registration": {"active_links_in_captured_body": [], "commented_form_candidate_urls": expected, "form_endpoint_queried_or_submitted": False},
        "event_year_inferred_from_index_or_capture": False,
        "events_actually_held_or_prizes_actually_awarded_proven": False,
    }


def venue_contract(document):
    doc = parse(document)
    text = doc.text
    mentions(text, "チャットルーム案内所", "チケット販売員", "チケットをもらって", "案内係", "北側", "右端", "マンモスホール", "右から二番目", "結婚式場")
    villages = (("マリナス", 51, 72, "トーテムポール南東", "TOTEM_SOUTHEAST"), ("カルターナ", 81, 49, "トーテムポール北東", "TOTEM_NORTHEAST"), ("サムギル", 111, 38, "村長宅北東スグ", "CHIEF_HOUSE_NORTHEAST_NEARBY"), ("ジャジャ", 85, 73, "村長宅南西スグ", "CHIEF_HOUSE_SOUTHWEST_NEARBY"))
    locations = []
    for name, east, south, wording, landmark in villages:
        match = re.search(re.escape(name) + r"\s*東(\d+)\s*南(\d+)\s*" + re.escape(wording), text)
        require(match is not None and (int(match[1]), int(match[2])) == (east, south), "official village entrance coordinates changed")
        locations.append({"village_as_written": name, "coordinate_labels": {"east": int(match[1]), "south": int(match[2])}, "nearby_landmark_description": landmark, "server_floor_id": None, "npc_id": None, "tw10_or_recovered25_map_join_proven": False})
    images = [r for r in doc.images if r["original_url"].rsplit("/", 1)[-1] in IMAGE_NAMES]
    require([r["original_url"].rsplit("/", 1)[-1] for r in images] == list(IMAGE_NAMES), "finite venue image reference set changed")
    return {"village_entrances": locations, "access_steps_described": ["ENTER_CHATROOM_INFORMATION_OFFICE", "TALK_TO_TICKET_SELLER_AND_RECEIVE_TICKET", "TALK_TO_GUIDE", "ENTER_CHATROOM"], "unnamed_npc_roles": ["TICKET_SELLER", "GUIDE"], "northern_corridor_destinations": {"RIGHTMOST_ENTRANCE": "MAMMOTH_HALL", "SECOND_FROM_RIGHT_ENTRANCE": "WEDDING_VENUE"}, "ticket_item_id": None, "ticket_price": None, "npc_script_predicates_and_transaction": None, "field_map_dat_or_collision_payload": None, "route_execution_proven": False}, images


def qualify(raw, final_url, key):
    capture, size, digest = PAGES[key]
    expected = f"https://web.archive.org/web/{capture}id_/" + ROOT + key + ".html"
    require(final_url == expected, "official page original/capture changed")
    require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, "official source bytes changed")
    text = raw.decode("shift_jis", errors="strict")
    return text, {"final_url": final_url, "actual_capture": capture, "bytes": size, "sha256": digest, "encoding": "shift_jis", "replacement_characters": 0, "normalized_visible_sha256": hashlib.sha256(parse(text).text.encode()).hexdigest()}


def image_metadata(raw, final_url, original):
    m = re.fullmatch(r"https://web\.archive\.org/web/(\d{14})id_/(http://www\.titan\.co\.jp/stoneage/image/[^/]+\.jpg)", final_url)
    require(m is not None and m[2] == original and original.rsplit("/", 1)[-1] in IMAGE_NAMES, "unqualified venue image original")
    require("19990101000000" <= m[1] <= "20021231235959", "venue image outside historical window")
    require(0 < len(raw) <= 1_000_000, "venue image size limit")
    with Image.open(io.BytesIO(raw)) as im:
        im.verify()
    with Image.open(io.BytesIO(raw)) as im:
        require(im.format == "JPEG", "not original JPEG format")
        width, height = im.size
    return {"final_url": final_url, "actual_capture": m[1], "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "actual_width": width, "actual_height": height, "format": "JPEG", "same_moment_as_html_proven": False, "same_build_as_tw10_proven": False}


def fetch(url):
    class FiniteRedirects(urllib.request.HTTPRedirectHandler):
        max_redirections = 4
        max_repeats = 1
    opener = urllib.request.build_opener(FiniteRedirects())
    with opener.open(urllib.request.Request(url, headers={"User-Agent": "StoneAge historical content research"}), timeout=40) as response:
        require(response.status == 200, "source HTTP status")
        return response.read(1_000_001), response.url


def build(acquisitions, acquire_image, unavailable=()):
    texts, sources = {}, {}
    for key in PAGES:
        texts[key], sources[key] = qualify(*acquisitions[key], key)
    index = parse(texts["event"])
    expected = [ROOT + p + ".html" for p in ("eventjss", "eventjsk", "eventusr", "eventmaz")]
    require(index.links == expected, "official index link provenance changed")
    mentions(index.text, "STONEAGE", "2000/10/14", "2000/09/28", "2000/10/02")
    venue, references = venue_contract(texts["eventmaz"])
    unavailable = set(unavailable)
    require(unavailable <= {r["original_url"] for r in references}, "unknown unqualified image reference")
    def image_row(row):
        raw, final = acquire_image(row["original_url"])
        return {**row, **image_metadata(raw, final, row["original_url"])}
    with ThreadPoolExecutor(max_workers=3) as pool:
        images = list(pool.map(image_row, [r for r in references if r["original_url"] not in unavailable]))
    return {"schema": "stoneage.jss2001.official_event_venue.r1", "source_pages": sources,
            "index": {"active_page_links": expected, "labelled_update_dates": {"official_upcoming": "2000-10-14", "official_results": "2000-09-28", "user_sponsorship": "2000-10-02"}, "index_update_dates_certify_event_year_or_occurrence": False, "results_and_user_sponsorship_pages_followed": False},
            "announcements": event_contract(texts["eventjss"]), "venue_access": venue,
            "image_reference_count": len(references), "qualified_image_count": len(images), "images": images,
            "unqualified_image_references": [{**r, "source_absence_established": False} for r in references if r["original_url"] in unavailable],
            "boundaries": {"first_party_jss_announcements_and_venue_only": True, "named_npc_quest_script_recovered": False, "actual_event_execution_proven": False, "original_server_or_form_executed": False, "original_html_or_image_pixels_retained_in_git": False, "jss1999_or_tw10_same_build_proven": False, "stage_a_family_status_changed": False, "stage_b_production": "GATED", "r79": "PAUSED_NON_BLOCKING"}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--images", type=Path)
    parser.add_argument("--source-index", type=Path)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    acquisitions = {}
    for key, (capture, _, _) in PAGES.items():
        url = f"https://web.archive.org/web/{capture}id_/" + ROOT + key + ".html"
        acquisitions[key] = ((args.input_dir / ("stoneage-jss-" + key + ".raw")).read_bytes(), url) if args.input_dir else fetch(url)
    if args.images:
        entries = json.loads(args.source_index.read_text())
        lookup = {r["original_url"]: r for r in entries}
        unavailable = [r["original_url"] for r in entries if "error" in r]
        def acquire(original):
            return (args.images / original.rsplit("/", 1)[-1]).read_bytes(), lookup[original]["final_url"]
    else:
        reference = json.loads(args.reference.read_text()) if args.reference else {}
        lookup = {r["original_url"]: r["final_url"] for r in reference.get("images", [])}
        unavailable = [r["original_url"] for r in reference.get("unqualified_image_references", [])]
        def acquire(original):
            return fetch(lookup.get(original, "https://web.archive.org/web/20010418085855id_/" + original))
    result = build(acquisitions, acquire, unavailable)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"source_pages": 3, "announcements": 2, "village_entrances": 4, "qualified_images": result["qualified_image_count"], "npc_quest_script_recovered": False}))


if __name__ == "__main__":
    main()
