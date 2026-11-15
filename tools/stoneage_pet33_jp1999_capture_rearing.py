"""PET33: exact 1999-05-18 contemporary preview of intended pet capture/rearing.

This source describes an announced feature BEFORE Japanese initial release.
It must never be promoted to a live deployed pet species or a runtime test.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://internet.watch.impress.co.jp/www/digest/backno/9905/18.htm"
SHA256 = "f1403f84cfd2bf7fbc356db65c2e015e87c96fa2c3316812605e58571d33218c"
BYTES = 23747
ENTRY_SHA256 = "f3840b1455c009cef20402043e3e0a5ef85287a9b2c320a5293fe2fe1ebfb6ef"
ENTRY_LENGTH = 118


class TextNodes(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []

    def handle_data(self, s):
        self.text.append(s)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def feature_entry(document):
    require("1999年5月18日" in document and "23:38" in document, "wrong original page date")
    p = TextNodes()
    p.feed(document)
    p.close()
    nodes = [" ".join(s.split()) for s in p.text]
    matches = [s for s in nodes if "日本システムサプライ" in s and "恐竜を捕獲" in s]
    require(len(matches) == 1, "wrong or ambiguous news item")
    passage = matches[0]
    require(len(passage) == ENTRY_LENGTH
            and hashlib.sha256(passage.encode("utf-8")).hexdigest() == ENTRY_SHA256,
            "1999 feature paragraph changed")
    require(all(token in passage for token in (
        "STONE AGE", "ゲーマーズドリーム", "今秋発売予定",
        "恐竜を捕獲・飼育", "Windows 95/98対応", "価格等未定")),
        "period feature/equipment/release status changed")
    return passage


def build(raw, final_url):
    require(final_url == URL, "source URL redirected to unverified location")
    require(len(raw) == BYTES and hashlib.sha256(raw).hexdigest() == SHA256,
            "primary period page changed")
    doc = raw.decode("utf-8", errors="strict")
    feature_entry(doc)
    return {
        "schema": "stoneage.pet33.jp1999_0518_prelaunch_pet_announced_source.r1",
        "source": {
            "url": URL,
            "page_date_as_written": "1999-05-18",
            "last_updated_time_as_written": "23:38",
            "bytes": BYTES,
            "sha256": SHA256,
            "replayed_encoding": "utf-8",
            "source_class": "CONTEMPORANEOUS_PERIOD_EDITORIAL_NOTICE",
            "publisher_of_news": "INTERNET_WATCH",
            "game_publisher_as_written": "JAPAN_SYSTEM_SUPPLY",
            "game_product_as_written": "STONE_AGE",
            "linked_official_site_base": "http://www.titan.co.jp/",
            "extraction_scope": "ONE_IDENTIFIED_PRODUCT_NEWS_ITEM"
        },
        "bounded_record": {
            "normalized_entry_characters": ENTRY_LENGTH,
            "normalized_entry_sha256": ENTRY_SHA256,
            "source_attestation_date_not_pet_release_date": "1999-05-18",
            "operator_region_context": "JP",
            "product_line_context": "STONEAGE_CLASSIC_PC_JSS",
            "service_platform_as_written": "GAMERS_DREAM",
            "pet_feature_capture": "PRE_LAUNCH_ANNOUNCED_ONLY",
            "pet_feature_rearing": "PRE_LAUNCH_ANNOUNCED_ONLY",
            "sale_or_launch_timing": "AUTUMN_1999_PLANNED_NOT_VERIFIED_SHIPPED",
            "windows_platforms_as_written": ["Windows 95", "Windows 98"],
            "official_game_live_feature_execution_proven": False,
            "1999_official_named_pet_species_in_this_entry": [],
            "named_pet_released_or_obtainable_proven": False,
            "pet_stat_growth_skills_identified": False,
            "original_1999_client_binary_or_server_deployment_proven": False,
            "source_year_does_not_prove_all_regions_or_later_builds": True
        },
        "chronology": {"prior_1999_jss_operator_changelog_preserved": "PET31_PET32",
                       "does_not_supersede_live_pet_release_audit": True,
                       "1999_year_review_status": "NOT_YEAR_AUDITED",
                       "active_module": "PET",
                       "current_frontier_year": 1999},
        "new_official_released_named_pet_species": [],
        "raw_source_html_published": False,
        "proprietary_game_assets_published": False
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.input is None:
        with urlopen(Request(URL, headers={"User-Agent": "Mozilla/5.0 (compatible; StoneAgeHistoricalEvidence/1.0)"}), timeout=50) as f:
            raw, final_url = f.read(), f.url
    else:
        raw, final_url = args.input.read_bytes(), URL
    report = build(raw, final_url)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "url": URL, "bytes": BYTES, "sha256": SHA256,
        "feature": "capture_and_rearing_as_prelaunch_design",
        "named_pet_release_proven": False, "year": 1999,
    }))


if __name__ == "__main__":
    main()
