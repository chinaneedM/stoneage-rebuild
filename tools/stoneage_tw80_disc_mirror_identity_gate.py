"""Historical 2005 8.0 disc vs 2006 third-party installer carrier gate.

A strict source-only audit; neither downloads nor executes candidate binaries.
"""
from datetime import date
from pathlib import Path
import json

LEDGER = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-TW80-DISC-MIRROR-IDENTITY-R1.json"
EXPECTED = (
    ("TW80_20050603_PRESS_DISC_PLAN", "2005-06-03", "2005-06-04",
     "https://acg.gamer.com.tw/search.php?c1=976&c2=3&machine=1%2C0&s=2&type=1",
     "PRESS_INDEX_PLANNED_FREE_80_UPDATE_DISC", None, None),
    ("TW80_20050608_LAUNCH", "2005-06-08", "2005-06-08",
     "https://gnn.gamer.com.tw/detail.php?sn=20167",
     "CONTEMPORARY_LAUNCH_RELEASE_REPORT", None, None),
    ("TW80_20060801_DLER_MIRROR", "2006-08-01", None,
     "https://www.nakuz.com/thread-2493728-1-1.html",
     "FAN_POST_THIRD_PARTY_MIRROR_WITH_PRIVATE_PATCH_STEPS",
     "Stoneage80.exe", "http://tcrc.dl.dler.org/Yesterday/v/wayi/Stoneage80.exe"),
)
FIELDS = ("id", "date", "event_date", "source", "kind", "file_name", "carrier_url")
CLAIMS = (
    "june4_disc_was_actually_handed_out",
    "dler_mirror_is_authenticated_taiwan_publisher_2005",
    "dler_mirror_is_bit_identical_to_june2005_disc",
    "filename_80_proves_original_exe_version",
    "sa_7505_7507_prove_8_0_runtime",
    "read_error_proves_http404",
    "original_pet_packet127_verified",
    "early_taiwan10_or_jss1999_feature_promoted",
)

def validate(doc: dict) -> str:
    if doc.get("schema") != "stoneage-tw80-disc-mirror-identity-gate-r1" or doc.get("recorded_on") != "2026-10-11":
        raise ValueError("Unexpected ledger schema/date")
    rows = doc.get("records")
    if not isinstance(rows, list) or len(rows) != len(EXPECTED):
        raise ValueError("Three independent source-era rows required")
    for row, accepted in zip(rows, EXPECTED):
        if tuple(row.get(k) for k in FIELDS) != accepted:
            raise ValueError("Source date, carrier or file identity drift")
        date.fromisoformat(row["date"])
        if row["event_date"] is not None:
            date.fromisoformat(row["event_date"])
        if len(row.get("reported", "")) < 85:
            raise ValueError("Missing original source limitation")
        if row.get("sha256") is not None:
            raise ValueError("No file was hashed")
        for k in ("bytes_verified", "publisher_verified", "original_pet_runtime_verified"):
            if row.get(k) is not False:
                raise ValueError("Unverified client or PET runtime promotion")
    claims = doc.get("claims", {})
    if set(claims) != set(CLAIMS) or any(claims.get(k) is not False for k in CLAIMS):
        raise ValueError("Unverified original disc/mirror attribution")
    if doc.get("pressure") != {"total":2486,"bounded_closed":2465,"open":18,"historical_ub":3}:
        raise ValueError("Unevidenced pressure closure")
    return "TW80_DISC_MIRROR_IDENTITY_BOUNDARY_PASS"

if __name__ == "__main__":
    print(validate(json.loads(LEDGER.read_text(encoding="utf-8"))))
