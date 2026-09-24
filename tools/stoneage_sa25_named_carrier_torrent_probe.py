#!/usr/bin/env python3
"""Cross-scan public old-disc torrent metadata against all source-named StoneAge 2.5 carriers.

This is metadata-only archaeology. It reads allseeds.zip and .torrent path metadata,
never disc/client payload bytes.
"""
from __future__ import annotations

import hashlib
import io
import re
import urllib.request
import zipfile

from tools.stoneage_sa25_exact_carrier_probe import TARGETS, norm, strict_match
from tools.stoneage_sa25_old_disc_torrent_probe import (
    MAX_TORRENT,
    MAX_ZIP,
    UA,
    URL,
    bdecode,
    root_info_span,
    torrent_paths,
)


def clean(v, n=3200):
    return " ".join(str(v or "").split()).replace("|", "%7C")[:n]


def canonical_period(s):
    n = norm(s)
    n = re.sub(r"2002年0?2月", "200202", n)
    n = re.sub(r"2002第0?2期", "200202", n)
    n = re.sub(r"2002年0?1月", "200201", n)
    n = re.sub(r"2002第0?1期", "200201", n)
    return n


FLEX_PERIODICALS = {
    "computer-news-gameworld": (("电脑报", "游戏世界"), "200202"),
    "game-king": (("游戏王",), "200202"),
    "home-computer-world": (("家庭电脑世界",), "200202"),
    "pc-free": (("pc任我行",), "200202"),
    "computer-fan-games": (("电脑爱好者", "玩游戏"), "200202"),
    "software-fashion": (("软件时尚",), "200202"),
    "crystal-sharp": (("水晶宝合", "锐"), "200202"),
    "popular-games": (("大众游戏",), "200202"),
    "chip-new-pc": (("chip", "新电脑"), "200202"),
    "online-club-gamebar": (("网上俱乐部", "游戏吧"), "200202"),
    "popular-pc-netbar": (("大众电脑", "网吧乐园"), "200202"),
    "computer-aviation": (("计算机与航空",), "200201"),
    "middle-school-computer": (("中学生电脑", "攻略特刊"), "2002"),
}


def flexible_periodical_match(label, blob):
    spec = FLEX_PERIODICALS.get(label)
    if not spec:
        return False
    anchors, period = spec
    c = canonical_period(blob)
    if not all(norm(a) in c for a in anchors):
        # Crystal-box source spelling is historically inconsistent: 宝合 / 宝盒.
        if label == "crystal-sharp":
            if not ((norm("水晶宝合") in c or norm("水晶宝盒") in c) and norm("锐") in c):
                return False
        else:
            return False
    return period in c


def classify_path(path):
    strict = []
    search_only = []
    low = norm(path)
    for label, queries, kind in TARGETS:
        if strict_match(label, queries, kind, path) or flexible_periodical_match(label, path):
            strict.append((label, kind))
            continue
        # Preserve useful lexical carrier leads without silently promoting them.
        if label == "bombing-chicken-game":
            if any(norm(x) in low for x in ("轰炸鸡", "哇靠轰炸鸡", "2001C226")):
                search_only.append((label, kind))
        elif kind == "periodical":
            anchors, _ = FLEX_PERIODICALS.get(label, ((), ""))
            if anchors and all(norm(a) in low for a in anchors):
                search_only.append((label, kind))
        elif kind == "guide":
            if any(norm(q.split(" 2002")[0]) in low for q in queries if q):
                search_only.append((label, kind))
    return tuple(strict), tuple(search_only)


