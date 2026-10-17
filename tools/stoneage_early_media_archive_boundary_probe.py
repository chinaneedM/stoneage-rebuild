"""Bounded early 17173 media URL replay; only derived metadata is retained.

A migrated article's displayed publication date is NOT an archived capture date.
Never infer original TW1.0 gameplay or full media site from navigation.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

LIMIT = 1_000_000
WINDOW_START, WINDOW_END = "19990101000000", "20021231235959"
TARGETS = (
    {"id":"jingyan_june2001", "url":"http://stoneage.17173.com/jingyan/jingyan.shtml",
     "requested":"20010614000000", "lead":"EXACT_LEGACY_CATEGORY_URL_IN_MIGRATED_2001_DATE_LABELED_ARTICLES"},
    {"id":"jingyan_end2002", "url":"http://stoneage.17173.com/jingyan/jingyan.shtml",
     "requested":"20021231000000", "lead":"SAME_EXACT_URL_SECOND_BOUNDED_WINDOW"},
    {"id":"pet_index_late_navigation_lead", "url":"http://stoneage.17173.com/chongwu/pet.htm",
     "requested":"20011231000000", "lead":"LATE_MIGRATED_NAV_LINK_NOT_2001_ATTESTATION"},
)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def origin_key(url):
    p = urllib.parse.urlsplit(url)
    if p.scheme not in ("http", "https") or not p.hostname or p.username or p.password:
        raise ValueError("invalid source URL")
    return p.hostname.lower(), p.path or "/", p.query

def archive_parts(url):
    match = re.fullmatch(r"https?://web\.archive\.org/web/(\d{14})(?:id_)?/(https?://.+)", url)
    if match is None:
        raise ValueError("no independently observed archive capture URL")
    return match.group(1), match.group(2)

class Anchors(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() not in ("a", "frame", "iframe", "area"):
            return
        a = dict(attrs)
        href = a.get("href") or a.get("src")
        if href:
            self.links.append(href.strip())

def qualify(raw, final_url, original):
    timestamp, observed_original = archive_parts(final_url)
    if origin_key(observed_original) != origin_key(original):
        raise ValueError("archive target URL changed")
    meta = {
        "actual_capture": timestamp, "archive_url": final_url,
        "raw_bytes": len(raw), "raw_sha256": digest(raw),
        "original_url_verified": True,
    }
    if not WINDOW_START <= timestamp <= WINDOW_END:
        return dict(meta, status="OUT_OF_WINDOW_NOT_EARLY_EVIDENCE",
                    qualified_link_count=0, sample_link_targets=[])
    if not (0 < len(raw) <= LIMIT):
        raise ValueError("archive body unavailable or too large")
    doc = raw.decode("gb18030", errors="replace")
    if not re.search(r"<(?:html|body|frameset)\b", doc, re.I):
        return dict(meta, status="EARLY_RESPONSE_NOT_HTML_NOT_QUALIFIED",
                    qualified_link_count=0, sample_link_targets=[])
    # A historical snapshot that is only an image/redirect shell is not enough.
    if not re.search(r"stone\s*age|stoneage|石器", doc, re.I):
        return dict(meta, status="EARLY_HTML_BRAND_NOT_ESTABLISHED",
                    qualified_link_count=0, sample_link_targets=[])
    parser = Anchors()
    parser.feed(doc)
    links = []
    for href in parser.links:
        if href.lower().startswith(("javascript:", "mailto:", "data:")):
            continue
        target = urllib.parse.urljoin(observed_original, href)
        parsed = urllib.parse.urlsplit(target)
        if parsed.scheme in ("http", "https") and not parsed.username and not parsed.password:
            links.append(target)
    return dict(meta, status="EARLY_CAPTURE_LINK_METADATA_QUALIFIED",
                qualified_link_count=len(links), sample_link_targets=links[:12],
                original_site_layout_verified=False,
                linked_article_date_verified=False,
                original_tw10_server_gameplay_verified=False)

def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "StoneAgeSourceBoundaryResearch/1.0",
        "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=18) as response:
        if response.status != 200:
            raise ValueError("HTTP non-200")
        raw = response.read(LIMIT + 1)
        if len(raw) > LIMIT:
            raise ValueError("response exceeds byte budget")
        return raw, response.url

def inspect(target):
    original, requested = target["url"], target["requested"]
    out = {"target_id": target["id"], "requested_original": original,
           "requested_capture_near": requested, "lead_basis": target["lead"],
           "availability_closest": None, "availability_error": None}
    availability = "https://archive.org/wayback/available?" + urllib.parse.urlencode(
        {"url":original, "timestamp":requested})
    try:
        body, final_url = get(availability)
        parsed = json.loads(body)
        candidate = parsed.get("archived_snapshots", {}).get("closest")
        out["availability_response"] = {"bytes":len(body), "sha256":digest(body),
                                        "url":final_url}
        if candidate:
            out["availability_closest"] = {"timestamp":candidate.get("timestamp"),
                                           "url":candidate.get("url"),
                                           "status":str(candidate.get("status"))}
    except Exception as exc:
        out["availability_error"] = type(exc).__name__ + ":" + str(exc)[:140]
    # Direct replay is separately attempted even if the availability API is empty.
    replay = "https://web.archive.org/web/" + requested + "id_/" + original
    out["replay_request"] = replay
    try:
        raw, final_url = get(replay)
        out.update(qualify(raw, final_url, original))
    except Exception as exc:
        out["status"] = "REPLAY_UNQUALIFIED_NOT_GLOBAL_ABSENCE"
        out["replay_error"] = type(exc).__name__ + ":" + str(exc)[:140]
    out["full_early_media_site_recovered"] = False
    out["same_build_pet_or_npc_identity_verified"] = False
    return out

def build(targets=TARGETS):
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(inspect, targets))
    qualified = sum(x["status"] == "EARLY_CAPTURE_LINK_METADATA_QUALIFIED" for x in results)
    return {"schema":"stoneage.early_media_archive_snapshot_boundary.r1",
            "targets":results,
            "counts":{"requested_targets":len(results), "qualified_early_link_pages":qualified},
            "source_1999_2002_globally_absent":False,
            "full_17173_early_site_restored":False,
            "tw10_original_pet_species_verified":False,
            "stage_b_game_or_website_started":False,
            "next_if_zero":"OPEN_EVIDENCE_LIMITED_THEN_22_DOMAIN_COVERAGE_REVIEW",
            "raw_html_or_images_archived_in_git":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    report=build()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"counts":report["counts"],
                      "statuses":{r["target_id"]:{"status":r["status"],
                       "actual_capture":r.get("actual_capture"),
                       "error":r.get("replay_error")} for r in report["targets"]}},
                     ensure_ascii=False))

if __name__=="__main__":
    main()
