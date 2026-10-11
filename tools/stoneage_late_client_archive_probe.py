"""Offline, non-executing late-client candidate and archive metadata probe.

No network, shell, extraction or proprietary file bundling. Metadata alone is
never original-game/region/version or PET feature acceptance.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "research/recovered/STONEAGE-LATE-CLIENT-CANDIDATE-LEDGER-R1.json"
EXPECTED = {
    "CN-WAYI-SA8-8016": ("LINK_ONLY", "BEIJING_WAYI_MAINLAND_DOMAIN"),
    "TW-YANG-2012-SIXPART": ("LINK_ONLY", "CLAIMED_WAYI_TAIWAN_INSTALLER_COMMUNITY_REPOST"),
    "COMMUNITY-CLIENT-8018-RESOURCE-TOOL": ("REFERENCE_ONLY", "UNKNOWN_COMMUNITY_PATCH_CONTEXT"),
    "COMMUNITY-CLIENT-8002A": ("REFERENCE_ONLY", "UNKNOWN_COMMUNITY_PRIVATE_SERVER_CONTEXT"),
}

def validate_ledger(ledger: dict) -> None:
    if ledger.get("schema") != "stoneage-late-client-candidate-ledger-r1":
        raise ValueError("Wrong source ledger schema")
    arr = ledger.get("candidates")
    if not isinstance(arr, list) or len(arr) != len(EXPECTED):
        raise ValueError("Unexpected candidate count")
    seen = set()
    for entry in arr:
        ident = entry.get("id")
        if ident not in EXPECTED or ident in seen:
            raise ValueError("Unexpected/duplicate candidate")
        seen.add(ident)
        expected_state, expected_region = EXPECTED[ident]
        if entry.get("status") != expected_state or entry.get("operator_region_context") != expected_region:
            raise ValueError("Candidate version/region admission drift: " + ident)
        if any(entry.get(k) is not False for k in ("clean_operator_sample", "bytes_verified", "manifest_verified", "version_embedded_verified", "pet_runtime_verified")):
            raise ValueError("Unverified binary was promoted: " + ident)
        if entry.get("sha256") is not None:
            raise ValueError("Invented byte hash in link-only record: " + ident)
        if not isinstance(entry.get("source"), str) or not entry["source"].startswith("https://"):
            raise ValueError("Historical source URL missing")
        carriers = entry.get("historical_carriers")
        if not isinstance(carriers, list) or any(not x.startswith(("http://", "https://")) for x in carriers):
            raise ValueError("Malformed carrier URLs")
    cn = next(x for x in arr if x["id"] == "CN-WAYI-SA8-8016")
    tw = next(x for x in arr if x["id"] == "TW-YANG-2012-SIXPART")
    if cn["historical_carriers"] != ["http://cdl.wayi.com.cn/sa8_8016.rar"]:
        raise ValueError("Mainland operator-domain candidate changed")
    if len(tw["historical_carriers"]) != 6 or "8.5_" not in tw["version_attribution"]:
        raise ValueError("Likely 8.5 multipart exclusion changed")
    if any("TW_8_0_CONFIRMED" in str(x) for x in arr):
        raise ValueError("Unproven Taiwan 8.0 promotion")

def _zip_unsafe(name: str) -> bool:
    normalized = name.replace("\\", "/")
    return (
        normalized.startswith("/")
        or bool(re.match(r"^[a-zA-Z]:", normalized))
        or ".." in normalized.split("/")
        or "\\x00" in normalized
    )

def inspect_archive(path: Path) -> dict:
    if not path.is_file():
        raise ValueError("Not a regular file")
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        head = stream.read(16)
        stream.seek(0)
        while chunk := stream.read(1024 * 1024):
            h.update(chunk)
            size += len(chunk)
    if head.startswith(b"Rar!\\x1a\\x07\\x01\\x00"):
        signature = "RAR5"
    elif head.startswith(b"Rar!\\x1a\\x07\\x00"):
        signature = "RAR4"
    elif head.startswith(b"7z\\xbc\\xaf\\x27\\x1c"):
        signature = "7Z"
    elif head.startswith(b"PK\\x03\\x04"):
        signature = "ZIP"
    elif head.startswith(b"MZ"):
        signature = "PE_OR_DOS_MZ"
    else:
        signature = "UNKNOWN"
    out = {
        "filename": path.name, "size_bytes": size, "sha256": h.hexdigest(),
        "magic_family": signature, "member_count": None,
        "zip_unsafe_member_names": [], "zip_name_sample": [],
        "provenance_verified": False, "operator_region_verified": False,
        "version_verified": False, "pet_runtime_verified": False,
    }
    if signature == "ZIP":
        try:
            with zipfile.ZipFile(path) as zf:
                infos = zf.infolist()
                out["member_count"] = len(infos)
                out["zip_unsafe_member_names"] = [x.filename for x in infos if _zip_unsafe(x.filename)][:32]
                out["zip_name_sample"] = [x.filename for x in infos[:32]]
        except (OSError, zipfile.BadZipFile, ValueError) as exc:
            out["zip_parse_error"] = type(exc).__name__
    return out

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    arg = parser.add_mutually_exclusive_group(required=True)
    arg.add_argument("--check", action="store_true", help="Validate committed source-lead status")
    arg.add_argument("--inspect", metavar="PATH", help="Inspect an external, local archive; never run/extract")
    options = parser.parse_args()
    if options.check:
        validate_ledger(json.loads(LEDGER_PATH.read_text(encoding="utf-8")))
        print("LATE_CLIENT_REGION_VERSION_PROVENANCE_BOUNDARY_PASS")
    else:
        print(json.dumps(inspect_archive(Path(options.inspect)), ensure_ascii=False, sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