def fetch_zip():
    req = urllib.request.Request(URL, headers={"User-Agent": UA, "Accept": "application/zip,*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        b = r.read(MAX_ZIP + 1)
        if len(b) > MAX_ZIP:
            raise ValueError("allseeds-too-large")
        return int(getattr(r, "status", r.getcode())), r.geturl(), dict(r.headers.items()), b


def main():
    print("StoneAge 2.5 source-named carrier old-disc torrent cross-scan — R1")
    print("SCOPE|20-source-named-carriers|public-allseeds.zip|torrent-path-metadata-only|no-disc-payload")
    st, final, h, zbytes = fetch_zip()
    print(
        f"ZIP|status={st}|bytes={len(zbytes)}|sha256={hashlib.sha256(zbytes).hexdigest()}|"
        f"last_modified={clean(h.get('Last-Modified'))}|final={clean(final)}"
    )

    counts = {
        "torrent": 0,
        "strict_torrents": 0,
        "strict_paths": 0,
        "lead_torrents": 0,
        "lead_paths": 0,
        "errors": 0,
    }
    labels = set()

    with zipfile.ZipFile(io.BytesIO(zbytes)) as z:
        print(f"COUNT|zip_entries|{len(z.namelist())}")
        for entry in z.namelist():
            if not entry.lower().endswith(".torrent"):
                continue
            counts["torrent"] += 1
            try:
                zi = z.getinfo(entry)
                if zi.file_size > MAX_TORRENT:
                    print(f"SKIP|entry={clean(entry)}|reason=torrent-too-large|bytes={zi.file_size}")
                    continue
                raw = z.read(entry)
                meta, _ = bdecode(raw, 0)
                paths = torrent_paths(meta)
                strict_rows = []
                lead_rows = []
                for path in paths:
                    strict, lead = classify_path(path)
                    if strict:
                        strict_rows.append((path, strict))
                        labels.update(x[0] for x in strict)
                    elif lead:
                        lead_rows.append((path, lead))

                if not strict_rows and not lead_rows:
                    continue

                try:
                    s, e = root_info_span(raw)
                    infohash = hashlib.sha1(raw[s:e]).hexdigest()
                except Exception:
                    infohash = ""

                if strict_rows:
                    counts["strict_torrents"] += 1
                    counts["strict_paths"] += len(strict_rows)
                    print(
                        f"TORRENT_STRICT|entry={clean(entry)}|infohash={infohash}|"
                        f"paths={len(paths)}|matching_paths={len(strict_rows)}"
                    )
                    for path, hits in strict_rows[:200]:
                        hittext = ",".join(f"{label}:{kind}" for label, kind in hits)
                        print(f"PATH_STRICT|entry={clean(entry)}|hits={clean(hittext)}|value={clean(path)}")

                if lead_rows:
                    counts["lead_torrents"] += 1
                    counts["lead_paths"] += len(lead_rows)
                    print(
                        f"TORRENT_LEAD|entry={clean(entry)}|infohash={infohash}|"
                        f"paths={len(paths)}|matching_paths={len(lead_rows)}"
                    )
                    for path, hits in lead_rows[:120]:
                        hittext = ",".join(f"{label}:{kind}" for label, kind in hits)
                        print(f"PATH_LEAD|entry={clean(entry)}|hits={clean(hittext)}|value={clean(path)}")
            except Exception as e:
                counts["errors"] += 1
                print(f"ERROR|entry={clean(entry)}|kind={type(e).__name__}|message={clean(e)}")

    print(f"COUNT|torrent_entries|{counts['torrent']}")
    print(f"COUNT|strict_torrents|{counts['strict_torrents']}")
    print(f"COUNT|strict_paths|{counts['strict_paths']}")
    print(f"COUNT|strict_labels|{len(labels)}")
    print(f"LABELS|strict={clean(','.join(sorted(labels)))}")
    print(f"COUNT|lead_torrents|{counts['lead_torrents']}")
    print(f"COUNT|lead_paths|{counts['lead_paths']}")
    print(f"COUNT|errors|{counts['errors']}")

    if counts["strict_paths"]:
        print("RESOLUTION|SOURCE_NAMED_CARRIER_PATHS_FOUND|inspect exact issue/disc identity and public payload availability next")
    elif counts["lead_paths"]:
        print("RESOLUTION|LEXICAL_CARRIER_NEIGHBORHOOD_ONLY|do not infer the exact source-named issue")
    elif counts["errors"]:
        print("RESOLUTION|PARTIAL_METADATA_FAILURE|retry failed metadata only")
    else:
        print("RESOLUTION|NO_SOURCE_NAMED_CARRIER_PATHS|tested torrent snapshot has no exact source-named carrier path")

    print(
        "EVIDENCE_BOUNDARY|a matching torrent path can identify a candidate historical carrier image only; "
        "the 2002 source says named media could contain either the full 2.5 package or updater, so actual media bytes/file tree "
        "must be inspected before any client or field-map provenance claim."
    )


if __name__ == "__main__":
    main()
