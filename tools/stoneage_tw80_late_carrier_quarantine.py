"""Reproducible strict identity gate for late 8.0-named carrier lookalikes.

Source metadata only. No downloading, executing, unarchiving or binary attestation.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

LEDGER = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-TW80-LATE-CARRIER-NEGATIVE-CONTROLS-R1.json"
LEADS = (
    ("CN-2007-NUMERIC-IP-SETUP", "2007-08-17", "StoneAge8.0setup.exe",
     "https://blog.sina.com.cn/s/blog_491de9d601000abm.html",
     "http://220.162.242.159/StoneAge8.0setup.exe",
     "MAINLAND_CLIENT_DESCRIBED_IN_2007_PLAYER_PRIVATE_SERVER_GUIDE",
     "CONTEMPORARY_COMMUNITY_TUTORIAL_THIRD_PARTY_IP"),
    ("CN-2013-REUSED-SETUP-NAME", "2013-02-17", "StoneAge8.0setup.exe",
     "https://www.iopq.net/thread-16840739-1-1.html", None,
     "MAINLAND_8_X_CLIENT_ALLOWED_IN_2013_PRIVATE_SERVER_GUIDE",
     "LATER_COMMUNITY_REUSE_AND_PATCHING_INSTRUCTIONS"),
    ("SA80-2016-SOURCEFORGE-REWORK", "2016-12-10", "SA80 project directory / Updated-Linux-SA80",
     "https://sourceforge.net/projects/sa80/files/",
     "https://sourceforge.net/projects/sa80/files/",
     "LATER_COMMUNITY_REWORK_SERVER_AND_DATA_NOT_TW_2005_RELEASE",
     "PUBLIC_2016_COMMUNITY_SOFTWARE_PROJECT"),
)
NEGATIVE_FLAGS = (
    "original_tw_2005_8_0_admitted", "original_publisher_binary_verified",
    "payload_retrieved", "original_pet_runtime_verified",
)
ASSERTIONS = (
    "matching_filename_proves_same_binary",
    "third_party_numeric_ip_is_official_taiwan_distribution",
    "sourceforge_2016_source_is_2005_taiwan_client",
    "post_install_community_patching_preserves_clean_snapshot",
    "unseen_payload_sha256_can_be_claimed",
    "official_taiwan_2005_8_0_binary_admitted",
    "genuine_paired_pet_opcode127_runtime_admitted",
    "early_jss1999_or_tw10_pet_membership_admitted",
)


def validate(document: dict) -> str:
    if document.get("schema") != "stoneage-tw80-late-carrier-negative-controls-r1":
        raise ValueError("Unexpected provenance ledger schema")
    if document.get("captured_on") != "2026-10-11" or "NOT verified official Taiwan" not in document.get("scope", ""):
        raise ValueError("Scope/date evidence boundary changed")
    leads = document.get("leads")
    if not isinstance(leads, list) or len(leads) != len(LEADS):
        raise ValueError("Candidate count changed")
    columns = ("id", "source_date", "filename", "source", "historical_url", "region_evidence", "custody_class")
    for row, expected in zip(leads, LEADS):
        if not isinstance(row, dict) or tuple(row.get(k) for k in columns) != expected:
            raise ValueError("Historical client identity/region/source changed")
        date.fromisoformat(row["source_date"])
        if not isinstance(row.get("source_statement"), str) or len(row["source_statement"]) < 40:
            raise ValueError("Required qualifying evidence statement missing")
        if any(row.get(flag) is not False for flag in NEGATIVE_FLAGS):
            raise ValueError("Unverified original runtime or publisher promoted")
        if row.get("sha256") is not None:
            raise ValueError("Invented original candidate SHA256")
    if set(document.get("assertions", {})) != set(ASSERTIONS) or any(document["assertions"].get(f) is not False for f in ASSERTIONS):
        raise ValueError("Unknown or promoted 8.0 installer claim")
    if document.get("pressure") != {"total": 2486, "bounded_closed": 2465, "open": 18, "historical_ub": 3}:
        raise ValueError("Unevidenced historical closure promotion")
    return "TW80_LATE_CARRIER_NEGATIVE_CONTROLS_PASS"


def main() -> None:
    print(validate(json.loads(LEDGER.read_text(encoding="utf-8"))))


if __name__ == "__main__":
    main()
