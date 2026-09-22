#!/usr/bin/env python3
"""Trace later-recovered Netmarble StoneAge download-page paths back to 2003-2004.

These exact paths were recovered from a 2006 official Netmarble StoneAge page.
They are candidates only until an earlier capture proves continuity. The probe
reads archive metadata and archived HTML link targets; it does not download
client binaries.
"""

from __future__ import annotations

from tools.stoneage_korea174_archive_probe import (
    DOWNLOAD_EXT,
    archived_links,
    availability,
    cdx_query,
    safe,
)

TARGETS=(
    (
        "netmarble-down-load",
        "http://game3.netmarble.net/cp_site/stoneage/down/down_load.asp",
    ),
    (
        "netmarble-down-debugler",
        "http://game3.netmarble.net/cp_site/stoneage/down/down_debugler.asp",
    ),
)
KEY_DATES=("20030721","20030728","20030815","20030915","20040115","20060401")
MAX_SNAPSHOTS=8


def merge_snapshots(url,cdx_rows,availability_rows):
    rows={}
    for row in cdx_rows:
        ts=str(row.get("timestamp",""))
        original=str(row.get("original","") or url)
        if ts:
            rows[(ts,original)]={
                "timestamp":ts,
                "original":original,
                "status":str(row.get("statuscode","")),
                "mime":str(row.get("mimetype","")),
                "digest":str(row.get("digest","")),
                "length":str(row.get("length","")),
                "source":"cdx",
            }
    for cap in availability_rows:
        if not cap:
            continue
        ts=str(cap.get("timestamp",""))
        if not ts:
            continue
        rows.setdefault(
            (ts,url),
            {
                "timestamp":ts,
                "original":url,
                "status":str(cap.get("status","")),
                "mime":"",
                "digest":"",
                "length":"",
                "source":"availability",
            },
        )
    return tuple(
        sorted(rows.values(),key=lambda row:(row["timestamp"],row["original"]))[
            :MAX_SNAPSHOTS
        ]
    )


def main():
    print("StoneAge Korea 1.74 Netmarble exact download-path traceback — R1")
    print("SCOPE|later-official-paths-as-candidates|2003-2004-proof-required|html-links-only|no-client-binary-download")
    print("PROVENANCE|candidate-paths-first-observed-on-2006-official-root")
    print("KEY_DATES|"+",".join(KEY_DATES))

    all_links=set()
    for label,url in TARGETS:
        cdx_rows=[]
        cdx_error=""
        try:
            cdx_rows=cdx_query(url,2003,2004,collapse=False,limit=100)
        except Exception as exc:
            cdx_error=f"{type(exc).__name__}:{exc}"

        avail_rows=[]
        avail_errors=[]
        for date in KEY_DATES:
            try:
                avail_rows.append(availability(url,date))
            except Exception as exc:
                avail_errors.append((date,f"{type(exc).__name__}:{exc}"))

        snapshots=merge_snapshots(url,cdx_rows,avail_rows)
        early=[
            row for row in snapshots
            if row["timestamp"][:4] in {"2003","2004"}
        ]
        print(
            f"TARGET|label={safe(label)}|url={safe(url)}|"
            f"cdx_rows={len(cdx_rows)}|cdx_error={safe(cdx_error)}|"
            f"availability_hits={sum(row is not None for row in avail_rows)}|"
            f"availability_errors={len(avail_errors)}|"
            f"selected_snapshots={len(snapshots)}|early_2003_2004={len(early)}"
        )
        for date,error in avail_errors:
            print(
                f"AVAIL_ERROR|label={safe(label)}|date={date}|error={safe(error)}"
            )
        for row in snapshots:
            print(
                f"SNAPSHOT|label={safe(label)}|timestamp={row['timestamp']}|"
                f"source={row['source']}|status={safe(row['status'])}|"
                f"mime={safe(row['mime'])}|length={safe(row['length'])}|"
                f"digest={safe(row['digest'])}|url={safe(row['original'])}"
            )
            try:
                links=archived_links(row["timestamp"],row["original"])
            except Exception as exc:
                print(
                    f"FETCH_ERROR|label={safe(label)}|timestamp={row['timestamp']}|"
                    f"error={safe(type(exc).__name__+':'+str(exc))}"
                )
                continue
            for target,anchor in links:
                all_links.add((label,row["timestamp"],target,anchor))

    print(f"COUNT|interesting_links|{len(all_links)}")
    print(
        f"COUNT|download_links|"
        f"{sum(1 for _,_,target,_ in all_links if DOWNLOAD_EXT.search(target))}"
    )
    for label,timestamp,target,anchor in sorted(all_links):
        kind="download" if DOWNLOAD_EXT.search(target) else "interest"
        print(
            f"LINK|label={safe(label)}|timestamp={timestamp}|kind={kind}|"
            f"target={safe(target)}|anchor={safe(anchor)}"
        )


if __name__=="__main__":
    main()
