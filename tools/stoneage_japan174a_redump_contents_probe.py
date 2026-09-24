#!/usr/bin/env python3
"""Probe modern Redump metadata for Japanese PC coverdiscs/demos containing StoneAge.

This queries only the public metadata index using the open-source vgindex
`contents` filter. No disc image or payload download is attempted.
"""

from __future__ import annotations

import hashlib

from tools.stoneage_japan2004_redump_probe import (
    clean,
    fetch,
    matching_rows,
    modern_url,
    result_count,
    visible_text,
)

TARGETS=(
    ("jp-pc-coverdisc-latin", {"region":"jp","system":"PC","category":"Coverdiscs","contents":"StoneAge"}),
    ("jp-pc-coverdisc-space", {"region":"jp","system":"PC","category":"Coverdiscs","contents":"Stone Age"}),
    ("jp-pc-coverdisc-japanese", {"region":"jp","system":"PC","category":"Coverdiscs","contents":"ストーンエイジ"}),
    ("jp-pc-coverdisc-filename", {"region":"jp","system":"PC","category":"Coverdiscs","contents":"sa174hg.exe"}),
    ("jp-pc-demo-latin", {"region":"jp","system":"PC","category":"Demos","contents":"StoneAge"}),
    ("jp-pc-any-filename", {"region":"jp","system":"PC","contents":"sa174hg.exe"}),
    ("global-pc-coverdisc-filename", {"system":"PC","category":"Coverdiscs","contents":"sa174hg.exe"}),
    ("global-pc-any-filename", {"system":"PC","contents":"sa174hg.exe"}),
)


def main():
    print("StoneAge Japan 1.74a Redump contents-index probe — R1")
    print("SCOPE|modern-redump-metadata|contents-filter|coverdiscs+demos|no-disc-download")
    print("QUERY_SCHEMA|source=superg/vgindex@main|field=contents|categories=Coverdiscs,Demos")
    completed=0
    errors=0
    conclusive=0
    positives=0
    matched_rows=0
    for label,params in TARGETS:
        url=modern_url(params)
        try:
            result=fetch(url)
        except Exception as exc:
            errors+=1
            print(f"ERROR|label={label}|kind={type(exc).__name__}|message={clean(exc)}")
            continue
        completed+=1
        body=result["body"]
        vis=visible_text(body)
        count=result_count(vis)
        rows=matching_rows(body)
        marker="Disc Database" in vis
        if marker and count is not None:
            conclusive+=1
        if count is not None and count>0:
            positives+=1
        matched_rows+=len(rows)
        print(
            f"QUERY|label={label}|status={result['status']}|bytes={len(body)}|"
            f"sha256={hashlib.sha256(body).hexdigest()}|database_marker={int(marker)}|"
            f"result_count={'' if count is None else count}|matching_rows={len(rows)}|"
            f"final={clean(result['final'])}"
        )
        for row in rows:
            print(f"MATCH|label={label}|row={clean(row,1800)}")

    print(f"COUNT|queries|{len(TARGETS)}")
    print(f"COUNT|completed|{completed}")
    print(f"COUNT|errors|{errors}")
    print(f"COUNT|conclusive|{conclusive}")
    print(f"COUNT|positive_queries|{positives}")
    print(f"COUNT|matching_rows|{matched_rows}")
    if positives:
        print("RESOLUTION|REDUMP_CONTENTS_CANDIDATES_FOUND|inspect positive disc records before any payload claim")
    elif conclusive==len(TARGETS) and errors==0:
        print("RESOLUTION|REDUMP_CONTENTS_NO_HIT|no indexed StoneAge/sa174hg contents match in tested coverdisc/demo surfaces")
    else:
        print("RESOLUTION|INCONCLUSIVE|Redump contents surface incomplete")


if __name__=="__main__":
    main()
