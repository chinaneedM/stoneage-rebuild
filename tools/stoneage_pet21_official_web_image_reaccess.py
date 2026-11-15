#!/usr/bin/env python3
"""PET21: bounded public web-image source reaccess, *not* an official client asset map.

Only pre-recorded historic operator-page image URL refs are admitted; all
commercial image bytes stay in transient process memory. Public outputs contain
URL, response status, original-format magic, dimensions, SHA256 and explicit
version/provenance limits, never pixel payloads or original server text.
"""
import argparse
import concurrent.futures
import hashlib
import json
import re
import socket
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json"
PINNED_CATALOG_GIT_BLOB = "fdb7d9aade2df62d1a1e06b2d2f9e383693ed980"
# Explicit dated research subset, across all three Hangame pages and all three
# Waei pages; not a crawl of 228 URLs nor a claim of exhaustive image coverage.
SAMPLE_ORDINALS = {
    "jp_official_web": (1, 2, 3, 44, 45, 46, 89, 90, 91, 123, 124),
    "cn_official_web": (1, 2, 6, 7, 34, 35, 66, 67, 68, 102, 103, 104),
}
SAMPLE_LIMIT = sum(map(len, SAMPLE_ORDINALS.values()))
ALLOWED_ARCHIVE_HOSTS = frozenset({"archive.org", "web.archive.org"})
MAX_IMAGE_BYTES = 256_000
MAX_AVAILABILITY_BYTES = 12_000
PATTERN_CAPTURE = re.compile(r"/web/(\d{14})(?:id_|im_)?/")


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def archive_url(image, capture):
    return "https://web.archive.org/web/" + capture + "id_/" + image


def availability_url(image, page_capture):
    return ("https://archive.org/wayback/available?url=" +
            quote(image, safe="") + "&timestamp=" + page_capture)


def verify_reference(url, source):
    p = urlsplit(url)
    if p.scheme not in ("http", "https") or p.username or p.password or p.query or p.fragment:
        raise ValueError("unsafe original image URL")
    host = (p.hostname or "").lower()
    if source == "jp_official_web":
        if host != "images.hangame.co.jp" or not re.fullmatch(
                r"/_images/game/saj/petpicgroup[1-3]-\d+\.gif", p.path):
            raise ValueError("unexpected Hangame source")
    elif source == "cn_official_web":
        if host != "www.waei.com.cn" or not re.fullmatch(
                r"/ZHUANQU/stoneage2/pet/img/newpet/\d+\.(?:JPG|jpg)", p.path):
            raise ValueError("unexpected Waei source")
    else:
        raise ValueError("not an official web image namespace")
    return url


def targets(catalog):
    if set(SAMPLE_ORDINALS) - set(catalog["datasets"]):
        raise ValueError("missing source namespaces")
    selected = []
    for source, ordinals in SAMPLE_ORDINALS.items():
        rows = catalog["datasets"][source]
        by_id = {row["web_ordinal"]: row for row in rows}
        if len(by_id) != len(rows):
            raise ValueError("duplicate operator web ordinals")
        for ordinal in ordinals:
            item = by_id[ordinal]
            ref = item["source_refs"][0]
            capture = ref["capture"]
            if not re.fullmatch(r"\d{14}", capture):
                raise ValueError("invalid archived original page capture")
            url = verify_reference(item["image_reference_url"], source)
            existing = item.get("image_actual_sha256")
            if existing is not None and not re.fullmatch(r"[a-f0-9]{64}", existing):
                raise ValueError("invalid previous image hash")
            selected.append({
                "source_namespace": source,
                "web_ordinal": ordinal,
                "record_id": item["id"],
                "name_as_written": item.get("name_as_written"),
                "original_image_url": url,
                "original_page_url": ref["url"],
                "page_archive_capture": capture,
                "page_body_sha256": ref["sha256"],
                "previously_verified_image_sha256": existing,
                "original_page_era_not_exact_client_build": True,
                "actual_client_species_id": None,
                "public_use_permission_verified": False,
            })
    if len(selected) != SAMPLE_LIMIT:
        raise ValueError("sample target count mismatch")
    return selected


class ArchiveOnlyRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlsplit(newurl).hostname not in ALLOWED_ARCHIVE_HOSTS:
            raise HTTPError(req.full_url, 403, "ARCHIVE_REDIRECT_OUTSIDE_ALLOWED_HOST", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENER = build_opener(ArchiveOnlyRedirect)


def retrieve(url, maxbytes, timeout):
    if urlsplit(url).hostname not in ALLOWED_ARCHIVE_HOSTS:
        raise ValueError("archive endpoint not allowed")
    req = Request(url, headers={
        "User-Agent": "StoneAge-SourceBoundedResearch/1.0 (historic pet source verification)",
        "Accept": "image/gif,image/jpeg,image/png,application/json,*/*;q=0.1",
    })
    try:
        with OPENER.open(req, timeout=timeout) as resp:
            destination = resp.geturl()
            if urlsplit(destination).hostname not in ALLOWED_ARCHIVE_HOSTS:
                return {"status": "UNTRUSTED_REDIRECT"}, None, None
            buf = resp.read(maxbytes + 1)
            return {"status": "HTTP_OK", "http_status": resp.status,
                    "final_url": destination,
                    "content_type": resp.headers.get("Content-Type", "")}, buf, resp.headers
    except HTTPError as e:
        return {"status": "HTTP_ERROR", "http_status": e.code}, None, None
    except (URLError, TimeoutError, socket.timeout, ConnectionError, OSError) as e:
        return {"status": "NETWORK_ERROR", "error_class": type(e).__name__}, None, None


def image_magic(body):
    if body.startswith((b"GIF87a", b"GIF89a")) and len(body) >= 10:
        return "GIF", [int.from_bytes(body[6:8], "little"), int.from_bytes(body[8:10], "little")]
    if body.startswith(b"\xff\xd8\xff") and body.endswith(b"\xff\xd9"):
        return "JPEG", None
    if body.startswith(b"\x89PNG\r\n\x1a\n") and len(body) >= 24:
        return "PNG", [int.from_bytes(body[16:20], "big"), int.from_bytes(body[20:24], "big")]
    return None, None


def image_proof(response, body, expected_sha):
    if body is None:
        return None
    if len(body) > MAX_IMAGE_BYTES:
        return {"kind": "RESPONSE_TOO_LARGE_NOT_RECOVERED", "byte_limit": MAX_IMAGE_BYTES}
    fmt, dimensions = image_magic(body)
    if fmt is None:
        return {"kind": "NON_IMAGE_RESPONSE_NOT_RECOVERED", "length": len(body),
                "content_type": response.get("content_type", "")[:80]}
    final = response.get("final_url", "")
    archive_match = PATTERN_CAPTURE.search(urlsplit(final).path)
    if not archive_match or urlsplit(final).hostname != "web.archive.org":
        return {"kind": "IMAGE_BYTES_WITHOUT_VERIFIED_ARCHIVE_PROVENANCE",
                "actual_bytes": len(body), "format": fmt}
    sha = hashlib.sha256(body).hexdigest()
    return {"kind": "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED",
            "archive_image_capture": archive_match.group(1),
            "actual_bytes": len(body), "format": fmt, "dimensions": dimensions,
            "sha256": sha,
            "earlier_confirmed_sha_matches": sha == expected_sha if expected_sha else None,
            "same_capture_instant_as_parent_page_proven": False,
            "official_game_client_graphic_id_proven": False,
            "image_publication_rights_proven": False}


def probe_one(target, timeout):
    out = dict(target)
    date = ("20060604065927" if target["source_namespace"] == "jp_official_web"
            and target["web_ordinal"] == 1
            else target["page_archive_capture"])
    primary, body, headers = retrieve(archive_url(target["original_image_url"], date),
                                       MAX_IMAGE_BYTES, timeout)
    out["attempt_1"] = {k: v for k, v in primary.items() if k != "final_url"}
    proof = image_proof(primary, body, target["previously_verified_image_sha256"])
    if proof and proof["kind"] == "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED":
        out["image_result"] = proof
        return out
    availability, response, hdr = retrieve(
        availability_url(target["original_image_url"], target["page_archive_capture"]),
        MAX_AVAILABILITY_BYTES, timeout)
    out["attempt_2"] = {k: v for k, v in availability.items() if k != "final_url"}
    available = None
    try:
        if response is not None and len(response) <= MAX_AVAILABILITY_BYTES:
            payload = json.loads(response)
            nearest = payload.get("archived_snapshots", {}).get("closest", {})
            if (nearest.get("available") and nearest.get("status") in ("200", 200)
                    and re.fullmatch(r"\d{14}", str(nearest.get("timestamp", "")))):
                available = nearest["timestamp"]
    except (ValueError, TypeError, AttributeError):
        pass
    if available:
        third, body3, hdr3 = retrieve(
            archive_url(target["original_image_url"], available), MAX_IMAGE_BYTES, timeout)
        out["attempt_3"] = {k: v for k, v in third.items() if k != "final_url"}
        verified = image_proof(third, body3, target["previously_verified_image_sha256"])
        if verified and verified["kind"] == "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED":
            out["image_result"] = verified
            return out
        out["image_result"] = verified or {"kind": "ARCHIVED_URL_NOT_READABLE_NOW"}
    else:
        out["image_result"] = proof or {"kind": "NOT_RETRIEVED_NETWORK_OR_INDEX_BLOCKED"}
    return out


def run_probe(rows, workers=4, timeout=8):
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        future_list = [pool.submit(probe_one, x, timeout) for x in rows]
        output = [future.result() for future in future_list]
    counts = {}
    for x in output:
        code = x["image_result"]["kind"]
        counts[code] = counts.get(code, 0) + 1
    return {
        "schema": "stoneage.pet21_bounded_official_web_image_reaccess_observations.r1",
        "source_catalog_git_blob": PINNED_CATALOG_GIT_BLOB,
        "scope": "BOUNDED_PER_URL_NETWORK_PROBES_NOT_ALL_IMAGES_OR_OFFICIAL_CLIENT_SPECIES",
        "sample_target_count": len(rows),
        "result_counts": counts,
        "source_qualified_archived_images_newly_observed":
            sum(x["image_result"]["kind"] == "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED"
                and not x["previously_verified_image_sha256"] for x in output),
        "original_media_written_to_disk_or_published": False,
        "no_response_does_not_prove_no_archived_image_exists": True,
        "no_historical_page_image_same_timestamp_claim": True,
        "records": output,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--verify-only", action="store_true")
    p.add_argument("--probe", action="store_true")
    p.add_argument("--timeout", type=int, default=8)
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--catalog", type=Path, default=CATALOG)
    args = p.parse_args()
    if args.verify_only == args.probe:
        p.error("choose exactly one of --verify-only or --probe")
    if not (1 <= args.timeout <= 20 and 1 <= args.workers <= 8):
        p.error("timeout must be 1..20, workers 1..8")
    raw = args.catalog.read_bytes()
    if git_blob(raw) != PINNED_CATALOG_GIT_BLOB:
        p.error("PET16 catalog Git blob has changed")
    rows = targets(json.loads(raw))
    if args.verify_only:
        data = {"status": "OFFLINE_SOURCE_REFERENCE_VALIDATION_OK",
                "source_catalog_git_blob": PINNED_CATALOG_GIT_BLOB,
                "sample_target_count": len(rows),
                "per_source_samples": {k: len(v) for k, v in SAMPLE_ORDINALS.items()},
                "no_network_or_original_images_acquired": True,
                "all_original_game_species_ids_unknown": True}
    else:
        data = run_probe(rows, workers=args.workers, timeout=args.timeout)
    print("PET21_RESULT_JSON_BEGIN")
    print(json.dumps(data, ensure_ascii=False, sort_keys=True))
    print("PET21_RESULT_JSON_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
