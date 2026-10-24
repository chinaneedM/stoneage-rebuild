"""Bounded live-body qualification for contemporaneously documented official mirrors.

This tool does NOT install, execute, or publish proprietary clients. A prefix is
never a full original client, and matching magic is never proof of official
purity. No success may be inferred from a redirected login or HTML response.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import ipaddress
import json
import socket
import urllib.error
import urllib.parse
import urllib.request

MAX_PREFIX = 4096
TIMEOUT_SEC = 14
TARGETS = (
    ("KR_HANANET_FULL_8119", "http://stoneage.hananet.net/down/sa.exe", "2001-02-10 STAD 8119; historical commented download button"),
    ("KR_HANANET_TRIAL_8120", "http://stoneage.hananet.net/down/sa_demo.exe", "2001-02-10 STAD 8120; historical commented download button"),
    ("KR_CNET_CATALOG_MIRROR", "http://korea.cnet.com/pc/games/online/stoneage.zip", "Inium 2000 official download page / CNET Software_Id 200009263856"),
    ("KR_GAGAMEL_FORMAL_MIRROR", "http://www.gagamel.com/web_data/download/stoneagebeta.zip", "Inium 2001 formal-downloads page; beta in filename not a classification"),
)


def sniff_prefix(sample: bytes) -> str:
    if sample.startswith(b"MZ"):
        return "MZ_PE_CANDIDATE"
    if sample.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")):
        return "ZIP_CANDIDATE"
    if sample.startswith(b"Rar!\x1a\x07"):
        return "RAR_CANDIDATE"
    if sample.startswith(b"7z\xbc\xaf\x27\x1c"):
        return "SEVEN_Z_CANDIDATE"
    h = sample[:1024].lstrip().lower()
    if h.startswith((b"<!doctype html", b"<html", b"<?xml", b"<head")) or b"<html" in h:
        return "HTML_NOT_INSTALLER"
    if not sample:
        return "EMPTY"
    return "UNCLASSIFIED_PREFIX"


def public_url(url: str) -> bool:
    p = urllib.parse.urlsplit(url)
    if p.scheme not in {"http", "https"} or not p.hostname or p.username or p.password:
        return False
    try:
        ip = ipaddress.ip_address(p.hostname)
    except ValueError:
        return p.hostname.lower() not in {"localhost", "localhost.localdomain"}
    return ip.is_global


class NoCrossHostRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not public_url(newurl):
            raise ValueError("unsafe_redirect_target")
        old = urllib.parse.urlsplit(req.full_url).hostname
        new = urllib.parse.urlsplit(newurl).hostname
        if old.lower() != new.lower():
            raise ValueError("cross_host_redirect_unverified")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def classify(status: int | None, magic: str, final_url: str, original_url: str,
             sample_len: int) -> str:
    if status not in (200, 206):
        return "NOT_RETRIEVED"
    if urllib.parse.urlsplit(final_url).hostname != urllib.parse.urlsplit(original_url).hostname:
        return "CROSS_HOST_UNQUALIFIED"
    if magic.endswith("_CANDIDATE") and sample_len >= 2:
        return "BINARY_PREFIX_ONLY_REQUIRES_COMPLETE_BYTES"
    return "NON_BINARY_OR_UNCLASSIFIED"


def probe(label: str, url: str, evidence: str, opener=None) -> dict:
    result = {
        "id": label, "historical_source_url": url, "historical_pin": evidence,
        "http_status": None, "final_url": None, "content_type": None,
        "content_range": None, "content_length_header": None,
        "sample_bytes": 0, "sample_sha256": None,
        "magic": None, "qualification": "NOT_RETRIEVED",
        "complete_body_downloaded": False, "complete_original_sha256": None,
        "build_verified": False, "official_clean_client_verified": False,
        "note": "No full payload, content tree, runtime or official purity claim.",
    }
    if not public_url(url):
        result["error"] = "unsupported_target_url"
        return result
    op = opener or urllib.request.build_opener(NoCrossHostRedirect())
    req = urllib.request.Request(url, headers={
        "User-Agent": "StoneAge-Source-Qualification/1.0 (research; bounded)",
        "Range": f"bytes=0-{MAX_PREFIX-1}",
        "Accept": "application/octet-stream,*/*;q=0.5",
    })
    try:
        with op.open(req, timeout=TIMEOUT_SEC) as response:
            sample = response.read(MAX_PREFIX)
            status = response.status
            final_url = response.geturl()
            result.update({
                "http_status": status,
                "final_url": final_url,
                "content_type": response.headers.get("Content-Type"),
                "content_range": response.headers.get("Content-Range"),
                "content_length_header": response.headers.get("Content-Length"),
                "sample_bytes": len(sample),
                "sample_sha256": hashlib.sha256(sample).hexdigest(),
                "magic": sniff_prefix(sample),
            })
            result["qualification"] = classify(status, result["magic"], final_url, url, len(sample))
    except urllib.error.HTTPError as error:
        result["http_status"] = error.code
        result["error"] = "HTTP_ERROR"
    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError, ValueError) as error:
        result["error"] = type(error).__name__
        # Never present the exception string as trusted unredacted evidence.
    return result


def make_report() -> dict:
    entries = [probe(*t) for t in TARGETS]
    return {
        "schema": "stoneage.early_official_client_live_prefix_probe.r1",
        "probe_utc": datetime.now(timezone.utc).isoformat(),
        "task": "EARLY-OFFICIAL-CLIENT-ORIGINAL-PAYLOAD-QUALIFICATION-02",
        "method": "Bounded 4096-byte Range GET, original historical hosts, no cross-host redirect",
        "entries": entries,
        "new_complete_original_client_bytes": 0,
        "new_verified_original_sha256": 0,
        "named_entity_to_original_image_id_newly_proven": 0,
        "boundary": "An HTTP response, 4096-byte prefix or executable magic is not a complete authenticated client.",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="-")
    args = ap.parse_args()
    data = json.dumps(make_report(), ensure_ascii=False, indent=2) + "\n"
    if args.output == "-":
        print(data, end="")
    else:
        from pathlib import Path
        Path(args.output).write_text(data, encoding="utf-8")


if __name__ == "__main__":
    main()
