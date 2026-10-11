"""Strict chronology, historical claim and binary-provenance boundary gate."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

MANIFEST = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-TW80-TW85-PRESS-CHRONOLOGY-R1.json"

EVENTS = (
    ("TW80_LAUNCH", "2005-06-08", "TW_8_0", "PRESS_RELEASE_REPORT"),
    ("TW80_PLAYER_PET", "2005-07-07", "TW_8_0", "PERIOD_PLAYER_REPORTED_MECHANICS"),
    ("TW80_SEPT_MARKETING", "2005-09-08", "TW_8_0", "PRESS_INDEX_ADDITIONAL_PET_GEAR_PROMO"),
    ("TW85_INSTALLER_NAME_TOKEN", "2006-06-16", "TW_8_5", "FILENAME_DATE_STRING_ONLY"),
    ("TW85_OPEN_TEST_ANNOUNCEMENT", "2006-06-21", "TW_8_5", "OPERATOR_SCHEDULE_PUBLIC_TEST"),
    ("TW85_CANG_LONG_ANNOUNCED", "2006-07-05", "TW_8_5", "OPERATOR_SCHEDULE_FIRST_SERVER"),
    ("TW85_ALL_SERVER_ANNOUNCED", "2006-07-12", "TW_8_5", "OPERATOR_SCHEDULE_ALL_SERVER"),
    ("TW85_SIX_PART_MIRROR", "2012-04-14", "TW_8_5", "COMMUNITY_ARCHIVE_METADATA"),
)
SOURCES = {
    "TW80_LAUNCH": "https://gnn.gamer.com.tw/detail.php?sn=20167",
    "TW80_PLAYER_PET": "https://www.gamez.com.tw/t/8-0/170704",
    "TW80_SEPT_MARKETING": "https://acg.gamer.com.tw/search.php?c1=976&c2=3&machine=1%2C0&s=2&type=1",
    "TW85_INSTALLER_NAME_TOKEN": "https://bbs.comefromchina.com/threads/449920/",
    "TW85_OPEN_TEST_ANNOUNCEMENT": "https://gnn.gamer.com.tw/detail.php?sn=23856",
    "TW85_CANG_LONG_ANNOUNCED": "https://gnn.gamer.com.tw/detail.php?sn=23856",
    "TW85_ALL_SERVER_ANNOUNCED": "https://gnn.gamer.com.tw/detail.php?sn=23856",
    "TW85_SIX_PART_MIRROR": "https://www.lab.welovesa.com/viewthread.php?action=printable&tid=1654",
}
FLAGS = {
    "tw80_pet_reported_as_release_feature": True,
    "pet_system_first_introduced_september_2005": False,
    "september_new_gear_items_press_index_reported": True,
    "filename_20060616_is_verified_release_date": False,
    "june21_2006_is_all_server_formal_85_launch": False,
    "july05_85_server_rollout_observed_verified": False,
    "july12_85_server_rollout_observed_verified": False,
    "wayi85_community_mirror_operator_binary_verified": False,
}

def validate(data):
    if data.get("schema") != "stoneage_tw80_tw85_press_chronology_r1":
        raise ValueError("Chronology schema mismatch")
    events = data.get("events")
    if not isinstance(events, list) or len(events) != len(EVENTS):
        raise ValueError("Event count not accepted")
    for got, (ident, when, family, stage) in zip(events, EVENTS):
        if tuple(got.get(k) for k in ("id","date","family","stage")) != (ident, when, family, stage):
            raise ValueError("Source-specific date, release family or evidence stage changed")
        if got.get("source") != SOURCES[ident] or not got.get("note"):
            raise ValueError("Source citation/evidence note changed or absent")
        if got.get("original_executable_bytes_verified") is not False:
            raise ValueError("Unverified executable promoted")
        date.fromisoformat(got["date"])
    if data.get("assertions") != FLAGS:
        raise ValueError("Historical press launch, marketing or actual-rollout classification promoted")
    if any(data.get(k) is not None for k in ("original_tw80_client_sha256","original_tw85_installer_sha256")):
        raise ValueError("Unobserved official hash invented")
    if any(data.get(k) is not False for k in ("original_enabled_pair_runtime_proven","original_packet127_observed","early_1999_or_tw10_pet_proven")):
        raise ValueError("Original PET binary/first-build inference forbidden")
    if data.get("pressure") != {"total":2486,"bounded_closed":2465,"open":18,"historical_ub":3}:
        raise ValueError("Unaccepted historical pressure promotion")
    return "TW80_TW85_DATED_CLAIMS_BOUNDARY_PASS"

def main():
    print(validate(json.loads(MANIFEST.read_text(encoding="utf-8"))))

if __name__ == "__main__":
    main()
