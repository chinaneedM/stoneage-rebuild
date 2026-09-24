#!/usr/bin/env python3
"""Bounded preservation-index probe for the inferred Feb-2002 GameWorld disc token.

The Jan-2002 issue is independently preserved as GAMEWORLD200201.iso. This tool
uses the adjacent GAMEWORLD200202 token only as a search hypothesis and queries
public metadata indexes; it never downloads disc/client payload bytes.
"""
from __future__ import annotations

import hashlib

from tools.stoneage_sa25_exact_carrier_probe import (
    clean,
    discm_rows,
    discm_url,
    fetch_json,
    ia_docs,
    ia_metadata,
    ia_url,
    interesting_files,
    norm,
)

QUERIES = (
    "GAMEWORLD200202",
    "GAMEWORLD200202.iso",
    "电脑报配套光盘之游戏世界200202",
    "电脑报 游戏世界 2002年2月",
)
ANCHORS = ("gameworld200202", "电脑报配套光盘之游戏世界200202")


def candidate_match(blob):
    n = norm(blob)
    return any(norm(a) in n for a in ANCHORS)


def main():
    print("StoneAge 2.5 GameWorld February-2002 adjacent-token preservation probe — R1")
    print("SCOPE|inferred-token-only|DiscMaster+IA-metadata|no-disc-payload")
    print("KNOWN_CONTROL|GAMEWORLD200201.iso|month=2002-01|status=independently-preserved")
    print("HYPOTHESIS_TOKEN|GAMEWORLD200202.iso|month=2002-02|status=search-only-not-fact")

    dm_hits = {}
    ia_hits = {}
    errors = []

    for q in QUERIES:
        try:
            st, final, body, data = fetch_json(discm_url(q))
            rows = discm_rows(data)
            hits = []
            for row in rows:
                blob = " ".join(
                    str(row.get(k) or "")
                    for k in ("itemName", "fileid", "filename", "href", "text", "title")
                )
                if candidate_match(blob):
                    hits.append(row)
            print(
                f"DISCM_QUERY|query={clean(q)}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|hits={len(hits)}|final={clean(final)}"
            )
            for row in hits:
                key = (str(row.get("itemid") or ""), str(row.get("fileid") or ""))
                dm_hits[key] = row
                print(
                    f"DISCM_HIT|itemid={clean(row.get('itemid'))}|itemName={clean(row.get('itemName'))}|"
                    f"fileid={clean(row.get('fileid'))}|filename={clean(row.get('filename'))}|"
                    f"size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|b3sum={clean(row.get('b3sum'))}"
                )
        except Exception as e:
            errors.append((f"discm:{q}", type(e).__name__, str(e)))

        try:
            st, final, body, data = fetch_json(ia_url(q))
            docs = ia_docs(data)
            hits = []
            for row in docs:
                blob = " ".join(
                    str(row.get(k) or "")
                    for k in ("identifier", "title", "description", "date", "year")
                )
                if candidate_match(blob):
                    hits.append(row)
            print(
                f"IA_QUERY|query={clean(q)}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|items={len(docs)}|hits={len(hits)}|final={clean(final)}"
            )
            for row in hits:
                ident = str(row.get("identifier") or "")
                ia_hits[ident] = row
                print(
                    f"IA_HIT|identifier={clean(ident)}|title={clean(row.get('title'))}|"
                    f"date={clean(row.get('date'))}|year={clean(row.get('year'))}|"
                    f"collection={clean(row.get('collection'))}"
                )
        except Exception as e:
            errors.append((f"ia:{q}", type(e).__name__, str(e)))

    file_hits = 0
    for ident, row in sorted(ia_hits.items()):
        try:
            st, final, body, meta = ia_metadata(ident)
            files = [f for f in interesting_files(meta) if candidate_match(str(f.get("name") or ""))]
            print(
                f"IA_META|identifier={clean(ident)}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|candidate_files={len(files)}|final={clean(final)}"
            )
            for f in files:
                file_hits += 1
                print(
                    f"IA_FILE|identifier={clean(ident)}|name={clean(f.get('name'))}|"
                    f"size={clean(f.get('size'))}|md5={clean(f.get('md5'))}|sha1={clean(f.get('sha1'))}"
                )
        except Exception as e:
            errors.append((f"ia-meta:{ident}", type(e).__name__, str(e)))

    for scope, kind, msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")

    print(f"COUNT|discm_hits|{len(dm_hits)}")
    print(f"COUNT|ia_items|{len(ia_hits)}")
    print(f"COUNT|ia_candidate_files|{file_hits}")
    print(f"COUNT|errors|{len(errors)}")
    if dm_hits or ia_hits or file_hits:
        print("RESOLUTION|ADJACENT_TOKEN_PRESERVATION_CANDIDATE|verify exact Feb-2002 issue before payload recovery")
    elif errors:
        print("RESOLUTION|PARTIAL_TOKEN_SEARCH_FAILURE|retry failed index only")
    else:
        print("RESOLUTION|NO_ADJACENT_TOKEN_HIT|bound inferred GAMEWORLD200202 token on tested indexes")
    print(
        "EVIDENCE_BOUNDARY|GAMEWORLD200202 is inferred from the independently preserved January filename pattern; "
        "a zero result does not prove loss, and a hit would still require exact February-issue provenance."
    )


if __name__ == "__main__":
    main()
