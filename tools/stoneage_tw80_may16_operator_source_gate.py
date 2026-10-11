"""Strict provenance for reported 2005-05-16 Taiwan Waei 8.0 test and dated official URL.

Does not attest original test client binaries, native gameplay or Web Archive captures.
"""
from __future__ import annotations
import json
from datetime import date
from pathlib import Path

LEDGER=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-TW80-MAY16-OPERATOR-URL-SOURCE-R1.json"
URL="http://www.wayi.com.tw/stoneage/actives/940329/page_3.html"
SOURCES=(
("TW80_TEST_20050516_FORUM_PERIOD_REPORT","2005-05-16","2005-05-16","https://bbs.8591.com.tw/index.php?action=detail&articleId=33&module=article","PERIOD_FORUM_CUSTODY_OF_DATED_PRESS_REPORT"),
("TW80_TEST_20050518_GAMES_IDV","2005-05-16","2005-05-18","https://www.games.idv.tw/news.php?mode=view&nid=326","CONTEMPORANEOUS_PRESS_WITH_EXPLICIT_OPERATOR_REFERENCE_URL"),
("TW80_TEST_20050518_17173","2005-05-16","2005-05-18","https://news.17173.com/content/2005-5-18/n358_274376.html","CONTEMPORANEOUS_MAINLAND_PRESS_ABOUT_TAIWAN_TEST_CAMPAIGN"),
("TW80_OPERATOR_ORIGINAL_URL_REFERENCE","2005-05-18","2005-05-18","https://www.games.idv.tw/news.php?mode=view&nid=326","HISTORICAL_OPERATOR_URL_QUOTED_BY_PRESS")
)
FLAGS={
"test_server_announced_as_open_on_may16":True,
"period_may16_to_may18_gm_activity_reported":True,
"original_may16_test_client_bytes_verified":False,
"authenticated_test_server_native_pet_execution_verified":False,
"web_current_operator_page_is_2005_original":False,
"quoted_wayi_url_is_downloadable_2005_installer":False,
"may16_reward_announced_proves_paid_out_to_users":False,
"may16_publisher_link_proves_8_0_packet127":False,
"prelaunch_taiwan_feature_can_be_promoted_to_jss1999_or_tw10":False,
"original_publisher_installer_sha256_verified":False,
"wayback_capture_already_authenticated":False,
}

def validate(d:dict)->str:
    if d.get("schema")!="stoneage-tw80-may16-operator-source-ledger-r1" or d.get("recorded_on")!="2026-10-11":
        raise ValueError("Ledger schema or recording date drift")
    if d.get("historical_operator_link")!=URL or d.get("sha256") is not None:
        raise ValueError("Publisher link or imaginary digest promoted")
    win=d.get("archive_probe_window")
    if win!={"from":2005,"to":2007,"kind":"WAYBACK_CDX_METADATA_ONLY_NO_ARCHIVE_BODY_OR_BINARIES"}:
        raise ValueError("Unbounded archive probe window or content promotion")
    rows=d.get("sources")
    if not isinstance(rows,list) or len(rows)!=len(SOURCES):
        raise ValueError("Four separate dated, source-scoped records required")
    for row,want in zip(rows,SOURCES):
        if tuple(row.get(k) for k in ("id","observed_date","source_date","source","evidence_kind"))!=want:
            raise ValueError("Contemporaneous provenance/identity was altered")
        date.fromisoformat(row["source_date"])
        date.fromisoformat(row["observed_date"])
        if len(row.get("content_scope",""))<80:
            raise ValueError("Source limitation statement missing")
    if d.get("claims")!=FLAGS:
        raise ValueError("Unverified test-client, publisher or PET claim promoted")
    if d.get("pressure")!={"total":2486,"bounded_closed":2465,"open":18,"historical_ub":3}:
        raise ValueError("Historical closure unsupported")
    return "TW80_MAY16_OPERATOR_SOURCE_BOUNDARY_PASS"

if __name__=="__main__":
    print(validate(json.loads(LEDGER.read_text(encoding="utf-8"))))
