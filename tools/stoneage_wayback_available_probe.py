#!/usr/bin/env python3
"""Probe Wayback Availability API for near-period StoneAge Korea distribution roots.

This records metadata only. It does not download archived pages or client binaries.
"""

from __future__ import annotations

import concurrent.futures
import json
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
API = "https://archive.org/wayback/available"

SURFACES = [
    ("inium-www", "http://www.stoneage.enium.co.kr/"),
    ("inium-bare", "http://stoneage.enium.co.kr/"),
    ("hananet-game", "http://game.hananet.net/"),
    ("hananet-pds", "http://pds.hananet.net/"),
    ("cnet-downloads", "http://korea.cnet.com/downloads/"),
]

KEY_DATES = [
    "20001004",
    "20001013",
    "20001027",
    "20001228",
    "20010115",
    "20010430",
]


def request_json(url: str, *, timeout: int = 8) -> dict:
    last = None
    for attempt in range(1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8", "replace"))
        except (urllib.error.URLError, TimeoutError, ConnectionError, json.JSONDecodeError) as exc:
            last = exc
            time.sleep(2 ** attempt)
    raise RuntimeError(f"request failed: {url}: {last}")


def parse_closest(payload: dict) -> dict | None:
    snapshots = payload.get("archived_snapshots")
    if not isinstance(snapshots, dict):
        return None
    closest = snapshots.get("closest")
    if not isinstance(closest, dict):
        return None
    if not closest.get("available"):
        return None
    return {
        "timestamp": str(closest.get("timestamp", "")),
        "status": str(closest.get("status", "")),
        "url": str(closest.get("url", "")),
    }


def safe(value: str) -> str:
    return "".join(ch for ch in value if ch >= " " and ch != "\x7f")[:700]


def main() -> None:
    print("StoneAge Korea 2000 Wayback Availability probe — R1")
    print("SCOPE|metadata-only|no-archived-page-download|no-client-binary-download")
    print("WINDOW|requested_dates=20001004,20001013,20001027,20001228,20010115,20010430")

    jobs = []
    for surface, target in SURFACES:
        for requested in KEY_DATES:
            query = urllib.parse.urlencode({"url": target, "timestamp": requested})
            jobs.append((surface, requested, API + "?" + query))

    def probe_one(job):
        surface, requested, url = job
        try:
            payload = request_json(url)
            closest = parse_closest(payload)
        except Exception as exc:
            return ("error", surface, requested, type(exc).__name__, str(exc))
        if closest is None:
            return ("row", surface, requested, "", "", "")
        return (
            "row",
            surface,
            requested,
            closest["timestamp"],
            closest["status"],
            closest["url"],
        )

    rows = []
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for result in executor.map(probe_one, jobs):
            if result[0] == "error":
                _, surface, requested, kind, message = result
                errors.append((surface, requested, kind, message))
            else:
                _, surface, requested, timestamp, status, url = result
                rows.append((surface, requested, timestamp, status, url))

    surface_order = {name: i for i, (name, _) in enumerate(SURFACES)}
    date_order = {date: i for i, date in enumerate(KEY_DATES)}
    errors.sort(key=lambda x: (surface_order[x[0]], date_order[x[1]]))
    rows.sort(key=lambda x: (surface_order[x[0]], date_order[x[1]]))

    for surface, requested, kind, message in errors:
        print(f"ERROR|surface={surface}|requested={requested}|kind={kind}|message={safe(message)}")

    print(f"COUNT|queries|{len(SURFACES) * len(KEY_DATES)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|available_results|{sum(1 for row in rows if row[2])}")

    for surface, requested, timestamp, status, url in rows:
        available = "1" if timestamp else "0"
        print(
            "RESULT|"
            f"surface={surface}|requested={requested}|available={available}|"
            f"timestamp={safe(timestamp)}|status={safe(status)}|url={safe(url)}"
        )


if __name__ == "__main__":
    main()
