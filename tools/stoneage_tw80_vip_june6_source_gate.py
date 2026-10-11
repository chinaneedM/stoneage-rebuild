"""Offline provenance gate for the alleged June 6 2005 Taiwan VIP 8.0 disc."""
from pathlib import Path
import json

LEDGER = (Path(__file__).resolve().parents[1] /
          "research/recovered/STONEAGE-TW80-VIP-JUNE6-DISC-SOURCE-R1.json")
IDS = ("EARLIEST_ATTRIBUTED_REPOST","BAHAMUT_REPOST","WELOVESA_REPOST","SHIQI_TV_REPOST")
URLS = (
    "http://bbs.wayi.com.tw/viewthread.php?tid=40940",
    "https://forum.gamer.com.tw/G2.php?bsn=1571&sn=1958",
    "https://www.lab.welovesa.com/viewthread.php?tid=38",
    "https://shiqi.tv/shiqi130.htm")
CHANNELS = (
    ("EVENT_JUNE4","2005-06-04","CONTEMPORARY_PRESS_REPORTED_PLANNED_DISC_GIVEAWAY"),
    ("VIP_JUNE6","2005-06-06","LATER_REPOST_CLAIMS_DISC_MAILED"),
    ("RELEASE_JUNE8","2005-06-08","CONTEMPORARY_RELEASE_PRESS_REPORTS_PACKAGED_UPDATE_DISC"))
CLAIMS = (
    "multiple_reposts_count_as_independent_sources",
    "wayi_forum_host_proves_official_2005_notice",
    "claimed_posting_proves_mailing",
    "vip_disc_identical_to_event_or_retail_disc",
    "disc_identity_or_original_sha_verified",
    "original_pet_packet127_verified",
    "taiwan10_or_jss1999_promoted",
    "engine_transition")

def validate(data):
    if data.get("schema") != "stoneage-tw80-vip-june6-source-gate-r1":
        raise ValueError("schema mismatch")
    if data.get("recorded_on") != "2026-10-12":
        raise ValueError("provenance date mismatch")
    lead = data.get("lead",{})
    if lead.get("claimed_event_date") != "2005-06-06" or lead.get("headline") != "親愛的石器時代VIP玩家 8.0光碟寄出":
        raise ValueError("headline/date drift")
    if lead.get("status") != "REPOST_ONLY_NOT_OFFICIAL_2005_NOTICE":
        raise ValueError("unjustified promotion to official 2005")
    for key in ("original_2005_operator_notice_retrieved","original_disc_image_retrieved",
                "publisher_file_manifest_retrieved","original_pet_runtime_verified"):
        if lead.get(key) is not False:
            raise ValueError("unverified original artifact")
    if lead.get("original_installer_sha256") is not None:
        raise ValueError("invented original hash")
    rows = data.get("lineage",[])
    if len(rows) != 4:
        raise ValueError("repost lineage cardinality")
    for i,row in enumerate(rows):
        if row.get("id") != IDS[i] or row.get("url") != URLS[i]:
            raise ValueError("repost lineage identity")
        if i == 0:
            if row.get("posted_at") != "2008-09-04" or row.get("retrieved_original") is not False:
                raise ValueError("unretrieved 2008 parent promoted")
        elif row.get("independently_verified") is not False or row.get("contains_claim") is not True:
            raise ValueError("copy treated as independent")
    channels = data.get("channels",[])
    if len(channels) != 3:
        raise ValueError("distribution channel cardinality")
    for row, expected in zip(channels, CHANNELS):
        if tuple(row.get(k) for k in ("id","date","status")) != expected or row.get("physical_disc_authenticated") is not False:
            raise ValueError("independent disc identities conflated")
        if not isinstance(row.get("source"), str) or not row["source"].startswith("https://"):
            raise ValueError("missing source")
    claims = data.get("claims",{})
    if set(claims) != set(CLAIMS) or any(claims[k] is not False for k in CLAIMS):
        raise ValueError("unverified claim promotion")
    if data.get("pressure") != {"total":2486,"bounded_closed":2465,"open":18,"historical_ub":3}:
        raise ValueError("pressure changed without source")
    return "TW80_VIP_JUNE6_REPOST_BOUNDARY_PASS"

if __name__ == "__main__":
    print(validate(json.loads(LEDGER.read_text(encoding="utf-8"))))
